from __future__ import annotations

try:
    from tools.curation.v2_phase7_design_common import D
except ModuleNotFoundError:
    from v2_phase7_design_common import D

DESIGNS = {
    "ai-organizational-adoption-and-leadership": D(
        "Create an evidence-bounded AI adoption and leadership plan with sponsors, pilot teams, capability building, measurable value, governance, and human decision gates without activating systems.",
        ["Design a bounded AI pilot adoption plan with sponsor, team, training, workflow change, value measures, and stop criteria.", "Prepare leadership decision material for whether and how to adopt this approved AI capability across one team."],
        [("Decide the AI capability, model, data, autonomy, and safety architecture.", "ai-capability-architecture-and-autonomy"), ("Configure production AI observability for the deployed system.", "ai-observability-configuration")],
        ["Freeze initiative and architecture status, user and business value hypotheses, teams, sponsors, current workflows, skills, governance, labor and change impacts, data boundaries, budget, risks, and decision owners.", "Select the smallest reversible pilot and define participants, enablement, process changes, support, communication, access, safeguards, and non-adoption option.", "Define measurable user, workflow, quality, cost, safety, trust, and organizational outcomes with baselines, review cadence, expansion and stop criteria.", "Return adoption plan, leadership options, ownership model, and unresolved risks for human approval; do not grant access, configure systems, enroll users, or expand autonomy."],
        ["AI adoption and pilot plan", "leadership decision material", "value and safety measurement contract", "ownership, enablement, and stop criteria"],
        "AI adoption cannot pass on enthusiasm or tool availability: it needs a reversible pilot, named sponsor and owners, workflow and labor impacts, measurable value and safety outcomes, governance, and stop criteria.",
        ["ai-capability-architecture-and-autonomy", "ai-agent-autonomy-and-human-control", "ai-observability-configuration", "feedback-and-continuous-learning-loop"],
        ["reversible-pilot", "sponsor-owner", "workflow-impact", "capability-building", "value-measures", "safety-governance", "stop-criteria"],
        ("Create a reversible one-team AI pilot with sponsor, workflow change, training, value and safety measures, and stop criteria.", "Select the model, retrieval, tools, autonomy, and safety architecture."),
        mutation_scope="run-output", human=True, data=True),
    "engineering-retrospective-and-improvement": D(
        "Conduct a blameless engineering retrospective from fresh delivery, repository, test, plan, and outcome evidence and propose owner-bound improvements without changing records or systems.",
        ["Run a blameless retrospective over this delivery window using repository history, test health, plan state, and outcomes.", "Identify technical-debt and process trends and propose small owner-bound improvement experiments."],
        [("Coordinate an active production incident and mitigation decisions.", "incident-response-coordination"), ("Persist an approved learning locally after validation.", "local-learning-persistence")],
        ["Freeze time window, teams, delivery and repository evidence, test and plan health, outcomes, incident records, prior actions, privacy, and participant boundaries.", "Build an evidence-linked timeline and distinguish observed fact, interpretation, systemic contributor, local decision, and unknown without blame or hindsight rewriting.", "Identify repeated strengths, friction, debt, coordination and tooling patterns, and compare prior improvement outcomes.", "Propose the smallest measurable improvement experiments with owner, due date, success signal, review date, and stop condition; do not edit history, assign blame, or persist automatically."],
        ["blameless retrospective", "evidence-linked trend and debt register", "small improvement experiments", "owner, deadline, metric, and review map"],
        "A retrospective cannot rewrite incident or delivery facts, assign personal blame, or create vague action items; every improvement needs evidence, owner, due date, measurable signal, and review condition.",
        ["incident-response-coordination", "feedback-and-continuous-learning-loop", "local-learning-persistence", "code-health-assessment"],
        ["blameless", "evidence-timeline", "fact-interpretation", "systemic-contributor", "owner-deadline", "measurable-improvement"],
        ("Review fresh delivery evidence blamelessly and propose small measurable owner-bound improvements.", "Coordinate the active incident and execute mitigation."),
        mutation_scope="none", human=True, data=True),
    "feedback-and-continuous-learning-loop": D(
        "Synthesize authorized runtime signals, customer feedback, experiment results, alerts, and residual assumptions into calibrated hypotheses, priorities, and the next learning cycle without collection or persistence.",
        ["Review the latest metrics, feedback, experiments, alerts, and assumptions and define the next learning cycle.", "Calibrate which hypotheses gained or lost confidence and route the next discovery, experiment, or reliability question."],
        [("Collect new customer interviews or proprietary feedback data.", "research-planning-and-governance"), ("Persist an approved learning record locally.", "local-learning-persistence")],
        ["Freeze review window, authorized inputs, source identities, metrics, feedback, experiment and incident evidence, assumptions, prior decisions, data governance, and decision owners.", "Normalize evidence strength and freshness while preserving dissent, minority evidence, causal uncertainty, missing data, and invalidated prior evidence.", "Update hypothesis confidence, opportunity or risk priority, decision thresholds, and unresolved questions without treating correlation as learning.", "Return learning record candidate, review cadence, next input and owner, and persistence handoff; do not collect data, persist, approve product changes, or configure systems."],
        ["calibrated hypothesis and learning record candidate", "evidence and uncertainty map", "priority and review cadence", "next discovery, experiment, reliability, or persistence handoff"],
        "Continuous learning must link each confidence or priority change to current authorized evidence and preserve contrary evidence; repeated opinion, stale metrics, or correlation alone is not learning.",
        ["research-planning-and-governance", "local-learning-persistence", "engineering-retrospective-and-improvement", "metrics-system-and-observability"],
        ["evidence-freshness", "hypothesis-calibration", "contrary-evidence", "causal-uncertainty", "review-cadence", "next-learning-input", "no-persistence"],
        ("Calibrate hypotheses from current authorized signals and define the next learning input without collecting or persisting data.", "Persist the approved learning record into the local project store."),
        mutation_scope="none", human=True, data=True),
    "incident-response-coordination": D(
        "Coordinate an active incident's severity, roles, timeline, hypotheses, mitigation options, communications, recovery criteria, and closure recommendation from read-only evidence without executing provider actions.",
        ["Coordinate this active incident using current impact evidence, assigning roles and maintaining a mitigation-first decision log.", "Structure severity, hypotheses, communications, escalation, recovery criteria, and specialist action handoffs without changing production."],
        [("Execute the approved release rollback.", "release-rollback-execution"), ("Perform the post-incident engineering retrospective after closure.", "engineering-retrospective-and-improvement")],
        ["Freeze incident identity, source and environment, start time, impact, affected users or services, current evidence, read-only provider scope, available specialist controls, safety boundaries, communication policy, and incident authority.", "Establish severity recommendation, incident lead, communications, operations and specialist owners, timeline, fact and hypothesis log, and decision cadence without provider acknowledgement or state change.", "Prioritize user and system safety, containment and reversible mitigation options; route exact actions to separately authorized rollback, deployment, infrastructure, or remediation owners.", "Track observed recovery against explicit criteria and recommend continue, escalate, rollback, recover, or close; preserve uncertainty and produce a closure record candidate without closing provider incidents."],
        ["incident coordination record", "roles, timeline, fact, hypothesis, and decision log", "mitigation and specialist action handoffs", "recovery evidence and closure recommendation"],
        "Coordination under external-read authority cannot acknowledge, silence, assign, comment, change traffic, scale, restart, deploy, rollback, remediate, or close provider incidents; every action routes to a separately authorized owner.",
        ["release-rollback-execution", "deployment-observation", "engineering-retrospective-and-improvement", "error-monitoring-issue-investigation"],
        ["severity", "roles", "timeline", "fact-hypothesis", "mitigation-first", "separate-action-owner", "no-provider-mutation", "closure-recommendation"],
        ("Coordinate severity, roles, timeline, reversible mitigation options, communications, and recovery criteria without provider mutation.", "Execute the approved rollback or close the provider incident."),
        mutation_scope="artifact-output", human=True, data=True),
    "local-learning-persistence": D(
        "Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.",
        ["Persist this approved source-linked learning to the local project store with retention and deletion metadata.", "Save one validated retrospective action and evidence record locally, returning its identity and hash."],
        [("Synthesize current signals into a learning recommendation first.", "feedback-and-continuous-learning-loop"), ("Synchronize learning records to an external service or another machine.", "project-context-and-learning-store")],
        ["Verify validated record and approval, project and local destination identity, source refs, evidence status, privacy class, minimization, retention, deletion, conflict policy, backup, rollback, and local-system authorization.", "Reject secrets, credentials, raw customer data beyond approval, unverified inference, unrelated project context, indefinite retention, and any external or cross-machine target.", "Write one normalized local record and metadata without changing the source evidence or promoting interpretation to fact.", "Validate read-back, record identity, hash where safe, provenance, retention, deletion path, conflict result, rollback, and explicit no-write or failure outcome."],
        ["persisted local learning identity", "source, evidence-status, and provenance metadata", "retention and deletion path", "read-back, hash, conflict, and rollback evidence"],
        "Local persistence accepts one validated approved record only; secrets, unverified inference, unrelated context, external synchronization, and indefinite retention are blocked.",
        ["feedback-and-continuous-learning-loop", "engineering-retrospective-and-improvement", "project-context-and-learning-store", "secrets-and-environment-governance"],
        ["one-validated-record", "local-only", "evidence-status", "provenance", "retention", "deletion", "read-back", "rollback"],
        ("Persist one approved evidence-linked learning locally with read-back, retention, deletion, and rollback evidence.", "Synthesize signals and decide what the learning should be."),
        mutation_scope="local-system-write", human=True, data=True, action=True),
}
