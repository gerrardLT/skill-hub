#!/usr/bin/env python3
"""
Generate curation semantic units for retro.
Extracts units from skills/retro/SKILL.md and skills/retro/sections/report-format.md.
"""

import json
import sys
from pathlib import Path

SKILLS_ROOT = Path("skills")
UNITS_ROOT = Path("curation/units")

def extract_lines(file_rel_path: str, start: int, end: int) -> str:
    full_path = SKILLS_ROOT / file_rel_path
    lines = full_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1:end])

def main():
    UNITS_ROOT.mkdir(parents=True, exist_ok=True)
    out_file = UNITS_ROOT / "retro.jsonl"

    units_def = [
        # 1. retro:unit-001 (rule: midnight-aligned time windows)
        {
            "id": "retro:unit-001",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 492,
            "origin_line_end": 492,
            "type": "rule",
            "meaning": "自然日与自然周午夜绝对对齐规则：按日（d）或周（w）指定时间跨度时，必须显式计算本地午夜零点时间戳并附带 T00:00:00 后缀传递给 --since，严禁使用相对模糊字符串导致当前运行时刻裁切失真",
            "boundary_condition": "Git 提交历史检索与复盘时段窗口参数化解析",
            "dependency_skills": [],
            "candidate_destination": "retro:midnight-aligned-window-rule",
            "validation_criteria": "生成的 --since 参数具备 YYYY-MM-DDT00:00:00 精确零点格式",
            "status": "retain"
        },
        # 2. retro:unit-002 (rule: freshness pre-flight fetch)
        {
            "id": "retro:unit-002",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 549,
            "origin_line_end": 556,
            "type": "rule",
            "meaning": "远端基线新鲜度前置拉取规范：在聚合指标前必须执行 git fetch origin <default>，若无 origin 或离线则记录失败标志并在报告中做无远端对齐披露",
            "boundary_condition": "工程复盘分析前的前置基线同步动作",
            "dependency_skills": [],
            "candidate_destination": "retro:freshness-preflight-rule",
            "validation_criteria": "成功拉取远端权威分支，并在离线时打上降级标志",
            "status": "retain"
        },
        # 3. retro:unit-003 (gate: stale base guard)
        {
            "id": "retro:unit-003",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 573,
            "origin_line_end": 578,
            "type": "gate",
            "meaning": "陈旧基线与无效窗口阻断门禁：若远端拉取成功但最新 commit 日期早于统计窗口起点（today - window），必须强行阻断复盘流程并提示排查系统时间漂移或远端拉取陈旧，防止凭空捏造无事实根据的复盘假象",
            "boundary_condition": "指标统计流水线启动前的绝对防御门禁",
            "dependency_skills": [],
            "candidate_destination": "retro:stale-base-guard",
            "validation_criteria": "捕获陈旧提交分支并阻断空洞复盘报告输出",
            "status": "retain"
        },
        # 4. retro:unit-004 (rule: user vs teammate attribution identity)
        {
            "id": "retro:unit-004",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 571,
            "origin_line_end": 571,
            "type": "rule",
            "meaning": "当前执行者身份归属法则：当前运行复盘的执行者必须统一映射为 'you'，其余作者一律归类为 teammates，确保叙事视角围绕自身产出与团队协同展开",
            "boundary_condition": "报告组织中个人视角与团队视角的结构划分",
            "dependency_skills": [],
            "candidate_destination": "retro:user-identity-attribution-rule",
            "validation_criteria": "准确区分当前开发者与协作队友的提交与指标归因",
            "status": "retain"
        },
        # 5. retro:unit-005 (rule: shortcut debt ledger)
        {
            "id": "retro:unit-005",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 791,
            "origin_line_end": 818,
            "type": "rule",
            "meaning": "工程捷径技术债台账规范：扫描代码库中显式留下的 gstack-shortcut 标记，核验是否有绑定决策 ID 以及是否声明了升级触发器（upgrade trigger），无触发器的债务必须作为静默腐化隐患重点曝光",
            "boundary_condition": "代码健康度复盘中的技术债务专项审查",
            "dependency_skills": [],
            "candidate_destination": "retro:shortcut-debt-ledger-rule",
            "validation_criteria": "准确输出技术债务清单，标记 unlinked 与 no-trigger 风险项",
            "status": "retain"
        },
        # 6. retro:unit-006 (method: load history and compare trends)
        {
            "id": "retro:unit-006",
            "source_path": "retro/SKILL.md",
            "origin_line_start": 822,
            "origin_line_end": 840,
            "type": "method",
            "meaning": "历史对比与环比趋势分析机制：读取历史 .context/retros/*.json 快照，计算测试覆盖比率、会话数、LOC/小时生产率、修复比率及深耕会话数的指标差值（Delta）并生成对比表格",
            "boundary_condition": "存在一期及以上历史复盘快照时的时序比对流程",
            "dependency_skills": [],
            "candidate_destination": "retro:load-history-and-compare",
            "validation_criteria": "正确计算增减差值与百分比，首期无历史时优雅静默降级",
            "status": "retain"
        },
        # 7. retro:unit-007 (template: tweetable summary)
        {
            "id": "retro:unit-007",
            "source_path": "retro/sections/report-format.md",
            "origin_line_start": 5,
            "origin_line_end": 8,
            "type": "template",
            "meaning": "社交级极简摘要模板：第一行输出单行紧凑速报，浓缩呈现周期、提交数、贡献者数、净增 LOC、测试行占比、PR 总量、峰值活跃时段及连续交付天数（Streak）",
            "boundary_condition": "复盘报告首行第一触点输出",
            "dependency_skills": [],
            "candidate_destination": "retro:tweetable-summary-template",
            "validation_criteria": "单行呈现关键数字，适合 10 秒快速概览",
            "status": "retain"
        },
        # 8. retro:unit-008 (rule: test health ratio guard)
        {
            "id": "retro:unit-008",
            "source_path": "retro/sections/report-format.md",
            "origin_line_start": 43,
            "origin_line_end": 48,
            "type": "rule",
            "meaning": "测试健康门禁与成长标记：统计总测试文件数、本期新增测试文件及回归测试提交；若新增代码中测试行占比低于 20%，必须强制标记为团队核心关注与薄弱成长区",
            "boundary_condition": "复盘报告中工程质量与测试健康模块的评估规范",
            "dependency_skills": [],
            "candidate_destination": "retro:test-health-ratio-rule",
            "validation_criteria": "当测试占比低于 20% 时触发告警并提出提升建议",
            "status": "retain"
        },
        # 9. retro:unit-009 (method: plan completion tracking)
        {
            "id": "retro:unit-009",
            "source_path": "retro/sections/report-format.md",
            "origin_line_start": 50,
            "origin_line_end": 71,
            "type": "method",
            "meaning": "计划达成度审计机制：调取交付审查日志中携带 plan_items_total 的记录，统计按计划交付的分支数、平均任务项完成率及最常被跳过的任务类别",
            "boundary_condition": "代码交付链路与规划计划绑定的交付效能审计",
            "dependency_skills": [],
            "candidate_destination": "retro:plan-completion-audit",
            "validation_criteria": "输出有规划交付分支数与平均项完成百分比",
            "status": "retain"
        },
        # 10. retro:unit-010 (template: personal deep-dive and team breakdown)
        {
            "id": "retro:unit-010",
            "source_path": "retro/sections/report-format.md",
            "origin_line_start": 78,
            "origin_line_end": 105,
            "type": "template",
            "meaning": "个人深度复盘与团队成员画质结构模板：为个人提供亮点表扬（Praise，锚定提交）与跃升建议（Growth），为每位队友细分交付成果、真实评价与 1 个针对性成长契机，客观披露 AI 协作比例",
            "boundary_condition": "平衡团队全貌与个人定制化成长反馈的复盘输出",
            "dependency_skills": [],
            "candidate_destination": "retro:personal-and-team-feedback-template",
            "validation_criteria": "评价全部锚定真实 Git commit，避免空洞打鸡血与非建设性批评",
            "status": "retain"
        }
    ]

    for u in units_def:
        u["raw_excerpt"] = extract_lines(u["source_path"], u["origin_line_start"], u["origin_line_end"])

    with open(out_file, "w", encoding="utf-8") as f:
        for u in units_def:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    print(f"Generated {len(units_def)} units for retro at {out_file}")

if __name__ == "__main__":
    main()
