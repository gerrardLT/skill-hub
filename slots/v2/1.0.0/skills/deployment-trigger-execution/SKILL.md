---
name: deployment-trigger-execution
description: Trigger one exact approved deployment workflow or hook with frozen parameters and per-action authorization, without merging code or observing or rolling back the result. Do not use for check deployment and merge readiness before triggering anything or observe the triggered deployment and production health without changing it.
---

# Deployment Trigger Execution

## Responsibility

Trigger one exact approved deployment workflow or hook with frozen parameters and per-action authorization, without merging code or observing or rolling back the result.

## Trigger

Use when the requested outcome is: Trigger one exact approved deployment workflow or hook with frozen parameters and per-action authorization, without merging code or observing or rolling back the result.

Do not use when:
- Check deployment and merge readiness before triggering anything. Route to `merge-and-deploy-readiness`.
- Observe the triggered deployment and production health without changing it. Route to `deployment-observation`.

## Required Inputs

- Release identity, reviewed deployment target, frozen parameters, provider or hook adapter, credentials, and current authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify exact workflow or hook, provider, repository or project, environment, artifact digest, config version, parameters, identity, budget, blast radius, timeout, cancellation, rollback owner, idempotency, and fresh per-action authorization.
2. Preview or dry-run the exact request where supported and record expected effects without exposing secrets.
3. Perform one bounded trigger; do not merge, alter config, select a different artifact, promote, observe, or rollback.
4. Record durable trigger receipt, run identity, request hash, status-at-return, duration, partial failure, retry prohibition or bounded retry, and cancellation path.

## Output Contract

Produce:
- deployment trigger receipt
- immutable request and artifact identity
- run or hook identity
- failure, cancellation, and handoff record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `per-action-authorization`
- `exact-target`
- `artifact-digest`
- `frozen-parameters`
- `idempotency`
- `trigger-receipt`
- `cancellation`

## Hard Gates

- One deployment-trigger authorization covers one exact workflow, environment, immutable artifact, parameter set, and attempt; it authorizes neither merge, configuration change, observation, promotion, nor rollback.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This candidate defines an action contract, but Phase 7 candidate construction does not execute the action. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `merge-and-deploy-readiness`
- `deployment-observation`
- `release-rollback-execution`
- `web-hosting-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
