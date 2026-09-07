# 系统全景图

```text
Goal / Existing Project / Incident
              │
              ▼
       Global Orchestrator
              │
     Tailoring + Domain Packs
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
    PM-OS  Design-OS Engineering-OS
      │       │        │
      └── Gates / Evidence / Trace ──┐
                                    ▼
                                  QA-OS
                                    ▼
                                Release-OS
                                    ▼
                               Evolution-OS
                                    │
                      Actual vs Expected / Root Cause
                                    └────→ Re-entry to owning OS
```

## 横向能力

```text
Local Shared Kernel / PostgreSQL Control Plane
RBAC / Approvals / Audit / Recovery / Secrets
Skill Lock / Security Scan / Effectiveness Lifecycle
Design Single-Director / QA Separation-of-Duties
Evolution Generic Core + Explicit Observability Adapters
USD / Token / Tool / Human Cost Governance
Evidence Collector / Dashboard / Job Queue
L5-B Matched Experiment
```

## 全链路追踪

```text
User Problem → Goal → Requirement → Flow → ADR → Code
→ Test → Release → Telemetry → Learning Decision
```

所有下游结论必须能追溯到上游原因；上游变化会污染下游状态。
