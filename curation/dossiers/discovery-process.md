# discovery-process Dossier

## Problem

`discovery-process` 解决的是团队从一个问题假设出发，却缺少从问题框定、研究、综合、方案探索、实验到决策的完整路径。其目标是在投入完整开发前逐步验证问题与方案，降低“先建再找需求”的风险；来源将它定义为与 delivery 并行、可重复运行的 continuous discovery practice，而非一次性研究项目（`skills/discovery-process/SKILL.md:20-23`）。

问题已经充分理解、只是战术 bug/technical debt，或组织已承诺某个方案且尚未解决 alignment 时，不应调用完整 discovery cycle（`skills/discovery-process/SKILL.md:66-69`）。

## When to Use

- 从粗略 problem hypothesis 探索新产品或 feature area。
- 系统调查 retention、churn、activation 等行为问题。
- 在 roadmap commitment 前验证战略 initiative。
- 建立持续的 customer touchpoint 与 discovery cadence。
- 输入最好包含起始问题假设；prior research、customer access、timeline 和本轮发现要支持的 decision 可补充。空输入也允许从问题框定开始构造假设（`skills/discovery-process/SKILL.md:25-34`）。

## When Not to Use

- 问题已经被充分理解，应转入 execution。
- Stakeholders 已经承诺具体 solution；应先处理 alignment，而不是用 discovery 为既定答案背书。
- tactical bug fix 或 technical debt 不需要问题发现。
- 只想做 solution usability testing；来源区分 problem discovery 与 solution testing。
- 不能获得必要客户证据、又要求声称问题或方案已验证时，应停在未验证状态，而非补造证据。

## Role

- Product manager：主导六阶段编排、组织研究、综合证据、维护问题与方案假设，并形成 GO/PIVOT/KILL 建议。
- Design：参与问题框定、访谈、综合、方案探索与 prototype experiments。
- Engineering lead：参与问题框定、机会/方案探索、可行性判断和需要工程实现的实验。
- Customer participants：提供过去行为、workarounds、alternatives 和 pain intensity 的一手证据；来源未定义招募同意或数据治理细则。
- Executives、product leadership、key stakeholders：消费 readout 并对后续建议形成 alignment。
- `workshop-facilitation` supplement：仅提供 guided conversation 的交互协议；`discovery-process` 保留 workflow sequence 与 domain-specific outputs 的优先权（`skills/discovery-process/SKILL.md:73-85`）。

## Inputs

核心输入是 starting problem hypothesis，即使很粗略也可。可选输入包括 prior research、customer access、timeline，以及 discovery 必须支持的 decision。

调用文本、pasted context dump 或 `ARGUMENTS:` 已给出的内容都算已回答，必须复用并跳过相应追问。空手调用不是阻塞：从 problem framing 开始构造 hypothesis。来源示例中的具体 churn、drop-off、人数、周期和行业事实仅用于说明，不是默认输入或通用阈值。

## Outputs

- Phase 1：problem hypothesis、research questions、validate/invalidate success criteria。
- Phase 2：interview guide、participant roster、synthesis plan。
- Phase 3：recorded sessions + detailed notes、按频率排列的 support-ticket themes、quantitative analytics insights；来源的 `Top 10` 只是操作参数，不是通用 Gate。
- Phase 4：affinity map、prioritized pain points、customer quotes、validated/refined problem statement。
- Phase 5：solution options、experiment results、customer feedback。
- Phase 6：GO/PIVOT/KILL decision；仅 GO 时生成 epic hypotheses 与 PRD；另记录 stakeholder alignment。
- 生命科学 Phase 6 案例还展示 build/defer scope、跨全部 sites 和两个 quarters 的 longitudinal metric，以及 residual assumptions/ownership log；其中所有数字和组织事实都只属于案例。
- `template.md` 提供 Discovery Summary 的汇总槽位；placeholder 不代表已获得证据。

这些是未来执行 workflow 的声明输出；本轮 Phase 3 策展没有开展访谈、实验或产品决策。

## Workflow

