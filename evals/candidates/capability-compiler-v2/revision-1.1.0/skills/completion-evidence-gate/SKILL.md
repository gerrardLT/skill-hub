---
name: completion-evidence-gate
description: "Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work. Use when Someone claims work is done, tests pass or a build is green and the claim must be checked against current command evidence; A status needs a supported, unsupported or partial verdict tied to exit codes, counts and artifact hashes. Do not use for: Fix the defects exposed by the completion check (-> defect-remediation)."
---

# Completion Evidence Gate

## Responsibility

Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work.

## Trigger

Use when the request matches any of:
- Someone claims work is done, tests pass or a build is green and the claim must be checked against current command evidence
- A status needs a supported, unsupported or partial verdict tied to exit codes, counts and artifact hashes

Do not use when:
- Fix the defects exposed by the completion check. Route to `defect-remediation`.

## Required Inputs

- A proposed status claim and the command capable of proving it.

## Procedure

1. Freeze the claimed outcome, target source or artifact identity, acceptance criteria, required checks, and evidence freshness window.
2. Validate every command, tool version, environment, exit code, duration, output summary, artifact path, and normalized hash against the current target.
3. If every criterion has current, target-bound evidence, return a clear Supported verdict with the evidence cited; otherwise list only the criteria that are unsupported and the owner for each.
4. Reject missing, stale, mismatched, self-attested, partial, skipped, or manually edited evidence and preserve failed checks.
5. Map each acceptance criterion to evidence and return a bounded status with limitations; never rerun commands, repair source, or upgrade a claim.

## Domain Guidance

- When the supplied evidence satisfies every acceptance criterion and is current and target-bound, the verdict is Supported, stated plainly with the exit code, counts and freshness that justify it. Do not return needs-input when nothing required is missing.
- List missing or stale items only for criteria they actually affect, and name the originating owner who should produce the missing evidence; this Skill never runs the commands itself.
- A command piped into another (for example `test | tee`) reports the last command's exit code and can mask a failure. Give the exact unpiped form that captures the real exit code (`set -o pipefail; cmd; echo rc=$?`), and ask for the identities of any failing tests, not only the count.

## Output Contract

Produce:
- criterion-to-evidence matrix
- completion gate result
- stale or missing evidence register
- limitations and invalidation conditions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `current-evidence`
- `source-identity`
- `command`
- `exit-code`
- `duration`
- `artifact-hash`
- `no-self-attestation`
- `limitations`

## Hard Gates

- A completion claim cannot pass from prose, status text, model confidence, stale output, or partial success; each required criterion needs current target-bound executable or artifact evidence.
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
- `baseline-regression-control`
- `artifact-persistence-and-tool-actions`
- `defect-remediation`
- `change-delivery-preflight`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
