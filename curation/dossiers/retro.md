# retro 来源能力档案

## Problem

在软件工程团队的快速迭代与敏捷交付中，团队往往忙于追逐下一个功能点，导致复盘机制流于表面或彻底缺位：
1. **主观感觉代替数据凭证**：复盘仅凭模糊印象（“这周大家挺辛苦/提交不少”），缺乏基于真实 Git 提交历史、代码质量指标（测试行比率、代码热点重复修改率）与工作会话时序规律的精确度量；
2. **缺乏时序趋势与历史对照**：单次复盘成为孤立碎片，无法对照上期数据（WoW 趋势）衡量代码库健康度或工程效能是提升还是退化；
3. **团队与个人视角割裂**：传统的机械统计要么千人一面忽略个人闪光点与阻碍，要么过度个人化引发不良考评焦虑，缺乏兼具团队总览与个人定制化成长反馈（Praise & Growth Areas）的平衡框架。

## When to Use

- **周期性周度/双周/月度工程复盘**：在每周五下午或冲刺（Sprint）结项时运行，全面复盘近期交付成果与工程质量。
- **阶段性交付物全景盘点（What did we ship）**：向技术领导层或跨职能团队通报最近 24 小时、7 天、14 天或 30 天上线的具体成果。
- **跨周期工程效能趋势对比（Retro Compare）**：对比当前周期与上一同等长度周期在提交类型分布、PR 规模、测试占比及热点文件抖动上的趋势迁移。
- **跨项目全局 AI 辅助产出复盘（Retro Global）**：在多项目工作空间中汇总多端代码贡献与上下文资产沉淀。

## When Not to Use

- **微观单次代码审查（Code Review）**：若目标是审查具体某一次 PR 的语法、架构或安全隐患，应使用 `code-review` 或审查专门技能，而非宏观工程复盘。
- **线上突发事故止血与根因复盘（Incident Response）**：突发生产事故需立即止血并依照 P0/P1 流程执行事故现场排查与事后复盘，应使用 `incident-response`。
- **实时任务进度跟踪（Daily Standup / Task Tracking）**：不适用于分钟级的日常任务跟进或简单的工单状态查询。

## Role

工程效能洞察与持续演进复盘专家（Engineering Retrospective & Work Pattern Analyst）。专职基于底层 Git 提交图、代码时空分布规律与质量指标生成客观、严谨、面向资深工程师/CTO 视角的复盘深度报告，挖掘隐性瓶颈并沉淀可复用的工程习惯。

## Inputs

- **时间窗口参数（Time Window）**：默认 7 天（7d），支持 24h、14d、30d、`compare`（与上期对比）及 `global`（跨项目）。
- **Git 仓库上下文**：基础分支（Base Branch）、远程远端拉取状态、本地提交历史、变更统计（Diffstat）。
- **历史复盘与沉淀资产**：`.context/retros/*.json` 历史快照、`~/.gstack/projects/{slug}/timeline.jsonl` 时间线日志、`learnings.jsonl` 既往经验。
- **个人身份识别元数据**：当前执行者身份（标记为 "you"），以区隔自身贡献与团队伙伴协同。

## Outputs

- **一句话社交级摘要（Tweetable Summary）**：紧凑提炼提交数、贡献者人数、新增/修改代码行数（LOC）、测试行占比、PR 数量、峰值活跃时段及连续提交打卡天数（Streak）。
- **多维结构化复盘通报（Engineering Retro Report）**：
  - **核心摘要表（Summary Table）**；
  - **环比趋势分析（Trends vs Last Retro）**；
  - **工时与会话时空规律（Time & Session Patterns）**：高效时段、协同节奏；
  - **交付速度与提交结构（Shipping Velocity）**：提交类型配比（feat/fix/chore）、PR 粒度分布、故障修复链（Fix-chain）检测；
  - **代码与测试健康（Code Quality & Test Health）**：测试行比率、热点文件频度（Hotspots）、测试套件净增量；
  - **计划达成度度量（Plan Completion）**：关联 `/ship` 交付计划的实际完成百分比；
  - **焦点与周度最佳交付（Focus & Ship of the Week）**；
  - **个人专属深度画像（Your Week）**：个人代码贡献、亮点称赞与潜在成长建议；
  - **团队贡献者矩阵与改进建议（Team Breakdown & Recommendations）**。
- **历史持久化快照**：落盘至 `.context/retros/{date}.json`，供下期对比复用。

## Workflow

1. **环境嗅探与基线分支对齐（Detect Platform & Base Branch）**：
   - 嗅探代码托管平台（GitHub / GitLab / 原生 Git），确定权威目标分支（main / master）。
2. **时区归一与自然日窗口对齐（Align Midnight Window）**：
   - 采用本地系统默认时区；
   - 针对日（d）与周（w）时间窗口强制采用零点对齐格式（`T00:00:00`），避免以当前运行秒数切片导致采样失真。
