---
name: monitoring-and-alert-configuration
description: Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization. Do not use for define the metric system and threshold rationale first or coordinate an active incident after an alert fires.
---

# Monitoring And Alert Configuration

## Responsibility

Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization.

## Trigger

Use when the requested outcome is: Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization.

Do not use when:
- Define the metric system and threshold rationale first. Route to `metrics-system-and-observability`.
- Coordinate an active incident after an alert fires. Route to `incident-response-coordination`.

## Required Inputs

- Signal definition, threshold rationale, evaluation window, recipients, provider, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, account, environment, metric definitions, SLO, threshold or burn-rate rationale, windows, missing-data behavior, severity, routing, schedules, deduplication, suppression, runbook, test method, owner, rollback, and fresh authorization.
2. Preview exact monitor and notification diff and predicted behavior against historical data where available.
3. Perform one bounded provider configuration change without acknowledging incidents or altering unrelated monitors, dashboards, or integrations.
4. Record provider receipt, monitor IDs and version, test notification or dry-run evidence, routing, noise and cost risk, propagation, and rollback.

## Output Contract

Produce:
- monitor and alert configuration receipt
- threshold, window, and missing-data contract
- routing and runbook map
- validation, noise, and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `SLO-threshold`
- `window`
- `missing-data`
- `actionable-owner`
- `routing`
- `deduplication`
- `runbook`
- `rollback`

## Hard Gates

- An alert requires an actionable owner, justified threshold and window, missing-data behavior, deduplication, runbook, validation, and rollback; alert volume alone is not coverage.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This candidate defines an action contract, but Phase 7 candidate construction does not execute the action. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `metrics-system-and-observability`
- `incident-response-coordination`
- `release-observability-configuration`
- `production-canary-monitoring`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
