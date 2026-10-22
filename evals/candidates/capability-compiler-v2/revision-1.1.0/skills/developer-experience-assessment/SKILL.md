---
name: developer-experience-assessment
description: "Execute an authorized developer journey and measure time-to-first-success, setup, errors, documentation, compatibility, and recovery without changing product source. Use when A repository or developer product must be used end to end by a new contributor persona, timing each step; Someone asks how long first success takes and where setup, docs or errors slow a developer down. Do not use for: Review the proposed developer-experience plan before implementation (-> developer-experience-plan-review); Fix the documentation, scripts, or tooling exposed by the assessment (-> defect-remediation)."
---

# Developer Experience Assessment

## Responsibility

Execute an authorized developer journey and measure time-to-first-success, setup, errors, documentation, compatibility, and recovery without changing product source.

## Trigger

Use when the request matches any of:
- A repository or developer product must be used end to end by a new contributor persona, timing each step
- Someone asks how long first success takes and where setup, docs or errors slow a developer down

Do not use when:
- Review the proposed developer-experience plan before implementation. Route to `developer-experience-plan-review`.
- Fix the documentation, scripts, or tooling exposed by the assessment. Route to `defect-remediation`.

## Required Inputs

- Repository, runnable setup path, common tasks, errors, timings, and contributor context.

## Procedure

1. Freeze persona, journey, clean environment, source identity, supported platform, documented commands, credentials boundary, success criterion, and time budget.
2. Run only approved local commands and record elapsed time, decisions, errors, retries, workarounds, outputs, and cleanup.
3. Compare actual behavior with documentation, compatibility promises, error messages, discoverability, and recovery expectations.
4. Return reproducible friction and success evidence with severity and bounded recommendations; do not repair source.

## Domain Guidance

- Include documentation navigation and the copy-paste of each documented snippet in the journey: a command that is documented but fails when pasted is a finding with the exact snippet and error.

## Output Contract

Produce:
- developer journey trace
- time-to-first-success evidence
- friction and recovery findings
- bounded DX recommendations

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `real-journey`
- `time-to-first-success`
- `environment`
- `commands`
- `errors`
- `recovery`
- `cleanup`

## Hard Gates

- Developer experience claims require a real target-bound journey with recorded environment, commands, elapsed time, errors, recovery, and cleanup; reading docs alone is insufficient.
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
- `developer-experience-plan-review`
- `defect-remediation`
- `tool-runtime-readiness`
- `documentation-authoring`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
