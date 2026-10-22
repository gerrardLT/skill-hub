---
name: tool-and-runtime-bootstrap
description: "Consolidated capability with 9 selectable modes: agent-workflow-runtime-support; artifact-persistence-and-tool-actions; local-agent-memory-setup; mobile-platform-runtime-support; provider-cli-authentication-setup; test-runtime-bootstrap; tool-runtime-readiness; workflow-orchestration-and-lifecycle; workflow-runtime-upgrade. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [agent-workflow-runtime-support, artifact-persistence-and-tool-actions, local-agent-memory-setup, mobile-platform-runtime-support, provider-cli-authentication-setup, test-runtime-bootstrap, tool-runtime-readiness, workflow-orchestration-and-lifecycle, workflow-runtime-upgrade]
---

# Tool And Runtime Bootstrap

## Responsibility

Consolidated capability covering 9 related modes: Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps.; Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task.; Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls.; Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source.; Install or authenticate one exact provider CLI after explicit local-system, credential, and external-session authorization, preserving non-secret identity, expiry, revocation, and cleanup evidence.; Install and configure one approved project-local test runtime, prove it with one real-behavior test, and restore dependency files if setup fails.; Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it.; Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.; Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `agent-workflow-runtime-support` | `local-exec` | A workflow run needs its session identity, consent state, checkpoints and host-tool availability set up once before domain steps start; Someone asks whether cross-project learnings may be used in this | Compose the domain capabilities and conditional edges for the workflow (-> workflow-orchestration-and-lifecycle); Execut |
| `artifact-persistence-and-tool-actions` | `workspace-write-local-exec` | One validated artifact must be written to a declared workspace path with path containment and a recorded hash; Someone asks to save a result file without touching any other file or the product source. | Render and validate the document's layout, links, and accessibility before persistence (-> document-rendering-and-valida |
| `local-agent-memory-setup` | `local-system-write-authorized-only` | A local, project-isolated memory or index runtime must be created with privacy, retention and removal terms; Someone asks whether a memory store can be set up without any remote sync and how to remove | Save and search actual project context after the runtime exists (-> project-context-and-learning-store); Upgrade the ins |
| `mobile-platform-runtime-support` | `local-exec` | A mobile app must be built and run on an approved simulator or device and the result diagnosed; Someone asks why a mobile build or test target fails in the local toolchain. | Install or upgrade the mobile toolchain or SDK on the local system (-> workflow-runtime-upgrade); Change application sou |
| `provider-cli-authentication-setup` | `local-system-write-external-session-authorized-only` | One provider command-line tool must be installed or authenticated with scoped, expiring access; Someone asks what identity, scope and revocation path a provider CLI login would create. | Execute the reviewed provider experiment after authentication (-> llm-experiment-execution); Verify an existing browser- |
| `test-runtime-bootstrap` | `workspace-write-local-exec` | A project has no working test runtime and one approved framework must be installed with a proving test; Someone asks for the smallest change that lets a project run tests, with a restore path if setup | Design the overall test strategy before a framework is selected (-> testing-portfolio-strategy); Author advanced tests o |
| `tool-runtime-readiness` | `local-exec` | A required local tool must be confirmed present, at the right version and able to do what the task needs; Someone asks whether a tool on the path is actually usable before an owner starts work. | Install or upgrade the missing workflow runtime (-> workflow-runtime-upgrade); Bootstrap a project-local test framework  |
| `workflow-orchestration-and-lifecycle` | `workspace-write` | A request needs a workflow composed from several capabilities and no existing Recipe covers it; A multi-stage effort needs typed handoffs, gates and invalidation rules defined before execution. | Execute these implementation tasks in the workspace (-> plan-execution-control); Classify a single vague request and cho |
| `workflow-runtime-upgrade` | `local-system-write-authorized-only` | One installed workflow runtime must be upgraded to a pinned version with backup and rollback; Someone asks what an upgrade would change and how to verify the new version is actually the one running. | Verify whether the current runtime is already ready without changing it (-> tool-runtime-readiness); Install or authenti |

## Mode: `agent-workflow-runtime-support`

### agent-workflow-runtime-support

#### Responsibility

Provide bounded session, consent, checkpoint, artifact-pointer, degradation, and host-tool runtime state once for an approved workflow without performing domain steps.

#### Trigger

Use when the request matches any of:
- A workflow run needs its session identity, consent state, checkpoints and host-tool availability set up once before domain steps start
- Someone asks whether cross-project learnings may be used in this session and where runtime state is stored

