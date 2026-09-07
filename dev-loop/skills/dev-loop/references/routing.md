# 68 个开源 Skills 全景路由表

本表以 2026-09 严选的 **6 域 Top 10（60 个）+ 8 个 Provider Adapters = 68 个开源 Skills** 为第一顺位核心骨架。

- **优先调用**：第一列的核心开源 Skill（来源仓库明确，支持 `npx skills add <source> --skill <name>` 安装）；
- **已装平替**：若环境尚未安装该开源 skill，自动降级调用第二列的本地已装市场插件技能；
- **终极兜底**：两类均不可用时，走第三列编排器内置 1 页纸兜底。

---

## ① 需求（PM 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地市场插件平替 |
|---:|---|---|---|---|---|
| 1 | `prd-development` | `deanpeters/Product-Manager-Skills` | **core** | 证据到完整 PRD 端到端编排 | `product-management:PRD生成` |
| 2 | `product-strategy-session` | `deanpeters/Product-Manager-Skills` | **core** | 定位、问题、战略与路线综合推演 | `product-management:PRD生成` |
| 3 | `discovery-process` | `deanpeters/Product-Manager-Skills` | **core** | 问题假设、用户访谈、综合与验证 | `product-management:产品脑暴` |
| 4 | `prioritization-frameworks` | `phuryn/pm-skills` | **core** | 优先排序问题与机会，而非机械排功能 | `product-management:需求优先级排序` |
| 5 | `outcome-roadmap` | `phuryn/pm-skills` | **core** | 将 Feature Roadmap 转为 Outcome Roadmap | `product-management:路线图更新` |
| 6 | `competitive-strategy` | `refoundai/lenny-skills` | recommended | 竞争结构、替代选择、切换成本与持久优势 | `product-management:竞品分析` |
| 7 | `interview-script` | `phuryn/pm-skills` | recommended | 基于 Mom Test 的用户访谈大纲设计 | `product-design:probe` |
| 8 | `pre-mortem` | `phuryn/pm-skills` | recommended | 上线前反事实失败审查（Tigers/Elephants） | `product-design:check` |
| 9 | `metrics-dashboard` | `phuryn/pm-skills` | recommended | North Star、输入指标与护栏指标三链设计 | `product-design:metric` |
| 10 | `ai-product-strategy` | `refoundai/lenny-skills` | conditional | AI 产品能力、非确定性 UX 与模型边界 | `product-design:brief` |

**默认组合**：`discovery-process` → `prd-development` → `prioritization-frameworks`。  
**兜底**：自产 1 页 PRD（问题陈述、用户画像、核心场景、验收标准、非目标）。

---