1. 接收并复用已有 hypothesis/context；没有 hypothesis 时从问题框定建立一个。
2. Phase 1 依次处理 problem framing、formal problem statement；仅当 segment 或 motivations 不清时补 proto-persona 或 JTBD，最后形成本阶段三类正式 outputs。
3. Gate 1 检查是否有足够 context 开始 research；不足时先审阅 support/churn/NPS、analytics、competitor/market evidence。
4. Phase 2 分别完成 interview prep、participant recruitment、scheduling/recording consent，再形成 guide、roster 和 synthesis plan。
5. Phase 3 围绕 past behavior、workarounds、alternatives 与 pain intensity 做访谈，结构化记录并并行检查 support、analytics、surveys，正式交付录音/详注、频率主题和定量洞察。
6. Gate 2 以重复模式且不再产生新信息判断 saturation；未达到则追加访谈并延长计划，来源数字均为 heuristic。
7. Phase 4 分别做 affinity mapping、条件性 journey map、pain prioritization、problem statement update，并汇总正式 outputs。
8. Phase 5 采用 OST，或在偏好 hypothesis-driven 时改用 Lean UX；随后分别设计和执行最小学习实验并汇总 outputs。
9. Gate 3 判断方案是否 validated；未通过则 pivot 到下一候选并重跑适配实验。
10. Phase 6 独立记录 GO/PIVOT/KILL；仅 GO 时连接 epic hypothesis 和 PRD；随后 read out 并记录真实 alignment，最后汇总正式 outputs。
11. 来源 timeline 保留完整顺序：Week 1 framing/planning/研究启动，Week 2 研究继续/synthesis，Week 3 solution/experiments，Week 4 decision/document；未饱和增加研究时间，方案未验证增加 pivot/retest 时间。
12. 规划时在 fast（3 周）、typical（4 周）、thorough（6-8 周）profile 中选择或调整；人数、轮次、分钟和周数都是 planning heuristics，不是 SLA。
13. 使用 `template.md` 汇总证据、实验、决策和 next steps，并维持与 delivery 并行的持续实践。

## Branches

- 空输入从 framing 起步；inline context 已覆盖的内容不重问。
- Context 不足先收集已有证据；来源估计增加 2-3 天，仅作 planning heuristic。
- Segment 不清才做 proto-persona；motivation 不清才做 JTBD。
- 未饱和追加访谈并影响周期；已饱和进入 synthesis。
- Pain 跨多个 journey phases 时才做 customer journey map。
- OST 与 hypothesis-driven Lean UX 是替代路径，不是机械叠加。
- 方案未验证则 pivot/retest 并影响周期；验证后才进入 Phase 6。
- GO 才生成 epic hypotheses 和 PRD；PIVOT/KILL 不产生这些下游交付。
- Fast/typical/thorough 是可调整 planning profiles；实际 saturation 与 solution-validation 分支可使周期偏离 profile。
- 受监管场景可使用 retrospective test 或 bounded paper pilot，但必须明确证据弱点。

## Rules

- 先验证问题，再验证方案；analytics/support 不能完全替代 qualitative interviews 对“why”的解释。
- 访谈聚焦过去行为，结构化记录 context、actions、pain、workarounds、quotes 和 insights。
- 实验以最少工作学习关键未知，并预设可观察 success criteria。
- 决策同时检查 problem、solution、strategic fit 和 feasibility；readout 与 stakeholder buy-in 分开记录。
- Saturation evidence gate、当前 cycle 的 time-box/execution handoff gate、后续 continuous discovery cadence 是三个独立约束，不互相绑定。
- 来源中所有人数、百分比、天数、金额、周期、评分和轮次都是 heuristic 或案例事实，不得提升为 SLA、配额或通用 Gate。
- 生命科学案例提醒：纵向指标必须保留 measurement window，决策后仍须记录 residual assumptions、representativeness limitation 和 owner；这些教学点不把案例数字泛化。
- `template.md` 是记录结构，不是完成证据；placeholder 不得冒充发现。
- Related Skills 只按 phase 保留 dependency map；本轮均未读取、未验证、未执行，执行前需另行核验契约。

## Exceptions

- 空手调用可开始，不要求先有正式 hypothesis。
- 已有 context 应直接计入答案，不能重新从第一问开始。
- Proto-persona、JTBD、journey map、Lean UX alternative、epic hypothesis 和 PRD 均由明确条件触发，不是每轮必做。
- 生命科学示例允许在 live experiment 不合规时改用较弱但可陈述局限的 retrospective/paper test；这不是降低证据诚实度的授权。
- 发现超出产品范围的问题时，应命名并移交正确 owner，而不是把所有发现吸收到产品 roadmap。
- 来源 `Dean's Work` 含待补链接占位符，只能保留为未解析 reference metadata。

## Dependencies

来源按 phase 声明编排：Phase 1 的 `problem-framing-canvas`、`problem-statement`、条件性的 `proto-persona`/`jobs-to-be-done`；Phase 2 的 `discovery-interview-prep`；Phase 4 条件性的 `customer-journey-mapping-workshop`；Phase 5 的 `opportunity-solution-tree` 或替代 `lean-ux-canvas`；Phase 6 GO 分支的 `epic-hypothesis`/`prd-development`。这些下游 Skills 本轮均未读取、未验证、未执行，因此 dependency map 只保留来源声明，不能证明版本或契约兼容。

Guided conversation 依赖恢复的 `workshop-facilitation` supplement。其 `SKILL.md` 与 `examples/inline-input-flow.md` 已完整读取，确认 one-question turns、entry modes、诚实 progress labels、pause/resume、decision-point recommendations 和 inline input crediting；它是交互协议依赖，不作为 discovery 领域方法 unit。`supplement.json` 已读取并确认 repository、revision、reason、文件清单与哈希声明。

