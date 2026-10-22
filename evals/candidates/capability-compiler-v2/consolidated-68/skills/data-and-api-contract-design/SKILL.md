---
name: data-and-api-contract-design
description: "Consolidated capability with 2 selectable modes: data-and-api-contract-design; service-identity-remapping. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [data-and-api-contract-design, service-identity-remapping]
---

# Data And Api Contract Design

## Responsibility

Consolidated capability covering 2 related modes: Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation.; Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `data-and-api-contract-design` | `workspace-write` | A feature needs its data schema, API shapes, migration and compatibility rules defined before coding; Someone asks for concrete DDL, request and response examples, error shapes, pagination, idempotenc | Implement the approved API handlers, persistence code, and tests (-> tdd-change-loop); Define who may perform each resou |
| `service-identity-remapping` | `remote-write-authorized-only` | A telemetry service name must be renamed in the provider without breaking dashboards, monitors and history; Someone asks what a service remap would affect before it is applied. | Define source revision and release metadata carried by telemetry (-> source-metadata-and-provenance); Verify whether ins |

## Mode: `data-and-api-contract-design`

### data-and-api-contract-design

#### Responsibility

Define versioned data schemas, invariants, migration and rollback, API shapes, validation, errors, pagination, idempotency, concurrency, compatibility, and authorization hooks before implementation.

#### Trigger

Use when the request matches any of:
- A feature needs its data schema, API shapes, migration and compatibility rules defined before coding
- Someone asks for concrete DDL, request and response examples, error shapes, pagination, idempotency and concurrency rules

Do not use when:
- Implement the approved API handlers, persistence code, and tests. Route to `tdd-change-loop`.
- Define who may perform each resource action and the tenant-isolation policy. Route to `authorization-and-permission-contracts`.

#### Required Inputs

- Approved requirements, domain entities, existing persistence and interfaces, consistency needs, and compatibility constraints.

#### Procedure

1. Freeze requirements, consumers, data owners, volumes, consistency, lifecycle, privacy, compatibility window, availability, and authorization dependencies.
2. Define entities, types, identifiers, nullability, invariants, relationships, indexes, retention, deletion, tenancy, and audit fields.
3. Specify expand-migrate-contract steps, backfill, dual-read or write if needed, verification, failure recovery, rollback limits, and irreversible boundaries.
4. Define endpoint or event shapes, validation, errors, status semantics, pagination or streaming, filtering, versioning, rate or size limits, idempotency, retries, ordering, and optimistic concurrency.
5. Provide contract examples and compatibility, property, negative, migration, and authorization test plans; do not implement or mutate data.

#### Domain Guidance

- Deliver concrete artifacts, not descriptions: actual DDL or schema files and at least one request and response example per endpoint, close enough that the implementer makes no design decisions.
- This Skill owns migration design (expand, migrate, contract, backfill, rollback limits); applying the migration in code routes to tdd-change-loop.

#### Output Contract

Produce:
- versioned data schema and invariant contract
- migration, backfill, verification, and rollback plan
- API or event interface schema
- compatibility, idempotency, concurrency, and test matrix
- concrete DDL or schema files and a request and response example per endpoint

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `schema-invariants`
- `migration`
- `compatibility`
- `validation-errors`
- `pagination`
- `idempotency`
- `concurrency`
- `authorization-hooks`
- `rollback`

#### Hard Gates

- No contract passes without explicit compatibility, idempotency or retry behavior, concurrency semantics, validation and error shapes, authorization hooks, and a verified migration path with rollback or declared point of no return.
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
- `authorization-and-permission-contracts`
- `architecture-deep-module-design`
- `tdd-change-loop`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `service-identity-remapping`

### service-identity-remapping

#### Responsibility

Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization.

#### Trigger

Use when the request matches any of:
- A telemetry service name must be renamed in the provider without breaking dashboards, monitors and history
- Someone asks what a service remap would affect before it is applied

Do not use when:
- Define source revision and release metadata carried by telemetry. Route to `source-metadata-and-provenance`.
- Verify whether instrumentation already emits the expected service and environment identity. Route to `apm-instrumentation-verification`.

#### Required Inputs

- Current service names, desired taxonomy, provider configuration, downstream dashboards, and authorization.

#### Procedure

1. Verify provider, account or org, environment, old and new identity, source or runtime emitters, collision search, aliases, retention, dashboards, monitors, SLOs, ownership, access, historical continuity, propagation, rollback, and fresh authorization.
2. Preview exact remapping and affected queries, routes, tags, alerts, and integrations; block on collision or ambiguous producers.
3. Perform one bounded provider configuration change without altering instrumentation, unrelated services, or deleting historical data.
4. Record provider receipt, old and new mapping, affected resources, propagation verification, residual gaps, and rollback command or action.

#### Domain Guidance

- Show an impact preview of every monitor and dashboard that references the old name before planning the rule. For an inferred-entity remap, confirm the outbound spans carry peer.service first.

#### Output Contract

Produce:
- service identity remap receipt
- collision and continuity evidence
- affected dashboard, alert, and integration map
- verification and rollback record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `old-new-identity`
- `collision-check`
- `historical-continuity`
- `affected-resources`
- `per-action-authorization`
- `rollback`

#### Hard Gates

- Identity remapping requires collision-free exact old and new identities, bounded provider scope, continuity plan, affected-resource inventory, verification, and rollback; renaming telemetry emitters is separate.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `source-metadata-and-provenance`
- `apm-instrumentation-verification`
- `release-observability-configuration`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
