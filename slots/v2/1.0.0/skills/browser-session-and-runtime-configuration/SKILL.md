---
name: browser-session-and-runtime-configuration
description: Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source. Do not use for persist authentication material into a browser profile or acquire page data or captures through the configured session.
---

# Browser Session And Runtime Configuration

## Responsibility

Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source.

## Trigger

Use when the requested outcome is: Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source.

Do not use when:
- Persist authentication material into a browser profile. Route to `browser-authentication-setup`.
- Acquire page data or captures through the configured session. Route to `browser-data-acquisition-runtime`.

## Required Inputs

- A validated browser task, session identifier, project path, wrapper contract, and CLI configuration.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify validated task, session identity, project path, wrapper contract, runtime and CLI versions, profile reference, ports, isolation, cleanup, and no-persistence rule.
2. Resolve invocation flags, environment references, output directories, timeouts, and wrapper dispatch without exposing credentials.
3. Run approved readiness or startup commands only for the ephemeral session and record command, version, exit, duration, runtime identifiers, and logs.
4. Return reproducible invocation settings, session state, degradation, and cleanup; do not authenticate, pair agents, acquire target data, or persist config.

## Output Contract

Produce:
- ephemeral browser session state
- reproducible wrapper and CLI invocation
- runtime evidence
- cleanup and degradation notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `ephemeral-session`
- `wrapper-contract`
- `project-isolation`
- `reproducible-invocation`
- `no-persistent-config`
- `cleanup`

## Hard Gates

- Session configuration is ephemeral runtime state: it cannot persist credentials or system config, pair agents, authorize data access, or perform the browser task itself.
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
- `browser-authentication-setup`
- `browser-agent-pairing-provisioning`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
