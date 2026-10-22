---
name: ai-safety-and-action-governance
description: Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation. Do not use for define the agent's graduated action rights, interruption, revocation, and fallback contract or perform the full application, infrastructure, ci, dependency, and supply-chain threat model.
---

# Ai Safety And Action Governance

## Responsibility

Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation.

## Trigger

Use when the requested outcome is: Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation.

Do not use when:
- Define the agent's graduated action rights, interruption, revocation, and fallback contract. Route to `ai-agent-autonomy-and-human-control`.
- Perform the full application, infrastructure, CI, dependency, and supply-chain threat model. Route to `security-audit-and-threat-modeling`.

## Required Inputs

- An AI capability, tools and permissions, threat scenarios, failure evidence, and consequence level.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the system boundary, models, prompts, data classes, tools, action classes, users, environments, safeguards, and evidence supplied for review.
2. Map prompt injection, indirect injection, exfiltration, privilege escalation, confused deputy, unsafe tool composition, persistence, poisoning, and denial or cost abuse paths.
3. Separate prevention, detection, containment, human confirmation, interruption, rollback, and recovery controls by action consequence.
4. Define reproducible red-team cases, success criteria, unsupported claims, and untested boundaries without executing prohibited attacks or changing source.
5. Issue blockers, residual risk, and explicit stop conditions to the human safety owner; do not approve autonomy or deployment.

## Output Contract

Produce:
- AI safety boundary
- threat and abuse-case register
- red-team and stop-condition plan
- human-checkpoint and residual-risk report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `prompt-injection`
- `data-exfiltration`
- `tool-abuse`
- `default-deny`
- `human-checkpoint`
- `containment`
- `stop-condition`

## Hard Gates

- High-impact, irreversible, privileged, privacy-sensitive, or externally consequential AI actions remain default-deny without explicit policy, task-scoped authorization, human confirmation, containment, and current safety evidence.
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
- `ai-agent-autonomy-and-human-control`
- `authorization-and-permission-contracts`
- `security-audit-and-threat-modeling`
- `risk-preflight-and-safety-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
