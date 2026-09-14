# ship 来源能力档案

## Problem

在软件交付生命周期中，将功能分支推送到远程仓库并建立 PR/MR 往往存在多重隐患：开发者在主干分支直接发版破坏基线；未在与最新远端主分支合并后的状态下执行测试导致合流后 CI 爆红；版本号与变更日志更新随意且易发生并发冲突；巨石型单次提交（Monolithic commit）严重破坏 `git bisect` 根因定位能力；开发者依赖陈旧过期的测试记忆直接推送，缺乏确定性的新鲜验证凭证；敏感密钥与 Token 极易随提交推送泄露。传统流程依赖零散的人工作业，缺乏全生命周期自动化、原子化提交拆分与强制性合规门禁。

## When to Use

- **功能分支交付与自动化 PR/MR 构建**：在完成功能开发与验证后，自动化执行基线对齐、测试运行、覆盖率审计、计划核对、版本自增、CHANGELOG 记录、提交原子拆分、脱敏扫描与 PR 创建。
- **差异测试覆盖率与计划完成度严审**：在合流前派发子代理审查改动代码行的测试覆盖深度，核对原始开发计划是否存在未完成项或无授权范围漂移。
- **可二分原子提交规范化重构**：将功能分支上的大差异按基础设施、核心逻辑、展示层与元数据分层拆解为多个独立可编译验证的原子 commit。
- **Apple 原生生态自动化分发**：当检测到 `.xcodeproj` 或 `.xcworkspace` 时，自动走 Store / TestFlight 独立打包发布链路。

## When Not to Use

- **主干基线分支（main / master）直接交付**：绝对禁止在默认基线分支上直接运行 ship。
- **编码与单测编写初期**：代码尚未具备基本完整性时应使用 dev-loop 编码循环或 TDD 技能。

## Role

发布工程与交付编排专家（Release Orchestrator & Delivery Pipeline Driver）。负责主导从功能分支收尾、基线合并、深度测试与对抗审查、原子提交拆分、敏感凭证拦截到最终 PR/MR 创建的全自动流水线。

## Inputs

- **Git 分支上下文**：当前特性分支、远端基线分支（如 `origin/main`）。
- **待交付代码差异**：本地未提交修改或已提交的历史提交集。
- **项目元数据**：`VERSION` 文件、`CHANGELOG.md`、`CLAUDE.md` 或项目配置文件。
- **外部环境凭证**：GitHub CLI (`gh`) 或 GitLab CLI (`glab`) 的认证态。

## Outputs

- **已对齐基线的原子提交序列**：分层构建且均能独立通过测试的线性 Git commit。
- **更新后的版本与发布文档**：自增后的 `VERSION` 文件与格式严格匹配的 `CHANGELOG.md`。
- **合规 PR/MR**：遵循 `v<NEW_VERSION> <type>: <summary>` 命名规范，包含测试证据、覆盖率与任务跟踪的完整 PR。
- **交付元数据度量**：记录覆盖率、计划完成率及交付耗时的持久化分析条目。

## Workflow

1. **Step 1: 分支与环境预检 (Pre-flight Gate)**：
   - 检验是否处于基线分支，若在 main/master 立即阻断；检查 CLI 鉴权状态。
2. **Step 2 & 3: 基线分支拉取与合并 (Fetch & Merge Base)**：
   - 从远端拉取最新基线分支并执行静默合并（`git merge origin/<base>`），保证测试在最新的合并态下运行。
3. **Step 4, 5, 6: 测试套件与评测套件执行 (Test Bootstrap & Run)**：
   - 自动探测并运行项目测试套件（Unit/Integration/E2E），若提示词文件有变动则运行 Eval 评测集，记录执行日志与时间戳。
4. **Step 7 & 8: 覆盖率与计划完成度审计 (Coverage & Plan Audits)**：
   - 派发子代理审查差异覆盖率（`test-coverage.md`），核对计划清单与验证证据（`plan-completion.md`）。
5. **Step 9, 10, 11: 对抗审查与专家军团 (Review Army & Adversarial)**：
   - 针对大型变更调用对抗式审查（`adversarial.md`），分析边界盲区并沉淀经验；处理已有 PR 的 Greptile 评审。
6. **Step 12 & 13: 语义版本自增与 CHANGELOG 写入 (Version Bump & Changelog)**：
   - 推导版本层级（Micro/Patch/Minor/Major），原子更新 `VERSION` 与 `CHANGELOG.md` 并提交。
7. **Step 14 & 15: 待办归档与原子提交拆分 (Todo Archival & Bisectable Splitting)**：
   - 归档待办事项；将差异拆解为基础设施、模型与服务、控制器与视图三层原子提交。
8. **Step 16: 新鲜验证凭据终验门禁 (Fresh Verification Evidence Gate)**：
   - 机械核验 Step 5 之后是否有非放行代码变动；若有变动必须重新跑测并捕获新鲜日志，杜绝口头断言。
