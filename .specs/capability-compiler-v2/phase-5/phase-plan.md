# Capability Compiler V2 — Phase 5 Plan

## Objective

Rewrite the 16 Phase 5 architecture, data/API, authorization, secrets, CI-security, frontend-boundary, AI-autonomy, and threat-model taxonomy capabilities into atomic, provenance-complete candidate Skills. Do not assemble a cross-domain architecture or security Recipe in this phase; conditional lifecycle orchestration remains Phase 8 work.

## Frozen Inputs

- Phase 2 artifact tree SHA-256: `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`
- Phase 3 artifact tree SHA-256: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 artifact tree SHA-256: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase ownership: exactly 16 IDs in `curation/v2/lifecycle/phase-ownership.json` phase `5`.
- Source Skills and V1 released Slots/Recipes remain immutable.

## Candidate Location

- `evals/candidates/capability-compiler-v2/phase-5/skills/<capability-id>/`
- Version: `0.1.0-v2-candidate`
- Status: `evaluating`
- Evaluation state: `not-run-phase-9`

## Atomic Boundaries

The phase must preserve these separations:

- architecture discovery, candidate reporting, deep module design, interface alternatives, diagrams, engineering review, and implementation planning are different responsibilities;
- data/API contract design specifies schemas, compatibility, validation, idempotency, errors, pagination, concurrency, and migration without implementing handlers or mutating production data;
- authorization contracts define subject/resource/action/context policy, deny behavior, tenancy, service identities, audit, and verification without provisioning credentials or changing provider policy;
- secrets/environment governance defines classification, ownership, injection, rotation, revocation, logging/redaction, and incident handling without reading or emitting secret values;
- threat modeling and audit report trust boundaries, abuse cases, findings, evidence, and remediation priorities without repairing source;
- CI hardening may edit only authorized workflow/config source and must pin authority, permissions, secret exposure, untrusted input, artifact provenance, and rollback behavior;
- frontend runtime boundaries may edit only authorized project source and must prevent server-only code, credentials, privileged actions, and unsafe dependency behavior from crossing into clients;
- AI capability, model/data architecture, autonomy/human control, and safety/action governance remain separate; no recommendation may activate tools, grant autonomy, expose data, or approve high-impact actions.

## Required Gates

Every candidate must include:

1. exact Phase 2 provenance sets and frozen Phase 2–4 artifact identities;
2. two positive triggers, two adjacent anti-triggers, one concrete boundary case, one authority-stop case, and two separate holdouts;
3. one distinctive semantic mutation and `not-run-phase-9` evaluation plan;
4. precise mutation scope independent of broad permission identity;
5. explicit trust-boundary, migration/reversibility, compatibility, verification, human-approval, or data-governance markers where applicable;
6. fail-closed status mapping and no remote write.

## Security Invariants

- Never request, print, persist, hash into evidence, or transmit secret values.
- Never treat authentication as authorization.
- Default deny when subject, resource, action, context, tenancy, or policy version is absent.
- Never let client code hold server credentials or privileged authorization decisions.
- Never let untrusted CI input execute in a privileged context or expose secrets.
- Never approve AI autonomy from capability availability; constrain tools, data, action class, spend, reversibility, observation, interruption, and human checkpoints.
- Threat findings require reproducible evidence and severity rationale; audit is not remediation.
- Architecture recommendations remain proposals until a named human owner approves the decision.

## Verification

Phase 5 Gate must fail closed on:

- Phase 2–4 artifact drift;
- missing/extra candidates or ownership mismatch;
- provenance or candidate hash drift;
- trigger/holdout leakage or unknown routes;
- a review/audit/reporting capability with source mutation;
- a source-editing capability hidden behind run-output-only scope;
- secret-value handling, remote-write authority, production mutation, or autonomous provider actions;
- missing authorization default-deny, data/API compatibility and idempotency, CI untrusted-input, frontend server/client, threat-boundary, AI human-control, or migration/reversibility markers;
- any evaluation plan claiming execution;
- unresolved semantic review findings.

## Outputs

- 16 candidate Skill packages.
- Phase 5 schemas, semantic-design ledger, holdout corpus, semantic review, Gate, mutation tests, artifact manifest, and phase report.
- Unified runner updated only after directed tests pass.

## Stop Conditions

Stop on prior-phase identity drift, source mutation, unresolved security-policy conflict, missing authority for any real system mutation, any need to access secret values, or ambiguity that changes trust boundaries, data migration, autonomy, or authorization semantics.
