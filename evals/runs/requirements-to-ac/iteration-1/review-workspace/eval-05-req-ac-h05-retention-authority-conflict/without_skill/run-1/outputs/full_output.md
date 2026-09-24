Status: blocked

# Acceptance Contract: Audit Export Retention

## Scope

This contract covers the availability and deletion timing of audit exports.

## Preserved Requirements

- R1 — Product brief: Audit exports must remain available for 30 days.
- R2 — Later security standard: Audit exports must be deleted after 7 days.

## Conflict

R1 requires availability through day 30, while R2 requires deletion after day 7. Both cannot be satisfied for the same audit export under a single retention policy. The inputs provide no authority ranking, exception, or decision owner, so neither rule may override the other.

## Acceptance Criteria

- AC1: The implementation preserves R1 as a binding, unresolved requirement; it does not shorten the stated 30-day availability period.
- AC2: The implementation preserves R2 as a binding, unresolved requirement; it does not extend the stated 7-day deletion deadline.
- AC3: The contract and any dependent implementation remain blocked while R1 and R2 apply to the same audit exports without an approved reconciliation.
- AC4: No retention period is selected, inferred, averaged, or treated as controlling before the required authority decision is recorded.
- AC5: Resolution evidence identifies the authorized decision owner, the authority or precedence basis, the chosen treatment of both rules, and any approved exception or scope distinction.
- AC6: Acceptance testing for a concrete retention duration must not proceed until the resolution evidence in AC5 exists.

## Decision Needed

An authorized governance decision is required to determine which rule has precedence or whether an approved exception or scope distinction reconciles them. The decision must also name the accountable owner and document the authority supporting the resolution.

## Blocking Condition

Blocked pending the documented authority decision. This contract intentionally does not choose a retention period.
