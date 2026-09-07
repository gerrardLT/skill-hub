# Changelog

## v2.5.0

- Added evidence-backed third-party Skill supply-chain intake/audit/lock pipeline.
- Added isolated formal L5-B execution runner with independent-context attestation and blind review.
- Added strict live PostgreSQL concurrency/dead-letter/advisory-lock/connection-loss validation.
- Added tamper-evident wall-clock soak runner; synthetic/backdated evidence cannot become formal.
- Added organization drills for RBAC, separation of duties, AES-GCM master-key rotation, backup/restore and audit export.
- Production Candidate maturity gate now re-opens artifacts and requires all five formal evidence classes.
- Regression: 116/116 tests + 7 subtests PASS; red team 68/68 PASS.

## 2.4.0

- Design-OS Core 去重为单主视觉导演 + UI/UX 知识层 + Web 规范层 + Motion 专项层；`frontend-design` 和 `design-taste-frontend` 降为条件性。
- QA-OS 重构为独立验证体系：新增 `testing-strategy`、`qa-only`、`code-review`、`playwright` Core；产品源码修复强制回流 Engineering。
- Evolution-OS 重构为厂商无关 Generic Core：systematic debugging、incident response、metrics、feedback、data validation、experiment design。
- 新增 Sentry / Datadog / PostHog 显式 Provider Adapter；无项目证据时禁止自动激活。
- 外部 Skill 安装器新增 `--provider`，支持 Agent-specific plugin，重复套件去重与不支持 Agent 的 fail-closed。
- Skill Governance 将 11 个 Provider Adapter 纳入锁定/冲突检查；外部未锁定条目由 60 增至 71，默认全部禁止安装。
- 新增 8 个 v2.4 组合回归测试和 5 个红队用例。
- v2.4 回归：106/106 tests + 7 subtests PASS；红队累计 60/60 PASS；7/7 Skills 静态验证 PASS。

## 2.3.0

- 修复 SQLite 多 Worker 任务领取竞态：使用原子条件 UPDATE + RETURNING，50 个任务压力下保持 50 次唯一领取。
- 项目状态更新升级为 revision compare-and-swap；并发重试压力下 revision/counter 精确收敛且审计链完整。
- 新增 `control_plane_stress.py`，覆盖任务并发、状态并发、过期 Job 重入队、过期 Lease 回收和审计完整性。
- L5-B 升级为严格匹配协议：相同起点/环境/模型/工具、独立执行上下文、平衡执行顺序、完整独立盲评、最终封存。
- 未封存真实 L5-B 只能输出 `provisional-*`；Synthetic 永远不能成为正式提效证据。
- 新增 `maturity_gate.py` 和成熟度策略；缺真实 L5-B、Live PostgreSQL、3 个可执行真实项目、30 天 soak 或组织级演练时禁止 Production Candidate 声明。
- 新增 6 个 v2.3 红队用例。

## 2.2.0

- 新增安全工作按责任归属路由：Remediation → Engineering，Verification → QA，Secret Rotation/Deployment → Release。
- 新增实施就绪度/外部前置审计路由：Research/Design/Protocol/Regulatory 输入用于 Build Readiness 判断时归 PM。
- 新增中英文真实任务改写回归，保持低置信 abstain，不以提高覆盖率换取错误自动路由。
- 使用 zwzz 绿地设计/研究包验证 PM Ready 阻断：关键设备协议、监管、支付和许可前置未闭合时禁止直接 Build。
- 使用 ZW-Insight 企业 SaaS Brownfield 发现供应商 JWT 默认签名密钥风险；源码修复后因 Maven/集成/生产轮换证据缺失，Verification Gate 正确阻断。
- Dogfooding 明确跨项目规则隔离：项目显式镜像/部署策略不得因其他仓库经验被机械判定为缺陷。

## 2.1.0

- 新增 Project Profile + Work Item Profile 双层动态裁剪。
- 新增 `work-start`、`work-status`、`work-end`，支持 bounded change 独立风险画像。
- Artifact/Evidence/Risk/Decision/Trace/Run/Learning 增加 Work Item 作用域，禁止跨变更借用旧证据。
- Gate、Quality、Trace、Health 改为按制品所属 Work Item 的治理档位复核。
- Domain Pack 改为按 Work Item 实际影响启用。
- bounded-lite 采用三核心制品，并压缩 Engineering/QA 状态机。
- 使用真实 aus-ele Brownfield 项目 Dogfooding；修复 v2.0 在小变更上的过度流程化与作用域漏洞。

## 2.0.0

- 新增 PostgreSQL-ready 生产控制面、乐观 revision、快照和哈希链审计。
- 新增分布式 Lease/fencing、幂等任务队列、heartbeat/retry/dead-letter/recovery。
- 新增 RBAC、独立 Gate 审批、AES-GCM Secrets、Outbox。
- 新增风险驱动的 Lite/Standard/High-Assurance 自动裁剪。
- 新增一键项目初始化和 Web Dashboard。
- 新增测试、覆盖率、制品与部署证据采集器。
- 新增 Skill 安全扫描、版本锁、冲突检测、效果生命周期。
- 新增 USD/Token/工具/人力预算治理。
- 新增 HarmonyOS、SaaS、AI Agent、电商、金融领域包。
- 新增 L5-B 匹配对照实验 Harness。
- 新增五类多项目参考验证和 PostgreSQL 静态一致性验证。
- 英文路由覆盖增强；保留低置信 abstain。

## 1.4.0

- 完成单项目 L5-A 可执行 Dogfooding。
