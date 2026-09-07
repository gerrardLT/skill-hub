# Integration Evidence Report

## Objective

Verify the HTTP boundary, state transitions and database behavior as one executable system.

## Facts and evidence

FastAPI TestClient creates a session, confirms one reservation, places the next member on the waitlist, cancels the reservation, promotes the waitlisted member and verifies metrics. Error tests verify 404 and 422 contracts.

## Decision and specification

Accept integration behavior for the pilot. HTTP status mapping is 201 RESERVED, 202 WAITLISTED, 200 CANCELED, 409 business conflict, 404 missing tenant resource and 422 invalid input.

## Risks and edge cases

No external reverse proxy, network fault injection, TLS or live browser is included. Local integration success does not prove cloud deployment compatibility.

## Verification and acceptance criteria

Pass requires the end-to-end API test and all state assertions. Evidence is `tests/test_api.py` and the full pytest run.

## Traceability and ownership

Owner: Integration reviewer. Inputs: SRC-001 and DH-001. Downstream: CR-001 and RGR-001.
