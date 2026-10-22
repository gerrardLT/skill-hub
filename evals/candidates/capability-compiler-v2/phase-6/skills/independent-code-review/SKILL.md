---
name: independent-code-review
description: Independently inspect a ref-bound code change for correctness, security, failure handling, compatibility, tests, and maintainability without editing it. Do not use for acquire the exact diff, provider metadata, and check evidence first or apply the accepted review fixes to source.
---

# Independent Code Review

## Responsibility

Independently inspect a ref-bound code change for correctness, security, failure handling, compatibility, tests, and maintainability without editing it.

## Trigger

Use when the requested outcome is: Independently inspect a ref-bound code change for correctness, security, failure handling, compatibility, tests, and maintainability without editing it.

Do not use when:
- Acquire the exact diff, provider metadata, and check evidence first. Route to `code-review-evidence-acquisition`.
- Apply the accepted review fixes to source. Route to `defect-remediation`.

## Required Inputs

- A specification, change description, and precise code-diff boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify exact base/head refs, complete diff and files, requirements or scope, tests, evidence freshness, and reviewer independence.
2. Trace changed logic through callers, data and authorization boundaries, failure paths, concurrency, compatibility, cleanup, and relevant tests.
3. Issue only actionable findings with source citation, scenario, consequence, severity, and expected contract; omit style preference and speculative abstraction.
4. Return findings, unknowns, and review recommendation without edits, comments, provider writes, or approval impersonation.

## Output Contract

Produce:
- independent code-review findings
- affected-caller and risk analysis
- test and evidence gaps
- human-owned review recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `code-review-evidence-acquisition`
- `defect-remediation`
- `implementation-spec-compliance-review`
- `provider-review-comment-response`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
