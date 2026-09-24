# independent-blackbox-qa

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Run diff-aware, quick, or regression black-box QA without modifying product source.

## Source Boundaries

- Input: An accessible application, change scope, QA mode, and authorized interaction boundary.
- Output: Report-only defects, screenshots, console evidence, and a health score; never a product-code repair.

## Required Upstream Dependencies

- `cluster:safe-browser-probing`
- `cluster:testing-portfolio-strategy`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
