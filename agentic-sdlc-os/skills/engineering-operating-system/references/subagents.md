# Subagent Roles

Use only when independent context or parallel work materially improves the decision.

## architecture-reviewer

独立评估边界、耦合、数据一致性、质量属性和演化成本。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## implementation-agent

只执行一个明确、可独立验证的计划单元。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## code-reviewer

不读取实现者思路，基于 diff、规格和测试独立审查。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## security-reviewer

执行威胁建模、权限、数据、依赖和滥用路径审查。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## Invocation contract

Specify role, bounded question, inputs, prohibited actions, output schema, evidence standard and stop condition. Never give review/research agents production write access by default.
