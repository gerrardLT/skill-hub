---
name: code-and-asset-remediation
description: "Consolidated capability with 5 selectable modes: defect-remediation; developer-self-check-and-fix; pull-request-comment-response; ui-remediation; website-audit-remediation. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [defect-remediation, developer-self-check-and-fix, pull-request-comment-response, ui-remediation, website-audit-remediation]
---

# Code And Asset Remediation

## Responsibility

Consolidated capability covering 5 related modes: Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace.; Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact.; Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads.; Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review.; Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `defect-remediation` | `workspace-write-local-exec` | A root cause is confirmed with a reproduction and the smallest safe source fix must be applied and verified; Someone asks for a patch plus a test that fails before and passes after, in an isolated wor | Investigate the symptom and establish a reproducible root cause first (-> root-cause-investigation); Independently revie |
| `developer-self-check-and-fix` | `workspace-write-local-exec` | An implementer has finished a task and should check their own work against the spec before handing it to independent review; A patch needs a self-review pass and deterministic in-scope fixes, not an a | Perform the independent code review and issue findings without changing source (-> independent-code-review); Investigate |
| `pull-request-comment-response` | `remote-write-authorized-only` | One identified pull request review comment needs a single evidence-backed reply posted under fresh authorization; Someone asks for the exact reply text and target for a specific review thread. | Acquire read-only pull-request and diff evidence before drafting a response (-> code-review-evidence-acquisition); Apply |
| `ui-remediation` | `workspace-write-local-exec` | Accepted UI findings must be fixed in source and the affected states recaptured for independent review; A reviewer's visual, responsive or interaction findings have been approved for repair. | Independently critique current rendered UI and issue findings (-> rendered-ui-critique-and-release-disposition); Define  |
| `website-audit-remediation` | `workspace-write-local-exec` | Accepted website audit findings (SEO, content, links, accessibility, performance) must be fixed in source; An audit report exists and the approved fixes should be applied in batches with re-audit evid | Assess the website and produce independent audit findings first (-> website-audit-assessment); Publish or deploy the rep |

## Mode: `defect-remediation`

### defect-remediation

#### Responsibility

Apply the smallest authorized source repair for a confirmed root cause and verify the changed behavior plus relevant regressions in one isolated workspace.

#### Trigger

Use when the request matches any of:
- A root cause is confirmed with a reproduction and the smallest safe source fix must be applied and verified
- Someone asks for a patch plus a test that fails before and passes after, in an isolated workspace

Do not use when:
- Investigate the symptom and establish a reproducible root cause first. Route to `root-cause-investigation`.
- Independently review the completed patch and report findings without edits. Route to `independent-code-review`.
- Fix only the author's own just-completed patch within its frozen scope. Route to `developer-self-check-and-fix`.

#### Required Inputs

- Confirmed finding, reproduction evidence, source workspace, repair authority, and regression contract.

#### Procedure

1. Confirm the workspace revision matches the revision the evidence came from; stop and flag any mismatch before patching.
2. Verify the confirmed cause, frozen scope, authorized workspace, single writer, reproduction, expected behavior, regression surface, and rollback path.
3. Inspect every caller and affected invariant; choose the highest shared correction point and avoid symptom guards or speculative refactors.
4. Write the smallest source and test patch that makes the reproduction fail before and pass after while preserving unrelated contracts.
5. Run approved focused and regression commands through the host, preserve failures, and return patch, evidence, changed files, and residual risk for independent review.

#### Domain Guidance

- If the evidence came from a specific release or revision, check out or diff that revision first; stop and flag when the frames or symptoms do not match the workspace.
- Discriminator: use when a root cause is confirmed and a minimal source repair is authorized.

#### Output Contract

Produce:
- minimal source and test patch
- before-and-after reproduction evidence
- focused and regression command records
- rollback and residual-risk note

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `confirmed-root-cause`
- `shared-fix-point`
- `minimal-patch`
- `single-writer`
- `focused-regression`
- `rollback`

#### Hard Gates

