# -*- coding: utf-8 -*-
"""
Generator for land-and-deploy semantic units.
Extracts verbatim excerpts from skills/land-and-deploy/SKILL.md
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
        # 1. land-and-deploy:unit-001 (gate: platform & base branch detection)
        {
            "id": "land-and-deploy:unit-001",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 535,
            "origin_line_end": 560,
            "type": "gate",
            "meaning": "代码托管平台与基线目标分支探测门禁：依据远端 URL 与 CLI 状态检测 GitHub 或 GitLab 宿主平台并解析目标基线分支",
            "boundary_condition": "执行 PR 合并与部署前的信息收集与上下文初始化阶段",
            "dependency_skills": [],
            "candidate_destination": "platform:hosting-and-base-branch-detector",
            "validation_criteria": "准确识别 GitHub/GitLab 平台及关联 PR 的目标合流分支",
            "status": "retain"
        },
        # 2. land-and-deploy:unit-002 (gate: pre-flight CLI authentication and PR state validation)
        {
            "id": "land-and-deploy:unit-002",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 638,
            "origin_line_end": 662,
            "type": "gate",
            "meaning": "发布预检 CLI 鉴权与 PR 状态校验门禁：验证 GitHub CLI 登录态并核查 PR 状态（拒绝已合并、已关闭或无 PR 场景）",
            "boundary_condition": "进入部署合并流水线前必须满足的入口门禁",
            "dependency_skills": [],
            "candidate_destination": "preflight:auth-and-pr-state-gate",
            "validation_criteria": "未鉴权或 PR 状态异常时立即挂起并给出明确指引",
            "status": "retain"
        },
        # 3. land-and-deploy:unit-003 (gate: first-run dry-run validation and configuration fingerprinting)
        {
            "id": "land-and-deploy:unit-003",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 665,
            "origin_line_end": 694,
            "type": "gate",
            "meaning": "首运行试运行校验与部署配置指纹门禁：基于 land-deploy-confirmed 校验配置变更与首次运行，必要时强制激活试运行导师模式",
            "boundary_condition": "初次执行或部署配置文件/工作流发生变动时的审定机制",
            "dependency_skills": [],
            "candidate_destination": "deploy:first-run-dry-run-validation",
            "validation_criteria": "首次部署或配置哈希漂移时阻断静默操作，引导用户完成审定",
            "status": "retain"
        },
        # 4. land-and-deploy:unit-004 (gate: pre-merge CI checks and conflict gate)
        {
            "id": "land-and-deploy:unit-004",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 700,
            "origin_line_end": 720,
            "type": "gate",
            "meaning": "合流前 CI 状态与代码冲突审查门禁：解析必要 CI 检查结果与冲突状态，失败或冲突时坚决阻断合流",
            "boundary_condition": "合并 PR 前的代码健康与合流可行性检查",
            "dependency_skills": [],
            "candidate_destination": "gate:pre-merge-ci-and-conflict",
            "validation_criteria": "CI 失败或存在代码冲突时绝对阻断合并操作",
            "status": "retain"
        },
        # 5. land-and-deploy:unit-005 (rule: CI waiting loop and timeout governance)
        {
            "id": "land-and-deploy:unit-005",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 723,
            "origin_line_end": 736,
            "type": "rule",
            "meaning": "CI 轮询等待与 15 分钟超时治理规则：针对处于 PENDING 的检查采用 gh pr checks --watch 监听，超时或挂起时安全中断",
            "boundary_condition": "必要 CI 检查尚在运行中的阻塞等待机制",
            "dependency_skills": [],
            "candidate_destination": "ci:watch-and-timeout-governance",
            "validation_criteria": "在 15 分钟内持续追踪 CI 状态，超时或失败时安全报错并给出排查建议",
            "status": "retain"
        },
        # 6. land-and-deploy:unit-006 (gate: VERSION drift detection across sibling workspaces)
        {
            "id": "land-and-deploy:unit-006",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 739,
            "origin_line_end": 758,
            "type": "gate",
            "meaning": "版本号跨工作区并发漂移拦截门禁：核验当前 PR 所声明的 VERSION 是否依然为下一个空闲槽位，拦截兄弟工作区抢占导致的冲突",
            "boundary_condition": "合流前检查版本号与基线分支版本演进一致性",
            "dependency_skills": [],
            "candidate_destination": "versioning:drift-detection-gate",
            "validation_criteria": "检测到基线版本抢占时中止合并并提示重跑 ship 更新元数据",
            "status": "retain"
        },
        # 7. land-and-deploy:unit-007 (method: multi-platform deploy observer and polling strategy)
        {
            "id": "land-and-deploy:unit-007",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 792,
            "origin_line_end": 825,
            "type": "method",
            "meaning": "多平台部署态势监听与指数轮询方法：支持 GitHub Actions 工作流 SHA 匹配监听及 Fly.io/Render 等平台 CLI/HTTP 探针轮询",
            "boundary_condition": "PR 合并后至生产服务就绪之间的发布管线追踪阶段",
            "dependency_skills": [],
            "candidate_destination": "deploy:multi-platform-observer",
            "validation_criteria": "准确捕捉合并提交触发的远端部署任务状态并完成健康确认",
            "status": "retain"
        },
        # 8. land-and-deploy:unit-008 (gate: post-deploy canary verification and error budget gate)
        {
            "id": "land-and-deploy:unit-008",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 857,
            "origin_line_end": 890,
            "type": "gate",
            "meaning": "部署后生产金丝雀探针与错误预算门禁：按变动范围实施分级金丝雀探针，注入 JS 错误捕获、性能指标提取与带标注视觉截图",
            "boundary_condition": "生产发布完成后的即时生产就绪健康验收",
            "dependency_skills": [],
            "candidate_destination": "canary:post-deploy-verification-gate",
            "validation_criteria": "页面加载返回 200，无严重 Uncaught 错误，且耗时在 10 秒以内",
            "status": "retain"
        },
        # 9. land-and-deploy:unit-009 (rule: health assessment criteria and rollback recommendation)
        {
            "id": "land-and-deploy:unit-009",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 906,
            "origin_line_end": 920,
            "type": "rule",
            "meaning": "生产金丝雀健康判定规则与回滚建议协商：基于状态码、控制台异常与性能分级判定 PASS/FAIL，异常时给出回滚推荐选项",
            "boundary_condition": "金丝雀探针数据采集完成后的质量裁决步骤",
            "dependency_skills": [],
            "candidate_destination": "health:assessment-and-rollback-decision",
            "validation_criteria": "任何严重错误发生时立即引导用户审查证据并提供一键回滚",
            "status": "retain"
        },
        # 10. land-and-deploy:unit-010 (method: non-destructive git revert and rollback PR creation)
        {
            "id": "land-and-deploy:unit-0010",
            "source_path": "land-and-deploy/SKILL.md",
            "origin_line_start": 923,
            "origin_line_end": 942,
            "type": "method",
            "meaning": "非破坏性代码回滚与回滚 PR 自动构建方法：在生产故障时执行 git revert 恢复基线，遇分支保护时自动降级生成回滚 PR",
            "boundary_condition": "发布失败或金丝雀检验劣化时执行的紧急恢复动作",
            "dependency_skills": [],
            "candidate_destination": "recovery:automated-git-revert-and-rollback-pr",
            "validation_criteria": "安全生成反向还原提交或回滚 PR，不污染历史基线",
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
    print(f"Building {len(units)} units for land-and-deploy...")

    output_path = pathlib.Path("curation/units/land-and-deploy.jsonl")
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
