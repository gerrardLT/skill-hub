# QA Test Strategy

## Objective

Independently verify product risks rather than repeat the engineering happy path.

## Facts and evidence

Risk priorities are oversell, duplicate state, queue disorder, tenant leakage, mismatched idempotency replay and incomplete audit. Test levels are API, transaction, concurrency, security boundary and nonfunctional probe.

## Decision and specification

Use risk-based execution: critical invariants on every change; API and audit regression on every release; performance probe before release; distributed database tests only after the architecture changes.

## Risks and edge cases

The pilot does not cover payment, time-based expiry, authentication or device UX. These are explicit exclusions rather than assumed passes.

## Verification and acceptance criteria

Release requires all critical tests pass, no open critical defect, coverage above 90 percent and a reproducible performance result with zero oversell.

## Traceability and ownership

Owner: QA OS. Inputs: PRD-001, TP-001 and RR-001. Downstream: RGR-001, NFR-001 and RELREC-001.
