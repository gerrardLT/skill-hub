# Discovery Evidence

## Objective

Determine whether reservation integrity and waitlist certainty are sufficiently evidenced to justify an executable pilot.

## Facts and evidence

Evidence source 1 is the user-owned feature workbook, narrowed to D26, D33 and the Reservation, WaitlistEntry and SeatHold state invariants. Evidence source 2 is the UI/UX specification that defines time-first booking, actionable taken-state recovery and calm waitlist status. Evidence source 3 is the executable concurrency test.

## Decision and specification

Proceed with a vertical slice centered on correctness, certainty and traceability. Do not broaden into full Venue OS scope during the pilot.

## Risks and edge cases

The workbook is a product specification, not observed production telemetry. The expert design document is not a usability study. These limitations block claims about market demand or user conversion.

## Verification and acceptance criteria

The pilot is justified when the selected requirements can be translated into falsifiable invariants and verified by deterministic tests. The evidence is sufficient for engineering validation, not business validation.

## Traceability and ownership

Requirement source hash is recorded in `source/requirements-selection.md`. Owner: PM OS. Downstream: PS-001, PRD-001 and RR-001.
