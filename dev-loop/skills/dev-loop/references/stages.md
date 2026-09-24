# 六步职责与 Gate 边界

阶段名称帮助解释流程，但可执行细节以 released recipe 和其引用的 released slot contract 为准。本文不指定来源 Skill，也不提供绕过 contract 的兜底方法。

## 共同规则

- 输入、输出、权限和 Gate 使用 recipe/contract 中的机器可读 key，不凭本文扩展。
- 当前步骤只有在状态为 `passed` 且证据有效时才能推进。
- `needs-input`、`failed`、`blocked` 都必须停止下游并执行 recipe 的 failure route。
- 未知项、来源、稳定 ID 和权威边界跨步骤原样保留。
- 上游哈希变化使依赖它的旧证据失效。

## ① 需求

- **职责**：将已知事实、产品意图、假设、冲突和未知项分离，形成可追溯需求与验收条件。
- **预期 recipe**：`recipes/write-prd.json`。
- **Gate 关注**：证据可追溯、关键规则保留、未知项不被猜测、验收标准可执行、权限和范围不越界。
- **失败语义**：缺少关键产品决策时为 `needs-input`；权威规则冲突时为 `blocked`。

## ② 设计

- **职责**：把已通过的需求 contract 映射为流程、状态、界面边界和设计证据。
- **预期 recipe**：`recipes/design-web-flow.json`。
- **Gate 关注**：需求 ID 完整映射，主路径和适用的空、载、错、权、边界及恢复状态有证据。
- **失败语义**：需求 Gate 未通过或必要状态无权威定义时停止，不自行补写产品政策。

## ③ 实现

- **职责**：依据通过的需求和设计 contract 实施测试先行的最小变更。
- **预期 recipe**：`recipes/build-feature-tdd.json`。
- **Gate 关注**：实际 RED/GREEN 证据、范围纪律、关键规则不回归、测试结果可重跑。
- **失败语义**：实现或测试失败记为 `failed` 并回到实现步骤；上游 contract 变化先使旧证据失效。

## ④ 验收

- **职责**：独立验证实现与需求、设计 contract 的一致性。
- **预期 recipe**：`recipes/qa-only.json`。
- **Gate 关注**：逐条验收证据、阻断缺陷、关键路径和适用边界。
- **只报不修**：QA 不修改产品源码、需求或设计；问题通过 failure route 返回责任上游。

## ⑤ 交付

- **职责**：在前置 Gate 全部通过后组织可接手、可审查、可发布的交付证据。
- **预期 recipe**：`recipes/ship-release.json`。
- **Gate 关注**：构建与测试可复现、配置和权限明确、已知限制诚实、发布依据存在。
- **失败语义**：缺少任一前置证据时为 `blocked`，不得用清单或说明文档代替运行证据。

## ⑥ 复盘

- **职责**：比较 Expected 与 Actual，记录证据支持的差距和决策，并生成下一轮需求输入。
- **预期 recipe**：`recipes/retro-to-requirements.json`。
- **Gate 关注**：根因有证据、结论不越界、至少一个结构化 next-requirements 输出由步骤生产。
- **闭环语义**：next-requirements 通过 `output_map` 成为下一轮需求步骤输入；输入变化后旧需求链证据必须失效并重跑。

## 完整闭环

`recipes/full-dev-loop.json` 组合以上阶段。单步和全闭环必须引用相同 slot contract；完整闭环不得内联方法正文，也不得在某阶段不可用时直接调用原始 `skills/`。
