# Interaction Specification

## Objective

Define state language and response behavior for fast, high-confidence booking decisions.

## Facts and evidence

The source design requires booking order of time, duration, table, participants, price and confirm. This backend pilot starts at the confirm decision. Server results are RESERVED, WAITLISTED or CANCELED; errors include a stable code and next action.

## Decision and specification

RESERVED shows a confirmation title and the reservation identifier. WAITLISTED shows position as the primary number and explains FIFO promotion. SESSION_NOT_FOUND offers return to availability. ALREADY_RESERVED opens the existing reservation. IDEMPOTENCY_CONFLICT instructs use of the original payload or a new key.

## Risks and edge cases

Never use color alone. Never display a fake countdown. Never discard the selected session after a race. Avoid generic 'operation failed' language. A network retry must reuse the same idempotency key.

## Verification and acceptance criteria

Prototype review must verify keyboard access, visible focus, status text, preserved context and distinct outcomes. API integration tests verify error content and stable retry behavior.

## Traceability and ownership

Owner: Design OS. Inputs: UF-001 and PRD-001. Downstream: PROTO-001, AR-001 and DH-001.
