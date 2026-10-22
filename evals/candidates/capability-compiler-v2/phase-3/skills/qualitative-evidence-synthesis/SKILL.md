---
name: qualitative-evidence-synthesis
description: Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions. Do not use for turn the synthesized themes into prioritized opportunities or run the interviews that produce the raw evidence.
---

# Qualitative Evidence Synthesis

## Responsibility

Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.

## Trigger

Use when the requested outcome is: Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.

Do not use when:
- Turn the synthesized themes into prioritized opportunities. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Run the interviews that produce the raw evidence. Route to `customer-interview-execution`.

## Required Inputs

- Interview notes, direct quotes, affinity material, journey evidence, and known bias.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify consent, minimization, redaction, retention, external-transfer, corpus identity, and analysis question.
2. Separate quote, observation, analyst code, interpretation, and unsupported inference.
3. Code records consistently and retain source IDs.
4. Synthesize themes with prevalence context, counterexamples, contradictions, and saturation limits.
5. Return findings and gaps without making priority or product decisions.

## Output Contract

Produce:
- coded evidence table
- theme map
- counterexample register
- confidence and saturation notes

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not expose raw participant data, count quotes as population prevalence, or erase minority and contradictory evidence.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `customer-interview-execution`
- `evidence-synthesis-and-opportunity-prioritization`
- `data-analysis-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
