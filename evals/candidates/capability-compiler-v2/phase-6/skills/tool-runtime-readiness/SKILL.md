---
name: tool-runtime-readiness
description: Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it. Do not use for install or upgrade the missing workflow runtime or bootstrap a project-local test framework and modify dependency files.
---

# Tool Runtime Readiness

## Responsibility

Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it.

## Trigger

Use when the requested outcome is: Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it.

Do not use when:
- Install or upgrade the missing workflow runtime. Route to `workflow-runtime-upgrade`.
- Bootstrap a project-local test framework and modify dependency files. Route to `test-runtime-bootstrap`.

## Required Inputs

- A tool request, project path, shell environment, and declared prerequisite contract.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze tool identity, required version or range, source, invocation, capability, platform, project context, prohibited actions, and expected smoke result.
2. Resolve the actual executable or wrapper and compare version and capability without trusting PATH presence alone.
3. Run only an approved non-destructive help, version, doctor, or bounded smoke command and record path, version, command, exit, duration, output, and side effects.
4. Return ready, incompatible, missing, blocked, or failed with exact upgrade or bootstrap handoff; do not install or modify configuration.

## Output Contract

Produce:
- tool readiness verdict
- executable and version evidence
- bounded smoke command record
- upgrade or bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `executable-path`
- `version`
- `required-capability`
- `bounded-smoke`
- `no-install`
- `failure-mode`

## Hard Gates

- PATH presence is not readiness: the exact executable, version, required capability, invocation, and bounded smoke behavior must be verified without installation or configuration changes.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `workflow-runtime-upgrade`
- `test-runtime-bootstrap`
- `agent-workflow-runtime-support`
- `document-rendering-and-validation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
