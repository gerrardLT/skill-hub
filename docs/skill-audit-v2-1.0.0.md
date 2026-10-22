# V2 1.0.0 原子 Skills 审核报告

> 只审不改：`slots/v2/1.0.0/` 与 `recipes/v2/1.0.0/` 未作任何修改（release tree `116651adca2b…`，Phase 12 Gate 复证）。逐项发现的证据与建议保留英文原文，便于对照文件行号。

## 结论

157 个 Skill 中：保留 53，改进 66，优先修订 34，合并 3，拆分 1。

整体看，这批 Skill 的边界、权限和 Gate 设计扎实（均分 2.9 以上），短板集中在两处：
- 来源保真偏低（均分 1.53/3）：来源里的具体技法、阈值、反模式在提纯时被抽象成了通用措辞。
- 实测增益有限：执行质量 A/B 中，带 Skill 的产出 99 胜 / 176 平 / 37 负（312 题，两种呈现顺序一致才计胜负）。

## 三层证据

| 层 | 方法 | 结果 |
|---|---|---|
| B 静态扫描 | 结构、模板化、契约一致、引用、重叠、溯源深度 | 见下方系统性问题 |
| C 语义审核 | 父级逐个读 SKILL/contract/provenance 与来源片段，8 维 0–3 分 | P1 92 条，P2 139 条 |
| D 执行 A/B | 每 Skill 2 道新题，gpt-5.6-sol 有/无 Skill 作答，claude-opus-5.5 双顺序盲评 | 1404 次调用，14,573,669 tokens |

8 维均分：边界 2.9，触发 2.62，程序 2.68，输出可验 2.48，Gate 2.97，权限 2.95，来源保真 1.53，实测 1.24。

## 执行 A/B 的规律

- 难题（含越权诱导、证据冲突、缺失授权）：66 胜 / 78 平 / 12 负。Skill 的治理与停止条件确实起作用。
- 常规题：33 胜 / 98 平 / 25 负。负的主因是：交付不够具体、在本可完成时返回 needs-input/blocked、漏掉具体发现。
- 评判两种顺序一致率 234/312，不一致的题一律记平。
- 每 Skill 只有 2 题、1 个评判模型，结论是方向性信号，不是统计结论。`browser-data-acquisition-runtime` 出题连续 4 次遇 provider 流中断，未实测。

## 系统性问题（影响全部或大部分 Skill）

1. Trigger 段逐字复述 Responsibility（157/157），没有提供额外的触发信号。
2. SKILL.md 未包含 contract 的 forbidden_actions（157/157），且多数缺第二条 hard gate（126/157）。模型只读 SKILL.md 时这些约束不可见。
3. 已发布的 contract 仍带发布前措辞 "claim ... released status"（93/157）。
4. Non-Responsibilities 引用了不存在的 Skill（6 个 Skill）：`provider-review-comment-response`、`schema-migration-safety`、`artifact-publication`、`pull-request-update`。
5. 高度相近却未互设 anti-trigger 的 Skill 对（4 对），如 playwright-test-engineering / vitest-tooling、ai-observability / log-observability。
6. 每个 Skill 恰好 2 条 anti-trigger、2 条 hard gate、4 项输出、4–5 步，Status Mapping 等段落 54–93 个 Skill 逐字共享。模板一致性好，但压掉了领域差异。
7. Phase 9 的 mutation 几乎测不出删改（存活 142，需行为挑战 14）；它只测路由决策，不测产出质量，本次 D 阶段补上了这一块。

## 跨 Skill 边界建议

- **ai-capability-architecture-and-autonomy, ai-model-and-data-architecture, ai-agent-autonomy-and-human-control, ai-safety-and-action-governance, ai-interaction-and-probabilistic-ux**：Five AI Skills; the router-only one adds a hop without design value. → Merge router-only Skill into ai-model-and-data-architecture; keep the other four.
- **web-hosting-deployment, edge-worker-deployment, kubernetes-application-deployment**：Three deploy Skills share an identical four-step skeleton; separation is justified by different failure modes but neither the shared skeleton nor the discriminator is stated. → Keep separate; add a one-line discriminator and mutual anti-triggers to each.
- **defect-remediation, ui-remediation, website-audit-remediation, developer-self-check-and-fix**：Four repair Skills share the same skeleton; separation is by finding origin and authority, which is sound but stated only partially. → Add one discriminator line per Skill: confirmed root cause / accepted UI finding / accepted audit finding / own in-scope patch.
- **local-learning-persistence, project-context-and-learning-store, local-agent-memory-setup**：Three local-memory Skills with overlapping vocabulary; split is write-one-record vs store setup vs agent memory setup but not stated in all three. → Add a shared three-way boundary sentence and mutual anti-triggers.
- **ai-observability-configuration, log-observability-configuration, release-observability-configuration, monitoring-and-alert-configuration**：Four provider-config Skills share an identical skeleton; separation is sound but discriminators are missing in two. → Add mutual anti-triggers keyed on signal type.
- **apm-onboarding-summary, apm-instrumentation-verification**：Summary has no independent method. → Merge.
- **frontend-rendering-and-interaction-performance, web-performance-diagnostics**：Both measure INP-adjacent interaction latency; ownership of INP is not stated. → Assign field INP to web-performance-diagnostics and component-level interaction traces to frontend-rendering-and-interaction-performance.
- **evidence-synthesis-and-opportunity-prioritization, opportunity-prioritization-and-frameworks**：Both rank opportunities. → Synthesis frames and compares; frameworks Skill alone ranks with a named formula.
- **results-analysis-and-decision-readout, evaluation-results-analysis, data-analysis-validation**：Three analysis Skills with partial anti-triggers. → Validation checks data; readout interprets product experiments; evaluation-results interprets model evals.
- **context-intake-and-routing, ui-task-routing-and-governance, workflow-orchestration-and-lifecycle**：Three routing-shaped Skills plus the V2 router; ownership of 'which capability next' is split four ways. → Router owns Recipe selection; context-intake owns cross-domain classification; ui-task-routing owns UI-only classification; orchestration only for uncovered workflows.
- **independent-plan-review, design-plan-review, developer-experience-plan-review, engineering-plan-review, executive-plan-review**：Five plan reviewers; boundaries are sound but only partially cross-referenced. → Add a shared reviewer-selection table referenced by all five.
- **playwright-test-engineering, vitest-tooling**：Highest lexical overlap in the catalog with no mutual anti-trigger. → Add mutual anti-triggers.
- **independent-code-review, code-review-evidence-acquisition**：Both reference a nonexistent provider-review-comment-response. → Point to pull-request-comment-response.
- **local-learning-persistence, project-context-and-learning-store, local-agent-memory-setup**：Write path duplicated. → Setup / write-one / read-maintain split.
- **document-rendering-and-validation, workflow-skill-authoring**：Both reference a nonexistent artifact-publication Skill. → Fix references.
- **cross-domain-ui-preflight-checklists, evidence-based-ui-review-and-release-gates, rendered-ui-critique-and-release-disposition**：Three Skills issue UI verdicts or dispositions. → Critique produces findings; release-gates owns disposition and absorbs preflight.

## 修订优先级

- 第一优先（合并/拆分/实测负向）（29）：`ai-capability-architecture-and-autonomy`、`apm-instrumentation-enablement`、`apm-instrumentation-verification`、`apm-onboarding-summary`、`architecture-candidate-reporting`、`change-packaging-and-versioning`、`completion-evidence-gate`、`cross-domain-ui-preflight-checklists`、`data-analysis-validation`、`deployment-observation`、`design-context-and-direction-contract`、`design-system-foundation-and-token-extraction`、`engineering-plan-review`、`evaluation-dataset-publication`、`evidence-synthesis-and-opportunity-prioritization`、`frontend-runtime-boundaries-and-dependency-safety`、`kubernetes-application-deployment`、`kubernetes-deployment-readiness`、`llm-experiment-execution`、`merge-and-deploy-readiness`、`observability-agent-installation`、`qualitative-evidence-synthesis`、`release-observability-configuration`、`remote-pull-request-merge`、`responsive-layout-and-spatial-composition`、`results-analysis-and-decision-readout`、`security-audit-and-threat-modeling`、`solution-hypothesis-and-experiment-design`、`ui-review-scope-and-evidence-acquisition`
- 第二优先（有 P1 问题或实测互有胜负）（66）：`agent-workflow-runtime-support`、`ai-agent-autonomy-and-human-control`、`ai-interaction-and-probabilistic-ux`、`ai-model-and-data-architecture`、`ai-observability-configuration`、`ai-organizational-adoption-and-leadership`、`ai-product-opportunity-and-wedge`、`architecture-interface-alternative-evaluation`、`browser-agent-pairing-provisioning`、`canary-baseline-management`、`cloud-reliability-assessment`、`code-health-assessment`、`code-review-evidence-acquisition`、`competitive-response-and-monitoring`、`context-intake-and-routing`、`customer-interview-execution`、`data-and-api-contract-design`、`deployment-environment-setup`、`deployment-trigger-execution`、`design-plan-review`、`developer-experience-plan-review`、`developer-self-check-and-fix`、`document-rendering-and-validation`、`documentation-authoring`、`edge-worker-deployment`、`engineering-retrospective-and-improvement`、`evidence-based-ui-review-and-release-gates`、`executive-plan-review`、`external-design-token-extraction-and-normalization`、`facilitation-and-collaboration-protocols`、`feedback-and-continuous-learning-loop`、`frontend-rendering-and-interaction-performance`、`git-destructive-command-guard`、`implementation-planning-and-handoff`、`incident-response-coordination`、`independent-code-review`、`local-branch-integration`、`local-git-guard-setup`、`local-learning-persistence`、`log-observability-configuration`、`metrics-system-and-observability`、`mobile-platform-runtime-support`、`monitoring-and-alert-configuration`、`opportunity-prioritization-and-frameworks`、`playwright-test-engineering`、`problem-framing-and-customer-research`、`production-canary-monitoring`、`production-trace-classification`、`project-context-and-learning-store`、`pull-request-comment-response`、`release-rollback-execution`、`remote-pull-request-change`、`rendered-ui-critique-and-release-disposition`、`resilience-and-determinism`、`root-cause-investigation`、`structural-power-and-moats`、`tdd-change-loop`、`test-case-design-and-export`、`ui-task-routing-and-governance`、`visual-language-and-anti-template-controls`、`vitest-tooling`、`web-hosting-deployment`、`web-performance-diagnostics`、`workflow-orchestration-and-lifecycle`、`workflow-runtime-upgrade`、`workflow-skill-authoring`
- 第三优先（仅 P2 问题）（9）：`architecture-deepening-discovery`、`change-delivery-preflight`、`document-and-artifact-governance`、`model-and-workflow-benchmarking`、`reference-library-and-deferred-material`、`release-documentation-maintenance`、`risk-preflight-and-safety-governance`、`source-metadata-and-provenance`、`ui-remediation`
- 保留（53）：`accessibility-contracts-and-assistive-validation`、`ai-safety-and-action-governance`、`apm-instrumentation-troubleshooting`、`architecture-deep-module-design`、`artifact-persistence-and-tool-actions`、`authorization-and-permission-contracts`、`baseline-regression-control`、`browser-agent-pairing-verification`、`browser-authentication-setup`、`browser-data-acquisition-runtime`、`browser-session-and-runtime-configuration`、`change-scope-freeze`、`ci-pipeline-security-hardening`、`competitive-case-library`、`content-copy-and-authentic-assets`、`decision-and-outcome-roadmapping`、`defect-remediation`、`developer-experience-assessment`、`diagram-and-architecture-artifact-generation`、`divergent-prototyping-and-variant-selection`、`error-monitoring-issue-investigation`、`evaluation-results-analysis`、`existing-interface-redesign-and-preservation`、`implementation-spec-compliance-review`、`independent-blackbox-qa`、`independent-plan-review`、`interaction-states-forms-and-navigation`、`isolated-task-implementation`、`llm-evaluator-engineering`、`llm-quality-evaluation`、`local-agent-memory-setup`、`market-positioning-and-competitive-power`、`market-segmentation-and-demand-intelligence`、`persona-jtbd-and-journey-modeling`、`plan-execution-control`、`plan-review-decision-synthesis`、`production-llm-trace-root-cause-analysis`、`provider-cli-authentication-setup`、`purposeful-motion-and-animation-engineering`、`qa-finding-triage`、`remote-git-push`、`requirements-and-delivery-contract`、`research-planning-and-governance`、`safe-browser-probing`、`secrets-and-environment-governance`、`service-identity-remapping`、`strategic-choice-and-differentiation`、`test-double-discipline`、`test-runtime-bootstrap`、`testing-portfolio-strategy`、`tool-runtime-readiness`、`website-audit-assessment`、`website-audit-remediation`

## 逐个 Skill 分析

图例：8 维分依次为 边界 / 触发 / 程序 / 输出可验 / Gate / 权限 / 来源保真 / 实测；A/B 列为 T1（常规）/ T2（难题）结果。

### architecture-data-api-and-security

#### `ai-agent-autonomy-and-human-control` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Decomposes agency into six graduated rights instead of one autonomy label.；Graduation and revocation require evidence thresholds.
- **P1 measured_efficacy**：Both holdouts tie; no measured lift over baseline. 建议：Phase D case requiring per-right preconditions and revocation triggers. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：The source's version-scoped agency ladder (v1/v2/v3 each with agency level, control mechanism and data flywheel) is not used to stage graduation. 建议：Express graduation as versioned rungs each naming its control and the data it collects. 证据：`skills/ai-product-strategy/references/artifacts.md:422-449`
- 来源中丢失的技法：versioned agency ladder with data flywheel

#### `ai-capability-architecture-and-autonomy` — 合并（目标：ai-model-and-data-architecture）

