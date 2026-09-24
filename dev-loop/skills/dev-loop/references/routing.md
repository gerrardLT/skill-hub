# Released Recipe 路由表

`dev-loop` 不直接调度来源 Skill，也不复制 slot 方法。它只把意图路由到 `recipes/` 中验证通过的 released recipe，再按 recipe 的精确引用调用 released slot contract。

## 意图映射

| 用户意图 | Recipe 文件 | 缺失或未发布时 |
|---|---|---|
| 需求或 PRD | `recipes/write-prd.json` | `blocked` |
| Web 流程设计 | `recipes/design-web-flow.json` | `blocked` |
| TDD 功能实现 | `recipes/build-feature-tdd.json` | `blocked` |
| 只做 QA | `recipes/qa-only.json` | `blocked` |
| 发布交付 | `recipes/ship-release.json` | `blocked` |
| 复盘回流需求 | `recipes/retro-to-requirements.json` | `blocked` |
| 完整研发闭环 | `recipes/full-dev-loop.json` | `blocked` |

## 路由验证

选择 recipe 后依次验证：

1. recipe 文件存在、结构符合 `recipes/schema.json` 且 `status` 为 `released`。
2. `evidence.composition_runs` 和 `evidence.review` 指向真实存在的发布证据。
3. 每个 step 的 `slot` 存在，`ref` 精确匹配 contract `version`，contract `status` 为 `released`。
4. `input_map`、`output_map`、Gate 和权限均落在 slot contract 声明的边界内。
5. 依赖图无环；输入有外部来源或上游生产者；recipe 输出有步骤生产者。
6. failure route 完整处理 `needs-input`、`failed`、`blocked`，且采取 fail-closed action。

任一验证失败都返回 `blocked`，并报告具体 recipe、slot、字段或证据缺口。不得把 draft/unreleased artifact 当作可执行资源。

## 替换规则

替换 slot 不是自然平替。仅当候选替换满足以下条件时才允许：

- 同样为 `released`；
- contract 的输入、输出、Gate 和权限与 recipe 映射兼容；
- recipe 的 `ref` 已显式更新到该版本；
- 替换 composition test 与 review evidence 已通过；
- 旧的下游 evidence 已失效并重跑。

## 当前发布状态

若仓库中没有 released recipe 或其依赖的 released slots，`dev-loop` 必须返回 `blocked`。它可以列出需要完成的 Gate 和证据，但不能自产文档、调用原始 `skills/`、自动降级或继续下游。
