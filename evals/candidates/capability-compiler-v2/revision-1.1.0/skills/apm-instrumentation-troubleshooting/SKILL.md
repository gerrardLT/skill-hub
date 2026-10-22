---
name: apm-instrumentation-troubleshooting
description: "Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners. Use when Expected traces, service names or versions are missing, duplicated or wrong in the APM provider; Someone asks why instrumentation that was enabled is not producing the expected signals. Do not use for: Enable or reconfigure APM instrumentation after diagnosis (-> apm-instrumentation-enablement); Verify expected service, environment, version, and trace evidence after a change (-> apm-instrumentation-verification)."
---

# APM Instrumentation Troubleshooting

## Responsibility

Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners.

## Trigger

Use when the request matches any of:
- Expected traces, service names or versions are missing, duplicated or wrong in the APM provider
- Someone asks why instrumentation that was enabled is not producing the expected signals

Do not use when:
- Enable or reconfigure APM instrumentation after diagnosis. Route to `apm-instrumentation-enablement`.
- Verify expected service, environment, version, and trace evidence after a change. Route to `apm-instrumentation-verification`.

## Required Inputs

- Failed verification evidence, platform variant, service configuration, logs, and authority boundary.

## Procedure

1. Freeze service, environment, version, platform, runtime, expected instrumentation, provider scope, read-only authority, symptom window, and sensitive-data boundary.
2. Inspect read-only status, agent or library versions, config metadata, startup evidence, network path, sampling, tags, trace routes, duplicate sources, and provider intake status.
3. Test competing hypotheses against timestamped evidence and separate missing emission, transport, sampling, identity, parsing, and provider-query failures.
4. Return root-cause confidence, evidence gaps, and exact enablement, installation, identity, or verification handoff; no remote fix.

## Domain Guidance

- Order checks provider side first (is the tracer reporting, does the provider recognise the service, what SDK configuration is active), then host side. Before asking for host access, say what you will check and why.

## Output Contract

Produce:
- APM troubleshooting evidence
- hypothesis and root-cause analysis
- signal-path diagnosis
- authorized fix and verification handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `read-only`
- `signal-path`
- `competing-hypotheses`
- `timestamped-evidence`
- `no-fix`
- `handoff`

## Hard Gates

- Troubleshooting is read-only: it cannot install agents, change sampling or tags, restart services, remap identity, or claim a fix from diagnosis alone.
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
- `apm-instrumentation-verification`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
