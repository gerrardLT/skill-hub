---
name: authorization-and-permission-contracts
description: "Consolidated capability with 2 selectable modes: authorization-and-permission-contracts; secrets-and-environment-governance. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [authorization-and-permission-contracts, secrets-and-environment-governance]
---

# Authorization And Permission Contracts

## Responsibility

Consolidated capability covering 2 related modes: Define and verify subject, resource, action, context, tenancy, privileged-path, service-identity, audit, and default-deny authorization contracts.; Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `authorization-and-permission-contracts` | `workspace-write` | A system needs an explicit who-can-do-what rule set including tenants, service identities and privileged paths; Someone asks for the negative authorization tests and enforcement points before access c | Define secret storage, injection, rotation, revocation, and environment boundaries (-> secrets-and-environment-governanc |
| `secrets-and-environment-governance` | `workspace-write` | A system needs rules for where secrets live, how they reach runtime and CI, how they rotate and how a leak is handled; A secret may have leaked into logs or a repository and the response order is uncl | Define which actors may perform resource actions and where authorization is enforced (-> authorization-and-permission-co |

## Mode: `authorization-and-permission-contracts`

### authorization-and-permission-contracts

#### Responsibility

Define and verify subject, resource, action, context, tenancy, privileged-path, service-identity, audit, and default-deny authorization contracts.

#### Trigger

Use when the request matches any of:
- A system needs an explicit who-can-do-what rule set including tenants, service identities and privileged paths
- Someone asks for the negative authorization tests and enforcement points before access control is built or changed

Do not use when:
- Define secret storage, injection, rotation, revocation, and environment boundaries. Route to `secrets-and-environment-governance`.
- Audit the whole application and infrastructure for threat paths and exploitable findings. Route to `security-audit-and-threat-modeling`.

#### Required Inputs

- Actors, resources, operations, trust boundaries, tenancy model, authentication context, and risk policy.

#### Procedure

1. Freeze actors and service identities, authentication evidence, resources, ownership, actions, context, tenancy, delegation, policy versions, and compliance constraints.
2. Build subject-resource-action-context rules with explicit allow conditions, default deny, tenant isolation, privileged paths, impersonation or support access, and break-glass boundaries.
3. Place enforcement at every trust boundary and prevent client claims, hidden UI, or authentication alone from authorizing server actions.
4. Define negative cases for cross-tenant, stale role, confused deputy, indirect object reference, bulk, background, export, and ownership-transfer paths.
5. Specify policy versioning, audit events, review, revocation, migration, and verification without provisioning identities or changing live policy.

#### Domain Guidance

- Map each rule to the matching access-control requirement in the project's chosen standard (for example OWASP ASVS V4) and name the server-side enforcement point for every rule.

#### Output Contract

Produce:
- authorization policy matrix
- trust-boundary enforcement map
- negative authorization test contract
- audit, migration, and residual-risk ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `subject-resource-action-context`
- `default-deny`
- `tenant-isolation`
- `server-enforcement`
- `negative-cases`
- `audit`
- `policy-migration`

#### Hard Gates

- Authentication is not authorization: any missing or untrusted subject, resource, action, context, tenancy, ownership, or policy version must fail closed at a server-side enforcement point.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `secrets-and-environment-governance`
- `security-audit-and-threat-modeling`
- `data-and-api-contract-design`
- `ai-agent-autonomy-and-human-control`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `secrets-and-environment-governance`

### secrets-and-environment-governance

#### Responsibility

Define secret classes, owners, environment boundaries, injection, least exposure, logging and redaction, rotation, revocation, retention, and incident procedures without accessing values.

#### Trigger

Use when the request matches any of:
- A system needs rules for where secrets live, how they reach runtime and CI, how they rotate and how a leak is handled
- A secret may have leaked into logs or a repository and the response order is unclear

Do not use when:
- Define which actors may perform resource actions and where authorization is enforced. Route to `authorization-and-permission-contracts`.
- Patch the CI workflow's secret exposure and untrusted-input vulnerabilities. Route to `ci-pipeline-security-hardening`.

#### Required Inputs

- Secret classes, environments, providers, CI/runtime paths, owners, rotation requirements, and authorization.

#### Procedure

1. Freeze secret and credential classes by name only, environments, owners, consumers, providers, trust boundaries, compliance constraints, and rotation requirements.
2. Map creation, storage class, injection, access, transit, logging, output, cache, artifact, backup, retention, and deletion paths without requesting or recording values.
3. Define least-exposure identities, environment separation, local development substitutes, redaction, scanning, rotation, revocation, and break-glass approval.
4. Specify leak detection, containment, revocation order, dependent-service recovery, evidence retention, and notification ownership.
5. Return a verification plan that checks names, references, policy, access metadata, and behavior without reading or hashing secret values.

#### Domain Guidance

- Leak-path examples to map: shell tracing (set -x) in steps that touch secrets, printing environment variables, untrusted multiline data written to the CI environment or output files, secrets passed to steps that run untrusted code or third-party actions, and tokens in request headers that end up in logs.

#### Output Contract

Produce:
- secrets and environment contract
- least-exposure and redaction map
- rotation and revocation procedure
- leak-response and value-free verification plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `no-secret-values`
- `environment-separation`
- `least-exposure`
- `redaction`
- `rotation`
- `revocation`
- `leak-response`

#### Hard Gates

- Secret values must never be requested, read, printed, copied, transformed, hashed into evidence, persisted, or sent to a model; verification uses names, references, metadata, policy, and behavior only.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `authorization-and-permission-contracts`
- `ci-pipeline-security-hardening`
- `security-audit-and-threat-modeling`
- `frontend-runtime-boundaries-and-dependency-safety`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
