---
name: agent-workflow-runtime-support
description: Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps. Do not use for compose the domain capabilities and conditional edges for the workflow or execute the selected atomic implementation task.
---

# Agent Workflow Runtime Support

## Responsibility

Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps.

## Trigger

Use when the requested outcome is: Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps.

Do not use when:
- Compose the domain capabilities and conditional edges for the workflow. Route to `workflow-orchestration-and-lifecycle`.
- Execute the selected atomic implementation task. Route to `isolated-task-implementation`.

## Required Inputs

- Session identity, host capabilities, local project, consent state, and runtime configuration.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze workflow and session identity, host capabilities, project path, consent, privacy, runtime configuration, artifact store, and checkpoint policy.
2. Initialize or load bounded state and verify source and artifact identities without inventing domain completion.
3. Expose only approved host-tool directives, artifact pointers, checkpoints, pause or resume state, and degradation notices.
4. Record runtime commands, exits, versions, duration, state hash, cleanup, and invalidation; route domain work to its owner.

## Output Contract

Produce:
- workflow runtime state
- consent and capability record
- checkpoint and artifact pointers
- degradation and cleanup notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `session-identity`
- `consent`
- `host-capabilities`
- `checkpoint`
- `artifact-pointer`
- `degradation`
- `no-domain-work`

## Hard Gates

- Runtime support may manage session mechanics only; it cannot execute, approve, or mark any domain capability complete from orchestration state.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `workflow-orchestration-and-lifecycle`
- `plan-execution-control`
- `artifact-persistence-and-tool-actions`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
