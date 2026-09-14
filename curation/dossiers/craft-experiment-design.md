# craft-experiment-design 来源能力档案

## Problem

在现代敏捷研发与产品迭代中，团队推行 A/B 测试或在线实验时常常陷入无序与随意：要么缺少明确、可证伪的假设陈述（Falsifiable Hypothesis），将试错退化为盲目碰运气；要么缺乏清晰的指标分层，仅盯着单一转化率却无视对系统时延、报错率或长期留存等护栏指标（Guardrail Metrics）的严重侵蚀；要么忽视流量分流偏倚、反向保留对照组（Holdout Strategy）策略以及实验运行周期的统计效力考量，导致实验结果充斥噪音与假阳性。

## When to Use

- **新功能或交互改版上线前的 A/B 测试方案设计**：将“我们应该测一下这个想法”转化为数据科学与工程团队可审阅执行的完整实验计划。
- **构建可证伪实验假设**：采用“如果我们实施 [变更]，那么将产生 [预期结果]，因为 [底层逻辑与用户心理]”的黄金公式严密定义实验意图。
- **全景实验指标体系构建**：明确界定单一定胜负的一级核心指标（Primary Metric）、辅助观察的二级指标（Secondary Metrics）与绝对不可劣化的护栏红线指标（Guardrail Metrics）。
- **受众分配与长期保留组（Holdout）策略规划**：制定实验人群过滤条件、流量切分比例（如 50/50 或梯度放量）以及长期影响度量的 Holdout 策略。

## When Not to Use

- **纯定性探索或早期概念验证**：在尚无充足用户基数与流量统计效力（Sample Size）的种子期，应优先采用用户深度访谈或原型可用性测试。
- **确定性合规与严重故障修复**：针对安全漏洞修补、合规硬性要求或崩溃修复，不应进行对照灰度实验，应全量迅速上线。

## Role

在线实验设计与因果推断规划专家（A/B Testing & Experimentation Design Specialist）。擅长从模糊的产品优化诉求中提炼出具备严密逻辑因果链的可证伪假设，构建涵盖核心指标与防御性护栏的度量体系，并科学估算实验时长与样本分配。

## Inputs

- **待测功能与变更描述（Change Context）**：UI/交互调整、算法推荐改动、文案替换或工作流重构细节。
- **业务诉求与变革理由（Why & Rationale）**：预期解决的用户痛点、业务驱动力或历史测试结论。
- **先验数据背景（Prior Context）**：历史转化率基线、日均活跃用户流量、最小可检测效应（MDE）期望。
- **受众与环境限制（Audience Constraints）**：目标人群范围（新注册用户、特定平台或特定国家）、工程技术依赖与潜在风险。

## Outputs

- **结构化实验设计规格书（Experiment Design Plan）**：
  1. **可证伪假设（Hypothesis Statement）**：标准化 If-Then-Because 三段式表述；
  2. **一级核心指标（Primary Metric）**：裁决实验胜败的唯一定量指标；
  3. **二级观测指标（Secondary Metrics）**：2-3 个辅助观察指标，监测用户全链路衍生行为；
  4. **护栏守底指标（Guardrail Metrics）**：性能时延、错误率、反弹率、长期留存等不得恶化的保护指标；
  5. **受众与分配策略（Audience & Allocation Strategy）**：入组受众定义、分流百分比与放量阶梯；
  6. **长期保留组策略（Holdout Strategy）**：全量推开后保留未受影响对照组以度量长期累积因果效应的方案与理由；
  7. **实验周期估算（Duration Estimate）**：基于统计效能、流量周期性（包含完整自然周）的运行天数估算；
  8. **风险与偏误防范（Risks & Considerations）**：新奇效应（Novelty Effect）、时效偏误、网络溢出效应等预案。

## Workflow

1. **澄清变更意图与业务背景（Clarify Change & Context）**：
   - 提取待测改动细节，若用户输入为空则主动触发提示引导补充变更动机与现状数据。
2. **形式化构造可证伪假设（Formulate Falsifiable Hypothesis）**：
   - 采用标准三段式模板强力绑定“变更操作”、“可度量结果”与“因果合理解释”，杜绝含混表述。
