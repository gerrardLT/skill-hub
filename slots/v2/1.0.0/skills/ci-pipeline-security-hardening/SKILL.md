---
name: ci-pipeline-security-hardening
description: Audit and minimally harden authorized CI workflow source for least privilege, immutable pinning, untrusted input, secret isolation, provenance, and safe rollback. Do not use for audit the wider application, infrastructure, dependency, secret, and ai threat surface or define repository-wide secret classification, ownership, injection, rotation, and revocation policy.
---

# Ci Pipeline Security Hardening

## Responsibility

Audit and minimally harden authorized CI workflow source for least privilege, immutable pinning, untrusted input, secret isolation, provenance, and safe rollback.

## Trigger

Use when the requested outcome is: Audit and minimally harden authorized CI workflow source for least privilege, immutable pinning, untrusted input, secret isolation, provenance, and safe rollback.

Do not use when:
- Audit the wider application, infrastructure, dependency, secret, and AI threat surface. Route to `security-audit-and-threat-modeling`.
- Define repository-wide secret classification, ownership, injection, rotation, and revocation policy. Route to `secrets-and-environment-governance`.

## Required Inputs

- CI workflow files, repository policy, trust boundaries, permissions, and runner context.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze authorized workflow files, trigger contexts, fork policy, runner trust, environments, tokens, secrets, artifacts, caches, releases, and rollback path.
2. Trace every untrusted input into expressions, shell, scripts, filenames, caches, artifacts, logs, comments, and privileged jobs.
3. Reduce job and token permissions, separate untrusted and privileged stages, pin third-party actions immutably, quote or avoid interpolation, and protect environment approvals.
4. Constrain OIDC audience and subject, secret exposure, cache poisoning, artifact substitution, generated provenance, retention, and release attestations.
5. Write the smallest authorized workflow/config patch and verification plan; preserve old behavior or document migration, and never trigger remote CI or provider mutation.

## Output Contract

Produce:
- CI threat findings
- minimal hardened workflow candidate
- verification and rollback plan
- residual supply-chain risk

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `least-privilege`
- `immutable-pinning`
- `untrusted-input`
- `secret-isolation`
- `OIDC`
- `artifact-provenance`
- `rollback`

## Hard Gates

- Untrusted pull-request code, metadata, artifacts, caches, or user-controlled strings must never execute in a context with secrets, write tokens, deployment identity, or unquoted command construction.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

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
- `security-audit-and-threat-modeling`
- `secrets-and-environment-governance`
- `baseline-regression-control`
- `change-delivery-preflight`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
