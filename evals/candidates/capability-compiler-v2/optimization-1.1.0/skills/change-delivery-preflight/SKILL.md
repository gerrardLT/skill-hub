---
name: change-delivery-preflight
description: "Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation. Use when A verified local change is about to be pushed and someone must check branch, refs, credentials and automation stops first; Someone asks whether a branch is clean, current with its base and safe to hand to the push step. Do not use for: Package the verified local changes into commits, version, changelog, and PR metadata (-> change-packaging-and-versioning); Push the already-packaged branch to its exact remote ref (-> remote-git-push)."
---

# Change Delivery Preflight

## Responsibility

Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation.

## Trigger

Use when the request matches any of:
- A verified local change is about to be pushed and someone must check branch, refs, credentials and automation stops first
- Someone asks whether a branch is clean, current with its base and safe to hand to the push step

Do not use when:
- Package the verified local changes into commits, version, changelog, and PR metadata. Route to `change-packaging-and-versioning`.
- Push the already-packaged branch to its exact remote ref. Route to `remote-git-push`.

## Required Inputs

- A reviewed change, repository state, delivery policy, and intended publication boundary.

## Procedure

1. Freeze repository, branch, base and head refs, expected remote, delivery policy, required checks, documentation, credential metadata boundary, and prohibited actions.
2. Inspect local state and approved read-only remote metadata for divergence, stale base, uncommitted files, forbidden files, secret indicators, version or changelog gaps, and automation stops.
3. Validate current test and completion evidence without rerunning source mutation or trusting stale status.
4. Return ready or blocked with exact findings and required next owner; do not commit, push, create PRs, merge, deploy, or alter provider state.

## Domain Guidance

- Check that the credential-redaction pre-push hook is installed, including when core.hooksPath points to a custom or committed hooks directory; report the hooks path and who owns it.
- Check whether other active branches or worktrees already claim the same version slot, and report the collision as advisory information for the packaging step.

## Output Contract

Produce:
- delivery preflight report
- branch and ref evidence
- credential and automation-stop status
- blocker and next-owner register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `branch-ref-identity`
- `merge-base`
- `clean-state`
- `credential-status`
- `automation-stops`
- `no-remote-mutation`

## Hard Gates

- Preflight is read-only: readiness never authorizes packaging, push, pull-request change, merge, deployment, or provider mutation.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `change-packaging-and-versioning`
- `remote-git-push`
- `remote-pull-request-change`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
