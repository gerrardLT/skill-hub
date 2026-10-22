---
name: ui-remediation
description: Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review. Do not use for independently critique current rendered ui and issue findings or define the ui review matrix and acquire current captures before judgment.
---

# Ui Remediation

## Responsibility

Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review.

## Trigger

Use when the requested outcome is: Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review.

Do not use when:
- Independently critique current rendered UI and issue findings. Route to `rendered-ui-critique-and-release-disposition`.
- Define the UI review matrix and acquire current captures before judgment. Route to `ui-review-scope-and-evidence-acquisition`.

## Required Inputs

- UI findings, source workspace, design system, platform variant, and write authority.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify accepted finding IDs, evidence, severity, repair direction, authorized files, design contract, affected states, review owner, and recapture plan.
2. Trace each finding to the smallest source change and preserve product truth, responsive behavior, content, accessibility, and interaction invariants.
3. Apply only approved repairs; route ambiguous taste, expanded scope, or architecture changes back to their owners.
4. Run approved focused checks and recapture affected route-state-viewport evidence; hand off to an independent reviewer without issuing disposition.

## Output Contract

Produce:
- bounded UI repair patch
- finding-to-change map
- focused verification evidence
- recapture bundle and independent-review handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `accepted-findings`
- `bounded-source-repair`
- `recapture`
- `reviewer-separation`
- `no-self-approval`

## Hard Gates

- UI remediation requires accepted reproducible findings and separate authorization; the remediator cannot create its own findings, waive risk, judge its recaptures, or issue release disposition.
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
- `rendered-ui-critique-and-release-disposition`
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `cross-domain-ui-preflight-checklists`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
