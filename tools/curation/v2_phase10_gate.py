#!/usr/bin/env python3
"""Fail-closed Phase 10 semantic-review and revision-4 evidence gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase9_gate import verify as verify_phase9
    from tools.curation.v2_phase9_grade import grade_value, verify_attempt
    from tools.curation.v2_phase9_runner import load, material_for, prompt_for, sha_text
except ModuleNotFoundError:
    from v2_phase9_gate import verify as verify_phase9
    from v2_phase9_grade import grade_value, verify_attempt
    from v2_phase9_runner import load, material_for, prompt_for, sha_text

PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"
PLAN_HASH = "b96a2b6172b9ee2760e3b9a40582a48e2516c70a5c9c42a0e4099ff6282ecd53"
EXPECTED_GROUPS = {
    "overall": (60, 60, 1.0),
    "p4_recipe_holdout": (4, 4, 1.0),
    "p8_router_authored": (14, 14, 1.0),
    "p8_router_holdout": (8, 8, 1.0),
    "p8_recipe_authored": (8, 8, 1.0),
    "p8_recipe_holdout": (6, 6, 1.0),
    "causal_mutation_control": (10, 10, 1.0),
    "causal_mutation_mutated": (10, 10, 1.0),
}
EXPECTED_THRESHOLDS = {"causal_mutations_all_killed": True, "evidence_complete": True, "p4_recipe_holdouts_all": True, "p8_recipe_authored_all": True, "p8_recipe_holdouts_all": True, "p8_router_authored_all": True, "p8_router_holdouts_all": True, "zero_actions": True}


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    prior = verify_phase9(workspace); add("phase-9-and-earlier-evidence-compatibility", [] if prior["ok"] and prior["release_blocked"] else ["Phase 9 evidence or release-block state changed"])
    identity_errors = []
    if load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json").get("tree_sha256") != PHASE9_TREE: identity_errors.append("Phase 9 tree drift")
    add("frozen-phase-9-identity", identity_errors)

    ledger_errors = []; ledger = load(workspace / "curation/v2/phase-10/skill-review-ledger.json")
    if ledger.get("skill_count") != 157 or ledger.get("reviewed_output_count") != 314 or ledger.get("verdict_counts") != {"accepted": 157} or ledger.get("final_user_approval") is not False: ledger_errors.append("Skill review ledger count/verdict/approval mismatch")
    ids = [item.get("skill_id") for item in ledger.get("records", [])]
    if len(ids) != len(set(ids)) or len(ids) != 157: ledger_errors.append("Skill review records duplicate or missing")
    for item in ledger.get("records", []):
        if item.get("verdict") != "accepted" or item.get("revision_required") is not False or item.get("reviewed_output_count") != 2 or {case.get("case_kind") for case in item.get("cases", [])} != {"should-trigger", "should-not-trigger"}: ledger_errors.append(f"{item.get('skill_id')}: incomplete review")
        for case in item.get("cases", []):
            if not all(case.get("checks", {}).values()) or not (workspace / case.get("evidence_path", "missing") / "grading.json").is_file(): ledger_errors.append(f"{item.get('skill_id')}/{case.get('case_id')}: review evidence invalid")
    add("all-157-skills-and-314-outputs-reviewed", ledger_errors)

    adjudication_errors = []; adjudications = load(workspace / "curation/v2/phase-10/finding-adjudications.json"); decision = load(workspace / "curation/v2/phase-10/renderer-taxonomy-decision.json")
    if adjudications.get("adjudication_count") != 6 or adjudications.get("unresolved") != [] or len({item.get("finding_id") for item in adjudications.get("adjudications", [])}) != 6: adjudication_errors.append("Phase 9 finding adjudications incomplete")
    if decision.get("selected_option") != "revise_fixture_fail_closed" or decision.get("final_release_approval") is not False: adjudication_errors.append("renderer taxonomy decision changed")
    add("phase-9-findings-and-user-taxonomy-decision", adjudication_errors)

    revision_errors = []
    histories = [(1, 56, 50, 6), (2, 58, 54, 4), (3, 60, 59, 1)]
    for revision, runs, passed, failed in histories:
        checkpoint = workspace / f".specs/capability-compiler-v2/phase-10/revision-{revision}-rejection.json"; evidence = workspace / f"evals/runs/capability-compiler-v2/phase-10/revision-{revision}"
        if not checkpoint.is_file(): revision_errors.append(f"revision {revision}: rejection checkpoint missing"); continue
        value = load(checkpoint)
        if value.get("status") != "rejected-targeted-threshold-miss" or value.get("completed_attempts") != runs or value.get("passed_runs") != passed or value.get("failed_runs") != failed or value.get("deleted_failures") != 0 or value.get("thresholds_lowered") is not False: revision_errors.append(f"revision {revision}: checkpoint mismatch")
        if len(list((evidence / "attempts").glob("run-*/run.json"))) != runs: revision_errors.append(f"revision {revision}: attempts not preserved")
    add("rejected-revisions-and-failed-evidence-preserved", revision_errors)

    revision4_errors = []; root = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-4"; patch = load(root / "patch-ledger.json")
    if patch.get("version") != "0.1.4-v2-candidate" or patch.get("atomic_skill_revisions") != 0 or patch.get("released") != 0 or patch.get("revision4_change_count") != 1: revision4_errors.append("revision 4 patch scope/version/release mismatch")
    if len(patch.get("revision4_records", [])) != 1 or not patch["revision4_records"][0]["path"].endswith("phase-4/complete-ui-design-and-review.json"): revision4_errors.append("revision 4 changed more than the authorized Recipe")
    recipe = load(root / "phase-4/complete-ui-design-and-review.json")
    expected_routes = [["review-evidence", "rendered-critique", "explicit-human-approval", "release-gate"], ["review-evidence", "rendered-critique", "explicit-human-approval", "separate-remediation-capability", "review-evidence", "rendered-critique", "explicit-human-approval", "release-gate"]]
    if [item.get("planned_route") for item in recipe.get("complete_route_planning", {}).get("sequences", [])] != expected_routes: revision4_errors.append("complete route planning does not preserve review evidence")
    add("bounded-revision-4-scope-and-semantics", revision4_errors)

    plan_errors = []; plan = load(workspace / "curation/v2/phase-10/run-plan.json"); tasks = plan.get("tasks", []); task_hash = sha_text(json.dumps(tasks, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if plan.get("revision") != 4 or plan.get("version") != "0.1.4-v2-candidate" or plan.get("task_count") != 60 or len(tasks) != 60 or plan.get("task_sha256") != task_hash or task_hash != PLAN_HASH: plan_errors.append("revision 4 plan identity/count/hash mismatch")
    if plan.get("counts") != {"causal-mutation": 20, "p4-recipe-holdout": 4, "p8-recipe": 14, "p8-router": 22} or plan.get("tools") != [] or plan.get("candidate_action_execution") is not False: plan_errors.append("revision 4 task composition or action boundary mismatch")
    for task in tasks:
        try:
            material = material_for(task, workspace); prompt, _ = prompt_for(task, material)
            if sha_text(material) != task.get("material_sha256") or sha_text(prompt) != task.get("prompt_sha256"): plan_errors.append(f"{task.get('id')}: prompt/material drift")
        except Exception as exc: plan_errors.append(f"{task.get('id')}: recompute failed {type(exc).__name__}:{exc}")
    add("revision-4-plan-and-prompts-recompute", plan_errors)

    attempt_errors = []; run_root = workspace / "evals/runs/capability-compiler-v2/phase-10"; rows = []
    for task in tasks:
        directory = run_root / "attempts" / task["id"]; verified, errors = verify_attempt(task, directory)
        if errors: attempt_errors.extend(f"{task['id']}:{error}" for error in errors); continue
        value = verified["parsed"]["value"]; passed, failures = grade_value(task, value); grade_path = directory / "grading.json"
        if not grade_path.is_file(): attempt_errors.append(f"{task['id']}: grading missing"); continue
        grading = load(grade_path); run = verified["run"]
        if not passed or failures or grading.get("passed") is not True or grading.get("failures") != [] or grading.get("actual") != value or run.get("candidate_action_executed") is not False or run.get("exit_status") != "completed" or run.get("parse_ok") is not True: attempt_errors.append(f"{task['id']}: run or grade not passing exactly")
        rows.append(task["id"])
    if len(rows) != 60: attempt_errors.append(f"verified passing attempts {len(rows)} != 60")
    add("all-60-targeted-attempts-pass-with-zero-actions", attempt_errors)

    aggregate_errors = []; report = load(run_root / "grading-report.json")
    if report.get("status") != "passed" or report.get("revision") != 4 or report.get("task_count") != 60 or report.get("completed_attempts") != 60 or report.get("evidence_errors") != [] or report.get("thresholds") != EXPECTED_THRESHOLDS or report.get("thresholds_passed") is not True or report.get("failed_runs") != []: aggregate_errors.append("revision 4 aggregate status/thresholds mismatch")
    for key, expected in EXPECTED_GROUPS.items():
        actual = report.get("groups", {}).get(key, {})
        if (actual.get("passed"), actual.get("total"), actual.get("accuracy")) != expected: aggregate_errors.append(f"{key}: aggregate mismatch")
    if len(report.get("mutation_results", [])) != 10 or any(item.get("status") != "killed" for item in report.get("mutation_results", [])): aggregate_errors.append("causal mutations are not 10/10 killed")
    add("revision-4-aggregates-and-100-percent-thresholds", aggregate_errors)

    review_errors = []; review = load(workspace / "curation/v2/phase-10/semantic-review.json")
    if review.get("status") != "passed-parent-direct-semantic-review" or review.get("final_user_release_approval") is not False or review.get("open_findings") != [] or review.get("release_disposition") != "eligible-for-phase-11-real-project-validation-not-released": review_errors.append("Phase 10 review status or release boundary mismatch")
    if review.get("revision4_results", {}).get("candidate_actions_executed") != 0: review_errors.append("review claims candidate action")
    add("semantic-review-complete-not-final-approval", review_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-10", "ok": not errors, "phase_10_complete": not errors, "final_user_release_approval": False, "released": False, "eligible_for_phase_11": not errors, "checks": checks, "counts": {"reviewed_skills": 157, "reviewed_outputs": 314, "adjudicated_findings": 6, "rejected_revisions_preserved": 3, "revision4_runs": len(rows), "causal_mutations_killed": 10}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
