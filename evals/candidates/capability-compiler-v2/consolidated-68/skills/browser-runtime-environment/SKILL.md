---
name: browser-runtime-environment
description: "Consolidated capability with 4 selectable modes: browser-agent-pairing-provisioning; browser-agent-pairing-verification; browser-authentication-setup; browser-session-and-runtime-configuration. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [browser-agent-pairing-provisioning, browser-agent-pairing-verification, browser-authentication-setup, browser-session-and-runtime-configuration]
---

# Browser Runtime Environment

## Responsibility

Consolidated capability covering 4 related modes: Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup.; Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration.; Configure authorized authentication state in one local browser profile for exact origins without exposing values or granting unrelated browsing authority.; Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `browser-agent-pairing-provisioning` | `local-system-write-external-session-authorized-only` | Another AI agent needs scoped, expiring access to a local browser session and someone must set up the pairing; Someone asks what a pairing would expose, for how long and how to revoke it. | Verify an existing pairing's connection and observed scope without changing it (-> browser-agent-pairing-verification);  |
| `browser-agent-pairing-verification` | `local-exec-external-read` | An existing browser-agent pairing must be checked for health, expiry and whether its scope matches what was approved; Someone asks why a paired agent cannot act, or whether a pairing is broader than i | Create or renew the pairing credential and local configuration (-> browser-agent-pairing-provisioning); Configure target |
| `browser-authentication-setup` | `local-system-write-authorized-only` | A browser profile needs logged-in state for one exact origin so later read-only acquisition can proceed; Someone asks to import or configure authentication for a site without exposing credential value | Acquire governed page data using an already-authenticated browser session (-> browser-data-acquisition-runtime); Provisi |
| `browser-session-and-runtime-configuration` | `local-exec` | An isolated, temporary browser session with a wrapper command and output directory must be prepared for a validated task; Someone asks for the exact invocation and session settings without persisting  | Persist authentication material into a browser profile (-> browser-authentication-setup); Acquire page data or captures  |

## Mode: `browser-agent-pairing-provisioning`

### browser-agent-pairing-provisioning

#### Responsibility

Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup.

#### Trigger

Use when the request matches any of:
- Another AI agent needs scoped, expiring access to a local browser session and someone must set up the pairing
- Someone asks what a pairing would expose, for how long and how to revoke it

Do not use when:
- Verify an existing pairing's connection and observed scope without changing it. Route to `browser-agent-pairing-verification`.
- Configure browser authentication material for a target origin locally. Route to `browser-authentication-setup`.

#### Required Inputs

- Running browser daemon, selected agent, local or remote mode, scope restrictions, credential retention, and explicit authorization.

#### Procedure

1. Verify daemon identity and health, selected agent, local or remote mode, origins and actions, network exposure, credential owner, expiry, retention, revocation, cleanup, and per-action authorization.
2. State whether the pairing relaunches the browser daemon and what open tabs, cookies and sessions would be lost; require explicit consent for that loss.
3. Preview exact listening interface, transport, credential storage, scope, lifetime, and exposure; refuse wildcard or indefinite access by default.
4. Perform only the approved pairing and local receipt update without revealing credential values in output or evidence.
5. Record non-secret pairing identity, scope, expiry, connection instructions, storage boundary, revocation command, exposure, and cleanup status.

#### Domain Guidance

- Preview the session-loss consequence before anything runs: pairing can relaunch the browser daemon, and a relaunch kills open tabs, cookies and logged-in sessions. Require explicit consent for a relaunch as a one-way action, and offer a pairing path that does not relaunch when one exists.
- Treat daemon relaunch and session loss as conditional provider behavior: claim it only when supplied or observed for the exact pairing path. Otherwise mark relaunch, tabs, cookies and login-session impact unknown and request provider evidence before consent.
- Do not import relaunch/session-loss rules from other browser pairing providers. Apply them only when the exact provider path supplies or verifies that behavior. Keep revocation command semantics separate from verified credential-file deletion; a --wipe flag does not prove deletion.

#### Output Contract

Produce:
- scoped pairing identity
- non-secret local configuration receipt
- expiry and revocation instructions
- network exposure and cleanup evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `per-action-authorization`
- `scoped-agent`
- `origin-action-scope`
- `expiry`
- `revocation`
- `network-exposure`
- `no-secret-output`

#### Hard Gates

- Pairing requires per-action authorization for exact agent, origins, actions, transport, exposure, and expiry; wildcard, hidden, reusable, or non-revocable credentials are blocked.
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
- `browser-agent-pairing-verification`
- `browser-authentication-setup`
- `browser-session-and-runtime-configuration`
- `provider-cli-authentication-setup`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `browser-agent-pairing-verification`

### browser-agent-pairing-verification

#### Responsibility

Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration.

#### Trigger

Use when the request matches any of:
- An existing browser-agent pairing must be checked for health, expiry and whether its scope matches what was approved
- Someone asks why a paired agent cannot act, or whether a pairing is broader than intended

Do not use when:
- Create or renew the pairing credential and local configuration. Route to `browser-agent-pairing-provisioning`.
- Configure target-origin authentication material in the browser profile. Route to `browser-authentication-setup`.

#### Required Inputs

- Pairing identity, browser status, expected scope, target platform, and permitted external read boundary.

#### Procedure

1. Freeze pairing identity, expected agent, transport, origins, actions, expiry, browser status, permitted external read, and prohibited changes.
2. Run approved health, connection, expiry, origin, and observed-scope checks without reading credential values.
3. Compare expected and observed identity and scope; classify disconnected, expired, mismatched, overbroad, healthy, or unverifiable.
4. Return evidence and a bounded re-provisioning recommendation; do not mint, renew, restart, widen, or edit configuration.

