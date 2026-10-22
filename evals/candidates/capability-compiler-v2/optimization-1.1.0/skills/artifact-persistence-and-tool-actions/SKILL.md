---
name: artifact-persistence-and-tool-actions
description: "Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task. Use when One validated artifact must be written to a declared workspace path with path containment and a recorded hash; Someone asks to save a result file without touching any other file or the product source. Do not use for: Render and validate the document's layout, links, and accessibility before persistence (-> document-rendering-and-validation); Publish this artifact to an external provider or repository (-> evaluation-dataset-publication); Save a learning or context record into the local learning store (-> local-learning-persistence)."
---

# Artifact Persistence And Tool Actions

## Responsibility

Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task.

## Trigger

Use when the request matches any of:
- One validated artifact must be written to a declared workspace path with path containment and a recorded hash
- Someone asks to save a result file without touching any other file or the product source

Do not use when:
- Render and validate the document's layout, links, and accessibility before persistence. Route to `document-rendering-and-validation`.
- Publish this artifact to an external provider or repository. Route to `evaluation-dataset-publication`.
- Save a learning or context record into the local learning store. Route to `local-learning-persistence`.

## Required Inputs

- A validated task, tool boundary, output location, and write authorization.

## Procedure

1. Verify the validated input, exact tool or write action, destination class, overwrite policy, authorization, and expected artifact identity.
2. Refuse path escape, undeclared files, source mutation disguised as persistence, remote targets, or destructive replacement without recovery.
3. Perform only the bounded action; preserve source bytes or declared normalization and record before/after identity.
4. Return the saved artifact or explicit no-write outcome with path, tool, exit status when applicable, hash, and limitations.

## Domain Guidance

- Order: write the file, compute its hash, then verify the written bytes against that hash. State a byte count or hash only when you computed it from the content given; otherwise leave an explicit placeholder.
- Never state an expected byte count or hash unless computed from the exact bytes. If not computed, leave a placeholder rather than estimating.

## Output Contract

Produce:
- bounded tool-action record
- persisted lifecycle artifact or no-write outcome
- path and hash evidence
- overwrite or recovery record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `bounded-action`
- `declared-path`
- `path-containment`
- `artifact-hash`
- `no-extra-files`
- `recovery`

## Hard Gates

- Persistence authority applies only to the declared artifact and location; it cannot authorize adjacent analysis, product-source edits, external publication, or additional files.
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
- `document-rendering-and-validation`
- `evaluation-dataset-publication`
- `completion-evidence-gate`
- `workflow-skill-authoring`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
