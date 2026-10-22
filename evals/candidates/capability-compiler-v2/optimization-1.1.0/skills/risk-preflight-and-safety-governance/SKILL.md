---
name: risk-preflight-and-safety-governance
description: "Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution. Use when A planned action touches irreversible, external, privileged or sensitive-data effects and needs a go, hold or escalate call first; Someone asks what approvals, controls and stop conditions a task needs before it is executed. Do not use for: Produce the full technical threat model for the approved architecture (-> security-audit-and-threat-modeling); Execute the authorized remote deployment (-> deployment-trigger-execution); Set action rights, graduation and revocation for an AI agent (-> ai-safety-and-action-governance)."
---

# Risk Preflight And Safety Governance

## Responsibility

Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution.

## Trigger

Use when the request matches any of:
- A planned action touches irreversible, external, privileged or sensitive-data effects and needs a go, hold or escalate call first
- Someone asks what approvals, controls and stop conditions a task needs before it is executed

Do not use when:
- Produce the full technical threat model for the approved architecture. Route to `security-audit-and-threat-modeling`.
- Execute the authorized remote deployment. Route to `deployment-trigger-execution`.
- Set action rights, graduation and revocation for an AI agent. Route to `ai-safety-and-action-governance`.

## Required Inputs

- Requirements, a solution, release plans, dependencies, permissions, and high-consequence assumptions.

## Procedure

1. Inventory intended actions, actors, systems, data, external boundaries, cost, and irreversible effects.
2. Classify safety, security, privacy, legal, reliability, human-impact, and authority risks.
3. Identify controls, evidence, approvals, least privilege, rollback, and monitoring needs.
4. Set proceed, needs-input, blocked, or specialist-review disposition with reasons.
5. Emit a preflight envelope only; do not perform the action.

## Domain Guidance

- Reversibility tiers and forced dispositions: tier 1 reversible locally (proceed with evidence), tier 2 reversible with cost or delay (proceed with named owner and rollback), tier 3 irreversible or external (stop at needs-input until fresh per-action authority exists), tier 4 safety- or legal-critical (blocked, escalate to a specialist).
- Prior authorization, tool availability or low technical difficulty never counts as current permission.

## Output Contract

Produce:
- risk preflight
- authority matrix
- control checklist
- stop and escalation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A prior authorization, tool availability, or low technical difficulty must never be treated as current permission for an irreversible or external action.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

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
- `security-audit-and-threat-modeling`
- `workflow-orchestration-and-lifecycle`
- `deployment-trigger-execution`
- `ai-safety-and-action-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