#### Domain Guidance

- Diagnosis table: 'tab not owned by your agent' means the agent acted on a tab it did not create and must open its own tab; 'domain not allowed' means the token restricts domains and the pairing needs re-provisioning with the needed origin; an expired token needs renewal through the provisioning Skill.
- After the remote agent is told to connect, confirm the connection from the browser status output and report which agent and scope appear.

#### Output Contract

Produce:
- pairing connection verdict
- expected-versus-observed scope
- diagnosis evidence
- bounded re-provisioning recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `existing-pairing`
- `expected-observed-scope`
- `read-only-verification`
- `no-mint`
- `no-config-change`
- `no-data-authority`

#### Hard Gates

- Verification authority is read-only: it cannot mint or renew credentials, restart the daemon, change config, widen scope, or treat connectivity as data-access authorization.
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

#### External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `browser-agent-pairing-provisioning`
- `browser-authentication-setup`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `browser-authentication-setup`

### browser-authentication-setup

#### Responsibility

Configure authorized authentication state in one local browser profile for exact origins without exposing values or granting unrelated browsing authority.

#### Trigger

Use when the request matches any of:
- A browser profile needs logged-in state for one exact origin so later read-only acquisition can proceed
- Someone asks to import or configure authentication for a site without exposing credential values

Do not use when:
- Acquire governed page data using an already-authenticated browser session. Route to `browser-data-acquisition-runtime`.
- Provision credentials that pair an external agent with the browser. Route to `browser-agent-pairing-provisioning`.

#### Required Inputs

- Browser profile, target origin, credential authority, local-system write authorization, retention, and deletion policy.

#### Procedure

1. Check whether the runtime is already attached to the user's authenticated browser; if so return a no-write outcome.
2. Verify browser profile, exact origins, credential owner, authentication method, local-system authorization, storage, retention, expiry, deletion, allowed validation, and prohibited output.
3. Back up or identify reversible profile state and preview exact files or browser stores affected without reading values into model context.
4. Perform only the approved local setup through the host, using native secure storage where available and never logging or persisting credential values in evidence.
5. Validate non-secret authentication status for the exact origin and record storage boundary, expiry, cleanup, rollback, and failure evidence.

#### Domain Guidance

- First check whether the runtime is already attached to the user's real, already authenticated browser. If so, return a no-write outcome stating that no import is needed, and do not copy any cookies.

#### Output Contract

Produce:
- configured local authentication state
- non-secret validation receipt
- storage and origin boundary
- expiry, cleanup, and rollback instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-origin`
- `secure-storage`
- `no-credential-output`
- `non-secret-validation`
- `expiry`
- `cleanup`
- `no-data-authority`

#### Hard Gates

- Authentication setup grants neither page-data authority nor general browsing scope; credential values never enter prompts, logs, hashes, receipts, or artifacts.
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
- `browser-data-acquisition-runtime`
- `browser-agent-pairing-provisioning`
- `browser-session-and-runtime-configuration`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `browser-session-and-runtime-configuration`

### browser-session-and-runtime-configuration

#### Responsibility

Create an isolated ephemeral browser runtime invocation from validated prerequisites without writing persistent auth, pairing, or project source.

#### Trigger

Use when the request matches any of:
- An isolated, temporary browser session with a wrapper command and output directory must be prepared for a validated task
- Someone asks for the exact invocation and session settings without persisting any login or configuration

Do not use when:
- Persist authentication material into a browser profile. Route to `browser-authentication-setup`.
- Acquire page data or captures through the configured session. Route to `browser-data-acquisition-runtime`.

#### Required Inputs

- A validated browser task, session identifier, project path, wrapper contract, and CLI configuration.

#### Procedure

1. Verify validated task, session identity, project path, wrapper contract, runtime and CLI versions, profile reference, ports, isolation, cleanup, and no-persistence rule.
2. Resolve invocation flags, environment references, output directories, timeouts, and wrapper dispatch without exposing credentials.
3. Run approved readiness or startup commands only for the ephemeral session and record command, version, exit, duration, runtime identifiers, and logs.
4. Return reproducible invocation settings, session state, degradation, and cleanup; do not authenticate, pair agents, acquire target data, or persist config.

#### Domain Guidance

- Prerequisite: confirm that npx is available (command -v npx); if not, pause and ask for Node.js and npm. Record the config file path that the task names, or 'none named' when it names none; do not claim that a default config file or dependency exists unless the task says so.
- When a task supplies an exact browser/runtime version, pin it in the proposed invocation or mark the invocation blocked. Record hashes for generated config and output artifacts; placeholders are not completion evidence. Name the actual policy/template owner when supplied, otherwise mark the authorizer unknown.
- Use only prerequisites named by the exact wrapper contract; do not add npx, browser-binding or approval gates from other providers. Every proposed isolated profile includes an explicit empty-directory preflight check and result placeholder.

#### Output Contract

Produce:
- ephemeral browser session state
- reproducible wrapper and CLI invocation
- runtime evidence
- cleanup and degradation notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `ephemeral-session`
- `wrapper-contract`
- `project-isolation`
- `reproducible-invocation`
- `no-persistent-config`
- `cleanup`

#### Hard Gates

- Session configuration is ephemeral runtime state: it cannot persist credentials or system config, pair agents, authorize data access, or perform the browser task itself.
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
- `browser-authentication-setup`
- `browser-agent-pairing-provisioning`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
