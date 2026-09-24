# evidence-based-ui-review-and-release-gates

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Review real renders against explicit criteria and issue evidence-bounded findings and release dispositions.

## Source Boundaries

- Input: An implementation, desktop and mobile captures, a brief, direction contract, target files, and findings.
- Output: Prioritized findings, fix or rebuild dispositions, recapture evidence, a verdict, and residual risk.

## Required Upstream Dependencies

- `cluster:accessibility-contracts-and-assistive-validation`
- `cluster:frontend-rendering-and-interaction-performance`
- `cluster:purposeful-motion-and-animation-engineering`
- `cluster:responsive-layout-and-spatial-composition`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
