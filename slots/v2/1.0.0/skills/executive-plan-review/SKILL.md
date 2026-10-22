---
name: executive-plan-review
description: Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership. Do not use for choose the company's strategy and approve the plan or review the plan's implementation interfaces and failure modes.
---

# Executive Plan Review

## Responsibility

Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.

## Trigger

Use when the requested outcome is: Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.

Do not use when:
- Choose the company's strategy and approve the plan. Route to `strategic-choice-and-differentiation`.
- Review the plan's implementation interfaces and failure modes. Route to `engineering-plan-review`.

## Required Inputs

- Plan, evidence, product context, constraints, and decision owners.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Read the plan, approved strategy, evidence, constraints, and decision authority.
2. Test problem importance, user value, leverage, alternatives, scope, reversibility, and downside.
3. Separate fact gaps, strategic disagreements, taste choices, and human-only decisions.
4. State proposed cuts, expansions, or options with evidence and tradeoffs.
5. Return challenged assumptions and required human decisions without persisting or approving a plan.

## Output Contract

Produce:
- executive plan review
- scope challenge
- one-way-door register
- human decision queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not turn an ambitious option into accepted scope or write a CEO plan without explicit human selection and a separate persistence capability.
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
- `engineering-plan-review`
- `plan-review-decision-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
