# User Flows

## Objective

Specify normal, full-capacity, retry, cancel, promotion and recovery paths.

## Facts and evidence

Normal: choose session -> submit -> RESERVED -> show time, venue and management actions. Full: submit -> WAITLISTED -> show current position and promotion rule. Retry: same key -> identical result. Cancel: confirm consequence -> CANCELED -> earliest waitlist entry promoted.

## Decision and specification

Flow F1 reserves capacity. F2 joins FIFO waitlist. F3 safely replays a request. F4 rejects reused keys with different payload. F5 cancels and promotes. F6 resolves missing session, duplicate member, invalid input and tenant mismatch with reason plus next action.

## Risks and edge cases

A race can change availability between page view and submit. The client must trust the server result and retain the selected session. A cancellation may have no waitlist and must still return a stable CANCELED state.

## Verification and acceptance criteria

Each flow maps to a test. F1-F5 must be deterministic. F6 must expose error code, message and next_action. No flow may show a success animation before the authoritative response.

## Traceability and ownership

Owner: Design OS. Inputs: IA-001 and PRD-001. Downstream: IS-001, PROTO-001 and INT-001.