- 权限：`workspace-write`；8 维分 2/2/2/2/2/3/1/1（合计 15/24）；语义裁决 merge；执行 A/B 无增益（平 / 平）
- 优点：Keeps a non-AI fallback explicit.
- **P1 boundary**：A routing-only Skill that classifies AI needs and hands them to four specialists; its name says 'architecture and autonomy' but it designs neither. It duplicates intake routing and adds a hop. 建议：Fold the capability-classification step and non-AI fallback into ai-model-and-data-architecture step 1; route specialist questions via the stage Recipe. 证据：`slots/v2/1.0.0/skills/ai-capability-architecture-and-autonomy/SKILL.md:10,28-32`
- **P2 source_fidelity**：One source reference (a three-line summary). 建议：Covered by merge. 证据：`skills/ai-product-strategy/SKILL.md:14-17`

#### `ai-model-and-data-architecture` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/1/3（合计 21/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Data rights, lineage, freshness and rollback required before any recommendation.；Both holdouts are candidate wins.
- **P1 source_fidelity**：The core source decision, RAG for live or external context versus fine-tuning for consistent behavior, is not stated as a decision rule; nor is the prompt-technique selection guide. 建议：Add a technique decision table: prompt / RAG / fine-tune / tool by need (dynamic context vs behavior specialization). 证据：`skills/ai-product-strategy/references/guest-insights.md:334-343; skills/ai-product-strategy/references/artifacts.md:588-607; SKILL.md:29-31`
- 来源中丢失的技法：RAG vs fine-tuning decision rule；prompt technique selection guide

#### `ai-safety-and-action-governance` — 保留

- 权限：`read-only`；8 维分 3/2/3/2/3/3/2/1（合计 19/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Concrete abuse-path list (indirect injection, confused deputy, tool composition).；Default-deny for high-impact actions.
- **P2 source_fidelity**：Source states prompt injection cannot be fully solved; the Skill does not forbid claiming it is mitigated, so a report could overstate safety. 建议：Add: injection residual risk is always reported as non-zero; controls reduce impact, never eliminate it. 证据：`skills/ai-product-strategy/references/guest-insights.md:625-632`

#### `architecture-candidate-reporting` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Same criteria for all candidates; abstention allowed.
- **P2 source_fidelity**：Source report format (self-contained HTML, diagram pattern chosen per candidate: dependency graph, mass diagram, cross-section) is reduced to 'tables and cards'. 建议：Name the diagram pattern per candidate type as guidance. 证据：`skills/improve-codebase-architecture/HTML-REPORT.md:1-34,57-93`
- **P2 measured_efficacy**：Mutation needs behavioral challenge. 建议：Phase D case with unequal evidence across candidates. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：diagram pattern selection per candidate

#### `architecture-deep-module-design` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/2（合计 21/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Rejects boundaries based on file layout; challenges for shallow delegation.
- **P2 source_fidelity**：Testability rules (accept dependencies, return results instead of side effects) are not named. 建议：Add them to step 5 challenge list. 证据：`skills/codebase-design/SKILL.md:67-97`
- 来源中丢失的技法：accept dependencies, return results

#### `architecture-deepening-discovery` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/2/2（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：YAGNI and leave-unchanged are first-class.
- **P2 source_fidelity**：Source scopes the scan by recent change history ('walk back a good stretch of commits') before looking; the Skill freezes history but does not weight recent churn. 建议：Prioritize areas by recent change frequency when no direction is given. 证据：`skills/improve-codebase-architecture/SKILL.md:17-26`
- 来源中丢失的技法：recent-churn scoping before scan

#### `architecture-interface-alternative-evaluation` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Cosmetic signature variants explicitly rejected.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case scoring structural independence of alternatives. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source 'Design It Twice' uses 3+ independent generators each with a separate brief to force radical difference; the Skill asks for 'at least two' generated in one pass, which tends to produce variants. 建议：Default to three alternatives generated from independent briefs; two only when constrained. 证据：`skills/codebase-design/DESIGN-IT-TWICE.md:1-39`
- 来源中丢失的技法：3+ independent generators with separate briefs

#### `authorization-and-permission-contracts` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Negative case list (IDOR, confused deputy, stale role, bulk, export) is strong.；Authentication is not authorization.
- **P2 source_fidelity**：Only two source refs (attack-surface census, CI permissions); the content is largely authored. Quality is high, provenance is thin. 建议：Record as authored with OWASP ASVS access-control mapping. 证据：`curation/v2/skill-audit/static-scan.json`

#### `ci-pipeline-security-hardening` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Untrusted input tracing into expressions and privileged jobs; immutable pinning.
- **P2 source_fidelity**：The source's high-risk context list (issue/PR title and body, head_ref, comment body) and the pull_request_target danger are not enumerated. 建议：Add the attacker-controllable context list and flag pull_request_target with checkout of PR head. 证据：`skills/github-actions-hardening/SKILL.md:43-72`
- 来源中丢失的技法：attacker-controllable github context list；pull_request_target classification

#### `data-and-api-contract-design` — 改进

- 权限：`workspace-write`；8 维分 3/2/3/3/3/3/1/1（合计 19/24）；语义裁决 improve；执行 A/B 有效（胜 / 平）
- 优点：Expand-migrate-contract, idempotency and concurrency required.
- **P1 trigger_precision**：Non-Responsibilities references `schema-migration-safety`, which does not exist in the catalog. 建议：Remove or point to the actual owner (this Skill owns migration design; execution routes to tdd-change-loop). 证据：`slots/v2/1.0.0/skills/data-and-api-contract-design/SKILL.md:86`
- **P2 source_fidelity**：Source demands actual SQL and request/response shapes 'so the implementer makes zero design decisions'; the Skill asks for shapes but not concrete DDL and examples. 建议：Require concrete DDL or schema files and at least one request/response example per endpoint. 证据：`skills/gstack/spec/SKILL.md:714-718`
- 来源中丢失的技法：actual SQL and payloads, zero implementer design decisions

#### `engineering-plan-review` — 优先修订

