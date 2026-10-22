---
name: independent-blackbox-qa
description: Independently exercise a built product through public user surfaces, record reproducible findings and evidence, and never inspect or repair source. Do not use for triage existing qa findings by reproducibility, severity, and owner or apply source repairs for accepted qa defects.
---

# Independent Blackbox Qa

## Responsibility

Independently exercise a built product through public user surfaces, record reproducible findings and evidence, and never inspect or repair source.

## Trigger

Use when the requested outcome is: Independently exercise a built product through public user surfaces, record reproducible findings and evidence, and never inspect or repair source.

Do not use when:
- Triage existing QA findings by reproducibility, severity, and owner. Route to `qa-finding-triage`.
- Apply source repairs for accepted QA defects. Route to `defect-remediation`.

## Required Inputs

- An accessible application, change scope, QA mode, and authorized interaction boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze build identity, environment, user roles, test accounts or fixtures, public surfaces, acceptance criteria, supported devices, data boundary, and prohibited actions.
2. Exercise task, boundary, invalid, error, permission, concurrency, interruption, recovery, accessibility, responsive, and persistence behavior through public interfaces only.
3. Record exact setup, steps, observed and expected result, route or API, state, environment, screenshot or trace, logs allowed to a user, and reproducibility.
4. Return numbered findings, blocked tests, coverage, and residual risk; do not read source, infer internals as fact, or repair anything.

## Output Contract

Produce:
- black-box QA run record
- reproducible numbered findings
- route-state coverage matrix
- blocked tests and residual risk

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- `qa-finding-triage`
- `defect-remediation`
- `ui-review-scope-and-evidence-acquisition`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
