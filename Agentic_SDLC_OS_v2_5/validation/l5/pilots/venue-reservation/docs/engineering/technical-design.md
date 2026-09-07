# Technical Design

## Objective

Implement capacity allocation and waitlist promotion with explicit transaction boundaries and verifiable invariants.

## Facts and evidence

FastAPI provides the HTTP boundary. Pydantic validates identifiers and capacity. SQLite uses WAL, busy_timeout and BEGIN IMMEDIATE. Partial unique indexes prevent duplicate active reservation and waitlist states. Audit events are append-only rows.

## Decision and specification

Reserve transaction: validate idempotency -> load tenant session -> reject duplicate active state -> count active reservations -> insert reservation or next queue sequence -> append event -> persist replay response -> commit. Cancel transaction marks CANCELED and promotes the lowest active queue_seq.

## Risks and edge cases

SQLite serializes writes and is a pilot constraint. A distributed implementation needs a database atomic update, lock or single-writer queue. JSON audit payloads must not contain secrets. Queue order reflects transaction admission rather than client timestamp.

## Verification and acceptance criteria

Verification requires concurrency tests, unique-index checks, replay tests, tenant isolation tests, coverage above 90 percent and local probe p95 below 500 ms with zero oversell.

## Traceability and ownership

Owner: Engineering OS. Inputs: PRD-001 and DH-001. Downstream: ADR-001, IP-001, TP-001 and SRC-001.
