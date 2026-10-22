---
name: independent-code-review
description: "Independently inspect a ref-bound code change for correctness, security, failure handling, compatibility, tests, and maintainability without editing it. Use when A ref-bound code change needs an independent review for correctness, security, failure handling and test gaps; Someone asks whether a diff is safe to merge and wants concrete scenarios, not style preferences. Do not use for: Acquire the exact diff, provider metadata, and check evidence first (-> code-review-evidence-acquisition); Apply the accepted review fixes to source (-> defect-remediation)."
---

# Independent Code Review

## Responsibility

Independently inspect a ref-bound code change for correctness, security, failure handling, compatibility, tests, and maintainability without editing it.

## Trigger

Use when the request matches any of:
- A ref-bound code change needs an independent review for correctness, security, failure handling and test gaps
- Someone asks whether a diff is safe to merge and wants concrete scenarios, not style preferences

Do not use when:
- Acquire the exact diff, provider metadata, and check evidence first. Route to `code-review-evidence-acquisition`.
- Apply the accepted review fixes to source. Route to `defect-remediation`.

## Required Inputs

- A specification, change description, and precise code-diff boundary.

## Procedure

1. Verify exact base/head refs, complete diff and files, requirements or scope, tests, evidence freshness, and reviewer independence.
2. Trace changed logic through callers, data and authorization boundaries, failure paths, concurrency, compatibility, cleanup, and relevant tests.
3. Rank findings by consequence; severe security and correctness defects come first, and style points never displace them.
4. Issue only actionable findings with source citation, scenario, consequence, severity, and expected contract; omit style preference and speculative abstraction.
5. Return findings, unknowns, and review recommendation without edits, comments, provider writes, or approval impersonation.

## Domain Guidance

- Lead with findings that have a concrete failing scenario, a source citation and a consequence; put style notes last or omit them. An authorization, tenancy or injection defect outranks any number of naming issues.
- Optional adversarial pass: after the standard review, try to break the change (malformed input, missing permissions, concurrent calls, partial failure) and report only scenarios you can trace through the code.

## Output Contract

Produce:
- independent code-review findings
- affected-caller and risk analysis
- test and evidence gaps
- human-owned review recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `base-head-refs`
- `callers`
- `failure-scenario`
- `source-citation`
- `severity`
- `no-fix`
- `no-provider-write`

## Hard Gates

- A finding requires a concrete failing or risky scenario, source citation, consequence, and contract; the reviewer never edits source, posts comments, or approves its own remediation.
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
- `code-review-evidence-acquisition`
- `defect-remediation`
- `implementation-spec-compliance-review`
- `pull-request-comment-response`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
