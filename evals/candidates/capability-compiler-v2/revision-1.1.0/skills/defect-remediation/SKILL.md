---
name: defect-remediation
description: "Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace. Use when A root cause is confirmed with a reproduction and the smallest safe source fix must be applied and verified; Someone asks for a patch plus a test that fails before and passes after, in an isolated workspace. Do not use for: Investigate the symptom and establish a reproducible root cause first (-> root-cause-investigation); Independently review the completed patch and report findings without edits (-> independent-code-review); Fix only the author's own just-completed patch within its frozen scope (-> developer-self-check-and-fix)."
---

# Defect Remediation

## Responsibility

Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace.

## Trigger

Use when the request matches any of:
- A root cause is confirmed with a reproduction and the smallest safe source fix must be applied and verified
- Someone asks for a patch plus a test that fails before and passes after, in an isolated workspace

Do not use when:
- Investigate the symptom and establish a reproducible root cause first. Route to `root-cause-investigation`.
- Independently review the completed patch and report findings without edits. Route to `independent-code-review`.
- Fix only the author's own just-completed patch within its frozen scope. Route to `developer-self-check-and-fix`.

## Required Inputs

- Confirmed finding, reproduction evidence, source workspace, repair authority, and regression contract.

## Procedure

1. Confirm the workspace revision matches the revision the evidence came from; stop and flag any mismatch before patching.
2. Verify the confirmed cause, frozen scope, authorized workspace, single writer, reproduction, expected behavior, regression surface, and rollback path.
3. Inspect every caller and affected invariant; choose the highest shared correction point and avoid symptom guards or speculative refactors.
4. Write the smallest source and test patch that makes the reproduction fail before and pass after while preserving unrelated contracts.
5. Run approved focused and regression commands through the host, preserve failures, and return patch, evidence, changed files, and residual risk for independent review.

## Domain Guidance

- If the evidence came from a specific release or revision, check out or diff that revision first; stop and flag when the frames or symptoms do not match the workspace.
- Discriminator: use when a root cause is confirmed and a minimal source repair is authorized.

## Output Contract

Produce:
- minimal source and test patch
- before-and-after reproduction evidence
- focused and regression command records
- rollback and residual-risk note

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `confirmed-root-cause`
- `shared-fix-point`
- `minimal-patch`
- `single-writer`
- `focused-regression`
- `rollback`

## Hard Gates

- Remediation cannot start from an unconfirmed symptom, and it cannot pass without a root-cause-linked patch plus current focused and affected-regression evidence.
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

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `root-cause-investigation`
- `tdd-change-loop`
- `developer-self-check-and-fix`
- `independent-code-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
