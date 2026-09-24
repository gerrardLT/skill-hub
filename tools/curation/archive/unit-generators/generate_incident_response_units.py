# -*- coding: utf-8 -*-
"""
Generator for incident-response semantic units.
Extracts verbatim excerpts from skills/incident-response/SKILL.md
and references/incident-playbook.md according to Phase 3 schema (12-key format).
"""

import json
import pathlib
import sys

sys.path.insert(0, "tools/curation")
from verify import verify_unit

def extract_lines(file_path: str, start: int, end: int) -> str:
    path = pathlib.Path("skills") / file_path
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1:end])

def build_units():
    units_def = [
        # 1. incident-response:unit-001 (gate: detection acknowledgment SLA gate)
        {
            "id": "incident-response:unit-001",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 55,
            "origin_line_end": 61,
            "type": "gate",
            "meaning": "事故探测确认与响应 SLA 门禁：在告警触发后的目标时限内（严重事故通常 5-15 分钟）必须完成确权，评估等级、呼叫值班人员并建立专属应急频道",
            "boundary_condition": "收到监控报警、用户报告或内部异常上报时的初次响应入口门禁",
            "dependency_skills": [],
            "candidate_destination": "incident:detection-acknowledgment-sla-gate",
            "validation_criteria": "在规定时限内完成确权响应并成功拉起应急沟通渠道",
            "status": "retain"
        },
        # 2. incident-response:unit-002 (rule: severity rubric and triage classification)
        {
            "id": "incident-response:unit-002",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 66,
            "origin_line_end": 76,
            "type": "rule",
            "meaning": "事故严重度分级准则与定损分类规则：基于核心功能影响面、数据完整性风险、安全渗透及收入损失将事故划分为 SEV-1 到 SEV-4 并绑定对应组织响应标准",
            "boundary_condition": "探测后确定响应规模与资源投入的分级定损阶段",
            "dependency_skills": [],
            "candidate_destination": "incident:severity-rubric-and-classification",
            "validation_criteria": "依据明确特征界定事故严重级别，并支持随处置信息逐步修正",
            "status": "retain"
        },
        # 3. incident-response:unit-003 (gate: mitigate first and stop bleeding rule)
        {
            "id": "incident-response:unit-003",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 77,
            "origin_line_end": 92,
            "type": "gate",
            "meaning": "止血优先于排查根因铁律门禁：在用户受损状态下，以最快速度采取回滚、关停开关、主从切换、扩容限流等止血模式，坚决禁止带病排查根因",
            "boundary_condition": "用户仍在遭受业务中断时的技术处置第一优先级",
            "dependency_skills": [],
            "candidate_destination": "incident:mitigate-first-principle-gate",
            "validation_criteria": "优先执行有效止血动作阻止用户影响扩散，根因分析移至后续排查",
            "status": "retain"
        },
        # 4. incident-response:unit-004 (rule: structured three-audience communication cadence)
        {
            "id": "incident-response:unit-004",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 93,
            "origin_line_end": 117,
            "type": "rule",
            "meaning": "三类受众结构化沟通节奏与守时原则：面向内部团队（15分钟高频）、管理层（30-60分钟业务视角）与外部客户（30分钟无指责通告），坚决按时更新并杜绝盲目猜测根因",
            "boundary_condition": "活跃事故处置全过程的信息同步与预期管理",
            "dependency_skills": [],
            "candidate_destination": "incident:three-audience-communication-cadence",
            "validation_criteria": "遵守既定时间窗发布客观事实通报，无进展时明确陈述正在调查",
            "status": "retain"
        },
        # 5. incident-response:unit-005 (gate: explicit resolution criteria and post-closure protocol)
        {
            "id": "incident-response:unit-005",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 121,
            "origin_line_end": 135,
            "type": "gate",
            "meaning": "事故闭环核验标准与复盘排期门禁：必须完成止血验证、系统全量复原与最终通报方可关闭事故，且必须在 1-2 周内排期 AAR 复盘",
            "boundary_condition": "事故结束与向常态运营交接的终验门禁",
            "dependency_skills": [],
            "candidate_destination": "incident:resolution-criteria-and-closure-gate",
            "validation_criteria": "业务旅程恢复核验通过，最终通告已发布，初始时间线完整归档",
            "status": "retain"
        },
        # 6. incident-response:unit-006 (rule: explicit incident roles and non-overlapping responsibilities)
        {
            "id": "incident-response:unit-006",
            "source_path": "incident-response/SKILL.md",
            "origin_line_start": 138,
            "origin_line_end": 149,
            "type": "rule",
            "meaning": "应急响应核心角色权责分离架构：划分事故指挥官 (IC)、沟通负责人 (Comms Lead)、技术处置负责人 (Ops Lead) 与记录员 (Scribe) 的专有职责，杜绝多头指挥与协同真空",
            "boundary_condition": "组织应急力量协同处置事故的权责基石",
            "dependency_skills": [],
            "candidate_destination": "incident:roles-and-responsibilities-architecture",
            "validation_criteria": "IC 专注于决策与协调，Comms 分流沟通负担，Ops 专注技术止血，Scribe 留存时间线",
            "status": "retain"
        },
        # 7. incident-response:unit-007 (rule: rollback decision rubric)
        {
            "id": "incident-response:unit-007",
            "source_path": "incident-response/references/incident-playbook.md",
            "origin_line_start": 169,
            "origin_line_end": 182,
            "type": "rule",
            "meaning": "代码部署回滚决策判定准则：近期发布与故障相关且回滚安全时果断回滚；存在疑虑时果断选择回滚，其恢复成本通常远低于破损状态下的带伤排查",
            "boundary_condition": "评估最近发布变更对线上事故影响时的回滚裁决",
            "dependency_skills": [],
            "candidate_destination": "incident:rollback-decision-rubric",
            "validation_criteria": "准确权衡回滚与就地修复风险，以最低成本恢复稳定基线",
            "status": "retain"
        },
        # 8. incident-response:unit-008 (rule: public status page communication anti-patterns and templates)
        {
            "id": "incident-response:unit-008",
            "source_path": "incident-response/references/incident-playbook.md",
            "origin_line_start": 136,
            "origin_line_end": 165,
            "type": "rule",
            "meaning": "公开状态页（Status Page）模板与反模式避坑指南：采用阶段化客观模板（调查中/已确认/监控中/已恢复），坚决规避含糊言辞、空洞承诺、技术黑话与供应商推诿指责",
            "boundary_condition": "对外向用户与公众发布服务健康通告时的表达规范",
            "dependency_skills": [],
            "candidate_destination": "incident:status-page-templates-and-anti-patterns",
            "validation_criteria": "通告语言通俗客观、精确限定影响范围，并附带可信的时间承诺",
            "status": "retain"
        },
        # 9. incident-response:unit-009 (method: common symptom mitigation patterns)
        {
            "id": "incident-response:unit-009",
            "source_path": "incident-response/references/incident-playbook.md",
            "origin_line_start": 238,
            "origin_line_end": 251,
            "type": "method",
            "meaning": "常见故障症状快速止血模式映射表：针对发布后报错、配置变更、数据库连接池耗尽、延迟飙升、安全攻击等典型场景，提供首选止血动作映射",
            "boundary_condition": "技术排查阶段依据初始症状快速决定首要止血手段",
            "dependency_skills": [],
            "candidate_destination": "incident:symptom-mitigation-patterns-mapping",
            "validation_criteria": "根据典型故障表象快速匹配回滚、关停开关、连接池扩容或系统隔离手段",
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

    return units

def main():
    skills_root = pathlib.Path("skills")
    units = build_units()
    print(f"Building {len(units)} units for incident-response...")

    output_path = pathlib.Path("curation/units/incident-response.jsonl")
    lines = []
    for u in units:
        errs, matches = verify_unit(u, skills_root)
        if errs or not matches:
            print(f"Unit {u['id']} validation failed: {errs}, matches={matches}")
            sys.exit(1)
        lines.append(json.dumps(u, ensure_ascii=False))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Successfully generated and validated {len(units)} units into {output_path}")

if __name__ == "__main__":
    main()