- 权限：`read-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Every claim must trace to approved intent and an executable evidence path.
- **P1 source_fidelity**：Source Step 0 scope challenge (what existing code already solves each sub-problem; what is the minimum change) is absent; the Skill reviews the plan as given and cannot flag reinvention. 建议：Add step: for each sub-problem, cite existing code that already solves it or record none found. 证据：`skills/gstack/plan-eng-review/SKILL.md:667-706; SKILL.md:28-32`
- **P2 trigger_precision**：Overlap with independent-code-review and implementation-spec-compliance-review (0.216); the plan-vs-code distinction is implicit. 建议：Add anti-trigger: completed diff routes to independent-code-review. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：scope challenge against existing code

#### `frontend-runtime-boundaries-and-dependency-safety` — 拆分（目标：audit vs repair (repair to defect-remediation)）

- 权限：`workspace-write`；8 维分 2/3/2/2/3/2/1/3（合计 18/24）；语义裁决 split；执行 A/B 有效（胜 / 平）
- 优点：No server credential may cross into a client bundle.；Both holdouts are candidate wins.
- **P1 boundary**：Combines audit and repair in one identity ('audit and minimally repair'), contradicting the V2 review/repair separation decision applied everywhere else. 建议：Make it read-only audit; route accepted repairs to defect-remediation. 证据：`slots/v2/1.0.0/skills/frontend-runtime-boundaries-and-dependency-safety/SKILL.md:10,31`
- **P2 source_fidelity**：Sources are a design-taste stack default and a redesign checklist; RSC/client boundary rules ('use client' isolation, providers in client components) are cited but not stated. 建议：Add framework-variant rules for RSC client/server boundaries. 证据：`skills/design-taste-frontend/SKILL.md:122-159`
- 来源中丢失的技法：RSC interactivity isolation rules

#### `secrets-and-environment-governance` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/1/3（合计 22/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Value-free verification; leak-response order.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Specific leak paths from the source (set -x tracing, untrusted multiline data into $GITHUB_ENV/$GITHUB_OUTPUT) are not listed. 建议：Add them to the leak-path map examples. 证据：`skills/github-actions-hardening/SKILL.md:106-115`

#### `security-audit-and-threat-modeling` — 优先修订

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：STRIDE plus supply chain; one reproducible finding per problem with exploit preconditions.
- **P2 source_fidelity**：Source Phase 0 stack detection and Phase 1 attack-surface census (count endpoints, admin routes, webhooks, jobs) are not explicit; and source stance 'the real attack surface is your dependencies' is not prioritized. 建议：Add a census step with counts per surface category before tracing threats. 证据：`skills/gstack/cso/SKILL.md:407-446,493-532`
- 来源中丢失的技法：attack surface census with counts

### delivery-deployment-and-release

#### `change-delivery-preflight` — 改进

- 权限：`local-exec-external-read`；8 维分 3/3/2/2/3/3/1/3（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Both Phase 9 holdouts are candidate wins.；Readiness explicitly grants no packaging, push or PR authority.
- **P2 source_fidelity**：Source checks that the credential-redaction pre-push hook is installed (including custom core.hooksPath); the Skill only says 'secret indicators'. 建议：Add 'redaction pre-push hook present, honouring core.hooksPath' as a named check. 证据：`skills/ship/SKILL.md:955-985; slots/v2/1.0.0/skills/change-delivery-preflight/SKILL.md:29`
- **P2 source_fidelity**：Sibling-worktree and version-queue collision detection from the landing report is dropped. 建议：Add a check for other active branches claiming the same version slot. 证据：`skills/gstack/landing-report/SKILL.md:454-493`
- 来源中丢失的技法：pre-push redaction hook check；sibling worktree version-claim collision

#### `change-packaging-and-versioning` — 优先修订

- 权限：`workspace-write-local-exec`；8 维分 3/3/2/2/3/3/1/3（合计 20/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Bisectable commits and no-push boundary are explicit.；Both Phase 9 holdouts are candidate wins.
- **P1 source_fidelity**：Version-state classification before bumping (FRESH vs ALREADY_BUMPED vs needs repair) is absent, so repeated packaging can double-bump the version. 建议：Require classifying current version state against the base before any version write. 证据：`skills/gstack/ship/SKILL.md:706-745; SKILL.md:30`
- **P2 source_fidelity**：WIP-commit handling and the anti-footgun rule 'never destroy non-WIP commits; stop and ask when unsure' are dropped. 建议：Add WIP-only detection and a stop condition before any history rewrite. 证据：`skills/gstack/ship/SKILL.md:853-892`
- 来源中丢失的技法：version bump state classification；WIP-only branch soft reset with non-WIP preservation

#### `deployment-environment-setup` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/2/1/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 互有胜负（负 / 胜）
- 优点：Local-config-only boundary and teardown plan are explicit.
- **P1 source_fidelity**：Platform detection from repository files (fly.toml, vercel.json, netlify.toml, render.yaml, workflows) and per-platform URL/health/status inference are absent; step 2 says 'select from approved constraints' without detection. 建议：Add a detection table mapping config files to platform adapters and derived health/status commands. 证据：`skills/gstack/setup-deploy/SKILL.md:482-521; SKILL.md:29`
- **P1 output_verifiability**：Output 'local deployment configuration candidate' has no schema; the source defines a fixed deploy-configuration block (platform, production URL, workflow, status command, merge method, health check, hooks). 建议：Adopt that block as the required output schema consumed by readiness and trigger Skills. 证据：`skills/gstack/setup-deploy/SKILL.md:569-608; SKILL.md:36`
- 来源中丢失的技法：platform detection from config files；standard deploy configuration block

#### `deployment-trigger-execution` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/2/2/3/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：One-attempt authorization with receipt, request hash and cancellation path.
- **P1 procedure**：Auto-deploy-on-merge platforms (Vercel, Netlify) need no trigger; the Skill has no 'not applicable' path and may fabricate a trigger action. 建议：Add a first check: if the configured platform deploys automatically, return not-applicable and hand off to deployment-observation. 证据：`skills/gstack/land-and-deploy/SKILL.md:832-835; SKILL.md:28-31`
- **P2 source_fidelity**：Run identification by matching the merge commit SHA and preferring the detected deploy workflow name is dropped. 建议：Require the run receipt to bind to the exact head or merge SHA. 证据：`skills/gstack/land-and-deploy/SKILL.md:796-810`
- 来源中丢失的技法：auto-deploy platforms need no explicit trigger；match workflow run by merge SHA

#### `edge-worker-deployment` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Bindings by reference and wildcard-route block are domain-specific.
- **P1 source_fidelity**：Source warns that a successful dry run proves build and packaging only, not remote resources or runtime behaviour; the Skill treats preview as a gate without stating that limit. 建议：State that dry-run success does not validate bindings or runtime and require the health handoff to check them. 证据：`skills/wrangler/SKILL.md:46-52; SKILL.md:29`
- **P2 source_fidelity**：Regenerating binding types after config change instead of hand-editing generated declarations is dropped. 建议：Add type regeneration and typecheck to the local validation step. 证据：`skills/wrangler/SKILL.md:46-52`
- **P2 trigger_precision**：Overlap 0.348 with web-hosting-deployment; neither names the other as an anti-trigger. 建议：Add mutual anti-triggers keyed on 'edge runtime/bindings/routes' vs 'static or SSR hosting project'. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：dry run does not prove remote resources；regenerate types after binding changes

#### `kubernetes-application-deployment` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 improve；执行 A/B 负向（平 / 负）
- 优点：Server-side diff rejection of unexpected namespace, identity or immutable-field changes.；Readiness failure blocks apply.
- **P2 source_fidelity**：The source's deploy-failure catalog (DS001-DS013) and rollback reference are not mapped to stop conditions. 建议：Map known failure codes to stop and recovery actions in step 3. 证据：`skills/azure-kubernetes/azure-kubernetes-app-deploy/SKILL.md:10-34`
- 来源中丢失的技法：DS001-DS013 failure catalog

#### `merge-and-deploy-readiness` — 优先修订

- 权限：`local-exec-external-read`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：Separate merge and deploy verdicts.；Rejects stale, self-attested or waived evidence.；Both Phase 9 holdouts are candidate wins.
- **P2 source_fidelity**：First-run dry-run validation keyed on a deploy-config hash is dropped. 建议：Flag first run or changed deploy config as requiring a dry-run verdict. 证据：`skills/land-and-deploy/SKILL.md:665-694`
- 来源中丢失的技法：first-run confirmation keyed on deploy-config hash

#### `pull-request-comment-response` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/3/2/3/3/3/1/1（合计 19/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：One comment, no thread resolution, no source change.
- **P1 source_fidelity**：Line-level review comments and top-level conversation comments use different reply endpoints; the Skill does not distinguish them, so a reply can land on the wrong thread. 建议：Require classifying comment type and binding the reply target accordingly. 证据：`skills/gstack/review/greptile-triage.md:97-111; SKILL.md:30`
- 来源中丢失的技法：line-level vs top-level reply endpoints

#### `remote-git-push` — 保留

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Exact refspec, expected remote SHA, non-force default.；Both Phase 9 holdouts are candidate wins.
- **P2 source_fidelity**：Credential redaction pre-push hook check is generalized to 'secret checks'. 建议：Name the redaction hook check explicitly. 证据：`skills/gstack/ship/SKILL.md:955-963; SKILL.md:28`

#### `remote-pull-request-change` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/2/2/3/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Rejects auto-merge enabling and source changes.
- **P1 source_fidelity**：Source requires regenerating the PR body from this run's fresh results on update and never reusing stale body content; the Skill does not. 建议：Add a rule: updates replace the body from current evidence; stale sections are removed. 证据：`skills/gstack/ship/sections/pr-body.md:59-67`
- **P2 source_fidelity**：Redaction must scan both title and body at the sink and refuse when the scan cannot run. 建议：State scan-at-sink for title and body with refuse-on-scan-failure. 证据：`skills/gstack/ship/sections/pr-body.md:180-225`
- 来源中丢失的技法：regenerate PR body from scratch on update；redaction scan at sink, refuse if unscannable

#### `remote-pull-request-merge` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/2/3/3/3/1/3（合计 21/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Refresh-before-merge drift block.；Branch deletion requires separate authority, a deliberate tightening of the source.
- **P1 procedure**：Merge queues and auto-merge are not addressed: in queue-protected repositories a direct merge fails, and enqueueing is a different action with deferred result. 建议：Define queue entry as an allowed method returning 'queued' with a pending-result handoff, never a merged claim. 证据：`skills/gstack/land-and-deploy/sections/merge-and-deploy.md:1-145; SKILL.md:30`
- 来源中丢失的技法：auto-merge first, respecting merge queue

#### `web-hosting-deployment` — 改进

- 权限：`remote-write-authorized-only`；8 维分 2/2/2/3/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Exact project, environment, domain and rollback target.
- **P1 boundary**：Git-integrated hosting deploys by commit and push; the Skill does not say that this path must route to change-packaging and remote-git-push instead of being performed here. 建议：Add: when the provider deploys from Git, return a handoff to remote-git-push; this Skill covers CLI or API deploys only. 证据：`skills/deploy-to-vercel/SKILL.md:53-92; SKILL.md:30`
- **P2 source_fidelity**：Deploy method selection by link/remote state and the tarball fallback are dropped. 建议：Add a method-selection step with these states. 证据：`skills/deploy-to-vercel/SKILL.md:53-92,181-220`
- 来源中丢失的技法：deploy method selection by link and git state；tarball deploy fallback

### implementation-and-code-quality

#### `change-scope-freeze` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Separates required change, permitted incidental cleanup, prohibited expansion and unresolved prerequisite.；Emits scope and stops; no implementation.
- **P2 source_fidelity**：Source enforces the frozen directory by resolving to an absolute path with trailing slash so sibling prefixes do not match; the Skill's 'allowed files' has no path-normalization rule. 建议：Require allowed paths recorded as normalized absolute prefixes with trailing separator. 证据：`skills/gstack/freeze/SKILL.md:48-76; slots/v2/1.0.0/skills/change-scope-freeze/SKILL.md:28`
- 来源中丢失的技法：absolute path plus trailing slash to avoid prefix collision

#### `code-health-assessment` — 改进

- 权限：`read-only`；8 维分 3/3/2/1/3/3/1/2（合计 18/24）；语义裁决 improve；执行 A/B 有效（胜 / 平）
- 优点：Leave-unchanged rationale is explicit.；Both holdouts are candidate wins.
- **P1 source_fidelity**：Source defines a weighted, tool-backed rubric (type check 22%, lint 18%, tests 28%, dead code 13%, ...) with thresholds per score band and a dashboard; the Skill reduces this to qualitative 'signals'. Its gate also says 'aggregate scores alone do not justify remediation', which is fine, but no score is produced at all, so trend comparison is impossible. 建议：Produce the weighted category score from deterministic tool exits as one output, alongside cited findings. 证据：`skills/gstack/health/SKILL.md:510-549,559-598; SKILL.md:29,36-39`
- **P2 measured_efficacy**：Phase 9 mutation needs a behavioral challenge; the current case set cannot detect removal of the leave-unchanged rule. 建议：Add a case where remediation cost exceeds evidence and the expected output is leave-unchanged. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：weighted category rubric with tool exit thresholds；health dashboard with duration per tool

#### `defect-remediation` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Highest shared correction point; reproduction fails before and passes after.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Source requires checking out the exact release revision recorded on the error event, and stopping when stack frames do not match the repository; the Skill assumes the workspace matches. 建议：Add a revision-match check between evidence and workspace before patching. 证据：`skills/sentry-debug-issue/SKILL.md:128-141`
- 来源中丢失的技法：diff against the release revision on the event

#### `developer-self-check-and-fix` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/2/2/1/3/3/1/0（合计 15/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Cannot impersonate independent review.
- **P1 source_fidelity**：The source's concrete self-review questions (completeness vs spec, YAGNI, naming by intent, tests verify behavior not mocks) and the four-state report (DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT) are replaced by a generic category list. 建议：Embed the question checklist and require one of the four report states. 证据：`skills/subagent-driven-development/implementer-prompt.md:74-113; SKILL.md:29,36`
- **P1 measured_efficacy**：Both holdouts tie: baseline routing already succeeds; no evidence the Skill improves self-review quality. 建议：Measure in phase D with a seeded-defect patch. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- 来源中丢失的技法：self-review question checklist；DONE_WITH_CONCERNS status

#### `git-destructive-command-guard` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/2/2/2/3/3/1/0（合计 16/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Safe commands must pass; installation separated.
- **P1 source_fidelity**：No baseline pattern list: the source enumerates concrete destructive forms (push --force, reset --hard, clean -f, branch -D, checkout/restore of uncommitted paths) and the hook wiring; 'declared patterns' leaves the corpus empty by default. 建议：Ship a default destructive-pattern table plus equivalent forms (e.g. -f vs --force, refspec '+'). 证据：`skills/git-guardrails-claude-code/SKILL.md:37-81; skills/gstack/careful/SKILL.md:32-71; SKILL.md:29`
- **P2 trigger_precision**：Nearest neighbour is workflow-skill-authoring; the real confusable local-git-guard-setup is covered, but no anti-trigger to change-scope-freeze edit restriction. 建议：Add anti-trigger for path-scoped edit restriction to change-scope-freeze. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：default destructive git pattern list；PreToolUse hook wiring

#### `isolated-task-implementation` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/2/3/3/2/2（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Reads full flow before writing; stops on ambiguity.；Single writer and isolation are hard gates.
- **P2 source_fidelity**：Source explicitly legitimizes escalation ('bad work is worse than no work') and lists escalation triggers (multiple valid architectures, code beyond provided context, restructuring). The Skill compresses this into 'stop on ambiguity'. 建议：List the escalation triggers explicitly. 证据：`skills/subagent-driven-development/implementer-prompt.md:57-73; SKILL.md:30`
- 来源中丢失的技法：explicit escalation trigger list

#### `local-branch-integration` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/2/3/3/3/3/2/3（合计 22/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Pre-integration recovery ref and exact recovery command.；Both holdouts are candidate wins.
- **P1 trigger_precision**：Non-Responsibilities references `pull-request-update`, which does not exist; the correct target is `remote-pull-request-change`. 建议：Replace with remote-pull-request-change. 证据：`slots/v2/1.0.0/skills/local-branch-integration/SKILL.md:78`
- **P2 source_fidelity**：Source auto-resolves only trivially mechanical conflicts (VERSION, CHANGELOG ordering) and stops otherwise; the Skill stops on any conflict, which is safer but loses the classification. 建议：Keep stop-on-conflict but report whether each conflict is mechanical or semantic. 证据：`skills/gstack/ship/SKILL.md:674-705`
- 来源中丢失的技法：mechanical vs semantic conflict classification

#### `plan-execution-control` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Explicit state machine with invalidation and evidence hashes.；Controller does not do specialist work.
- **P2 source_fidelity**：Source handling of implementer statuses (DONE_WITH_CONCERNS: read concerns before review; NEEDS_CONTEXT: answer then re-dispatch) and the 'never dispatch parallel implementers' rule are not mapped to state transitions. 建议：Map these statuses to transitions and add a no-parallel-writer invariant. 证据：`skills/subagent-driven-development/SKILL.md:104-121,236-267`
- 来源中丢失的技法：status-specific handling of implementer reports；no parallel implementation dispatch

#### `root-cause-investigation` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 有效（胜 / 平）
- 优点：One variable at a time; cause vs trigger vs symptom; sibling-path analysis.
- **P1 measured_efficacy**：Both holdouts tie and mutation needs a behavioral challenge: Phase 9 cannot show the Skill improves investigations. 建议：Phase D case: a defect whose last stack frame is a red herring. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source 'Red Flags' self-interrupts ('just try changing X', 'it's probably X') and the backward trace-up-the-call-chain technique are compressed. 建议：Add a short red-flag list and 'trace backward until the original bad value' rule. 证据：`skills/systematic-debugging/SKILL.md:215-277; skills/systematic-debugging/root-cause-tracing.md:109-169`
- 来源中丢失的技法：red-flag rationalization list；backward call-chain tracing

#### `tdd-change-loop` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/3/3/3/2/0（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：RED for the expected reason before code; refactor only while green.
- **P1 measured_efficacy**：Both holdouts tie; no measured lift. 建议：Phase D case requiring a test that fails for the right reason. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source rebuttals of 'tests after' and 'already manually tested' are dropped; these are the main failure modes in practice. 建议：Add a two-line anti-rationalization note. 证据：`skills/test-driven-development/SKILL.md:206-256`
- 来源中丢失的技法：rebuttal of tests-after and manual-testing rationalizations

#### `ui-remediation` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/3/2/2/3/3/1/3（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Cannot judge its own recaptures.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Source captures a pre-fix state snapshot and screenshot as fixtures and adds a regression test that restores that state; the Skill recaptures only after. 建议：Require pre-fix capture and, where state restore exists, a regression fixture. 证据：`skills/gstack/ios-fix/SKILL.md:416-427,455-465; SKILL.md:31`
- 来源中丢失的技法：pre-fix state snapshot fixture；state-restore regression test

#### `website-audit-remediation` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/2/2/2/3/3/2/2（合计 19/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Deduplicates shared causes; no self-close; separate reassessment.
- **P2 trigger_precision**：Overlap 0.286 with ui-remediation; the discriminator (audit-tool findings incl. SEO/content vs rendered UI critique findings) is implicit. 建议：Add mutual anti-triggers naming the finding source. 证据：`curation/v2/skill-audit/static-scan.json`

### learning-retrospective-and-governance

#### `ai-organizational-adoption-and-leadership` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/0（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Reversible smallest pilot plus explicit non-adoption option.；Gate rejects enthusiasm or tool availability as evidence.
- **P1 source_fidelity**：Source adoption patterns are absent: top-down sponsorship paired with bottom-up 'tiger team' evangelists, a divergence period followed by top-down convergence on few bets, and preferring repeatable processes over open-ended knowledge work. 建议：Add a pilot-selection step that scores candidate workflows on repeatability and names the diverge/converge phase plan. 证据：`skills/ai-product-strategy/references/guest-insights.md:800-807,848-855; slots/v2/1.0.0/skills/ai-organizational-adoption-and-leadership/SKILL.md:28-31`
- **P1 measured_efficacy**：Both Phase 9 holdouts tie: baseline already routes correctly, so the Skill shows no measured lift. 建议：Add execution-quality cases that require the source patterns, then re-measure in phase D. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json paired_skill_holdouts`
- 来源中丢失的技法：tiger teams of early adopters；diverge-then-converge on high-conviction bets；audit AI features against core objectives to avoid bloat

#### `engineering-retrospective-and-improvement` — 改进

- 权限：`read-only`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Blameless fact/interpretation separation is explicit.；Every action needs owner, date, signal and stop condition.
- **P1 source_fidelity**：The source's quantitative metric set (commits, LOC delta, active days, shipping streak, context switches/day, per-project breakdown) and snapshot-to-snapshot trend comparison are reduced to 'identify patterns'. 建议：Define a default metric table and require comparison with the previous retrospective snapshot when one is supplied. 证据：`skills/gstack/retro/SKILL.md:1091-1130,1172-1211; SKILL.md:30`
- **P2 output_verifiability**：'Trend and debt register' has no schema, so two runs cannot be compared. 建议：Specify register columns: pattern, evidence refs, first seen, frequency, owner, status. 证据：`SKILL.md:37`
- 来源中丢失的技法：global metric overview table；per-project breakdown；retro snapshot JSON for trend comparison

#### `feedback-and-continuous-learning-loop` — 改进

- 权限：`read-only`；8 维分 3/2/1/1/3/3/0/0（合计 13/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Preserves dissent and minority evidence; rejects correlation as learning.
- **P1 source_fidelity**：Cited sources do not support the responsibility: deploy follow-up messages and an AI cost-lever framework. The Skill is effectively unsourced synthesis. 建议：Re-ground in continuous-discovery or experiment-readout sources, or mark as authored without source technique. 证据：`skills/gstack/land-and-deploy/SKILL.md:1006-1022; skills/ai-product-strategy/references/artifacts.md:33-44`
- **P1 procedure**：'Update hypothesis confidence' has no confidence scale or update rule, so calibration is not reproducible. 建议：Declare a confidence scale (e.g. 5-level with evidence criteria per level) and require before/after values with the evidence that moved them. 证据：`slots/v2/1.0.0/skills/feedback-and-continuous-learning-loop/SKILL.md:30`
- **P2 trigger_precision**：Overlaps engineering-retrospective (outcome review) and data-analysis-validation (metric interpretation) without anti-triggers to either. 建议：Add anti-triggers to engineering-retrospective-and-improvement and data-analysis-validation. 证据：`SKILL.md:17-18`

