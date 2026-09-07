# Engineering Test Plan

## Objective

Prove the transactional and API invariants before independent QA.

## Facts and evidence

Unit tests cover capacity, FIFO promotion, replay, duplicate member, tenant isolation and audit sequence. Integration tests cover HTTP statuses and actionable errors. Concurrency tests submit 100 reservations and parallel cancellations. Coverage is measured with coverage.py.

## Decision and specification

Test data uses isolated temporary SQLite databases. Concurrency uses separate connections through the service and ThreadPoolExecutor. The performance probe records parameters, throughput and latency percentiles.

## Risks and edge cases

Thread scheduling is not deterministic, so tests assert contiguous queue positions and promotion set rather than member arrival order. The local probe is a guardrail, not a capacity forecast.

## Verification and acceptance criteria

Pass: all tests green, zero oversell, exact capacity allocation, unique positions, correct promotion count and coverage above 90 percent.

## Traceability and ownership

Owner: Engineering OS. Inputs: PRD-001 and TD-001. Downstream: UTE-001, IE-001 and TS-001.
