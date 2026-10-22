# GOAL：Capability Compiler V2 全量 Skills 融合与完整软件生产系统

## 最终状态

仓库中的 139 个 Skill roots 及其必要引用文件均被逐文件读取或以明确理由排除；所有纳入能力均完成来源可追踪的原子化、同类比较、重复消解、互补合并、冲突裁决与条件变体保留，并被重写为本项目自有、可独立调用、可组合、可评测的 V2 Skills。V2 通过条件化 Recipes 覆盖从模糊产品想法到产品发现、UX/UI、架构、数据/API/权限/安全、实现、测试、性能、交付、观测、回滚、事故响应与复盘的完整软件生命周期。现有 V1 在建设期保持稳定；V2 仅在机器 Gate、真实项目验证与人工语义评审全部通过后受控发布。

## 验收——全部满足且有证据才算完成

### A. 全量来源覆盖

- Inventory 覆盖当前冻结基线中的全部 139 个 Skill roots；新增、删除或内容变化必须显式报告。
- 每个 Skill root 的 `SKILL.md` 及其声明或实际依赖的必要 references/scripts/templates/examples 均有逐文件状态：`read` 或 `excluded`。
- `excluded` 必须有具体、可审计理由；未分类文件数为 0。
- 每个已读文件保存路径、内容 hash、读取状态和来源版本证据。
- 原始 `skills/` 保持不可变；任何 hash 漂移均使来源 Gate 失败。

### B. 能力提取与融合

- 每个纳入的语义单元都包含：来源位置、原文证据、意义、适用边界、依赖、失败模式、候选去向与验证标准。
- 每个纳入 Unit 恰好归属一个主要能力簇，或有明确 defer/exclude 决策；悬空与重复分配均为 0。
- 每个能力簇都必须有同类比较矩阵，显式记录：`duplicate`、`complementary`、`conditional-variant`、`conflict`、`strong-dependency`；不得只生成 source index。
- 每个冲突都有保留、合并、条件分支或拒绝的裁决及理由。
- 每个 V2 Skill 必须是重新综合后的本项目能力，不得只是原 Skill 拼接或 source-index skeleton。
- 每个 V2 Skill 的 provenance 可双向追踪到来源 Units 和裁决记录。

### C. 完整软件生命周期能力

V2 至少形成并验证以下能力域；具体 Skill 数量由语义边界决定，不预设一个 Skill 对应一个领域：

1. 产品发现、用户研究、问题验证、产品策略、优先级、需求与成功指标。
2. UX 流程、信息架构、原型、视觉方向、设计系统与 Token、响应式布局、组件与交互状态、内容文案、可访问性、动效、真实渲染评审。
3. 系统架构、模块边界、数据模型、API Contract、权限模型、安全、第三方依赖、迁移与可观测性设计。
4. 实施计划、TDD、前后端实现、代码评审、Unit/Integration/E2E、回归、安全与性能验证。
5. 交付预检、配置与 Secrets、数据库迁移、部署、Canary、监控、回滚、事故响应、指标回顾与复盘。

### D. 条件化 Recipes 与路由

- 根据项目类型与风险选择必要分支，而非所有任务强制走同一路径。
- 至少提供经过验证的 `greenfield-fullstack-web` 完整 Recipe；它必须包含真正的 UX/UI 分支，不得以“设计方向”替代 UI 设计与验证。
- 同一输入、锁定版本与授权条件下，路由与产物合同可复现。
- 未发布 Skills 不得进入 released Recipe；版本必须精确锁定。
- 阶段之间传递独立逻辑产物，不得把需求、设计、实现、QA 折叠为同一 bundle。

### E. Skill 质量评测

- 每个拟发布 V2 Skill 都有冻结的 baseline、candidate、holdout、mutation suites。
- 每个 suite 保存真实模型输出、工具事件、命令、退出码、耗时、产物路径与 SHA-256。
- Candidate 必须相对 baseline 有可解释改进；holdout 不得依赖训练案例措辞；mutation 必须证明 Gate 能发现关键缺失或篡改。
- 主观产物（产品、UI、设计）必须有人类可审查的并排输出与明确 rubric；客观产物必须优先使用可执行断言。
- 触发描述须有 should-trigger / should-not-trigger 测试，避免错误路由。

### F. 真实端到端验收

