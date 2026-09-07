# Prioritized Opportunities

## Objective

Rank problem opportunities rather than feature requests using value, risk reduction, evidence strength and implementation cost.

## Facts and evidence

Opportunity O1 atomic capacity allocation scores 10/10 risk reduction and has direct acceptance evidence. O2 idempotent retry scores 9/10 because duplicate requests are explicitly named. O3 FIFO promotion scores 9/10 because it closes released capacity. O4 visual table map scores 5/10 for this pilot because it does not prove backend integrity.

## Decision and specification

Priority order is O1 atomic allocation, O2 idempotency, O3 waitlist promotion, O4 actionable error contract, O5 metrics and audit, then visual map integration. The first five are committed for pilot-0.1.0.

## Risks and edge cases

A pure value score could over-prioritize visible UI and miss catastrophic oversell. The ranking therefore treats correctness and recoverability as non-compensable gates.

## Verification and acceptance criteria

Each committed opportunity must map to at least one PRD requirement and one automated test. O1 must pass a 100-request concurrency test with zero oversell.

## Traceability and ownership

Owner: PM OS. Inputs: PS-001 and DE-001. Downstream: PRD-001 and OR-001.
