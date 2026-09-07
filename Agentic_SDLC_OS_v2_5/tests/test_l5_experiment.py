from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "l5_experiment.py"
spec = importlib.util.spec_from_file_location("l5", MODULE_PATH)
l5 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(l5)


def metrics(scale: float = 1.0, improved: bool = False):
    if not improved:
        return {
            "lead_time_hours": 100 * scale,
            "rework_rate": 0.30,
            "escaped_defects": 5,
            "incidents": 2,
            "rollback_rate": 0.20,
            "trace_coverage": 0.45,
            "evidence_decision_rate": 0.40,
            "goal_attainment": 0.55,
            "human_hours": 80,
            "token_cost_usd": 0,
            "actionability_score": 6.0,
        }
    return {
        "lead_time_hours": 75 * scale,
        "rework_rate": 0.18,
        "escaped_defects": 3,
        "incidents": 1,
        "rollback_rate": 0.10,
        "trace_coverage": 0.85,
        "evidence_decision_rate": 0.80,
        "goal_attainment": 0.72,
        "human_hours": 65,
        "token_cost_usd": 35,
        "actionability_score": 8.0,
    }


class TestL5Experiment(unittest.TestCase):
    def test_insufficient_data_is_not_overclaimed(self):
        exp = l5.new_experiment("demo", "historical-matched", 2, "test", synthetic=False)
        l5.add_iteration(exp, "baseline", "b1", "artifact-b1", metrics())
        l5.add_iteration(exp, "sdlc", "s1", "artifact-s1", metrics(improved=True))
        result = l5.analyze(exp)
        self.assertEqual(result["decision"], "insufficient-data")
        self.assertFalse(result["enough_data"])

    def test_positive_requires_multiple_categories_without_severe_regression(self):
        exp = l5.new_experiment("demo", "parallel", 2, "test", synthetic=True)
        for index in range(2):
            l5.add_iteration(exp, "baseline", f"b{index}", f"artifact-b{index}", metrics(1 + index * 0.05))
            l5.add_iteration(exp, "sdlc", f"s{index}", f"artifact-s{index}", metrics(1 + index * 0.05, improved=True))
        l5.add_review(exp, "artifact-b0", "r1", "A", 6, 6, 6)
        l5.add_review(exp, "artifact-s0", "r1", "B", 8, 8, 8)
        result = l5.analyze(exp)
        self.assertEqual(result["decision"], "positive")
        self.assertTrue(result["enough_data"])
        self.assertFalse(result["severe_regressions"])
        self.assertGreaterEqual(len(result["primary_categories_improved"]), 2)

    def test_severe_quality_regression_forces_negative(self):
        exp = l5.new_experiment("demo", "parallel", 2, "test")
        for index in range(2):
            baseline = metrics()
            treatment = metrics(improved=True)
            treatment["incidents"] = 5
            l5.add_iteration(exp, "baseline", f"b{index}", f"b{index}", baseline)
            l5.add_iteration(exp, "sdlc", f"s{index}", f"s{index}", treatment)
        result = l5.analyze(exp)
        self.assertEqual(result["decision"], "negative")
        self.assertIn("incidents", result["severe_regressions"])

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "experiment.json"
            self.assertEqual(l5.main(["init", str(path), "--project", "demo", "--synthetic"]), 0)
            self.assertTrue(path.exists())
            self.assertEqual(l5.main(["validate", str(path), "--json"]), 0)


if __name__ == "__main__":
    unittest.main()
