---
name: production-canary-monitoring
description: "Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation. Use when Approved production pages need sampling against frozen baselines after a deploy, with noise controlled; Someone asks whether production pages have changed materially since the baseline and whether to investigate. Do not use for: Create or approve the immutable canary baseline artifacts (-> canary-baseline-management); Execute the approved release rollback (-> release-rollback-execution); Observe provider status, error rate and latency for a deployed change (-> deployment-observation)."
---

# Production Canary Monitoring

## Responsibility

Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation.

## Trigger

Use when the request matches any of:
- Approved production pages need sampling against frozen baselines after a deploy, with noise controlled
- Someone asks whether production pages have changed materially since the baseline and whether to investigate

Do not use when:
- Create or approve the immutable canary baseline artifacts. Route to `canary-baseline-management`.
- Execute the approved release rollback. Route to `release-rollback-execution`.
- Observe provider status, error rate and latency for a deployed change. Route to `deployment-observation`.

## Required Inputs

- A deployed application, safely accessible pages, and a trusted initial baseline.

## Procedure

1. Freeze deployment and baseline identities, allowlisted pages or signals, sampling cadence, windows, masks, thresholds, known noise, data policy, read-only authority, alert owner, and rollback condition.
2. Use approved read-only production requests or provider queries and write only bounded local evidence artifacts.
3. Compare current samples with immutable baselines, classify material, expected, noisy, unavailable, or ambiguous diffs, and track persistence and correlation with release health.
4. Return evidence, noise and confidence, alerts or recommendations, and recapture needs; never auto-promote, modify baseline, repair, change traffic, or rollback.

## Domain Guidance

- Sample on a fixed cadence (default every 60 seconds for the stated duration), reopening each page fresh so no state carries between checks, and classify each diff as material, expected, noisy, unavailable or ambiguous with persistence counts.

## Output Contract

Produce:
- production canary samples
- baseline diff and classification
- noise-control and confidence record
- investigation or rollback recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `immutable-baseline`
- `allowlisted-production`
- `sampling-window`
- `noise-control`
- `diff-classification`
- `no-auto-rollback`

## Hard Gates

- Canary monitoring is read-only: immutable baselines cannot be silently updated, and a threshold breach may recommend but never execute promotion, repair, traffic change, or rollback.
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
- `canary-baseline-management`
- `deployment-observation`
- `release-rollback-execution`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
