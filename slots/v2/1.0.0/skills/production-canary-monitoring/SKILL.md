---
name: production-canary-monitoring
description: Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation. Do not use for create or approve the immutable canary baseline artifacts or execute the approved release rollback.
---

# Production Canary Monitoring

## Responsibility

Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation.

## Trigger

Use when the requested outcome is: Continuously sample approved production pages or signals against immutable baselines, control alert noise, and recommend investigation or rollback without production mutation.

Do not use when:
- Create or approve the immutable canary baseline artifacts. Route to `canary-baseline-management`.
- Execute the approved release rollback. Route to `release-rollback-execution`.

## Required Inputs

- A deployed application, safely accessible pages, and a trusted initial baseline.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze deployment and baseline identities, allowlisted pages or signals, sampling cadence, windows, masks, thresholds, known noise, data policy, read-only authority, alert owner, and rollback condition.
2. Use approved read-only production requests or provider queries and write only bounded local evidence artifacts.
3. Compare current samples with immutable baselines, classify material, expected, noisy, unavailable, or ambiguous diffs, and track persistence and correlation with release health.
4. Return evidence, noise and confidence, alerts or recommendations, and recapture needs; never auto-promote, modify baseline, repair, change traffic, or rollback.

## Output Contract

Produce:
- production canary samples
- baseline diff and classification
- noise-control and confidence record
- investigation or rollback recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `immutable-baseline`
- `allowlisted-production`
- `sampling-window`
- `noise-control`
- `diff-classification`
- `no-auto-rollback`

## Hard Gates

- Canary monitoring is read-only: immutable baselines cannot be silently updated, and a threshold breach may recommend but never execute promotion, repair, traffic change, or rollback.
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
- `canary-baseline-management`
- `deployment-observation`
- `release-rollback-execution`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
