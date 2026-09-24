#!/usr/bin/env python3
"""
Generate curation semantic units for analyzing-user-feedback.
Extracts units from skills/analyzing-user-feedback/SKILL.md,
skills/analyzing-user-feedback/references/artifacts.md,
and skills/analyzing-user-feedback/references/guest-insights.md.
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
    out_file = UNITS_ROOT / "analyzing-user-feedback.jsonl"

    units_def = [
        # 1. analyzing-user-feedback:unit-001 (rule: experiential empathy and problem-solving separation)
        {
            "id": "analyzing-user-feedback:unit-001",
            "source_path": "analyzing-user-feedback/SKILL.md",
            "origin_line_start": 21,
            "origin_line_end": 25,
            "type": "rule",
            "meaning": "体验式共情与解法解耦铁律：组织跨职能走查时严格遵循‘不准使用内部行话、不是来解决问题或提BUG’两大规则，沉浸式体验用户原生摩擦",
            "boundary_condition": "组织内部产品走查或沉浸式体验会时的前置纪律",
            "dependency_skills": [],
            "candidate_destination": "feedback:experiential-empathy-discipline",
            "validation_criteria": "体验阶段坚决推迟解决方案讨论，全心记录原生操作阻碍",
            "status": "retain"
        },
        # 2. analyzing-user-feedback:unit-002 (rule: mandatory service participation)
        {
            "id": "analyzing-user-feedback:unit-002",
            "source_path": "analyzing-user-feedback/SKILL.md",
            "origin_line_start": 26,
            "origin_line_end": 30,
            "type": "rule",
            "meaning": "全员业务核心服务强制实践规范：要求全体员工（包括高管与产研）定期亲历业务核心履约或服务（如跑腿、客服），建立真实共情并捕获深层运营缺陷",
            "boundary_condition": "建立企业全员用户同理心与一线运营连接机制",
            "dependency_skills": [],
            "candidate_destination": "feedback:mandatory-service-participation",
            "validation_criteria": "制度化设定员工履约频次，将现场摩擦转化为产品质量抓手",
            "status": "retain"
        },
        # 3. analyzing-user-feedback:unit-003 (rule: statistical representation filtering)
        {
            "id": "analyzing-user-feedback:unit-003",
            "source_path": "analyzing-user-feedback/SKILL.md",
            "origin_line_start": 36,
            "origin_line_end": 40,
            "type": "rule",
            "meaning": "统计代表性过滤法则：声音大不等于需求广，必须严格审查发声群体的身份与大盘占比，杜绝被嗓门最大的极客少数派绑架",
            "boundary_condition": "评估高声量抗议或客诉时的理性甄别准则",
            "dependency_skills": [],
            "candidate_destination": "feedback:statistical-representation-filtering",
            "validation_criteria": "审查反馈者的大盘占比（是否达10%）与实际人群代表性",
            "status": "retain"
        },
        # 4. analyzing-user-feedback:unit-004 (rule: balanced feedback portfolio framework)
        {
            "id": "analyzing-user-feedback:unit-004",
            "source_path": "analyzing-user-feedback/references/artifacts.md",
            "origin_line_start": 7,
            "origin_line_end": 11,
            "type": "rule",
            "meaning": "平衡反馈组合全景法则：各反馈渠道均有特定偏见（社媒偏极客、工单偏挫折、销售偏预期），PM必须维护包含多渠道的平衡反馈组合以消除盲区",
            "boundary_condition": "搭建产品日常用户反馈输入通路时的架构设计",
            "dependency_skills": [],
            "candidate_destination": "feedback:balanced-portfolio-framework",
            "validation_criteria": "明确标出各渠道偏差并在综合决策时互相对冲校准",
            "status": "retain"
        },
        # 5. analyzing-user-feedback:unit-005 (method: Complaint-Storms exercise)
        {
            "id": "analyzing-user-feedback:unit-005",
            "source_path": "analyzing-user-feedback/references/artifacts.md",
            "origin_line_start": 12,
            "origin_line_end": 16,
            "type": "method",
            "meaning": "体验吐槽风暴（Complaint-Storms）操作规程：跨职能团队先投影邻近竞品逐屏记录困惑与痛点，随后以同等严苛标准审查自家产品屏幕",
            "boundary_condition": "打破内部认知盲区、建立敏锐产品批判视角的团队工作坊",
            "dependency_skills": [],
            "candidate_destination": "feedback:complaint-storms-methodology",
            "validation_criteria": "按5步流程先竞品后自身逐屏走查，详尽输出摩擦清单",
            "status": "retain"
        },
        # 6. analyzing-user-feedback:unit-006 (method: Representation x Influence Matrix)
        {
            "id": "analyzing-user-feedback:unit-006",
            "source_path": "analyzing-user-feedback/references/artifacts.md",
            "origin_line_start": 27,
            "origin_line_end": 45,
            "type": "method",
            "meaning": "代表性与影响力二维评估矩阵（Representation × Influence）：结合受众占比（>=10%）与人际号召力划分四大象限，高代表性×高影响力优先行动，低代表性×低影响力理性暂缓并解释原因",
            "boundary_condition": "海量客诉与建议的优先级定级与过滤裁决",
            "dependency_skills": [],
            "candidate_destination": "feedback:representation-influence-matrix",
            "validation_criteria": "明确归入四大象限，并附带针对非采纳群体的解释沟通机制",
            "status": "retain"
        },
        # 7. analyzing-user-feedback:unit-007 (method: Depth of Effect x Breadth of Effect matrix)
        {
            "id": "analyzing-user-feedback:unit-007",
            "source_path": "analyzing-user-feedback/references/artifacts.md",
            "origin_line_start": 46,
            "origin_line_end": 66,
            "type": "method",
            "meaning": "影响深度与广度决策矩阵（Depth × Breadth）：以影响广度为横轴、影响深度为纵轴，右上立即执行，左下果断放弃，模糊象限结合信任资产、战略目标与顾问委员会审慎决策",
            "boundary_condition": "评估复杂功能改动或争议性需求时的取舍裁决",
            "dependency_skills": [],
            "candidate_destination": "feedback:depth-breadth-prioritization-matrix",
            "validation_criteria": "准确判定特征所处象限，并引入 Trust Vault 进行边缘仲裁",
            "status": "retain"
        },
        # 8. analyzing-user-feedback:unit-008 (method: Trust Vault measurement and management)
        {
            "id": "analyzing-user-feedback:unit-008",
            "source_path": "analyzing-user-feedback/references/artifacts.md",
            "origin_line_start": 82,
            "origin_line_end": 101,
            "type": "method",
            "meaning": "用户信任资产库（The Trust Vault）度量与运作体系：将社区信任作为可充值与透支的资产管理，季度轻量调研量化得分，低分期推迟争议发布、前置补齐体验赢点（MEOWs）",
            "boundary_condition": "重大争议性发布或激进改版前的风险评估与节奏调控",
            "dependency_skills": [],
            "candidate_destination": "feedback:trust-vault-governance",
            "validation_criteria": "采用0-6分度量，根据信任库水位调整发布节奏或追加信任储蓄",
            "status": "retain"
        },
        # 9. analyzing-user-feedback:unit-009 (method: centralized feedback and ops bridge)
        {
            "id": "analyzing-user-feedback:unit-009",
            "source_path": "analyzing-user-feedback/references/guest-insights.md",
            "origin_line_start": 20,
            "origin_line_end": 30,
            "type": "method",
            "meaning": "产品运营双向反馈桥梁构建规程：设立专职 Product Operations 嵌入产研团队并对运营负责，将分布式一线市场客诉过滤为中心研发可规模化解决的共性技术课题",
            "boundary_condition": "跨国或多业务线规模化运营下的产研与一线协同架构",
            "dependency_skills": [],
            "candidate_destination": "feedback:product-ops-bridge-architecture",
            "validation_criteria": "形成双向闭环，将局部现场感知提炼为全局通用技术方案",
            "status": "retain"
        },
        # 10. analyzing-user-feedback:unit-010 (method: AI-driven autonomous document clustering)
        {
            "id": "analyzing-user-feedback:unit-010",
            "source_path": "analyzing-user-feedback/references/guest-insights.md",
            "origin_line_start": 46,
            "origin_line_end": 56,
            "type": "method",
            "meaning": "大模型命令行智能体自动化文档分析规程：利用 CLI 代理自主扫描大容量访谈纪要与客诉文本，维护 Notebook 知识本提炼跨文档的核心共性洞察",
            "boundary_condition": "利用 AI 批量处理非结构化用户研究与反馈资产",
            "dependency_skills": [],
            "candidate_destination": "feedback:ai-agent-feedback-synthesis",
            "validation_criteria": "多文档批量扫描，形成语义聚类与结构化笔记本沉淀",
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

    print(f"Building {len(units)} units for analyzing-user-feedback...")
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
