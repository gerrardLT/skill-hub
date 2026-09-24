Status: blocked

# Acceptance Contract

## Problem Frame

- `CONFLICT-1` (`conflict`): The product brief states, "refunds require a human review." The later comment states, "auto-refund every request." These statements prescribe incompatible handling for the same refund requests.
- Evidence and authority labels are preserved as supplied: `product brief` and `later comment`. No owner resolution or authority ranking was supplied, so neither statement overrides the other.
- The critical premise needed to produce a coherent refund acceptance contract is unresolved.

## Requirements And Rules

- `RULE-1`: Refunds require a human review.
  - Source: product brief.
  - Authority: supplied but not established as controlling relative to `RULE-2`.
  - State: preserved; disputed by `RULE-2`; not approved by this contract.
- `RULE-2`: Auto-refund every request.
  - Source: later comment.
  - Authority: supplied but not established as controlling relative to `RULE-1`.
  - State: preserved; disputed by `RULE-1`; not approved by this contract.
- `OPEN-1`: Decide the authoritative refund policy: human review, automatic refund, or another policy explicitly chosen by an authorized owner.
  - Decision owner: unknown.
  - Effective date: unknown.
  - Hard gate: the decision and its effective date must be recorded by the authorized decision owner before refund behavior is treated as ready for acceptance criteria.

## Acceptance-Criteria Readiness

No executable Given/When/Then acceptance criteria are issued. Any criterion asserting either human review or automatic refund would select an unresolved policy, alter product intent, and create an invalid QA contract.

Unresolved prerequisites:

1. Authoritative refund policy.
2. Decision owner with authority to resolve the conflict.
3. Effective date of the resolved policy.

## Coverage

- Success: blocked; expected refund behavior depends on `OPEN-1`.
- Error: blocked; no authoritative processing policy is available.
- Boundary: blocked; request coverage and exceptions cannot be inferred.
- Permission: blocked; human authority and automation permissions are unresolved.
- Recovery: blocked; no authoritative failure or retry behavior was supplied.
- Non-regression: blocked; there is no resolved baseline policy to preserve.

## Read-Only Quality Gate

- `FINDING-1`
  - Severity: blocking.
  - Violated gate: `scope-and-authority` / `unknown-preservation` prerequisite.
  - Location: `RULE-1`, `RULE-2`, `OPEN-1`.
  - Evidence: the product brief requires human review; the later comment requires automatic refund for every request; no owner resolved the conflict.
  - Consequence: safe and meaningful acceptance criteria cannot be produced without choosing authority or inventing policy.
- Gate result: `blocked`.
- QA action: read-only review only; no requirement, rule, policy, authority, or acceptance criterion was repaired, selected, or rewritten.

## Required Decision

An authorized but currently unknown decision owner must resolve which refund policy is authoritative and specify its effective date. This artifact deliberately preserves both supplied authorities and makes no policy selection.
