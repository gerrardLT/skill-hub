# Phase 2 Plan：按软件生命周期重构能力域与融合规范

## 目标

把 Phase 1 的全量来源证据重构为 V2 独立候选 taxonomy：覆盖从产品发现到生产复盘的完整软件生命周期，并为每个候选能力定义单一职责、生命周期位置、权限身份、输入输出、条件变体、融合规则、依赖与来源追踪。

## 非目标

- 不在本阶段写最终 V2 `SKILL.md`。
- 不发布 Slots、Recipes 或修改 released V1 资产。
- 不把 930 个 deferred root atoms 直接塞入旧 88 clusters。
- 不把 gstack/runtime boilerplate、平台命令或 vendor 配方提升为通用能力。
- 不执行远端 Git、云资源变更、真实部署或外部系统写入。

## 当前仓库上下文

Phase 1 已通过七层 Gate：

- 139/139 roots 有 dossiers，2,337/2,337 files 已分类。
- 965 canonical Units 已在旧 88 clusters；104 auxiliary Units 已 retain，2 merge，8 因来源支持不足而 defer。
- 旧 canonical Units 只覆盖 49 roots；其余 90 roots 已提取 1,138 条 exact-source records，208 条 exact duplicates 已 merge，留下 930 个 distinct deferred atoms。
- 88 comparisons、232 source-pair audits、17 explicit relationships、0 unresolved conflicts。
- 七项用户融合政策已机器化。
- 全仓 19 Gates、261 tests 通过；V1/source drift=0。

Phase 2 的核心问题不是继续提取，而是将“88 个旧 clusters + 104 retained auxiliary + 930 distinct deferred atoms”重构为职责清晰、生命周期完整、可供 Phase 3–7 分域提纯的 V2 capability catalog。

## 输入与前置 Gate

- `GOAL.v2.md`
- `.specs/capability-compiler-v2/goal-contract.md`
- `.specs/capability-compiler-v2/phase-1/phase-report.json`
- `.specs/capability-compiler-v2/phase-1/artifact-manifest.json`
- `curation/v2/dossiers/`
- `curation/v2/comparisons/`
- `curation/v2/relationships.json`
- `curation/v2/units/auxiliary.json`
- `curation/v2/units/root-derived.json`
- `curation/v2/fusion-policy.json`
- 只读 `curation/clusters.json`、`curation/units/`、`skills/`

前置要求：`python tools/curation/v2_phase1_gate.py --workspace-root .` 必须通过。

## 生命周期 taxonomy

使用稳定域 ID；能力 ID 不绑定来源 Skill 名：

1. `domain:product-discovery-and-strategy`
2. `domain:requirements-and-planning`
3. `domain:ux-ui-and-accessibility`
4. `domain:architecture-data-api-and-security`
5. `domain:implementation-and-code-quality`
6. `domain:testing-and-quality-assurance`
7. `domain:performance-and-reliability`
8. `domain:delivery-deployment-and-release`
9. `domain:observability-operations-and-incidents`
10. `domain:learning-retrospective-and-governance`
11. `domain:tool-runtime-and-artifact-support`

第 11 域只容纳执行支持能力；不得被包装成用户可见业务能力。

## 子阶段与顺序

### 2A：建立 lifecycle schema 与 coverage baseline

1. 建立 domains、stages、permission identities 与 capability schema。
2. 冻结 Phase 1 输入 identities/hashes。
3. 为 88 旧 clusters 逐项映射一个 primary domain 与一个 lifecycle stage。
4. 检查完整生命周期是否有空域、空阶段或职责重叠。

### 2B：分类 930 distinct deferred root atoms

1. 以 root dossier、exact source slice、标题与副作用为证据分类。
2. 每个 representative atom 必须：
   - 指向现有 V2 candidate capability；或
   - 指向新 candidate capability；或
   - 明确 defer/exclude，并给具体理由。
3. 208 exact-merge records 继承 target 的分类，不重复计数。
4. gstack shared runtime、session preamble、telemetry、artifact sync 与 setup mechanics 保留为 tool/runtime support，不复制到每个业务能力。
5. 平台专用实现保留 provider variant，不误抽象为唯一云标准。

### 2C：重构 candidate capabilities

对每个 capability 记录：

- 稳定 `capability_id`
- primary domain / stage
- 单一职责与非职责
- 输入、输出、完成证据
- permission identity：`read-only`、`workspace-write`、`workspace-write-local-exec`、`workspace-write-external-read`、`local-exec`、`local-exec-external-read`、`external-read`、`local-system-write-authorized-only`、`remote-write-authorized-only`
- hard gates 与 stop conditions
- 来源 clusters / canonical Units / auxiliary Units / root-derived atoms
- duplicate merge、complement、conditional variant、conflict resolution
- provider/framework variants 与适用条件
- 上下游依赖
- Phase 3–7 owning phase

### 2D：融合政策与条件变体

强制应用：

