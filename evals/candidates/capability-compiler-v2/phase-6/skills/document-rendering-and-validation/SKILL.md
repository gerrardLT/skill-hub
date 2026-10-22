---
name: document-rendering-and-validation
description: Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations. Do not use for author or substantively edit the source document first or package and version the verified rendered artifact for change delivery.
---

# Document Rendering And Validation

## Responsibility

Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations.

## Trigger

Use when the requested outcome is: Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations.

Do not use when:
- Author or substantively edit the source document first. Route to `documentation-authoring`.
- Package and version the verified rendered artifact for change delivery. Route to `change-packaging-and-versioning`.

## Required Inputs

- Approved document source, renderer, format, template, accessibility target, and output path.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze source and template hashes, renderer and version, target format and path, fonts or assets, page and accessibility criteria, link policy, and overwrite authorization.
2. Render only the approved source through the declared local command and record exit, duration, logs, and output identity.
3. Inspect pagination, clipping, overflow, fonts, images, links, headings, metadata, text extraction, language, and accessible structure where tooling supports it.
4. Return artifact, hash, validation evidence, unresolved rendering limitations, and rollback or no-write outcome; do not rewrite content or publish.

## Output Contract

Produce:
- rendered document artifact
- renderer command evidence
- layout, link, and accessibility validation
- hash and residual-limitations report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `source-hash`
- `renderer-version`
- `output-hash`
- `layout-validation`
- `link-validation`
- `accessibility-limitations`

## Hard Gates

- A successful renderer exit is insufficient: the declared output must have current hash and inspected layout, links, text, metadata, and accessibility evidence or explicit unsupported limitations.
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
- `documentation-authoring`
- `artifact-persistence-and-tool-actions`
- `artifact-publication`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