9. **Step 17, 18, 19: 凭证防护、文档同步与 PR 创建 (Push & PR Creation)**：
   - 运行预推送脱敏钩子（拦截私钥与 Token），推送特性分支，派发文档同步子代理后创建带有规范版本前缀的 PR/MR。
10. **Step 20: 交付指标持久化 (Persist Metrics)**：
    - 记录交付耗时与质量指标供后续复盘。

## Branches

- **Apple 独立发布分支 (Apple Release Branch)**：检测到 Xcode 平台时，在预检后直接分流至 `apple-release.md`，执行独立证书签名与 TestFlight 分发。
- **冲突中断分支 (Merge Conflict Branch)**：基线合并产生复杂代码冲突时安全挂起，展示冲突文件由人工裁决。
- **版本降级离线分支 (Offline Version Branch)**：网络离线时降级为本地计算版本并打印警告。
- **连续检查点压缩分支 (Checkpoint Squash Branch)**：启用检查点模式时，通过 rebase 优雅压缩中间态提交。

## Rules

- **非交互自动化铁律**：默认保持自主推进，仅在基线分支误触、测试失败、复杂冲突或大版本确认时中断停机。
- **可二分原子提交原则**：禁止将多模块改动揉杂为单个巨石提交，提交历史必须支持 `git bisect` 自动化追溯。
- **PR 标题版本前缀不变式**：PR/MR 标题必须以 `v<NEW_VERSION>` 开头，保持与发布版本严格对应。
- **测试合并态原则**：必须在合并了远端基线之后执行测试，严禁在脱离基线的孤立分支上声称测试通过。

## Exceptions

- **仅文档与注释改动**：可豁免重型测试覆盖率审计与全量评测，走轻量化交付通道。
- **受保护分支无法直接推送**：在异常恢复中转换为 PR 流程处理。

## Dependencies

- **Git & GitHub CLI (`gh`) / GitLab CLI (`glab`)**：核心分支操作与 PR 生命周期管理。
- **运行时环境**：Bun / Node.js、jq 以及项目专用构建工具。
- **可选移动端工具链**：Xcode CLI。

## Permissions and Side Effects

- **权限要求**：Git 本地提交与远端推送权限、创建与更新 PR/MR 权限、本地测试与构建执行权限。
- **副作用**：向本地仓库创建多个提交、向远端仓库推送新分支、在 GitHub/GitLab 创建或更新 PR、修改版本与日志文件。

## Gates

- **Gate 1: Branch Gate**：严禁在 main/master 分支上发起交付流程。
- **Gate 2: Fresh Evidence Gate**：提交前必须具备绝对新鲜的测试通过日志，代码变动后立即失效必须重跑。
- **Gate 3: Adversarial Review Gate**：大型改动必须完成对抗式审查并未发现严重盲区。
- **Gate 4: Pre-push Credential Guard**：拦截 API Key、私钥与访问令牌，禁止敏感数据外溢。
- **Gate 5: PR Title & Doc-Sync Gate**：PR 必须带有自增版本前缀并先行派发文档同步。

## Open Questions

- 在多仓库（Polyrepo）分布式架构下，如何协调跨仓库间的原子 PR 创建与依赖版本锁同步？
- 如何在缺乏完整本地测试环境的边缘设备上安全模拟端到端验证门禁？

## Unique Value

将零碎繁重且极易出错的发布操作（版本、CHANGELOG、原子提交拆分、新鲜测试验证、防泄漏扫描与 PR 组装）高度封装为单一机械化确定性状态机，彻底消除了“带伤推送”、“凭空断言测试”与“生产主干合流冲突”等质量顽疾。

## Reading Coverage

本档案已 100% 覆盖以下主干及扩展规范文件：
- `skills/ship/SKILL.md` (核心编排骨架与状态机)
- `skills/ship/sections/manifest.json` (章节清单索引)
- `skills/ship/sections/apple-release.md` / `.tmpl` (Apple 平台分发适配器)
- `skills/ship/sections/tests.md` / `.tmpl` (测试与评测套件执行)
- `skills/ship/sections/test-coverage.md` / `.tmpl` (差异覆盖率审计)
- `skills/ship/sections/plan-completion.md` / `.tmpl` (计划完成度与漂移核查)
- `skills/ship/sections/review-army.md` / `.tmpl` (预发布多专家军团审查)
- `skills/ship/sections/greptile.md` / `.tmpl` (代码审查意见处理)
- `skills/ship/sections/adversarial.md` / `.tmpl` (对抗式盲区审查)
- `skills/ship/sections/changelog.md` / `.tmpl` (变更日志生成与格式化)
- `skills/ship/sections/pr-body.md` / `.tmpl` (PR 组装与文档同步)
