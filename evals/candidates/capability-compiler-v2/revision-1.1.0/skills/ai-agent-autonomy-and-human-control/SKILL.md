---
name: ai-agent-autonomy-and-human-control
description: "Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy. Use when An AI agent is about to be given actions and someone must define which rights it has, who can interrupt it and when rights grow or are revoked; Autonomy for an AI task is being discussed as one label and needs to be split into observe, recommend, draft, simulate and execute rights. Do not use for: Choose the model, retrieval, prompt, and data architecture for this AI capability (-> ai-model-and-data-architecture); Assess prompt injection, tool abuse, and unsafe-action risks for the proposed agent (-> ai-safety-and-action-governance)."
---

# AI Agent Autonomy And Human Control

## Responsibility

Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy.

## Trigger

Use when the request matches any of:
- An AI agent is about to be given actions and someone must define which rights it has, who can interrupt it and when rights grow or are revoked
- Autonomy for an AI task is being discussed as one label and needs to be split into observe, recommend, draft, simulate and execute rights

Do not use when:
- Choose the model, retrieval, prompt, and data architecture for this AI capability. Route to `ai-model-and-data-architecture`.
- Assess prompt injection, tool abuse, and unsafe-action risks for the proposed agent. Route to `ai-safety-and-action-governance`.

## Required Inputs

- A task definition, agent capabilities, human roles, failure cost, and observed behavior.

## Procedure

1. Freeze the task, users, environment, tools, data, action classes, current rights, failure cost, and named human roles.
2. Decompose agency into observe, recommend, draft, simulate, execute-reversible, and execute-high-impact rights instead of one autonomy label.
3. For each right define preconditions, scope, rate or spend bounds, confirmation, observability, interruption, rollback, and fallback.
4. Define evidence thresholds, shadow or simulation stages, adversarial cases, and regression conditions for graduation or revocation.
5. Return a recommended current level and unresolved risks for human approval; never grant or activate rights.

## Domain Guidance

- Express graduation as versioned rungs (v1, v2, v3). Each rung names its agency level, the control that bounds it, the evidence threshold to reach it, the data it collects, and the trigger that revokes it.
- Every right needs preconditions, scope, rate or spend bounds, confirmation, interruption, rollback or containment, and a fallback when the agent cannot act.
- Discriminator: owns the autonomy level, approval points and override paths of an agent; model and data choices come from ai-model-and-data-architecture.

## Output Contract

Produce:
- agency and action-right contract
- human-control and interruption map
- autonomy graduation and revocation criteria
- fallback and residual-risk record

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `authorization-and-permission-contracts`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
