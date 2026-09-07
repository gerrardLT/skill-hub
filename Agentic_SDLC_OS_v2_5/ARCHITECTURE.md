# 架构

## 1. 分层

```text
Experience Layer    CLI / Bootstrap / Dashboard / Approval UI
Orchestration Layer Global Router + 6 Domain OS
Governance Layer    Gates / RBAC / Budgets / Skill Lock / Domain Policies
State Layer         Local .sdlc Kernel or Database Control Plane
Execution Layer     Skills / Subagents / Jobs / External Tools
Evidence Layer      Code / Tests / Coverage / Deploy / Telemetry / User Feedback
```

## 2. 本地 Shared Kernel

单写入者项目使用 `.sdlc/`：

```text
.sdlc/
├── state.json              机器事实源
├── config.json             流程、预算和领域策略
├── audit/events.jsonl      哈希链审计
├── ledgers/                证据、假设、决策、风险、制品、追踪、学习、运行
├── gates/                  Gate 评估
├── domain-packs/           激活的领域约束
└── evidence/               自动采集证据
```

accepted 制品记录内容哈希和质量评分。上游变化会使可达下游制品 `stale`；旧 Gate 或 Waiver 自动失效。


## Specialist composition governance

```text
Design      = one primary visual director + knowledge/constraint/motion layers
QA          = independent verifier; production remediation belongs to Engineering
Evolution   = vendor-neutral Generic Core + explicit Sentry/Datadog/PostHog Adapter
```

Third-party specialists are dependencies, not authorities. They remain below Work Item scope, evidence quality, Gate and human authorization. Provider adapters are activated only by project/deployment evidence and cannot own `learning-decision`.

## 3. 数据库控制面

多人、多 Agent 或并发 Runner 使用 `control_plane/`：

- SQLAlchemy + PostgreSQL；SQLite 仅用于本地与测试。
- 项目 revision 实现乐观并发控制。
- revision snapshot + hash-chained project events 支持恢复和篡改检测。
- 分布式 Lease 使用 TTL 与单调 fencing token；外部副作用必须校验 token。
- Job Queue 支持幂等、优先级、lease、heartbeat、retry、dead-letter、reap。
- Approval 绑定项目 revision；项目变化后审批变为 stale。
- 高保障项目强制申请人与批准人分离。
- RBAC、Bearer Token、AES-GCM Secret、Outbox、恢复巡检。

## 4. 状态机与 Gate

```text
PM → Design → Engineering → QA → Release → Evolution
↑                                             ↓
└────────────── evidence-based re-entry ──────┘
```

| Gate | 交接 |
|---|---|
| `pm-ready` | PM → Design |
| `design-ready` | Design → Engineering |
| `build-ready` | 技术设计 → Build |
| `verification-ready` | Engineering → QA |
| `release-ready` | QA → Release |
| `production-ready` | Release → Evolution |
| `learning-decision` | Evolution → 任一 OS |

Gate 验证：制品内容、完整性、证据质量、有向追踪、领域覆盖、风险和独立审批。关键风险不能被综合分、Waiver 或预算压力抵消。

## 5. 动态裁剪

`process-tailoring.json` 对九项风险打分，并由硬升级规则覆盖综合分。领域包追加风险、控制、制品、证据和 Gate overlay。

- Lite：低风险、可逆、小影响。
- Standard：普通生产项目。
- High-Assurance：高敏感、受监管、不可逆、大影响面。

## 6. Skill 治理

每个 Skill 都有内容哈希、来源、许可证审查状态、安全状态、生命周期和效果分。严格模式拒绝未锁定外部 Skill。运行结果可把 Skill 从 canary 提升为 active，或降级为 quarantine/retired。

## 7. 成本治理

预算在执行前评估，在执行后记账。降级顺序优先减少投机性并行和重复研究；安全、隐私、关键风险、回滚和事故响应不可因预算被关闭。

## 8. 证据与实验

L0–L4 验证控制正确性；L5-A 验证真实需求能否形成可运行闭环；L5-B 才验证相对普通 Agent 的净收益。合成实验只验证 Harness，不作为效果证据。
## Project governance vs Work Item governance

The project Profile is a default envelope, not a permanent tax on every change. v2.1 introduces an active Work Item layer: bounded changes are rescored from their affected paths, risk factors and domain impacts. Gates, artifact quality and compressed stages use the active Work Item Profile; unbounded or hard-risk work cannot downshift. Records are scoped by `work_item_id` so evidence is not silently reused across unrelated changes.

