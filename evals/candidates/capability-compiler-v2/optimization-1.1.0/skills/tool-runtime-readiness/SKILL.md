---
name: tool-runtime-readiness
description: "Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it. Use when A required local tool must be confirmed present, at the right version and able to do what the task needs; Someone asks whether a tool on the path is actually usable before an owner starts work. Do not use for: Install or upgrade the missing workflow runtime (-> workflow-runtime-upgrade); Bootstrap a project-local test framework and modify dependency files (-> test-runtime-bootstrap)."
---

# Tool Runtime Readiness

## Responsibility

Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it.

## Trigger

Use when the request matches any of:
- A required local tool must be confirmed present, at the right version and able to do what the task needs
- Someone asks whether a tool on the path is actually usable before an owner starts work

Do not use when:
- Install or upgrade the missing workflow runtime. Route to `workflow-runtime-upgrade`.
- Bootstrap a project-local test framework and modify dependency files. Route to `test-runtime-bootstrap`.

## Required Inputs

- A tool request, project path, shell environment, and declared prerequisite contract.

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

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `executable-path`
- `version`
- `required-capability`
- `bounded-smoke`
- `no-install`
- `failure-mode`

## Hard Gates

- PATH presence is not readiness: the exact executable, version, required capability, invocation, and bounded smoke behavior must be verified without installation or configuration changes.
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
- `workflow-runtime-upgrade`
- `test-runtime-bootstrap`
- `agent-workflow-runtime-support`
- `document-rendering-and-validation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
