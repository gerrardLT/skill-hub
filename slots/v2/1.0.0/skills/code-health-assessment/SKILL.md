---
name: code-health-assessment
description: Assess a codebase's maintainability, complexity, duplication, dependency, error-handling, and test-health risks from supplied source without editing it. Do not use for independently review this specific patch for correctness and security or apply the accepted code-health repairs to source.
---

# Code Health Assessment

## Responsibility

Assess a codebase's maintainability, complexity, duplication, dependency, error-handling, and test-health risks from supplied source without editing it.

## Trigger

Use when the requested outcome is: Assess a codebase's maintainability, complexity, duplication, dependency, error-handling, and test-health risks from supplied source without editing it.

Do not use when:
- Independently review this specific patch for correctness and security. Route to `independent-code-review`.
- Apply the accepted code-health repairs to source. Route to `defect-remediation`.

## Required Inputs

- Repository, time window, quality signals, ownership, and exclusions.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze repository scope, source identity, languages, generated or vendor exclusions, change history evidence, and assessment criteria.
2. Trace concrete duplication, complexity, coupling, cohesion, dead code, error handling, dependency, test, and ownership signals with citations.
3. Distinguish measurable risk from style preference and identify leave-unchanged cases where remediation cost exceeds evidence.
4. Return prioritized findings, affected change scenarios, bounded options, and residual uncertainty without edits.

## Output Contract

Produce:
- code-health findings
- maintainability evidence map
- priority and leave-unchanged rationale
- bounded remediation options

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `maintainability`
- `complexity`
- `duplication`
- `coupling`
- `error-handling`
- `test-health`
- `leave-unchanged`

## Hard Gates

- A code-health finding needs a cited source location and plausible maintenance consequence; stylistic dislike, hypothetical reuse, and aggregate scores alone do not justify remediation.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `independent-code-review`
- `architecture-deepening-discovery`
- `defect-remediation`
- `developer-experience-assessment`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
