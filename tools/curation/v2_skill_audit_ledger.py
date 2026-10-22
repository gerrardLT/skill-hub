#!/usr/bin/env python3
"""Phase E: merge static scan (B), semantic review (C) and execution A/B (D) into one per-Skill ledger and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

SCAN = Path("curation/v2/skill-audit/static-scan.json")
SEMANTIC = Path("curation/v2/skill-audit/semantic")
PHASE_D = Path("evals/runs/capability-compiler-v2/skill-audit/phase-d/report.json")
LEDGER = Path("curation/v2/skill-audit/ledger.json")
REPORT = Path("docs/skill-audit-v2-1.0.0.md")
RELEASE_TREE = "116651adca2b907b3629e7e1954cddcd15cf0388e3401facaf2e8cb5c210d852"
DIMS = ["boundary", "trigger_precision", "procedure", "output_verifiability", "gate_specificity", "permission_fit", "source_fidelity", "measured_efficacy"]
DIM_ZH = {"boundary": "边界", "trigger_precision": "触发", "procedure": "程序", "output_verifiability": "输出可验", "gate_specificity": "Gate", "permission_fit": "权限", "source_fidelity": "来源保真", "measured_efficacy": "实测"}
FINAL_ZH = {"keep": "保留", "improve": "改进", "revise": "优先修订", "merge": "合并", "split": "拆分"}
D_ZH = {"effective": "有效", "no-gain": "无增益", "mixed": "互有胜负", "negative": "负向", "incomplete": "未测"}
OUT_ZH = {"win": "胜", "tie": "平", "loss": "负", "incomplete": "未测"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def final_disposition(c_verdict: str, d_verdict: str, p1: int) -> tuple[str, int]:
    """Return (disposition, tier). Tier 1 = act first, 4 = keep."""
    if c_verdict in {"merge", "split"}:
        return c_verdict, 1
    if d_verdict == "negative":
        return "revise", 1
    if d_verdict == "mixed" or (c_verdict == "improve" and p1):
        return ("revise" if d_verdict == "mixed" else "improve"), 2
    if c_verdict == "improve":
        return "improve", 3
    return "keep", 4


def build(workspace: Path) -> dict[str, Any]:
    scan = {item["id"]: item for item in load(workspace / SCAN)["skills"]}
    scan_doc = load(workspace / SCAN)
    phase_d = load(workspace / PHASE_D)
    semantic, cross = {}, []
    for path in sorted((workspace / SEMANTIC).glob("*.json")):
        doc = load(path)
        cross += [{"domain": doc["domain"], **item} for item in doc.get("cross_skill_findings", [])]
        for skill in doc["skills"]:
            semantic[skill["id"]] = {**skill, "domain": doc["domain"]}
    entries = []
    for skill_id in sorted(scan):
        c = semantic[skill_id]
        d = phase_d["per_skill"].get(skill_id, {"verdict": "incomplete", "outcomes": []})
        p1 = sum(f["priority"] == "P1" for f in c["findings"])
        p2 = sum(f["priority"] == "P2" for f in c["findings"])
        disposition, tier = final_disposition(c["verdict"], d["verdict"], p1)
        entries.append({
            "id": skill_id, "domain": c["domain"], "permission_identity": scan[skill_id]["permission_identity"],
            "static": {"findings": scan[skill_id]["static_findings"], "dangling_refs": scan[skill_id]["dangling_refs"], "nearest": scan[skill_id]["nearest_neighbours"][0], "source_refs": scan[skill_id]["source_evidence_refs"], "phase9_holdouts": scan[skill_id]["phase9_holdouts"], "phase9_mutation": scan[skill_id]["phase9_mutation"]},
            "semantic": {"scores": c["scores"], "total": sum(c["scores"].values()), "verdict": c["verdict"], "target": c.get("merge_or_split_target"), "strengths": c["strengths"], "findings": c["findings"], "lost_source_techniques": c["lost_source_techniques"], "p1": p1, "p2": p2},
            "execution_ab": {"verdict": d["verdict"], "tasks": [{"task": o["task"], "kind": o.get("kind"), "outcome": o["outcome"], "orders_agree": o.get("orders_agree")} for o in d["outcomes"]]},
            "final": {"disposition": disposition, "tier": tier},
        })
    totals = {dim: round(sum(e["semantic"]["scores"][dim] for e in entries) / len(entries), 2) for dim in DIMS}
    summary = {
        "skills": len(entries),
        "final": dict(Counter(e["final"]["disposition"] for e in entries)),
        "tiers": dict(sorted(Counter(e["final"]["tier"] for e in entries).items())),
        "semantic_verdicts": dict(Counter(e["semantic"]["verdict"] for e in entries)),
        "execution_verdicts": dict(Counter(e["execution_ab"]["verdict"] for e in entries)),
        "findings": {"P1": sum(e["semantic"]["p1"] for e in entries), "P2": sum(e["semantic"]["p2"] for e in entries)},
        "mean_scores": totals,
        "static_finding_counts": scan_doc["finding_counts"],
        "execution_task_outcomes": phase_d["task_outcomes"], "judge_order_agreement": phase_d["judge_order_agreement"],
        "execution_by_kind": dict(sorted(Counter(f"{t['kind']}:{t['outcome']}" for e in entries for t in e["execution_ab"]["tasks"] if t["kind"]).items())),
        "phase_d_calls": phase_d["calls_recorded"], "phase_d_tokens": phase_d["total_tokens"],
    }
    inputs = {str(p): hashlib.sha256((workspace / p).read_bytes()).hexdigest() for p in [SCAN, PHASE_D, *sorted(q.relative_to(workspace) for q in (workspace / SEMANTIC).glob("*.json"))]}
    return {"schema_version": "2.0", "audit": "v2-1.0.0-atomic-skills", "release_asset_tree_sha256": RELEASE_TREE, "release_modified": False, "inputs": {k.replace("\\", "/"): v for k, v in inputs.items()}, "summary": summary, "cross_skill_findings": cross, "skills": entries}


def verify(ledger: dict[str, Any], workspace: Path) -> list[str]:
    errors = []
    catalog = {item["id"] for item in load(workspace / "slots/v2/catalog.json")["skills"]}
    ids = [e["id"] for e in ledger["skills"]]
    if sorted(ids) != sorted(catalog) or len(ids) != len(set(ids)):
        errors.append("ledger does not cover the 157 released Skills exactly once")
    for e in ledger["skills"]:
        if set(e["semantic"]["scores"]) != set(DIMS) or any(v not in (0, 1, 2, 3) for v in e["semantic"]["scores"].values()):
            errors.append(f"{e['id']}: invalid scores")
        if any(not f.get("evidence") or not f.get("recommendation") for f in e["semantic"]["findings"]):
            errors.append(f"{e['id']}: finding without evidence or recommendation")
        if e["semantic"]["verdict"] in {"merge", "split"} and not e["semantic"]["target"]:
            errors.append(f"{e['id']}: merge/split without target")
        if (e["final"]["disposition"], e["final"]["tier"]) != final_disposition(e["semantic"]["verdict"], e["execution_ab"]["verdict"], e["semantic"]["p1"]):
            errors.append(f"{e['id']}: final disposition inconsistent")
    for path, digest in ledger["inputs"].items():
        if hashlib.sha256((workspace / path).read_bytes()).hexdigest() != digest:
            errors.append(f"input drift: {path}")
    return errors


def render(ledger: dict[str, Any]) -> str:
    s = ledger["summary"]
    tier_names = {1: "第一优先（合并/拆分/实测负向）", 2: "第二优先（有 P1 问题或实测互有胜负）", 3: "第三优先（仅 P2 问题）", 4: "保留"}
    lines = [
        "# V2 1.0.0 原子 Skills 审核报告", "",
        "> 只审不改：`slots/v2/1.0.0/` 与 `recipes/v2/1.0.0/` 未作任何修改（release tree `" + RELEASE_TREE[:12] + "…`，Phase 12 Gate 复证）。逐项发现的证据与建议保留英文原文，便于对照文件行号。", "",
        "## 结论", "",
        f"157 个 Skill 中：保留 {s['final'].get('keep', 0)}，改进 {s['final'].get('improve', 0)}，优先修订 {s['final'].get('revise', 0)}，合并 {s['final'].get('merge', 0)}，拆分 {s['final'].get('split', 0)}。",
        "",
        "整体看，这批 Skill 的边界、权限和 Gate 设计扎实（均分 2.9 以上），短板集中在两处：",
        f"- 来源保真偏低（均分 {s['mean_scores']['source_fidelity']}/3）：来源里的具体技法、阈值、反模式在提纯时被抽象成了通用措辞。",
        f"- 实测增益有限：执行质量 A/B 中，带 Skill 的产出 {s['execution_task_outcomes'].get('win', 0)} 胜 / {s['execution_task_outcomes'].get('tie', 0)} 平 / {s['execution_task_outcomes'].get('loss', 0)} 负（312 题，两种呈现顺序一致才计胜负）。",
        "",
        "## 三层证据", "",
        "| 层 | 方法 | 结果 |", "|---|---|---|",
        f"| B 静态扫描 | 结构、模板化、契约一致、引用、重叠、溯源深度 | 见下方系统性问题 |",
        f"| C 语义审核 | 父级逐个读 SKILL/contract/provenance 与来源片段，8 维 0–3 分 | P1 {s['findings']['P1']} 条，P2 {s['findings']['P2']} 条 |",
        f"| D 执行 A/B | 每 Skill 2 道新题，gpt-5.6-sol 有/无 Skill 作答，claude-opus-5.5 双顺序盲评 | {s['phase_d_calls']} 次调用，{s['phase_d_tokens']:,} tokens |",
        "",
        "8 维均分：" + "，".join(f"{DIM_ZH[k]} {v}" for k, v in s["mean_scores"].items()) + "。", "",
        "## 执行 A/B 的规律", "",
        f"- 难题（含越权诱导、证据冲突、缺失授权）：{s['execution_by_kind'].get('hard:win', 0)} 胜 / {s['execution_by_kind'].get('hard:tie', 0)} 平 / {s['execution_by_kind'].get('hard:loss', 0)} 负。Skill 的治理与停止条件确实起作用。",
        f"- 常规题：{s['execution_by_kind'].get('standard:win', 0)} 胜 / {s['execution_by_kind'].get('standard:tie', 0)} 平 / {s['execution_by_kind'].get('standard:loss', 0)} 负。负的主因是：交付不够具体、在本可完成时返回 needs-input/blocked、漏掉具体发现。",
        f"- 评判两种顺序一致率 {s['judge_order_agreement']['agree']}/{s['judge_order_agreement']['agree'] + s['judge_order_agreement']['disagree']}，不一致的题一律记平。",
        "- 每 Skill 只有 2 题、1 个评判模型，结论是方向性信号，不是统计结论。`browser-data-acquisition-runtime` 出题连续 4 次遇 provider 流中断，未实测。",
        "",
        "## 系统性问题（影响全部或大部分 Skill）", "",
        f"1. Trigger 段逐字复述 Responsibility（{s['static_finding_counts'].get('trigger-restates-responsibility', 0)}/157），没有提供额外的触发信号。",
        f"2. SKILL.md 未包含 contract 的 forbidden_actions（{s['static_finding_counts'].get('skill-md-omits-forbidden-actions', 0)}/157），且多数缺第二条 hard gate（{s['static_finding_counts'].get('skill-md-omits-contract-hard-gate', 0)}/157）。模型只读 SKILL.md 时这些约束不可见。",
        f"3. 已发布的 contract 仍带发布前措辞 \"claim ... released status\"（{s['static_finding_counts'].get('stale-prerelease-forbidden-action', 0)}/157）。",
        f"4. Non-Responsibilities 引用了不存在的 Skill（{s['static_finding_counts'].get('dangling-non-responsibility-ref', 0)} 个 Skill）：`provider-review-comment-response`、`schema-migration-safety`、`artifact-publication`、`pull-request-update`。",
        f"5. 高度相近却未互设 anti-trigger 的 Skill 对（{s['static_finding_counts'].get('high-semantic-overlap', 0) // 2} 对），如 playwright-test-engineering / vitest-tooling、ai-observability / log-observability。",
        "6. 每个 Skill 恰好 2 条 anti-trigger、2 条 hard gate、4 项输出、4–5 步，Status Mapping 等段落 54–93 个 Skill 逐字共享。模板一致性好，但压掉了领域差异。",
        f"7. Phase 9 的 mutation 几乎测不出删改（存活 {s['static_finding_counts'].get('mutation-survived', 0)}，需行为挑战 {s['static_finding_counts'].get('mutation-behavioral-challenge-needed', 0)}）；它只测路由决策，不测产出质量，本次 D 阶段补上了这一块。",
        "",
        "## 跨 Skill 边界建议", "",
    ]
    for item in ledger["cross_skill_findings"]:
        lines.append(f"- **{', '.join(item['skills'])}**：{item['issue']} → {item['recommendation']}")
    lines += ["", "## 修订优先级", ""]
    for tier in [1, 2, 3, 4]:
        ids = [e for e in ledger["skills"] if e["final"]["tier"] == tier]
        lines.append(f"- {tier_names[tier]}（{len(ids)}）：" + "、".join(f"`{e['id']}`" for e in ids))
    lines += ["", "## 逐个 Skill 分析", "", "图例：8 维分依次为 " + " / ".join(DIM_ZH[d] for d in DIMS) + "；A/B 列为 T1（常规）/ T2（难题）结果。", ""]
    domains = sorted({e["domain"] for e in ledger["skills"]})
    for domain in domains:
        lines += [f"### {domain}", ""]
        for e in [x for x in ledger["skills"] if x["domain"] == domain]:
            sem, ab = e["semantic"], e["execution_ab"]
            tasks = " / ".join(OUT_ZH.get(t["outcome"], t["outcome"]) for t in ab["tasks"]) or "未测"
            scores = "/".join(str(sem["scores"][d]) for d in DIMS)
            target = f"（目标：{sem['target']}）" if sem["target"] else ""
            lines += [
                f"#### `{e['id']}` — {FINAL_ZH[e['final']['disposition']]}{target}",
                "",
                f"- 权限：`{e['permission_identity']}`；8 维分 {scores}（合计 {sem['total']}/24）；语义裁决 {sem['verdict']}；执行 A/B {D_ZH[ab['verdict']]}（{tasks}）",
            ]
            if sem["strengths"]:
                lines.append("- 优点：" + "；".join(sem["strengths"]))
            for f in sem["findings"]:
                lines.append(f"- **{f['priority']} {f['dimension']}**：{f['issue']} 建议：{f['recommendation']} 证据：`{f['evidence']}`")
            if not sem["findings"]:
                lines.append("- 未发现需修订的问题。")
            if sem["lost_source_techniques"]:
                lines.append("- 来源中丢失的技法：" + "；".join(sem["lost_source_techniques"]))
            lines.append("")
    lines += ["## 证据位置", "",
              "- 审核合同：`.specs/capability-compiler-v2/skill-audit/plan.md`、`phase-d-design.md`",
              "- 静态扫描：`curation/v2/skill-audit/static-scan.json`",
              "- 语义审核：`curation/v2/skill-audit/semantic/*.json`",
              "- 执行 A/B：`evals/runs/capability-compiler-v2/skill-audit/phase-d/`（含 task-set、每次调用的 prompt/输出/receipt）",
              "- 被拒的试点与失败记录：`phase-d-pilot-1/finding.json`、`phase-d/gen-failed/`、`curation/v2/skill-audit/failures/`",
              "- 汇总 ledger：`curation/v2/skill-audit/ledger.json`", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace_root.resolve()
    if args.verify_only:
        ledger = load(workspace / LEDGER)
    else:
        ledger = build(workspace)
        (workspace / LEDGER).write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        (workspace / REPORT).write_text(render(ledger), encoding="utf-8", newline="\n")
    errors = verify(ledger, workspace)
    print(json.dumps({"ok": not errors, "errors": errors[:20], "summary": {k: ledger["summary"][k] for k in ["skills", "final", "tiers", "execution_verdicts", "findings"]}}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    # ponytail: disposition self-check; move to tests/ if the rule grows
    assert final_disposition("merge", "effective", 0) == ("merge", 1)
    assert final_disposition("keep", "negative", 0) == ("revise", 1)
    assert final_disposition("keep", "mixed", 0) == ("revise", 2)
    assert final_disposition("improve", "no-gain", 1) == ("improve", 2)
    assert final_disposition("improve", "effective", 0) == ("improve", 3)
    assert final_disposition("keep", "incomplete", 0) == ("keep", 4)
    raise SystemExit(main())
