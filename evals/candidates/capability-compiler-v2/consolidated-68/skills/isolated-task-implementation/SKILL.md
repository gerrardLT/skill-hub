---
name: isolated-task-implementation
description: "Consolidated capability with 4 selectable modes: developer-experience-assessment; facilitation-and-collaboration-protocols; isolated-task-implementation; workflow-skill-authoring. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [developer-experience-assessment, facilitation-and-collaboration-protocols, isolated-task-implementation, workflow-skill-authoring]
---

# Isolated Task Implementation

## Responsibility

Consolidated capability covering 4 related modes: Execute an authorized developer journey and measure time-to-first-success, setup, errors, documentation, compatibility, and recovery without changing product source.; Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.; Implement one frozen task in one isolated authorized workspace with a single writer, bounded checks, and a reviewable handoff.; Author and locally validate one atomic workflow Skill from an approved capability contract, provenance, fixtures, trigger policy, and package boundary.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `developer-experience-assessment` | `local-exec` | A repository or developer product must be used end to end by a new contributor persona, timing each step; Someone asks how long first success takes and where setup, docs or errors slow a developer dow | Review the proposed developer-experience plan before implementation (-> developer-experience-plan-review); Fix the docum |
| `facilitation-and-collaboration-protocols` | `workspace-write` | A group needs a structured session to surface evidence, disagreement and decisions, and someone must design how it runs; An AI-led or AI-assisted workshop needs turn-taking rules, pacing and a decisio | Make the disputed product decision for the group (-> plan-review-decision-synthesis); Interview customers one-on-one abo |
| `isolated-task-implementation` | `workspace-write-local-exec` | One fully specified task must be implemented in an isolated workspace with a single writer and a reviewable handoff; A work slice is ready to code and tests must run through the host before review. | Execute and track a multi-step implementation plan with checkpoints and invalidation (-> plan-execution-control); Repair |
| `workflow-skill-authoring` | `workspace-write-local-exec` | A capability contract and its evidence must be turned into one atomic Skill package with trigger fixtures; Someone asks for a candidate Skill with provenance and tests, staged but not released. | Assemble several released Skills into a conditional lifecycle Recipe (-> workflow-orchestration-and-lifecycle); Push the |

## Mode: `developer-experience-assessment`

### developer-experience-assessment

#### Responsibility

Execute an authorized developer journey and measure time-to-first-success, setup, errors, documentation, compatibility, and recovery without changing product source.

#### Trigger

Use when the request matches any of:
- A repository or developer product must be used end to end by a new contributor persona, timing each step
- Someone asks how long first success takes and where setup, docs or errors slow a developer down

Do not use when:
- Review the proposed developer-experience plan before implementation. Route to `developer-experience-plan-review`.
- Fix the documentation, scripts, or tooling exposed by the assessment. Route to `defect-remediation`.

#### Required Inputs

- Repository, runnable setup path, common tasks, errors, timings, and contributor context.

#### Procedure

1. Freeze persona, journey, clean environment, source identity, supported platform, documented commands, credentials boundary, success criterion, and time budget.
2. Run only approved local commands and record elapsed time, decisions, errors, retries, workarounds, outputs, and cleanup.
3. Compare actual behavior with documentation, compatibility promises, error messages, discoverability, and recovery expectations.
4. Return reproducible friction and success evidence with severity and bounded recommendations; do not repair source.

#### Domain Guidance

- Include documentation navigation and the copy-paste of each documented snippet in the journey: a command that is documented but fails when pasted is a finding with the exact snippet and error.

#### Output Contract

Produce:
- developer journey trace
- time-to-first-success evidence
- friction and recovery findings
- bounded DX recommendations

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `real-journey`
- `time-to-first-success`
- `environment`
- `commands`
- `errors`
- `recovery`
- `cleanup`

#### Hard Gates

- Developer experience claims require a real target-bound journey with recorded environment, commands, elapsed time, errors, recovery, and cleanup; reading docs alone is insufficient.
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
- `developer-experience-plan-review`
- `defect-remediation`
- `tool-runtime-readiness`
- `documentation-authoring`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `facilitation-and-collaboration-protocols`

### facilitation-and-collaboration-protocols

#### Responsibility

Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.

#### Trigger

Use when the request matches any of:
- A group needs a structured session to surface evidence, disagreement and decisions, and someone must design how it runs
- An AI-led or AI-assisted workshop needs turn-taking rules, pacing and a decision log

Do not use when:
- Make the disputed product decision for the group. Route to `plan-review-decision-synthesis`.
- Interview customers one-on-one about past behavior. Route to `customer-interview-execution`.

#### Required Inputs

- A multi-role task, incomplete context, stakeholder set, and decision boundary.

#### Procedure

1. Define the session question, participants, roles, authority, pre-reads, and data boundary.
2. Select activities that elicit independent evidence before convergence.
3. Timebox divergence, synthesis, decision, dissent, and follow-up.
4. Record decision owner, rationale, objections, unknowns, and expiry conditions.
5. Produce actions and unresolved items without fabricating consensus.

