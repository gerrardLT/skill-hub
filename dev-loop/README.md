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

`.workflow/state.json` 是机器事实源，记录 recipe/version、step ref、输入哈希、产物、证据、尝试次数、失败指纹及失效历史；`.workflow/state.md` 由 JSON 自动生成，仅供阅读。状态写入使用原子替换；损坏状态保留诊断副本并返回 `blocked`。

## 当前发布路径

- `write-prd@1.0.0`
- `design-web-flow@1.0.0`
- `build-feature-tdd@1.0.0`
- `qa-only@1.0.0`
- `ship-release@1.0.0`
- `retro-to-requirements@1.0.0`
- `full-dev-loop@1.0.0`
- 兼容入口：`requirements-to-acceptance-criteria@0.2.0`

## 安全行为

- 歧义返回 `needs-input`，不猜测。
- QA 只报不修。
- 代码写入仅在显式授权的隔离 worktree 中发生。
- 远端 Git、网络、合并与部署须分别显式授权。
- `ship-release` 默认只生成 release-ready 包，不 push、merge 或 deploy。