当前来源目录没有 CLI、MCP、脚本、网络或凭据依赖。External frameworks、Productside Blueprint 和 Dean's Work placeholder 仅作 reference metadata；本轮未联网或外部核验。

## Permissions and Side Effects

本轮分析只读取来源、合同、相邻样例和 supplement，并只写 `curation/dossiers/discovery-process.md`、`curation/units/discovery-process.jsonl`、`curation/coverage.json`；没有执行来源或第三方脚本、Skill、访谈、实验、安装、网络、生产系统或凭据操作。

未来实际运行该 workflow 会安排客户访谈、请求 recording consent、处理 transcripts/notes、分析 support/analytics、运行 prototypes 或 experiments、创建决策与 PRD 等 artifacts，并影响 roadmap。来源没有给出隐私、保留期、实验审批或生产变更授权机制，执行前需由项目治理补齐。

## Gates

- Route Gate：问题是否仍存在 discovery uncertainty；问题已理解或只是 bug/technical debt 时不进入。
- Context Gate：是否有足够 evidence 开始 research；不足则先收集已有数据。
- Saturation Gate：是否还在产生新 insights；判定必须记录直接证据，不能只引用机械样本数。
- Solution-validation Gate：实验是否支持关键 hypothesis；失败进入 pivot/retest。
- Decision Gate：problem validated、solution validated、strategic fit、feasible 四项共同支持 GO；否则 PIVOT 或 KILL。
- Phase 3 策展 Gate：dossier 恰有规定 16 个 H2；unit 字段、类型、状态、路径和逐字 excerpt 合同通过；coverage 登记所有 reachable source 与 manifest-declared supplement files。

## Open Questions

- 来源没有给出“enough context”“saturation”“validated”和“feasible”的跨项目量表，应由项目研究计划定义。
- 招募、知情同意、录音、个人数据处理、保存期限与访问控制未定义。
- quantitative analytics 的数据源、查询口径和与 qualitative evidence 的权重未定义。
- 各 experiment type 的风险审查、统计设计和上线授权未定义。
- 下游 Skills 的当前版本和输出兼容性未在本来源拆解中核验。
- External frameworks 与 Dean's Work 占位引用未联网验证。

## Unique Value

该来源的独特价值是把 problem hypothesis 到 GO/PIVOT/KILL 串成三个显式学习 Gate 的六阶段闭环：先决定 context 是否够、再决定研究是否饱和、最后决定方案是否经实验支持。它同时连接 qualitative interviews、support/analytics、affinity synthesis、机会树/Lean UX、最小学习实验和正式决策，因此不是单一访谈、问题陈述或 usability testing 能力的重复。

生命科学示例补充了受监管环境中的证据诚实模式：访问昂贵时先用已有数据杀死错误假设；不能 live experiment 时使用较弱替代测试并明示局限；超出产品边界的发现移交 owner。其 Phase 6 还示范了把 build/defer scope、longitudinal metric 的 measurement window、决策后 residual assumptions 与 owner 一起写入记录。以上教学价值可迁移，但 31/14 天、两个 quarters、两个 sites、40% 等均是案例事实，不外推为通用 Gate。

## Reading Coverage

- `skills/discovery-process/SKILL.md` — `read`；入口、边界、六阶段、三个 decision points、pitfalls、依赖和引用均已完整读取。
- `skills/discovery-process/template.md` — `read`；Discovery Summary 完整模板已读取。
- `skills/discovery-process/examples/sample.md` — `read`；SaaS good/bad discovery 复合案例及修复路径已读取。
- `skills/discovery-process/examples/sample-lifesciences.md` — `read`；受监管多站点临床流程案例及方法边界已读取。
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/SKILL.md` — `read`；恢复的 guided interaction protocol 已完整读取。
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/examples/inline-input-flow.md` — `read`；inline input crediting 与反模式示例已完整读取。
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/supplement.json` — `read`；已核对 provenance、revision、reason、declared files 与 hashes；它是 manifest metadata，不属于 coverage 的 material-file set。
- `skills/discovery-process/references/` — `excluded`；来源快照中不存在该目录。
- `skills/discovery-process/reference/` — `excluded`；来源快照中不存在该目录。
- `skills/discovery-process/templates/` — `excluded`；来源使用根目录 `template.md`，不存在复数目录。
- `skills/discovery-process/sections/` — `excluded`；来源快照中不存在该目录。
- `skills/discovery-process/scripts/` — `excluded`；来源快照中不存在该目录，未执行任何脚本。
- `SKILL.md` 列出的 Related Skills — `excluded`；它们是跨 Skill orchestration dependencies，不是 verifier 所定义的本来源 reachable attachments，本轮未读取或执行。