# safe-browser-probing

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Use constrained browser sessions for navigation, snapshots, interaction, tracing, and extraction with safe references.

## Source Boundaries

- Input: A target page, authorized interactions, and a ready browser runtime.
- Output: Browser observations, screenshots, snapshots, traces, and interaction evidence, not an independent QA verdict.

## Required Upstream Dependencies

- `cluster:tool-runtime-readiness`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
