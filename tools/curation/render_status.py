#!/usr/bin/env python3
"""Render authoritative status from executable Gate and release reports."""
from __future__ import annotations

import argparse
import datetime
import json
import re
from pathlib import Path


def _test_summary(stdout: str) -> str:
    matches = re.findall(r"(\d+ passed(?:, \d+ (?:warning|warnings))?)", stdout)
    if not matches:
        raise ValueError("test summary missing from gate report")
    return matches[-1]


def render(workspace: Path) -> None:
    report = json.loads((workspace / "curation/gate-report.json").read_text(encoding="utf-8"))
    if report.get("gate") != "all-repository-gates":
        raise ValueError("unexpected gate report")
    results = {item["name"]: item for item in report["results"]}
    ok = report.get("ok") is True and all(item["ok"] for item in results.values())
    today = datetime.date.today().isoformat()
    phase = {
        1: results["source"]["ok"], 2: results["phase2"]["ok"], 3: results["phase3"]["ok"],
        4: results["phase4"]["ok"], 5: results["phase5-provenance"]["ok"] and results["phase5-release"]["ok"],
        6: results["phase6"]["ok"], 7: results["phase7"]["ok"], 8: results["phase8-source"]["ok"] and results.get("runtime", {}).get("ok", False),
    }
    status_doc = json.loads((workspace / "curation/slot-release-status.json").read_text(encoding="utf-8"))
    released_slots = sum(item.get("disposition") == "released" for item in status_doc["items"])
    draft_slots = sum(item.get("disposition") != "released" for item in status_doc["items"])
    released_recipes = len([path for path in (workspace / "recipes").glob("*.json") if path.stem not in {"schema", "catalog"} and json.loads(path.read_text(encoding="utf-8")).get("status") == "released"])
    tests = _test_summary(results["tests"]["stdout"])
    verdict = "complete" if ok else "blocked"
    final = {
        "audit_id": f"capability-compiler-gate-audit-{today}", "audited_at": today,
        "source_of_truth": "curation/gate-report.json", "overall_verdict": verdict,
        "completion_claim_allowed": ok,
        "phase_status": [{"phase": number, "status": "passed" if passed else "failed", "evidence": "curation/gate-report.json"} for number, passed in phase.items()],
        "released_assets": {"slots": released_slots, "recipes": released_recipes, "unreleased_slots": draft_slots},
        "test_summary": tests,
        "local_install_sync_required_for_repository_completion": False,
        "next_valid_action": "Sync local plugin copies and create the verified local commit." if ok else "Fix failing executable gates before release.",
    }
    (workspace / "curation/final-audit.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checklist = {"checklist_id": f"full-dev-loop-prompt-to-artifact-{today}", "source_of_truth": "curation/gate-report.json", "objective": "Release a fail-closed stateful six-stage dev loop.", "overall_status": "passed" if ok else "failed", "phases": final["phase_status"], "released_assets": final["released_assets"], "next_valid_action": final["next_valid_action"]}
    (workspace / "curation/prompt-to-artifact-checklist.json").write_text(json.dumps(checklist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    goal = f"""# GOAL：Capability Compiler 六步闭环

## 最终状态：{'✅ 完成' if ok else '❌ 阻断'}

本文件由 `tools/curation/render_status.py` 从机器 Gate 生成。

- 审计日期：{today}
- 自动测试：{tests}
- 原始 `skills/` 基线：{'通过' if results['source']['ok'] else '失败'}
- Phase 1–8：{'全部通过' if ok else '存在失败'}
- Released slots：{released_slots}
- Unreleased slots：{draft_slots}
- Released recipes：{released_recipes}
- 自然语言路由、状态恢复、失败回跳和授权 Gate：{'通过' if results.get('runtime', {}).get('ok') else '失败'}

## 权威证据

- `curation/gate-report.json`
- `curation/final-audit.json`
- `evals/runs/full-dev-loop/`
"""
    (workspace / "GOAL.md").write_text(goal, encoding="utf-8")
    summary = f"""# Skills Hub 状态

> 由 `tools/curation/render_status.py` 从机器 Gate 生成。

- 总体状态：`{verdict}`
- 68 个 catalog entries
- 49 个 included sources，15 个 deferred-platform sources
- 965 个 semantic units，88 个 capability clusters
- {released_slots} 个 released slots，{draft_slots} 个 unreleased slots
- {released_recipes} 个 released recipes
- 自动测试：{tests}
- Phase 1–8：{'全部通过' if ok else '存在失败'}
- 权威审计：`curation/final-audit.json`
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
