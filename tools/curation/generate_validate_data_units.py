#!/usr/bin/env python3
"""
Generate curation semantic units for validate-data.
Extracts units from skills/validate-data/SKILL.md.
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
    out_file = UNITS_ROOT / "validate-data.jsonl"

    units_def = [
        # 1. validate-data:unit-001 (method: end-to-end data analysis validation workflow)
        {
            "id": "validate-data:unit-001",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 26,
            "origin_line_end": 96,
            "type": "method",
            "meaning": "数据分析交付前质量验证全流程：涵盖方法论审查、QA清单执行、经典陷阱排查、计算抽检、可视化失真检查、叙述结论评估至生成三级置信度评级",
            "boundary_condition": "向业务或管理层汇报前对数据分析成果实施系统性质检",
            "dependency_skills": [],
            "candidate_destination": "data-qa:validation-workflow",
            "validation_criteria": "包含方法论、计算、可视化、叙述与置信度评级（Ready to share / Share with caveats / Needs revision）完整步骤",
            "status": "retain"
        },
        # 2. validate-data:unit-002 (template: validation report schema)
        {
            "id": "validate-data:unit-002",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 97,
            "origin_line_end": 125,
            "type": "template",
            "meaning": "数据验证报告模板：输出总体评估评级、方法论审查、问题列表（含高/中/低严重度与影响）、抽检结果、可视化审查、改进建议与必要声明",
            "boundary_condition": "规范化呈现数据分析审查结论的标准结构",
            "dependency_skills": [],
            "candidate_destination": "data-qa:validation-report-template",
            "validation_criteria": "结构包含分级评估、发现的问题、抽检状态与声明清单",
            "status": "retain"
        },
        # 3. validate-data:unit-003 (method: pre-delivery QA checklist)
        {
            "id": "validate-data:unit-003",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 129,
            "origin_line_end": 166,
            "type": "method",
            "meaning": "数据交付前 QA 四维核查清单：逐项扫描数据质量检查（源、新鲜度、完备性、空值、去重、过滤）、计算检查（聚合、分母、日期、JOIN、口径、求和）、合理性检查与呈现检查",
            "boundary_condition": "数据分析报告定稿前的机械化检查门禁",
            "dependency_skills": [],
            "candidate_destination": "data-qa:pre-delivery-qa-checklist",
            "validation_criteria": "全量覆盖数据质量、计算正确性、常理合理性与格式呈现四维度",
            "status": "retain"
        },
        # 4. validate-data:unit-004 (rule: join explosion prevention rule)
        {
            "id": "validate-data:unit-004",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 169,
            "origin_line_end": 184,
            "type": "rule",
            "meaning": "多对多 JOIN 膨胀防错铁律：多表连接必须通过对比连接前后行数（`SELECT COUNT(*)`）进行核验，对跨表统计实体强制使用 `COUNT(DISTINCT a.id)` 避免非预期行数翻倍",
            "boundary_condition": "编写与审查复杂多表 SQL 查询时的计算准则",
            "dependency_skills": [],
            "candidate_destination": "data-qa:join-explosion-guard",
            "validation_criteria": "行数增长超出预期时必须停机排查关联基数",
            "status": "retain"
        },
        # 5. validate-data:unit-005 (rule: survivorship bias detection rule)
        {
            "id": "validate-data:unit-005",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 185,
            "origin_line_end": 195,
            "type": "rule",
            "meaning": "幸存者偏差排查法则：在得出任何结论前必须自问‘谁不在这个数据集中’，避免仅分析现存/活跃/成功实体而丢失流失、失败群体的真实全貌",
            "boundary_condition": "定义分析样本人群与提取历史数据时的思维防线",
            "dependency_skills": [],
            "candidate_destination": "data-qa:survivorship-bias-detection",
            "validation_criteria": "明确核查已被删除、流失或评估未通过的实体是否被误过滤",
            "status": "retain"
        },
        # 6. validate-data:unit-006 (rule: incomplete period comparison guard)
        {
            "id": "validate-data:unit-006",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 196,
            "origin_line_end": 205,
            "type": "rule",
            "meaning": "未完成时间窗口对比拦截铁律：严禁将尚未结束的局部时段（如周中、月中进行中的指标）与已终结的历史完整周期直接汇总对比，必须截取相同天数或对齐至完整周期",
            "boundary_condition": "进行环比、同比或阶段业绩度量时的基准约束",
            "dependency_skills": [],
            "candidate_destination": "data-qa:incomplete-period-comparison-guard",
            "validation_criteria": "严格保障对比周期的时间天数与采样边界完全对齐",
            "status": "retain"
        },
        # 7. validate-data:unit-007 (rule: average of averages prohibition rule)
        {
            "id": "validate-data:unit-007",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 216,
            "origin_line_end": 227,
            "type": "rule",
            "meaning": "预计算均值二次求平均绝对禁止铁律：当子群样本量不一时，对预计算均值取简单平均必定导致数学失真，必须回到明细源数据重新聚合或执行加权平均",
            "boundary_condition": "跨分群、跨部门或跨层级汇总均值时的数学准则",
            "dependency_skills": [],
            "candidate_destination": "data-qa:prohibit-average-of-averages",
            "validation_criteria": "坚决禁止 `(avg_a + avg_b) / 2`，强制采用样本量加权计算",
            "status": "retain"
        },
        # 8. validate-data:unit-008 (rule: outcome-based selection bias guard)
        {
            "id": "validate-data:unit-008",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 238,
            "origin_line_end": 247,
            "type": "rule",
            "meaning": "因果倒置与选择性分群偏差防范法则：严禁使用待测结果指标（如是否完成某动作）来逆向定义分群自变量，分群必须严格基于实验/处理前的初始特征",
            "boundary_condition": "设计分群对比与因果推断分析时的定义基石",
            "dependency_skills": [],
            "candidate_destination": "data-qa:selection-bias-prevention",
            "validation_criteria": "确保分群变量在时间轴上先于结果变量产生，杜绝循环论证",
            "status": "retain"
        },
        # 9. validate-data:unit-009 (method: magnitude and cross-validation techniques)
        {
            "id": "validate-data:unit-009",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 258,
            "origin_line_end": 288,
            "type": "method",
            "meaning": "数量级与多途径交叉验证技术：包含通过两种不同逻辑独立反算相同指标、手工追踪单个明细记录、与大盘对照、反向工程验算、边界值检查及五大约束异动红线预警",
            "boundary_condition": "对计算结果开展独立有效性压力测试的验证手段",
            "dependency_skills": [],
            "candidate_destination": "data-qa:magnitude-and-cross-validation",
            "validation_criteria": "至少采用两种不同计算途径交叉核对核心数值，捕捉非预期异动",
            "status": "retain"
        },
        # 10. validate-data:unit-010 (template: reproducible analysis documentation standard)
        {
            "id": "validate-data:unit-010",
            "source_path": "validate-data/SKILL.md",
            "origin_line_start": 289,
            "origin_line_end": 330,
            "type": "template",
            "meaning": "可复现数据分析文档标准模板：明确规范分析问题、数据源（表名与快照日期）、指标/分群精准口径、方法步骤、假设与局限、关键发现、带注SQL查询与局限声明",
            "boundary_condition": "沉淀可传承、支持第三方复现审计的数据分析资产文档",
            "dependency_skills": [],
            "candidate_destination": "data-qa:reproducible-documentation-standard",
            "validation_criteria": "第三方依据该文档即可在相同数据源上 100% 独立复现分析结果",
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

    print(f"Building {len(units)} units for validate-data...")
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
