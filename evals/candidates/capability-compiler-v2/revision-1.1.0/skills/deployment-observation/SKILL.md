---
name: deployment-observation
description: "Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution. Use when A change has just been deployed and someone needs read-only health evidence against thresholds and a continue, investigate or rollback recommendation; Someone asks whether the release is healthy and what evidence would justify rolling back. Do not use for: Trigger the approved deployment workflow (-> deployment-trigger-execution); Execute the approved rollback after its condition and authorization are satisfied (-> release-rollback-execution)."
---

# Deployment Observation

## Responsibility

Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution.

## Trigger

Use when the request matches any of:
- A change has just been deployed and someone needs read-only health evidence against thresholds and a continue, investigate or rollback recommendation
- Someone asks whether the release is healthy and what evidence would justify rolling back

Do not use when:
- Trigger the approved deployment workflow. Route to `deployment-trigger-execution`.
- Execute the approved rollback after its condition and authorization are satisfied. Route to `release-rollback-execution`.

## Required Inputs

- A deployed change identity, provider read access, observation window, expected signals, and health thresholds.

## Procedure

1. Confirm deploy completion for the platform (workflow run for the merge SHA, or propagation wait) and record it as the window start.
2. Freeze deployment and artifact identity, provider, environment, observation window, expected rollout, health and business criteria, baseline, alerts, read-only authority, rollback condition, and owner.
3. Read current provider status and approved production signals; bind every observation to timestamp, query, environment, release, and source.
4. Compare rollout, availability, errors, latency, saturation, resource, logs, traces, user or business guardrails, and anomalies against thresholds and baseline.
5. Persist bounded evidence and recommend continue, extend, investigate, or rollback; do not acknowledge alerts, change traffic, config, scale, repair, or rollback.

## Domain Guidance

- The observation window starts at confirmed deploy completion per platform: a matching workflow run for the merge SHA has succeeded, or an auto-deploy platform has had its propagation wait. Record the start time and how it was confirmed.
- When the identity is read-only, decline to roll back and say so. Still give an explicit rollback recommendation addressed to a named authorized operator, with the trigger condition and the evidence that supports it, and enumerate the evidence still missing.
- Bind every observation to its query, timestamp, environment and release.

## Output Contract

Produce:
- deployment observation evidence
- health and guardrail comparison
- anomaly and confidence report
- continue, investigate, or rollback recommendation
- explicit rollback recommendation addressed to an authorized operator, with missing-evidence list

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `deployment-identity`
- `observation-window`
- `current-signals`
- `baseline-thresholds`
- `read-only`
- `rollback-recommendation-not-action`

## Hard Gates

- Observation is read-only and cannot mutate production; a rollback recommendation is not rollback authorization or execution.
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
- `deployment-trigger-execution`
- `release-rollback-execution`
- `production-canary-monitoring`
- `incident-response-coordination`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
