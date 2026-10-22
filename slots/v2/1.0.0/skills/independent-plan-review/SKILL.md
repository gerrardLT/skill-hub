---
name: independent-plan-review
description: Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions. Do not use for review only the user interface and design states in this plan or rewrite the plan to address the findings.
---

# Independent Plan Review

## Responsibility

Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.

## Trigger

Use when the requested outcome is: Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.

Do not use when:
- Review only the user interface and design states in this plan. Route to `design-plan-review`.
- Rewrite the plan to address the findings. Route to `implementation-planning-and-handoff`.

## Required Inputs

- A proposed plan, repository constraints, task boundaries, and verification requirements.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Freeze the reviewed plan version and its upstream artifacts.
2. Trace requirements to tasks, outputs, checks, owners, dependencies, risks, and rollback.
3. Identify missing, extra, contradictory, ambiguous, or untestable plan content with citations.
4. Classify severity, applicability, and whether a finding requires evidence or a human decision.
5. Return a verdict and amendments without editing or approving the plan.

## Output Contract

Produce:
- independent plan review
- traceability gaps
- finding register
- review verdict

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- The review must cite the frozen plan; generic best-practice advice without a demonstrated gap is not a finding.
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

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-plan-review`
- `developer-experience-plan-review`
- `executive-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
