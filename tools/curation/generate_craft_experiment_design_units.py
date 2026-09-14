#!/usr/bin/env python3
"""
Generate curation semantic units for craft-experiment-design.
Extracts units from skills/craft-experiment-design/SKILL.md.
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
    out_file = UNITS_ROOT / "craft-experiment-design.jsonl"

    units_def = [
        # 1. craft-experiment-design:unit-001 (method: experiment design 8-part framework)
        {
            "id": "craft-experiment-design:unit-001",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 28,
            "origin_line_end": 40,
            "type": "method",
            "meaning": "在线实验设计八大要素规程：覆盖假设公式化、一级裁决指标、二级辅助指标、护栏指标、受众与分流比例、长期保留组策略、时长估算及风险评估",
            "boundary_condition": "将优化思路转化为工程与数据科学可审查的完整实验设计方案",
            "dependency_skills": [],
            "candidate_destination": "experimentation:8-part-design-framework",
            "validation_criteria": "设计必须系统性完整涵盖八项要素，使用具体指标名与明确假设",
            "status": "retain"
        },
        # 2. craft-experiment-design:unit-002 (rule: falsifiable hypothesis formulation standard)
        {
            "id": "craft-experiment-design:unit-002",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 30,
            "origin_line_end": 30,
            "type": "rule",
            "meaning": "可证伪实验假设构造铁律：实验假设必须严格采用‘If we [change], then [outcome], because [rationale]’的标准公式陈述，明确因果逻辑",
            "boundary_condition": "撰写与审阅 A/B 测试方案假设时的唯一准则",
            "dependency_skills": [],
            "candidate_destination": "experimentation:falsifiable-hypothesis-rule",
            "validation_criteria": "包含明确的自变量改动、可度量产出与合理解释，杜绝模糊断言",
            "status": "retain"
        },
        # 3. craft-experiment-design:unit-003 (rule: single primary metric invariant)
        {
            "id": "craft-experiment-design:unit-003",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 31,
            "origin_line_end": 31,
            "type": "rule",
            "meaning": "单一定胜负核心指标原则：Primary Metric 必须为唯一定量指标，作为判定实验成功或失败的终极决断依据，避免多重检验偏差",
            "boundary_condition": "定义实验成功标准时的核心约束",
            "dependency_skills": [],
            "candidate_destination": "experimentation:single-primary-metric-rule",
            "validation_criteria": "实验方案中只存在唯一的裁决指标，杜绝并列核心指标",
            "status": "retain"
        },
        # 4. craft-experiment-design:unit-004 (rule: secondary metrics for unintended effects)
        {
            "id": "craft-experiment-design:unit-004",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 32,
            "origin_line_end": 32,
            "type": "rule",
            "meaning": "二级指标协同观测规范：配置 2-3 个辅助指标监测非预期衍生效应与全链路行为变化，但不得替代核心指标作为决断标准",
            "boundary_condition": "实验观测体系设计时的深度补充",
            "dependency_skills": [],
            "candidate_destination": "experimentation:secondary-metrics-guideline",
            "validation_criteria": "指标数量适中（2-3个），聚焦于捕获上下游联动行为",
            "status": "retain"
        },
        # 5. craft-experiment-design:unit-005 (gate: guardrail metrics non-degradation gate)
        {
            "id": "craft-experiment-design:unit-005",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 33,
            "origin_line_end": 33,
            "type": "gate",
            "meaning": "护栏指标不可劣化门禁：错误率、时延、留存等系统或关键体验指标必须定义明确底线阈值，一旦发生统计显著劣化，坚决否决上线",
            "boundary_condition": "实验裁决与功能全量推开前的安全熔断底线",
            "dependency_skills": [],
            "candidate_destination": "experimentation:guardrail-metrics-gate",
            "validation_criteria": "护栏指标发生劣化时严格阻断功能全量发布",
            "status": "retain"
        },
        # 6. craft-experiment-design:unit-006 (rule: long-term holdout strategy evaluation)
        {
            "id": "craft-experiment-design:unit-006",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 35,
            "origin_line_end": 35,
            "type": "rule",
            "meaning": "长期保留对照组策略审定规程：在功能推开后明确评估是否保留特定比例的 Holdout 组以持续度量长期累积因果效应与衰减，并给出理由",
            "boundary_condition": "设计大范围或深远影响特性的长期度量机制",
            "dependency_skills": [],
            "candidate_destination": "experimentation:holdout-strategy-rule",
            "validation_criteria": "显式说明是否维持保留组及其商业与度量依据",
            "status": "retain"
        },
        # 7. craft-experiment-design:unit-007 (method: baseline context integration and duration tuning)
        {
            "id": "craft-experiment-design:unit-007",
            "source_path": "craft-experiment-design/SKILL.md",
            "origin_line_start": 44,
            "origin_line_end": 47,
            "type": "method",
            "meaning": "先验基线数据注入与时长调优方法：将已有转化率、流量基数与历史测试结果注入设计方案，支撑样本量估算与护栏指标智能推荐",
            "boundary_condition": "估算实验运行周期与分配比例时的上下文校准",
            "dependency_skills": [],
            "candidate_destination": "experimentation:prior-context-tuning-method",
            "validation_criteria": "根据历史基线与流量测算合理的实验运行周期",
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

    sys.path.insert(0, "tools/curation")
    from verify import verify_unit

    print(f"Building {len(units)} units for craft-experiment-design...")
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
