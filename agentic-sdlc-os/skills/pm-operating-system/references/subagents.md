# Subagent Roles

Use only when independent context or parallel work materially improves the decision.

## research-agent

并行收集市场、用户、政策和技术一手证据；返回证据账本，不替代决策。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## competitive-agent

独立分析直接竞品、替代方案、状态 quo、分发与结构性优势。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## product-red-team

对问题、战略、PRD、商业模型和指标做最强反方审查。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## evidence-agent

区分事实/推断/假设，检查证据直接性、时效性和冲突。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## Invocation contract

Specify role, bounded question, inputs, prohibited actions, output schema, evidence standard and stop condition. Never give review/research agents production write access by default.
