---
name: ai-organizational-adoption-and-leadership
description: "Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems. Use when Leadership asks how to roll out an AI initiative: which team pilots first, who sponsors it, how value and risk are measured; An AI pilot needs enablement, ownership, stop criteria and an expansion decision before any access is granted. Do not use for: Decide the AI capability, model, data, autonomy, and safety architecture (-> ai-model-and-data-architecture); Configure production AI observability for the deployed system (-> ai-observability-configuration)."
---

# AI Organizational Adoption And Leadership

## Responsibility

Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.

## Trigger

Use when the request matches any of:
- Leadership asks how to roll out an AI initiative: which team pilots first, who sponsors it, how value and risk are measured
- An AI pilot needs enablement, ownership, stop criteria and an expansion decision before any access is granted

Do not use when:
- Decide the AI capability, model, data, autonomy, and safety architecture. Route to `ai-model-and-data-architecture`.
- Configure production AI observability for the deployed system. Route to `ai-observability-configuration`.

## Required Inputs

- An AI initiative, organizational constraints, leadership questions, pilot candidates, and value hypotheses.

## Procedure

1. Freeze initiative and architecture status, user and business value hypotheses, teams, sponsors, current workflows, skills, governance, labor and change impacts, data boundaries, budget, risks, and decision owners.
2. Score each candidate pilot workflow on repeatability and reversibility and state why the chosen one is the smallest test of differentiated value.
3. Select the smallest reversible pilot and define participants, enablement, process changes, support, communication, access, safeguards, and non-adoption option.
4. Define measurable user, workflow, quality, cost, safety, trust, and organizational outcomes with baselines, review cadence, expansion and stop criteria.
5. Return adoption plan, leadership options, ownership model, and unresolved risks for human approval; do not grant access, configure systems, enroll users, or expand autonomy.

## Domain Guidance

- Pilot selection: score each candidate workflow on repeatability (same steps, same inputs, frequent) and reversibility; prefer repeatable business processes over open-ended knowledge work.
- Pair top-down sponsorship with bottom-up early adopters: name a small tiger team of technically adjacent evangelists who can show measurable return quickly.
- Plan a diverge phase (teams explore freely under stated limits) followed by a dated converge decision on a few high-conviction bets; audit each AI feature against the core objective so adoption does not add product bloat.

## Output Contract

Produce:
- AI adoption and pilot plan
- leadership decision material
- value and safety measurement contract
- ownership, enablement, and stop criteria

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `reversible-pilot`
- `sponsor-owner`
- `workflow-impact`
- `capability-building`
- `value-measures`
- `safety-governance`
- `stop-criteria`

## Hard Gates

- AI adoption cannot pass on enthusiasm or tool availability: it needs a reversible pilot, named sponsor and owners, workflow and labor impacts, measurable value and safety outcomes, governance, and stop criteria.
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
- `ai-model-and-data-architecture`
- `ai-agent-autonomy-and-human-control`
- `ai-observability-configuration`
- `feedback-and-continuous-learning-loop`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
