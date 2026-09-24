# Acceptance Contract: Refund Policy

## Status

**Blocked** — the supplied authorities conflict, and no owner has resolved which refund policy is authoritative.

## Supplied Statements

1. Product brief: refunds require a human review.
2. Later comment: auto-refund every request.

Both statements are preserved as supplied. Neither is treated as approved or controlling.

## Pre-Mortem Analysis: Refund Handling

### Tigers (Real Risks)

- **Launch-Blocking — unresolved refund authority:** A request cannot simultaneously require human review and be automatically refunded in every case. Proceeding without a decision could produce inconsistent refund outcomes, financial exposure, customer harm, or implementation based on an unauthorized policy.

### Paper Tigers (Overblown Concerns)

- None identified from the supplied facts. There is not enough evidence to classify either policy itself as overblown.

### Elephants (Unspoken Worries)

- **Decision authority is unknown:** No accountable owner is identified for resolving the policy conflict.
- **Effective date is unknown:** Even after a policy is selected, the inputs do not state when it becomes effective.
- **Authoritative refund policy is unknown:** The relative authority of the product brief and later comment is not established.

### Action Plan for the Launch-Blocking Tiger

- **Risk:** Conflicting refund rules could cause the product or operators to apply an unapproved policy.
- **Mitigation:** Obtain an explicit decision that identifies the authoritative refund rule, records whether it supersedes the other statement, and specifies its effective date. Keep implementation and policy-dependent acceptance criteria blocked until that decision is recorded.
- **Owner:** Unknown; an authorized refund-policy decision owner must be identified.
- **Due date:** Before implementation or launch; no calendar date was supplied.

## Decision Required

An authorized owner must decide which rule governs refunds:

- refunds require human review; or
- every request is automatically refunded.

The decision must also state the effective date and the disposition of the non-selected statement. This contract does not select a policy.

## Acceptance Conditions for Unblocking

The requirement may move from **Blocked** only when all of the following are observable:

- A named, authorized decision owner is recorded.
- The owner explicitly identifies the authoritative refund policy.
- The decision explicitly addresses both supplied statements and states which one, if either, supersedes the other.
- An effective date is recorded.
- Policy-dependent acceptance criteria are drafted from the recorded decision without silently changing either original statement.

Until then, no acceptance criterion asserting automatic refund or mandatory human review can be considered approved.
