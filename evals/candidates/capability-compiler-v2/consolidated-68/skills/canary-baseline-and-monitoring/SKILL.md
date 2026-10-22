---
name: canary-baseline-and-monitoring
description: "Consolidated capability with 3 selectable modes: canary-baseline-management; deployment-observation; production-canary-monitoring. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [canary-baseline-management, deployment-observation, production-canary-monitoring]
---

# Canary Baseline And Monitoring

## Responsibility

Consolidated capability covering 3 related modes: Create or update immutable local canary baseline evidence only for explicitly selected production pages, without application or provider mutation.; Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution.; Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `canary-baseline-management` | `artifact-write-local-exec-external-read` | Chosen production pages need a frozen baseline capture to compare future canary samples against; A healthy release should replace the old baseline and the change must be recorded without deleting the  | Continuously observe production pages and diff signals against the baseline (-> production-canary-monitoring); Fix the a |
| `deployment-observation` | `artifact-write-local-exec-external-read` | A change has just been deployed and someone needs read-only health evidence against thresholds and a continue, investigate or rollback recommendation; Someone asks whether the release is healthy and w | Trigger the approved deployment workflow (-> deployment-trigger-execution); Execute the approved rollback after its cond |
| `production-canary-monitoring` | `artifact-write-local-exec-external-read` | Approved production pages need sampling against frozen baselines after a deploy, with noise controlled; Someone asks whether production pages have changed materially since the baseline and whether to  | Create or approve the immutable canary baseline artifacts (-> canary-baseline-management); Execute the approved release  |

## Mode: `canary-baseline-management`

### canary-baseline-management

#### Responsibility

Create or update immutable local canary baseline evidence only for explicitly selected production pages, without application or provider mutation.

#### Trigger

Use when the request matches any of:
- Chosen production pages need a frozen baseline capture to compare future canary samples against
- A healthy release should replace the old baseline and the change must be recorded without deleting the old one

Do not use when:
- Continuously observe production pages and diff signals against the baseline. Route to `production-canary-monitoring`.
- Fix the application after an accepted canary finding. Route to `defect-remediation`.

#### Required Inputs

- Approved URL and pages, external read authority, artifact directory, prior baseline, and baseline-write decision.

#### Procedure

1. Freeze deployment and source identity, selected allowlisted pages, states, viewport, browser, data boundary, capture fields, masking, retention, baseline version, replacement approval, and artifact destination.
2. Use approved local and read-only external capture, avoid authenticated or sensitive pages unless separately governed, and record complete provenance.
3. Write immutable baseline artifacts, manifest, hashes, masks, thresholds, and supersession links without changing application source or provider config.
4. Return baseline identity, old and new relationship, capture evidence, limitations, and deletion path.

#### Domain Guidance

- Capture a baseline before the deploy; replace it only after a healthy canary, with the prior version kept and linked in an explicit supersession record (old id, new id, reason, approver).
- Define concrete invalidation triggers for each baseline (release changes layout, A/B test active, data-dependent content) and flag measurable shifts the new capture shows, for example a rise in largest contentful paint.

#### Output Contract

Produce:
- versioned canary baseline artifacts
- capture provenance manifest
- threshold and masking policy
- supersession and deletion record
- supersession record and baseline invalidation triggers

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `allowlisted-pages`
- `immutable-baseline`
- `capture-provenance`
- `masking`
- `thresholds`
- `supersession`

#### Hard Gates

