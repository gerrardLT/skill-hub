---
name: code-review-evidence-acquisition
description: "Acquire authorized repository and provider-read evidence for a code review, bind it to exact refs, and stop before issuing findings or comments. Use when A code change needs its exact diff, history, tests and read-only provider metadata collected before anyone reviews it; Someone asks for a reproducible evidence bundle bound to base and head refs. Do not use for: Analyze the evidence and issue independent code-review findings (-> independent-code-review); Post an evidence-backed response to an identified pull-request review comment (-> pull-request-comment-response)."
---

# Code Review Evidence Acquisition

## Responsibility

Acquire authorized repository and provider-read evidence for a code review, bind it to exact refs, and stop before issuing findings or comments.

## Trigger

Use when the request matches any of:
- A code change needs its exact diff, history, tests and read-only provider metadata collected before anyone reviews it
- Someone asks for a reproducible evidence bundle bound to base and head refs

Do not use when:
- Analyze the evidence and issue independent code-review findings. Route to `independent-code-review`.
- Post an evidence-backed response to an identified pull-request review comment. Route to `pull-request-comment-response`.

## Required Inputs

- Change identity, base and head refs, approved provider read access, review scope, and untrusted-content boundary.

## Procedure

1. Freeze repository, base and head refs, review scope, provider-read authorization, target PR or change identity, and excluded material.
2. Acquire only approved local diff, history, files, tests, and read-only provider checks or metadata; perform no comments, labels, updates, or other writes.
3. Record commands or provider requests, timestamps, refs, tool versions, exits, artifact hashes, truncation, and unavailable evidence.
4. Return an evidence manifest and completeness status for the reviewer; do not infer findings or approve the change.

## Domain Guidance

- Fetch the latest base read-only where authorized, compute the merge base, and diff the head against that merge base so a stale local base does not create false positives. Record the fetch, the merge-base SHA and any truncation.

## Output Contract

Produce:
- review evidence bundle
- base-head and provider identity manifest
- acquisition command records
- evidence completeness result

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `base-head-refs`
- `provider-read-only`
- `evidence-provenance`
- `no-findings`
- `no-comments`
- `completeness`

## Hard Gates

- Review evidence is valid only when bound to exact base/head refs and provider identity; acquisition authority never includes findings, comments, labels, source edits, or remote writes.
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

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `independent-code-review`
- `pull-request-comment-response`
- `implementation-spec-compliance-review`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
