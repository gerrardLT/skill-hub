#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "l5b_matched_experiment.py"
spec = importlib.util.spec_from_file_location("l5b", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load L5-B harness")
l5b = importlib.util.module_from_spec(spec)
sys.modules["l5b"] = l5b
spec.loader.exec_module(l5b)

OUTPUT = Path(__file__).resolve().parent / "synthetic-matched.json"
REPORT = Path(__file__).resolve().parent / "SYNTHETIC_SMOKE_REPORT.md"
RESULT = Path(__file__).resolve().parent / "synthetic-result.json"


def main() -> int:
    exp = l5b.new_experiment(
        "Agentic SDLC OS v2.3 harness smoke",
        target_pairs=5,
        seed=20260831,
        hypothesis="The harness can preserve preregistration, blinding, matched records, integrity and analysis boundaries.",
        synthetic=True,
    )
    domains = ["web", "mobile", "ai-agent", "brownfield", "finance"]
    for index, domain in enumerate(domains, 1):
        l5b.add_task(exp, f"task-{index}", f"{index:064x}", domain, min(5, index), 60)
    l5b.freeze(exp)
    for index in range(1, 6):
        baseline = {
            "lead_time_minutes": 100 + index * 2,
            "human_minutes": 80 + index,
            "token_cost_usd": 5.0 + index * 0.1,
            "rework_fraction": 0.24,
            "escaped_defects": 4,
            "critical_defects": 1,
            "trace_coverage": 0.58,
            "acceptance_pass_rate": 0.74,
            "maintainability_score": 6.0,
        }
        sdlc = {
            "lead_time_minutes": 78 + index,
            "human_minutes": 62 + index,
            "token_cost_usd": 4.7 + index * 0.1,
            "rework_fraction": 0.12,
            "escaped_defects": 2,
            "critical_defects": 0,
            "trace_coverage": 0.91,
            "acceptance_pass_rate": 0.94,
            "maintainability_score": 8.1,
        }
        metrics_by_arm = {"baseline": baseline, "sdlc": sdlc}
        assignment = l5b.assignment_for(exp, f"task-{index}")
        for position, arm in enumerate(assignment["order"]):
            l5b.record_run(
                exp,
                task_id=f"task-{index}",
                arm=arm,
                executor_code=f"synthetic-{arm}",
                execution_context_id=f"synthetic-context-{index}-{arm}-{position}",
                model="controlled-model-family",
                prompt_hash=("a" if arm == "baseline" else "b") * 64,
                toolset_hash="c" * 64,
                start_state_hash=f"{index:064x}",
                environment_hash="9" * 64,
                artifact_hash=("d" if arm == "baseline" else "e") * 64,
                run_log_hash=("f" if arm == "baseline" else "8") * 64,
                metrics=metrics_by_arm[arm],
            )
    for assignment in exp["assignments"]:
        for arm in sorted(l5b.ARMS):
            code = assignment["blind_artifact_codes"][arm]
            score = 7.0 if arm == "baseline" else 8.5
            l5b.add_review(
                exp,
                blind_artifact_code=code,
                reviewer_code="synthetic-blind-reviewer",
                correctness=score,
                completeness=score,
                maintainability=score,
                usability=score,
                notes="Synthetic harness smoke; not real effectiveness evidence.",
            )
    l5b.seal(exp)
    errors = l5b.validate(exp)
    if errors:
        raise RuntimeError("Synthetic experiment invalid: " + "; ".join(errors))
    result = l5b.analyze(exp)
    if result["decision"] != "synthetic-smoke-only":
        raise RuntimeError("Synthetic boundary failed")
    l5b.atomic_write(OUTPUT, exp)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(l5b.report_markdown(exp, result), encoding="utf-8")
    print(json.dumps({"valid": True, "decision": result["decision"], "pairs": result["complete_pairs"], "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
