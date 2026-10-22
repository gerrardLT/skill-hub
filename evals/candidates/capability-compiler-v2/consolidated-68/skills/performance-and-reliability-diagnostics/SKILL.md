---
name: performance-and-reliability-diagnostics
description: "Consolidated capability with 4 selectable modes: evaluation-results-analysis; frontend-rendering-and-interaction-performance; model-and-workflow-benchmarking; web-performance-diagnostics. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [evaluation-results-analysis, frontend-rendering-and-interaction-performance, model-and-workflow-benchmarking, web-performance-diagnostics]
---

# Performance And Reliability Diagnostics

## Responsibility

Consolidated capability covering 4 related modes: Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.; Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair.; Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.; Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `evaluation-results-analysis` | `local-exec` | Finished LLM experiment or evaluation runs must be compared on predeclared metrics with variance and failure slices; Someone asks whether a model or prompt variant is really better once uncertainty an | Execute the reviewed experiment against the provider (-> llm-experiment-execution); Evaluate raw model outputs with metr |
| `frontend-rendering-and-interaction-performance` | `local-exec` | A specific interaction (click, type, scroll, route change) feels slow or janky and needs a trace-backed explanation; Component-level rendering, long tasks, hydration or animation frame drops must be m | Audit broad page-load, network, cache, image, and Core Web Vitals behavior (-> web-performance-diagnostics); Apply the a |
| `model-and-workflow-benchmarking` | `local-exec` | Two or more model, prompt or workflow variants must be compared on frozen cases for quality, latency and cost; Someone asks which variant to pick once run-to-run variance and failed cases are counted. | Run a remote provider experiment to produce missing outputs (-> llm-experiment-execution); Perform detailed LLM quality  |
| `web-performance-diagnostics` | `local-exec` | A page or journey needs a page-load, network, caching or Core Web Vitals baseline under declared conditions; Someone asks why a page is slow and needs waterfall, asset and bundle evidence rather than  | Profile component-level rendering and interaction latency (-> frontend-rendering-and-interaction-performance); Apply the |

## Mode: `evaluation-results-analysis`

### evaluation-results-analysis

#### Responsibility

Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.

#### Trigger

Use when the request matches any of:
- Finished LLM experiment or evaluation runs must be compared on predeclared metrics with variance and failure slices
- Someone asks whether a model or prompt variant is really better once uncertainty and cost are counted

Do not use when:
- Execute the reviewed experiment against the provider. Route to `llm-experiment-execution`.
- Evaluate raw model outputs with metrics, judges, and human agreement first. Route to `llm-quality-evaluation`.
- Interpret a product or UX experiment against its go, pivot or kill rule. Route to `results-analysis-and-decision-readout`.
- Check whether the data or metric itself is correct. Route to `data-analysis-validation`.

#### Required Inputs

- Experiment results, metric contract, baseline, statistical assumptions, and known data limits.

#### Procedure

1. Freeze run identities, dataset and evaluator versions, metric contract, thresholds, exclusions, statistical assumptions, baseline, costs, and known data limits.
2. Verify result completeness, pairing, missingness, duplicates, contamination, retries, failed runs, and comparable versions before analysis.
3. Compute declared aggregates, distributions, uncertainty, effect sizes or intervals, failure slices, cost and latency, and sensitivity without metric shopping.
4. Return supported and unsupported claims, regressions, tradeoffs, and a recommendation to the named human owner; do not rerun, approve, or deploy.

#### Domain Guidance

- Analysis split: data-analysis-validation checks the data, results-analysis-and-decision-readout interprets product experiments, evaluation-results-analysis interprets model evaluations.

#### Output Contract

Produce:
- experiment comparison
- variance and uncertainty report
- failure-slice and regression analysis
- evidence-bounded human decision readout

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `frozen-metrics`
- `variance`
- `uncertainty`
- `failure-slices`
- `cost-latency`
- `no-metric-shopping`
- `human-decision`

#### Hard Gates