- 巨型来源拆为原子 capabilities；来源 Skill 仅作为 provenance 或 Recipe 候选。
- 只有 accessibility、safety、security、performance、data governance、evidence integrity、authorization 可成为全局硬规则。
- 审美规则为 context-selected variants。
- 产品 GO/PIVOT/KILL、路线与建设批准由人决定。
- 客户/专有/录音/外部 judge 数据强制 data-governance Gate。
- RICE、ICE、Opportunity Score 等必须记录命名公式变体。
- remote write、merge、deploy 只在当次明确授权下可用。
- review-only 与 fix-capable 权限身份不得融合为同一个执行模式。

### 2E：依赖图与阶段 handoff

1. 建立 lifecycle stage DAG。
2. 为 capability 建强依赖与可选依赖。
3. 定义跨阶段 handoff artifacts 与 invalidation 规则。
4. 检测循环依赖、孤立能力、越权依赖与阶段倒置。
5. 将 Phase 3–7 各自 owning capabilities 冻结为输入清单。

### 2F：Phase Gate

必须同时满足：

- 11/11 domains、所有 mandatory lifecycle stages 均有职责定义。
- 88/88 legacy clusters 恰好映射一个 primary capability。
- 965 canonical Units + 104 retained auxiliary Units 恰好归属一个 primary capability。
- 930/930 distinct root-derived atoms 有 assign/defer/exclude 决策。
- 208/208 exact merges 可追到已分类 target。
- 8/8 unsupported auxiliary summaries 保持 defer，不得偷渡。
- 每个 capability 有完整 contract、provenance、permission identity、fusion decisions 与 owning phase。
- review-only / write / remote-write 权限边界无冲突。
- policy violations = 0；unresolved conflicts = 0；dependency cycles = 0；orphan capabilities = 0。
- V1/source drift = 0。

## 允许修改

- `.specs/capability-compiler-v2/phase-2/`
- `curation/v2/lifecycle/`
- `curation/v2/capabilities/`
- `curation/v2/fusion/`
- `tools/curation/v2_*`
- `tests/curation/test_v2_*`
- `GOAL.v2.md`
- `.specs/capability-compiler-v2/goal-contract.md`
- `tools/curation/run_all_gates.py`（仅接入 Phase 2 Gate）

## 只读路径

- `skills/`
- V1 `slots/`、`recipes/`、`dev-loop/`
- `curation/clusters.json`
- `curation/units/`
- Phase 0/1 已冻结输入 evidence（若需更正，须生成 supersession，不覆盖历史事实）

## 预期产物与稳定 ID

- `curation/v2/lifecycle/domains.json`
- `curation/v2/lifecycle/stages.json`
- `curation/v2/lifecycle/cluster-map.json`
- `curation/v2/lifecycle/root-atom-map.json`
- `curation/v2/lifecycle/dependencies.json`
- `curation/v2/capabilities/catalog.json`
- `curation/v2/capabilities/<capability-id>.json`
- `curation/v2/fusion/decisions.jsonl`
- `.specs/capability-compiler-v2/phase-2/gate-report.json`
- `.specs/capability-compiler-v2/phase-2/artifact-manifest.json`
- `.specs/capability-compiler-v2/phase-2/phase-report.json`

ID 格式：`capability:<kebab-case>`、`domain:<kebab-case>`、`stage:<NN>-<kebab-case>`、`V2-FUSION-<NNNN>`。

## 验收命令与阈值

```bash
python tools/curation/v2_phase1_gate.py --workspace-root .
python tools/curation/v2_phase2_gate.py --workspace-root .
python -m pytest -q tests/curation/test_v2_*.py
python tools/curation/run_all_gates.py --workspace-root . --output curation/gate-report.json
git diff --check
```

量化阈值采用 2F 全部条件；不得以 aggregate count 替代逐 ID coverage。

人工语义抽样至少覆盖：

- 产品发现与人类决策权
- 完整 UX/UI 与 contextual aesthetics
- 架构/data/API/security
- TDD/代码评审/独立 QA 权限分离
- performance/reliability
- deploy/canary/rollback/incident response
- Datadog/Sentry/Azure/Vercel/Cloudflare provider variants
- gstack runtime/tool support 与用户可见能力分离

## 风险与未知

- 930 个 deferred atoms 中约 640 来自 gstack；若按标题机械建能力会重造巨型 Skill 或复制 runtime boilerplate。
- 平台 Skills 高度 provider-specific；应保留 adapter variants，而非制造虚假的 provider-neutral 实现。
- 旧 88 clusters 偏向此前 49 roots，不能作为最终 taxonomy 的数量或边界约束。
- 旧 Units 的 source summaries 可作为比较证据，但最终 capability contract 必须回到 exact source citations 与 Phase 1 dossiers。

当前无须用户新增裁决：权限、产品决策、数据治理、公式变体、审美规则和部署边界均已有批准政策。

## 失败回滚与证据失效

- Phase 2 仅写 V2 并行路径；失败时删除本阶段候选产物即可，不影响 V1。
- 任一 Phase 1 hash、dossier、Unit disposition 或 comparison 变化，使相关 capability mapping、fusion decisions、dependency graph 与 Phase 3–7 输入清单失效。
- 任一 capability 无来源、无 permission identity、跨 incompatible execution identities、或依赖图成环，Phase 2 Gate 必须失败。
- 不通过 Phase 2 Gate，不进入 Phase 3。
