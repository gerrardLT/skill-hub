---
name: workflow-orchestration-and-lifecycle
description: Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work. Do not use for execute these implementation tasks in the workspace or classify a single vague request and choose only the next capability.
---

# Workflow Orchestration And Lifecycle

## Responsibility

Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.

## Trigger

Use when the requested outcome is: Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.

Do not use when:
- Execute these implementation tasks in the workspace. Route to `plan-execution-control`.
- Classify a single vague request and choose only the next capability. Route to `context-intake-and-routing`.

## Required Inputs

- A request, phase state, available capabilities, and execution constraints.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Read request, current lifecycle state, artifact identities, available capability contracts, permissions, and stop conditions.
2. Select the smallest applicable capabilities and conditional branches; omit non-applicable stages with reasons.
3. Construct typed handoffs, authority transitions, feedback edges, and evidence invalidation rules.
4. Advance only on machine and human gates; stop on incompatible permissions or stale evidence.
5. Emit workflow state and next action without executing any selected capability.

## Output Contract

Produce:
- workflow graph
- routing decisions
- typed handoffs
- state and invalidation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Orchestration may route, stop, retry, or invalidate, but must never impersonate a selected capability or merge incompatible execution identities.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `context-intake-and-routing`
- `implementation-planning-and-handoff`
- `plan-execution-control`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
