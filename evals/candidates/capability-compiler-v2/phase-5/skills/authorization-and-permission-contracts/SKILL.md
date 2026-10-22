---
name: authorization-and-permission-contracts
description: Define and verify subject, resource, action, context, tenancy, privileged-path, service-identity, audit, and default-deny authorization contracts. Do not use for define secret storage, injection, rotation, revocation, and environment boundaries or audit the whole application and infrastructure for threat paths and exploitable findings.
---

# Authorization And Permission Contracts

## Responsibility

Define and verify subject, resource, action, context, tenancy, privileged-path, service-identity, audit, and default-deny authorization contracts.

## Trigger

Use when the requested outcome is: Define and verify subject, resource, action, context, tenancy, privileged-path, service-identity, audit, and default-deny authorization contracts.

Do not use when:
- Define secret storage, injection, rotation, revocation, and environment boundaries. Route to `secrets-and-environment-governance`.
- Audit the whole application and infrastructure for threat paths and exploitable findings. Route to `security-audit-and-threat-modeling`.

## Required Inputs

- Actors, resources, operations, trust boundaries, tenancy model, authentication context, and risk policy.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze actors and service identities, authentication evidence, resources, ownership, actions, context, tenancy, delegation, policy versions, and compliance constraints.
2. Build subject-resource-action-context rules with explicit allow conditions, default deny, tenant isolation, privileged paths, impersonation or support access, and break-glass boundaries.
3. Place enforcement at every trust boundary and prevent client claims, hidden UI, or authentication alone from authorizing server actions.
4. Define negative cases for cross-tenant, stale role, confused deputy, indirect object reference, bulk, background, export, and ownership-transfer paths.
5. Specify policy versioning, audit events, review, revocation, migration, and verification without provisioning identities or changing live policy.

## Output Contract

Produce:
- authorization policy matrix
- trust-boundary enforcement map
- negative authorization test contract
- audit, migration, and residual-risk ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `subject-resource-action-context`
- `default-deny`
- `tenant-isolation`
- `server-enforcement`
- `negative-cases`
- `audit`
- `policy-migration`

## Hard Gates

- Authentication is not authorization: any missing or untrusted subject, resource, action, context, tenancy, ownership, or policy version must fail closed at a server-side enforcement point.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `secrets-and-environment-governance`
- `security-audit-and-threat-modeling`
- `data-and-api-contract-design`
- `ai-agent-autonomy-and-human-control`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
