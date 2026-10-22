---
name: feedback-and-continuous-learning-loop
description: "Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence. Use when A review cycle has new metrics, customer feedback, experiment results or alerts and someone must update what the team believes and what to do next; Hypotheses and priorities need re-rating after new evidence, with contrary evidence kept visible. Do not use for: Collect new customer interviews or proprietary feedback data (-> research-planning-and-governance); Persist an approved learning record locally (-> local-learning-persistence); Review an engineering period for delivery friction and improvement experiments (-> engineering-retrospective-and-improvement); Validate that a dataset, metric or analysis is correct before anyone uses it (-> data-analysis-validation)."
---

# Feedback And Continuous Learning Loop

## Responsibility

Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.

## Trigger

Use when the request matches any of:
- A review cycle has new metrics, customer feedback, experiment results or alerts and someone must update what the team believes and what to do next
- Hypotheses and priorities need re-rating after new evidence, with contrary evidence kept visible

Do not use when:
- Collect new customer interviews or proprietary feedback data. Route to `research-planning-and-governance`.
- Persist an approved learning record locally. Route to `local-learning-persistence`.
- Review an engineering period for delivery friction and improvement experiments. Route to `engineering-retrospective-and-improvement`.
- Validate that a dataset, metric or analysis is correct before anyone uses it. Route to `data-analysis-validation`.

## Required Inputs

- Runtime metrics, customer feedback, experiment results, alerts, and residual assumptions.

## Procedure

1. Freeze review window, authorized inputs, source identities, metrics, feedback, experiment and incident evidence, assumptions, prior decisions, data governance, and decision owners.
2. Normalize evidence strength and freshness while preserving dissent, minority evidence, causal uncertainty, missing data, and invalidated prior evidence.
3. Update hypothesis confidence, opportunity or risk priority, decision thresholds, and unresolved questions without treating correlation as learning.
4. Return learning record candidate, review cadence, next input and owner, and persistence handoff; do not collect data, persist, approve product changes, or configure systems.

## Domain Guidance

- Confidence scale for every hypothesis: 1 untested assumption, 2 single anecdotal source, 3 multiple consistent sources, 4 measured in a controlled or pre-registered comparison, 5 replicated. Record the value before and after, and the specific evidence that moved it.
- Treat correlation, stale metrics and repeated opinion as no movement. State the evidence age and reject anything older than the stated review window.
- End with one next learning input, its owner and a review date.

## Output Contract

Produce:
- calibrated hypothesis and learning record candidate
- evidence and uncertainty map
- priority and review cadence
- next discovery, experiment, reliability, or persistence handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `evidence-freshness`
- `hypothesis-calibration`
- `contrary-evidence`
- `causal-uncertainty`
- `review-cadence`
- `next-learning-input`
- `no-persistence`

## Hard Gates

- Continuous learning must link each confidence or priority change to current authorized evidence and preserve contrary evidence; repeated opinion, stale metrics, or correlation alone is not learning.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `research-planning-and-governance`
- `local-learning-persistence`
- `engineering-retrospective-and-improvement`
- `metrics-system-and-observability`
- `data-analysis-validation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
