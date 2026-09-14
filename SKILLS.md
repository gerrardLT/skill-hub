# 本地 Skills 资产与审计状态

> **原始资产位置**：`skills/<skill-name>/`
> **事实口径**：68 个 catalog entry、64 个唯一 catalog 名称、66 个顶层 Skill root、73 个 embedded Skill root、全树 139 个 `SKILL.md` 入口。
> **落盘状态**：68 个 catalog entry 均可关联到本地顶层 Skill root 或重复引用；文件落盘不等于依赖完整、来源已核实或可离线运行。
> **当前终验结论**：未完成。阶段 1 通过；阶段 2 部分完成；阶段 3-8 未通过各自 Gate。详见 `curation/final-audit.json`。

## 阶段状态

| 阶段 | 状态 | 可接受证据 | 主要缺口 |
|---:|---|---|---|
| 1. 冻结原始资产 | `passed` | `curation/baseline.json`；source verifier 实跑 `ok=true` | 无 |
| 2. 资产底账与缺口 | `partial` | `curation/inventory.json`、`curation/gaps.json`、`skills-lock.json` | 59 个 review-required；13 个 standalone blocker；来源/许可证/运行依赖未全部闭合 |
| 3. 全量拆解 | `failed` | 6 个 cluster dossier、114 个草稿 unit | 33 个 included skill 无 unit；无逐来源 dossier/阅读覆盖；60 个 excerpt 非字面原文 |
| 4. 能力地图 | `failed` | `curation/capability-map.json` 草稿 | 无 `clusters.json`、`decisions.jsonl`、`coverage.json`；输入覆盖不足 |
| 5. 需求到 AC 试点 | `failed` | TC01 人工撰写对照草稿 | 无真实 baseline/candidate 同环境运行、holdout、mutation、blind review、slot/contract/provenance |
| 6. 全量提纯 | `failed` | 6 组方法/输出/报告草稿 | 无 `slots/`、每簇 eval、mutation、人工评审；部分 JSON 无法解析 |
| 7. 配方与组合验证 | `failed` | Gate 与 ITS simulation 文档 | 无 `recipes/`、recipe verifier、真实组合/替换/回流测试；simulation 不能作为执行证据 |
| 8. dev-loop 接入与终验 | `failed` | 原 dev-loop 源文件仍存在 | 总控未调用 recipe/slot；安装副本漂移；无全量 final Gate |

## 验证边界

- `python -m pytest tests/curation -v`：本次审核实跑 `10 passed`，只覆盖 baseline、inventory、source diff、lock/scope/identity；不覆盖阶段 3-8。
- `tools/curation/verify.py source`：本次审核实跑 `added=0 / changed=0 / removed=0 / ok=true`。
- `tools/curation/verify.py inventory`：本次审核实跑 `ok=true`，只证明顶层 lock、scope 和 forbidden identity 一致。
- `curation/experiments/ITS*.json`：设计/模拟记录，未执行；其中的 `actual_result`、`PASS` 和 `100%` 不视为测试证据。
- `curation/experiments/*-purification-method-v3.json`：候选方法草稿，不是可独立调用的 Slot。

## ① 需求域 (PM / Requirements)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `prd-development` | `deanpeters/Product-Manager-Skills` | 证据到完整 PRD 的端到端编排 | 已落盘 / included |
| 2 | `product-strategy-session` | `deanpeters/Product-Manager-Skills` | 定位、问题、战略与路线的综合推演 | 已落盘 / included |
| 3 | `discovery-process` | `deanpeters/Product-Manager-Skills` | 问题假设、研究、综合与验证 | 已落盘 / included |
| 4 | `prioritization-frameworks` | `phuryn/pm-skills` | 优先排序问题与机会，而非机械排功能 | 已落盘 / included |
| 5 | `outcome-roadmap` | `phuryn/pm-skills` | 将 Feature Roadmap 转为 Outcome Roadmap | 已落盘 / included |
| 6 | `competitive-strategy` | `refoundai/lenny-skills` | 竞争结构、替代选择、切换成本与持久优势分析 | 已落盘 / included |
| 7 | `interview-script` | `phuryn/pm-skills` | 基于 Mom Test / Continuous Discovery 的访谈设计 | 已落盘 / included |
| 8 | `pre-mortem` | `phuryn/pm-skills` | 发布前反事实失败审查 | 已落盘 / included |
| 9 | `metrics-dashboard` | `phuryn/pm-skills` | North Star、输入指标和护栏指标 | 已落盘 / included |
| 10 | `ai-product-strategy` | `refoundai/lenny-skills` | AI 产品能力、非确定性 UX 与模型边界 | 已落盘 / included |

