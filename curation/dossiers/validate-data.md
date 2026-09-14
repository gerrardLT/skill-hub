# validate-data 来源能力档案

## Problem

在数据驱动的研发、分析与产品决策流中，向管理层或利益相关方呈现未经严格质检的分析报告极易导致灾难性后果：微小的 SQL 连接缺陷导致行数呈笛卡尔积膨胀（Join Explosion）、幸存者偏差（Survivorship Bias）导致遗漏流失客群、跨时区未统一引发统计断代、以及将未结束的当期数据直接对比完整历史周期的未完成周期误判。传统的人工审阅往往缺乏系统化的防错清单，容易轻信表面符合预期的数字，将具有致命逻辑缺陷的结论推向高层决策。

## When to Use

- **面向重大利益相关方汇报前的数据审查**：在向管理层、业务方或外部客户发送季度业务总结、财务报表或流失归因分析前执行全流程质检。
- **复杂 SQL 查询与聚合逻辑核验**：检查多表 JOIN、GROUP BY 粒度、条件过滤以及比率分母是否准确。
- **分析结论与数据证据匹配度评估**：检查报告结论是否被真实数据支撑、是否误把相关性当作因果性、是否过度外推。
- **可视化图表合规度检查**：检查柱状图零基线截断、非均匀刻度比例、3D 失真效果及具有误导性的轴定义。

## When Not to Use

- **自动化单测或静态类型检查**：代码级语法 linting、单元测试覆盖率核查（应由 vitest 或 eslint 处理）。
- **实时高并发数据库查询调优**：索引缺失优化、数据库执行计划（EXPLAIN ANALYZE）深潜（应由专门的数据库 DBA 工具处理）。

## Role

数据分析质检与逻辑偏差审查官（Analytical QA & Methodology Auditor）。专注于在数据分析成果向利益相关方交付前，从方法论假设、计算逻辑、合理性交叉校验、视觉呈现及叙述结论等多维度实施穿透式审查，给出置信度评级并指出隐患盲区。

## Inputs

- **待审分析载体**：Markdown 报告、Jupyter Notebook、电子表格、PRD 中的数据支撑段落。
- **底层查询与数据源元数据**：SQL 查询语句、表结构定义、数据快照时间（As of Date）。
- **图表与可视化素材**：嵌入报告中的折线图、柱状图、转化漏斗图及原始聚合数据集。
- **业务上下文与目标问题**：分析旨在解答的核心问题、人群界定与核心指标口径定义。

## Outputs

- **验证报告（Validation Report）**：
  - 总体置信度评级（Overall Assessment: Ready to share / Share with caveats / Needs revision）；
  - 方法论与假设审查结论（Methodology Review）；
  - 发现的缺陷清单（Issues Found，包含 High/Medium/Low 严重级别与影响说明）；
  - 计算与聚合独立抽检结果（Calculation Spot-Checks）；
  - 可视化失真检查结果（Visualization Review）；
  - 针对性改进建议（Suggested Improvements）；
  - 必须告知利益相关方的限制与声明（Required Caveats）。

## Workflow

1. **审阅方法论与初始假设（Review Methodology & Assumptions）**：
   - 检验问题框定（Question Framing）是否切题；
   - 检验表与数据源选择、时间跨度截取及分析客群（Population）定义是否存在无意排除。
2. **执行交付前 QA 清单（Run Pre-Delivery QA Checklist）**：
   - 逐项扫描数据质量检查项（数据源有效性、新鲜度、完备性、空值处理、去重性、WHERE 过滤）；
   - 扫描计算检查项（聚合粒度、分母非零与口径一致性、日期对齐、JOIN 类型及子项加和一致性）。
3. **排查典型分析陷阱（Check Common Analytical Pitfalls）**：
   - 重点审查 JOIN 膨胀、幸存者偏差、未完周期与完整周期对比、分母口径漂移、平均数再平均（Average of Averages）、时区偏差及辛普森悖论。
4. **独立抽检关键计算与量级核实（Verify Calculations & Sanity Check）**：
   - 独立反算核心指标；
   - 进行量级合理性检验（Smell Test）、同指标多途径交叉检验（Cross-Validation）与反向工程校验。
