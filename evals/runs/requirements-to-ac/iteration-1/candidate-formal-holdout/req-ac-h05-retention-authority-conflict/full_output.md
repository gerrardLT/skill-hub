Status: blocked

# Acceptance Contract

## Problem Frame

1. `FACT-1` — The supplied product brief requires audit exports to remain available for 30 days. Source: product input, clause 1. Supplied authority: product brief; no relative authority ranking supplied.
2. `FACT-2` — The supplied later security standard requires deletion after 7 days. Source: product input, clause 2. Supplied authority: later security standard; no relative authority ranking supplied.
3. `CONFLICT-1` — `FACT-1` and `FACT-2` impose incompatible retention outcomes for audit exports from day 7 through day 30. Both rules are preserved; neither overrides the other.
4. `OPEN-1` — The governing authority or authorized decision owner for resolving `CONFLICT-1` is not supplied.
5. `OPEN-2` — No exception or reconciliation rule is supplied that permits both 30-day availability and deletion after 7 days.

Target-user framing: no target user was supplied.

Problem framing: an acceptance contract cannot establish one executable audit-export retention behavior while the two supplied rules conflict and their authority relationship is unknown.

Impact framing: acceptance criteria for retention, availability, deletion, boundaries, and non-regression would encode an unsupported retention decision.

## Requirements And Rules

- `SCOPE-1` — Audit-export retention and availability are in scope. Source: `FACT-1`, `FACT-2`.
- `RULE-1` — Audit exports must remain available for 30 days. Source: product brief / `FACT-1`. Authority: product brief; ranking unknown.
- `RULE-2` — Audit exports must be deleted after 7 days. Source: later security standard / `FACT-2`. Authority: security standard; ranking unknown.
- `OPEN-1` — An authorized decision is required to determine which rule governs, or to supply an approved exception or reconciliation rule. Required decision authority: the owner empowered to rank or reconcile the product brief and security standard; that owner is not identified in the input.
- Relationship: `RULE-1` conflicts with `RULE-2`; both are critical and retained without modification.
- Hard gate: requirements readiness is blocked until `OPEN-1` is resolved by an identified authorized decision owner.

## Acceptance Criteria

No Given/When/Then acceptance criteria are issued. The governing retention period is a required precondition, and producing criteria would necessarily choose, weaken, or reinterpret one of the conflicting rules.

Uncovered due to the block:

- `RULE-1` — no valid observable criterion can be asserted without resolving the authority conflict.
- `RULE-2` — no valid observable criterion can be asserted without resolving the authority conflict.
- Success, error, boundary, permission, recovery, and non-regression coverage remain unassessed; none is marked not applicable.

## Decision Needed

Identify the authorized decision owner and obtain an authoritative ruling that ranks `RULE-1` and `RULE-2`, or supplies an approved exception or reconciliation rule. This contract does not choose a retention period.

## QA Quality Gate — Report Only

- `FINDING-1` — Severity: blocking. Gate: `scope-and-authority`. Location: `RULE-1`, `RULE-2`, `OPEN-1`. Evidence: conflicting 30-day availability and 7-day deletion rules are supplied without authority ranking, exception, or decision owner. Consequence: no authoritative retention behavior can be contracted.
- `FINDING-2` — Severity: blocking. Gate: `ac-testability`. Location: Acceptance Criteria. Evidence: the retention threshold required for observable Given/When/Then outcomes is unresolved. Consequence: any executable-looking criterion would invent or select a policy.
- `FINDING-3` — Severity: blocking. Gate: `applicable-path-coverage`. Location: Acceptance Criteria. Evidence: no authoritative baseline exists for boundary or non-regression behavior. Consequence: coverage cannot be completed or validly classified as not applicable.

Gate results:

- `artifact-availability`: passed — the supplied product input and frozen candidate contracts were available.
- `end-to-end-traceability`: blocked — both rules trace to the input, but neither can trace to valid AC before an authority decision.
- `critical-rule-retention`: passed — both conflicting rules are retained verbatim in substance.
- `scope-and-authority`: blocked — authority ranking and decision owner are absent.
- `unknown-preservation`: passed — missing authority, owner, and exception/reconciliation rule remain explicit.
- `ac-testability`: blocked — meaningful criteria cannot be produced safely.
- `applicable-path-coverage`: blocked — coverage depends on the unresolved governing rule.
- `evidence-backed-verdict`: passed — the blocked verdict follows from the supplied conflict and missing authority.
- `read-only-review`: passed — QA reports findings and performs no repair.

Unresolved input: an authoritative conflict-resolution decision from an identified owner empowered to rank or reconcile the two supplied rules.