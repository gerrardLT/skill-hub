# Workflow

Purpose: 独立证明软件在目标环境和真实风险下达到可接受质量，并明确剩余风险。

## Stages

### 1. INTAKE

继承需求、设计、实现、变更范围、风险、验收标准和工程自证。

Primary output: `qa-intake`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 2. RISK_ANALYSIS

按影响×可能性识别业务、数据、安全、兼容、性能和恢复风险。

Primary output: `quality-risk-model`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 3. STRATEGY

决定测试层级、范围、自动化边界、环境、数据和退出标准。

Primary output: `test-strategy`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 4. CASE_DESIGN

从风险和追踪关系生成正向、负向、边界、状态和滥用用例。

Primary output: `test-cases`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 5. ENVIRONMENT

验证构建、配置、数据、依赖、账号、可观测性和可重复性。

Primary output: `environment-readiness`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 6. EXECUTION

执行自动化、探索式、API、端到端和设备/浏览器验证。

Primary output: `test-execution-evidence`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 7. DEFECT_LOOP

复现、分级、定位、修复验证，并保护回归覆盖。

Primary output: `defect-disposition`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 8. REGRESSION

根据变更影响运行最小充分回归和关键业务旅程。

Primary output: `regression-report`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 9. NON_FUNCTIONAL

验证性能、安全、可靠性、可访问性、兼容和恢复。

Primary output: `nonfunctional-report`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 10. RECOMMENDATION

汇总证据、覆盖、缺陷和残余风险，通过 release-ready。

Primary output: `release-recommendation`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

## Regression and re-entry

- New contradictory evidence: return to the earliest stage that owns the invalid assumption.
- Downstream implementation constraint: distinguish a true constraint from convenience; update the owning artifact and traceability.
- Critical risk: block progression unless mitigated, explicitly accepted or formally waived.
- Small bounded request: execute only affected stages while preserving upstream/downstream checks.