- V2 正式发布前，必须完成一个从模糊想法开始的全新全栈 Web App 真实案例。
- 案例须覆盖：产品需求、UX/UI、响应式与可访问性、前后端、数据/API/权限、安全、测试、真实浏览器渲染评审、性能、交付预检、部署计划、观测、回滚方案与复盘。
- 实现运行于隔离 worktree/snapshot；宿主执行测试、构建、lint、浏览器和性能检查。
- 最终必须有可运行应用、本地交付包、完整 patch、证据 manifest、残余风险和人工评审包。
- 实际远端部署仅在届时获得一次性明确授权后执行；没有授权时，部署阶段以可复算的预检与计划收束，不冒充已经部署。

### G. 全局 Gate

- 全仓 tests、schema、source、provenance、coverage、relationship、slot、recipe、runtime、security、evidence、lifecycle、release Gates 全绿。
- 发布报告不得读取陈旧自报状态；关键事实必须重新计算。
- 人工逐域批准产品、UX/UI、架构、实现、QA、交付与复盘后，发布器方可将 V2 从 `evaluating` 提升为 `released`。
- 最终状态文档必须分别报告：来源覆盖完成度、融合完成度、评测完成度、生命周期覆盖度和已发布资产；不得再用一个 `complete` 混淆局部 Gate 与整体产品完成度。

## 不变量——任何时候不得违反

- 原始 `skills/` 不可修改；来源内容只读并以 hash 监控。
- V1 的 10 个 released Slots 与 8 个 released Recipes 在 V2 建设期保持可运行；V2 使用独立版本与候选路径，不覆盖 V1。
- 未经明确授权，不执行 remote Git、push、PR、merge、部署、云资源修改或外部系统写入。
- 实际部署即使属于 Recipe，也必须取得当次明确授权；默认只做本地构建、预检、打包与计划。
- QA、设计评审与发布评审默认只读；实现写权限必须绑定隔离工作区和授权范围。
- 不得以手写 `passed: true`、模拟命令结果、删除失败测试、放宽阈值、跳过 suite、伪造 hash 或复用陈旧证据制造达标假象。
- 不得为了减少工作量把全部原始 Skills 直接拼接进一个巨型 Skill；应按单一职责和渐进披露设计。
- 不得强行吸收与软件生产无关的能力；但每项排除必须有领域分类与理由，并保留可追溯决策。
- 遇到用户意图、范围、业务语义、风险接受度或不可逆操作不确定时，必须暂停并使用交互问题请求裁决。

## 边界

### 允许修改

- `.specs/capability-compiler-v2/`
- `curation/`
- `slots/` 中新增的 V2 候选及现有元数据的兼容扩展
- `recipes/` 中新增的 V2 候选及 schema/catalog 的兼容扩展
- `evals/`
- `tools/curation/`
- `tests/curation/`、必要的 evaluation tests
- `docs/`
- `.github/workflows/verify.yml`
- `dev-loop/` 的 V2 兼容接入
- 项目根状态文档，但必须区分 V1 与 V2

### 只读

- `skills/`
- 外部来源缓存与第三方仓库原始快照
- 现有 V1 released 资产的行为合同；若发现必须修改，先提出迁移方案并等待确认

### 外部项目

- 仅可使用独立 worktree/snapshot；不得修改用户原始脏工作区。
- 任何远端、付费、不可逆或生产操作均需单次明确授权。

## 阶段执行协议

每一阶段开始前，先创建该阶段的 `phase-plan.md`，至少包含：

1. 本阶段目标与非目标。
2. 与当前仓库真实状态的上下文匹配结果。
3. 输入来源、依赖和前置 Gate。
4. 细分任务及顺序。
5. 允许修改与只读路径。
6. 预期产物和稳定 ID。
7. 验收命令、量化阈值和人工评审点。
8. 风险、未知项和需用户裁决的问题。
9. 失败回滚与证据失效策略。

若存在第 8 项中的真实不确定性，暂停并询问用户；若没有，则直接实施，不为形式性确认停工。

## 迭代策略——每轮必须走完

1. 先读取阶段计划、上一阶段证据和当前仓库状态，建立可重复 baseline。
2. 更新假设账本：当前假设、支持证据、反对证据、已排除路线。
3. 选择能最大区分当前竞争假设的最小、可归因改动。
4. 实施后运行本阶段完整验收面，不只运行局部测试。
5. 记录“假设 → 改动 → 结果 → 下一实验”，并保存输出与 hash。
6. 阶段 Gate 不通过，不进入下一阶段；返回当前阶段修复。
7. 主观 Skills 使用基线对照与人工评审；客观 Skills 使用可执行断言与 mutation。
8. 不重复已证伪路线；新证据改变方向时，以证据为准。

