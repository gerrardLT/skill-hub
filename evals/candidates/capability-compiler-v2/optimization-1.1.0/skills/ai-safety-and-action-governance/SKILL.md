---
name: ai-safety-and-action-governance
description: "Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation. Use when An AI feature with tools, data access or actions needs its injection, exfiltration and tool-abuse risks assessed independently; Someone asks what red-team cases, default-deny boundaries and stop conditions an agent needs before release. Do not use for: Define the agent's graduated action rights, interruption, revocation, and fallback contract (-> ai-agent-autonomy-and-human-control); Perform the full application, infrastructure, CI, dependency, and supply-chain threat model (-> security-audit-and-threat-modeling)."
---

# AI Safety And Action Governance

## Responsibility

Independently assess AI prompt, data, tool, and action risks; define red-team scope, default-deny boundaries, human checkpoints, stop conditions, and residual risk without remediation.

## Trigger

Use when the request matches any of:
- An AI feature with tools, data access or actions needs its injection, exfiltration and tool-abuse risks assessed independently
- Someone asks what red-team cases, default-deny boundaries and stop conditions an agent needs before release

Do not use when:
- Define the agent's graduated action rights, interruption, revocation, and fallback contract. Route to `ai-agent-autonomy-and-human-control`.
- Perform the full application, infrastructure, CI, dependency, and supply-chain threat model. Route to `security-audit-and-threat-modeling`.

## Required Inputs

- An AI capability, tools and permissions, threat scenarios, failure evidence, and consequence level.

## Procedure

1. Freeze the system boundary, models, prompts, data classes, tools, action classes, users, environments, safeguards, and evidence supplied for review.
2. Map prompt injection, indirect injection, exfiltration, privilege escalation, confused deputy, unsafe tool composition, persistence, poisoning, and denial or cost abuse paths.
3. Separate prevention, detection, containment, human confirmation, interruption, rollback, and recovery controls by action consequence.
4. Define reproducible red-team cases, success criteria, unsupported claims, and untested boundaries without executing prohibited attacks or changing source.
5. Issue blockers, residual risk, and explicit stop conditions to the human safety owner; do not approve autonomy or deployment.

## Domain Guidance

- Prompt injection cannot be fully solved. Report injection residual risk as non-zero in every assessment; controls reduce impact and likelihood, they never eliminate the risk. Red-team with creative personas and scenarios.
- Discriminator: owns misuse, action-risk and governance rules for AI actions; it sets limits that the other AI Skills must respect.

## Output Contract

Produce:
- AI safety boundary
- threat and abuse-case register
- red-team and stop-condition plan
- human-checkpoint and residual-risk report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `ai-agent-autonomy-and-human-control`
- `authorization-and-permission-contracts`
- `security-audit-and-threat-modeling`
- `risk-preflight-and-safety-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
