---
name: evidence-synthesis-and-opportunity-prioritization
description: "Synthesize heterogeneous evidence into bounded opportunity statements and compare them on explicit dimensions without hiding disagreement; ranking is left to the frameworks Skill or the human owner. Use when Mixed evidence (research notes, usage data, support tickets, competitor facts) must be reconciled into opportunity statements; Someone asks how strongly the evidence supports each candidate opportunity and where sources disagree. Do not use for: Apply RICE or ICE with an exact formula to an existing opportunity set (-> opportunity-prioritization-and-frameworks); Code raw interview observations into themes before opportunity framing (-> qualitative-evidence-synthesis)."
---

# Evidence Synthesis And Opportunity Prioritization

## Responsibility

Synthesize heterogeneous evidence into bounded opportunity statements and compare them on explicit dimensions without hiding disagreement; ranking is left to the frameworks Skill or the human owner.

## Trigger

Use when the request matches any of:
- Mixed evidence (research notes, usage data, support tickets, competitor facts) must be reconciled into opportunity statements
- Someone asks how strongly the evidence supports each candidate opportunity and where sources disagree

Do not use when:
- Apply RICE or ICE with an exact formula to an existing opportunity set. Route to `opportunity-prioritization-and-frameworks`.
- Code raw interview observations into themes before opportunity framing. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- Research notes, behavior data, support signals, competitive evidence, and candidate opportunities.

## Procedure

1. Normalize evidence identities, populations, time windows, authority, and confidence.
2. Triangulate corroboration and contradiction across qualitative and quantitative sources.
3. Frame opportunities as user/problem/outcome statements without embedding solutions.
4. Compare importance, frequency, severity, reach, confidence, and strategic relevance as explicit dimensions.
5. Return a recommendation, dissent, unknowns, and evidence needed to change the ranking.

## Domain Guidance

- Compare opportunities on importance, frequency, severity, reach, confidence and strategic relevance as separate columns. A requested composite ranking is calculated by the frameworks Skill through an explicit handoff; do not silently omit it.
- A deferred rename to evidence-synthesis-and-opportunity-framing is recorded; the id stays stable in this release.
- When the request also requires scores or ranking, deliver the synthesis and an explicit input-ready handoff to opportunity-prioritization-and-frameworks. Do not describe ranking as forbidden by the user or as awaiting approval merely to calculate it. A provisional evidence-led comparison may be delivered, labelled as a recommendation, not an approved decision.

## Output Contract

Produce:
- opportunity set
- evidence-to-opportunity matrix
- comparison on explicit dimensions
- dissent register
- ranking handoff with evidence matrix, candidate ids, missing inputs and named scoring owner

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- No opportunity rank may be justified by source count alone or by silently converting assumptions into evidence.
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
- `qualitative-evidence-synthesis`
- `data-analysis-validation`
- `opportunity-prioritization-and-frameworks`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
