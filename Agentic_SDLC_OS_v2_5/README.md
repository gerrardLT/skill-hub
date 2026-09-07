# Agentic SDLC Operating System v2.5

一套可执行、可审计、可回退的 AI 软件全生命周期操作系统。它把产品、设计、工程、测试、发布和线上演化连接为一个证据闭环，而不是一组孤立提示词。

> **定位：本仓 = Agentic SDLC「治理内核」（Governance Kernel），不是开箱即用的专家能力包。**
> 它提供六域编排、Shared Kernel、Gate 交接链、证据/成本/哈希审计、Skill 治理与成熟度 Gate；但**不内置**各域真正执行的专家 skill（design / engineering / qa 等）。当前 **71 个外部专家 / Provider Adapter 候选全部 `deny-unlocked`**（`strict_external_install_ready=false`、`install_allowed=false`）。因此开箱状态只是一副治理骨架，需按 `SKILLS_RANKINGS.md` 与 `THIRD_PARTY_SKILLS.md` 完成供应链 intake 与 Commit 锁定后**另行安装**，六域专家能力方可启用。

## 体系

```text
Agentic SDLC Orchestrator
├── Shared Kernel：状态、证据、假设、决策、风险、追踪、Gate、运行成本
├── PM-OS
├── Design-OS
├── Engineering-OS
├── QA-OS
├── Release-OS
└── Evolution-OS → 依据真实结果回流任一上游 OS
```



## v2.5 Specialist Skill 组合升级

- **Design-OS 去重**：Core 收敛为 `impeccable + ui-ux-pro-max + web-design-guidelines + review-animations`；同一工作项只允许一个主视觉导演。
- **QA-OS 职责分离**：Core 改为 `testing-strategy + verification-before-completion + qa-only + code-review + playwright`；QA 不得修改产品源码后自我验收。
- **Evolution-OS 厂商解耦**：Generic Core 负责诊断/指标/反馈/数据/实验；Sentry、Datadog、PostHog 改为显式 Provider Adapter。
- **外部 Skill 治理扩展**：60 个六域通用候选 + 11 个 Provider Adapter 全部进入 Skill Lock；未锁定 Commit 时继续 fail-closed。
- v2.5 回归：**116/116 tests + 7 subtests PASS；68/68 红队 PASS；7/7 OS Skills PASS**。
- 成熟度仍为 **Beta Candidate**，未因 Skill 组合升级而放宽生产证据要求。

## v2.3 生产声明与并发安全升级

- SQLite 本地模式的 Job Claim 与 Project Revision 已改为数据库原子 CAS，避免多 Worker 双领和静默丢写。
- L5-B 强制相同起点/环境/模型/工具、独立上下文、平衡顺序、完整盲评和最终 Seal。
- 新增 Maturity Claim Gate：证据不足时系统直接拒绝 Production Candidate 标签。
- 当前成熟度仍为 **Beta Candidate**；Live PostgreSQL、正式 L5-B、30 天 soak 尚未完成。

## v2.2 多项目 Dogfooding 升级

1. **安全任务按责任路由**：鉴权/密钥修复 → Engineering；独立安全验证/回归 → QA；生产密钥轮换与部署 → Release。
2. **实施就绪度路由**：当研究、设计、协议、监管或合规材料被用于判断“能否开始开发”时，路由到 PM，而不是被设计关键词误导。
3. **跨项目规则隔离**：项目自身策略优先于上一项目经验；例如 ZW-Insight 明确配置的 npm 镜像不会被 aus-ele 的 lockfile 经验机械判错。
4. **真实项目验证扩展**：新增 zwzz 绿地实施就绪审计与 ZW-Insight 企业 SaaS 安全修复；缺少运行环境时 Gate 保持阻断，不伪造测试通过。

## v2.1 真实项目 Dogfooding 升级