#### Domain Guidance

- Default protocol for AI-facilitated sessions: open with a heads-up and an entry mode (guided, context dump, best guess); ask one question per turn in plain language; show progress labels such as Context 3/8; handle interruptions with pause and resume; offer numbered recommendations at decision points.
- Collect independent input before convergence, then timebox divergence, synthesis and decision; record dissent and the named decision owner.

#### Output Contract

Produce:
- facilitation plan
- role and authority map
- decision log template
- follow-up register
- session script with entry mode, question sequence and progress labels

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- A facilitator may structure and record the decision but must not manufacture consensus or decide for the named owner.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `customer-interview-execution`
- `plan-review-decision-synthesis`
- `document-and-artifact-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `isolated-task-implementation`

### isolated-task-implementation

#### Responsibility

Implement one frozen task in one isolated authorized workspace with a single writer, bounded checks, and a reviewable handoff.

#### Trigger

Use when the request matches any of:
- One fully specified task must be implemented in an isolated workspace with a single writer and a reviewable handoff
- A work slice is ready to code and tests must run through the host before review

Do not use when:
- Execute and track a multi-step implementation plan with checkpoints and invalidation. Route to `plan-execution-control`.
- Repair an independently confirmed defect after root-cause evidence exists. Route to `defect-remediation`.

#### Required Inputs

- One approved task, complete task-local context, isolated workspace, edit scope, test command, and escalation boundary.

#### Procedure

1. Verify frozen scope, clean isolated workspace, base identity, single-writer ownership, required inputs, acceptance criteria, tests, and prohibited paths.
2. Read the full affected flow and existing patterns before writing; reuse current helpers and keep the smallest coherent diff.
3. Implement only the assigned slice and its required tests or fixtures; stop on ambiguity, scope expansion, dependency conflict, or concurrent mutation.
4. Run approved focused checks through the host and return patch, changed files, evidence, assumptions, and handoff state without integration or remote actions.

#### Domain Guidance

- Escalate instead of guessing when: the task needs an architectural decision with several valid approaches, understanding code beyond what was provided, uncertainty about whether the approach is correct, or restructuring code the plan did not anticipate. Stopping with a clear question is correct; bad work is worse than no work.

#### Output Contract

Produce:
- isolated implementation patch
- changed-file and scope evidence
- focused verification records
- review and integration handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `isolated-workspace`
- `single-writer`
- `frozen-task`
- `minimal-diff`
- `host-checks`
- `no-integration`

#### Hard Gates

- One task has one writer and one isolated workspace; missing isolation, dirty-state ambiguity, concurrent ownership, or scope expansion blocks implementation.
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
- `change-scope-freeze`
- `plan-execution-control`
- `defect-remediation`
- `local-branch-integration`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `workflow-skill-authoring`

### workflow-skill-authoring

#### Responsibility

Author and locally validate one atomic workflow Skill from an approved capability contract, provenance, fixtures, trigger policy, and package boundary.

#### Trigger

Use when the request matches any of:
- A capability contract and its evidence must be turned into one atomic Skill package with trigger fixtures
- Someone asks for a candidate Skill with provenance and tests, staged but not released

Do not use when:
- Assemble several released Skills into a conditional lifecycle Recipe. Route to `workflow-orchestration-and-lifecycle`.
- Push the already packaged Skill branch to its approved remote ref. Route to `remote-git-push`.

#### Required Inputs

- Capability contract, source evidence, runtime target, fixtures, tests, and package boundary.

#### Procedure

1. Freeze capability responsibility, non-responsibilities, source evidence, runtime target, permission identity, package path, fixtures, trigger and anti-trigger cases, and release boundary.
2. Read the canonical runtime SDK or schema and reuse existing package conventions before writing the smallest atomic Skill and support files.
3. Preserve exact provenance and authority, add deterministic schema and fixture checks, and test trigger boundaries and failure states through approved local commands.
4. Stage only the candidate package, report hashes and evidence, and require separate evaluation, human approval, and publication; do not commit or release.

#### Domain Guidance

- Naming: lowercase letters, digits and single dashes, at most 32 characters, starting with a letter, no consecutive dashes. Provide 3 to 5 trigger phrases and at least as many near-miss non-trigger cases.

#### Output Contract

Produce:
- atomic workflow Skill candidate
- trigger and anti-trigger fixtures
- provenance and permission contract
- local validation and packaging evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `atomic-responsibility`
- `provenance`
- `trigger-anti-trigger`
- `permission-identity`
- `fixture-test`
- `candidate-not-release`

#### Hard Gates

- A candidate Skill must have one atomic responsibility, exact provenance, tested trigger boundaries, least authority, and no release claim; multi-stage orchestration belongs to a Recipe.
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
- `workflow-orchestration-and-lifecycle`
- `artifact-persistence-and-tool-actions`
- `tool-runtime-readiness`
- `remote-git-push`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
