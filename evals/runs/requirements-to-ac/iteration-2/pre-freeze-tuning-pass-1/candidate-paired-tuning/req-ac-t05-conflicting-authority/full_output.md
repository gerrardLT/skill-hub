Status: blocked

# Acceptance Contract

## 1. Problem Framing

1. `CONFLICT-1` (`conflict`)
   - Statement A: "Refunds require a human review."
   - Source: product brief.
   - Authority: the product brief is identified as a source, but no decision-owning authority is supplied.
   - Statement B: "Auto-refund every request."
   - Source: later comment.
   - Authority: the comment is later, but no evidence establishes that recency grants it authority to override the product brief.
   - Conflict: requiring human review is incompatible with automatically refunding every request.
2. `OPEN-1` (`open-question`)
   - Which refund policy is authoritative: mandatory human review or automatic refund of every request?
   - Required decision-maker: an authorized owner for refund policy. No such owner or resolution was supplied.

Target-user framing: No target user was supplied.

Problem framing: Refund behavior cannot be specified safely because the supplied sources prescribe mutually exclusive handling and no authorized resolution exists.

Impact framing: An acceptance contract that selected either statement would invent policy and could authorize behavior contrary to the unresolved source.

Critical gap: An authorized refund-policy decision is unavailable.

## 2. Requirements And Rules

- `REQ-1`: Refunds require a human review.
  - Source: product brief.
  - Authority: unresolved.
  - Relationship: conflicts with `REQ-2`; blocked by `OPEN-1`.
- `REQ-2`: Every refund request is automatically refunded.
  - Source: later comment.
  - Authority: unresolved; later timing alone does not establish override authority.
  - Relationship: conflicts with `REQ-1`; blocked by `OPEN-1`.
- `RULE-1`: Neither `REQ-1` nor `REQ-2` may be selected, subordinated, or treated as effective until an authorized refund-policy owner resolves the conflict.
  - Source: derived process constraint required to preserve the supplied conflict and authority boundary; it does not choose product policy.
- `DEP-1`: A documented decision from an authorized refund-policy owner identifying the governing requirement and the disposition of the conflicting statement.
- `SCOPE-1`: Included: policy governing the handling of refund requests.
- `OPEN-1`: Obtain an authoritative decision choosing between mandatory human review and automatic refund of every request, including confirmation of which source controls.

Readiness result: The requirement set is not ready for acceptance-criteria generation because its governing policy and authority are unresolved.

## 3. Acceptance Criteria

No Given/When/Then criteria are produced. Either policy would require materially different observable outcomes, so producing criteria now would select or blend a policy without authority.

Traceability:

- `REQ-1` -> uncovered because of `CONFLICT-1` and `OPEN-1`.
- `REQ-2` -> uncovered because of `CONFLICT-1` and `OPEN-1`.
- `RULE-1` -> enforced by stopping criteria generation.

Coverage: Success, error, boundary, permission, recovery, and non-regression paths remain unevaluated because the authoritative base behavior is not established. No class is marked not applicable.

Unresolved input: A documented decision from an authorized refund-policy owner selecting the governing policy and resolving the competing source.

## 4. Requirements Quality Gate

### Findings

- `FINDING-1`
  - Severity: blocking.
  - Violated gate: `scope-and-authority`.
  - Artifact location: `CONFLICT-1`, `REQ-1`, `REQ-2`, `OPEN-1`.
  - Evidence: The product brief requires human review; the later comment requires auto-refunding every request; no authorized owner or resolution is supplied.
  - Consequence: The governing refund behavior cannot be determined without authority overreach.
- `FINDING-2`
  - Severity: blocking.
  - Violated gate: `ac-testability` and `applicable-path-coverage`.
  - Artifact location: Acceptance Criteria.
  - Evidence: No criteria can be generated without choosing between incompatible expected outcomes.
  - Consequence: There is no valid executable acceptance contract for refund behavior.

### Gate Results

- Artifact availability: affirmative; the supplied statements and generated intermediate records are present.
- End-to-end traceability: affirmative through the conflict, requirements, dependency, and unresolved decision.
- Critical-rule retention: affirmative; both policy statements are retained verbatim in substance.
- Scope and authority: blocked by unresolved authority conflict.
- Unknown preservation: affirmative; the missing owner decision remains explicit.
- Acceptance-criteria testability: blocked because authoritative expected behavior is unknown.
- Applicable-path coverage: blocked; no unsupported scenarios or not-applicable claims were invented.
- Evidence-backed verdict: affirmative; the verdict follows directly from the preserved conflict and absent authority resolution.
- Read-only review: affirmative; the quality gate did not repair or select product policy.

Decision required: An authorized refund-policy owner must decide whether refunds require human review or every request is auto-refunded, identify which source governs, and record the disposition of the other statement. This output does not select a policy.
