from __future__ import annotations

try:
    from tools.curation.v2_phase6_design_common import D
except ModuleNotFoundError:
    from v2_phase6_design_common import D

DESIGNS = {
    "evaluation-dataset-publication": D(
        "Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.",
        ["Publish this approved redacted evaluation dataset version to the named provider target and record its deletion path.", "Create one immutable provider dataset from the frozen manifest after confirming rights, retention, and per-action authorization."],
        [("Design or modify the local evaluation samples and schema before publication.", "test-case-design-and-export"), ("Run the reviewed LLM experiment against the published dataset.", "llm-experiment-execution")],
        ["Verify frozen local manifest and hashes, schema, provenance, consent or license, minimization, redaction, sensitive fields, external-transfer authority, provider target, region, retention, deletion, owner, budget, and per-action authorization.", "Preview the exact sample count, bytes, metadata, visibility, version identity, and provider request without exposing secret values.", "Perform one idempotent provider create or upload action, refusing overwrite, public visibility, unrelated target, or mutable latest aliases unless explicitly authorized.", "Record provider response, immutable dataset identity, request and local hashes, count, duration, cost if any, retention, deletion or rollback path, and partial-failure cleanup."],
        ["versioned provider dataset identity", "publication request and receipt", "local-provider hash and count evidence", "governance, retention, deletion, and failure-cleanup record"],
        "Remote dataset publication is one per-action-authorized write to an exact provider target and version; missing rights, redaction, transfer, retention, deletion, visibility, idempotency, or cleanup terms blocks publication.",
        ["test-case-design-and-export", "llm-experiment-execution", "llm-evaluator-engineering", "artifact-persistence-and-tool-actions"],
        ["per-action-authorization", "exact-provider-target", "frozen-version", "redaction", "external-transfer", "idempotency", "publication-receipt", "deletion-path"],
        ("Publish the frozen redacted eval-v3 manifest to the exact private provider dataset target and record immutable identity and deletion evidence.", "Generate or revise the evaluation cases and schema before a publication manifest is frozen."),
        mutation_scope="remote-provider-write", human=True, data=True, external=True),
    "evaluation-results-analysis": D(
        "Analyze frozen experiment results against declared metrics, variance, failure slices, costs, and decision thresholds without rerunning experiments or approving product changes.",
        ["Analyze these frozen experiment runs against the preregistered metrics, variance, cost, and failure-slice thresholds.", "Compare baseline and candidate LLM results and identify uncertainty, regressions, slice failures, and unsupported conclusions."],
        [("Execute the reviewed experiment against the provider.", "llm-experiment-execution"), ("Evaluate raw model outputs with metrics, judges, and human agreement first.", "llm-quality-evaluation")],
        ["Freeze run identities, dataset and evaluator versions, metric contract, thresholds, exclusions, statistical assumptions, baseline, costs, and known data limits.", "Verify result completeness, pairing, missingness, duplicates, contamination, retries, failed runs, and comparable versions before analysis.", "Compute declared aggregates, distributions, uncertainty, effect sizes or intervals, failure slices, cost and latency, and sensitivity without metric shopping.", "Return supported and unsupported claims, regressions, tradeoffs, and a recommendation to the named human owner; do not rerun, approve, or deploy."],
        ["experiment comparison", "variance and uncertainty report", "failure-slice and regression analysis", "evidence-bounded human decision readout"],
        "Analysis cannot change metrics, thresholds, exclusions, or slices after seeing results without labeling the work exploratory; incomplete or incomparable runs cannot yield a pass claim.",
        ["llm-experiment-execution", "llm-quality-evaluation", "model-and-workflow-benchmarking", "results-analysis-and-decision-readout"],
        ["frozen-metrics", "variance", "uncertainty", "failure-slices", "cost-latency", "no-metric-shopping", "human-decision"],
        ("Analyze the frozen paired runs under preregistered metrics and thresholds, preserving failed runs, variance, cost, and slice regressions.", "Submit a new provider experiment because the current outcome is inconclusive."),
        mutation_scope="artifact-output", human=True, data=True),
    "llm-evaluator-engineering": D(
        "Implement bounded local or draft-online evaluator definitions and calibration checks against an explicit quality contract; provider activation remains separate.",
        ["Implement local evaluator code and calibration fixtures for groundedness, citation, and refusal quality.", "Create a draft judge rubric and disagreement calibration using authorized redacted traces without calling a provider."],
        [("Run the frozen evaluator across model outputs and produce scores.", "llm-quality-evaluation"), ("Activate an online provider experiment using the evaluator.", "llm-experiment-execution")],
        ["Freeze quality dimensions, observable criteria, trace classes, labels, evaluator mode, judge policy, data governance, workspace, expected errors, and calibration target.", "Choose deterministic checks before model judges; define inputs, outputs, abstention, invalid cases, parsing, versions, and cost or transfer boundary.", "Implement the smallest local evaluator, rubric, fixtures, and executable checks; online calls remain stubs or draft configuration unless separately authorized.", "Calibrate against labeled cases and human disagreement, test adversarial and malformed inputs, record false positives or negatives, and return limitations and activation handoff."],
        ["evaluator definitions and local source", "rubric and labeled calibration fixtures", "local executable check evidence", "limitations and provider-activation handoff"],
        "An evaluator cannot pass from plausible rubric prose: it needs versioned executable behavior, labeled calibration cases, abstention and invalid handling, disagreement evidence, and no unauthorized provider call.",
        ["llm-quality-evaluation", "llm-experiment-execution", "evaluation-results-analysis", "test-case-design-and-export"],
        ["quality-contract", "deterministic-first", "versioned-evaluator", "calibration", "abstention", "malformed-input", "no-provider-activation"],
        ("Implement a local groundedness evaluator with labeled calibration cases, abstention, malformed handling, and disagreement evidence.", "Execute an online provider experiment using the frozen evaluator and dataset."),
        mutation_scope="authorized-workspace", data=True),
    "llm-experiment-execution": D(
        "Execute one reviewed frozen LLM experiment against exact dataset and evaluator versions under per-action provider-write, budget, and data-transfer authorization.",
        ["Run this approved experiment once against the named provider, frozen dataset version, evaluator versions, and budget.", "Submit the reviewed candidate-versus-baseline LLM run and record immutable run identity, parameters, cost, duration, and failures."],
        [("Design or calibrate the evaluator before experiment review.", "llm-evaluator-engineering"), ("Analyze the frozen completed experiment results and advise the human owner.", "evaluation-results-analysis")],
        ["Verify reviewed experiment definition, hypotheses, variants, model and prompt versions, dataset identity, evaluator versions, seeds, sampling parameters, provider target, region, budget, transfer policy, retention, stop rules, and per-action authorization.", "Preview exact request count, max cost, data fields leaving the boundary, retries, concurrency, idempotency key, and cancellation or partial-failure behavior.", "Perform only the authorized provider run; do not change prompts, samples, evaluators, metrics, thresholds, or budget after submission.", "Record provider run identity, exact parameters, raw result references and hashes, failed cases, retries, cost, duration, status, cancellation, and cleanup for later analysis."],
        ["provider experiment run identity", "frozen parameter and version manifest", "raw result references and failure evidence", "cost, duration, cancellation, and cleanup record"],
        "Experiment execution requires one exact reviewed definition and per-action provider authorization; any prompt, model, dataset, evaluator, metric, budget, transfer, or target drift invalidates or blocks the run.",
        ["llm-evaluator-engineering", "evaluation-dataset-publication", "evaluation-results-analysis", "llm-quality-evaluation"],
        ["reviewed-definition", "exact-provider-target", "frozen-versions", "per-action-authorization", "budget", "idempotency", "run-receipt", "no-post-submit-drift"],
        ("Submit the reviewed frozen baseline-candidate experiment once and preserve exact run, parameter, cost, duration, retry, and failure evidence.", "Analyze the completed runs against metrics and thresholds."),
        mutation_scope="remote-provider-write", human=True, data=True, external=True),
    "llm-quality-evaluation": D(
        "Evaluate supplied model outputs with governed deterministic metrics, factuality checks, calibrated judges, human agreement, statistics, and regression comparisons without provider activation.",
        ["Evaluate these supplied model outputs for groundedness, factuality, relevance, refusal, and regression with confidence intervals.", "Compare automated and judge scores with human labels, calibrate disagreement, and report failure slices."],
        [("Implement or revise the evaluator definitions and calibration fixtures.", "llm-evaluator-engineering"), ("Execute a new provider experiment to generate outputs.", "llm-experiment-execution")],
        ["Freeze output, reference, dataset, model and prompt identities, criteria, evaluator versions, annotations, baseline, statistical plan, and governance boundary.", "Validate completeness, contamination, label quality, inter-annotator agreement, slice definitions, and evaluator applicability.", "Run approved local deterministic metrics and supplied or locally available judges; an external LLM Judge requires explicit transfer and provider authorization or remains blocked.", "Compute scores, confidence or variance, agreement, regressions, failure slices, examples, and evaluator limitations; preserve invalid and failed cases."],
        ["repeatable quality scores", "factuality and groundedness evidence", "human-judge agreement and calibration", "confidence, regression, and failure-slice report"],
        "External LLM Judge use is not implicit in local evaluation authority; without explicit data-transfer, provider, retention, deletion, and cost authorization, judge-dependent results remain blocked.",
        ["llm-evaluator-engineering", "llm-experiment-execution", "evaluation-results-analysis", "model-and-workflow-benchmarking"],
        ["deterministic-metrics", "factuality", "judge-calibration", "human-agreement", "confidence", "regression", "external-judge-authorization"],
        ("Evaluate supplied outputs locally with deterministic checks and calibrated labels, blocking any external judge that lacks transfer authorization.", "Generate new outputs by running a provider experiment."),
        mutation_scope="artifact-output", data=True),
    "model-and-workflow-benchmarking": D(
        "Benchmark supplied model or workflow variants on frozen cases, matched environments, metrics, variance, cost, latency, and evidence without remote submission or product approval.",
        ["Benchmark these local workflow variants over frozen cases with matched budgets, repeated runs, cost, latency, and variance.", "Compare supplied model outputs or approved local runners under one metric and environment contract."],
        [("Run a remote provider experiment to produce missing outputs.", "llm-experiment-execution"), ("Perform detailed LLM quality scoring with judges and human agreement.", "llm-quality-evaluation")],
        ["Freeze cases, variants, versions, runner, environment, hardware, seeds, warmup, repeats, timeouts, budget, metrics, thresholds, and exclusions.", "Verify comparable inputs and execution conditions and preserve failed, timed-out, invalid, and retried cases.", "Run only approved local or supplied-output comparisons, recording versions, commands, exits, durations, cost assumptions, artifacts, and hashes.", "Report distributions, variance, regressions, cost-quality-latency tradeoffs, sensitivity, and an evidence-bounded recommendation without choosing product strategy."],
        ["matched benchmark run evidence", "metric distributions and variance", "cost-quality-latency comparison", "regression and recommendation report"],
        "A benchmark requires frozen cases and versions, matched environment and budgets, warmup, repeated runs, variance, failed-case retention, and exact artifacts; leaderboard point estimates alone fail.",
        ["llm-quality-evaluation", "llm-experiment-execution", "evaluation-results-analysis", "baseline-regression-control"],
        ["frozen-cases", "matched-environment", "warmup", "repeated-runs", "variance", "failed-case-retention", "cost-quality-latency"],
        ("Benchmark three local workflow versions on frozen cases with warmup, repeats, timeouts, failures, variance, cost, and latency.", "Submit missing candidate outputs to a remote model provider."),
        mutation_scope="artifact-output", data=True),
}
