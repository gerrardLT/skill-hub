# Phase 1 Plan：逐来源深读、原子能力补全与语义关系审计

## 目标

将 Phase 0 的来源清单升级为逐 root 可审计的语义理解，并为每个能力簇建立完整的来源比较、关系与裁决证据。

## 非目标

- 不发布 V2 Skills。
- 不把 source-index skeleton 冒充融合 Skill。
- 不在本阶段设计最终生命周期 Recipe。
- 不修改原始 `skills/` 或 V1 released 资产。

## 上下文匹配

Phase 0 已复算：139 roots、2,337 source files；64 roots/597 files 已有 coverage 声明，75 roots/1,740 files 未覆盖；965 canonical Units 已聚类，114 auxiliary Units 未进入 canonical cluster set；88 clusters 仅有 15 条显式语义关系；82 Slots 是 draft skeleton。

## 输入与前置 Gate

- Phase 0 baseline/gaps/report
- 原始 `skills/` 与来源 hashes
- `curation/coverage.json`、dossiers、units、clusters、decisions
- V2 工程合同

Phase 0 Gate 必须通过，V1 compatibility manifest 必须保持不变。

## 子阶段与任务

### 1A：来源阅读账本

1. 为 139 roots 建 V2 root record。
2. 所有 `SKILL.md` 标为 `semantic-read`，记录 hash、frontmatter、章节结构与 root 归属。
3. 对 references/scripts/templates/examples/assets/vendor/generated 文件逐项判定：`semantic-read`、`behavior-reviewed` 或 `excluded`。
4. `excluded` 必须有具体 reason code 与说明；脚本不可仅凭扩展名排除。
5. 建立 2,337 文件的完整 V2 coverage ledger。

### 1B：Root dossiers

每个 root dossier 至少记录：

- 触发条件与适用场景
- 单一职责与非职责
- 输入与输出
- 核心方法和阶段
- 工具、脚本与外部依赖
- 权限与副作用
- 强项、独有方法、薄弱点
- 失败模式、反模式与停机条件
- 可复用单位候选
- 与父/子 root 的关系

### 1C：Unit 统一

1. 将 114 auxiliary Units 转为 canonical schema。
2. 验证原文位置与 excerpt。
3. 与 965 canonical Units 做精确和语义去重。
4. 每个 auxiliary Unit 必须有 merge/supersede/retain/defer/exclude 决策。
5. 更新 V2-only unit ledger，不改 V1 canonical data。

### 1D：同类比较矩阵

每个 cluster 生成：

- 来源列表及其贡献 Units
- capability dimensions
- 每个来源在各 dimension 的做法、优势、限制、证据
- 缺失维度
- 推荐融合规则

### 1E：关系、冲突与裁决

逐 cluster 显式记录 duplicate、complementary、conditional-variant、conflict、strong-dependency。每个 conflict 必须有 retain/merge/branch/reject 裁决；每个 variant 必须有适用条件。

### 1F：Phase Gate

- 139/139 root dossiers
- 139/139 `SKILL.md` semantic-read
- 2,337/2,337 files classified
- 114/114 auxiliary Units disposed
- 88/88 cluster comparison matrices
- 88/88 cluster relationship audits
- unresolved conflicts = 0
- V1 asset drift = 0

## 文件边界

允许修改：

- `.specs/capability-compiler-v2/phase-1/`
- `curation/v2/coverage.json`
- `curation/v2/dossiers/`
- `curation/v2/units/`
- `curation/v2/comparisons/`
- `curation/v2/relationships.json`
- `curation/v2/decisions.jsonl`
- `tools/curation/v2_*`
- `tests/curation/test_v2_*`

只读：`skills/`、V1 `slots/`、V1 `recipes/`、V1 curation facts。

## 产物

- 完整 file ledger
- 139 root dossiers
- canonical V2 unit ledger
- 88 comparison matrices
- relationships 与 decisions
- Phase 1 report 和可重复 Gate

## 验收策略

机械事实以脚本复算；语义内容按抽样反查 source excerpt、完整字段和 cluster dimensions；关系覆盖必须按 cluster 声明完成，不以全局少量示例代替。

## 风险与未知

- 大量平台/vendor 支持文件可能不贡献通用方法；仍须具体分类。
- 60 个 gstack embedded roots 与 11 个 dd-apm embedded roots可能共享父目录文件，ledger 应允许一文件服务多个 root，但物理文件只计一次。
- 同义 Unit 的语义去重不能只靠文本 hash；需保留人工/模型裁决证据。

当前无须用户裁决。

## 失败与失效

任一 root 未读、文件未分类、Unit 无处置、cluster 无矩阵或冲突无裁决，Phase 1 不得通过。来源 hash 变化使相关 dossier、Units、comparison 和下游 V2 evidence 全部失效。
