# cross-domain-ui-preflight-checklists

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Run cross-cutting UI preflight checks for accessibility, content, interaction states, responsive behavior, and release readiness.

## Source Boundaries

- Input: A rendered UI, acceptance criteria, content, supported devices, and release boundary.
- Output: A checklist result, blocking findings, evidence requirements, and residual risk.

## Required Upstream Dependencies

- `cluster:interaction-states-forms-and-navigation`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
