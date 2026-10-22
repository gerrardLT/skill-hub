---
name: release-packaging-and-preflight
description: "Consolidated capability with 3 selectable modes: change-delivery-preflight; change-packaging-and-versioning; merge-and-deploy-readiness. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [change-delivery-preflight, change-packaging-and-versioning, merge-and-deploy-readiness]
---

# Release Packaging And Preflight

## Responsibility

Consolidated capability covering 3 related modes: Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation.; Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes.; Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `change-delivery-preflight` | `local-exec-external-read` | A verified local change is about to be pushed and someone must check branch, refs, credentials and automation stops first; Someone asks whether a branch is clean, current with its base and safe to han | Package the verified local changes into commits, version, changelog, and PR metadata (-> change-packaging-and-versioning |
| `change-packaging-and-versioning` | `workspace-write-local-exec` | Verified local changes must be grouped into clean commits with a version bump and changelog before anything is pushed; A release needs PR text and release notes drafted from evidence, with secrets red | Check whether the unpackaged branch is ready for delivery first (-> change-delivery-preflight); Push the completed packa |
| `merge-and-deploy-readiness` | `local-exec-external-read` | A pull request is about to be merged or deployed and someone needs a fresh go or no-go from current evidence; Someone asks whether merge and deployment can proceed separately, and what exactly is stil | Merge the identified pull request after a passing fresh gate (-> remote-pull-request-merge); Trigger the approved deploy |

## Mode: `change-delivery-preflight`

### change-delivery-preflight

#### Responsibility

Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation.

#### Trigger

Use when the request matches any of:
- A verified local change is about to be pushed and someone must check branch, refs, credentials and automation stops first
- Someone asks whether a branch is clean, current with its base and safe to hand to the push step

Do not use when:
- Package the verified local changes into commits, version, changelog, and PR metadata. Route to `change-packaging-and-versioning`.
- Push the already-packaged branch to its exact remote ref. Route to `remote-git-push`.

#### Required Inputs

- A reviewed change, repository state, delivery policy, and intended publication boundary.

#### Procedure

1. Freeze repository, branch, base and head refs, expected remote, delivery policy, required checks, documentation, credential metadata boundary, and prohibited actions.
2. Inspect local state and approved read-only remote metadata for divergence, stale base, uncommitted files, forbidden files, secret indicators, version or changelog gaps, and automation stops.
3. Validate current test and completion evidence without rerunning source mutation or trusting stale status.
4. Return ready or blocked with exact findings and required next owner; do not commit, push, create PRs, merge, deploy, or alter provider state.

#### Domain Guidance

- Check that the credential-redaction pre-push hook is installed, including when core.hooksPath points to a custom or committed hooks directory; report the hooks path and who owns it.
- Check whether other active branches or worktrees already claim the same version slot, and report the collision as advisory information for the packaging step.

#### Output Contract

Produce:
- delivery preflight report
- branch and ref evidence
- credential and automation-stop status
- blocker and next-owner register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `branch-ref-identity`
- `merge-base`
- `clean-state`
- `credential-status`
- `automation-stops`
- `no-remote-mutation`

#### Hard Gates

- Preflight is read-only: readiness never authorizes packaging, push, pull-request change, merge, deployment, or provider mutation.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `change-packaging-and-versioning`
- `remote-git-push`
- `remote-pull-request-change`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `change-packaging-and-versioning`

### change-packaging-and-versioning

#### Responsibility

Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes.

#### Trigger

Use when the request matches any of:
- Verified local changes must be grouped into clean commits with a version bump and changelog before anything is pushed
- A release needs PR text and release notes drafted from evidence, with secrets redacted

Do not use when:
- Check whether the unpackaged branch is ready for delivery first. Route to `change-delivery-preflight`.
- Push the completed package to the approved remote ref. Route to `remote-git-push`.

#### Required Inputs

- Implemented and reviewed changes with fresh verification evidence.

#### Procedure

1. Classify version state against the base and decide the semver level from observable behavior change; state the alternative level when the choice is debatable.
2. Verify preflight result, frozen diff, local branch, commit policy, version scheme, changelog authority, release scope, evidence, and secret or credential exclusions.
3. Group changes into the smallest coherent bisectable local commits without rewriting unrelated history or fabricating test claims.
4. Update only authorized local version, changelog, and release or PR metadata with evidence-linked content and redaction.
5. Run approved local packaging checks and return commit IDs, version, changed files, metadata hashes, and exact push handoff; no remote action.

#### Domain Guidance

- Classify version state against the base before any write: fresh (bump needed), already bumped (keep), or inconsistent across version files (repair and report). Never double-bump on a second run.
- Pick the semver level from behavior: any observable change to an existing output, rounding or default is potentially breaking. State the level you chose, the alternative level, and the reason, and ask the owner to confirm when the two differ.
- If the branch holds only WIP commits, soft-reset to the merge base before packaging; never discard non-WIP commits and stop to ask when unsure.

#### Output Contract

Produce:
- bisectable local commits
- version and changelog updates
- redacted PR and release metadata
- local packaging evidence and push handoff
- semver decision with chosen level, alternative level and reason

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `local-only`
- `bisectable-commits`
- `version`
- `changelog`
- `redaction`
- `no-push`

#### Hard Gates

- Packaging is local only: it may create approved commits and metadata but cannot push, create or update a PR, merge, tag remotely, deploy, or claim remote delivery.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `change-delivery-preflight`
- `remote-git-push`
- `remote-pull-request-change`
- `release-documentation-maintenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `merge-and-deploy-readiness`

### merge-and-deploy-readiness

#### Responsibility

Perform a fresh read-only gate over branch, pull request, conflicts, CI, reviews, version drift, deployment preview, rollback, and authorization before merge or deploy.

#### Trigger

Use when the request matches any of:
- A pull request is about to be merged or deployed and someone needs a fresh go or no-go from current evidence
- Someone asks whether merge and deployment can proceed separately, and what exactly is still missing

Do not use when:
- Merge the identified pull request after a passing fresh gate. Route to `remote-pull-request-merge`.
- Trigger the approved deployment after merge and deployment authorization. Route to `deployment-trigger-execution`.

#### Required Inputs

- A pull request, target branch, CI state, version state, and deployment configuration.

#### Procedure

1. Freeze repository and PR identity, base and head refs, commit SHA, required checks and reviews, merge policy, release artifact, environment, deployment preview, observability, rollback, and authorization owners.
2. Separate required gates (from policy, task or deploy configuration) from advisory checks; only required gates can block.
3. Read current remote and local evidence for open state, approvals, checks, conflicts, base drift, version or changelog, secret scan, artifact digest, deployment dry run, health gates, and rollback readiness.
4. Reject stale, mismatched, superseded, partial, self-attested, or waived evidence without named authority.
5. Return merge-ready, deploy-ready, needs-input, or blocked separately with exact missing conditions; perform no merge, deploy, push, comment, or configuration write.

#### Domain Guidance

- Judge only against the gates the repository policy, the task or the deploy configuration actually require. List any extra check you consider worthwhile as advisory and never let it turn a GO into a NO-GO.
- Give the merge verdict and the deploy verdict separately. When the supplied evidence satisfies every required gate the verdict is GO, stated with the evidence that supports it.
- A first run, or a changed deploy configuration since the last confirmed run, requires a dry-run verdict before deploy readiness can pass.

#### Output Contract

Produce:
- merge readiness result
- deployment readiness result
- fresh PR and artifact evidence
- blocker, authorization, and rollback register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `fresh-readiness`
- `exact-PR`
- `base-head`
- `checks-reviews`
- `artifact-digest`
- `separate-merge-deploy`
- `no-mutation`

#### Hard Gates

- Readiness cannot mutate remote state and must issue separate merge and deploy verdicts; a passing merge gate neither performs nor authorizes deployment.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `remote-pull-request-merge`
- `deployment-trigger-execution`
- `change-delivery-preflight`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
