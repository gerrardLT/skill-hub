# prioritization-frameworks Dossier

## Problem

`prioritization-frameworks` 解决的是面对客户问题、initiative、idea、requirement 或个人任务时，团队缺少与对象和决策复杂度匹配的优先排序方法。来源提供 9 个框架的选择摘要，并展开 Opportunity Score、ICE、RICE 的计算方式，目标是避免把所有对象塞进同一种评分表（`skills/prioritization-frameworks/SKILL.md:6`）。

其核心立场是优先排序 customer problems/opportunities，而不是让客户直接设计 solution 或机械排 features（`skills/prioritization-frameworks/SKILL.md:10`）。来源是 reference guide，不是完整的调研、工作坊、roadmap 决策或组合优化 workflow。

## When to Use

- 需要为 customer problems 选择 Opportunity Score。
- 需要快速比较 ideas/initiatives，可使用 ICE。
- 较大团队需要把 reach 与 per-customer impact 分开，可使用 RICE。
- 需要为个人任务、快速二维分诊、风险收益、客户期望、多因素决策或 requirements classification 选择轻量框架。
- 需要比较 RICE 与 ICE，或理解不同框架的用途与边界。

## When Not to Use

- 需要客户直接指定 feature solution；来源明确要求先排序 problems/opportunities。
- 需要从原始研究数据发现客户问题；本来源不提供访谈、survey design 或 qualitative synthesis workflow。
- 需要把 Kano 当成严格优先级排序算法；来源只把它定位为理解 expectations。
- 需要把 Impact vs Effort 当作战略决策的严谨模型；来源只支持 quick triage。
- 需要完整 roadmap、资源排程、依赖求解或 portfolio optimization；本来源没有这些机制。
- 缺少输入数据却要求输出精确、可辩护的排名；不得编造 importance、satisfaction、reach、confidence、ease、effort 或 weights。

## Role

来源没有规定参与角色或责任分工；本来源自身只充当 framework reference，不执行调研、评分会议、模板下载或 roadmap 承诺。以下是为实际采用框架而策展推导的角色 safeguard，不是来源原文：

- PM / decision owner：确认待排序对象、选择框架、定义时间范围和评分口径，并对最终决策负责。
- Customer research owner：为 Opportunity Score 提供 importance 与 satisfaction 数据；来源未定义 survey 设计和样本治理。
- Engineering / delivery：为 ease 或 effort 提供估算，并暴露实现约束。
- Cross-functional stakeholders：在 Weighted Decision Matrix 等多因素决策中对 criteria、weights 与 evidence 对齐。

## Inputs

共同输入是明确的 prioritization object 与 decision context。不同框架还需要不同字段：Opportunity Score 需要归一化到 0–1 的 Importance 和 Satisfaction；ICE 需要 Opportunity Score、受影响客户数、1–10 Confidence 与 1–10 Ease；RICE 需要 Reach、Opportunity Score、0–100% Confidence 与 person-month Effort。

其余框架的摘要输入分别涉及 urgent/important、impact/effort、risk/reward、Kano expectation category、weighted criteria scores 或 Must/Should/Could/Won't 分类。来源没有规定数据采集周期、评分者、缺失值、tie-break 或置信区间处理。

## Outputs

- Opportunity Score：current value、opportunity score、customer value created，以及 Importance × Satisfaction 图上的机会位置。
- ICE：Impact × Confidence × Ease 的排序分数。
- RICE：(Reach × Impact × Confidence) / Effort 的排序分数。
- 其余框架：与其用途相符的二维象限、expectation category、多因素加权结果或 requirement class。

来源没有定义统一的最终 roadmap artifact、批准动作、自动执行副作用或“框架选择记录”。为支持审计，策展建议另行记录待排序对象、所选框架、输入口径、假设和边界；该记录是推导 safeguard，不是来源声明的输出。

## Workflow

