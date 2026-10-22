---
name: qa-finding-triage
description: Triage independently observed QA findings by reproducibility, severity, duplication, scope, ownership, and next capability without source repair. Do not use for run a new black-box qa campaign against the product or apply the accepted defect repair to source.
---

# Qa Finding Triage

## Responsibility

Triage independently observed QA findings by reproducibility, severity, duplication, scope, ownership, and next capability without source repair.

## Trigger

Use when the requested outcome is: Triage independently observed QA findings by reproducibility, severity, duplication, scope, ownership, and next capability without source repair.

Do not use when:
- Run a new black-box QA campaign against the product. Route to `independent-blackbox-qa`.
- Apply the accepted defect repair to source. Route to `defect-remediation`.

## Required Inputs

- QA findings, evidence, affected surface, release context, and severity policy.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze finding identities, build or source identity, evidence, reproduction records, acceptance criteria, severity policy, and ownership map.
2. Normalize expected and observed behavior, environment, frequency, scope, impact, and evidence freshness.
3. Reproduce only from supplied evidence where permitted; merge true duplicates without losing affected variants or independent reports.
4. Assign disposition, severity rationale, owner, next capability, and missing evidence; do not fix, close from assertion, or accept risk.

## Output Contract

Produce:
- deduplicated QA finding register
- reproducibility and severity rationale
- ownership and routing map
- blocked and missing-evidence list

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `deduplication`
- `reproducibility`
- `severity`
- `ownership`
- `routing`
- `no-fix`
- `no-risk-acceptance`

## Hard Gates

- Triage may classify and route findings but cannot repair source, waive risk, close defects without current evidence, or overwrite independent severity ownership.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `independent-blackbox-qa`
- `root-cause-investigation`
- `defect-remediation`
- `rendered-ui-critique-and-release-disposition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
