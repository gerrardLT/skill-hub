# <source-id> Dossier

> 本文件针对一个纳入范围的顶层 Skill。所有判断必须引用 `skills/` 原始文件或明确标记为新增分析。

## Problem

描述该 Skill 解决的问题，以及问题不成立时为何不应调用。

## When to Use

列出触发场景、前置状态与正向边界。

## When Not to Use

列出反向边界、应路由到其他能力的场景与不可安全执行的情况。

## Role

说明执行者角色、用户角色以及与实现、QA、审批者的职责分界。

## Inputs

记录必填输入、可选输入、允许的未知值和信息不足时的状态。

## Outputs

记录产物、字段语义、状态值和消费者。

## Workflow

按实际执行顺序描述完整主流程，不省略验证步骤。

## Branches

记录模式、条件分支、降级路径、中断与恢复行为。

## Rules

记录不可绕过的规则及其适用范围。

## Exceptions

记录例外、授权要求和例外不成立的条件。

## Dependencies

记录引用文件、其他 Skills、CLI、MCP、网络、凭据、运行时和版本状态。

## Permissions and Side Effects

记录读取、写入、安装、外部调用、生产操作和不可逆影响。

## Gates

记录通过、失败、`needs-input`、`blocked` 的判定与直接证据。

## Open Questions

记录证据不足、来源缺口、待人工裁决和不应猜测的问题。

## Unique Value

说明该 Skill 相对其他能力不可替代的内容，不使用泛化赞美。

## Reading Coverage

逐项列出入口、可达 references/templates/examples/sections/scripts；状态只能是 `read` 或 `excluded`，`excluded` 必须附理由。
