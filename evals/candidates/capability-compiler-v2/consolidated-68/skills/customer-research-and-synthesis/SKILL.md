---
name: customer-research-and-synthesis
description: "Consolidated capability with 4 selectable modes: customer-interview-execution; evidence-synthesis-and-opportunity-prioritization; problem-framing-and-customer-research; qualitative-evidence-synthesis. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [customer-interview-execution, evidence-synthesis-and-opportunity-prioritization, problem-framing-and-customer-research, qualitative-evidence-synthesis]
---

# Customer Research And Synthesis

## Responsibility

Consolidated capability covering 4 related modes: Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.; Synthesize heterogeneous evidence into bounded opportunity statements and compare them on explicit dimensions without hiding disagreement; ranking is left to the frameworks Skill or the human owner.; Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.; Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `customer-interview-execution` | `workspace-write` | An interview script or session needs to be non-leading, consented and recorded without mixing observation and interpretation; Someone asks for behavior-first interview questions and a note template fo | Synthesize themes across these completed interview records (-> qualitative-evidence-synthesis); Recruit or contact custo |
| `evidence-synthesis-and-opportunity-prioritization` | `workspace-write` | Mixed evidence (research notes, usage data, support tickets, competitor facts) must be reconciled into opportunity statements; Someone asks how strongly the evidence supports each candidate opportunit | Apply RICE or ICE with an exact formula to an existing opportunity set (-> opportunity-prioritization-and-frameworks); C |
| `problem-framing-and-customer-research` | `workspace-write` | Raw notes, a request or a hypothesis must be reframed as a customer problem before any solution is discussed; Someone asks whether a problem is real, who has it, how painful it is and what evidence is | Design experiments for a proposed solution hypothesis (-> solution-hypothesis-and-experiment-design); Synthesize themes  |
| `qualitative-evidence-synthesis` | `workspace-write` | Interview notes and quotes must be coded into themes with counterexamples and contradictions preserved; Someone asks what the qualitative evidence actually supports and where it is thin or split. | Turn the synthesized themes into prioritized opportunities (-> evidence-synthesis-and-opportunity-prioritization); Run t |

## Mode: `customer-interview-execution`

### customer-interview-execution

#### Responsibility

Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.

#### Trigger

Use when the request matches any of:
- An interview script or session needs to be non-leading, consented and recorded without mixing observation and interpretation
- Someone asks for behavior-first interview questions and a note template for customer conversations

Do not use when:
- Synthesize themes across these completed interview records. Route to `qualitative-evidence-synthesis`.
- Recruit or contact customers using their private details. Route to `research-planning-and-governance`.

#### Required Inputs

- A research objective, participant context, consent boundary, and interview script.

#### Procedure

1. Verify purpose, participant authority, consent, minimization, recording, retention, deletion, and external-transfer boundaries.
2. Write behavior-first questions about past events; remove pitching, hypotheticals, and confirmation cues.
3. Run or guide the session without contacting participants autonomously.
4. Record quotes and observations with source IDs; label interviewer inference separately.
5. Close with consented follow-up and deletion commitments.

#### Domain Guidance

- Restate the consent boundary exactly as the participant and owner gave it and do not invent extra terms. When a request goes past that boundary (external or commercial use, quoting in a roadmap, sharing beyond the team), deliver the part inside consent, propose asking for separate explicit consent for the wider use, and name the decision owner for any roadmap or status claim. Never block a follow-up the participant agreed to.
- Probes: 'tell me more about that', a gentle repeated 'why' (two or three times), 'can you give me a specific example', 'what happened next'.
- Observation log fields: participant id, date, key jobs, current solution, biggest pain, desired outcome, willingness to pay, direct quotes with source ids, and interviewer inference labelled separately.
- Record gaps in the evidence (for example a lost or inaudible segment) as follow-up: say what was lost and plan to re-collect it.

#### Output Contract

Produce:
- interview guide
- consent and governance record
- observation log
- follow-up register
- probe list and observation-log template

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not recruit, contact, record, retain, or transfer participant data without explicit authorization and governance terms.
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
- `research-planning-and-governance`
- `qualitative-evidence-synthesis`
- `problem-framing-and-customer-research`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `evidence-synthesis-and-opportunity-prioritization`

### evidence-synthesis-and-opportunity-prioritization

#### Responsibility

Synthesize heterogeneous evidence into bounded opportunity statements and compare them on explicit dimensions without hiding disagreement; ranking is left to the frameworks Skill or the human owner.

#### Trigger

Use when the request matches any of:
- Mixed evidence (research notes, usage data, support tickets, competitor facts) must be reconciled into opportunity statements
- Someone asks how strongly the evidence supports each candidate opportunity and where sources disagree

Do not use when:
- Apply RICE or ICE with an exact formula to an existing opportunity set. Route to `opportunity-prioritization-and-frameworks`.
- Code raw interview observations into themes before opportunity framing. Route to `qualitative-evidence-synthesis`.

#### Required Inputs

- Research notes, behavior data, support signals, competitive evidence, and candidate opportunities.

#### Procedure

