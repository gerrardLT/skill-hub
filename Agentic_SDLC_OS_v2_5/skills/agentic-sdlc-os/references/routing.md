# Routing and Re-entry

## Route by ownership of the decision

- PM owns problem, target user, strategic choice, scope, priority and product outcome.
- Design owns task flow, information architecture, interaction, visual language and usability evidence.
- Engineering owns technical design, implementation, code-level quality and engineering self-verification.
- QA owns independent quality evidence and residual-risk recommendation.
- Release owns controlled production change, migration, rollback and rollout verification.
- Evolution owns observation, incident triage, diagnosis, experiments and learning decisions.

## Diagnose before routing symptoms

Examples:

- Low conversion can be a product mismatch, confusing design, defect, performance issue or bad instrumentation.
- A failed deployment can be release configuration, code defect, capacity issue or migration design.
- User complaints can reflect expectation, UX, reliability or segment mismatch.

For ambiguous symptoms, route first to Evolution/DIAGNOSE. Then re-enter the owning OS.

The CLI router is only a deterministic first-pass classifier. It returns `decision`, confidence, ambiguity and alternatives. When `decision=abstain`, `recommended_os` is empty and no state transition is allowed; the Orchestrator must use full semantic context or obtain the missing context. For routed tasks, still combine the result with current state, upstream evidence, project type and the cost of misrouting. Incident projects start in Evolution by default; brownfield and migration projects start in Engineering unless `--start-os` overrides the default.

## Re-entry mapping

| Gap | Default route |
| --- | --- |
| Problem or target-user assumption | PM / DISCOVERY |
| Positioning, priority or business model | PM / STRATEGY or PRIORITIZATION |
| Flow, comprehension or interaction | Design / USER_FLOWS or INTERACTION |
| Visual coherence or accessibility | Design / VISUAL_SYSTEM or VALIDATION |
| Architecture or implementation defect | Engineering / TECHNICAL_DESIGN or BUILD |
| Missing risk coverage | QA / RISK_ANALYSIS or CASE_DESIGN |
| Rollout, migration or environment failure | Release / READINESS, MIGRATION or DEPLOYMENT_PLAN |
| Instrumentation or causal uncertainty | Evolution / OBSERVE, DIAGNOSE or EXPERIMENT |

After a material upstream change, use traceability to identify and invalidate affected downstream artifacts and Gates.

Forward stage movement is adjacent by default. Backward movement is recorded as rework. Skipping stages or jumping forward across OS boundaries requires an approved emergency override.
