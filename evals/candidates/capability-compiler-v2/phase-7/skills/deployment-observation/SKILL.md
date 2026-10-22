---
name: deployment-observation
description: Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution. Do not use for trigger the approved deployment workflow or execute the approved rollback after its condition and authorization are satisfied.
---

# Deployment Observation

## Responsibility

Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution.

## Trigger

Use when the requested outcome is: Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution.

Do not use when:
- Trigger the approved deployment workflow. Route to `deployment-trigger-execution`.
- Execute the approved rollback after its condition and authorization are satisfied. Route to `release-rollback-execution`.

## Required Inputs

- A deployed change identity, provider read access, observation window, expected signals, and health thresholds.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze deployment and artifact identity, provider, environment, observation window, expected rollout, health and business criteria, baseline, alerts, read-only authority, rollback condition, and owner.
2. Read current provider status and approved production signals; bind every observation to timestamp, query, environment, release, and source.
3. Compare rollout, availability, errors, latency, saturation, resource, logs, traces, user or business guardrails, and anomalies against thresholds and baseline.
4. Persist bounded evidence and recommend continue, extend, investigate, or rollback; do not acknowledge alerts, change traffic, config, scale, repair, or rollback.

## Output Contract

Produce:
- deployment observation evidence
- health and guardrail comparison
- anomaly and confidence report
- continue, investigate, or rollback recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `deployment-identity`
- `observation-window`
- `current-signals`
- `baseline-thresholds`
- `read-only`
- `rollback-recommendation-not-action`

## Hard Gates

- Observation is read-only and cannot mutate production; a rollback recommendation is not rollback authorization or execution.
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
- `deployment-trigger-execution`
- `release-rollback-execution`
- `production-canary-monitoring`
- `incident-response-coordination`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
