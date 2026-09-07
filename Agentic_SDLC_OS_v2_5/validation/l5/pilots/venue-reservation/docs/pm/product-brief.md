# Product Brief - Atomic Venue Reservation

## Problem and context

Peak booking demand can create duplicate requests, unfair ordering and oversold capacity. Requirement D26 demands atomic table holds and D33 requires a fair queue with zero oversell. The current pilot isolates this risk-heavy core before payment, check-in or pricing complexity is added.

## Users and audience

Primary users are venue members booking a session and operators responsible for capacity integrity. Secondary users are support staff investigating failed retries, cancellations and promotion order through an immutable audit trail.

## Outcome and objective

A member receives one actionable state: RESERVED or WAITLISTED. A cancellation immediately promotes the earliest eligible waitlist entry. The system must never report more active reservations than configured capacity.

## Scope and non-goals

Scope includes session creation, reservation, FIFO waitlist, cancellation, automatic promotion, tenant isolation, idempotency, audit and metrics. Non-goals are payments, membership entitlement, table maps, physical access, notifications and multi-region scaling.

## Evidence and facts

Source: `source/requirements-selection.md`. D26 explicitly requires 100 concurrent requests without oversell. D33 requires server-side ordering, one active token per member and a direct waitlist path. The design source requires errors to state the reason, current state and next action.

## Risks and assumptions

SQLite serialization is acceptable for a local pilot but not assumed sufficient for multi-node production. FIFO is based on transaction admission order. A future eligibility service may reject a promoted member and therefore needs a skip-and-reason compensation path.

## Success metrics and acceptance criteria

Oversell count must equal 0. Exactly capacity requests must become RESERVED. Remaining requests must receive unique FIFO positions. Retry replay must return the original result. Coverage must exceed 90 percent and p95 for 200 local requests must stay under 500 ms.
