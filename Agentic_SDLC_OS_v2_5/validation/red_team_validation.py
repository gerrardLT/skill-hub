#!/usr/bin/env python3
"""Adversarial regression suite for Agentic SDLC OS v2.0.

This complements unittest coverage with black-box CLI attacks and writes a
machine-readable report to validation/red_team_results.json.
"""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"
GATES = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
ROUTING = json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))


def load_cli_module():
    spec = importlib.util.spec_from_file_location("agentic_sdlc_cli", CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load SDLC CLI module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SDLC = load_cli_module()


def run(args: list[str]) -> SimpleNamespace:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        returncode = int(SDLC.main(args))
    return SimpleNamespace(returncode=returncode, stdout=stdout.getvalue(), stderr=stderr.getvalue())


def run_process(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(CLI), *args], text=True, capture_output=True, timeout=30)


def init(root: Path, project_type: str = "greenfield") -> None:
    cp = run(["init", str(root), "--name", "red-team", "--type", project_type, "--criticality", "medium"])
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr or cp.stdout)


def state(root: Path) -> dict[str, Any]:
    return json.loads((root / ".sdlc" / "state.json").read_text(encoding="utf-8"))


def add_artifact(root: Path, artifact_id: str, artifact_type: str, content: str | None = None) -> subprocess.CompletedProcess[str]:
    path = root / "docs" / f"{artifact_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        contract = SDLC.artifact_contract(artifact_type)
        lines = [f"# {artifact_type}", ""]
        for index, group in enumerate(contract.get("required_section_groups", []), 1):
            heading = str(group[0]).title()
            lines.extend([
                f"## {heading}", "",
                (
                    f"Verified source EV-{index} records a concrete {heading.lower()} decision. "
                    f"Owner red-team-reviewer must validate at least {index + 2} measurable cases, "
                    "link ticket RT-100, record risks, and reject the change if the threshold fails."
                ),
                "",
            ])
        minimum = int(contract.get("minimum_substantive_chars", 220))
        while SDLC.substantive_chars("\n".join(lines)) < minimum + 40:
            lines.extend([
                "Source EV-extra and requirement RT-100 provide additional verified evidence and ownership.",
                "",
            ])
        body = "\n".join(lines)
    else:
        body = content
    path.write_text(body, encoding="utf-8")
    return run([
        "add-artifact", str(root), "--id", artifact_id, "--type", artifact_type,
        "--path", str(path), "--status", "accepted", "--owner", "red-team",
        "--verified-by", "red-team-reviewer",
    ])


def prepare_gate(root: Path, gate_name: str, *, traces: bool = True, duplicate_evidence: bool = False) -> list[str]:
    project = state(root)["project"]
    spec = SDLC.resolve_gate_spec(GATES[gate_name], project.get("profile", "standard"), project.get("criticality", "medium"))
    ids_by_type: dict[str, str] = {}
    for index, artifact_type in enumerate(spec["required"]):
        artifact_id = f"a-{index}"
        cp = add_artifact(root, artifact_id, artifact_type)
        if cp.returncode != 0:
            raise RuntimeError(cp.stderr or cp.stdout)
        ids_by_type[artifact_type] = artifact_id
    ids = list(ids_by_type.values())
    if traces:
        seen: set[tuple[str, str, str]] = set()
        touched: set[str] = set()
        counter = 0
        for trace_path in spec.get("trace_paths", []):
            for source_type, target_type in zip(trace_path, trace_path[1:]):
                source, target = ids_by_type[source_type], ids_by_type[target_type]
                signature = (source, "derives", target)
                if signature in seen:
                    continue
                seen.add(signature)
                touched.update([source, target])
                cp = run([
                    "trace", str(root), "--id", f"t-{counter}", "--from", source,
                    "--to", target, "--relation", "derives",
                ])
                if cp.returncode != 0:
                    raise RuntimeError(cp.stderr or cp.stdout)
                counter += 1
        for artifact_id in ids:
            if artifact_id in touched:
                continue
            cp = run([
                "trace", str(root), "--id", f"t-{counter}", "--from", artifact_id,
                "--to", f"goal:{gate_name}", "--relation", "supports",
            ])
            if cp.returncode != 0:
                raise RuntimeError(cp.stderr or cp.stdout)
            counter += 1
    total = max(
        int(spec.get("minimum_evidence", 0)),
        int(spec.get("minimum_distinct_sources", 0)),
        int(spec.get("minimum_evidence_targets", 0)),
    )
    high = int(spec.get("minimum_high_quality_evidence", 0))
    for index in range(total):
        if duplicate_evidence:
            claim = "same duplicated claim"
            source = "same-source"
            supports = ids[0]
        else:
            claim = f"independent observation {index}"
            source = f"source-{index}"
            supports = ids[index % len(ids)]
        cp = run([
            "add-evidence", str(root), "--id", f"e-{index}", "--claim", claim,
            "--source", source, "--source-type", "test",
            "--quality", "high" if index < high else "medium", "--supports", supports,
            "--method", "black-box regression fixture",
        ])
        if cp.returncode != 0:
            raise RuntimeError(cp.stderr or cp.stdout)
    return ids


