---
name: root-cause-investigation
description: Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source. Do not use for apply the smallest patch for the already-confirmed root cause or run an independent broad code-quality review unrelated to one observed defect.
---

# Root Cause Investigation

## Responsibility

Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source.

## Trigger

Use when the requested outcome is: Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source.

Do not use when:
- Apply the smallest patch for the already-confirmed root cause. Route to `defect-remediation`.
- Run an independent broad code-quality review unrelated to one observed defect. Route to `independent-code-review`.

## Required Inputs

- A test failure, production incident, unexpected behavior, build issue, or performance problem.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the symptom, target identity, environment, reproduction, expected behavior, scope, permitted commands, and existing evidence.
2. Reproduce with the smallest controlled case and record command, exit, duration, output, state, and frequency without changing source.
3. Trace callers, data and control flow, boundaries, recent changes, and sibling paths; test competing hypotheses one variable at a time.
4. Locate the first violated invariant or common cause, distinguish cause from trigger and symptom, and return evidence, affected surface, and a bounded remediation handoff.

## Output Contract

Produce:
- minimal reproduction
- hypothesis and experiment ledger
- root-cause evidence chain
- affected-surface and remediation handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `reproduction`
- `callers`
- `competing-hypotheses`
- `first-divergent-invariant`
- `cause-not-symptom`
- `no-source-edit`

## Hard Gates

- Investigation cannot declare root cause from correlation, the last stack frame, or one patched symptom; it needs a reproducible causal chain and sibling-path analysis.
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
- `defect-remediation`
- `resilience-and-determinism`
- `independent-code-review`
- `change-scope-freeze`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
