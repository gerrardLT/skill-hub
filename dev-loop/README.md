# Dev Loop 研发闭环

基于 Capability Compiler 发布契约的六步研发工作流编排器。六阶段目前为评测候选，尚未发布；仅 `requirements-to-acceptance-criteria@0.2.0` 可路由执行。

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
| 需求或 PRD | `evals/candidates/full-dev-loop/recipes/write-prd.json`（未发布） |
| Web 流程设计 | `evals/candidates/full-dev-loop/recipes/design-web-flow.json`（未发布） |
| TDD 功能实现 | `evals/candidates/full-dev-loop/recipes/build-feature-tdd.json`（未发布） |
| 只做 QA | `evals/candidates/full-dev-loop/recipes/qa-only.json`（未发布） |
| 发布交付 | `evals/candidates/full-dev-loop/recipes/ship-release.json`（未发布） |
| 复盘回流需求 | `evals/candidates/full-dev-loop/recipes/retro-to-requirements.json`（未发布） |
| 完整研发闭环 | `evals/candidates/full-dev-loop/recipes/full-dev-loop.json`（未发布） |

只有 recipe 自身、其 release evidence 以及全部依赖 slot 都验证为 released 时才可执行。否则返回 `blocked`；若 recipe 已发布但缺少 contract 要求的必要输入，则返回 `needs-input`。

详细路由和替换规则见 `skills/dev-loop/references/routing.md`；阶段职责与 Gate 边界见 `skills/dev-loop/references/stages.md`。

## 状态记录

`.workflow/state.json` 是机器事实源，记录 recipe/version、step ref、输入哈希、产物、证据、尝试次数、失败指纹及失效历史；`.workflow/state.md` 由 JSON 自动生成，仅供阅读。状态写入使用原子替换；损坏状态保留诊断副本并返回 `blocked`。

## 当前发布路径

- `requirements-to-acceptance-criteria@0.2.0`

六阶段候选不得由路由器执行。既有 `evals/runs/full-dev-loop/` 只含生成的通过声明，不能作为真实评测。

## 安全行为

- 歧义返回 `needs-input`，不猜测。
- QA 只报不修。
- 六阶段实现仍处评测中；不可视作生产级权限隔离。
- `bash` 可绕过工具名权限，网络、远端 Git 和部署的宿主强制隔离尚待实现与验证。
- `ship-release` 默认只生成 release-ready 包，不 push、merge 或 deploy。
