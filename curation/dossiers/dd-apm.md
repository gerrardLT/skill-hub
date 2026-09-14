# dd-apm 来源能力档案

## Problem

为 Datadog APM 安装、自动埋点、service remapping、trace 查询和服务性能分析提供路由与基础操作。

## When to Use

用于 Kubernetes/Linux APM onboarding、SSI、服务改名、trace 搜索、依赖和服务性能分析。

## When Not to Use

若请求不匹配安装、remapping 或下方分析能力，应先澄清；APM volume/cost 目前无专门子技能。

## Role

Datadog APM 请求路由器与 Pup 操作指南。

## Inputs

部署形态、环境标签、service/trace 标识、时间窗口、目标操作及现有 Datadog 配置。

## Outputs

正确子技能路由、Pup 查询或配置命令、服务与 trace 分析、SLO 创建建议和故障排查结论。

## Workflow

先按 Kubernetes、Linux、service remapping 路由；否则检查上下文、发现缺失值、必要时确认，再执行目标命令并分析结果。

## Branches

Kubernetes SSI、Linux SSI、service remapping、一般 trace/service 分析；重叠时按 orchestrator、host 和命名症状裁决。

## Rules

匹配安装或 remapping 时必须立即读取指定子技能；确认 env tag，不假设 prod；避免 speculative commands 和高基数 tags。

## Exceptions

APM 成本请求先区分 sampling 与 retention；trace ID 无直接 get 命令时以窄窗口 search 代替。

## Dependencies

Datadog Labs Pup、有效认证；安装场景依赖对应未在本轮拆解的子技能。

## Permissions and Side Effects

查询服务、trace 和 flow map；可能安装 agent/SSI、创建 SLO 或配置 ingestion remapping，具体写操作由分派子技能决定。

## Gates

先判定部署形态和目标；缺值先发现再确认；无 traces 时核验 ddtrace、`DD_TRACE_ENABLED` 和 header propagation。

## Open Questions

顶层 SKILL.md 未定义一般 APM 配置写操作的统一确认门禁。

## Unique Value

用明确反模式和重叠裁决，把高风险的 SSI 安装与无需 rollout 的 service remapping 正确分流。

## Reading Coverage

本轮只完整读取了顶层 `skills/dd-apm/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