- Remediation cannot start from an unconfirmed symptom, and it cannot pass without a root-cause-linked patch plus current focused and affected-regression evidence.
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
- `root-cause-investigation`
- `tdd-change-loop`
- `developer-self-check-and-fix`
- `independent-code-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `developer-self-check-and-fix`

### developer-self-check-and-fix

#### Responsibility

Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact.

#### Trigger

Use when the request matches any of:
- An implementer has finished a task and should check their own work against the spec before handing it to independent review
- A patch needs a self-review pass and deterministic in-scope fixes, not an approval

Do not use when:
- Perform the independent code review and issue findings without changing source. Route to `independent-code-review`.
- Investigate a newly observed behavior whose root cause is not established. Route to `root-cause-investigation`.

#### Required Inputs

- Implemented code, its task specification, test output, and change list.

#### Procedure

1. Freeze the patch, scope, acceptance criteria, changed files, existing test evidence, and independent-review handoff boundary.
2. Inspect the diff and affected callers for correctness, error handling, security, compatibility, dead code, formatting, and test gaps.
3. Fix only reproducible in-scope defects; route scope expansion or unknown cause to the owning capability instead of opportunistic refactoring.
4. Run approved focused checks, record every correction and remaining concern, and hand off without declaring independent approval.

#### Domain Guidance

- Self-review questions. Completeness: is every requirement implemented, and are edge cases handled? Quality: are names accurate, is the code clean? Discipline: nothing built beyond the spec (YAGNI). Testing: do tests verify behavior rather than mocks?
- Report one state: DONE, DONE_WITH_CONCERNS (finished with doubts about correctness or scope, concerns listed), BLOCKED (cannot continue), or NEEDS_CONTEXT (named information missing).
- Fix only deterministic defects inside the frozen scope; everything else goes to the owner in the report.
- Discriminator: use for the author's own in-scope patch after it is complete; it never accepts findings from an independent review.
- Review every changed artifact, including unrelated edits, and give an explicit keep, split or revert disposition. Supply the exact runnable verification command when requested. Fix every deterministic in-scope defect and its boundary tests; do not invent behavior for undefined inputs—record the missing owner decision instead.

#### Output Contract

Produce:
- self-review checklist
- bounded correction patch
- updated focused evidence
- independent-review handoff
- report state (DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT) with concerns listed

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `self-review`
- `changed-files`
- `bounded-correction`
- `no-scope-expansion`
- `no-independent-approval`
- `handoff`

#### Hard Gates

- A developer correction pass may fix deterministic in-scope defects but must never impersonate independent review, erase failed evidence, or expand the frozen change.
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
- `defect-remediation`
- `root-cause-investigation`
- `independent-code-review`
- `implementation-spec-compliance-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `pull-request-comment-response`

### pull-request-comment-response

#### Responsibility

Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads.

#### Trigger

Use when the request matches any of:
- One identified pull request review comment needs a single evidence-backed reply posted under fresh authorization
- Someone asks for the exact reply text and target for a specific review thread

Do not use when:
- Acquire read-only pull-request and diff evidence before drafting a response. Route to `code-review-evidence-acquisition`.
- Apply the accepted requested source change. Route to `defect-remediation`.

#### Required Inputs

- Comment identity, verified finding classification, response artifact, evidence links, provider, and current authorization.

#### Procedure

1. Classify the comment as line-level or top-level and bind the reply target and endpoint to that class.
2. Verify repository, PR, comment or thread ID, author request, current refs, source and test evidence, response text, redaction, thread action, and fresh per-action authorization.
3. Ensure the response addresses only the identified comment, distinguishes fixed, declined, needs-input, and follow-up states, and cites current evidence without fabricated claims.
4. Preview exact body and target; perform one comment or reply write only, with no source edit, label, assignment, resolution, merge, or unrelated thread action.
5. Record provider receipt, comment URL or ID, request hash, resulting state, and failure or retry status.

#### Domain Guidance

- Classify the target first: a line-level review comment is answered as a reply in its thread; a top-level conversation comment is answered as a new conversation comment. Bind the reply target to that class and never post a line-level reply to the wrong endpoint.
- If a reply fails (closed PR, no permission), report the failure and stop; do not retry to a different target.
- Preserve the approved reply body byte-for-byte; do not add links, facts or edits without separate approval. Bind the proposed response and receipt to the exact authorization reference. Determine temporal validity from an explicit evaluation timestamp, never an assumed current date.

#### Output Contract