## ② 设计域 (Design / UX)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `impeccable` | `pbakaus/impeccable` | 主设计引擎：设计方向、系统化审查、打磨与项目设计记忆 | 已落盘 / included |
| 2 | `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | 跨 Web/Mobile 的 UI/UX 模式、组件、排版、色彩与无障碍知识库 | 已落盘 / included |
| 3 | `web-design-guidelines` | `vercel-labs/agent-skills` | 以可用性、Web 规范与可访问性规则约束视觉实现 | 已落盘 / included |
| 4 | `review-animations` | `emilkowalski/skills` | 独立审查动效时机、缓动、持续时间、性能与 reduced-motion | 已落盘 / included |
| 5 | `redesign-existing-projects` | `leonxlnx/taste-skill` | 对已有低质量界面做 audit-first 的系统重设计 | 已落盘 / included |
| 6 | `web-accessibility` | `magnus919/agent-skills` | 基于 WCAG 2.2 的语义、键盘、焦点、表单、动效与人工验证证据 | 已落盘 / included |
| 7 | `prototype` | `emilkowalski/skills` | 并行生成真正不同的交互方案并可视化比较 | 已落盘 / included |
| 8 | `frontend-design` | `anthropics/skills` | 鲜明非模板化的 Greenfield 视觉生成 | 已落盘 / included |
| 9 | `extract-design-system` | `arvindrk/extract-design-system` | 从合法公开页面提取设计原语用于研究和系统迁移 | 已落盘 / included |
| 10 | `design-taste-frontend` | `leonxlnx/taste-skill` | 品牌页/落地页/作品集的高变化度 anti-slop 视觉方向 | 已落盘 / included |

## ③ 实现域 (Engineering / Code)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `writing-plans` | `obra/superpowers` | 将规格拆成可验证的小步实施计划 | 已落盘 / included |
| 2 | `test-driven-development` | `obra/superpowers` | 强制红-绿-重构和回归证据 | 已落盘 / included |
| 3 | `systematic-debugging` | `obra/superpowers` | 先定位根因，再实施单一修复 | 已落盘 / included |
| 4 | `requesting-code-review` | `obra/superpowers` | 使用独立上下文做代码审查 | 已落盘 / included |
| 5 | `verification-before-completion` | `obra/superpowers` | 完成声明前必须有新鲜验证证据 | 已落盘 / included |
| 6 | `executing-plans` | `obra/superpowers` | 按批次执行并在检查点复核 | 已落盘 / included |
| 7 | `subagent-driven-development` | `obra/superpowers` | 将独立任务分派给隔离上下文并逐项审查 | 已落盘 / included |
| 8 | `improve-codebase-architecture` | `mattpocock/skills` | 发现架构摩擦与深模块重构机会 | 已落盘 / included |
| 9 | `codebase-design` | `mattpocock/skills` | 设计深模块、接口边界、可测试性与模块接缝 | 已落盘 / included |
| 10 | `git-guardrails-claude-code` | `mattpocock/skills` | Git 操作与提交安全护栏 | 已落盘 / included |

## ④ 验收域 (QA / Verification)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `testing-strategy` | `anthropics/knowledge-work-plugins` | 按业务风险设计测试层级、覆盖边界、环境、数据与退出标准 | 已落盘 / included |
| 2 | `verification-before-completion` | `obra/superpowers` | 禁止没有新鲜可复现证据的完成/通过声明 | 已落盘 / duplicate-reference |
| 3 | `qa-only` | `garrytan/gstack` | 独立的 report-only Web QA：截图、复现、健康分，不修改产品源码 | 已落盘 / included |
| 4 | `code-review` | `anthropics/knowledge-work-plugins` | 从 correctness/security/performance/maintainability 独立审查变更 | 已落盘 / included |
| 5 | `playwright` | `openai/skills` | 真实浏览器交互、快照、截图、UI 流程与运行时证据 | 已落盘 / included |
| 6 | `playwright-best-practices` | `currents-dev/playwright-best-practices-skill` | Playwright E2E、flaky、fixtures、selector、CI 和高级测试模式知识 | 已落盘 / included |
| 7 | `web-accessibility` | `magnus919/agent-skills` | WCAG 2.2 导向的可访问性任务验证与证据记录 | 已落盘 / duplicate-reference |
| 8 | `audit-website` | `squirrelscan/skills` | SEO、性能、安全、技术与无障碍综合扫描 | 已落盘 / included |
| 9 | `vitest` | `antfu/skills` | Vitest 项目的单元与集成测试知识 | 已落盘 / included |
| 10 | `github-actions-hardening` | `github/awesome-copilot` | 审查 CI 工作流脚本注入、权限与供应链风险 | 已落盘 / deferred-platform |

## ⑤ 交付域 (Release / Operations)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 0 | `gstack` | `garrytan/gstack` | GStack 完整套件补充入口，不计入 68 个 catalog entry | 已落盘 / supplemental |
| 1 | `ship` | `garrytan/gstack` | 从验证、同步到 PR 的发布执行 | 已落盘 / included |
| 2 | `land-and-deploy` | `garrytan/gstack` | 合并、部署与发布状态闭环 | 已落盘 / included |
| 3 | `canary` | `garrytan/gstack` | 金丝雀验证与异常阻断 | 已落盘 / included |
| 4 | `deploy-to-vercel` | `vercel-labs/agent-skills` | Vercel 部署与结果检查 | 已落盘 / deferred-platform |
| 5 | `vercel-optimize` | `vercel-labs/agent-skills` | Vercel 上线后的性能与配置优化 | 已落盘 / deferred-platform |
| 6 | `wrangler` | `cloudflare/skills` | Cloudflare Workers 部署、环境、Secrets、版本与回滚 | 已落盘 / deferred-platform |
| 7 | `azure-reliability` | `microsoft/azure-skills` | Azure PaaS 高可用、健康探针与跨区恢复 | 已落盘 / deferred-platform |
| 8 | `azure-kubernetes` | `microsoft/azure-skills` | AKS/Kubernetes 部署知识 | 已落盘 / deferred-platform |
| 9 | `github-actions-hardening` | `github/awesome-copilot` | CI/CD 安全强化 | 已落盘 / deferred-platform duplicate-reference |
| 10 | `sentry-setup-releases` | `getsentry/plugin-claude` | 为发布建立 Sentry release、deploy、commit 关联与验证 | 已落盘 / deferred-platform |

## ⑥ 复盘域 (Evolution / Retrospective)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `systematic-debugging` | `obra/superpowers` | 强制先定位根因和证据链，再提出修复 | 已落盘 / duplicate-reference |
| 2 | `incident-response` | `rampstackco/claude-skills` | 生产事故检测、分级、止损、沟通、升级与恢复的结构化流程 | 已落盘 / included |
| 3 | `metrics-review` | `anthropics/knowledge-work-plugins` | 指标层级、趋势、异常、分群、目标差距与行动建议 | 已落盘 / included |
| 4 | `analyzing-user-feedback` | `refoundai/lenny-skills` | 综合评论、访谈、工单与定量信号，检查反馈代表性 | 已落盘 / included |
| 5 | `validate-data` | `anthropics/knowledge-work-plugins` | 在产品决策前验证方法、数据质量、聚合逻辑、偏差与结论支持度 | 已落盘 / included |
| 6 | `craft-experiment-design` | `amplitude/builder-skills` | 将干预转成可证伪假设、主指标、护栏、受众、holdout 与时长计划 | 已落盘 / included |
| 7 | `craft-experiment-readout` | `amplitude/builder-skills` | 对实验结果做结论、风险与后续决策读出 | 已落盘 / included |
| 8 | `retro` | `garrytan/gstack` | 从交付/会话结果反推流程和 Agent 工作方式改进 | 已落盘 / included |
| 9 | `llm-evaluation` | `wshobson/agents` | AI/LLM 产品的自动与人工评估体系 | 已落盘 / included |
| 10 | `web-perf` | `cloudflare/skills` | Web 性能基线、诊断与持续改进 | 已落盘 / included |

## ⑦ 三方监控适配器 (Provider Adapters)

| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |
|--:|---|---|---|:---:|
| 1 | `sentry-debug-issue` | `getsentry/sentry-for-ai` | 用 Sentry issue/trace/log/breadcrumb/Seer 上下文定位生产问题 | 已落盘 / deferred-platform |
| 2 | `sentry-create-alert` | `getsentry/sentry-for-ai` | 把已验证的生产信号转成 Sentry 告警/通知工作流 | 已落盘 / deferred-platform |
| 3 | `sentry-setup-ai-monitoring` | `getsentry/sentry-for-ai` | AI/LLM 产品的 Sentry Agent/Token/Trace 监控 | 已落盘 / deferred-platform |
| 4 | `dd-logs` | `datadog-labs/agent-skills` | 查询和分析 Datadog 日志 | 已落盘 / deferred-platform |
| 5 | `dd-apm` | `datadog-labs/agent-skills` | APM/Trace 服务性能与错误诊断 | 已落盘 / deferred-platform |
| 6 | `dd-monitors` | `datadog-labs/agent-skills` | 基于已确认信号管理告警与监控 | 已落盘 / deferred-platform |
| 7 | `agent-observability-trace-rca` | `datadog-labs/agent-skills` | 从真实 Agent trace 做根因分析 | 已落盘 / deferred-platform |
| 8 | `agent-observability-eval-pipeline` | `datadog-labs/agent-skills` | 把生产 Agent 失败模式转成持续评估流水线 | 已落盘 / deferred-platform |

## 下一步

按 `curation/final-audit.json` 回退到阶段 2/3：先闭合资产状态并完成全部 included 来源的逐份 dossier、语义单元和阅读覆盖。阶段 3 Gate 通过前，不再推进或宣称阶段 4-8 完成。
