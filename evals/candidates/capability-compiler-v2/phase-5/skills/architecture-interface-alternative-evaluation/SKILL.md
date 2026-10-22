---
name: architecture-interface-alternative-evaluation
description: Generate at least two independent interface alternatives and compare information hiding, caller complexity, dependencies, failure behavior, testability, compatibility, and migration cost. Do not use for design the full chosen module boundary, dependency direction, seams, and test plan or format already-developed candidates into the final architecture decision report.
---

# Architecture Interface Alternative Evaluation

## Responsibility

Generate at least two independent interface alternatives and compare information hiding, caller complexity, dependencies, failure behavior, testability, compatibility, and migration cost.

## Trigger

Use when the requested outcome is: Generate at least two independent interface alternatives and compare information hiding, caller complexity, dependencies, failure behavior, testability, compatibility, and migration cost.

Do not use when:
- Design the full chosen module boundary, dependency direction, seams, and test plan. Route to `architecture-deep-module-design`.
- Format already-developed candidates into the final architecture decision report. Route to `architecture-candidate-reporting`.

## Required Inputs

- A bounded module problem, constraints, and an interface-design objective.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the problem, callers, invariants, constraints, compatibility needs, and evaluation criteria before ideation.
2. Generate at least two structurally independent alternatives rather than renamed signatures over the same boundary.
3. Specify each alternative's contract, hidden and exposed knowledge, dependencies, failure and concurrency semantics, tests, compatibility, migration, and rollback.
4. Compare with declared evidence and sensitivity, including a minimal-change or no-change option where valid.
5. Recommend or abstain for a named human owner; do not implement or silently choose based on taste.

## Output Contract

Produce:
- independent interface alternatives
- contract and failure comparison
- migration and compatibility matrix
- human-owned recommendation

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `independent-alternatives`
- `information-hiding`
- `caller-complexity`
- `failure-semantics`
- `compatibility`
- `migration`

## Hard Gates

- Alternatives must differ in responsibility boundary or information hiding; cosmetic signature variants do not satisfy divergent architecture evaluation.
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
- `architecture-deep-module-design`
- `architecture-candidate-reporting`
- `data-and-api-contract-design`
- `engineering-plan-review`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