Do not use when:
- Compose the domain capabilities and conditional edges for the workflow. Route to `workflow-orchestration-and-lifecycle`.
- Execute the selected atomic implementation task. Route to `isolated-task-implementation`.
- Track step states, dependencies, checkpoints and invalidation of an approved plan. Route to `plan-execution-control`.

#### Required Inputs

- Session identity, host capabilities, local project, consent state, and runtime configuration.

#### Procedure

1. Freeze workflow and session identity, host capabilities, project path, consent, privacy, runtime configuration, artifact store, and checkpoint policy.
2. Initialize or load bounded state and verify source and artifact identities without inventing domain completion.
3. Expose only approved host-tool directives, artifact pointers, checkpoints, pause or resume state, and degradation notices.
4. Record runtime commands, exits, versions, duration, state hash, cleanup, and invalidation; route domain work to its owner.

#### Domain Guidance

- Cross-project learning consent has three states: unset, false, true, with project-only as the default. Record the state only when the task or owner addresses it; otherwise write 'not addressed' and stay project-only. Do not invent a consent entry, an owner name or a skill name that the task did not give.
- Step state, dependencies and invalidation belong to plan-execution-control; this Skill owns host and session mechanics only.
- A date without a labelled meaning is not an expiry. Preserve its exact supplied label and mark unspecified consent validity unknown; checkpoint artifact pointers include step identity, path and content hash without inventing them.
- If learning or consent scope is not explicitly supplied, record it as unknown/not addressed. Do not convert a default into a claimed policy, consent state, owner decision or cross-project restriction.

#### Output Contract

Produce:
- workflow runtime state
- consent and capability record
- checkpoint and artifact pointers
- degradation and cleanup notice

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `session-identity`
- `consent`
- `host-capabilities`
- `checkpoint`
- `artifact-pointer`
- `degradation`
- `no-domain-work`

#### Hard Gates