#### `local-learning-persistence` — 改进

- 权限：`local-system-write-authorized-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：One record, local only, read-back verified, rollback declared.；Rejects secrets and indefinite retention.
- **P1 source_fidelity**：No record schema: the source's learning types (pattern, pitfall, preference, architecture, tool, operational), confidence, source and files fields are dropped, so 'normalized record' is undefined. 建议：Embed the minimal record schema with the type taxonomy. 证据：`skills/gstack/design-review/SKILL.md:1714-1740; SKILL.md:30`
- **P2 source_fidelity**：Source pitfall about hand-built paths (branch names with '/' create subdirectories) is not preserved. 建议：Add a destination-path normalization check to step 1. 证据：`skills/gstack/ship/SKILL.md:1047-1075`
- **P2 trigger_precision**：Nearest neighbours project-context-and-learning-store (0.283) and local-agent-memory-setup (0.265) are close; only one is an anti-trigger. 建议：Add anti-trigger to local-agent-memory-setup (setup of the store versus writing one record). 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：learning type taxonomy；route writes through the logging helper, never hand-built paths

#### `release-documentation-maintenance` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/3/2/2/3/3/2/0（合计 18/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Coverage map and no-deploy-claim gate are faithful to the source.；Change classification (added/changed/fixed/deprecated/removed) is concrete.
- **P2 source_fidelity**：Public-surface extraction list (exports, CLI flags, config options, endpoints, env vars, renamed/removed surface) and the Diataxis audit lens are dropped. 建议：Add the surface-extraction checklist and tag each doc as tutorial/how-to/reference/explanation. 证据：`skills/gstack/document-release/SKILL.md:537-576; SKILL.md:29`
- **P2 procedure**：Source distinguishes obvious factual updates (apply) from risky or subjective ones (ask); the Skill has no such split. 建议：Return subjective edits as proposals requiring owner decision. 证据：`skills/gstack/document-release/SKILL.md:442-481`
- 来源中丢失的技法：Diataxis audit lens；public surface extraction from diff；auto-apply factual vs ask for subjective

#### `source-metadata-and-provenance` — 改进

- 权限：`read-only`；8 维分 3/1/2/3/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Fact / provider claim / inference / interpretation separation is precise.；Explicitly refuses to infer deployment from a commit.
- **P2 trigger_precision**：Both anti-triggers point to provider-configuration Skills that are not its real confusables; release-documentation-maintenance and reference-library-and-deferred-material are closer in intent. 建议：Replace or add anti-triggers to release-documentation-maintenance and reference-library-and-deferred-material. 证据：`SKILL.md:17-18`
- **P2 source_fidelity**：Sources are a license text and a decision audit-trail table; no provenance technique (e.g. SPDX identifiers, lineage graph format) is carried. 建议：Adopt SPDX license identifiers and a declared lineage-edge format. 证据：`skills/frontend-design/LICENSE.txt:1-177; skills/gstack/autoplan/SKILL.md:877-887`
- 来源中丢失的技法：incremental decision audit-trail table

### observability-operations-and-incidents

#### `ai-observability-configuration` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/1/2/3/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Prompt, response, tool and retrieved content denied by default.
- **P1 trigger_precision**：Overlap 0.386 with log-observability-configuration; neither names the other as an anti-trigger. 建议：Add mutual anti-triggers: gen_ai spans and agent traces vs log pipelines. 证据：`curation/v2/skill-audit/static-scan.json`
- **P1 source_fidelity**：The source's canonical gen_ai.* attribute conventions and the SDK-detected vs manual instrumentation split are absent, so the 'governed telemetry schema' has no reference vocabulary. 建议：Reference OpenTelemetry/Sentry gen_ai semantic conventions as the default schema and detect supported SDKs before manual instrumentation. 证据：`skills/sentry-setup-ai-monitoring/SKILL.md:12-44,269-308; slots/v2/1.0.0/skills/ai-observability-configuration/SKILL.md:28-29`
- 来源中丢失的技法：gen_ai.* semantic conventions；SDK auto-instrumentation before manual spans

#### `apm-instrumentation-enablement` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/2（合计 22/24）；语义裁决 keep；执行 A/B 负向（平 / 负）
- 优点：Duplicate auto/manual instrumentation blocks change; overhead budget required.
- **P2 source_fidelity**：Source 'resolve every context variable before step 0' and 'extend the existing agent resource, never a separate manifest' are not carried. 建议：Add both as preconditions for the Kubernetes variant. 证据：`skills/dd-apm/k8s-ssi/enable-ssi/SKILL.md:12-51,135-174`
- 来源中丢失的技法：resolve all context variables before acting；extend existing agent resource

#### `apm-instrumentation-troubleshooting` — 保留

- 权限：`external-read`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Separates emission, transport, sampling, identity, parsing and query failures.
- **P2 source_fidelity**：Provider-side first checks (is the tracer reporting, does APM recognise the service, effective SDK config) and the 'explain why before asking for host access' rule are dropped. 建议：Order checks provider-side first, then host-side with stated rationale. 证据：`skills/dd-apm/k8s-ssi/troubleshoot-ssi/SKILL.md:329-360; skills/dd-apm/linux-ssi/troubleshoot-ssi/SKILL.md:240-279`
- **P2 measured_efficacy**：Mutation needs behavioral challenge. 建议：Phase D case. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：provider-side diagnostic order

#### `apm-instrumentation-verification` — 优先修订

- 权限：`external-read`；8 维分 3/3/3/3/3/3/2/2（合计 22/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：Known-request evidence required; configuration presence alone insufficient.
- 未发现需修订的问题。

#### `apm-onboarding-summary` — 合并（目标：apm-instrumentation-verification）

- 权限：`read-only`；8 维分 2/3/2/3/3/3/1/2（合计 19/24）；语义裁决 merge；执行 A/B 互有胜负（负 / 胜）
- 优点：Configured is never verified; seven-state classification.
- **P2 boundary**：A read-only aggregation of other Skills' outputs with no domain method of its own; the source onboarding summary is itself a live verification report. Separate Skill adds routing surface without capability. 建议：Fold the service coverage matrix into apm-instrumentation-verification as its multi-service output. 证据：`skills/dd-apm/k8s-ssi/onboarding-summary/SKILL.md:3-7; slots/v2/1.0.0/skills/apm-onboarding-summary/SKILL.md:28-31`
- 来源中丢失的技法：deep links into provider UI per verified service

#### `canary-baseline-management` — 优先修订

- 权限：`artifact-write-local-exec-external-read`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 互有胜负（负 / 胜）
- 优点：Immutable baselines with supersession continuity.
- **P2 source_fidelity**：Source captures the baseline before deploy and offers update only after a healthy canary; the Skill does not tie baseline replacement to a healthy-canary condition. 建议：Require healthy canary evidence as precondition for supersession. 证据：`skills/gstack/canary/SKILL.md:548-587,715-725`
- 来源中丢失的技法：pre-deploy capture; update only after healthy canary

#### `deployment-observation` — 优先修订

- 权限：`artifact-write-local-exec-external-read`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 improve；执行 A/B 负向（平 / 负）
- 优点：Rollback recommendation is not action; every observation bound to query and time.
- **P1 source_fidelity**：Platform-specific wait strategies (workflow run polling by merge SHA, auto-deploy propagation wait) are absent, so the start of the observation window is undefined. 建议：Define window start as confirmed deploy completion per platform strategy. 证据：`skills/gstack/land-and-deploy/SKILL.md:792-831; SKILL.md:28-29`
- 来源中丢失的技法：deploy wait strategy per platform

#### `error-monitoring-issue-investigation` — 保留

- 权限：`external-read`；8 维分 3/2/3/2/3/3/2/2（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Grouping artifact vs symptom vs cause; no resolve/mute/assign.
- **P2 source_fidelity**：Issue category handling (error vs performance vs cron-monitor) changes what context means; not stated. 建议：Add category classification as step 1. 证据：`skills/sentry-debug-issue/SKILL.md:72-111`
- **P2 trigger_precision**：Anti-trigger to root-cause-investigation (local reproduction) is missing. 建议：Add it. 证据：`SKILL.md:17-18`
- 来源中丢失的技法：issue category determines context

#### `incident-response-coordination` — 改进

- 权限：`external-read`；8 维分 3/3/3/2/3/3/1/2（合计 20/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Mitigation first; every action routes to a separately authorized owner.
- **P1 source_fidelity**：No severity scale definition, no communication cadence (internal every 15 minutes) and no status-page templates, all present in the source playbook; 'severity recommendation' is unanchored. 建议：Embed SEV1-SEV4 definitions, three-audience cadence and update templates. 证据：`skills/incident-response/SKILL.md:93-117; skills/incident-response/references/incident-playbook.md:136-165`
- 来源中丢失的技法：SEV scale；15-minute internal update cadence；status page templates

#### `log-observability-configuration` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/1/3/3/3/3/1/0（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Secret and sensitive fields denied by default; volume and cost bounded.
- **P1 trigger_precision**：Overlap 0.386 with ai-observability-configuration without anti-trigger. 建议：Add anti-trigger. 证据：`curation/v2/skill-audit/static-scan.json`
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Pipeline processor patterns (grok parser, remappers) and the troubleshooting table (missing logs, high cost, slow search) are dropped. 建议：Add exclusion filters as the first cost control and the troubleshooting table. 证据：`skills/dd-logs/SKILL.md:76-103,198-206`
- 来源中丢失的技法：exclusion filters for cost；grok parsing pipeline

#### `metrics-system-and-observability` — 改进

- 权限：`external-read`；8 维分 3/3/3/3/3/3/2/0（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Exact numerator/denominator/window/owner/linked action required.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with an ambiguous denominator. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：'One metric this feature must move' and weekly/monthly review cadence are cited but not required. 建议：Require one primary metric and a review cadence. 证据：`skills/prd-development/SKILL.md:346-392; skills/metrics-review/SKILL.md:275-317`
- 来源中丢失的技法：single primary metric；review cadence

#### `monitoring-and-alert-configuration` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/0（合计 20/24）；语义裁决 improve；执行 A/B 有效（胜 / 平）
- 优点：Burn-rate rationale, missing-data behavior, runbook and dedup required.
- **P1 measured_efficacy**：Both holdouts tie; mutation needs behavioral challenge. 建议：Phase D case with an alert lacking an actionable owner. 证据：`curation/v2/skill-audit/static-scan.json`

#### `observability-agent-installation` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 负向（平 / 负）
- 优点：Pinned digest, no mutable latest, uninstall path.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Cluster-type decision (self-hosted needs kubelet tlsVerify false; managed omits it) is a known install failure and not stated. 建议：Add cluster-type variant notes. 证据：`skills/dd-apm/k8s-ssi/agent-install/SKILL.md:145-184`

#### `production-canary-monitoring` — 改进

- 权限：`artifact-write-local-exec-external-read`；8 维分 3/2/3/3/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Diff classification with persistence tracking; no auto-rollback.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 trigger_precision**：Overlaps deployment-observation; page-level visual canary vs provider health signals not stated. 建议：Add mutual anti-triggers. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：fresh page reopen per check, 60s cadence default

#### `production-llm-trace-root-cause-analysis` — 保留

- 权限：`external-read`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Success/failure comparison and first divergent stage required.
- **P2 source_fidelity**：Source mode selection (error / eval / generic) for finding problematic spans is not carried. 建议：Add the three investigation modes. 证据：`skills/agent-observability-trace-rca/SKILL.md:193-232`
- 来源中丢失的技法：error/eval/generic investigation modes

#### `production-trace-classification` — 改进

- 权限：`external-read`；8 维分 3/3/3/2/3/3/1/0（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Category criteria defined before reading outcomes; uncategorized preserved.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Single source ref; pass/partial/fail outcome labelling and pass-rate summary from source are not the output form. 建议：Adopt yes/partial/no outcome label and pass rate in counts. 证据：`skills/agent-observability-eval-pipeline/SKILL.md:207-246`
- 来源中丢失的技法：yes/partial/no outcome labels

#### `release-observability-configuration` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/2/3/3/3/1/1（合计 19/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Association never proves deployment.
- **P1 source_fidelity**：Source's first step, diagnose which half exists (SDK release tag on events vs CI release creation with commits) before configuring anything, is absent. 建议：Add a half-present diagnosis step before any change. 证据：`skills/sentry-setup-releases/SKILL.md:26-64; SKILL.md:28`
- 来源中丢失的技法：diagnose which half of release wiring exists first；suspect-commit path

#### `release-rollback-execution` — 改进

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Migration compatibility and predeclared condition required.
- **P1 procedure**：Rollback method is unspecified; the source's default is a revert commit that redeploys, which needs Git push authority this Skill does not hold. Provider rollback vs revert commit are different actions. 建议：Declare method: provider-native rollback here; revert-commit path routes to change-packaging and remote-git-push. 证据：`skills/gstack/land-and-deploy/SKILL.md:923-944; SKILL.md:28-31`
- 来源中丢失的技法：revert commit as rollback method

#### `service-identity-remapping` — 保留

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Impact preview of monitors and dashboards; collision blocks.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Inferred-entity remaps require peer.service on outbound spans; not stated. 建议：Add as precondition for inferred-entity variant. 证据：`skills/dd-apm/service-remapping/SKILL.md:13-58`

### performance-and-reliability

#### `cloud-reliability-assessment` — 改进

- 权限：`external-read`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（胜 / 平）
- 优点：Read-only boundary is explicit and lists forbidden operations (failover, scale, restore).；Failure-domain, RTO/RPO and dependency coverage are concrete.
- **P1 source_fidelity**：Provider-specific checks from the Azure source are reduced to a generic list; the per-resource assessment table (zone redundancy per plan, health-check path, storage LRS/ZRS) is gone. 建议：Add a provider-variant checklist section (Azure first) with the per-resource table columns from the source. 证据：`skills/azure-reliability/SKILL.md:10-49; slots/v2/1.0.0/skills/cloud-reliability-assessment/SKILL.md:29`
- **P2 output_verifiability**：Findings are 'prioritized' without a declared severity or effort scheme; source classifies quick wins (no downtime) versus migrations with cost impact. 建议：Require each finding to carry severity, downtime impact and cost-impact fields. 证据：`skills/azure-reliability/SKILL.md:137-176; SKILL.md:31`
- 来源中丢失的技法：per-resource reliability assessment table；quick-win vs migration classification with cost and downtime flags

#### `frontend-rendering-and-interaction-performance` — 改进

- 权限：`local-exec`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Measurement discipline (frozen journey, warmup, sample count, distribution) is strong.；Clean split from web-performance-diagnostics via mutual anti-triggers.
- **P1 procedure**：No quantitative budgets: no long-task (50 ms), frame (16.7 ms) or INP (200 ms) thresholds, so 'bottleneck' has no objective cut-off. 建议：Add default budgets used when the user supplies none, and require reporting against them. 证据：`slots/v2/1.0.0/skills/frontend-rendering-and-interaction-performance/SKILL.md:28-31`
- **P1 source_fidelity**：Known cause catalog from sources is absent: animating non-transform/opacity properties, parent CSS-variable driven child transforms, main-thread Framer Motion shorthands. 建议：Add a hypothesis catalog mapping trace symptoms to these causes. 证据：`skills/review-animations/STANDARDS.md:110-129`
- 来源中丢失的技法：animate only transform/opacity；avoid parent CSS variable driving child transforms；Framer Motion shorthand is not hardware-accelerated

#### `kubernetes-deployment-readiness` — 优先修订

- 权限：`external-read`；8 维分 3/3/2/1/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Dry-run is allowed only when guaranteed non-mutating; otherwise marked unavailable.；No-apply authority is explicit.
- **P1 output_verifiability**：Output is a free-form 'ready or blocked' list; the source's severity taxonomy (incompatible / requiresChanges / autoFixed) and per-issue Current/Required/Fix/Docs format are dropped. 建议：Adopt the severity taxonomy, blocker-first ordering and per-issue record format. 证据：`skills/azure-kubernetes/azure-kubernetes-automatic-readiness/SKILL.md:161-200; SKILL.md:31`
- **P2 source_fidelity**：AKS Automatic constraint-spec checks are not exposed as a provider variant. 建议：Add an AKS Automatic variant referencing safeguard constraints such as container resource requests. 证据：`skills/azure-kubernetes/azure-kubernetes-automatic-readiness/SKILL.md:10-49`
- 来源中丢失的技法：incompatible/requiresChanges/autoFixed severity；group by constraint when more than 10 issues；per-issue Current/Required/Fix/Docs record

#### `resilience-and-determinism` — 优先修订

- 权限：`local-exec`；8 维分 1/2/2/2/3/3/1/1（合计 15/24）；语义裁决 improve；执行 A/B 互有胜负（胜 / 负）
- 优点：One-factor-at-a-time variation and retry-masking detection are well specified.
- **P1 boundary**：Required input demands 'a confirmed cause' while the responsibility is to diagnose; the Skill cannot start on an unexplained flaky test, which is its main use case. 建议：Change input to 'an observed nondeterministic or resilience failure with reproduction context'. 证据：`slots/v2/1.0.0/skills/resilience-and-determinism/SKILL.md:10,22`
- **P1 source_fidelity**：Condition-based waiting, the source's proven fix pattern for timing flakiness (15 flaky tests fixed), is not named as a hypothesis or recommendation. 建议：List 'arbitrary sleep/timeout' as a first-class hypothesis and recommend condition-based waiting. 证据：`skills/systematic-debugging/condition-based-waiting-example.ts:1-158`
- **P2 source_fidelity**：Defense-in-depth validation layers are cited as evidence but not used in recommendations. 建议：Reference the four validation layers when recommending repairs for invalid-data causes. 证据：`skills/systematic-debugging/defense-in-depth.md:21-86`
- 来源中丢失的技法：condition-based waiting replacing arbitrary timeouts；defense-in-depth validation layers

#### `web-performance-diagnostics` — 改进

- 权限：`local-exec`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Rejects single Lighthouse score as evidence.；Third-party boundary is part of the frozen setup.
- **P1 procedure**：Core Web Vitals are named without thresholds (LCP 2.5 s, INP 200 ms, CLS 0.1 at p75) and without lab-vs-field distinction. 建议：Add good/needs-improvement/poor thresholds and require labelling lab versus field data. 证据：`slots/v2/1.0.0/skills/web-performance-diagnostics/SKILL.md:29-30`
- **P2 source_fidelity**：Framework/bundler detection and tree-shaking checks that drive attribution are dropped. 建议：Add bundler detection and bundle-attribution step to ownership analysis. 证据：`skills/web-perf/SKILL.md:150-193`
- 来源中丢失的技法：framework and bundler detection table；tree-shaking/sideEffects checks

### product-discovery-and-strategy

#### `ai-product-opportunity-and-wedge` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/0（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Forces a non-AI alternative and falsification conditions.
- **P1 source_fidelity**：Two named source frameworks are absent: the differentiation stack (data > interface > model, most to least defensible) and the promise-to-payoff wedge selection matrix. 建议：Score candidate wedges on promise-to-payoff and classify defensibility by the data/interface/model stack. 证据：`skills/ai-product-strategy/references/artifacts.md:101-115,148-157; slots/v2/1.0.0/skills/ai-product-opportunity-and-wedge/SKILL.md:29-31`
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case where a model-only advantage must be rated weak. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- 来源中丢失的技法：data > interface > model differentiation stack；promise-to-payoff wedge matrix

#### `competitive-case-library` — 保留

- 权限：`workspace-write`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Case schema (actor, context, move, outcome, source, date, confidence) and fact-vs-inference label are enforceable.
- **P2 trigger_precision**：Phase 9 baseline routed a holdout to qualitative-evidence-synthesis; the boundary between normalizing competitor cases and synthesizing research is not stated. 建议：Add anti-trigger: customer research corpus routes to qualitative-evidence-synthesis; this Skill handles competitor/comparable moves. 证据：`evals/runs/capability-compiler-v2/phase-9/attempts/run-0007`

#### `competitive-response-and-monitoring` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/1/0（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Noise/watch/investigate/decision thresholds; no auto-change of price or messaging.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source distinction between competitors and comparables (similar problem, different market) and the 'adopt proven industry patterns' response option are not included. 建议：Monitor comparables explicitly and list 'adopt proven pattern' as a response option. 证据：`skills/competitive-strategy/references/guest-insights.md:277-286,367-376`
- 来源中丢失的技法：competitors vs comparables；adopt industry-standard patterns as a response

#### `customer-interview-execution` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/3（合计 22/24）；语义裁决 keep；执行 A/B 互有胜负（负 / 胜）
- 优点：Past-behavior questions, no pitching; consent before anything.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Probing techniques ('tell me more', gentle repeated why, ask for a specific example, what happened next) and the note template fields are not carried. 建议：Add probe list and observation-log template. 证据：`skills/interview-script/SKILL.md:61-98`
- 来源中丢失的技法：probing technique list；note-taking template

#### `data-analysis-validation` — 优先修订

- 权限：`workspace-write`；8 维分 3/2/3/2/3/3/2/0（合计 18/24）；语义裁决 improve；执行 A/B 负向（平 / 负）
- 优点：Recompute aggregates; denominators and leakage checks.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with a denominator error. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source reproducibility documentation template (question, sources with as-of date, definitions, caveats) is not the required output. 建议：Adopt it as the reproduction-notes schema. 证据：`skills/validate-data/SKILL.md:289-330`
- **P2 trigger_precision**：Close to evaluation-results-analysis (0.157); product metrics vs LLM eval results not separated. 建议：Add anti-trigger to evaluation-results-analysis. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：analysis documentation template

#### `decision-and-outcome-roadmapping` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/1/1（合计 19/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Now/next/later without false dates; kill criteria explicit.
- **P2 source_fidelity**：Sources describe stakeholder presentation, not roadmap construction; roadmap technique is authored. 建议：Mark authored. 证据：`skills/product-strategy-session/SKILL.md:239-263`

#### `evidence-synthesis-and-opportunity-prioritization` — 优先修订

- 权限：`workspace-write`；8 维分 2/2/3/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 负向（负 / 负）
- 优点：Triangulation and dissent register; no rank from source count.
- **P1 boundary**：Name and output both include 'prioritization' and a priority recommendation, overlapping opportunity-prioritization-and-frameworks; the difference (qualitative judgment vs named formula) is only in anti-triggers. 建议：Rename to evidence-synthesis-and-opportunity-framing; output a comparison on explicit dimensions, leave ranking to the frameworks Skill or the human. 证据：`SKILL.md:10,32,39`
- 来源中丢失的技法：PRD self-assessment diagnostic

#### `executive-plan-review` — 改进

- 权限：`read-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：One-way-door register; no scope acceptance without human selection.
- **P1 source_fidelity**：Source review modes (scope expansion, selective expansion, hold scope, scope reduction) chosen up front, and the anti-skip rule over 11 sections, are absent; the Skill has no posture selection. 建议：Require choosing one review mode first and evaluating every section, stating 'no issues' explicitly. 证据：`skills/gstack/openclaw/skills/gstack-openclaw-ceo-review/SKILL.md:6-45,125-164`
- 来源中丢失的技法：four review modes；anti-skip rule

