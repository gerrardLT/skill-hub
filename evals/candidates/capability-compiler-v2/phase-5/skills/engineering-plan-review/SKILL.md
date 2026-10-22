---
name: engineering-plan-review
description: Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it. Do not use for write or revise the implementation plan and work breakdown or perform a source and runtime threat audit of the actual system.
---

# Engineering Plan Review

## Responsibility

Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it.

## Trigger

Use when the requested outcome is: Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it.

Do not use when:
- Write or revise the implementation plan and work breakdown. Route to `implementation-planning-and-handoff`.
- Perform a source and runtime threat audit of the actual system. Route to `security-audit-and-threat-modeling`.

## Required Inputs

- Approved requirements, plan, architecture context, constraints, and existing system evidence.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the plan, approved requirements and design, target source identity, constraints, risk tolerance, and review scope.
2. Trace each requirement and design decision to plan steps, interfaces, data changes, tests, migration, rollout, and rollback.
3. Review dependency direction, failure behavior, concurrency, authorization, secrets, operability, performance, compatibility, and ownership.
4. Cite missing, contradictory, infeasible, untestable, risky, or unnecessary work with consequence and bounded recommendation.
5. Return findings, alternatives, residual risk, and approve-revise-block recommendation to the human owner without editing the plan or source.

## Output Contract

Produce:
- independent engineering review
- traceability and risk findings
- missing-test and rollback register
- human-owned review recommendation

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `traceability`
- `architecture`
- `data-migration`
- `authorization`
- `failure-modes`
- `operability`
- `rollback`
- `verification`

## Hard Gates

- A plan cannot pass on completeness of prose: every material architecture, data, security, migration, failure, and verification claim must trace to approved intent and an executable evidence path.
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

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `implementation-planning-and-handoff`
- `independent-plan-review`
- `security-audit-and-threat-modeling`
- `plan-review-decision-synthesis`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
