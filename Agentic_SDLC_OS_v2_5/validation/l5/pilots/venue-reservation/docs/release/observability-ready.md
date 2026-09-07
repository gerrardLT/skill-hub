# Observability Readiness

## Objective

Define the minimum signals needed to detect invariant failure and explain reservation state.

## Facts and evidence

Signals include capacity, reserved, available, active waitlist, joined total, promotion total, conversion rate, cancellations, oversold boolean and audit event count. Audit event types identify session open, reservation, waitlist join, promotion and cancellation.

## Decision and specification

Alert immediately on oversold=true, active reservations above capacity, failed tenant isolation test or missing audit event for a material transition. Performance p95 above 500 ms is a warning, not a correctness override.

## Risks and edge cases

Metrics are per session and local. There is no centralized log store, durable alerting or long-term retention. These are required before external release.

## Verification and acceptance criteria

Ready means metrics endpoint is available, audit events are queryable and the probe report records parameters and version.

## Traceability and ownership

Owner: Release and Evolution OS. Inputs: DEP-001 and MP-001. Downstream: TEL-001 and DIA-001.
