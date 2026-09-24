# document-and-artifact-governance

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Define durable document structure, artifact fields, authorship rules, and output comprehension checks.

## Source Boundaries

- Input: A document or artifact purpose, audience, source evidence, and required fields.
- Output: A governed artifact contract, readable output, and explicit unknowns.

## Required Upstream Dependencies

- `cluster:source-metadata-and-provenance`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
