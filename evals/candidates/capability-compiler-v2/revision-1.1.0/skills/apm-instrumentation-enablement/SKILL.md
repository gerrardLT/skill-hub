---
name: apm-instrumentation-enablement
description: "Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization. Use when One service needs APM tracing turned on through one approved instrumentation method after the agent is in place; Someone asks for the exact change that enables tracing for a service and environment without duplicate instrumentation. Do not use for: Verify that existing instrumentation emits correct traces and identity (-> apm-instrumentation-verification); Install the required observability agent on the target platform (-> observability-agent-installation)."
---

# APM Instrumentation Enablement

## Responsibility

Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization.

## Trigger

Use when the request matches any of:
- One service needs APM tracing turned on through one approved instrumentation method after the agent is in place
- Someone asks for the exact change that enables tracing for a service and environment without duplicate instrumentation

Do not use when:
- Verify that existing instrumentation emits correct traces and identity. Route to `apm-instrumentation-verification`.
- Install the required observability agent on the target platform. Route to `observability-agent-installation`.

## Required Inputs

- Installed agent, service runtime, platform variant, environment, and authorization.

## Procedure

1. Verify provider, platform and runtime, service and environment, current agents and libraries, compatibility, identity tags, sampling, sensitive fields, overhead budget, release metadata, health, rollback, and fresh authorization.
2. Choose exactly one instrumentation path, reusing an existing exporter where present, and give the concrete change with its resource and cost impact.
3. Detect duplicate auto and manual instrumentation, conflicting versions, unsupported runtime, and unexpected data capture before previewing exact change.
4. Perform one bounded enablement through the provider or platform adapter without installing unrelated agents or modifying other services.
5. Record provider receipt, instrumentation version, affected service, config, restart or propagation, health, verification handoff, and rollback.

## Domain Guidance

- Commit to exactly one instrumentation path. When an existing exporter or collector is already in use, reuse it and state why; leave no open alternative. Show the concrete change (for example a task-definition or manifest diff with the sidecar, dependency ordering and memory or cost increase for approval).
- Kubernetes variant preconditions: every context variable resolved before step 0, and the agent resource is extended in place rather than replaced with a second manifest.

## Output Contract

Produce:
- APM enablement receipt
- instrumentation and service identity
- duplicate and compatibility evidence
- verification and rollback handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `single-instrumentation-path`
- `service-environment`
- `compatibility`
- `overhead-budget`
- `telemetry-governance`
- `rollback`

## Hard Gates

- APM enablement requires a single known instrumentation path, exact service and environment identity, compatibility and overhead checks, governed telemetry, and rollback; duplicate instrumentation blocks change.
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
- `apm-instrumentation-verification`
- `apm-instrumentation-troubleshooting`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
