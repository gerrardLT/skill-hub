from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "l5b_matched_experiment.py"
spec = importlib.util.spec_from_file_location("v20_l5b", PATH)
assert spec and spec.loader
l5b = importlib.util.module_from_spec(spec)
sys.modules["v20_l5b"] = l5b
spec.loader.exec_module(l5b)


class L5BCase(unittest.TestCase):
    def make_experiment(self, *, synthetic: bool = True, contamination: str = "none", seal: bool = False):
        exp = l5b.new_experiment("matched-test", 5, 42, "SDLC improves delivery", synthetic)
        sha = "a" * 64
        for index in range(5):
            l5b.add_task(exp, f"task-{index}", sha[:-1] + str(index), "web", 3, 60)
        l5b.freeze(exp)
        for index in range(5):
            base = {
                "lead_time_minutes": 100 + index,
                "human_minutes": 80 + index,
                "token_cost_usd": 5.0,
                "rework_fraction": 0.25,
                "escaped_defects": 4,
                "critical_defects": 1,
                "trace_coverage": 0.60,
                "acceptance_pass_rate": 0.75,
                "maintainability_score": 6.0,
            }
            improved = {
                "lead_time_minutes": 75 + index,
                "human_minutes": 60 + index,
                "token_cost_usd": 4.5,
                "rework_fraction": 0.12,
                "escaped_defects": 2,
                "critical_defects": 0,
                "trace_coverage": 0.92,
                "acceptance_pass_rate": 0.95,
                "maintainability_score": 8.0,
            }
            metrics_by_arm = {"baseline": base, "sdlc": improved}
            assignment = l5b.assignment_for(exp, f"task-{index}")
            for position, arm in enumerate(assignment["order"]):
                l5b.record_run(
                    exp,
                    task_id=f"task-{index}",
                    arm=arm,
                    executor_code=f"executor-{arm}",
                    execution_context_id=f"ctx-{index}-{arm}-{position}",
                    model="same-model",
                    prompt_hash=("b" if arm == "baseline" else "c") * 64,
                    toolset_hash="d" * 64,
                    start_state_hash=f"{index + 1:064x}",
                    environment_hash="e" * 64,
                    artifact_hash=("f" if arm == "baseline" else "1") * 64,
                    run_log_hash=("2" if arm == "baseline" else "3") * 64,
                    metrics=metrics_by_arm[arm],
                    contamination=contamination if index == 0 and arm == "sdlc" else "none",
                )
        for assignment in exp["assignments"]:
            for arm in sorted(l5b.ARMS):
                l5b.add_review(
                    exp,
                    blind_artifact_code=assignment["blind_artifact_codes"][arm],
                    reviewer_code="blind-reviewer",
                    correctness=8,
                    completeness=8,
                    maintainability=8,
                    usability=8,
                )
        if seal:
            l5b.seal(exp)
        return exp

    def test_preregistration_chain_blinding_order_and_synthetic_boundary(self) -> None:
        exp = self.make_experiment(synthetic=True)
        self.assertFalse(l5b.validate(exp))
        result = l5b.analyze(exp)
        self.assertEqual(result["decision"], "synthetic-smoke-only")
        self.assertEqual(result["complete_pairs"], 5)
        self.assertTrue(result["improved_primary_categories"])
        codes = [code for item in exp["assignments"] for code in item["blind_artifact_codes"].values()]
        self.assertEqual(len(codes), len(set(codes)))
        baseline_first = sum(item["order"][0] == "baseline" for item in exp["assignments"])
        sdlc_first = sum(item["order"][0] == "sdlc" for item in exp["assignments"])
        self.assertLessEqual(abs(baseline_first - sdlc_first), 1)

    def test_real_requires_seal_for_formal_positive(self) -> None:
        real = self.make_experiment(synthetic=False)
        provisional = l5b.analyze(real)
        self.assertEqual(provisional["decision"], "provisional-positive")
        self.assertFalse(provisional["formal_evidence_eligible"])
        l5b.seal(real)
        result = l5b.analyze(real)
        self.assertEqual(result["decision"], "positive")
        self.assertTrue(result["formal_evidence_eligible"])
        with self.assertRaises(RuntimeError):
            l5b.add_review(real, blind_artifact_code=real["assignments"][0]["blind_artifact_codes"]["baseline"], reviewer_code="late", correctness=8, completeness=8, maintainability=8, usability=8)

    def test_contamination_and_control_mismatch_invalidate(self) -> None:
        contaminated = self.make_experiment(synthetic=False, contamination="executor-learned-other-arm")
        self.assertEqual(l5b.analyze(contaminated)["decision"], "invalid-contamination")
        with self.assertRaises(RuntimeError):
            l5b.seal(contaminated)

        mismatch = self.make_experiment(synthetic=False)
        task = mismatch["runs"][0]["task_id"]
        paired = [run for run in mismatch["runs"] if run["task_id"] == task]
        paired[1]["model"] = "different-model"
        # Rebuild chain after deliberate semantic mutation to isolate control validation.
        mismatch["record_chain_head"] = "GENESIS"
        previous = "GENESIS"
        for run in mismatch["runs"]:
            run["previous_hash"] = previous
            run["record_hash"] = l5b.digest({k: v for k, v in run.items() if k != "record_hash"})
            previous = run["record_hash"]
        mismatch["record_chain_head"] = previous
        self.assertEqual(l5b.analyze(mismatch)["decision"], "invalid-controls")

    def test_tamper_and_preregistration_mutation_are_detected(self) -> None:
        exp = self.make_experiment()
        exp["runs"][0]["metrics"]["lead_time_minutes"] = 999
        errors = l5b.validate(exp)
        self.assertTrue(any("record_hash mismatch" in item for item in errors))
        exp2 = self.make_experiment()
        exp2["tasks"][0]["domain"] = "tampered"
        errors2 = l5b.validate(exp2)
        self.assertIn("preregistration hash mismatch", errors2)
        with self.assertRaises(RuntimeError):
            l5b.add_task(exp2, "late-task", "1" * 64, "web", 2, 10)

    def test_run_order_and_context_reuse_are_blocked(self) -> None:
        exp = l5b.new_experiment("order", 3, 7, "h", True)
        for index in range(3):
            l5b.add_task(exp, f"t{index}", f"{index + 1:064x}", "web", 2, 10)
        l5b.freeze(exp)
        assignment = l5b.assignment_for(exp, "t0")
        wrong_arm = assignment["order"][1]
        metrics = {name: (0.5 if "fraction" in name or "coverage" in name or "rate" in name else 1.0) for name in l5b.METRICS}
        metrics["maintainability_score"] = 5.0
        with self.assertRaises(RuntimeError):
            l5b.record_run(exp, task_id="t0", arm=wrong_arm, executor_code="e", execution_context_id="ctx", model="m", prompt_hash="1"*64, toolset_hash="2"*64, start_state_hash="3"*64, environment_hash="4"*64, artifact_hash="5"*64, run_log_hash="6"*64, metrics=metrics)


if __name__ == "__main__":
    unittest.main()