- Runtime support may manage session mechanics only; it cannot execute, approve, or mark any domain capability complete from orchestration state.
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
- `plan-execution-control`
- `artifact-persistence-and-tool-actions`
- `tool-runtime-readiness`
- `isolated-task-implementation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `artifact-persistence-and-tool-actions`

### artifact-persistence-and-tool-actions

#### Responsibility

Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task.

#### Trigger

Use when the request matches any of:
- One validated artifact must be written to a declared workspace path with path containment and a recorded hash
- Someone asks to save a result file without touching any other file or the product source

Do not use when:
- Render and validate the document's layout, links, and accessibility before persistence. Route to `document-rendering-and-validation`.
- Publish this artifact to an external provider or repository. Route to `evaluation-dataset-publication`.
- Save a learning or context record into the local learning store. Route to `local-learning-persistence`.

#### Required Inputs

- A validated task, tool boundary, output location, and write authorization.

#### Procedure

1. Verify the validated input, exact tool or write action, destination class, overwrite policy, authorization, and expected artifact identity.
2. Refuse path escape, undeclared files, source mutation disguised as persistence, remote targets, or destructive replacement without recovery.
3. Perform only the bounded action; preserve source bytes or declared normalization and record before/after identity.
4. Return the saved artifact or explicit no-write outcome with path, tool, exit status when applicable, hash, and limitations.

#### Domain Guidance

- Order: write the file, compute its hash, then verify the written bytes against that hash. State a byte count or hash only when you computed it from the content given; otherwise leave an explicit placeholder.
- Never state an expected byte count or hash unless computed from the exact bytes. If not computed, leave a placeholder rather than estimating.

#### Output Contract

Produce:
- bounded tool-action record
- persisted lifecycle artifact or no-write outcome
- path and hash evidence
- overwrite or recovery record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `bounded-action`
- `declared-path`
- `path-containment`
- `artifact-hash`
- `no-extra-files`
- `recovery`

#### Hard Gates

- Persistence authority applies only to the declared artifact and location; it cannot authorize adjacent analysis, product-source edits, external publication, or additional files.
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
- `document-rendering-and-validation`
- `evaluation-dataset-publication`
- `completion-evidence-gate`
- `workflow-skill-authoring`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `local-agent-memory-setup`

### local-agent-memory-setup

#### Responsibility

Initialize one project-isolated local agent memory or indexing runtime under explicit privacy, retention, deletion, and rollback controls.

#### Trigger

Use when the request matches any of:
- A local, project-isolated memory or index runtime must be created with privacy, retention and removal terms
- Someone asks whether a memory store can be set up without any remote sync and how to remove it

Do not use when:
- Save and search actual project context after the runtime exists. Route to `project-context-and-learning-store`.
- Upgrade the installed workflow runtime version. Route to `workflow-runtime-upgrade`.
- Write one new learning or context record. Route to `local-learning-persistence`.

#### Required Inputs

- Project identity, runtime target, privacy choice, local-system write authorization, and retention policy.

#### Procedure

1. Verify project identity, runtime target and version, local-system authorization, paths, data classes, exclusions, privacy, encryption if required, retention, deletion, external sync policy, backup, and rollback.
2. Preview exact local files, directories, services, ports, or config keys and refuse shared or global stores unless explicitly approved.
3. Create only the bounded project-isolated runtime and health check without ingesting project content beyond the declared fixture.
4. Record non-sensitive config identity, health evidence, isolation, size, retention, removal, rollback, and failure cleanup.

#### Domain Guidance

- Remote or hosted memory backends, including ones that need an access token or a cloud database, are not covered. Return blocked for them and name the local-only alternative.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.

#### Output Contract

Produce:
- project-isolated memory runtime
- non-sensitive configuration receipt
- health and isolation evidence
- removal and rollback instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `project-isolation`
- `privacy`
- `retention`
- `deletion`
- `no-implicit-sync`
- `health-check`
- `rollback`

#### Hard Gates

- Local memory setup requires explicit project isolation, privacy, retention, deletion, and rollback; it cannot ingest arbitrary project data or enable external synchronization implicitly.
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

#### Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `project-context-and-learning-store`
- `workflow-runtime-upgrade`
- `tool-runtime-readiness`
- `secrets-and-environment-governance`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `mobile-platform-runtime-support`

### mobile-platform-runtime-support

#### Responsibility

Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source.

#### Trigger

Use when the request matches any of:
- A mobile app must be built and run on an approved simulator or device and the result diagnosed
- Someone asks why a mobile build or test target fails in the local toolchain

Do not use when:
- Install or upgrade the mobile toolchain or SDK on the local system. Route to `workflow-runtime-upgrade`.
- Change application source to fix the diagnosed mobile defect. Route to `defect-remediation`.

#### Required Inputs

- Mobile project, platform tools, simulator or device, local authority, and cleanup boundary.

#### Procedure

1. Freeze source identity, platform, toolchain, runtime, simulator or device, target, command, signing or credential boundary, and allowed local actions.
2. Verify readiness without exposing credentials or mutating global toolchains; run only the approved build or test target.
3. Record command, versions, device identity, exit, duration, logs, artifacts, cleanup, and environmental limitations.
4. Return run evidence or bounded diagnosis and handoff; do not install system components or edit source.

#### Domain Guidance

- Readiness checks before running: iOS, xcodebuild -showsdks and xcrun simctl list for the exact simulator; Android, adb devices and the SDK and build-tools versions. Record the before and after device list.
- Give a concrete check for each step (for example the expected build success line in the log, the artifact type and location) and state every assumption as an assumption; never invent a condition the task did not state.

#### Output Contract

Produce:
- mobile runtime readiness record
- build or test execution evidence
- device and toolchain manifest
- bounded diagnosis and cleanup status

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `platform`
- `toolchain`
- `simulator-device`
- `target`
- `command-evidence`
- `no-secret-values`
- `no-source-edit`

#### Hard Gates

- Mobile runtime evidence must name the exact source, platform, toolchain, target, simulator or device, command, exit, duration, and artifacts; missing signing or setup authority blocks rather than prompting for secrets.
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
- `workflow-runtime-upgrade`
- `defect-remediation`
- `baseline-regression-control`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `provider-cli-authentication-setup`

### provider-cli-authentication-setup

#### Responsibility

Install or authenticate one exact provider CLI after explicit local-system, credential, and external-session authorization, preserving non-secret identity, expiry, revocation, and cleanup evidence.

#### Trigger

Use when the request matches any of:
- One provider command-line tool must be installed or authenticated with scoped, expiring access
- Someone asks what identity, scope and revocation path a provider CLI login would create

Do not use when:
- Execute the reviewed provider experiment after authentication. Route to `llm-experiment-execution`.
- Verify an existing browser-agent pairing rather than a provider CLI session. Route to `browser-agent-pairing-verification`.

#### Required Inputs

- Provider CLI, version or install source, local-system authority, credential owner, authentication method, and cleanup policy.

#### Procedure

1. Verify provider, CLI source and version, platform, account owner, authentication method, scopes, region, storage, expiry, revocation, cleanup, local-system and per-action external-session authorization.
2. Preview exact binary source, files, config keys, browser or device login flow, scopes, and persistent session effects; refuse pasted secrets or overbroad scopes.
3. Perform only the approved install or authentication through the host, keeping credential values out of model, logs, hashes, and receipts.
4. Validate non-secret CLI identity and scope, then record version, account alias, region, expiry, storage, revocation, uninstall, cleanup, and failure state.

#### Output Contract

Produce:
- verified CLI version and non-secret identity
- scope and storage boundary
- expiry and revocation path
- uninstall, cleanup, and failure evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-provider`
- `approved-version`
- `least-scope`
- `non-secret-identity`
- `expiry`
- `revocation`
- `no-provider-action`

