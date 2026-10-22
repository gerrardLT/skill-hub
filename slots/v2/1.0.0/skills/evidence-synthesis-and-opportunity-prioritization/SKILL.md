---
name: evidence-synthesis-and-opportunity-prioritization
description: Synthesize heterogeneous evidence into bounded opportunity statements and a traceable priority recommendation without hiding disagreement. Do not use for apply rice or ice with an exact formula to an existing opportunity set or code raw interview observations into themes before opportunity framing.
---

# Evidence Synthesis And Opportunity Prioritization

## Responsibility

Synthesize heterogeneous evidence into bounded opportunity statements and a traceable priority recommendation without hiding disagreement.

## Trigger

Use when the requested outcome is: Synthesize heterogeneous evidence into bounded opportunity statements and a traceable priority recommendation without hiding disagreement.

Do not use when:
- Apply RICE or ICE with an exact formula to an existing opportunity set. Route to `opportunity-prioritization-and-frameworks`.
- Code raw interview observations into themes before opportunity framing. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- Research notes, behavior data, support signals, competitive evidence, and candidate opportunities.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Normalize evidence identities, populations, time windows, authority, and confidence.
2. Triangulate corroboration and contradiction across qualitative and quantitative sources.
3. Frame opportunities as user/problem/outcome statements without embedding solutions.
4. Compare importance, frequency, severity, reach, confidence, and strategic relevance as explicit dimensions.
5. Return a recommendation, dissent, unknowns, and evidence needed to change the ranking.

## Output Contract

Produce:
- opportunity set
- evidence-to-opportunity matrix
- priority recommendation
- dissent register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- No opportunity rank may be justified by source count alone or by silently converting assumptions into evidence.
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
- `qualitative-evidence-synthesis`
- `data-analysis-validation`
- `opportunity-prioritization-and-frameworks`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
