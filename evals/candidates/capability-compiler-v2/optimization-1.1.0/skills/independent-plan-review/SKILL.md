---
name: independent-plan-review
description: "Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions. Use when A plan needs a general completeness and consistency review covering traceability, scope, tests and risks; Someone wants a verdict on whether a plan is ready for implementation without choosing a specialty lens. Do not use for: Review only the user interface and design states in this plan (-> design-plan-review); Rewrite the plan to address the findings (-> implementation-planning-and-handoff); Review architecture, data, failure modes and operability in depth (-> engineering-plan-review)."
---

# Independent Plan Review

## Responsibility

Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.

## Trigger

Use when the request matches any of:
- A plan needs a general completeness and consistency review covering traceability, scope, tests and risks
- Someone wants a verdict on whether a plan is ready for implementation without choosing a specialty lens

Do not use when:
- Review only the user interface and design states in this plan. Route to `design-plan-review`.
- Rewrite the plan to address the findings. Route to `implementation-planning-and-handoff`.
- Review architecture, data, failure modes and operability in depth. Route to `engineering-plan-review`.

## Required Inputs

- A proposed plan, repository constraints, task boundaries, and verification requirements.

## Procedure

1. Freeze the reviewed plan version and its upstream artifacts.
2. Trace requirements to tasks, outputs, checks, owners, dependencies, risks, and rollback.
3. Identify missing, extra, contradictory, ambiguous, or untestable plan content with citations.
4. Classify severity, applicability, and whether a finding requires evidence or a human decision.
5. Return a verdict and amendments without editing or approving the plan.

## Domain Guidance

- Reviewer selection: general completeness and traceability here; UX lens to design-plan-review; developer-facing surface to developer-experience-plan-review; strategy and scope leverage to executive-plan-review; architecture and failure modes to engineering-plan-review. Then synthesis of several reviews goes to plan-review-decision-synthesis.
- Reviewer selection: independent-plan-review for traceability and completeness; design-plan-review for UX scope and states; developer-experience-plan-review for developer setup and interfaces; engineering-plan-review for architecture and failure modes; executive-plan-review for leverage, scope and one-way decisions.
- Preserve stated access exactly. Do not replace read-only repository access with message-only/no-access, and do not claim unavailable tools unless supplied or observed.

## Output Contract

Produce:
- independent plan review
- traceability gaps
- finding register
- review verdict

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- The review must cite the frozen plan; generic best-practice advice without a demonstrated gap is not a finding.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `design-plan-review`
- `developer-experience-plan-review`
- `executive-plan-review`
- `implementation-planning-and-handoff`
- `engineering-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
