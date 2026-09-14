# vercel-optimize 来源能力档案

## Problem

针对部署在 Vercel 平台的现代 Web 项目（尤其是 Next.js、SvelteKit、Nuxt 等），避免不结合实际生产指标的盲目优化，通过确定性门禁、真实可观测性数据分析与代码静态扫描相结合，产出有指标支撑、具备版本感知并可落地的性能与账单成本优化方案。

## When to Use

用于 Vercel 账单削减（函数调用量、构建时长、流式数据传输、Fluid compute 等）、排查高耗时或高成本路由、探测缓存命中瓶颈、Core Web Vitals 优化或审查系统瓶颈等真实生产运维与优化场景。

## When Not to Use

不用于尚未部署在 Vercel 或未配置 Vercel 关联的项目；不在未获取生产真实指标（`signals.json`）之前随意对源码展开全局盲目检索；不用于试图推测未经核实的具体美元节省金额。

## Role

Vercel 性能与成本优化架构师。负责自动化收集平台真实可观测性信号、实施确定性规则门禁、深入调查指标异常路由的代码与配置、产出严格可复现且带版本文档依据的优化报告。

## Inputs

已链接并经过认证的 Vercel 项目上下文与 CLI 凭据、本地应用源码与包配置、Vercel 可观测性指标与账单数据（14 天分析窗口）、由门禁工具判定的候选检查范围与用户关于预算或候选数量的选择。

## Outputs

校验过的优化诊断报告（Markdown 格式）、针对每个通过门禁候选的深入调查简报与确切源码定位（带文件与行号）、符合目标框架版本的权威文档引用清单，以及面向用户的最终精简摘要。

## Workflow

1. 前置预检：验证 Vercel CLI 认证、项目目录关联状态（`vercel link`）及框架支持类型；
2. 收集与合并信号：拉取 Vercel 生产指标（Metrics/Usage/Contract）并扫描本地代码，合并为统一的信号清单；
3. 门禁决策：通过确定性规则门禁筛选出真正具备指标支撑的高价值候选优化项，非阻塞式向用户呈现或直接深入调查；
4. 针对候选项提取代码调用链路并生成调查简报，逐项核实路由源码逻辑与适用缓存策略；
5. 结果校验与渲染：对产出的每一条建议进行有效性、版本匹配度及安全性校验，格式化输出可审计的实施报告。

## Branches

支持 Next.js App/Pages Router、SvelteKit、Nuxt 全量指标映射分支；Astro 走受限平台级检查分支；Hono/Remix 或未知框架走用户确认后的受限平台代码审计分支；无 Observability Plus 权限时走确认降级为静态扫描分支。

## Rules

严格遵循“指标优先”（Metrics first）原则，绝不脱离生产监控信号直接猜测性能瓶颈；调查范围严格限定在命中候选项的路由与局部导入链中，严禁全仓库无序 grep；禁止向用户承诺具体的“节省 $N”金钱数字，仅使用成本数量级术语；严禁在命令中明文泄露认证令牌。

## Exceptions

对于 Vercel Workflow 运行时端点（`/.well-known/workflow/v1/*`）或长连接流式响应（SSE/AI 流式输出），不应仅因挂钟耗时较长而直接断定需要降低函数执行时长；缺乏 14 天有效流量时必须向用户明确说明仅能执行与流量无关的基础检查。

## Dependencies

已安装的 Node.js 20+、Vercel CLI v53+（支持 metrics/usage/contract 子命令）、本地依赖解析环境及已认证授权的 Vercel 账户与关联项目。

## Permissions and Side Effects

在独立临时运行目录（`RUN_DIR`）中读写信号与临时简报文件；调用 Vercel CLI 读取项目生产监控数据与账单指标；只读访问本地代码库与配置文件。

## Gates

未完成项目关联与账户作用域解析前必须阻断继续；不支持框架或无可观测性数据时必须向用户获取降级许可；最终报告中的建议必须具备行号证据与严格匹配当前技术栈版本的权威引用。

## Open Questions

顶层 SKILL.md 未提供在大规模微前端或包含多套自定义跨云反向代理架构下，Vercel 边缘缓存命中率与多源链路指标的端到端自动化归因方案。

## Unique Value

彻底扭转了基于猜测与通用八股文进行前端性能优化的传统模式，建立了一套严格以生产实测指标为唯一驱动、以确定性数学规则为准入门槛的严肃工业级优化审计体系。

## Reading Coverage

本轮只完整读取了顶层 `skills/vercel-optimize/SKILL.md`（共 274 行）。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
