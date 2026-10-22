---
name: root-cause-investigation
description: "Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source. Use when A bug, failing test, incident or regression needs its real cause found and demonstrated before anyone patches it; Someone proposes a quick fix for a symptom and the cause has not been established. Do not use for: Apply the smallest patch for the already-confirmed root cause (-> defect-remediation); Run an independent broad code-quality review unrelated to one observed defect (-> independent-code-review)."
---

# Root Cause Investigation

## Responsibility

Reproduce and trace an observed defect to the highest shared evidence-backed cause without editing product source.

## Trigger

Use when the request matches any of:
- A bug, failing test, incident or regression needs its real cause found and demonstrated before anyone patches it
- Someone proposes a quick fix for a symptom and the cause has not been established

Do not use when:
- Apply the smallest patch for the already-confirmed root cause. Route to `defect-remediation`.
- Run an independent broad code-quality review unrelated to one observed defect. Route to `independent-code-review`.

## Required Inputs

- A test failure, production incident, unexpected behavior, build issue, or performance problem.

## Procedure

1. Freeze the symptom, target identity, environment, reproduction, expected behavior, scope, permitted commands, and existing evidence.
2. Reproduce with the smallest controlled case and record command, exit, duration, output, state, and frequency without changing source.
3. Trace callers, data and control flow, boundaries, recent changes, and sibling paths; test competing hypotheses one variable at a time.
4. Locate the first violated invariant or common cause, distinguish cause from trigger and symptom, and return evidence, affected surface, and a bounded remediation handoff.

## Domain Guidance

- Red flags that mean stop and investigate: 'quick fix now, investigate later', 'just try changing X', 'it's probably X', 'I don't fully understand but this might work', and listing fixes before any investigation.
- Trace backward from the symptom through each caller until you find the original bad value or first violated invariant; the last stack frame is usually a symptom, not the cause.
- Test one hypothesis at a time with a change in exactly one variable.

## Output Contract

Produce:
- minimal reproduction
- hypothesis and experiment ledger
- root-cause evidence chain
- affected-surface and remediation handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `reproduction`
- `callers`
- `competing-hypotheses`
- `first-divergent-invariant`
- `cause-not-symptom`
- `no-source-edit`

## Hard Gates

- Investigation cannot declare root cause from correlation, the last stack frame, or one patched symptom; it needs a reproducible causal chain and sibling-path analysis.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `defect-remediation`
- `resilience-and-determinism`
- `independent-code-review`
- `change-scope-freeze`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