- Analysis cannot change metrics, thresholds, exclusions, or slices after seeing results without labeling the work exploratory; incomplete or incomparable runs cannot yield a pass claim.
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

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `llm-experiment-execution`
- `llm-quality-evaluation`
- `model-and-workflow-benchmarking`
- `results-analysis-and-decision-readout`
- `data-analysis-validation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `frontend-rendering-and-interaction-performance`

### frontend-rendering-and-interaction-performance

#### Responsibility

Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair.

#### Trigger

Use when the request matches any of:
- A specific interaction (click, type, scroll, route change) feels slow or janky and needs a trace-backed explanation
- Component-level rendering, long tasks, hydration or animation frame drops must be measured on a frozen journey

Do not use when:
- Audit broad page-load, network, cache, image, and Core Web Vitals behavior. Route to `web-performance-diagnostics`.
- Apply the approved performance optimization to frontend source. Route to `defect-remediation`.

#### Required Inputs

- A rendered frontend, interaction traces, performance measurements, and device constraints.

#### Procedure

1. Freeze source identity, journey, viewport, device or CPU profile, browser, data, cache state, warmup, sample count, budgets, and instrumentation.
2. Run approved local measurements for render phases, input delay, long tasks, layout work, hydration, state updates, and animation frames.
3. Report distributions and traces, distinguish noise from repeatable bottlenecks, and link suspected causes to source or runtime evidence.
4. Return baseline, bottlenecks, uncertainty, and optimization hypotheses without editing source or claiming production impact.

#### Domain Guidance

- Default budgets when the user supplies none: long task <= 50 ms, frame <= 16.7 ms (60 fps), interaction latency (INP) <= 200 ms at p75; report every measured value against them and say when a default was used.
- Hypothesis catalog: animating width/height/top/left instead of transform/opacity triggers layout and paint; a parent CSS variable driving child transforms recalculates every child; Framer Motion x/y/scale shorthands run on the main thread and drop frames under load.
- Ownership: field INP belongs to web-performance-diagnostics; this Skill owns component-level interaction traces.
- Ownership: component-level render and interaction traces belong here; page-level Core Web Vitals, including field INP, belong to web-performance-diagnostics.

#### Output Contract

Produce:
- interaction performance baseline
- trace and distribution evidence
- repeatable bottleneck findings
- optimization hypotheses and limits

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `frozen-journey`
- `device-profile`
- `warmup`
- `sample-count`
- `distribution`
- `interaction-latency`
- `trace`

#### Hard Gates

- A frontend performance finding requires a frozen journey, representative device profile, warmup, sample count, distribution, budget, and repeatable trace; one fast or slow run is not evidence.
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

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `web-performance-diagnostics`
- `defect-remediation`
- `purposeful-motion-and-animation-engineering`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `model-and-workflow-benchmarking`

### model-and-workflow-benchmarking

#### Responsibility

Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.

#### Trigger

Use when the request matches any of:
- Two or more model, prompt or workflow variants must be compared on frozen cases for quality, latency and cost
- Someone asks which variant to pick once run-to-run variance and failed cases are counted

Do not use when:
- Run a remote provider experiment to produce missing outputs. Route to `llm-experiment-execution`.
- Perform detailed LLM quality scoring with judges and human agreement. Route to `llm-quality-evaluation`.
- Compare an application's performance before and after a code change. Route to `baseline-regression-control`.
- Measure web page load and Core Web Vitals. Route to `web-performance-diagnostics`.

#### Required Inputs

- Frozen cases, candidate variants, metric contract, environment, and budget.

#### Procedure

1. Freeze cases, variants, versions, runner, environment, hardware, seeds, warmup, repeats, timeouts, budget, metrics, thresholds, and exclusions.
2. Verify comparable inputs and execution conditions and preserve failed, timed-out, invalid, and retried cases.
3. Run only approved local or supplied-output comparisons, recording versions, commands, exits, durations, cost assumptions, artifacts, and hashes.
4. Report distributions, variance, regressions, cost-quality-latency tradeoffs, sensitivity, and an evidence-bounded recommendation without choosing product strategy.

#### Domain Guidance

- Scope is model and workflow variants on frozen cases. Preview which providers and credentials a multi-provider benchmark would use before running anything, and never submit remotely.

#### Output Contract

Produce:
- matched benchmark run evidence
- metric distributions and variance
- cost-quality-latency comparison
- regression and recommendation report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `frozen-cases`
- `matched-environment`
- `warmup`
- `repeated-runs`
- `variance`
- `failed-case-retention`
- `cost-quality-latency`

#### Hard Gates

- A benchmark requires frozen cases and versions, matched environment and budgets, warmup, repeated runs, variance, failed-case retention, and exact artifacts; leaderboard point estimates alone fail.
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

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `llm-quality-evaluation`
- `llm-experiment-execution`
- `evaluation-results-analysis`
- `baseline-regression-control`
- `web-performance-diagnostics`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `web-performance-diagnostics`

### web-performance-diagnostics

#### Responsibility

Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair.

#### Trigger

Use when the request matches any of:
- A page or journey needs a page-load, network, caching or Core Web Vitals baseline under declared conditions
- Someone asks why a page is slow and needs waterfall, asset and bundle evidence rather than one Lighthouse score

Do not use when:
- Profile component-level rendering and interaction latency. Route to `frontend-rendering-and-interaction-performance`.
- Apply the approved Web performance fixes. Route to `defect-remediation`.

#### Required Inputs

- A web application, controlled sampling environment, network waterfall, and build information.

#### Procedure

1. Freeze URL or build, source identity, journey, browser, device and network profile, cache mode, warmup, sample count, budgets, and third-party boundary.
2. Run approved local diagnostics and record navigation, Web Vitals, waterfall, CPU, assets, cache, server timing, and screenshots or traces.
3. Report distributions, outliers, repeatable bottlenecks, suspected ownership, and environmental uncertainty rather than one score.
4. Return baseline and prioritized hypotheses without editing source, changing production, or claiming user impact beyond conditions.

#### Domain Guidance

- Core Web Vitals thresholds at p75: LCP good <= 2.5 s, poor > 4 s; INP good <= 200 ms, poor > 500 ms; CLS good <= 0.1, poor > 0.25. Label every number as lab or field data and never mix them in one verdict.
- Detect the framework and bundler from config files and package.json, then attribute large bundles to owning packages and check tree-shaking (sideEffects, usedExports, production mode) before proposing hypotheses.
- Field INP ownership sits here; component-level interaction traces belong to frontend-rendering-and-interaction-performance.
- Ownership: field and lab INP, LCP, CLS and other Core Web Vitals belong here; component-level interaction traces belong to frontend-rendering-and-interaction-performance.

#### Output Contract

Produce:
- Web performance baseline
- Core Web Vitals and waterfall evidence
- repeatable bottleneck findings
- optimization hypotheses and limitations
- threshold table with lab or field label per metric

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `Core-Web-Vitals`
- `waterfall`
- `cache-mode`
- `network-profile`
- `warmup`
- `sample-count`
- `distribution`

#### Hard Gates

- A Web performance claim requires repeated runs with recorded browser, device, network, cache, warmup, sample count, distribution, budget, and target identity; a single Lighthouse score cannot pass.
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

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `frontend-rendering-and-interaction-performance`
- `defect-remediation`
- `website-audit-assessment`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
