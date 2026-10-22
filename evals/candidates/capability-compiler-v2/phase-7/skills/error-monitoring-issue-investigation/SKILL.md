---
name: error-monitoring-issue-investigation
description: Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation. Do not use for apply the confirmed source repair or respond to a pull-request comment about the repair.
---

# Error Monitoring Issue Investigation

## Responsibility

Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation.

## Trigger

Use when the requested outcome is: Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation.

Do not use when:
- Apply the confirmed source repair. Route to `defect-remediation`.
- Respond to a pull-request comment about the repair. Route to `pull-request-comment-response`.

## Required Inputs

- Issue identity, event context, release, environment, source access, and authority boundary.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze provider, project, issue ID, time range, environment, release, data policy, read-only authority, source mapping, and investigation question.
2. Inspect current event groups, samples, stack traces, breadcrumbs, tags, frequency, users or tenants, release correlation, first and last seen, and linked traces under minimization.
3. Test competing hypotheses against source and runtime evidence and distinguish grouping artifact, symptom, trigger, and root cause.
4. Return evidence, confidence, affected surface, and bounded repair or further-instrumentation recommendation; do not comment, assign, resolve, ignore, mute, edit source, or change provider state.

## Output Contract

Produce:
- error issue evidence bundle
- hypothesis and root-cause analysis
- release and impact correlation
- bounded repair or instrumentation recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-issue`
- `read-only-events`
- `release-correlation`
- `competing-hypotheses`
- `cause-not-stack-frame`
- `no-provider-mutation`

## Hard Gates

- Issue investigation is read-only: it cannot resolve, mute, assign, comment, change grouping, edit source, or treat one stack trace as proven root cause.
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
- `defect-remediation`
- `production-llm-trace-root-cause-analysis`
- `production-trace-classification`
- `pull-request-comment-response`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