## 阶段顺序

0. 全量来源与现有产物真实性复核。
1. 逐来源深读、原子能力补全与语义关系审计。
2. 按软件生命周期重构能力域与融合规范。
3. 提纯并验证产品发现与需求 Skills。
4. 提纯并验证完整 UX/UI Skills 与 Recipe。
5. 提纯并验证架构、数据、API、权限与安全 Skills。
6. 提纯并验证实现、测试、评审与性能 Skills。
7. 提纯并验证部署、观测、回滚与事故响应 Skills。
8. 组装条件化完整软件生产 Recipes 与路由器。
9. 执行多域 baseline/candidate/holdout/mutation 评测。
10. 候选人工语义评审与修订，不执行正式发布。
11. 全栈 Web App 端到端真实验收与最终文档。
12. 最终人工批准与受控发布。

## 停止条件

### 完成

仅当 A–G 全部有最新证据通过，V2 人工评审批准，受控发布完成，且最终状态报告无 blocker 时，方可声明整体完成。

### 阻断

遇到以下任一情况应停止并报告，而非猜测：

- 缺少来源文件、许可或必要附件，无法完成可信读取。
- 业务语义、生命周期边界、真实项目需求或风险接受度需要用户裁决。
- 必须越过允许路径、执行远端/生产操作或破坏 V1 才能继续。
- 连续 3 轮无实质进展。
- 评测方法不能区分 candidate 与 baseline。

阻断报告必须包含：已尝试路线、关键证据、最可能原因排序、真正 blocker、解除所需输入。

## 当前已确认的用户决策

- 来源范围：全部 139 个 Skill roots。
- 部署边界：默认预检；只有当次明确授权后才允许真实部署。
- V2 发布前强制真实案例：从零全栈 Web App。
- 阶段控制：每阶段先细分；仅在有不确定项时暂停询问，否则直接实施。
- 兼容策略：V1 稳定运行，V2 以并行候选建设。


## 假设账本

| # | 假设 | 支持证据 | 反对证据 | 状态 |
|---|---|---|---|---|
| H1 | 旧 965 canonical Units 仅足作语义审计起点，须与 retained auxiliary、root-derived atoms 及 support fragments 共同重构 | Phase 1/2 Gate；157 个 source-grounded candidate capabilities | 82 个 V1 Slot 仍只是 source-index skeleton | 已验证 |
| H2 | 现有 Compiler/runtime 可承载 V2，无需重写执行底座 | 25 Gates、343 tests、真实 QA 回跳、Phase 2–7 fail-closed Gates | 尚未验证 Phase 8 条件化 UI/部署 Recipes 与 Phase 11 全栈案例 | 部分验证 |
| H3 | UI/UX 候选来源已足够形成首个深度融合域 | Phase 2 有 17 个 Phase 4 owning capabilities，且 review/remediation identities 已分离 | 尚无完整 UI baseline/candidate/holdout/mutation 与真实渲染评审 | 待验证 |
| H4 | 生命周期 taxonomy 必须把 review/repair、preflight/remote change、observation/rollback 作为不同权限身份 | Phase 2 side-effect audit、11 项 mutation tests、0 permission violations | 后续 Skills/Recipes 尚须证明运行时仍保持分离 | 当前最强 |

## 轮次记录

### R0：合同定稿
- 假设：先保留 V1、并行建设 V2，可避免破坏已验证闭环。
- 改动：确认全量 139 roots、授权部署边界、强制 greenfield fullstack Web 验收、ask-uncertain-only 阶段控制，并重排最终发布顺序。
- 结果：用户批准合同；V2 可进入阶段 0。
- 下一实验：复核 139 roots、597 个已登记文件、现有 dossiers/units/clusters 与真实磁盘内容，建立 V2 baseline。

