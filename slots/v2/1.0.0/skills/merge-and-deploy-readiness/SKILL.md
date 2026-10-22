---
name: merge-and-deploy-readiness
description: Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy. Do not use for merge the identified pull request after a passing fresh gate or trigger the approved deployment after merge and deployment authorization.
---

# Merge And Deploy Readiness

## Responsibility

Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy.

## Trigger

Use when the requested outcome is: Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy.

Do not use when:
- Merge the identified pull request after a passing fresh gate. Route to `remote-pull-request-merge`.
- Trigger the approved deployment after merge and deployment authorization. Route to `deployment-trigger-execution`.

## Required Inputs

- A pull request, target branch, CI state, version state, and deployment configuration.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze repository and PR identity, base and head refs, commit SHA, required checks and reviews, merge policy, release artifact, environment, deployment preview, observability, rollback, and authorization owners.
2. Read current remote and local evidence for open state, approvals, checks, conflicts, base drift, version or changelog, secret scan, artifact digest, deployment dry run, health gates, and rollback readiness.
3. Reject stale, mismatched, superseded, partial, self-attested, or waived evidence without named authority.
4. Return merge-ready, deploy-ready, needs-input, or blocked separately with exact missing conditions; perform no merge, deploy, push, comment, or configuration write.

## Output Contract

Produce:
- merge readiness result
- deployment readiness result
- fresh PR and artifact evidence
- blocker, authorization, and rollback register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `fresh-readiness`
- `exact-PR`
- `base-head`
- `checks-reviews`
- `artifact-digest`
- `separate-merge-deploy`
- `no-mutation`

## Hard Gates

- Readiness cannot mutate remote state and must issue separate merge and deploy verdicts; a passing merge gate neither performs nor authorizes deployment.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `remote-pull-request-merge`
- `deployment-trigger-execution`
- `change-delivery-preflight`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
