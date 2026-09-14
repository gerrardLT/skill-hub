# dd-monitors 来源能力档案

## Problem

安全创建和维护 Datadog monitors，减少抖动、无范围告警和缺少行动上下文造成的告警疲劳。

## When to Use

用于列出、读取、创建、审计 monitors，以及通过 downtime 静默计划内告警。

## When Not to Use

不直接删除 monitor；也不使用不存在的 Pup mute/unmute 命令。

## Role

Datadog monitor 管理与告警质量守门指南。

## Inputs

monitor ID 或 JSON 文件、tag scope、查询窗口、阈值与恢复阈值、runbook、通知目标和 downtime 配置。

## Outputs

monitor 列表或详情、新 monitor、downtime、缺 owner 或噪声审计结果及排障建议。

## Workflow

先检查上下文和发现缺值；列出或读取现状；按 SLO 设定有范围的稳定阈值；加入 recovery 与 runbook；文件化创建并审计。

## Branches

metric、query、service check、event、log、composite 与 APM monitor；计划静默走 downtime，行为变更走 monitor edit。

## Rules

告警必须 actionable、合理窗口、明确 scope、恢复阈值与 runbook；禁止直接删除，先标记待删除。

## Exceptions

计划静默通过 downtime payload；无 Pup mute/unmute。

## Dependencies

已安装并认证的 Datadog Pup；审计示例使用 `jq`。

## Permissions and Side Effects

读取 monitor；创建或更新 monitor 会影响告警；downtime 会抑制通知；安全删除流程会改名而非删除。

## Gates

创建前确认查询有数据、scope 与阈值有依据；删除请求不得直接执行；认证错误先刷新。

## Open Questions

顶层 SKILL.md 未定义最终物理删除已标记 monitor 的流程。

## Unique Value

将告警可操作性、抗抖动、最小范围和安全删除约束固化为 monitor 管理基线。

## Reading Coverage

本轮只完整读取了顶层 `skills/dd-monitors/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
