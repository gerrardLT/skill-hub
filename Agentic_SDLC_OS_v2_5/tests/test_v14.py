from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "validation" / "l5" / "pilots" / "venue-reservation"


class TestV14Dogfood(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PILOT / relative).read_text(encoding="utf-8"))

    def test_real_project_pilot_verification_passes(self):
        result = self.load("reports/pilot-verification.json")
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(result["tests"]["coverage_percent"], 90.0)
        self.assertTrue(result["deployment"]["passed"])
        self.assertEqual(result["deployment"]["failed_checks"], [])
        self.assertFalse(result["performance"]["oversold"])
        self.assertEqual(result["performance"]["reserved"], result["performance"]["capacity"])

    def test_full_control_plane_traversal_has_no_bypass(self):
        result = self.load("reports/sdlc-dogfood-run.json")
        self.assertTrue(result["passed"])
        self.assertEqual(result["artifacts"], 42)
        self.assertEqual(result["quality"]["invalid"], 0)
        self.assertEqual(result["forced_transitions"], 0)
        self.assertEqual(result["waivers"], 0)
        self.assertEqual(result["final_state"], "pm/DISCOVERY")
        self.assertEqual({item["status"] for item in result["gates"].values()}, {"pass"})
        self.assertTrue(result["validation"]["valid"])
        self.assertTrue(result["audit"]["valid"])

    def test_deployment_smoke_covers_closed_loop(self):
        result = self.load("reports/deployment-smoke.json")
        self.assertTrue(result["passed"])
        names = {item["name"] for item in result["checks"] if item["passed"]}
        self.assertEqual(names, {
            "health", "create_session", "reserve_capacity", "idempotent_replay",
            "waitlist_on_full", "fifo_promotion", "no_oversell", "tenant_isolation",
        })

    def test_prototype_exposes_accessible_server_confirmed_states(self):
        html = (PILOT / "prototype" / "index.html").read_text(encoding="utf-8")
        css = (PILOT / "prototype" / "app.css").read_text(encoding="utf-8")
        js = (PILOT / "prototype" / "app.js").read_text(encoding="utf-8")
        self.assertIn('class="skip-link"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('aria-live="assertive"', html)
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("服务端确认中", js)
        self.assertIn("候补已自动转正", js)

    def test_report_does_not_overclaim_causality(self):
        report = (ROOT / "validation" / "l5" / "REAL_PROJECT_DOGFOOD_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("L5-A 真实项目单臂 Dogfooding：PASS", report)
        self.assertIn("L5-B 因果效果验证：尚未完成", report)
        self.assertIn("不能宣称", report)
        selection = (PILOT / "source" / "requirements-selection.md").read_text(encoding="utf-8")
        self.assertIn("SHA-256", selection)
        self.assertIn("D26", selection)
        self.assertIn("D33", selection)


if __name__ == "__main__":
    unittest.main()
