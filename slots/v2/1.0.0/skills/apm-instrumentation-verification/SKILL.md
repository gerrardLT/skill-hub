---
name: apm-instrumentation-verification
description: Verify from read-only current evidence that APM instrumentation emits correct service, environment, version, trace linkage, sampling, and governed fields. Do not use for enable the missing instrumentation or change its configuration or troubleshoot why expected signals are absent or malformed.
---

# Apm Instrumentation Verification

## Responsibility

Verify from read-only current evidence that APM instrumentation emits correct service, environment, version, trace linkage, sampling, and governed fields.

## Trigger

Use when the requested outcome is: Verify from read-only current evidence that APM instrumentation emits correct service, environment, version, trace linkage, sampling, and governed fields.

Do not use when:
- Enable the missing instrumentation or change its configuration. Route to `apm-instrumentation-enablement`.
- Troubleshoot why expected signals are absent or malformed. Route to `apm-instrumentation-troubleshooting`.

## Required Inputs

- Instrumented environment, expected service identity, provider read access, and observation window.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze expected service, environment, version, release, platform, routes, trace scenarios, field policy, sampling, time window, and read-only authority.
2. Acquire current provider evidence for known requests, trace and span relationships, errors, latency, identity tags, release linkage, and governed attributes.
3. Compare expected and observed coverage, duplication, sampling, redaction, clock and propagation delay, and mark untested scenarios.
4. Return verified, partial, failed, or blocked with exact evidence and troubleshooting handoff; no config change.

## Output Contract

Produce:
- APM verification matrix
- current trace evidence
- expected-observed identity and coverage
- gap and troubleshooting handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `known-request`
- `current-trace`
- `service-environment-version`
- `trace-linkage`
- `redaction`
- `no-config-change`

## Hard Gates

- Instrumentation verifies only with current known-request evidence carrying the correct service, environment, version, relationships, sampling, and governed fields; configuration presence alone is insufficient.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `apm-instrumentation-enablement`
- `apm-instrumentation-troubleshooting`
- `service-identity-remapping`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
