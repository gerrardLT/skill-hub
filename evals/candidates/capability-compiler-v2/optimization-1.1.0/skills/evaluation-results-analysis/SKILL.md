---
name: evaluation-results-analysis
description: "Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes. Use when Finished LLM experiment or evaluation runs must be compared on predeclared metrics with variance and failure slices; Someone asks whether a model or prompt variant is really better once uncertainty and cost are counted. Do not use for: Execute the reviewed experiment against the provider (-> llm-experiment-execution); Evaluate raw model outputs with metrics, judges, and human agreement first (-> llm-quality-evaluation); Interpret a product or UX experiment against its go, pivot or kill rule (-> results-analysis-and-decision-readout); Check whether the data or metric itself is correct (-> data-analysis-validation)."
---

# Evaluation Results Analysis

## Responsibility

Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.

## Trigger

Use when the request matches any of:
- Finished LLM experiment or evaluation runs must be compared on predeclared metrics with variance and failure slices
- Someone asks whether a model or prompt variant is really better once uncertainty and cost are counted

Do not use when:
- Execute the reviewed experiment against the provider. Route to `llm-experiment-execution`.
- Evaluate raw model outputs with metrics, judges, and human agreement first. Route to `llm-quality-evaluation`.
- Interpret a product or UX experiment against its go, pivot or kill rule. Route to `results-analysis-and-decision-readout`.
- Check whether the data or metric itself is correct. Route to `data-analysis-validation`.

## Required Inputs

- Experiment results, metric contract, baseline, statistical assumptions, and known data limits.

## Procedure

1. Freeze run identities, dataset and evaluator versions, metric contract, thresholds, exclusions, statistical assumptions, baseline, costs, and known data limits.
2. Verify result completeness, pairing, missingness, duplicates, contamination, retries, failed runs, and comparable versions before analysis.
3. Compute declared aggregates, distributions, uncertainty, effect sizes or intervals, failure slices, cost and latency, and sensitivity without metric shopping.
4. Return supported and unsupported claims, regressions, tradeoffs, and a recommendation to the named human owner; do not rerun, approve, or deploy.

## Domain Guidance

- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

## Output Contract

Produce:
- experiment comparison
- variance and uncertainty report
- failure-slice and regression analysis
- evidence-bounded human decision readout

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `llm-experiment-execution`
- `llm-quality-evaluation`
- `model-and-workflow-benchmarking`
- `results-analysis-and-decision-readout`
- `data-analysis-validation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
