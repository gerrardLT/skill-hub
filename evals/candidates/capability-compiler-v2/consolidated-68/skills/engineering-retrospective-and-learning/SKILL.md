---
name: engineering-retrospective-and-learning
description: "Consolidated capability with 3 selectable modes: engineering-retrospective-and-improvement; feedback-and-continuous-learning-loop; reference-library-and-deferred-material. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [engineering-retrospective-and-improvement, feedback-and-continuous-learning-loop, reference-library-and-deferred-material]
---

# Engineering Retrospective And Learning

## Responsibility

Consolidated capability covering 3 related modes: Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.; Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.; Record source-linked reference or deferred material with applicability, freshness, supersession, and non-operational status without presenting it as current guidance.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `engineering-retrospective-and-improvement` | `read-only` | A sprint, release or project window has ended and the team wants an evidence-based blameless retrospective; Someone asks what repeated friction, debt or coordination problems the last period showed an | Coordinate an active production incident and mitigation decisions (-> incident-response-coordination); Persist an approv |
| `feedback-and-continuous-learning-loop` | `read-only` | A review cycle has new metrics, customer feedback, experiment results or alerts and someone must update what the team believes and what to do next; Hypotheses and priorities need re-rating after new e | Collect new customer interviews or proprietary feedback data (-> research-planning-and-governance); Persist an approved  |
| `reference-library-and-deferred-material` | `read-only` | Material that is historical, illustrative or deferred must be recorded with its source and freshness without becoming guidance; Someone asks to park an external framework or old claim with a revisit c | Integrate the source into a current candidate Skill after semantic review (-> workflow-skill-authoring); Store a verifie |

## Mode: `engineering-retrospective-and-improvement`

### engineering-retrospective-and-improvement

#### Responsibility

Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.

#### Trigger

Use when the request matches any of:
- A sprint, release or project window has ended and the team wants an evidence-based blameless retrospective
- Someone asks what repeated friction, debt or coordination problems the last period showed and what small experiments to run next

Do not use when:
- Coordinate an active production incident and mitigation decisions. Route to `incident-response-coordination`.
- Persist an approved learning locally after validation. Route to `local-learning-persistence`.
- Synthesize runtime signals and feedback into calibrated hypotheses. Route to `feedback-and-continuous-learning-loop`.

#### Required Inputs

- A time window, Git history, test health, plan state, delivery outcomes, and prior retrospectives.

#### Procedure

1. Freeze time window, teams, delivery and repository evidence, test and plan health, outcomes, incident records, prior actions, privacy, and participant boundaries.
2. Build an evidence-linked timeline and distinguish observed fact, interpretation, systemic contributor, local decision, and unknown without blame or hindsight rewriting.
3. Identify repeated strengths, friction, debt, coordination and tooling patterns, and compare prior improvement outcomes.
4. Propose the smallest measurable improvement experiments with owner, due date, success signal, review date, and stop condition; do not edit history, assign blame, or persist automatically.

#### Domain Guidance

- Default metric table when the user supplies none: commits and active days, net lines changed, PR size distribution, test pass rate and coverage, incident count, and context switches; show each as current value, previous value and delta.
- When a previous retrospective snapshot is supplied, compare against it and report which prior actions were completed, dropped (with the reason) or still open.
- Keep feedback blameless: attribute patterns to systems and process, and cite evidence (commit, metric, plan item) for every claim. Personal feedback is given only when the requester supplied individual evidence and asked for it.

#### Output Contract

Produce:
- blameless retrospective
- evidence-linked trend and debt register
- small improvement experiments
- owner, deadline, metric, and review map
- trend and debt register with columns: pattern, evidence refs, first seen, frequency, owner, status

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `blameless`
- `evidence-timeline`
- `fact-interpretation`
- `systemic-contributor`
- `owner-deadline`
- `measurable-improvement`

#### Hard Gates