来源没有提供端到端 workflow；以下顺序是基于其公式、用途和边界策展推导的 application safeguard，不是来源原文：

1. 明确排序对象是 customer problem、initiative/idea、requirement 还是 personal task。为遵守“优先 problems/opportunities”的核心原则，遇到 solution request 时可先澄清其底层 problem/opportunity。
2. 按对象和决策复杂度选框架：customer problems 优先 Opportunity Score；ideas/initiatives 快排可用 ICE；需要单独建模 Reach 和 Effort 时用 RICE；其他 6 个框架只按摘要用途条件性采用。
3. 为所选框架定义评分范围、时间窗口、population 与证据来源；不得混用 0–1、1–10、0–100% 或 person-month 而不说明。
4. 收集框架要求的输入。Opportunity Score 先取得并归一化 Importance/Satisfaction；ICE/RICE 再补 reach/customer count、confidence 与 ease/effort。
5. 按来源公式计算，并保留原始输入和中间值，避免只留下不可审计的最终 score。
6. 按框架语义解释结果：Opportunity Score 寻找 high-importance/low-satisfaction problems；ICE/RICE 中高分优先；Kano 只帮助理解 expectations；Impact vs Effort 只用于 quick triage。
7. 将 score 作为决策证据而非自动授权；记录数据缺口、估算不确定性和未由本来源覆盖的资源、依赖或战略约束。

## Branches

- 排 customer problems：使用 Opportunity Score，并将 Importance 与 Satisfaction 归一化为 0–1。
- 快速排 ideas/initiatives：使用 ICE；其 Impact 在本来源中定义为 Opportunity Score × affected customers。
- 大团队需要更细粒度：使用 RICE，把 Reach 与 per-customer Impact 分开，并用 Effort 作除数。
- 个人 PM 任务：Eisenhower Matrix。
- 简单快速分诊：Impact vs Effort；战略决策不得仅依赖它。
- 不确定性是核心维度：Risk vs Reward。
- 理解 expectation 类型：Kano；不把 category 直接冒充优先级。
- 多因素且需要 stakeholder buy-in：Weighted Decision Matrix。
- requirements scope classification：MoSCoW，并保留其 project-management origin 警示。

## Rules

- 优先排序 problems/opportunities，不让 customers 直接设计 solutions。
- Opportunity Score、ICE、RICE 必须按来源定义使用各自单位和公式，不能把 Ease 与 Effort 混为同向变量。
- Opportunity Score 的 Importance 与 Satisfaction 需先归一化到 0–1。
- Opportunity Score 高值表示 high importance、low satisfaction 的优先机会；Importance-vs-Satisfaction 图的 upper-left 是来源所述 sweet spot。
- Kano 用于 understanding expectations，不是排序算法。
- Impact vs Effort 是 quick triage，不足以单独支撑 rigorous strategic decisions。
- 外部模板和 Further Reading 只作为链接元数据；本轮未访问，不能声称内容、可用性或版本已核验。

## Exceptions

- 同一个 customer problem 可先用 Opportunity Score 估 per-customer opportunity，再把结果作为 ICE Impact 的组成部分或 RICE Impact；必须保留转换和 population 口径。
- Weighted Decision Matrix 可容纳多个 criteria，但来源没有给出 criteria、weights 或评分标尺，实际采用时必须另行定义。
- MoSCoW 可用于 requirements，但来源特别提示其 project-management origin；不能把类别当价值测量。
- 来源称有 9 个 frameworks，但只有 Opportunity Score、ICE、RICE 获得公式级展开；其他框架不得补造来源未提供的详细步骤。
- 没有数据时可以选择框架并列出所需输入，但不能产生伪精确排名。

## Dependencies

当前来源目录只有 `SKILL.md`，没有本地模板、references、scripts 或 examples。四个 Templates 链接和三个 Further Reading 链接都是 HTTPS 外部资源，本轮未联网读取，也不属于 verifier 的本地 reachable attachments。

