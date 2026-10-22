---
name: test-framework-tooling
description: "Consolidated capability with 4 selectable modes: playwright-test-engineering; test-double-discipline; vitest-tooling; website-audit-assessment. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [playwright-test-engineering, test-double-discipline, vitest-tooling, website-audit-assessment]
---

# Test Framework Tooling

## Responsibility

Consolidated capability covering 4 related modes: Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source.; Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces.; Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source.; Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `playwright-test-engineering` | `local-exec` | A browser behavior needs an end-to-end Playwright test designed, or existing Playwright tests need running and diagnosing; Someone asks for role-based locators, web-first assertions and isolated fixtu | Install and configure Playwright in the project and write a real first test (-> test-runtime-bootstrap); Perform product |
| `test-double-discipline` | `local-exec` | A test needs isolation from a dependency and someone must decide between real code, a fake, a stub or a mock; Someone asks whether a mock is testing behavior or just mirroring the implementation. | Implement and run the full test through the selected framework (-> vitest-tooling); Design the project-wide balance of u |
| `vitest-tooling` | `local-exec` | A JavaScript or TypeScript unit or integration test needs designing, or an existing Vitest suite needs running and diagnosing; Someone asks for controlled time, isolated modules and cleanup in Vitest  | Install and configure Vitest in a project that lacks a test runtime (-> test-runtime-bootstrap); Define the minimal test |
| `website-audit-assessment` | `local-exec-external-read` | An authorized website needs an independent audit across content, accessibility, SEO, performance, security signals and links; Someone asks for a reproducible findings list and a before and after compa | Apply the accepted website audit fixes to authorized source (-> website-audit-remediation); Run a narrow Web performance |

## Mode: `playwright-test-engineering`

### playwright-test-engineering

#### Responsibility

Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source.

#### Trigger

Use when the request matches any of:
- A browser behavior needs an end-to-end Playwright test designed, or existing Playwright tests need running and diagnosing
- Someone asks for role-based locators, web-first assertions and isolated fixtures for a user journey

Do not use when:
- Install and configure Playwright in the project and write a real first test. Route to `test-runtime-bootstrap`.
- Perform product-level black-box QA and issue release findings. Route to `independent-blackbox-qa`.
- Write or run unit or integration tests for Node modules with Vitest. Route to `vitest-tooling`.

#### Required Inputs

- Browser behaviors, test environments, risks, data, and automation acceptance goals.

#### Procedure

1. Freeze behavior, environment, project conventions, runtime availability, data and auth boundary, browser matrix, risks, and acceptance goal.
2. Prefer user-visible behavior, role or contract locators, web-first assertions, isolated data, complete auth state, and deterministic waiting; avoid implementation selectors and sleeps.
3. Emit candidate test, fixture, config, or locator changes as an artifact; only run authorized existing project tests and collect traces, screenshots, video, and exits.
4. Return candidate source, run evidence or blocked bootstrap handoff, flake controls, and limitations; do not modify project files under a local-exec identity.

#### Domain Guidance

- Candidate tests are delivered as artifacts. Applying them to the project is a separate authorized step owned by tdd-change-loop or isolated-task-implementation; name the one that fits and hand the artifact over.

#### Output Contract

Produce:
- Playwright candidate test artifact
- fixture and locator design
- existing-test execution evidence
- flake and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `candidate-test-artifact`
- `role-locator`
- `web-first-assertion`
- `isolated-fixture`
- `deterministic-wait`
- `no-project-write`

#### Hard Gates

- A local-exec Playwright candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `test-runtime-bootstrap`
- `independent-blackbox-qa`
- `safe-browser-probing`
- `test-double-discipline`
- `vitest-tooling`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `test-double-discipline`

### test-double-discipline

#### Responsibility

Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces.

#### Trigger

Use when the request matches any of:
- A test needs isolation from a dependency and someone must decide between real code, a fake, a stub or a mock
- Someone asks whether a mock is testing behavior or just mirroring the implementation

Do not use when:
- Implement and run the full test through the selected framework. Route to `vitest-tooling`.
- Design the project-wide balance of unit, integration, contract, and end-to-end tests. Route to `testing-portfolio-strategy`.

#### Required Inputs

- A test design that requires dependency isolation or an existing test double.

#### Procedure

1. Freeze the behavior under test, real dependency contract, failure modes, speed or isolation need, existing double, and production boundary.
2. Prefer real code, in-memory implementation, fake server, contract fixture, or dependency injection before mocks and spies.
3. Keep the double at an owned boundary, provide complete realistic shapes and failures, and avoid test-only methods in production APIs.
4. Use approved local analysis or tests to expose brittle coupling and return a minimal strategy or candidate artifact without project-source mutation.

