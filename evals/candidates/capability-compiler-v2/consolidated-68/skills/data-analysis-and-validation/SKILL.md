---
name: data-analysis-and-validation
description: "Consolidated capability with 3 selectable modes: data-analysis-validation; evaluation-dataset-publication; results-analysis-and-decision-readout. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [data-analysis-validation, evaluation-dataset-publication, results-analysis-and-decision-readout]
---

# Data Analysis And Validation

## Responsibility

Consolidated capability covering 3 related modes: Validate a dataset, metric definition, transformation, and analytical claim before decision use.; Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.; Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `data-analysis-validation` | `workspace-write` | A metric, dataset or analytical claim must be checked for correctness before it supports a decision; Someone asks whether a result is trustworthy, including denominators, cohorts, leakage and confound | Collect new customer data to fill these gaps (-> research-planning-and-governance); Make the product decision from the v |
| `evaluation-dataset-publication` | `remote-write-authorized-only` | One frozen, versioned evaluation dataset must be uploaded to one exact provider target after governance checks; Someone asks what must be true (rights, redaction, retention, visibility) before a datas | Design or modify the local evaluation samples and schema before publication (-> test-case-design-and-export); Run the re |
| `results-analysis-and-decision-readout` | `workspace-write` | A finished product experiment or research result must be read against the thresholds declared beforehand; Someone asks whether to go, pivot or kill on the result and what uncertainty remains. | Design the experiment and its success criteria before execution (-> solution-hypothesis-and-experiment-design); Commit t |

## Mode: `data-analysis-validation`

### data-analysis-validation

#### Responsibility

Validate a dataset, metric definition, transformation, and analytical claim before decision use.

#### Trigger

Use when the request matches any of:
- A metric, dataset or analytical claim must be checked for correctness before it supports a decision
- Someone asks whether a result is trustworthy, including denominators, cohorts, leakage and confounds

Do not use when:
- Collect new customer data to fill these gaps. Route to `research-planning-and-governance`.
- Make the product decision from the validated result. Route to `results-analysis-and-decision-readout`.
- Interpret model evaluation results across experiments. Route to `evaluation-results-analysis`.

#### Required Inputs

- Product metrics, feedback, queries, an experiment design, or experiment results.

#### Procedure

1. Freeze the question, population, time window, metric formula, and expected decision use.
2. Audit source authority, consent, schema, missingness, duplication, leakage, and transformations.
3. Recompute key aggregates and compare denominators, cohorts, and uncertainty.
4. Test plausible alternative explanations and sensitivity to exclusions.
5. Return supported claims, unsupported claims, and data gaps.

#### Domain Guidance

- Recompute the headline aggregate from the supplied data and show the arithmetic. State every denominator. Check sample ratio mismatch for experiments (compute the chi-square against the intended split and call a failed check a failed check with the statistic).
- Reproduction notes template: question, data sources with as-of date, definitions, method, result, caveats and known unknowns.
- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

#### Output Contract

Produce:
- analysis validation report
- metric definition register
- reproduction notes
- claim evidence table
- recomputed aggregates with arithmetic and sample-ratio check

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- No analytical claim passes without reproducible inputs, a declared denominator, and preserved uncertainty.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `results-analysis-and-decision-readout`
- `qualitative-evidence-synthesis`
- `research-planning-and-governance`
- `evaluation-results-analysis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `evaluation-dataset-publication`

### evaluation-dataset-publication

#### Responsibility

Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.

#### Trigger

Use when the request matches any of:
- One frozen, versioned evaluation dataset must be uploaded to one exact provider target after governance checks
- Someone asks what must be true (rights, redaction, retention, visibility) before a dataset may be published

Do not use when:
- Design or modify the local evaluation samples and schema before publication. Route to `test-case-design-and-export`.
- Run the reviewed LLM experiment against the published dataset. Route to `llm-experiment-execution`.

#### Required Inputs

- Approved samples, schema, minimization and redaction policy, provider target, retention policy, and authorization.

#### Procedure

1. Verify frozen local manifest and hashes, schema, provenance, consent or license, minimization, redaction, sensitive fields, external-transfer authority, provider target, region, retention, deletion, owner, budget, and per-action authorization.
2. Preview the exact sample count, bytes, metadata, visibility, version identity, and provider request without exposing secret values.
3. Perform one idempotent provider create or upload action, refusing overwrite, public visibility, unrelated target, or mutable latest aliases unless explicitly authorized.
4. Record provider response, immutable dataset identity, request and local hashes, count, duration, cost if any, retention, deletion or rollback path, and partial-failure cleanup.

#### Domain Guidance

- Redaction gaps block every publish target that would carry the affected fields, not only the requested one. When a safer target such as a staging dataset is available after the gaps are fixed, propose it as a conditional path with its own authorization need.
- The proposed action must name a target that satisfies the governance terms; never propose the prohibited production-shared target.

#### Output Contract

Produce:
- versioned provider dataset identity
- publication request and receipt
- local-provider hash and count evidence
- governance, retention, deletion, and failure-cleanup record
- conditional alternative target with its own authorization need

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `per-action-authorization`
- `exact-provider-target`
- `frozen-version`
- `redaction`
- `external-transfer`
- `idempotency`
- `publication-receipt`
- `deletion-path`

#### Hard Gates

- Remote dataset publication is one per-action-authorized write to an exact provider target and version; missing rights, redaction, transfer, retention, deletion, visibility, idempotency, or cleanup terms blocks publication.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

#### External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `test-case-design-and-export`
- `llm-experiment-execution`
- `llm-evaluator-engineering`
- `artifact-persistence-and-tool-actions`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `results-analysis-and-decision-readout`

### results-analysis-and-decision-readout

#### Responsibility

Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.

#### Trigger

Use when the request matches any of:
- A finished product experiment or research result must be read against the thresholds declared beforehand
- Someone asks whether to go, pivot or kill on the result and what uncertainty remains

Do not use when:
- Design the experiment and its success criteria before execution. Route to `solution-hypothesis-and-experiment-design`.
- Commit the roadmap to the recommended decision. Route to `decision-and-outcome-roadmapping`.
- Analyze model or evaluator results from an LLM evaluation run. Route to `evaluation-results-analysis`.
- Check whether the data or metric itself is correct. Route to `data-analysis-validation`.

#### Required Inputs

- Experiment or research data, metrics, baselines, bias checks, and decision criteria.

#### Procedure

1. Freeze experiment identity, preregistered hypothesis, metrics, thresholds, exclusions, and analysis population.
2. Validate result provenance and note protocol deviations or missing data.
3. Compare outcomes to thresholds, uncertainty, segments, counter-metrics, and plausible alternatives.
4. Separate observed result, interpretation, recommendation, and unknown.
5. Return GO/PIVOT/KILL or continue recommendation for the named human decision owner.

#### Domain Guidance

- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

#### Output Contract

Produce:
- results readout
- threshold comparison
- failure-slice analysis
- human decision recommendation

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- A recommendation may not be presented as a product decision, and post-hoc thresholds must be labeled rather than disguised as preregistered criteria.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `solution-hypothesis-and-experiment-design`
- `decision-and-outcome-roadmapping`
- `data-analysis-validation`
- `evaluation-results-analysis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
