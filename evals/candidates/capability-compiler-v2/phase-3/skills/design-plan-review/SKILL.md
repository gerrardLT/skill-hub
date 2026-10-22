---
name: design-plan-review
description: Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions. Do not use for create the actual responsive ui design and token system or implement fixes to the interface after review.
---

# Design Plan Review

## Responsibility

Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions.

## Trigger

Use when the requested outcome is: Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions.

Do not use when:
- Create the actual responsive UI design and token system. Route to `design-context-and-direction-contract`.
- Implement fixes to the interface after review. Route to `ui-remediation`.

## Required Inputs

- Plan, UX scope, existing design system, user flows, constraints, and decision owners.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Confirm that UI scope exists; otherwise return not-applicable with evidence.
2. Inspect users, journeys, information architecture, states, responsiveness, accessibility, content, motion, and rendered-review plan.
3. Classify gaps as evidence defect, implementation ambiguity, contextual taste choice, or non-blocking suggestion.
4. Cite the plan section for every finding and preserve contradictory constraints.
5. Return amendments and human taste decisions; never edit or approve the plan.

## Output Contract

Produce:
- design plan review
- missing-state matrix
- taste-decision register
- amendment recommendations

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Review evidence only; do not create design artifacts, mutate the plan, or treat contextual aesthetics as universal law.
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
- `developer-experience-plan-review`
- `design-context-and-direction-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
