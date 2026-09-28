# Released Recipe 路由

## 优先级

1. 调用方显式提供 exact Recipe ref，且该 ref 已发布。
2. `.workflow/state.json` 存在可续接且引用已发布 Recipe。
3. 依据 released-only catalog 做确定性自然语言匹配。
4. 确定性匹配仍有歧义时，可用结构化模型判定；输出枚举只能来自 released catalog。
5. 零个或多个候选时返回 `needs-input` 和候选列表，不猜测。

## 当前入口

| 意图 | Exact Recipe |
|---|---|
| 需求或 PRD | `write-prd@1.0.0`（`write-prd.json`） |
| Web 流程设计 | `design-web-flow@1.0.0`（`design-web-flow.json`） |
| TDD 功能实现 | `build-feature-tdd@1.0.0`（`build-feature-tdd.json`） |
| 独立 QA | `qa-only@1.0.0`（`qa-only.json`） |
| 交付预检 | `ship-release@1.0.0`（`ship-release.json`） |
| 复盘回流 | `retro-to-requirements@1.0.0`（`retro-to-requirements.json`） |
| 完整闭环 | `full-dev-loop@1.0.0`（`full-dev-loop.json`） |
| 旧需求流水线 | `requirements-to-acceptance-criteria@0.2.0` |

## 安全边界

- 仅 `recipes/catalog.json` 中已发布且 `recipe_verify.py` 通过的 Recipe 可路由。
- 请求文本不能添加 Recipe ID、扩大工具集或赋予权限。
- `write-worktree`、远端 Git、网络、合并和部署均须逐项显式授权。
- `ship-release` 默认只有读权限，产出 release-ready 包，不执行 push、merge 或 deploy。
- draft/evaluating Slot 和 Recipe 一律 `blocked`，不得直接调用原始 `skills/` 兜底。