#### `market-positioning-and-competitive-power` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/3（合计 22/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Claim-proof register; copyability of position checked.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Source lesson that the real alternative may be internal (spending the same resources elsewhere) is not part of the alternatives step. 建议：Include 'internal alternative / do nothing' in the comparison frame. 证据：`skills/product-strategy-session/examples/sample-lifesciences.md:76-92`

#### `market-segmentation-and-demand-intelligence` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Demographics alone are not a segment; no fabricated TAM.
- **P2 source_fidelity**：Underserved long-tail segment strategy (compete where incumbents cannot) is a cited source pattern but not an evaluation lens. 建议：Add 'incumbent access gap' to attractiveness comparison. 证据：`skills/competitive-strategy/references/artifacts.md:207-220`

#### `opportunity-prioritization-and-frameworks` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/0（合计 20/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Exact formula variant, scales and sensitivity required; hybrids rejected.
- **P1 measured_efficacy**：Both holdouts tie and the Phase 9 mutation control was invalid, so no valid behavioral evidence exists. 建议：Phase D case requiring an exact RICE computation with sensitivity. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Source RICE definition uses Opportunity Score as Impact; the Skill does not show canonical variable definitions, so models may use the common Impact 0.25-3 scale silently. 建议：List canonical definitions per framework variant. 证据：`skills/prioritization-frameworks/SKILL.md:37-46`
- 来源中丢失的技法：RICE with Opportunity Score as Impact

#### `persona-jtbd-and-journey-modeling` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/1/1（合计 19/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Forces only when supported; no invented demographics.
- **P2 source_fidelity**：No JTBD statement format (When [situation], I want to [motivation], so I can [outcome]) or four-forces model is specified. 建议：Specify the JTBD statement template and push/pull/anxiety/habit forces. 证据：`SKILL.md:29-31,38`

#### `problem-framing-and-customer-research` — 改进

- 权限：`workspace-write`；8 维分 2/3/2/2/3/3/1/0（合计 16/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Solution-free frame is a crisp gate.
- **P1 source_fidelity**：41 source refs include the office-hours forcing questions (demand reality, status quo, desperate specificity, narrowest wedge) and the problem-statement format; none are retained. The Skill classifies claims but does not interrogate them. 建议：Add the forcing-question set as the interrogation step and a structured problem statement output. 证据：`skills/gstack/office-hours/SKILL.md:540-557,636-675; skills/prd-development/SKILL.md:173-217`
- **P2 boundary**：Name says 'customer research' but the Skill only processes supplied evidence; research planning and interviews belong elsewhere. 建议：Rename to problem-framing. 证据：`SKILL.md:10`
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with solution-laden input notes. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- 来源中丢失的技法：office-hours forcing questions；problem statement template

#### `qualitative-evidence-synthesis` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/1/0（合计 18/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Quote counts not presented as prevalence; counterexamples kept.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with a minority contradicting theme. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source depth-by-breadth 2x2 for feedback is cited but unused. 建议：Offer depth x breadth as optional theme characterization (not prioritization). 证据：`skills/analyzing-user-feedback/references/artifacts.md:46-66`
- 来源中丢失的技法：depth x breadth feedback matrix

#### `research-planning-and-governance` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Decision linkage and stopping rule; full governance contract before contact.；Both holdouts are candidate wins.
- 未发现需修订的问题。

#### `results-analysis-and-decision-readout` — 优先修订

- 权限：`workspace-write`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：Post-hoc thresholds labelled; GO/PIVOT/KILL as recommendation only.
- **P2 trigger_precision**：Overlap 0.34 with evaluation-results-analysis; product experiment vs model evaluation not stated in anti-triggers. 建议：Add mutual anti-triggers. 证据：`curation/v2/skill-audit/static-scan.json`

#### `solution-hypothesis-and-experiment-design` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 负向（平 / 负）
- 优点：Falsifiable prediction, counterfactual and kill criterion required.
- **P2 source_fidelity**：Experiment type menu (concierge, fake door, prototype, A/B) from discovery sources is not listed. 建议：List experiment types by risk and cost. 证据：`skills/discovery-process/SKILL.md:393-410`
- 来源中丢失的技法：experiment type menu

#### `strategic-choice-and-differentiation` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Mutually exclusive choices; reversal evidence stated.
- **P2 source_fidelity**：Niche-network corollary (disruptive products start with weird niche audiences) is cited but not a lens. 建议：Optional lens for networked products. 证据：`skills/competitive-strategy/references/artifacts.md:77-88`

