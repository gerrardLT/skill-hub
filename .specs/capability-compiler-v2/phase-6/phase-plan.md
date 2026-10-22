# Capability Compiler V2 — Phase 6 Plan

## Objective

Rewrite the 54 Phase 6 implementation, testing, review, evaluation, performance, browser/tool runtime, and local workflow capabilities into atomic, provenance-complete candidate Skills. This phase does not assemble giant implementation, QA, benchmark, or browser workflows; conditional orchestration remains Phase 8.

## Frozen Inputs

- Phase 2 tree: `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`
- Phase 3 tree: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 tree: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase 5 tree: `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`
- Phase ownership: exactly 54 IDs in `curation/v2/lifecycle/phase-ownership.json` phase `6`.
- Source Skills and all released V1 assets remain immutable.

## Candidate Location

- `evals/candidates/capability-compiler-v2/phase-6/skills/<capability-id>/`
- Version: `0.1.0-v2-candidate`
- Status: `evaluating`
- Evaluation state: `not-run-phase-9`

## Review Batches

Batching controls review size only; it does not merge contracts or change Phase 2 ownership.

### A. Change Implementation and Evidence

- change scope freeze, plan execution control, isolated implementation, TDD, root-cause investigation, defect remediation, developer self-check/fix, UI remediation, website remediation;
- artifact persistence, completion evidence, resilience/determinism, local branch integration, destructive Git guard;
- implementation/spec compliance and independent code review remain separate from mutation.

### B. Test, QA, Runtime, and Performance

- baseline/regression, test strategy/cases/doubles/bootstrap, Playwright, Vitest, mobile runtime, browser probing;
- independent black-box QA, QA triage, code health, code-review evidence, developer-experience assessment;
- frontend interaction performance, Web performance diagnostics, website audit assessment;
- review and diagnostics must never silently repair source.

### C. LLM Evaluation and Experimentation

- evaluator engineering, quality evaluation, results analysis, model/workflow benchmarking;
- experiment execution and dataset publication retain distinct remote-write identities and per-action authorization;
- prompts, datasets, outputs, judges, costs, seeds, versions, contamination, privacy, external transfer, and publication rights require explicit governance.

### D. Browser, Tool, Local-System, and Workflow Support

- browser auth, session/runtime configuration, data acquisition, pairing provisioning/verification;
- tool readiness, workflow runtime support/upgrade, provider CLI auth, local memory/context store, local Git guard;
- document rendering, reference/deferred material, workflow Skill authoring, artifact tool actions;
- setup, verification, acquisition, authoring, and runtime upgrade remain distinct identities.

## Permission Invariants

Phase 2 permission identities are upper bounds, not automatic authorization to use every action.

- `read-only`: no mutation or command execution.
- `local-exec*`: model remains read-only; host executes only approved bounded commands and writes only declared evidence artifacts.
- `workspace-write*`: source mutation only where the atomic responsibility explicitly implements or repairs authorized project files; otherwise limit writes to run outputs or candidate artifacts.
- `local-system-write-*`: require explicit local-system authorization, bounded paths or configuration keys, backup/rollback, no project-source disguise, and no credential disclosure.
- `local-system-write-external-session-authorized-only`: require per-action authorization, scoped session identity, expiry, revocation, and no general remote-write authority.
- `remote-write-authorized-only`: require per-action authorization, exact provider/repository/dataset target, dry-run or preview where available, idempotency, rollback or deletion terms, and durable provider response evidence.
- independent QA, review, audit, evidence acquisition, and finding triage never repair source.

## Required Semantic Gates

Each candidate must define exact provenance, concrete triggers and anti-triggers, separate holdouts, one semantic mutation, precise mutation scope, and `not-run-phase-9`. The set must enforce:

- RED/GREEN/refactor ordering and independent host verification for TDD;
- root cause before remediation and one writer per authorized workspace;
- plan step state, invalidation, checkpoint, resume, and evidence lineage;
- test pyramid or portfolio rationale, hermetic doubles, deterministic fixtures, runtime bootstrap, and named tool boundaries;
- real browser/runtime evidence for black-box QA and performance claims;
- stable baseline identity, thresholds, variance, sample size, warmup, environment, and regression attribution;
- code review evidence acquisition separated from findings, provider comments, and fixes;
- LLM evaluator validity, judge governance, calibration, contamination, reproducibility, cost, and publication rights;
- browser authentication/session setup separated from read-only acquisition and probing;
- destructive Git and local-system mutations protected by explicit confirmation and recoverability;
- completion claims backed by current commands, exits, duration, artifact hashes, source identity, and limitations.

## Remote and Credential Boundaries

- No remote write is exercised in Phase 6 candidate construction or Gate execution.
- No browser/provider login, pairing, credential mint, experiment submission, or dataset publication is executed.
- No credential, cookie, token, API key, secret, or raw private dataset value enters candidate evidence.
- Remote-write candidates remain declarative and unexecuted until a later explicitly authorized real evaluation.

## Verification

Phase 6 Gate must fail closed on:

- Phase 2–5 identity drift;
- candidate ownership/provenance/hash mismatch;
- trigger/holdout leakage or baseline fabrication;
- mutation scope broader than the atomic responsibility;
- reviewer/auditor/QA source write;
- source implementer lacking authorized workspace scope;
- local-system or remote-write candidate without per-action authorization, target, expiry/revocation, evidence, and recovery terms;
- fake command, browser, benchmark, publication, or provider evidence;
- missing testing, performance, LLM-eval, browser, Git, completion, or determinism semantic markers;
- unresolved semantic-review findings.

## Outputs

- 54 candidate Skill packages.
- Phase 6 schemas, batch ledger, holdout corpus, semantic review, Gate, mutation tests, manifest, and report.
- Unified runner update after directed suites pass.

## Stop Conditions

Stop on prior-phase drift, ambiguous credential/remote authority, any need to contact a provider or browser session, any proposed destructive Git/local-system operation without recovery, missing private-data governance, or a semantic conflict that changes review independence, source ownership, benchmark validity, or publication rights.
