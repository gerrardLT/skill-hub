# Capability Compiler 进度

更新日期：2026-09-15

## 总体状态

**未完成。** 当前权威完成审计仍为 `not-complete`，禁止声明全部交付完成。

| 阶段 | Gate 状态 | 交付状态 | 说明 |
|---|---|---|---|
| Phase 1 | passed | 已完成 | `skills/` 基线已冻结并可机械验证。 |
| Phase 2 | passed | 已完成 | 资产、来源、依赖和平台边界已完成对账；禁止 provider 未进入运行资产。 |
| Phase 3 | passed | 已完成 | 49 个 included sources、15 个 deferred sources、965 个 semantic units 已完成验证。 |
| Phase 4 | passed | 已完成 | 965 个 units 已 exactly-once 分配到 88 个 clusters，无未处理冲突或悬空引用。 |
| Phase 5 | failed | 进行中 | iteration-2 candidate 正在冻结前评测；完整 Gate 5 证据链尚未形成。 |
| Phase 6 | passed | 部分可用 | 88 个 clusters 均已有最终 `unreleased` 处置，但 released slots 仍为 0。 |
| Phase 7 | failed | 未完成 | released slots 为 0，七个正式 recipes 和组合运行证据不存在。 |
| Phase 8 | failed | 部分完成 | dev-loop 静态路由和两个本地副本同步已验证，但没有 released runtime path。 |

## 已完成

### Phase 1：原始资产冻结

- 已建立 `curation/policy.json`，记录只读原料、状态、硬失败、平台延期和禁入规则。
- 已建立 `curation/baseline.json`，保存 `skills/` 的文件、字节数和 SHA-256 基线。
- source verifier 最近记录为 `added=[]`、`changed=[]`、`removed=[]`。
- `skills/` 保持只读，未使用网络、未安装依赖、未执行第三方 Skill 脚本。

### Phase 2：资产底账与边界

- 68 个 catalog entries 与物理入口、别名、suite 和补充材料已对账。
- 来源、许可证、附件引用、命令、MCP、网络、凭据和安装依赖均有显式状态。
- 15 个平台专用来源保持 `deferred-platform`，不进入运行 recipes。
- 禁止 provider 的内容扫描结果为空；禁令本身保留在 policy/audit 文档中。

### Phase 3：全量来源拆解

- 已完成 49 个 included sources 的 dossiers 和逐字、可定位 semantic units。
- 已验证 965 个 semantic units。
- 15 个 deferred-platform sources 已有范围 dossier 和 coverage 处置。
- required attachment、行号、逐字摘录和阅读覆盖的已知缺口均已修复。

### Phase 4：能力地图与决策

- 已建立 88 个能力 clusters。
- 965 个 included units 均有 exactly-once 去向。
- duplicate、conflict、conditional variant、strong dependency 和 loss risk 已记录在 `curation/decisions.jsonl`。
- 当前 verifier 无 duplicate、dangling、unassigned 或 unhandled-overlap 错误。

### Phase 5：已经具备的基础证据

- rubric、tuning cases、iteration-1 formal holdout 和 eval manifest 已落盘。
- 四个 pilot slots 的 method、contract 和 provenance 已物化。
- pilot structural provenance verifier 已通过：4 个 slots、54 个 mapped units。
- iteration-1 candidate freeze 仍有效：12 个文件，SHA-256 和 byte count 可重算。
- 五项 mutation 均能被 Gate 检出。
- downstream handoff 已验证 17/17 stable IDs 保留。
- benchmark token/duration 已与 agent notification timing 对齐。
- 官方 skill-creator Viewer 已生成，并在真实浏览器中验证无 console error/warning。
- iteration-2 candidate 已与 canonical frozen slots 隔离在 `evals/candidates/requirements-to-ac/0.2.0-candidate/`。
- iteration-2 tuning pass 1 已保留 12 个真实 candidate/baseline runs，读取闭包审计为 12/12 无污染。
- pass 1 candidate 状态匹配 5/6，baseline 状态匹配 6/6；失败记录未删除或替换。
- t01 的最小规则修订诊断已真实返回 `Status: passed`，并保存 notification timing。

### Phase 6：处置覆盖

- 88 个通用 clusters 均已有 materialized slot 和最终处置记录。
- 当前统计：88 个 `draft`、88 个 `unreleased`、0 个 `released`。
- Gate 6 通过仅证明 materialization/disposition coverage 完整，不代表这些 slots 已获得语义发布资格。

### Phase 8：已经完成的静态接入

- dev-loop 路由已改为：`intent -> released recipe -> exact released slot contract`。
- 无 released recipe 时会 fail closed，不回退到原始 `skills/` 或自产方法。
- 两个 Qoder 本地副本已同步并通过逐文件 SHA-256 校验：2 个 targets、11 个 checked files、0 errors。
- 最近记录的全量离线测试为 `158 passed in 42.40s`。
- 最近记录的全树 JSON 解析为 531 个文件、0 invalid。

## 进行中

### Phase 5 iteration-2 冻结前评测

当前正在处理 `evals/runs/requirements-to-ac/iteration-2/pre-freeze-tuning-pass-2/`：

