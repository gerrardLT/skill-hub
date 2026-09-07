from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from test_sdlc import SDLCBase, future_iso, sdlc


class TestV13Controls(SDLCBase):
    def write_artifact(self, root: Path, artifact_type: str, name: str) -> Path:
        path = root / "docs" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.substantive_content(artifact_type), encoding="utf-8")
        return path

    def test_hollow_structural_shell_is_rejected(self):
        path = self.root / "docs" / "hollow.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        repeated = "This section will be completed as appropriate by relevant stakeholders."
        path.write_text(
            "# Hollow\n\n"
            "## Objective\n\n" + repeated + "\n\n"
            "## Evidence\n\n" + repeated + "\n\n"
            "## Risks\n\n" + repeated + "\n\n"
            "## Acceptance Criteria\n\n" + repeated + "\n\n"
            "## Traceability\n\n" + repeated + "\n",
            encoding="utf-8",
        )
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", "hollow", "--type", "generic-spec",
            "--path", str(path), "--status", "accepted", "--owner", "pm",
        ])
        self.assertEqual(code, 2)
        self.assertTrue(
            "insufficient_concrete_signals" in err
            or "repetitive_section_content" in err
            or "excessive_vague_language" in err,
            err,
        )

    def test_compliant_artifact_records_quality_score(self):
        artifact_id = self.create_and_register("product-brief", "quality-product-brief")
        item = self.state()["artifacts"][artifact_id]
        self.assertGreaterEqual(float(item["quality_score"]), 0.75)
        self.assertIn(item["quality_contract"], {"product-brief", "default"})
        code, out, err = self.run_cli(["quality", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["invalid"], 0)

    def test_chinese_product_brief_contract_is_supported(self):
        path = self.root / "docs" / "中文产品简报.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# 中文产品简报\n\n"
            "## 问题\n\n来源 EV-CN-01 显示，3 家试点场馆在 30 次预约中发生 11 次冲突。\n\n"
            "## 用户\n\n目标用户是负责预约、收款和日结的单店管理员，负责人：产品经理。\n\n"
            "## 目标\n\n系统必须在 4 周试点中把重复预约降为 0，并让 95% 的订单在 10 分钟内确认。\n\n"
            "## 范围与非目标\n\n范围包含单场馆、预约和支付状态；不包含跨国税务与多门店加盟。\n\n"
            "## 证据与事实\n\n证据来自 2026-08-30 的用户访谈和预约日志，样本量有限，需要上线埋点复核。\n\n"
            "## 风险与假设\n\n风险 R-CN-01 是支付对账错误，必须使用幂等事件和每日对账。\n\n"
            "## 成功指标与验收标准\n\n至少完成 20 次预约且无重复预约、无严重隐私事故，否则判定失败并回到需求发现。\n\n"
            "## 可追溯性\n\n需求 PRD-CN-01 关联证据 EV-CN-01、测试 TEST-CN-01 和版本 REL-CN-01。产品负责人每周复核访谈、埋点和缺陷数据；当确认率低于 95%、出现重复预约或严重支付错误时，必须创建决策记录并回流到需求、设计或工程阶段。试点结束后以 20 笔真实订单、客服工单和对账结果共同判断是否继续扩大范围。\n",
            encoding="utf-8",
        )
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", "cn-brief", "--type", "product-brief",
            "--path", str(path), "--status", "accepted", "--owner", "产品经理",
            "--verified-by", "评审人",
        ])
        self.assertEqual(code, 0, err)
        self.assertGreaterEqual(float(self.state()["artifacts"]["cn-brief"]["quality_score"]), 0.75)

    def test_high_assurance_requires_independent_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code, _, err = self.run_cli([
                "init", str(root), "--name", "strict", "--criticality", "medium",
                "--profile", "high-assurance",
            ])
            self.assertEqual(code, 0, err)
            path = self.write_artifact(root, "product-brief", "brief")
            base = [
                "add-artifact", str(root), "--id", "brief", "--type", "product-brief",
                "--path", str(path), "--status", "accepted", "--owner", "Alice Chen",
            ]
            code, _, err = self.run_cli(base)
            self.assertEqual(code, 2)
            self.assertIn("independent --verified-by", err)
            code, _, err = self.run_cli([*base, "--verified-by", "Alice Chen"])
            self.assertEqual(code, 2)
            self.assertIn("cannot independently verify", err)
            code, _, err = self.run_cli([*base, "--verified-by", "Bob Lee"])
            self.assertEqual(code, 0, err)

    def test_accepted_upstream_change_marks_downstream_stale(self):
        source = self.create_and_register("product-brief", "source")
        target = self.create_and_register("prd", "target")
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "source-target", "--from", source,
            "--to", target, "--relation", "derives",
        ])
        self.assertEqual(code, 0, err)
        source_path = self.root / self.state()["artifacts"][source]["path"]
        source_path.write_text(
            source_path.read_text(encoding="utf-8")
            + "\n## Change Record\n\nDecision ID: CR-991 must expand pilot evidence to 25 users.\n",
            encoding="utf-8",
        )
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", source, "--type", "product-brief",
            "--path", str(source_path), "--status", "accepted", "--owner", "test",
            "--verified-by", "test-suite",
        ])
        self.assertEqual(code, 0, err)
        state = self.state()
        self.assertTrue(state["artifacts"][target]["stale"])
        self.assertIn(source, state["artifacts"][target]["stale_from"])

    def test_reaccepting_stale_artifact_clears_staleness(self):
        source = self.create_and_register("product-brief", "source")
        target = self.create_and_register("prd", "target")
        self.run_cli([
            "trace", str(self.root), "--id", "source-target", "--from", source,
            "--to", target, "--relation", "derives",
        ])
        source_path = self.root / self.state()["artifacts"][source]["path"]
        source_path.write_text(
            source_path.read_text(encoding="utf-8")
            + "\n## Change Record\n\nDecision ID: CR-992 must cover 30 users.\n",
            encoding="utf-8",
        )
        self.run_cli([
            "add-artifact", str(self.root), "--id", source, "--type", "product-brief",
            "--path", str(source_path), "--status", "accepted", "--owner", "test",
            "--verified-by", "test-suite",
        ])
        target_path = self.root / self.state()["artifacts"][target]["path"]
        code, _, err = self.run_cli([
            "add-artifact", str(self.root), "--id", target, "--type", "prd",
            "--path", str(target_path), "--status", "accepted", "--owner", "test",
            "--verified-by", "test-suite",
        ])
        self.assertEqual(code, 0, err)
        self.assertFalse(self.state()["artifacts"][target]["stale"])

    def test_manual_upstream_tamper_invalidates_downstream_gate_artifact(self):
        gate_ids = self.satisfy_gate("pm-ready")
        product_brief = next(x for x in gate_ids if self.state()["artifacts"][x]["type"] == "product-brief")
        extra = self.create_and_register("generic-spec", "extra-upstream")
        code, _, err = self.run_cli([
            "trace", str(self.root), "--id", "extra-brief", "--from", extra,
            "--to", product_brief, "--relation", "derives",
        ])
        self.assertEqual(code, 0, err)
        code, _, err = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 0, err)
        extra_path = self.root / self.state()["artifacts"][extra]["path"]
        extra_path.write_text(extra_path.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        code, out, _ = self.run_cli(["gate", str(self.root), "--name", "pm-ready", "--json"])
        self.assertEqual(code, 2)
        payload = json.loads(out)
        invalid_by_id = {item["id"]: item for item in payload["invalid_artifacts"]}
        self.assertIn(product_brief, invalid_by_id)
        self.assertTrue(any("upstream_artifact_invalid" in issue for issue in invalid_by_id[product_brief]["issues"]))

    def test_impact_command_reports_descendants_and_gates(self):
        source = self.create_and_register("product-brief", "source")
        target = self.create_and_register("prd", "target")
        self.run_cli([
            "trace", str(self.root), "--id", "source-target", "--from", source,
            "--to", target, "--relation", "derives",
        ])
        code, out, err = self.run_cli([
            "impact", str(self.root), "--artifact-id", source, "--json",
        ])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertIn(target, payload["descendants"])
        self.assertIn("pm-ready", payload["affected_gates"])

    def test_reconcile_persists_direct_and_downstream_staleness(self):
        source = self.create_and_register("product-brief", "source")
        target = self.create_and_register("prd", "target")
        self.run_cli([
            "trace", str(self.root), "--id", "source-target", "--from", source,
            "--to", target, "--relation", "derives",
        ])
        source_path = self.root / self.state()["artifacts"][source]["path"]
        source_path.write_text(source_path.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        code, out, _ = self.run_cli(["reconcile", str(self.root), "--apply", "--json"])
        self.assertEqual(code, 2)
        payload = json.loads(out)
        self.assertIn(source, payload["direct_invalid"])
        state = self.state()
        self.assertTrue(state["artifacts"][source]["stale"])
        self.assertTrue(state["artifacts"][target]["stale"])

    def test_upstream_tamper_invalidates_existing_waiver_snapshot(self):
        gates = json.loads((Path(__file__).resolve().parents[1] / "manifest" / "gates.json").read_text())
        spec = sdlc.resolve_gate_spec(gates["pm-ready"], "standard", "medium")
        required = list(spec["required"])
        ids = {item: self.create_and_register(item, f"waiver-{item}") for item in required}
        self.trace_gate_paths("pm-ready", ids, spec)
        # Deliberately do not add evidence: the gate fails and can be waived.
        extra = self.create_and_register("generic-spec", "waiver-upstream")
        self.run_cli([
            "trace", str(self.root), "--id", "waiver-extra", "--from", extra,
            "--to", ids["product-brief"], "--relation", "derives",
        ])
        code, out, err = self.run_cli([
            "gate", str(self.root), "--name", "pm-ready", "--waive",
            "--reason", "timeboxed prototype", "--approver", "Alice Chen",
            "--approval-id", "CR-900", "--compensating-control", "manual evidence review",
            "--expires", future_iso(1), "--json",
        ])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "waived")
        extra_path = self.root / self.state()["artifacts"][extra]["path"]
        extra_path.write_text(extra_path.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")
        allowed, result = sdlc.gate_allows_transition(self.state(), "pm-ready", self.root)
        self.assertFalse(allowed)
        self.assertEqual(result["status"], "fail")

    def test_record_run_and_budget_metrics(self):
        cfg_path = self.root / ".sdlc" / "config.json"
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
        config["cost_budget_usd"] = 0.05
        config["token_budget"] = 1000
        cfg_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        for index, outcome in enumerate(["success", "failed"]):
            code, _, err = self.run_cli([
                "record-run", str(self.root), "--id", f"run-{index}", "--actor", "agent-a",
                "--os", "engineering", "--skill", "implementation", "--model", "model-x",
                "--outcome", outcome, "--duration-ms", "100", "--tokens-input", "600",
                "--tokens-output", "100", "--tool-calls", "3", "--cost-usd", "0.04",
            ])
            self.assertEqual(code, 0, err)
        code, out, err = self.run_cli(["metrics", str(self.root), "--json"])
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["runs"], 2)
        self.assertEqual(payload["tokens"], 1400)
        self.assertEqual(payload["tool_calls"], 6)
        self.assertAlmostEqual(payload["cost_usd"], 0.08)
        self.assertEqual(payload["run_success_rate"], 0.5)
        self.assertEqual(len(payload["warnings"]), 2)


if __name__ == "__main__":
    unittest.main()
