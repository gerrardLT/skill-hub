---
name: monitoring-and-alert-configuration
description: "Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization. Use when A monitor or alert route must be created or changed from an approved SLO, threshold, window and owner; Someone asks for the exact alert definition with missing-data behavior, routing and runbook. Do not use for: Define the metric system and threshold rationale first (-> metrics-system-and-observability); Coordinate an active incident after an alert fires (-> incident-response-coordination); Handle model calls, prompts, traces and evaluation telemetry (-> ai-observability-configuration); Handle log collection, parsing, routing and retention (-> log-observability-configuration); Handle release and commit association for services and environments (-> release-observability-configuration)."
---

# Monitoring And Alert Configuration

## Responsibility

Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization.

## Trigger

Use when the request matches any of:
- A monitor or alert route must be created or changed from an approved SLO, threshold, window and owner
- Someone asks for the exact alert definition with missing-data behavior, routing and runbook

Do not use when:
- Define the metric system and threshold rationale first. Route to `metrics-system-and-observability`.
- Coordinate an active incident after an alert fires. Route to `incident-response-coordination`.
- Handle model calls, prompts, traces and evaluation telemetry. Route to `ai-observability-configuration`.
- Handle log collection, parsing, routing and retention. Route to `log-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.

## Required Inputs

- Signal definition, threshold rationale, evaluation window, recipients, provider, and authorization.

## Procedure

1. Verify provider, account, environment, metric definitions, SLO, threshold or burn-rate rationale, windows, missing-data behavior, severity, routing, schedules, deduplication, suppression, runbook, test method, owner, rollback, and fresh authorization.
2. Preview exact monitor and notification diff and predicted behavior against historical data where available.
3. Perform one bounded provider configuration change without acknowledging incidents or altering unrelated monitors, dashboards, or integrations.
4. Record provider receipt, monitor IDs and version, test notification or dry-run evidence, routing, noise and cost risk, propagation, and rollback.

## Domain Guidance

- An alert without an actionable named owner and a runbook is not ready: return the definition as a draft and name who must accept it before creation.
- Preview predicted alert volume from historical data where available and state the noise and cost risk.
- Discriminator by signal type: this Skill handles monitors and alert routes from approved SLOs.
- Rollback verification must check that the changed rule and routes have actually reverted in the exact authorized provider target, not merely that the rollback command returned successfully. Proposal-only outputs label this verification as pending.

## Output Contract

Produce:
- monitor and alert configuration receipt
- threshold, window, and missing-data contract
- routing and runbook map
- validation, noise, and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `metrics-system-and-observability`
- `incident-response-coordination`
- `release-observability-configuration`
- `production-canary-monitoring`
- `ai-observability-configuration`
- `log-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
