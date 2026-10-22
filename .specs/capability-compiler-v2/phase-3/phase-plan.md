# Phase 3 Plan：提纯并验证产品发现与需求 Skills

## 目标

把 Phase 2 冻结的 31 个 Phase 3 owning capabilities 重写为本项目自有、来源可追踪、单一职责、可独立触发且可供后续 Recipe 编排的 V2 candidate Skills，覆盖治理 intake、产品发现、证据研究、策略与优先级、需求、计划和评审决策。每个候选须有机器可验证的 contract、provenance、trigger/anti-trigger cases、evaluation plan 和至少一个能发现关键删改的 mutation check。

## 非目标

- 不修改或发布 V1 `slots/`、`recipes/`、`dev-loop/`。
- 不在本阶段创建 Phase 4–7 的 UI、architecture、implementation 或 deployment Skills。
- 不把产品发现、研究、优先级、requirements、plan reviews 重新拼成单一巨型 Skill；跨能力顺序留给 Phase 8 Recipes。
- 不在本阶段执行外部访谈、客户数据访问、外部 LLM Judge、网络写入、remote Git、PR、merge 或 deploy。
- 不把静态 test-case definitions 冒充 Phase 9 的真实模型 baseline/candidate/holdout 运行证据。
- 不把 `evaluating` candidate 写入 released recipe 或宣称已发布。

## 当前仓库上下文

Phase 2 已通过并冻结：

- 11 domains、15 stages、13 mandatory handoffs。
- 157 candidate capability contracts；Phase 3 ownership 恰为 31 项。
- 88 legacy clusters、965 canonical Units、104 retained auxiliary Units、1,138 root-derived records 和 4 个 semantically reviewed support fragments 已有唯一、可追踪决策。
- 1,244 fusion decisions；dependency graph 为 99 hard、110 optional、40 feedback；0 hard cycle、0 isolated capability。
- review/repair、preflight/remote change、observation/rollback、workspace/artifact/local-system writes 已分离。
- 全仓 20 Gates、272 tests 通过；source drift=0、V1 asset drift=0。
- Phase 2 artifact manifest：169 artifacts，tree SHA-256 `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`。

Phase 3 candidate 路径采用：

`evals/candidates/capability-compiler-v2/phase-3/skills/<capability-id>/`

此路径与 V1 released assets 平行；Phase 9 评测、Phase 10 人工语义评审和 Phase 12 最终批准前，不复制到 `slots/`。

## 输入与前置 Gate

- `GOAL.v2.md`
- `.specs/capability-compiler-v2/goal-contract.md`
- `.specs/capability-compiler-v2/phase-2/artifact-manifest.json`
- `.specs/capability-compiler-v2/phase-2/phase-report.json`
- `curation/v2/lifecycle/phase-ownership.json`
- `curation/v2/lifecycle/dependencies.json`
- `curation/v2/capabilities/*.json`
- `curation/v2/fusion/decisions.jsonl`
- `curation/v2/fusion-policy.json`
- Phase 1 dossiers、comparisons、Units 和只读 `skills/`

前置要求：

```bash
python tools/curation/v2_phase2_gate.py --workspace-root .
```

必须通过，且 Phase 2 artifact tree hash 必须与本计划所列 identity 一致。

## 冻结能力清单

Phase 3 只处理 `curation/v2/lifecycle/phase-ownership.json` 中 phase `3` 的 31 个 IDs：

- `capability:ai-product-opportunity-and-wedge`
- `capability:competitive-case-library`
- `capability:competitive-response-and-monitoring`
- `capability:context-intake-and-routing`
- `capability:customer-interview-execution`
- `capability:data-analysis-validation`
- `capability:decision-and-outcome-roadmapping`
- `capability:design-plan-review`
- `capability:developer-experience-plan-review`
- `capability:document-and-artifact-governance`
- `capability:documentation-authoring`
- `capability:evidence-synthesis-and-opportunity-prioritization`
- `capability:executive-plan-review`
- `capability:facilitation-and-collaboration-protocols`
- `capability:implementation-planning-and-handoff`
- `capability:independent-plan-review`
- `capability:market-positioning-and-competitive-power`
- `capability:market-segmentation-and-demand-intelligence`
- `capability:opportunity-prioritization-and-frameworks`
- `capability:persona-jtbd-and-journey-modeling`
- `capability:plan-review-decision-synthesis`
- `capability:problem-framing-and-customer-research`
- `capability:qualitative-evidence-synthesis`
- `capability:requirements-and-delivery-contract`
- `capability:research-planning-and-governance`
- `capability:results-analysis-and-decision-readout`
- `capability:risk-preflight-and-safety-governance`
- `capability:solution-hypothesis-and-experiment-design`
- `capability:strategic-choice-and-differentiation`
- `capability:structural-power-and-moats`
- `capability:workflow-orchestration-and-lifecycle`

