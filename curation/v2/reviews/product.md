# Capability Compiler V2 — Phase 1B Product Capability Audit

## Scope and method

This audit covers the 14 assigned skill roots only. Each assigned `SKILL.md` was read in full. Every local file found directly beneath each assigned root was classified and, where semantically relevant, read in full. No old dossier was used as evidence. No network source, remote Git operation, script, test, merge, deployment, or repository write was invoked.

The governing contract requires root-level dossiers to cover triggers, responsibilities, inputs/outputs, methods, dependencies, permissions, strengths, weaknesses, failure modes, reusable-unit candidates, and parent/child relationships; it also requires every support file to receive a concrete `semantic-read`, `behavior-reviewed`, or `excluded` disposition (`.specs/capability-compiler-v2/phase-1/phase-plan.md:20-44`). The coverage ledger identifies 139 roots and 2,337 source files and distinguishes semantic-review, behavior-review, and excluded files (`curation/v2/coverage.json:1-13`). No assigned root contains a nested skill root.

Disposition meanings used here:

- **semantic-read** — prose, template, example, or code-in-document that contributes methods, rules, outputs, or evidence.
- **behavior-reviewed** — executable behavior-bearing script or program reviewed as behavior.
- **excluded** — binary, generated/vendor fixture, or irrelevant implementation internal, with reason.
- There are **no executable scripts, binary assets, generated/vendor files, or test fixtures** in the assigned roots. Code blocks inside `llm-evaluation` are documentation examples, not repository-executable scripts.

---

## 1. `ai-product-strategy`

### Exact root and skill path

- Root: `skills/ai-product-strategy/`
- Skill: `skills/ai-product-strategy/SKILL.md`

### Semantic dossier

- **Trigger:** Use when deciding where AI creates real product value, selecting an AI architecture, calibrating autonomy, or seeking defensibility in an AI product. The skill frames its purpose as prioritizing high-impact workflows while managing non-determinism and long-term defensibility (`skills/ai-product-strategy/SKILL.md:1-16`).
- **Non-trigger:** Not a detailed implementation guide, model benchmark, prompt-writing procedure, or production evaluation harness. It does not design a specific model pipeline or execute experiments.
- **Responsibility:** Identify an AI wedge, choose broadly between RAG and fine-tuning, stage autonomy, and align product design with expected model improvement (`skills/ai-product-strategy/SKILL.md:10-16`).
- **Non-responsibility:** Engineering architecture beyond high-level selection; legal/privacy review; quantitative evaluation design; model procurement; implementation.
- **Inputs:** User problem/workflow, live-data needs, desired model behavior, current data advantage, acceptable failure modes, and likely future model capability. Its questions explicitly solicit friction, architecture needs, probabilistic UX, platform obsolescence risk, proprietary data, and learning-loop metabolism (`skills/ai-product-strategy/SKILL.md:72-79`).
- **Outputs:** Strategic recommendations concerning wedge, architecture, human control, data defensibility, verticalization, and roadmap posture. The support catalog adds agency-ladder, CC/CD, product-rigor, prompt-selection, and defensibility artifacts (`skills/ai-product-strategy/references/artifacts.md:1-214`, `skills/ai-product-strategy/references/artifacts.md:589-800`).
- **Core workflow:**  
  1. Find a recurring high-friction chore.  
  2. Decide whether dynamic knowledge suggests RAG or specialized behavior suggests fine-tuning.  
  3. Begin with constrained, human-reviewed agency.  
  4. Collect interaction data and strengthen the learning loop.  
  5. Build around vertical workflow/data advantages.  
  6. Avoid scaffolding whose only value is compensating for temporary model limits.
- **Branches:** RAG versus fine-tuning; augmentation versus replacement; low-, medium-, or high-agency versions; build versus buy; horizontal foundation capability versus vertical application; current-model optimization versus future-capability posture.
- **Rules, gates, and stop conditions:** Do not add AI without a validated user problem; design for imperfect output; increase agency only after behavioral evidence; do not treat temporary scaffolding as the moat; proprietary/licensed data and workflow fit outrank model access (`skills/ai-product-strategy/SKILL.md:18-69`, `skills/ai-product-strategy/SKILL.md:81-88`). The detailed CC/CD framework adds explicit reference data, eval, controlled deployment, behavior review, and graduation criteria (`skills/ai-product-strategy/references/artifacts.md:157-205`).
- **Tools/dependencies:** Foundation models, RAG, fine-tuning, prompt engineering, evaluation data, logging, human review, and potentially external model providers. No repository executable dependency exists.
- **Permissions/side effects:** Advisory by default. Applying it may initiate prototypes, pilots, data collection, or limited deployments. Those actions require separate privacy, security, cost, and operational authorization; the skill itself grants none.
- **Strongest unique methods:**  
  - “Promise-to-payoff” wedge selection around frequent chores.  
  - An agency/control ladder tied to earned evidence.  
  - “Products as living organisms,” emphasizing learning-loop metabolism.  
  - Differentiation hierarchy of proprietary data, workflow/interface, then model.  
  - Explicit warning that base-model advances may erase scaffolding.  
  These are elaborated with worked agency progressions and CC/CD patterns in the artifact catalog (`skills/ai-product-strategy/references/artifacts.md:86-205`, `skills/ai-product-strategy/references/artifacts.md:620-685`).
- **Weaknesses/failure modes:**  
  - The root skill compresses a large, sometimes conditional corpus into four steps without a decision record or scoring rubric.
  - “Build for future models” can conflict with present safety, reliability, and customer evidence unless treated as a bounded hypothesis rather than license to ship unreliable behavior.
  - The RAG/fine-tuning split omits combinations and other adaptation methods.
  - Several supporting guest records have blank insights, so source volume is not equivalent to usable evidence (`skills/ai-product-strategy/references/guest-insights.md:63-68`, `skills/ai-product-strategy/references/guest-insights.md:96-101`).
  - Generic adoption may produce an AI feature strategy without task-specific evals, security analysis, or economics.
