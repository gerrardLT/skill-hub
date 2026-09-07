# Workflow

Purpose: 用线上真实行为、反馈和运行证据纠正此前判断，并把问题路由回真正拥有根因的 OS。

## Stages

### 1. INTAKE

明确观察窗口、版本、用户群、指标定义、事件和已知变更。

Primary output: `evolution-intake`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 2. OBSERVE

汇集产品指标、日志、追踪、错误、性能、成本、反馈和支持信号。

Primary output: `telemetry-report`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 3. TRIAGE

按影响、紧急性、范围和可逆性区分事故、缺陷、体验或战略问题。

Primary output: `signal-triage`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 4. DIAGNOSE

构建时间线和竞争假设，以证据排除并定位根因。

Primary output: `diagnosis`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 5. PRIORITIZE

按用户/业务影响、风险、信心和可逆性选择干预。

Primary output: `intervention-priority`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 6. INTERVENE

选择修复、配置、回滚、设计改动、产品实验或停止。

Primary output: `intervention-plan`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 7. EXPERIMENT

定义假设、样本、指标、护栏、停止规则和分析方法。

Primary output: `experiment-plan`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 8. VERIFY

比较 Expected vs Actual，控制混杂，验证副作用与持续性。

Primary output: `intervention-result`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 9. LEARN

区分 assumption/evidence/execution/strategy 等 gap，形成决策。

Primary output: `learning-decision`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 10. REENTRY

通过 learning-decision Gate 回流对应 OS 和具体阶段。

Primary output: `learning-decision`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

## Regression and re-entry

- New contradictory evidence: return to the earliest stage that owns the invalid assumption.
- Downstream implementation constraint: distinguish a true constraint from convenience; update the owning artifact and traceability.
- Critical risk: block progression unless mitigated, explicitly accepted or formally waived.
- Small bounded request: execute only affected stages while preserving upstream/downstream checks.