Produce:
- provider comment receipt
- posted response and evidence links
- target PR and thread identity
- failure or bounded retry record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-comment`
- `evidence-backed`
- `redaction`
- `per-action-authorization`
- `comment-receipt`
- `no-source-change`
- `no-thread-resolution`

#### Hard Gates

- Authorization covers one exact PR comment response and no other thread, source change, resolution, label, assignment, merge, or deployment action.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `code-review-evidence-acquisition`
- `defect-remediation`
- `remote-pull-request-change`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `ui-remediation`

### ui-remediation

#### Responsibility

Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review.

#### Trigger

Use when the request matches any of:
- Accepted UI findings must be fixed in source and the affected states recaptured for independent review
- A reviewer's visual, responsive or interaction findings have been approved for repair

Do not use when:
- Independently critique current rendered UI and issue findings. Route to `rendered-ui-critique-and-release-disposition`.
- Define the UI review matrix and acquire current captures before judgment. Route to `ui-review-scope-and-evidence-acquisition`.
- Fix accepted findings from a website audit tool (SEO, content, links, performance). Route to `website-audit-remediation`.

#### Required Inputs

- UI findings, source workspace, design system, platform variant, and write authority.

#### Procedure

1. Capture the pre-fix state of each affected route and viewport before changing source.
2. Verify accepted finding IDs, evidence, severity, repair direction, authorized files, design contract, affected states, review owner, and recapture plan.
3. Trace each finding to the smallest source change and preserve product truth, responsive behavior, content, accessibility, and interaction invariants.
4. Apply only approved repairs; route ambiguous taste, expanded scope, or architecture changes back to their owners.
5. Run approved focused checks and recapture affected route-state-viewport evidence; hand off to an independent reviewer without issuing disposition.

#### Domain Guidance

- Capture the pre-fix state of each affected route and viewport first. Where the app supports restoring state, add a regression fixture that restores the pre-fix state and asserts the fixed behavior.
- Discriminator: use when accepted, evidence-backed UI findings exist and need source changes.

#### Output Contract

Produce:
- bounded UI repair patch
- finding-to-change map
- focused verification evidence
- recapture bundle and independent-review handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `accepted-findings`
- `bounded-source-repair`
- `recapture`
- `reviewer-separation`
- `no-self-approval`

#### Hard Gates

- UI remediation requires accepted reproducible findings and separate authorization; the remediator cannot create its own findings, waive risk, judge its recaptures, or issue release disposition.
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
- `rendered-ui-critique-and-release-disposition`
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `website-audit-remediation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `website-audit-remediation`

### website-audit-remediation

#### Responsibility

Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary.

#### Trigger

Use when the request matches any of:
- Accepted website audit findings (SEO, content, links, accessibility, performance) must be fixed in source
- An audit report exists and the approved fixes should be applied in batches with re-audit evidence prepared

Do not use when:
- Assess the website and produce independent audit findings first. Route to `website-audit-assessment`.
- Publish or deploy the repaired website. Route to `deployment-trigger-execution`.
- Fix accepted findings from a rendered UI critique. Route to `ui-remediation`.
- Repair a defect whose root cause was confirmed outside a website audit. Route to `defect-remediation`.

#### Required Inputs

- Confirmed audit finding, source mapping, approved repair scope, workspace, and local verification command.

#### Procedure

1. Verify accepted finding IDs, original evidence, repair criteria, authorized files, content and SEO authority, test commands, and rollback boundary.
2. Deduplicate shared causes and order the smallest fixes that close findings without masking evidence or broad redesign.
3. Apply only authorized source, content, or local configuration changes; preserve unrelated routes, analytics, SEO, and behavior.
4. Run approved focused checks and prepare reassessment evidence; never deploy, close findings from self-attestation, or perform the independent audit.

#### Domain Guidance

- Discriminator: use when accepted website audit findings exist and need source changes.
- State unverified API and resource-type assumptions that the patch depends on; for missing image resources require a bounded nil guard or stop condition. Record independently observed out-of-scope defects in a separate handoff without repairing them or self-certifying the audit.

#### Output Contract

Produce:
- bounded website repair patch
- finding-to-fix traceability
- focused verification records
- independent reassessment handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `accepted-audit-findings`
- `bounded-repair`
- `SEO-preservation`
- `reassessment`
- `no-deploy`
- `no-self-close`

#### Hard Gates

- Website remediation cannot begin without accepted audit findings and cannot close them without separate current reassessment; repair authority never includes deployment.
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
- `website-audit-assessment`
- `ui-remediation`
- `deployment-trigger-execution`
- `completion-evidence-gate`
- `defect-remediation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
