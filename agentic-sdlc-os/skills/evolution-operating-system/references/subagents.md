# Subagent Roles

Use only when independent context or parallel work materially improves the decision.

## incident-investigator

独立构建时间线、竞争根因和证据需求，不修改生产。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## telemetry-analyst

检查指标定义、分群、基线、异常和数据质量。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## experiment-reviewer

审查假设、样本、护栏、停止规则和因果解释。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## learning-red-team

尝试用替代解释推翻结论，防止事后合理化。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## Invocation contract

Specify role, bounded question, inputs, prohibited actions, output schema, evidence standard and stop condition. Never give review/research agents production write access by default.
