---
name: qa-operating-system
description: >-
  Run an independent, risk-based quality-assurance operating system from test intake and risk analysis through strategy, test design, environment and data readiness, exploratory and automated execution, defect triage, regression, non-functional testing and release recommendation. Use when designing test systems, auditing software quality, building automated tests, validating a feature or release, reproducing defects, testing APIs or web applications, or deciding whether residual risk is acceptable for release. Integrates with Agentic SDLC traceability and the release-ready gate.
---

# QA Operating System

独立证明软件在目标环境和真实风险下达到可接受质量，并明确剩余风险。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `release-ready` before handoff.

## Specialist composition policy

- Use `testing-strategy` to define the risk model and test architecture before expanding test volume.
- Use `verification-before-completion` as the claim gate: no fresh evidence, no PASS/DONE claim.
- Prefer `qa-only` for independent browser QA because QA must report defects rather than silently repair the product it is judging.
- Use `code-review` as an independent change review; findings route to Engineering for product-source remediation.
- Use OpenAI `playwright` as the browser execution/evidence layer. Add `playwright-best-practices` only after installation-integrity verification and when the project actually has a Playwright suite.
- Keep TDD and root-cause implementation debugging in Engineering by default. QA may reproduce and isolate failures, but must not become the author and approver of the same production fix.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 继承需求、设计、实现、变更范围、风险、验收标准和工程自证。 | `qa-intake` |
| RISK_ANALYSIS | 按影响×可能性识别业务、数据、安全、兼容、性能和恢复风险。 | `quality-risk-model` |
| STRATEGY | 决定测试层级、范围、自动化边界、环境、数据和退出标准。 | `test-strategy` |
| CASE_DESIGN | 从风险和追踪关系生成正向、负向、边界、状态和滥用用例。 | `test-cases` |
| ENVIRONMENT | 验证构建、配置、数据、依赖、账号、可观测性和可重复性。 | `environment-readiness` |
| EXECUTION | 执行自动化、探索式、API、端到端和设备/浏览器验证。 | `test-execution-evidence` |
| DEFECT_LOOP | 复现、分级、定位并把产品源码修复路由给 Engineering；QA 独立验证修复并保护回归覆盖。 | `defect-disposition` |
| REGRESSION | 根据变更影响运行最小充分回归和关键业务旅程。 | `regression-report` |
| NON_FUNCTIONAL | 验证性能、安全、可靠性、可访问性、兼容和恢复。 | `nonfunctional-report` |
| RECOMMENDATION | 汇总证据、覆盖、缺陷和残余风险，通过 release-ready。 | `release-recommendation` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- QA 不以“用例全部通过”代替风险判断。
- QA 不得修改产品源码来让自己的验收通过；QA 可以维护测试、fixture、测试工具和报告。产品源码修复必须路由到 Engineering，再由独立 QA 复验。
- 同一 Agent/执行上下文不得既完成生产修复又作为最终独立 QA 批准者。
- 生产级关键路径至少有一条可重复的端到端证据。
- 缺陷关闭必须包含复现前失败和修复后通过的证据。
- 发布建议必须明确已测、未测、残余风险和回滚触发条件。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: source-change、code-review、integration-evidence、security-review、acceptance criteria.
- Downstream owner: `release-operating-system`.
- Required Gate: `release-ready`.
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
