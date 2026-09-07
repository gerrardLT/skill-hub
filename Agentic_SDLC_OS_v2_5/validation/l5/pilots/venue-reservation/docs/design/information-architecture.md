# Information Architecture

## Objective

Define the smallest member and operator information structure for a reservation decision without exposing database concepts.

## Facts and evidence

The design source specifies a time-first model, a single highlighted decision, an actionable table-taken state and a waitlist position that reduces uncertainty. API resources are session, reservation, waitlist outcome and metrics.

## Decision and specification

Member flow uses Session Availability -> Reservation Decision -> Confirmation or Waitlist Status -> Cancellation Result. Operator flow uses Session Metrics -> Audit Events -> Issue diagnosis. Private booking and social matchmaking remain separate information spaces.

## Risks and edge cases

Do not show raw queue sequence as a guarantee of time. Do not collapse RESERVED and WAITLISTED into a generic success state. Do not expose tenant identifiers in member content.

## Verification and acceptance criteria

Acceptance requires every PRD state to have one clear surface, one primary action and an explicit next step. Errors must preserve session context instead of resetting the task.

## Traceability and ownership

Owner: Design OS. Inputs: PRD-001 and source UI/UX specification. Downstream: UF-001, IS-001 and DH-001.
