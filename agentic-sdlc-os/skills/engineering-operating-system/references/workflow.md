# Workflow

Purpose: 把产品与设计规格转化为可维护、可测试、安全、可靠、可观测的实现，并提供新鲜验证证据。

## Stages

### 1. INTAKE

继承 PRD、设计规格、验收标准、约束、风险和追踪关系。

Primary output: `engineering-intake`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 2. REQUIREMENTS_REVIEW

识别歧义、不可实现项、边界条件、数据与非功能需求。

Primary output: `requirements-review`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 3. TECHNICAL_DESIGN

定义组件、接口、数据流、失败模式、依赖和运维边界。

Primary output: `technical-design`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 4. ARCHITECTURE

记录关键 ADR、质量属性、威胁、容量、迁移和回滚设计。

Primary output: `architecture-decisions`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 5. PLAN

拆成可独立验证的小步，明确测试、文件、依赖和检查点。

Primary output: `implementation-plan / test-plan / security-plan`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 6. BUILD

按 TDD 或等价验证循环实现，保持小批次和可回退提交。

Primary output: `source-change / unit-test-evidence`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 7. CODE_REVIEW

用独立上下文审查正确性、安全、复杂度、兼容和维护性。

Primary output: `code-review`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 8. INTEGRATION

验证模块、接口、数据、配置和外部依赖的真实集成。

Primary output: `integration-evidence`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 9. HARDENING

执行安全、性能、可靠性、依赖、可观测性和迁移检查。

Primary output: `security-review / performance-report`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 10. HANDOFF

重新运行验证命令，注册证据并通过 verification-ready。

Primary output: `verification-ready`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

## Regression and re-entry

- New contradictory evidence: return to the earliest stage that owns the invalid assumption.
- Downstream implementation constraint: distinguish a true constraint from convenience; update the owning artifact and traceability.
- Critical risk: block progression unless mitigated, explicitly accepted or formally waived.
- Small bounded request: execute only affected stages while preserving upstream/downstream checks.
