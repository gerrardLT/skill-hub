---
name: pm-operating-system
description: >-
  Run an evidence-driven product-management operating system from intake through discovery, strategy, prioritization, PRD, outcome roadmap, risk validation, measurement and handoff. Use when defining what software to build, deciding whether a product or feature is worth building, validating user problems, synthesizing research, comparing alternatives, setting product strategy, writing or reviewing a PRD, prioritizing opportunities, defining success metrics, or preparing a product package for design. Integrates with the Agentic SDLC shared kernel, Gate system, traceability and learning loop.
---

# PM Operating System

确定为什么做、为谁做、解决什么问题、如何衡量，并把可验证的产品意图交给设计。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `pm-ready` before handoff.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 明确决策、用户、业务目标、边界、项目类型和最大未知量。 | `product-brief` |
| DISCOVERY | 将需求表述改写为问题假设，收集行为与用户证据并寻找反证。 | `discovery-evidence` |
| STRATEGY | 定义 ICP、JTBD、替代方案、定位、战略楔子、差异化和产品论点。 | `product-strategy` |
| PRIORITIZATION | 优先排列问题/机会而非功能；根据场景选择评分框架。 | `prioritized-opportunities` |
| DEFINITION | 把证据、战略、范围、用户旅程、边界和指标固化为 PRD。 | `prd` |
| PLANNING | 把目标分解为 Outcome → Opportunity → Initiative → Experiment/Feature。 | `outcome-roadmap` |
| VALIDATION | 执行 pre-mortem、反方审查和关键假设检查，维护风险登记。 | `risk-register` |
| MEASUREMENT | 建立 North Star、输入指标、护栏指标及 Metric → Hypothesis → Decision。 | `measurement-plan` |
| HANDOFF | 检查全套产品制品、追踪关系和未决问题，通过 pm-ready。 | `pm-ready` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- 没有证据证明问题真实存在时，不把解决方案包装成事实。
- 优先级先排问题/机会，再排方案。
- PRD 必须包含目标、非目标、边界状态、约束、指标、风险和未决问题。
- 所有关键指标必须能触发明确决策。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: 项目上下文、业务目标、已有研究或线上信号.
- Downstream owner: `design-operating-system`.
- Required Gate: `pm-ready`.
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
