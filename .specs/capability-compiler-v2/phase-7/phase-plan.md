# Capability Compiler V2 — Phase 7 Plan

## Objective

Rewrite the 39 Phase 7 delivery, deployment, observability, rollback, incident-response, and learning capabilities into atomic, provenance-complete candidate Skills. Phase 7 constructs contracts and evaluation fixtures only. It does not push, create or merge pull requests, deploy, alter provider configuration, roll back production, install agents, remap identities, authenticate, or mutate incident systems.

## Frozen Inputs

- Phase 2 tree: `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`
- Phase 3 tree: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 tree: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase 5 tree: `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`
- Phase 6 tree: `7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561`
- Phase ownership: exactly 39 IDs under phase `7`.
- Source Skills and released V1 assets remain immutable.

## Candidate Location

- `evals/candidates/capability-compiler-v2/phase-7/skills/<capability-id>/`
- Version: `0.1.0-v2-candidate`
- Status: `evaluating`
- Evaluation state: `not-run-phase-9`
- Action execution state: `not-executed-phase-7`

## Review Batches

### A. Change Delivery and Deployment

Keep separate:

- local change packaging;
- delivery and merge/deploy readiness preflight;
- remote branch push;
- pull-request create/update;
- pull-request comment response;
- pull-request merge;
- deployment environment contract;
- generic deployment trigger;
- Web-hosting, edge-worker, and Kubernetes deployment;
- Kubernetes readiness;
- release documentation;
- service-identity remapping;
- rollback execution.

Each remote action requires fresh per-action authorization, exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded retries, failure cleanup, and rollback/recovery. One authorization never cascades to another remote action.

### B. Observability and Production Evidence

Keep separate:

- APM enablement, verification, troubleshooting, and summary;
- observability agent installation;
- logs, metrics, alerts, release observability, AI/LLM observability, and source metadata;
- canary baseline artifact management and production canary observation;
- deployment observation;
- trace classification, LLM trace root-cause analysis, error-monitoring investigation, and cloud reliability assessment.

Configuration and installation use remote-write identities. Verification, diagnosis, classification, investigation, and assessment are read-only. Observation writes only evidence artifacts and never rolls back or repairs production.

### C. Incident, Adoption, Retrospective, and Learning

Keep separate:

- incident coordination from remediation or rollback execution;
- engineering retrospective from live incident response;
- feedback/learning-loop recommendation from local persistence;
- local learning persistence from external synchronization;
- AI organizational adoption from AI architecture or autonomous action.

## Permission Invariants

- `remote-write-authorized-only`: contract exists in Phase 7, but no action executes. A real action needs fresh per-action authorization for one exact provider/repository/environment/resource and one bounded operation.
- `external-read`: read-only provider evidence; no acknowledgements, comments, labels, configuration, remediation, deploy, rollback, or closure.
- `artifact-write-local-exec-external-read`: provider and local checks may write bounded evidence artifacts only; product/provider state remains unchanged.
- `local-exec-external-read`: preflight and readiness only; no remote or source mutation.
- `read-only`: analysis and recommendations only.
- `workspace-write*`: only declared local contracts, packaging, or documentation; no implicit Git/provider action.
- `local-system-write-authorized-only`: project-local learning store only, with privacy, retention, deletion, backup, rollback, and no external sync.

## Required Semantic Gates

Each candidate must provide exact provenance and prior tree identities, hand-authored responsibility/procedure/gate, exact mutation scope, two positive triggers, two adjacent anti-triggers, one boundary, one authority stop, two separate holdouts, one semantic mutation, and planned/not-run evaluation.

The set must enforce:

- package before push; push before PR change; readiness before merge; merge authorization does not authorize deploy;
- deployment preflight, trigger, observation, and rollback use different identities;
- observation cannot mutate production; rollback cannot invent a target or proceed without incident/release authority and current recovery evidence;
- deployment target, artifact digest, configuration version, environment, identity, region/cluster, budget/blast radius, health criteria, timeout, cancellation, and rollback are explicit;
- observability configuration records data classes, sampling, redaction, retention, cost, access, cardinality, and deletion;
- source metadata and release identity permit correlation but never leak source, PII, credentials, or secret values;
- canary baselines are immutable artifacts; production canary decisions use current read-only evidence and do not auto-promote or rollback;
- incident coordination preserves timeline, hypotheses, commands, ownership, communication, safety, and decision logs without performing specialist fixes;
- retrospectives are blameless, evidence-linked, owner/deadline bound, and cannot rewrite the incident record;
- feedback recommendations and local persistence remain separate; persistence cannot make unverified inferences canonical.

## Remote and Production Boundary

Phase 7 construction, compilation, Gates, tests, semantic review, and reporting execute no remote/provider/production action. No credentials or secret values enter candidate artifacts. Every remote candidate must explicitly state `not-executed-phase-7`; no provider receipt, production observation, deploy status, merge status, rollback status, or incident-system mutation may be fabricated.

## Verification

The Phase 7 Gate must fail closed on:

- Phase 2–6 tree drift;
- ownership, provenance, baseline, hash, schema, trigger, or holdout mismatch;
- remote, external-read, artifact-only, preflight, workspace, or local-system scope drift;
- remote candidate without exact target, per-action authorization, immutable input, idempotency, receipt, and recovery markers;
- observation or assessment with mutation authority;
- rollback merged with observation or incident coordination;
- preflight claiming push, merge, or deploy;
- deployment candidate claiming execution;
- missing observability governance, canary, incident, retrospective, or learning markers;
- false Phase 9 or release evidence;
- unresolved semantic review findings.

## Outputs

- 39 candidate Skill packages.
- Three review-batch ledgers, schemas, holdouts, semantic review, Gate, mutation tests, manifest, and phase report.
- Unified runner update after directed tests pass.

## Stop Conditions

Stop on prior-phase drift, ambiguous production/provider authority, any request to execute a remote or production action, credential exposure, missing rollback or blast-radius control, unsafe incident action, missing telemetry governance, or semantic ambiguity that merges preflight, change, observation, rollback, incident, and learning identities.
