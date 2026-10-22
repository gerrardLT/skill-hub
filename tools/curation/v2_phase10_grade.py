#!/usr/bin/env python3
"""Grade all 56 Phase 10 targeted revision attempts with 100% predeclared thresholds."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase9_grade import grade_value, metric, verify_attempt
    from tools.curation.v2_phase9_runner import attempt_manifest, load, sha_text, write
    from tools.curation.v2_phase10_runner import PLAN_PATH, RUN_ROOT
except ModuleNotFoundError:
    from v2_phase9_grade import grade_value, metric, verify_attempt
    from v2_phase9_runner import attempt_manifest, load, sha_text, write
    from v2_phase10_runner import PLAN_PATH, RUN_ROOT


def grade(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); plan = load(workspace / PLAN_PATH); run_root = workspace / RUN_ROOT; rows = []; evidence_errors = []
    for task in plan["tasks"]:
        directory = run_root / "attempts" / task["id"]; verified, errors = verify_attempt(task, directory); value = verified["parsed"]["value"] if verified and verified["parsed"].get("ok") else None; passed, failures = grade_value(task, value); run = verified["run"] if verified else {}
        if errors: evidence_errors.extend(f"{task['id']}:{error}" for error in errors)
        row = {"run_id": task["id"], "category": task["category"], "variant": task["variant"], "set": task.get("set"), "case_id": task["case_id"], "mutation_id": task.get("mutation_id"), "passed": bool(verified and not errors and run.get("exit_status") == "completed" and passed), "grade_failures": errors + failures + ([] if run.get("exit_status") == "completed" else ["run-not-completed"]), "duration_ms": run.get("duration_ms"), "total_tokens": run.get("token_usage", {}).get("totalTokens") if isinstance(run.get("token_usage"), dict) else None, "evidence_path": directory.relative_to(workspace).as_posix()}
        rows.append(row); write(directory / "grading.json", {"schema_version": "2.0", "run_id": task["id"], "passed": row["passed"], "expected": task["expected"], "actual": value, "failures": row["grade_failures"], "evidence_path": row["evidence_path"]}); write(directory / "artifact-manifest.json", attempt_manifest(directory))
    groups = {
        "overall": metric(rows),
        "p4_recipe_holdout": metric([row for row in rows if row["category"] == "p4-recipe-holdout"]),
        "p8_router_authored": metric([row for row in rows if row["category"] == "p8-router" and row["set"] == "authored"]),
        "p8_router_holdout": metric([row for row in rows if row["category"] == "p8-router" and row["set"] == "holdout"]),
        "p8_recipe_authored": metric([row for row in rows if row["category"] == "p8-recipe" and row["set"] == "authored"]),
        "p8_recipe_holdout": metric([row for row in rows if row["category"] == "p8-recipe" and row["set"] == "holdout"]),
        "causal_mutation_control": metric([row for row in rows if row["category"] == "causal-mutation" and row["variant"] == "control"]),
        "causal_mutation_mutated": metric([row for row in rows if row["category"] == "causal-mutation" and row["variant"] == "mutated"]),
    }
    mutation_results = []
    for mutation_id in sorted({row["mutation_id"] for row in rows if row["mutation_id"]}):
        pair = {row["variant"]: row for row in rows if row["mutation_id"] == mutation_id}; status = "killed" if set(pair) == {"control", "mutated"} and pair["control"]["passed"] and pair["mutated"]["passed"] else "invalid-control" if pair.get("control") and not pair["control"]["passed"] else "survived"
        mutation_results.append({"mutation_id": mutation_id, "status": status, "control_run": pair.get("control", {}).get("run_id"), "mutated_run": pair.get("mutated", {}).get("run_id")})
    thresholds = {"p4_recipe_holdouts_all": groups["p4_recipe_holdout"]["accuracy"] == 1.0, "p8_router_authored_all": groups["p8_router_authored"]["accuracy"] == 1.0, "p8_router_holdouts_all": groups["p8_router_holdout"]["accuracy"] == 1.0, "p8_recipe_authored_all": groups["p8_recipe_authored"]["accuracy"] == 1.0, "p8_recipe_holdouts_all": groups["p8_recipe_holdout"]["accuracy"] == 1.0, "causal_mutations_all_killed": all(item["status"] == "killed" for item in mutation_results), "evidence_complete": not evidence_errors and len(rows) == 60, "zero_actions": all(load(run_root / "attempts" / task["id"] / "run.json").get("candidate_action_executed") is False for task in plan["tasks"])}
    report = {"schema_version": "2.0", "phase": 10, "revision": 4, "status": "passed" if all(thresholds.values()) else "failed", "task_count": 60, "completed_attempts": len(rows), "evidence_errors": evidence_errors, "groups": groups, "thresholds": thresholds, "thresholds_passed": all(thresholds.values()), "mutation_results": mutation_results, "failed_runs": [row for row in rows if not row["passed"]], "runs": rows}
    write(run_root / "grading-report.json", report); return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); report = grade(args.workspace_root); print(json.dumps({"status": report["status"], "completed_attempts": report["completed_attempts"], "evidence_errors": len(report["evidence_errors"]), "groups": {key: {"passed": value["passed"], "total": value["total"], "accuracy": value["accuracy"]} for key, value in report["groups"].items()}, "mutations": dict(Counter(item["status"] for item in report["mutation_results"])), "thresholds": report["thresholds"], "thresholds_passed": report["thresholds_passed"]}, ensure_ascii=False, sort_keys=True)); return 0 if report["thresholds_passed"] and not report["evidence_errors"] else 1


if __name__ == "__main__": raise SystemExit(main())
