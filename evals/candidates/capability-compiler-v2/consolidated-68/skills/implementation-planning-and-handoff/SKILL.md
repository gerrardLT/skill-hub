---
name: implementation-planning-and-handoff
description: "Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code. Use when An approved spec needs a step-by-step implementation plan that an engineer with no project context could execute; Tasks must be split into reviewable slices with exact files, tests and verification commands. Do not use for: Clarify ambiguous product requirements before planning (-> requirements-and-delivery-contract); Execute the approved implementation tasks (-> plan-execution-control)."
---

# Implementation Planning And Handoff

## Responsibility

Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code.

## Trigger

Use when the request matches any of:
- An approved spec needs a step-by-step implementation plan that an engineer with no project context could execute
- Tasks must be split into reviewable slices with exact files, tests and verification commands

Do not use when:
- Clarify ambiguous product requirements before planning. Route to `requirements-and-delivery-contract`.
- Execute the approved implementation tasks. Route to `plan-execution-control`.

## Required Inputs

- A confirmed specification, architecture boundaries, repository conventions, and test requirements.

## Procedure

1. Verify approved requirements, architecture, UX decisions, constraints, and unresolved blockers.
2. Map each task to requirement IDs, interfaces, affected areas, test evidence, and completion criteria.
3. Give every task its exact files, a failing test step first, and a verification command with the expected result; mark unverified paths as assumptions.
4. Order tasks by dependency, risk retirement, migration safety, and integration points.
5. Size tasks to independently reviewable changes; preserve rollback and observability work.
6. Emit handoff artifacts, blocked prerequisites, and review checkpoints.

## Domain Guidance

- Write for a zero-context engineer: every task names exact files (create, modify with line range, test file), the behavior to implement and the exact verification command with its expected output.
- Each task starts with a failing test step, then the minimal change, then the verification run. Paths come from the repository as supplied; an unverified path is labeled assumption.
- Map every task to requirement ids and order by dependency, risk retirement and migration safety.
- Validate every referenced task id against the actual plan. Explicitly identify missing/null data and undefined boundary semantics before handing off implementation; do not invent task ids.

## Output Contract

Produce:
- implementation plan
- requirement-task traceability
- dependency graph
- verification handoffs
- per-task file list, failing-test-first step and exact verification command

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not plan around unresolved product behavior, invent file paths as facts, or execute source changes.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `requirements-and-delivery-contract`
- `workflow-orchestration-and-lifecycle`
- `plan-execution-control`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
