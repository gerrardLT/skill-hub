# Agentic SDLC OS：六域外部 Skills Top 10

基线日期：2026-09-01。排名用于构建最小高价值能力栈，不代表无条件安装顺序。

## 评估方法

综合：任务价值、方法完整性、Agent 可执行性、公开采用信号、维护/来源可信度、安全与上下文成本、与现有 OS 的互补性。Stars/安装量只作为采用信号，不能替代源码与工作流质量判断。

## 总体采用规则

1. 先安装本仓库 7 个 Orchestrator Skills。
2. 每个 OS 默认只启用 `core`；不要一次安装全部候选。
3. 同一职责只保留一个主 Skill；明显重叠能力降为 Recommended/Conditional。
4. QA 与 Engineering 必须保持独立验收边界。
5. Evolution 默认保持厂商无关；Sentry/Datadog/PostHog 只通过显式 Provider Adapter 激活。
6. 第三方 Skill 不能绕过 `.sdlc/` Gate、证据、风险、人类授权和 Skill Lock。


## PM-OS

产品发现、战略、优先级、定义与指标闭环。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `prd-development` | deanpeters/Product-Manager-Skills | core | 证据到完整 PRD 的端到端编排 |
| 2 | `product-strategy-session` | deanpeters/Product-Manager-Skills | core | 定位、问题、战略与路线的综合推演 |
| 3 | `discovery-process` | deanpeters/Product-Manager-Skills | core | 问题假设、研究、综合与验证 |
| 4 | `prioritization-frameworks` | phuryn/pm-skills | core | 优先排序问题与机会，而非机械排功能 |
| 5 | `outcome-roadmap` | phuryn/pm-skills | core | 将 Feature Roadmap 转为 Outcome Roadmap |
| 6 | `competitive-strategy` | refoundai/lenny-skills | recommended | 竞争结构、替代选择、切换成本与持久优势分析 |
| 7 | `interview-script` | phuryn/pm-skills | recommended | 基于 Mom Test / Continuous Discovery 的访谈设计 |
| 8 | `pre-mortem` | phuryn/pm-skills | recommended | 发布前反事实失败审查 |
| 9 | `metrics-dashboard` | phuryn/pm-skills | recommended | North Star、输入指标和护栏指标 |
| 10 | `ai-product-strategy` | refoundai/lenny-skills | conditional | AI 产品能力、非确定性 UX 与模型边界 |

**默认最小集：** `prd-development` + `product-strategy-session` + `discovery-process` + `prioritization-frameworks` + `outcome-roadmap`


## Design-OS

研究、信息架构、交互、视觉、原型与设计验收。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `impeccable` | pbakaus/impeccable | core | 主设计引擎：设计方向、系统化审查、打磨与项目设计记忆 |
| 2 | `ui-ux-pro-max` | nextlevelbuilder/ui-ux-pro-max-skill | core | 跨 Web/Mobile 的 UI/UX 模式、组件、排版、色彩与无障碍知识库 |
| 3 | `web-design-guidelines` | vercel-labs/agent-skills | core | 以可用性、Web 规范与可访问性规则约束视觉实现 |
| 4 | `review-animations` | emilkowalski/skills | core | 独立审查动效时机、缓动、持续时间、性能与 reduced-motion |
| 5 | `redesign-existing-projects` | leonxlnx/taste-skill | recommended | 对已有低质量界面做 audit-first 的系统重设计 |
| 6 | `web-accessibility` | magnus919/agent-skills | recommended | 基于 WCAG 2.2 的语义、键盘、焦点、表单、动效与人工验证证据 |
| 7 | `prototype` | emilkowalski/skills | recommended | 并行生成真正不同的交互方案并可视化比较 |
| 8 | `frontend-design` | anthropics/skills | conditional | 鲜明非模板化的 Greenfield 视觉生成 |
| 9 | `extract-design-system` | arvindrk/extract-design-system | conditional | 从合法公开页面提取设计原语用于研究和系统迁移 |
| 10 | `design-taste-frontend` | leonxlnx/taste-skill | conditional | 品牌页/落地页/作品集的高变化度 anti-slop 视觉方向 |

**默认最小集：** `impeccable` + `ui-ux-pro-max` + `web-design-guidelines` + `review-animations`

