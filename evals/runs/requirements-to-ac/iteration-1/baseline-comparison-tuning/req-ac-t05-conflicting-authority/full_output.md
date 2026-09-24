Status: blocked

# Refund Policy Acceptance Contract

## Supplied Statements

- Product brief: "refunds require a human review."
- Later comment: "auto-refund every request."

## Authority Conflict

The two supplied rules prescribe mutually exclusive handling for the same refund requests: one requires human review, while the other requires every request to be refunded automatically. No owner has resolved which statement is authoritative. Neither rule is selected or treated as approved in this contract.

## Requirement State

- **Requirement:** The refund flow must follow the authoritative refund policy once it is resolved.
- **State:** Blocked by unresolved policy authority.
- **Launch risk:** Launching before resolution could either bypass a required human control or fail to provide an intended automatic refund. This is a launch-blocking Tiger.

## Decision Required

An authorized decision owner must choose and document one authoritative policy, reconcile or supersede the conflicting statement, and provide its effective date.

- Authoritative refund policy: Unknown
- Decision owner: Unknown
- Effective date: Unknown
- Due date: Must be set by the decision owner before implementation approval or launch

## Acceptance Criteria

1. **Conflict remains visible:** Given the policy is unresolved, when the acceptance contract is reviewed, then both original statements are shown and neither is represented as approved.
2. **Blocked behavior:** Given no authoritative policy has been designated, when implementation or launch approval is requested, then the refund-policy requirement is reported as blocked and no automatic-refund or mandatory-human-review behavior is accepted as the governing rule.
3. **Authority resolution:** Given an authorized decision owner resolves the conflict, when the decision is recorded, then the record identifies the selected authoritative policy, the decision owner, the effective date, and which prior statement is superseded or reconciled.
4. **Contract update:** Given the resolution record is complete, when this contract is updated, then testable criteria for the selected policy may replace this blocked placeholder without implying that the unselected rule remains authoritative.
5. **Incomplete resolution:** Given any of the authoritative policy, decision owner, or effective date remains unknown, when readiness is assessed, then status remains blocked.

## Launch-Blocking Action Plan

- **Risk:** Conflicting refund instructions could produce unauthorized or inconsistent customer outcomes.
- **Mitigation:** Obtain and record an explicit authority decision; do not infer policy from document recency.
- **Owner:** Unknown; an accountable policy owner must be named.
- **Completion date:** Unknown; must precede implementation approval or launch.