### R1：Phase 0 全量真实性 baseline
- 假设：现有来源未漂移，但旧 coverage 只覆盖了部分文件，且“965 Units / 92 Slots”不等于已完成融合。
- 改动：新增可复算 Phase 0 audit、V1 compatibility manifest、forward gaps 和失败测试；处理 raw/normalized root hash 算法差异。
- 结果：139 roots 与 2,337 文件 source baseline 完全一致；64 roots 已有 coverage，75 roots 未覆盖；597 个源文件已分类，1,740 个未分类；965 canonical Units 已聚类，114 auxiliary Units 待处置；10 Slots released，82 个只是 source-index skeleton。全仓 18 Gates 通过，224 tests passed。
- 下一实验：Phase 1 逐 root 补 coverage，逐文件 read/exclude，统一 114 auxiliary Units，并将 15 条关系扩展为逐 cluster 的完整语义对照。

### R2：Phase 1A 与融合政策
- 假设：旧 `read` 声明不能证明 V2 深读，巨型来源 Skill 也不应直接成为生产 Skill。
- 改动：建立 139 roots / 2,337 files V2 review ledger、61,361 行 source index、9 个互斥审阅批次、root dossier schema、auxiliary normalization/matching、cluster comparison Gate 与 Phase 1 aggregate Gate；用户批准七项融合政策。
- 结果：所有 roots/file identities 已入账；114 auxiliary Units 已规范化；V2 明确采用原子 Skills、语境化审美规则、人工产品决策、强制数据治理、命名公式变体、来源缺陷 defer-and-rewrite、三状态加 subkind。首轮 9-lane 只读审阅因 workflow timeout 仅完成 6 条；三条缺失 lane 经用户授权由主流程只读 fallback 完成，provenance 明确区分，未冒充子代理产物。
- 下一实验：将全部审阅证据转换为结构化 dossiers、Units、comparison matrices 与关系裁决。

### R3：Phase 1 全量语义审计完成
- 假设：139 个 dossiers 与文件分类仍不足以证明全量原子化；旧 965 canonical Units 仅覆盖 49 个 roots，另 90 个 roots 必须补 source-grounded atoms。
- 改动：生成并验证 139 个 root dossiers；将 2,337 文件分类为 914 semantic-read、1,296 behavior-reviewed、127 excluded；处置 114 auxiliary Units；为旧未覆盖的 90 roots 提取 1,138 条 source-exact records，并将 208 条 exact duplicates 合并为 930 个 distinct deferred atoms；为 88 clusters 建 source × 7 dimensions matrices、232 source-pair audits、17 explicit relationships 与所有 dependency audits；把七项用户政策写入敏感 cluster fusion rules。
- 结果：Phase 1 七层 Gate 全绿；114 auxiliary dispositions 为 104 retain、8 defer、2 merge；88/88 comparisons、88/88 relationship audits、unresolved conflicts=0；V1/source drift=0。全仓 19 Gates 通过，261 tests passed（1 个第三方 deprecation warning）。Phase 1 evidence manifest 含 249 个 artifacts，tree SHA-256 `ae9df68a96715066d715db9dce312f573b66f0d0c484e40d6c4a223c4760d608`。
- 下一实验：Phase 2 将 930 个 deferred root atoms 与现有 88 clusters 重构为覆盖完整软件生命周期的能力域与融合规范；不直接扩增巨型 Skills。

### R4：Phase 2 生命周期 taxonomy 与权限身份完成
- 假设：旧 88 clusters 不能直接充当 V2 原子能力；多阶段来源须拆为 atomic capabilities，Recipe 壳须 defer，且 source side effects 必须决定 permission identity。
- 改动：建立 11 domains、15 stages、13 mandatory handoffs、157 个 candidate capability contracts、结构化 provider variants、1,244 条 fusion decisions 与 249 条 dependency decisions；分类 1,138 root atoms 为 878 assign、49 defer-to-Recipe、3 fixture exclude、208 exact merge；拆分 observability eval、autoplan、QA、website audit、subagent pipeline、design review、ship、land/deploy、Sentry 与 Datadog mixed workflows；新增 source-fragment provenance，分离 review/repair、preflight/push/PR/merge/deploy、observation/rollback 与 artifact/local-system writes。
- 结果：88 legacy clusters、965 canonical Units、104 retained auxiliary Units 均唯一归属；0 orphan capabilities、0 dependency islands、0 hard cycles、0 policy violations、0 known mutation-identity violations。Phase 2 Gate 九层全绿；定向 mutation/manifest suite 11 passed。Phase 2 manifest 含 169 artifacts，tree SHA-256 `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`。
- 下一实验：Phase 3 只提纯 31 个 Phase 3 owning product/requirements capabilities，建立 V2 Skills、trigger contracts 与 baseline/candidate/holdout/mutation evidence；不提前实现 UI、architecture 或 deployment Skills。