5. **评估可视化呈现规范（Assess Visualizations）**：
   - 柱状图强制要求 Y 轴从零开始；检查坐标轴标签、比较图表间刻度一致性，剔除失真元素。
6. **裁决叙述与结论置信度（Evaluate Narrative & Assess Confidence）**：
   - 核验结论是否具有充分证据、是否承认不确定性；
   - 输出三分制总体评估评级及必须披露的声明。

## Branches

- **SQL 逻辑专项核查分支（SQL Logic Deep-Dive）**：当输入为纯 SQL 脚本时，强制执行 JOIN 前后行数变化测试（`SELECT COUNT(*)` 探针），检查聚合字段与去重逻辑。
- **附带声明分享分支（Share with Caveats Branch）**：在方法基本成立但存在已知口径局限时，强制要求产出规范的“利益相关方须知声明列表”。
- **阻断重修分支（Needs Revision Gate Branch）**：一旦触发 High 级别缺陷（如关键数字错误、严重膨胀或颠倒因果），严格标记阻断并按优先级列出返工待办。

## Rules

- **不可平均“平均数”铁律（Never Average Averages）**：严禁对预计算的平均值直接求简单算术平均，必须从原始明细汇总或使用加权平均。
- **JOIN 行数守恒原则（Join Row Count Verification）**：在执行多表关联时，必须验证关联后行数是否符合业务实体对应关系，杜绝非预期的多对多膨胀。
- **完整时段对比铁律（Complete Periods Only）**：严禁拿进行中的未完成周期（如本月第10天）与完整历史周期直接进行数值总和对比。
- **柱状图从零起始原则（Bar Charts Start at Zero）**：所有柱状图坐标轴必须从 0 轴起始，禁止通过截断坐标轴人为夸大微小差异。
- **结论与证据相称原则（Proportional Confidence）**：结论陈述的笃定程度必须严格匹配数据证据的强弱；存在混杂因素时必须显式标注关联不等于因果。

## Exceptions

- **战略性定性探索**：新业务探索初期数据量极度稀缺时，可在明确标注小样本局限性的前提下，输出定性洞察与观察，不强制要求大样本统计显著性。
- **实时运维脉搏快照**：在线事故快速止血时，可接受带有时效局限的快照数据，事后再做完整周期复盘。

## Dependencies

- **工具生态依赖**：SQL 运行环境、数据仓库、Python/Jupyter 数据分析环境、报表渲染系统。
- **协作方依赖**：数据分析师、报告撰写者与业务决策人。

## Permissions and Side Effects

- **权限要求**：数据仓库只读权限、分析报告文档读取权限。
- **副作用**：无直接破坏性副作用；作为质量门禁可能阻断未达标分析材料的对外发布。

## Gates

- **Gate 1: Join & Aggregation Integrity Gate**：SQL 查询必须通过行数变化检验与非聚合列完整性检验，存在非预期膨胀时阻断。
- **Gate 2: Sanity Smell Test Gate**：核心指标必须通过数量级检验，子项百分比之和必须接近 100%。
- **Gate 3: Pre-Delivery Confidence Sign-off Gate**：在正式向高管或外部汇报前，必须取得“Ready to share”或明确列出“Required Caveats”。

## Open Questions

- 当底层上游数仓发生无通知静默数据污染时，下游分析审查工具如何通过差分指纹实现零假设自适应拦截？
- 如何在保护商业敏感数据的前提下，自动生成满足第三方审计的最小化脱敏可复现包？

## Unique Value

建立了涵盖“假设审查 -> 交付前清单 -> 七大经典分析陷阱排查 -> 独立反算验证 -> 图表合规 -> 叙述结论审计”的端到端严密防线，从源头杜绝带伤数据报告误导商业与技术重大决策。

## Reading Coverage

- `skills/validate-data/SKILL.md`: 涵盖全流程工作流、预交付 QA 清单（数据质量/计算/合理性/呈现）、七大经典陷阱（Join Explosion, Survivorship Bias 等）、合理性检验方法、可复现文档标准与报告模版。