- **Overlap/duplicate/dependency candidates:**  
  - Strong dependency on `llm-evaluation` for eval design and regression gates.
  - Complements `competitive-strategy` on defensibility and `analyzing-user-feedback` on learning signals.
  - Depends on discovery skills before declaring a wedge validated.
  - Its experiment and metrics material overlaps `craft-experiment-design` and `craft-experiment-readout`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/ai-product-strategy/SKILL.md` | semantic-read | Root trigger, principles, questions, mistakes, and high-level workflow. |
| `skills/ai-product-strategy/references/artifacts.md` | semantic-read | Full framework, checklist, template, example, and tool catalog; supplies methods omitted from the root summary. |
| `skills/ai-product-strategy/references/guest-insights.md` | semantic-read | Source-derived claims, quotations, tactical advice, and provenance; reviewed as evidence rather than accepted by dossier inheritance. |

---

## 2. `analyzing-user-feedback`

### Exact root and skill path

- Root: `skills/analyzing-user-feedback/`
- Skill: `skills/analyzing-user-feedback/SKILL.md`

### Semantic dossier

- **Trigger:** Use when synthesizing qualitative and quantitative feedback, determining representativeness, creating dogfooding practices, or using LLMs to cluster large feedback corpora (`skills/analyzing-user-feedback/SKILL.md:1-16`).
- **Non-trigger:** Not a customer-interview script, survey-design guide, statistical inference procedure, or automatic prioritization engine.
- **Responsibility:** Categorize signals, test whether feedback represents a meaningful population, create direct product-immersion practices, and scale synthesis with AI.
- **Non-responsibility:** Decide product strategy from feedback alone; let users design solutions; replace direct access to raw signals; validate quantitative causal claims.
- **Inputs:** Support tickets, interviews, reviews, surveys, analytics, user identity/segment, influence, frequency, product journeys, and internal dogfooding observations.
- **Outputs:** Themes, representation/influence assessments, friction logs, prioritized feedback, trust signals, and dogfooding or AI-clustering process recommendations.
- **Core workflow:**  
  1. Aggregate diverse channels without erasing provenance.  
  2. Cluster by theme and segment.  
  3. assess representation and influence.  
  4. Compare breadth and depth of effect.  
  5. Immerse teams in real workflows.  
  6. Prioritize action and close the loop with users.
- **Branches:** Broad representative issue versus influential niche issue; deep/few versus shallow/many effect; AI clustering versus manual review; service participation versus product dogfooding; act, monitor, explain deferral, or reject.
- **Rules, gates, and stop conditions:** Loudness is not representativeness; audits should initially prohibit solutioning; AI-generated reports should retain links to raw customer evidence; feedback closure matters; distinguish access demand from demonstrated value (`skills/analyzing-user-feedback/SKILL.md:18-63`, `skills/analyzing-user-feedback/SKILL.md:75-82`). The support file formalizes representation × influence and depth × breadth matrices (`skills/analyzing-user-feedback/references/artifacts.md:28-91`).
- **Tools/dependencies:** Feedback hubs, Slack/Notion/Coda, CRM context, support feeds, analytics, LLM clustering, advisory councils, friction logs, and trust surveys. These are suggested systems, not installed dependencies.
- **Permissions/side effects:** May ingest customer conversations into AI tools, require employees to use a service, contact users, or create tickets. Privacy, consent, retention, employee safety, and access controls are external gates.
- **Strongest unique methods:** Representation × influence; depth × breadth; Trust Vault; “Study Group” no-solution empathy rule; direct immersion/dogfooding; preserving source links during AI root-cause classification (`skills/analyzing-user-feedback/references/artifacts.md:28-118`, `skills/analyzing-user-feedback/references/artifacts.md:188-245`).
- **Weaknesses/failure modes:**  
  - The root summary does not prescribe an output schema, sampling log, deduplication rule, or confidence notation.
  - Frequency can be mistaken for prevalence when channels have different selection biases.
  - Influence weighting can privilege powerful users over harmed but less visible groups.
  - LLM clustering can blur raw evidence; the references explicitly warn to retain original conversations.
  - Mandatory dogfooding may be impractical or unsafe for some services and requires an alternative.
- **Overlap/duplicate/dependency candidates:**  
  - Direct upstream evidence source for `discovery-process`, `prd-development`, and `product-strategy-session`.
  - Complements `interview-script`; does not duplicate interview conduct.
  - Depends on `validate-data` when quantitative prevalence or trend claims are made.
  - Its prioritization matrices overlap, but are not identical to, `prioritization-frameworks`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/analyzing-user-feedback/SKILL.md` | semantic-read | Defines synthesis, representativeness, immersion, AI use, questions, and common mistakes. |
| `skills/analyzing-user-feedback/references/artifacts.md` | semantic-read | Detailed matrices, dogfooding processes, trust measures, examples, and operational tools. |
| `skills/analyzing-user-feedback/references/guest-insights.md` | semantic-read | Primary semantic evidence for feedback operations and stated limitations; includes some blank/N/A records that were not treated as substantive support. |

---

## 3. `competitive-strategy`

### Exact root and skill path

- Root: `skills/competitive-strategy/`
- Skill: `skills/competitive-strategy/SKILL.md`

### Semantic dossier

- **Trigger:** Use when defining the real competitive set, auditing durable advantage, evaluating incumbent vulnerability, or choosing cost leadership versus differentiation (`skills/competitive-strategy/SKILL.md:1-16`).
- **Non-trigger:** Not a feature-comparison-only exercise, market-sizing calculator, pricing implementation, or guarantee that a proposed moat is durable.
- **Responsibility:** Reframe competition from customer context, identify structural power, expose switching costs, and choose a coherent winning path.
- **Non-responsibility:** Produce live competitive intelligence without supplied/current research; execute acquisitions; determine legal antitrust posture; substitute for customer interviews.
- **Inputs:** Customer alternatives, job context, incumbent business model, buyer/user frustration, switching frictions, company strengths, market lifecycle, pricing/cost position, and competitor moves.
- **Outputs:** Demand-side competitor set, moat/power hypothesis, incumbent vulnerability assessment, cost-versus-differentiation choice, and candidate asymmetries.
- **Core workflow:**  
  1. Ask what customers would use if the product vanished.  
  2. Separate direct competitors from substitutes/comparables.  
  3. Identify structural benefit and barrier.  
  4. Test whether competitors cannot or will not copy.  
  5. Inspect true switching costs and buyer/user frustration.  
  6. Choose low cost or differentiated activity system.  
  7. Concentrate effort on a vulnerable target.
- **Branches:** Supply-side versus demand-side competition; “can’t copy” versus “won’t copy”; startup-stage counter-positioning versus later network/scale/switching power; match an industry primitive versus differentiate; low cost versus uniqueness.
- **Rules, gates, and stop conditions:** Do not mistake growth or UI quality for power; do not copy visible features without underlying context; early startups should not rely on mature brand/process power; avoid markets where neither buyer nor user is frustrated; avoid being “stuck in the middle” (`skills/competitive-strategy/SKILL.md:18-74`, `skills/competitive-strategy/SKILL.md:88-95`). The support catalog’s benefit-plus-barrier and vulnerability tests make these gates more explicit (`skills/competitive-strategy/references/artifacts.md:34-52`, `skills/competitive-strategy/references/artifacts.md:143-174`).
- **Tools/dependencies:** Customer interviews, competitive/comparable research, feature deconstructs, pricing history, Wayback Machine, SWOT/wargaming, and market data.
- **Permissions/side effects:** Mostly analysis. Live market research may use external sites; strategic recommendations may affect investment or positioning but no action is authorized by the skill.
- **Strongest unique methods:** Demand-side competition; true switching-cost assessment including politics and career stakes; Power Progression; benefit-plus-barrier moat test; can’t-versus-won’t copying; magnifying-glass model of power, focus, and vulnerable target (`skills/competitive-strategy/references/artifacts.md:34-52`, `skills/competitive-strategy/references/artifacts.md:69-82`, `skills/competitive-strategy/references/artifacts.md:143-174`).
- **Weaknesses/failure modes:**  
  - No standard final artifact or evidence-confidence field.
  - “Adopt industry primitives” and “differentiate” are compatible only when the primitive is explicitly classified as table stakes; the root leaves this conditionality implicit.
  - Competitive research can become reactive feature matching, which the source itself warns against.
  - Broad moat language risks relabeling ordinary execution as structural power unless the benefit and barrier are separately evidenced.
