---
name: evolution-operating-system
description: >-
  Run the post-production evolution operating system from telemetry and feedback observation through signal triage, root-cause diagnosis, prioritization, intervention, experiment, verification, learning and evidence-driven re-entry into product, design, engineering, QA or release. Use when production metrics change, users report problems, incidents occur, retention or conversion declines, experiments need analysis, technical health degrades, or a shipped product must continuously improve. Integrates with Agentic SDLC learning-decision gate and prevents reflexive feature accumulation.
---

# Evolution Operating System

用线上真实行为、反馈和运行证据纠正此前判断，并把问题路由回真正拥有根因的 OS。

## Execution protocol

1. Read `.sdlc/state.json`, `.sdlc/context.md`, the current OS note, accepted upstream artifacts, open risks and traceability.
2. Confirm that this OS owns the current decision. If not, route to the owning OS and state why.
3. Determine the earliest stage whose entry evidence is insufficient; do not restart from INTAKE mechanically.
4. Use installed specialist Skills only for the bounded stage they improve. Preserve this Skill’s state, evidence and Gate rules.
5. Produce or update the required artifact, explicitly separating facts, inferences, assumptions and decisions.
6. Register the artifact and supporting evidence in the shared kernel; add traceability to upstream and downstream objects.
7. Run independent review or a bounded subagent when confirmation bias or specialist depth matters.
8. Verify acceptance criteria with fresh evidence. Run `learning-decision` before handoff.

## Generic core + Provider Adapter policy

Keep Evolution vendor-neutral by default. The generic core owns reasoning and learning; observability providers only supply bounded evidence/actions.

- Generic core: `systematic-debugging` + `incident-response` + `metrics-review` + `analyzing-user-feedback` + `validate-data` + `craft-experiment-design`.
- Detect an observability provider from repository configuration, deployed architecture or explicit user evidence. Never infer a provider merely because its Skill is installed.
- Activate only the provider actually used by the project: `sentry`, `datadog`, `posthog`, or none. Multiple providers are allowed only when production evidence shows they are both active.
- Sentry adapter: production issues/traces/logs, alerts and AI monitoring.
- Datadog adapter: logs/APM/monitors; AI Agent projects may add trace-RCA and eval-pipeline Skills.
- PostHog adapter: product analytics/experiments/metric investigation; AI products may add LLM analytics.
- Provider Skills may strengthen OBSERVE, TRIAGE, DIAGNOSE and VERIFY. They **must not** override evidence quality, Gate decisions, human authorization or the final `learning-decision`.
- If provider access is unavailable, record the missing evidence and fall back to generic telemetry analysis; do not fabricate provider results.

## Workflow

| Stage | Objective | Primary output |
| --- | --- | --- |
| INTAKE | 明确观察窗口、版本、用户群、指标定义、事件和已知变更。 | `evolution-intake` |
| OBSERVE | 汇集产品指标、日志、追踪、错误、性能、成本、反馈和支持信号；仅在证据确认后启用对应 Provider Adapter。 | `telemetry-report` |
| TRIAGE | 按影响、紧急性、范围和可逆性区分事故、缺陷、体验或战略问题。 | `signal-triage` |
| DIAGNOSE | 构建时间线和竞争假设，以证据排除并定位根因。 | `diagnosis` |
| PRIORITIZE | 按用户/业务影响、风险、信心和可逆性选择干预。 | `intervention-priority` |
| INTERVENE | 选择修复、配置、回滚、设计改动、产品实验或停止。 | `intervention-plan` |
| EXPERIMENT | 定义假设、样本、指标、护栏、停止规则和分析方法。 | `experiment-plan` |
| VERIFY | 比较 Expected vs Actual，控制混杂，验证副作用与持续性。 | `intervention-result` |
| LEARN | 区分 assumption/evidence/execution/strategy 等 gap，形成决策。 | `learning-decision` |
| REENTRY | 通过 learning-decision Gate 回流对应 OS 和具体阶段。 | `learning-decision` |

Read [workflow.md](references/workflow.md) for entry/exit logic and regression paths.

## Non-negotiable rules

- 相关性不等于因果；诊断必须列出竞争假设和反证。
- Observability Provider 只提供证据和受限操作，不拥有 `learning-decision`，也不得绕过 Release/QA Gate。
- 未检测到真实 Provider 时不得自动启用 Sentry、Datadog 或 PostHog 专用 Skill。
- 事故先止损和恢复，再进行无责根因分析。
- 不要默认增加功能；允许停止、回滚、删除和改变策略。
- 每个学习结论必须包含 Expected、Actual、Gap、Decision 和 Re-entry。

- Never convert an assumption into a fact because a document is polished.
- Never waive a Gate or authorize production-impacting action without explicit human approval.
- When upstream evidence changes, invalidate and re-check affected downstream artifacts.

## Handoff

- Upstream inputs: production-verification、observability-ready、release history、telemetry and feedback.
- Downstream owner: `pm/design/engineering/qa/release 中拥有根因的 OS`.
- Required Gate: `learning-decision`.
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
