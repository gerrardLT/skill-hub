---
name: executive-plan-review
description: "Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership. Use when A plan needs a leadership-level challenge of scope, leverage, user value and one-way decisions before commitment; Someone asks whether the plan is too small, too large or hides an irreversible bet. Do not use for: Choose the company's strategy and approve the plan (-> strategic-choice-and-differentiation); Review the plan's implementation interfaces and failure modes (-> engineering-plan-review); Review the plan from the perspective owned by independent-plan-review (-> independent-plan-review); Review the plan from the perspective owned by design-plan-review (-> design-plan-review); Review the plan from the perspective owned by developer-experience-plan-review (-> developer-experience-plan-review)."
---

# Executive Plan Review

## Responsibility

Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.

## Trigger

Use when the request matches any of:
- A plan needs a leadership-level challenge of scope, leverage, user value and one-way decisions before commitment
- Someone asks whether the plan is too small, too large or hides an irreversible bet

Do not use when:
- Choose the company's strategy and approve the plan. Route to `strategic-choice-and-differentiation`.
- Review the plan's implementation interfaces and failure modes. Route to `engineering-plan-review`.
- Review the plan from the perspective owned by independent-plan-review. Route to `independent-plan-review`.
- Review the plan from the perspective owned by design-plan-review. Route to `design-plan-review`.
- Review the plan from the perspective owned by developer-experience-plan-review. Route to `developer-experience-plan-review`.

## Required Inputs

- Plan, evidence, product context, constraints, and decision owners.

## Procedure

1. State the review mode (expansion, selective expansion, hold scope or reduction) and evaluate every section, writing 'no issues found' where that is the result.
2. Read the plan, approved strategy, evidence, constraints, and decision authority.
3. Test problem importance, user value, leverage, alternatives, scope, reversibility, and downside.
4. Separate fact gaps, strategic disagreements, taste choices, and human-only decisions.
5. State proposed cuts, expansions, or options with evidence and tradeoffs.
6. Return challenged assumptions and required human decisions without persisting or approving a plan.

## Domain Guidance

- Choose one review mode first and state it: scope expansion (dream bigger), selective expansion (hold the base, cherry-pick additions), hold scope (make it bulletproof), or scope reduction (cut to the core).
- Evaluate every review section without skipping; when a section has no findings write 'no issues found' explicitly rather than omitting it.
- Ambitious options stay options until a human selects them; none becomes accepted scope through this review.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

## Output Contract

Produce:
- executive plan review
- scope challenge
- one-way-door register
- human decision queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not turn an ambitious option into accepted scope or write a CEO plan without explicit human selection and a separate persistence capability.
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
- `engineering-plan-review`
- `plan-review-decision-synthesis`
- `strategic-choice-and-differentiation`
- `design-plan-review`
- `developer-experience-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