- 已保存 t01 的 `full_output.md`、`tool_evidence.raw.json` 和 `timing.json`。
- t01 当前输出状态为 `passed`，与 tuning case 的 expected status 一致。
- raw evidence 声明严格离线、无网络、未修改 skills，并列出配置中的 8 个 candidate `SKILL.md`/`contract.json`。
- 仍需机械重算 8 个当前 source file hashes，并生成规范化 `tool_evidence.json` 与 `run.json`。
- 完成单例诊断验证后，必须运行最终完整的 6 对 candidate/baseline paired tuning；不能只凭 t01 诊断冻结 candidate。

## 未完成

### Phase 5：完整 Gate 5

1. 规范化并机械验证 pass-2 t01 diagnostic evidence。
2. 同批运行最终 6 个 candidate 与 6 个 baseline tuning cases。
3. 验证全部 candidate status 与 expected status 匹配，并保留全部失败和 excluded runs。
4. 将最终 tuning evidence 加入四个 candidate provenance 文件。
5. 生成 iteration-2 的 12-file candidate freeze，并重算每个 SHA-256 和 byte count。
6. freeze 后创建一套全新的 iteration-2 formal holdout；iteration-1 h01-h06 已成为 tuning evidence，禁止复用为未见 holdout。
7. 同环境运行 candidate/baseline formal holdout。
8. 对波动 case 获取至少 verifier 要求数量的有效 paired repeated runs，并生成 variance report。
9. 基于 frozen candidate 重跑 mutation 和 downstream handoff。
10. 使用 notification timing 生成官方 benchmark。
11. 使用 skill-creator 官方 generator 生成并验证 Viewer。
12. 完成 blind human semantic review。
13. 获取真实用户通过 Viewer 提交的 `feedback.json`；禁止自动生成或推断人工反馈。
14. 只有上述证据全部通过后，才能把相应 pilot slots 从 `evaluating/unreleased` 改为 `released`。

### Phase 6：可执行 slots

- released slots 当前为 0。
- 四个 pilot slots 仍等待完整 Gate 5 和人工评审。
- 其余 84 个 slots 均明确保持 unreleased；若 recipes 依赖它们，必须分别补齐 rubric、baseline、candidate、holdout、mutation 和 review evidence 后才能发布。
- 不得通过直接修改 release-status JSON 绕过评测。

### Phase 7：recipes 与组合验证

以下七个 required recipe 文件尚不存在：

- `recipes/write-prd.json`
- `recipes/design-web-flow.json`
- `recipes/build-feature-tdd.json`
- `recipes/qa-only.json`
- `recipes/ship-release.json`
- `recipes/retro-to-requirements.json`
- `recipes/full-dev-loop.json`

仍需完成：

- recipes 只能引用 exact-version released slot contracts。
- 创建 `evals/cases/composition/` 与 `evals/runs/composition/`。
- 验证输入输出映射、stable IDs、unknown preservation 和 provenance 传递。
- 验证 `needs-input`、`failed`、`blocked` 均阻断下游执行。
- 验证 contract-compatible replacement。
- 验证上游输入变化使下游旧证据失效。
- 验证 QA 只报告、不修复产品源码。
- 验证 retro 输出成为下一轮 requirements input。

### Phase 8：真实运行与终验

- released recipe 数量仍为 0，真实 runtime 当前正确结果为 `blocked`。
- Gate 5/6/7 满足后，需执行真实 `intent -> recipe -> slot contract -> artifact` 端到端运行。
- 运行资产变化后需重新同步两个本地 Qoder 副本并重算 SHA-256。
- 需重新执行 source baseline、禁入扫描、JSON parse、全部 verifier、mutation、composition 和 pytest。
- 需更新 `curation/prompt-to-artifact-checklist.json`、`curation/final-audit.json` 和 `SKILLS.md`。
- 只有 final audit 无缺口且 `completion_claim_allowed=true` 时，才能声明全部完成。

## 当前阻断链

```text
Phase 5 完整语义证据与人工反馈
  -> 发布满足证据要求的 slots
  -> 构建并发布只引用 released slots 的 recipes
  -> 执行真实 dev-loop runtime
  -> 重新同步与全量终验
  -> 允许完成声明
```

## 权威证据

- 实施计划：`docs/superpowers/plans/2026-09-09-capability-compiler-implementation.md`
- 完成审计：`curation/final-audit.json`
- Prompt 映射：`curation/prompt-to-artifact-checklist.json`
- Slot 状态：`curation/slot-release-status.json`
- 本地同步审计：`curation/dev-loop-sync-audit.json`
- iteration-2 candidate：`evals/candidates/requirements-to-ac/0.2.0-candidate/`
- iteration-2 当前运行：`evals/runs/requirements-to-ac/iteration-2/`

## 更新规则

- 只根据已落盘、可解析、可机械重算的证据更新“已完成”。
- `passed` 的结构 Gate 不自动等于语义发布。
- 自动通知不是用户确认或人工评审。
- failed/excluded runs 必须保留，不得选择性删除。
- frozen candidate、canonical slots 和 `skills/` 不得在对应冻结边界内修改。
- 本文是便于阅读的进度页；发生冲突时，以 `curation/final-audit.json` 和实际 verifier 输出为准。
