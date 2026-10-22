---
name: independent-plan-review
description: "Consolidated capability with 3 selectable modes: engineering-plan-review; executive-plan-review; independent-plan-review. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [engineering-plan-review, executive-plan-review, independent-plan-review]
---

# Independent Plan Review

## Responsibility

Consolidated capability covering 3 related modes: Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it.; Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.; Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `engineering-plan-review` | `read-only` | A plan needs an independent architecture, data, failure-mode and rollback review before build starts; Someone asks whether a plan is safe to approve and wants gaps traced to approved requirements. | Write or revise the implementation plan and work breakdown (-> implementation-planning-and-handoff); Perform a source an |
| `executive-plan-review` | `read-only` | A plan needs a leadership-level challenge of scope, leverage, user value and one-way decisions before commitment; Someone asks whether the plan is too small, too large or hides an irreversible bet. | Choose the company's strategy and approve the plan (-> strategic-choice-and-differentiation); Review the plan's implemen |
| `independent-plan-review` | `read-only` | A plan needs a general completeness and consistency review covering traceability, scope, tests and risks; Someone wants a verdict on whether a plan is ready for implementation without choosing a speci | Review only the user interface and design states in this plan (-> design-plan-review); Rewrite the plan to address the f |

## Mode: `engineering-plan-review`

### engineering-plan-review

#### Responsibility

Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it.

#### Trigger

Use when the request matches any of:
- A plan needs an independent architecture, data, failure-mode and rollback review before build starts
- Someone asks whether a plan is safe to approve and wants gaps traced to approved requirements

Do not use when:
- Write or revise the implementation plan and work breakdown. Route to `implementation-planning-and-handoff`.
- Perform a source and runtime threat audit of the actual system. Route to `security-audit-and-threat-modeling`.
- Review the finished diff rather than the plan. Route to `independent-code-review`.
- Review the plan from the perspective owned by independent-plan-review. Route to `independent-plan-review`.
- Review the plan from the perspective owned by design-plan-review. Route to `design-plan-review`.
- Review the plan from the perspective owned by developer-experience-plan-review. Route to `developer-experience-plan-review`.
- Review the plan from the perspective owned by executive-plan-review. Route to `executive-plan-review`.

#### Required Inputs

- Approved requirements, plan, architecture context, constraints, and existing system evidence.

#### Procedure

1. Freeze the plan, approved requirements and design, target source identity, constraints, risk tolerance, and review scope.
2. Challenge scope: for each sub-problem cite existing code that already covers it or record none found, and name the minimum change.
3. Trace each requirement and design decision to plan steps, interfaces, data changes, tests, migration, rollout, and rollback.
4. Review dependency direction, failure behavior, concurrency, authorization, secrets, operability, performance, compatibility, and ownership.
5. Cite missing, contradictory, infeasible, untestable, risky, or unnecessary work with consequence and bounded recommendation.
6. Return findings, alternatives, residual risk, and approve-revise-block recommendation to the human owner without editing the plan or source.

#### Domain Guidance

- Scope challenge first: for each sub-problem, cite existing code that already solves it or record that none was found, and name the minimum change that would satisfy the requirement.
- Deliver amendments as exact replacement text or a change set the owner can apply, not as general advice. The review itself never edits the plan or source.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

#### Output Contract

Produce:
- independent engineering review
- traceability and risk findings
- missing-test and rollback register
- human-owned review recommendation
- amendments as exact change set

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `traceability`
- `architecture`
- `data-migration`
- `authorization`
- `failure-modes`
- `operability`
- `rollback`
- `verification`

#### Hard Gates

- A plan cannot pass on completeness of prose: every material architecture, data, security, migration, failure, and verification claim must trace to approved intent and an executable evidence path.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `implementation-planning-and-handoff`
- `independent-plan-review`
- `security-audit-and-threat-modeling`
- `plan-review-decision-synthesis`
- `independent-code-review`
- `design-plan-review`
- `developer-experience-plan-review`
- `executive-plan-review`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `executive-plan-review`

