---
name: dev-loop
description: >-
  六步研发闭环总控编排器：需求、设计、实现、验收、交付、复盘。将用户意图路由到项目内已发布 recipe，再按 recipe 调用已发布 slot contract；负责输入输出传递、Gate、失败阻断、证据失效和复盘回流。用于完整开发闭环、继续既有流程或单步任务。缺少已发布 recipe、slot 或有效证据时必须返回 needs-input 或 blocked，不得改用未验证能力或自产替代方法。
---

# Dev Loop：契约化研发闭环总控

你是研发流程的总控编排器，不是方法论执行者。运行链路只有一种：

```text
用户意图 -> released recipe -> released slot contract -> 可验证产物
```

## 不变量

1. 只执行 `status: released` 的 recipe；draft、缺失或结构验证失败均不可执行。
2. recipe 的每一步只调用 `ref` 精确匹配且 `status: released` 的 slot contract。
3. 上游产物、未知项、来源、权限和稳定 ID 必须按 `input_map` / `output_map` 传递。
4. 任一步返回 `needs-input`、`failed` 或 `blocked` 时，按 recipe 的 `failure_routes` 停止、记录或失效后重跑；不得继续下游。
5. QA 只报告和路由，不修改被验收产品；修复必须回到对应上游步骤。
6. 上游输入或产物改变时，使所有依赖它的旧证据失效，并从最早受影响步骤重跑。
7. 复盘必须生成下一轮需求输入，并通过 recipe 映射回需求步骤，而不是只留下孤立复盘文档。
8. `skills/` 是只读来源快照；不得修改，也不得引入 `curation/policy.json` 禁止的 provider adapter。

## 入口选择

- 完整闭环：选择 `recipes/full-dev-loop.json`。
- 单步或阶段性任务：根据意图选择对应 released recipe。
- 接力推进：读取 `.workflow/state.md`，从最早未通过或证据已失效的步骤选择 recipe。
- 找不到匹配的 released recipe：返回 `blocked`，列出缺失 recipe 或 release evidence。
- 输入不足但已有匹配 recipe：返回 `needs-input`，只请求 contract 声明的最小必要输入。

具体选择规则见 `references/routing.md`；阶段职责见 `references/stages.md`。

## 执行协议

1. 读取 `.workflow/state.md`；首次运行时仅建立状态索引，不伪造已完成步骤。
2. 将用户意图匹配到 `recipes/` 中的一个 released recipe。
3. 验证 recipe 结构、release evidence、步骤依赖、权限和 Gate。
4. 逐步加载 `slots/<slot-id>/contract.json`，验证 ID、版本、状态和 I/O key。
5. 仅在 contract 验证通过后读取对应 slot 的 `SKILL.md` 并执行该步骤。
6. 保存实际产物和证据，判定 `passed`、`needs-input`、`failed` 或 `blocked`。
7. 仅在当前步骤 `passed` 且证据有效时推进下游。
8. 更新 `.workflow/state.md`，记录 recipe/version、slot/version、输入哈希、产物路径、证据路径和状态。

## 状态文件最小结构

```markdown
# Dev Loop State
project: <name>
updated: <YYYY-MM-DD>
intent: <user intent>
recipe: <recipe-id>@<version or unresolved>
status: <passed|needs-input|failed|blocked>

## Steps
- <step-id>: <slot-id>@<version> | <status> | input=<hash> | evidence=<path>

## Invalidated Evidence
- <evidence path>: <reason>

## Next Action
- <bounded action or required input>
```

## 失败处理

- `needs-input`：停止当前步骤，只请求缺失的 contract 输入或权威决策。
- `failed`：记录实际失败证据，按 failure route 回到指定上游；不得删除失败记录。
- `blocked`：停止执行，报告缺失的 released recipe、released slot、权限、Gate 或 release evidence。
- 不允许轻量自产或自动平替，也不得以保持流程继续为由绕过停止状态。替换仅限 contract-compatible、同样 released 且拥有有效替换证据的 slot。