def record(name: str, passed: bool, observed: Any, expected: str, severity: str = "P0") -> dict[str, Any]:
    return {
        "case": name,
        "severity": severity,
        "control_passed": bool(passed),
        "expected": expected,
        "observed": observed,
    }


def main() -> int:
    results: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cp = run(["transition", str(root), "--to-stage", "HANDOFF", "--reason", "skip"])
        results.append(record(
            "stage_skip_blocked", cp.returncode != 0 and state(root)["current_stage"] == "INTAKE",
            {"returncode": cp.returncode, "stage": state(root)["current_stage"], "stderr": cp.stderr.strip()},
            "Direct INTAKE -> HANDOFF is rejected without approved force.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        missing = root / "missing.md"
        cp = run([
            "add-artifact", str(root), "--id", "missing", "--type", "product-brief",
            "--path", str(missing), "--status", "accepted",
        ])
        results.append(record(
            "missing_artifact_rejected", cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "A missing local artifact cannot be accepted.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cp = add_artifact(root, "empty", "product-brief", "")
        results.append(record(
            "empty_artifact_rejected", cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "An empty artifact cannot be accepted.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        prepare_gate(root, "pm-ready", duplicate_evidence=True)
        cp = run(["gate", str(root), "--name", "pm-ready", "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "duplicate_evidence_excluded", cp.returncode != 0 and payload["evidence_count"] == 1,
            {"returncode": cp.returncode, "status": payload["status"], "evidence_count": payload["evidence_count"],
             "duplicates": len(payload.get("duplicate_evidence", []))},
            "Repeated evidence cannot satisfy minimum evidence or source diversity.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cfg_path = root / ".sdlc" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["allow_waiver"] = False
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        cp = run([
            "gate", str(root), "--name", "pm-ready", "--waive", "--reason", "fast",
            "--approver", "Alice Chen", "--approval-id", "CR-1",
            "--compensating-control", "manual review", "--expires", "2099-01-01T00:00:00Z",
        ])
        results.append(record(
            "waiver_policy_enforced", cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "Project configuration can disable all gate waivers.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cp = run([
            "gate", str(root), "--name", "pm-ready", "--waive", "--reason", "fast",
            "--approver", "ChatGPT Agent", "--approval-id", "CR-2",
            "--compensating-control", "manual review", "--expires", "2099-01-01T00:00:00Z",
        ])
        results.append(record(
            "nonhuman_waiver_rejected", cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "An AI or automation identity cannot approve a waiver.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cp = run([
            "gate", str(root), "--name", "pm-ready", "--waive", "--reason", "fast",
            "--approver", "Alice Chen", "--approval-id", "CR-3",
            "--compensating-control", "manual review",
        ])
        results.append(record(
            "unbounded_waiver_rejected", cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "A waiver requires an explicit future expiry.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        state_path = root / ".sdlc" / "state.json"
        payload = state(root)
        payload["status"] = "nonsense"
        state_path.write_text(json.dumps(payload), encoding="utf-8")
        cp = run(["validate", str(root), "--json"])
        report = json.loads(cp.stdout)
        results.append(record(
            "state_corruption_detected", cp.returncode != 0 and not report["valid"],
            {"returncode": cp.returncode, "errors": report["errors"]},
            "Invalid state values are detected before further workflow execution.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        base = Path(td)
        root = base / "project"
        init(root)
        escape = base / "escape.md"
        cp = run([
            "new-artifact", str(root), "--id", "escape", "--type", "prd",
            "--filename", "../../escape.md",
        ])
        results.append(record(
            "artifact_path_escape_rejected", cp.returncode != 0 and not escape.exists(),
            {"returncode": cp.returncode, "escaped_file_exists": escape.exists(), "stderr": cp.stderr.strip()},
            "Artifact creation cannot escape .sdlc/artifacts.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        ids = prepare_gate(root, "pm-ready")
        before = run(["gate", str(root), "--name", "pm-ready", "--json"])
        artifact_path = root / state(root)["artifacts"][ids[0]]["path"]
        artifact_path.write_text(artifact_path.read_text(encoding="utf-8") + "\nchanged after approval\n", encoding="utf-8")
        after = run(["gate", str(root), "--name", "pm-ready", "--json"])
        after_payload = json.loads(after.stdout)
        issues = [issue for item in after_payload.get("invalid_artifacts", []) for issue in item.get("issues", [])]
        results.append(record(
            "artifact_tampering_detected", before.returncode == 0 and after.returncode != 0 and "content_changed_since_acceptance" in issues,
            {"before": before.returncode, "after": after.returncode, "issues": issues},
            "Changing accepted content invalidates its gate binding.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        count = 12

        def add(index: int) -> int:
            cp = run_process([
                "add-evidence", str(root), "--id", f"c-{index}", "--claim", f"claim {index}",
                "--source", f"source-{index}", "--source-type", "test", "--quality", "medium",
            ])
            return cp.returncode

        with ThreadPoolExecutor(max_workers=6) as pool:
            codes = list(pool.map(add, range(count)))
        present = len(state(root).get("evidence", []))
        results.append(record(
            "concurrent_updates_serialized", all(code == 0 for code in codes) and present == count,
            {"successful_commands": sum(code == 0 for code in codes), "records_present": present},
            "Concurrent agents do not silently lose successful state updates.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        add = run([
            "add-risk", str(root), "--id", "r-1", "--title", "data loss",
            "--severity", "critical", "--status", "open", "--mitigation", "backup",
        ])
        update = run([
            "update-risk", str(root), "--id", "r-1", "--status", "closed",
            "--mitigation", "restored and verified", "--owner", "Alice Chen",
        ])
        risk = next(item for item in state(root)["risks"] if item["id"] == "r-1")
        results.append(record(
            "risk_lifecycle_is_mutable", add.returncode == 0 and update.returncode == 0 and risk["status"] == "closed",
            {"add": add.returncode, "update": update.returncode, "risk": risk},
            "A risk can be updated or closed without creating duplicate ledger IDs.",
            severity="P1",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        prepare_gate(root, "pm-ready", traces=False)
        cp = run(["gate", str(root), "--name", "pm-ready", "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "gate_requires_trace_coverage", cp.returncode != 0 and payload["trace_coverage"] < payload["minimum_trace_coverage"],
            {"returncode": cp.returncode, "status": payload["status"], "coverage": payload["trace_coverage"]},
            "Gate passage requires configured traceability coverage.",
            severity="P1",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        prepare_gate(root, "pm-ready", traces=False)
        project_state = state(root)
        for index, artifact_id in enumerate(project_state["artifacts"]):
            cp = run([
                "trace", str(root), "--id", f"spoof-{index}", "--from", artifact_id,
                "--to", "goal:pm-ready", "--relation", "supports",
            ])
            if cp.returncode != 0:
                raise RuntimeError(cp.stderr or cp.stdout)
        cp = run(["gate", str(root), "--name", "pm-ready", "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "arbitrary_trace_spoof_blocked",
            cp.returncode != 0 and payload["trace_coverage"] == 1.0 and payload["trace_path_coverage"] < payload["minimum_trace_path_coverage"],
            {"returncode": cp.returncode, "artifact_coverage": payload["trace_coverage"], "path_coverage": payload["trace_path_coverage"]},
            "Arbitrary links cannot substitute for required directed lifecycle paths.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cp_invalid = run([
            "trace", str(root), "--from", "invented-node", "--to", "goal:x", "--relation", "supports",
        ])
        cp_relation = run([
            "trace", str(root), "--from", "goal:x", "--to", "goal:y", "--relation", "pretends",
        ])
        results.append(record(
            "trace_schema_enforced",
            cp_invalid.returncode != 0 and cp_relation.returncode != 0,
            {"invalid_endpoint": cp_invalid.stderr.strip(), "invalid_relation": cp_relation.stderr.strip()},
            "Trace endpoints and relation vocabulary are validated at write time.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        audit_path = root / ".sdlc" / "audit" / "events.jsonl"
        lines = audit_path.read_text(encoding="utf-8").splitlines()
        event = json.loads(lines[0])
        event["actor"] = "tampered-actor"
        lines[0] = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        cp = run(["audit", str(root), "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "audit_hash_chain_detects_tampering",
            cp.returncode != 0 and not payload["valid"],
            {"returncode": cp.returncode, "errors": payload["errors"]},
            "Changing a historical audit event invalidates the append-only hash chain.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        cp = run([
            "init", str(root), "--name", "unsafe-lite", "--criticality", "high", "--profile", "lite",
        ])
        results.append(record(
            "high_criticality_lite_profile_blocked",
            cp.returncode != 0,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "High-criticality projects cannot silently downgrade to the lite process.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        run([
            "add-risk", str(root), "--id", "critical-health", "--title", "irreversible loss",
            "--severity", "critical", "--mitigation", "stop deployment",
        ])
        cp = run(["health", str(root), "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "health_score_cannot_average_away_critical_risk",
            cp.returncode != 0 and payload["score"] <= 49 and "open-critical-risk" in payload["hard_fails"],
            {"returncode": cp.returncode, "score": payload["score"], "hard_fails": payload["hard_fails"]},
            "A critical risk is a non-compensable health threshold failure.",
            severity="P1",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        repeated = "This section will be completed as appropriate by relevant stakeholders."
        hollow = (
            "# Hollow\n\n"
            "## Objective\n\n" + repeated + "\n\n"
            "## Evidence\n\n" + repeated + "\n\n"
            "## Risks\n\n" + repeated + "\n\n"
            "## Acceptance Criteria\n\n" + repeated + "\n\n"
            "## Traceability\n\n" + repeated + "\n"
        )
        cp = add_artifact(root, "hollow", "generic-spec", hollow)
        results.append(record(
            "hollow_structural_shell_rejected",
            cp.returncode != 0 and any(
                marker in cp.stderr for marker in [
                    "insufficient_concrete_signals", "repetitive_section_content", "excessive_vague_language"
                ]
            ),
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "Headings and length alone cannot make vague repetitive content acceptable.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        cp_init = run([
            "init", str(root), "--name", "high-assurance", "--criticality", "medium",
            "--profile", "high-assurance",
        ])
        if cp_init.returncode != 0:
            raise RuntimeError(cp_init.stderr or cp_init.stdout)
        seed = add_artifact(root, "seed", "product-brief")
        if seed.returncode != 0:
            raise RuntimeError(seed.stderr or seed.stdout)
        path = root / state(root)["artifacts"]["seed"]["path"]
        cp = run([
            "add-artifact", str(root), "--id", "self-verified", "--type", "product-brief",
            "--path", str(path), "--status", "accepted", "--owner", "Alice Chen",
            "--verified-by", "Alice Chen",
        ])
        results.append(record(
            "self_verification_blocked_in_high_assurance",
            cp.returncode != 0 and "cannot independently verify" in cp.stderr,
            {"returncode": cp.returncode, "stderr": cp.stderr.strip()},
            "High-assurance artifacts require a verifier independent from the owner.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        if add_artifact(root, "upstream", "product-brief").returncode != 0:
            raise RuntimeError("Could not create upstream fixture")
        if add_artifact(root, "downstream", "prd").returncode != 0:
            raise RuntimeError("Could not create downstream fixture")
        run([
            "trace", str(root), "--id", "upstream-downstream", "--from", "upstream",
            "--to", "downstream", "--relation", "derives",
        ])
        upstream_path = root / state(root)["artifacts"]["upstream"]["path"]
        upstream_path.write_text(
            upstream_path.read_text(encoding="utf-8")
            + "\n## Change Record\n\nDecision CR-130 must validate 25 users before release.\n",
            encoding="utf-8",
        )
        cp = run([
            "add-artifact", str(root), "--id", "upstream", "--type", "product-brief",
            "--path", str(upstream_path), "--status", "accepted", "--owner", "red-team",
            "--verified-by", "red-team-reviewer",
        ])
        downstream = state(root)["artifacts"]["downstream"]
        results.append(record(
            "accepted_upstream_change_stales_downstream",
            cp.returncode == 0 and downstream.get("stale") is True and "upstream" in downstream.get("stale_from", []),
            {"returncode": cp.returncode, "downstream": downstream},
            "Changing an accepted upstream artifact invalidates accepted downstream derivatives.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        ids = prepare_gate(root, "pm-ready")
        before = run(["gate", str(root), "--name", "pm-ready", "--json"])
        brief = next(
            artifact_id for artifact_id in ids
            if state(root)["artifacts"][artifact_id]["type"] == "product-brief"
        )
        extra = add_artifact(root, "unlisted-upstream", "generic-spec")
        if extra.returncode != 0:
            raise RuntimeError(extra.stderr or extra.stdout)
        run([
            "trace", str(root), "--id", "unlisted-brief", "--from", "unlisted-upstream",
            "--to", brief, "--relation", "derives",
        ])
        extra_path = root / state(root)["artifacts"]["unlisted-upstream"]["path"]
        extra_path.write_text(extra_path.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        after = run(["gate", str(root), "--name", "pm-ready", "--json"])
        payload = json.loads(after.stdout)
        invalid = {item["id"]: item for item in payload.get("invalid_artifacts", [])}
        results.append(record(
            "unlisted_upstream_drift_propagates_to_gate",
            before.returncode == 0 and after.returncode != 0 and brief in invalid
            and any("upstream_artifact_invalid" in issue for issue in invalid[brief].get("issues", [])),
            {"before": before.returncode, "after": after.returncode, "invalid": invalid.get(brief)},
            "A changed upstream dependency cannot hide merely because it is not directly listed by the gate.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        add_artifact(root, "reconcile-source", "product-brief")
        add_artifact(root, "reconcile-target", "prd")
        run([
            "trace", str(root), "--id", "reconcile-edge", "--from", "reconcile-source",
            "--to", "reconcile-target", "--relation", "derives",
        ])
        path = root / state(root)["artifacts"]["reconcile-source"]["path"]
        path.write_text(path.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        cp = run(["reconcile", str(root), "--apply", "--json"])
        project_state = state(root)
        results.append(record(
            "reconcile_persists_transitive_staleness",
            cp.returncode != 0
            and project_state["artifacts"]["reconcile-source"].get("stale") is True
            and project_state["artifacts"]["reconcile-target"].get("stale") is True,
            {"returncode": cp.returncode, "source": project_state["artifacts"]["reconcile-source"],
             "target": project_state["artifacts"]["reconcile-target"]},
            "Reconciliation persists both direct drift and transitive downstream staleness.",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        cfg_path = root / ".sdlc" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["cost_budget_usd"] = 0.01
        cfg["token_budget"] = 100
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        run([
            "record-run", str(root), "--id", "costly-run", "--actor", "agent-a", "--os", "engineering",
            "--skill", "implementation", "--model", "model-x", "--outcome", "success",
            "--tokens-input", "150", "--tokens-output", "50", "--tool-calls", "4", "--cost-usd", "0.02",
        ])
        cp = run(["metrics", str(root), "--json"])
        payload = json.loads(cp.stdout)
        results.append(record(
            "agent_cost_and_token_budget_exposure",
            cp.returncode == 0 and len(payload.get("warnings", [])) == 2,
            {"returncode": cp.returncode, "metrics": payload},
            "Agent runs expose cost and token budget overruns instead of hiding execution cost.",
            severity="P1",
        ))

    with tempfile.TemporaryDirectory(prefix="sdlc-red-team-") as td:
        root = Path(td) / "project"
        init(root)
        ids = prepare_gate(root, "pm-ready")
        project_state = state(root)
        project_state["evidence"] = []
        (root / ".sdlc" / "state.json").write_text(
            json.dumps(project_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        brief = next(
            artifact_id for artifact_id in ids
            if state(root)["artifacts"][artifact_id]["type"] == "product-brief"
        )
        add_artifact(root, "waiver-upstream", "generic-spec")
        run([
            "trace", str(root), "--id", "waiver-upstream-brief", "--from", "waiver-upstream",
            "--to", brief, "--relation", "derives",
        ])
        expires = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        waived = run([
            "gate", str(root), "--name", "pm-ready", "--waive", "--reason", "timeboxed prototype",
            "--approver", "Alice Chen", "--approval-id", "CR-130", "--compensating-control", "manual review",
            "--expires", expires, "--json",
        ])
        path = root / state(root)["artifacts"]["waiver-upstream"]["path"]
        path.write_text(path.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")
        allowed, current = SDLC.gate_allows_transition(state(root), "pm-ready", root)
        results.append(record(
            "upstream_drift_invalidates_existing_waiver",
            waived.returncode == 0 and not allowed and current.get("status") == "fail",
            {"waiver_returncode": waived.returncode, "allowed_after_drift": allowed, "current": current},
            "A waiver is bound to current upstream integrity and cannot survive dependency drift.",
        ))

    holdout = json.loads((ROOT / "validation" / "benchmarks" / "router-holdout.json").read_text(encoding="utf-8"))
    route_state = {
        "current_os": "engineering",
        "os_states": {name: {"stage": stages[0]} for name, stages in ROUTING["os_stages"].items()},
    }
    auto_routes = 0
    correct_routes = 0
    unsafe_routes: list[dict[str, str]] = []
    for item in holdout:
        outcome = SDLC.route_task(route_state, item["task"])
        if outcome["decision"] == "route":
            auto_routes += 1
            if outcome["recommended_os"] == item["expected_os"]:
                correct_routes += 1
            else:
                unsafe_routes.append({
                    "expected": item["expected_os"],
                    "actual": str(outcome["recommended_os"]),
                    "task": item["task"],
                })
    coverage = auto_routes / len(holdout)
    precision = correct_routes / auto_routes if auto_routes else None
    results.append(record(
        "low_confidence_router_abstains_safely", not unsafe_routes,
        {"cases": len(holdout), "auto_routes": auto_routes, "coverage": coverage,
         "precision": precision, "unsafe_routes": unsafe_routes},
        "The deterministic router must abstain instead of silently routing an unseen paraphrase to the wrong OS.",
        severity="P1",
    ))

    ambiguous = json.loads((ROOT / "validation" / "benchmarks" / "router-ambiguous.json").read_text(encoding="utf-8"))
    unexpected = []
    for item in ambiguous:
        outcome = SDLC.route_task(route_state, item["task"])
        if outcome["decision"] != "abstain":
            unexpected.append({"task": item["task"], "actual": outcome["recommended_os"]})
    results.append(record(
        "ambiguous_router_never_silently_advances",
        not unexpected,
        {"cases": len(ambiguous), "unexpected_auto_routes": unexpected},
        "Ambiguous or underspecified tasks are returned for semantic/human clarification.",
        severity="P1",
    ))

    failed = [item for item in results if not item["control_passed"]]
    report = {
        "system_version": SDLC.VERSION,
        "summary": {
            "cases": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "all_controls_passed": not failed,
        },
        "results": results,
    }
    output = ROOT / "validation" / "red_team_results.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
