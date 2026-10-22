---
name: local-agent-memory-setup
description: "Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls. Use when A local, project-isolated memory or index runtime must be created with privacy, retention and removal terms; Someone asks whether a memory store can be set up without any remote sync and how to remove it. Do not use for: Save and search actual project context after the runtime exists (-> project-context-and-learning-store); Upgrade the installed workflow runtime version (-> workflow-runtime-upgrade); Write one new learning or context record (-> local-learning-persistence)."
---

# Local Agent Memory Setup

## Responsibility

Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls.

## Trigger

Use when the request matches any of:
- A local, project-isolated memory or index runtime must be created with privacy, retention and removal terms
- Someone asks whether a memory store can be set up without any remote sync and how to remove it

Do not use when:
- Save and search actual project context after the runtime exists. Route to `project-context-and-learning-store`.
- Upgrade the installed workflow runtime version. Route to `workflow-runtime-upgrade`.
- Write one new learning or context record. Route to `local-learning-persistence`.

## Required Inputs

- Project identity, runtime target, privacy choice, local-system write authorization, and retention policy.

## Procedure

1. Verify project identity, runtime target and version, local-system authorization, paths, data classes, exclusions, privacy, encryption if required, retention, deletion, external sync policy, backup, and rollback.
2. Preview exact local files, directories, services, ports, or config keys and refuse shared or global stores unless explicitly approved.
3. Create only the bounded project-isolated runtime and health check without ingesting project content beyond the declared fixture.
4. Record non-sensitive config identity, health evidence, isolation, size, retention, removal, rollback, and failure cleanup.

## Domain Guidance

- Remote or hosted memory backends, including ones that need an access token or a cloud database, are not covered. Return blocked for them and name the local-only alternative.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.

## Output Contract

Produce:
- project-isolated memory runtime
- non-sensitive configuration receipt
- health and isolation evidence
- removal and rollback instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `project-context-and-learning-store`
- `workflow-runtime-upgrade`
- `tool-runtime-readiness`
- `secrets-and-environment-governance`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