1. **双层流程裁剪**：项目 Profile 作为默认治理强度；每个 bounded Work Item 根据自身风险、影响路径和领域影响重新评估，允许安全降档但禁止绕过硬风险。
2. **工作项隔离**：Artifact、Evidence、Risk、Decision、Trace、Run、Learning 绑定 Work Item；不同变更不能复用历史证据“借过” Gate。
3. **按制品治理**：历史制品按照创建它的 Work Item Profile 复核，避免项目级 high-assurance 阈值误杀低风险小修复。
4. **领域包按影响启用**：安装了 AI Agent/SaaS 等 Pack 不代表每个变更都承受全部附加 Gate，只有实际受影响的工作项才启用。
5. **Bounded-lite 压缩**：低风险小变更采用 `Change Plan → Change Verification → Release Recommendation`，并压缩工程/QA 阶段；测试与审查作为证据而非重复文档。
6. **真实 Brownfield 试点**：在 aus-ele 仓库中识别并修复 lockfile 镜像污染，同时由真实流程暴露并修复上述控制面问题。

## v2.0 八项升级

1. **L5-B 匹配对照实验**：预注册、随机顺序、盲评、链式哈希、配对 Bootstrap 与污染判定。
2. **多项目验证**：Web SaaS、HarmonyOS、AI Agent、旧系统改造、金融发布五类可执行参考场景。
3. **生产级控制面**：PostgreSQL-ready、乐观并发、分布式租约与 fencing、任务队列、RBAC、审批、审计、恢复、AES-GCM 密钥。
4. **使用体验**：风险裁剪的一键初始化、Web 看板、Gate 审批、代码/测试/覆盖率/部署证据自动采集。
5. **动态流程裁剪**：九项风险因素选择 `lite / standard / high-assurance`，硬风险自动升级。
6. **Skill 治理**：安全扫描、版本锁定、冲突检测、效果评分、隔离与淘汰策略。
7. **成本治理**：USD、Token、工具调用、人力预算；预判、降级、阻断和受保护工作。
8. **领域扩展包**：HarmonyOS、SaaS、AI Agent、电商、金融。

## 快速开始

```bash
# 一键初始化：自动选择最小安全流程
python scripts/bootstrap_project.py ./my-project --name my-project \
  --domain-pack saas --budget-usd 25 --token-budget 500000 \
  --blast-radius 2 --data-sensitivity 2 --user-exposure 3

# 查看状态和下一步
python skills/agentic-sdlc-os/scripts/sdlc.py status ./my-project
python skills/agentic-sdlc-os/scripts/sdlc.py next ./my-project

# 对已有项目中的一个有界变更单独裁剪
python skills/agentic-sdlc-os/scripts/sdlc.py work-start ./my-project \
  --id WORK-001 --title "修复依赖锁文件镜像" --bounded \
  --affected-path web/package-lock.json
python skills/agentic-sdlc-os/scripts/sdlc.py work-status ./my-project

# 自动采集测试与制品证据
python scripts/collect_evidence.py ./my-project \
  --test-command "python -m pytest" --artifact dist/app.zip --register
```

## 多人/多 Agent 控制面

```bash
python scripts/control_plane.py generate-master-key
python scripts/control_plane.py init-db --database-url sqlite+pysqlite:///control.db
python scripts/control_plane.py serve --database-url sqlite+pysqlite:///control.db --port 8787
```

生产部署使用 `docker-compose.yml` 与 PostgreSQL；必须替换示例凭据并接入正式密钥管理。

## 验证

```bash
python scripts/run_validation.py
python scripts/postgres_conformance.py
python validation/l5b/generate_synthetic_smoke.py
python scripts/build_release.py
```

当前证据边界：

- L0–L4 控制与对抗测试：可本地复现。
- L5-A 单项目可执行 Dogfooding：已有。
- 五类多项目**参考场景**：已执行，但不等同于五个外部真实项目的长期运营。
- L5-B 工具链：合成烟测通过；真实普通 Agent 对照尚需实际运行。
- PostgreSQL：DDL 静态一致性通过；当前环境未执行 live PostgreSQL 集成测试。
- 不能据此宣称已经因果证明提效、降本或达到 30 天生产稳定性。

详细说明：`ARCHITECTURE.md`、`INSTALL.md`、`USAGE.md`、`PRODUCTION_READINESS.md`、`VALIDATION_REPORT.md`。
