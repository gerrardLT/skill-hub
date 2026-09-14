# agent-observability-trace-rca 来源能力档案

## Problem

从生产 LLM traces 中区分表面症状与真实根因，并依据 eval、runtime error 或结构异常建立可验证的失败分类。

## When to Use

用于解释应用失败、eval 低分、运行错误、延迟或 agent/retrieval 结构异常。

## When Not to Use

不用于无 `ml_app`/eval 线索时猜测，也不在 Datadog MCP 与 `pup` 均不可用时继续；不会自动执行修复或发布 notebook。

## Role

生产 LLM trace 根因分析器，负责信号选择、开放编码、轴向编码、trace tree 导航和证据化建议。

## Inputs

`ml_app` 必需（给出 eval 时仍需 app）；可选 eval name、timeframe、mode 与 failure filter，也可消费 Session Classification Summary。

## Outputs

Signal Summary、3–8 类失败 taxonomy、根因链、具体建议、完整 RCA 报告，以及经用户选择后的文件或 notebook 导出。

## Workflow

检测 backend；解析输入并推断模式；搜索问题 spans；识别 app profile；开放编码与轴向编码；导航代表性 trace；生成建议；编译报告；询问后续动作。

## Branches

Eval Signal、Error Signal、Generic 三模式可自动选择或切换；分类摘要可跳过 Phase 0/1；无数据自动 pivot Generic；分布式 trace 与空 agent loop 有重建 fallback。

## Rules

查询必须显式包含 `@ml_app`；工具调用按规定并行和分批；详细中间分析不对外叙述；每项结论引用 trace 证据、展示数量并匿名化 PII。

## Exceptions

问题样本少于 15 可合并编码阶段；单一模式占比超过 80% 可提前进入 RCA；超过 50 条先抽样；Seer 结果仅作待验证假设。

## Dependencies

Datadog LLM Observability MCP 或 `pup`；可选 Datadog notebook MCP/pup fallback；若应用代码可用则可定位 prompt、tool 和 routing。

## Permissions and Side Effects

分析阶段以读取远端观测数据为主；仅用户选择后保存报告、修改代码或创建 notebook。任何代码修改前必须询问。

## Gates

backend 可用；输入充分；Phase 2/3 mandatory checkpoints；修复前必须对照本地仓库；任何 post-analysis action 均需用户选择。

## Open Questions

顶层 SKILL.md 未明确结构异常阈值 `N` 的统一取值。

## Unique Value

把 eval verdict、error 与结构异常统一为从 symptom span 跨父子/兄弟节点追到根因的证据链。

## Reading Coverage

本轮只完整读取了顶层 `skills/agent-observability-trace-rca/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
