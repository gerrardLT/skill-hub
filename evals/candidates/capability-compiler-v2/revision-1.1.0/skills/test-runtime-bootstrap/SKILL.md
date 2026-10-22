---
name: test-runtime-bootstrap
description: "Install and configure one approved project-local test runtime, prove it with one real-behavior test, and restore dependency files if setup fails. Use when A project has no working test runtime and one approved framework must be installed with a proving test; Someone asks for the smallest change that lets a project run tests, with a restore path if setup fails. Do not use for: Design the overall test strategy before a framework is selected (-> testing-portfolio-strategy); Author advanced tests once the runtime already exists (-> vitest-tooling)."
---

# Test Runtime Bootstrap

## Responsibility

Install and configure one approved project-local test runtime, prove it with one real-behavior test, and restore dependency files if setup fails.

## Trigger

Use when the request matches any of:
- A project has no working test runtime and one approved framework must be installed with a proving test
- Someone asks for the smallest change that lets a project run tests, with a restore path if setup fails

Do not use when:
- Design the overall test strategy before a framework is selected. Route to `testing-portfolio-strategy`.
- Author advanced tests once the runtime already exists. Route to `vitest-tooling`.

## Required Inputs

- Project runtime, selected test framework, package policy, workspace authority, install command, and rollback baseline.

## Procedure

1. Freeze project runtime, selected framework and version, package manager, install source, package policy, authorized files, example behavior, commands, and rollback baseline.
2. Inspect existing dependencies and config; use the current toolchain and add the minimum packages and configuration only if absent.
3. Write one real-behavior smoke test, run the approved command through the host, and capture dependency diff, tool version, exit, duration, and output.
4. On any failed install, config, or proof, restore dependency and config files to the baseline and report failure; never change global tooling or remote systems.

## Domain Guidance

- When no framework is selected, propose defaults from project markers (for example manage.py: pytest with Django, package.json: Vitest or Jest, Gemfile: RSpec) as an offer; never run an install on a guess.

## Output Contract

Produce:
- minimal project test configuration
- one passing real-behavior test
- dependency and lockfile diff
- verification or rollback evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `project-local`
- `minimal-install`
- `real-behavior-test`
- `dependency-diff`
- `rollback-baseline`
- `no-global-change`

## Hard Gates

- Bootstrap passes only when the project-local runtime and one real-behavior test run successfully; failed setup must restore dependency and configuration files exactly.
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
- `testing-portfolio-strategy`
- `vitest-tooling`
- `playwright-test-engineering`
- `workflow-runtime-upgrade`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
