---
name: incident-response-coordination
description: Coordinate an active incident's severity, roles, timeline, hypotheses, mitigation options, communications, recovery criteria, and closure recommendation from read-only evidence without executing provider actions. Do not use for execute the approved release rollback or perform the post-incident engineering retrospective after closure.
---

# Incident Response Coordination

## Responsibility

Coordinate an active incident's severity, roles, timeline, hypotheses, mitigation options, communications, recovery criteria, and closure recommendation from read-only evidence without executing provider actions.

## Trigger

Use when the requested outcome is: Coordinate an active incident's severity, roles, timeline, hypotheses, mitigation options, communications, recovery criteria, and closure recommendation from read-only evidence without executing provider actions.

Do not use when:
- Execute the approved release rollback. Route to `release-rollback-execution`.
- Perform the post-incident engineering retrospective after closure. Route to `engineering-retrospective-and-improvement`.

## Required Inputs

- An active production anomaly, impact evidence, alerts, and available mitigation controls.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze incident identity, source and environment, start time, impact, affected users or services, current evidence, read-only provider scope, available specialist controls, safety boundaries, communication policy, and incident authority.
2. Establish severity recommendation, incident lead, communications, operations and specialist owners, timeline, fact and hypothesis log, and decision cadence without provider acknowledgement or state change.
3. Prioritize user and system safety, containment and reversible mitigation options; route exact actions to separately authorized rollback, deployment, infrastructure, or remediation owners.
4. Track observed recovery against explicit criteria and recommend continue, escalate, rollback, recover, or close; preserve uncertainty and produce a closure record candidate without closing provider incidents.

## Output Contract

Produce:
- incident coordination record
- roles, timeline, fact, hypothesis, and decision log
- mitigation and specialist action handoffs
- recovery evidence and closure recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `severity`
- `roles`
- `timeline`
- `fact-hypothesis`
- `mitigation-first`
- `separate-action-owner`
- `no-provider-mutation`
- `closure-recommendation`

## Hard Gates

- Coordination under external-read authority cannot acknowledge, silence, assign, comment, change traffic, scale, restart, deploy, rollback, remediate, or close provider incidents; every action routes to a separately authorized owner.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `release-rollback-execution`
- `deployment-observation`
- `engineering-retrospective-and-improvement`
- `error-monitoring-issue-investigation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