3. **分层定义实验度量体系（Establish Metric Hierarchy）**：
   - 选定唯一定胜负的 Primary Metric（杜绝多个核心指标导致多重假设检验陷阱）；
   - 选定 2-3 个紧密关联的 Secondary Metrics；
   - 选定与业务基本盘和系统可用性强相关的 Guardrail Metrics。
4. **规划人群受众与流量分流（Plan Audience & Allocation）**：
   - 确定样本切分粒度（如 User ID、Device ID 或 Org ID 哈希）；
   - 设定分配比例与逐步放量梯度。
5. **设计保留组与时长评估（Holdout & Duration Planning）**：
   - 评估功能是否有必要保留 1%-5% 的全局长期 Holdout 群体；
   - 结合周周期性（Day-of-week Effect）确保实验至少覆盖 1-2 个完整业务周。
6. **审查实验风险与防错前置（Review Risks & Assumptions）**：
   - 标明需要与数据科学家或后端工程核验的前提假设与潜在干扰。

## Branches

- **高风险激进变动分支（High-Risk Ramp Branch）**：对涉及核心变现或重要工作流的变更，采用 5% -> 20% -> 50% 的阶梯式渐进放量，密切监听护栏指标。
- **长期因果度量分支（Long-Term Holdout Branch）**：针对可能存在疲劳效应或长期隐性流失的特性，强制保留微小比例（如 2%）的长期未受影响组并持续跟踪 3-6 个月。

## Rules

- **单一核心决策指标铁律（Single Primary Metric Invariant）**：每次实验只允许定义 1 个 Primary Metric 作为统计检验的裁决标准，严禁使用多个等权核心指标制造假阳性。
- **标准三段式假设铁律（If-Then-Because Hypothesis Invariant）**：假设陈述必须严格遵循“If we [change], then [outcome], because [rationale]”的可证伪格式。
- **护栏不可妥协原则（Non-Negotiable Guardrails）**：实验即便显著提升了 Primary Metric，只要突破了任一 Guardrail Metric 阈值，一律不得判定为成功上线。
- **完整自然周覆盖原则（Full Business Cycle Coverage）**：实验运行时长必须以完整自然周（7天、14天）为最小单位，杜绝跨半周即停止导致周内周期性偏差。

## Exceptions

- **大流量微改动（Extreme Traffic Micro-Test）**：对于拥有千万级 DAU 且改动极微小（如按钮颜色/微小文案）的实验，可在极短时长（24-48小时）内收集足额统计样本，此时可在排除日间效应后缩短周期。
- **紧急故障逃生**：实验运行中若 Guardrail 指标发生灾难性劣化（如崩溃率上升 50%），应立即触发紧急熔断终止实验。

## Dependencies

- **实验平台基础设施**：分流服务（Feature Flag / Experiment Engine，如 LaunchDarkly、Statsig）、埋点事件采集。
- **统计工具支持**：样本量计算器（Power Analysis Calculator）、显著性检验套件。

## Permissions and Side Effects

- **权限要求**：实验分流平台配置权限、分析平台数据访问权限。
- **副作用**：分流对照可能使部分用户在测试期体验到不成熟或劣化的变体。

## Gates

- **Gate 1: Hypothesis Falsifiability Gate**：实验设计方案必须具备明确的 If-Then-Because 结构且预期结果可量化测量。
- **Gate 2: Guardrail Metrics Specification Gate**：实验方案中必须明确包含至少 1 项不可劣化的系统或体验护栏指标。
- **Gate 3: Cross-Functional Alignment Gate**：在正式向流量平台注入配置前，方案必须由产品、工程与数据分析三方审签。

## Open Questions

- 当两个独立团队在同一核心页面各自运行 A/B 测试时，如何从架构上检测并消除交叉实验的交互干扰（Interaction Effects）？
- 对于高度个性化的 AI 动态生成内容，如何界定对照组与实验组在输入随机性下的因果基线？

## Unique Value

将零散模糊的试错冲动标准化为严谨、可审计、满足因果推断要求的工程化实验方案，通过明确的指标三层防护与完整周期约束，保障产品迭代基于真实价值而非统计假象。

## Reading Coverage

- `skills/craft-experiment-design/SKILL.md`: 涵盖提示模板、实验设计八大要素（Hypothesis, Primary Metric, Secondary Metrics, Guardrail Metrics, Audience & Allocation, Holdout Strategy, Duration Estimate, Risks & Considerations）及最佳实践建议。