- **Overlap/duplicate/dependency candidates:**  
  - Complements `ai-product-strategy` on AI defensibility.
  - Feeds strategic context in `prd-development` and positioning in `product-strategy-session`.
  - Depends on interviews and feedback synthesis for demand-side alternatives and true switching costs.
  - Overlaps prioritization only at strategic choice level, not backlog scoring.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/competitive-strategy/SKILL.md` | semantic-read | Root strategic trigger, principles, questions, and anti-patterns. |
| `skills/competitive-strategy/references/artifacts.md` | semantic-read | Detailed power, switching-cost, disruption, positioning, checklist, example, and research-tool methods. |
| `skills/competitive-strategy/references/guest-insights.md` | semantic-read | Source-specific claims and tactical evidence; blank insight records were not treated as proof. |

---

## 4. `craft-experiment-design`

### Exact root and skill path

- Root: `skills/craft-experiment-design/`
- Skill: `skills/craft-experiment-design/SKILL.md`

### Semantic dossier

- **Trigger:** Designing an A/B test, experiment plan, hypothesis, launch holdout, audience allocation, or metric set (`skills/craft-experiment-design/SKILL.md:1-11`).
- **Non-trigger:** Reading completed results, validating SQL, designing qualitative discovery, or implementing experiment infrastructure.
- **Responsibility:** Turn a proposed change into a reviewable experiment brief.
- **Non-responsibility:** Calculate sample size from raw traffic and effect assumptions, implement randomization, validate telemetry, or guarantee causal validity.
- **Inputs:** Proposed change and rationale; ideally baseline rates, traffic, prior tests, and product context (`skills/craft-experiment-design/SKILL.md:16-46`).
- **Outputs:** Falsifiable hypothesis, primary/secondary/guardrail metrics, audience and allocation, holdout recommendation, duration estimate, assumptions, and risks.
- **Core workflow:** Parse context; formulate “If change, then outcome, because rationale”; choose one decision metric; add secondary and guardrail metrics; define population/allocation; decide holdout; estimate duration; state bias and implementation risks.
- **Branches:** Empty input means ask for change and rationale; persistent holdout versus no holdout; full eligible audience versus scoped segment; equal versus unequal allocation.
- **Rules, gates, and stop conditions:** One primary metric; guardrails must not degrade; duration/allocation claims must expose assumptions; data and engineering assumptions should be called out (`skills/craft-experiment-design/SKILL.md:20-43`).
- **Tools/dependencies:** Analytics baselines, experimentation platform, engineering instrumentation, and data-science review.
- **Permissions/side effects:** The skill drafts a plan only. Launching a test changes user exposure and needs product, engineering, privacy, and risk approval.
- **Strongest unique methods:** Compact experiment-plan contract combining decision metric, guardrails, allocation, holdout, duration, and bias review.
- **Weaknesses/failure modes:**  
  - No explicit MDE, power, alpha, sample-ratio mismatch, novelty effect, contamination, sequential-testing, or multiple-testing checks.
  - A duration “estimate” can become invented precision if baseline traffic and variance are absent.
  - No explicit pre-registration or stop-rule field.
- **Overlap/duplicate/dependency candidates:** Upstream of `craft-experiment-readout`; specialized child capability of discovery and strategy workflows; should pair with `validate-data` for instrumentation and analysis QA.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/craft-experiment-design/SKILL.md` | semantic-read | Entire root consists of the experiment brief contract and guidance. No other support files exist. |

---

## 5. `craft-experiment-readout`

### Exact root and skill path

- Root: `skills/craft-experiment-readout/`
- Skill: `skills/craft-experiment-readout/SKILL.md`

### Semantic dossier

- **Trigger:** A completed experiment with results requiring a winner/inconclusive call, ship/iterate/kill recommendation, or stakeholder communication (`skills/craft-experiment-readout/SKILL.md:1-12`).
- **Non-trigger:** Experiment design before launch, raw SQL verification, or causal analysis without experiment metadata/results.
- **Responsibility:** Convert supplied results into an accessible decision memo and tailored stakeholder message.
- **Non-responsibility:** Independently reproduce calculations, retrieve missing telemetry, repair randomization, or infer significance from incomplete data.
- **Inputs:** Hypothesis, variants, metrics, sample sizes, confidence intervals, duration, audience, segments, and intended communication audience (`skills/craft-experiment-readout/SKILL.md:17-48`).
- **Outputs:** Summary, hypothesis recap, numeric results, significance interpretation, winner or inconclusive finding, segment analysis, recommendation, learnings, TL;DR, impact, owners, and timelines.
- **Core workflow:** Restate test; report actual numbers; separate statistical from practical significance; inspect segment heterogeneity; call winner or inconclusive; recommend ship/iterate/kill; tailor communication.
- **Branches:** Winner versus inconclusive; ship versus iterate versus kill; leadership versus engineering/company-wide message; aggregate versus segment-specific result.
- **Rules, gates, and stop conditions:** Do not force a winner from ambiguous evidence; use plain language; make action clear to skimmers; state actual metrics and significance (`skills/craft-experiment-readout/SKILL.md:29-55`).
- **Tools/dependencies:** Supplied analytics screenshots/tables, experiment report, and audience context.
- **Permissions/side effects:** Drafts communication only. A “ship” recommendation does not itself authorize deployment.
- **Strongest unique methods:** Joins analytical readout with a second, audience-specific communication artifact in one concise contract.
- **Weaknesses/failure modes:**  
  - No mandatory checks for sample-ratio mismatch, pre-test metric definitions, stopping-rule violations, novelty, contamination, or multiple comparisons.
  - “Segment analysis” can encourage post-hoc slicing unless pre-specified or labeled exploratory.
  - The skill may repeat incorrect input calculations because independent verification is not required.
- **Overlap/duplicate/dependency candidates:** Direct successor to `craft-experiment-design`; depends on `validate-data` for calculation/method QA; experiment evidence may feed `discovery-process`, `prd-development`, or `product-strategy-session`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/craft-experiment-readout/SKILL.md` | semantic-read | Entire root defines results interpretation and stakeholder communication. No other support files exist. |

---

## 6. `discovery-process`

### Exact root and skill path

- Root: `skills/discovery-process/`
- Skill: `skills/discovery-process/SKILL.md`

### Semantic dossier

- **Trigger:** A team needs a full problem-to-validated-solution discovery cycle, especially for new opportunities, churn/retention investigation, or continuous discovery (`skills/discovery-process/SKILL.md:1-20`, `skills/discovery-process/SKILL.md:67-78`).
- **Non-trigger:** Well-understood execution, tactical bugs, technical debt, or a situation where stakeholders have irrevocably committed to a solution before alignment is repaired (`skills/discovery-process/SKILL.md:79-83`).
- **Responsibility:** Orchestrate framing, research planning, interviews, synthesis, opportunity generation, experiments, and go/pivot/kill decision.
- **Non-responsibility:** Replace delivery, run as waterfall research, or produce detailed implementation requirements before validation.
- **Inputs:** Rough problem hypothesis; optional prior research, customer access, timeline, and decision context. Existing invocation context must be reused rather than re-asked (`skills/discovery-process/SKILL.md:27-38`).
- **Outputs:** Problem hypothesis, research questions, interview guide/roster, transcripts/notes, thematic clusters, prioritized pains, solution options, experiment results, decision, epic hypotheses, and optionally a PRD (`skills/discovery-process/SKILL.md:122-132`, `skills/discovery-process/SKILL.md:211-219`, `skills/discovery-process/SKILL.md:262-274`, `skills/discovery-process/SKILL.md:308-360`).
- **Core workflow:** Six phases: frame; plan research; conduct research; synthesize; generate/validate solutions; decide/document. The root provides timelines, participants, outputs, and component-skill delegation for each phase (`skills/discovery-process/SKILL.md:101-360`).
- **Branches:**  
  - Insufficient framing context leads to existing-data review.  
  - Unclear segment/JTBD adds proto-persona or JTBD work.  
  - No saturation adds interviews.  
  - Journey-spanning pain adds journey mapping.  
  - OST versus Lean UX Canvas.  
  - Invalidated solution pivots and reruns experiments.  
  - Final GO, PIVOT, or KILL.
- **Rules, gates, and stop conditions:** Interview consent; focus on past behavior; saturation is recurring pain across at least three interviews with no new insight; choose the least work that answers the next uncertainty; do not proceed to build without problem, solution, strategic-fit, and feasibility checks (`skills/discovery-process/SKILL.md:137-230`, `skills/discovery-process/SKILL.md:276-360`).
- **Tools/dependencies:** `workshop-facilitation`, problem framing, problem statement, proto-persona, JTBD, discovery interview prep, journey mapping, OST or Lean UX Canvas, epic hypothesis, and PRD development (`skills/discovery-process/SKILL.md:85-99`, `skills/discovery-process/SKILL.md:461-506`).
- **Permissions/side effects:** Recruiting and compensating participants, recording interviews with consent, handling transcripts, conducting prototype/fake-door/A/B tests, and presenting decisions all have real operational and privacy effects.
- **Strongest unique methods:** End-to-end decision gates; explicit saturation branch; frequency × intensity × strategic-fit pain scoring; “least work to learn the next most important thing”; GO/PIVOT/KILL completion.
- **Weaknesses/failure modes:**  
  - Fixed “5–10 interviews” and simple saturation heuristics can overstate generalizability.
  - The root says always interview 5–10 even when existing evidence is strong; the life-sciences example more appropriately shows an existing query killing the initial hypothesis before interviews (`skills/discovery-process/SKILL.md:411-419`; `skills/discovery-process/examples/sample-lifesciences.md:18-35`).
  - Fake-door and customer research activities need explicit ethical/privacy review not encoded as a general gate.
  - The workflow is long and can become ceremony; its own time-box warning partly mitigates this (`skills/discovery-process/SKILL.md:435-451`).
- **Overlap/duplicate/dependency candidates:**  
  - Parent/orchestrator of `interview-script`-like interviewing, experiment design, synthesis, and PRD.
  - Strong overlap with the middle phases of `product-strategy-session`; discovery is narrower and more evidence-focused.
  - Feeds `prd-development`.
  - `analyzing-user-feedback` is a synthesis complement, not a replacement.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/discovery-process/SKILL.md` | semantic-read | Complete six-phase workflow, gates, dependencies, pitfalls, and timing. |
