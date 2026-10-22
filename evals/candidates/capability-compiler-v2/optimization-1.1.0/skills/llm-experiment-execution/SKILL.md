---
name: llm-experiment-execution
description: "Execute one reviewed frozen LLM experiment against exact dataset and evaluator versions under per-action provider-write, budget, and data-transfer authorization. Use when One reviewed, frozen LLM experiment must be launched against an exact dataset and evaluator versions under budget and transfer authorization; Someone asks for the exact run configuration, cost preview and cancellation path before an experiment is submitted. Do not use for: Design or calibrate the evaluator before experiment review (-> llm-evaluator-engineering); Analyze the frozen completed experiment results and advise the human owner (-> evaluation-results-analysis)."
---

# LLM Experiment Execution

## Responsibility

Execute one reviewed frozen LLM experiment against exact dataset and evaluator versions under per-action provider-write, budget, and data-transfer authorization.

## Trigger

Use when the request matches any of:
- One reviewed, frozen LLM experiment must be launched against an exact dataset and evaluator versions under budget and transfer authorization
- Someone asks for the exact run configuration, cost preview and cancellation path before an experiment is submitted

Do not use when:
- Design or calibrate the evaluator before experiment review. Route to `llm-evaluator-engineering`.
- Analyze the frozen completed experiment results and advise the human owner. Route to `evaluation-results-analysis`.

## Required Inputs

- Frozen experiment definition, dataset version, evaluator versions, provider target, budget, and authorization.

## Procedure

1. Verify reviewed experiment definition, hypotheses, variants, model and prompt versions, dataset identity, evaluator versions, seeds, sampling parameters, provider target, region, budget, transfer policy, retention, stop rules, and per-action authorization.
2. Preview exact request count, max cost, data fields leaving the boundary, retries, concurrency, idempotency key, and cancellation or partial-failure behavior.
3. Perform only the authorized provider run; do not change prompts, samples, evaluators, metrics, thresholds, or budget after submission.
4. Record provider run identity, exact parameters, raw result references and hashes, failed cases, retries, cost, duration, status, cancellation, and cleanup for later analysis.

## Domain Guidance

- Deliver a complete run configuration pinned to the frozen values that were supplied (dataset version, evaluator versions, model and parameters, seeds, budget, stop rules). Use a REQUIRED placeholder only for a value the task did not provide, and list each such value with its owner.
- Compute the cost preview with the arithmetic shown and name any unpriced component, such as a judge model, instead of leaving the total open.

## Output Contract

Produce:
- provider experiment run identity
- frozen parameter and version manifest
- raw result references and failure evidence
- cost, duration, cancellation, and cleanup record
- complete run configuration pinned to supplied frozen values, with placeholders only for unsupplied items

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `reviewed-definition`
- `exact-provider-target`
- `frozen-versions`
- `per-action-authorization`
- `budget`
- `idempotency`
- `run-receipt`
- `no-post-submit-drift`

## Hard Gates

- Experiment execution requires one exact reviewed definition and per-action provider authorization; any prompt, model, dataset, evaluator, metric, budget, transfer, or target drift invalidates or blocks the run.
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

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `llm-evaluator-engineering`
- `evaluation-dataset-publication`
- `evaluation-results-analysis`
- `llm-quality-evaluation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
