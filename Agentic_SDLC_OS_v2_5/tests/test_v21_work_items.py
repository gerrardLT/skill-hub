from __future__ import annotations

import json
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))
from test_sdlc import SDLCBase


class TestV21WorkItems(SDLCBase):
    def make_high_assurance_ai_project(self) -> None:
        state = self.state()
        state["project"]["criticality"] = "high"
        state["project"]["profile"] = "high-assurance"
        state["current_os"] = "engineering"
        state["current_stage"] = "INTAKE"
        for os_name, entry in state["os_states"].items():
            entry["status"] = "active" if os_name == "engineering" else "pending"
        state["os_states"]["engineering"]["stage"] = "INTAKE"
        (self.root / ".sdlc" / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        config_path = self.root / ".sdlc" / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        pack = json.loads((Path(__file__).resolve().parents[1] / "domain-packs" / "ai-agent" / "pack.json").read_text(encoding="utf-8"))
        config.update({
            "process_profile": "high-assurance",
            "domain_packs": ["ai-agent"],
            "domain_gate_overlays": pack["gate_overlays"],
            "domain_required_evidence": pack["required_evidence"],
        })
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    def test_bounded_low_risk_change_can_downgrade_high_assurance_project(self):
        self.make_high_assurance_ai_project()
        code, out, err = self.run_cli([
            "work-start", str(self.root), "--title", "replace npm mirror in lockfile", "--bounded",
            "--affected-path", "web/package-lock.json", "--json",
        ])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["profile"], "lite")
        self.assertEqual(payload["criticality"], "low")
        self.assertEqual(payload["domain_impacts"], [])

        code, out, err = self.run_cli(["gate", str(self.root), "--name", "build-ready", "--json"])
        self.assertEqual(code, 2, err)
        gate = json.loads(out)
        self.assertEqual(gate["profile"], "lite")
        self.assertEqual(gate["project_profile"], "high-assurance")
        self.assertNotIn("threat-model", gate["required"])
        self.assertNotIn("capacity-plan", gate["required"])
        self.assertEqual(gate["domain_required_artifacts"], [])

    def test_unbounded_work_cannot_downgrade_project_profile(self):
        self.make_high_assurance_ai_project()
        code, out, err = self.run_cli([
            "work-start", str(self.root), "--title", "general cleanup", "--affected-path", "backend/cleanup.py", "--json",
        ])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["profile"], "high-assurance")

    def test_protected_path_escalates_bounded_lite_work_to_standard(self):
        self.make_high_assurance_ai_project()
        code, out, err = self.run_cli([
            "work-start", str(self.root), "--title", "adjust CI", "--bounded",
            "--affected-path", ".github/workflows/ci.yml", "--json",
        ])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["profile"], "standard")
        self.assertIn("protected-path>=standard", payload["hard_escalations"])

    def test_domain_overlay_applies_only_when_work_impacts_domain(self):
        self.make_high_assurance_ai_project()
        code, out, err = self.run_cli([
            "work-start", str(self.root), "--title", "change agent prompt routing", "--bounded",
            "--affected-path", "backend/agent/orchestrator.py", "--json",
        ])
        self.assertEqual(code, 0, err)
        self.assertIn("ai-agent", json.loads(out)["domain_impacts"])
        code, out, err = self.run_cli(["gate", str(self.root), "--name", "verification-ready", "--json"])
        self.assertEqual(code, 2, err)
        gate = json.loads(out)
        self.assertIn("eval-plan", gate["domain_required_artifacts"])
        self.assertIn("prompt-threat-model", gate["domain_required_artifacts"])

    def test_project_and_previous_work_artifacts_do_not_satisfy_active_work_gate(self):
        self.make_high_assurance_ai_project()
        # Register before any work item; it is project-scoped and must not satisfy a change-scoped gate.
        self.create_and_register("change-plan", artifact_id="project-change-plan")
        code, _, err = self.run_cli([
            "work-start", str(self.root), "--title", "lockfile repair", "--bounded",
            "--affected-path", "web/package-lock.json",
        ])
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["gate", str(self.root), "--name", "build-ready", "--json"])
        self.assertEqual(code, 2, err)
        self.assertIn("change-plan", json.loads(out)["missing_artifacts"])

        # Add a work-scoped artifact, close the work, then start another work item.
        self.create_and_register("change-plan", artifact_id="work1-change-plan")
        code, _, err = self.run_cli(["work-end", str(self.root), "--status", "completed", "--outcome", "fixture"])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "work-start", str(self.root), "--title", "second lockfile repair", "--bounded",
            "--affected-path", "web/package-lock.json",
        ])
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["gate", str(self.root), "--name", "build-ready", "--json"])
        self.assertEqual(code, 2, err)
        self.assertIn("change-plan", json.loads(out)["missing_artifacts"])

    def test_trace_and_quality_use_artifact_work_profile(self):
        self.make_high_assurance_ai_project()
        code, _, err = self.run_cli([
            "work-start", str(self.root), "--title", "small lockfile repair", "--bounded",
            "--affected-path", "web/package-lock.json",
        ])
        self.assertEqual(code, 0, err)
        source = self.create_and_register("change-plan", artifact_id="lite-change-plan")
        target = self.create_and_register("test-plan", artifact_id="lite-test-plan")
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "lite-trace", "--from", source, "--to", target, "--relation", "supports",
        ])
        self.assertEqual(code, 0, err)
        state = self.state()
        self.assertFalse(state["artifacts"][target].get("stale", False))
        code, out, err = self.run_cli(["quality", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["invalid"], 0)
        code, _, err = self.run_cli(["work-end", str(self.root), "--status", "completed", "--outcome", "fixture"])
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["quality", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["invalid"], 0)
        profiles = {item["id"]: item["governance_profile"] for item in payload["artifacts"]}
        self.assertEqual(profiles[source], "lite")
        self.assertEqual(profiles[target], "lite")

    def test_bounded_lite_work_compresses_stage_machine(self):
        self.make_high_assurance_ai_project()
        code, _, err = self.run_cli([
            "work-start", str(self.root), "--title", "small lockfile repair", "--bounded",
            "--affected-path", "web/package-lock.json",
        ])
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["next", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["kind"], "gate")
        self.assertEqual(payload["target_stage"], "BUILD")
        self.assertEqual(payload["gate"], "build-ready")


if __name__ == "__main__":
    import unittest
    unittest.main()