| `skills/discovery-process/template.md` | semantic-read | Fill-in summary contract for framing, evidence, opportunities, experiments, decision, and next steps. |
| `skills/discovery-process/examples/sample.md` | semantic-read | Positive and negative SaaS examples showing intended gate behavior. |
| `skills/discovery-process/examples/sample-lifesciences.md` | semantic-read | Domain variant covering scarce access, ethics, regulatory consequences, non-randomized validation, and explicit evidence limits. |

---

## 7. `interview-script`

### Exact root and skill path

- Root: `skills/interview-script/`
- Skill: `skills/interview-script/SKILL.md`

### Semantic dossier

- **Trigger:** Preparing a customer interview guide or discovery interview focused on JTBD, real past behavior, pains, alternatives, and willingness to invest (`skills/interview-script/SKILL.md:1-15`).
- **Non-trigger:** Interview recruitment, sample-size planning, research synthesis, survey creation, usability testing, or solution pitching.
- **Responsibility:** Produce a customized, timed interview script and note-taking template using Mom Test principles.
- **Non-responsibility:** Conduct the interview, secure participants, analyze a cohort, or validate a product idea from one conversation.
- **Inputs:** Research topic, objectives, decisions to inform, assumptions, persona, interview duration, and supplied briefs/personas/notes.
- **Outputs:** Opening, warm-up, JTBD exploration, probes, wrap-up, and structured notes (`skills/interview-script/SKILL.md:17-105`).
- **Core workflow:** Clarify objectives; set learning/consent expectations; establish role/context; ask about the last concrete occurrence; follow tools, actors, sequence, pain, workarounds, outcomes, and current investment; probe specifics; close with omissions and referrals.
- **Branches:** Adapt questions by persona, domain, objective, and time; follow an interesting thread with repeated “why,” examples, sequence, or emotion probes.
- **Rules, gates, and stop conditions:** Ask about life and past behavior, not the product idea or hypothetical future; listen approximately 80%; never pitch; treat compliments as noise; obtain recording permission (`skills/interview-script/SKILL.md:67-86`).
- **Tools/dependencies:** Supplied research artifacts, recording system if consented, markdown output, and human interviewer.
- **Permissions/side effects:** May handle personal data and recordings. Consent is explicitly required for recording; storage, retention, and deletion rules remain external.
- **Strongest unique methods:** Timed script architecture, past-event JTBD questioning, probing ladder, 80/20 listening rule, and concise structured notes.
- **Weaknesses/failure modes:**  
  - “Magic wand” and “what would you give up” are hypothetical prompts and sit uneasily beside the strict past-behavior rule (`skills/interview-script/SKILL.md:47-59`, `skills/interview-script/SKILL.md:73-76`).
  - “Why?” repeated several times can feel interrogative unless adapted carefully.
  - No recruitment/sampling, accessibility, safeguarding, privacy-retention, or analysis protocol.
- **Overlap/duplicate/dependency candidates:** Component of `discovery-process`; evidence source for `analyzing-user-feedback`; complements rather than duplicates strategy and PRD workflows.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/interview-script/SKILL.md` | semantic-read | Complete script method and note template. No other support files exist. |

---

## 8. `llm-evaluation`

### Exact root and skill path

- Root: `skills/llm-evaluation/`
- Skill: `skills/llm-evaluation/SKILL.md`

### Semantic dossier

- **Trigger:** Building or reviewing systematic LLM application evaluation, model/prompt comparison, regressions, benchmarks, baselines, or unexpected behavior (`skills/llm-evaluation/SKILL.md:1-19`).
- **Non-trigger:** General product strategy, a one-off subjective “vibe check,” production observability by itself, or generic experiment communication.
- **Responsibility:** Explain automated, human, and LLM-judge evaluation approaches and provide implementation patterns.
- **Non-responsibility:** Supply a ready-to-run package, choose task-specific thresholds without context, guarantee judge validity, or deploy evaluation infrastructure.
- **Inputs:** Model callable, test cases, expected answers/context, task type, metrics, human annotations, baselines, comparison variants, and benchmark data.
- **Outputs:** Aggregate/raw metric scores, human rating forms, inter-rater agreement, judge scores, A/B summaries, regression flags, and benchmark distributions.
- **Core workflow:** Choose evaluation modality; assemble test set; run predictions; calculate task metrics; use human or LLM judgment for qualitative dimensions; compare variants; detect regressions; retain raw scores and summaries.
- **Branches:** Generation/classification/retrieval metrics; human versus automated versus judge; pointwise/pairwise/reference-based/reference-free; benchmark versus regression; standard metric versus custom metric (`skills/llm-evaluation/SKILL.md:21-71`).
- **Rules, gates, and stop conditions:** Match metrics to task; retain raw scores; use human evaluation for qualities hard to automate; establish baselines before regression checks. The reference supplies significance and threshold examples, though not a unified release gate (`skills/llm-evaluation/references/details.md:1-338`).
- **Tools/dependencies:** Examples import NumPy, NLTK, `rouge_score`, `bert_score`, Transformers, Detoxify, Anthropic SDK, Pydantic, scikit-learn, SciPy, and LangSmith (`skills/llm-evaluation/references/details.md:1-338`). None are declared in the repository’s `pyproject.toml`, which only contains pytest configuration (`pyproject.toml:1-3`).
- **Permissions/side effects:** Example judge calls transmit prompts/responses to Anthropic; Transformer examples may download models; LangSmith examples create datasets/examples and run hosted evaluations. These require credentials, network, privacy approval, cost control, and data-governance review.
- **Strongest unique methods:** Broad multimodal evaluation taxonomy; pointwise/pairwise/reference judge patterns; inter-rater agreement; baseline-relative regression detector; benchmark distribution reporting.
- **Weaknesses/failure modes:**  
  - The root Quick Start is not runnable as written: `calculate_accuracy`, `calculate_bleu`, `calculate_bertscore`, and `check_groundedness` are not defined there (`skills/llm-evaluation/SKILL.md:73-125`).
  - The detailed `calculate_bleu(reference, hypothesis)` signature does not match the Quick Start call using `prediction=...`, causing an unexpected keyword/missing argument failure if directly combined (`skills/llm-evaluation/SKILL.md:96-103`; `skills/llm-evaluation/references/details.md:5-17`).
  - Examples rely on many undeclared dependencies and external services.
  - The A/B helper chooses the larger mean as “winner” regardless of statistical significance, despite separately calculating a p-value (`skills/llm-evaluation/references/details.md:221-275`).
  - Regression relative-change calculations divide by the baseline without guarding a zero baseline (`skills/llm-evaluation/references/details.md:278-326`).
  - No treatment of judge position bias, self-preference, calibration, leakage, prompt injection, or repeated-run variance.
- **Overlap/duplicate/dependency candidates:**  
  - Required downstream partner for `ai-product-strategy`.
  - Complements `craft-experiment-design/readout`; LLM eval measures task quality while experiment skills measure product/user outcomes.
  - `validate-data` should QA metric computation and conclusions.
  - Code examples are implementation patterns, not behavior-bearing repository scripts.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/llm-evaluation/SKILL.md` | semantic-read | Evaluation taxonomy and Quick Start API sketch. |
