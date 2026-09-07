#!/usr/bin/env python3
"""Evidence-backed maturity gate for Agentic SDLC OS release claims.

The gate re-opens and verifies signed/hashed evidence artifacts. It never trusts
summary booleans copied into the maturity evidence file for production-only controls.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "manifest" / "maturity-policy.json"
L5B_PATH = ROOT / "scripts" / "l5b_matched_experiment.py"
SOAK_PATH = ROOT / "scripts" / "soak_runner.py"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_artifact(base: Path, item: dict[str, Any], errors: list[str], label: str) -> Path | None:
    raw = item.get("artifact") or item.get("report_path") or item.get("experiment_path")
    expected = item.get("sha256")
    if not raw:
        errors.append(f"{label}: missing artifact path")
        return None
    path = Path(str(raw))
    if not path.is_absolute():
        path = (base / path).resolve()
    if not path.is_file():
        errors.append(f"{label}: artifact not found: {path}")
        return None
    if expected:
        actual = sha256(path)
        if actual != expected:
            errors.append(f"{label}: sha256 mismatch")
            return None
    else:
        errors.append(f"{label}: missing sha256")
        return None
    return path


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_json_report(path: Path | None, failures: list[str], label: str) -> dict[str, Any]:
    if path is None:
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("report root must be an object")
        return payload
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        failures.append(f"{label}: unreadable report: {exc}")
        return {}


def assess(evidence_path: Path, target: str) -> dict[str, Any]:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    requirements = policy["targets"][target]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    base = evidence_path.parent
    failures: list[str] = []
    checks: dict[str, Any] = {}

    projects = evidence.get("real_projects", [])
    checks["real_project_inputs"] = len(projects)
    executable = [item for item in projects if item.get("executable") is True and item.get("verified") is True]
    checks["executable_real_projects"] = len(executable)
    for index, item in enumerate(executable, 1):
        resolve_artifact(base, item, failures, f"real_project[{index}]")
    if len(projects) < int(requirements.get("minimum_real_project_inputs", 0)):
        failures.append("insufficient real project inputs")
    if len(executable) < int(requirements.get("minimum_executable_real_projects", 0)):
        failures.append("insufficient independently verified executable real projects")

    if requirements.get("require_control_regression"):
        regression = evidence.get("control_regression", {})
        checks["control_regression"] = regression.get("passed") is True
        if regression.get("passed") is not True:
            failures.append("control regression is not passing")
        elif regression.get("artifact") or regression.get("report_path"):
            resolve_artifact(base, regression, failures, "control_regression")

    if requirements.get("require_external_skill_supply_chain"):
        item = evidence.get("skill_supply_chain", {})
        path = resolve_artifact(base, item, failures, "skill_supply_chain")
        report = load_json_report(path, failures, "skill_supply_chain")
        checks["skill_supply_chain"] = report
        if report.get("passed") is not True or report.get("strict_external_install_ready") is not True:
            failures.append("external Skill supply chain is not formally locked and install-ready")
        if report.get("formal") is not True:
            failures.append("external Skill supply chain evidence is not formal")
        if int(report.get("blocked_entries", 1)) != 0:
            failures.append("external Skill supply chain has blocked units")

    if requirements.get("require_real_l5b"):
        l5b_item = evidence.get("l5b", {})
        experiment_path = resolve_artifact(base, l5b_item, failures, "l5b")
        l5b_result: dict[str, Any] = {}
        if experiment_path:
            module = load_module("maturity_l5b", L5B_PATH)
            experiment = module.load(experiment_path)
            structural = module.validate(experiment)
            if structural:
                failures.append("l5b structural validation failed: " + "; ".join(structural))
            else:
                l5b_result = module.analyze(experiment)
                if l5b_result.get("synthetic"):
                    failures.append("l5b is synthetic")
                if l5b_result.get("complete_pairs", 0) < int(requirements.get("minimum_l5b_pairs", 0)):
                    failures.append("l5b pair count below policy")
                if requirements.get("require_l5b_sealed") and not l5b_result.get("sealed"):
                    failures.append("l5b is not sealed")
                if requirements.get("require_l5b_positive") and l5b_result.get("decision") != "positive":
                    failures.append(f"l5b decision is {l5b_result.get('decision')}, not positive")
                if not l5b_result.get("formal_evidence_eligible"):
                    failures.append("l5b is not formal-evidence eligible")
        checks["l5b"] = l5b_result

    if requirements.get("require_live_postgresql"):
        item = evidence.get("postgresql", {})
        path = resolve_artifact(base, item, failures, "postgresql")
        report = load_json_report(path, failures, "postgresql")
        checks["postgresql"] = report
        if report.get("passed") is not True or report.get("live_postgresql") is not True or report.get("database") != "postgresql":
            failures.append("live PostgreSQL validation missing or failed")
        pg_fields = {
            "require_postgresql_concurrency_stress": ("concurrency_stress", "PostgreSQL concurrency stress not verified"),
            "require_postgresql_recovery_drill": ("recovery_drill", "PostgreSQL recovery drill not verified"),
            "require_postgresql_dead_letter_drill": ("dead_letter_drill", "PostgreSQL dead-letter recovery not verified"),
            "require_postgresql_connection_fault_drill": ("connection_fault_drill", "PostgreSQL connection-loss recovery not verified"),
        }
        for policy_key, (field, message) in pg_fields.items():
            if requirements.get(policy_key) and report.get(field) is not True:
                failures.append(message)

    if int(requirements.get("minimum_soak_days", 0)):
        item = evidence.get("soak", {})
        path = resolve_artifact(base, item, failures, "soak")
        soak_result: dict[str, Any] = {}
        if path:
            try:
                module = load_module("maturity_soak", SOAK_PATH)
                state = module.load(path)
                soak_result = module.assess_state(state)
            except Exception as exc:
                failures.append(f"soak: validation failed: {exc}")
        checks["soak"] = soak_result
        if soak_result.get("formal_evidence_eligible") is not True:
            failures.append("production soak is not formal-evidence eligible")
        if int(soak_result.get("observation_days", 0)) < int(requirements["minimum_soak_days"]):
            failures.append("production soak duration below policy")
        if float(soak_result.get("elapsed_days", 0)) < float(requirements["minimum_soak_days"]):
            failures.append("production soak wall-clock duration below policy")
        if int(soak_result.get("p0_incidents", 999)) > int(requirements.get("maximum_soak_p0", 0)):
            failures.append("production soak has P0 incidents")
        if int(soak_result.get("p1_control_plane_incidents", 999)) > int(requirements.get("maximum_soak_p1", 0)):
            failures.append("production soak has P1 control-plane incidents")

    drill_fields = {
        "require_rbac_drill": "rbac",
        "require_secret_rotation_drill": "secret_rotation",
        "require_backup_restore_drill": "backup_restore",
        "require_audit_export_drill": "audit_export",
    }
    if any(requirements.get(key) for key in drill_fields):
        item = evidence.get("organization_drills", {})
        path = resolve_artifact(base, item, failures, "organization_drills")
        report = load_json_report(path, failures, "organization_drills")
        checks["organization_drills"] = report
        if report.get("passed") is not True:
            failures.append("organization drills did not pass")
        if requirements.get("require_formal_organization_drills") and report.get("formal_evidence_eligible") is not True:
            failures.append("organization drills are not formal-evidence eligible")
        for policy_key, field in drill_fields.items():
            if requirements.get(policy_key) and report.get(field) is not True:
                failures.append(f"organization drill missing: {field}")

    failures = list(dict.fromkeys(failures))
    return {
        "target": target,
        "passed": not failures,
        "claim_allowed": target if not failures else None,
        "failures": failures,
        "checks": checks,
        "policy_version": policy["version"],
    }


def template() -> dict[str, Any]:
    return {
        "real_projects": [],
        "control_regression": {"passed": False, "artifact": "", "sha256": ""},
        "skill_supply_chain": {"artifact": "", "sha256": ""},
        "l5b": {"experiment_path": "", "sha256": ""},
        "postgresql": {"artifact": "", "sha256": ""},
        "soak": {"artifact": "", "sha256": ""},
        "organization_drills": {"artifact": "", "sha256": ""},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evidence-backed Agentic SDLC OS maturity gate")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("template"); p.add_argument("--output")
    p = sub.add_parser("assess"); p.add_argument("evidence"); p.add_argument("--target", choices=["beta-candidate", "production-candidate"], default="production-candidate"); p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "template":
        payload = template()
        if args.output:
            Path(args.output).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2)); return 0
    try:
        result = assess(Path(args.evidence).resolve(), args.target)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, RuntimeError) as exc:
        result = {"target": args.target, "passed": False, "claim_allowed": None, "failures": [str(exc)]}
    print(json.dumps(result, indent=2) if args.json else ("PASS" if result["passed"] else "BLOCKED\n- " + "\n- ".join(result["failures"])))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
