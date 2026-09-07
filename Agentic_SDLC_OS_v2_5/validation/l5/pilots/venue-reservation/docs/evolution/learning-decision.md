# Learning Decision

## Expected hypothesis

Agentic SDLC OS should convert a dense real requirement set into a traceable, executable and safely releasable vertical slice with zero critical invariant failures.

## Actual observed result

The pilot produced 11 passing tests, 96 percent coverage, zero oversell across 200 parallel reservation attempts, exact capacity allocation, FIFO promotion and a complete local release evidence chain.

## Gap and diagnosis

Control-plane and engineering correctness met expectations. The unclosed gap is causal effectiveness: there is no matched baseline, no repeated iteration sample, no human-hour measurement and no real customer telemetry.

## Evidence and data

Evidence is `reports/performance.json`, `reports/coverage.json`, pytest output, accepted `.sdlc` artifacts, audit events and gate results. Synthetic or local evidence is explicitly labeled and not promoted to production-effect claims.

## Decision and action

Decision: KEEP the v2.0 dogfood and experiment tooling; do not declare Agentic SDLC OS production-effective. Next action: run a preregistered paired comparison with at least two baseline and two SDLC iterations, then target five per arm.

## Route, re-entry and owner

Re-enter Evolution EXPERIMENT for L5 comparison design. Owner: experiment-reviewer. Engineering re-entry is conditional only if a distributed-storage pilot is selected. No PM scope expansion is approved yet.
