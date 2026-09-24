# Acceptance Contract: Refund Handling

Status: blocked

## Source Requirements

- Product brief: Refunds require a human review.
- Later comment: Auto-refund every request.

## Conflict

The two authoritative inputs prescribe incompatible refund behavior. The later comment does not resolve or explicitly supersede the product brief, and no owner has resolved which instruction governs. This contract therefore preserves both statements and selects neither policy.

## Decision Needed

An authorized product owner must decide which refund policy governs:

- require human review before issuing a refund; or
- automatically refund every request.

The decision must also state whether it supersedes the conflicting source and identify its effective scope.

## Acceptance Conditions

- Both conflicting statements remain documented without reinterpretation.
- No implementation policy is selected or inferred while the conflict is unresolved.
- Refund behavior dependent on this requirement is blocked from acceptance.
- Acceptance can resume only after an authorized owner records the governing policy and resolves the conflict.
