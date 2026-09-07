# Venue Reservation Dogfood Pilot

## Objective

Run the Agentic SDLC OS against a real user-owned product requirement set and produce an executable vertical slice rather than a document-only demonstration.

## Facts and evidence

Source anchors are `source/requirements.xlsx`, its selected extract, and two design specifications. The selected capabilities are D26 dynamic table locking and D33 fair queueing. The implementation test suite currently has 11 passing tests.

## Decision and specification

Build a FastAPI and SQLite service for atomic capacity allocation, FIFO waitlist promotion, idempotent retries, tenant isolation, audit events and measurable runtime behavior. Keep payment and physical check-in outside this pilot.

## Risks and edge cases

This is a controlled local pilot, not an external production rollout. It cannot prove business conversion, long-term reliability or causal improvement over a baseline Agent without matched iterations.

## Verification and acceptance criteria

Pass requires zero oversell under 100 concurrent requests, FIFO promotion, 100 percent test pass, code coverage above 90 percent, and a local performance probe with p95 below 500 ms. Observed p95 is 107.185 ms and coverage is 96 percent.

## Traceability and ownership

Owner: Agentic SDLC OS dogfood team. Version: pilot-0.1.0. The full evidence chain is recorded in `.sdlc`, `reports`, and the six OS artifact folders.
