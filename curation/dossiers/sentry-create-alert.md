# sentry-create-alert 来源能力档案

## Problem

通过处于 beta 的 Sentry workflow engine API 创建带触发、过滤和通知动作的 issue alert。

## When to Use

用于创建 Sentry alert、通知、priority/de-escalation workflow，以及 email、Slack、PagerDuty 等动作。

## When Not to Use

不用于旧 Alerts UI 专属规则假设；缺少 alerts 写权限或必要配置时不应发起创建。

## Role

Sentry workflow alert 配置与 API 执行器。

## Inputs

org slug、auth token、region、alert name、trigger events、可选 conditions、action type 和 target。

## Outputs

workflow payload、创建后的 workflow ID、UI link，以及 API 错误诊断。

## Workflow

收集缺失配置；通过成员、团队和 integration API 解析 ID；按 polymorphic comparison 构造 payload；POST 创建；验证 201 并返回链接。

## Branches

trigger 类型与 condition logic 分支；email、Slack、PagerDuty、Discord、Teams、Opsgenie、Jira、GitHub 使用不同 action 配置。

## Rules

trigger `logicType` 固定 `any-short`；action 位于 `actionFilters[].actions`，`triggers.actions` 固定空数组；frequency 只能取允许值。

## Exceptions

缺少 workflow-engine-ui feature flag 时使用 legacy rules 页面；condition 可用 `conditionResult:false` 反转。

## Dependencies

shell `curl`、Sentry org token（`alerts:write` 或兼容管理 scope）、正确 region 与已配置 integration。

## Permissions and Side Effects

读取组织成员、团队和 integrations；创建、更新或删除 workflow 会改变告警和通知行为；token 不应进入档案输出。

## Gates

必填配置齐全；名称先解析为 ID；payload 类型与 comparison shape 匹配；创建必须返回 HTTP 201。

## Open Questions

顶层 SKILL.md 未明确在展示 payload 后是否需要额外用户确认。

## Unique Value

明确编码 beta workflow engine 的 trigger/filter/action 数据模型及多态 condition 结构，降低 400 与错误通知目标风险。

## Reading Coverage

本轮只完整读取了顶层 `skills/sentry-create-alert/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