- A retrospective cannot rewrite incident or delivery facts, assign personal blame, or create vague action items; every improvement needs evidence, owner, due date, measurable signal, and review condition.
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

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `incident-response-coordination`
- `feedback-and-continuous-learning-loop`
- `local-learning-persistence`
- `code-health-assessment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `feedback-and-continuous-learning-loop`

### feedback-and-continuous-learning-loop

#### Responsibility

Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.

#### Trigger

Use when the request matches any of:
- A review cycle has new metrics, customer feedback, experiment results or alerts and someone must update what the team believes and what to do next
- Hypotheses and priorities need re-rating after new evidence, with contrary evidence kept visible

Do not use when:
- Collect new customer interviews or proprietary feedback data. Route to `research-planning-and-governance`.
- Persist an approved learning record locally. Route to `local-learning-persistence`.
- Review an engineering period for delivery friction and improvement experiments. Route to `engineering-retrospective-and-improvement`.
- Validate that a dataset, metric or analysis is correct before anyone uses it. Route to `data-analysis-validation`.

#### Required Inputs

- Runtime metrics, customer feedback, experiment results, alerts, and residual assumptions.

#### Procedure

1. Freeze review window, authorized inputs, source identities, metrics, feedback, experiment and incident evidence, assumptions, prior decisions, data governance, and decision owners.
2. Normalize evidence strength and freshness while preserving dissent, minority evidence, causal uncertainty, missing data, and invalidated prior evidence.
3. Update hypothesis confidence, opportunity or risk priority, decision thresholds, and unresolved questions without treating correlation as learning.
4. Return learning record candidate, review cadence, next input and owner, and persistence handoff; do not collect data, persist, approve product changes, or configure systems.

#### Domain Guidance

- Confidence scale for every hypothesis: 1 untested assumption, 2 single anecdotal source, 3 multiple consistent sources, 4 measured in a controlled or pre-registered comparison, 5 replicated. Record the value before and after, and the specific evidence that moved it.
- Treat correlation, stale metrics and repeated opinion as no movement. State the evidence age and reject anything older than the stated review window.
- End with one next learning input, its owner and a review date.
- Quantify uncertainty of before/after rates when denominators exist. A point estimate clearing a threshold is not evidence its confidence interval clears that threshold. Reopen assumptions contradicted by evidence.

#### Output Contract

Produce:
- calibrated hypothesis and learning record candidate
- evidence and uncertainty map
- priority and review cadence
- next discovery, experiment, reliability, or persistence handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `evidence-freshness`
- `hypothesis-calibration`
- `contrary-evidence`
- `causal-uncertainty`
- `review-cadence`
- `next-learning-input`
- `no-persistence`

#### Hard Gates

- Continuous learning must link each confidence or priority change to current authorized evidence and preserve contrary evidence; repeated opinion, stale metrics, or correlation alone is not learning.
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

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `research-planning-and-governance`
- `local-learning-persistence`
- `engineering-retrospective-and-improvement`
- `metrics-system-and-observability`
- `data-analysis-validation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `reference-library-and-deferred-material`

### reference-library-and-deferred-material

#### Responsibility

Record source-linked reference or deferred material with applicability, freshness, supersession, and non-operational status without presenting it as current guidance.

#### Trigger

Use when the request matches any of:
- Material that is historical, illustrative or deferred must be recorded with its source and freshness without becoming guidance
- Someone asks to park an external framework or old claim with a revisit condition

Do not use when:
- Integrate the source into a current candidate Skill after semantic review. Route to `workflow-skill-authoring`.
- Store a verified active project decision as current context. Route to `project-context-and-learning-store`.

#### Required Inputs

- A source reference, historical claim, external framework, or material outside the active execution path.

#### Procedure

1. Freeze source identity, version or date, claim, intended audience, current task scope, reason for reference or deferral, owner, and revisit trigger.
2. Classify historical, illustrative, conditional, conflicting, superseded, deferred, or unsupported material without normalizing it into current policy.
3. Record exact provenance, applicability, freshness limit, conflicts, successor references, and non-operational warning.
4. Return a bounded reference record and revisit condition; do not execute source instructions or claim adoption.

#### Output Contract

Produce:
- reference or deferral record
- provenance and freshness limit
- conflict and supersession links
- owner and revisit condition

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `provenance`
- `freshness`
- `applicability`
- `non-operational`
- `supersession`
- `revisit-condition`

#### Hard Gates

- Reference retention never makes material current operational guidance; missing date, scope, provenance, applicability, or supersession status blocks adoption claims.
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
- `workflow-skill-authoring`
- `project-context-and-learning-store`
- `documentation-authoring`
- `context-intake-and-routing`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