### R5：Phase 3 产品发现与需求候选 Skills 完成
- 假设：Phase 2 taxonomy 只有在每项职责被重写为有具体 trigger、anti-trigger、procedure、output、hard gate 与 provenance 的 candidate Skill 后，才超越 source-index skeleton。
- 改动：为 31 个 Phase 3 owning capabilities 手工定义 semantic designs，并生成 31 套 `SKILL.md`、contract、provenance、trigger cases 与 evaluation plans；建立 186 authored routing cases、62 个物理分离的 holdout cases、31 个 planned mutations 和 8 组关键边界人工语义样本；修复 legacy contract 宽职责继承、holdout 复用、generic boundary placeholders、假 released baseline 与 compiler 删除人工证据五类问题。
- 结果：Phase 3 九层 Gate 全绿；31 candidates 均为 `evaluating@0.1.0-v2-candidate`，其中 25 workspace-write/run-output、6 read-only/no-mutation，released=0；所有 evaluation state 为 `not-run-phase-9`，未冒充模型评测或人工批准。全仓 21 Gates、283 tests 通过（1 个第三方 deprecation warning）。Phase 3 manifest 含 164 artifacts，tree SHA-256 `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`。
- 下一实验：Phase 4 提纯 17 个 UX/UI owning capabilities，补完整 user flow、IA、design system/tokens、responsive、states、accessibility、motion 与 rendered review candidate contracts；不得以设计方向 Skill 代替完整 UI 流程。

### R6：Phase 4 完整 UX/UI 候选 Skills 与 Recipe 完成
- 假设：完整 UI 能力须将方向、系统、内容、响应式、交互状态、无障碍、动效、AI 不确定性、真实渲染证据、独立评审与发布建议分为原子身份，再以条件 Recipe 编排；单一设计方向 Skill 或静态源码检查不足。
- 改动：手工重写 17 个 Phase 4 semantic designs，生成 17 套 candidate packages、102 authored cases、34 独立 holdouts、17 semantic mutations；建立 17-step `complete-ui-design-and-review` candidate Recipe、8 authored Recipe cases、4 holdouts、2 mutations。Recipe 对 new build、existing redesign、supplied external tokens、prototype variants、AI UX、motion 与 rendered review 条件分支，并保留 4 个人类 checkpoint。修复 Recipe 粗权限重新放宽、external token 网络越权暗示、optional branch 未回主流程、accessibility validation 暗示 local exec 四类问题。
- 结果：Phase 4 十一层 Gate 全绿；8 个 authorized-workspace 实现型 Skills、7 个 run-output 合同/审阅 Skills、2 个 artifact-only rendered-review Skills 精确分离。真实 rendered evidence 不得由静态源码、单截图或模型自报替代；review/preflight 不得修源码。全仓 22 Gates、297 tests 通过（1 个第三方 deprecation warning）。Phase 4 manifest 含 99 artifacts，tree SHA-256 `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`。全部仍为 `evaluating` / `not-run-phase-9`，released=0。
- 下一实验：Phase 5 提纯 16 个 architecture/data/API/auth/security owning capabilities，明确 trust boundaries、schema contracts、migration、idempotency、authorization、secrets、threat modeling 与 AI autonomy safety；不得让 architecture recommendation 自动执行 infra 或 security mutation。

### R7：Phase 5 架构、数据、API、权限与安全候选 Skills 完成
- 假设：架构与安全能力只有在 discovery、alternatives、module design、reporting、data/API、authorization、secrets、source hardening、AI autonomy 与 independent audit 使用不同 mutation scopes 时，方可防止建议自动变更系统或审计者自修自证。
- 改动：手工重写 16 个 Phase 5 semantic designs，生成 16 套 candidate packages、96 authored cases、32 独立 holdouts、16 semantic mutations；将 source side effect 收窄为 2 个 authorized-workspace Skills、11 个 run-output contracts、2 个 read-only/no-mutation reviewers、1 个 local-exec/artifact-only threat audit。修复 diagram candidate 无 local-exec 却声称 renderer validation，以及跨 Skill marker 可代偿 authorization `default-deny` 两类问题。
- 结果：Phase 5 十层 Gate 全绿；secret values 禁止 request/read/print/copy/transform/hash/persist/transmit；authentication 不代替 authorization；data/API 强制 compatibility、migration、idempotency、concurrency、error、authorization hooks 与 rollback；AI action rights 强制 human checkpoints、interruption、containment、revocation 与 fallback。全仓 23 Gates、310 tests 通过（1 个第三方 deprecation warning）。Phase 5 manifest 含 89 artifacts，tree SHA-256 `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`。全部仍为 `evaluating` / `not-run-phase-9`，released=0。
- 下一实验：Phase 6 分批提纯 54 个 implementation/testing/review/performance owning capabilities；先冻结 source mutation、local execution、artifact review 与 external-read identities，再按 build、test、review、performance 四组设计，避免 giant implementation workflow。