#### `structural-power-and-moats` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Seven Powers enumerated with mechanism, barrier and decay.
- **P1 measured_efficacy**：Both holdouts tie; mutation needs behavioral challenge. 建议：Phase D case where growth is mislabeled as a moat. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Source switching-cost model (time + money + organizational + emotional) is reduced to the label. 建议：Expand switching-cost assessment to the four components. 证据：`skills/competitive-strategy/references/artifacts.md:137-158`
- 来源中丢失的技法：four-component switching cost

### requirements-and-planning

#### `context-intake-and-routing` — 改进

- 权限：`read-only`；8 维分 3/1/2/2/2/3/0/1（合计 14/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Emits a routing envelope only; refuses to manufacture domain analysis to justify a route.
- **P1 trigger_precision**：Overlap 0.381 with ui-task-routing-and-governance and neither names the other as an anti-trigger, so a UI request can be routed by the generic intake or vice versa. 建议：Add anti-trigger: UI-only scope routes to ui-task-routing-and-governance; this Skill handles cross-domain or unclassified intake. 证据：`curation/v2/skill-audit/static-scan.json; slots/v2/1.0.0/skills/context-intake-and-routing/SKILL.md:17-18`
- **P1 source_fidelity**：Cited sources are an AI product checklist and AI strategy questions, unrelated to request intake or routing; the Skill has no source technique behind it. 建议：Re-ground in a routing source or mark as authored; add a concrete routing decision table (stage x risk x authority). 证据：`skills/ai-product-strategy/references/artifacts.md:530-567; skills/ai-product-strategy/SKILL.md:65-79`

#### `design-plan-review` — 改进

