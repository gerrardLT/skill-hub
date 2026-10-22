---
name: provider-cli-authentication-setup
description: Install or authenticate one exact provider CLI after explicit local-system, credential, and external-session authorization, preserving non-secret identity, expiry, revocation, and cleanup evidence. Do not use for execute the reviewed provider experiment after authentication or verify an existing browser-agent pairing rather than a provider cli session.
---

# Provider Cli Authentication Setup

## Responsibility

Install or authenticate one exact provider CLI after explicit local-system, credential, and external-session authorization, preserving non-secret identity, expiry, revocation, and cleanup evidence.

## Trigger

Use when the requested outcome is: Install or authenticate one exact provider CLI after explicit local-system, credential, and external-session authorization, preserving non-secret identity, expiry, revocation, and cleanup evidence.

Do not use when:
- Execute the reviewed provider experiment after authentication. Route to `llm-experiment-execution`.
- Verify an existing browser-agent pairing rather than a provider CLI session. Route to `browser-agent-pairing-verification`.

## Required Inputs

- Provider CLI, version or install source, local-system authority, credential owner, authentication method, and cleanup policy.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify provider, CLI source and version, platform, account owner, authentication method, scopes, region, storage, expiry, revocation, cleanup, local-system and per-action external-session authorization.
2. Preview exact binary source, files, config keys, browser or device login flow, scopes, and persistent session effects; refuse pasted secrets or overbroad scopes.
3. Perform only the approved install or authentication through the host, keeping credential values out of model, logs, hashes, and receipts.
4. Validate non-secret CLI identity and scope, then record version, account alias, region, expiry, storage, revocation, uninstall, cleanup, and failure state.

## Output Contract

Produce:
- verified CLI version and non-secret identity
- scope and storage boundary
- expiry and revocation path
- uninstall, cleanup, and failure evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-provider`
- `approved-version`
- `least-scope`
- `non-secret-identity`
- `expiry`
- `revocation`
- `no-provider-action`

## Hard Gates

- CLI authentication is setup authority only: it cannot execute provider mutations, and credential values or recovery codes never enter prompts, logs, hashes, or artifacts.
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
- `llm-experiment-execution`
- `evaluation-dataset-publication`
- `browser-agent-pairing-verification`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
