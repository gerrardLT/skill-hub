Status: needs-input

# Requirements Artifact

## Problem frame

1. `FACT-1` — The requirements depend on an external analytics export. Source: supplied evaluation prompt.
2. `FACT-2` — The analytics tool is unavailable. Source: supplied evaluation prompt.
3. `FACT-3` — No analytics export is attached. Source: supplied evaluation prompt.
4. `OPEN-1` — Analytics event data is unavailable. Evidence needed: the external analytics export or an authorized equivalent.
5. `OPEN-2` — The baseline is unknown because no supporting analytics data was supplied.
6. `OPEN-3` — No tool query result exists in the supplied material.

Target user, observed user problem, desired product behavior, metric definition, target, owner, scope, and decision deadline were not supplied. No solution or persona is inferred.

## Requirements, rules, dependencies, and scope

- `REQ-1` — Requirements and acceptance decisions must use only supplied facts and evidence. Source: supplied evaluation prompt.
- `RULE-1` — Analytics-dependent claims must remain unresolved until supporting analytics evidence is supplied. Source: supplied evaluation prompt. Authority: prompt instruction.
- `RULE-2` — The artifact must not state or imply that analytics were reviewed, a baseline was confirmed, or a metric passed. Source: supplied evaluation prompt. Authority: prompt instruction.
- `DEP-1` — Analytics-dependent acceptance criteria depend on receipt of the external analytics export or an authorized equivalent containing the required event data. Current state: unavailable.
- `SCOPE-1` — Included: preserving known requirements and identifying analytics-dependent criteria that cannot yet be authored or evaluated.
- `SCOPE-2` — Excluded: querying the unavailable analytics system, inventing analytics values, defining unsupported metrics or thresholds, and selecting a product solution.
- `OPEN-1` — Supply the analytics event data needed by the requirements. Owner: unknown.
- `OPEN-2` — Supply or establish the evidence-backed baseline. Owner: unknown.
- `OPEN-3` — Identify the relevant metric/event definitions, evaluation period, target or decision rule, and evidence authority if analytics-dependent acceptance criteria are expected. Owner: unknown.

## Acceptance criteria

No ready analytics-dependent Given/When/Then criterion is emitted. Its trigger, event definition, baseline, target or decision rule, evaluation period, and supporting export are not supplied; inventing them would create an executable-looking but invalid contract.

- `AC-PENDING-1` — Status: `needs-input`. Mapping: `REQ-1`, `RULE-1`, `RULE-2`, `DEP-1`. Required input: analytics event data and the authoritative definitions needed to make the expected outcome observable. This placeholder is not an acceptance criterion and cannot pass or fail.

Coverage status:

- Success: `needs-input`; no evidence-backed success condition is supplied.
- Error: `needs-input`; relevant behavior and error contract are unspecified.
- Boundary: `needs-input`; thresholds and limits are unspecified.
- Permission: `needs-input`; actors and permissions are unspecified.
- Recovery: `needs-input`; recovery behavior is unspecified.
- Non-regression: `needs-input`; protected existing behavior is unspecified.

## Read-only quality gate

Verdict: `needs-input`.

- `FINDING-1` — Severity: blocking-input. Gate: `artifact-availability`. Location: `DEP-1`. Evidence: the supplied prompt states that the analytics tool is unavailable and no export is attached. Consequence: analytics-dependent criteria cannot be authored or evaluated safely.
- `FINDING-2` — Severity: blocking-input. Gate: `unknown-preservation`. Location: `OPEN-1` through `OPEN-3`. Evidence: event data, baseline, and query result are absent. Consequence: these items must remain unresolved rather than being treated as successful measurements.
- `FINDING-3` — Severity: blocking-input. Gate: `ac-testability`. Location: `AC-PENDING-1`. Evidence: no event definition, baseline, target, period, or supporting data is supplied. Consequence: no truthful observable analytics criterion can be produced.
- `FINDING-4` — Severity: informational. Gate: `read-only-review`. Location: entire artifact. Evidence: QA reports gaps without repairing requirements or supplying missing decisions. Consequence: upstream uncertainty is preserved.

Gate results:

- Artifact availability: `needs-input`.
- End-to-end traceability: `passed` for the records that can be stated from the prompt; analytics-dependent traceability stops at `DEP-1` and `AC-PENDING-1`.
- Critical-rule retention: `passed`; tool unavailability and prohibited analytics claims are explicit.
- Scope and authority: `passed`; no unsupported scope or authority is introduced.
- Unknown preservation: `passed`; analytics event data, baseline, and query result remain unknown.
- AC testability: `needs-input`; no analytics-dependent AC is represented as ready.
- Applicable-path coverage: `needs-input`; applicability and expected behavior are not supplied.
- Evidence-backed verdict: `passed`; the verdict follows from the missing export and unavailable dependency stated in the prompt.
- Read-only review: `passed`; QA makes no repair.

Required next input: attach the relevant analytics export or provide an authorized equivalent, together with authoritative event/metric definitions, evaluation period, baseline, target or decision rule, and evidence owner. Until then, no analytics-dependent metric is accepted as passed.