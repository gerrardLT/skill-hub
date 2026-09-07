#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module); return module


supply = load("v25_red_supply", ROOT / "scripts" / "skill_supply_chain.py")
soak = load("v25_red_soak", ROOT / "scripts" / "soak_runner.py")
pg = load("v25_red_pg", ROOT / "scripts" / "postgres_live_validation.py")


def record(case: str, passed: bool, expected: str, observed: Any, severity: str = "P0") -> dict[str, Any]:
    return {"case": case, "severity": severity, "control_passed": passed, "expected": expected, "observed": observed}


def repo_evidence(root: Path, *, license_text: str, skill_text: str, commit: str = "a"*40) -> tuple[Path, dict[str, Any]]:
    repo = root / "repo"; skill = repo / "impeccable"; skill.mkdir(parents=True)
    (repo / "LICENSE").write_text(license_text, encoding="utf-8")
    (skill / "SKILL.md").write_text(skill_text, encoding="utf-8")
    evidence = supply.build_template(); evidence["formal"] = True
    item = next(x for x in evidence["repositories"] if x["repo"] == "pbakaus/impeccable")
    item.update({"commit_sha": commit, "snapshot_path": str(repo), "snapshot_sha256": supply.tree_hash(repo), "license_id": "MIT"})
    path = root / "evidence.json"; path.write_text(json.dumps(evidence), encoding="utf-8")
    return path, evidence


def selected_unit(report: dict[str, Any]) -> dict[str, Any]:
    return next(x for x in report["unit_reports"] if x["repo"] == "pbakaus/impeccable" and x["skill"] == "impeccable")


def main() -> int:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="sdlc-v25-red-") as temp:
        base = Path(temp)
        mit = "Permission is hereby granted, free of charge\nTHE SOFTWARE IS PROVIDED \"AS IS\"\n"
        good = "---\nname: impeccable\ndescription: design\n---\nUse safe design methods.\n"

        path, evidence = repo_evidence(base / "mutable", license_text=mit, skill_text=good, commit="main")
        report = supply.audit(path); unit = selected_unit(report)
        results.append(record("external_skill_requires_immutable_commit", not unit["install_allowed"] and any("40-char" in x for x in unit["failures"]), "Mutable refs/branch names must never unlock third-party Skill installation.", unit["failures"]))

        unknown_root = base / "unknown"; repo = unknown_root / "repo"; skill=repo/"impeccable"; skill.mkdir(parents=True)
        (repo/"LICENSE").write_text("Proprietary custom terms", encoding="utf-8"); (skill/"SKILL.md").write_text(good, encoding="utf-8")
        evidence=supply.build_template(); evidence["formal"]=True; item=next(x for x in evidence["repositories"] if x["repo"]=="pbakaus/impeccable")
        item.update({"commit_sha":"b"*40,"snapshot_path":str(repo),"snapshot_sha256":supply.tree_hash(repo),"license_id":"unknown"}); ep=unknown_root/"evidence.json"; ep.write_text(json.dumps(evidence)); unit=selected_unit(supply.audit(ep))
        results.append(record("unknown_or_disallowed_license_is_blocked", not unit["install_allowed"] and any("license not allowed" in x for x in unit["failures"]), "Unapproved licenses must fail closed.", unit["failures"]))

        broken = good + "\n[missing](references/DOES_NOT_EXIST.md)\n"
        path,_=repo_evidence(base/"broken",license_text=mit,skill_text=broken); unit=selected_unit(supply.audit(path))
        results.append(record("broken_skill_resource_link_is_blocked", not unit["install_allowed"] and any("broken local resource" in x for x in unit["failures"]), "A Skill with missing local resources must not be installable.", unit["failures"]))

        start=datetime(2026,8,1,tzinfo=timezone.utc); state=soak.new_state(system_version="2.5.0",target_days=3,synthetic=True,started_at=start)
        for i in range(4): soak.add_observation(state,at=start+timedelta(days=i),health_pass=True,audit_pass=True,stress_pass=True,availability=1.0)
        soak.seal(state); assessment=soak.assess_state(state)
        results.append(record("synthetic_30day_soak_never_counts_as_formal", assessment["sealed"] and not assessment["formal_evidence_eligible"], "Backdated/synthetic soak may test the harness but must never count toward maturity.", assessment))

        tamper=soak.new_state(system_version="2.5.0",target_days=1,synthetic=True,started_at=start); soak.add_observation(tamper,at=start+timedelta(days=1),health_pass=True,audit_pass=True,stress_pass=True,availability=1.0); tamper["observations"][0]["availability"]=0.0; t=soak.assess_state(tamper)
        results.append(record("soak_hash_chain_detects_tampering", not t["chain_valid"], "Post-hoc modification of soak observations must invalidate the chain.", t["failures"]))

        pg_report=pg.validate(f"sqlite+pysqlite:///{base/'fake-pg.db'}",jobs=5,workers=2,updates=2,connection_fault=True)
        results.append(record("sqlite_cannot_masquerade_as_live_postgresql", pg_report.get("passed") is False and pg_report.get("live_postgresql") is False, "Production PostgreSQL evidence must come from a PostgreSQL dialect/server.", pg_report))

        org_path=base/"org.json"; proc=subprocess.run([sys.executable,str(ROOT/"scripts"/"organization_drills.py"),"--output",str(org_path)],capture_output=True,text=True); org=json.loads(org_path.read_text()) if org_path.exists() else {}
        results.append(record("local_org_drill_cannot_unlock_formal_maturity", proc.returncode==0 and org.get("passed") is True and org.get("formal_evidence_eligible") is False, "Local SQLite/RBAC/secret mechanics can pass without becoming organization-grade evidence.", org))

        cfg_proc=subprocess.run([sys.executable,str(ROOT/"scripts"/"l5b_formal_runner.py"),"template"],capture_output=True,text=True)
        template=json.loads(cfg_proc.stdout)
        results.append(record("formal_l5b_defaults_to_no_context_attestation", cfg_proc.returncode==0 and template.get("formal_context_attestation") is False and template.get("synthetic") is False, "A formal experiment template must default to blocked until independent contexts are externally attested.", {"formal_context_attestation":template.get("formal_context_attestation"),"synthetic":template.get("synthetic")}))

    passed=sum(1 for x in results if x["control_passed"])
    output={"system_version":"2.5.0","scope":"supply-chain-l5b-postgres-soak-organization-claim-safety","summary":{"cases":len(results),"passed":passed,"failed":len(results)-passed,"all_controls_passed":passed==len(results)},"results":results}
    path=ROOT/"validation"/"v25_red_team_results.json"; path.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2)); return 0 if passed==len(results) else 2


if __name__ == "__main__": raise SystemExit(main())
