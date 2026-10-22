---
name: data-and-api-contract-design
description: "Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation. Use when A feature needs its data schema, API shapes, migration and compatibility rules defined before coding; Someone asks for concrete DDL, request and response examples, error shapes, pagination, idempotency and concurrency rules. Do not use for: Implement the approved API handlers, persistence code, and tests (-> tdd-change-loop); Define who may perform each resource action and the tenant-isolation policy (-> authorization-and-permission-contracts)."
---

# Data And API Contract Design

## Responsibility

Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation.

## Trigger

Use when the request matches any of:
- A feature needs its data schema, API shapes, migration and compatibility rules defined before coding
- Someone asks for concrete DDL, request and response examples, error shapes, pagination, idempotency and concurrency rules

Do not use when:
- Implement the approved API handlers, persistence code, and tests. Route to `tdd-change-loop`.
- Define who may perform each resource action and the tenant-isolation policy. Route to `authorization-and-permission-contracts`.

## Required Inputs

- Approved requirements, domain entities, existing persistence and interfaces, consistency needs, and compatibility constraints.

## Procedure

1. Freeze requirements, consumers, data owners, volumes, consistency, lifecycle, privacy, compatibility window, availability, and authorization dependencies.
2. Define entities, types, identifiers, nullability, invariants, relationships, indexes, retention, deletion, tenancy, and audit fields.
3. Specify expand-migrate-contract steps, backfill, dual-read or write if needed, verification, failure recovery, rollback limits, and irreversible boundaries.
4. Define endpoint or event shapes, validation, errors, status semantics, pagination or streaming, filtering, versioning, rate or size limits, idempotency, retries, ordering, and optimistic concurrency.
5. Provide contract examples and compatibility, property, negative, migration, and authorization test plans; do not implement or mutate data.

## Domain Guidance

- Deliver concrete artifacts, not descriptions: actual DDL or schema files and at least one request and response example per endpoint, close enough that the implementer makes no design decisions.
- This Skill owns migration design (expand, migrate, contract, backfill, rollback limits); applying the migration in code routes to tdd-change-loop.

## Output Contract

Produce:
- versioned data schema and invariant contract
- migration, backfill, verification, and rollback plan
- API or event interface schema
- compatibility, idempotency, concurrency, and test matrix
- concrete DDL or schema files and a request and response example per endpoint

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `authorization-and-permission-contracts`
- `architecture-deep-module-design`
- `tdd-change-loop`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
