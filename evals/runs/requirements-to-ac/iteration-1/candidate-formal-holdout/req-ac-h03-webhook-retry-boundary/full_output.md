Status: needs-input

## 1. Problem framing

### Classified items

1. `FACT-1` (`fact`): The requested product behavior concerns batch webhook delivery. Source: supplied product input. Authority: user-supplied product input.
2. `FACT-2` (`fact`): Valid events must retain their supplied event IDs. Source: supplied product input. Authority: user-supplied product input.
3. `FACT-3` (`fact`): Failed destinations may be retried without redelivering successful destinations. Source: supplied product input. Authority: user-supplied product input.
4. `FACT-4` (`fact`): Every delivery attempt must produce an observable result for each destination attempted. Source: supplied product input. Authority: user-supplied product input.
5. `FACT-5` (`fact`): Processing must stop above the documented concurrency cap. Source: supplied product input. Authority: user-supplied product input.
6. `FACT-6` (`fact`): The concurrency-cap value is not supplied. Source: supplied product input. Authority: user-supplied product input.
7. `FACT-7` (`fact`): Queueing technology must not be selected. Source: supplied product input. Authority: user-supplied product input.
8. `OPEN-QUESTION-1` (`open-question`): What is the authoritative documented concurrency-cap value? Evidence: none supplied. Decision authority: the owner of the documented concurrency policy.

### Target user, problem, impact, evidence, and gaps

- Target user: not supplied.
- Problem: batch webhook delivery needs to preserve event identity, isolate retries to failed destinations, expose per-destination attempt results, and enforce a concurrency boundary.
- Impact: not supplied beyond the required behaviors.
- Evidence: only the supplied product input; no external or local product evidence was authorized.
- Conflicts: none supplied.
- Critical gap: the concurrency-cap value is absent. The known behavior can be framed, but the exact concurrency boundary cannot be converted into an executable threshold test without an authoritative value.

## 2. Requirements and rules

### Requirements

- `REQ-1`: For every valid event processed for batch webhook delivery, the system must retain that event's supplied event ID. Source: `FACT-2`. Authority: user-supplied product input. Relationship: covered by `AC-1`.
- `REQ-2`: When retrying failed destinations for a batch, the system must not redeliver that retry to destinations that already succeeded. Source: `FACT-3`. Authority: user-supplied product input. Relationships: covered by `AC-2`; constrained by `RULE-1`.
- `REQ-3`: Every delivery attempt must produce an observable result for each destination included in that attempt. Source: `FACT-4`. Authority: user-supplied product input. Relationships: covered by `AC-3` and `AC-4`.
- `REQ-4`: Processing must stop when proceeding would place concurrency above the documented cap. Source: `FACT-5`. Authority: user-supplied product input. Relationships: depends on `DEP-1`; unresolved by `OPEN-1`.

### Rules

- `RULE-1`: A destination that succeeded in an earlier attempt is excluded from a retry of failed destinations for that batch. Source: `FACT-3`. Authority: user-supplied product input. Relationship: constrains `REQ-2`.
- `RULE-2`: Event IDs are supplied inputs and must not be replaced for valid events. Source: `FACT-2`. Authority: user-supplied product input. Relationship: constrains `REQ-1`.
- `RULE-3`: Queueing technology is outside the authorized decision scope and must not be selected. Source: `FACT-7`. Authority: user-supplied product input.

### Dependencies, scope, and open items

- `DEP-1`: An authoritative documented concurrency-cap value is required to evaluate the boundary in `REQ-4`. Source: `FACT-5`, `FACT-6`, `OPEN-QUESTION-1`.
- `SCOPE-1` (included): Batch webhook event-ID preservation, destination-specific retry behavior, per-destination attempt observability, and concurrency-cap enforcement. Source: `FACT-1` through `FACT-5`.
- `SCOPE-2` (excluded): Selection of queueing technology. Source: `FACT-7`.
- `OPEN-1`: Supply the authoritative documented concurrency-cap value. Source: `FACT-6`, `OPEN-QUESTION-1`. This is unresolved and prevents complete boundary acceptance criteria for `REQ-4`.