来源提及 Dan Olsen、The Lean Product Playbook、Product Compass 和 CPDM 等外部归属；这些仅按原文保留，未核验原始出版物、课程或模板。没有声明其他本地 Skill dependency。

## Permissions and Side Effects

本轮 Phase 3 策展只读取 `skills/prioritization-frameworks/SKILL.md`，并写入对应 dossier、units 与 coverage；没有修改 `skills/` 快照，没有访问外链、下载模板、运行脚本、安装依赖、写 roadmap、触发客户 survey 或更改生产系统。

未来实际应用可能收集客户调查数据、组织评分会议、访问 Google Drive/Slides/Sheets 或外部课程，并影响 roadmap 和资源配置。这些动作需要各自的数据治理、网络访问和决策授权；本来源没有提供授权机制。

## Gates

来源没有声明 formal Gates；以下是为防止错误套用而策展推导的检查点，不是来源原文：

- Object Gate：是否明确待排序对象；feature request 若掩盖对象，可先澄清底层 problem/opportunity。
- Framework Gate：框架是否匹配 customer problem、initiative、requirement、personal task 或 expectation-understanding 场景。
- Data Gate：所选公式的所有输入是否存在、单位是否明确；缺失时停在输入清单。
- Scale Gate：Importance/Satisfaction、Confidence、Ease、Effort 等量表是否按框架分别校准，未发生隐式混用。
- Interpretation Gate：结果是否按框架能力边界解释，尤其不把 Kano 或 quick-triage matrix 冒充严格战略排序。
- Phase 3 策展 Gate：dossier 恰有 16 个规定 H2；units 字段、类型、状态、路径和逐字 excerpt 合同通过；coverage 登记唯一 reachable source file。

## Open Questions

- Opportunity Score survey 的题目、样本选择、聚合方法、误差与显著性没有定义。
- ICE 的 affected customers 和 RICE Reach 使用什么时间窗口、是否去重没有定义。
- Confidence、Ease、Effort 的评分锚点、评分人和校准机制没有定义。
- Weighted Decision Matrix 的 criteria、weights、normalization 和 sensitivity analysis 没有定义。
- 来源没有处理 ties、dependencies、mandatory work、capacity、risk appetite 或 portfolio balance。
- 三个展开公式与外部模板/文章的当前版本一致性未联网核验。

## Unique Value

该来源的独特价值是以“排序对象”而非流行度选方法：Opportunity Score 面向 customer problems，ICE 面向快速 initiative/idea prioritization，RICE 面向需要 reach/effort granularity 的较大团队；同时明确 Kano 是 expectation understanding、Impact vs Effort 只是 quick triage。这些边界能防止把所有决策退化为一张通用打分表。

它还把 Opportunity Score 嵌入 ICE/RICE 的 Impact 定义，形成从 customer need evidence 到 initiative score 的桥梁。但这是该来源的特定公式口径，不应无标注替换其他组织已有的 ICE/RICE 定义。

## Reading Coverage

- `skills/prioritization-frameworks/SKILL.md` — `read`；frontmatter、core principle、Opportunity Score/ICE/RICE 公式、9-framework overview、Templates 与 Further Reading 已完整读取。
- `skills/prioritization-frameworks/references/` — `excluded`；来源快照中不存在该目录。
- `skills/prioritization-frameworks/reference/` — `excluded`；来源快照中不存在该目录。
- `skills/prioritization-frameworks/templates/` — `excluded`；来源只有外部 template links，没有本地目录。
- `skills/prioritization-frameworks/examples/` — `excluded`；来源快照中不存在该目录。
- `skills/prioritization-frameworks/scripts/` — `excluded`；来源快照中不存在该目录，未执行任何脚本。
- `SKILL.md:64-67` 的四个 template URLs — `excluded`；外部链接未访问，非本地 reachable files。
- `SKILL.md:73-75` 的三个 Further Reading URLs — `excluded`；外部链接未访问，非本地 reachable files。