3. **远端新鲜度拉取与陈旧门禁（Fetch & Freshness Guard）**：
   - 执行 `git fetch origin <base>` 刷新远端基线；
   - 校验最新提交日期是否落于窗口内，杜绝基线严重落后导致无产出假象。
4. **指标批量聚合计算（Gather Metrics Pipeline）**：
   - 调用指标引擎或执行 Git 聚合脚本，一次性产出提交总量、作者明细、类型分布、测试 LOC 比率、热点文件及连续打卡天数。
5. **历史资产加载与环比对照（Load Prior Retros & Compare）**：
   - 读取最近 1-5 期 `.context/retros/*.json`；
   - 对比测试行比例升降、提交频率变化及历史经验应用状态（Prior learning applied）。
6. **叙事报告生成与持久化落盘（Generate Report & Save Snapshot）**：
   - 依据 `sections/report-format.md` 模板渲染全景复盘文本；
   - 保存结构化指标 JSON 供下周期读取。

## Branches

- **周期环比对比分支（Compare Branch）**：携带 `compare` 参数时，同时计算前序等长时段的基线指标，逐项输出指标差值（Delta）与迁移评估。
- **跨项目全局复盘分支（Global Branch）**：在脱离单一仓库时，跨本地配置的所有工作空间聚合时间线与产出资产。
- **离线降级运行分支（Offline Degraded Branch）**：在无网络或无远程 remote 时，降级为仅针对本地已拉取 ref 计算，并在报告显著位置声明“offline run”。

## Rules

- **自然日午夜绝对对齐铁律（Midnight-Aligned Invariant）**：天与周粒度的 `--since` 必须显式携带 `T00:00:00` 零点后缀，严禁使用相对模糊时间造成早晚时段统计偏差。
- **陈旧基线阻断铁律（Stale Base Guard）**：若拉取成功但分析分支上的最新 commit 早于 `today - window`，必须直接阻断并提示刷新，防止编造空洞叙事。
- **事实与推论分离原则（No Hallucinated Scores）**：聚焦真实 Git 数据与事实度量，严禁在无证据前提下凭空编造完备性评分或主观臆测。
- **测试比率警戒门禁（Test Ratio Growth Flag）**：当周期测试行数占新增代码总行数比例低于 20% 时，必须强制将其标记为团队核心成长与隐患区。

## Exceptions

- **本地单机无 Remote 仓库**：当检测到 `GUARD_REMOTE: none` 或无远端权限时，放行 fetch 失败门禁，但必须在报告正文首段明确披露“未执行远端新鲜度对齐”。
- **初始化新仓库首周**：首期复盘无历史对比基线时，自动隐藏“Trends vs Last Retro”小节。

## Dependencies

- **基础环境依赖**：Git CLI（支持 `git log`, `git diff` 等高级统计参数）。
- **可选集成依赖**：`gh` / `glab` CLI，本地项目上下文存储目录 `.context/retros/`。

## Permissions and Side Effects

- **权限要求**：Git 仓库读权限、网络拉取只读权限（`git fetch`）、本地 `.context/retros/` 文件写入权限。
- **副作用**：向本地仓库创建或更新复盘历史 JSON 文件；无任何远程推流或代码破坏性副作用。

## Gates

- **Gate 1: Freshness & Stale Base Gate**：验证最新提交处于统计窗口之内，杜绝空仓库或死分支统计。
- **Gate 2: Zero-Hallucination Metrics Gate**：所有指标数值必须由 Git 真实管道输出推导，严禁口头伪造。
- **Gate 3: Retrospective Snapshot Persistence Gate**：复盘完成必须将结构化数据落盘至 `.context/retros/{date}.json`。

## Open Questions

- 当代码库存在大量由自动化脚手架或 LLM 单次生成的巨石代码（10k+ 行）时，如何合理平滑其对团队真实有效 LOC 产出比的冲击？
- 跨时区跨国分布式团队异步协作时，会话时长算法如何精准剔除静止挂起时间？

## Unique Value

彻底摆脱口头化、形式主义的复盘走过场，以客观的 Git 提交图谱为事实锚点，融合了工程质量、时空规律、任务计划达成与个性化成长引导，将复盘升维为驱动技术团队持续自我进化的工程级引擎。

## Reading Coverage

- `skills/retro/SKILL.md`: 涵盖时间窗口解析（零点对齐）、平台嗅探、新鲜度前置检查（Step 0.5）、数据收集（Step 1）、陈旧基线守卫与降级执行规范。
- `skills/retro/sections/manifest.json`: 章节索引与触发器声明。
- `skills/retro/sections/report-format.md`: 涵盖 Tweetable summary、Summary Table、Trends、Time & Session Patterns、Shipping Velocity、Code Quality Signals、Test Health、Plan Completion、Focus、Your Week 及团队细分报表结构。
