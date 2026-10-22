---
name: error-monitoring-issue-investigation
description: "Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation. Use when One error-monitoring issue needs its events, releases and stack traces turned into an evidence-bounded root-cause hypothesis; Someone asks what caused an alert or a regression in production errors, read-only. Do not use for: Apply the confirmed source repair (-> defect-remediation); Respond to a pull-request comment about the repair (-> pull-request-comment-response); Reproduce and trace a defect locally from a failing test or incident (-> root-cause-investigation)."
---

# Error Monitoring Issue Investigation

## Responsibility

Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation.

## Trigger

Use when the request matches any of:
- One error-monitoring issue needs its events, releases and stack traces turned into an evidence-bounded root-cause hypothesis
- Someone asks what caused an alert or a regression in production errors, read-only

Do not use when:
- Apply the confirmed source repair. Route to `defect-remediation`.
- Respond to a pull-request comment about the repair. Route to `pull-request-comment-response`.
- Reproduce and trace a defect locally from a failing test or incident. Route to `root-cause-investigation`.

## Required Inputs

- Issue identity, event context, release, environment, source access, and authority boundary.

## Procedure

1. Classify the issue as error, performance or scheduled-job monitor before pulling context.
2. Freeze provider, project, issue ID, time range, environment, release, data policy, read-only authority, source mapping, and investigation question.
3. Inspect current event groups, samples, stack traces, breadcrumbs, tags, frequency, users or tenants, release correlation, first and last seen, and linked traces under minimization.
4. Test competing hypotheses against source and runtime evidence and distinguish grouping artifact, symptom, trigger, and root cause.
5. Return evidence, confidence, affected surface, and bounded repair or further-instrumentation recommendation; do not comment, assign, resolve, ignore, mute, edit source, or change provider state.

## Domain Guidance

- Step 1: classify the issue (error, performance, or scheduled-job monitor). The category decides what context means: an error needs stack and breadcrumbs, a performance issue needs the trace, a monitor issue needs the missed check-in history.

## Output Contract

Produce:
- error issue evidence bundle
- hypothesis and root-cause analysis
- release and impact correlation
- bounded repair or instrumentation recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-issue`
- `read-only-events`
- `release-correlation`
- `competing-hypotheses`
- `cause-not-stack-frame`
- `no-provider-mutation`

## Hard Gates

- Issue investigation is read-only: it cannot resolve, mute, assign, comment, change grouping, edit source, or treat one stack trace as proven root cause.
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
- `defect-remediation`
- `production-llm-trace-root-cause-analysis`
- `production-trace-classification`
- `pull-request-comment-response`
- `root-cause-investigation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
