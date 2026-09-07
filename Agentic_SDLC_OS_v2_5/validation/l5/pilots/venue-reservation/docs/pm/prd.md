# PRD - Reservation and Waitlist Vertical Slice

## Problem

Members competing for scarce venue capacity can submit retries at the same time. A naive implementation may oversell, duplicate a member, lose fairness or provide a dead-end error. The product must expose a single authoritative state and a recovery path.

## Users and jobs to be done

Member JTBD: reserve a valid session with confidence, or know the exact waitlist position and what happens next. Operator JTBD: prove that capacity, promotion order and retries are correct, then diagnose every material state change from audit data.

## Goals and non-goals

Goals: atomic allocation, one active reservation or waitlist entry per member and session, FIFO promotion, idempotent retries, tenant isolation, actionable errors, immutable audit events and session metrics. Non-goals: payment, entitlement, notifications, check-in, table selection UI and distributed deployment.

## Functional requirements

REQ-001 create an OPEN session with capacity 1-500. REQ-002 reserve within one immediate transaction. REQ-003 return WAITLISTED with a unique position when full. REQ-004 reuse of an idempotency key with identical payload returns the original response; different payload returns 409. REQ-005 cancellation promotes the earliest WAITLISTED entry. REQ-006 all reads and writes are tenant scoped. REQ-007 emit audit events for session open, reservation, waitlist join, promotion and cancellation. REQ-008 expose capacity, reserved, waitlisted, conversion and oversell metrics.

## User journey

Create session -> member submits reserve -> server validates tenant and uniqueness -> atomic capacity decision -> RESERVED or WAITLISTED -> member retries safely -> a reserved member cancels -> earliest waitlist member becomes RESERVED -> operator inspects metrics and audit evidence.

## Edge cases, constraints and risks

Handle concurrent requests, duplicate members, stale retries, invalid identifiers, closed or missing sessions, tenant mismatch and concurrent cancellations. FIFO is transaction order, not network arrival time. SQLite is accepted only for this local pilot and requires a different lock design for multi-node production.

## Metrics and success criteria

Oversell equals 0. Under 100 concurrent attempts and capacity 10, exactly 10 become RESERVED and 90 receive positions 1-90. All cancellation promotions must select the lowest active queue sequence. Test pass rate must be 100 percent, code coverage above 90 percent, and local p95 under 500 ms.

## Acceptance criteria

AC-001 through AC-008 are verified by `tests/test_service.py`, `tests/test_concurrency.py`, `tests/test_api.py`, `tests/test_audit.py`, coverage evidence and the performance probe. Any capacity breach, duplicate active state or tenant data exposure is a release blocker.

## Traceability and evidence

Source requirements: D26, D33, Reservation, WaitlistEntry, SeatHold, R02 and R08 in `source/requirements-selection.md`. Owner: PM OS. Version: PRD-001. Downstream: design flow, technical design, tests, release plan and telemetry.
