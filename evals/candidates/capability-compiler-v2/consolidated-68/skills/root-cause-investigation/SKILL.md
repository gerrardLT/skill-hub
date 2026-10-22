---
name: root-cause-investigation
description: "Consolidated capability with 2 selectable modes: error-monitoring-issue-investigation; root-cause-investigation. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [error-monitoring-issue-investigation, root-cause-investigation]
---

# Root Cause Investigation

## Responsibility

Consolidated capability covering 2 related modes: Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation.; Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `error-monitoring-issue-investigation` | `external-read` | One error-monitoring issue needs its events, releases and stack traces turned into an evidence-bounded root-cause hypothesis; Someone asks what caused an alert or a regression in production errors, re | Apply the confirmed source repair (-> defect-remediation); Respond to a pull-request comment about the repair (-> pull-r |
| `root-cause-investigation` | `workspace-write-local-exec` | A bug, failing test, incident or regression needs its real cause found and demonstrated before anyone patches it; Someone proposes a quick fix for a symptom and the cause has not been established. | Apply the smallest patch for the already-confirmed root cause (-> defect-remediation); Run an independent broad code-qua |

## Mode: `error-monitoring-issue-investigation`

### error-monitoring-issue-investigation

#### Responsibility

Investigate one error-monitoring issue from read-only event evidence to an evidence-bounded root-cause hypothesis and repair recommendation without provider or source mutation.

#### Trigger

Use when the request matches any of:
- One error-monitoring issue needs its events, releases and stack traces turned into an evidence-bounded root-cause hypothesis
- Someone asks what caused an alert or a regression in production errors, read-only

Do not use when:
- Apply the confirmed source repair. Route to `defect-remediation`.
- Respond to a pull-request comment about the repair. Route to `pull-request-comment-response`.
- Reproduce and trace a defect locally from a failing test or incident. Route to `root-cause-investigation`.

#### Required Inputs

- Issue identity, event context, release, environment, source access, and authority boundary.

#### Procedure

1. Classify the issue as error, performance or scheduled-job monitor before pulling context.
2. Freeze provider, project, issue ID, time range, environment, release, data policy, read-only authority, source mapping, and investigation question.
3. Inspect current event groups, samples, stack traces, breadcrumbs, tags, frequency, users or tenants, release correlation, first and last seen, and linked traces under minimization.
4. Test competing hypotheses against source and runtime evidence and distinguish grouping artifact, symptom, trigger, and root cause.
5. Return evidence, confidence, affected surface, and bounded repair or further-instrumentation recommendation; do not comment, assign, resolve, ignore, mute, edit source, or change provider state.

#### Domain Guidance

- Step 1: classify the issue (error, performance, or scheduled-job monitor). The category decides what context means: an error needs stack and breadcrumbs, a performance issue needs the trace, a monitor issue needs the missed check-in history.

#### Output Contract

Produce:
- error issue evidence bundle
- hypothesis and root-cause analysis
- release and impact correlation
- bounded repair or instrumentation recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-issue`
- `read-only-events`
- `release-correlation`
- `competing-hypotheses`
- `cause-not-stack-frame`
- `no-provider-mutation`

#### Hard Gates

- Issue investigation is read-only: it cannot resolve, mute, assign, comment, change grouping, edit source, or treat one stack trace as proven root cause.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `defect-remediation`
- `production-llm-trace-root-cause-analysis`
- `production-trace-classification`
- `pull-request-comment-response`
- `root-cause-investigation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `root-cause-investigation`

### root-cause-investigation

#### Responsibility

Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source.

#### Trigger

Use when the request matches any of:
- A bug, failing test, incident or regression needs its real cause found and demonstrated before anyone patches it
- Someone proposes a quick fix for a symptom and the cause has not been established

Do not use when:
- Apply the smallest patch for the already-confirmed root cause. Route to `defect-remediation`.
- Run an independent broad code-quality review unrelated to one observed defect. Route to `independent-code-review`.

#### Required Inputs

- A test failure, production incident, unexpected behavior, build issue, or performance problem.

#### Procedure

1. Freeze the symptom, target identity, environment, reproduction, expected behavior, scope, permitted commands, and existing evidence.
2. Reproduce with the smallest controlled case and record command, exit, duration, output, state, and frequency without changing source.
3. Trace callers, data and control flow, boundaries, recent changes, and sibling paths; test competing hypotheses one variable at a time.
4. Locate the first violated invariant or common cause, distinguish cause from trigger and symptom, and return evidence, affected surface, and a bounded remediation handoff.

#### Domain Guidance

- Red flags that mean stop and investigate: 'quick fix now, investigate later', 'just try changing X', 'it's probably X', 'I don't fully understand but this might work', and listing fixes before any investigation.
- Trace backward from the symptom through each caller until you find the original bad value or first violated invariant; the last stack frame is usually a symptom, not the cause.
- Test one hypothesis at a time with a change in exactly one variable.

#### Output Contract

Produce:
- minimal reproduction
- hypothesis and experiment ledger
- root-cause evidence chain
- affected-surface and remediation handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `reproduction`
- `callers`
- `competing-hypotheses`
- `first-divergent-invariant`
- `cause-not-symptom`
- `no-source-edit`

#### Hard Gates

- Investigation cannot declare root cause from correlation, the last stack frame, or one patched symptom; it needs a reproducible causal chain and sibling-path analysis.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `defect-remediation`
- `resilience-and-determinism`
- `independent-code-review`
- `change-scope-freeze`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
