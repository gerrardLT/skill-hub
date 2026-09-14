# metrics-review 来源能力档案

## Problem

在产品研发与运营生命周期中，团队常常陷入两类极端：要么“数据盲目”，仅凭直觉和主观假设推演业务决策；要么“数据过载”，在堆砌了数十甚至上百个指标的混乱大盘中迷失重点，沉溺于持续增长却缺乏业务实质的“虚荣指标”（如累计注册数、PV总和）。此外，常规指标审查往往沦为数字复读（“指标环比下降了 5%”），缺乏业务归因、多层级健康诊断（北极星 -> L1 -> L2）、分群下钻以及直接指导工程/产品动作的敏捷治理闭环。

## When to Use

- **周期性例行指标复盘会议**：周度健康巡检（15-30分钟）、月度深度趋势审查（30-60分钟）、季度商业复盘（QBR，60-90分钟与 OKR 评分复盘）。
- **指标异常与异动排查**：关键转化率骤跌、DAU/WAU 异常波动、线上事故或功能发布后的业务指标冲击评估。
- **目标达成度度量与计分卡生成**：对照业务 OKR 与季度 Target，生成红黄绿（On track / At risk / Miss）可视化计分卡。
- **数据驱动的改进假设生成**：根据下钻诊断（L2）与留存/激活流失点，驱动下一轮 A/B 测试、功能优化或架构投资提案。

## When Not to Use

- **纯技术系统与基础设施可观测性监控**：服务器 CPU、内存使用率、Pod 崩溃率或数据库慢查询审查（应使用专有 APM/运维可观测性工具）。
- **无明确业务周期或零基线新功能上线首小时**：此时应使用发布后冒烟、金丝雀探针或客户端错误监控，而非宏观产品指标复盘。

## Role

产品指标分析与敏捷治理专家（Product Metrics Review & Actionable Insights Lead）。擅长构建“北极星指标 - L1核心生命周期指标 - L2诊断指标”的分层结构，穿透表象波动，实施分群归因与周期对比，并将原始统计数据转化为直接驱动研发动作与实验假设的决策计分卡。

## Inputs

- **时间跨度与分析窗口**：上周（Weekly）、上月（Monthly）、上季度（Quarterly）或指定日期区间。
- **对比基准数据**：上一周期数据（MoM/WoW）、去年同期数据（YoY）、既定目标值（Target）及行业基准。
- **数据源与统计表单**：连通的分析平台数据源，或用户提供的表格、截图、指标日志。
- **业务上下文与大事件背景**：新版本发布（Launches）、线上事故（Outages）、营销活动（Marketing Campaigns）、节假日与季节性效应（Seasonality）。

## Outputs

- **核心执行摘要（Executive Summary）**：2-3句话浓缩整体产品健康度、核心异动与首要警示。
- **指标计分卡（Metric Scorecard）**：包含 Metric、Current、Previous、Change、Target、Status（On track / At risk / Miss）的紧凑表格。
- **深度趋势与归因分析（Trend & Attribution Analysis）**：显著异动说明、多指标相关性与归因假设（非断言因果）、分群下钻。
- **亮点与隐患清单（Bright Spots & Areas of Concern）**：表现超预期亮点与早期风险预警。
- **敏捷行动建议（Recommended Actions）**：待排查清单（Investigations）、待启动实验（Experiments）、重点投入方向（Investments）与监控告警（Alerts）。
- **背景与数据局限（Context & Caveats）**：已知数据质量问题与口径偏差说明。

## Workflow

1. **收集指标与业务基线（Gather Metrics Data）**：
   - 从数据源或用户输入获取目标时段指标、环比/同比基准与既定 Target；
   - 收集同期的版本发布、营销推广或系统事故等业务事件上下文。
2. **构建指标层级框架（Organize Hierarchy）**：
   - 确立顶层北极星指标（North Star Metric，如活跃协作团队数、每周核心工作流完成次数）；
   - 梳理 L1 六大核心生命周期健康指标：获取（Acquisition）、激活（Activation）、活跃度（Engagement）、留存（Retention）、商业化（Monetization）、满意度（Satisfaction）；
   - 挂载 L2 诊断级下钻指标（步骤漏斗、功能渗透、分群留存、页面性能）。
