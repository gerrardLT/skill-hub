---
name: engineering-operating-system
description: >-
  Run a disciplined software-engineering operating system from requirements review through technical design, architecture decisions, implementation planning, test-driven development, code review, integration, security and performance hardening, and evidence-backed handoff to QA. Use when designing system architecture, implementing features, refactoring codebases, debugging defects, reviewing pull requests, planning migrations, defining APIs or data models, or proving that implementation is complete. Integrates with Agentic SDLC build-ready and verification-ready gates, shared memory and end-to-end traceability.
---

# Engineering Operating System

把产品与设计规格转化为可维护、可测试、安全、可靠、可观测的实现，并提供新鲜验证证据。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `verification-ready` before handoff.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 继承 PRD、设计规格、验收标准、约束、风险和追踪关系。 | `engineering-intake` |
| REQUIREMENTS_REVIEW | 识别歧义、不可实现项、边界条件、数据与非功能需求。 | `requirements-review` |
| TECHNICAL_DESIGN | 定义组件、接口、数据流、失败模式、依赖和运维边界。 | `technical-design` |
| ARCHITECTURE | 记录关键 ADR、质量属性、威胁、容量、迁移和回滚设计。 | `architecture-decisions` |
| PLAN | 拆成可独立验证的小步，明确测试、文件、依赖和检查点。 | `implementation-plan / test-plan / security-plan` |
| BUILD | 按 TDD 或等价验证循环实现，保持小批次和可回退提交。 | `source-change / unit-test-evidence` |
| CODE_REVIEW | 用独立上下文审查正确性、安全、复杂度、兼容和维护性。 | `code-review` |
| INTEGRATION | 验证模块、接口、数据、配置和外部依赖的真实集成。 | `integration-evidence` |
| HARDENING | 执行安全、性能、可靠性、依赖、可观测性和迁移检查。 | `security-review / performance-report` |
| HANDOFF | 重新运行验证命令，注册证据并通过 verification-ready。 | `verification-ready` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- 进入 BUILD 前通过 build-ready；禁止边写边补核心架构。
- 修复缺陷先定位根因，避免只压制症状。
- 声称完成前必须运行新鲜验证，而不是引用旧输出。
- 代码审查应由独立上下文执行，并区分必须修复与可选建议。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: prd、design-handoff、acceptance criteria、risk-register.
- Downstream owner: `qa-operating-system`.
- Required Gate: `verification-ready`.
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
