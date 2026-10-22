---
name: code-health-assessment
description: "Assess a codebase's maintainability, complexity, duplication, dependency, error-handling, and test-health risks from supplied source without editing it. Use when A codebase needs a maintainability and risk assessment from static evidence and tool output without changing it; Someone asks which code-quality problems are worth fixing and which should be left alone. Do not use for: Independently review this specific patch for correctness and security (-> independent-code-review); Apply the accepted code-health repairs to source (-> defect-remediation)."
---

# Code Health Assessment

## Responsibility

Assess a codebase's maintainability, complexity, duplication, dependency, error-handling, and test-health risks from supplied source without editing it.

## Trigger

Use when the request matches any of:
- A codebase needs a maintainability and risk assessment from static evidence and tool output without changing it
- Someone asks which code-quality problems are worth fixing and which should be left alone

Do not use when:
- Independently review this specific patch for correctness and security. Route to `independent-code-review`.
- Apply the accepted code-health repairs to source. Route to `defect-remediation`.

## Required Inputs

- Repository, time window, quality signals, ownership, and exclusions.

## Procedure

1. Freeze repository scope, source identity, languages, generated or vendor exclusions, change history evidence, and assessment criteria.
2. Trace concrete duplication, complexity, coupling, cohesion, dead code, error handling, dependency, test, and ownership signals with citations.
3. Distinguish measurable risk from style preference and identify leave-unchanged cases where remediation cost exceeds evidence.
4. Return prioritized findings, affected change scenarios, bounded options, and residual uncertainty without edits.

## Domain Guidance

- Use the categories, weights and scales the task or owner supplies. When none are supplied, report a per-category status from the tool exits (tool, version, command, exit, duration) without a composite number. A composite score with illustrative weights (type check 22%, lint 18%, tests 28%, dead code 13%, other checks 19%) may be offered only as a labelled optional convention, never as a prescribed rule.
- Show a per-category table with score, status and detail, then cited findings. Sort findings by maintenance consequence; a style preference without a cited consequence is not a finding.
- If remediation cost exceeds the evidenced benefit, the recommendation is leave unchanged, with the reasoning stated.

## Output Contract

Produce:
- code-health findings
- maintainability evidence map
- priority and leave-unchanged rationale
- bounded remediation options
- per-category status table from tool exits (composite score only when weights are supplied)

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `independent-code-review`
- `architecture-deepening-discovery`
- `defect-remediation`
- `developer-experience-assessment`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
