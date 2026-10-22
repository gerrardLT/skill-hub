---
name: design-plan-review
description: "Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions. Use when A plan or spec with user-facing screens needs a design review before implementation starts; Someone asks which UX states, flows, accessibility and responsive decisions the plan is missing. Do not use for: Create the actual responsive UI design and token system (-> design-context-and-direction-contract); Implement fixes to the interface after review (-> ui-remediation); Review the plan from the perspective owned by independent-plan-review (-> independent-plan-review); Review the plan from the perspective owned by developer-experience-plan-review (-> developer-experience-plan-review); Review the plan from the perspective owned by engineering-plan-review (-> engineering-plan-review); Review the plan from the perspective owned by executive-plan-review (-> executive-plan-review)."
---

# Design Plan Review

## Responsibility

Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions.

## Trigger

Use when the request matches any of:
- A plan or spec with user-facing screens needs a design review before implementation starts
- Someone asks which UX states, flows, accessibility and responsive decisions the plan is missing

Do not use when:
- Create the actual responsive UI design and token system. Route to `design-context-and-direction-contract`.
- Implement fixes to the interface after review. Route to `ui-remediation`.
- Review the plan from the perspective owned by independent-plan-review. Route to `independent-plan-review`.
- Review the plan from the perspective owned by developer-experience-plan-review. Route to `developer-experience-plan-review`.
- Review the plan from the perspective owned by engineering-plan-review. Route to `engineering-plan-review`.
- Review the plan from the perspective owned by executive-plan-review. Route to `executive-plan-review`.

## Required Inputs

- Plan, UX scope, existing design system, user flows, constraints, and decision owners.

## Procedure

1. Confirm that UI scope exists; otherwise return not-applicable with evidence.
2. Inspect users, journeys, information architecture, states, responsiveness, accessibility, content, motion, and rendered-review plan.
3. Classify gaps as evidence defect, implementation ambiguity, contextual taste choice, or non-blocking suggestion.
4. Cite the plan section for every finding and preserve contradictory constraints.
5. Return amendments and human taste decisions; never edit or approve the plan.

## Domain Guidance

- If mockups or rendered references exist, review against them. If only text exists, record 'text-only review' as a stated confidence limit.
- Rate each design area 0-10 (information architecture, states, flows, accessibility, responsiveness, content, motion) and state what the plan would need for a 10; that gap is the amendment.
- Separate missing decisions from taste choices and leave taste choices to the named human owner.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

## Output Contract

Produce:
- design plan review
- missing-state matrix
- taste-decision register
- amendment recommendations
- per-area 0-10 rating with the gap to 10

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Review evidence only; do not create design artifacts, mutate the plan, or treat contextual aesthetics as universal law.
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
- `developer-experience-plan-review`
- `design-context-and-direction-contract`
- `ui-remediation`
- `engineering-plan-review`
- `executive-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
