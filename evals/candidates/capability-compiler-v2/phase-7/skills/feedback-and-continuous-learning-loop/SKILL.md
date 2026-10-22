---
name: feedback-and-continuous-learning-loop
description: Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence. Do not use for collect new customer interviews or proprietary feedback data or persist an approved learning record locally.
---

# Feedback And Continuous Learning Loop

## Responsibility

Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.

## Trigger

Use when the requested outcome is: Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.

Do not use when:
- Collect new customer interviews or proprietary feedback data. Route to `research-planning-and-governance`.
- Persist an approved learning record locally. Route to `local-learning-persistence`.

## Required Inputs

- Runtime metrics, customer feedback, experiment results, alerts, and residual assumptions.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze review window, authorized inputs, source identities, metrics, feedback, experiment and incident evidence, assumptions, prior decisions, data governance, and decision owners.
2. Normalize evidence strength and freshness while preserving dissent, minority evidence, causal uncertainty, missing data, and invalidated prior evidence.
3. Update hypothesis confidence, opportunity or risk priority, decision thresholds, and unresolved questions without treating correlation as learning.
4. Return learning record candidate, review cadence, next input and owner, and persistence handoff; do not collect data, persist, approve product changes, or configure systems.

## Output Contract

Produce:
- calibrated hypothesis and learning record candidate
- evidence and uncertainty map
- priority and review cadence
- next discovery, experiment, reliability, or persistence handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `research-planning-and-governance`
- `local-learning-persistence`
- `engineering-retrospective-and-improvement`
- `metrics-system-and-observability`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
