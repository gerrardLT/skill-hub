---
name: document-rendering-and-validation
description: "Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations. Use when An approved document source must be rendered to PDF or HTML and the output checked for layout, links and accessibility; Someone asks whether a rendered file matches the approved source and release hash. Do not use for: Author or substantively edit the source document first (-> documentation-authoring); Package and version the verified rendered artifact for change delivery (-> change-packaging-and-versioning)."
---

# Document Rendering And Validation

## Responsibility

Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations.

## Trigger

Use when the request matches any of:
- An approved document source must be rendered to PDF or HTML and the output checked for layout, links and accessibility
- Someone asks whether a rendered file matches the approved source and release hash

Do not use when:
- Author or substantively edit the source document first. Route to `documentation-authoring`.
- Package and version the verified rendered artifact for change delivery. Route to `change-packaging-and-versioning`.

## Required Inputs

- Approved document source, renderer, format, template, accessibility target, and output path.

## Procedure

1. Freeze source and template hashes, renderer and version, target format and path, fonts or assets, page and accessibility criteria, link policy, and overwrite authorization.
2. Render only the approved source through the declared local command and record exit, duration, logs, and output identity.
3. Inspect pagination, clipping, overflow, fonts, images, links, headings, metadata, text extraction, language, and accessible structure where tooling supports it.
4. Return artifact, hash, validation evidence, unresolved rendering limitations, and rollback or no-write outcome; do not rewrite content or publish.

## Domain Guidance

- Compare the source hash with the approved value and state the result plainly: when it matches, say it matches and cite the approval; when it does not, say exactly which hash differs. A mismatch between an intermediate file and the release hash is not an integrity failure of the source.
- Separate template defects from author-content defects in the fix list so each goes to its owner.

## Output Contract

Produce:
- rendered document artifact
- renderer command evidence
- layout, link, and accessibility validation
- hash and residual-limitations report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `source-hash`
- `renderer-version`
- `output-hash`
- `layout-validation`
- `link-validation`
- `accessibility-limitations`

## Hard Gates

- A successful renderer exit is insufficient: the declared output must have current hash and inspected layout, links, text, metadata, and accessibility evidence or explicit unsupported limitations.
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
- `documentation-authoring`
- `artifact-persistence-and-tool-actions`
- `completion-evidence-gate`
- `change-packaging-and-versioning`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