清单漂移、重复、漏项或越界纳入其他 owning phase 均使 Gate 失败。

## 子阶段与顺序

### 3A：冻结输入与 candidate schema

1. 复核 Phase 2 manifest、31 IDs、dependency edges 与 permission identities。
2. 建立 V2 candidate contract/provenance/trigger/evaluation schemas；保持 V1 schema 与 released assets 不变。
3. 定义稳定版本 `0.1.0-v2-candidate`、状态 `evaluating` 和 candidate catalog。
4. 为 `workspace-write` 与 `read-only` 建不同 execution identity；产品建议不得持有产品批准权。

### 3B：按职责族提纯 Skills

按下列职责族逐项重写，但每项保持独立 Skill：

1. intake 与治理：context routing、research governance、risk preflight、artifact governance。
2. discovery evidence：problem framing、interviews、qualitative synthesis、data validation、persona/JTBD/journey、market segmentation、competitive evidence。
3. hypothesis 与 strategy：solution hypothesis、AI wedge、positioning、structural power、strategic choice、competitive response。
4. prioritization 与 decisions：evidence synthesis、named frameworks、results readout、outcome roadmap；GO/PIVOT/KILL 只输出建议，最终决定归人。
5. requirements 与 planning：requirements contract、implementation handoff、facilitation、documentation。
6. independent plan lenses：general、executive、design、DX reviews；review 与 plan mutation/approval 分离。
7. synthesis 与 routing：decision synthesis、workflow routing；只编排/合成，不执行下游能力。

每个 `SKILL.md` 至少包含：trigger、anti-trigger、responsibility、required inputs、procedure、output contract、hard gates、stop/status mapping、data-governance boundary、non-responsibilities 和 handoff。

### 3C：provenance 与条件变体

1. 从 Phase 2 contract 复制并复核 source clusters、canonical/auxiliary/root-derived units、support fragments 和 fusion decisions。
2. 每个引用须双向可追到 Phase 1/2 evidence；不得生成无来源 methodology。
3. RICE、ICE、Opportunity Score 等保留命名变体；每次使用必须声明 exact formula、变量定义、假设和所选 variant。
4. aesthetic/taste decisions 保持人类裁决；plan review 只提出证据化建议。
5. 访谈、客户/专有数据、录音和 external Judge 缺授权、最小化、脱敏、保留、外传或删除边界时返回 `needs-input` 或 `blocked`。

### 3D：trigger 与 anti-trigger contracts

每个 Skill 至少定义：

- 2 个 should-trigger cases。
- 2 个 should-not-trigger cases，至少一个与相邻 Phase 3 Skill 区分。
- 1 个 boundary/needs-input case。
- 1 个 authority or data-governance stop case（若适用）。

Gate 检查 case identity、预期 Skill、禁止 Skill、理由和输入 fixture；Phase 9 才执行真实 routing/model runs。

### 3E：evaluation plans 与本阶段 checks

每个 Skill 建立冻结 evaluation plan：

- baseline：最接近的 V1 Slot、source Skill 或无能力 baseline，须明确身份。
- candidate：本阶段 candidate version/hash。
- holdout：与 authored examples 措辞不同的 case IDs。
- mutation：至少一个删除 hard gate、边界、unknown preservation、formula declaration、human authority 或 data-governance rule 后应失败的 case。
- rubric：主观 outputs 使用证据、未知保留、边界、可执行性和人类决策权；客观 contracts 使用 schema/trace/identity assertions。

本阶段只验证 plans、fixtures、hashes、trigger matrices 和 deterministic mutation detectors 完整可执行；真实模型输出、工具事件、命令证据和 candidate-vs-baseline 改进由 Phase 9 生成。

### 3F：Phase Gate

同时满足：

- 31/31 owning capabilities 恰好各有一个 candidate Skill。
- 每项有 `SKILL.md`、`contract.json`、`provenance.json`、`trigger-cases.json`、`evaluation-plan.json`。
- candidate contract 通过 schema，状态均为 `evaluating`，版本精确一致。
- provenance 覆盖 capability 的全部 source IDs、fusion decisions 和 source evidence，无未知引用。
- trigger/anti-trigger 数量与相邻边界完整，无 duplicate case IDs。
- 31/31 evaluation plans 含 baseline/candidate/holdout/mutation，且不冒充已执行 evidence。
- named formula、human-owned product decision、data governance、review-only identities 和 source defect policies 无违反。
- Phase 3 ownership 之外 candidate count=0；V1/source drift=0。
- Phase 2 Gate、Phase 3 Gate、全部 tests、统一 runner 与 `git diff --check` 通过。

## 允许修改

