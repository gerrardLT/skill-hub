---
name: results-analysis-and-decision-readout
description: "Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision. Use when A finished product experiment or research result must be read against the thresholds declared beforehand; Someone asks whether to go, pivot or kill on the result and what uncertainty remains. Do not use for: Design the experiment and its success criteria before execution (-> solution-hypothesis-and-experiment-design); Commit the roadmap to the recommended decision (-> decision-and-outcome-roadmapping); Analyze model or evaluator results from an LLM evaluation run (-> evaluation-results-analysis); Check whether the data or metric itself is correct (-> data-analysis-validation)."
---

# Results Analysis And Decision Readout

## Responsibility

Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.

## Trigger

Use when the request matches any of:
- A finished product experiment or research result must be read against the thresholds declared beforehand
- Someone asks whether to go, pivot or kill on the result and what uncertainty remains

Do not use when:
- Design the experiment and its success criteria before execution. Route to `solution-hypothesis-and-experiment-design`.
- Commit the roadmap to the recommended decision. Route to `decision-and-outcome-roadmapping`.
- Analyze model or evaluator results from an LLM evaluation run. Route to `evaluation-results-analysis`.
- Check whether the data or metric itself is correct. Route to `data-analysis-validation`.

## Required Inputs

- Experiment or research data, metrics, baselines, bias checks, and decision criteria.

## Procedure

1. Freeze experiment identity, preregistered hypothesis, metrics, thresholds, exclusions, and analysis population.
2. Validate result provenance and note protocol deviations or missing data.
3. Compare outcomes to thresholds, uncertainty, segments, counter-metrics, and plausible alternatives.
4. Separate observed result, interpretation, recommendation, and unknown.
5. Return GO/PIVOT/KILL or continue recommendation for the named human decision owner.

## Domain Guidance

- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

## Output Contract

Produce:
- results readout
- threshold comparison
- failure-slice analysis
- human decision recommendation

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A recommendation may not be presented as a product decision, and post-hoc thresholds must be labeled rather than disguised as preregistered criteria.
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
- `solution-hypothesis-and-experiment-design`
- `decision-and-outcome-roadmapping`
- `data-analysis-validation`
- `evaluation-results-analysis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
