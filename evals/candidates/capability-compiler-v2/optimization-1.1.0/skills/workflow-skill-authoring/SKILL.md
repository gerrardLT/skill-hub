---
name: workflow-skill-authoring
description: "Author and locally validate one atomic workflow Skill from an approved capability contract, provenance, fixtures, trigger policy, and package boundary. Use when A capability contract and its evidence must be turned into one atomic Skill package with trigger fixtures; Someone asks for a candidate Skill with provenance and tests, staged but not released. Do not use for: Assemble several released Skills into a conditional lifecycle Recipe (-> workflow-orchestration-and-lifecycle); Push the already packaged Skill branch to its approved remote ref (-> remote-git-push)."
---

# Workflow Skill Authoring

## Responsibility

Author and locally validate one atomic workflow Skill from an approved capability contract, provenance, fixtures, trigger policy, and package boundary.

## Trigger

Use when the request matches any of:
- A capability contract and its evidence must be turned into one atomic Skill package with trigger fixtures
- Someone asks for a candidate Skill with provenance and tests, staged but not released

Do not use when:
- Assemble several released Skills into a conditional lifecycle Recipe. Route to `workflow-orchestration-and-lifecycle`.
- Push the already packaged Skill branch to its approved remote ref. Route to `remote-git-push`.

## Required Inputs

- Capability contract, source evidence, runtime target, fixtures, tests, and package boundary.

## Procedure

1. Freeze capability responsibility, non-responsibilities, source evidence, runtime target, permission identity, package path, fixtures, trigger and anti-trigger cases, and release boundary.
2. Read the canonical runtime SDK or schema and reuse existing package conventions before writing the smallest atomic Skill and support files.
3. Preserve exact provenance and authority, add deterministic schema and fixture checks, and test trigger boundaries and failure states through approved local commands.
4. Stage only the candidate package, report hashes and evidence, and require separate evaluation, human approval, and publication; do not commit or release.

## Domain Guidance

- Naming: lowercase letters, digits and single dashes, at most 32 characters, starting with a letter, no consecutive dashes. Provide 3 to 5 trigger phrases and at least as many near-miss non-trigger cases.

## Output Contract

Produce:
- atomic workflow Skill candidate
- trigger and anti-trigger fixtures
- provenance and permission contract
- local validation and packaging evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `atomic-responsibility`
- `provenance`
- `trigger-anti-trigger`
- `permission-identity`
- `fixture-test`
- `candidate-not-release`

## Hard Gates

- A candidate Skill must have one atomic responsibility, exact provenance, tested trigger boundaries, least authority, and no release claim; multi-stage orchestration belongs to a Recipe.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `workflow-orchestration-and-lifecycle`
- `artifact-persistence-and-tool-actions`
- `tool-runtime-readiness`
- `remote-git-push`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