- 权限：`read-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Scope gate first: returns not-applicable when no UI scope exists.；Separates taste decisions from evidence defects.
- **P1 source_fidelity**：The source reviews design by generating visual mockups by default when a designer tool is available ('real visuals, not text descriptions'); the Skill reviews text only and never asks for or references visual artifacts. 建议：Add: when mockups or rendered references exist, review against them; otherwise record 'text-only review' as a confidence limit. 证据：`skills/gstack/plan-design-review/SKILL.md:786-825; SKILL.md:29`
- **P2 procedure**：No scoring dimensions: the source rates each design area and states what a 10 would look like; the Skill only lists areas. 建议：Rate each area 0-10 with the gap to 10 stated as the amendment. 证据：`skills/gstack/plan-design-review/SKILL.md:468-507`
- 来源中丢失的技法：mockup-first plan review；per-dimension 0-10 with 'what would make it 10'

#### `developer-experience-plan-review` — 改进

- 权限：`read-only`；8 维分 3/2/2/1/2/3/1/0（合计 14/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Journey coverage (setup, first success, debug, upgrade) is right.
- **P1 source_fidelity**：Source principle 'gather evidence and force decisions before scoring' starts with target-developer persona interrogation; the Skill has no persona step, so expectations and tolerance are undefined. 建议：Add step 1: identify target developer persona and its expectations before tracing journeys. 证据：`skills/gstack/plan-devex-review/SKILL.md:796-835; SKILL.md:28-30`
- **P1 output_verifiability**：'Measurable DX outcomes' is named but no metric (time-to-first-success, steps to hello world, error-to-fix time) is required. 建议：Require at least time-to-first-success and failure-recovery criteria. 证据：`SKILL.md:30,39`
- **P2 measured_efficacy**：Both holdouts tie; mutation needs a behavioral challenge. 建议：Phase D case with a plan that has a hidden onboarding gap. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：developer persona interrogation；minute-2 abandonment vs minute-5 delight lens

#### `document-and-artifact-governance` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Clear split: governs identity and lifecycle, never authors content.
- **P2 source_fidelity**：Sources are document templates, not governance practices; staleness and invalidation rules are authored without source technique. 建议：Mark as authored; define a default state set (draft, approved, superseded, stale, retired) and staleness triggers. 证据：`skills/discovery-process/template.md:1-39; skills/product-strategy-session/template.md:1-38`

#### `documentation-authoring` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：One Diataxis type per document; no unverified present-tense claims.
- **P1 source_fidelity**：The source's most important step, codebase archaeology before writing (map structure, read entry points, trace flows), is reduced to 'build a source map from approved facts'; for code documentation the Skill does not instruct reading the code. 建议：Add a research step: when documenting code, read entry points and trace the documented flow before drafting. 证据：`skills/gstack/document-generate/SKILL.md:489-528; SKILL.md:29`
- **P2 measured_efficacy**：Mutation needs a behavioral challenge. 建议：Phase D case requiring type-pure how-to without explanation drift. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：codebase archaeology before writing

#### `facilitation-and-collaboration-protocols` — 改进

- 权限：`workspace-write`；8 维分 3/3/2/2/3/3/1/1（合计 18/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Independent evidence before convergence; no manufactured consensus.
- **P1 source_fidelity**：The workshop-facilitation interaction protocol (entry modes guided/context-dump/best-guess, one question per turn, progress labels, pause/resume, numbered recommendations) is the source's facilitation source of truth and is absent. 建议：Add the protocol as the default for AI-facilitated sessions. 证据：`skills/discovery-process/SKILL.md:73-85; SKILL.md:28-32`
- 来源中丢失的技法：entry modes；one-question turns with progress labels；pause/resume handling

#### `implementation-planning-and-handoff` — 改进

- 权限：`workspace-write`；8 维分 3/2/2/2/3/3/1/0（合计 16/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Requirement-to-task traceability and risk-first ordering.
- **P1 source_fidelity**：The source task format (exact files to create/modify with line ranges, failing test first, exact command with expected failure, bite-sized steps for a zero-context engineer) is reduced to 'map tasks to affected areas'; the gate even forbids 'inventing file paths as facts' without requiring verified paths. 建议：Require verified file paths, a failing-test-first step and an exact verification command per task. 证据：`skills/writing-plans/SKILL.md:1-20,63-105; SKILL.md:29,46`
- **P1 measured_efficacy**：Both holdouts tie and mutation needs a behavioral challenge. 建议：Phase D: score plans on zero-context executability. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：exact file and line task header；failing test as step 1；plan written for a zero-context engineer

#### `independent-plan-review` — 保留

- 权限：`read-only`；8 维分 3/2/2/2/3/3/2/1（合计 18/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Generic advice without a demonstrated gap is not a finding.
- **P2 trigger_precision**：Anti-triggers cover design review and rewriting, but not engineering-plan-review (0.188), its closest confusable. 建议：Add anti-trigger: architecture/test-strategy depth review routes to engineering-plan-review. 证据：`curation/v2/skill-audit/static-scan.json`

#### `plan-review-decision-synthesis` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Decision classification (mechanical/taste/one-way door) faithful to source.；Cannot downgrade a blocking dissent.
- **P2 source_fidelity**：The source's six decision principles used to auto-resolve mechanical items are not carried; the Skill classifies but gives no resolution rule for mechanical items. 建议：State that mechanical items carry a recommended resolution with the principle cited; only taste and one-way items go to the human queue. 证据：`skills/gstack/autoplan/SKILL.md:570-587`
- 来源中丢失的技法：six decision principles

#### `requirements-and-delivery-contract` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Actor-trigger-condition-response statements with stable IDs.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Out-of-scope list with rationale and dependency section from the PRD source are not required outputs. 建议：Add 'explicit out-of-scope with rationale' to the output contract. 证据：`skills/prd-development/SKILL.md:471-534`

#### `risk-preflight-and-safety-governance` — 改进

- 权限：`read-only`；8 维分 3/2/2/2/3/3/1/1（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Prior authorization or tool availability is never current permission.
- **P2 procedure**：Risk classification has no scale (likelihood x impact or reversibility tiers), so dispositions are not reproducible. 建议：Define reversibility tiers and the disposition each tier forces. 证据：`SKILL.md:29-31`
- **P2 trigger_precision**：Close to ai-safety-and-action-governance without an anti-trigger. 建议：Route AI-agent action policy to ai-safety-and-action-governance. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：refuse-and-show-next-safe-window pattern from industrial requirements

#### `workflow-orchestration-and-lifecycle` — 改进

- 权限：`workspace-write`；8 维分 2/3/2/2/3/3/2/1（合计 18/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Never impersonates a selected capability.
- **P1 boundary**：Duplicates the role of the released V2 router and composite Recipes (select, sequence, gate, invalidate). An atomic Skill that orchestrates contradicts the decision that workflows live in Recipes. 建议：Narrow to 'plan a workflow for a request not covered by an existing Recipe' and require reuse of an existing Recipe when one matches. 证据：`recipes/v2/1.0.0/router.json; SKILL.md:10,28-32`
- 来源中丢失的技法：per-task spec review then quality review loop

### testing-and-quality-assurance

#### `baseline-regression-control` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Separates new regression, pre-existing failure, flake and intended change; no threshold moves after results.
- **P2 source_fidelity**：Sources are canary page baselines; test-suite regression attribution is authored. 建议：Mark authored. 证据：`skills/canary/SKILL.md:548-574,715-725`

#### `code-review-evidence-acquisition` — 改进

- 权限：`local-exec-external-read`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Evidence bound to exact base/head refs; stops before findings.
- **P1 trigger_precision**：Non-Responsibilities references `provider-review-comment-response`, which does not exist; the owner is `pull-request-comment-response`. 建议：Replace the reference. 证据：`slots/v2/1.0.0/skills/code-review-evidence-acquisition/SKILL.md:76`
- **P2 source_fidelity**：Source fetches the latest base and diffs against the computed merge base to avoid stale-base false positives; the Skill freezes refs but does not require merge-base diffing. 建议：Require merge-base diff against a freshly fetched base (read-only fetch where authorized). 证据：`skills/gstack/review/SKILL.md:553-569`
- 来源中丢失的技法：merge-base diff after fresh base fetch；advisory version-queue collision status

#### `completion-evidence-gate` — 优先修订

- 权限：`local-exec`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：Rejects prose, status text and stale output; never reruns or upgrades a claim.
- **P2 trigger_precision**：Anti-trigger 'run the missing tests' routes to baseline-regression-control, which compares baseline vs candidate; producing missing evidence is better owned by the implementing Skill or tdd-change-loop. 建议：Route missing-evidence production to the originating owner; reserve baseline-regression-control for comparisons. 证据：`slots/v2/1.0.0/skills/completion-evidence-gate/SKILL.md:17`
- 来源中丢失的技法：confidence gate with false-positive filtering before reporting

#### `developer-experience-assessment` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Real journey with elapsed time; reading docs alone insufficient.
- **P2 source_fidelity**：Source dogfoods documentation and getting-started through a browser as well as the CLI; the Skill is command-centric. 建议：Include docs navigation and copy-paste of documented snippets in the journey. 证据：`skills/gstack/devex-review/SKILL.md:662-701`

#### `evaluation-dataset-publication` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 负向（平 / 负）
- 优点：Idempotent upload; refuses overwrite, public visibility and mutable latest aliases.
- 未发现需修订的问题。

#### `evaluation-results-analysis` — 保留

- 权限：`local-exec`；8 维分 3/2/3/3/3/3/1/1（合计 19/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：No metric shopping; post-hoc work labelled exploratory.
- **P2 trigger_precision**：Overlap 0.34 with results-analysis-and-decision-readout; model evaluation vs product experiment not stated. 建议：Add mutual anti-triggers. 证据：`curation/v2/skill-audit/static-scan.json`

#### `implementation-spec-compliance-review` — 保留

- 权限：`read-only`；8 维分 3/3/3/3/3/3/3/3（合计 24/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Implementer report treated as untrusted claim; missing and extra behavior both checked; both holdouts are candidate wins.
- 未发现需修订的问题。

#### `independent-blackbox-qa` — 保留

- 权限：`artifact-write-local-exec-external-read`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Public surfaces only; numbered reproducible findings with coverage matrix.
- **P2 source_fidelity**：Source diff-aware mode uses the branch diff to choose what to test. The Skill correctly forbids source inspection, but should accept a change-scope summary from another owner to focus testing. 建议：Accept a supplied change-scope list as input without reading source. 证据：`skills/qa-only/SKILL.md:594-645`
- 来源中丢失的技法：diff-aware test focus via supplied scope

#### `independent-code-review` — 改进

- 权限：`read-only`；8 维分 3/2/3/3/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Findings require scenario, citation, consequence and contract; style preferences omitted.
- **P1 trigger_precision**：Non-Responsibilities references `provider-review-comment-response`, which does not exist. 建议：Replace with pull-request-comment-response. 证据：`slots/v2/1.0.0/skills/independent-code-review/SKILL.md:79`
- **P1 measured_efficacy**：Both holdouts tie and mutation needs a behavioral challenge, for one of the most frequently used Skills. 建议：Phase D case: a diff with one seeded authorization bug among style noise. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Source adversarial 'challenge' mode (try to break the change) is distinct from standard review and is not offered. 建议：Add an optional adversarial pass. 证据：`skills/gstack/codex/SKILL.md:584-621`
- 来源中丢失的技法：adversarial challenge mode

#### `llm-evaluator-engineering` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Deterministic checks before judges; calibration against labels; both holdouts are candidate wins.
- 未发现需修订的问题。

#### `llm-experiment-execution` — 优先修订

- 权限：`remote-write-authorized-only`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 负向（负 / 平）
- 优点：No post-submit drift; max cost preview; both holdouts are candidate wins.
- 未发现需修订的问题。

#### `llm-quality-evaluation` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/2（合计 22/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：External judge blocked without transfer authorization; agreement and contamination checks.
- 未发现需修订的问题。

#### `model-and-workflow-benchmarking` — 改进

- 权限：`local-exec`；8 维分 2/2/3/3/3/3/2/1（合计 19/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Warmup, repeats, failed-case retention; leaderboard point estimates fail.
- **P2 boundary**：Sources mix cross-model skill benchmarking with web performance regression benchmarking; the latter belongs to baseline-regression-control and web-performance-diagnostics. 建议：Scope to model/workflow variants; route app performance regression elsewhere. 证据：`skills/gstack/benchmark/SKILL.md:240-279`
- 来源中丢失的技法：auth preview before multi-provider benchmark

#### `playwright-test-engineering` — 改进

- 权限：`local-exec`；8 维分 3/1/3/3/3/2/2/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Role locators, web-first assertions, no sleeps.
- **P1 trigger_precision**：Overlap 0.447 with vitest-tooling, the highest in the catalog; neither names the other as an anti-trigger. 建议：Add mutual anti-triggers: browser/E2E vs unit/integration in Node. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 permission_fit**：Writes tests only as candidate artifacts; no Skill then applies them to the project except tdd-change-loop, which is not named. 建议：Name tdd-change-loop or isolated-task-implementation as the apply owner. 证据：`SKILL.md:30-31`
- 来源中丢失的技法：activity-to-reference decision tree

#### `qa-finding-triage` — 保留

- 权限：`read-only`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：Dedupe without losing variants; no risk acceptance.
- **P2 source_fidelity**：Source tier cutoffs (quick: critical+high, standard: +medium, exhaustive: all) and 'previously skipped finding' dedup are not carried. 建议：Add tier-based disposition recommendation and prior-skip dedup. 证据：`skills/gstack/qa/SKILL.md:710-735; skills/gstack/review/SKILL.md:766-805`
- 来源中丢失的技法：tier severity cutoffs；cross-review skipped-finding dedup

#### `safe-browser-probing` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：One question, allowlisted origins, no generalization into an audit.
- 未发现需修订的问题。

#### `test-case-design-and-export` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/0/0（合计 17/24）；语义裁决 improve；执行 A/B 互有胜负（负 / 胜）
- 优点：Every case states preconditions, data, action and observable result.
- **P1 source_fidelity**：Cited sources are a dependency install message and a description; the source's five-dimension case quality score (coverage, executability, independence, maintainability, completeness, 20% each) is attached to testing-portfolio-strategy instead and absent here, so 'score coverage' is undefined. 建议：Move the quality-score rubric here and require it in the coverage matrix. 证据：`skills/test-case-generator/SKILL.md:3-7,108-113,200-208`
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- 来源中丢失的技法：five-dimension test case quality score

#### `test-double-discipline` — 保留

- 权限：`local-exec`；8 维分 3/3/3/2/3/3/3/3（合计 23/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Real code first; no test-only production API; both holdouts are candidate wins.
- 未发现需修订的问题。

#### `testing-portfolio-strategy` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/2/1/2（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Risk mapped to cheapest observing layer; rejects pyramid dogma; both holdouts are candidate wins.
- **P2 permission_fit**：local-exec identity for a design-only Skill that runs nothing. 建议：Reduce to read-only or run-output. 证据：`slots/v2/1.0.0/skills/testing-portfolio-strategy/contract.json; SKILL.md:28-31`
- **P2 source_fidelity**：Sources are test-case generator features, which belong to test-case-design-and-export. 建议：Reassign sources; mark portfolio method authored. 证据：`skills/test-case-generator/SKILL.md:19-27,200-208`

#### `vitest-tooling` — 改进

- 权限：`local-exec`；8 维分 3/1/3/3/3/2/2/1（合计 18/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Controlled time, explicit cleanup, snapshots only where meaningful.
- **P1 trigger_precision**：Overlap 0.447 with playwright-test-engineering without anti-trigger. 建议：Add mutual anti-trigger. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Type testing (.test-d.ts with expectTypeOf) and file:line test selection are not mentioned. 建议：Add as available techniques. 证据：`skills/vitest/references/advanced-type-testing.md:10-23; skills/vitest/references/core-cli.md:14-28`
- 来源中丢失的技法：type tests via expectTypeOf；run test by file:line

#### `website-audit-assessment` — 保留

- 权限：`local-exec-external-read`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Respects robots and rate limits; deduplicated findings with reassessment requirement.
- **P2 source_fidelity**：Source baseline diff / regression-since report is the natural reassessment mechanism and is not referenced. 建议：Use baseline diff for reassessment when a prior audit exists. 证据：`skills/audit-website/references/OUTPUT-FORMAT.md:123-160`
- 来源中丢失的技法：regression-since baseline diff

### tool-runtime-and-artifact-support

#### `agent-workflow-runtime-support` — 改进

- 权限：`local-exec`；8 维分 2/2/2/2/3/3/1/1（合计 16/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Cannot mark domain work complete from orchestration state.
- **P1 source_fidelity**：The dominant cited source pattern is 'prior learnings' lookup with an explicit cross-project consent setting; the Skill mentions consent but not the per-project vs cross-project learning boundary that the sources gate on. 建议：Add an explicit cross-project learning consent state (unset/false/true) defaulting to project-only. 证据：`skills/gstack/cso/SKILL.md:535-574; skills/gstack/investigate/SKILL.md:470-509; slots/v2/1.0.0/skills/agent-workflow-runtime-support/SKILL.md:28-30`
- **P2 boundary**：Session mechanics overlap plan-execution-control (checkpoint, pause/resume) and workflow-orchestration-and-lifecycle. 建议：State that step state belongs to plan-execution-control; this Skill owns host/session mechanics only. 证据：`SKILL.md:30`
- 来源中丢失的技法：cross-project learnings consent flag

#### `artifact-persistence-and-tool-actions` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Path containment, no extra files, explicit no-write outcome.
- **P2 trigger_precision**：Nearest neighbour local-learning-persistence (0.2) is not an anti-trigger; workspace artifact vs local-system learning store is implicit. 建议：Add anti-trigger. 证据：`curation/v2/skill-audit/static-scan.json`

#### `browser-agent-pairing-provisioning` — 改进

- 权限：`local-system-write-external-session-authorized-only`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Scoped, expiring, revocable; no wildcard access.
- **P1 source_fidelity**：Source one-way-door warning is missing: pairing may relaunch the browser daemon, killing open tabs, cookies and logged-in sessions. The Skill's preview lists exposure but not session-loss consequence. 建议：Add daemon-relaunch and session-loss to the preview and require explicit consent for it. 证据：`skills/gstack/pair-agent/SKILL.md:520-559; slots/v2/1.0.0/skills/browser-agent-pairing-provisioning/SKILL.md:29`
- 来源中丢失的技法：live-daemon relaunch consent (session loss)

#### `browser-agent-pairing-verification` — 保留

- 权限：`local-exec-external-read`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Six-state diagnosis; connectivity is not data authority.
- **P2 source_fidelity**：Source troubleshooting table ('tab not owned by your agent', 'domain not allowed') maps errors to causes; not carried. 建议：Add an error-to-diagnosis table. 证据：`skills/gstack/pair-agent/SKILL.md:713-730`
- 来源中丢失的技法：pairing error message diagnosis table

#### `browser-authentication-setup` — 保留

- 权限：`local-system-write-authorized-only`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：No value exposure; non-secret validation; both holdouts are candidate wins.
- **P2 source_fidelity**：Source checks whether the runtime is already attached to the real browser (CDP mode) before importing anything; the Skill lacks this no-op path. 建议：Add 'already authenticated via attached real browser' as a no-write outcome. 证据：`skills/gstack/setup-browser-cookies/SKILL.md:153-192`
- 来源中丢失的技法：CDP mode check before cookie import

#### `browser-data-acquisition-runtime` — 保留

- 权限：`external-read`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 未测（未测）
- 优点：Login does not authorize acquisition or reuse; read-only actions only.
- **P2 measured_efficacy**：Mutation needs behavioral challenge. 建议：Phase D case with a form-submit temptation. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Sources are browser launch setup, not acquisition technique; the governance content is authored. 建议：Mark authored. 证据：`skills/gstack/open-gstack-browser/SKILL.md:162-313`

#### `browser-session-and-runtime-configuration` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Ephemeral only; reproducible invocation.
- **P2 source_fidelity**：Source prerequisite (npx availability, pause and ask if absent) and the playwright-cli.json config file convention are not named. 建议：Name the prerequisite check and config file. 证据：`skills/playwright/SKILL.md:12-32; skills/playwright/references/workflows.md:72-89`

#### `diagram-and-architecture-artifact-generation` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Every node and edge traced or marked unknown; syntactically valid invented diagram fails.
- **P2 source_fidelity**：Write .mmd source first, then render once as a triplet; rendering mechanics are reduced to a 'host request', which is correct given no renderer owner, but the source-first ordering should be stated. 建议：State source file is persisted before any render request. 证据：`skills/gstack/diagram/SKILL.md:194-262`

#### `document-rendering-and-validation` — 优先修订

- 权限：`workspace-write-local-exec`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 improve；执行 A/B 互有胜负（负 / 胜）
- 优点：Renderer exit is insufficient; inspected layout and accessibility required.
- **P1 trigger_precision**：Non-Responsibilities references `artifact-publication`, which does not exist. 建议：Replace with artifact-persistence-and-tool-actions or evaluation-dataset-publication as appropriate. 证据：`slots/v2/1.0.0/skills/document-rendering-and-validation/SKILL.md:73`
- 来源中丢失的技法：publication mode with cover, TOC, chapter breaks

#### `local-agent-memory-setup` — 保留

- 权限：`local-system-write-authorized-only`；8 维分 3/2/3/3/3/3/1/3（合计 21/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Project isolation; no implicit sync; both holdouts are candidate wins.
- **P2 source_fidelity**：The primary source sets up a remote-backed knowledge base using an access token; the Skill narrows to local only, a deliberate tightening, but does not say remote-backed setups are out of scope. 建议：State that remote or hosted memory backends are not covered and block. 证据：`skills/gstack/setup-gbrain/SKILL.md:401-440,1007-1046`

#### `local-git-guard-setup` — 优先修订

- 权限：`local-system-write-authorized-only`；8 维分 3/3/3/3/3/3/1/1（合计 20/24）；语义裁决 keep；执行 A/B 互有胜负（负 / 胜）
- 优点：Hooks-path classification; refuses committed or shared hooks paths.
- **P2 source_fidelity**：Single one-line source; content is authored. The core risk it guards (chaining installer renaming a team's committed hooks) is well captured. 建议：Mark authored. 证据：`skills/gstack/ship/SKILL.md:965`

#### `mobile-platform-runtime-support` — 优先修订

- 权限：`local-exec`；8 维分 3/3/2/3/3/3/1/1（合计 19/24）；语义裁决 improve；执行 A/B 互有胜负（负 / 胜）
- 优点：Missing signing blocks rather than prompting for secrets.
- **P2 source_fidelity**：Sources describe codegen regeneration and debug-bridge removal, which are source edits; the Skill forbids source edits, so the cited technique is not applicable and the Skill's own procedure is generic. 建议：Re-ground in simulator/device run diagnostics or mark authored; add platform-specific readiness checks (xcodebuild -showsdks, adb devices). 证据：`skills/gstack/ios-sync/SKILL.md:426-448; skills/gstack/ios-clean/SKILL.md:447-460`

#### `project-context-and-learning-store` — 改进

- 权限：`local-system-write-authorized-only`；8 维分 2/2/3/3/3/3/2/1（合计 19/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Per-record opt-in; tombstones; no cross-machine sync.
- **P1 boundary**：Save operation duplicates local-learning-persistence (one validated record to a local store); the two differ only in that this one also restores/searches/prunes. 建议：Make this the read/maintain Skill (restore, search, prune, reconcile) and route all writes of new records to local-learning-persistence. 证据：`curation/v2/skill-audit/static-scan.json (0.283); SKILL.md:10`
- **P2 source_fidelity**：Source restore-point pattern (capture verbatim prior plan state with branch and commit, prepend restore pointer) is the best-developed technique and is not named. 建议：Add restore-point record type. 证据：`skills/gstack/autoplan/SKILL.md:705-751`
- 来源中丢失的技法：restore point with verbatim prior state and re-run instructions

#### `provider-cli-authentication-setup` — 保留

- 权限：`local-system-write-external-session-authorized-only`；8 维分 3/3/3/3/3/3/0/1（合计 19/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Refuses pasted secrets and overbroad scopes; setup authority only.
- **P2 source_fidelity**：Only source is a section heading; the Skill is fully authored. 建议：Mark authored. 证据：`skills/dd-apm/k8s-ssi/troubleshoot-ssi/SKILL.md:32-33`

#### `reference-library-and-deferred-material` — 改进

- 权限：`local-exec`；8 维分 3/2/3/3/3/2/1/1（合计 18/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：Retention never makes material operational guidance.
- **P2 permission_fit**：Identity is local-exec although the procedure only records metadata; no command is executed. 建议：Reduce to workspace-write run-output. 证据：`slots/v2/1.0.0/skills/reference-library-and-deferred-material/contract.json; SKILL.md:28-31`
- **P2 source_fidelity**：Sources are arbitrary deferred fragments (workflow summary, ASL levels); this is the right home for them, but no technique is required. 建议：None beyond marking authored. 证据：`skills/discovery-process/SKILL.md:87-91`

#### `test-runtime-bootstrap` — 保留

- 权限：`workspace-write-local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（胜 / 胜）
- 优点：One real-behavior test proves setup; exact restore on failure.
- **P2 source_fidelity**：Framework selection by ecosystem marker table is in the sibling source and not referenced. 建议：Reference marker-to-framework defaults when none is selected. 证据：`skills/gstack/design-review/SKILL.md:590-629,663-671`

#### `tool-runtime-readiness` — 保留

- 权限：`local-exec`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：PATH presence is not readiness; five-state verdict.
- 未发现需修订的问题。

#### `workflow-runtime-upgrade` — 改进

- 权限：`local-system-write-authorized-only`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Pinned target, backup, rollback, post-upgrade health.
- **P1 source_fidelity**：Source warns that a running daemon keeps serving the old binary after upgrade and must be stopped unconditionally, and that a local vendored copy must be handled; without this the post-upgrade health check can pass against stale code. 建议：Add stop-stale-daemon and vendored-copy steps before health verification. 证据：`skills/gstack/gstack-upgrade/SKILL.md:192-231,269-308; SKILL.md:31`
- 来源中丢失的技法：stop stale daemon after upgrade；handle local vendored copy

#### `workflow-skill-authoring` — 改进