- A canary baseline is an immutable evidence artifact for explicit pages and states; replacing it requires approval and preserves the prior version, reason, and comparison continuity.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `production-canary-monitoring`
- `deployment-observation`
- `defect-remediation`
- `source-metadata-and-provenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `deployment-observation`

### deployment-observation

#### Responsibility

Observe one deployed change through read-only provider status and production health signals, persist bounded evidence, and recommend continue, investigate, or rollback without recovery execution.

#### Trigger

Use when the request matches any of:
- A change has just been deployed and someone needs read-only health evidence against thresholds and a continue, investigate or rollback recommendation
- Someone asks whether the release is healthy and what evidence would justify rolling back

Do not use when:
- Trigger the approved deployment workflow. Route to `deployment-trigger-execution`.
- Execute the approved rollback after its condition and authorization are satisfied. Route to `release-rollback-execution`.

#### Required Inputs

- A deployed change identity, provider read access, observation window, expected signals, and health thresholds.

#### Procedure

1. Confirm deploy completion for the platform (workflow run for the merge SHA, or propagation wait) and record it as the window start.
2. Freeze deployment and artifact identity, provider, environment, observation window, expected rollout, health and business criteria, baseline, alerts, read-only authority, rollback condition, and owner.
3. Read current provider status and approved production signals; bind every observation to timestamp, query, environment, release, and source.
4. Compare rollout, availability, errors, latency, saturation, resource, logs, traces, user or business guardrails, and anomalies against thresholds and baseline.
5. Persist bounded evidence and recommend continue, extend, investigate, or rollback; do not acknowledge alerts, change traffic, config, scale, repair, or rollback.

#### Domain Guidance

- The observation window starts at confirmed deploy completion per platform: a matching workflow run for the merge SHA has succeeded, or an auto-deploy platform has had its propagation wait. Record the start time and how it was confirmed.
- When the identity is read-only, decline to roll back and say so. Still give an explicit rollback recommendation addressed to a named authorized operator, with the trigger condition and the evidence that supports it, and enumerate the evidence still missing.
- Bind every observation to its query, timestamp, environment and release.

#### Output Contract

Produce:
- deployment observation evidence
- health and guardrail comparison
- anomaly and confidence report
- continue, investigate, or rollback recommendation
- explicit rollback recommendation addressed to an authorized operator, with missing-evidence list

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `deployment-identity`
- `observation-window`
- `current-signals`
- `baseline-thresholds`
- `read-only`
- `rollback-recommendation-not-action`

#### Hard Gates

- Observation is read-only and cannot mutate production; a rollback recommendation is not rollback authorization or execution.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `deployment-trigger-execution`
- `release-rollback-execution`
- `production-canary-monitoring`
- `incident-response-coordination`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `production-canary-monitoring`

### production-canary-monitoring

#### Responsibility

Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation.

#### Trigger

Use when the request matches any of:
- Approved production pages need sampling against frozen baselines after a deploy, with noise controlled
- Someone asks whether production pages have changed materially since the baseline and whether to investigate

Do not use when:
- Create or approve the immutable canary baseline artifacts. Route to `canary-baseline-management`.
- Execute the approved release rollback. Route to `release-rollback-execution`.
- Observe provider status, error rate and latency for a deployed change. Route to `deployment-observation`.

#### Required Inputs

- A deployed application, safely accessible pages, and a trusted initial baseline.

#### Procedure

1. Freeze deployment and baseline identities, allowlisted pages or signals, sampling cadence, windows, masks, thresholds, known noise, data policy, read-only authority, alert owner, and rollback condition.
2. Use approved read-only production requests or provider queries and write only bounded local evidence artifacts.
3. Compare current samples with immutable baselines, classify material, expected, noisy, unavailable, or ambiguous diffs, and track persistence and correlation with release health.
4. Return evidence, noise and confidence, alerts or recommendations, and recapture needs; never auto-promote, modify baseline, repair, change traffic, or rollback.

#### Domain Guidance

- Sample on a fixed cadence (default every 60 seconds for the stated duration), reopening each page fresh so no state carries between checks, and classify each diff as material, expected, noisy, unavailable or ambiguous with persistence counts.

#### Output Contract

Produce:
- production canary samples
- baseline diff and classification
- noise-control and confidence record
- investigation or rollback recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `immutable-baseline`
- `allowlisted-production`
- `sampling-window`
- `noise-control`
- `diff-classification`
- `no-auto-rollback`

#### Hard Gates

- Canary monitoring is read-only: immutable baselines cannot be silently updated, and a threshold breach may recommend but never execute promotion, repair, traffic change, or rollback.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `canary-baseline-management`
- `deployment-observation`
- `release-rollback-execution`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
