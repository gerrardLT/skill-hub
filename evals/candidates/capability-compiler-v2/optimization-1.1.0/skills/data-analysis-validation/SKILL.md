---
name: data-analysis-validation
description: "Validate a dataset, metric definition, transformation, and analytical claim before decision use. Use when A metric, dataset or analytical claim must be checked for correctness before it supports a decision; Someone asks whether a result is trustworthy, including denominators, cohorts, leakage and confounds. Do not use for: Collect new customer data to fill these gaps (-> research-planning-and-governance); Make the product decision from the validated result (-> results-analysis-and-decision-readout); Interpret model evaluation results across experiments (-> evaluation-results-analysis)."
---

# Data Analysis Validation

## Responsibility

Validate a dataset, metric definition, transformation, and analytical claim before decision use.

## Trigger

Use when the request matches any of:
- A metric, dataset or analytical claim must be checked for correctness before it supports a decision
- Someone asks whether a result is trustworthy, including denominators, cohorts, leakage and confounds

Do not use when:
- Collect new customer data to fill these gaps. Route to `research-planning-and-governance`.
- Make the product decision from the validated result. Route to `results-analysis-and-decision-readout`.
- Interpret model evaluation results across experiments. Route to `evaluation-results-analysis`.

## Required Inputs

- Product metrics, feedback, queries, an experiment design, or experiment results.

## Procedure

1. Freeze the question, population, time window, metric formula, and expected decision use.
2. Audit source authority, consent, schema, missingness, duplication, leakage, and transformations.
3. Recompute key aggregates and compare denominators, cohorts, and uncertainty.
4. Test plausible alternative explanations and sensitivity to exclusions.
5. Return supported claims, unsupported claims, and data gaps.

## Domain Guidance

- Recompute the headline aggregate from the supplied data and show the arithmetic. State every denominator. Check sample ratio mismatch for experiments (compute the chi-square against the intended split and call a failed check a failed check with the statistic).
- Reproduction notes template: question, data sources with as-of date, definitions, method, result, caveats and known unknowns.
- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

## Output Contract

Produce:
- analysis validation report
- metric definition register
- reproduction notes
- claim evidence table
- recomputed aggregates with arithmetic and sample-ratio check

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- No analytical claim passes without reproducible inputs, a declared denominator, and preserved uncertainty.
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

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `results-analysis-and-decision-readout`
- `qualitative-evidence-synthesis`
- `research-planning-and-governance`
- `evaluation-results-analysis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
