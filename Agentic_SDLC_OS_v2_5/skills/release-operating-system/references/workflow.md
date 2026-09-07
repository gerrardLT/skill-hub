# Workflow

Purpose: 把已验证的版本以渐进、可观测、可回滚且有明确授权的方式送入生产。

## Stages

### 1. INTAKE

继承 QA 建议、版本范围、残余风险、依赖、负责人和发布窗口。

Primary output: `release-intake`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 2. READINESS

核验审批、变更冻结、运行手册、值守、状态页和外部依赖。

Primary output: `release-readiness`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 3. BUILD_ARTIFACT

生成可追踪、不可变、已签名或可校验的构建制品。

Primary output: `build-artifact`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 4. ENVIRONMENT

验证生产配置、密钥、权限、容量、网络和可观测性。

Primary output: `environment-verification`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 5. MIGRATION

定义前向/回滚迁移、兼容窗口、备份和数据验证。

Primary output: `migration-plan`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 6. DEPLOYMENT_PLAN

定义步骤、批次、审批、指标、停止和回滚条件。

Primary output: `release-plan / rollback-plan`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 7. ROLLOUT

按 canary/灰度/分批方式执行；每步验证后才扩大。

Primary output: `deployment-evidence`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 8. PRODUCTION_VERIFICATION

验证合成旅程、核心指标、日志、错误率和数据正确性。

Primary output: `production-verification`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 9. STABILIZATION

观察完整风险窗口，处理告警、回滚或补救。

Primary output: `observability-ready`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

### 10. REVIEW

记录结果、偏差、事故和改进，通过 production-ready。

Primary output: `production-ready`.

Exit only when the output has explicit acceptance criteria, registered evidence and no hidden critical blocker.

## Regression and re-entry

- New contradictory evidence: return to the earliest stage that owns the invalid assumption.
- Downstream implementation constraint: distinguish a true constraint from convenience; update the owning artifact and traceability.
- Critical risk: block progression unless mitigated, explicitly accepted or formally waived.
- Small bounded request: execute only affected stages while preserving upstream/downstream checks.
