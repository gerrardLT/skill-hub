# External Skill Candidates

这些是 **Evolution-OS** 的候选增强能力，不是运行依赖。v2.4 使用 **Core + bounded Recommended + Conditional**：默认只启用最小 Core；出现明确能力缺口后再加 Recommended；Conditional 必须由项目、技术栈或具体任务证据触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `systematic-debugging` · obra/superpowers | core | 强制先定位根因和证据链，再提出修复 | — |
| 2 | `incident-response` · rampstackco/claude-skills | core | 生产事故检测、分级、止损、沟通、升级与恢复的结构化流程 | 主动事故用；事后学习仍由 Evolution-OS 的 LEARN/REENTRY 负责 |
| 3 | `metrics-review` · anthropics/knowledge-work-plugins | core | 指标层级、趋势、异常、分群、目标差距与行动建议 | — |
| 4 | `analyzing-user-feedback` · refoundai/lenny-skills | core | 综合评论、访谈、工单与定量信号，检查反馈代表性 | — |
| 5 | `validate-data` · anthropics/knowledge-work-plugins | core | 在产品决策前验证方法、数据质量、聚合逻辑、偏差与结论支持度 | — |
| 6 | `craft-experiment-design` · amplitude/builder-skills | core | 将干预转成可证伪假设、主指标、护栏、受众、holdout 与时长计划 | — |
| 7 | `craft-experiment-readout` · amplitude/builder-skills | recommended | 对实验结果做结论、风险与后续决策读出 | — |
| 8 | `retro` · garrytan/gstack | recommended | 从交付/会话结果反推流程和 Agent 工作方式改进 | gstack 套件安装；run setup once |
| 9 | `llm-evaluation` · wshobson/agents | conditional | AI/LLM 产品的自动与人工评估体系 | 仅 AI 产品；安装路径与权限必须先验证 |
| 10 | `web-perf` · cloudflare/skills | conditional | Web 性能基线、诊断与持续改进 | 仅 Web 性能问题 |

## Provider adapters

Provider Adapter **不是 Evolution Core**。只有仓库配置、部署架构或用户明确证据证明项目实际使用该平台时才启用。

| Provider | Rank | Skill | Tier | Role | Notes |
| --- | ---: | --- | --- | --- | --- |
| datadog | 1 | `dd-logs` · datadog-labs/agent-skills | core | 查询和分析 Datadog 日志 | 需要 Datadog pup/auth；先审查网络和凭据权限 |
| datadog | 2 | `dd-apm` · datadog-labs/agent-skills | core | APM/Trace 服务性能与错误诊断 | 需要 Datadog pup/auth |
| datadog | 3 | `dd-monitors` · datadog-labs/agent-skills | recommended | 基于已确认信号管理告警与监控 | 需要 Datadog pup/auth |
| datadog | 4 | `agent-observability-trace-rca` · datadog-labs/agent-skills | conditional | 从真实 Agent trace 做根因分析 | 仅 AI Agent 生产流量 |
| datadog | 5 | `agent-observability-eval-pipeline` · datadog-labs/agent-skills | conditional | 把生产 Agent 失败模式转成持续评估流水线 | 仅 AI Agent；与 Evolution Experiment/Verify 结合 |
| posthog | 1 | `querying-posthog-data` · posthog/skills | core | PostHog 指标、漏斗、留存、路径、日志、实验和 LLM traces 的受治理查询入口 | 需要 PostHog MCP 才能执行真实查询 |
| posthog | 2 | `investigate-metric` · posthog/posthog | core | 针对指标下降/上升/平台期做分群、路径、留存和变更窗口根因调查 | 需要 PostHog MCP v2；必须做对照分群/交叉验证 |
| posthog | 3 | `llm-analytics-setup` · posthog/skills | conditional | 为 AI/LLM 产品接入 PostHog token/cost/latency/trace 分析 | 仅 AI/LLM 产品；严禁把 PII 放入 capture 事件属性 |
| sentry | 1 | `sentry-debug-issue` · getsentry/sentry-for-ai | core | 用 Sentry issue/trace/log/breadcrumb/Seer 上下文定位生产问题 | Sentry 官方要求安装对应 Agent 的分发插件；Cursor 通过 Settings > Plugins 添加 getsentry/plugin-cursor。 |
| sentry | 2 | `sentry-create-alert` · getsentry/sentry-for-ai | recommended | 把已验证的生产信号转成 Sentry 告警/通知工作流 | 与 sentry-debug-issue 共用官方插件，安装器会去重。 |
| sentry | 3 | `sentry-setup-ai-monitoring` · getsentry/sentry-for-ai | conditional | AI/LLM 产品的 Sentry Agent/Token/Trace 监控 | 仅 AI/LLM 产品。 |

示例：

```bash
# Generic Evolution Core only
python <agentic-sdlc-os>/scripts/install_external_skills.py --os evolution --profile core

# Generic Core + Datadog core adapter
python <agentic-sdlc-os>/scripts/install_external_skills.py --os evolution --profile core --provider datadog

# Sentry plugin requires agent-specific distribution; preview for Codex
python <agentic-sdlc-os>/scripts/install_external_skills.py --os evolution --profile core --provider sentry --agent codex --allow-custom
```

Provider Skill 只增强 OBSERVE / TRIAGE / DIAGNOSE / VERIFY，不拥有 `learning-decision`，不得覆盖 Gate、证据质量或人工授权。
