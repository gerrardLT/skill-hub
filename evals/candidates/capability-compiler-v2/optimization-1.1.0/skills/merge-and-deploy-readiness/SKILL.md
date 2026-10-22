---
name: merge-and-deploy-readiness
description: "Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy. Use when A pull request is about to be merged or deployed and someone needs a fresh go or no-go from current evidence; Someone asks whether merge and deployment can proceed separately, and what exactly is still missing. Do not use for: Merge the identified pull request after a passing fresh gate (-> remote-pull-request-merge); Trigger the approved deployment after merge and deployment authorization (-> deployment-trigger-execution)."
---

# Merge And Deploy Readiness

## Responsibility

Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy.

## Trigger

Use when the request matches any of:
- A pull request is about to be merged or deployed and someone needs a fresh go or no-go from current evidence
- Someone asks whether merge and deployment can proceed separately, and what exactly is still missing

Do not use when:
- Merge the identified pull request after a passing fresh gate. Route to `remote-pull-request-merge`.
- Trigger the approved deployment after merge and deployment authorization. Route to `deployment-trigger-execution`.

## Required Inputs

- A pull request, target branch, CI state, version state, and deployment configuration.

## Procedure

1. Freeze repository and PR identity, base and head refs, commit SHA, required checks and reviews, merge policy, release artifact, environment, deployment preview, observability, rollback, and authorization owners.
2. Separate required gates (from policy, task or deploy configuration) from advisory checks; only required gates can block.
3. Read current remote and local evidence for open state, approvals, checks, conflicts, base drift, version or changelog, secret scan, artifact digest, deployment dry run, health gates, and rollback readiness.
4. Reject stale, mismatched, superseded, partial, self-attested, or waived evidence without named authority.
5. Return merge-ready, deploy-ready, needs-input, or blocked separately with exact missing conditions; perform no merge, deploy, push, comment, or configuration write.

## Domain Guidance

- Judge only against the gates the repository policy, the task or the deploy configuration actually require. List any extra check you consider worthwhile as advisory and never let it turn a GO into a NO-GO.
- Give the merge verdict and the deploy verdict separately. When the supplied evidence satisfies every required gate the verdict is GO, stated with the evidence that supports it.
- A first run, or a changed deploy configuration since the last confirmed run, requires a dry-run verdict before deploy readiness can pass.

## Output Contract

Produce:
- merge readiness result
- deployment readiness result
- fresh PR and artifact evidence
- blocker, authorization, and rollback register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `remote-pull-request-merge`
- `deployment-trigger-execution`
- `change-delivery-preflight`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
