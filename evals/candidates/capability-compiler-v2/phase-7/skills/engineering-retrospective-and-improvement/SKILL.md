---
name: engineering-retrospective-and-improvement
description: Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems. Do not use for coordinate an active production incident and mitigation decisions or persist an approved learning locally after validation.
---

# Engineering Retrospective And Improvement

## Responsibility

Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.

## Trigger

Use when the requested outcome is: Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.

Do not use when:
- Coordinate an active production incident and mitigation decisions. Route to `incident-response-coordination`.
- Persist an approved learning locally after validation. Route to `local-learning-persistence`.

## Required Inputs

- A time window, Git history, test health, plan state, delivery outcomes, and prior retrospectives.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze time window, teams, delivery and repository evidence, test and plan health, outcomes, incident records, prior actions, privacy, and participant boundaries.
2. Build an evidence-linked timeline and distinguish observed fact, interpretation, systemic contributor, local decision, and unknown without blame or hindsight rewriting.
3. Identify repeated strengths, friction, debt, coordination and tooling patterns, and compare prior improvement outcomes.
4. Propose the smallest measurable improvement experiments with owner, due date, success signal, review date, and stop condition; do not edit history, assign blame, or persist automatically.

## Output Contract

Produce:
- blameless retrospective
- evidence-linked trend and debt register
- small improvement experiments
- owner, deadline, metric, and review map

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `blameless`
- `evidence-timeline`
- `fact-interpretation`
- `systemic-contributor`
- `owner-deadline`
- `measurable-improvement`

## Hard Gates

- A retrospective cannot rewrite incident or delivery facts, assign personal blame, or create vague action items; every improvement needs evidence, owner, due date, measurable signal, and review condition.
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
- `incident-response-coordination`
- `feedback-and-continuous-learning-loop`
- `local-learning-persistence`
- `code-health-assessment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
