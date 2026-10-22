---
name: implementation-planning-and-handoff
description: Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code. Do not use for clarify ambiguous product requirements before planning or execute the approved implementation tasks.
---

# Implementation Planning And Handoff

## Responsibility

Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code.

## Trigger

Use when the requested outcome is: Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code.

Do not use when:
- Clarify ambiguous product requirements before planning. Route to `requirements-and-delivery-contract`.
- Execute the approved implementation tasks. Route to `plan-execution-control`.

## Required Inputs

- A confirmed specification, architecture boundaries, repository conventions, and test requirements.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify approved requirements, architecture, UX decisions, constraints, and unresolved blockers.
2. Map each task to requirement IDs, interfaces, affected areas, test evidence, and completion criteria.
3. Order tasks by dependency, risk retirement, migration safety, and integration points.
4. Size tasks to independently reviewable changes; preserve rollback and observability work.
5. Emit handoff artifacts, blocked prerequisites, and review checkpoints.

## Output Contract

Produce:
- implementation plan
- requirement-task traceability
- dependency graph
- verification handoffs

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not plan around unresolved product behavior, invent file paths as facts, or execute source changes.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `requirements-and-delivery-contract`
- `workflow-orchestration-and-lifecycle`
- `plan-execution-control`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
