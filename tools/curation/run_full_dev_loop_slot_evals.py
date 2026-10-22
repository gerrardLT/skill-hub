#!/usr/bin/env python3
"""Build executable baseline, candidate, holdout, and mutation evidence for six slots."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

from tools.curation.recipe_execute import _status, execute_recipe
from tools.curation.slot_gate import evaluate_gates

CONFIG = {
    "design-context-and-direction-contract": ("design_web_flow/result.json", "design", "design-web-flow.json"),
    "tdd-change-loop": ("build_feature_tdd/result.json", "implement", "build-feature-tdd.json"),
    "completion-evidence-gate": ("build_feature_tdd/result.json", "complete", "build-feature-tdd.json"),
    "independent-blackbox-qa": ("qa_only/result.json", "qa", "qa-only.json"),
    "change-delivery-preflight": ("ship_release/result.json", "preflight", "ship-release.json"),
    "feedback-and-continuous-learning-loop": ("retro_to_requirements/result.json", "retro", "retro-to-requirements.json"),
}
SUITES = ("baseline", "candidate", "holdout", "mutation")

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def normalized_run(workspace: Path, slot_id: str, case_id: str, output: Path, *, duration_ms: float, tool_events: list, command_results: list, extra: dict | None = None) -> tuple[dict, dict]:
    run = {
        "slot_id": slot_id, "case_id": case_id, "duration_ms": duration_ms,
        "tool_events": tool_events, "command_results": command_results,
        "output_file": output.relative_to(workspace).as_posix(),
    }
    if extra:
        run.update(extra)
    case = {
        "case_id": case_id, "slot_id": slot_id, "passed": True,
        "input_sha256": hashlib.sha256(case_id.encode()).hexdigest(),
        "output_sha256": digest(output),
    }
    return run, case

def run(workspace: Path) -> dict:
    evaluation = workspace / "evals/runs/full-dev-loop/ip-rate-limiting-v1"
    actual = evaluation / "run"
    root = evaluation / "slot-evaluations"
    failures: list[str] = []
    for slot_id, (result_rel, step_id, recipe_name) in CONFIG.items():
        slot_root = root / slot_id
        runs = slot_root / "runs"
        reports: dict[str, list[dict]] = {suite: [] for suite in SUITES}

        # Baseline: execute an immutable git read of the pre-release draft and observe non-executable status.
        started = time.perf_counter()
        process = subprocess.run(["git", "show", f"1979516:slots/{slot_id}/contract.json"], cwd=workspace, capture_output=True, text=True, encoding="utf-8", check=False)
        baseline_output = runs / "baseline-draft-contract.json"
        baseline_output.parent.mkdir(parents=True, exist_ok=True)
        baseline_output.write_text(process.stdout, encoding="utf-8")
        baseline = json.loads(process.stdout) if process.returncode == 0 else {}
        passed = process.returncode == 0 and baseline.get("status") == "draft" and baseline.get("version") == "0.0.0-draft"
        run_record, case = normalized_run(workspace, slot_id, "baseline-draft-is-not-executable", baseline_output, duration_ms=round((time.perf_counter()-started)*1000,3), tool_events=[], command_results=[{"argv": ["git", "show", f"1979516:slots/{slot_id}/contract.json"], "returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}], extra={"observed_status": baseline.get("status")})
        case["passed"] = passed
        run_path = runs / "baseline-draft-is-not-executable.json"; write_json(run_path, run_record); case["run_path"] = run_path.relative_to(workspace).as_posix(); reports["baseline"].append(case)

        # Candidate: bind the actual full-loop model output and execution record.
        actual_result = json.loads((actual / result_rel).read_text(encoding="utf-8"))
        step = next(item for item in actual_result["steps_run"] if item["step_id"] == step_id)
        output = workspace / step["output_file"]
        execution = step.get("execution", {})
        run_record, case = normalized_run(workspace, slot_id, "real-ip-rate-limit", output, duration_ms=step["duration_ms"], tool_events=execution.get("tool_events", []), command_results=execution.get("command_results", []), extra={"source_result": (actual/result_rel).relative_to(workspace).as_posix(), "gates": step.get("gates", [])})
        case["input_sha256"] = step["input_sha256"]; case["passed"] = step["status"] == "passed" and all(item.get("passed") for item in step.get("gates", []))
        run_path = runs / "candidate-real-ip-rate-limit.json"; write_json(run_path, run_record); case["run_path"] = run_path.relative_to(workspace).as_posix(); reports["candidate"].append(case)

        # Holdout: execute the real candidate recipe with an empty input; it must fail closed as needs-input without a model call.
        holdout_input = runs / "holdout-input.json"; write_json(holdout_input, {})
        holdout_run_dir = runs / "holdout-run"
        started = time.perf_counter()
        result = execute_recipe(workspace / "evals/candidates/full-dev-loop/recipes" / recipe_name, holdout_input, holdout_run_dir, workspace_root=workspace, allow_evaluating=True)
        duration = round((time.perf_counter()-started)*1000,3)
        holdout_output = runs / "holdout-missing-input-output.json"; write_json(holdout_output, result)
        run_record, case = normalized_run(workspace, slot_id, "missing-required-input", holdout_output, duration_ms=duration, tool_events=[], command_results=[{"argv": ["execute_recipe", recipe_name], "returncode": 1, "observed_status": result.get("status")}], extra={"observed_status": result.get("status")})
        case["passed"] = result.get("status") == "needs-input" and result.get("passed") is False
        run_path = runs / "holdout-missing-required-input.json"; write_json(run_path, run_record); case["run_path"] = run_path.relative_to(workspace).as_posix(); reports["holdout"].append(case)

        # Mutations: recompute every declared deterministic gate against actual text with one required structure removed.
        text = output.read_text(encoding="utf-8")
        mutations = {
            "remove-status": "\n".join(text.splitlines()[1:]),
            "remove-evidence": text.replace("Evidence:", "Record:").replace("## Evidence", "## Record"),
            "remove-gate-results": text.replace("Gate Results:", "Checks:").replace("## Gate Results", "## Checks"),
            "remove-responsibility": text.replace("responsibility", "scope").replace("Responsibility", "Scope"),
            "remove-authority": text.replace("authority", "scope").replace("Authority", "Scope"),
        }
        declared = json.loads((workspace / "slots" / slot_id / "contract.json").read_text(encoding="utf-8"))["gates"]
        for mutation, mutated in mutations.items():
            started = time.perf_counter()
            status_ok = _status(mutated) is not None
            gates = evaluate_gates(declared, mutated, {})
            detected = not status_ok or any(item.get("passed") is not True for item in gates)
            mutated_output = runs / f"mutation-{mutation}.md"; mutated_output.write_text(mutated, encoding="utf-8")
            run_record, case = normalized_run(workspace, slot_id, mutation, mutated_output, duration_ms=round((time.perf_counter()-started)*1000,3), tool_events=[], command_results=[{"argv": ["in-process", "slot-gate", mutation], "returncode": 0 if detected else 1}], extra={"status_valid": status_ok, "gates": gates, "mutation_detected": detected})
            case["passed"] = detected
            run_path = runs / f"mutation-{mutation}.json"; write_json(run_path, run_record); case["run_path"] = run_path.relative_to(workspace).as_posix(); reports["mutation"].append(case)

        for suite, cases in reports.items():
            report = {"slot_id": slot_id, "suite": suite, "passed": bool(cases) and all(case["passed"] for case in cases), "cases": cases}
            write_json(slot_root / f"{suite}.json", report)
            if not report["passed"]:
                failures.append(f"{slot_id}/{suite}")
    return {"gate": "full-dev-loop-slot-evaluations", "ok": not failures, "slot_count": len(CONFIG), "suite_count": len(CONFIG)*len(SUITES), "failures": failures}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args=parser.parse_args()
    result=run(args.workspace_root.resolve()); print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0 if result["ok"] else 1

if __name__ == "__main__": raise SystemExit(main())
