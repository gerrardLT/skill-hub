---
name: apm-instrumentation-verification
description: "Verify from read-only current evidence that APM instrumentation emits correct service, environment, version, trace linkage, sampling, and governed fields, and summarize multi-service onboarding coverage with its evidence and gaps. Use when Tracing was enabled and someone needs proof from current data that service, environment, version and trace linkage are right; Several services were onboarded and the owner needs one coverage view of which are verified, partly verified or stale. Do not use for: Enable the missing instrumentation or change its configuration (-> apm-instrumentation-enablement); Troubleshoot why expected signals are absent or malformed (-> apm-instrumentation-troubleshooting)."
---

# APM Instrumentation Verification

## Responsibility

Verify from read-only current evidence that APM instrumentation emits correct service, environment, version, trace linkage, sampling, and governed fields, and summarize multi-service onboarding coverage with its evidence and gaps.

## Trigger

Use when the request matches any of:
- Tracing was enabled and someone needs proof from current data that service, environment, version and trace linkage are right
- Several services were onboarded and the owner needs one coverage view of which are verified, partly verified or stale

Do not use when:
- Enable the missing instrumentation or change its configuration. Route to `apm-instrumentation-enablement`.
- Troubleshoot why expected signals are absent or malformed. Route to `apm-instrumentation-troubleshooting`.

## Required Inputs

- Instrumented environment, expected service identity, provider read access, and observation window.

## Procedure

1. Freeze expected service, environment, version, release, platform, routes, trace scenarios, field policy, sampling, time window, and read-only authority.
2. Acquire current provider evidence for known requests, trace and span relationships, errors, latency, identity tags, release linkage, and governed attributes.
3. Compare expected and observed coverage, duplication, sampling, redaction, clock and propagation delay, and mark untested scenarios.
4. Return verified, partial, failed, or blocked with exact evidence and troubleshooting handoff; no config change.

## Domain Guidance

- Multi-service coverage matrix: classify each service as not planned, blocked, configured but unverified, partially verified, verified, degraded or stale, never upgrading a status from prose. Each row links its status to current evidence, an owner, the gap and the next capability.
- Explain each gap concretely: for example zero root spans on a worker fits a downstream service that receives context, not a fault; an unknown_service source means the service name was never set. Give the fix as a specific check or change with its owner.
- A configured service is not verified, and stale evidence is not current.

## Output Contract

Produce:
- APM verification matrix
- current trace evidence
- expected-observed identity and coverage
- gap and troubleshooting handoff
- service coverage matrix with per-row evidence, owner, gap and next action
- stale-evidence register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `known-request`
- `current-trace`
- `service-environment-version`
- `trace-linkage`
- `redaction`
- `no-config-change`

## Hard Gates

- Instrumentation verifies only with current known-request evidence carrying the correct service, environment, version, relationships, sampling, and governed fields; configuration presence alone is insufficient.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `apm-instrumentation-enablement`
- `apm-instrumentation-troubleshooting`
- `service-identity-remapping`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