## ② 设计（Design 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地市场插件平替 |
|---:|---|---|---|---|---|
| 1 | `impeccable` | `pbakaus/impeccable` | **core** | 主视觉导演：系统化审查、打磨与设计记忆 | `product-design:brief` + `flow-web` |
| 2 | `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | **core** | 跨 Web/Mobile 的 UI/UX 模式、组件与无障碍知识库 | `ui-ux-pro-max-skill:ui-ux-pro-max` |
| 3 | `web-design-guidelines` | `vercel-labs/agent-skills` | **core** | 以可用性与 Web 规范约束视觉实现 | `design-review:ui-designer` |
| 4 | `review-animations` | `emilkowalski/skills` | **core** | 独立审查动效时机、缓动、持续时间与性能 | `product-design:motion-plan` |
| 5 | `redesign-existing-projects` | `leonxlnx/taste-skill` | recommended | 对已有低质量界面做 audit-first 系统重设计 | `product-design:audit` |
| 6 | `web-accessibility` | `magnus919/agent-skills` | recommended | WCAG 2.2 语义、键盘、焦点、表单与动效验证 | `design-review:accessibility-review` |
| 7 | `prototype` | `emilkowalski/skills` | recommended | 并行生成不同交互方案并可视化比较 | `huashu-design` |
| 8 | `frontend-design` | `anthropics/skills` | conditional | 鲜明非模板化的 Greenfield 视觉生成 | `product-design:board` |
| 9 | `extract-design-system` | `arvindrk/extract-design-system` | conditional | 从公开页面提取设计原语用于迁移与研究 | `product-design:extract` |
| 10 | `design-taste-frontend` | `leonxlnx/taste-skill` | conditional | 品牌页/落地页的高变化度 anti-slop 视觉方向 | `product-design:board` |

**默认组合**：`impeccable`（主导演，唯一）+ `ui-ux-pro-max`（知识层）+ `web-design-guidelines`（规范约束）+ `review-animations`（动效把关）。  
**规则**：同一工作项只允许一个主视觉导演；不让多个设计 skill 互搏。  
**兜底**：自产 1 页设计规格（页面清单、每页关键状态、导航结构、交互要点）。

---

## ③ 实现（Engineering 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地环境辅助 |
|---:|---|---|---|---|---|
| 1 | `writing-plans` | `obra/superpowers` | **core** | 将规格拆成可验证的小步实施计划 | `superpowers:writing-plans` |
| 2 | `test-driven-development` | `obra/superpowers` | **core** | 强制红-绿-重构和回归证据 | `superpowers:test-driven-development` |
| 3 | `systematic-debugging` | `obra/superpowers` | **core** | 先定位根因，再实施单一修复 | `superpowers:systematic-debugging` |
| 4 | `requesting-code-review` | `obra/superpowers` | **core** | 使用独立上下文做代码审查 | `superpowers:requesting-code-review` |
| 5 | `verification-before-completion` | `obra/superpowers` | **core** | 完成声明前必须有新鲜验证证据 | `superpowers:verification-before-completion` |
| 6 | `executing-plans` | `obra/superpowers` | recommended | 按批次执行并在检查点复核 | `superpowers:executing-plans` |
| 7 | `subagent-driven-development` | `obra/superpowers` | recommended | 将独立任务分派给隔离上下文并逐项审查 | `superpowers:subagent-driven-development` |
| 8 | `improve-codebase-architecture` | `mattpocock/skills` | recommended | 发现架构摩擦与深模块重构机会 | `architecture-visualization:architecture-health` |
| 9 | `codebase-design` | `mattpocock/skills` | recommended | 设计深模块、接口边界、可测试性与接缝 | `architecture-visualization:system-modeler` |
| 10 | `git-guardrails-claude-code` | `mattpocock/skills` | conditional | Git 操作与提交安全护栏 | `superpowers:using-git-worktrees` |

**额外编码约束**：始终叠加 `andrej-karpathy-skills:karpathy-guidelines`（克制、外科手术式修改、可验证）。  
**兜底**：主 Agent 按 PRD 验收标准直接编写实现，并运行测试自验。

---

## ④ 验收（QA 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地市场插件平替 |
|---:|---|---|---|---|---|
| 1 | `testing-strategy` | `anthropics/knowledge-work-plugins` | **core** | 按业务风险设计测试层级、边界、环境与退出标准 | `product-design:qa` |
| 2 | `verification-before-completion` | `obra/superpowers` | **core** | 禁止没有新鲜可复现证据的完成/通过声明 | `superpowers:verification-before-completion` |
| 3 | `qa-only` | `garrytan/gstack` | **core** | 独立的 report-only Web QA：截图/复现/健康分，不改源码 | `product-design:qa` |
| 4 | `code-review` | `anthropics/knowledge-work-plugins` | **core** | 从正确性/安全/性能/可维护性独立审查变更 | `superpowers:receiving-code-review` |
| 5 | `playwright` | `openai/skills` | **core** | 真实浏览器交互、快照、截图、UI 流程与运行时证据 | `playwright` |
| 6 | `playwright-best-practices` | `currents-dev/playwright-best-practices` | recommended | E2E、flaky、fixtures、selector 和 CI 模式 | `test-case-generator` |
| 7 | `web-accessibility` | `magnus919/agent-skills` | recommended | WCAG 2.2 导向的可访问性任务验证与证据记录 | `design-review:accessibility-review` |
| 8 | `audit-website` | `squirrelscan/skills` | conditional | SEO、性能、安全、技术与无障碍综合扫描 | `design-review:design-debt-review` |
| 9 | `vitest` | `antfu/skills` | conditional | Vitest 项目的单元与集成测试知识 | 本地 pytest / vitest runner |
| 10 | `github-actions-hardening` | `github/awesome-copilot` | recommended | 审查 CI 工作流脚本注入、权限与供应链风险 | 手工 CI 审查 |

**核心铁律**：QA 只负责发现、复现、独立报告；产品源码修复必须交给 Engineering，禁止 QA 自修自验。  
**兜底**：编排器按 PRD 验收标准逐条人工核对表。

---

## ⑤ 交付（Release 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地市场插件平替 |
|---:|---|---|---|---|---|
| 1 | `ship` | `garrytan/gstack` | **core** | 从验证、同步到 PR 的安全发布执行 | `shipping-artifacts` |
| 2 | `land-and-deploy` | `garrytan/gstack` | recommended | 合并、部署与发布状态闭环 | git push / PR flow |
| 3 | `canary` | `garrytan/gstack` | recommended | 金丝雀验证与异常阻断 | 部署脚本 |
| 4 | `deploy-to-vercel` | `vercel-labs/agent-skills` | conditional | Vercel 部署与结果检查 | 平台 CLI |
| 5 | `vercel-optimize` | `vercel-labs/agent-skills` | conditional | Vercel 上线后的性能与配置优化 | 平台 CLI |
| 6 | `wrangler` | `cloudflare/skills` | conditional | Cloudflare Workers 部署、Secrets 与回滚 | 平台 CLI |
| 7 | `azure-reliability` | `microsoft/azure-skills` | conditional | Azure PaaS 高可用与跨区恢复 | 平台 CLI |
| 8 | `azure-kubernetes` | `microsoft/azure-skills` | conditional | AKS/Kubernetes 部署知识 | kubectl / helm |
| 9 | `github-actions-hardening` | `github/awesome-copilot` | **core** | CI/CD 安全强化与供应链护栏 | 手工审查 |
| 10 | `sentry-setup-releases` | `getsentry/plugin-claude` | recommended | 建立 Sentry release / deploy / commit 关联 | 平台 API |

**兜底**：从代码扫描自产 README、架构说明、环境变量清单与启动步骤。

---

## ⑥ 复盘（Evolution 域 Top 10）

| Rank | 开源 Skill | Source 仓库 | Tier | 核心价值 | 本地市场插件平替 |
|---:|---|---|---|---|---|
| 1 | `systematic-debugging` | `obra/superpowers` | **core** | 强制先定位根因和证据链，再提出修复 | `superpowers:systematic-debugging` |
| 2 | `incident-response` | `rampstackco/claude-skills` | **core** | 生产事故检测、分级、止损与恢复流程 | 手工事故复盘 |
| 3 | `metrics-review` | `anthropics/knowledge-work-plugins` | **core** | 指标层级、趋势、异常、目标差距与行动建议 | `product-management:产品指标复盘` |
| 4 | `analyzing-user-feedback` | `refoundai/lenny-skills` | **core** | 综合评论、访谈、工单与定量信号，检查代表性 | `product-management:用户反馈分析` |
| 5 | `validate-data` | `anthropics/knowledge-work-plugins` | **core** | 在决策前验证数据质量、聚合逻辑与结论支持度 | `huashu-data-pro` |
| 6 | `craft-experiment-design` | `amplitude/builder-skills` | **core** | 将干预转成可证伪假设、指标、受众与时长计划 | 手工 A/B 设计 |
| 7 | `craft-experiment-readout` | `amplitude/builder-skills` | recommended | 对实验结果做结论、风险与后续决策读出 | 手工读出 |
| 8 | `retro` | `garrytan/gstack` | recommended | 从交付结果反推流程和 Agent 工作方式改进 | `product-design:retro` |
| 9 | `llm-evaluation` | `wshobson/agents` | conditional | AI/LLM 产品的自动与人工评估体系 | 自动化 Eval |
| 10 | `web-perf` | `cloudflare/skills` | conditional | Web 性能基线、诊断与持续改进 | 性能报告 |

**兜底**：自产 Expected vs Actual 对比表 + 3 条行动建议，经验写入 `.workflow/state.md` 决策记录回流第①步。

---

## Evolution Provider Adapters（8 个）

仅在项目明确接入对应监控平台时激活，只提供数据证据，不能越权替代通用 Core 做决策：

| 平台 | Rank | 开源 Skill | Tier | 职责 |
|---|---:|---|---|---|
| **Datadog** | 1 | `dd-logs` | core | 查询和分析 Datadog 运行日志 |
| Datadog | 2 | `dd-apm` | core | APM/Trace 服务性能与错误诊断 |
| Datadog | 3 | `dd-monitors` | recommended | 基于已确认信号管理监控与告警 |
| Datadog | 4 | `agent-observability-trace-rca` | conditional | 从真实 Agent trace 做根因分析 |
| Datadog | 5 | `agent-observability-eval-pipeline` | conditional | 生产 Agent 失败模式转持续评估流水线 |
| **Sentry** | 1 | `sentry-debug-issue` | core | 用 Sentry trace/log/breadcrumb 定位生产 Issue |
| Sentry | 2 | `sentry-create-alert` | recommended | 生产信号转 Sentry 告警工作流 |
| Sentry | 3 | `sentry-setup-ai-monitoring` | conditional | AI/LLM 产品的 Sentry 监控 |

### 已移除：PostHog 适配器（3 个）

按用户决策 **完全移除**，原因同 [`SKILLS.md`](../SKILLS.md) — 依赖 PostHog 平台或单技能源仓库体积达 6.5GB：

| Skill | Tier | 移除原因 |
|-------|------|---------|
| `querying-posthog-data` | core | 绑定 PostHog 平台，非通用能力 |
| `investigate-metric` | core | 需要拉取整个 `posthog/posthog` 主仓库（6645MB），成本不可接受 |
| `llm-analytics-setup` | conditional | 绑定 PostHog 平台，非通用能力 |

复盘域的指标分析能力已由本表的 `metrics-review` + `validate-data`（Anthropics）覆盖。
