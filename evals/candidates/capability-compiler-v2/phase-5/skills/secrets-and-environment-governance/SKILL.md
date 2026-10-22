---
name: secrets-and-environment-governance
description: Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values. Do not use for define which actors may perform resource actions and where authorization is enforced or patch the ci workflow's secret exposure and untrusted-input vulnerabilities.
---

# Secrets And Environment Governance

## Responsibility

Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values.

## Trigger

Use when the requested outcome is: Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values.

Do not use when:
- Define which actors may perform resource actions and where authorization is enforced. Route to `authorization-and-permission-contracts`.
- Patch the CI workflow's secret exposure and untrusted-input vulnerabilities. Route to `ci-pipeline-security-hardening`.

## Required Inputs

- Secret classes, environments, providers, CI/runtime paths, owners, rotation requirements, and authorization.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze secret and credential classes by name only, environments, owners, consumers, providers, trust boundaries, compliance constraints, and rotation requirements.
2. Map creation, storage class, injection, access, transit, logging, output, cache, artifact, backup, retention, and deletion paths without requesting or recording values.
3. Define least-exposure identities, environment separation, local development substitutes, redaction, scanning, rotation, revocation, and break-glass approval.
4. Specify leak detection, containment, revocation order, dependent-service recovery, evidence retention, and notification ownership.
5. Return a verification plan that checks names, references, policy, access metadata, and behavior without reading or hashing secret values.

## Output Contract

Produce:
- secrets and environment contract
- least-exposure and redaction map
- rotation and revocation procedure
- leak-response and value-free verification plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `no-secret-values`
- `environment-separation`
- `least-exposure`
- `redaction`
- `rotation`
- `revocation`
- `leak-response`

## Hard Gates

- Secret values must never be requested, read, printed, copied, transformed, hashed into evidence, persisted, or sent to a model; verification uses names, references, metadata, policy, and behavior only.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `authorization-and-permission-contracts`
- `ci-pipeline-security-hardening`
- `security-audit-and-threat-modeling`
- `frontend-runtime-boundaries-and-dependency-safety`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
