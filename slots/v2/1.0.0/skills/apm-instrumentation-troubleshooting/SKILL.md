---
name: apm-instrumentation-troubleshooting
description: Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners. Do not use for enable or reconfigure apm instrumentation after diagnosis or verify expected service, environment, version, and trace evidence after a change.
---

# Apm Instrumentation Troubleshooting

## Responsibility

Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners.

## Trigger

Use when the requested outcome is: Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners.

Do not use when:
- Enable or reconfigure APM instrumentation after diagnosis. Route to `apm-instrumentation-enablement`.
- Verify expected service, environment, version, and trace evidence after a change. Route to `apm-instrumentation-verification`.

## Required Inputs

- Failed verification evidence, platform variant, service configuration, logs, and authority boundary.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze service, environment, version, platform, runtime, expected instrumentation, provider scope, read-only authority, symptom window, and sensitive-data boundary.
2. Inspect read-only status, agent or library versions, config metadata, startup evidence, network path, sampling, tags, trace routes, duplicate sources, and provider intake status.
3. Test competing hypotheses against timestamped evidence and separate missing emission, transport, sampling, identity, parsing, and provider-query failures.
4. Return root-cause confidence, evidence gaps, and exact enablement, installation, identity, or verification handoff; no remote fix.

## Output Contract

Produce:
- APM troubleshooting evidence
- hypothesis and root-cause analysis
- signal-path diagnosis
- authorized fix and verification handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `read-only`
- `signal-path`
- `competing-hypotheses`
- `timestamped-evidence`
- `no-fix`
- `handoff`

## Hard Gates

- Troubleshooting is read-only: it cannot install agents, change sampling or tags, restart services, remap identity, or claim a fix from diagnosis alone.
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
- `apm-instrumentation-verification`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
