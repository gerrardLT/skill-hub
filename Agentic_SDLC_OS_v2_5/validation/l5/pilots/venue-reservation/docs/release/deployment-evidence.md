# Deployment Evidence Report

## Objective

Record a reproducible local deployment and smoke sequence for pilot-0.1.0.

## Facts and evidence

Environment: current container, Python 3, FastAPI, SQLite WAL, localhost only. Procedure: run tests, start Uvicorn, call /health, create capacity-1 session, reserve member A, waitlist member B, cancel A, verify B promotion, stop process.

## Decision and specification

Deployment evidence is accepted for the controlled environment. It does not represent external production deployment.

## Risks and edge cases

Network, TLS, authentication, process supervision and persistence were not exercised. Changing any of these invalidates the evidence boundary.

## Verification and acceptance criteria

Pass requires all smoke calls return expected states, metrics show oversold=false and rollback terminates the process.

## Traceability and ownership

Owner: Release operator. Inputs: RLP-001, RBP-001 and MIG-001. Downstream: PV-001 and OBS-001.
