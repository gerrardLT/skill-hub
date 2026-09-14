# github-actions-hardening 来源能力档案

## Problem

识别一般代码 linter 难以发现的 GitHub Actions trust boundary、表达式注入、特权触发器、供应链和 token 权限风险。

## When to Use

用于审计、加固或新建 `.github/workflows/`，以及处理危险 trigger、permissions、action pinning、OIDC、secrets 和 self-hosted runner。

## When Not to Use

不把普通 fork `pull_request` 运行不可信代码本身误判为高危；不自动应用修复。

## Role

GitHub Actions 专项安全 reviewer。

## Inputs

workflow YAML、触发器、`${{ }}` 表达式、`run`/`script`/action inputs、permissions、uses refs、secret/output 处理和 runner 类型。

## Outputs

severity summary、按 issue type 分组的精确 findings、文件与行位置、风险解释及 CRITICAL/HIGH 的前后修复 YAML。

## Workflow

映射 trigger 与 trust；查找 script injection；检查特权 trigger 是否执行 fork code；审计 permissions；审计 action refs；检查 secrets/outputs；生成报告。

## Branches

依据 trigger 和外部贡献者可控性定级；第三方与 first-party actions 采用不同 pinning 风险；已加固 workflow 输出检查清单。

## Rules

不可信 expression 不得直接插入 shell；特权 workflow 不得运行 fork code；默认 deny-all 或最小权限；第三方 action 必须完整 SHA pin。

## Exceptions

first-party action 未 pin 通常为 LOW；版本注释缺失为 INFO；fork `pull_request` 默认只读且无 secrets。

## Dependencies

待审 GitHub Actions 文件；详细 trust、injection、permissions、supply chain 和 report 规则位于 supporting references。

## Permissions and Side Effects

本技能只审查并提出修复，不自动修改 workflow；若后续应用建议，会改变 CI token、触发和 action 行为。

## Gates

必须按七步顺序；先输出 severity summary；每个高严重度项必须有具体修复；精确引用 offending YAML 与位置。

## Open Questions

顶层 SKILL.md 未定义用户批准后由谁应用修复。

## Unique Value

围绕 Actions 表达式预展开和特权 trigger 的独特执行模型进行威胁建模，而非复用通用应用安全扫描。

## Reading Coverage

本轮只完整读取了顶层 `skills/github-actions-hardening/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
