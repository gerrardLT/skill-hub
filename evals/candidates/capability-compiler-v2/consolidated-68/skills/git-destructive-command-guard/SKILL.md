---
name: git-destructive-command-guard
description: "Consolidated capability with 2 selectable modes: git-destructive-command-guard; local-git-guard-setup. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [git-destructive-command-guard, local-git-guard-setup]
---

# Git Destructive Command Guard

## Responsibility

Consolidated capability covering 2 related modes: Author and validate a repository-scoped guard policy that intercepts declared destructive Git command patterns before execution without installing it silently.; Install or configure one approved repository-local Git guard after classifying the hooks path, with consent, verification, backup, and uninstall instructions.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `git-destructive-command-guard` | `workspace-write-local-exec` | A repository needs a guard that blocks destructive Git commands before an agent or developer runs them; Someone asks for the block and allow rules, test fixtures and hook wiring for dangerous commands | Install the already-approved guard into the repository's local Git configuration (-> local-git-guard-setup); Integrate t |
| `local-git-guard-setup` | `local-system-write-authorized-only` | An approved Git guard script must be installed into one repository's local hooks after checking who owns the hooks path; Someone asks whether a guard can be enabled without disturbing committed or sha | Author or change the guard policy and fixtures in project source (-> git-destructive-command-guard); Integrate a base br |

## Mode: `git-destructive-command-guard`

### git-destructive-command-guard

#### Responsibility

Author and validate a repository-scoped guard policy that intercepts declared destructive Git command patterns before execution without installing it silently.

#### Trigger

Use when the request matches any of:
- A repository needs a guard that blocks destructive Git commands before an agent or developer runs them
- Someone asks for the block and allow rules, test fixtures and hook wiring for dangerous commands

Do not use when:
- Install the already-approved guard into the repository's local Git configuration. Route to `local-git-guard-setup`.
- Integrate the approved base branch into the isolated local change branch. Route to `local-branch-integration`.
- Restrict edits to one directory or a frozen set of paths. Route to `change-scope-freeze`.

#### Required Inputs

- A command hook environment, dangerous-command policy, and local configuration.

#### Procedure

1. Freeze the dangerous-command policy, shell or hook environment, repository artifact boundary, bypass rules, user-confirmation behavior, and installation owner.
2. Represent exact and equivalent destructive forms without intercepting ordinary status, diff, add, commit, fetch, or safe restore use.
3. Write only the authorized guard source, configuration template, and deterministic allow/block fixtures in the workspace.
4. Run approved fixture checks and return the candidate guard; require a separate local-system setup capability for installation or enablement.

#### Domain Guidance

- Default destructive-pattern table: push --force and -f and refspecs starting with +, push --delete and :branch, reset --hard, clean -f and -fd, checkout -- . and restore of uncommitted paths, branch -D, stash drop and clear, reflog expire, filter-branch. Include equivalent forms and chained or quoted commands.
- Near-miss pairs must pass: --force-with-lease when explicitly allowed, reset --soft, clean -n, branch -d, stash push.
- Parse commands with a real tokenizer (for example shlex), split chained commands at &&, ||, ; and |, and never match by substring alone.
- Evaluate every flag and refspec independently. --force-with-lease does not cancel --force or a leading +refspec. Unknown Git global options, malformed syntax and ambiguous shell constructs must fail closed; a main-branch exception or environment override cannot silently bypass the guard.

#### Output Contract

Produce:
- guard policy source
- allow and block fixture corpus
- local validation evidence
- separate installation handoff
- default destructive-pattern table with near-miss pass cases

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `destructive-patterns`
- `safe-command-pass`
- `repository-artifact`
- `no-silent-install`
- `separate-local-setup`

#### Hard Gates

- Guard authoring may create tested repository artifacts but cannot modify Git config, hook paths, aliases, shell startup, or enable interception without separate local-system authorization.
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
- `local-git-guard-setup`
- `local-branch-integration`
- `change-scope-freeze`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `local-git-guard-setup`

### local-git-guard-setup

#### Responsibility

Install or configure one approved repository-local Git guard after classifying the hooks path, with consent, verification, backup, and uninstall instructions.

#### Trigger

Use when the request matches any of:
- An approved Git guard script must be installed into one repository's local hooks after checking who owns the hooks path
- Someone asks whether a guard can be enabled without disturbing committed or shared hooks

Do not use when:
- Author or change the guard policy and fixtures in project source. Route to `git-destructive-command-guard`.
- Integrate a base branch into a local change branch. Route to `local-branch-integration`.

#### Required Inputs

- Repository Git-dir evidence, hooks-path classification, guard artifact, user consent, and local-system write authorization.

#### Procedure

1. Verify repository Git-dir, current hooksPath and ownership, tracked or committed status, existing hooks, approved guard artifact hash, consent, local-system authority, backup, and uninstall plan.
2. Refuse committed, shared, custom, managed, or ambiguous hook paths unless an exact non-destructive plan is separately approved.
3. Back up affected local config or hook state, install only the approved artifact, and do not rename or overwrite unrelated hooks silently.
4. Verify safe and blocked fixtures in the installed path and record config, hash, exit, backup, restore, uninstall, or safe refusal.

#### Domain Guidance

- Install only the approved hook file at the classified hooks path and, when a backup is needed, back up only the single file it replaces. Create no extra directories or files beyond what the plan lists.
- In the receipt, quote the consent text verbatim and state explicitly what was and was not changed.
- Committed hook files such as .husky are outside local-only installation authority. Do not propose committing, modifying or silently enabling them as part of this capability. Name the actual consenting owner and route any source change separately.

#### Output Contract

Produce:
- local guard installation receipt or refusal
- hooks-path classification
- installed verification evidence
- backup, restore, and uninstall instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `hooks-path-classification`
- `explicit-consent`
- `no-committed-hook-change`
- `backup`
- `verification`
- `uninstall`

#### Hard Gates

- Never silently enable a guard or modify a committed, shared, custom, or ambiguous hooks directory; explicit consent, backup, verification, and uninstall are mandatory.
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
- `git-destructive-command-guard`
- `local-branch-integration`
- `tool-runtime-readiness`
- `workflow-runtime-upgrade`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
