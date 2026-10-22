---
name: local-agent-memory-setup
description: Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls. Do not use for save and search actual project context after the runtime exists or upgrade the installed workflow runtime version.
---

# Local Agent Memory Setup

## Responsibility

Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls.

## Trigger

Use when the requested outcome is: Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls.

Do not use when:
- Save and search actual project context after the runtime exists. Route to `project-context-and-learning-store`.
- Upgrade the installed workflow runtime version. Route to `workflow-runtime-upgrade`.

## Required Inputs

- Project identity, runtime target, privacy choice, local-system write authorization, and retention policy.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify project identity, runtime target and version, local-system authorization, paths, data classes, exclusions, privacy, encryption if required, retention, deletion, external sync policy, backup, and rollback.
2. Preview exact local files, directories, services, ports, or config keys and refuse shared or global stores unless explicitly approved.
3. Create only the bounded project-isolated runtime and health check without ingesting project content beyond the declared fixture.
4. Record non-sensitive config identity, health evidence, isolation, size, retention, removal, rollback, and failure cleanup.

## Output Contract

Produce:
- project-isolated memory runtime
- non-sensitive configuration receipt
- health and isolation evidence
- removal and rollback instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `project-isolation`
- `privacy`
- `retention`
- `deletion`
- `no-implicit-sync`
- `health-check`
- `rollback`

## Hard Gates

- Local memory setup requires explicit project isolation, privacy, retention, deletion, and rollback; it cannot ingest arbitrary project data or enable external synchronization implicitly.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `project-context-and-learning-store`
- `workflow-runtime-upgrade`
- `tool-runtime-readiness`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
