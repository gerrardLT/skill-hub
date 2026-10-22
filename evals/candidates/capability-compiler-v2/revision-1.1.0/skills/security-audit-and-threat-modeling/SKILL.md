---
name: security-audit-and-threat-modeling
description: "Independently threat-model and audit supplied architecture, source, dependencies, infrastructure, CI, secrets metadata, AI, and skill supply chain using authorized local checks, without remediation. Use when A system, repository or pipeline needs an independent threat model and reproducible security findings; Someone asks which attack paths through dependencies, CI, secrets metadata or AI features are real and how severe. Do not use for: Apply approved fixes to the source after findings are accepted (-> defect-remediation); Define the narrower AI prompt, tool, action, and human-checkpoint safety contract (-> ai-safety-and-action-governance)."
---

# Security Audit And Threat Modeling

## Responsibility

Independently threat-model and audit supplied architecture, source, dependencies, infrastructure, CI, secrets metadata, AI, and skill supply chain using authorized local checks, without remediation.

## Trigger

Use when the request matches any of:
- A system, repository or pipeline needs an independent threat model and reproducible security findings
- Someone asks which attack paths through dependencies, CI, secrets metadata or AI features are real and how severe

Do not use when:
- Apply approved fixes to the source after findings are accepted. Route to `defect-remediation`.
- Define the narrower AI prompt, tool, action, and human-checkpoint safety contract. Route to `ai-safety-and-action-governance`.

## Required Inputs

- Architecture, code, dependencies, infrastructure evidence, trust boundaries, and test authorization.

## Procedure

1. Build an attack-surface census with counts per category and detect the stack before tracing threats.
2. Freeze scope, target source identity, architecture, data classes, identities, trust boundaries, environments, authorized commands, prohibited tests, and evidence retention.
3. Model assets, actors, entry points, boundaries, privileges, dependencies, data flows, AI and automation paths, CI, secret references, and skill supply chain.
4. Trace spoofing, tampering, repudiation, disclosure, denial, elevation, tenancy, injection, supply-chain, credential, unsafe-action, and recovery abuse cases proportionate to scope.
5. Use only approved local non-destructive checks; record command, exit code, tool version, duration, target identity, output hash, and limitations without accessing secret values.
6. Issue one reproducible finding per problem with evidence, affected boundary, exploit preconditions, impact, severity rationale, remediation options, verification, and residual risk; do not edit source.

## Domain Guidance

- Start with an attack-surface census with counts per category: endpoints, authentication boundaries, external integrations, file upload paths, admin routes, webhooks, background jobs, WebSocket channels, CI workflows, and dependencies. Detect the technology stack first because it changes which checks apply.
- Treat the dependency and supply chain as a primary surface: check that third-party CI actions are pinned to full commit SHAs rather than mutable tags, and that lockfiles are enforced (for example npm ci).
- Report only findings you can reproduce or evidence; mark a confidence level and filter likely false positives before listing.

## Output Contract

Produce:
- threat model and trust-boundary map
- authorized local-check evidence manifest
- reproducible prioritized findings
- remediation options and residual-risk report
- attack-surface census with counts

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `trust-boundary`
- `authorized-local-check`
- `reproducible-finding`
- `severity-rationale`
- `no-remediation`
- `no-secret-values`

## Hard Gates

- A security finding requires a cited trust boundary, reproducible evidence, exploit preconditions, impact, and severity rationale; audit permission never implies destructive testing, source repair, credential access, or remote mutation.
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
- `defect-remediation`
- `ai-safety-and-action-governance`
- `ci-pipeline-security-hardening`
- `secrets-and-environment-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
