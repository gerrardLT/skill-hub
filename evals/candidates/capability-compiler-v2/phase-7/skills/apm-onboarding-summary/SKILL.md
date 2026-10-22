---
name: apm-onboarding-summary
description: Summarize current APM onboarding coverage, verified evidence, gaps, owners, and next actions without configuring or verifying systems itself. Do not use for verify instrumentation by reading current provider traces or enable instrumentation for a missing service.
---

# Apm Onboarding Summary

## Responsibility

Summarize current APM onboarding coverage, verified evidence, gaps, owners, and next actions without configuring or verifying systems itself.

## Trigger

Use when the requested outcome is: Summarize current APM onboarding coverage, verified evidence, gaps, owners, and next actions without configuring or verifying systems itself.

Do not use when:
- Verify instrumentation by reading current provider traces. Route to `apm-instrumentation-verification`.
- Enable instrumentation for a missing service. Route to `apm-instrumentation-enablement`.

## Required Inputs

- Installation, enablement, verification, and troubleshooting evidence.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze service inventory, environments, enablement receipts, verification reports, troubleshooting results, ownership, target coverage, and evidence freshness.
2. Classify each service as not planned, blocked, configured-unverified, partially verified, verified, degraded, or stale without upgrading status from prose.
3. Link every status and gap to current evidence, owner, dependency, target date, and next capability.
4. Return summary and action map only; no provider read, configuration, installation, or approval.

## Output Contract

Produce:
- APM onboarding status summary
- service coverage matrix
- gap and owner action map
- stale-evidence register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `service-inventory`
- `configured-not-verified`
- `evidence-freshness`
- `owner`
- `next-action`
- `no-provider-action`

## Hard Gates

- Onboarding summary cannot treat configured as verified or stale evidence as current; every service status needs an evidence reference and owner.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `apm-instrumentation-verification`
- `apm-instrumentation-enablement`
- `apm-instrumentation-troubleshooting`
- `observability-agent-installation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
