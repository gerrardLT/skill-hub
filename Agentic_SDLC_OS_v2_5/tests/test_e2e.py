from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_sdlc import ROOT, SDLCBase


class TestEndToEndWorkflows(SDLCBase):
    def stages(self):
        return json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))["os_stages"]

    def advance_to_last_stage(self, os_name: str):
        stages = self.stages()[os_name]
        state = self.state()
        self.assertEqual(state["current_os"], os_name)
        index = stages.index(state["current_stage"])
        for stage in stages[index + 1:]:
            code, _, err = self.run_cli([
                "transition", str(self.root), "--to-os", os_name, "--to-stage", stage,
                "--reason", f"complete {os_name}/{stage}",
            ])
            self.assertEqual(code, 0, f"{os_name}/{stage}: {err}")

    def handoff(self, target_os: str):
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", target_os, "--to-stage", "INTAKE",
            "--reason", f"handoff to {target_os}",
        ])
        self.assertEqual(code, 0, err)

    def test_greenfield_full_lifecycle_and_learning_reentry(self):
        self.satisfy_gate("pm-ready")
        self.advance_to_last_stage("pm")
        self.handoff("design")

        self.satisfy_gate("design-ready")
        self.advance_to_last_stage("design")
        self.handoff("engineering")

        self.satisfy_gate("build-ready")
        stages = self.stages()["engineering"]
        for stage in stages[1:]:
            code, _, err = self.run_cli([
                "transition", str(self.root), "--to-os", "engineering", "--to-stage", stage,
                "--reason", f"complete engineering/{stage}",
            ])
            if stage == "HANDOFF" and code != 0:
                # verification-ready is intentionally satisfied just before handoff.
                self.satisfy_gate("verification-ready")
                code, _, err = self.run_cli([
                    "transition", str(self.root), "--to-os", "engineering", "--to-stage", stage,
                    "--reason", f"complete engineering/{stage}",
                ])
            self.assertEqual(code, 0, f"engineering/{stage}: {err}")
        # verification-ready is a cross-OS gate, not an internal stage gate.
        if "verification-ready-source-change" not in self.state()["artifacts"]:
            self.satisfy_gate("verification-ready")
        self.handoff("qa")

        self.satisfy_gate("release-ready")
        self.advance_to_last_stage("qa")
        self.handoff("release")

        self.satisfy_gate("production-ready")
        self.advance_to_last_stage("release")
        self.handoff("evolution")

        self.satisfy_gate("learning-decision")
        self.advance_to_last_stage("evolution")
        code, _, err = self.run_cli([
            "learn", str(self.root), "--expected", "activation +10%", "--actual", "activation +2%",
            "--gap", "target segment mismatch", "--gap-type", "strategy",
            "--decision", "return to discovery", "--route-os", "pm", "--route-stage", "DISCOVERY",
            "--evidence", "learning-decision-ev-0",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "pm", "--to-stage", "DISCOVERY",
            "--reason", "production evidence invalidated the ICP assumption",
        ])
        self.assertEqual(code, 0, err)

        code, out, err = self.run_cli(["validate", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertTrue(result["valid"], result)
        state = self.state()
        self.assertEqual((state["current_os"], state["current_stage"]), ("pm", "DISCOVERY"))
        self.assertTrue(state["history"][-1]["rework"])
        self.assertFalse(any(x.get("forced") for x in state["history"] if isinstance(x, dict)))

    def test_incident_project_starts_in_evolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, _, err = self.run_cli([
                "init", str(root), "--name", "incident", "--type", "incident", "--criticality", "high",
            ])
            self.assertEqual(code, 0, err)
            state = self.state(root)
            self.assertEqual(state["current_os"], "evolution")
            code, out, err = self.run_cli([
                "route", str(root), "线上严重故障，先止损并回滚", "--json",
            ])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["recommended_os"], "evolution")

    def test_brownfield_project_starts_in_engineering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, _, err = self.run_cli([
                "init", str(root), "--name", "legacy", "--type", "brownfield", "--criticality", "medium",
            ])
            self.assertEqual(code, 0, err)
            self.assertEqual(self.state(root)["current_os"], "engineering")


if __name__ == "__main__":
    unittest.main()
