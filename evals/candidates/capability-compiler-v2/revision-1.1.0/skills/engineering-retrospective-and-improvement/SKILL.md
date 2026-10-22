---
name: engineering-retrospective-and-improvement
description: "Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems. Use when A sprint, release or project window has ended and the team wants an evidence-based blameless retrospective; Someone asks what repeated friction, debt or coordination problems the last period showed and what small experiments to run next. Do not use for: Coordinate an active production incident and mitigation decisions (-> incident-response-coordination); Persist an approved learning locally after validation (-> local-learning-persistence); Synthesize runtime signals and feedback into calibrated hypotheses (-> feedback-and-continuous-learning-loop)."
---

# Engineering Retrospective And Improvement

## Responsibility

Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.

## Trigger

Use when the request matches any of:
- A sprint, release or project window has ended and the team wants an evidence-based blameless retrospective
- Someone asks what repeated friction, debt or coordination problems the last period showed and what small experiments to run next

Do not use when:
- Coordinate an active production incident and mitigation decisions. Route to `incident-response-coordination`.
- Persist an approved learning locally after validation. Route to `local-learning-persistence`.
- Synthesize runtime signals and feedback into calibrated hypotheses. Route to `feedback-and-continuous-learning-loop`.

## Required Inputs

- A time window, Git history, test health, plan state, delivery outcomes, and prior retrospectives.

## Procedure

1. Freeze time window, teams, delivery and repository evidence, test and plan health, outcomes, incident records, prior actions, privacy, and participant boundaries.
2. Build an evidence-linked timeline and distinguish observed fact, interpretation, systemic contributor, local decision, and unknown without blame or hindsight rewriting.
3. Identify repeated strengths, friction, debt, coordination and tooling patterns, and compare prior improvement outcomes.
4. Propose the smallest measurable improvement experiments with owner, due date, success signal, review date, and stop condition; do not edit history, assign blame, or persist automatically.

## Domain Guidance

- Default metric table when the user supplies none: commits and active days, net lines changed, PR size distribution, test pass rate and coverage, incident count, and context switches; show each as current value, previous value and delta.
- When a previous retrospective snapshot is supplied, compare against it and report which prior actions were completed, dropped (with the reason) or still open.
- Keep feedback blameless: attribute patterns to systems and process, and cite evidence (commit, metric, plan item) for every claim. Personal feedback is given only when the requester supplied individual evidence and asked for it.

## Output Contract

Produce:
- blameless retrospective
- evidence-linked trend and debt register
- small improvement experiments
- owner, deadline, metric, and review map
- trend and debt register with columns: pattern, evidence refs, first seen, frequency, owner, status

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `blameless`
- `evidence-timeline`
- `fact-interpretation`
- `systemic-contributor`
- `owner-deadline`
- `measurable-improvement`

## Hard Gates

- A retrospective cannot rewrite incident or delivery facts, assign personal blame, or create vague action items; every improvement needs evidence, owner, due date, measurable signal, and review condition.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `incident-response-coordination`
- `feedback-and-continuous-learning-loop`
- `local-learning-persistence`
- `code-health-assessment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