### R8：Phase 6 实现、测试、评审、性能与运行时候选 Skills 完成
- 假设：实现与验证领域必须以 atomic side-effect identity 拆分 source writing、local execution、artifact review、browser read、local-system mutation、external session 与 provider write；否则测试工具、评审、认证或 benchmark 会隐式获得项目或远端写权限。
- 改动：以四个手工 semantic-design 批次提纯 54 个 candidates，生成 324 authored cases、108 独立 holdouts、54 semantic mutations。精确保留 10 个 source writers、4 个 no-mutation reviewers、19 个 local-exec evidence Skills、5 个 local-system writers、2 个 external-session writers、2 个 remote-provider writers及其他 bounded identities。修复 direct-script import、local context 越权 external sync、4 个假 capability route、set-operator precedence、Playwright/Vitest local-exec 写项目及 local-system action boundary 六类问题。
- 结果：Phase 6 十层 Gate 全绿；TDD 强制 RED-before-code；completion 强制 current target-bound command/exit/duration/hash；review/QA/audit 不修源码；benchmark 强制 matched environment、warmup、repeats、variance 与 failed-case retention；external LLM Judge 须独立 transfer/provider 授权；browser login 不等于 data authority。全仓 24 Gates、326 tests 通过（1 个第三方 deprecation warning）。Phase 6 manifest 含 280 artifacts，tree SHA-256 `7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561`。全部仍为 `evaluating` / `not-run-phase-9`；2 remote-write、2 external-session、5 local-system candidates 均 `not-executed-phase-6`。
- 下一实验：Phase 7 分批提纯 39 个 deployment/observability/recovery/incident owning capabilities，严格拆分 preflight、packaging、push、PR、merge、deploy trigger、observation、rollback、incident response 与 postmortem；建设期不执行任何 remote/provider/production mutation。

### R9：Phase 7 部署、观测、回滚、事故与学习候选 Skills 完成
- 假设：delivery 与 production 能力须将 preflight、packaging、push、PR change/comment/merge、deploy trigger/adapter、observation、rollback、incident coordination 与 retrospective 拆成不同 one-action identities；否则一次远端授权会级联成不可控发布。
- 改动：以三批手工 semantic designs 提纯 39 个 candidates，生成 234 authored cases、78 独立 holdouts、39 semantic mutations；为 16 个 remote-write candidates 建立 16 个唯一 mutation scopes，并保持 12 observers、2 preflights、4 no-mutation analysts、3 local source writers、1 local-system writer 的精确身份。收窄 incident coordination 为 external-read 协调、deployment environment setup 为 local config-only，并机器锁定 canary baseline immutable、observation-not-rollback 与 one-authorization-never-cascades。
- 结果：Phase 7 十层 Gate 全绿；package→push→PR→readiness→merge→deploy 按独立证据和授权推进；merge 不授权 deploy；observation 不执行 rollback；incident coordination 不 acknowledge/close provider incident；telemetry 强制 minimization/redaction/sampling/retention/access/deletion。全仓 25 Gates、343 tests 通过（1 个第三方 deprecation warning）。Phase 7 manifest 含 205 artifacts，tree SHA-256 `c76902fd5df781db653e214268b044cb4a8cc389a4fce0a188f72a5fba829926`。全部仍为 `evaluating` / `not-run-phase-9` / `not-executed-phase-7`。
- 下一实验：Phase 8 组装条件化完整生命周期 candidate Recipes 与 router，覆盖 157 atomic capabilities、15 stages、13 mandatory handoffs、human checkpoints、feedback invalidation 与 remote-action stops；不得将全部 capabilities 串成单一 always-on 流程。

