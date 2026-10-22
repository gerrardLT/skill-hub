---
name: log-observability-configuration
description: Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization. Do not use for define metrics, dashboards, and alert semantics from approved outcomes or install the observability agent required to collect host logs.
---

# Log Observability Configuration

## Responsibility

Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization.

## Trigger

Use when the requested outcome is: Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization.

Do not use when:
- Define metrics, dashboards, and alert semantics from approved outcomes. Route to `metrics-system-and-observability`.
- Install the observability agent required to collect host logs. Route to `observability-agent-installation`.

## Required Inputs

- Log sources, schemas, provider, authorization, retention, redaction, and routing requirements.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, account, sources, services, environments, log schemas, fields, PII and secret classes, minimization, redaction, parsing, routing, sampling, retention, region, access, cost, deletion, failure handling, and fresh authorization.
2. Preview exact sources, pipelines, indexes, destinations, transformations, and sample redacted events; block credential or sensitive-value capture.
3. Perform one bounded configuration change without modifying applications, unrelated pipelines, monitors, or retention outside scope.
4. Record provider receipt, config version, sample validation, volume and cost estimate, access, retention, deletion, propagation, and rollback.

## Output Contract

Produce:
- log configuration receipt
- source, parse, and route schema
- redaction, retention, access, and cost record
- sample validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-log-sources`
- `parsing`
- `routing`
- `redaction`
- `retention`
- `access`
- `volume-cost`
- `deletion`

## Hard Gates

- Logs deny secret and sensitive fields by default and require exact source, parsing, routing, retention, access, deletion, volume, and cost boundaries before provider mutation.
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
- `monitoring-and-alert-configuration`
- `observability-agent-installation`
- `source-metadata-and-provenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
