---
name: opportunity-and-roadmap-prioritization
description: "Consolidated capability with 4 selectable modes: ai-organizational-adoption-and-leadership; ai-product-opportunity-and-wedge; decision-and-outcome-roadmapping; opportunity-prioritization-and-frameworks. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [ai-organizational-adoption-and-leadership, ai-product-opportunity-and-wedge, decision-and-outcome-roadmapping, opportunity-prioritization-and-frameworks]
---

# Opportunity And Roadmap Prioritization

## Responsibility

Consolidated capability covering 4 related modes: Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.; Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.; Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.; Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `ai-organizational-adoption-and-leadership` | `workspace-write` | Leadership asks how to roll out an AI initiative: which team pilots first, who sponsors it, how value and risk are measured; An AI pilot needs enablement, ownership, stop criteria and an expansion dec | Decide the AI capability, model, data, autonomy, and safety architecture (-> ai-model-and-data-architecture); Configure  |
| `ai-product-opportunity-and-wedge` | `workspace-write` | A team asks whether AI gives real, defensible user value for a workflow and which narrow entry point to start with; Someone wants AI wedge candidates compared against a simpler non-AI alternative with | Design the model, vector database, and inference architecture for this approved AI feature (-> ai-model-and-data-archite |
| `decision-and-outcome-roadmapping` | `workspace-write` | An approved strategy must become a now, next, later roadmap organized by outcomes and decisions rather than features; Someone asks which assumptions must be resolved, and by when, before each roadmap  | Rank raw opportunities before strategy is approved (-> opportunity-prioritization-and-frameworks); Break an approved roa |
| `opportunity-prioritization-and-frameworks` | `workspace-write` | A set of opportunities must be ranked with a named formula such as RICE, ICE or Opportunity Score; Someone asks for a reproducible score and how the ranking changes if the inputs change. | Synthesize raw evidence into opportunity statements before scoring (-> evidence-synthesis-and-opportunity-prioritization |

## Mode: `ai-organizational-adoption-and-leadership`

### ai-organizational-adoption-and-leadership

#### Responsibility

Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.

#### Trigger

Use when the request matches any of:
- Leadership asks how to roll out an AI initiative: which team pilots first, who sponsors it, how value and risk are measured
- An AI pilot needs enablement, ownership, stop criteria and an expansion decision before any access is granted

Do not use when:
- Decide the AI capability, model, data, autonomy, and safety architecture. Route to `ai-model-and-data-architecture`.
- Configure production AI observability for the deployed system. Route to `ai-observability-configuration`.

#### Required Inputs

- An AI initiative, organizational constraints, leadership questions, pilot candidates, and value hypotheses.

#### Procedure

1. Freeze initiative and architecture status, user and business value hypotheses, teams, sponsors, current workflows, skills, governance, labor and change impacts, data boundaries, budget, risks, and decision owners.
2. Score each candidate pilot workflow on repeatability and reversibility and state why the chosen one is the smallest test of differentiated value.
3. Select the smallest reversible pilot and define participants, enablement, process changes, support, communication, access, safeguards, and non-adoption option.
4. Define measurable user, workflow, quality, cost, safety, trust, and organizational outcomes with baselines, review cadence, expansion and stop criteria.
5. Return adoption plan, leadership options, ownership model, and unresolved risks for human approval; do not grant access, configure systems, enroll users, or expand autonomy.

#### Domain Guidance

- Pilot selection: score each candidate workflow on repeatability (same steps, same inputs, frequent) and reversibility; prefer repeatable business processes over open-ended knowledge work.
- Pair top-down sponsorship with bottom-up early adopters: name a small tiger team of technically adjacent evangelists who can show measurable return quickly.
- Plan a diverge phase (teams explore freely under stated limits) followed by a dated converge decision on a few high-conviction bets; audit each AI feature against the core objective so adoption does not add product bloat.

#### Output Contract

Produce:
- AI adoption and pilot plan
- leadership decision material
- value and safety measurement contract
- ownership, enablement, and stop criteria

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `reversible-pilot`
- `sponsor-owner`
- `workflow-impact`
- `capability-building`
- `value-measures`
- `safety-governance`
- `stop-criteria`

#### Hard Gates

- AI adoption cannot pass on enthusiasm or tool availability: it needs a reversible pilot, named sponsor and owners, workflow and labor impacts, measurable value and safety outcomes, governance, and stop criteria.
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

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ai-model-and-data-architecture`
- `ai-agent-autonomy-and-human-control`
- `ai-observability-configuration`
- `feedback-and-continuous-learning-loop`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `ai-product-opportunity-and-wedge`

### ai-product-opportunity-and-wedge

#### Responsibility

Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.

#### Trigger

Use when the request matches any of:
- A team asks whether AI gives real, defensible user value for a workflow and which narrow entry point to start with
- Someone wants AI wedge candidates compared against a simpler non-AI alternative with falsification conditions

Do not use when:
- Design the model, vector database, and inference architecture for this approved AI feature. Route to `ai-model-and-data-architecture`.
- Write acceptance criteria for the approved AI assistant scope. Route to `requirements-and-delivery-contract`.

#### Required Inputs

- A validated customer problem, workflow friction, model trajectory, data advantage, and business constraint.

#### Procedure

1. State the user job, current workaround, pain, and evidence strength.
2. Compare AI leverage with a simpler deterministic or human process.
3. Map required data rights, feedback loop, failure cost, and human-control boundary.
4. Select the smallest wedge that can test differentiated value; preserve alternatives and unknowns.
5. Return a recommendation and falsification conditions for human decision.

#### Domain Guidance

- Score each candidate wedge on promise to payoff: the ratio of user effort removed to reward delivered, how often the workflow runs, and how repeatable its steps are. Pick the smallest wedge that tests differentiated value.
- Rate defensibility by layer, most to least durable: proprietary or uniquely accessible data, then interface and workflow integration, then the model itself. A model-only advantage is rated weak because any competitor can buy the same model.
- Always state the non-AI alternative and the condition under which the AI wedge would be falsified.

#### Output Contract

Produce:
- AI opportunity brief
- wedge hypothesis
- non-AI alternative
- data and feedback-loop risks
- wedge scoring table (promise-to-payoff) and defensibility rating by data, interface and model layer

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not treat probabilistic behavior, novelty, or model availability as proof of user value or product approval.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `solution-hypothesis-and-experiment-design`
- `ai-model-and-data-architecture`
- `strategic-choice-and-differentiation`
- `requirements-and-delivery-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `decision-and-outcome-roadmapping`

### decision-and-outcome-roadmapping

#### Responsibility

Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.

#### Trigger

Use when the request matches any of:
- An approved strategy must become a now, next, later roadmap organized by outcomes and decisions rather than features
- Someone asks which assumptions must be resolved, and by when, before each roadmap item can be committed

Do not use when:
- Rank raw opportunities before strategy is approved. Route to `opportunity-prioritization-and-frameworks`.
- Break an approved roadmap item into implementation tasks. Route to `implementation-planning-and-handoff`.

#### Required Inputs

- Strategy, candidate initiatives, experiment conclusions, priorities, capacity, and dependencies.

#### Procedure

1. Freeze approved outcomes, constraints, strategic choices, and decision owners.
2. Map assumptions and evidence needed to unlock each decision.
3. Sequence now/next/later horizons by dependency and learning value, not false date precision.
4. Represent options, kill criteria, and reversible commitments explicitly.
5. Define review cadence and handoff criteria without approving work.

#### Output Contract

Produce:
- outcome roadmap
- decision map
- assumption ledger
- review cadence

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- A roadmap item must link to an approved outcome and decision gate; feature presence alone is not sufficient.
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
- `opportunity-prioritization-and-frameworks`
- `implementation-planning-and-handoff`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `opportunity-prioritization-and-frameworks`

### opportunity-prioritization-and-frameworks

#### Responsibility

Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.

#### Trigger

Use when the request matches any of:
- A set of opportunities must be ranked with a named formula such as RICE, ICE or Opportunity Score
- Someone asks for a reproducible score and how the ranking changes if the inputs change

Do not use when:
- Synthesize raw evidence into opportunity statements before scoring. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Approve the highest-scoring item for delivery. Route to `decision-and-outcome-roadmapping`.

#### Required Inputs

- Validated problems, opportunities, evidence strength, constraints, and decision criteria.

#### Procedure

1. Verify comparable opportunity definitions, decision owner, time horizon, and required input evidence.
2. Name the framework and exact formula variant; define every variable, scale, direction, and normalization.
3. Record observed values, estimates, confidence, missing data, and sensitivity ranges.
4. Compute scores reproducibly and show how alternate variants or assumptions change ranking.
5. Return ranking as advice with caveats and human selection points.

#### Domain Guidance

- Canonical variants: RICE = (Reach x Impact x Confidence) / Effort with Reach in users per period, Impact on a stated scale, Confidence 0-100% and Effort in person-months; ICE = (Impact + Confidence + Ease) / 3 or the product, as named; Opportunity Score = Importance + max(Importance - Satisfaction, 0). Compute the variant the owner named. If the owner names a mix, compute the closest canonical variant and state the difference.
- Always compute the scores, show the arithmetic, and show the ranking under at least one alternate assumption (sensitivity).
- When an input is missing (for example an effort estimate), still deliver: compute provisional scores with the assumption labelled, give the ranking for items with known inputs, show how the ranking moves across the plausible range of the missing value, and name the owner who can supply it. Never declare the ranking indeterminate with no scores. Where sources conflict (survey versus usage), tie the conflict to the confidence score.
- A request to choose a scoring method authorizes proposing a clearly labelled analytical method, not approving a roadmap. Unknown effort limits effort-based comparisons, not evidence-only provisional rankings.

#### Output Contract

Produce:
- framework declaration
- scoring table
- sensitivity analysis
- human decision brief
- canonical variant definition and arithmetic for every score

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Declare the exact named or custom scoring formula, units and assumptions before computing; do not silently mix incompatible variants. If the user asks you to choose a method, propose and label a suitable formula without implying decision approval.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Named Formula Variants

When using RICE, ICE, Opportunity Score, or another named framework, record the framework name, exact formula variant, every variable and scale, assumptions, missing values, and sensitivity. Never silently combine formulas.

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `evidence-synthesis-and-opportunity-prioritization`
- `decision-and-outcome-roadmapping`
- `results-analysis-and-decision-readout`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
