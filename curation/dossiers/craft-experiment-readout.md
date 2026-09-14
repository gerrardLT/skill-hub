# craft-experiment-readout 来源能力档案

## Problem

在 A/B 测试或在线实验完成数据回收后，团队在结果通报与决策阶段常面临多重挑战：数据分析师提供的统计报告充斥着 p 值、置信区间和复杂的统计学黑话，导致非技术利益相关方与管理层无法快速提炼业务洞察；由于对模糊结果（Inconclusive）心存顾虑，团队容易强行宣布胜利（P-hacking 或忽视统计效力）；此外，常规通报往往仅停留在“胜出/失败”表面，缺乏跨受众分群差异下钻、缺乏清晰的“发布 / 迭代 / 放弃”（Ship / Iterate / Kill）决断建议，且未能将单次实验经验沉淀为指导未来产品演进的组织级认知资产。

## When to Use

- **A/B 测试或在线实验周期结束后的收官复盘**：将原始指标变动、样本量、置信区间与运行天数转化为全团队可直接行动的结构化通报。
- **实验获胜方裁决与发布决断**：明确给出确定的胜出变体裁决，或在统计结果模糊时诚实声明“无显著差异（Inconclusive）”，并输出明确的 Ship、Iterate 或 Kill 决策。
- **受众差异化分群洞察分析**：下钻分析效应在不同受众群体间的异质性表现（如新老用户、付费/免费方案、iOS/Android/Web 平台）。
- **面向利益相关方的分级通告草拟**：根据受众受众类型（高管、研发团队、跨职能业务方、全员）定制通俗通报，包含 1-2 句高信噪比 TL;DR 与明确动作负责人。

## When Not to Use

- **实验前期的假设与指标规划**：尚未上线运行的测试方案构思阶段（应使用 `craft-experiment-design`）。
- **实验运行中的实时流量分流与报警**：实验进行中的线上监控与异常熔断（应使用 Feature Flag / APM 探针）。

## Role

在线实验复盘与业务决策叙事专家（Experiment Readout & Decision Narrative Lead）。擅长将复杂的数理统计数据转化为通俗、清晰、具有高决策指导价值的结构化通报，恪守客观诚实原则，平衡统计显著性与实际业务价值（Practical Significance），并推动跨职能落地执行。

## Inputs

- **实验元数据与初始设定**：实验名称、初始假设、一级裁决指标、护栏指标、运行周期与目标受众。
- **原始实验数据与统计结果**：各变体（Control vs Variant(s)）样本量、转化率/均值、相对提升百分比（Lift）、p 值、95% 置信区间。
- **分群维度下钻数据**：新老用户、客户端平台、套餐等级等细分指标表现。
- **目标通报受众（Audience Profile）**：高管层（Leadership）、核心研发团队（Engineering）、跨职能业务伙伴（Cross-Functional Partners）或公司全员。

## Outputs

- **结构化实验复盘报告（Experiment Readout）**：
  1. **执行摘要（Summary）**：一段话提炼测试内容、核心结果与最终建议；
  2. **假设回溯（Hypothesis Recap）**：重申初始预期与理论依据；
  3. **核心结果表（Results）**：指标对比，明确区分统计显著性与实际业务显著性；
  4. **胜出裁决（Winner Declaration）**：明确判定胜出者或诚实标注为 inconclusive；
  5. **分群表现分析（Segment Analysis）**：跨人群效应异质性洞察；
  6. **三元决断建议（Recommendation）**：Ship（全量推开）、Iterate（调整重测）或 Kill（彻底下线）及后续动作；
  7. **组织经验沉淀（Learnings）**：超越单次特性的长远产品启示。
- **利益相关方定制通报（Stakeholder Comms Draft）**：
  - **超短核心结论（TL;DR）**：1-2 句话捕获核心要点；
  - **业务影响（Impact）**：对受众业务与底线指标的直接意义；
  - **下一步行动清单（Next Steps）**：明确行动项、责任人与时间表。

## Workflow

1. **收集实验数据与受众画像（Gather Results & Identify Audience）**：
   - 获取实验结果明细，若为空则引导用户补充变体指标、样本量、置信区间与运行周期；
   - 明确通报的核心受众（高管侧重业务底线，研发侧重稳定性与架构）。
2. **假设回溯与基线对比（Recap Hypothesis & Baseline）**：
   - 对齐初始假设，对比实际走势与预期的吻合程度。
