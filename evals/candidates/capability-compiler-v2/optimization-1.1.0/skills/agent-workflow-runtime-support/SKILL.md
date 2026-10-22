---
name: agent-workflow-runtime-support
description: "Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps. Use when A workflow run needs its session identity, consent state, checkpoints and host-tool availability set up once before domain steps start; Someone asks whether cross-project learnings may be used in this session and where runtime state is stored. Do not use for: Compose the domain capabilities and conditional edges for the workflow (-> workflow-orchestration-and-lifecycle); Execute the selected atomic implementation task (-> isolated-task-implementation); Track step states, dependencies, checkpoints and invalidation of an approved plan (-> plan-execution-control)."
---

# Agent Workflow Runtime Support

## Responsibility

Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps.

## Trigger

Use when the request matches any of:
- A workflow run needs its session identity, consent state, checkpoints and host-tool availability set up once before domain steps start
- Someone asks whether cross-project learnings may be used in this session and where runtime state is stored

Do not use when:
- Compose the domain capabilities and conditional edges for the workflow. Route to `workflow-orchestration-and-lifecycle`.
- Execute the selected atomic implementation task. Route to `isolated-task-implementation`.
- Track step states, dependencies, checkpoints and invalidation of an approved plan. Route to `plan-execution-control`.

## Required Inputs

- Session identity, host capabilities, local project, consent state, and runtime configuration.

## Procedure

1. Freeze workflow and session identity, host capabilities, project path, consent, privacy, runtime configuration, artifact store, and checkpoint policy.
2. Initialize or load bounded state and verify source and artifact identities without inventing domain completion.
3. Expose only approved host-tool directives, artifact pointers, checkpoints, pause or resume state, and degradation notices.
4. Record runtime commands, exits, versions, duration, state hash, cleanup, and invalidation; route domain work to its owner.

## Domain Guidance

- Cross-project learning consent has three states: unset, false, true, with project-only as the default. Record the state only when the task or owner addresses it; otherwise write 'not addressed' and stay project-only. Do not invent a consent entry, an owner name or a skill name that the task did not give.
- Step state, dependencies and invalidation belong to plan-execution-control; this Skill owns host and session mechanics only.
- A date without a labelled meaning is not an expiry. Preserve its exact supplied label and mark unspecified consent validity unknown; checkpoint artifact pointers include step identity, path and content hash without inventing them.
- If learning or consent scope is not explicitly supplied, record it as unknown/not addressed. Do not convert a default into a claimed policy, consent state, owner decision or cross-project restriction.

## Output Contract

Produce:
- workflow runtime state
- consent and capability record
- checkpoint and artifact pointers
- degradation and cleanup notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `plan-execution-control`
- `artifact-persistence-and-tool-actions`
- `tool-runtime-readiness`
- `isolated-task-implementation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
