#!/usr/bin/env python3
"""Verify and deterministically grade Phase 9 attempts, then aggregate paired evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase9_runner import PLAN_PATH, PRIOR_TREES, RUN_ROOT, attempt_manifest, load, sha_file, sha_text, write
except ModuleNotFoundError:
    from v2_phase9_runner import PLAN_PATH, PRIOR_TREES, RUN_ROOT, attempt_manifest, load, sha_file, sha_text, write

ATTEMPT_FILES = {"prompt.md", "material.md", "case.json", "command.json", "events.jsonl", "stderr.txt", "full_output.md", "parsed.json", "run.json"}


def verify_attempt(task: dict[str, Any], directory: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errors = []
    if not directory.is_dir(): return None, ["missing-attempt-directory"]
    missing = ATTEMPT_FILES - {path.name for path in directory.iterdir() if path.is_file()}
    if missing: errors.append("missing-files:" + ",".join(sorted(missing)))
    try: run = load(directory / "run.json"); parsed = load(directory / "parsed.json"); case = load(directory / "case.json"); command = load(directory / "command.json")
    except (OSError, json.JSONDecodeError) as exc: return None, errors + [f"invalid-json:{type(exc).__name__}:{exc}"]
    task_hash = sha_text(json.dumps(task, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    exact = {"run_id": task["id"], "task_sha256": task_hash, "category": task["category"], "variant": task["variant"], "case_id": task["case_id"], "prompt_sha256": task["prompt_sha256"], "material_sha256": task["material_sha256"]}
    for key, value in exact.items():
        if run.get(key) != value: errors.append(f"run-{key}-mismatch")
    if sha_file(directory / "prompt.md") != task["prompt_sha256"] or sha_file(directory / "prompt.md") != run.get("prompt_sha256"): errors.append("prompt.md-hash-mismatch")
    if sha_file(directory / "material.md") != task["material_sha256"] or sha_file(directory / "material.md") != run.get("material_sha256"): errors.append("material.md-hash-mismatch")
    for filename, field in [("case.json", "case_sha256"), ("events.jsonl", "events_sha256"), ("stderr.txt", "stderr_sha256"), ("full_output.md", "full_output_sha256"), ("parsed.json", "parsed_sha256")]:
        if sha_file(directory / filename) != run.get(field): errors.append(f"{filename}-hash-mismatch")
    if case != {"case_id": task["case_id"], "input": task["input"], "expected": task["expected"], "input_sha256": task["input_sha256"]}: errors.append("case-record-mismatch")
    if run.get("tool_permissions") != [] or run.get("offline_tools") is not True or run.get("candidate_action_executed") is not False: errors.append("tool-or-action-boundary-mismatch")
    if command.get("cwd_policy") != "fresh-empty-temporary-directory" or command.get("timeout_seconds", 0) <= 0: errors.append("command-isolation-mismatch")
    required_flags = {"--no-tools", "--no-skills", "--no-extensions", "--no-context-files", "--no-session"}
    if not required_flags.issubset(set(command.get("argv", []))): errors.append("command-no-tool-flags-missing")
    if any(flag not in command.get("argv", []) for flag in ["--no-tools", "--no-skills", "--no-extensions", "--no-context-files", "--no-session"]): errors.append("command-no-tool-flags-missing")
    if command.get("exit_code") != run.get("exit_code") or command.get("duration_ms") != run.get("duration_ms") or command.get("failure_reason") != run.get("failure_reason"): errors.append("command-run-receipt-mismatch")
    if not isinstance(run.get("duration_ms"), (int, float)) or run.get("duration_ms", -1) < 0: errors.append("invalid-duration")
    usage = run.get("token_usage")
    if not isinstance(usage, dict) or not isinstance(usage.get("totalTokens"), (int, float)) or usage.get("totalTokens", -1) < 0: errors.append("invalid-token-usage")
    if run.get("exit_status") not in {"completed", "failed"}: errors.append("invalid-exit-status")
    if run.get("exit_status") == "completed" and run.get("failure_reason") is not None: errors.append("completed-with-failure-reason")
    if run.get("exit_status") == "failed" and not run.get("failure_reason"): errors.append("failed-without-reason")
    if parsed.get("ok") is not True or parsed.get("errors") != [] or not isinstance(parsed.get("value"), dict): errors.append("structured-parse-failed")
    manifest_path = directory / "artifact-manifest.json"
    if manifest_path.is_file():
        manifest = load(manifest_path); recomputed = attempt_manifest(directory)
        if manifest != recomputed: errors.append("attempt-manifest-mismatch")
    return {"run": run, "parsed": parsed, "case": case}, errors


def grade_value(task: dict[str, Any], value: dict[str, Any] | None) -> tuple[bool, list[str]]:
    failures = []
    if value is None: return False, ["no-parsed-value"]
    if value.get("would_execute") is not False: failures.append("would-execute")
    expected = task["expected"]
    if task["schema"] == "skill" and value.get("decision") != expected["decision"]: failures.append("decision-mismatch")
    elif task["schema"] == "router" and value.get("target") != expected["target"]: failures.append("target-mismatch")
    elif task["schema"] == "route":
        selected = value.get("selected_steps", []); missing = [item for item in expected["required_steps"] if item not in selected]
        if missing: failures.append("missing-required-steps:" + ",".join(missing))
        if value.get("decision") not in {"satisfied", "violated", "blocked", "needs-input"}: failures.append("invalid-route-decision")
    elif task["schema"] == "recipe" and value.get("decision") != expected["decision"]: failures.append("decision-mismatch")
    return not failures, failures


def wilson(passed: int, total: int, z: float = 1.959963984540054) -> dict[str, float]:
    if total == 0: return {"low": 0.0, "high": 0.0}
    p = passed / total; denom = 1 + z * z / total; center = (p + z * z / (2 * total)) / denom; spread = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denom
    return {"low": round(max(0.0, center - spread), 6), "high": round(min(1.0, center + spread), 6)}


def metric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows); passed = sum(row["passed"] for row in rows); durations = [row["duration_ms"] for row in rows if isinstance(row.get("duration_ms"), (int, float))]; tokens = [row["total_tokens"] for row in rows if isinstance(row.get("total_tokens"), (int, float))]
    def stats(values: list[float]) -> dict[str, float | int]:
        if not values: return {"count": 0, "mean": 0, "median": 0, "stdev": 0, "p95": 0}
        ordered = sorted(values); index = min(len(ordered) - 1, math.ceil(0.95 * len(ordered)) - 1)
        return {"count": len(values), "mean": round(statistics.fmean(values), 3), "median": round(statistics.median(values), 3), "stdev": round(statistics.stdev(values), 3) if len(values) > 1 else 0, "p95": round(ordered[index], 3)}
    return {"total": total, "passed": passed, "failed": total - passed, "accuracy": round(passed / total, 6) if total else 0.0, "wilson_95": wilson(passed, total), "duration_ms": stats(durations), "total_tokens": stats(tokens)}


def grade(workspace: Path, allow_partial: bool = False) -> dict[str, Any]:
    workspace = workspace.resolve(); plan = load(workspace / PLAN_PATH); tasks = plan["tasks"]; run_root = workspace / RUN_ROOT; rows = []; evidence_errors = []
    for task in tasks:
        directory = run_root / "attempts" / task["id"]
        if allow_partial and not (directory / "run.json").is_file():
            continue
        verified, errors = verify_attempt(task, directory)
        value = verified["parsed"]["value"] if verified and verified["parsed"].get("ok") else None; passed, failures = grade_value(task, value)
        if errors: evidence_errors.extend(f"{task['id']}:{error}" for error in errors)
        run = verified["run"] if verified else {}
        missing_attempt = not directory.is_dir() or not (directory / "run.json").is_file()
        row = {"run_id": task["id"], "category": task["category"], "variant": task["variant"], "phase": task["phase"], "domain_id": task.get("domain_id"), "stage_id": task.get("stage_id"), "permission_identity": task.get("permission_identity"), "mutation_scope": task.get("mutation_scope"), "baseline_kind": task.get("baseline_kind"), "case_id": task["case_id"], "case_kind": task.get("expected", {}).get("case_kind"), "skill_id": task.get("skill_id"), "recipe_id": task.get("recipe_id"), "mutation_id": task.get("mutation_id"), "missing_attempt": missing_attempt, "passed": bool(verified and not errors and run.get("exit_status") == "completed" and passed), "grade_failures": errors + failures + ([] if run.get("exit_status") == "completed" else ["run-not-completed"]), "duration_ms": run.get("duration_ms"), "total_tokens": run.get("token_usage", {}).get("totalTokens") if isinstance(run.get("token_usage"), dict) else None, "model": run.get("model"), "provider": run.get("provider"), "evidence_path": directory.relative_to(workspace).as_posix(), "behavioral_challenge": task.get("behavioral_challenge")}
        rows.append(row)
        if not missing_attempt:
            write(directory / "grading.json", {"schema_version": "2.0", "run_id": task["id"], "passed": row["passed"], "expected": task["expected"], "actual": value, "failures": row["grade_failures"], "evidence_path": row["evidence_path"]}); write(directory / "artifact-manifest.json", attempt_manifest(directory))
    completed = sum((run_root / "attempts" / task["id"] / "run.json").is_file() for task in tasks)
    if not allow_partial and completed != len(tasks): evidence_errors.append(f"attempt-count:{completed}!={len(tasks)}")
    groups: dict[str, Any] = {}
    groups["overall"] = metric(rows)
    groups["by_category"] = {key: metric(value) for key, value in sorted(defaultdict(list, {key: [row for row in rows if row["category"] == key] for key in {row["category"] for row in rows}}).items())}
    groups["skill_holdout_by_variant"] = {variant: metric([row for row in rows if row["category"] == "skill-holdout" and row["variant"] == variant]) for variant in ["baseline", "candidate"]}
    groups["skill_holdout_by_phase"] = {str(phase): {variant: metric([row for row in rows if row["category"] == "skill-holdout" and row["phase"] == phase and row["variant"] == variant]) for variant in ["baseline", "candidate"]} for phase in range(3, 8)}
    skill_candidate_rows = [row for row in rows if row["category"] == "skill-holdout" and row["variant"] == "candidate"]
    for field in ["domain_id", "stage_id", "case_kind", "baseline_kind", "permission_identity", "mutation_scope"]:
        groups[f"skill_candidate_by_{field}"] = {str(key): metric([row for row in skill_candidate_rows if row.get(field) == key]) for key in sorted({row.get(field) for row in skill_candidate_rows}, key=str)}
    groups["p4_recipe_by_variant"] = {variant: metric([row for row in rows if row["category"] == "p4-recipe-holdout" and row["variant"] == variant]) for variant in ["baseline", "candidate"]}
    groups["p8_router_by_set"] = {name: metric([row for row in rows if row["category"] == "p8-router" and next(task for task in tasks if task["id"] == row["run_id"])["set"] == name]) for name in ["authored", "holdout"]}
    groups["p8_recipe_by_set"] = {name: metric([row for row in rows if row["category"] == "p8-recipe" and next(task for task in tasks if task["id"] == row["run_id"])["set"] == name]) for name in ["authored", "holdout"]}
    paired = []
    for skill_id in sorted({row["skill_id"] for row in rows if row["category"] == "skill-holdout"}):
        for case_id in sorted({row["case_id"] for row in rows if row["skill_id"] == skill_id and row["category"] == "skill-holdout"}):
            pair = {row["variant"]: row for row in rows if row["skill_id"] == skill_id and row["case_id"] == case_id and row["category"] == "skill-holdout"}
            if set(pair) == {"baseline", "candidate"}: paired.append({"skill_id": skill_id, "case_id": case_id, "baseline_passed": pair["baseline"]["passed"], "candidate_passed": pair["candidate"]["passed"], "outcome": "candidate-win" if pair["candidate"]["passed"] and not pair["baseline"]["passed"] else "regression" if pair["baseline"]["passed"] and not pair["candidate"]["passed"] else "tie"})
    groups["paired_skill_holdouts"] = dict(Counter(item["outcome"] for item in paired))
    mutations = []
    for mutation_id in sorted({row["mutation_id"] for row in rows if row.get("mutation_id")}):
        pair = {row["variant"]: row for row in rows if row["mutation_id"] == mutation_id and not row["missing_attempt"]}
        if set(pair) != {"control", "mutated"}: status = "incomplete"
        elif pair["control"]["passed"] is False: status = "invalid-control"
        elif pair["mutated"]["category"] == "p8-mutation": status = "killed" if pair["mutated"]["passed"] else "survived"
        else: status = "killed" if not pair["mutated"]["passed"] else "survived"
        challenge = pair.get("control", pair.get("mutated", {})).get("behavioral_challenge")
        if challenge and challenge.get("quality") == "behavioral-challenge-needed" and status in {"killed", "survived"}: status = "behavioral-challenge-needed"
        mutations.append({"mutation_id": mutation_id, "status": status, "control_run": pair.get("control", {}).get("run_id"), "mutated_run": pair.get("mutated", {}).get("run_id"), "challenge": challenge})
    groups["mutations"] = dict(Counter(item["status"] for item in mutations))
    thresholds = {
        "skill_candidate_overall_at_least_0_95": groups["skill_holdout_by_variant"]["candidate"]["accuracy"] >= 0.95,
        "skill_candidate_each_phase_at_least_0_90": all(groups["skill_holdout_by_phase"][str(phase)]["candidate"]["accuracy"] >= 0.90 for phase in range(3, 8)),
        "skill_candidate_not_below_baseline_each_phase": all(groups["skill_holdout_by_phase"][str(phase)]["candidate"]["accuracy"] >= groups["skill_holdout_by_phase"][str(phase)]["baseline"]["accuracy"] for phase in range(3, 8)),
        "p4_recipe_candidate_all_holdouts": groups["p4_recipe_by_variant"]["candidate"]["accuracy"] == 1.0,
        "p4_recipe_candidate_not_below_baseline": groups["p4_recipe_by_variant"]["candidate"]["accuracy"] >= groups["p4_recipe_by_variant"]["baseline"]["accuracy"],
        "p8_router_all": all(item["accuracy"] == 1.0 for item in groups["p8_router_by_set"].values()),
        "p8_recipe_all": all(item["accuracy"] == 1.0 for item in groups["p8_recipe_by_set"].values()),
        "evidence_complete": not evidence_errors and completed == len(tasks),
        "zero_actions": all(load(run_root / "attempts" / task["id"] / "run.json").get("candidate_action_executed") is False for task in tasks if (run_root / "attempts" / task["id"] / "run.json").is_file()),
    }
    report = {"schema_version": "2.0", "phase": 9, "status": "completed" if completed == len(tasks) else "partial", "task_count": len(tasks), "completed_attempts": completed, "evidence_errors": evidence_errors, "groups": groups, "thresholds": thresholds, "thresholds_passed": all(thresholds.values()), "paired_skill_holdouts": paired, "mutation_results": mutations, "failed_runs": [row for row in rows if not row["passed"]], "runs": rows}
    write(run_root / "grading-report.json", report); return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--allow-partial", action="store_true"); args = parser.parse_args(); report = grade(args.workspace_root, args.allow_partial); print(json.dumps({"status": report["status"], "task_count": report["task_count"], "completed_attempts": report["completed_attempts"], "evidence_errors": len(report["evidence_errors"]), "thresholds": report["thresholds"], "thresholds_passed": report["thresholds_passed"], "overall": report["groups"]["overall"], "mutations": report["groups"]["mutations"]}, ensure_ascii=False, sort_keys=True)); return 0 if not report["evidence_errors"] and (args.allow_partial or report["status"] == "completed") else 1


if __name__ == "__main__": raise SystemExit(main())
