#!/usr/bin/env python3
"""Fail-closed evidence gate for completed Phase 9 evaluations; release thresholds remain separate."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase8_gate import verify as verify_phase8
    from tools.curation.v2_phase9_grade import grade_value, verify_attempt
    from tools.curation.v2_phase9_runner import MODEL, PLAN_PATH, PRIOR_TREES, RUN_ROOT, load, material_for, prompt_for, sha_file, sha_text
except ModuleNotFoundError:
    from v2_phase8_gate import verify as verify_phase8
    from v2_phase9_grade import grade_value, verify_attempt
    from v2_phase9_runner import MODEL, PLAN_PATH, PRIOR_TREES, RUN_ROOT, load, material_for, prompt_for, sha_file, sha_text

EXPECTED_COUNTS = {"p4-recipe-holdout": 8, "p4-recipe-mutation": 4, "p8-mutation": 12, "p8-recipe": 14, "p8-router": 22, "skill-holdout": 628, "skill-mutation": 314}
EXPECTED_THRESHOLDS = {
    "evidence_complete": True,
    "p4_recipe_candidate_all_holdouts": False,
    "p4_recipe_candidate_not_below_baseline": True,
    "p8_recipe_all": False,
    "p8_router_all": False,
    "skill_candidate_each_phase_at_least_0_90": True,
    "skill_candidate_not_below_baseline_each_phase": True,
    "skill_candidate_overall_at_least_0_95": True,
    "zero_actions": True,
}
EXPECTED_METRICS = {
    "skill_baseline": (159, 314, 0.506369),
    "skill_candidate": (314, 314, 1.0),
    "p4_baseline": (0, 4, 0.0),
    "p4_candidate": (3, 4, 0.75),
    "p8_router_authored": (9, 14, 0.642857),
    "p8_router_holdout": (5, 8, 0.625),
    "p8_recipe_authored": (8, 8, 1.0),
    "p8_recipe_holdout": (4, 6, 0.666667),
}


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    prior = verify_phase8(workspace); add("phase-8-and-earlier-compatibility", [] if prior["ok"] else prior["errors"])
    identity_errors = []
    for phase, expected in PRIOR_TREES.items():
        path = workspace / f".specs/capability-compiler-v2/{phase.replace('phase', 'phase-')}/artifact-manifest.json"
        if not path.is_file() or load(path).get("tree_sha256") != expected: identity_errors.append(f"{phase}: tree identity drift")
    add("prior-phase-artifact-identities", identity_errors)

    plan_path = workspace / PLAN_PATH; plan_errors = []
    if not plan_path.is_file():
        plan = {"tasks": []}; plan_errors.append("run plan missing")
    else: plan = load(plan_path)
    tasks = plan.get("tasks", []); task_ids = [task.get("id") for task in tasks]
    task_hash = sha_text(json.dumps(tasks, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if plan.get("task_count") != 1002 or len(tasks) != 1002 or len(set(task_ids)) != 1002: plan_errors.append("run plan does not contain exactly 1002 unique tasks")
    if plan.get("counts") != EXPECTED_COUNTS: plan_errors.append("run plan category counts changed")
    if plan.get("task_sha256") != task_hash: plan_errors.append("run plan task hash mismatch")
    if plan.get("model_request") != MODEL or plan.get("thinking") != "low" or plan.get("tools") != [] or plan.get("network_tools") is not False or plan.get("candidate_action_execution") is not False: plan_errors.append("run plan execution isolation changed")
    if plan.get("provider_inference_channel") != "router9-qoder" or plan.get("prior_artifact_trees") != PRIOR_TREES: plan_errors.append("run plan provider or prior identities changed")
    for task in tasks:
        try:
            material = material_for(task, workspace); prompt, _ = prompt_for(task, material)
            if sha_text(material) != task.get("material_sha256") or sha_text(prompt) != task.get("prompt_sha256") or sha_text(task.get("input", "")) != task.get("input_sha256"): plan_errors.append(f"{task.get('id')}: material, prompt, or input hash drift")
        except Exception as exc: plan_errors.append(f"{task.get('id')}: cannot recompute prompt: {type(exc).__name__}:{exc}")
    add("frozen-plan-and-prompt-recomputation", plan_errors)

    attempt_errors = []; run_root = workspace / RUN_ROOT; rows = []
    attempt_dirs = {path.name for path in (run_root / "attempts").glob("run-*") if path.is_dir()} if (run_root / "attempts").is_dir() else set()
    if attempt_dirs != set(task_ids): attempt_errors.append("attempt directories do not exactly match plan")
    for task in tasks:
        directory = run_root / "attempts" / task["id"]; verified, errors = verify_attempt(task, directory)
        if errors: attempt_errors.extend(f"{task['id']}:{error}" for error in errors); continue
        assert verified is not None
        run = verified["run"]; parsed = verified["parsed"]; passed, failures = grade_value(task, parsed["value"])
        grade_path = directory / "grading.json"
        if not grade_path.is_file(): attempt_errors.append(f"{task['id']}: grading missing"); continue
        grading = load(grade_path)
        expected_pass = bool(run["exit_status"] == "completed" and passed)
        if grading.get("run_id") != task["id"] or grading.get("passed") != expected_pass or grading.get("expected") != task["expected"] or grading.get("actual") != parsed["value"] or grading.get("failures") != failures: attempt_errors.append(f"{task['id']}: grade not exactly recomputable")
        event_lines = [line for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        try: events = [json.loads(line) for line in event_lines]
        except json.JSONDecodeError as exc: attempt_errors.append(f"{task['id']}: invalid event line {exc}"); events = []
        if any(str(event.get("type", "")).startswith("tool_execution_") for event in events): attempt_errors.append(f"{task['id']}: tool execution event present")
        if (run.get("provider"), run.get("model"), run.get("response_model"), run.get("stop_reason")) != ("router9-qoder", MODEL, "gpt-5.6-sol", "stop"): attempt_errors.append(f"{task['id']}: model identity or stop reason changed")
        if run.get("exit_status") != "completed" or run.get("exit_code") != 0 or run.get("parse_ok") is not True or run.get("candidate_action_executed") is not False: attempt_errors.append(f"{task['id']}: execution, parse, or action state invalid")
        rows.append({"task": task, "run": run, "passed": expected_pass, "failures": failures})
    add("attempt-evidence-events-grades-and-zero-actions", attempt_errors)

    report_errors = []; report_path = run_root / "grading-report.json"
    if not report_path.is_file(): report = {}; report_errors.append("grading report missing")
    else: report = load(report_path)
    if report.get("status") != "completed" or report.get("task_count") != 1002 or report.get("completed_attempts") != 1002 or report.get("evidence_errors") != []: report_errors.append("grading report completion/evidence state mismatch")
    if report.get("thresholds") != EXPECTED_THRESHOLDS or report.get("thresholds_passed") is not False: report_errors.append("predeclared threshold results changed")
    groups = report.get("groups", {})
    sources = {
        "skill_baseline": groups.get("skill_holdout_by_variant", {}).get("baseline", {}),
        "skill_candidate": groups.get("skill_holdout_by_variant", {}).get("candidate", {}),
        "p4_baseline": groups.get("p4_recipe_by_variant", {}).get("baseline", {}),
        "p4_candidate": groups.get("p4_recipe_by_variant", {}).get("candidate", {}),
        "p8_router_authored": groups.get("p8_router_by_set", {}).get("authored", {}),
        "p8_router_holdout": groups.get("p8_router_by_set", {}).get("holdout", {}),
        "p8_recipe_authored": groups.get("p8_recipe_by_set", {}).get("authored", {}),
        "p8_recipe_holdout": groups.get("p8_recipe_by_set", {}).get("holdout", {}),
    }
    for key, expected in EXPECTED_METRICS.items():
        actual = sources[key]
        if (actual.get("passed"), actual.get("total"), actual.get("accuracy")) != expected: report_errors.append(f"{key}: aggregate metric changed")
    if groups.get("paired_skill_holdouts") != {"candidate-win": 155, "tie": 159} or groups.get("mutations") != {"behavioral-challenge-needed": 14, "invalid-control": 2, "killed": 5, "survived": 144}: report_errors.append("paired or mutation aggregate changed")
    if len(report.get("runs", [])) != 1002 or {row.get("run_id") for row in report.get("runs", [])} != set(task_ids): report_errors.append("grading report run ledger mismatch")
    report_runs = {row["run_id"]: row for row in report.get("runs", [])}
    for row in rows:
        reported = report_runs.get(row["task"]["id"], {})
        if reported.get("passed") != row["passed"] or reported.get("grade_failures") != row["failures"] or reported.get("evidence_path") != (run_root / "attempts" / row["task"]["id"]).relative_to(workspace).as_posix(): report_errors.append(f"{row['task']['id']}: aggregate row mismatch")
    add("aggregate-metrics-thresholds-and-failed-case-retention", report_errors)

    calibration_errors = []
    calibration_roots = [
        workspace / "evals/runs/capability-compiler-v2/phase-9-pilots/routing-readiness-calibration-v1",
        workspace / "evals/runs/capability-compiler-v2/phase-9-pilots/recipe-route-completeness-calibration-v2",
        workspace / "evals/runs/capability-compiler-v2/phase-9-pilots/attempt-manifest-grading-migration-v3",
    ]
    for root in calibration_roots:
        finding = root / "finding.json"
        if not finding.is_file(): calibration_errors.append(f"{root.name}: finding missing"); continue
        value = load(finding)
        if value.get("deleted_failures") != 0 or value.get("production_evidence_eligible") is not False: calibration_errors.append(f"{root.name}: calibration disposition changed")
    if len(list((calibration_roots[0] / "run-root/attempts").glob("run-*/run.json"))) != 8: calibration_errors.append("calibration v1 does not preserve 8 attempts")
    if len(list((calibration_roots[1] / "attempts").glob("run-*/run.json"))) != 12: calibration_errors.append("calibration v2 does not preserve 12 attempts")
    add("protocol-calibrations-and-failed-evidence-retention", calibration_errors)

    review_errors = []; review_path = workspace / "curation/v2/phase-9/semantic-review.json"
    if not review_path.is_file(): review_errors.append("semantic review missing")
    else:
        review = load(review_path)
        if review.get("status") != "completed-with-findings" or review.get("reviewed_run_count") != 1002 or len(review.get("open_findings", [])) != 6 or review.get("release_disposition") != "blocked-pending-phase-10-revision-and-human-review": review_errors.append("semantic review status/findings/release disposition mismatch")
        if review.get("thresholds", {}).get("failed") != ["p4_recipe_candidate_all_holdouts", "p8_router_all", "p8_recipe_all"]: review_errors.append("semantic review threshold failures changed")
    add("semantic-adjudication-and-release-block", review_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {
        "gate": "capability-compiler-v2-phase-9",
        "ok": not errors,
        "evaluation_complete": not errors,
        "release_thresholds_passed": False,
        "release_blocked": True,
        "checks": checks,
        "counts": {"planned_runs": len(tasks), "verified_attempts": len(rows), "candidate_skill_holdouts_passed": EXPECTED_METRICS["skill_candidate"][0], "candidate_skill_holdouts_total": EXPECTED_METRICS["skill_candidate"][1], "open_findings": 6, "preserved_calibration_attempts": 20},
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
