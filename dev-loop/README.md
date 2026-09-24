# Dev Loop 研发闭环

基于 Capability Compiler 发布契约的六步研发工作流编排器。

```text
用户意图 -> released recipe -> released slot contract -> 可验证产物
```

## 它是什么

`dev-loop` 只负责路由、传递、Gate、状态和证据生命周期：

- 根据完整闭环、接力或单步意图选择 `recipes/` 中的 released recipe；
- 按 recipe 的步骤、映射和精确版本引用调用 `slots/` 中的 released contract；
- 保留上游字段、未知项、来源、权限和稳定 ID；
- 在 `needs-input`、`failed` 或 `blocked` 时停止下游；
- 在上游改变时使旧证据失效并从受影响步骤重跑；
- 保持 QA 只报不修，并把复盘输出映射为下一轮需求输入。

它不直接调用原始 `skills/`，不复制 slot 方法，也不提供自产或未验证平替。

## Recipe 入口

| 意图 | Recipe |
|---|---|
| 需求或 PRD | `recipes/write-prd.json` |
| Web 流程设计 | `recipes/design-web-flow.json` |
| TDD 功能实现 | `recipes/build-feature-tdd.json` |
| 只做 QA | `recipes/qa-only.json` |
| 发布交付 | `recipes/ship-release.json` |
| 复盘回流需求 | `recipes/retro-to-requirements.json` |
| 完整研发闭环 | `recipes/full-dev-loop.json` |

只有 recipe 自身、其 release evidence 以及全部依赖 slot 都验证为 released 时才可执行。否则返回 `blocked`；若 recipe 已发布但缺少 contract 要求的必要输入，则返回 `needs-input`。

详细路由和替换规则见 `skills/dev-loop/references/routing.md`；阶段职责与 Gate 边界见 `skills/dev-loop/references/stages.md`。

## 状态记录

`.workflow/state.md` 记录当前 recipe/version、每个 slot/version、输入哈希、产物和证据路径、四态结果以及失效原因。文件存在或人工撰写 PASS 不能替代实际 Gate 证据。

## 当前安全行为

在 Capability Compiler 尚无 released recipes 或 released slots 时，插件必须明确 `blocked`。这表示路由保护正常工作，不代表流程或能力已经发布。
