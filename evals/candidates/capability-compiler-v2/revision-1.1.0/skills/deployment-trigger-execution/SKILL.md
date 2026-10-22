---
name: deployment-trigger-execution
description: "Trigger one exact approved deployment workflow or hook with frozen parameters and per-action authorization, without merging code or observing or rolling back the result. Use when One approved deployment workflow or hook must be triggered with frozen parameters and fresh authorization; Someone asks for the exact trigger request, run identity and cancellation path for a specific release. Do not use for: Check deployment and merge readiness before triggering anything (-> merge-and-deploy-readiness); Observe the triggered deployment and production health without changing it (-> deployment-observation)."
---

# Deployment Trigger Execution

## Responsibility

Trigger one exact approved deployment workflow or hook with frozen parameters and per-action authorization, without merging code or observing or rolling back the result.

## Trigger

Use when the request matches any of:
- One approved deployment workflow or hook must be triggered with frozen parameters and fresh authorization
- Someone asks for the exact trigger request, run identity and cancellation path for a specific release

Do not use when:
- Check deployment and merge readiness before triggering anything. Route to `merge-and-deploy-readiness`.
- Observe the triggered deployment and production health without changing it. Route to `deployment-observation`.

## Required Inputs

- Release identity, reviewed deployment target, frozen parameters, provider or hook adapter, credentials, and current authorization.

## Procedure

1. If the platform deploys automatically on merge, return not-applicable and hand off to deployment-observation; otherwise continue.
2. Verify exact workflow or hook, provider, repository or project, environment, artifact digest, config version, parameters, identity, budget, blast radius, timeout, cancellation, rollback owner, idempotency, and fresh per-action authorization.
3. Preview or dry-run the exact request where supported and record expected effects without exposing secrets.
4. Perform one bounded trigger; do not merge, alter config, select a different artifact, promote, observe, or rollback.
5. Record durable trigger receipt, run identity, request hash, status-at-return, duration, partial failure, retry prohibition or bounded retry, and cancellation path.

## Domain Guidance

- First check whether the configured platform deploys automatically on merge (for example Vercel or Netlify). If so no trigger exists: return not-applicable and hand off to deployment-observation.
- Bind the run receipt to the exact head or merge commit SHA and prefer the workflow whose name matches the configured deploy workflow when several match.

## Output Contract

Produce:
- deployment trigger receipt
- immutable request and artifact identity
- run or hook identity
- failure, cancellation, and handoff record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `merge-and-deploy-readiness`
- `deployment-observation`
- `release-rollback-execution`
- `web-hosting-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
