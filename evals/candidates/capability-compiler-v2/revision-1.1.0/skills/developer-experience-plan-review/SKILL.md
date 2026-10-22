---
name: developer-experience-plan-review
description: "Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes. Use when A plan for an SDK, CLI, API, docs or tooling needs review for the developer onboarding and error experience; Someone wants measurable DX criteria (time to first success, recovery) added to a plan before it ships. Do not use for: Measure the live repository onboarding experience (-> developer-experience-assessment); Implement the setup and error-message fixes (-> defect-remediation); Review the plan from the perspective owned by independent-plan-review (-> independent-plan-review); Review the plan from the perspective owned by design-plan-review (-> design-plan-review); Review the plan from the perspective owned by engineering-plan-review (-> engineering-plan-review); Review the plan from the perspective owned by executive-plan-review (-> executive-plan-review)."
---

# Developer Experience Plan Review

## Responsibility

Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes.

## Trigger

Use when the request matches any of:
- A plan for an SDK, CLI, API, docs or tooling needs review for the developer onboarding and error experience
- Someone wants measurable DX criteria (time to first success, recovery) added to a plan before it ships

Do not use when:
- Measure the live repository onboarding experience. Route to `developer-experience-assessment`.
- Implement the setup and error-message fixes. Route to `defect-remediation`.
- Review the plan from the perspective owned by independent-plan-review. Route to `independent-plan-review`.
- Review the plan from the perspective owned by design-plan-review. Route to `design-plan-review`.
- Review the plan from the perspective owned by engineering-plan-review. Route to `engineering-plan-review`.
- Review the plan from the perspective owned by executive-plan-review. Route to `executive-plan-review`.

## Required Inputs

- Plan, approved product scope, current developer journey evidence, constraints, and decision owners.

## Procedure

1. Identify the target developer persona and its expectations before tracing any journey.
2. Establish whether the plan has a developer-facing surface; otherwise return not-applicable.
3. Trace setup, first success, common task, debugging, failure, and upgrade journeys.
4. Check API, CLI, SDK, docs, examples, compatibility, observability, and measurable DX criteria.
5. Classify assumptions and cite every plan gap.
6. Return amendments and unknowns without editing or approving the plan.

## Domain Guidance

- Step 1 is the target developer persona: who they are, what they already know, what they tolerate. Judge every journey against that persona, not a generic developer.
- Require measurable criteria: time to first success (target minutes), steps to hello world, time from error to fix, and upgrade effort between versions.
- Minute-2 abandonment test: name the first point where this persona would quit and what the plan does about it.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

## Output Contract

Produce:
- DX plan review
- developer journey gaps
- measurement recommendations
- plan amendments
- persona statement and measurable DX criteria (time to first success, failure recovery)

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not substitute general code quality comments for evidence about a developer-facing journey.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `independent-plan-review`
- `design-plan-review`
- `developer-experience-assessment`
- `defect-remediation`
- `engineering-plan-review`
- `executive-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
