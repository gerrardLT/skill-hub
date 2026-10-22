---
name: mobile-platform-runtime-support
description: "Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source. Use when A mobile app must be built and run on an approved simulator or device and the result diagnosed; Someone asks why a mobile build or test target fails in the local toolchain. Do not use for: Install or upgrade the mobile toolchain or SDK on the local system (-> workflow-runtime-upgrade); Change application source to fix the diagnosed mobile defect (-> defect-remediation)."
---

# Mobile Platform Runtime Support

## Responsibility

Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source.

## Trigger

Use when the request matches any of:
- A mobile app must be built and run on an approved simulator or device and the result diagnosed
- Someone asks why a mobile build or test target fails in the local toolchain

Do not use when:
- Install or upgrade the mobile toolchain or SDK on the local system. Route to `workflow-runtime-upgrade`.
- Change application source to fix the diagnosed mobile defect. Route to `defect-remediation`.

## Required Inputs

- Mobile project, platform tools, simulator or device, local authority, and cleanup boundary.

## Procedure

1. Freeze source identity, platform, toolchain, runtime, simulator or device, target, command, signing or credential boundary, and allowed local actions.
2. Verify readiness without exposing credentials or mutating global toolchains; run only the approved build or test target.
3. Record command, versions, device identity, exit, duration, logs, artifacts, cleanup, and environmental limitations.
4. Return run evidence or bounded diagnosis and handoff; do not install system components or edit source.

## Domain Guidance

- Readiness checks before running: iOS, xcodebuild -showsdks and xcrun simctl list for the exact simulator; Android, adb devices and the SDK and build-tools versions. Record the before and after device list.
- Give a concrete check for each step (for example the expected build success line in the log, the artifact type and location) and state every assumption as an assumption; never invent a condition the task did not state.

## Output Contract

Produce:
- mobile runtime readiness record
- build or test execution evidence
- device and toolchain manifest
- bounded diagnosis and cleanup status

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `platform`
- `toolchain`
- `simulator-device`
- `target`
- `command-evidence`
- `no-secret-values`
- `no-source-edit`

## Hard Gates

- Mobile runtime evidence must name the exact source, platform, toolchain, target, simulator or device, command, exit, duration, and artifacts; missing signing or setup authority blocks rather than prompting for secrets.
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
- `workflow-runtime-upgrade`
- `defect-remediation`
- `baseline-regression-control`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
