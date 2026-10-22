---
name: service-identity-remapping
description: Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization. Do not use for define source revision and release metadata carried by telemetry or verify whether instrumentation already emits the expected service and environment identity.
---

# Service Identity Remapping

## Responsibility

Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization.

## Trigger

Use when the requested outcome is: Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization.

Do not use when:
- Define source revision and release metadata carried by telemetry. Route to `source-metadata-and-provenance`.
- Verify whether instrumentation already emits the expected service and environment identity. Route to `apm-instrumentation-verification`.

## Required Inputs

- Current service names, desired taxonomy, provider configuration, downstream dashboards, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, account or org, environment, old and new identity, source or runtime emitters, collision search, aliases, retention, dashboards, monitors, SLOs, ownership, access, historical continuity, propagation, rollback, and fresh authorization.
2. Preview exact remapping and affected queries, routes, tags, alerts, and integrations; block on collision or ambiguous producers.
3. Perform one bounded provider configuration change without altering instrumentation, unrelated services, or deleting historical data.
4. Record provider receipt, old and new mapping, affected resources, propagation verification, residual gaps, and rollback command or action.

## Output Contract

Produce:
- service identity remap receipt
- collision and continuity evidence
- affected dashboard, alert, and integration map
- verification and rollback record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `old-new-identity`
- `collision-check`
- `historical-continuity`
- `affected-resources`
- `per-action-authorization`
- `rollback`

## Hard Gates

- Identity remapping requires collision-free exact old and new identities, bounded provider scope, continuity plan, affected-resource inventory, verification, and rollback; renaming telemetry emitters is separate.
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
- `source-metadata-and-provenance`
- `apm-instrumentation-verification`
- `release-observability-configuration`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
