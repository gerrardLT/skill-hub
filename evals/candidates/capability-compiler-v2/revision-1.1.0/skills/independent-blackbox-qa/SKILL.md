---
name: independent-blackbox-qa
description: "Independently exercise a built product through public user surfaces, record reproducible findings and evidence, and never inspect or repair source. Use when A built product must be exercised through its public surfaces by someone who has not seen the source; Someone asks for numbered, reproducible QA findings with route, state and expected versus observed behavior. Do not use for: Triage existing QA findings by reproducibility, severity, and owner (-> qa-finding-triage); Apply source repairs for accepted QA defects (-> defect-remediation)."
---

# Independent Blackbox QA

## Responsibility

Independently exercise a built product through public user surfaces, record reproducible findings and evidence, and never inspect or repair source.

## Trigger

Use when the request matches any of:
- A built product must be exercised through its public surfaces by someone who has not seen the source
- Someone asks for numbered, reproducible QA findings with route, state and expected versus observed behavior

Do not use when:
- Triage existing QA findings by reproducibility, severity, and owner. Route to `qa-finding-triage`.
- Apply source repairs for accepted QA defects. Route to `defect-remediation`.

## Required Inputs

- An accessible application, change scope, QA mode, and authorized interaction boundary.

## Procedure

1. Freeze build identity, environment, user roles, test accounts or fixtures, public surfaces, acceptance criteria, supported devices, data boundary, and prohibited actions.
2. Exercise task, boundary, invalid, error, permission, concurrency, interruption, recovery, accessibility, responsive, and persistence behavior through public interfaces only.
3. Record exact setup, steps, observed and expected result, route or API, state, environment, screenshot or trace, logs allowed to a user, and reproducibility.
4. Return numbered findings, blocked tests, coverage, and residual risk; do not read source, infer internals as fact, or repair anything.

## Domain Guidance

- A change-scope summary supplied by another owner may focus the test plan (routes, features, risk areas). It is an input, not permission to read source.

## Output Contract

Produce:
- black-box QA run record
- reproducible numbered findings
- route-state coverage matrix
- blocked tests and residual risk

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `public-surfaces`
- `current-build`
- `reproducible-steps`
- `expected-observed`
- `independence`
- `no-source-inspection`
- `no-repair`

## Hard Gates

- Black-box QA must use public product surfaces and current build evidence; source inspection, implementation knowledge, or self-repair invalidates reviewer independence.
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
- `qa-finding-triage`
- `defect-remediation`
- `ui-review-scope-and-evidence-acquisition`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
