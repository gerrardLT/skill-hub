# sentry-setup-ai-monitoring 来源能力档案

## Problem

在各类主流技术栈（JavaScript/Node.js、Python、PHP/Laravel 及边缘运行时等）中规范接入 Sentry AI Agent 监控与 LLM 可观测性，避免未经用户许可捕获敏感 PII 内容，并防止因采样配置不当或指标计算口径错误导致追踪断链或监控失真。

## When to Use

用于在应用中需要监控 LLM 外部调用（OpenAI, Anthropic, LangChain, Google GenAI, Vercel AI 等）、跟踪 AI Agent 执行生命周期、追踪对话轮次（Conversations）、统计 Token 消耗及延迟/成本指标的场景。

## When Not to Use

不用于通用应用基础 Sentry SDK 安装与常规未包含 AI/LLM 模块的普通错误/性能监控；不在未获得用户明确授权的情况下擅自开启包含敏感提示词与模型响应的 PII 抓取配置。

## Role

Sentry AI 与智能体可观测性配置器。负责检测本地安装的 AI SDK 技术栈、评估链路追踪采样率、在保障数据隐私合规前提下生成规范的 Sentry 追踪与对话分组配置。

## Inputs

本地项目技术栈依赖文件（如 `package.json`, `requirements.txt`, `pyproject.toml`, `composer.json`）、当前 Sentry 配置文件及采样参数、支持的 AI SDK 列表、用户关于是否捕获提示词/输出（PII）的授权确认，以及对话分组标识（Conversation ID）。

## Outputs

校验过的 Sentry 配置文件更新（包含针对 AI 追踪的 `tracesSampler` 或采样率配置）、支持库的集成初始化配置、针对不支持自动打补丁运行时的手动 `startSpan` 埋点代码，以及对 Conversations 视图所需会话标识的注入方案。

## Workflow

1. 优先扫描项目依赖文件，自动检测已安装的 AI SDK 与配套 Sentry SDK 版本；
2. 检查现有链路追踪采样率，在采样率小于 100% 且未设置 tracesSampler 时提示用户配置保障 AI 完整 Span 树的采样逻辑；
3. 审查数据合规与敏感信息策略，严格就 prompt/output 抓取向用户征求显式授权；
4. 依据目标运行环境（Node.js, Python, Laravel, Cloudflare Workers, Next.js 等）输出对应集成声明或手动 instrument 包装；
5. 在多轮对话场景下设置标准的 `gen_ai.conversation.id` 并通过 Traces 仪表盘校验验证。

## Branches

Node.js/Python 走原生自动集成注入分支；Laravel 走 `sentry-laravel` 配合 `laravel/ai` 驱动分支；Cloudflare Workers 因 `workerd` 不支持猴子补丁走构建时插件或手动封装分支；前端/Next.js 走客户端封装 `instrumentOpenAiClient` 分支；无现成 SDK 时走 `gen_ai.*` 语义约定的通用 Manual Instrumentation 分支。

## Rules

LLM 提示词与补全内容可能包含高敏感个人隐私（PII），未经用户明确确认绝对禁止开启 `recordInputs`/`recordOutputs`/`send_default_pii`；Token 统计中 cached 与 reasoning 均为 total 的子集而非独立累加，计算成本与消耗时必须遵守包含约束；对话标识必须为短且不含斜杠的安全标识符。

## Exceptions

若项目采用 Cloudflare Workers 运行时，常规 Node.js 的全局猴子补丁机制无效，必须改用 Vite 构建插件或显式代码包装；在未安装受支持 AI SDK 的自研引擎中，必须严格遵循 Sentry 语义属性命名规范手动声明 span。

## Dependencies

已安装的 Sentry SDK（JS 10.53.0+, Python 2.60.0+, Laravel 4.27.0+ 等）以及对应被监控的 AI 提供商 SDK（OpenAI, Anthropic, LangChain 等）。

## Permissions and Side Effects

本地修改应用代码与 Sentry 配置文件；配置向 Sentry 上报追踪 Span 与 Token 计费元数据；若开启 PII 捕获将传输提示词与输出文本至 Sentry 服务端。

## Gates

在改动任何数据捕获配置前必须就 PII 隐私政策向用户确认；在采样率可能丢失 AI Span 时必须提示配置专用采样器；改动后必须本地校验代码语法与测试。

## Open Questions

顶层 SKILL.md 未详述在离线或私有化部署 Sentry（Self-Hosted）环境中，各细分厂商模型最新的 Token 单价与成本计算引擎是否完全与 SaaS 端同步。

## Unique Value

建立了端到端覆盖多语言多环境的 AI 智能体可观测性实践，严格约束了合规隐私红线，并标准化了对话层级与 Token 计算维度的指标建模。

## Reading Coverage

本轮只完整读取了顶层 `skills/sentry-setup-ai-monitoring/SKILL.md`（共 407 行）。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
