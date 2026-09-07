---
name: design-operating-system
description: >-
  Run a complete product-design operating system from product-intent intake through research, information architecture, user flows, interaction states, visual system, prototype, usability and accessibility validation, development handoff and implementation acceptance. Use when creating or redesigning websites, apps, mini-programs, dashboards or software interfaces; when converting PRDs into user experiences; when defining design systems, states, motion and responsive behavior; or when auditing whether a design is usable, accessible, coherent and implementation-ready. Integrates with Agentic SDLC evidence, gates and traceability.
---

# Design Operating System

把已验证的产品意图转化为可理解、可操作、可访问、可实现并可验证的体验规格。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `design-ready` before handoff.

## Specialist composition policy

- Use **one primary visual director** per work item. Default to `impeccable`; do not let `frontend-design` or `design-taste-frontend` co-lead the same visual decision.
- Use `ui-ux-pro-max` as the cross-platform UI/UX knowledge layer, not as a competing art director.
- Use `web-design-guidelines` as an objective Web usability/accessibility constraint layer.
- Use `review-animations` when motion, transition, gesture or micro-interaction quality materially matters.
- Activate `redesign-existing-projects` only for brownfield redesign, `web-accessibility` for explicit accessibility depth, `prototype` when alternatives need comparison, and `extract-design-system` only for lawful design-system research.
- Treat `frontend-design` as a Greenfield/fallback generator and `design-taste-frontend` as a marketing/brand-surface specialist, not default product-UI cores.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 继承 PM 目标、范围、用户、约束、指标和风险；形成设计问题。 | `design-brief` |
| RESEARCH | 补充任务研究、行为路径、认知负荷、环境和可访问性需求。 | `design-research` |
| INFORMATION_ARCHITECTURE | 定义对象、内容模型、导航、层级和查找路径。 | `information-architecture` |
| USER_FLOWS | 覆盖主流程、替代流程、异常、权限、中断与恢复。 | `user-flows` |
| INTERACTION | 定义组件行为、输入反馈、状态机、错误恢复和微交互。 | `interaction-spec` |
| VISUAL_SYSTEM | 建立设计令牌、排版、空间、色彩、层级、组件和动效语言。 | `design-system` |
| PROTOTYPE | 制作覆盖关键任务和关键状态的可测试原型。 | `prototype` |
| VALIDATION | 执行可用性、启发式、无障碍、响应式和内容验证。 | `usability-report / accessibility-report` |
| HANDOFF | 交付标注、状态、资源、验收条件和实现风险。 | `design-handoff` |
| ACCEPTANCE | 对实现进行设计验收并通过 design-ready 或发起返工。 | `design-ready` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- 设计必须覆盖 loading、empty、error、success、permission、offline 等真实状态。
- 审美不能牺牲可用性、无障碍、性能和平台一致性。
- 原型必须可验证关键任务，不以静态首页代替完整流程。
- 设计交付必须包含可实现规格，而不是只提供截图。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: product-brief、prd、outcome-roadmap、measurement-plan、risk-register.
- Downstream owner: `engineering-operating-system`.
- Required Gate: `design-ready`.
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
