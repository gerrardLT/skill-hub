# Dev Loop 研发闭环

六步研发工作流编排器，打包为 Qoder 插件。

```text
①需求 → ②设计 → ③实现 → ④验收 → ⑤交付 → ⑥复盘 ─┐
  ↑                                              │
  └──────────── 经验回流，开启下一轮 ←────────────┘
```

## 它是什么

一个轻量总控 skill（`dev-loop`）：不实现任何方法论，只做四件事——**路由**到环境中最合适的已安装 skill、把上游产物**传递**给下游、执行一句话 **Gate** 把关、维护 `.workflow/state.md` **记忆**。可整条闭环跑，也可只用其中任意一步。

## 安装

将本目录（`dev-loop/`）放入 Qoder 插件目录（如 `~/.qoder/plugins/`）。

## 用法

- **全闭环**："帮我从 0 做一个记账小工具" → 从①走到⑥；
- **接力**："继续上次的项目" → 按状态文件从断点继续；
- **单步**："只做设计走查" / "只做验收" → 直接进对应步骤。

每步详细路由与场景备选见 [skills/dev-loop/references/routing.md](skills/dev-loop/references/routing.md)。

## 路由的 skill（可选依赖）

未安装任何外部 skill 也能跑——每步有内置兜底指引，产物标注 `⚠️ 降级执行`。

| 步 | 主要路由目标 |
|----|--------------|
| ① 需求 | `product-management:PRD生成`（备选：产品脑暴 / 用户故事拆解 / 需求优先级排序 / 竞品分析） |
| ② 设计 | `product-design:brief` → `flow-web` / `flow-mobile`（备选：sitemap / board / chart / edge / impeccable） |
| ③ 实现 | 主 agent 直接编码（辅助：`context7:context7-mcp` / `sql-queries` / `dummy-dataset`） |
| ④ 验收 | `product-design:qa`（备选：`design-review:*` 系列 / `test-case-generator` / `intended-vs-implemented`） |
| ⑤ 交付 | `shipping-artifacts`（备选：`product-design:prd`） |
| ⑥ 复盘 | `product-design:retro`（备选：`product-management:产品指标复盘` / 用户反馈分析 / 路线图更新） |

## 状态文件

工作状态写在目标项目的 `.workflow/state.md`（纯 markdown，人类可直接编辑）：当前步、六步产物索引、决策记录、下一步动作。删除该文件即重置流程。
