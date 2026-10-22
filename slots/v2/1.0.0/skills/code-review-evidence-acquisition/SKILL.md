---
name: code-review-evidence-acquisition
description: Acquire authorized repository and provider-read evidence for a code review, bind it to exact refs, and stop before issuing findings or comments. Do not use for analyze the evidence and issue independent code-review findings or post an evidence-backed response to an identified pull-request review comment.
---

# Code Review Evidence Acquisition

## Responsibility

Acquire authorized repository and provider-read evidence for a code review, bind it to exact refs, and stop before issuing findings or comments.

## Trigger

Use when the requested outcome is: Acquire authorized repository and provider-read evidence for a code review, bind it to exact refs, and stop before issuing findings or comments.

Do not use when:
- Analyze the evidence and issue independent code-review findings. Route to `independent-code-review`.
- Post an evidence-backed response to an identified pull-request review comment. Route to `pull-request-comment-response`.

## Required Inputs

- Change identity, base and head refs, approved provider read access, review scope, and untrusted-content boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze repository, base and head refs, review scope, provider-read authorization, target PR or change identity, and excluded material.
2. Acquire only approved local diff, history, files, tests, and read-only provider checks or metadata; perform no comments, labels, updates, or other writes.
3. Record commands or provider requests, timestamps, refs, tool versions, exits, artifact hashes, truncation, and unavailable evidence.
4. Return an evidence manifest and completeness status for the reviewer; do not infer findings or approve the change.

## Output Contract

Produce:
- review evidence bundle
- base-head and provider identity manifest
- acquisition command records
- evidence completeness result

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `base-head-refs`
- `provider-read-only`
- `evidence-provenance`
- `no-findings`
- `no-comments`
- `completeness`

## Hard Gates

- Review evidence is valid only when bound to exact base/head refs and provider identity; acquisition authority never includes findings, comments, labels, source edits, or remote writes.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `independent-code-review`
- `provider-review-comment-response`
- `implementation-spec-compliance-review`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
