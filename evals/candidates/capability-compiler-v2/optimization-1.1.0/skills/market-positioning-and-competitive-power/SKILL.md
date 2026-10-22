---
name: market-positioning-and-competitive-power
description: "Evaluate a proposed market position against customer evidence, alternatives, category context, and sources of bargaining or competitive power. Use when A proposed market position needs testing against customer evidence, alternatives and competitive power; Someone asks whether a positioning claim is credible and which claims competitors can copy quickly. Do not use for: Assess whether the business has a durable structural moat (-> structural-power-and-moats); Write the final approved marketing copy (-> documentation-authoring)."
---

# Market Positioning And Competitive Power

## Responsibility

Evaluate a proposed market position against customer evidence, alternatives, category context, and sources of bargaining or competitive power.

## Trigger

Use when the request matches any of:
- A proposed market position needs testing against customer evidence, alternatives and competitive power
- Someone asks whether a positioning claim is credible and which claims competitors can copy quickly

Do not use when:
- Assess whether the business has a durable structural moat. Route to `structural-power-and-moats`.
- Write the final approved marketing copy. Route to `documentation-authoring`.

## Required Inputs

- Market questions, customer alternatives, competitive evidence, and business constraints.

## Procedure

1. Define target segment, job, alternatives, promised value, proof, category, and comparison frame.
2. Test claim relevance and credibility against customer and competitor evidence.
3. Map who gains or loses power across buyer, supplier, complement, channel, and rival relationships.
4. Identify unsupported superiority claims and positions competitors can copy quickly.
5. Return position options, proof gaps, risks, and a human decision request.

## Domain Guidance

- The comparison frame includes the internal alternative and doing nothing (spending the same effort elsewhere), not only rival products.

## Output Contract

Produce:
- positioning evidence map
- competitive power analysis
- claim-proof register
- position options

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not convert an attractive phrase into a validated position or imply market power without evidence about alternatives and bargaining structure.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `structural-power-and-moats`
- `strategic-choice-and-differentiation`
- `competitive-case-library`
- `documentation-authoring`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