**v2.4 关键规则：** `impeccable` 为默认唯一视觉主导；`frontend-design`/`design-taste-frontend` 不再与其同时作为 Core。

## Engineering-OS

技术设计、计划、实现、评审、集成与加固。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `writing-plans` | obra/superpowers | core | 将规格拆成可验证的小步实施计划 |
| 2 | `test-driven-development` | obra/superpowers | core | 强制红-绿-重构和回归证据 |
| 3 | `systematic-debugging` | obra/superpowers | core | 先定位根因，再实施单一修复 |
| 4 | `requesting-code-review` | obra/superpowers | core | 使用独立上下文做代码审查 |
| 5 | `verification-before-completion` | obra/superpowers | core | 完成声明前必须有新鲜验证证据 |
| 6 | `executing-plans` | obra/superpowers | recommended | 按批次执行并在检查点复核 |
| 7 | `subagent-driven-development` | obra/superpowers | recommended | 将独立任务分派给隔离上下文并逐项审查 |
| 8 | `improve-codebase-architecture` | mattpocock/skills | recommended | 发现架构摩擦与深模块重构机会 |
| 9 | `codebase-design` | mattpocock/skills | recommended | 设计深模块、接口边界、可测试性与模块接缝 |
| 10 | `git-guardrails-claude-code` | mattpocock/skills | conditional | Git 操作与提交安全护栏 |

**默认最小集：** `writing-plans` + `test-driven-development` + `systematic-debugging` + `requesting-code-review` + `verification-before-completion`


## QA-OS

独立风险驱动测试、回归、非功能验证与发布建议。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `testing-strategy` | anthropics/knowledge-work-plugins | core | 按业务风险设计测试层级、覆盖边界、环境、数据与退出标准 |
| 2 | `verification-before-completion` | obra/superpowers | core | 禁止没有新鲜可复现证据的完成/通过声明 |
| 3 | `qa-only` | garrytan/gstack | core | 独立的 report-only Web QA：截图、复现、健康分，不修改产品源码 |
| 4 | `code-review` | anthropics/knowledge-work-plugins | core | 从 correctness/security/performance/maintainability 独立审查变更 |
| 5 | `playwright` | openai/skills | core | 真实浏览器交互、快照、截图、UI 流程与运行时证据 |
| 6 | `playwright-best-practices` | currents-dev/playwright-best-practices-skill | recommended | Playwright E2E、flaky、fixtures、selector、CI 和高级测试模式知识 |
| 7 | `web-accessibility` | magnus919/agent-skills | recommended | WCAG 2.2 导向的可访问性任务验证与证据记录 |
| 8 | `audit-website` | squirrelscan/skills | conditional | SEO、性能、安全、技术与无障碍综合扫描 |
| 9 | `vitest` | antfu/skills | conditional | Vitest 项目的单元与集成测试知识 |
| 10 | `github-actions-hardening` | github/awesome-copilot | recommended | 审查 CI 工作流脚本注入、权限与供应链风险 |

**默认最小集：** `testing-strategy` + `verification-before-completion` + `qa-only` + `code-review` + `playwright`

**v2.4 关键规则：** QA 负责发现、复现、独立验证；产品源码修复归 Engineering，禁止 QA 自修自验。

## Release-OS

发布准备、渐进式交付、验证、回滚与复盘。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `ship` | garrytan/gstack | core | 从验证、同步到 PR 的发布执行 |
| 2 | `land-and-deploy` | garrytan/gstack | recommended | 合并、部署与发布状态闭环 |
| 3 | `canary` | garrytan/gstack | recommended | 金丝雀验证与异常阻断 |
| 4 | `deploy-to-vercel` | vercel-labs/agent-skills | conditional | Vercel 部署与结果检查 |
| 5 | `vercel-optimize` | vercel-labs/agent-skills | conditional | Vercel 上线后的性能与配置优化 |
| 6 | `wrangler` | cloudflare/skills | conditional | Cloudflare Workers 部署、环境、Secrets、版本与回滚 |
| 7 | `azure-reliability` | microsoft/azure-skills | conditional | Azure PaaS 高可用、健康探针与跨区恢复 |
| 8 | `azure-kubernetes` | microsoft/azure-skills | conditional | AKS/Kubernetes 部署知识 |
| 9 | `github-actions-hardening` | github/awesome-copilot | core | CI/CD 安全强化 |
| 10 | `sentry-setup-releases` | getsentry/plugin-claude | recommended | 为发布建立 Sentry release、deploy、commit 关联与验证 |

