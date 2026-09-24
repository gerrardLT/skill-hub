# -*- coding: utf-8 -*-
"""
Generator for ship semantic units.
Extracts verbatim excerpts from skills/ship/SKILL.md and sections/
and validates each unit according to Phase 3 schema (12-key format).
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
        # 1. ship:unit-001 (gate: branch pre-flight gate)
        {
            "id": "ship:unit-001",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 570,
            "origin_line_end": 577,
            "type": "gate",
            "meaning": "发布流程预检分支门禁：检查当前分支，如果在基线分支或默认分支则直接中止发布，要求必须从特性分支发起交付",
            "boundary_condition": "执行任何代码合并、测试或推送动作前的绝对入口门禁",
            "dependency_skills": [],
            "candidate_destination": "preflight:branch-gate",
            "validation_criteria": "在 main 或 master 分支上调用 ship 时立即报错并中止流程",
            "status": "retain"
        },
        # 2. ship:unit-002 (rule: automated ship stopping and non-stopping conditions)
        {
            "id": "ship:unit-002",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 502,
            "origin_line_end": 526,
            "type": "rule",
            "meaning": "全自动发布执行与停止规程：定义何时必须停机询问（基线分支、复杂冲突、测试失败、高风险门禁）与何时必须静默自动推进",
            "boundary_condition": "整个自动化交付流水线的中断与交互判定规则",
            "dependency_skills": [],
            "candidate_destination": "workflow:automation-stop-rules",
            "validation_criteria": "常规操作无需人工交互确认，遇到既定硬阻断时安全挂起",
            "status": "retain"
        },
        # 3. ship:unit-003 (method: merge base branch before running tests)
        {
            "id": "ship:unit-003",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 674,
            "origin_line_end": 685,
            "type": "method",
            "meaning": "测前合并基线分支操作：从远端拉取最新基线分支并静默合并至特性分支，确保测试在最新合并态执行",
            "boundary_condition": "运行测试套件之前的代码同步步骤",
            "dependency_skills": [],
            "candidate_destination": "git:merge-base-before-tests",
            "validation_criteria": "特性分支包含远端基线最新提交，无未决冲突时平滑进入跑测阶段",
            "status": "retain"
        },
        # 4. ship:unit-004 (rule: version bump classification and decision rules)
        {
            "id": "ship:unit-004",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 706,
            "origin_line_end": 726,
            "type": "rule",
            "meaning": "语义版本判定与自动自增规则：基于差异规模与特征信号分类版本级别（MICRO/PATCH/MINOR/MAJOR），结合状态机驱动写入",
            "boundary_condition": "测试与审查通过后的版本递增步骤",
            "dependency_skills": [],
            "candidate_destination": "versioning:bump-classification-rules",
            "validation_criteria": "按代码差异特征准确推导版本递增层级，大版本变动主动请求确认",
            "status": "retain"
        },
        # 5. ship:unit-005 (rule: bisectable commits splitting and ordering rules)
        {
            "id": "ship:unit-005",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 871,
            "origin_line_end": 905,
            "type": "rule",
            "meaning": "可二分原子提交拆分规程：将差异按基础设施、模型与服务、控制器与视图、版本元数据的顺序分层拆解为独立可编译验证的原子提交",
            "boundary_condition": "多文件综合性功能发布时的代码提交组织",
            "dependency_skills": [],
            "candidate_destination": "git:bisectable-commits-splitting",
            "validation_criteria": "生成的提交历史支持线性追溯与 git bisect 排障，无坏死中间态提交",
            "status": "retain"
        },
        # 6. ship:unit-006 (gate: fresh verification evidence gate)
        {
            "id": "ship:unit-006",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 909,
            "origin_line_end": 936,
            "type": "gate",
            "meaning": "新鲜验证凭据铁律门禁：严禁在缺乏新鲜验证凭证的情况下声称完成；任何非放行代码修改后必须全量重新跑测记录证据",
            "boundary_condition": "分支推送及创建 PR 之前的终极验收门禁",
            "dependency_skills": [],
            "candidate_destination": "verification:fresh-evidence-gate",
            "validation_criteria": "代码与测试执行时间戳严格匹配，杜绝凭空推断与过期缓存",
            "status": "retain"
        },
        # 7. ship:unit-007 (gate: credential pre-push guard)
        {
            "id": "ship:unit-007",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 955,
            "origin_line_end": 985,
            "type": "gate",
            "meaning": "推送前敏感信息脱敏防护门禁：在执行 git push 前检查是否挂载预推送钩子，拦截 API 密钥、私钥与敏感 Token",
            "boundary_condition": "执行远程仓库推送操作之前的安全屏障",
            "dependency_skills": [],
            "candidate_destination": "security:pre-push-credential-guard",
            "validation_criteria": "若存在敏感凭证泄漏风险则立即阻断推送并提醒开发者清除",
            "status": "retain"
        },
        # 8. ship:unit-008 (rule: PR/MR title invariant and doc-sync rule)
        {
            "id": "ship:unit-008",
            "source_path": "ship/SKILL.md",
            "origin_line_start": 1040,
            "origin_line_end": 1046,
            "type": "rule",
            "meaning": "PR 标题版本前缀与文档同步强制不变式：PR/MR 标题强制遵循 v<NEW_VERSION> 前缀规范，且必须先派发文档同步子代理",
            "boundary_condition": "创建或更新 PR/MR 的最终收尾阶段",
            "dependency_skills": [],
            "candidate_destination": "delivery:pr-title-and-docsync-invariant",
            "validation_criteria": "创建的 PR 标题带有规范版本前缀，且包含与变更同步的文档更新",
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
    units = build_units()
    skills_root = pathlib.Path("skills")
    errors = []

    for unit in units:
        errs, matches = verify_unit(unit, skills_root)
        if errs or not matches:
            errors.extend([f"[{unit['id']}] {e}" for e in errs])
            if not matches and not errs:
                errors.append(f"[{unit['id']}] excerpt does not match source")

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(" ", err)
        sys.exit(1)

    output_path = pathlib.Path("curation/units/ship.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for unit in units:
            f.write(json.dumps(unit, ensure_ascii=False) + "\n")

    print(f"SUCCESS: Generated {len(units)} validated units in {output_path}")

if __name__ == "__main__":
    main()