- `.specs/capability-compiler-v2/phase-3/`
- `curation/v2/phase-3/`
- `evals/candidates/capability-compiler-v2/phase-3/`
- `evals/cases/capability-compiler-v2/phase-3/`
- `tools/curation/v2_*`
- `tests/curation/test_v2_*`
- `tools/curation/run_all_gates.py`（仅接入 Phase 3 Gate）
- `GOAL.v2.md`
- `.specs/capability-compiler-v2/goal-contract.md`

## 只读路径

- `skills/`
- V1 `slots/`、`recipes/`、`dev-loop/`
- Phase 0–2 已冻结 evidence 与 manifests；若发现错误须生成 supersession，不覆盖历史事实。
- Phase 4–7 owning capability candidate paths。

## 预期产物与稳定 ID

- `curation/v2/phase-3/candidate-skill.schema.json`
- `curation/v2/phase-3/provenance.schema.json`
- `curation/v2/phase-3/trigger-cases.schema.json`
- `curation/v2/phase-3/evaluation-plan.schema.json`
- `curation/v2/phase-3/designs.json`
- `evals/candidates/capability-compiler-v2/phase-3/catalog.json`
- `evals/candidates/capability-compiler-v2/phase-3/skills/<id>/SKILL.md`
- `evals/candidates/capability-compiler-v2/phase-3/skills/<id>/contract.json`
- `evals/candidates/capability-compiler-v2/phase-3/skills/<id>/provenance.json`
- `evals/candidates/capability-compiler-v2/phase-3/skills/<id>/trigger-cases.json`
- `evals/candidates/capability-compiler-v2/phase-3/skills/<id>/evaluation-plan.json`
- `.specs/capability-compiler-v2/phase-3/gate-report.json`
- `.specs/capability-compiler-v2/phase-3/artifact-manifest.json`
- `.specs/capability-compiler-v2/phase-3/phase-report.json`

Skill ID 使用 Phase 2 capability slug；case ID 使用 `V2-P3-<skill>-<kind>-NN`；mutation ID 使用 `V2-P3-MUT-<skill>-NN`。

## 验收命令与阈值

```bash
python tools/curation/v2_phase2_gate.py --workspace-root .
python tools/curation/v2_compile_phase3_skills.py --workspace-root .
python tools/curation/v2_phase3_gate.py --workspace-root . --output .specs/capability-compiler-v2/phase-3/gate-report.json
python -m pytest -q tests/curation -k "v2 and phase3"
python tools/curation/run_all_gates.py --workspace-root . --output curation/gate-report.json
python tools/curation/v2_phase3_report.py --workspace-root . --pytest-summary "<fresh>" --repository-gate-count <fresh>
git diff --check
```

阈值采用 3F 全部条件；aggregate count 不能替代逐 ID equality、source reference、trigger boundary 或 mutation checks。

## 人工语义抽样

本阶段在机器 Gate 前由主流程至少逐项抽样：

- problem framing 与 solution hypothesis 不互相越界。
- interview/data/feedback Skills 遵守 data-governance Gate。
- RICE、ICE、Opportunity Score 不混成无名公式。
- evidence synthesis、prioritization、roadmap 与 human GO/PIVOT/KILL authority 分离。
- requirements、implementation plan 和 plan reviews 不互相吞并。
- executive/design/DX/general review lenses 保留独立差异与只读身份。
- workflow orchestration 不执行下游工作。

## 风险与未知

- Phase 2 的 31 项中含多个相邻 product methods；若只替换名词生成模板，会重造 source-index skeleton。须为每项写具体 procedure 与 anti-trigger。
- 既有 V1 `problem-framing`、`requirements-and-delivery-contract` 可作 baseline，但不得复制其 release status 或陈旧 evidence。
- 产品与设计建议多属主观产物；本阶段只能冻结 rubric 和 cases，不能冒充 Phase 9 人工/模型评测。
- 31 Skills 全部一次性发布会放大 routing collision；trigger matrix 必须先证明边界，Phase 8 再做 recipe routing。

当前无须用户新增裁决：产品最终决策权、数据治理、formula variants、V1/V2 并行和发布顺序均已有机器化政策。

## 失败回滚与证据失效

- Phase 3 仅写并行 candidate 路径；失败时删除本阶段候选即可，不影响 V1 或 Phase 2 taxonomy。
- Phase 2 artifact tree、ownership、capability contract、fusion decision 或 source hash 变化，使关联 candidate Skill、trigger cases、evaluation plan 和 Phase 3 manifest 失效。
- 任一 Skill 缺 provenance、职责不原子、trigger 与相邻 Skill 冲突、越过人类产品决定或绕过 data governance，Phase 3 Gate 必须失败。
- 不通过 Phase 3 Gate，不进入 Phase 4。