### R10：Phase 8 条件化生命周期 Recipes 与最小充分路由完成
- 假设：157 个 atomic candidates 只有在 primary stage 唯一归属、每步显式条件、权限身份不放宽、13 handoffs 可失效、stage 15 仅作横切支持、router 优先最小目标时，才可组成完整生命周期；直接串成 always-on giant workflow 会破坏原子边界与授权隔离。
- 改动：编译 15 个 stage Recipes、5 个 bounded/full composite Recipes、1 个 fail-closed router，并引用 Phase 4 专用 UI Recipe；157 candidates exactly-once 进入 primary stage，249 dependency records 按 target stage 无损投影，13 mandatory handoffs 保留四类 artifact contract 与四类 invalidation。建立 14 router authored cases、8 router holdouts、8 Recipe authored cases、6 Recipe holdouts、6 planned mutations与 16 组人工边界审阅；修复 full lifecycle precedence、`authorized-local-git` 未受保护及脆弱 schema 字面量三项问题。
- 结果：Phase 8 十二层 Gate 全绿；27 个 remote/local-system/external-session/local-git protected steps 均为 `disabled-pending-current-authorization`；atomic→stage→specialized UI→bounded composite→explicit full lifecycle→governance fallback 的最小充分顺序被机器锁定。全仓 26 Gates、362 tests 通过（1 个第三方 deprecation warning）；`git diff --check` 无 whitespace error。Phase 8 manifest 含 33 artifacts，tree SHA-256 `501d9cddfdc44fec4af8f17470c99b57b48ffced977e0fa7086cce568fa92f66`。全部仍为 `evaluating` / `not-run-phase-9`，released=0，远端、provider、browser-auth、local-system 与 production actions executed=0。
- 下一实验：Phase 9 对冻结的 157 Skills 与 21 Recipe/router targets 执行真实 baseline/candidate/holdout/mutation 评测；须保存模型输入输出、runner 命令、退出码、耗时、artifact hashes 与失败样本，不得将静态 cases 或模型自报当作通过证据。

### R11：Phase 9 真实模型评测完成，证据绿而发布阈值仍阻断
- 假设：静态 trigger fixtures 与 deterministic Gates 不能证明模型实际路由行为；真实评测须在无 tools 的 fresh Pi processes 中，对 baseline/candidate/holdout/mutation 作同模型配对，并将 evidence completeness 与 release quality thresholds 分离。
- 改动：冻结并执行 1,002 个 `router9-qoder/cx/gpt-5.6-sol` runs：628 Skill holdouts、314 Skill mutation control/mutants、12 Phase 4 Recipe runs、22 Phase 8 router runs、14 Phase 8 Recipe runs、12 Phase 8 mutation runs。每次保存 prompt/material/case/command/events/stderr/output/parse/run/grade/manifest；完成两次协议校准与一次 manifest migration，保留全部 20 个被拒校准 attempts，deleted failures=0。预先锁定 accuracy thresholds，不在结果后放宽。
- 结果：1,002/1,002 completed、1,002/1,002 strict parse、evidence errors=0、candidate actions=0，总计 5,709,179 tokens。Atomic Skills candidate unseen holdouts 为 314/314（100%），baseline 为 159/314（50.64%），配对 155 wins、159 ties、0 regressions，Phase 3–7 各 cohort 均 100%。但 Phase 4 Recipe 为 3/4，Phase 8 router 为 authored 9/14、holdout 5/8，Phase 8 Recipe 为 authored 8/8、holdout 4/6，故 `release_thresholds_passed=false`、`release_blocked=true`。全仓 27 Gates、374 tests 通过（1 个第三方 deprecation warning）；Phase 9 manifest 含 13,254 artifacts，tree SHA-256 `7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152`。
- 下一实验：Phase 10 在新的 revision 路径中人工裁决并修订六项 open findings：两项 Recipe gap、六项 explicit safety route、两项 atomic-vs-stage fixture conflict、Phase 4 human-checkpoint route marker、mutation challenge validity 与 lifecycle-approval/action-authorization distinction；不得改写 Phase 9 evidence、删除失败、降低阈值或提前发布。

