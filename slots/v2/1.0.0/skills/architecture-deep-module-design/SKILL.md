---
name: architecture-deep-module-design
description: Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification. Do not use for scan the codebase for evidence-backed module-deepening opportunities or generate at least two independent interface alternatives and compare them before choosing.
---

# Architecture Deep Module Design

## Responsibility

Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification.

## Trigger

Use when the requested outcome is: Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification.

Do not use when:
- Scan the codebase for evidence-backed module-deepening opportunities. Route to `architecture-deepening-discovery`.
- Generate at least two independent interface alternatives and compare them before choosing. Route to `architecture-interface-alternative-evaluation`.

## Required Inputs

- A module, its interfaces and dependencies, or evidenced architectural friction.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the module responsibility, callers, dependencies, data ownership, invariants, failure modes, change history, tests, and observed friction.
2. Identify what complexity must be hidden versus exposed as stable policy and reject boundaries based only on file layout or naming.
3. Define the smallest coherent interface, invariants, ownership, dependency direction, seams, failure behavior, and observability.
4. Map old-to-new behavior, compatibility, incremental migration, rollback, and affected tests without implementing the change.
5. Challenge the design for leakage, shallow delegation, temporal coupling, test fragility, and speculative extensibility before recommendation.

## Output Contract

Produce:
- deep-module boundary
- interface and invariant contract
- dependency and seam map
- compatibility, migration, rollback, and test plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

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
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `architecture-deepening-discovery`
- `architecture-interface-alternative-evaluation`
- `data-and-api-contract-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
