---
name: research-planning-and-governance
description: Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries. Do not use for conduct the already approved customer interviews or synthesize the completed qualitative corpus.
---

# Research Planning And Governance

## Responsibility

Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.

## Trigger

Use when the requested outcome is: Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.

Do not use when:
- Conduct the already approved customer interviews. Route to `customer-interview-execution`.
- Synthesize the completed qualitative corpus. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- A research question, target population, access constraints, ethical boundary, and timebox.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. State the decision, research question, prior evidence, unknown, owner, and stopping rule.
2. Select method and sampling logic appropriate to the claim; name bias and representativeness limits.
3. Define authorization, consent, minimization, redaction, recording, retention, access, external-transfer, and deletion policy.
4. Specify protocol, evidence schema, quality checks, analysis plan, and recruitment boundary.
5. Return the plan and blocked governance inputs; do not recruit or collect data.

## Output Contract

Produce:
- research plan
- sampling and method rationale
- data-governance contract
- analysis and stopping plan

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- No participant contact, collection, recording, external Judge use, or proprietary-data transfer may begin from an incomplete governance contract.
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
- `data-analysis-validation`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
