#!/usr/bin/env python3
"""Verify recovery, QA feedback, rerun, and evidence invalidation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(run_root: Path, recipe_path: Path) -> dict:
    errors: list[str] = []
    final = load(run_root / "result.json")
    state = load(run_root.parent / "state/state.json")
    recipe = load(recipe_path)
    if final.get("status") != "passed" or state.get("status") != "passed":
        errors.append("final run or durable state is not passed")
    attempts = state.get("attempts", {})
    if not all(attempts.get(step, 0) >= 1 for step in ("write_prd", "design_web_flow", "build_feature_tdd", "qa_only", "ship_release", "retro_to_requirements")):
        errors.append("stage attempt history incomplete")
    markers = {item["step_id"]: item.get("invalidated_previous_evidence") for item in final.get("steps_run", [])}
    for step in ("design_web_flow", "build_feature_tdd", "qa_only", "ship_release"):
        if markers.get(step) != "upstream-reran":
            errors.append(f"downstream evidence was not invalidated: {step}")
    first_failure = run_root.parent / "attempt-1/run/result.json"
    if not first_failure.is_file() or load(first_failure).get("passed") is not False:
        errors.append("initial fail-closed run missing")
    qa_red = run_root.parent / "qa-red.json"
    if not qa_red.is_file() or load(qa_red).get("returncode") == 0:
        errors.append("QA RED evidence missing")
    qa = load(run_root / "qa_only/result.json")
    if qa.get("passed") is not True:
        errors.append("QA correction rerun did not pass")
    else:
        commands = qa["steps_run"][0].get("execution", {}).get("command_results", [])
        if not any(item.get("returncode") == 0 and "12 passed" in item.get("stdout", "") for item in commands):
            errors.append("QA GREEN evidence missing")
    route = any(item.get("from") == "qa_only" and item.get("to") == "build_feature_tdd" and item.get("action") == "invalidate-and-rerun" and "failed" in item.get("on_status", []) for item in recipe.get("failure_routes", []))
    mapping = any(item == {"from_step": "qa_only", "to_step": "build_feature_tdd", "artifact": "qa-verdict", "target_input": "Correction feedback"} for item in recipe.get("feedback_mappings", []))
    if not route or not mapping:
        errors.append("QA feedback route is incomplete")
    return {"gate": "full-dev-loop-lifecycle", "ok": not errors, "attempts": attempts, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--recipe", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.run_root, args.recipe)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
