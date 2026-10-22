---
name: developer-self-check-and-fix
description: "Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact. Use when An implementer has finished a task and should check their own work against the spec before handing it to independent review; A patch needs a self-review pass and deterministic in-scope fixes, not an approval. Do not use for: Perform the independent code review and issue findings without changing source (-> independent-code-review); Investigate a newly observed behavior whose root cause is not established (-> root-cause-investigation)."
---

# Developer Self Check And Fix

## Responsibility

Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact.

## Trigger

Use when the request matches any of:
- An implementer has finished a task and should check their own work against the spec before handing it to independent review
- A patch needs a self-review pass and deterministic in-scope fixes, not an approval

Do not use when:
- Perform the independent code review and issue findings without changing source. Route to `independent-code-review`.
- Investigate a newly observed behavior whose root cause is not established. Route to `root-cause-investigation`.

## Required Inputs

- Implemented code, its task specification, test output, and change list.

## Procedure

1. Freeze the patch, scope, acceptance criteria, changed files, existing test evidence, and independent-review handoff boundary.
2. Inspect the diff and affected callers for correctness, error handling, security, compatibility, dead code, formatting, and test gaps.
3. Fix only reproducible in-scope defects; route scope expansion or unknown cause to the owning capability instead of opportunistic refactoring.
4. Run approved focused checks, record every correction and remaining concern, and hand off without declaring independent approval.

## Domain Guidance

- Self-review questions. Completeness: is every requirement implemented, and are edge cases handled? Quality: are names accurate, is the code clean? Discipline: nothing built beyond the spec (YAGNI). Testing: do tests verify behavior rather than mocks?
- Report one state: DONE, DONE_WITH_CONCERNS (finished with doubts about correctness or scope, concerns listed), BLOCKED (cannot continue), or NEEDS_CONTEXT (named information missing).
- Fix only deterministic defects inside the frozen scope; everything else goes to the owner in the report.
- Discriminator: use for the author's own in-scope patch after it is complete; it never accepts findings from an independent review.
- Review every changed artifact, including unrelated edits, and give an explicit keep, split or revert disposition. Supply the exact runnable verification command when requested. Fix every deterministic in-scope defect and its boundary tests; do not invent behavior for undefined inputs—record the missing owner decision instead.

## Output Contract

Produce:
- self-review checklist
- bounded correction patch
- updated focused evidence
- independent-review handoff
- report state (DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT) with concerns listed

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `self-review`
- `changed-files`
- `bounded-correction`
- `no-scope-expansion`
- `no-independent-approval`
- `handoff`

## Hard Gates

- A developer correction pass may fix deterministic in-scope defects but must never impersonate independent review, erase failed evidence, or expand the frozen change.
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
- `root-cause-investigation`
- `independent-code-review`
- `implementation-spec-compliance-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
