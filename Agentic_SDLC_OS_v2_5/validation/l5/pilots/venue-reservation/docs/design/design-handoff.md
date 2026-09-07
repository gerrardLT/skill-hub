# Design Handoff

## Objective

Translate member states and error recovery into implementable API and frontend contracts.

## Facts and evidence

RESERVED maps to HTTP 201, WAITLISTED to 202, cancellation to 200, business conflicts to 409, missing tenant resource to 404 and validation failures to 422. Each business error returns code, message and next_action.

## Decision and specification

Engineering must preserve the session identifier, member identifier and idempotency key through retries. Frontend must render authoritative response state and never infer capacity from stale availability. Queue position is integer text with an explanation, not a countdown.

## Risks and edge cases

The pilot does not implement the full visual application. Integration consumers must not assume payment state, hold TTL or table map availability. Those require new requirements and state contracts.

## Verification and acceptance criteria

Handoff accepted when API tests verify status mapping and the prototype covers RESERVED, WAITLISTED and error states. Changes to PRD state names invalidate this handoff until re-reviewed.

## Traceability and ownership

Owner: Design OS. Inputs: IA-001, UF-001, IS-001, DS-001, PROTO-001, UR-001 and AR-001. Downstream: TD-001 and TP-001.
