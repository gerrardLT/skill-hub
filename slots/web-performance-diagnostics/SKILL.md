# web-performance-diagnostics

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Measure web vitals, network behavior, and build output to identify bottlenecks and sustained optimizations.

## Source Boundaries

- Input: A web application, controlled sampling environment, network waterfall, and build information.
- Output: Performance metrics, bottleneck evidence, recommendations, budgets, and an audit report.

## Required Upstream Dependencies

- `cluster:safe-browser-probing`
- `cluster:tool-runtime-readiness`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
