#!/usr/bin/env python3
"""Static and structural validation for Agentic SDLC OS v2.2."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path("/home/oai/skills/skill-creator/scripts/quick_validate.py")
EXPECTED_SKILLS = {
    "agentic-sdlc-os", "pm-operating-system", "design-operating-system",
    "engineering-operating-system", "qa-operating-system",
    "release-operating-system", "evolution-operating-system",
}
REQUIRED_DOCS = {
    "README.md", "ARCHITECTURE.md", "SYSTEM_MAP.md", "INSTALL.md", "USAGE.md",
    "SKILLS_RANKINGS.md", "THIRD_PARTY_SKILLS.md", "COMPLETION_MATRIX.md",
    "CHANGELOG.md", "VALIDATION_PLAN.md", "VALIDATION_REPORT.md",
    "PRODUCTION_READINESS.md", "SECURITY_MODEL.md", "LICENSE",
}
REQUIRED_ASSETS = {
    "scripts/bootstrap_project.py", "scripts/tailor_process.py", "scripts/apply_domain_pack.py",
    "scripts/collect_evidence.py", "scripts/skill_governance.py", "scripts/cost_governance.py",
    "scripts/l5b_matched_experiment.py", "scripts/postgres_conformance.py",
    "scripts/control_plane.py", "scripts/sync_control_plane.py", "scripts/check_embedded_parity.py",
    "control_plane/agentic_sdlc_cp/api.py", "control_plane/migrations/001_initial_postgresql.sql",
    "docker-compose.yml", "manifest/process-tailoring.json", "manifest/skill-policy.json",
    "manifest/cost-policy.json", "manifest/skills.lock.json",
    "validation/l5b/PROTOCOL.md", "validation/l5b/synthetic-matched.json",
    "validation/l5b/synthetic-result.json", "validation/l5b/SYNTHETIC_SMOKE_REPORT.md",
    "validation/multi_project/scenarios.json", "validation/multi_project/REPORT.md",
    "validation/l5/REAL_PROJECT_DOGFOOD_REPORT.md",
}


def load_json(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload


def run(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def schema_validate(instance_path: Path, schema_path: Path) -> str | None:
    try:
        from jsonschema.validators import validator_for
        from referencing import Registry, Resource
        instance = load_json(instance_path); schema = load_json(schema_path)
        registry = Registry()
        evidence = schema_path.parent / "evidence.schema.json"
        if evidence.exists():
            registry = registry.with_resource(
                "https://example.local/agentic-sdlc/evidence.schema.json",
                Resource.from_contents(load_json(evidence)),
            )
        klass = validator_for(schema); klass.check_schema(schema)
        klass(schema, registry=registry).validate(instance)
        return None
    except Exception as exc:
        return str(exc)


def main() -> int:
    errors: list[str] = []
    for name in sorted(REQUIRED_DOCS):
        if not (ROOT / name).exists(): errors.append(f"missing doc: {name}")
    for name in sorted(REQUIRED_ASSETS):
        if not (ROOT / name).exists(): errors.append(f"missing asset: {name}")

    skill_dirs = {item.name for item in (ROOT / "skills").iterdir() if item.is_dir()}
    if skill_dirs != EXPECTED_SKILLS:
        errors.append(f"skill set mismatch: {sorted(skill_dirs)}")
    for name in sorted(EXPECTED_SKILLS):
        path = ROOT / "skills" / name
        ok, output = run([sys.executable, str(VALIDATOR), str(path)])
        print(f"[{name}] {'PASS' if ok else 'FAIL'}")
        if not ok: errors.append(f"skill validation {name}: {output}")
        if not (path / "agents" / "openai.yaml").exists(): errors.append(f"missing agent metadata: {name}")

    ok, output = run([sys.executable, "-m", "compileall", "-q", "scripts", "control_plane", "skills"])
    if not ok: errors.append("compileall: " + output)

    for path in sorted((ROOT / "manifest").rglob("*.json")) + sorted((ROOT / "domain-packs").rglob("*.json")):
        try: load_json(path)
        except Exception as exc: errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    for pack in sorted((ROOT / "domain-packs").glob("*/pack.json")):
        payload = load_json(pack)
        required = {"id", "name", "version", "keywords", "risk_adjustment", "required_controls", "required_artifacts", "required_evidence", "gate_overlays"}
        missing = required - set(payload)
        if missing: errors.append(f"domain pack {pack.parent.name} missing {sorted(missing)}")

    master = ROOT / "skills" / "agentic-sdlc-os"
    parity_files = [
        "bootstrap_project.py", "tailor_process.py", "apply_domain_pack.py", "collect_evidence.py",
        "skill_governance.py", "cost_governance.py", "l5b_matched_experiment.py",
        "sync_control_plane.py", "control_plane.py", "postgres_conformance.py",
    ]
    for name in parity_files:
        source = ROOT / "scripts" / name; target = master / "scripts" / name
        if not target.exists() or source.read_bytes() != target.read_bytes():
            errors.append(f"stale embedded script: {name}")
    for name in ["os-routing.json", "gates.json", "external-skills.json", "artifact-contracts.json"]:
        if (ROOT / "manifest" / name).read_bytes() != (master / "references" / "manifests" / name).read_bytes():
            errors.append(f"stale bundled manifest: {name}")
    for name in ["project-state.schema.json", "evidence.schema.json", "gate-result.schema.json", "handoff.schema.json"]:
        if (ROOT / "manifest" / "schemas" / name).read_bytes() != (master / "references" / "manifests" / name).read_bytes():
            errors.append(f"stale bundled schema: {name}")

    for source, target in [
        (ROOT / "manifest", master / "manifest"),
        (ROOT / "domain-packs", master / "domain-packs"),
        (ROOT / "control_plane", master / "control_plane"),
    ]:
        source_files = {p.relative_to(source) for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        target_files = {p.relative_to(target) for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        if source_files != target_files:
            errors.append(f"embedded tree mismatch: {source.name}")
        for rel in source_files & target_files:
            if (source / rel).read_bytes() != (target / rel).read_bytes():
                errors.append(f"stale embedded file: {source.name}/{rel}")

    example = ROOT / "examples" / "saas-mvp" / ".sdlc" / "state.json"
    pilot = ROOT / "validation" / "l5" / "pilots" / "venue-reservation" / ".sdlc" / "state.json"
    schema = ROOT / "manifest" / "schemas" / "project-state.schema.json"
    for path in [example, pilot]:
        issue = schema_validate(path, schema)
        if issue: errors.append(f"schema validation {path.relative_to(ROOT)}: {issue}")

    checks = [
        # Comprehensive root vs embedded-copy parity (sha256); supersedes the partial inline check above.
        [sys.executable, "scripts/check_embedded_parity.py", "--quiet"],
        [sys.executable, "scripts/skill_governance.py", "verify-lock", "--lock", "manifest/skills.lock.json"],
        [sys.executable, "scripts/l5b_matched_experiment.py", "validate", "validation/l5b/synthetic-matched.json", "--json"],
        [sys.executable, "scripts/postgres_conformance.py"],
    ]
    for command in checks:
        ok, output = run(command)
        if not ok: errors.append("command failed: " + " ".join(command) + " :: " + output)

    if errors:
        print("\nVALIDATION FAILED")
        for item in errors: print("-", item)
        return 1
    print("\nVALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
