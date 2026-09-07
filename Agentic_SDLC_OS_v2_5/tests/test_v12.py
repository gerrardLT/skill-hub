from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_sdlc import ROOT, SDLCBase, sdlc


class TestV12Controls(SDLCBase):
    def test_lite_profile_reduces_required_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, _, err = self.run_cli([
                "init", str(root), "--name", "lite", "--criticality", "low",
            ])
            self.assertEqual(code, 0, err)
            state = self.state(root)
            self.assertEqual(state["project"]["profile"], "lite")
            gates = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
            lite = sdlc.resolve_gate_spec(gates["pm-ready"], "lite", "low")
            standard = sdlc.resolve_gate_spec(gates["pm-ready"], "standard", "medium")
            self.assertLess(len(lite["required"]), len(standard["required"]))
            self.satisfy_gate("pm-ready", root=root)
            code, out, err = self.run_cli(["gate", str(root), "--name", "pm-ready", "--json"])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["profile"], "lite")

    def test_high_criticality_rejects_lite_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = self.run_cli([
                "init", tmp, "--name", "unsafe", "--criticality", "high", "--profile", "lite",
            ])
            self.assertEqual(code, 2)
            self.assertIn("cannot use", err)

    def test_arbitrary_trace_coverage_does_not_satisfy_directed_paths(self):
        gates = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
        spec = sdlc.resolve_gate_spec(gates["pm-ready"], "standard", "medium")
        ids_by_type = {
            item: self.create_and_register(item, f"arbitrary-{item}") for item in spec["required"]
        }
        for index, artifact_id in enumerate(ids_by_type.values()):
            code, _, err = self.run_cli([
                "trace", str(self.root), "--id", f"arbitrary-trace-{index}",
                "--from", artifact_id, "--to", "goal:pm-ready", "--relation", "supports",
            ])
            self.assertEqual(code, 0, err)
        total = max(
            int(spec.get("minimum_evidence", 0)),
            int(spec.get("minimum_distinct_sources", 0)),
            int(spec.get("minimum_evidence_targets", 0)),
        )
        artifact_ids = list(ids_by_type.values())
        for index in range(total):
            self.add_evidence(
                f"arbitrary-ev-{index}", artifact_ids[index % len(artifact_ids)],
                "high" if index < int(spec.get("minimum_high_quality_evidence", 0)) else "medium",
                source=f"arbitrary-source-{index}",
            )
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        result = json.loads(out)
        self.assertEqual(code, 2)
        self.assertEqual(result["trace_coverage"], 1.0)
        self.assertLess(result["trace_path_coverage"], result["minimum_trace_path_coverage"])

    def test_trace_validation_rejects_invalid_and_duplicate_edges(self):
        a = self.create_and_register("product-brief", "trace-a")
        b = self.create_and_register("prd", "trace-b")
        code, _, err = self.run_cli([
            "trace", str(self.root), "--from", "missing-node", "--to", b, "--relation", "supports",
        ])
        self.assertEqual(code, 2)
        self.assertIn("Invalid trace source", err)
        code, _, err = self.run_cli([
            "trace", str(self.root), "--from", a, "--to", b, "--relation", "invented",
        ])
        self.assertEqual(code, 2)
        self.assertIn("Invalid trace relation", err)
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "valid-edge", "--from", a, "--to", b, "--relation", "derives",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "duplicate-edge", "--from", a, "--to", b, "--relation", "derives",
        ])
        self.assertEqual(code, 2)
        self.assertIn("Duplicate trace edge", err)

    def test_audit_chain_detects_event_and_state_tampering(self):
        code, out, err = self.run_cli(["audit", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)["valid"])
        audit_path = self.root / ".sdlc" / "audit" / "events.jsonl"
        lines = audit_path.read_text(encoding="utf-8").splitlines()
        first = json.loads(lines[0])
        first["event"] = "tampered"
        lines[0] = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        code, out, _ = self.run_cli(["audit", str(self.root), "--json"])
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(out)["valid"])

    def test_health_caps_score_on_critical_risk(self):
        code, out, err = self.run_cli(["health", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        baseline = json.loads(out)
        self.assertFalse(baseline["hard_fails"])
        code, _, err = self.run_cli([
            "add-risk", str(self.root), "--id", "health-critical", "--title", "irreversible loss",
            "--severity", "critical", "--mitigation", "stop deployment",
        ])
        self.assertEqual(code, 0, err)
        code, out, _ = self.run_cli(["health", str(self.root), "--json"])
        result = json.loads(out)
        self.assertEqual(code, 2)
        self.assertLessEqual(result["score"], 49)
        self.assertIn("open-critical-risk", result["hard_fails"])

    def test_migrate_v11_like_state(self):
        state_path = self.root / ".sdlc" / "state.json"
        state = self.state()
        state["version"] = "1.1.0"
        state.pop("revision", None)
        state["project"].pop("profile", None)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        audit_path = self.root / ".sdlc" / "audit" / "events.jsonl"
        audit_path.unlink()
        config_path = self.root / ".sdlc" / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config.pop("process_profile", None)
        config.pop("audit_chain", None)
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        code, _, err = self.run_cli(["migrate", str(self.root), "--profile", "standard"])
        self.assertEqual(code, 0, err)
        migrated = self.state()
        self.assertEqual(migrated["version"], sdlc.VERSION)
        self.assertEqual(migrated["project"]["profile"], "standard")
        self.assertIsInstance(migrated["revision"], int)
        code, out, err = self.run_cli(["validate", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)["valid"])

    def test_router_holdout_has_high_coverage_and_ambiguous_tasks_abstain(self):
        routing = json.loads((ROOT / "manifest" / "os-routing.json").read_text(encoding="utf-8"))
        state = {
            "current_os": "engineering",
            "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
        }
        holdout = json.loads((ROOT / "validation" / "benchmarks" / "router-holdout.json").read_text(encoding="utf-8"))
        routed = [sdlc.route_task(state, item["task"]) for item in holdout]
        auto = [item for item in routed if item["decision"] == "route"]
        self.assertGreaterEqual(len(auto) / len(holdout), 0.90)
        self.assertTrue(all(result["recommended_os"] == case["expected_os"] for result, case in zip(routed, holdout)))

        ambiguous = json.loads((ROOT / "validation" / "benchmarks" / "router-ambiguous.json").read_text(encoding="utf-8"))
        self.assertTrue(all(sdlc.route_task(state, item["task"])["decision"] == "abstain" for item in ambiguous))


if __name__ == "__main__":
    unittest.main()
