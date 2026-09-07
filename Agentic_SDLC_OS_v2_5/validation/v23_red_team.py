#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


l5b = load("v23_red_l5b", ROOT / "scripts" / "l5b_matched_experiment.py")
maturity = load("v23_red_maturity", ROOT / "scripts" / "maturity_gate.py")


def record(case: str, passed: bool, expected: str, observed: Any, severity: str = "P0") -> dict[str, Any]:
    return {"case": case, "severity": severity, "control_passed": passed, "expected": expected, "observed": observed}


def controlled_experiment() -> dict[str, Any]:
    exp = l5b.new_experiment("v23-red", 3, 3, "h", False)
    for i in range(3):
        l5b.add_task(exp, f"t{i}", f"{i+1:064x}", "web", 2, 10)
    l5b.freeze(exp)
    baseline = {"lead_time_minutes": 100, "human_minutes": 50, "token_cost_usd": 2, "rework_fraction": .2, "escaped_defects": 2, "critical_defects": 0, "trace_coverage": .6, "acceptance_pass_rate": .8, "maintainability_score": 6}
    improved = {"lead_time_minutes": 70, "human_minutes": 40, "token_cost_usd": 2, "rework_fraction": .1, "escaped_defects": 1, "critical_defects": 0, "trace_coverage": .9, "acceptance_pass_rate": .95, "maintainability_score": 8}
    for i in range(3):
        assignment = l5b.assignment_for(exp, f"t{i}")
        for pos, arm in enumerate(assignment["order"]):
            l5b.record_run(exp, task_id=f"t{i}", arm=arm, executor_code=f"exec-{arm}", execution_context_id=f"ctx-{i}-{arm}-{pos}", model="same", prompt_hash=("1" if arm == "baseline" else "2")*64, toolset_hash="3"*64, start_state_hash=f"{i+5:064x}", environment_hash="4"*64, artifact_hash=("5" if arm == "baseline" else "6")*64, run_log_hash=("7" if arm == "baseline" else "8")*64, metrics=baseline if arm == "baseline" else improved)
        for arm in l5b.ARMS:
            l5b.add_review(exp, blind_artifact_code=assignment["blind_artifact_codes"][arm], reviewer_code="blind-reviewer", correctness=8, completeness=8, maintainability=8, usability=8)
    return exp


def main() -> int:
    results: list[dict[str, Any]] = []

    stress = subprocess.run([sys.executable, str(ROOT / "scripts" / "control_plane_stress.py"), "--jobs", "30", "--workers", "8", "--updates-per-worker", "5"], cwd=ROOT, capture_output=True, text=True)
    payload = json.loads(stress.stdout) if stress.stdout.strip().startswith("{") else {"stdout": stress.stdout, "stderr": stress.stderr}
    results.append(record("sqlite_multiworker_job_claim_is_unique", stress.returncode == 0 and payload.get("jobs", {}).get("duplicate_claims") == 0, "Local SQLite safety mode must never double-lease the same job.", payload.get("jobs")))
    results.append(record("sqlite_concurrent_state_updates_are_cas_serialized", stress.returncode == 0 and payload.get("state", {}).get("revision") == payload.get("state", {}).get("expected_updates") and payload.get("state", {}).get("audit", {}).get("valid") is True, "Concurrent updates must preserve every successful retry and the audit chain.", payload.get("state")))
    results.append(record("recovery_drill_requeues_and_reaps", stress.returncode == 0 and payload.get("recovery_drill") is True, "Expired jobs and leases must be recoverable without audit corruption.", payload.get("recovery")))

    exp = controlled_experiment()
    provisional = l5b.analyze(exp)
    results.append(record("unsealed_l5b_cannot_be_formal_positive", provisional.get("decision") == "provisional-positive" and provisional.get("formal_evidence_eligible") is False, "An otherwise positive real experiment remains provisional until sealed.", {"decision": provisional.get("decision"), "formal": provisional.get("formal_evidence_eligible")}))

    mismatch = controlled_experiment()
    task = mismatch["runs"][0]["task_id"]
    pair = [run for run in mismatch["runs"] if run["task_id"] == task]
    pair[1]["toolset_hash"] = "9" * 64
    previous = "GENESIS"
    for run in mismatch["runs"]:
        run["previous_hash"] = previous
        run["record_hash"] = l5b.digest({k: v for k, v in run.items() if k != "record_hash"})
        previous = run["record_hash"]
    mismatch["record_chain_head"] = previous
    mismatch_result = l5b.analyze(mismatch)
    results.append(record("l5b_toolset_mismatch_invalidates_causal_claim", mismatch_result.get("decision") == "invalid-controls", "Cross-arm model/tool/start-state controls must match before a causal claim is allowed.", mismatch_result.get("control_errors")))

    gate = maturity.assess(ROOT / "validation" / "maturity" / "current-evidence.json", "production-candidate")
    results.append(record("maturity_gate_blocks_unsupported_production_claim", gate.get("passed") is False and gate.get("claim_allowed") is None and any("synthetic" in item for item in gate.get("failures", [])) and any("PostgreSQL" in item for item in gate.get("failures", [])), "Synthetic L5-B and SQLite-only stress evidence cannot unlock Production Candidate.", gate.get("failures")))

    passed = sum(item["control_passed"] for item in results)
    output = {"system_version": "2.3.0", "scope": "concurrency-l5b-maturity-claim-safety", "summary": {"cases": len(results), "passed": passed, "failed": len(results)-passed, "all_controls_passed": passed == len(results)}, "results": results}
    path = ROOT / "validation" / "v23_red_team_results.json"
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0 if passed == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
