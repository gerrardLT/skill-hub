---
name: release-operating-system
description: >-
  Run a safe software-release operating system from readiness review through immutable build, environment and configuration validation, migration planning, deployment plan, progressive rollout, production verification, stabilization, rollback and release review. Use when preparing or executing deployments, CI/CD, canary or gray releases, database migrations, feature flags, production verification, rollback plans, incident-safe launches or cloud-platform releases. Integrates with Agentic SDLC release-ready and production-ready gates and never deploys without explicit authorization.
---

# Release Operating System

把已验证的版本以渐进、可观测、可回滚且有明确授权的方式送入生产。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `production-ready` before handoff.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 继承 QA 建议、版本范围、残余风险、依赖、负责人和发布窗口。 | `release-intake` |
| READINESS | 核验审批、变更冻结、运行手册、值守、状态页和外部依赖。 | `release-readiness` |
| BUILD_ARTIFACT | 生成可追踪、不可变、已签名或可校验的构建制品。 | `build-artifact` |
| ENVIRONMENT | 验证生产配置、密钥、权限、容量、网络和可观测性。 | `environment-verification` |
| MIGRATION | 定义前向/回滚迁移、兼容窗口、备份和数据验证。 | `migration-plan` |
| DEPLOYMENT_PLAN | 定义步骤、批次、审批、指标、停止和回滚条件。 | `release-plan / rollback-plan` |
| ROLLOUT | 按 canary/灰度/分批方式执行；每步验证后才扩大。 | `deployment-evidence` |
| PRODUCTION_VERIFICATION | 验证合成旅程、核心指标、日志、错误率和数据正确性。 | `production-verification` |
| STABILIZATION | 观察完整风险窗口，处理告警、回滚或补救。 | `observability-ready` |
| REVIEW | 记录结果、偏差、事故和改进，通过 production-ready。 | `production-ready` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- 任何生产写操作、部署或回滚都需要明确授权。
- 必须先定义停止条件和回滚路径，再开始 rollout。
- 数据库迁移必须考虑向前/向后兼容和不可逆步骤。
- 部署成功不等于发布成功；必须验证用户旅程和业务/技术指标。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: release-recommendation、regression-report、nonfunctional-report、defect-disposition.
- Downstream owner: `evolution-operating-system`.
- Required Gate: `production-ready`.
- Use the standard output envelope and completion status from the global OS.

## Subagents

Use the bounded roles in [subagents.md](references/subagents.md) only for independent research, parallelizable work, red-team review or permission isolation. The main agent owns synthesis.

## References

- Stage details and routing: [workflow.md](references/workflow.md)
- Outputs and acceptance: [outputs.md](references/outputs.md)
- Gate checklist: [gates.md](references/gates.md)
- External Skill candidates: [external-skills.md](references/external-skills.md)
- Subagent roles: [subagents.md](references/subagents.md)
- Scenarios: [examples.md](references/examples.md)
- Shared-kernel commands: [kernel-commands.md](references/kernel-commands.md)
