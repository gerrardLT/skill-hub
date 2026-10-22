---
name: model-and-workflow-benchmarking
description: "Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval. Use when Two or more model, prompt or workflow variants must be compared on frozen cases for quality, latency and cost; Someone asks which variant to pick once run-to-run variance and failed cases are counted. Do not use for: Run a remote provider experiment to produce missing outputs (-> llm-experiment-execution); Perform detailed LLM quality scoring with judges and human agreement (-> llm-quality-evaluation); Compare an application's performance before and after a code change (-> baseline-regression-control); Measure web page load and Core Web Vitals (-> web-performance-diagnostics)."
---

# Model And Workflow Benchmarking

## Responsibility

Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.

## Trigger

Use when the request matches any of:
- Two or more model, prompt or workflow variants must be compared on frozen cases for quality, latency and cost
- Someone asks which variant to pick once run-to-run variance and failed cases are counted

Do not use when:
- Run a remote provider experiment to produce missing outputs. Route to `llm-experiment-execution`.
- Perform detailed LLM quality scoring with judges and human agreement. Route to `llm-quality-evaluation`.
- Compare an application's performance before and after a code change. Route to `baseline-regression-control`.
- Measure web page load and Core Web Vitals. Route to `web-performance-diagnostics`.

## Required Inputs

- Frozen cases, candidate variants, metric contract, environment, and budget.

## Procedure

1. Freeze cases, variants, versions, runner, environment, hardware, seeds, warmup, repeats, timeouts, budget, metrics, thresholds, and exclusions.
2. Verify comparable inputs and execution conditions and preserve failed, timed-out, invalid, and retried cases.
3. Run only approved local or supplied-output comparisons, recording versions, commands, exits, durations, cost assumptions, artifacts, and hashes.
4. Report distributions, variance, regressions, cost-quality-latency tradeoffs, sensitivity, and an evidence-bounded recommendation without choosing product strategy.

## Domain Guidance

- Scope is model and workflow variants on frozen cases. Preview which providers and credentials a multi-provider benchmark would use before running anything, and never submit remotely.

## Output Contract

Produce:
- matched benchmark run evidence
- metric distributions and variance
- cost-quality-latency comparison
- regression and recommendation report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `llm-quality-evaluation`
- `llm-experiment-execution`
- `evaluation-results-analysis`
- `baseline-regression-control`
- `web-performance-diagnostics`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