### executive-plan-review

#### Responsibility

Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.

#### Trigger

Use when the request matches any of:
- A plan needs a leadership-level challenge of scope, leverage, user value and one-way decisions before commitment
- Someone asks whether the plan is too small, too large or hides an irreversible bet

Do not use when:
- Choose the company's strategy and approve the plan. Route to `strategic-choice-and-differentiation`.
- Review the plan's implementation interfaces and failure modes. Route to `engineering-plan-review`.
- Review the plan from the perspective owned by independent-plan-review. Route to `independent-plan-review`.
- Review the plan from the perspective owned by design-plan-review. Route to `design-plan-review`.
- Review the plan from the perspective owned by developer-experience-plan-review. Route to `developer-experience-plan-review`.

#### Required Inputs

- Plan, evidence, product context, constraints, and decision owners.

#### Procedure

1. State the review mode (expansion, selective expansion, hold scope or reduction) and evaluate every section, writing 'no issues found' where that is the result.
2. Read the plan, approved strategy, evidence, constraints, and decision authority.
3. Test problem importance, user value, leverage, alternatives, scope, reversibility, and downside.
4. Separate fact gaps, strategic disagreements, taste choices, and human-only decisions.
5. State proposed cuts, expansions, or options with evidence and tradeoffs.
6. Return challenged assumptions and required human decisions without persisting or approving a plan.

#### Domain Guidance

- Choose one review mode first and state it: scope expansion (dream bigger), selective expansion (hold the base, cherry-pick additions), hold scope (make it bulletproof), or scope reduction (cut to the core).
- Evaluate every review section without skipping; when a section has no findings write 'no issues found' explicitly rather than omitting it.
- Ambitious options stay options until a human selects them; none becomes accepted scope through this review.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

#### Output Contract

Produce:
- executive plan review
- scope challenge
- one-way-door register
- human decision queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not turn an ambitious option into accepted scope or write a CEO plan without explicit human selection and a separate persistence capability.
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
- `independent-plan-review`
- `engineering-plan-review`
- `plan-review-decision-synthesis`
- `strategic-choice-and-differentiation`
- `design-plan-review`
- `developer-experience-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `independent-plan-review`

### independent-plan-review

#### Responsibility

Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.

#### Trigger

Use when the request matches any of:
- A plan needs a general completeness and consistency review covering traceability, scope, tests and risks
- Someone wants a verdict on whether a plan is ready for implementation without choosing a specialty lens

Do not use when:
- Review only the user interface and design states in this plan. Route to `design-plan-review`.
- Rewrite the plan to address the findings. Route to `implementation-planning-and-handoff`.
- Review architecture, data, failure modes and operability in depth. Route to `engineering-plan-review`.

#### Required Inputs

- A proposed plan, repository constraints, task boundaries, and verification requirements.

#### Procedure

1. Freeze the reviewed plan version and its upstream artifacts.
2. Trace requirements to tasks, outputs, checks, owners, dependencies, risks, and rollback.
3. Identify missing, extra, contradictory, ambiguous, or untestable plan content with citations.
4. Classify severity, applicability, and whether a finding requires evidence or a human decision.
5. Return a verdict and amendments without editing or approving the plan.

#### Domain Guidance

- Reviewer selection: general completeness and traceability here; UX lens to design-plan-review; developer-facing surface to developer-experience-plan-review; strategy and scope leverage to executive-plan-review; architecture and failure modes to engineering-plan-review. Then synthesis of several reviews goes to plan-review-decision-synthesis.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.
- Preserve stated access exactly. Do not replace read-only repository access with message-only/no-access, and do not claim unavailable tools unless supplied or observed.

#### Output Contract

Produce:
- independent plan review
- traceability gaps
- finding register
- review verdict

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- The review must cite the frozen plan; generic best-practice advice without a demonstrated gap is not a finding.
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
- `design-plan-review`
- `developer-experience-plan-review`
- `executive-plan-review`
- `implementation-planning-and-handoff`
- `engineering-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