| `skills/llm-evaluation/references/details.md` | semantic-read | Documentation containing implementation patterns and worked code examples; reviewed semantically and for behavioral implications, but it is not an executable repository script. |

---

## 9. `outcome-roadmap`

### Exact root and skill path

- Root: `skills/outcome-roadmap/`
- Skill: `skills/outcome-roadmap/SKILL.md`

### Semantic dossier

- **Trigger:** Converting a feature/project roadmap into measurable customer and business outcomes, or making roadmap intent more strategic (`skills/outcome-roadmap/SKILL.md:1-14`).
- **Non-trigger:** Selecting strategy from scratch, estimating delivery capacity, prioritizing an unsorted backlog, or committing release dates.
- **Responsibility:** Reveal the reason behind each planned output, rewrite it as an outcome, attach metrics, and preserve strategic alignment and flexible timing.
- **Non-responsibility:** Validate whether the proposed outcome is achievable, prove causality, or select implementation solutions.
- **Inputs:** Current roadmap, initiatives, customer problems, business metrics, strategy documents, objectives, assumptions, dependencies, and sequencing.
- **Outputs:** Original-to-outcome mapping, outcome statements, key metrics, dependencies/sequencing, strategic context, assumptions, and quarter/phase windows (`skills/outcome-roadmap/SKILL.md:16-62`).
- **Core workflow:** Read roadmap; repeatedly ask “so what?”; identify feature/output; uncover customer and business change; rewrite as “Enable [segment] to [outcome] so that [business impact]”; attach metrics and flexible windows.
- **Branches:** Supplied strategy versus external context research; one output per outcome versus multiple outputs serving one outcome; retain, combine, or reframe initiatives.
- **Rules, gates, and stop conditions:** Outcomes must be testable/measurable; do not lock implementation to one feature; prefer quarters over exact dates; if an outcome cannot be articulated, continue probing rather than merely renaming the feature (`skills/outcome-roadmap/SKILL.md:24-69`).
- **Tools/dependencies:** Roadmap and strategy documents; optional web search; markdown output.
- **Permissions/side effects:** May instruct web search and save `Outcome-Roadmap-[year].md` (`skills/outcome-roadmap/SKILL.md:16-18`, `skills/outcome-roadmap/SKILL.md:58-62`). Those are side effects requiring runtime authorization; none occurred in this audit.
- **Strongest unique methods:** Simple output-to-outcome rewrite formula plus explicit customer and business effects, metrics, and flexible windows.
- **Weaknesses/failure modes:**  
  - A rewritten sentence can remain a feature disguised as an outcome.
  - Example targets such as “50% faster” can invite unsupported numbers if baselines are absent.
  - No explicit assumption/open-question tagging or validation gate.
  - Web research can silently introduce uncited or stale strategic context.
- **Overlap/duplicate/dependency candidates:** Complements `product-strategy-session`; depends on validated problems and prioritization; its metric claims should be checked with `validate-data`; can consume PRD and experiment evidence.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/outcome-roadmap/SKILL.md` | semantic-read | Complete transformation method, output contract, and side-effect instructions. No other support files exist. |

---

## 10. `prd-development`

### Exact root and skill path

- Root: `skills/prd-development/`
- Skill: `skills/prd-development/SKILL.md`

### Semantic dossier

- **Trigger:** Creating an engineering-ready PRD for a major feature or initiative from discovery notes, research, metrics, and constraints (`skills/prd-development/SKILL.md:1-20`).
- **Non-trigger:** Small bug fixes, trivial features, already-aligned work needing only stories, or continuous-discovery experiments better served by Lean UX Canvas (`skills/prd-development/SKILL.md:103-117`).
- **Responsibility:** Build a living alignment document connecting problem, users, strategic context, solution, success metrics, stories, scope, risks, and open questions.
- **Non-responsibility:** Pixel-level design, frozen waterfall specification, or replacement for cross-functional collaboration.
- **Inputs:** Initiative, discovery evidence, problem statement, personas/JTBD, strategy/OKRs, proposed solution, metrics, constraints, dependencies, risks, and existing context (`skills/prd-development/SKILL.md:27-38`).
- **Outputs:** Ten-section PRD, inline assumptions/open questions, acceptance criteria, out-of-scope boundaries, risk/mitigation entries, and self-assessment (`skills/prd-development/SKILL.md:41-89`, `skills/prd-development/SKILL.md:133-150`; `skills/prd-development/template.md:1-72`).
- **Core workflow:** Draft summary; evidence-backed problem; users/personas; strategy and why now; high-level solution; primary/secondary/guardrail metrics; epic and user stories; exclusions; dependencies/risks; open questions; refine summary and self-assess.
- **Branches:** Empty-handed workflow versus supplied artifacts; optional journey/JTBD, TAM, competitive context, wireframes, and story map; straightforward versus complex timing; optional stakeholder review.
- **Rules, gates, and stop conditions:** Reuse supplied context; do not invent missing facts; tag gaps inline as assumption or open question; maintain one primary metric and at least one guardrail; keep design high-level; document explicit non-scope and unresolved decisions (`skills/prd-development/SKILL.md:27-38`, `skills/prd-development/SKILL.md:133-150`; `skills/prd-development/template.md:22-43`).
- **Tools/dependencies:** `workshop-facilitation`; problem statement/framing; proto-persona; JTBD; TAM calculator; story mapping; epic hypothesis; epic breakdown; user story; optional journey mapping and design tools (`skills/prd-development/SKILL.md:119-150`, `skills/prd-development/SKILL.md:626-674`).
- **Permissions/side effects:** Creates a durable PRD and may solicit stakeholder review, analytics baselines, and design/engineering work. It does not confer approval to build.
- **Strongest unique methods:** Inline assumption/open-question tags; per-section cross-consistency checks; explicit out-of-scope section; primary/secondary/guardrail metric structure; post-document self-assessment (`skills/prd-development/template.md:22-43`, `skills/prd-development/template.md:92-137`, `skills/prd-development/template.md:414-497`).
- **Weaknesses/failure modes:**  
  - The workflow is verbose and risks document ceremony for medium-sized work.
  - Writing the executive summary first can anchor the document around a premature solution, though the instruction to refine it last mitigates this (`skills/prd-development/SKILL.md:153-169`).
  - Many numeric examples look concrete and can be copied without evidence; the template’s tags are therefore essential.
  - The root says eight phases while the output has ten sections, which is coherent but easy to misread as incomplete phase coverage.
  - “Engineering-ready” may overpromise when architecture, non-functional requirements, security, compliance, migration, and operations are not universally required fields.
- **Overlap/duplicate/dependency candidates:**  
  - Downstream of `discovery-process`; final execution artifact within `product-strategy-session`.
  - Success metrics and risks overlap `craft-experiment-design` and `pre-mortem`.
  - Strategic context overlaps `competitive-strategy`.
  - Analysis evidence should be validated with `validate-data`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/prd-development/SKILL.md` | semantic-read | Full eight-phase facilitation workflow, orchestration links, timing, and pitfalls. |