3. **统计与实际显著性裁决（Evaluate Statistical & Practical Significance）**：
   - 评估 p 值与置信区间，确认是否达到统计显著；
   - 评估提升幅度是否具有实际商业价值（排除极微弱但显著的“无感提升”）；
   - 检查护栏指标是否完好。
4. **诚实定性胜负（Declare Winner or Ambiguity）**：
   - 明确标注胜出变体；若数据未达显著或结果互有冲突，坚决声明 inconclusive，严禁强行定胜。
5. **分群下钻与长远经验萃取（Segment Drill-down & Extract Learnings）**：
   - 排查局部受众的偏好分化；提炼对后续产品路线图有价值的深层认知。
6. **裁决建议与通告生成（Formulate Recommendation & Draft Comms）**：
   - 给出 Ship / Iterate / Kill 裁决；
   - 生成带 TL;DR、业务影响与 Next Steps 的自洽通报文本。

## Branches

- **全量发布分支（Ship Branch）**：指标在核心与护栏上均达标胜出，规划 100% 放量时间表与代码清理任务。
- **调整重测分支（Iterate Branch）**：方向具有潜力但关键细节受阻（如特定分群流失严重），提炼调整假设并规划下一轮实验。
- **彻底下线分支（Kill Branch）**：核心指标劣化或护栏突破，果断彻底撤回代码，将失败教训记录入知识库。
- **模糊结果分支（Inconclusive Branch）**：差异在零轴附近徘徊，分析样本效力不足或机制无效原因，客观向高管陈述不确定性。

## Rules

- **诚实面对模糊铁律（Honesty in Ambiguity Invariant）**：严禁在统计不显著或结果冲突时强行判定获胜方，必须如实声明不确定性并解释原因。
- **双重显著性核验原则（Statistical vs Practical Significance）**：不仅要检查数学上的统计显著性（p < 0.05），更要评估绝对提升是否值得工程维护成本（实际商业显著性）。
- **受众通俗化表达铁律（Plain Language, No Jargon）**：面向跨职能或管理层通报时，严禁滥用专业统计公式与缩写，必须转化为业务能懂的自然语言。
- **明确三元决断原则（Clear Three-Way Recommendation）**：建议必须直接在 Ship、Iterate、Kill 三者中明确站位，严禁给出模棱两可、无法推动执行的软弱结论。

## Exceptions

- **零胜负但具工程降本价值（Cost-Reduction Win）**：实验组业务指标与对照组持平（平手），但实验组架构具备极高的性能优势或成本节省时，依然可判定为 Ship（降本发布）。
- **重大护栏一票否决**：即便 Primary Metric 暴增 30%，若崩溃率或合规护栏严重翻红，一律触发 Kill 流程。

## Dependencies

- **数据依赖**：实验分析平台产出的指标报表、置信区间、分群下钻数据。
- **跨职能协作**：数据科学家审核统计边界、工程团队评估上线与清理成本。

## Permissions and Side Effects

- **权限要求**：数据平台报表读取权限、团队内部通讯工具发送草稿权限。
- **副作用**：通报决断将直接触发工程侧代码合并发布、全量灰度放量或实验代码彻底下线清理。

## Gates

- **Gate 1: Metric Significance & Power Gate**：确认实验已达预定运行时长与样本量要求，避免过早偷窥数据（Peeking）。
- **Gate 2: Guardrail Metric Clearance Gate**：确认所有预设护栏指标均处于安全绿线以内。
- **Gate 3: Actionable TL;DR Gate**：产出的通报材料必须具备可在 30 秒内通读并明确下一步负责人的 TL;DR。

## Open Questions

- 当实验结果出现统计显著但在不同核心客群（新客大涨 vs 老客大跌）间发生两极分化时，如何通过业务权重量化整体得失？
- 如何在多实验并发环境下，科学剥离长期复合收益对单次实验复盘通报的干扰？

## Unique Value

打通了从“实验原始统计报表”到“高管与全员行动决策”的最后一公里，以诚实的胜负判定、敏锐的分群下钻与通俗精准的分级沟通，避免了假阳性浪费工程资源，推动数据转化为可靠的业务推进力。

## Reading Coverage

- `skills/craft-experiment-readout/SKILL.md`: 涵盖提示模板、复盘报告 7 大构成（Summary, Hypothesis Recap, Results, Winner, Segment Analysis, Recommendation, Learnings）及利益相关方通报 3 大要素（TL;DR, Impact, Next Steps）与沟通最佳实践。
