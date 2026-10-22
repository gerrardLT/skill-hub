---
name: model-and-workflow-benchmarking
description: Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval. Do not use for run a remote provider experiment to produce missing outputs or perform detailed llm quality scoring with judges and human agreement.
---

# Model And Workflow Benchmarking

## Responsibility

Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.

## Trigger

Use when the requested outcome is: Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.

Do not use when:
- Run a remote provider experiment to produce missing outputs. Route to `llm-experiment-execution`.
- Perform detailed LLM quality scoring with judges and human agreement. Route to `llm-quality-evaluation`.

## Required Inputs

- Frozen cases, candidate variants, metric contract, environment, and budget.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze cases, variants, versions, runner, environment, hardware, seeds, warmup, repeats, timeouts, budget, metrics, thresholds, and exclusions.
2. Verify comparable inputs and execution conditions and preserve failed, timed-out, invalid, and retried cases.
3. Run only approved local or supplied-output comparisons, recording versions, commands, exits, durations, cost assumptions, artifacts, and hashes.
4. Report distributions, variance, regressions, cost-quality-latency tradeoffs, sensitivity, and an evidence-bounded recommendation without choosing product strategy.

## Output Contract

Produce:
- matched benchmark run evidence
- metric distributions and variance
- cost-quality-latency comparison
- regression and recommendation report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `frozen-cases`
- `matched-environment`
- `warmup`
- `repeated-runs`
- `variance`
- `failed-case-retention`
- `cost-quality-latency`

## Hard Gates

- A benchmark requires frozen cases and versions, matched environment and budgets, warmup, repeated runs, variance, failed-case retention, and exact artifacts; leaderboard point estimates alone fail.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `llm-quality-evaluation`
- `llm-experiment-execution`
- `evaluation-results-analysis`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
