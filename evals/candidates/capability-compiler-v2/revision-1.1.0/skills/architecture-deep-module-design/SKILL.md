---
name: architecture-deep-module-design
description: "Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification. Use when One module needs a smaller, deeper interface that hides complexity with a migration path; Callers know too much about a module and someone must redesign its boundary without rewriting everything. Do not use for: Scan the codebase for evidence-backed module-deepening opportunities (-> architecture-deepening-discovery); Generate at least two independent interface alternatives and compare them before choosing (-> architecture-interface-alternative-evaluation)."
---

# Architecture Deep Module Design

## Responsibility

Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification.

## Trigger

Use when the request matches any of:
- One module needs a smaller, deeper interface that hides complexity with a migration path
- Callers know too much about a module and someone must redesign its boundary without rewriting everything

Do not use when:
- Scan the codebase for evidence-backed module-deepening opportunities. Route to `architecture-deepening-discovery`.
- Generate at least two independent interface alternatives and compare them before choosing. Route to `architecture-interface-alternative-evaluation`.

## Required Inputs

- A module, its interfaces and dependencies, or evidenced architectural friction.

## Procedure

1. Freeze the module responsibility, callers, dependencies, data ownership, invariants, failure modes, change history, tests, and observed friction.
2. Identify what complexity must be hidden versus exposed as stable policy and reject boundaries based only on file layout or naming.
3. Define the smallest coherent interface, invariants, ownership, dependency direction, seams, failure behavior, and observability.
4. Map old-to-new behavior, compatibility, incremental migration, rollback, and affected tests without implementing the change.
5. Challenge the design for leakage, shallow delegation, temporal coupling, test fragility, and speculative extensibility before recommendation.

## Domain Guidance

- Testability rules for the challenge step: accept dependencies instead of creating them inside the module, and return results instead of producing side effects, so the interface can be tested without mocking internals.

## Output Contract

Produce:
- deep-module boundary
- interface and invariant contract
- dependency and seam map
- compatibility, migration, rollback, and test plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `information-hiding`
- `deep-module`
- `interface`
- `invariants`
- `dependency-direction`
- `seams`
- `migration-rollback`

## Hard Gates

- A module is not deeper merely because code moved: the proposed interface must hide material complexity, reduce caller knowledge, preserve behavior, and have an incremental migration and rollback path.
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

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `architecture-deepening-discovery`
- `architecture-interface-alternative-evaluation`
- `data-and-api-contract-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
