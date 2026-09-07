# Subagent Roles

Use only when independent context or parallel work materially improves the decision.

## release-safety-reviewer

在执行前独立审查计划、依赖、权限、停止和回滚条件。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## migration-reviewer

审查数据兼容、锁、容量、备份、验证和逆向迁移。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## production-verifier

用独立证据验证真实生产旅程与关键指标。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## incident-commander

出现异常时协调止损、通信、决策和记录，不直接取代技术调查。

Required output: conclusion, supporting evidence, contrary evidence, assumptions, risks, confidence and next action.

## Invocation contract

Specify role, bounded question, inputs, prohibited actions, output schema, evidence standard and stop condition. Never give review/research agents production write access by default.
