---
name: risk-preflight-and-safety-governance
description: Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution. Do not use for produce the full technical threat model for the approved architecture or execute the authorized remote deployment.
---

# Risk Preflight And Safety Governance

## Responsibility

Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution.

## Trigger

Use when the requested outcome is: Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution.

Do not use when:
- Produce the full technical threat model for the approved architecture. Route to `security-audit-and-threat-modeling`.
- Execute the authorized remote deployment. Route to `deployment-trigger-execution`.

## Required Inputs

- Requirements, a solution, release plans, dependencies, permissions, and high-consequence assumptions.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Inventory intended actions, actors, systems, data, external boundaries, cost, and irreversible effects.
2. Classify safety, security, privacy, legal, reliability, human-impact, and authority risks.
3. Identify controls, evidence, approvals, least privilege, rollback, and monitoring needs.
4. Set proceed, needs-input, blocked, or specialist-review disposition with reasons.
5. Emit a preflight envelope only; do not perform the action.

## Output Contract

Produce:
- risk preflight
- authority matrix
- control checklist
- stop and escalation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- A prior authorization, tool availability, or low technical difficulty must never be treated as current permission for an irreversible or external action.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

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
- `security-audit-and-threat-modeling`
- `workflow-orchestration-and-lifecycle`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
