# external-design-token-extraction-and-normalization

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Extract and normalize design primitives from an authorized external surface without treating them as project authority or writing project tokens.

## Source Boundaries

- Input: An authorized public reference, extraction runtime, and requested analysis mode.
- Output: Reviewed normalized primitives, raw/normalized evidence, provenance, and explicit write-approval state.

## Required Upstream Dependencies

- `cluster:source-metadata-and-provenance`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
