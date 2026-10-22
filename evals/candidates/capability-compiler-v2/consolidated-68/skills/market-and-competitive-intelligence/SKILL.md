---
name: market-and-competitive-intelligence
description: "Consolidated capability with 5 selectable modes: competitive-case-library; competitive-response-and-monitoring; market-positioning-and-competitive-power; market-segmentation-and-demand-intelligence; strategic-choice-and-differentiation. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [competitive-case-library, competitive-response-and-monitoring, market-positioning-and-competitive-power, market-segmentation-and-demand-intelligence, strategic-choice-and-differentiation]
---

# Market And Competitive Intelligence

## Responsibility

Consolidated capability covering 5 related modes: Build a traceable case library from supplied or authorized competitor evidence for later comparison.; Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.; Evaluate a proposed market position against customer evidence, alternatives, category context, and sources of bargaining or competitive power.; Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability.; Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `competitive-case-library` | `workspace-write` | Dated competitor or comparable-company moves need to be recorded as reusable, sourced cases; Someone asks for a library of what rivals did, in what context and with what observed outcome. | Set up an ongoing competitor alert and response cadence (-> competitive-response-and-monitoring); Choose our final marke |
| `competitive-response-and-monitoring` | `workspace-write` | Competitor moves need watch signals, thresholds and pre-agreed response options rather than ad hoc reactions; Someone asks when a competitor release should trigger an investigation or a strategy decis | Build a one-time repository of historical competitor cases (-> competitive-case-library); Write the approved launch resp |
| `market-positioning-and-competitive-power` | `workspace-write` | A proposed market position needs testing against customer evidence, alternatives and competitive power; Someone asks whether a positioning claim is credible and which claims competitors can copy quick | Assess whether the business has a durable structural moat (-> structural-power-and-moats); Write the final approved mark |
| `market-segmentation-and-demand-intelligence` | `workspace-write` | A market must be divided into segments by job, urgency, willingness to pay and reachability rather than demographics; Someone asks which segment to validate first and what evidence of demand exists fo | Create a detailed evidence-bounded persona and journey for the selected segment (-> persona-jtbd-and-journey-modeling);  |
| `strategic-choice-and-differentiation` | `workspace-write` | Several mutually exclusive strategic options must be compared on value, fit, tradeoffs and reversibility; Someone asks what differentiates a position and what evidence would reverse the recommendation | Score a backlog of opportunities with a named prioritization formula (-> opportunity-prioritization-and-frameworks); Ass |

## Mode: `competitive-case-library`

### competitive-case-library

#### Responsibility

Build a traceable case library from supplied or authorized competitor evidence for later comparison.

#### Trigger

Use when the request matches any of:
- Dated competitor or comparable-company moves need to be recorded as reusable, sourced cases
- Someone asks for a library of what rivals did, in what context and with what observed outcome

Do not use when:
- Set up an ongoing competitor alert and response cadence. Route to `competitive-response-and-monitoring`.
- Choose our final market position against these competitors. Route to `market-positioning-and-competitive-power`.
- Code customer interview or research notes into themes. Route to `qualitative-evidence-synthesis`.

#### Required Inputs

- A competitive question, case material, historical context, and applicability boundary.

#### Procedure

1. Define inclusion criteria, time window, and source authority.
2. Record each case as actor, context, move, observed outcome, source, date, and confidence.
3. Normalize comparable dimensions without erasing source-specific context.
4. Separate observed outcomes from causal claims and analyst inference.
5. Index gaps, stale cases, and reusable comparison tags.

#### Output Contract

Produce:
- competitive case records
- evidence-quality register
- case taxonomy
- staleness queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- A case without a source, observation date, and fact-versus-inference label cannot enter the library.
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

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `competitive-response-and-monitoring`
- `market-positioning-and-competitive-power`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `competitive-response-and-monitoring`

### competitive-response-and-monitoring

#### Responsibility

Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.

#### Trigger

Use when the request matches any of:
- Competitor moves need watch signals, thresholds and pre-agreed response options rather than ad hoc reactions
- Someone asks when a competitor release should trigger an investigation or a strategy decision

Do not use when:
- Build a one-time repository of historical competitor cases. Route to `competitive-case-library`.
- Write the approved launch response copy and assets. Route to `documentation-authoring`.

#### Required Inputs

- Competitor releases, market signals, comparable products, and monitoring evidence.

#### Procedure

1. Name the competitive assumption and signals that could change it.
2. Define legal, ethical, source, cadence, owner, and staleness boundaries.
3. Separate noise, watch, investigate, and decision thresholds.
4. Draft no-response, reversible probe, and strategic-response options with evidence needs.
5. Escalate threshold crossings to human strategy owners.

#### Domain Guidance

- Monitor comparables as well as direct competitors: comparables tackle a similar problem in a different market and show patterns that will reach yours.
- Response options include no response, a reversible probe, a strategic response, and adopting a proven industry pattern when it is better than inventing a new one.

