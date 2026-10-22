# Phase 0 Plan：全量来源与现有产物真实性复核

## 目标

建立 V2 的可重复事实 baseline。此阶段只验证“有什么、读了什么、拆了什么、融合到了什么程度”，不提纯、不发布任何新 Skill。

## 非目标

- 不重写 Skills。
- 不调整能力域。
- 不修改 V1 released Slots/Recipes。
- 不运行远端、网络、merge 或 deploy。

## 上下文匹配

当前机器报告声称：139 Skill roots、64 catalog skills、597 个 coverage 文件记录、965 个纳入 Units、88 clusters、92 Slots、10 released Slots、8 released Recipes。另有 57 个 Unit 文件及若干补充 Units；必须解释物理计数和 Gate 计数的差异。82 个 Slot 明示为 draft source-index skeleton，不能计入已融合成品。

## 输入与依赖

- `skills/` 只读快照与 `skills-lock.json`
- `curation/inventory.json`
- `curation/coverage.json`
- `curation/dossiers/`
- `curation/units/`
- `curation/clusters.json`
- `curation/decisions.jsonl`
- `slots/`、`recipes/`
- `curation/gate-report.json`

前置 Gate：现有 V1 全量 Gate 通过；V2 合同已获用户批准。

## 任务拆分

1. 从磁盘重新枚举 Skill roots、文件和内容 hash，不依赖旧计数。
2. 对照 inventory 与 lock，报告 missing/untracked/changed roots。
3. 对 coverage 中每个文件验证路径、状态、理由和可读取性。
4. 加载所有 dossier 与 Units，验证来源摘录位置及物理/纳入/补充计数。
5. 验证 cluster identity、Unit 唯一归属、依赖与 relationship 覆盖率。
6. 分类 92 Slots：released、evaluating、draft-skeleton；计算来源多样性与是否存在融合方法正文。
7. 冻结 V1 资产 hash，后续阶段以此检测兼容性漂移。
8. 生成 baseline、gap report 和 Phase 0 Gate。
9. 添加自动测试：磁盘漂移、未登记 root、缺失 coverage 文件、模糊状态、V1 漂移必须失败。

## 文件边界

允许修改：

- `.specs/capability-compiler-v2/phase-0/`
- `tools/curation/v2_phase0_audit.py`
- `tests/curation/test_v2_phase0_audit.py`

只读：

- `skills/`
- `slots/`
- `recipes/`
- 现有 `curation/` 资产

## 产物

- `.specs/capability-compiler-v2/phase-0/baseline.json`
- `.specs/capability-compiler-v2/phase-0/gaps.json`
- `.specs/capability-compiler-v2/phase-0/phase-report.json`
- V1 compatibility hash manifest
- 可重复 Phase 0 Gate 与测试

## 验收

- 139 roots 均能由磁盘和 inventory 对应解释。
- 未登记 root = 0；missing root = 0；changed locked root = 0。
- Coverage 中未分类文件 = 0；登记却缺失文件 = 0。
- Unit 物理数、纳入数、deferred/supplement 数均明确解释。
- 纳入 Unit 的重复 ID、悬空、重复 cluster assignment 均为 0。
- 92 Slots 全部有真实分类；draft skeleton 不得计为 purified。
- V1 released asset hash manifest 完整且后续可复算。
- 新增测试全绿，现有 Gate 无回归。

## 风险与未知

- Inventory 的 139 roots 包含顶层和嵌套 roots，不能用目录名简单去重。
- coverage 的 read/excluded 是声明，Phase 0 只能验证文件身份与声明一致；语义阅读质量留给 Phase 1。
- 额外 Units 可能来自 supplements 或历史 pilot，须分类而非删除。

当前没有需要用户裁决的未知项。

## 失败与证据失效

任一来源、coverage 或 V1 hash 不可解释时，Phase 0 失败，后续阶段不得启动。若审计工具本身修改只读路径，立即停止并恢复该改动。