| `skills/prd-development/template.md` | semantic-read | Authoritative fill-in PRD structure, assumption/open-question protocol, cross-section checks, and self-assessment. |
| `skills/prd-development/examples/sample.md` | semantic-read | Good/bad SaaS examples demonstrating evidence, tags, metrics, and failure patterns. |
| `skills/prd-development/examples/sample-industrial.md` | semantic-read | Industrial/hardware variant with regulatory gates, rollback, absolute guardrails, and physical-release constraints. |

---

## 11. `pre-mortem`

### Exact root and skill path

- Root: `skills/pre-mortem/`
- Skill: `skills/pre-mortem/SKILL.md`

### Semantic dossier

- **Trigger:** Stress-testing a PRD or launch plan shortly before launch, surfacing failure scenarios, and assigning mitigation for launch blockers (`skills/pre-mortem/SKILL.md:1-15`).
- **Non-trigger:** General backlog prioritization, post-incident analysis, detailed reliability testing, or risk discovery without a product/launch context.
- **Responsibility:** Imagine failure, classify risks, triage urgency, and create owner/date mitigation plans for blockers.
- **Non-responsibility:** Prove probability, execute mitigation, replace security/compliance review, or provide quantitative risk modeling.
- **Inputs:** PRD or launch plan, target market, assumptions, schedule, evidence, and cross-functional concerns.
- **Outputs:** Tigers, Paper Tigers, Elephants, urgency labels, and action plans with mitigation, owner, and due date (`skills/pre-mortem/SKILL.md:22-80`).
- **Core workflow:** Read plan; assume launch failure; work backward to causes; classify risk type; classify Tigers by launch-blocking/fast-follow/track; assign concrete blocker action.
- **Branches:** Tiger versus Paper Tiger versus Elephant; launch-blocking versus fast-follow versus track; investigate uncertain concerns or actively mitigate evidence-backed ones.
- **Rules, gates, and stop conditions:** Every launch-blocking Tiger needs concrete mitigation, owner, and completion date; involve engineering, design, and go-to-market; revisit before launch (`skills/pre-mortem/SKILL.md:47-86`).
- **Tools/dependencies:** PRD/launch plan, optional web research, cross-functional participants, markdown output.
- **Permissions/side effects:** May use web search and save `PreMortem-[product-name]-[date].md` (`skills/pre-mortem/SKILL.md:17-19`, `skills/pre-mortem/SKILL.md:80-82`). Its decisions can block launch, so governance/authority must be explicit outside the skill.
- **Strongest unique methods:** Memorable Tiger/Paper Tiger/Elephant taxonomy combined with urgency and owned launch-blocker actions.
- **Weaknesses/failure modes:**  
  - Internal rule conflict: an Elephant is defined as an uncertain concern deserving investigation, but the notes say “Default to Tiger if unsure” (`skills/pre-mortem/SKILL.md:39-45`, `skills/pre-mortem/SKILL.md:84-86`). This collapses the distinction and can inflate blocker lists.
  - No likelihood, impact, detectability, evidence-strength, or residual-risk scale.
  - Paper Tigers depend heavily on facilitator judgment and may dismiss stakeholder concerns without evidence.
- **Overlap/duplicate/dependency candidates:** Complements PRD risk sections; pre-launch counterpart to experiment guardrails; should feed roadmap gates and rely on specialist security/legal/reliability review where applicable.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/pre-mortem/SKILL.md` | semantic-read | Complete risk taxonomy, urgency method, action schema, and side-effect instructions. No other support files exist. |

---

## 12. `prioritization-frameworks`

### Exact root and skill path

- Root: `skills/prioritization-frameworks/`
- Skill: `skills/prioritization-frameworks/SKILL.md`

### Semantic dossier

- **Trigger:** Learning, selecting, or comparing prioritization frameworks such as Opportunity Score, ICE, RICE, Kano, MoSCoW, or weighted matrices (`skills/prioritization-frameworks/SKILL.md:1-8`).
- **Non-trigger:** A facilitated prioritization session requiring context gathering and recommendation, detailed portfolio optimization, or automatic backlog scoring.
- **Responsibility:** Provide formulas, intended use, and broad framework-selection guidance.
- **Non-responsibility:** Validate input estimates, resolve stakeholder conflict, determine strategy, or enforce a single framework.
- **Inputs:** Item type—problem, initiative, requirement, or personal task—plus importance, satisfaction, reach, impact, confidence, ease/effort, risk, and stakeholder criteria as applicable.
- **Outputs:** Framework choice guidance and resulting scores/categories.
- **Core workflow:** Prioritize problems before solutions; use Opportunity Score for needs; use ICE for quick idea ranking; RICE for reach/effort granularity; use the overview to select simpler matrices or requirement categories where appropriate.
- **Branches:** Problem versus initiative versus requirement versus personal task; quick triage versus granular scale; understanding expectations with Kano versus ranking; stakeholder-weighted decision matrix versus formulaic score.
- **Rules, gates, and stop conditions:** Normalize Opportunity Score inputs to 0–1; use higher score as priority for Opportunity/ICE/RICE; do not misuse Kano as a ranking formula; treat Impact/Effort as quick triage and MoSCoW cautiously (`skills/prioritization-frameworks/SKILL.md:9-66`).
- **Tools/dependencies:** Customer importance/satisfaction survey and linked external PDF/Google Slides/Sheets templates (`skills/prioritization-frameworks/SKILL.md:68-77`).
- **Permissions/side effects:** Reference-only locally. Following external template links would access third-party services; none were accessed.
- **Strongest unique methods:** Concise side-by-side framework taxonomy; clear distinction between opportunity/problem prioritization and solution/initiative scoring.
- **Weaknesses/failure modes:**  
  - No facilitated process for choosing among the nine methods despite the trigger promising selection help.
  - ICE uses 1–10 confidence/ease while RICE uses percentage confidence and person-month effort; scores are not comparable across methods.
  - Multiplicative scores magnify uncertain estimates and can create false precision.
  - Opportunity Score, ICE Impact, and RICE Impact use repository-specific definitions that should not be silently mixed with other organizations’ conventions.
  - No tie-break, sensitivity analysis, strategic-fit override, dependency handling, or confidence-evidence rubric.
- **Overlap/duplicate/dependency candidates:** Used by `product-strategy-session`; complements feedback depth/breadth and discovery pain scoring; feeds `outcome-roadmap` sequencing. It is a reference, whereas a prioritization-advisor skill would be the interactive selector.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/prioritization-frameworks/SKILL.md` | semantic-read | Complete formulas, comparison table, cautions, and external template references. No local support files exist. |

