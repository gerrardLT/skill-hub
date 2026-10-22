---
name: implementation-spec-compliance-review
description: Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source. Do not use for review the same patch broadly for correctness, security, and code-quality defects or fix accepted compliance gaps in the source.
---

# Implementation Spec Compliance Review

## Responsibility

Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source.

## Trigger

Use when the requested outcome is: Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source.

Do not use when:
- Review the same patch broadly for correctness, security, and code-quality defects. Route to `independent-code-review`.
- Fix accepted compliance gaps in the source. Route to `defect-remediation`.

## Required Inputs

- Approved task requirements, implementation diff, source snapshot, and implementer report as an untrusted claim.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze requirement and design versions, source ref, patch, scope contract, test evidence, and review exclusions.
2. Map each stable requirement and design decision to implementation locations, tests, runtime evidence, or an explicit missing item.
3. Identify omitted, extra, contradictory, stale, or unverifiable behavior and distinguish spec defects from implementation defects.
4. Return a compliance matrix, findings, and revise-or-block recommendation for the human owner without edits.

## Output Contract

Produce:
- requirement-to-implementation matrix
- compliance findings
- extra and missing behavior register
- human-owned disposition recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `frozen-spec`
- `source-ref`
- `traceability`
- `missing-behavior`
- `extra-behavior`
- `no-source-edit`

## Hard Gates

- Compliance passes only when every frozen requirement and design obligation has current implementation and verification evidence and no unapproved behavior is silently introduced.
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
- `independent-code-review`
- `defect-remediation`
- `requirements-and-delivery-contract`
- `engineering-plan-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