#### Hard Gates

- CLI authentication is setup authority only: it cannot execute provider mutations, and credential values or recovery codes never enter prompts, logs, hashes, or artifacts.
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

#### Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `llm-experiment-execution`
- `evaluation-dataset-publication`
- `browser-agent-pairing-verification`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `test-runtime-bootstrap`

### test-runtime-bootstrap

#### Responsibility

Install and configure one approved project-local test runtime, prove it with one real-behavior test, and restore dependency files if setup fails.

#### Trigger

Use when the request matches any of:
- A project has no working test runtime and one approved framework must be installed with a proving test
- Someone asks for the smallest change that lets a project run tests, with a restore path if setup fails

Do not use when:
- Design the overall test strategy before a framework is selected. Route to `testing-portfolio-strategy`.
- Author advanced tests once the runtime already exists. Route to `vitest-tooling`.

#### Required Inputs

- Project runtime, selected test framework, package policy, workspace authority, install command, and rollback baseline.

#### Procedure

1. Freeze project runtime, selected framework and version, package manager, install source, package policy, authorized files, example behavior, commands, and rollback baseline.
2. Inspect existing dependencies and config; use the current toolchain and add the minimum packages and configuration only if absent.
3. Write one real-behavior smoke test, run the approved command through the host, and capture dependency diff, tool version, exit, duration, and output.
4. On any failed install, config, or proof, restore dependency and config files to the baseline and report failure; never change global tooling or remote systems.

#### Domain Guidance

- When no framework is selected, propose defaults from project markers (for example manage.py: pytest with Django, package.json: Vitest or Jest, Gemfile: RSpec) as an offer; never run an install on a guess.
- Use a minimal executable test with the exact behavior and expected value requested, not a trivial substitute. Verification must show at least one test ran and zero failures. Rollback restores config and lockfile plus dependency installation from that lockfile (for example npm ci), only under the same approved workspace scope.

#### Output Contract

Produce:
- minimal project test configuration
- one passing real-behavior test
- dependency and lockfile diff
- verification or rollback evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `project-local`
- `minimal-install`
- `real-behavior-test`
- `dependency-diff`
- `rollback-baseline`
- `no-global-change`

#### Hard Gates

- Bootstrap passes only when the project-local runtime and one real-behavior test run successfully; failed setup must restore dependency and configuration files exactly.
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

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `testing-portfolio-strategy`
- `vitest-tooling`
- `playwright-test-engineering`
- `workflow-runtime-upgrade`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `tool-runtime-readiness`

### tool-runtime-readiness

#### Responsibility

Verify one required local tool runtime, version, invocation, capability, and safe failure mode without installing or upgrading it.

#### Trigger

Use when the request matches any of:
- A required local tool must be confirmed present, at the right version and able to do what the task needs
- Someone asks whether a tool on the path is actually usable before an owner starts work

Do not use when:
- Install or upgrade the missing workflow runtime. Route to `workflow-runtime-upgrade`.
- Bootstrap a project-local test framework and modify dependency files. Route to `test-runtime-bootstrap`.

#### Required Inputs

- A tool request, project path, shell environment, and declared prerequisite contract.

#### Procedure

1. Freeze tool identity, required version or range, source, invocation, capability, platform, project context, prohibited actions, and expected smoke result.
2. Resolve the actual executable or wrapper and compare version and capability without trusting PATH presence alone.
3. Run only an approved non-destructive help, version, doctor, or bounded smoke command and record path, version, command, exit, duration, output, and side effects.
4. Return ready, incompatible, missing, blocked, or failed with exact upgrade or bootstrap handoff; do not install or modify configuration.

#### Output Contract

Produce:
- tool readiness verdict
- executable and version evidence
- bounded smoke command record
- upgrade or bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `executable-path`
- `version`
- `required-capability`
- `bounded-smoke`
- `no-install`
- `failure-mode`

