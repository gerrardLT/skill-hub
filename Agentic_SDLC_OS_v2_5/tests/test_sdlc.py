from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"
spec = importlib.util.spec_from_file_location("sdlc", MODULE_PATH)
sdlc = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(sdlc)


def future_iso(days: int = 1) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class SDLCBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        code, _, err = self.run_cli([
            "init", str(self.root), "--name", "demo", "--type", "greenfield", "--criticality", "medium"
        ])
        self.assertEqual(code, 0, err)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, argv):
        out = StringIO()
        err = StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = sdlc.main(argv)
        return code, out.getvalue(), err.getvalue()

    def state(self, root: Path | None = None):
        root = root or self.root
        return json.loads((root / ".sdlc" / "state.json").read_text(encoding="utf-8"))

    def substantive_content(self, artifact_type: str) -> str:
        contract = sdlc.artifact_contract(artifact_type)
        lines = [f"# {artifact_type}", ""]
        for index, group in enumerate(contract.get("required_section_groups", []), 1):
            heading = str(group[0]).title()
            lines.extend([
                f"## {heading}",
                "",
                (
                    f"Reviewed {heading.lower()} content {index} records concrete facts, named owners, "
                    "measurable conditions, relevant constraints, and a verifiable downstream decision. "
                    "The fixture is deliberately explicit so structural quality checks exercise real content."
                ),
                "",
            ])
        minimum = int(contract.get("minimum_substantive_chars", 220))
        while sdlc.substantive_chars("\n".join(lines)) < minimum + 40:
            lines.extend([
                "Additional verified detail links the decision to evidence, implementation, validation, risk controls, and ownership.",
                "",
            ])
        return "\n".join(lines)

    def create_and_register(
        self,
        artifact_type: str,
        artifact_id: str | None = None,
        status: str = "accepted",
        root: Path | None = None,
    ):
        root = root or self.root
        path = root / "docs" / f"{artifact_type}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.substantive_content(artifact_type), encoding="utf-8")
        artifact_id = artifact_id or f"art-{artifact_type}"
        code, _, err = self.run_cli([
            "add-artifact", str(root), "--id", artifact_id, "--type", artifact_type,
            "--path", str(path), "--status", status, "--owner", "test", "--verified-by", "test-suite",
        ])
        self.assertEqual(code, 0, err)
        return artifact_id

    def add_evidence(
        self,
        evidence_id: str,
        supports: str,
        quality: str = "medium",
        source: str | None = None,
        root: Path | None = None,
        claim: str | None = None,
    ) -> None:
        root = root or self.root
        source = source or f"test-source-{evidence_id}"
        claim = claim or f"independent verified claim {evidence_id}"
        code, _, err = self.run_cli([
            "add-evidence", str(root), "--id", evidence_id, "--claim", claim,
            "--source", source, "--source-type", "test", "--quality", quality,
            "--supports", supports, "--method", "automated fixture",
        ])
        self.assertEqual(code, 0, err)

    def trace_all(self, artifact_ids: list[str], root: Path | None = None) -> None:
        root = root or self.root
        if not artifact_ids:
            return
        if len(artifact_ids) == 1:
            pairs = [(artifact_ids[0], "goal:validated")]
        else:
            pairs = list(zip(artifact_ids, artifact_ids[1:]))
            pairs.append((artifact_ids[-1], "goal:validated"))
        for index, (source, target) in enumerate(pairs):
            code, _, err = self.run_cli([
                "trace", str(root), "--id", f"trace-{artifact_ids[0]}-{index}",
                "--from", source, "--to", target, "--relation", "supports",
            ])
            self.assertEqual(code, 0, err)

    def trace_gate_paths(
        self, gate_name: str, ids_by_type: dict[str, str], spec: dict, root: Path | None = None
    ) -> None:
        root = root or self.root
        seen: set[tuple[str, str, str]] = set()
        touched: set[str] = set()
        counter = 0
        for path_types in spec.get("trace_paths", []):
            for source_type, target_type in zip(path_types, path_types[1:]):
                source = ids_by_type[source_type]
                target = ids_by_type[target_type]
                signature = (source, "derives", target)
                if signature in seen:
                    continue
                seen.add(signature)
                touched.update([source, target])
                code, _, err = self.run_cli([
                    "trace", str(root), "--id", f"{gate_name}-path-{counter}",
                    "--from", source, "--to", target, "--relation", "derives",
                ])
                self.assertEqual(code, 0, err)
                counter += 1
        for artifact_id in ids_by_type.values():
            if artifact_id in touched:
                continue
            code, _, err = self.run_cli([
                "trace", str(root), "--id", f"{gate_name}-coverage-{counter}",
                "--from", artifact_id, "--to", f"goal:{gate_name}", "--relation", "supports",
            ])
            self.assertEqual(code, 0, err)
            counter += 1

    def satisfy_gate(self, gate_name: str, root: Path | None = None, include_high: bool | None = None) -> list[str]:
        root = root or self.root
        state = self.state(root)
        gates = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
        profile = state["project"].get("profile", "standard")
        spec = sdlc.resolve_gate_spec(gates[gate_name], profile, state["project"]["criticality"])
        required = list(spec["required"])
        if include_high is False:
            required = [x for x in required if x not in gates[gate_name].get("required_high_criticality", [])]
        ids_by_type = {t: self.create_and_register(t, f"{gate_name}-{t}", root=root) for t in required}
        self.trace_gate_paths(gate_name, ids_by_type, spec, root)
        artifact_ids = list(ids_by_type.values())
        evidence_count = int(spec.get("minimum_evidence", 0))
        high_count = int(spec.get("minimum_high_quality_evidence", 0))
        target_count = int(spec.get("minimum_evidence_targets", 0))
        source_count = int(spec.get("minimum_distinct_sources", 0))
        total = max(evidence_count, target_count, source_count)
        for index in range(total):
            target = artifact_ids[index % len(artifact_ids)] if artifact_ids else gate_name
            quality = "high" if index < high_count else "medium"
            self.add_evidence(
                f"{gate_name}-ev-{index}", target, quality=quality,
                source=f"{gate_name}-source-{index}", root=root,
            )
        return artifact_ids

    def create_waiver(self, gate_name: str = "pm-ready"):
        return self.run_cli([
            "gate", str(self.root), "--name", gate_name, "--waive",
            "--reason", "timeboxed reversible prototype", "--approver", "Alice Chen",
            "--approval-id", "CR-123", "--compensating-control", "daily review and automatic rollback",
            "--expires", future_iso(1), "--json",
        ])


