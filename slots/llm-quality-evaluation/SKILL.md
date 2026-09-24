# llm-quality-evaluation

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Evaluate language models with automated metrics, factuality checks, judges, human agreement, statistics, and regressions.

## Source Boundaries

- Input: Model outputs, references, criteria, annotations, and trusted historical baselines.
- Output: Repeatable scores, grounded quality judgments, statistical confidence, benchmarks, and regression signals.

## Required Upstream Dependencies

- `cluster:data-analysis-validation`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
