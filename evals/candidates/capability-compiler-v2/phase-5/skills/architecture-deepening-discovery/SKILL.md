---
name: architecture-deepening-discovery
description: Find evidence-backed shallow modules, leaked boundaries, repeated orchestration, and change hotspots, and recommend deepen or leave unchanged under YAGNI. Do not use for design the selected module's exact boundary, interface, seams, migration, and tests or review an implementation plan for architecture, data, failure, security, and operability gaps.
---

# Architecture Deepening Discovery

## Responsibility

Find evidence-backed shallow modules, leaked boundaries, repeated orchestration, and change hotspots, and recommend deepen or leave unchanged under YAGNI.

## Trigger

Use when the requested outcome is: Find evidence-backed shallow modules, leaked boundaries, repeated orchestration, and change hotspots, and recommend deepen or leave unchanged under YAGNI.

Do not use when:
- Design the selected module's exact boundary, interface, seams, migration, and tests. Route to `architecture-deep-module-design`.
- Review an implementation plan for architecture, data, failure, security, and operability gaps. Route to `engineering-plan-review`.

## Required Inputs

- A codebase, change hotspots, repeated logic, and maintenance-friction evidence.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze repository scope, observed maintenance pain, change history, ownership, incidents, repeated logic, and excluded areas.
2. Trace callers and dependencies for shallow delegation, knowledge leakage, repeated orchestration, unstable interfaces, and coupled changes.
3. Quantify or cite friction, frequency, blast radius, and existing test seams; distinguish style dislike from maintenance evidence.
4. Generate bounded candidates and a leave-unchanged option with expected benefit, migration cost, risk, and evidence gaps.
5. Rank investigation priority without designing or implementing modules; reject speculative abstractions.

## Output Contract

Produce:
- architecture friction inventory
- deepening candidate register
- YAGNI leave-unchanged cases
- evidence and priority report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `shallow-module`
- `boundary-leak`
- `change-coupling`
- `maintenance-evidence`
- `YAGNI`
- `leave-unchanged`

## Hard Gates

- No deepening candidate passes on aesthetics or hypothetical reuse alone; it needs cited recurring friction, boundary leakage, change coupling, or operational cost that exceeds migration risk.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `architecture-deep-module-design`
- `architecture-interface-alternative-evaluation`
- `architecture-candidate-reporting`
- `engineering-plan-review`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
