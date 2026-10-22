---
name: structural-power-and-moats
description: Assess durable structural advantage mechanisms, prerequisites, counterevidence, decay, and imitation risk without treating current performance as a moat. Do not use for choose the company's final strategic direction or craft the customer-facing market position.
---

# Structural Power And Moats

## Responsibility

Assess durable structural advantage mechanisms, prerequisites, counterevidence, decay, and imitation risk without treating current performance as a moat.

## Trigger

Use when the requested outcome is: Assess durable structural advantage mechanisms, prerequisites, counterevidence, decay, and imitation risk without treating current performance as a moat.

Do not use when:
- Choose the company's final strategic direction. Route to `strategic-choice-and-differentiation`.
- Craft the customer-facing market position. Route to `market-positioning-and-competitive-power`.

## Required Inputs

- A proposed advantage, customer evidence, cost structure, workflow, and imitation scenario.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Define the claimed advantage, relevant market, customer value, alternative, and evidence window.
2. Test scale economies, network economies, counter-positioning, switching costs, branding, cornered resource, and process power only where applicable.
3. For each candidate, state mechanism, prerequisite, reinforcement loop, imitation barrier, counterevidence, and decay risk.
4. Separate current strength, temporary lead, execution quality, and structural power.
5. Return supported, unsupported, and testable moat hypotheses.

## Output Contract

Produce:
- structural power assessment
- mechanism evidence map
- counterevidence and decay register
- moat hypothesis backlog

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Growth, market share, brand awareness, proprietary data, or technical complexity alone must not be labeled a moat without a durable causal mechanism.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

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
- `strategic-choice-and-differentiation`
- `market-positioning-and-competitive-power`
- `competitive-response-and-monitoring`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