1. Normalize evidence identities, populations, time windows, authority, and confidence.
2. Triangulate corroboration and contradiction across qualitative and quantitative sources.
3. Frame opportunities as user/problem/outcome statements without embedding solutions.
4. Compare importance, frequency, severity, reach, confidence, and strategic relevance as explicit dimensions.
5. Return a recommendation, dissent, unknowns, and evidence needed to change the ranking.

#### Domain Guidance

- Compare opportunities on importance, frequency, severity, reach, confidence and strategic relevance as separate columns. A requested composite ranking is calculated by the frameworks Skill through an explicit handoff; do not silently omit it.
- A deferred rename to evidence-synthesis-and-opportunity-framing is recorded; the id stays stable in this release.
- When the request also requires scores or ranking, deliver the synthesis and an explicit input-ready handoff to opportunity-prioritization-and-frameworks. Do not describe ranking as forbidden by the user or as awaiting approval merely to calculate it. A provisional evidence-led comparison may be delivered, labelled as a recommendation, not an approved decision.

#### Output Contract

Produce:
- opportunity set
- evidence-to-opportunity matrix
- comparison on explicit dimensions
- dissent register
- ranking handoff with evidence matrix, candidate ids, missing inputs and named scoring owner

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- No opportunity rank may be justified by source count alone or by silently converting assumptions into evidence.
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
- `qualitative-evidence-synthesis`
- `data-analysis-validation`
- `opportunity-prioritization-and-frameworks`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `problem-framing-and-customer-research`

### problem-framing-and-customer-research

#### Responsibility

Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.

#### Trigger

Use when the request matches any of:
- Raw notes, a request or a hypothesis must be reframed as a customer problem before any solution is discussed
- Someone asks whether a problem is real, who has it, how painful it is and what evidence is missing

Do not use when:
- Design experiments for a proposed solution hypothesis. Route to `solution-hypothesis-and-experiment-design`.
- Synthesize themes across multiple raw interview records. Route to `qualitative-evidence-synthesis`.

#### Required Inputs

- A problem hypothesis, target users, prior research, access constraints, and a decision to support.

#### Procedure

1. Inventory supplied claims, sources, authority, target users, and stated unknowns.
2. Interrogate the frame with the forcing questions (demand evidence, status quo, specific user, narrowest version) and restate any solution-shaped input as a problem.
3. Classify each material claim as fact, assumption, open question, or conflict.
4. Describe observed problem, context, behavior, workaround, impact, and evidence without solution language.
5. Preserve conflicting accounts and unknowns that change scope, outcome, authority, or safety.
6. Return a solution-free frame or needs-input/blocked status.

#### Domain Guidance

- Interrogate the frame with forcing questions: what is the strongest evidence of demand (not interest), what do people do today instead (the status quo), who specifically needs this most, and what is the narrowest version that would matter.
- Problem statement format: who has the problem, what it is, why it hurts, and the evidence (quotes, data) with source ids. It names no feature, mechanism or vendor. When the request is already solution-shaped, restate it as the underlying problem and list the solution as an unvalidated assumption.

#### Output Contract

Produce:
- problem frame
- classification register
- conflict register
- critical gap list
- structured problem statement with evidence and source ids

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Any proposed feature, mechanism, vendor, architecture, or implied solution in the problem frame is a boundary failure.
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
- `qualitative-evidence-synthesis`
- `solution-hypothesis-and-experiment-design`
- `requirements-and-delivery-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `qualitative-evidence-synthesis`

### qualitative-evidence-synthesis

#### Responsibility

Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.

#### Trigger

Use when the request matches any of:
- Interview notes and quotes must be coded into themes with counterexamples and contradictions preserved
- Someone asks what the qualitative evidence actually supports and where it is thin or split

Do not use when:
- Turn the synthesized themes into prioritized opportunities. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Run the interviews that produce the raw evidence. Route to `customer-interview-execution`.

#### Required Inputs

- Interview notes, direct quotes, affinity material, journey evidence, and known bias.

#### Procedure

1. Verify consent, minimization, redaction, retention, external-transfer, corpus identity, and analysis question.
2. Separate quote, observation, analyst code, interpretation, and unsupported inference.
3. Code records consistently and retain source IDs.
4. Synthesize themes with prevalence context, counterexamples, contradictions, and saturation limits.
5. Return findings and gaps without making priority or product decisions.

#### Domain Guidance

- Characterize each theme by depth (how strongly it affects those who hold it) and breadth (how many participants) as description only; this is not prioritization. Keep every minority or contradicting account as its own entry with its source id and say how it limits the theme.
- State the directional conclusion the evidence supports, while preserving minority accounts and uncertainty. Do not claim workspace access is unavailable when the task explicitly grants it; distinguish the actual no-tools evaluation environment from ownership.

#### Output Contract

Produce:
- coded evidence table
- theme map
- counterexample register
- confidence and saturation notes
- depth and breadth characterization per theme

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Do not expose raw participant data, count quotes as population prevalence, or erase minority and contradictory evidence.
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
- `customer-interview-execution`
- `evidence-synthesis-and-opportunity-prioritization`
- `data-analysis-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
