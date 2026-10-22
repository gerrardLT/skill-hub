---
name: results-analysis-and-decision-readout
description: Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision. Do not use for design the experiment and its success criteria before execution or commit the roadmap to the recommended decision.
---

# Results Analysis And Decision Readout

## Responsibility

Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.

## Trigger

Use when the requested outcome is: Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.

Do not use when:
- Design the experiment and its success criteria before execution. Route to `solution-hypothesis-and-experiment-design`.
- Commit the roadmap to the recommended decision. Route to `decision-and-outcome-roadmapping`.

## Required Inputs

- Experiment or research data, metrics, baselines, bias checks, and decision criteria.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Freeze experiment identity, preregistered hypothesis, metrics, thresholds, exclusions, and analysis population.
2. Validate result provenance and note protocol deviations or missing data.
3. Compare outcomes to thresholds, uncertainty, segments, counter-metrics, and plausible alternatives.
4. Separate observed result, interpretation, recommendation, and unknown.
5. Return GO/PIVOT/KILL or continue recommendation for the named human decision owner.

## Output Contract

Produce:
- results readout
- threshold comparison
- failure-slice analysis
- human decision recommendation

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- A recommendation may not be presented as a product decision, and post-hoc thresholds must be labeled rather than disguised as preregistered criteria.
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
- `solution-hypothesis-and-experiment-design`
- `decision-and-outcome-roadmapping`
- `data-analysis-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
