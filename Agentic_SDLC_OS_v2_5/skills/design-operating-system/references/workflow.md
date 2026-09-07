# Workflow

Purpose: 把已验证的产品意图转化为可理解、可操作、可访问、可实现并可验证的体验规格。

## Stages

### 1. INTAKE

继承 PM 目标、范围、用户、约束、指标和风险；形成设计问题。

Primary output: `design-brief`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 2. RESEARCH

补充任务研究、行为路径、认知负荷、环境和可访问性需求。

Primary output: `design-research`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 3. INFORMATION_ARCHITECTURE

定义对象、内容模型、导航、层级和查找路径。

Primary output: `information-architecture`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 4. USER_FLOWS

覆盖主流程、替代流程、异常、权限、中断与恢复。

Primary output: `user-flows`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 5. INTERACTION

定义组件行为、输入反馈、状态机、错误恢复和微交互。

Primary output: `interaction-spec`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 6. VISUAL_SYSTEM

建立设计令牌、排版、空间、色彩、层级、组件和动效语言。

Primary output: `design-system`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 7. PROTOTYPE

制作覆盖关键任务和关键状态的可测试原型。

Primary output: `prototype`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 8. VALIDATION

执行可用性、启发式、无障碍、响应式和内容验证。

Primary output: `usability-report / accessibility-report`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 9. HANDOFF

交付标注、状态、资源、验收条件和实现风险。

Primary output: `design-handoff`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 10. ACCEPTANCE

对实现进行设计验收并通过 design-ready 或发起返工。

Primary output: `design-ready`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

## Regression and re-entry

- New contradictory evidence: return to the earliest stage that owns the invalid assumption.
- Downstream implementation constraint: distinguish a true constraint from convenience; update the owning artifact and traceability.
- Critical risk: block progression unless mitigated, explicitly accepted or formally waived.
- Small bounded request: execute only affected stages while preserving upstream/downstream checks.
