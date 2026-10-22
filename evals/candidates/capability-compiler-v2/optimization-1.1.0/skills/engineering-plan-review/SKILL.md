---
name: engineering-plan-review
description: "Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it. Use when A plan needs an independent architecture, data, failure-mode and rollback review before build starts; Someone asks whether a plan is safe to approve and wants gaps traced to approved requirements. Do not use for: Write or revise the implementation plan and work breakdown (-> implementation-planning-and-handoff); Perform a source and runtime threat audit of the actual system (-> security-audit-and-threat-modeling); Review the finished diff rather than the plan (-> independent-code-review); Review the plan from the perspective owned by independent-plan-review (-> independent-plan-review); Review the plan from the perspective owned by design-plan-review (-> design-plan-review); Review the plan from the perspective owned by developer-experience-plan-review (-> developer-experience-plan-review)."
---

# Engineering Plan Review

## Responsibility

Independently review an implementation plan for architecture, interfaces, data, failure modes, security, operability, migration, verification, and execution risk without editing it.

## Trigger

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

## Required Inputs

- Approved requirements, plan, architecture context, constraints, and existing system evidence.

## Procedure

1. Freeze the plan, approved requirements and design, target source identity, constraints, risk tolerance, and review scope.
2. Challenge scope: for each sub-problem cite existing code that already covers it or record none found, and name the minimum change.
3. Trace each requirement and design decision to plan steps, interfaces, data changes, tests, migration, rollout, and rollback.
4. Review dependency direction, failure behavior, concurrency, authorization, secrets, operability, performance, compatibility, and ownership.
5. Cite missing, contradictory, infeasible, untestable, risky, or unnecessary work with consequence and bounded recommendation.
6. Return findings, alternatives, residual risk, and approve-revise-block recommendation to the human owner without editing the plan or source.

## Domain Guidance

- Scope challenge first: for each sub-problem, cite existing code that already solves it or record that none was found, and name the minimum change that would satisfy the requirement.
- Deliver amendments as exact replacement text or a change set the owner can apply, not as general advice. The review itself never edits the plan or source.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.

## Output Contract

Produce:
- independent engineering review
- traceability and risk findings
- missing-test and rollback register
- human-owned review recommendation
- amendments as exact change set

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `traceability`
- `architecture`
- `data-migration`
- `authorization`
- `failure-modes`
- `operability`
- `rollback`
- `verification`

## Hard Gates

- A plan cannot pass on completeness of prose: every material architecture, data, security, migration, failure, and verification claim must trace to approved intent and an executable evidence path.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

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