class TestKernel(SDLCBase):
    def test_init_creates_kernel(self):
        self.assertTrue((self.root / ".sdlc" / "state.json").exists())
        self.assertTrue((self.root / ".sdlc" / "SUMMARY.md").exists())
        self.assertEqual(self.state()["current_os"], "pm")
        self.assertEqual(self.state()["version"], sdlc.VERSION)

    def test_route(self):
        code, out, err = self.run_cli(["route", str(self.root), "帮我设计用户流程和交互原型", "--json"])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["recommended_os"], "design")
        self.assertIn("confidence", payload)

    def test_pm_gate_requires_relevant_evidence(self):
        gates = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
        ids = [self.create_and_register(t) for t in gates["pm-ready"]["required"]]
        self.trace_all(ids)
        self.add_evidence("irrelevant", "external:other", quality="high")
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 2)
        result = json.loads(out)
        self.assertEqual(result["evidence_shortfall"], gates["pm-ready"]["minimum_evidence"])

        for index in range(3):
            self.add_evidence(
                f"ev-{index}", ids[index], quality="high" if index == 0 else "medium",
                source=f"source-{index}",
            )
        code, out, err = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "pass")

    def test_critical_risk_blocks_gate(self):
        self.satisfy_gate("pm-ready")
        self.run_cli([
            "add-risk", str(self.root), "--id", "risk-critical", "--title", "data loss",
            "--severity", "critical", "--likelihood", "possible", "--mitigation", "backup", "--owner", "eng",
        ])
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 2)
        self.assertIn("risk-critical", json.loads(out)["blocking_critical_risks"])

    def test_gate_waiver_and_transition(self):
        code, out, err = self.create_waiver()
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "waived")
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "design", "--to-stage", "INTAKE", "--reason", "approved waiver",
        ])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.state()["current_os"], "design")

    def test_backward_rework_does_not_require_force(self):
        code, _, err = self.create_waiver()
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "design", "--to-stage", "INTAKE", "--reason", "handoff",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "pm", "--to-stage", "DISCOVERY",
            "--reason", "design found invalid assumption",
        ])
        self.assertEqual(code, 0, err)
        state = self.state()
        self.assertEqual(state["current_os"], "pm")
        self.assertTrue(state["history"][-1]["rework"])

    def test_build_ready_enforced(self):
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "engineering", "--to-stage", "PLAN",
            "--reason", "test fixture", "--force", "--approver", "Alice Chen", "--approval-id", "CR-200",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli([
            "transition", str(self.root), "--to-os", "engineering", "--to-stage", "BUILD", "--reason", "start build",
        ])
        self.assertEqual(code, 2)
        self.assertIn("build-ready", err)

    def test_learning_and_validation(self):
        code, _, err = self.run_cli([
            "learn", str(self.root), "--expected", "activation +10%", "--actual", "+1%", "--gap", "segment mismatch",
            "--gap-type", "strategy", "--decision", "revalidate ICP", "--route-os", "pm", "--route-stage", "DISCOVERY",
        ])
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["validate", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        self.assertTrue(json.loads(out)["valid"])

    def test_all_gate_manifests_can_pass(self):
        gates = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))
        for gate_name in gates:
            with self.subTest(gate=gate_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                code, _, err = self.run_cli(["init", str(root), "--name", gate_name, "--criticality", "medium"])
                self.assertEqual(code, 0, err)
                self.satisfy_gate(gate_name, root=root)
                code, out, err = self.run_cli(["gate", str(root), "--name", gate_name, "--json"])
                self.assertEqual(code, 0, f"{gate_name}: {out} {err}")
                self.assertEqual(json.loads(out)["status"], "pass")

    def test_high_criticality_requires_additional_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, _, err = self.run_cli(["init", str(root), "--name", "high", "--criticality", "high"])
            self.assertEqual(code, 0, err)
            spec = json.loads((ROOT / "manifest" / "gates.json").read_text(encoding="utf-8"))["pm-ready"]
            ids = [self.create_and_register(t, f"a-{t}", root=root) for t in spec["required"]]
            self.trace_all(ids, root)
            for index in range(max(spec["minimum_evidence"], spec["minimum_distinct_sources"], spec["minimum_evidence_targets"])):
                self.add_evidence(
                    f"high-ev-{index}", ids[index % len(ids)], "high" if index == 0 else "medium",
                    source=f"high-source-{index}", root=root,
                )
            code, out, _ = self.run_cli(["gate", str(root), "--name", "pm-ready", "--json"])
            self.assertEqual(code, 2)
            missing = set(json.loads(out)["missing_artifacts"])
            self.assertEqual(missing, set(spec["required_high_criticality"]))

    def test_expired_waiver_is_rejected(self):
        code, _, err = self.run_cli([
            "gate", str(self.root), "--name", "pm-ready", "--waive", "--reason", "expired",
            "--approver", "Alice Chen", "--approval-id", "CR-300", "--compensating-control", "none",
            "--expires", "2000-01-01T00:00:00Z",
        ])
        self.assertEqual(code, 2)
        self.assertIn("future", err)

    def test_new_artifact(self):
        code, out, err = self.run_cli([
            "new-artifact", str(self.root), "--id", "prd-1", "--type", "prd", "--owner", "pm",
        ])
        self.assertEqual(code, 0, err)
        self.assertTrue((self.root / ".sdlc" / "artifacts" / "prd.md").exists())
        self.assertIn("prd-1", self.state()["artifacts"])


if __name__ == "__main__":
    unittest.main()
