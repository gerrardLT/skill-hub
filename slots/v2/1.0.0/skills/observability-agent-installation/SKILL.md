---
name: observability-agent-installation
description: Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization. Do not use for enable application-level apm instrumentation after the agent exists or verify emitted apm signals read-only after installation.
---

# Observability Agent Installation

## Responsibility

Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization.

## Trigger

Use when the requested outcome is: Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization.

Do not use when:
- Enable application-level APM instrumentation after the agent exists. Route to `apm-instrumentation-enablement`.
- Verify emitted APM signals read-only after installation. Route to `apm-instrumentation-verification`.

## Required Inputs

- Platform, environment, provider account, credentials, desired instrumentation, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider and platform variant, targets, OS or cluster versions, pinned package or image digest, integrity, identities, permissions, secret references, network, ports, resources, telemetry fields, redaction, sampling, retention, cost, health, upgrade, rollback, and fresh authorization.
2. Preview exact package, daemon, workload, RBAC, network, and config changes; block duplicate agents, privilege escalation, mutable latest, or uncontrolled telemetry.
3. Perform one bounded install with timeout and stop conditions without changing application code or unrelated platform resources.
4. Record installation receipt, artifact identity, target inventory, permissions, health, emitted-signal handoff, partial failure cleanup, uninstall, and rollback.

## Output Contract

Produce:
- agent installation receipt
- pinned artifact and target inventory
- permission and telemetry governance evidence
- health, uninstall, and rollback record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `pinned-agent`
- `exact-targets`
- `least-privilege`
- `telemetry-governance`
- `health`
- `uninstall`
- `rollback`

## Hard Gates

- Agent installation requires a pinned verified artifact, exact targets, least privilege, governed telemetry, resource and network bounds, health evidence, and uninstall or rollback; mutable latest and duplicate agents are blocked.
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
- `apm-instrumentation-enablement`
- `apm-instrumentation-verification`
- `log-observability-configuration`
- `kubernetes-deployment-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
