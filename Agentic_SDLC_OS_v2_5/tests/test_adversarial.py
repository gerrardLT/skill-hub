from __future__ import annotations

import json
import unittest
from pathlib import Path

from test_sdlc import ROOT, SDLCBase, future_iso, sdlc


class TestAdversarialControls(SDLCBase):
    def test_accepted_missing_artifact_is_rejected(self):
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", "missing", "--type", "product-brief",
            "--path", "does-not-exist.md", "--status", "accepted",
        ])
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err)

    def test_duplicate_evidence_does_not_satisfy_gate(self):
        spec = json.loads((ROOT / "manifest" / "gates.json").read_text())["pm-ready"]
        ids = [self.create_and_register(t) for t in spec["required"]]
        self.trace_all(ids)
        for index, quality in enumerate(["high", "medium", "medium"]):
            self.add_evidence(
                f"dup-{index}", ids[0], quality=quality,
                source="same-source", claim="same-claim",
            )
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        result = json.loads(out)
        self.assertEqual(code, 2)
        self.assertEqual(result["evidence_count"], 1)
        self.assertEqual(len(result["duplicate_evidence"]), 2)

    def test_artifact_tampering_invalidates_gate(self):
        ids = self.satisfy_gate("pm-ready")
        code, _, err = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 0, err)
        artifact = self.state()["artifacts"][ids[0]]
        path = self.root / artifact["path"]
        path.write_text(path.read_text(encoding="utf-8") + "\nunaudited change\n", encoding="utf-8")
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        result = json.loads(out)
        self.assertEqual(code, 2)
        issues = [issue for item in result["invalid_artifacts"] for issue in item["issues"]]
        self.assertIn("content_changed_since_acceptance", issues)

    def test_forward_stage_skip_is_blocked(self):
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-stage", "HANDOFF", "--reason", "skip everything",
        ])
        self.assertEqual(code, 2)
        self.assertIn("Cannot skip stages", err)

    def test_force_requires_human_approval(self):
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "release", "--to-stage", "ROLLOUT",
            "--reason", "emergency", "--force",
        ])
        self.assertEqual(code, 2)
        self.assertIn("human approver", err)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "release", "--to-stage", "ROLLOUT",
            "--reason", "emergency", "--force", "--approver", "AI Agent", "--approval-id", "CR-X",
        ])
        self.assertEqual(code, 2)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "release", "--to-stage", "ROLLOUT",
            "--reason", "emergency", "--force", "--approver", "Ravi Patel", "--approval-id", "CR-900",
        ])
        self.assertEqual(code, 0, err)

    def test_ai_approver_cannot_waive_gate(self):
        code, _, err = self.run_cli([
            "gate", str(self.root), "--name", "pm-ready", "--waive", "--reason", "fast",
            "--approver", "ChatGPT Agent", "--approval-id", "CR-1",
            "--compensating-control", "manual review", "--expires", future_iso(1),
        ])
        self.assertEqual(code, 2)
        self.assertIn("human approver", err)

    def test_critical_risk_is_nonwaivable(self):
        self.run_cli([
            "add-risk", str(self.root), "--id", "critical-1", "--title", "data corruption",
            "--severity", "critical", "--mitigation", "restore backup",
        ])
        code, _, err = self.run_cli([
            "gate", str(self.root), "--name", "pm-ready", "--waive", "--reason", "fast",
            "--approver", "Ravi Patel", "--approval-id", "CR-2",
            "--compensating-control", "manual review", "--expires", future_iso(1),
        ])
        self.assertEqual(code, 2)
        self.assertIn("non-waivable", err)

    def test_waiver_is_invalidated_by_relevant_state_change(self):
        code, _, err = self.create_waiver()
        self.assertEqual(code, 0, err)
        self.create_and_register("product-brief", "changed-snapshot")
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "design", "--to-stage", "INTAKE", "--reason", "use stale waiver",
        ])
        self.assertEqual(code, 2)
        self.assertIn("pm-ready", err)

    def test_path_traversal_is_rejected(self):
        code, _, err = self.run_cli([
            "new-artifact", str(self.root), "--id", "evil", "--type", "prd", "--filename", "../../escape.md",
        ])
        self.assertEqual(code, 2)
        self.assertIn("escapes", err)
        self.assertFalse((self.root / "escape.md").exists())

    def test_external_accepted_artifact_requires_checksum(self):
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", "external", "--type", "prd",
            "--path", "https://example.com/prd", "--status", "accepted",
        ])
        self.assertEqual(code, 2)
        self.assertIn("checksum", err)
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", "external", "--type", "prd",
            "--path", "https://example.com/prd", "--status", "accepted", "--checksum", "a" * 64,
        ])
        self.assertEqual(code, 0, err)

    def test_high_quality_opinion_is_not_high_quality_gate_evidence(self):
        spec = json.loads((ROOT / "manifest" / "gates.json").read_text())["pm-ready"]
        ids = [self.create_and_register(t) for t in spec["required"]]
        self.trace_all(ids)
        for index in range(3):
            code, _, err = self.run_cli([
                "add-evidence", str(self.root), "--id", f"op-{index}", "--claim", f"opinion {index}",
                "--source", f"person-{index}", "--source-type", "opinion", "--quality", "high",
                "--supports", ids[index],
            ])
            self.assertEqual(code, 0, err)
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out)["high_quality_evidence_shortfall"], 1)

    def test_duplicate_record_id_is_rejected(self):
        self.add_evidence("same-id", "external:first")
        code, _, err = self.run_cli([
            "add-risk", str(self.root), "--id", "same-id", "--title", "duplicate",
            "--severity", "low", "--mitigation", "none",
        ])
        self.assertEqual(code, 2)
        self.assertIn("already exists", err)


    def test_risk_can_be_updated_and_closed(self):
        code, _, err = self.run_cli([
            "add-risk", str(self.root), "--id", "r-update", "--title", "temporary risk",
            "--severity", "high", "--status", "open", "--mitigation", "investigate",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "update-risk", str(self.root), "--id", "r-update", "--status", "closed",
            "--mitigation", "verified fix", "--owner", "Alice Chen",
        ])
        self.assertEqual(code, 0, err)
        risk = next(item for item in self.state()["risks"] if item["id"] == "r-update")
        self.assertEqual(risk["status"], "closed")
        self.assertEqual(risk["mitigation"], "verified fix")

    def test_self_trace_is_rejected(self):
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "self", "--from", "goal:x", "--to", "goal:x", "--relation", "supports",
        ])
        self.assertEqual(code, 2)
        self.assertIn("different", err)

    def test_router_benchmark(self):
        cases = json.loads((ROOT / "validation" / "benchmarks" / "router-cases.json").read_text(encoding="utf-8"))
        routing = json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))
        state = {
            "current_os": "pm",
            "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
        }
        routed = 0
        correct = 0
        errors = []
        for case in cases:
            result = sdlc.route_task(state, case["task"])
            if result["decision"] == "abstain":
                continue
            routed += 1
            if result["recommended_os"] == case["expected_os"]:
                correct += 1
            else:
                errors.append((case["expected_os"], result["recommended_os"], case["task"]))
        precision = correct / routed
        coverage = routed / len(cases)
        self.assertGreaterEqual(precision, 0.95, errors)
        self.assertGreaterEqual(coverage, 0.90)
        self.assertEqual(sdlc.route_task(state, "build a reliable backend service")["recommended_os"], "engineering")

    def test_router_holdout_never_auto_routes_wrong_domain(self):
        cases = json.loads((ROOT / "validation" / "benchmarks" / "router-holdout.json").read_text(encoding="utf-8"))
        routing = json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))
        state = {
            "current_os": "engineering",
            "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
        }
        unsafe = []
        for case in cases:
            result = sdlc.route_task(state, case["task"])
            if result["decision"] == "route" and result["recommended_os"] != case["expected_os"]:
                unsafe.append((case["expected_os"], result["recommended_os"], case["task"]))
            if result["decision"] == "abstain":
                self.assertIsNone(result["recommended_os"])
                self.assertIsNotNone(result["fallback_os"])
        self.assertFalse(unsafe, unsafe)

    def test_router_abstains_on_underspecified_task(self):
        routing = json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))
        state = {
            "current_os": "engineering",
            "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
        }
        result = sdlc.route_task(state, "继续处理这个问题")
        self.assertEqual(result["decision"], "abstain")
        self.assertIsNone(result["recommended_os"])
        self.assertEqual(result["fallback_os"], "engineering")

    def test_validate_detects_state_corruption(self):
        state_path = self.root / ".sdlc" / "state.json"
        state = self.state()
        state["current_stage"] = "NOT_A_STAGE"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        code, out, _ = self.run_cli(["validate", str(self.root), "--json"])
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(out)["valid"])


if __name__ == "__main__":
    unittest.main()
