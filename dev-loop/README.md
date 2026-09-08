# Dev Loop 研发闭环

六步研发工作流编排器，轻量、原生、极简的 Qoder 插件。

```text
①需求 → ②设计 → ③实现 → ④验收 → ⑤交付 → ⑥复盘 ─┐
  ↑                                              │
  └──────────── 经验回流，开启下一轮 ←────────────┘
```

## 它是什么

一个专精于**研发闭环总控**的元编排器（`dev-loop`）：
- **不硬编码具体方法论**：自己不做笨重实现，只负责**路由、传递、把关、记忆**；
- **直连 Qoder 成熟核心能力**：无缝调度本地已装的成熟插件（`superpowers`、`ui-ux-pro-max`、`product-management`、`playwright` 等），不搞复杂的外部仓库全家桶；
- **硬 Gate 把关**：每一步必须满足严格的输入/输出验收标准方可进入下一步；
- **轻量状态记忆**：基于项目本地的 `.workflow/state.md` 进行断点接力与决策追踪；
- **灵活调用**：可从头到尾跑完整研发全生命周期闭环，也可按需单步独立调用。

## 六步极简路由矩阵

| 研发步骤 | 核心调度能力 | 职责定位与核心产出 |
|---|---|---|
| **① 需求** | `product-management:PRD生成` | 需求分析、用户痛点与 Given/When/Then 验收标准 → `docs/prd.md` |
| **② 设计** | `ui-ux-pro-max-skill:ui-ux-pro-max` | 页面信息架构、异常态覆盖（空/载/错/权）与样式系统 → `docs/design.md` |
| **③ 实现** | `superpowers:writing-plans` + `test-driven-development` | 任务拆解、测试先行与高质量编码实现 → `src/` + 自动化单测 |
| **④ 验收** | `playwright` + `superpowers:verification-before-completion` | 独立运行、浏览器端到端走查与证据校验（只报不修） → `docs/qa-report.md` |
| **⑤ 交付** | `shipping-artifacts` | 系统架构说明、数据链路、环境变量清单与部署指南 → `docs/` 交付集 + `README.md` |
| **⑥ 复盘** | `superpowers:systematic-debugging` + `product-management:产品指标复盘` | 真实运行复盘、指标差距归因，输出下一轮需求项 → `docs/retro.md` 回流至 ① |

> 详细阶段定义与 Gate 准则见 [references/stages.md](skills/dev-loop/references/stages.md)。

## 常用触发方式

- **全流程闭环**："从 0 开始做一个个人记账小工具" / "按 dev-loop 跑完整流程"；
- **断点接力推进**："继续上次的项目" / "dev-loop 下一步"（自动读取当前项目的 `.workflow/state.md`）；
- **单步独立调用**："只帮我把这个需求整理成 PRD" / "只对这个页面做端到端验收走查"。

## 项目状态文件（`.workflow/state.md`）

运行时自动维护在目标项目根目录下：
```markdown
# Dev Loop 状态
项目：<项目名称>                最近更新：2026-09-08
当前步：③ 实现（进行中）

## 产物索引
① 需求  docs/prd.md ✅
② 设计  docs/design.md ✅
③ 实现  src/ （进行中）
④ 验收  —
⑤ 交付  —
⑥ 复盘  —

## 决策记录
- [2026-09-08] 设计选型确定为沉浸式暗色模式，覆盖空状态与加载态

## 下一步
- 完成主流程端到端单测与业务实现
```
