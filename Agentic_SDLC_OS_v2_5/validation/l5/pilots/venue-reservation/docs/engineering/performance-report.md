# Performance Report

## Objective

Measure local serialization cost while verifying capacity integrity under parallel demand.

## Facts and evidence

Method: 200 requests, capacity 20, 32 workers, temporary SQLite WAL database. Result: throughput 1064.434 requests per second, p50 1.857 ms, p95 107.185 ms, p99 133.551 ms, reserved 20, waitlisted 180, oversold=false.

## Decision and specification

Accept the local performance guardrail because p95 is below 500 ms and the correctness invariant held. Performance is secondary to zero oversell.

## Risks and edge cases

The probe shares one host process and warm local storage. It is not a production load test, capacity model or multi-region benchmark. Variance should be sampled over repeated runs before changing thresholds.

## Verification and acceptance criteria

Pass criteria: exact capacity allocation, oversold=false, no exceptions and p95 below 500 ms. Raw result: `reports/performance.json`.

## Traceability and ownership

Owner: Performance reviewer. Inputs: SRC-001 and TP-001. Downstream: NFR-001 and TEL-001.