**默认最小集：** `ship` + `github-actions-hardening`


## Evolution-OS

厂商无关的可观测性、诊断、实验、学习与跨域回流。

| Rank | Skill | Source | Tier | Core value |
| ---: | --- | --- | --- | --- |
| 1 | `systematic-debugging` | obra/superpowers | core | 强制先定位根因和证据链，再提出修复 |
| 2 | `incident-response` | rampstackco/claude-skills | core | 生产事故检测、分级、止损、沟通、升级与恢复的结构化流程 |
| 3 | `metrics-review` | anthropics/knowledge-work-plugins | core | 指标层级、趋势、异常、分群、目标差距与行动建议 |
| 4 | `analyzing-user-feedback` | refoundai/lenny-skills | core | 综合评论、访谈、工单与定量信号，检查反馈代表性 |
| 5 | `validate-data` | anthropics/knowledge-work-plugins | core | 在产品决策前验证方法、数据质量、聚合逻辑、偏差与结论支持度 |
| 6 | `craft-experiment-design` | amplitude/builder-skills | core | 将干预转成可证伪假设、主指标、护栏、受众、holdout 与时长计划 |
| 7 | `craft-experiment-readout` | amplitude/builder-skills | recommended | 对实验结果做结论、风险与后续决策读出 |
| 8 | `retro` | garrytan/gstack | recommended | 从交付/会话结果反推流程和 Agent 工作方式改进 |
| 9 | `llm-evaluation` | wshobson/agents | conditional | AI/LLM 产品的自动与人工评估体系 |
| 10 | `web-perf` | cloudflare/skills | conditional | Web 性能基线、诊断与持续改进 |

**默认最小集：** `systematic-debugging` + `incident-response` + `metrics-review` + `analyzing-user-feedback` + `validate-data` + `craft-experiment-design`

**v2.4 关键规则：** 上述 10 项是 Generic 层。Observability Provider 不进入默认 Core。

## Evolution Provider Adapters

仅在真实项目证据确认使用对应平台时启用。

| Provider | Rank | Skill | Tier | Role |
| --- | ---: | --- | --- | --- |
| datadog | 1 | `dd-logs` | core | 查询和分析 Datadog 日志 |
| datadog | 2 | `dd-apm` | core | APM/Trace 服务性能与错误诊断 |
| datadog | 3 | `dd-monitors` | recommended | 基于已确认信号管理告警与监控 |
| datadog | 4 | `agent-observability-trace-rca` | conditional | 从真实 Agent trace 做根因分析 |
| datadog | 5 | `agent-observability-eval-pipeline` | conditional | 把生产 Agent 失败模式转成持续评估流水线 |
| posthog | 1 | `querying-posthog-data` | core | PostHog 指标、漏斗、留存、路径、日志、实验和 LLM traces 的受治理查询入口 |
| posthog | 2 | `investigate-metric` | core | 针对指标下降/上升/平台期做分群、路径、留存和变更窗口根因调查 |
| posthog | 3 | `llm-analytics-setup` | conditional | 为 AI/LLM 产品接入 PostHog token/cost/latency/trace 分析 |
| sentry | 1 | `sentry-debug-issue` | core | 用 Sentry issue/trace/log/breadcrumb/Seer 上下文定位生产问题 |
| sentry | 2 | `sentry-create-alert` | recommended | 把已验证的生产信号转成 Sentry 告警/通知工作流 |
| sentry | 3 | `sentry-setup-ai-monitoring` | conditional | AI/LLM 产品的 Sentry Agent/Token/Trace 监控 |


## 结构化清单与安装

- 机器可读清单：`manifest/external-skills.json`
- Design Core：`python skills/agentic-sdlc-os/scripts/install_external_skills.py --os design --profile core`
- QA Core：`python skills/agentic-sdlc-os/scripts/install_external_skills.py --os qa --profile core`
- Evolution Generic Core：`python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core`
- Evolution + Datadog：`python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core --provider datadog`

执行第三方安装仍需 `--execute --acknowledge-review`；Custom/Plugin 安装还需 `--allow-custom`。排名应在仓库重大版本、权限、许可证或维护状态变化时重新复核。
