#!/usr/bin/env python3
"""Compile 31 semantically designed Phase 3 V2 candidate Skills."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.0-v2-candidate"
PHASE2_TREE = "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601"


def D(trigger: str, triggers: list[str], anti: list[tuple[str, str]], procedure: list[str], artifacts: list[str], gate: str, neighbors: list[str], *, data: bool = False, formula: bool = False, human: bool = False, boundary: str = "The request lacks a source, scope, or decision owner needed to preserve traceability.", authority: str = "The request asks the Skill to make or execute a decision outside its authority.") -> dict[str, Any]:
    return {"trigger": trigger, "triggers": triggers, "anti": anti, "procedure": procedure, "artifacts": artifacts, "distinctive_gate": gate, "neighbors": neighbors, "data_governance": data, "named_formula": formula, "human_decision": human, "boundary_case": boundary, "authority_case": authority}


DESIGNS: dict[str, dict[str, Any]] = {
    "ai-product-opportunity-and-wedge": D(
        "Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.",
        ["Assess whether AI is actually needed for this support workflow and find the narrowest useful wedge.", "Compare an AI feature idea with a deterministic alternative and identify the learning loop."],
        [("Design the model, vector database, and inference architecture for this approved AI feature.", "ai-model-and-data-architecture"), ("Write acceptance criteria for the approved AI assistant scope.", "requirements-and-delivery-contract")],
        ["State the user job, current workaround, pain, and evidence strength.", "Compare AI leverage with a simpler deterministic or human process.", "Map required data rights, feedback loop, failure cost, and human-control boundary.", "Select the smallest wedge that can test differentiated value; preserve alternatives and unknowns.", "Return a recommendation and falsification conditions for human decision."],
        ["AI opportunity brief", "wedge hypothesis", "non-AI alternative", "data and feedback-loop risks"],
        "Do not treat probabilistic behavior, novelty, or model availability as proof of user value or product approval.",
        ["solution-hypothesis-and-experiment-design", "ai-model-and-data-architecture", "strategic-choice-and-differentiation"], data=True, human=True),
    "competitive-case-library": D(
        "Build a traceable case library from supplied or authorized competitor evidence for later comparison.",
        ["Create a reusable library of competitor onboarding examples with source dates and confidence.", "Organize these authorized market cases by customer, move, outcome, and evidence quality."],
        [("Set up an ongoing competitor alert and response cadence.", "competitive-response-and-monitoring"), ("Choose our final market position against these competitors.", "market-positioning-and-competitive-power")],
        ["Define inclusion criteria, time window, and source authority.", "Record each case as actor, context, move, observed outcome, source, date, and confidence.", "Normalize comparable dimensions without erasing source-specific context.", "Separate observed outcomes from causal claims and analyst inference.", "Index gaps, stale cases, and reusable comparison tags."],
        ["competitive case records", "evidence-quality register", "case taxonomy", "staleness queue"],
        "A case without a source, observation date, and fact-versus-inference label cannot enter the library.",
        ["competitive-response-and-monitoring", "market-positioning-and-competitive-power", "qualitative-evidence-synthesis"], data=True),
    "competitive-response-and-monitoring": D(
        "Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.",
        ["Design a monthly competitor monitoring and response protocol for pricing and packaging changes.", "Turn this competitor movement into evidence thresholds and reversible response options."],
        [("Build a one-time repository of historical competitor cases.", "competitive-case-library"), ("Write the approved launch response copy and assets.", "documentation-authoring")],
        ["Name the competitive assumption and signals that could change it.", "Define legal, ethical, source, cadence, owner, and staleness boundaries.", "Separate noise, watch, investigate, and decision thresholds.", "Draft no-response, reversible probe, and strategic-response options with evidence needs.", "Escalate threshold crossings to human strategy owners."],
        ["monitoring contract", "signal register", "response option matrix", "escalation record"],
        "Monitoring may recommend options but must not scrape unauthorized sources or auto-change product, price, or messaging.",
        ["competitive-case-library", "strategic-choice-and-differentiation", "results-analysis-and-decision-readout"], data=True, human=True),
    "context-intake-and-routing": D(
        "Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work.",
        ["Route this vague product request to the right discovery or requirements capability.", "Inspect this task context and state the next capability, missing input, and stop condition."],
        [("Research the customer's underlying problem from these notes.", "problem-framing-and-customer-research"), ("Orchestrate the approved multi-stage capability workflow.", "workflow-orchestration-and-lifecycle")],
        ["Inventory the request, supplied artifacts, requested outcome, and explicit exclusions.", "Classify lifecycle stage, reversibility, risk, data sensitivity, and decision owner.", "Identify missing prerequisites and incompatible authority.", "Select one next capability or return needs-input/blocked with reasons.", "Emit only a routing envelope and preserved unknowns."],
        ["intake register", "routing decision", "missing-input list", "authority boundary"],
        "Never manufacture domain analysis merely to justify a route; route only from supplied evidence and declared scope.",
        ["workflow-orchestration-and-lifecycle", "risk-preflight-and-safety-governance", "problem-framing-and-customer-research"], human=True),
    "customer-interview-execution": D(
        "Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.",
        ["Create a non-leading interview guide and evidence log for these authorized participants.", "Help facilitate this consented customer interview and separate quotes, observations, and hypotheses."],
        [("Synthesize themes across these completed interview records.", "qualitative-evidence-synthesis"), ("Recruit or contact customers using their private details.", "research-planning-and-governance")],
        ["Verify purpose, participant authority, consent, minimization, recording, retention, deletion, and external-transfer boundaries.", "Write behavior-first questions about past events; remove pitching, hypotheticals, and confirmation cues.", "Run or guide the session without contacting participants autonomously.", "Record quotes and observations with source IDs; label interviewer inference separately.", "Close with consented follow-up and deletion commitments."],
        ["interview guide", "consent and governance record", "observation log", "follow-up register"],
        "Do not recruit, contact, record, retain, or transfer participant data without explicit authorization and governance terms.",
        ["research-planning-and-governance", "qualitative-evidence-synthesis", "problem-framing-and-customer-research"], data=True),
    "data-analysis-validation": D(
        "Validate a dataset, metric definition, transformation, and analytical claim before decision use.",
        ["Check whether this activation analysis supports the claimed retention conclusion.", "Validate these product metrics, joins, missing values, and comparison assumptions."],
        [("Collect new customer data to fill these gaps.", "research-planning-and-governance"), ("Make the product decision from the validated result.", "results-analysis-and-decision-readout")],
        ["Freeze the question, population, time window, metric formula, and expected decision use.", "Audit source authority, consent, schema, missingness, duplication, leakage, and transformations.", "Recompute key aggregates and compare denominators, cohorts, and uncertainty.", "Test plausible alternative explanations and sensitivity to exclusions.", "Return supported claims, unsupported claims, and data gaps."],
        ["analysis validation report", "metric definition register", "reproduction notes", "claim evidence table"],
        "No analytical claim passes without reproducible inputs, a declared denominator, and preserved uncertainty.",
        ["results-analysis-and-decision-readout", "qualitative-evidence-synthesis", "research-planning-and-governance"], data=True),
    "decision-and-outcome-roadmapping": D(
        "Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.",
        ["Turn these approved outcomes and assumptions into a decision roadmap with review points.", "Replace this feature calendar with outcome horizons, evidence gates, and options."],
        [("Rank raw opportunities before strategy is approved.", "opportunity-prioritization-and-frameworks"), ("Break an approved roadmap item into implementation tasks.", "implementation-planning-and-handoff")],
        ["Freeze approved outcomes, constraints, strategic choices, and decision owners.", "Map assumptions and evidence needed to unlock each decision.", "Sequence now/next/later horizons by dependency and learning value, not false date precision.", "Represent options, kill criteria, and reversible commitments explicitly.", "Define review cadence and handoff criteria without approving work."],
        ["outcome roadmap", "decision map", "assumption ledger", "review cadence"],
        "A roadmap item must link to an approved outcome and decision gate; feature presence alone is not sufficient.",
        ["opportunity-prioritization-and-frameworks", "implementation-planning-and-handoff", "strategic-choice-and-differentiation"], human=True),
    "design-plan-review": D(
        "Independently review a plan for UX scope, flows, states, evidence, accessibility, responsiveness, and unresolved taste decisions.",
        ["Review this implementation plan for missing UX states and design-system implications.", "Run an independent design lens on this plan without redesigning the interface."],
        [("Create the actual responsive UI design and token system.", "design-context-and-direction-contract"), ("Implement fixes to the interface after review.", "ui-remediation")],
        ["Confirm that UI scope exists; otherwise return not-applicable with evidence.", "Inspect users, journeys, information architecture, states, responsiveness, accessibility, content, motion, and rendered-review plan.", "Classify gaps as evidence defect, implementation ambiguity, contextual taste choice, or non-blocking suggestion.", "Cite the plan section for every finding and preserve contradictory constraints.", "Return amendments and human taste decisions; never edit or approve the plan."],
        ["design plan review", "missing-state matrix", "taste-decision register", "amendment recommendations"],
        "Review evidence only; do not create design artifacts, mutate the plan, or treat contextual aesthetics as universal law.",
        ["independent-plan-review", "developer-experience-plan-review", "design-context-and-direction-contract"], human=True),
    "developer-experience-plan-review": D(
        "Independently review a plan for developer setup, interfaces, feedback loops, errors, documentation, upgrades, and measurable DX outcomes.",
        ["Review this SDK plan for onboarding, error, upgrade, and time-to-first-success gaps.", "Apply a developer-experience lens to this CLI implementation plan."],
        [("Measure the live repository onboarding experience.", "developer-experience-assessment"), ("Implement the setup and error-message fixes.", "defect-remediation")],
        ["Establish whether the plan has a developer-facing surface; otherwise return not-applicable.", "Trace setup, first success, common task, debugging, failure, and upgrade journeys.", "Check API, CLI, SDK, docs, examples, compatibility, observability, and measurable DX criteria.", "Classify assumptions and cite every plan gap.", "Return amendments and unknowns without editing or approving the plan."],
        ["DX plan review", "developer journey gaps", "measurement recommendations", "plan amendments"],
        "Do not substitute general code quality comments for evidence about a developer-facing journey.",
        ["independent-plan-review", "design-plan-review", "developer-experience-assessment"], human=True),
    "document-and-artifact-governance": D(
        "Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.",
        ["Define governance for PRDs, decisions, diagrams, test evidence, and release artifacts.", "Create a source-of-truth and staleness policy for these project documents."],
        [("Write the actual architecture explanation document.", "documentation-authoring"), ("Persist a completed artifact to disk.", "artifact-persistence-and-tool-actions")],
        ["Inventory artifact types, consumers, producers, authority, and trust-boundary crossings.", "Assign stable identity, owner, canonical location, state, and replacement rules.", "Define required metadata, evidence links, retention, deletion, and access boundary.", "Define staleness and upstream-change invalidation rules.", "Publish the governance map and unresolved ownership gaps."],
        ["artifact registry", "ownership matrix", "state-transition policy", "staleness and retention rules"],
        "Governance may define where and when artifacts exist but must not invent, approve, or silently rewrite their contents.",
        ["documentation-authoring", "source-metadata-and-provenance", "artifact-persistence-and-tool-actions"]),
    "documentation-authoring": D(
        "Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.",
        ["Write a how-to for this verified local development workflow using the supplied commands.", "Turn these approved architecture facts into an explanation document with source links."],
        [("Decide the lifecycle, owner, and retention of all project documents.", "document-and-artifact-governance"), ("Update release notes from a shipped diff.", "release-documentation-maintenance")],
        ["Choose exactly one documentation intent and audience; state prerequisites and exclusions.", "Build a source map from approved facts, commands, and decisions.", "Draft the minimum structure appropriate to reference, explanation, how-to, or tutorial.", "Mark unknowns and avoid claiming unexecuted commands or unsupported behavior.", "Self-check links, examples, accessibility, and handoff for rendering or review."],
        ["documentation artifact", "source map", "validation notes", "unresolved-facts register"],
        "Never blend documentation types or turn an unverified command, feature, or future plan into present-tense fact.",
        ["document-and-artifact-governance", "release-documentation-maintenance", "document-rendering-and-validation"]),
    "evidence-synthesis-and-opportunity-prioritization": D(
        "Synthesize heterogeneous evidence into bounded opportunity statements and a traceable priority recommendation without hiding disagreement.",
        ["Synthesize these interviews, support tickets, and metrics into evidence-backed opportunities.", "Prioritize this evidence set by problem importance and confidence without using a named score yet."],
        [("Apply RICE or ICE with an exact formula to an existing opportunity set.", "opportunity-prioritization-and-frameworks"), ("Code raw interview observations into themes before opportunity framing.", "qualitative-evidence-synthesis")],
        ["Normalize evidence identities, populations, time windows, authority, and confidence.", "Triangulate corroboration and contradiction across qualitative and quantitative sources.", "Frame opportunities as user/problem/outcome statements without embedding solutions.", "Compare importance, frequency, severity, reach, confidence, and strategic relevance as explicit dimensions.", "Return a recommendation, dissent, unknowns, and evidence needed to change the ranking."],
        ["opportunity set", "evidence-to-opportunity matrix", "priority recommendation", "dissent register"],
        "No opportunity rank may be justified by source count alone or by silently converting assumptions into evidence.",
        ["qualitative-evidence-synthesis", "data-analysis-validation", "opportunity-prioritization-and-frameworks"], data=True, human=True),
    "executive-plan-review": D(
        "Independently challenge a plan's leverage, scope, user value, one-way doors, strategic risk, and decision ownership.",
        ["Review this plan as an executive for scope, leverage, one-way doors, and missing business decisions.", "Challenge whether this feature plan is the smallest valuable move without approving it."],
        [("Choose the company's strategy and approve the plan.", "strategic-choice-and-differentiation"), ("Review the plan's implementation interfaces and failure modes.", "engineering-plan-review")],
        ["Read the plan, approved strategy, evidence, constraints, and decision authority.", "Test problem importance, user value, leverage, alternatives, scope, reversibility, and downside.", "Separate fact gaps, strategic disagreements, taste choices, and human-only decisions.", "State proposed cuts, expansions, or options with evidence and tradeoffs.", "Return challenged assumptions and required human decisions without persisting or approving a plan."],
        ["executive plan review", "scope challenge", "one-way-door register", "human decision queue"],
        "Do not turn an ambitious option into accepted scope or write a CEO plan without explicit human selection and a separate persistence capability.",
        ["independent-plan-review", "engineering-plan-review", "plan-review-decision-synthesis"], human=True),
    "facilitation-and-collaboration-protocols": D(
        "Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.",
        ["Design a cross-functional workshop for resolving these product assumptions and ownership gaps.", "Create a decision session protocol that prevents dominant voices from erasing dissent."],
        [("Make the disputed product decision for the group.", "plan-review-decision-synthesis"), ("Interview customers one-on-one about past behavior.", "customer-interview-execution")],
        ["Define the session question, participants, roles, authority, pre-reads, and data boundary.", "Select activities that elicit independent evidence before convergence.", "Timebox divergence, synthesis, decision, dissent, and follow-up.", "Record decision owner, rationale, objections, unknowns, and expiry conditions.", "Produce actions and unresolved items without fabricating consensus."],
        ["facilitation plan", "role and authority map", "decision log template", "follow-up register"],
        "A facilitator may structure and record the decision but must not manufacture consensus or decide for the named owner.",
        ["customer-interview-execution", "plan-review-decision-synthesis", "document-and-artifact-governance"], data=True, human=True),
    "implementation-planning-and-handoff": D(
        "Convert approved requirements and design decisions into dependency-ordered implementation tasks and evidence-bearing handoffs without writing code.",
        ["Break this approved design into testable implementation tasks with dependencies and file boundaries.", "Create an implementation handoff from these requirements, interfaces, and migration decisions."],
        [("Clarify ambiguous product requirements before planning.", "requirements-and-delivery-contract"), ("Execute the approved implementation tasks.", "plan-execution-control")],
        ["Verify approved requirements, architecture, UX decisions, constraints, and unresolved blockers.", "Map each task to requirement IDs, interfaces, affected areas, test evidence, and completion criteria.", "Order tasks by dependency, risk retirement, migration safety, and integration points.", "Size tasks to independently reviewable changes; preserve rollback and observability work.", "Emit handoff artifacts, blocked prerequisites, and review checkpoints."],
        ["implementation plan", "requirement-task traceability", "dependency graph", "verification handoffs"],
        "Do not plan around unresolved product behavior, invent file paths as facts, or execute source changes.",
        ["requirements-and-delivery-contract", "workflow-orchestration-and-lifecycle", "plan-execution-control"]),
    "independent-plan-review": D(
        "Independently inspect a plan for traceability, completeness, consistency, feasibility, scope, tests, risks, and unresolved decisions.",
        ["Run a general independent review of this implementation plan against its requirements.", "Check this plan for missing dependencies, contradictions, scope creep, and unverifiable tasks."],
        [("Review only the user interface and design states in this plan.", "design-plan-review"), ("Rewrite the plan to address the findings.", "implementation-planning-and-handoff")],
        ["Freeze the reviewed plan version and its upstream artifacts.", "Trace requirements to tasks, outputs, checks, owners, dependencies, risks, and rollback.", "Identify missing, extra, contradictory, ambiguous, or untestable plan content with citations.", "Classify severity, applicability, and whether a finding requires evidence or a human decision.", "Return a verdict and amendments without editing or approving the plan."],
        ["independent plan review", "traceability gaps", "finding register", "review verdict"],
        "The review must cite the frozen plan; generic best-practice advice without a demonstrated gap is not a finding.",
        ["design-plan-review", "developer-experience-plan-review", "executive-plan-review"], human=True),
    "market-positioning-and-competitive-power": D(
        "Evaluate a proposed market position against customer evidence, alternatives, category context, and sources of bargaining or competitive power.",
        ["Assess whether this positioning claim is credible and powerful against actual alternatives.", "Map our proposed category position to customer evidence and competitive power."],
        [("Assess whether the business has a durable structural moat.", "structural-power-and-moats"), ("Write the final approved marketing copy.", "documentation-authoring")],
        ["Define target segment, job, alternatives, promised value, proof, category, and comparison frame.", "Test claim relevance and credibility against customer and competitor evidence.", "Map who gains or loses power across buyer, supplier, complement, channel, and rival relationships.", "Identify unsupported superiority claims and positions competitors can copy quickly.", "Return position options, proof gaps, risks, and a human decision request."],
        ["positioning evidence map", "competitive power analysis", "claim-proof register", "position options"],
        "Do not convert an attractive phrase into a validated position or imply market power without evidence about alternatives and bargaining structure.",
        ["structural-power-and-moats", "strategic-choice-and-differentiation", "competitive-case-library"], data=True, human=True),
    "market-segmentation-and-demand-intelligence": D(
        "Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability.",
        ["Segment this market by demand differences rather than demographics alone.", "Assess which customer segment has the strongest urgent demand using these sources."],
        [("Create a detailed evidence-bounded persona and journey for the selected segment.", "persona-jtbd-and-journey-modeling"), ("Choose the final strategic segment and commit resources.", "strategic-choice-and-differentiation")],
        ["Define market boundary, unit of analysis, sources, time window, and decision use.", "Identify candidate segments from job, trigger, pain, urgency, workaround, willingness, constraints, and reachability.", "Estimate demand evidence and uncertainty without inventing market size.", "Compare segment attractiveness, access, strategic fit, and exclusion risk.", "Return segment hypotheses and validation gaps for human choice."],
        ["segment model", "demand evidence matrix", "segment attractiveness comparison", "validation backlog"],
        "Demographics alone do not constitute a demand segment, and missing market evidence must not become fabricated TAM.",
        ["persona-jtbd-and-journey-modeling", "market-positioning-and-competitive-power", "strategic-choice-and-differentiation"], data=True, human=True),
    "opportunity-prioritization-and-frameworks": D(
        "Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.",
        ["Score these opportunities with RICE and declare the exact formula and assumptions.", "Compare ICE and Opportunity Score variants for this backlog without hiding missing inputs."],
        [("Synthesize raw evidence into opportunity statements before scoring.", "evidence-synthesis-and-opportunity-prioritization"), ("Approve the highest-scoring item for delivery.", "decision-and-outcome-roadmapping")],
        ["Verify comparable opportunity definitions, decision owner, time horizon, and required input evidence.", "Name the framework and exact formula variant; define every variable, scale, direction, and normalization.", "Record observed values, estimates, confidence, missing data, and sensitivity ranges.", "Compute scores reproducibly and show how alternate variants or assumptions change ranking.", "Return ranking as advice with caveats and human selection points."],
        ["framework declaration", "scoring table", "sensitivity analysis", "human decision brief"],
        "Reject any unnamed, hybrid, or partially specified RICE, ICE, Opportunity Score, or custom formula.",
        ["evidence-synthesis-and-opportunity-prioritization", "decision-and-outcome-roadmapping", "results-analysis-and-decision-readout"], formula=True, human=True),
    "persona-jtbd-and-journey-modeling": D(
        "Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts.",
        ["Create an evidence-bounded JTBD and journey from these interview and behavior records.", "Model the actors, triggers, anxieties, workarounds, and touchpoints in this customer journey."],
        [("Segment the whole market and estimate demand attractiveness.", "market-segmentation-and-demand-intelligence"), ("Design the interface flow that implements this journey.", "design-context-and-direction-contract")],
        ["Establish evidence sources, target decision, actor granularity, and confidence.", "Separate role, context, behavior, goal, job, desired progress, and unsupported demographic detail.", "Map trigger, consideration, action, use, failure, recovery, and follow-up touchpoints.", "Record functional, emotional, and social forces only when supported.", "Return model, evidence links, contradictions, and research gaps."],
        ["persona or actor model", "JTBD statement set", "journey map", "evidence and gap register"],
        "Proto-persona decoration, invented demographics, and generic journey stages must never be presented as customer evidence.",
        ["market-segmentation-and-demand-intelligence", "qualitative-evidence-synthesis", "design-context-and-direction-contract"], data=True),
    "plan-review-decision-synthesis": D(
        "Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.",
        ["Combine these executive, design, DX, and engineering reviews into a decision matrix.", "Synthesize conflicting plan-review findings while preserving dissent and human taste choices."],
        [("Perform the independent design review that is missing.", "design-plan-review"), ("Approve and edit the plan using the synthesized recommendations.", "implementation-planning-and-handoff")],
        ["Verify review identities, frozen plan version, citations, applicability, and independence.", "Deduplicate findings by underlying decision without erasing distinct rationale.", "Classify evidence defect, reversible choice, taste decision, one-way door, conflict, and non-applicable item.", "Preserve agreement, dissent, dependencies, and proposed amendments.", "Return an audit trail and explicit human decisions; do not approve or write the plan."],
        ["review decision matrix", "dissent register", "proposed amendments", "human approval queue"],
        "Synthesis cannot manufacture reviewer consensus, downgrade a blocking dissent, or convert recommendations into approved scope.",
        ["independent-plan-review", "executive-plan-review", "design-plan-review", "developer-experience-plan-review"], human=True),
    "problem-framing-and-customer-research": D(
        "Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.",
        ["Frame the customer problem in these notes without proposing a solution.", "Classify the supplied discovery evidence into facts, assumptions, conflicts, and open questions."],
        [("Design experiments for a proposed solution hypothesis.", "solution-hypothesis-and-experiment-design"), ("Synthesize themes across multiple raw interview records.", "qualitative-evidence-synthesis")],
        ["Inventory supplied claims, sources, authority, target users, and stated unknowns.", "Classify each material claim as fact, assumption, open question, or conflict.", "Describe observed problem, context, behavior, workaround, impact, and evidence without solution language.", "Preserve conflicting accounts and unknowns that change scope, outcome, authority, or safety.", "Return a solution-free frame or needs-input/blocked status."],
        ["problem frame", "classification register", "conflict register", "critical gap list"],
        "Any proposed feature, mechanism, vendor, architecture, or implied solution in the problem frame is a boundary failure.",
        ["qualitative-evidence-synthesis", "solution-hypothesis-and-experiment-design", "requirements-and-delivery-contract"], data=True),
    "qualitative-evidence-synthesis": D(
        "Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.",
        ["Synthesize these authorized interview notes into traceable themes and counterexamples.", "Code this feedback corpus while preserving minority evidence and contradictions."],
        [("Turn the synthesized themes into prioritized opportunities.", "evidence-synthesis-and-opportunity-prioritization"), ("Run the interviews that produce the raw evidence.", "customer-interview-execution")],
        ["Verify consent, minimization, redaction, retention, external-transfer, corpus identity, and analysis question.", "Separate quote, observation, analyst code, interpretation, and unsupported inference.", "Code records consistently and retain source IDs.", "Synthesize themes with prevalence context, counterexamples, contradictions, and saturation limits.", "Return findings and gaps without making priority or product decisions."],
        ["coded evidence table", "theme map", "counterexample register", "confidence and saturation notes"],
        "Do not expose raw participant data, count quotes as population prevalence, or erase minority and contradictory evidence.",
        ["customer-interview-execution", "evidence-synthesis-and-opportunity-prioritization", "data-analysis-validation"], data=True),
    "requirements-and-delivery-contract": D(
        "Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope.",
        ["Turn this approved problem and scope into EARS-style requirements and acceptance criteria.", "Create a delivery contract with actors, triggers, observable outcomes, edge cases, and traceability."],
        [("Discover whether this is the right customer problem to solve.", "problem-framing-and-customer-research"), ("Design the technical architecture and interfaces for approved requirements.", "architecture-candidate-reporting")],
        ["Verify approved problem, scope, users, outcomes, constraints, authority, and unresolved decisions.", "Assign stable requirement IDs and write actor-trigger-condition-observable-response statements.", "Cover normal, alternate, error, empty, boundary, recovery, permission, and non-functional behavior where applicable.", "Link acceptance criteria to requirements and evidence; reject implementation-only or subjective criteria.", "Run completeness, consistency, testability, scope, and unknown-preservation gate."],
        ["requirements specification", "acceptance criteria", "traceability matrix", "unknown and conflict register"],
        "Do not invent product behavior, choose architecture, or mark subjective and unobservable outcomes as acceptance criteria.",
        ["problem-framing-and-customer-research", "implementation-planning-and-handoff", "risk-preflight-and-safety-governance"], human=True),
    "research-planning-and-governance": D(
        "Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.",
        ["Plan customer research for this decision with sampling and data-governance controls.", "Choose a research method and evidence threshold without contacting participants yet."],
        [("Conduct the already approved customer interviews.", "customer-interview-execution"), ("Synthesize the completed qualitative corpus.", "qualitative-evidence-synthesis")],
        ["State the decision, research question, prior evidence, unknown, owner, and stopping rule.", "Select method and sampling logic appropriate to the claim; name bias and representativeness limits.", "Define authorization, consent, minimization, redaction, recording, retention, access, external-transfer, and deletion policy.", "Specify protocol, evidence schema, quality checks, analysis plan, and recruitment boundary.", "Return the plan and blocked governance inputs; do not recruit or collect data."],
        ["research plan", "sampling and method rationale", "data-governance contract", "analysis and stopping plan"],
        "No participant contact, collection, recording, external Judge use, or proprietary-data transfer may begin from an incomplete governance contract.",
        ["customer-interview-execution", "data-analysis-validation", "qualitative-evidence-synthesis"], data=True),
    "results-analysis-and-decision-readout": D(
        "Interpret frozen experiment or decision results against predeclared criteria, uncertainty, failure slices, and alternatives without making the final product decision.",
        ["Analyze these experiment results against the preset success and kill thresholds.", "Prepare a decision readout with uncertainty, failure slices, and a GO/PIVOT/KILL recommendation."],
        [("Design the experiment and its success criteria before execution.", "solution-hypothesis-and-experiment-design"), ("Commit the roadmap to the recommended decision.", "decision-and-outcome-roadmapping")],
        ["Freeze experiment identity, preregistered hypothesis, metrics, thresholds, exclusions, and analysis population.", "Validate result provenance and note protocol deviations or missing data.", "Compare outcomes to thresholds, uncertainty, segments, counter-metrics, and plausible alternatives.", "Separate observed result, interpretation, recommendation, and unknown.", "Return GO/PIVOT/KILL or continue recommendation for the named human decision owner."],
        ["results readout", "threshold comparison", "failure-slice analysis", "human decision recommendation"],
        "A recommendation may not be presented as a product decision, and post-hoc thresholds must be labeled rather than disguised as preregistered criteria.",
        ["solution-hypothesis-and-experiment-design", "decision-and-outcome-roadmapping", "data-analysis-validation"], data=True, human=True),
    "risk-preflight-and-safety-governance": D(
        "Classify task risk, reversibility, trust boundaries, data sensitivity, authorization, evidence, and required stop or escalation before execution.",
        ["Run a preflight on this proposed research and product task for safety, privacy, and authority.", "Classify the irreversible actions and missing approvals before this plan proceeds."],
        [("Produce the full technical threat model for the approved architecture.", "security-audit-and-threat-modeling"), ("Execute the authorized remote deployment.", "deployment-trigger-execution")],
        ["Inventory intended actions, actors, systems, data, external boundaries, cost, and irreversible effects.", "Classify safety, security, privacy, legal, reliability, human-impact, and authority risks.", "Identify controls, evidence, approvals, least privilege, rollback, and monitoring needs.", "Set proceed, needs-input, blocked, or specialist-review disposition with reasons.", "Emit a preflight envelope only; do not perform the action."],
        ["risk preflight", "authority matrix", "control checklist", "stop and escalation record"],
        "A prior authorization, tool availability, or low technical difficulty must never be treated as current permission for an irreversible or external action.",
        ["context-intake-and-routing", "security-audit-and-threat-modeling", "workflow-orchestration-and-lifecycle"], data=True, human=True),
    "solution-hypothesis-and-experiment-design": D(
        "Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria.",
        ["Design the smallest experiment that could falsify this solution hypothesis.", "Compare prototype, concierge, and data experiments for this validated problem."],
        [("Frame whether the customer problem is real from raw notes.", "problem-framing-and-customer-research"), ("Analyze the completed experiment and make a recommendation.", "results-analysis-and-decision-readout")],
        ["Verify the problem frame, target behavior, current evidence, ethical boundary, and decision to be informed.", "Write hypothesis, mechanism, predicted observable change, counterfactual, and failure interpretation.", "Generate experiment options ranked by learning value, risk, cost, and reversibility.", "Declare population, method, metrics, guardrails, thresholds, duration, stopping, and analysis plan before execution.", "Return experiment contract, risks, and authorization needs without running it."],
        ["hypothesis register", "experiment options", "selected experiment contract", "stopping and analysis criteria"],
        "A test without a falsifiable prediction, counterfactual, and predeclared success or kill criterion is not an experiment contract.",
        ["problem-framing-and-customer-research", "results-analysis-and-decision-readout", "ai-product-opportunity-and-wedge"], data=True, human=True),
    "strategic-choice-and-differentiation": D(
        "Compare strategic choices by customer value, coherence, tradeoffs, differentiation, capability fit, reversibility, and evidence, leaving selection to humans.",
        ["Compare these three strategic directions and state the tradeoffs and evidence gaps.", "Assess whether this differentiation is meaningful, defensible, and coherent for the chosen segment."],
        [("Score a backlog of opportunities with a named prioritization formula.", "opportunity-prioritization-and-frameworks"), ("Assess structural moat mechanisms in the business model.", "structural-power-and-moats")],
        ["Freeze objective, decision owner, constraints, alternatives, evidence, and no-change option.", "Evaluate customer value, fit, focus, differentiation, capabilities, economics, risk, reversibility, and second-order effects.", "State mutually exclusive choices and the tradeoffs each accepts.", "Identify evidence that would reverse the recommendation.", "Return a recommendation, dissent, unknowns, and explicit human selection point."],
        ["strategy choice matrix", "tradeoff register", "differentiation evidence", "human decision brief"],
        "Do not disguise a bundle of incompatible choices as a strategy or convert recommendation strength into approval authority.",
        ["market-positioning-and-competitive-power", "structural-power-and-moats", "decision-and-outcome-roadmapping"], human=True),
    "structural-power-and-moats": D(
        "Assess durable structural advantage mechanisms, prerequisites, counterevidence, decay, and imitation risk without treating current performance as a moat.",
        ["Assess which structural power mechanisms, if any, this business can credibly build.", "Challenge the claimed network effect and map its prerequisites and decay risks."],
        [("Choose the company's final strategic direction.", "strategic-choice-and-differentiation"), ("Craft the customer-facing market position.", "market-positioning-and-competitive-power")],
        ["Define the claimed advantage, relevant market, customer value, alternative, and evidence window.", "Test scale economies, network economies, counter-positioning, switching costs, branding, cornered resource, and process power only where applicable.", "For each candidate, state mechanism, prerequisite, reinforcement loop, imitation barrier, counterevidence, and decay risk.", "Separate current strength, temporary lead, execution quality, and structural power.", "Return supported, unsupported, and testable moat hypotheses."],
        ["structural power assessment", "mechanism evidence map", "counterevidence and decay register", "moat hypothesis backlog"],
        "Growth, market share, brand awareness, proprietary data, or technical complexity alone must not be labeled a moat without a durable causal mechanism.",
        ["strategic-choice-and-differentiation", "market-positioning-and-competitive-power", "competitive-response-and-monitoring"], data=True, human=True),
    "workflow-orchestration-and-lifecycle": D(
        "Select and sequence atomic capabilities, preserve state and artifact identities, enforce gates, and route feedback without performing downstream work.",
        ["Build a conditional capability workflow for this product task from the approved atomic contracts.", "Resume this lifecycle run from its saved stage and invalidate stale downstream evidence."],
        [("Execute these implementation tasks in the workspace.", "plan-execution-control"), ("Classify a single vague request and choose only the next capability.", "context-intake-and-routing")],
        ["Read request, current lifecycle state, artifact identities, available capability contracts, permissions, and stop conditions.", "Select the smallest applicable capabilities and conditional branches; omit non-applicable stages with reasons.", "Construct typed handoffs, authority transitions, feedback edges, and evidence invalidation rules.", "Advance only on machine and human gates; stop on incompatible permissions or stale evidence.", "Emit workflow state and next action without executing any selected capability."],
        ["workflow graph", "routing decisions", "typed handoffs", "state and invalidation record"],
        "Orchestration may route, stop, retry, or invalidate, but must never impersonate a selected capability or merge incompatible execution identities.",
        ["context-intake-and-routing", "implementation-planning-and-handoff", "plan-execution-control"], human=True),
}

HOLDOUTS: dict[str, tuple[str, str]] = {
    "ai-product-opportunity-and-wedge": ("A claims triage team wants an AI assistant. Decide whether a smaller deterministic intervention would prove value first, and define the narrow learning wedge.", "The AI assistant scope is approved; specify model serving, retrieval, storage, and observability architecture."),
    "competitive-case-library": ("Normalize these dated competitor launch records into reusable cases while separating observed outcomes from analyst inference.", "Set thresholds and owners for reacting to future competitor pricing changes."),
    "competitive-response-and-monitoring": ("Define which rival packaging signals merit watching, investigation, or a human strategy decision, including a no-response option.", "Catalog these historical competitor moves as source-dated reusable cases."),
    "context-intake-and-routing": ("Given this mixed request and its authority limits, return only the next atomic capability, missing inputs, and stop state.", "Analyze the supplied research notes and produce the customer problem frame itself."),
    "customer-interview-execution": ("Prepare a consented session about recent purchasing behavior; keep quotes, observations, and interviewer interpretation distinct.", "Across twenty completed interviews, code themes, contradictions, and saturation limits."),
    "data-analysis-validation": ("Audit whether the claimed conversion lift survives cohort, denominator, missing-data, and exclusion checks.", "Design a governed collection plan to obtain new customer data that could close these gaps."),
    "decision-and-outcome-roadmapping": ("Convert approved outcomes into now-next-later decisions, evidence gates, and kill criteria without promising a feature calendar.", "Rank these unprioritized opportunities with an exact named scoring framework before roadmap construction."),
    "design-plan-review": ("Inspect this checkout-plan document for omitted responsive, accessibility, empty, error, and recovery states without redesigning it.", "Produce the responsive checkout designs, components, tokens, and interaction states."),
    "developer-experience-plan-review": ("Review an SDK plan for time-to-first-success, upgrade, error, documentation, and compatibility gaps without touching code.", "Run the repository setup and measure the live onboarding journey."),
    "document-and-artifact-governance": ("Define owners, canonical locations, stale conditions, retention, and replacement rules for specs, ADRs, and test evidence.", "Draft the actual how-to explaining the approved local setup commands."),
    "documentation-authoring": ("Using only the verified commands and architecture facts, write one audience-specific troubleshooting how-to with source links.", "Define which documentation is canonical, who owns it, and when it expires."),
    "evidence-synthesis-and-opportunity-prioritization": ("Triangulate support logs, interviews, and usage data into solution-free opportunities, dissent, and a traceable ranking rationale.", "Apply the team's selected RICE formula to the already validated opportunity list."),
    "executive-plan-review": ("Challenge this proposal's leverage, scope, irreversible commitments, and user value; leave acceptance to the named sponsor.", "Choose the company's strategic direction and approve the plan for implementation."),
    "facilitation-and-collaboration-protocols": ("Design a workshop that elicits independent evidence before convergence and records dissent, owner, and decision expiry.", "Resolve the disputed roadmap choice on behalf of the workshop participants."),
    "implementation-planning-and-handoff": ("Turn approved requirements, interfaces, and UX decisions into dependency-ordered, independently verifiable work slices.", "Resolve the product behavior that remains ambiguous in these requirements before implementation planning."),
    "independent-plan-review": ("Against the frozen requirements, find missing, extra, contradictory, infeasible, or untestable plan content with citations.", "Limit the review to visual hierarchy, UI states, responsiveness, and accessibility."),
    "market-positioning-and-competitive-power": ("Test whether the proposed category promise is relevant, credible, distinct from alternatives, and supported by bargaining-power evidence.", "Evaluate whether claimed network effects and switching costs form a durable moat."),
    "market-segmentation-and-demand-intelligence": ("Derive demand segments from job, urgency, workaround, willingness, constraints, and reachability rather than age bands.", "Build the selected segment's detailed JTBD and end-to-end journey."),
    "opportunity-prioritization-and-frameworks": ("Use the team's stated RICE variant to score the frozen opportunity set, showing variable definitions, estimates, and sensitivity.", "Turn raw notes and metrics into the opportunity statements that should later be scored."),
    "persona-jtbd-and-journey-modeling": ("From cited behavior records, model actors, triggering circumstances, desired progress, forces, and failure/recovery touchpoints.", "Estimate the market attractiveness and reachability of all candidate segments."),
    "plan-review-decision-synthesis": ("Combine four independent reviews of the same plan, retain disagreements, and separate reversible choices from human taste decisions.", "Perform the missing independent engineering review before any synthesis."),
    "problem-framing-and-customer-research": ("Classify the supplied claims and evidence into a solution-free account of the user's context, workaround, pain, impact, and critical unknowns.", "Choose prototype types, metrics, thresholds, and duration for testing a proposed solution."),
    "qualitative-evidence-synthesis": ("Code this governed feedback corpus into traceable themes while preserving counterexamples, minority evidence, and analyst inference labels.", "Rank the resulting opportunities by importance, confidence, and strategic fit."),
    "requirements-and-delivery-contract": ("Write stable requirement IDs and observable acceptance criteria for the approved behavior, including permission, error, boundary, and recovery cases.", "Determine from discovery evidence whether this is the right problem to solve."),
    "research-planning-and-governance": ("Plan evidence collection for a churn decision, including sampling logic, consent, minimization, recording, retention, transfer, and deletion.", "Contact the approved participants and conduct the scheduled interviews."),
    "results-analysis-and-decision-readout": ("Compare the frozen experiment results with preregistered thresholds and failure slices, then advise the human owner without deciding.", "Select metrics, guardrails, duration, and stopping rules for an experiment that has not run."),
    "risk-preflight-and-safety-governance": ("Before work begins, classify sensitive data, external effects, reversibility, approvals, rollback, and specialist review needs.", "Produce a full technical threat model for the already approved system architecture."),
    "solution-hypothesis-and-experiment-design": ("For this validated problem, define a falsifiable mechanism and the smallest reversible test with predeclared success and kill criteria.", "Use the raw discovery notes to determine whether the customer problem itself is valid."),
    "strategic-choice-and-differentiation": ("Compare the no-change option and three mutually exclusive strategies by value, coherence, differentiation, fit, risk, and reversibility.", "Calculate RICE scores for a backlog within an already selected strategy."),
    "structural-power-and-moats": ("Test the claimed data network effect for causal reinforcement, prerequisites, imitation barriers, counterevidence, and decay.", "Choose which of the assessed strategic alternatives the company will fund."),
    "workflow-orchestration-and-lifecycle": ("From atomic contracts and current state, construct conditional stages, typed handoffs, feedback routes, and invalidation without executing them.", "Open the workspace and carry out the selected implementation capability."),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def baseline_for(slug: str, capability: dict[str, Any]) -> dict[str, Any]:
    released = {
        "problem-framing-and-customer-research": "problem-framing@0.2.0",
        "risk-preflight-and-safety-governance": "requirements-quality-gate@0.2.0",
    }
    if slug in released:
        return {"kind": "released-v1-slot", "identity": released[slug], "reason": "Closest released V1 behavior boundary; candidate must improve provenance, atomicity, trigger separation, or policy enforcement without regressing the V1 core."}
    roots = sorted({evidence.split("/", 1)[0] for evidence in capability["source_evidence"] if "/" in evidence})
    return {"kind": "source-skill", "identity": roots[0] if roots else "no-capability-baseline", "reason": "Closest source behavior; no released V1 Slot has this exact atomic responsibility."}


def render_skill(slug: str, capability: dict[str, Any], design: dict[str, Any]) -> str:
    inputs = "\n".join(f"- {item}" for item in capability["inputs"])
    outputs = "\n".join(f"- {item}" for item in design["artifacts"])
    procedure = "\n".join(f"{index}. {item}" for index, item in enumerate(design["procedure"], 1))
    neighbors = "\n".join(f"- `{item}`" for item in design["neighbors"])
    governance = """
## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.
""" if design["data_governance"] else ""
    formula = """
## Named Formula Variants

When using RICE, ICE, Opportunity Score, or another named framework, record the framework name, exact formula variant, every variable and scale, assumptions, missing values, and sensitivity. Never silently combine formulas.
""" if design["named_formula"] else ""
    human = """
## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.
""" if design["human_decision"] else ""
    return f"""---
name: {slug}
description: {design['trigger']} Do not use for {design['anti'][0][0].rstrip('.').lower()} or {design['anti'][1][0].rstrip('.').lower()}.
---

# {slug.replace('-', ' ').title()}

## Responsibility

{design['trigger']}

## Trigger

Use when the requested outcome is: {design['trigger']}

Do not use when:
- {design['anti'][0][0]} Route to `{design['anti'][0][1]}`.
- {design['anti'][1][0]} Route to `{design['anti'][1][1]}`.

## Required Inputs

{inputs}

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

{procedure}

## Output Contract

Produce:
{outputs}

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- {design['distinctive_gate']}
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
{governance}{formula}{human}
## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

{capability['non_responsibility']}

Adjacent capabilities:
{neighbors}

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
"""


def schemas() -> dict[str, dict[str, Any]]:
    strings = {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": True}
    nonempty = {**strings, "minItems": 1}
    contract = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "responsibility", "inputs", "outputs", "permission_identity", "statuses", "hard_gates", "forbidden_actions", "artifact_types", "execution", "policy"], "properties": {
        "schema_version": {"const": "2.0"}, "id": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string", "pattern": "^capability:"}, "responsibility": {"type": "string", "minLength": 20}, "inputs": nonempty, "outputs": nonempty, "permission_identity": {"enum": ["workspace-write", "read-only"]}, "statuses": {"type": "array", "const": ["passed", "needs-input", "blocked", "failed"]}, "hard_gates": nonempty, "forbidden_actions": nonempty, "artifact_types": nonempty,
        "execution": {"type": "object", "additionalProperties": False, "required": ["adapter", "model_tools", "mutation_scope", "remote_write"], "properties": {"adapter": {"const": "artifact"}, "model_tools": strings, "mutation_scope": {"enum": ["run-output", "none"]}, "remote_write": {"const": False}}},
        "policy": {"type": "object", "additionalProperties": False, "required": ["human_decision", "data_governance", "named_formula_variants"], "properties": {"human_decision": {"type": "boolean"}, "data_governance": {"type": "boolean"}, "named_formula_variants": {"type": "boolean"}}}
    }}
    provenance = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "phase2_artifact_tree_sha256", "source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs", "candidate_files"], "properties": {"schema_version": {"const": "2.0"}, "id": {"type": "string"}, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string"}, "phase2_artifact_tree_sha256": {"const": PHASE2_TREE}, "source_cluster_ids": strings, "canonical_unit_ids": strings, "retained_auxiliary_unit_ids": strings, "root_derived_atom_ids": strings, "source_fragment_ids": strings, "fusion_decision_ids": nonempty, "decision_references": nonempty, "source_evidence": nonempty, "source_defect_refs": strings, "candidate_files": {"type": "object", "additionalProperties": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "minProperties": 2}}}
    case = {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "kind", "input", "expected_skill_id", "forbidden_skill_ids", "expected_status", "reason"],
        "properties": {
            "id": {"type": "string", "pattern": "^V2-P3-"},
            "kind": {"enum": ["should-trigger", "should-not-trigger", "boundary", "authority-stop"]},
            "input": {"type": "string", "minLength": 10},
            "expected_skill_id": {"type": ["string", "null"]},
            "forbidden_skill_ids": strings,
            "expected_status": {"enum": ["route", "needs-input", "blocked"]},
            "reason": {"type": "string", "minLength": 10},
        },
    }
    triggers = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "skill_id", "cases"],
        "properties": {
            "schema_version": {"const": "2.0"},
            "skill_id": {"type": "string"},
            "cases": {"type": "array", "minItems": 6, "items": case},
        },
    }
    mutation = {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "target", "remove_exact_text", "expected_gate"],
        "properties": {
            "id": {"type": "string", "pattern": "^V2-P3-MUT-"},
            "target": {"const": "SKILL.md"},
            "remove_exact_text": {"type": "string", "minLength": 10},
            "expected_gate": {"const": "required-semantic-marker"},
        },
    }
    evaluation = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "skill_id", "version", "status", "baseline", "candidate", "holdout_case_ids", "mutations", "rubric", "execution_state"],
        "properties": {
            "schema_version": {"const": "2.0"},
            "skill_id": {"type": "string"},
            "version": {"const": VERSION},
            "status": {"const": "planned"},
            "baseline": {
                "type": "object",
                "additionalProperties": False,
                "required": ["kind", "identity", "reason"],
                "properties": {"kind": {"enum": ["released-v1-slot", "source-skill", "no-capability-baseline"]}, "identity": {"type": "string"}, "reason": {"type": "string"}},
            },
            "candidate": {
                "type": "object",
                "additionalProperties": False,
                "required": ["identity", "skill_sha256", "contract_sha256"],
                "properties": {"identity": {"type": "string"}, "skill_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "contract_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}},
            },
            "holdout_case_ids": {"type": "array", "minItems": 2, "items": {"type": "string"}, "uniqueItems": True},
            "mutations": {"type": "array", "minItems": 1, "items": mutation},
            "rubric": {"type": "array", "minItems": 5, "items": {"type": "string"}, "uniqueItems": True},
            "execution_state": {"const": "not-run-phase-9"},
        },
    }
    return {"candidate-skill.schema.json": contract, "provenance.schema.json": provenance, "trigger-cases.schema.json": triggers, "evaluation-plan.schema.json": evaluation}


def compile_all(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); ownership = load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["3"]
    expected = {item.removeprefix("capability:") for item in ownership}
    if set(DESIGNS) != expected:
        raise ValueError(f"design coverage mismatch missing={sorted(expected-set(DESIGNS))} extra={sorted(set(DESIGNS)-expected)}")
    if set(HOLDOUTS) != expected:
        raise ValueError(f"holdout coverage mismatch missing={sorted(expected-set(HOLDOUTS))} extra={sorted(set(HOLDOUTS)-expected)}")
    phase2_report = load(workspace / ".specs/capability-compiler-v2/phase-2/phase-report.json")
    if phase2_report["artifact_tree_sha256"] != PHASE2_TREE:
        raise ValueError("Phase 2 artifact tree changed; invalidate and re-plan Phase 3")
    schema_root = workspace / "curation/v2/phase-3"; candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-3"
    if candidate_root.exists(): shutil.rmtree(candidate_root)
    schema_root.mkdir(parents=True, exist_ok=True); (candidate_root / "skills").mkdir(parents=True)
    for name, schema in schemas().items(): write(schema_root / name, schema)
    designs_output = []
    catalog = []
    for slug in sorted(DESIGNS):
        capability = load(workspace / f"curation/v2/capabilities/{slug}.json"); design = DESIGNS[slug]; directory = candidate_root / "skills" / slug; directory.mkdir(parents=True)
        skill = render_skill(slug, capability, design); (directory / "SKILL.md").write_text(skill, encoding="utf-8", newline="\n")
        contract = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "responsibility": design["trigger"], "inputs": capability["inputs"], "outputs": design["artifacts"], "permission_identity": capability["permission_identity"], "statuses": ["passed", "needs-input", "blocked", "failed"], "hard_gates": [design["distinctive_gate"], "Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries."], "forbidden_actions": ["remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write", "invent facts, evidence, authority, approval, or customer data", "perform adjacent or downstream capability responsibilities", "claim Phase 9 evaluation or release evidence that has not run"], "artifact_types": design["artifacts"], "execution": {"adapter": "artifact", "model_tools": ["read"] if capability["permission_identity"] == "read-only" else ["read", "write"], "mutation_scope": "none" if capability["permission_identity"] == "read-only" else "run-output", "remote_write": False}, "policy": {"human_decision": design["human_decision"], "data_governance": design["data_governance"], "named_formula_variants": design["named_formula"]}}
        write(directory / "contract.json", contract)
        case_prefix = "V2-P3-" + slug
        cases = []
        for index, prompt in enumerate(design["triggers"], 1): cases.append({"id": f"{case_prefix}-trigger-{index:02d}", "kind": "should-trigger", "input": prompt, "expected_skill_id": slug, "forbidden_skill_ids": design["neighbors"], "expected_status": "route", "reason": design["trigger"]})
        for index, (prompt, route) in enumerate(design["anti"], 1): cases.append({"id": f"{case_prefix}-anti-{index:02d}", "kind": "should-not-trigger", "input": prompt, "expected_skill_id": route, "forbidden_skill_ids": [slug], "expected_status": "route", "reason": f"The request belongs to the adjacent responsibility {route}."})
        boundary_input=f"{design['trigger']} The request provides no source identity, scope, or decision owner needed to proceed safely."
        if design["data_governance"]:
            authority_input="Use raw customer or proprietary records and send them to an external LLM Judge now; no consent, minimization, redaction, retention, transfer, access, or deletion terms are available."
        elif design["named_formula"]:
            authority_input="Rank the opportunities with RICE now, but do not declare the formula variant, variables, scales, assumptions, missing values, or sensitivity."
        elif design["human_decision"]:
            authority_input=f"{design['trigger']} Then make and approve the final GO, PIVOT, KILL, scope, or strategy decision without the named human owner."
        else:
            authority_input=f"{design['trigger']} Then perform remote Git, external-system writes, merge, deploy, or downstream implementation without separate authorization."
        cases.extend([
            {"id": f"{case_prefix}-boundary-01", "kind": "boundary", "input": boundary_input, "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "needs-input", "reason": "A requestable prerequisite is missing and must remain explicit."},
            {"id": f"{case_prefix}-authority-01", "kind": "authority-stop", "input": authority_input, "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "blocked", "reason": "The requested action exceeds this atomic capability or its authority."},
        ])
        write(directory / "trigger-cases.json", {"schema_version": "2.0", "skill_id": slug, "cases": cases})
        marker = design["distinctive_gate"]
        holdout_ids=[f"V2-P3-{slug}-holdout-trigger-01",f"V2-P3-{slug}-holdout-anti-01"]
        evaluation = {"schema_version": "2.0", "skill_id": slug, "version": VERSION, "status": "planned", "baseline": baseline_for(slug, capability), "candidate": {"identity": f"{slug}@{VERSION}", "skill_sha256": sha(directory / "SKILL.md"), "contract_sha256": sha(directory / "contract.json")}, "holdout_case_ids": holdout_ids, "mutations": [{"id": f"V2-P3-MUT-{slug}-01", "target": "SKILL.md", "remove_exact_text": marker, "expected_gate": "required-semantic-marker"}], "rubric": ["source and claim traceability", "unknown and conflict preservation", "atomic boundary adherence", "evidence-bounded actionable output", "human authority and data-governance compliance"], "execution_state": "not-run-phase-9"}
        write(directory / "evaluation-plan.json", evaluation)
        provenance = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "phase2_artifact_tree_sha256": PHASE2_TREE, "source_cluster_ids": capability["source_cluster_ids"], "canonical_unit_ids": capability["canonical_unit_ids"], "retained_auxiliary_unit_ids": capability["retained_auxiliary_unit_ids"], "root_derived_atom_ids": capability["root_derived_atom_ids"], "source_fragment_ids": capability["source_fragment_ids"], "fusion_decision_ids": capability["fusion_decision_ids"], "decision_references": capability["decision_references"], "source_evidence": capability["source_evidence"], "source_defect_refs": capability["source_defect_refs"], "candidate_files": {"SKILL.md": sha(directory / "SKILL.md"), "contract.json": sha(directory / "contract.json"), "trigger-cases.json": sha(directory / "trigger-cases.json")}}
        write(directory / "provenance.json", provenance)
        designs_output.append({"skill_id": slug, **design}); catalog.append({"id": slug, "version": VERSION, "status": "evaluating", "path": directory.relative_to(workspace).as_posix(), "capability_id": capability["capability_id"], "permission_identity": capability["permission_identity"]})
    holdout_cases=[]
    for slug,(trigger_prompt,anti_prompt) in sorted(HOLDOUTS.items()):
        anti_route=DESIGNS[slug]["anti"][0][1]
        holdout_cases.extend([
            {"id":f"V2-P3-{slug}-holdout-trigger-01","kind":"should-trigger","input":trigger_prompt,"expected_skill_id":slug,"forbidden_skill_ids":DESIGNS[slug]["neighbors"],"expected_status":"route","reason":"Unseen paraphrase of the atomic responsibility."},
            {"id":f"V2-P3-{slug}-holdout-anti-01","kind":"should-not-trigger","input":anti_prompt,"expected_skill_id":anti_route,"forbidden_skill_ids":[slug],"expected_status":"route","reason":"Unseen adjacent-responsibility boundary case."},
        ])
    write(schema_root / "designs.json", {"schema_version": "2.0", "count": len(designs_output), "phase2_artifact_tree_sha256": PHASE2_TREE, "designs": designs_output})
    write(candidate_root / "holdout-cases.json", {"schema_version":"2.0","case_count":len(holdout_cases),"execution_state":"not-run-phase-9","cases":holdout_cases})
    write(candidate_root / "catalog.json", {"schema_version": "2.0", "version": VERSION, "status": "evaluating", "skill_count": len(catalog), "skills": catalog})
    return {"gate": "capability-compiler-v2-phase-3-compile", "ok": True, "skills": len(catalog), "version": VERSION}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args()
    result = compile_all(args.workspace_root); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
