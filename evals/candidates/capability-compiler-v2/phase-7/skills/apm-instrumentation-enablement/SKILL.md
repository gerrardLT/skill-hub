---
name: apm-instrumentation-enablement
description: Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization. Do not use for verify that existing instrumentation emits correct traces and identity or install the required observability agent on the target platform.
---

# Apm Instrumentation Enablement

## Responsibility

Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization.

## Trigger

Use when the requested outcome is: Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization.

Do not use when:
- Verify that existing instrumentation emits correct traces and identity. Route to `apm-instrumentation-verification`.
- Install the required observability agent on the target platform. Route to `observability-agent-installation`.

## Required Inputs

- Installed agent, service runtime, platform variant, environment, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, platform and runtime, service and environment, current agents and libraries, compatibility, identity tags, sampling, sensitive fields, overhead budget, release metadata, health, rollback, and fresh authorization.
2. Detect duplicate auto and manual instrumentation, conflicting versions, unsupported runtime, and unexpected data capture before previewing exact change.
3. Perform one bounded enablement through the provider or platform adapter without installing unrelated agents or modifying other services.
4. Record provider receipt, instrumentation version, affected service, config, restart or propagation, health, verification handoff, and rollback.

## Output Contract

Produce:
- APM enablement receipt
- instrumentation and service identity
- duplicate and compatibility evidence
- verification and rollback handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `single-instrumentation-path`
- `service-environment`
- `compatibility`
- `overhead-budget`
- `telemetry-governance`
- `rollback`

## Hard Gates

- APM enablement requires a single known instrumentation path, exact service and environment identity, compatibility and overhead checks, governed telemetry, and rollback; duplicate instrumentation blocks change.
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
- `apm-instrumentation-verification`
- `apm-instrumentation-troubleshooting`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
