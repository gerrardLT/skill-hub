# SaaS MVP Product Brief

## Problem

Three pilot table-tennis venue operators reported double bookings and missed payment follow-up in interviews dated 2026-08-30. Source EV-PILOT-01 records 11 incidents across 30 booking attempts.

## Users

The initial user is a single-location venue administrator responsible for booking, payment confirmation, and daily reconciliation. Owner: product lead.

## Outcome

The MVP must reduce double-booking incidents to zero during a four-week pilot and raise completed booking confirmation to at least 95% within 10 minutes.

## Scope and Non-goals

Scope includes one venue type, one administrator role, booking creation, payment status, and conflict detection. Marketplace discovery, multi-country tax, and multi-venue franchises are excluded.

## Evidence and Facts

Evidence ID EV-PILOT-01 comes from three semi-structured operator interviews and reviewed booking logs. The sample is small, so the decision remains reversible until pilot telemetry is available.

## Risks and Assumptions

Risk R-PAY-01 is payment reconciliation mismatch. The system must use idempotent payment events and daily reconciliation. Assumption A-SETUP-01 states that setup under 60 minutes is acceptable.

## Success Metrics and Acceptance Criteria

Pass when 20 pilot bookings complete with zero double booking, at least 95% confirmation within 10 minutes, and no critical privacy or payment incident. Fail and return to Discovery if any critical condition is breached.

## Traceability

Requirement PRD-BOOK-01 derives from EV-PILOT-01 and links to goal:validated-booking-flow, implementation ticket ENG-BOOK-01, test TEST-BOOK-01, and release REL-PILOT-01.
