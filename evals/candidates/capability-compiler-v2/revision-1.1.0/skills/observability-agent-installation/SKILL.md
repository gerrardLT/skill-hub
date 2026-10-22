---
name: observability-agent-installation
description: "Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization. Use when One observability agent must be installed on exact hosts or a cluster with a pinned artifact and least privilege; Someone asks for the exact install change, health check and uninstall path for an agent. Do not use for: Enable application-level APM instrumentation after the agent exists (-> apm-instrumentation-enablement); Verify emitted APM signals read-only after installation (-> apm-instrumentation-verification)."
---

# Observability Agent Installation

## Responsibility

Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization.

## Trigger

Use when the request matches any of:
- One observability agent must be installed on exact hosts or a cluster with a pinned artifact and least privilege
- Someone asks for the exact install change, health check and uninstall path for an agent

Do not use when:
- Enable application-level APM instrumentation after the agent exists. Route to `apm-instrumentation-enablement`.
- Verify emitted APM signals read-only after installation. Route to `apm-instrumentation-verification`.

## Required Inputs

- Platform, environment, provider account, credentials, desired instrumentation, and authorization.

## Procedure

1. Verify provider and platform variant, targets, OS or cluster versions, pinned package or image digest, integrity, identities, permissions, secret references, network, ports, resources, telemetry fields, redaction, sampling, retention, cost, health, upgrade, rollback, and fresh authorization.
2. Preview exact package, daemon, workload, RBAC, network, and config changes; block duplicate agents, privilege escalation, mutable latest, or uncontrolled telemetry.
3. Perform one bounded install with timeout and stop conditions without changing application code or unrelated platform resources.
4. Record installation receipt, artifact identity, target inventory, permissions, health, emitted-signal handoff, partial failure cleanup, uninstall, and rollback.

## Domain Guidance

- Cluster-type variant: self-hosted clusters (minikube, kind) need kubelet TLS verification disabled in the agent configuration; managed clusters (GKE, EKS, AKS) omit that setting.
- Health verification requires one healthy agent pod per node, naming every node by architecture (including arm64 nodes) and naming any node that has no pod yet.

## Output Contract

Produce:
- agent installation receipt
- pinned artifact and target inventory
- permission and telemetry governance evidence
- health, uninstall, and rollback record
- per-node health check list by architecture

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `apm-instrumentation-enablement`
- `apm-instrumentation-verification`
- `log-observability-configuration`
- `kubernetes-deployment-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