## 3. Acceptance criteria

### Numbered criteria

`AC-1` — Preserve supplied event IDs (`REQ-1`, `RULE-2`; success and non-regression)

- Given a valid event with a supplied event ID and one or more batch webhook destinations,
- When the event is processed for delivery,
- Then the event ID observable in the delivery processing outcome for that event equals the supplied event ID.

`AC-2` — Retry only failed destinations (`REQ-2`, `RULE-1`; recovery and non-regression)

- Given a batch delivery attempt has an observable successful result for at least one destination and an observable failed result for at least one other destination,
- When the failed destinations are retried,
- Then a new delivery attempt is observable for each retried failed destination, and no new delivery attempt is observable for any destination that already succeeded.

`AC-3` — Observe successful per-destination attempt results (`REQ-3`; success)

- Given a batch webhook delivery attempt includes one or more destinations,
- When a destination attempt succeeds,
- Then an observable successful result exists for that destination and that attempt.

`AC-4` — Observe failed per-destination attempt results (`REQ-3`; error)

- Given a batch webhook delivery attempt includes one or more destinations,
- When a destination attempt fails,
- Then an observable failed result exists for that destination and that attempt.

### Coverage and unresolved input

- Success: covered by `AC-1` and `AC-3`.
- Error: covered by `AC-4`.
- Recovery: covered by `AC-2`.
- Non-regression: covered by `AC-1` and `AC-2`.
- Boundary: not fully testable. `REQ-4` is uncovered because the documented concurrency-cap value is not supplied; no numeric threshold is invented.
- Permission: no permission behavior was supplied, so no permission criterion is asserted and the class is not marked `not-applicable` without evidence.
- Unresolved input: the authoritative documented concurrency-cap value required for a Given/When/Then boundary criterion for `REQ-4`.

## 4. Requirements quality gate (read-only; no repair)

### Verdict

`needs-input`

### Findings

- `FINDING-1` — Severity: blocking. Violated gate: `unknown-preservation` / `applicable-path-coverage` / `ac-testability`. Artifact location: `REQ-4`, `DEP-1`, `OPEN-1`, acceptance-criteria boundary coverage. Evidence: the product input requires stopping above a documented concurrency cap but explicitly does not supply its value. Consequence: the exact at-cap and above-cap behavior cannot be tested against an authoritative threshold; `REQ-4` has no valid executable AC.

### Gate results

- `artifact-availability`: passed — all four chain sections are present in this output.
- `end-to-end-traceability`: needs-input — `REQ-1` through `REQ-3` trace to criteria, while `REQ-4` is intentionally uncovered pending `OPEN-1`.
- `critical-rule-retention`: passed — event-ID retention, retry isolation, per-destination observability, concurrency stopping, and the prohibition on choosing queueing technology are retained.
- `scope-and-authority`: passed — only supplied product behavior is represented; no queueing technology or unsupported product decision is introduced.
- `unknown-preservation`: passed — the missing cap value remains explicit in `OPEN-QUESTION-1`, `DEP-1`, and `OPEN-1`.
- `ac-testability`: needs-input — `AC-1` through `AC-4` are observable Given/When/Then criteria, but the concurrency boundary cannot be made executable without the cap value.
- `applicable-path-coverage`: needs-input — known success, error, recovery, and non-regression paths are covered; required boundary coverage remains incomplete.
- `evidence-backed-verdict`: passed — the `needs-input` verdict follows directly from the explicitly absent cap value.
- `read-only-review`: passed — QA reports the gap and does not repair requirements, invent a cap, or add an AC using a guessed threshold.

### Required input

Provide the authoritative documented concurrency-cap value. QA makes no repair and selects no queueing technology.
