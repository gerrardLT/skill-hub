---
name: data-and-api-contract-design
description: Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation. Do not use for implement the approved api handlers, persistence code, and tests or define who may perform each resource action and the tenant-isolation policy.
---

# Data And Api Contract Design

## Responsibility

Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation.

## Trigger

Use when the requested outcome is: Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation.

Do not use when:
- Implement the approved API handlers, persistence code, and tests. Route to `tdd-change-loop`.
- Define who may perform each resource action and the tenant-isolation policy. Route to `authorization-and-permission-contracts`.

## Required Inputs

- Approved requirements, domain entities, existing persistence and interfaces, consistency needs, and compatibility constraints.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze requirements, consumers, data owners, volumes, consistency, lifecycle, privacy, compatibility window, availability, and authorization dependencies.
2. Define entities, types, identifiers, nullability, invariants, relationships, indexes, retention, deletion, tenancy, and audit fields.
3. Specify expand-migrate-contract steps, backfill, dual-read or write if needed, verification, failure recovery, rollback limits, and irreversible boundaries.
4. Define endpoint or event shapes, validation, errors, status semantics, pagination or streaming, filtering, versioning, rate or size limits, idempotency, retries, ordering, and optimistic concurrency.
5. Provide contract examples and compatibility, property, negative, migration, and authorization test plans; do not implement or mutate data.

## Output Contract

Produce:
- versioned data schema and invariant contract
- migration, backfill, verification, and rollback plan
- API or event interface schema
- compatibility, idempotency, concurrency, and test matrix

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `schema-invariants`
- `migration`
- `compatibility`
- `validation-errors`
- `pagination`
- `idempotency`
- `concurrency`
- `authorization-hooks`
- `rollback`

## Hard Gates

- No contract passes without explicit compatibility, idempotency or retry behavior, concurrency semantics, validation and error shapes, authorization hooks, and a verified migration path with rollback or declared point of no return.
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
- `authorization-and-permission-contracts`
- `architecture-deep-module-design`
- `tdd-change-loop`
- `schema-migration-safety`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