3. **趋势对比与分群归因（Analyze Trends & Attribution）**：
   - 评估变化速率（加速/减速）与突发异常（Spikes/Drops）；
   - 进行分群交叉分析，验证大盘平稳是否掩盖了某细分群体的大幅萎缩；
   - 识别先行指标（Leading Indicators）与滞后指标（Lagging Indicators）联动关系。
4. **生成审查报告与计分卡（Generate Review & Scorecard）**：
   - 输出结构化 30 秒通读摘要、Markdown 表格式计分卡；
   - 明确标注亮眼表现与风险敞口。
5. **输出动作提案与闭环跟进（Translate into Actions）**：
   - 将问题转化为明确的四类后续动作：排查调研、A/B 实验假设、产品投入、阈值告警；
   - 提议建立持续监控大盘或更新复盘模板。

## Branches

- **周度指标巡检分支（Weekly Check）**：15-30 分钟敏捷复盘，重点关注北极星指标异动、活跃实验统计显著性与异常报警。
- **月度深度复盘分支（Monthly Review）**：30-60 分钟深度复盘，包含完整 L1 计分卡、新老人群队列留存曲线与功能采纳度下钻。
- **季度业务评估分支（Quarterly Business Review - QBR）**：60-90 分钟战略评估，涵盖季度 OKR 达成打分、年同比分析及下一季度目标校准。

## Rules

- **上下文对比铁律**：严禁罗列孤立的绝对数值，必须附带环比、同比、目标值或基准线的对照。
- **相关不等于因果原则**：指标异动归因分析必须明确指出不确定性与混杂因素，避免轻率将关联性断定为因果关系。
- **动作导向原则**：指标审查如果不能产生至少一项明确的产品决策或工程行动，则该审查无效。
- **虚荣指标剔除原则**：禁止将累计总量等单调递增的指标作为核心健康度凭据，优先采纳比率、留存率、频次与队列曲线。
- **分群下钻原则**：在整体指标持平或轻微波动时，必须下钻检查主力客群与长尾客群的结构性分化。

## Exceptions

- **偶发性外部干扰**：因自然灾害、全国性节假日、机房大规模宕机导致的瞬时数据跌落，应在 Context & Caveats 明确剔除对比，不归结为产品体验问题。
- **指标口径变更**：若当期发生埋点重构或口径口径调整，必须做口径对齐换算或明确断代标识。

## Dependencies

- **数据源依赖**：分析平台（Product Analytics Connector）或用户输入的结构化业务数据。
- **协作方依赖**：产品经理、数据分析师与核心工程负责人。

## Permissions and Side Effects

- **权限要求**：数据报表与分析工具读取权限，文档落盘权限。
- **副作用**：无直接破坏性副作用；输出结论将引导后续研发优先级与实验资源分配。

## Gates

- **Gate 1: Metric Hierarchy Alignment Gate**：在深入分析前必须对齐北极星指标与 L1 指标定义，缺失时先协助定义层级。
- **Gate 2: Comparison Baseline Completeness Gate**：计分卡中的核心指标必须具备 Previous 或 Target 基线，缺少基线不得评定 Status。
- **Gate 3: Actionability Sign-off Gate**：产出的审查报告必须包含可执行的 Recommended Actions，杜绝纯叙述性文本。

## Open Questions

- 当宏观市场环境快速下行导致整体获客成本激增时，如何动态调节 L1 目标以平衡团队信心与商业诉求？
- AI Agent 驱动的高频自动化操作如何与传统真实人类的 DAU/MAU 活跃定义进行精准区隔？

## Unique Value

建立了从“数据收集 -> 指标层级梳理 -> 分群归因 -> 计分卡呈现 -> 行动与实验转化”的标准闭环，将混沌的数据噪音提炼为直接支撑敏捷开发与迭代决策的高信噪比资产。

## Reading Coverage

- `skills/metrics-review/SKILL.md`: 完整覆盖工作流、指标层级框架、常用指标定义、OKR 目标设定、审查频次模式与大盘反模式。
