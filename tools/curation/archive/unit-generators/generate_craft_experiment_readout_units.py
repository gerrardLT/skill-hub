#!/usr/bin/env python3
"""
Generate curation semantic units for craft-experiment-readout.
Extracts units from skills/craft-experiment-readout/SKILL.md.
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
    out_file = UNITS_ROOT / "craft-experiment-readout.jsonl"

    units_def = [
        # 1. craft-experiment-readout:unit-001 (method: 7-part experiment readout framework)
        {
            "id": "craft-experiment-readout:unit-001",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 30,
            "origin_line_end": 39,
            "type": "method",
            "meaning": "实验复盘报告 7 大核心要素结构：包含一句话执行摘要、假设回溯、核心指标结果与双重显著性核验、获胜方诚实判定、分群异质性分析、三元决断建议（Ship/Iterate/Kill）与长远经验萃取",
            "boundary_condition": "A/B 测试或在线实验数据回收完成后的收官复盘规程",
            "dependency_skills": [],
            "candidate_destination": "experimentation:7-part-readout-framework",
            "validation_criteria": "结构完备，覆盖统计结果、分群下钻、明确决策与组织级认知积累",
            "status": "retain"
        },
        # 2. craft-experiment-readout:unit-002 (template: stakeholder communication draft)
        {
            "id": "craft-experiment-readout:unit-002",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 40,
            "origin_line_end": 47,
            "type": "template",
            "meaning": "利益相关方通报模板与沟通规范：包含 1-2 句核心结论 TL;DR、对受众业务的直接影响（Impact）、带责任人与时间表的下一步行动（Next Steps），采用通俗平实语言杜绝统计黑话",
            "boundary_condition": "向管理层、工程团队或全员发布实验结果通报的标准模版",
            "dependency_skills": [],
            "candidate_destination": "experimentation:stakeholder-communication-template",
            "validation_criteria": "TL;DR 具备 30 秒通读行动力，Next Steps 明确动作责任人",
            "status": "retain"
        },
        # 3. craft-experiment-readout:unit-003 (rule: statistical vs practical significance check)
        {
            "id": "craft-experiment-readout:unit-003",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 34,
            "origin_line_end": 34,
            "type": "rule",
            "meaning": "双重显著性判定原则：在呈现关键指标数据时，必须同时明确标出统计显著性（Statistical Significance）与实际商业显著性（Practical Significance），排除统计上显著但实际收益极微弱的变体",
            "boundary_condition": "审查实验指标收益时的决策准则",
            "dependency_skills": [],
            "candidate_destination": "experimentation:statistical-and-practical-significance-rule",
            "validation_criteria": "综合考量置信区间与工程上线维护成本，杜绝盲信 p 值",
            "status": "retain"
        },
        # 4. craft-experiment-readout:unit-004 (rule: honesty in ambiguous results)
        {
            "id": "craft-experiment-readout:unit-004",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 35,
            "origin_line_end": 35,
            "type": "rule",
            "meaning": "模糊结果诚实判定法则：当测试指标未达显著性或变体间呈现冲突时，坚决声明为 inconclusive，严禁为了交差强行宣布获胜方",
            "boundary_condition": "裁决统计不显著或模糊实验时的职业道德准则",
            "dependency_skills": [],
            "candidate_destination": "experimentation:honesty-in-ambiguity-rule",
            "validation_criteria": "对模糊测试给出客观归因与下一步重测或放弃建议",
            "status": "retain"
        },
        # 5. craft-experiment-readout:unit-005 (rule: user segment variation analysis)
        {
            "id": "craft-experiment-readout:unit-005",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 36,
            "origin_line_end": 36,
            "type": "rule",
            "meaning": "用户分群异质性下钻分析规范：在汇总大盘指标之外，必须排查不同受众群体（如新用户与老用户、免费与付费方案、不同平台）间的效应分化，防止大盘中和遮蔽细分人群的强烈不满",
            "boundary_condition": "深入分析实验效果背后的受众结构差异",
            "dependency_skills": [],
            "candidate_destination": "experimentation:segment-heterogeneity-analysis",
            "validation_criteria": "按核心维度拆分指标走势，暴露局部抵消或特定群体的异常",
            "status": "retain"
        },
        # 6. craft-experiment-readout:unit-006 (rule: decisive three-way recommendation)
        {
            "id": "craft-experiment-readout:unit-006",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 37,
            "origin_line_end": 37,
            "type": "rule",
            "meaning": "清晰明确的三元行动决断铁律：建议必须直接落地到 Ship（全量推开）、Iterate（调整迭代）或 Kill（彻底下线）之一，并定义具体的下一步执行步骤",
            "boundary_condition": "实验复盘向工程与运营交付结论时的决断要求",
            "dependency_skills": [],
            "candidate_destination": "experimentation:ship-iterate-kill-recommendation",
            "validation_criteria": "明确在发布、迭代、放弃中定性，杜绝含糊其辞",
            "status": "retain"
        },
        # 7. craft-experiment-readout:unit-007 (method: audience-tailored communication framing)
        {
            "id": "craft-experiment-readout:unit-007",
            "source_path": "craft-experiment-readout/SKILL.md",
            "origin_line_start": 53,
            "origin_line_end": 56,
            "type": "method",
            "meaning": "受众定制化沟通适配规程：针对不同利益相关方（高管侧重商业底线，工程侧重稳定性与架构，全员侧重业务认知）调整复盘通报的侧重点与语言风格，复用成熟模板实现高效沟通",
            "boundary_condition": "将实验结论分层对齐至跨职能组织的协同实践",
            "dependency_skills": [],
            "candidate_destination": "experimentation:audience-tailored-communication",
            "validation_criteria": "根据受众层级精确匹配技术细节深度与战略影响表达",
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

    print(f"Building {len(units)} units for craft-experiment-readout...")
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
