---
name: browser-session-and-runtime-configuration
description: "Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source. Use when An isolated, temporary browser session with a wrapper command and output directory must be prepared for a validated task; Someone asks for the exact invocation and session settings without persisting any login or configuration. Do not use for: Persist authentication material into a browser profile (-> browser-authentication-setup); Acquire page data or captures through the configured session (-> browser-data-acquisition-runtime)."
---

# Browser Session And Runtime Configuration

## Responsibility

Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source.

## Trigger

Use when the request matches any of:
- An isolated, temporary browser session with a wrapper command and output directory must be prepared for a validated task
- Someone asks for the exact invocation and session settings without persisting any login or configuration

Do not use when:
- Persist authentication material into a browser profile. Route to `browser-authentication-setup`.
- Acquire page data or captures through the configured session. Route to `browser-data-acquisition-runtime`.

## Required Inputs

- A validated browser task, session identifier, project path, wrapper contract, and CLI configuration.

## Procedure

1. Verify validated task, session identity, project path, wrapper contract, runtime and CLI versions, profile reference, ports, isolation, cleanup, and no-persistence rule.
2. Resolve invocation flags, environment references, output directories, timeouts, and wrapper dispatch without exposing credentials.
3. Run approved readiness or startup commands only for the ephemeral session and record command, version, exit, duration, runtime identifiers, and logs.
4. Return reproducible invocation settings, session state, degradation, and cleanup; do not authenticate, pair agents, acquire target data, or persist config.

## Domain Guidance

- Prerequisite: confirm that npx is available (command -v npx); if not, pause and ask for Node.js and npm. Record the config file path that the task names, or 'none named' when it names none; do not claim that a default config file or dependency exists unless the task says so.
- When a task supplies an exact browser/runtime version, pin it in the proposed invocation or mark the invocation blocked. Record hashes for generated config and output artifacts; placeholders are not completion evidence. Name the actual policy/template owner when supplied, otherwise mark the authorizer unknown.
- Use only prerequisites named by the exact wrapper contract; do not add npx, browser-binding or approval gates from other providers. Every proposed isolated profile includes an explicit empty-directory preflight check and result placeholder.

## Output Contract

Produce:
- ephemeral browser session state
- reproducible wrapper and CLI invocation
- runtime evidence
- cleanup and degradation notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `ephemeral-session`
- `wrapper-contract`
- `project-isolation`
- `reproducible-invocation`
- `no-persistent-config`
- `cleanup`

## Hard Gates

- Session configuration is ephemeral runtime state: it cannot persist credentials or system config, pair agents, authorize data access, or perform the browser task itself.
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
- `browser-authentication-setup`
- `browser-agent-pairing-provisioning`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
