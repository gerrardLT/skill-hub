---
name: ai-organizational-adoption-and-leadership
description: Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems. Do not use for decide the ai capability, model, data, autonomy, and safety architecture or configure production ai observability for the deployed system.
---

# Ai Organizational Adoption And Leadership

## Responsibility

Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.

## Trigger

Use when the requested outcome is: Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.

Do not use when:
- Decide the AI capability, model, data, autonomy, and safety architecture. Route to `ai-capability-architecture-and-autonomy`.
- Configure production AI observability for the deployed system. Route to `ai-observability-configuration`.

## Required Inputs

- An AI initiative, organizational constraints, leadership questions, pilot candidates, and value hypotheses.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze initiative and architecture status, user and business value hypotheses, teams, sponsors, current workflows, skills, governance, labor and change impacts, data boundaries, budget, risks, and decision owners.
2. Select the smallest reversible pilot and define participants, enablement, process changes, support, communication, access, safeguards, and non-adoption option.
3. Define measurable user, workflow, quality, cost, safety, trust, and organizational outcomes with baselines, review cadence, expansion and stop criteria.
4. Return adoption plan, leadership options, ownership model, and unresolved risks for human approval; do not grant access, configure systems, enroll users, or expand autonomy.

## Output Contract

Produce:
- AI adoption and pilot plan
- leadership decision material
- value and safety measurement contract
- ownership, enablement, and stop criteria

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- `ai-capability-architecture-and-autonomy`
- `ai-agent-autonomy-and-human-control`
- `ai-observability-configuration`
- `feedback-and-continuous-learning-loop`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
