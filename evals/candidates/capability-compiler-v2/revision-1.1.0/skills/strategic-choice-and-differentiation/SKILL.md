---
name: strategic-choice-and-differentiation
description: "Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans. Use when Several mutually exclusive strategic options must be compared on value, fit, tradeoffs and reversibility; Someone asks what differentiates a position and what evidence would reverse the recommendation. Do not use for: Score a backlog of opportunities with a named prioritization formula (-> opportunity-prioritization-and-frameworks); Assess structural moat mechanisms in the business model (-> structural-power-and-moats)."
---

# Strategic Choice And Differentiation

## Responsibility

Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.

## Trigger

Use when the request matches any of:
- Several mutually exclusive strategic options must be compared on value, fit, tradeoffs and reversibility
- Someone asks what differentiates a position and what evidence would reverse the recommendation

Do not use when:
- Score a backlog of opportunities with a named prioritization formula. Route to `opportunity-prioritization-and-frameworks`.
- Assess structural moat mechanisms in the business model. Route to `structural-power-and-moats`.

## Required Inputs

- A market position, baseline utility, cost structure, strategic strength, and candidate differentiation.

## Procedure

1. Freeze objective, decision owner, constraints, alternatives, evidence, and no-change option.
2. Evaluate customer value, fit, focus, differentiation, capabilities, economics, risk, reversibility, and second-order effects.
3. State mutually exclusive choices and the tradeoffs each accepts.
4. Identify evidence that would reverse the recommendation.
5. Return a recommendation, dissent, unknowns, and explicit human selection point.

## Domain Guidance

- For networked products use the niche-first lens: the early audience often looks like a weird niche and the product like a toy; test whether the niche can compound before judging the market as small.

## Output Contract

Produce:
- strategy choice matrix
- tradeoff register
- differentiation evidence
- human decision brief

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not disguise a bundle of incompatible choices as a strategy or convert recommendation strength into approval authority.
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
- `market-positioning-and-competitive-power`
- `structural-power-and-moats`
- `decision-and-outcome-roadmapping`
- `opportunity-prioritization-and-frameworks`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
