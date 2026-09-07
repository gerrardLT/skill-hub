# Dev Loop 外部 Skills 完整安装清单

> 数据源：v2.5 归档 `manifest/external-skills.json`（2026-09-01 基线严选）
> 总计：**60 个六域候选 + 8 个 Provider 适配器 = 68 个**（PostHog 移除后精简）

**当前安装状态**: ✅ 全部 25 个 core-tier 技能已安装；另装 `retro`（recommended tier，因 SKILL.md 第⑥步路由直接引用它）= **26 个已装**
**锁文件**: [`skills.lock.json`](skills.lock.json) — 每仓库 commit SHA + 每技能 SKILL.md 的 sha256
**恢复脚本**: [`restore-skills.sh`](restore-skills.sh) — 一键重放全部安装命令
**校验工具**: [`audit-skills.py`](audit-skills.py) — 以文件系统为准核对安装状态，输出 `audit-report.md`

## 分层统计

| Tier | 数量 | 含义 |
|------|------|------|
| **core** | 25 | 该域最小高价值能力，**核心链路必需** ✅ **全部已装** |
| recommended | 19 | 出现真实工作流缺口后再加 |
| conditional | 14 | 必须由技术栈/平台/任务证据触发 |
| provider_adapter | 8 | Sentry/Datadog adapter（PostHog removed） |

## ① 需求域（pm）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `prd-development` | `deanpeters/Product-Manager-Skills` | **core** | 6MB | ✅ 已装 |
| 2 | `product-strategy-session` | `deanpeters/Product-Manager-Skills` | **core** | 6MB | ✅ 已装 |
| 3 | `discovery-process` | `deanpeters/Product-Manager-Skills` | **core** | 6MB | ✅ 已装 |
| 4 | `prioritization-frameworks` | `phuryn/pm-skills` | **core** | 未测 | ✅ 已装 |
| 5 | `outcome-roadmap` | `phuryn/pm-skills` | **core** | 未测 | ✅ 已装 |
| 6 | `competitive-strategy` | `refoundai/lenny-skills` | recommended | 未测 | ⬜ 待装 |
| 7 | `interview-script` | `phuryn/pm-skills` | recommended | 未测 | ⬜ 待装 |
| 8 | `pre-mortem` | `phuryn/pm-skills` | recommended | 未测 | ⬜ 待装 |
| 9 | `metrics-dashboard` | `phuryn/pm-skills` | recommended | 未测 | ⬜ 待装 |
| 10 | `ai-product-strategy` | `refoundai/lenny-skills` | conditional | 未测 | ⬜ 待装 |