---

## 13. `product-strategy-session`

### Exact root and skill path

- Root: `skills/product-strategy-session/`
- Skill: `skills/product-strategy-session/SKILL.md`

### Semantic dossier

- **Trigger:** A team needs validated direction across positioning, problem framing, solution exploration, prioritization, roadmap, alignment, and initial execution planning (`skills/product-strategy-session/SKILL.md:1-20`).
- **Non-trigger:** Tactical feature additions, already-validated strategy, or work without executive sponsorship (`skills/product-strategy-session/SKILL.md:65-77`).
- **Responsibility:** Orchestrate a multi-week strategy arc from ambiguity to aligned, prioritized, executable direction.
- **Non-responsibility:** Replace each component skill’s detailed method, guarantee market validation, or act as a one-meeting brainstorm.
- **Inputs:** Product/product line, forcing strategic question, current positioning, discovery artifacts, roadmap drafts, stakeholders, and alignment deadline (`skills/product-strategy-session/SKILL.md:27-38`).
- **Outputs:** Positioning, personas/JTBD, validated problem, opportunity/solution options, epic hypotheses, ranked roadmap, stakeholder approval, stories, and first release plan.
- **Core workflow:** Six phases: positioning/context; problem framing/validation; solution exploration; prioritization/roadmap; stakeholder alignment; execution planning (`skills/product-strategy-session/SKILL.md:94-300`).
- **Branches:**  
  - Insufficient customer context adds interviews.  
  - Unvalidated problem adds discovery.  
  - OST versus Lean UX Canvas.  
  - High uncertainty adds experiments.  
  - Optional story map, TAM, press release.  
  - Supplied artifacts allow phases to be skipped.
- **Rules, gates, and stop conditions:** Require executive sponsorship; do not skip problem validation; do not run as solo PM work; adapt at decision points instead of blindly executing all phases; time-box and move to execution (`skills/product-strategy-session/SKILL.md:65-77`, `skills/product-strategy-session/SKILL.md:351-397`).
- **Tools/dependencies:** `workshop-facilitation`, positioning workshop, proto-persona, JTBD, problem framing/statement, discovery interview prep, journey mapping, OST/Lean UX, epic hypothesis, story mapping, prioritization advisor, TAM calculator, press release, epic breakdown, and user story (`skills/product-strategy-session/SKILL.md:79-92`, `skills/product-strategy-session/SKILL.md:399-443`).
- **Permissions/side effects:** Schedules workshops/interviews, runs customer experiments, presents to executives, ranks investments, and creates a sprint/release plan. These are organizational commitments, not merely document generation.
- **Strongest unique methods:** Comprehensive strategy-to-execution orchestration with explicit sponsorship requirement and uncertainty-driven decision points.
- **Weaknesses/failure modes:**  
  - It claims validated strategy but does not itself contain a full research conduct/synthesis phase; it delegates optional interviews and experiments.
  - Scope is very broad and can duplicate discovery, roadmap, and PRD workflows.
  - Execution planning at the end may prematurely convert a strategic session into delivery commitment if validation evidence remains weak.
  - The simple template does not preserve explicit assumptions, evidence citations, gates, or unresolved questions (`skills/product-strategy-session/template.md:1-26`).
- **Overlap/duplicate/dependency candidates:**  
  - Broad parent workflow containing much of `discovery-process`.
  - Consumes prioritization capability and can produce inputs to `outcome-roadmap` and `prd-development`.
  - Competitive strategy strengthens Phase 1 but is not explicitly orchestrated.
  - Experiments should delegate to experiment design/readout rather than use only generic POC instructions.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/product-strategy-session/SKILL.md` | semantic-read | Full six-phase strategy orchestration, gates, dependencies, timing, and pitfalls. |
| `skills/product-strategy-session/template.md` | semantic-read | Summary structure for context, customer, problem, opportunities, prioritization, roadmap, metrics, and next steps. |
| `skills/product-strategy-session/examples/sample.md` | semantic-read | Good/bad SaaS variants demonstrating discovery and solution-alternative expectations. |
| `skills/product-strategy-session/examples/sample-lifesciences.md` | semantic-read | Regulated-domain variant with internal opportunity cost, segment elimination, compliance gates, kill criterion, and bounded pilot. |

---

## 14. `validate-data`

### Exact root and skill path

- Root: `skills/validate-data/`
- Skill: `skills/validate-data/SKILL.md`

### Semantic dossier

- **Trigger:** QA of an analysis before stakeholder use, including methodology, calculations, SQL results, aggregations, charts, bias, and conclusion support (`skills/validate-data/SKILL.md:1-22`).
- **Non-trigger:** Producing an analysis from no data, writing a warehouse pipeline, running a formal statistical audit without source access, or validating an LLM’s task quality.
- **Responsibility:** Review question framing, data selection, population, definitions, comparisons, calculations, visualization, narrative, caveats, and reproducibility.
- **Non-responsibility:** Guarantee correctness when data/query access is missing; execute fixes; certify regulated analysis.
- **Inputs:** Report/document, file, notebook/spreadsheet, SQL plus results, charts with underlying data, or methodology/findings description (`skills/validate-data/SKILL.md:14-22`).
- **Outputs:** Three-level assessment, methodology review, severity-ranked issues, spot checks, visualization review, improvements, and stakeholder caveats (`skills/validate-data/SKILL.md:75-111`).
- **Core workflow:** Review assumptions; run QA checklist; inspect known pitfalls; independently spot-check calculations; inspect visualization; test narrative/conclusions; recommend improvements; assign confidence.
- **Branches:** Ready to share, share with caveats, or needs revision; visualization section only when charts exist; recalculation only where source data permits.
- **Rules, gates, and stop conditions:** Verify source freshness/completeness/nulls/deduplication/filters; verify grain, denominators, dates, joins, metrics, and totals; run magnitude/cross-reference/boundary checks; communicate limitations; preserve reproducibility (`skills/validate-data/SKILL.md:113-169`, `skills/validate-data/SKILL.md:251-364`).
- **Tools/dependencies:** Access to source tables/files, SQL, spreadsheet/notebook or calculator, known dashboards/finance records, and chart source data. `CONNECTORS.md` is referenced but lies outside the assigned root and was not required to understand this skill’s semantic method (`skills/validate-data/SKILL.md:9-10`).
- **Permissions/side effects:** Primarily read-only review. The documentation recommends version-control storage and sharing the validation report, but actual writes require separate authorization (`skills/validate-data/SKILL.md:344-364`, `skills/validate-data/SKILL.md:380-384`).
- **Strongest unique methods:** Comprehensive pre-delivery checklist; concrete join-explosion, survivorship, incomplete-period, denominator-shift, average-of-averages, timezone, and selection-bias catalog; cross-validation and red-flag heuristics.
- **Weaknesses/failure modes:**  
  - No explicit rule forbids “Ready to share” when source data or queries are unavailable; confidence must therefore distinguish inspected from merely asserted evidence.
  - “Bar charts start at zero” is framed as universal rather than contextual.
  - It does not prescribe formal statistical-test selection, uncertainty propagation, or experiment-specific checks such as sample-ratio mismatch.
  - “Use `COUNT(DISTINCT)`” can hide an erroneous join rather than fix its grain if applied mechanically (`skills/validate-data/SKILL.md:175-190`).
- **Overlap/duplicate/dependency candidates:**  
  - QA dependency for experiment readouts, roadmap metrics, PRD evidence, and feedback prevalence claims.
  - Complements `llm-evaluation`: this validates analysis methodology; that measures LLM behavior.
  - Complements `pre-mortem` by validating quantitative risk evidence, but is not a risk workshop.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/validate-data/SKILL.md` | semantic-read | Complete QA workflow, checklists, pitfalls, sanity methods, documentation standards, and examples. No local support files exist. |

