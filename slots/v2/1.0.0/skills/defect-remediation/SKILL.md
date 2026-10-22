---
name: defect-remediation
description: Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace. Do not use for investigate the symptom and establish a reproducible root cause first or independently review the completed patch and report findings without edits.
---

# Defect Remediation

## Responsibility

Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace.

## Trigger

Use when the requested outcome is: Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace.

Do not use when:
- Investigate the symptom and establish a reproducible root cause first. Route to `root-cause-investigation`.
- Independently review the completed patch and report findings without edits. Route to `independent-code-review`.

## Required Inputs

- Confirmed finding, reproduction evidence, source workspace, repair authority, and regression contract.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify the confirmed cause, frozen scope, authorized workspace, single writer, reproduction, expected behavior, regression surface, and rollback path.
2. Inspect every caller and affected invariant; choose the highest shared correction point and avoid symptom guards or speculative refactors.
3. Write the smallest source and test patch that makes the reproduction fail before and pass after while preserving unrelated contracts.
4. Run approved focused and regression commands through the host, preserve failures, and return patch, evidence, changed files, and residual risk for independent review.

## Output Contract

Produce:
- minimal source and test patch
- before-and-after reproduction evidence
- focused and regression command records
- rollback and residual-risk note

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `confirmed-root-cause`
- `shared-fix-point`
- `minimal-patch`
- `single-writer`
- `focused-regression`
- `rollback`

## Hard Gates

- Remediation cannot start from an unconfirmed symptom, and it cannot pass without a root-cause-linked patch plus current focused and affected-regression evidence.
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
- `root-cause-investigation`
- `tdd-change-loop`
- `developer-self-check-and-fix`
- `independent-code-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