#### Output Contract

Produce:
- monitoring contract
- signal register
- response option matrix
- escalation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Monitoring may recommend options but must not scrape unauthorized sources or auto-change product, price, or messaging.
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
- `competitive-case-library`
- `strategic-choice-and-differentiation`
- `results-analysis-and-decision-readout`
- `documentation-authoring`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `market-positioning-and-competitive-power`

### market-positioning-and-competitive-power

#### Responsibility

Evaluate a proposed market position against customer evidence, alternatives, category context, and sources of bargaining or competitive power.

#### Trigger

Use when the request matches any of:
- A proposed market position needs testing against customer evidence, alternatives and competitive power
- Someone asks whether a positioning claim is credible and which claims competitors can copy quickly

Do not use when:
- Assess whether the business has a durable structural moat. Route to `structural-power-and-moats`.
- Write the final approved marketing copy. Route to `documentation-authoring`.

#### Required Inputs

- Market questions, customer alternatives, competitive evidence, and business constraints.

#### Procedure

1. Define target segment, job, alternatives, promised value, proof, category, and comparison frame.
2. Test claim relevance and credibility against customer and competitor evidence.
3. Map who gains or loses power across buyer, supplier, complement, channel, and rival relationships.
4. Identify unsupported superiority claims and positions competitors can copy quickly.
5. Return position options, proof gaps, risks, and a human decision request.

#### Domain Guidance

- The comparison frame includes the internal alternative and doing nothing (spending the same effort elsewhere), not only rival products.

#### Output Contract

Produce:
- positioning evidence map
- competitive power analysis
- claim-proof register
- position options

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not convert an attractive phrase into a validated position or imply market power without evidence about alternatives and bargaining structure.
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
- `structural-power-and-moats`
- `strategic-choice-and-differentiation`
- `competitive-case-library`
- `documentation-authoring`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `market-segmentation-and-demand-intelligence`

### market-segmentation-and-demand-intelligence

#### Responsibility

Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability.

#### Trigger

Use when the request matches any of:
- A market must be divided into segments by job, urgency, willingness to pay and reachability rather than demographics
- Someone asks which segment to validate first and what evidence of demand exists for each

Do not use when:
- Create a detailed evidence-bounded persona and journey for the selected segment. Route to `persona-jtbd-and-journey-modeling`.
- Choose the final strategic segment and commit resources. Route to `strategic-choice-and-differentiation`.

#### Required Inputs

- Customer situations, alternatives, segment constraints, incumbent observations, and market evidence.

#### Procedure

1. Define market boundary, unit of analysis, sources, time window, and decision use.
2. Identify candidate segments from job, trigger, pain, urgency, workaround, willingness, constraints, and reachability.
3. Estimate demand evidence and uncertainty without inventing market size.
4. Compare segment attractiveness, access, strategic fit, and exclusion risk.
5. Return segment hypotheses and validation gaps for human choice.

#### Domain Guidance

- In the attractiveness comparison include the incumbent access gap: segments where incumbents cannot or will not serve (for example secondary markets they lack inventory in) are often the better entry.

#### Output Contract

Produce:
- segment model
- demand evidence matrix
- segment attractiveness comparison
- validation backlog

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Demographics alone do not constitute a demand segment, and missing market evidence must not become fabricated TAM.
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
- `persona-jtbd-and-journey-modeling`
- `market-positioning-and-competitive-power`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `strategic-choice-and-differentiation`

### strategic-choice-and-differentiation

#### Responsibility

Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.

#### Trigger

Use when the request matches any of:
- Several mutually exclusive strategic options must be compared on value, fit, tradeoffs and reversibility
- Someone asks what differentiates a position and what evidence would reverse the recommendation

Do not use when:
- Score a backlog of opportunities with a named prioritization formula. Route to `opportunity-prioritization-and-frameworks`.
- Assess structural moat mechanisms in the business model. Route to `structural-power-and-moats`.

#### Required Inputs

- A market position, baseline utility, cost structure, strategic strength, and candidate differentiation.

#### Procedure

1. Freeze objective, decision owner, constraints, alternatives, evidence, and no-change option.
2. Evaluate customer value, fit, focus, differentiation, capabilities, economics, risk, reversibility, and second-order effects.
3. State mutually exclusive choices and the tradeoffs each accepts.
4. Identify evidence that would reverse the recommendation.
5. Return a recommendation, dissent, unknowns, and explicit human selection point.

#### Domain Guidance

- For networked products use the niche-first lens: the early audience often looks like a weird niche and the product like a toy; test whether the niche can compound before judging the market as small.

#### Output Contract

Produce:
- strategy choice matrix
- tradeoff register
- differentiation evidence
- human decision brief

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not disguise a bundle of incompatible choices as a strategy or convert recommendation strength into approval authority.
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
- `market-positioning-and-competitive-power`
- `structural-power-and-moats`
- `decision-and-outcome-roadmapping`
- `opportunity-prioritization-and-frameworks`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
