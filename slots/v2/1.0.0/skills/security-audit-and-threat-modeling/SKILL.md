---
name: security-audit-and-threat-modeling
description: Independently threat-model and audit supplied architecture, source, dependencies, infrastructure, CI, secrets metadata, AI, and skill supply chain using authorized local checks, without remediation. Do not use for apply approved fixes to the source after findings are accepted or define the narrower ai prompt, tool, action, and human-checkpoint safety contract.
---

# Security Audit And Threat Modeling

## Responsibility

Independently threat-model and audit supplied architecture, source, dependencies, infrastructure, CI, secrets metadata, AI, and skill supply chain using authorized local checks, without remediation.

## Trigger

Use when the requested outcome is: Independently threat-model and audit supplied architecture, source, dependencies, infrastructure, CI, secrets metadata, AI, and skill supply chain using authorized local checks, without remediation.

Do not use when:
- Apply approved fixes to the source after findings are accepted. Route to `defect-remediation`.
- Define the narrower AI prompt, tool, action, and human-checkpoint safety contract. Route to `ai-safety-and-action-governance`.

## Required Inputs

- Architecture, code, dependencies, infrastructure evidence, trust boundaries, and test authorization.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze scope, target source identity, architecture, data classes, identities, trust boundaries, environments, authorized commands, prohibited tests, and evidence retention.
2. Model assets, actors, entry points, boundaries, privileges, dependencies, data flows, AI and automation paths, CI, secret references, and skill supply chain.
3. Trace spoofing, tampering, repudiation, disclosure, denial, elevation, tenancy, injection, supply-chain, credential, unsafe-action, and recovery abuse cases proportionate to scope.
4. Use only approved local non-destructive checks; record command, exit code, tool version, duration, target identity, output hash, and limitations without accessing secret values.
5. Issue one reproducible finding per problem with evidence, affected boundary, exploit preconditions, impact, severity rationale, remediation options, verification, and residual risk; do not edit source.

## Output Contract

Produce:
- threat model and trust-boundary map
- authorized local-check evidence manifest
- reproducible prioritized findings
- remediation options and residual-risk report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `trust-boundary`
- `authorized-local-check`
- `reproducible-finding`
- `severity-rationale`
- `no-remediation`
- `no-secret-values`

## Hard Gates

- A security finding requires a cited trust boundary, reproducible evidence, exploit preconditions, impact, and severity rationale; audit permission never implies destructive testing, source repair, credential access, or remote mutation.
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

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `defect-remediation`
- `ai-safety-and-action-governance`
- `ci-pipeline-security-hardening`
- `secrets-and-environment-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
