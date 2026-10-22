---
name: change-packaging-and-versioning
description: "Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes. Use when Verified local changes must be grouped into clean commits with a version bump and changelog before anything is pushed; A release needs PR text and release notes drafted from evidence, with secrets redacted. Do not use for: Check whether the unpackaged branch is ready for delivery first (-> change-delivery-preflight); Push the completed package to the approved remote ref (-> remote-git-push)."
---

# Change Packaging And Versioning

## Responsibility

Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes.

## Trigger

Use when the request matches any of:
- Verified local changes must be grouped into clean commits with a version bump and changelog before anything is pushed
- A release needs PR text and release notes drafted from evidence, with secrets redacted

Do not use when:
- Check whether the unpackaged branch is ready for delivery first. Route to `change-delivery-preflight`.
- Push the completed package to the approved remote ref. Route to `remote-git-push`.

## Required Inputs

- Implemented and reviewed changes with fresh verification evidence.

## Procedure

1. Classify version state against the base and decide the semver level from observable behavior change; state the alternative level when the choice is debatable.
2. Verify preflight result, frozen diff, local branch, commit policy, version scheme, changelog authority, release scope, evidence, and secret or credential exclusions.
3. Group changes into the smallest coherent bisectable local commits without rewriting unrelated history or fabricating test claims.
4. Update only authorized local version, changelog, and release or PR metadata with evidence-linked content and redaction.
5. Run approved local packaging checks and return commit IDs, version, changed files, metadata hashes, and exact push handoff; no remote action.

## Domain Guidance

- Classify version state against the base before any write: fresh (bump needed), already bumped (keep), or inconsistent across version files (repair and report). Never double-bump on a second run.
- Pick the semver level from behavior: any observable change to an existing output, rounding or default is potentially breaking. State the level you chose, the alternative level, and the reason, and ask the owner to confirm when the two differ.
- If the branch holds only WIP commits, soft-reset to the merge base before packaging; never discard non-WIP commits and stop to ask when unsure.

## Output Contract

Produce:
- bisectable local commits
- version and changelog updates
- redacted PR and release metadata
- local packaging evidence and push handoff
- semver decision with chosen level, alternative level and reason

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `local-only`
- `bisectable-commits`
- `version`
- `changelog`
- `redaction`
- `no-push`

## Hard Gates

- Packaging is local only: it may create approved commits and metadata but cannot push, create or update a PR, merge, tag remotely, deploy, or claim remote delivery.
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
- `change-delivery-preflight`
- `remote-git-push`
- `remote-pull-request-change`
- `release-documentation-maintenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
