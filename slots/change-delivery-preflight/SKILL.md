# change-delivery-preflight

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Prepare a verified change for delivery by checking branch state, merge base, credentials, automation stops, and documentation invariants.

## Source Boundaries

- Input: A reviewed change, repository state, delivery policy, and intended publication boundary.
- Output: A delivery-ready package or explicit preflight blockers; no merge or deployment action.

## Required Upstream Dependencies

- `cluster:completion-evidence-gate`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
