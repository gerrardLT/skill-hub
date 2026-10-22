---
name: developer-experience-plan-review
description: Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes. Do not use for measure the live repository onboarding experience or implement the setup and error-message fixes.
---

# Developer Experience Plan Review

## Responsibility

Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes.

## Trigger

Use when the requested outcome is: Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes.

Do not use when:
- Measure the live repository onboarding experience. Route to `developer-experience-assessment`.
- Implement the setup and error-message fixes. Route to `defect-remediation`.

## Required Inputs

- Plan, approved product scope, current developer journey evidence, constraints, and decision owners.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Establish whether the plan has a developer-facing surface; otherwise return not-applicable.
2. Trace setup, first success, common task, debugging, failure, and upgrade journeys.
3. Check API, CLI, SDK, docs, examples, compatibility, observability, and measurable DX criteria.
4. Classify assumptions and cite every plan gap.
5. Return amendments and unknowns without editing or approving the plan.

## Output Contract

Produce:
- DX plan review
- developer journey gaps
- measurement recommendations
- plan amendments

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not substitute general code quality comments for evidence about a developer-facing journey.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `independent-plan-review`
- `design-plan-review`
- `developer-experience-assessment`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
