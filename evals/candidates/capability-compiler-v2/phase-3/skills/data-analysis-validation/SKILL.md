---
name: data-analysis-validation
description: Validate a dataset, metric definition, transformation, and analytical claim before decision use. Do not use for collect new customer data to fill these gaps or make the product decision from the validated result.
---

# Data Analysis Validation

## Responsibility

Validate a dataset, metric definition, transformation, and analytical claim before decision use.

## Trigger

Use when the requested outcome is: Validate a dataset, metric definition, transformation, and analytical claim before decision use.

Do not use when:
- Collect new customer data to fill these gaps. Route to `research-planning-and-governance`.
- Make the product decision from the validated result. Route to `results-analysis-and-decision-readout`.

## Required Inputs

- Product metrics, feedback, queries, an experiment design, or experiment results.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Freeze the question, population, time window, metric formula, and expected decision use.
2. Audit source authority, consent, schema, missingness, duplication, leakage, and transformations.
3. Recompute key aggregates and compare denominators, cohorts, and uncertainty.
4. Test plausible alternative explanations and sensitivity to exclusions.
5. Return supported claims, unsupported claims, and data gaps.

## Output Contract

Produce:
- analysis validation report
- metric definition register
- reproduction notes
- claim evidence table

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- No analytical claim passes without reproducible inputs, a declared denominator, and preserved uncertainty.
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
- `results-analysis-and-decision-readout`
- `qualitative-evidence-synthesis`
- `research-planning-and-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
