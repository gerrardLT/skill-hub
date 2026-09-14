# agent-observability-eval-pipeline 来源能力档案

## Problem

为已有 Datadog LLM Observability traces 的 `ml_app` 提供从生产轨迹到评估器、数据集、实验和结果分析的确定性端到端引导，避免阶段边界、状态和执行确认不一致。

## When to Use

用于用户要求运行 eval pipeline、从 traces 建立 eval、引导式创建数据集与实验，或从分类、RCA 一路推进到实验分析。

## When Not to Use

不用于应用埋点、深度修改应用、自动创建 `.env`，也不在缺少 Datadog MCP 与 `pup` 时继续。

## Role

纯编排与教学层；分析逻辑委托给五个 agent-observability 子技能，并统一六阶段信封、检查点和状态持久化。

## Inputs

必需 `ml_app`；可选 project、timeframe、trace limit、输出格式、评估器模式、起止阶段、既有阶段产物、应用根目录、环境文件、输出目录和 backend。

## Outputs

阶段状态文件、分类与 RCA 产物、评估器产物、已发布数据集信息、生成并运行的实验、分析结果及最终摘要。

## Workflow

启动时固定 backend 与 invocation ID；执行 precheck；依次分类、RCA、评估器 bootstrap、采样并发布数据集、生成/审阅/运行实验、分析实验；每阶段先持久化再等待检查点。

## Branches

支持 MCP/pup backend；`--start-at`/`--stop-after` 连续切片；offline/online/data-only 三种评估器输出；缺失状态、无 traces、凭证问题或无效阶段范围时停止。

## Rules

全程使用同一 backend；每阶段不得自动前进；不得截断子技能输出；仅 Phase 4 和 5 执行代码；Phase 5 运行前必须等待 `run`；project name 全程保持一致。

## Exceptions

Phase 4 的创建与发布之间没有可编辑暂停；可在检查点重做单一阶段；旧参数 `--publish`、`--sdk-code` 仅作为兼容别名。

## Dependencies

Datadog LLM Observability MCP 或 `pup`；五个指定子技能；Phase 4/5 所需 Python SDK、provider credentials 与本地 Bash/Python 环境。

## Permissions and Side Effects

创建输出目录和状态文件；Phase 4 向 Datadog 发布数据集；Phase 5 执行实验并调用 provider API。不会提交或推送代码，也不会创建 `.env`。

## Gates

precheck 必须确认 backend、近期 traces、project、输出目录和凭证；阶段间必须显式 checkpoint；Phase 5 codegen 后必须单独审阅确认。

## Open Questions

顶层 SKILL.md 未明确各外部子技能在版本不兼容时的统一降级策略。

## Unique Value

把多个独立 observability 子技能包装为可暂停、可恢复、阶段产物可追踪且面向学习者的六阶段流水线。

## Reading Coverage

本轮只完整读取了顶层 `skills/agent-observability-eval-pipeline/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
