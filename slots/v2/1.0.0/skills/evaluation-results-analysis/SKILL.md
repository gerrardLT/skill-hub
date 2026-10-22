---
name: evaluation-results-analysis
description: Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes. Do not use for execute the reviewed experiment against the provider or evaluate raw model outputs with metrics, judges, and human agreement first.
---

# Evaluation Results Analysis

## Responsibility

Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.

## Trigger

Use when the requested outcome is: Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.

Do not use when:
- Execute the reviewed experiment against the provider. Route to `llm-experiment-execution`.
- Evaluate raw model outputs with metrics, judges, and human agreement first. Route to `llm-quality-evaluation`.

## Required Inputs

- Experiment results, metric contract, baseline, statistical assumptions, and known data limits.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze run identities, dataset and evaluator versions, metric contract, thresholds, exclusions, statistical assumptions, baseline, costs, and known data limits.
2. Verify result completeness, pairing, missingness, duplicates, contamination, retries, failed runs, and comparable versions before analysis.
3. Compute declared aggregates, distributions, uncertainty, effect sizes or intervals, failure slices, cost and latency, and sensitivity without metric shopping.
4. Return supported and unsupported claims, regressions, tradeoffs, and a recommendation to the named human owner; do not rerun, approve, or deploy.

## Output Contract

Produce:
- experiment comparison
- variance and uncertainty report
- failure-slice and regression analysis
- evidence-bounded human decision readout

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `frozen-metrics`
- `variance`
- `uncertainty`
- `failure-slices`
- `cost-latency`
- `no-metric-shopping`
- `human-decision`

## Hard Gates

- Analysis cannot change metrics, thresholds, exclusions, or slices after seeing results without labeling the work exploratory; incomplete or incomparable runs cannot yield a pass claim.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `llm-experiment-execution`
- `llm-quality-evaluation`
- `model-and-workflow-benchmarking`
- `results-analysis-and-decision-readout`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