---

# Cross-root relationship hypotheses

## Duplicate or near-duplicate capability candidates

1. **Problem framing and validation workflow duplication**
   - `discovery-process` and `product-strategy-session` both orchestrate problem framing, interviews when context is weak, OST/Lean UX alternatives, experiments, and decision gates.
   - Fusion hypothesis: retain `discovery-process` as the evidence-validation workflow; let `product-strategy-session` depend on it rather than restating abbreviated discovery logic.

2. **Success-metric structure duplication**
   - `craft-experiment-design`, `prd-development`, and `validate-data` all discuss primary, secondary, guardrail, baseline, and comparison quality.
   - Fusion hypothesis: canonical units should separate **metric design**, **experiment decision design**, and **analysis QA**, then reference them rather than duplicate them.

3. **Strategic defensibility overlap**
   - `ai-product-strategy` and `competitive-strategy` both discuss verticalization, proprietary data, switching costs/stickiness, incumbent exposure, and model commoditization.
   - Variant hypothesis: AI strategy is a conditional specialization of competitive strategy, adding non-determinism, model capability curves, data flywheels, evals, and agency control.

4. **Feedback prioritization overlap**
   - `analyzing-user-feedback` offers representation × influence and depth × breadth; `prioritization-frameworks` offers Opportunity Score, ICE, and RICE.
   - Complement hypothesis: the former qualifies evidence and constituency; the latter ranks validated problems or initiatives. They should not be merged into one undifferentiated score.

5. **Risk-section duplication**
   - `prd-development` contains dependency/risk/mitigation fields; `pre-mortem` specializes pre-launch risk discovery and urgency.
   - Dependency hypothesis: PRD risk section captures known risks continuously; pre-mortem is a later adversarial review that updates those fields.

## Complement hypotheses

1. `interview-script` produces structured raw evidence; `analyzing-user-feedback` synthesizes it; `discovery-process` decides whether evidence validates a problem.
2. `craft-experiment-design` defines the test; `validate-data` checks methodology/results; `craft-experiment-readout` communicates the decision.
3. `ai-product-strategy` chooses AI product posture; `llm-evaluation` supplies application-quality evidence; product experiments determine whether that quality creates user/business value.
4. `competitive-strategy` shapes strategic context; `product-strategy-session` aligns choices; `outcome-roadmap` expresses those choices as measurable intent; `prd-development` turns a chosen initiative into an execution artifact.
5. `pre-mortem` should consume a PRD and launch plan, while `validate-data` checks the quantitative claims used to classify risks.

## Conflict hypotheses requiring explicit V2 adjudication

1. **Uncertainty taxonomy conflict in `pre-mortem`:** “Elephant” means uncertain and needing investigation, while “default to Tiger if unsure” says uncertainty should become a real risk. Recommended adjudication: uncertainty stays Elephant until evidence supports Tiger; only high-consequence uncertainty may be provisionally launch-blocking.
2. **Future-model posture versus current reliability:** `ai-product-strategy` advises avoiding temporary scaffolding and building for future capability, while its safety/agency material requires gradual evidence. Recommended adjudication: future capability guides architecture, never current release gates.
3. **Industry primitives versus differentiation:** `competitive-strategy` advises adopting table-stakes primitives while also demanding a distinct race. Recommended adjudication: explicitly classify each element as table stakes, operational excellence, or differentiating activity.
4. **Past-behavior rule versus hypothetical interview prompts:** `interview-script` rejects future hypotheticals but includes “magic wand” and “what would you give up.” Recommended adjudication: retain those only as secondary probes after concrete past behavior, never as validation evidence.
5. **LLM A/B winner logic:** `llm-evaluation` labels the higher mean the winner even when its own p-value may be non-significant. Recommended adjudication: winner must be `inconclusive` unless a predeclared statistical/practical gate passes.
6. **Discovery sample rule versus domain constraints:** `discovery-process` says always interview 5–10, while its regulated-domain example demonstrates that existing data and constrained access can justify a different evidence plan. Recommended adjudication: require an evidence-sufficiency rationale, not a universal interview count.

## Conditional variants

- **SaaS versus regulated/physical domains:** The life-sciences and industrial examples add regulatory gates, ethical constraints, non-randomized validation, rollback, absolute stop conditions, and explicit kill criteria. These are meaningful domain variants, not illustrative decoration.
- **Qualitative versus quantitative validation:** Interviews and feedback synthesis explain behavior; experiments and data QA quantify effects. Neither should supersede the other without a stated reason.
- **Product outcome versus LLM quality:** Product experiments measure user/business outcomes; LLM evals measure system behavior. Both are required for AI products, but their metrics and release gates differ.
- **Reference versus workflow:** `prioritization-frameworks` is a static reference, while discovery, strategy, and PRD roots are orchestration workflows. V2 should not treat them as interchangeable skill shapes.

## Strong dependency candidates

1. `product-strategy-session` → `discovery-process` when customer/problem evidence is weak.
2. `discovery-process` → interview preparation/script, feedback synthesis, experiment design, and PRD development.
3. `prd-development` → validated discovery evidence; optionally competitive strategy and data validation.
4. `outcome-roadmap` → validated strategy and metrics.
5. `craft-experiment-readout` → experiment design metadata and data validation.
6. `ai-product-strategy` → LLM evaluation for model/application quality and experiment design for product impact.
7. `pre-mortem` → PRD/launch plan plus specialist reviews for security, legal, compliance, or reliability.
8. Every workflow root using guided conversation → `workshop-facilitation`, as explicitly declared in discovery, PRD, and strategy roots.

# Unresolved questions

1. Should V2 preserve `prioritization-frameworks` as a reference-only capability, or pair it with an interactive selector that gathers item type, evidence quality, uncertainty, dependencies, and strategic constraints?
2. Which exact calculation convention should be canonical for “Opportunity Score,” ICE Impact, and RICE Impact? The current root uses repository-specific definitions that may differ from users’ existing conventions.
3. Should experiment design/readout acquire mandatory fields for MDE, power, alpha, sample-ratio mismatch, stopping rule, novelty, contamination, and multiple testing, or should those live in a separate statistical experiment-analysis capability?
4. Should `llm-evaluation` remain conceptual documentation, or is runnable implementation intended? If runnable, dependency declaration, corrected call signatures, zero-baseline handling, inconclusive A/B outcomes, and tests are required.
5. What privacy/data-governance adapter governs customer transcripts, support tickets, proprietary data, and external LLM judge calls across feedback, discovery, AI strategy, and LLM evaluation?
6. Should external web research remain an implicit tool in `outcome-roadmap` and `pre-mortem`, or require a source-freshness/citation gate?
7. What evidence threshold distinguishes a validated problem from a hypothesis across `discovery-process`, `product-strategy-session`, and `prd-development`?
8. Should the Tiger/Paper Tiger/Elephant vocabulary be retained after resolving its uncertainty conflict, or replaced with evidence strength × impact × urgency fields?
9. Is `product-strategy-session` intended to produce an approved strategy, an evidence-backed recommendation, or merely a session summary? Its current language alternates among all three.
10. Should domain-specific regulated/hardware gates become reusable canonical units rather than remaining only in examples?
11. How should accessibility, vulnerable-participant safeguards, recording retention, and deletion be represented in the interview/discovery contract?
12. Should “save as markdown” instructions remain within individual skills, or be centralized as a platform output policy so semantic capabilities do not assume write permission?