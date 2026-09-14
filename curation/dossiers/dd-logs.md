# dd-logs 来源能力档案

## Problem

以成本意识搜索、处理、归档 Datadog logs，并管理索引排除、日志指标和敏感数据。

## When to Use

用于日志搜索、archive/restriction/custom destination 查看、处理器设计、成本排除、日志指标和脱敏。

## When Not to Use

不用于顶层未定义的日志 rehydration CLI；该操作需 Datadog UI/API。

## Role

Datadog Logs 查询与配置操作指南。

## Inputs

查询、时间范围、service/env/attribute 条件、archive/processor/exclusion 配置和目标指标。

## Outputs

日志搜索结果、噪声来源分析、processor/exclusion/archive 配置示例、日志指标信息与排障建议。

## Workflow

检查上下文；发现缺失值；必要时确认；执行 Pup 搜索或配置列表；按成本、基数和敏感数据规则优化。

## Branches

全文、tag、attribute、range、boolean 与 wildcard 查询；归档、排除、指标和敏感数据分别处理。

## Rules

优先缩小时间与索引范围；只索引有价值日志；日志指标仅按有界维度分组；敏感信息发送前清洗。

## Exceptions

Pup 0.42.0 没有 rehydrate 命令；该流程转 UI/API。

## Dependencies

已安装并认证的 Datadog Pup；部分本地聚合示例依赖 `jq`。

## Permissions and Side Effects

搜索和列出配置通常只读；创建或调整 processor、exclusion、archive 或 metric 会改变日志处理、保留成本和可见性。

## Gates

缺少必要范围时先发现或询问；高基数分组不得采用；排除前确认日志确实可丢弃。

## Open Questions

顶层 SKILL.md 未给出创建或更新 archive、processor、exclusion 的具体 Pup 命令与确认流程。

## Unique Value

把日志可查询性、归档合规、索引成本和敏感数据处理放在同一操作框架中。

## Reading Coverage

本轮只完整读取了顶层 `skills/dd-logs/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