## ② 设计域（design）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `impeccable` | `pbakaus/impeccable` | **core** | 未测 | ✅ 已装 |
| 2 | `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | **core** | 8MB | ✅ 已装 |
| 3 | `web-design-guidelines` | `vercel-labs/agent-skills` | **core** | 未测 | ✅ 已装 |
| 4 | `review-animations` | `emilkowalski/skills` | **core** | 120KB | ✅ 已装 |
| 5 | `redesign-existing-projects` | `leonxlnx/taste-skill` | recommended | 33MB | ⬜ 待装 |
| 6 | `web-accessibility` | `magnus919/agent-skills` | recommended | 19MB | ⬜ 待装 |
| 7 | `prototype` | `emilkowalski/skills` | recommended | 120KB | ⬜ 待装 |
| 8 | `frontend-design` | `anthropics/skills` | conditional | 5MB | ⬜ 待装 |
| 9 | `extract-design-system` | `arvindrk/extract-design-system` | conditional | 284KB | ⬜ 待装 |
| 10 | `design-taste-frontend` | `leonxlnx/taste-skill` | conditional | 33MB | ⬜ 待装 |

## ③ 实现域（engineering）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `writing-plans` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 2 | `test-driven-development` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 3 | `systematic-debugging` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 4 | `requesting-code-review` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 5 | `verification-before-completion` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 6 | `executing-plans` | `obra/superpowers` | recommended | 4MB | ⬜ 待装 |
| 7 | `subagent-driven-development` | `obra/superpowers` | recommended | 4MB | ⬜ 待装 |
| 8 | `improve-codebase-architecture` | `mattpocock/skills` | recommended | 2MB | ⬜ 待装 |
| 9 | `codebase-design` | `mattpocock/skills` | recommended | 2MB | ⬜ 待装 |
| 10 | `git-guardrails-claude-code` | `mattpocock/skills` | conditional | 2MB | ⬜ 待装 |

## ④ 验收域（qa）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `testing-strategy` | `anthropics/knowledge-work-plugins` | **core** | 5MB | ✅ 已装 |
| 2 | `verification-before-completion` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 3 | `qa-only` | `garrytan/gstack` | **core** | 27.9MB | ✅ 已装 |
| 4 | `code-review` | `anthropics/knowledge-work-plugins` | **core** | 5MB | ✅ 已装 |
| 5 | `playwright` | `openai/skills` | **core** | 未测 | ✅ 已装 |
| 6 | `playwright-best-practices` | `currents-dev/playwright-best-practices-skill` | recommended | 341KB | ⬜ 待装 |
| 7 | `web-accessibility` | `magnus919/agent-skills` | recommended | 19MB | ⬜ 待装 |
| 8 | `audit-website` | `squirrelscan/skills` | conditional | 未测 | ⬜ 待装 |
| 9 | `vitest` | `antfu/skills` | conditional | 1MB | ⬜ 待装 |
| 10 | `github-actions-hardening` | `github/awesome-copilot` | recommended | 110MB | ✅ 已装 |

## ⑤ 交付域（release）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `ship` | `garrytan/gstack` | **core** | 27.9MB | ✅ 已装 |
| 2 | `land-and-deploy` | `garrytan/gstack` | recommended | 27.9MB | ⬜ 待装 |
| 3 | `canary` | `garrytan/gstack` | recommended | 27.9MB | ⬜ 待装 |
| 4 | `deploy-to-vercel` | `vercel-labs/agent-skills` | conditional | 未测 | ⬜ 待装 |
| 5 | `vercel-optimize` | `vercel-labs/agent-skills` | conditional | 未测 | ⬜ 待装 |
| 6 | `wrangler` | `cloudflare/skills` | conditional | 2MB | ⬜ 待装 |
| 7 | `azure-reliability` | `microsoft/azure-skills` | conditional | 8MB | ⬜ 待装 |
| 8 | `azure-kubernetes` | `microsoft/azure-skills` | conditional | 8MB | ⬜ 待装 |
| 9 | `github-actions-hardening` | `github/awesome-copilot` | **core** | 110MB | ✅ 已装 |
| 10 | `sentry-setup-releases` | `getsentry/plugin-claude` | recommended | 1MB | ⬜ 待装 |

## ⑥ 复盘域（evolution）— 10 个

| # | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|--:|-------|--------|------|---------|------|
| 1 | `systematic-debugging` | `obra/superpowers` | **core** | 4MB | ✅ 已装 |
| 2 | `incident-response` | `rampstackco/claude-skills` | **core** | 未测 | ✅ 已装 |
| 3 | `metrics-review` | `anthropics/knowledge-work-plugins` | **core** | 5MB | ✅ 已装 |
| 4 | `analyzing-user-feedback` | `refoundai/lenny-skills` | **core** | 未测 | ✅ 已装 |
| 5 | `validate-data` | `anthropics/knowledge-work-plugins` | **core** | 5MB | ✅ 已装 |
| 6 | `craft-experiment-design` | `amplitude/builder-skills` | **core** | 1MB | ✅ 已装 |
| 7 | `craft-experiment-readout` | `amplitude/builder-skills` | recommended | 1MB | ⬜ 待装 |
| 8 | `retro` | `garrytan/gstack` | recommended | 27.9MB | ✅ 已装 |
| 9 | `llm-evaluation` | `wshobson/agents` | conditional | 未测 | ⬜ 待装 |
| 10 | `web-perf` | `cloudflare/skills` | conditional | 2MB | ⬜ 待装 |

## Provider 适配器 — 8 个

| Provider | Skill | 源仓库 | Tier | 仓库体积 | 状态 |
|----------|-------|--------|------|---------|------|
| sentry | `sentry-debug-issue` | `getsentry/sentry-for-ai` | core | 35MB | ⬜ 待装 |
| sentry | `sentry-create-alert` | `getsentry/sentry-for-ai` | recommended | 35MB | ⬜ 待装 |
| sentry | `sentry-setup-ai-monitoring` | `getsentry/sentry-for-ai` | conditional | 35MB | ⬜ 待装 |
| datadog | `dd-logs` | `datadog-labs/agent-skills` | core | 842KB | ⬜ 待装 |
| datadog | `dd-apm` | `datadog-labs/agent-skills` | core | 842KB | ⬜ 待装 |
| datadog | `dd-monitors` | `datadog-labs/agent-skills` | recommended | 842KB | ⬜ 待装 |
| datadog | `agent-observability-trace-rca` | `datadog-labs/agent-skills` | conditional | 842KB | ⬜ 待装 |
| datadog | `agent-observability-eval-pipeline` | `datadog-labs/agent-skills` | conditional | 842KB | ⬜ 待装 |

### 已移除：PostHog 适配器（3 个）

按用户决策 **完全移除**，不列入候选：

| Skill | 源仓库 | 移除原因 |
|-------|--------|---------|
| `querying-posthog-data` | `posthog/skills` | 依赖 PostHog 平台，非通用能力 |
| `investigate-metric` | `posthog/posthog` | 🚨 源仓库 **6645MB**，体积不可接受 |
| `llm-analytics-setup` | `posthog/skills` | 依赖 PostHog 平台，非通用能力 |

其中 `investigate-metric` 需拉取整个 `posthog/posthog` 主仓库（6.5GB），单技能成本远超收益；
另两个虽轻量但同样绑定 PostHog 平台。复盘域的指标分析能力由
`metrics-review` + `validate-data` + `analyzing-user-feedback`（均已安装）覆盖。