#### Output Contract

Produce:
- test-double decision
- owned boundary and contract
- complete fixture or fake design
- anti-pattern and verification evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `owned-boundary`
- `real-code-first`
- `complete-shape`
- `meaningful-failure`
- `no-internal-mock`
- `no-test-only-production-api`

#### Hard Gates

- A double is justified only at a real owned boundary and must preserve complete contract shapes and meaningful failures; mocking internals or adding test-only production APIs fails.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `vitest-tooling`
- `playwright-test-engineering`
- `testing-portfolio-strategy`
- `tdd-change-loop`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `vitest-tooling`

### vitest-tooling

#### Responsibility

Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source.

#### Trigger

Use when the request matches any of:
- A JavaScript or TypeScript unit or integration test needs designing, or an existing Vitest suite needs running and diagnosing
- Someone asks for controlled time, isolated modules and cleanup in Vitest tests

Do not use when:
- Install and configure Vitest in a project that lacks a test runtime. Route to `test-runtime-bootstrap`.
- Define the minimal test-double boundary before writing mocks. Route to `test-double-discipline`.
- Write or run browser end-to-end tests. Route to `playwright-test-engineering`.

#### Required Inputs

- A JavaScript or TypeScript unit or integration test project using Vitest.

#### Procedure

1. Freeze behavior, project conventions, existing config, runtime availability, module boundaries, data, environment, and accepted command.
2. Use behavior-focused assertions, complete fixtures, controlled time, explicit cleanup, isolated modules, and stable snapshots only where semantically useful.
3. Emit candidate test or config source as an artifact; run only existing authorized project tests and record command, version, exit, duration, and output.
4. Return candidate source, diagnosis, test-double concerns, and bootstrap handoff; do not modify project files under a local-exec identity.

#### Domain Guidance

- Type tests use the .test-d.ts suffix with expectTypeOf. Run one test by file and line (vitest path/file.test.ts:10), use vitest run in CI, and pass a name filter to narrow a run.

#### Output Contract

Produce:
- Vitest candidate test artifact
- configuration or fixture design
- existing-suite execution evidence
- diagnosis and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `candidate-test-artifact`
- `behavior-assertion`
- `controlled-time`
- `cleanup`
- `isolation`
- `no-project-write`

#### Hard Gates

- A local-exec Vitest candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `test-runtime-bootstrap`
- `test-double-discipline`
- `tdd-change-loop`
- `testing-portfolio-strategy`
- `playwright-test-engineering`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `website-audit-assessment`

### website-audit-assessment

#### Responsibility

Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation.

#### Trigger

Use when the request matches any of:
- An authorized website needs an independent audit across content, accessibility, SEO, performance, security signals and links
- Someone asks for a reproducible findings list and a before and after comparison with an earlier audit

Do not use when:
- Apply the accepted website audit fixes to authorized source. Route to `website-audit-remediation`.
- Run a narrow Web performance diagnostic under controlled conditions. Route to `web-performance-diagnostics`.

#### Required Inputs

- A scannable site, audit CLI, permitted external read scope, and optional frozen baseline.

#### Procedure

1. Freeze authorized origins, routes, crawl limits, authentication boundary, data policy, source or deployment identity, devices, criteria, and prohibited actions.
2. Use approved local commands and read-only external requests or browser actions; respect robots, rate, privacy, account, purchase, and destructive-state boundaries.
3. Record route, request, tool, version, timestamp, state, viewport, response, capture, hash, and reproducibility for each assessed criterion.
4. Issue deduplicated findings with severity, evidence, affected routes, owner, and reassessment requirement; do not repair, deploy, or post externally.

#### Domain Guidance

- When a prior audit exists, reassess with a baseline diff (regression since the baseline) and report new, fixed and unchanged findings rather than only a fresh list.

#### Output Contract

Produce:
- website assessment evidence manifest
- deduplicated reproducible findings
- route and criterion coverage
- reassessment and residual-risk report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `authorized-origins`
- `read-only-external`
- `crawl-limit`
- `criterion-evidence`
- `reproducible-finding`
- `no-remediation`

#### Hard Gates

- Assessment authority is read-only: no source repair, form submission with consequential state, account change, provider mutation, deployment, or finding closure is permitted.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

#### External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `website-audit-remediation`
- `web-performance-diagnostics`
- `safe-browser-probing`
- `ui-review-scope-and-evidence-acquisition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
