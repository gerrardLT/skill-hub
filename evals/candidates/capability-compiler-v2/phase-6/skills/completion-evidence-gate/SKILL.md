---
name: completion-evidence-gate
description: Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work. Do not use for run the missing tests or build commands needed to create evidence or fix the defects exposed by the completion check.
---

# Completion Evidence Gate

## Responsibility

Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work.

## Trigger

Use when the requested outcome is: Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work.

Do not use when:
- Run the missing tests or build commands needed to create evidence. Route to `baseline-regression-control`.
- Fix the defects exposed by the completion check. Route to `defect-remediation`.

## Required Inputs

- A proposed status claim and the command capable of proving it.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the claimed outcome, target source or artifact identity, acceptance criteria, required checks, and evidence freshness window.
2. Validate every command, tool version, environment, exit code, duration, output summary, artifact path, and normalized hash against the current target.
3. Reject missing, stale, mismatched, self-attested, partial, skipped, or manually edited evidence and preserve failed checks.
4. Map each acceptance criterion to evidence and return a bounded status with limitations; never rerun commands, repair source, or upgrade a claim.

## Output Contract

Produce:
- criterion-to-evidence matrix
- completion gate result
- stale or missing evidence register
- limitations and invalidation conditions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `current-evidence`
- `source-identity`
- `command`
- `exit-code`
- `duration`
- `artifact-hash`
- `no-self-attestation`
- `limitations`

## Hard Gates

- A completion claim cannot pass from prose, status text, model confidence, stale output, or partial success; each required criterion needs current target-bound executable or artifact evidence.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `baseline-regression-control`
- `artifact-persistence-and-tool-actions`
- `defect-remediation`
- `change-delivery-preflight`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
