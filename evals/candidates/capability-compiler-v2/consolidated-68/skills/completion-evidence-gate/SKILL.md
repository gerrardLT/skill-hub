---
name: completion-evidence-gate
description: "Consolidated capability with 4 selectable modes: baseline-regression-control; completion-evidence-gate; implementation-spec-compliance-review; rendered-ui-critique-and-release-disposition. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [baseline-regression-control, completion-evidence-gate, implementation-spec-compliance-review, rendered-ui-critique-and-release-disposition]
---

# Completion Evidence Gate

## Responsibility

Consolidated capability covering 4 related modes: Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair.; Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work.; Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source.; Independently critique current rendered UI and animation behavior and prioritize reproducible findings; recommend recapture or hand the findings to the release gate, without issuing the release disposition or mutating source.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `baseline-regression-control` | `local-exec` | A frozen baseline and a candidate must be run under matched conditions to find which differences are real regressions; Someone asks whether a failure is new, pre-existing, flaky or an intended change. | Design the project-wide mix of test layers and quality checks (-> testing-portfolio-strategy); Apply the accepted repair |
| `completion-evidence-gate` | `local-exec` | Someone claims work is done, tests pass or a build is green and the claim must be checked against current command evidence; A status needs a supported, unsupported or partial verdict tied to exit code | Fix the defects exposed by the completion check (-> defect-remediation) |
| `implementation-spec-compliance-review` | `read-only` | An implementation must be checked against its approved requirements for missing, extra or contradicting behavior; Someone asks whether what was built is what was requested, nothing more and nothing le | Review the same patch broadly for correctness, security, and code-quality defects (-> independent-code-review); Fix acce |
| `rendered-ui-critique-and-release-disposition` | `artifact-write-local-exec-external-read` | Current rendered captures and traces exist and someone needs a critique with reproducible, prioritized findings; A UI review needs blockers separated from improvements, taste choices and evidence gaps | Define which routes, states, viewports, traces, and tools must be captured for review (-> ui-review-scope-and-evidence-a |

## Mode: `baseline-regression-control`

### baseline-regression-control

#### Responsibility

Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair.

#### Trigger

Use when the request matches any of:
- A frozen baseline and a candidate must be run under matched conditions to find which differences are real regressions
- Someone asks whether a failure is new, pre-existing, flaky or an intended change

Do not use when:
- Design the project-wide mix of test layers and quality checks. Route to `testing-portfolio-strategy`.
- Apply the accepted repair for a confirmed regression. Route to `defect-remediation`.

#### Required Inputs

- A trusted historical baseline and a current measurement made under the same contract.

#### Procedure

1. Freeze baseline and candidate identities, environment, commands, data, seeds, warmup, thresholds, allowed variance, and comparison exclusions.
2. Run approved checks in matched conditions and record commands, versions, exits, duration, artifacts, hashes, and retries.
3. Separate new regression, pre-existing failure, flaky or environmental variance, intended change, and incomparable evidence.
4. Return a comparison and attribution report; never repair source, delete failures, or move thresholds after results.

#### Output Contract

Produce:
- matched baseline and candidate evidence
- regression attribution matrix
- variance and comparability report
- bounded repair handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `baseline-identity`
- `candidate-identity`
- `matched-environment`
- `threshold`
- `variance`
- `warmup`
- `regression-attribution`

#### Hard Gates

- A regression verdict requires frozen identities and matched commands, environment, data, seeds, warmup, thresholds, and retry policy; unmatched or stale evidence is incomparable, not passing.
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
- `testing-portfolio-strategy`
- `resilience-and-determinism`
- `defect-remediation`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `completion-evidence-gate`

### completion-evidence-gate

#### Responsibility

Verify a completion claim from current reproducible commands, exits, durations, source identity, artifacts, hashes, and declared limitations without changing the work.

#### Trigger

Use when the request matches any of:
- Someone claims work is done, tests pass or a build is green and the claim must be checked against current command evidence
- A status needs a supported, unsupported or partial verdict tied to exit codes, counts and artifact hashes

Do not use when:
- Fix the defects exposed by the completion check. Route to `defect-remediation`.

#### Required Inputs

- A proposed status claim and the command capable of proving it.

#### Procedure

1. Freeze the claimed outcome, target source or artifact identity, acceptance criteria, required checks, and evidence freshness window.
2. Validate every command, tool version, environment, exit code, duration, output summary, artifact path, and normalized hash against the current target.
3. If every criterion has current, target-bound evidence, return a clear Supported verdict with the evidence cited; otherwise list only the criteria that are unsupported and the owner for each.
4. Reject missing, stale, mismatched, self-attested, partial, skipped, or manually edited evidence and preserve failed checks.
5. Map each acceptance criterion to evidence and return a bounded status with limitations; never rerun commands, repair source, or upgrade a claim.

#### Domain Guidance

- When the supplied evidence satisfies every acceptance criterion and is current and target-bound, the verdict is Supported, stated plainly with the exit code, counts and freshness that justify it. Do not return needs-input when nothing required is missing.
- List missing or stale items only for criteria they actually affect, and name the originating owner who should produce the missing evidence; this Skill never runs the commands itself.
- A command piped into another (for example `test | tee`) reports the last command's exit code and can mask a failure. Give the exact unpiped form that captures the real exit code (`set -o pipefail; cmd; echo rc=$?`), and ask for the identities of any failing tests, not only the count.

#### Output Contract

Produce:
- criterion-to-evidence matrix
- completion gate result
- stale or missing evidence register
- limitations and invalidation conditions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `current-evidence`
- `source-identity`
- `command`
- `exit-code`
- `duration`
- `artifact-hash`
- `no-self-attestation`
- `limitations`

#### Hard Gates

- A completion claim cannot pass from prose, status text, model confidence, stale output, or partial success; each required criterion needs current target-bound executable or artifact evidence.
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
- `baseline-regression-control`
- `artifact-persistence-and-tool-actions`
- `defect-remediation`
- `change-delivery-preflight`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `implementation-spec-compliance-review`

### implementation-spec-compliance-review

#### Responsibility

Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source.

#### Trigger

Use when the request matches any of:
- An implementation must be checked against its approved requirements for missing, extra or contradicting behavior
- Someone asks whether what was built is what was requested, nothing more and nothing less

Do not use when:
- Review the same patch broadly for correctness, security, and code-quality defects. Route to `independent-code-review`.
- Fix accepted compliance gaps in the source. Route to `defect-remediation`.

#### Required Inputs

- Approved task requirements, implementation diff, source snapshot, and implementer report as an untrusted claim.

#### Procedure

1. Freeze requirement and design versions, source ref, patch, scope contract, test evidence, and review exclusions.
2. Map each stable requirement and design decision to implementation locations, tests, runtime evidence, or an explicit missing item.
3. Identify omitted, extra, contradictory, stale, or unverifiable behavior and distinguish spec defects from implementation defects.
4. Return a compliance matrix, findings, and revise-or-block recommendation for the human owner without edits.

#### Domain Guidance

- Check both direction and date when deriving future time windows: replacing the hour on the same date may schedule in the past. Trace opt-out, timezones and added behavior against each requirement.

#### Output Contract

Produce:
- requirement-to-implementation matrix
- compliance findings
- extra and missing behavior register
- human-owned disposition recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `frozen-spec`
- `source-ref`
- `traceability`
- `missing-behavior`
- `extra-behavior`
- `no-source-edit`

#### Hard Gates

- Compliance passes only when every frozen requirement and design obligation has current implementation and verification evidence and no unapproved behavior is silently introduced.
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
- `independent-code-review`
- `defect-remediation`
- `requirements-and-delivery-contract`
- `engineering-plan-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `rendered-ui-critique-and-release-disposition`

### rendered-ui-critique-and-release-disposition

#### Responsibility

Independently critique current rendered UI and animation behavior and prioritize reproducible findings; recommend recapture or hand the findings to the release gate, without issuing the release disposition or mutating source.

#### Trigger

Use when the request matches any of:
- Current rendered captures and traces exist and someone needs a critique with reproducible, prioritized findings
- A UI review needs blockers separated from improvements, taste choices and evidence gaps

Do not use when:
- Define which routes, states, viewports, traces, and tools must be captured for review. Route to `ui-review-scope-and-evidence-acquisition`.
- Edit the product source to fix the accepted UI findings. Route to `ui-remediation`.

#### Required Inputs

- Rendered captures, interaction traces, design criteria, accessibility context, and implementation constraints.

#### Procedure

1. Verify evidence identity, recency, route, viewport, state, zoom, theme, input mode, runtime, and contract coverage before critique.
2. Review user-flow clarity, information hierarchy, typography, color, spacing, content authenticity, responsive reflow, states, accessibility signals, and animation behavior in real renders.
3. Write one reproducible finding per issue with evidence citation, affected task and state, severity, principle, consequence, and bounded repair direction.
4. Separate blockers, high-value improvements, taste choices, evidence gaps, and accepted residual risk.
5. Recommend pass, needs-repair, recapture, or blocked to the human owner; never mutate product source or perform release.

#### Domain Guidance

- Audit categories: visual hierarchy and composition, typography, color and contrast, spacing and layout, interaction states, responsive reflow, motion, content and copy, accessibility signals, and perceived performance. Rate each finding high, medium or polish impact and give a category.
- The release disposition belongs to evidence-based-ui-review-and-release-gates; this Skill ends with the prioritized findings and a recapture need.
- Boundary: this Skill produces prioritized findings from rendered evidence; applying explicit release criteria and the final disposition recommendation belong to evidence-based-ui-review-and-release-gates.

#### Output Contract

Produce:
- rendered critique
- prioritized reproducible findings
- remediation hierarchy
- recapture recommendation and release-gate handoff

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `real-renders`
- `multi-viewport`
- `interaction-traces`
- `reproducible-findings`
- `no-source-mutation`

#### Hard Gates

- Static source review, DOM assertions, or a single ideal screenshot cannot substitute for current rendered evidence across the declared routes, states, viewports, input modes, and motion behavior.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

#### Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
