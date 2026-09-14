#!/usr/bin/env python3
"""
Generate curation semantic units for metrics-review.
Extracts units from skills/metrics-review/SKILL.md.
"""

import json
from pathlib import Path

SKILLS_ROOT = Path("skills")
UNITS_ROOT = Path("curation/units")

def extract_lines(file_rel_path: str, start: int, end: int) -> str:
    full_path = SKILLS_ROOT / file_rel_path
    lines = full_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1:end])

def main():
    UNITS_ROOT.mkdir(parents=True, exist_ok=True)
    out_file = UNITS_ROOT / "metrics-review.jsonl"

    units_def = [
        # 1. metrics-review:unit-001 (method: metrics review workflow and scorecard generation)
        {
            "id": "metrics-review:unit-001",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 19,
            "origin_line_end": 58,
            "type": "method",
            "meaning": "产品指标复盘标准工作流：从收集数据、构建层级、分析趋势（当前值、趋势、目标对比、变化率、异常值与分群相关性）到驱动下钻",
            "boundary_condition": "组织和开展周期性产品指标审查时的标准流程",
            "dependency_skills": [],
            "candidate_destination": "metrics:review-workflow-and-trend-analysis",
            "validation_criteria": "包含基线对比、层级组织与相关性/分群归因分析步骤",
            "status": "retain"
        },
        # 2. metrics-review:unit-002 (template: executive summary and scorecard report schema)
        {
            "id": "metrics-review:unit-002",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 61,
            "origin_line_end": 100,
            "type": "template",
            "meaning": "指标复盘报告标准化结构与计分卡 Schema：包含2-3句执行摘要、表格化指标计分卡、亮点、隐患、行动建议及上下文局限说明",
            "boundary_condition": "将数据分析结果呈现给团队与利益相关方时的报告模式",
            "dependency_skills": [],
            "candidate_destination": "metrics:scorecard-and-report-structure",
            "validation_criteria": "具备计分卡表格（Metric/Current/Previous/Change/Target/Status）与明确的行动建议分类",
            "status": "retain"
        },
        # 3. metrics-review:unit-003 (rule: actionability and decision-driving principle)
        {
            "id": "metrics-review:unit-003",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 89,
            "origin_line_end": 95,
            "type": "rule",
            "meaning": "指标分析动作转化铁律：指标审查必须输出明确的后续动作分类（深入调查排查、A/B 实验假设、重点投入、阈值监控告警），严禁无动作的纯数字堆砌",
            "boundary_condition": "评估指标复盘交付质量与有效性的核心门禁",
            "dependency_skills": [],
            "candidate_destination": "metrics:actionable-recommendations-rule",
            "validation_criteria": "每项隐患或异动均能映射到具体的工程或产品动作分类",
            "status": "retain"
        },
        # 4. metrics-review:unit-004 (rule: North Star metric definition and criteria)
        {
            "id": "metrics-review:unit-004",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 111,
            "origin_line_end": 125,
            "type": "rule",
            "meaning": "北极星指标定义模式与四大特征：必须具备价值对齐性、先行预测性、团队可操作性与通俗易懂性，并按协作、交易、SaaS等产品形态给出范式",
            "boundary_condition": "构建产品指标层级顶层框架时的设计准则",
            "dependency_skills": [],
            "candidate_destination": "metrics:north-star-definition-pattern",
            "validation_criteria": "指标紧密挂钩核心用户价值与长期留存，而非短视商业指标",
            "status": "retain"
        },
        # 5. metrics-review:unit-005 (rule: L1 health indicators across user lifecycle)
        {
            "id": "metrics-review:unit-005",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 126,
            "origin_line_end": 166,
            "type": "rule",
            "meaning": "L1 核心健康指标体系模式：映射至用户全生命周期的六大维度（Acquisition获客、Activation激活、Engagement活跃、Retention留存、Monetization变现、Satisfaction满意度）",
            "boundary_condition": "衡量产品全局健康度与瓶颈定位时的维度分解",
            "dependency_skills": [],
            "candidate_destination": "metrics:l1-lifecycle-health-indicators",
            "validation_criteria": "全面覆盖转化率、时间到达、粘性比例、队列留存、NRR 与 NPS/CSAT",
            "status": "retain"
        },
        # 6. metrics-review:unit-006 (rule: retention and cohort analysis methodology)
        {
            "id": "metrics-review:unit-006",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 190,
            "origin_line_end": 203,
            "type": "rule",
            "meaning": "留存率与队列（Cohort）分析规范：关注 D1/D7/D30 周期留存曲线，识别初期流失（激活问题）与平缓拐点（稳固基线），对比新老队列评估改进效果",
            "boundary_condition": "度量产品持久价值与健康留存基线的核心分析方法",
            "dependency_skills": [],
            "candidate_destination": "metrics:retention-and-cohort-methodology",
            "validation_criteria": "绘制并对比分群留存曲线，准确区分激活与长期参与度缺陷",
            "status": "retain"
        },
        # 7. metrics-review:unit-007 (method: OKR and metric target setting framework)
        {
            "id": "metrics-review:unit-007",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 235,
            "origin_line_end": 274,
            "type": "method",
            "meaning": "OKR 目标制定与指标 Target 设定规程：KR 必须衡量业务结果而非交付产出，结合历史基线、行业基准、趋势轨迹与资源投入设定 Commit 与 Stretch 目标",
            "boundary_condition": "季度业务目标规划与指标打分复盘时的操作准则",
            "dependency_skills": [],
            "candidate_destination": "metrics:okr-and-target-setting-framework",
            "validation_criteria": "KR 具备可量化产出、合理挑战度（70%达成率为佳）并支持中期调优",
            "status": "retain"
        },
        # 8. metrics-review:unit-008 (method: multi-tier review cadences)
        {
            "id": "metrics-review:unit-008",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 275,
            "origin_line_end": 317,
            "type": "method",
            "meaning": "多层级指标复盘频次模式：周检（15-30m，速览北极星与异常）、月会（30-60m，深入L1与队列）、季报（60-90m，QBR/OKR评分与战略调优）的权责与议程矩阵",
            "boundary_condition": "建立团队持续数据治理与复盘节奏的组织实践",
            "dependency_skills": [],
            "candidate_destination": "metrics:review-cadence-matrix",
            "validation_criteria": "明确区分各周期会议的参会对象、核心议题与产出动作",
            "status": "retain"
        },
        # 9. metrics-review:unit-009 (rule: dashboard anti-patterns and vanity metrics)
        {
            "id": "metrics-review:unit-009",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 355,
            "origin_line_end": 362,
            "type": "rule",
            "meaning": "大盘设计反模式与虚荣指标避坑：严禁仅展示单调递增的虚荣指标、超出一屏的过多指标、缺少基准对比的孤立数值、陈旧指标、过程产出指标与千人一面通用大盘",
            "boundary_condition": "审查与重构产品数据大盘时的防错准则",
            "dependency_skills": [],
            "candidate_destination": "metrics:dashboard-anti-patterns",
            "validation_criteria": "识别并剔除无行动价值的虚假增长指标与混乱大盘设计",
            "status": "retain"
        },
        # 10. metrics-review:unit-010 (rule: attribution caution and segment mask rule)
        {
            "id": "metrics-review:unit-010",
            "source_path": "metrics-review/SKILL.md",
            "origin_line_start": 380,
            "origin_line_end": 388,
            "type": "rule",
            "meaning": "归因审慎与分群掩蔽破除法则：严禁将相关性断言为因果关系；当整体宏观指标平稳时，必须强制执行分群下钻以暴露局部抵消的结构性风险",
            "boundary_condition": "进行深度业务数据解读与策略制定的思考铁律",
            "dependency_skills": [],
            "candidate_destination": "metrics:attribution-caution-and-segment-masking",
            "validation_criteria": "分析中明确指出归因不确定性，且通过分群排查宏观平缓下的微观剧变",
            "status": "retain"
        }
    ]

    units = []
    for item in units_def:
        raw_excerpt = extract_lines(
            item["source_path"],
            item["origin_line_start"],
            item["origin_line_end"]
        )
        unit = {
            "id": item["id"],
            "source_path": item["source_path"],
            "origin_line_start": item["origin_line_start"],
            "origin_line_end": item["origin_line_end"],
            "type": item["type"],
            "raw_excerpt": raw_excerpt,
            "meaning": item["meaning"],
            "boundary_condition": item["boundary_condition"],
            "dependency_skills": item["dependency_skills"],
            "candidate_destination": item["candidate_destination"],
            "validation_criteria": item["validation_criteria"],
            "status": item["status"]
        }
        units.append(unit)

    # Validate each unit using verify.py
    import sys
    sys.path.insert(0, "tools/curation")
    from verify import verify_unit

    print(f"Building {len(units)} units for metrics-review...")
    with open(out_file, "w", encoding="utf-8") as f:
        for u in units:
            errs, matches = verify_unit(u, skills_root=SKILLS_ROOT)
            if errs or not matches:
                print(f"Unit {u['id']} validation failed: {errs}, matches={matches}")
                sys.exit(1)
            # Verify verbatim match with source
            source_file = SKILLS_ROOT / u["source_path"]
            source_content = source_file.read_text(encoding="utf-8").splitlines()
            expected = "\n".join(source_content[u["origin_line_start"]-1:u["origin_line_end"]])
            if u["raw_excerpt"] != expected:
                print(f"Unit {u['id']} verbatim mismatch!")
                sys.exit(1)
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    print(f"Successfully generated and validated {len(units)} units into {out_file}")

if __name__ == "__main__":
    main()
