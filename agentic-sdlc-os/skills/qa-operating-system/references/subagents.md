# Subagent Roles

Use only when independent context or parallel work materially improves the decision.

## test-designer

从风险和追踪关系独立生成边界、状态、故障和滥用用例。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## exploratory-tester

以新鲜上下文探索系统，不被已有测试用例锚定。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## automation-reviewer

审查测试是否稳定、分层、可维护，识别假阳性和假阴性。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## quality-red-team

尝试证明发布建议错误，寻找未覆盖的高影响失败。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## Invocation contract

Specify role, bounded question, inputs, prohibited actions, output schema, evidence standard and stop condition. Never give review/research agents production write access by default.