### R12：Phase 10 全量语义评审与 Revision 4 完成
- 假设：Phase 9 的 157 Skills 已具稳定原子路由质量，修订应仅限 Recipe/router open findings；人工式语义评审须逐 Skill 读取两条真实 candidate outputs，不得以 aggregate 100% 代替，也不得把 parent-direct review 冒充最终用户发布批准。
- 改动：逐项审阅 157 Skills、314 candidate outputs，核验 decision、matched boundary、reason、tools/action denial 与 evidence path，157 项均 accepted、atomic revisions=0；裁决六项 Phase 9 findings。对 Recipe/router 依预写 stop condition 迭代四个隔离版本：Revision 1 为 50/56、Revision 2 为 54/58、Revision 3 为 59/60，全部失败证据保留；用户裁决不新增 renderer-bootstrap capability，无 owner 时 fail-closed，并明确授权 bounded Revision 3/4。Revision 4 仅前置 Phase 4 complete-route 的 `review-evidence`，未改 157 Skills。
- 结果：Revision 4 的 60/60 targeted runs、4/4 Phase 4 holdouts、14/14+8/8 Phase 8 router、8/8+6/6 Phase 8 Recipe、10/10 controls 与 10/10 causal mutants 全过，evidence errors=0、candidate actions=0。四轮共 234 runs、3,081,829 tokens，released claims=0；Phase 10 parent-direct review open findings=0，但 `final_user_release_approval=false`。全仓 28 Gates、383 tests 通过（1 个第三方 deprecation warning）；`git diff --check` 无 whitespace error。Phase 10 manifest 含 2,707 artifacts，tree SHA-256 `7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56`。
- 下一实验：Phase 11 以一个从模糊想法开始的全新全栈 Web App，在独立 snapshot/worktree 中执行真实需求、UX/UI、架构、前后端、数据/API/权限、安全、测试、浏览器渲染评审、性能、交付预检、部署计划、观测、回滚与复盘；无当次授权不执行远端部署。

### R13：Phase 11 BenchShare 全栈真实验收完成
- 假设：Revision 4 只有在一个从产品选择开始、跨需求、UX/UI、架构、安全、实现、独立 QA、真实性能、package、观测/回滚计划与复盘的隔离全栈案例中通过，才可进入最终人工批准；静态 contracts、unit tests 或单张截图均不足。
- 改动：用户选择 BenchShare 与 municipal-wayfinding 视觉方向；在独立 snapshot 中以 Python 3.12 stdlib + SQLite + native HTML/CSS/JS 实现 member request/cancel、coordinator approve/reject 与原子 overlap prevention。模型 writer 仅持 `read/edit/write`，宿主执行测试；独立 read-only review 发现 1 high + 5 medium 问题，先补 RED regressions，再由不同 writer 一次修复，confirmation 全关。真实 Playwright 三轮保留失败/拒绝证据，最终覆盖 12 个 desktop/mobile/keyboard/loading/empty/error/submitting/success/conflict/cancel states；独立 black-box QA 的两项 evidence gaps 亦经新 evidence 关闭。另作 50+50+20 local latency runs、十路并发审批、deterministic package 双构建、fresh unpack 14 tests、patch exact rebuild 与 DB backup/restore rehearsal。
- 结果：应用当前 tests 14 passed；browser iteration 3 与 independent QA 通过，unexpected console/page errors=0；health/list/create p95 分别 17.893/19.031/33.8ms，十路审批为 1 approved、9 conflicts、0 500、SQLite integrity ok。Package SHA-256 `8fb653c637294f2a10edd3f9d540d6dabf74a9d1d1dded71e6ab3c0445cf3309`，patch SHA-256 `15bf934015d39cdb2f0bb04185216474ba7641ceeec8293727c9c47907040a7f`。统一 29 Gates 全绿、390 tests passed（1 个第三方 deprecation warning）；`git diff --check` 无 whitespace error。Phase 11 manifest 含 335 artifacts，tree SHA-256 `275a2139cf207ac50105d3e65fd2138b371a3e2dbe0dce4b05ab043cb1cd5fbc`。失败 evidence deleted=0、thresholds lowered=false、remote/provider/production actions=0、released=false、final user release approval=false。
- 下一实验：Phase 12 向用户提交 final approval packet；只有用户明确批准后，才在本地受控发布 V2 candidates/Recipes/router。任何 commit、push、PR、merge、deploy 或 provider mutation 仍需独立的当次授权。

## 执行指示

- 每阶段开始前先创建并校验 `phase-plan.md`；存在真实不确定项时暂停询问，无不确定项则直接实施。
- 每轮结束将“假设 → 改动 → 结果 → 下一实验”追加到本文件，并更新假设账本。
- 只按本合同停止条件终止；局部 Gate 完成不得冒充整体目标完成。
