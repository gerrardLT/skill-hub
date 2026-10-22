---
name: ai-agent-autonomy-and-human-control
description: Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy. Do not use for choose the model, retrieval, prompt, and data architecture for this ai capability or assess prompt injection, tool abuse, and unsafe-action risks for the proposed agent.
---

# Ai Agent Autonomy And Human Control

## Responsibility

Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy.

## Trigger

Use when the requested outcome is: Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy.

Do not use when:
- Choose the model, retrieval, prompt, and data architecture for this AI capability. Route to `ai-model-and-data-architecture`.
- Assess prompt injection, tool abuse, and unsafe-action risks for the proposed agent. Route to `ai-safety-and-action-governance`.

## Required Inputs

- A task definition, agent capabilities, human roles, failure cost, and observed behavior.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the task, users, environment, tools, data, action classes, current rights, failure cost, and named human roles.
2. Decompose agency into observe, recommend, draft, simulate, execute-reversible, and execute-high-impact rights instead of one autonomy label.
3. For each right define preconditions, scope, rate or spend bounds, confirmation, observability, interruption, rollback, and fallback.
4. Define evidence thresholds, shadow or simulation stages, adversarial cases, and regression conditions for graduation or revocation.
5. Return a recommended current level and unresolved risks for human approval; never grant or activate rights.

## Output Contract

Produce:
- agency and action-right contract
- human-control and interruption map
- autonomy graduation and revocation criteria
- fallback and residual-risk record

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `action-classes`
- `graduated-autonomy`
- `human-checkpoint`
- `interruption`
- `rollback`
- `revocation`
- `fallback`

## Hard Gates

- No action right expands without task-specific evidence, a named human owner, observable bounds, interruption, rollback or containment, and explicit approval.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `ai-capability-architecture-and-autonomy`
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `authorization-and-permission-contracts`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