- 权限：`workspace-write-local-exec`；8 维分 3/2/3/3/3/3/2/1（合计 20/24）；语义裁决 improve；执行 A/B 有效（平 / 胜）
- 优点：One atomic responsibility; candidate not release.
- **P1 trigger_precision**：Non-Responsibilities references `artifact-publication`, which does not exist. 建议：Replace with the real owner or remove. 证据：`slots/v2/1.0.0/skills/workflow-skill-authoring/SKILL.md:74`
- **P2 source_fidelity**：Source naming constraints (lowercase, digits, dashes, <=32 chars, starts with a letter) and 3-5 trigger phrases are not stated. 建议：Add naming and trigger-count rules. 证据：`skills/gstack/skillify/SKILL.md:460-499`
- 来源中丢失的技法：skill name constraints；3-5 trigger phrases

### ux-ui-and-accessibility

#### `accessibility-contracts-and-assistive-validation` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/3（合计 23/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Every criterion bound to a user task, state and evidence; generic WCAG checklist cannot pass.；Both holdouts are candidate wins; 32 source refs.
- **P2 source_fidelity**：Numeric thresholds from source (4.5:1 normal text, 3:1 large text, 2-4px focus ring) are not stated as defaults. 建议：Add WCAG 2.2 AA default thresholds used when the contract does not override them. 证据：`skills/ui-ux-pro-max/references/quick-reference.md:7-34; slots/v2/1.0.0/skills/accessibility-contracts-and-assistive-validation/SKILL.md:30`
- 来源中丢失的技法：contrast ratio thresholds；spec vs APG source-status distinction

#### `ai-interaction-and-probabilistic-ux` — 改进

- 权限：`workspace-write`；8 维分 3/3/3/2/3/2/1/0（合计 17/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Rejects decorative confidence theater; correction/undo proportional to consequence.
- **P1 measured_efficacy**：Both holdouts tie; no measured lift. 建议：Phase D case requiring uncertainty and correction states. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 permission_fit**：Responsibility is to 'design' interaction, yet permission is authorized-workspace (source write); the procedure never writes source. 建议：Reduce to run-output, or add an explicit implementation step. 证据：`slots/v2/1.0.0/skills/ai-interaction-and-probabilistic-ux/contract.json; SKILL.md:28-32`
- **P2 source_fidelity**：Sources are two high-level quotes; no concrete AI UX pattern (streaming partials, citation display, regenerate, thumbs feedback) is grounded. 建议：Add a pattern catalog per state. 证据：`skills/ai-product-strategy/references/guest-insights.md:730-753`

#### `content-copy-and-authentic-assets` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/2（合计 21/24）；语义裁决 keep；执行 A/B 有效（平 / 胜）
- 优点：Bans lorem ipsum, fake testimonials, invented metrics; covers every UI state.
- **P2 source_fidelity**：Source density rule (headline <= 8 words, sub-paragraph <= 25 words, one asset or CTA per section) and image-generation-first asset priority are dropped. 建议：Add density defaults for marketing surfaces. 证据：`skills/design-taste-frontend/SKILL.md:262-332`
- **P2 measured_efficacy**：Mutation needs behavioral challenge. 建议：Phase D case with fabricated social proof in the brief. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：section content density limits；asset sourcing priority order

#### `cross-domain-ui-preflight-checklists` — 合并（目标：evidence-based-ui-review-and-release-gates）

- 权限：`workspace-write`；8 维分 2/1/2/2/2/3/1/0（合计 13/24）；语义裁决 merge；执行 A/B 无增益（平 / 平）
- 优点：Not-applicable must be justified.
- **P1 boundary**：Functionally a subset of evidence-based-ui-review-and-release-gates (criteria vs current evidence, blocker classification, no repair) with a broader domain list; two Skills with the same verdict function confuse routing. 建议：Merge as the 'preflight mode' of evidence-based-ui-review-and-release-gates. 证据：`slots/v2/1.0.0/skills/cross-domain-ui-preflight-checklists/SKILL.md:10,28-32; slots/v2/1.0.0/skills/evidence-based-ui-review-and-release-gates/SKILL.md:10,28-32`
- **P1 source_fidelity**：The concrete source checklists (14-point final pre-flight, canonical pre-delivery checklist) are not reproduced; the Skill only names domains. 建议：Carry the canonical checklist items into the merged Skill. 证据：`skills/design-taste-frontend/SKILL.md:910-980; skills/ui-ux-pro-max/references/pro-rules.md:64-117`
- 来源中丢失的技法：canonical pre-delivery checklist items

#### `design-context-and-direction-contract` — 优先修订

- 权限：`workspace-write`；8 维分 3/2/3/2/3/3/2/0（合计 18/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Flow and hierarchy before styling; every visual choice traced to authority or human taste decision.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case scoring traceability of choices. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source single-question product-context intake (pre-filled from codebase) is reduced to 'classify facts'. 建议：Add one consolidated intake question with inferred defaults. 证据：`skills/gstack/design-consultation/SKILL.md:672-711`
- **P2 trigger_precision**：Overlap 0.192 with visual-language-and-anti-template-controls; contract vs implementation split not named in anti-triggers. 建议：Add anti-trigger to visual-language for implementing the visual grammar. 证据：`curation/v2/skill-audit/static-scan.json`
- 来源中丢失的技法：single consolidated context question pre-filled from codebase

#### `design-system-foundation-and-token-extraction` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 负向（平 / 负）
- 优点：Reuse first; no parallel system or alias maze.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with an existing token set that already covers the need. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Source brief-to-official-design-system map (when to use an official package instead of inventing CSS) is absent. 建议：Add 'prefer official system package when brief matches' step. 证据：`skills/design-taste-frontend/SKILL.md:82-120`
- 来源中丢失的技法：brief to official design-system map；rendered-system extraction over DESIGN.md claims

#### `divergent-prototyping-and-variant-selection` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Structural divergence required; human selects; never auto-promote.
- **P2 source_fidelity**：Source verify-before-present step (every variant renders, interactions respond, console clean) and in-page variant picker are not required. 建议：Require a clean-console render check per variant before comparison. 证据：`skills/prototype/SKILL.md:59-73; skills/prototype/PICKER.md:140-197`
- 来源中丢失的技法：variant picker harness；flip through all variants before showing user

#### `evidence-based-ui-review-and-release-gates` — 改进

- 权限：`workspace-write`；8 维分 3/2/3/3/3/3/1/3（合计 21/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Rejects stale or self-attested evidence; four-value disposition.；Both holdouts are candidate wins.
- **P1 boundary**：Absorbs cross-domain-ui-preflight-checklists per merge recommendation; also overlaps rendered-ui-critique (0.255) on disposition. Critique should produce findings; this Skill should own the release gate only. 建议：Remove disposition from rendered-ui-critique or make this Skill consume its findings exclusively. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Sources are an em-dash ban and a prototype hand-off; no release-gate technique. 建议：Mark as authored. 证据：`skills/design-taste-frontend/SKILL.md:685-703; skills/prototype/SKILL.md:59-73`

#### `existing-interface-redesign-and-preservation` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/3/3/3/2/2（合计 22/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Preserve/migrate/replace/remove decisions with owners; SEO and analytics invariants.
- **P2 source_fidelity**：Source redesign mode detection (greenfield vs redesign-preserve vs overhaul) is called the single biggest source of bad output; the Skill assumes a preserve mode without classifying. 建议：Add mode classification as step 1. 证据：`skills/design-taste-frontend/SKILL.md:783-833`
- 来源中丢失的技法：redesign mode detection

#### `external-design-token-extraction-and-normalization` — 改进

- 权限：`workspace-write`；8 维分 3/2/3/3/3/2/1/0（合计 17/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：Observed external values are evidence, not authority; provenance per primitive.
- **P1 permission_fit**：Named 'external read' in coverage yet step 2 forbids browsing or fetching and the identity is workspace-write; the Skill cannot acquire the capture it needs, and the source tool (npx extract-design-system <url>) is unusable. 建议：Either declare external-read for one authorized URL via the source tool, or route acquisition explicitly to a capture capability. 证据：`slots/v2/1.0.0/skills/external-design-token-extraction-and-normalization/SKILL.md:29,47; skills/extract-design-system/SKILL.md:39-50`
- **P2 measured_efficacy**：Both holdouts tie. 建议：Phase D case. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- 来源中丢失的技法：extract-only vs starter files mode；results are initialization, not pixel-perfect reproduction

#### `interaction-states-forms-and-navigation` — 保留

- 权限：`workspace-write`；8 维分 2/3/3/3/3/3/2/1（合计 20/24）；语义裁决 keep；执行 A/B 无增益（平 / 平）
- 优点：Exhaustive state list; preserves user input through failures; happy path alone cannot pass.
- **P2 source_fidelity**：Touch target minimums (44pt / 48dp, 8px spacing) and the console-error hook during flow walks are not carried. 建议：Add target-size defaults and console error capture in step 5. 证据：`skills/ui-ux-pro-max/references/quick-reference.md:35-54; skills/gstack/design-review/SKILL.md:1192-1231`
- **P2 boundary**：Both defines and implements; broad but coherent. Acceptable. 建议：None required. 证据：`SKILL.md:10`
- 来源中丢失的技法：touch target size minimums

#### `purposeful-motion-and-animation-engineering` — 保留

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/2（合计 21/24）；语义裁决 keep；执行 A/B 有效（胜 / 平）
- 优点：Interruption, reduced motion with information equivalence, deterministic end state.
- **P2 source_fidelity**：Transform/opacity-only rule and motion token guidance are not stated. 建议：Add as default implementation rule. 证据：`skills/ui-ux-pro-max/references/quick-reference.md:134-161`
- 来源中丢失的技法：animate transform/opacity only

#### `rendered-ui-critique-and-release-disposition` — 改进

- 权限：`artifact-write-local-exec-external-read`；8 维分 2/2/3/3/3/3/2/1（合计 19/24）；语义裁决 improve；执行 A/B 有效（胜 / 胜）
- 优点：One reproducible finding per issue; real renders only.
- **P1 boundary**：Issues a release disposition, duplicating evidence-based-ui-review-and-release-gates. 建议：Rename to rendered-ui-critique; output findings only and hand off disposition. 证据：`SKILL.md:32; curation/v2/skill-audit/static-scan.json`
- **P2 source_fidelity**：Source 10-category, ~80-item design audit checklist with high/medium/polish impact is reduced to a one-line list. 建议：Embed category list and impact scale. 证据：`skills/gstack/design-review/SKILL.md:1065-1104`
- 来源中丢失的技法：10-category design audit checklist；high/medium/polish impact rating

#### `responsive-layout-and-spatial-composition` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/0（合计 19/24）；语义裁决 improve；执行 A/B 负向（负 / 平）
- 优点：Intermediate widths, 200% zoom and long content required.
- **P1 measured_efficacy**：Both holdouts tie. 建议：Phase D case with intermediate-width breakage. 证据：`evals/runs/capability-compiler-v2/phase-9/grading-report.json`
- **P2 source_fidelity**：Hard layout rules (hero fits viewport, headline max 2 lines, never disable zoom, 16px body minimum) are dropped. 建议：Add as default constraints. 证据：`skills/design-taste-frontend/SKILL.md:234-261; skills/ui-ux-pro-max/references/quick-reference.md:93-113`
- 来源中丢失的技法：hero fits initial viewport；never disable zoom；16px body minimum

#### `ui-review-scope-and-evidence-acquisition` — 优先修订

- 权限：`artifact-write-local-exec-external-read`；8 维分 3/3/3/3/3/3/2/1（合计 21/24）；语义裁决 keep；执行 A/B 负向（负 / 负）
- 优点：Route-state-viewport-theme-input-motion matrix; capture provenance binding.
- **P2 source_fidelity**：Source offers test-runner commands from ecosystem markers but never runs a guessed command; the Skill says 'approved local commands' without the offer-not-run rule. 建议：State: unknown capture commands are proposed, not executed. 证据：`skills/gstack/design-review/SKILL.md:590-629`

#### `ui-task-routing-and-governance` — 改进

- 权限：`workspace-write`；8 维分 3/1/3/2/3/2/2/3（合计 19/24）；语义裁决 improve；执行 A/B 无增益（平 / 平）
- 优点：Nine-way UI intent classification; both holdouts are candidate wins.
- **P1 trigger_precision**：Overlap 0.381 with context-intake-and-routing without mutual anti-trigger. 建议：Add anti-trigger: non-UI or mixed-domain intake routes to context-intake-and-routing. 证据：`curation/v2/skill-audit/static-scan.json`
- **P2 permission_fit**：workspace-write for a Skill that only routes; context-intake-and-routing is read-only for the same job. 建议：Align to read-only. 证据：`slots/v2/1.0.0/skills/ui-task-routing-and-governance/contract.json`

#### `visual-language-and-anti-template-controls` — 优先修订

- 权限：`workspace-write`；8 维分 3/3/3/2/3/3/2/3（合计 22/24）；语义裁决 keep；执行 A/B 互有胜负（胜 / 负）
- 优点：Named generic patterns to remove; taste alternatives preserved for humans.；Both holdouts are candidate wins.
- **P2 source_fidelity**：Source AI-tells list (no neon glow, no pure #000, desaturated accents) and 'defaults not bans, the brief can earn any of them' nuance are partly dropped. 建议：Add the tells list with the brief-can-earn-it exception. 证据：`skills/design-taste-frontend/SKILL.md:595-684; skills/impeccable/reference/craft-floor.md:19-44`
- 来源中丢失的技法：AI-tell visual pattern list

## 证据位置

- 审核合同：`.specs/capability-compiler-v2/skill-audit/plan.md`、`phase-d-design.md`
- 静态扫描：`curation/v2/skill-audit/static-scan.json`
- 语义审核：`curation/v2/skill-audit/semantic/*.json`
- 执行 A/B：`evals/runs/capability-compiler-v2/skill-audit/phase-d/`（含 task-set、每次调用的 prompt/输出/receipt）
- 被拒的试点与失败记录：`phase-d-pilot-1/finding.json`、`phase-d/gen-failed/`、`curation/v2/skill-audit/failures/`
- 汇总 ledger：`curation/v2/skill-audit/ledger.json`
