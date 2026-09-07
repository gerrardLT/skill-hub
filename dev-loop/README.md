# Dev Loop 研发闭环

六步研发工作流编排器，打包为 Qoder 插件。以 **68 个开源顶流 Skills 体系** 为核心执行骨架（PostHog 移除后精简）。

```text
①需求 → ②设计 → ③实现 → ④验收 → ⑤交付 → ⑥复盘 ─┐
  ↑                                              │
  └──────────── 经验回流，开启下一轮 ←────────────┘
```

## 它是什么

一个轻量总控 skill（`dev-loop`）：不硬编码任何具体方法论，只做四件事——**路由**到严选的 68 个开源顶流 Skills、把上游产物**传递**给下游、执行一句话 **Gate** 把关、维护 `.workflow/state.md` **轻量记忆**。可整条闭环运行，也可单步独立调用。

## 核心骨架：68 个开源 Skills 体系

全部精选自 GitHub 顶级开源项目（deanpeters、phuryn、impeccable、superpowers、gstack 等），按六域划分，每域 10 个候选 + 8 个观测 Provider 适配器：

| 步骤 | 默认 Core 组合（开源第一顺位） | 来源仓库 | 本地已装插件平替 |
|------|------------------------------|---------|------------------|
| **① 需求** | `prd-development` + `discovery-process` + `prioritization-frameworks` | `deanpeters/Product-Manager-Skills`, `phuryn/pm-skills` | `product-management:PRD生成` |
| **② 设计** | `impeccable` + `ui-ux-pro-max` + `web-design-guidelines` | `pbakaus/impeccable`, `nextlevelbuilder/ui-ux-pro-max-skill` | `product-design:brief` → `flow-web` |
| **③ 实现** | `writing-plans` + `test-driven-development` + `systematic-debugging` | `obra/superpowers` | `superpowers:*` |
| **④ 验收** | `testing-strategy` + `verification-before-completion` + `qa-only` | `anthropics/knowledge-work-plugins`, `garrytan/gstack` | `product-design:qa` |
| **⑤ 交付** | `ship` + `github-actions-hardening` | `garrytan/gstack`, `github/awesome-copilot` | `shipping-artifacts` |
| **⑥ 复盘** | `systematic-debugging` + `analyzing-user-feedback` + `retro` | `obra/superpowers`, `refoundai/lenny-skills`, `garrytan/gstack` | `product-design:retro` |

完整 68 个技能清单、适用场景与 Provider 适配器（Sentry/Datadog）见 [skills/dev-loop/references/routing.md](skills/dev-loop/references/routing.md)。

安装状态与版本锁定见 [SKILLS.md](SKILLS.md)、[skills.lock.json](skills.lock.json)；一键恢复用 [restore-skills.sh](restore-skills.sh)。

## 安装外部开源 Skill

支持通过 `npx skills add` 按需安装任意候选：

```bash
# PM 域核心
npx skills add deanpeters/Product-Manager-Skills --skill prd-development -y
npx skills add phuryn/pm-skills --skill prioritization-frameworks -y

# 设计域核心
npx skills add pbakaus/impeccable --skill impeccable -y
npx skills add nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max -y

# 工程与验收核心（superpowers 套件）
npx skills add obra/superpowers --skill test-driven-development -y
npx skills add garrytan/gstack --skill qa-only -y
```

> **未安装时也不中断**：自动降级走本地已装市场插件，两类均无时走内置 1 页纸兜底指引并标注 `⚠️ 降级执行`。

## 用法

- **全闭环**："帮我从 0 做一个记账小工具" → 从①走到⑥；
- **接力**："继续上次的项目" → 按状态文件从断点继续；
- **单步**："只写 PRD" / "只做设计走查" / "只做验收" → 直接进对应步骤。

## 状态文件

工作状态写在目标项目的 `.workflow/state.md`（纯 markdown）：当前步、六步产物索引、决策记录、下一步动作。
