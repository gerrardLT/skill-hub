---
name: ai-safety-and-action-governance
description: "Consolidated capability with 2 selectable modes: ai-agent-autonomy-and-human-control; ai-safety-and-action-governance. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [ai-agent-autonomy-and-human-control, ai-safety-and-action-governance]
---

# Ai Safety And Action Governance

## Responsibility

Consolidated capability covering 2 related modes: Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy.; Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `ai-agent-autonomy-and-human-control` | `workspace-write` | An AI agent is about to be given actions and someone must define which rights it has, who can interrupt it and when rights grow or are revoked; Autonomy for an AI task is being discussed as one label  | Choose the model, retrieval, prompt, and data architecture for this AI capability (-> ai-model-and-data-architecture); A |
| `ai-safety-and-action-governance` | `read-only` | An AI feature with tools, data access or actions needs its injection, exfiltration and tool-abuse risks assessed independently; Someone asks what red-team cases, default-deny boundaries and stop condi | Define the agent's graduated action rights, interruption, revocation, and fallback contract (-> ai-agent-autonomy-and-hu |

## Mode: `ai-agent-autonomy-and-human-control`

### ai-agent-autonomy-and-human-control

#### Responsibility

Define an evidence-gated agency contract for AI tasks, action rights, human handoffs, interruption, fallback, and graduated autonomy.

#### Trigger

Use when the request matches any of:
- An AI agent is about to be given actions and someone must define which rights it has, who can interrupt it and when rights grow or are revoked
- Autonomy for an AI task is being discussed as one label and needs to be split into observe, recommend, draft, simulate and execute rights

Do not use when:
- Choose the model, retrieval, prompt, and data architecture for this AI capability. Route to `ai-model-and-data-architecture`.
- Assess prompt injection, tool abuse, and unsafe-action risks for the proposed agent. Route to `ai-safety-and-action-governance`.

#### Required Inputs

- A task definition, agent capabilities, human roles, failure cost, and observed behavior.

#### Procedure

1. Freeze the task, users, environment, tools, data, action classes, current rights, failure cost, and named human roles.
2. Decompose agency into observe, recommend, draft, simulate, execute-reversible, and execute-high-impact rights instead of one autonomy label.
3. For each right define preconditions, scope, rate or spend bounds, confirmation, observability, interruption, rollback, and fallback.
4. Define evidence thresholds, shadow or simulation stages, adversarial cases, and regression conditions for graduation or revocation.
5. Return a recommended current level and unresolved risks for human approval; never grant or activate rights.

#### Domain Guidance

- Express graduation as versioned rungs (v1, v2, v3). Each rung names its agency level, the control that bounds it, the evidence threshold to reach it, the data it collects, and the trigger that revokes it.
- Every right needs preconditions, scope, rate or spend bounds, confirmation, interruption, rollback or containment, and a fallback when the agent cannot act.
- Discriminator: owns the autonomy level, approval points and override paths of an agent; model and data choices come from ai-model-and-data-architecture.

#### Output Contract

Produce:
- agency and action-right contract
- human-control and interruption map
- autonomy graduation and revocation criteria
- fallback and residual-risk record

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `action-classes`
- `graduated-autonomy`
- `human-checkpoint`
- `interruption`
- `rollback`
- `revocation`
- `fallback`

#### Hard Gates

- No action right expands without task-specific evidence, a named human owner, observable bounds, interruption, rollback or containment, and explicit approval.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `authorization-and-permission-contracts`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `ai-safety-and-action-governance`

### ai-safety-and-action-governance

#### Responsibility

Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation.

#### Trigger

Use when the request matches any of:
- An AI feature with tools, data access or actions needs its injection, exfiltration and tool-abuse risks assessed independently
- Someone asks what red-team cases, default-deny boundaries and stop conditions an agent needs before release

Do not use when:
- Define the agent's graduated action rights, interruption, revocation, and fallback contract. Route to `ai-agent-autonomy-and-human-control`.
- Perform the full application, infrastructure, CI, dependency, and supply-chain threat model. Route to `security-audit-and-threat-modeling`.

#### Required Inputs

- An AI capability, tools and permissions, threat scenarios, failure evidence, and consequence level.

#### Procedure

1. Freeze the system boundary, models, prompts, data classes, tools, action classes, users, environments, safeguards, and evidence supplied for review.
2. Map prompt injection, indirect injection, exfiltration, privilege escalation, confused deputy, unsafe tool composition, persistence, poisoning, and denial or cost abuse paths.
3. Separate prevention, detection, containment, human confirmation, interruption, rollback, and recovery controls by action consequence.
4. Define reproducible red-team cases, success criteria, unsupported claims, and untested boundaries without executing prohibited attacks or changing source.
5. Issue blockers, residual risk, and explicit stop conditions to the human safety owner; do not approve autonomy or deployment.

#### Domain Guidance

- Prompt injection cannot be fully solved. Report injection residual risk as non-zero in every assessment; controls reduce impact and likelihood, they never eliminate the risk. Red-team with creative personas and scenarios.
- Discriminator: owns misuse, action-risk and governance rules for AI actions; it sets limits that the other AI Skills must respect.

#### Output Contract

Produce:
- AI safety boundary
- threat and abuse-case register
- red-team and stop-condition plan
- human-checkpoint and residual-risk report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `prompt-injection`
- `data-exfiltration`
- `tool-abuse`
- `default-deny`
- `human-checkpoint`
- `containment`
- `stop-condition`

#### Hard Gates

- High-impact, irreversible, privileged, privacy-sensitive, or externally consequential AI actions remain default-deny without explicit policy, task-scoped authorization, human confirmation, containment, and current safety evidence.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ai-agent-autonomy-and-human-control`
- `authorization-and-permission-contracts`
- `security-audit-and-threat-modeling`
- `risk-preflight-and-safety-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
