---
name: workflow-orchestration-and-lifecycle
description: "Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work. Use when A request needs a workflow composed from several capabilities and no existing Recipe covers it; A multi-stage effort needs typed handoffs, gates and invalidation rules defined before execution. Do not use for: Execute these implementation tasks in the workspace (-> plan-execution-control); Classify a single vague request and choose only the next capability (-> context-intake-and-routing)."
---

# Workflow Orchestration And Lifecycle

## Responsibility

Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.

## Trigger

Use when the request matches any of:
- A request needs a workflow composed from several capabilities and no existing Recipe covers it
- A multi-stage effort needs typed handoffs, gates and invalidation rules defined before execution

Do not use when:
- Execute these implementation tasks in the workspace. Route to `plan-execution-control`.
- Classify a single vague request and choose only the next capability. Route to `context-intake-and-routing`.

## Required Inputs

- A request, phase state, available capabilities, and execution constraints.

## Procedure

1. Read request, current lifecycle state, artifact identities, available capability contracts, permissions, and stop conditions.
2. Check the released Recipes and router first; if one matches, return its id instead of composing a new workflow.
3. Select the smallest applicable capabilities and conditional branches; omit non-applicable stages with reasons.
4. Construct typed handoffs, authority transitions, feedback edges, and evidence invalidation rules.
5. Advance only on machine and human gates; stop on incompatible permissions or stale evidence.
6. Emit workflow state and next action without executing any selected capability.

## Domain Guidance

- Reuse first: if an existing stage, composite or specialized Recipe matches the request, name it and stop; design a new workflow only for the uncovered remainder.
- The router owns Recipe selection; this Skill plans only what the released Recipes do not cover and never executes a selected capability.
- Routing ownership: use only when no Recipe covers the workflow; the router selects Recipes and context-intake-and-routing classifies requests.
- Missing action authorization is not a broader prohibition. Do not invent bans on cloud mutation, external writes or downstream capabilities beyond supplied policy.

## Output Contract

Produce:
- workflow graph
- routing decisions
- typed handoffs
- state and invalidation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Orchestration may route, stop, retry, or invalidate, but must never impersonate a selected capability or merge incompatible execution identities.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `context-intake-and-routing`
- `implementation-planning-and-handoff`
- `plan-execution-control`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