#### Hard Gates

- PATH presence is not readiness: the exact executable, version, required capability, invocation, and bounded smoke behavior must be verified without installation or configuration changes.
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
- `workflow-runtime-upgrade`
- `test-runtime-bootstrap`
- `agent-workflow-runtime-support`
- `document-rendering-and-validation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `workflow-orchestration-and-lifecycle`

### workflow-orchestration-and-lifecycle

#### Responsibility

Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.

#### Trigger

Use when the request matches any of:
- A request needs a workflow composed from several capabilities and no existing Recipe covers it
- A multi-stage effort needs typed handoffs, gates and invalidation rules defined before execution

Do not use when:
- Execute these implementation tasks in the workspace. Route to `plan-execution-control`.
- Classify a single vague request and choose only the next capability. Route to `context-intake-and-routing`.

#### Required Inputs

- A request, phase state, available capabilities, and execution constraints.

#### Procedure

1. Read request, current lifecycle state, artifact identities, available capability contracts, permissions, and stop conditions.
2. Check the released Recipes and router first; if one matches, return its id instead of composing a new workflow.
3. Select the smallest applicable capabilities and conditional branches; omit non-applicable stages with reasons.
4. Construct typed handoffs, authority transitions, feedback edges, and evidence invalidation rules.
5. Advance only on machine and human gates; stop on incompatible permissions or stale evidence.
6. Emit workflow state and next action without executing any selected capability.

#### Domain Guidance

- Reuse first: if an existing stage, composite or specialized Recipe matches the request, name it and stop; design a new workflow only for the uncovered remainder.
- The router owns Recipe selection; this Skill plans only what the released Recipes do not cover and never executes a selected capability.
- Routing ownership: use only when no Recipe covers the workflow; the router selects Recipes and context-intake-and-routing classifies requests.
- Missing action authorization is not a broader prohibition. Do not invent bans on cloud mutation, external writes or downstream capabilities beyond supplied policy.

#### Output Contract

Produce:
- workflow graph
- routing decisions
- typed handoffs
- state and invalidation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Orchestration may route, stop, retry, or invalidate, but must never impersonate a selected capability or merge incompatible execution identities.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `context-intake-and-routing`
- `implementation-planning-and-handoff`
- `plan-execution-control`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `workflow-runtime-upgrade`

### workflow-runtime-upgrade

#### Responsibility

Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes.

#### Trigger

Use when the request matches any of:
- One installed workflow runtime must be upgraded to a pinned version with backup and rollback
- Someone asks what an upgrade would change and how to verify the new version is actually the one running

Do not use when:
- Verify whether the current runtime is already ready without changing it. Route to `tool-runtime-readiness`.
- Install or authenticate a provider CLI and external session. Route to `provider-cli-authentication-setup`.

#### Required Inputs

- Installed runtime, target version, local-system write authorization, compatibility constraints, and rollback path.

#### Procedure

1. Verify installed runtime identity and version, source, target version and integrity, compatibility, local-system authority, files and services affected, configuration, data migration, backup, rollback, and downtime.
2. Preview exact commands, package or binary source, changes, migrations, restarts, and credential boundaries; refuse unpinned or untrusted updates.
3. Stop any process started before the upgrade and handle a vendored copy, then restart and verify the version the new process reports.
4. Back up state, perform only the approved upgrade through the host, stop on migration or verification failure, and avoid provider login or unrelated global changes.
5. Run version and compatibility checks, record before and after identity, commands, exits, duration, changed paths, health, rollback test or instructions, and cleanup.

#### Domain Guidance

- After the upgrade, stop any running daemon or background process that was started before it: a running process keeps serving the old binary and will make a health check pass against stale code. Then start fresh and verify the version it reports.
- Handle a local vendored copy of the runtime in the project explicitly: detect it, upgrade or report it separately, and note whether team mode requires the two to match.

#### Output Contract

Produce:
- runtime upgrade receipt
- before and after version evidence
- compatibility and health checks
- backup, rollback, and cleanup record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `detected-version`
- `pinned-target`
- `trusted-source`
- `compatibility`
- `backup`
- `rollback`
- `health-check`

#### Hard Gates

- A runtime upgrade requires a pinned trusted target, explicit affected paths, compatibility and migration plan, backup, rollback, and current post-upgrade health evidence; unpinned latest upgrades fail closed.
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
- `tool-runtime-readiness`
- `provider-cli-authentication-setup`
- `local-agent-memory-setup`
- `test-runtime-bootstrap`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
