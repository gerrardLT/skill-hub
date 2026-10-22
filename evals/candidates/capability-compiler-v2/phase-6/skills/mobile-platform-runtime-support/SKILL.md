---
name: mobile-platform-runtime-support
description: Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source. Do not use for install or upgrade the mobile toolchain or sdk on the local system or change application source to fix the diagnosed mobile defect.
---

# Mobile Platform Runtime Support

## Responsibility

Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source.

## Trigger

Use when the requested outcome is: Run and diagnose an approved mobile build or test target in a declared local simulator or device environment without changing project source.

Do not use when:
- Install or upgrade the mobile toolchain or SDK on the local system. Route to `workflow-runtime-upgrade`.
- Change application source to fix the diagnosed mobile defect. Route to `defect-remediation`.

## Required Inputs

- Mobile project, platform tools, simulator or device, local authority, and cleanup boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze source identity, platform, toolchain, runtime, simulator or device, target, command, signing or credential boundary, and allowed local actions.
2. Verify readiness without exposing credentials or mutating global toolchains; run only the approved build or test target.
3. Record command, versions, device identity, exit, duration, logs, artifacts, cleanup, and environmental limitations.
4. Return run evidence or bounded diagnosis and handoff; do not install system components or edit source.

## Output Contract

Produce:
- mobile runtime readiness record
- build or test execution evidence
- device and toolchain manifest
- bounded diagnosis and cleanup status

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- `workflow-runtime-upgrade`
- `defect-remediation`
- `baseline-regression-control`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
