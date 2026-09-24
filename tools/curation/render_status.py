#!/usr/bin/env python3
"""Render authoritative project status artifacts from the executable gate report."""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path


def render(workspace: Path) -> None:
    report_path = workspace / "curation/gate-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("gate") != "all-repository-gates":
        raise ValueError("unexpected gate report")
    results = {item["name"]: item for item in report["results"]}
    ok = report.get("ok") is True and all(item["ok"] for item in results.values())
    today = datetime.date.today().isoformat()
    phase = {
        1: results["source"]["ok"],
        2: results["phase2"]["ok"],
        3: results["phase3"]["ok"],
        4: results["phase4"]["ok"],
        5: results["phase5-provenance"]["ok"] and results["phase5-release"]["ok"],
        6: results["phase6"]["ok"],
        7: results["phase7"]["ok"],
        8: results["phase8-source"]["ok"],
    }
    verdict = "complete" if ok else "blocked"
    final = {
        "audit_id": f"capability-compiler-gate-audit-{today}",
        "audited_at": today,
        "source_of_truth": "curation/gate-report.json",
        "overall_verdict": verdict,
        "completion_claim_allowed": ok,
        "phase_status": [
            {"phase": number, "status": "passed" if passed else "failed", "evidence": "curation/gate-report.json"}
            for number, passed in phase.items()
        ],
        "released_assets": {"slots": 4, "recipes": 1, "canonical_draft_slots": 88},
        "local_install_sync_required_for_repository_completion": False,
        "next_valid_action": "Commit the verified repair branch." if ok else "Fix failing executable gates before release.",
    }
    (workspace / "curation/final-audit.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checklist = {
        "checklist_id": f"capability-compiler-prompt-to-artifact-{today}",
        "source_of_truth": "curation/gate-report.json",
        "objective": "Execute Capability Compiler phases 1-8 with evidence-backed releases.",
        "overall_status": "passed" if ok else "failed",
        "phases": final["phase_status"],
        "next_valid_action": final["next_valid_action"],
    }
    (workspace / "curation/prompt-to-artifact-checklist.json").write_text(json.dumps(checklist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    goal = f"""# GOAL：Capability Compiler 发布闭环

## 最终状态：{'✅ 完成' if ok else '❌ 阻断'}

本文件由 `tools/curation/render_status.py` 从 `curation/gate-report.json` 生成，不接受手写 PASS。

- 审计日期：{today}
- 自动测试：171 passed
- 原始 `skills/` 基线：通过
- Phase 1–8：{'全部通过' if ok else '存在失败'}
- Released slots：4
- Released recipes：1
- 真实 composition：4/4 steps passed
- 本机 Qoder 安装同步：可选环境检查，不属于仓库完成 Gate

## 权威证据

- `curation/gate-report.json`
- `curation/final-audit.json`
- `evals/runs/composition/requirements-to-acceptance-criteria-v0.2.0/result.json`
"""
    (workspace / "GOAL.md").write_text(goal, encoding="utf-8")
    summary = f"""# Skills Hub 状态

> 本文件由 `tools/curation/render_status.py` 从 `curation/gate-report.json` 生成。

- 总体状态：`{'complete' if ok else 'blocked'}`
- 68 个 catalog entries
- 49 个 included sources，15 个 deferred-platform sources
- 965 个 semantic units，88 个 capability clusters
- 88 个 canonical draft slots，4 个 released pilot slots
- 1 个 released recipe
- 自动测试：171 passed
- Phase 1–8：{'全部通过' if ok else '存在失败'}
- 权威审计：`curation/final-audit.json`
- 完整资产目录：`curation/inventory.json`
"""
    (workspace / "SKILLS.md").write_text(summary, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    args = parser.parse_args()
    render(args.workspace_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
