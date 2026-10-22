---
name: strategic-choice-and-differentiation
description: Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans. Do not use for score a backlog of opportunities with a named prioritization formula or assess structural moat mechanisms in the business model.
---

# Strategic Choice And Differentiation

## Responsibility

Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.

## Trigger

Use when the requested outcome is: Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.

Do not use when:
- Score a backlog of opportunities with a named prioritization formula. Route to `opportunity-prioritization-and-frameworks`.
- Assess structural moat mechanisms in the business model. Route to `structural-power-and-moats`.

## Required Inputs

- A market position, baseline utility, cost structure, strategic strength, and candidate differentiation.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Freeze objective, decision owner, constraints, alternatives, evidence, and no-change option.
2. Evaluate customer value, fit, focus, differentiation, capabilities, economics, risk, reversibility, and second-order effects.
3. State mutually exclusive choices and the tradeoffs each accepts.
4. Identify evidence that would reverse the recommendation.
5. Return a recommendation, dissent, unknowns, and explicit human selection point.

## Output Contract

Produce:
- strategy choice matrix
- tradeoff register
- differentiation evidence
- human decision brief

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not disguise a bundle of incompatible choices as a strategy or convert recommendation strength into approval authority.
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
- `market-positioning-and-competitive-power`
- `structural-power-and-moats`
- `decision-and-outcome-roadmapping`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
