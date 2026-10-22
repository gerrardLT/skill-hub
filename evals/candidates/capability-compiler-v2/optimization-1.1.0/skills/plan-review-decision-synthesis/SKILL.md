---
name: plan-review-decision-synthesis
description: "Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews. Use when Several independent plan reviews exist and someone must merge them into one decision view without hiding disagreement; A plan needs its open issues sorted into mechanical fixes, taste choices and one-way doors for a human to decide. Do not use for: Perform the independent design review that is missing (-> design-plan-review); Approve and edit the plan using the synthesized recommendations (-> implementation-planning-and-handoff)."
---

# Plan Review Decision Synthesis

## Responsibility

Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.

## Trigger

Use when the request matches any of:
- Several independent plan reviews exist and someone must merge them into one decision view without hiding disagreement
- A plan needs its open issues sorted into mechanical fixes, taste choices and one-way doors for a human to decide

Do not use when:
- Perform the independent design review that is missing. Route to `design-plan-review`.
- Approve and edit the plan using the synthesized recommendations. Route to `implementation-planning-and-handoff`.

## Required Inputs

- Independent review findings, plan version, decision policy, authority, and unresolved questions.

## Procedure

1. Verify review identities, frozen plan version, citations, applicability, and independence.
2. Deduplicate findings by underlying decision without erasing distinct rationale.
3. Classify evidence defect, reversible choice, taste decision, one-way door, conflict, and non-applicable item.
4. Preserve agreement, dissent, dependencies, and proposed amendments.
5. Return an audit trail and explicit human decisions; do not approve or write the plan.

## Domain Guidance

- Mechanical items (one clearly right answer) carry a recommended resolution with the principle cited and stay out of the human queue. Taste choices and one-way doors go to the human approval queue with the owner named.
- Decision principles for mechanical items: choose completeness, fix what is inside the blast radius, prefer the simpler option when two fix the same thing, and never resolve a conflict between reviewers silently.

## Output Contract

Produce:
- review decision matrix
- dissent register
- proposed amendments
- human approval queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Synthesis cannot manufacture reviewer consensus, downgrade a blocking dissent, or convert recommendations into approved scope.
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
- `executive-plan-review`
- `design-plan-review`
- `developer-experience-plan-review`
- `implementation-planning-and-handoff`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
