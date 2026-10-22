---
name: secrets-and-environment-governance
description: "Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values. Use when A system needs rules for where secrets live, how they reach runtime and CI, how they rotate and how a leak is handled; A secret may have leaked into logs or a repository and the response order is unclear. Do not use for: Define which actors may perform resource actions and where authorization is enforced (-> authorization-and-permission-contracts); Patch the CI workflow's secret exposure and untrusted-input vulnerabilities (-> ci-pipeline-security-hardening)."
---

# Secrets And Environment Governance

## Responsibility

Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values.

## Trigger

Use when the request matches any of:
- A system needs rules for where secrets live, how they reach runtime and CI, how they rotate and how a leak is handled
- A secret may have leaked into logs or a repository and the response order is unclear

Do not use when:
- Define which actors may perform resource actions and where authorization is enforced. Route to `authorization-and-permission-contracts`.
- Patch the CI workflow's secret exposure and untrusted-input vulnerabilities. Route to `ci-pipeline-security-hardening`.

## Required Inputs

- Secret classes, environments, providers, CI/runtime paths, owners, rotation requirements, and authorization.

## Procedure

1. Freeze secret and credential classes by name only, environments, owners, consumers, providers, trust boundaries, compliance constraints, and rotation requirements.
2. Map creation, storage class, injection, access, transit, logging, output, cache, artifact, backup, retention, and deletion paths without requesting or recording values.
3. Define least-exposure identities, environment separation, local development substitutes, redaction, scanning, rotation, revocation, and break-glass approval.
4. Specify leak detection, containment, revocation order, dependent-service recovery, evidence retention, and notification ownership.
5. Return a verification plan that checks names, references, policy, access metadata, and behavior without reading or hashing secret values.

## Domain Guidance

- Leak-path examples to map: shell tracing (set -x) in steps that touch secrets, printing environment variables, untrusted multiline data written to the CI environment or output files, secrets passed to steps that run untrusted code or third-party actions, and tokens in request headers that end up in logs.

## Output Contract

Produce:
- secrets and environment contract
- least-exposure and redaction map
- rotation and revocation procedure
- leak-response and value-free verification plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `authorization-and-permission-contracts`
- `ci-pipeline-security-hardening`
- `security-audit-and-threat-modeling`
- `frontend-runtime-boundaries-and-dependency-safety`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
