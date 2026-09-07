# Measurement Plan

## Objective

Define decision-linked metrics before implementation and prevent vanity measurements from replacing invariant checks.

## Facts and evidence

Primary metrics are oversold boolean, active reservations versus capacity, FIFO position continuity, waitlist promotion count, idempotent replay equality, test pass rate and coverage. Secondary metrics are throughput and p50/p95/p99 latency from a local controlled probe.

## Decision and specification

Release blocker thresholds: oversold must be false, capacity equality exact, FIFO positions contiguous, tenant leakage zero and tests 100 percent pass. Performance guardrail: p95 below 500 ms for 200 requests with 32 workers on the current container.

## Risks and edge cases

Local latency does not represent cloud production. Coverage does not prove requirement correctness. Waitlist conversion in the pilot is mechanically induced by cancellations and is not a business conversion metric.

## Verification and acceptance criteria

Data sources are SQLite state, audit events, pytest, coverage JSON and `reports/performance.json`. Each result must include timestamp, parameters and version identity.

## Traceability and ownership

Owner: PM OS with Evolution verification. Input: PRD-001. Downstream: TEL-001 and LD-001.
