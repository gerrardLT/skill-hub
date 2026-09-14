# product-strategy-session Dossier

## Problem

`product-strategy-session` 解决的是产品或产品线存在战略模糊、方向分歧或只有 backlog 没有可信路线的问题。它把定位、问题发现与验证、方案探索、优先级和路线规划串成一个通常持续 2–4 周的可重复过程，目标是形成可供团队执行的 validated direction，而不是直接产出 feature list。证据见 `skills/product-strategy-session/SKILL.md:20-23`、`:38-51`。

问题不成立时不应调用：战略已经清晰且完成验证、只是战术 feature addition，或没有 executive sponsorship 使方向无法获得资源时。证据见 `skills/product-strategy-session/SKILL.md:58-67`。

## When to Use

- 新产品或重大 initiative 启动前，需要从定位推进到路线。
- 年度或季度战略规划需要跨职能形成共同方向。
- 既有产品需要 repositioning。
- 新产品负责人需要通过共同过程完成战略对齐。
- 团队有 backlog 但缺少方向，或需要把定位、发现和 roadmap 串起来。

调用时至少提供产品/产品线和推动 session 的 strategic question 最有帮助；既有 positioning、discovery artifacts、roadmap drafts 和需要对齐的人员可作为补充输入。已随调用传入的文本、context dump 或 `ARGUMENTS:` 内容不得重复追问，空手时仍可从 positioning 开始。证据见 `skills/product-strategy-session/SKILL.md:25-34`。

## When Not to Use

- 已有清晰且已验证的 strategy，不需要完整策略弧。
- 只增加战术功能，没有战略转向。
- 缺少 executive sponsorship，无法让战略获得资源或优先级。
- 把任务当作 feature brainstorm、waterfall planning 或 solo PM exercise。
- 低不确定性场景不应无条件执行所有阶段；应使用 decision points 缩短流程。

## Role

- Product manager：通常负责引导、整合产物、形成问题/方案/优先级/路线并推进执行规划。
- Product leadership 与 executives：提供战略约束、参与定位/优先级并在 Phase 5 对方向作资源和推进层面的对齐。
- Design：参与 persona、JTBD、问题、方案和 story map 等活动。
- Engineering lead：参与问题框定、方案可行性、epic 优先级、路线 sequencing 和执行规划。
- Marketing、sales、customer success、customer-facing teams：分别在定位、用户画像、问题与客户上下文中提供输入。
- `workshop-facilitation`：只定义 guided conversation 的交互协议；本来源定义六阶段的 workflow logic 和 domain outputs，发生冲突时以后者为准。证据见 `skills/product-strategy-session/SKILL.md:71-83`。
- Customer participants：在客户上下文不足、问题未验证或方案不确定时，作为访谈、POC 或实验对象；来源只规定数量和形式，不规定招募、同意或数据处理机制。

## Inputs

必填或核心输入：

- 产品或产品线。
- 推动 session 的 strategic question。

可选输入：

- 既有 positioning。
- 既有 discovery artifacts。
- roadmap drafts。
- 需要对齐的 stakeholders。

允许的未知状态：

- 没有已有材料时从 Phase 1 positioning 开始。
- 客户上下文不足、问题未验证或方案不确定时，不是假定已知，而是进入对应 discovery/experiment 分支并增加时间。
- 模板中的 `Success Metrics` 只声明需要填写 key metrics；来源没有定义指标公式、数据源或阈值，不能推断成固定验收标准。

## Outputs

主流程输出按阶段累积：

- Draft positioning statement。
- 1–3 个 hypothesis-driven proto-personas。
- 每个 persona 的 JTBD statements。
- Refined problem statement、How Might We question 和供 PRD/roadmap 使用的 formal problem statement。
- 跨 touchpoint 问题可选的 journey map，包含 pain points 和 opportunities。
- Opportunity solution tree，或 Lean UX Canvas 形式的 business problem、hypotheses、experiments。
- Top 3–5 initiatives 的 epic hypotheses。
- 复杂 feature 可选的 story map，含 backbone 和 release slices。
- Recommended prioritization framework、ranked backlog of epics 和按 release/quarter 编排的 roadmap。
- 可选的、带 citations 的 TAM/SAM/SOM market size projections。
- Stakeholder feedback、open questions、approval to proceed，以及根据反馈更新后的 strategy artifacts。
- 按模式拆解的 user stories、带 acceptance criteria 的 stories，以及 first sprint/release plan。
- 模板 `template.md` 定义的汇总结构：Strategy Context、Target Customer、Problem Framing、Opportunities、Solution Hypotheses、Prioritization、Roadmap / Sequencing、Success Metrics、Next Steps。

消费者是后续 PRD、roadmap、epic breakdown、user story 和 execution planning 能力；本来源本身不实现这些下游 Skills。

## Workflow

1. 确认产品/产品线和 strategic question，复用调用中已提供的 context，不重复询问；没有已有材料时从定位开始。
2. Phase 1（Week 1 Days 1–2）：运行 positioning workshop，形成 draft positioning；建立 1–3 个 proto-personas；为每个 persona 映射 JTBD。
3. 在 Phase 1 后判断 customer context 是否足够。若不足，准备 discovery interview、安排 5–10 次 customer interviews、验证 positioning assumptions，并增加 1 周；否则进入 Phase 2。
4. Phase 2（Week 1 Days 3–5）：运行 problem framing canvas，形成 refined problem statement 和 How Might We；创建 formal problem statement；当问题跨多个 touchpoints 或 phases 时可选运行 customer journey mapping。
5. 在 Phase 2 后判断问题是否 validated。若未验证，安排 5–10 个客户的 discovery interviews，根据发现迭代 problem statement，并增加 1 周；否则进入 Phase 3。
6. Phase 3（Week 2 Days 1–3）：用 OST 生成 opportunities、solutions 和 POC recommendation；若偏好 hypothesis-driven approach，可改用 Lean UX Canvas；定义 top 3–5 initiatives 的 epic hypotheses；复杂 feature 需要 release planning 时可选创建 user story map。
7. 在 Phase 3 后判断是否需要在 commit 前测试方案。高不确定性时设计 POC experiments，用 prototype、concierge 或 landing page test 测试 10–20 个客户，并增加 1–2 周；低不确定性时进入 Phase 4。
8. Phase 4（Week 2 Days 4–5）：选择 prioritization framework；按该框架给 epics 打分并形成 ranked backlog；按 release 编排 roadmap；仅在 exec presentation、fundraising 或 market sizing 需要时运行 TAM/SAM/SOM。
9. Phase 5（Week 3）：major launch 或 exec buy-in 需要时可先创建 visionary press release；向 execs、product leadership 和 key stakeholders 展示 positioning、problem、solution options/prioritization 和 roadmap，收集 feedback、open questions 与 approval to proceed；用 1–2 天更新 strategy artifacts。
10. Phase 6（Week 4）：用 epic breakdown advisor 拆解 top epic；写带 acceptance criteria 的 user stories；与 engineering 规划 first sprint/release。
11. 汇总并交付模板规定的策略摘要。总时长按分支为 minimum 2 weeks、typical 3 weeks、maximum 4–6 weeks；Phase 6 后从 strategy mode 转入 execution，避免无限分析。证据见 `skills/product-strategy-session/SKILL.md:292-338`、`:392-397`。

## Branches

- Customer context：足够则进入 Phase 2；不足则 discovery interview prep、5–10 次访谈、验证 positioning assumptions、+1 week。
- Problem validation：已验证则进入 Phase 3；未验证则 5–10 个客户访谈、迭代问题陈述、+1 week。
- Journey mapping：问题跨多个 touchpoints 或 phases 时才加入。
- Solution exploration：OST 是默认路径；偏好 hypothesis-driven approach 时使用 Lean UX Canvas 替代。
- Story map：只有复杂 feature 且需要 release planning 时加入。
- Solution commitment：high uncertainty 进入 10–20 customer POC experiments，+1–2 weeks；low uncertainty 直接进入 prioritization。
- TAM/SAM/SOM：仅在 exec presentation、fundraising 或 market sizing 场景加入，输出必须带 citations。
- Press release：仅 major product launch 或 exec buy-in 场景加入。
- 监管或内部产品决策：示例显示可把 opportunity cost、vendor-grade validation、named exit、kill criterion 和 non-goals 作为路线决策约束；这些是可迁移的 decision patterns，不是固定数字或当前项目事实。
- 任何暂停、恢复、逐题提问和 quick-select 的对话行为来自被引用的 facilitation protocol；本来源只保留其协议依赖和 workflow precedence，不把未读取的下游协议细节当成本来源事实。

## Rules

- 先理解定位和问题，再探索方案；不得把策略 session 降级为 feature brainstorm。
- 关键假设必须经过对应的 customer context、problem validation 或 solution experiment decision point；不能无条件跳过或无条件增加验证。
- 需要跨职能参与，不能由 PM 独自完成后再向团队展示成品。
- 开始前应 확보 executive commitment，并预定 Phase 5 presentation；没有 sponsorship 时策略难以获得资源。
- 使用 `template.md` 记录完整汇总结构，但不得把模板中的 placeholder 当作已完成产物。
- 将 2–4 周视为 time-box；完成 Phase 6 后转入 execution，不把 strategy mode 延长成永久过程。
- 来源中声明的 5–10、10–20、1–3、3–5、2–4 周等数字是该 workflow 的操作参数或示例约束；生命科学示例中的公司、人数、市场规模、license 数量、18 个月和 engineer-quarters 不能外推为通用阈值。
- 下游 Skills 只作为依赖声明；本次拆解不读取或执行这些 Skills。

## Exceptions

- 空手调用不是阻塞条件：允许从 positioning 开始。
- 已有足够 artifacts 时可以 skip ahead，而不是重复做全部活动。
- Customer journey mapping、story map、TAM/SAM/SOM、press release 都是条件分支，不是每次必做。
- 低不确定性时可以不运行 solution experiments；高不确定性时应在 commit 前测试。
- 生命科学示例中的 compliance artifact 变成 roadmap gate、named exit、kill criterion 和 non-goals，说明受监管或内部资源竞争场景需要把领域约束提升为决策条件；来源没有授权把这些示例阈值复制到其他场景。
- `Dean's Work` 的引用区保留了待补链接占位符；它不是可执行依赖，也不是本项目事实。

## Dependencies

来源入口声明编排以下依赖，但它们不属于本次 `product-strategy-session` 目录的已读附件：

- Phase 1：`positioning-workshop`、`proto-persona`、`jobs-to-be-done`。
- Phase 2：`problem-framing-canvas`、`problem-statement`、可选的 `customer-journey-mapping-workshop`、验证分支的 `discovery-interview-prep`。
- Phase 3：`opportunity-solution-tree`、替代路径 `lean-ux-canvas`、`epic-hypothesis`、可选的 `user-story-mapping-workshop`。
- Phase 4：`prioritization-advisor`、可选的 `tam-sam-som-calculator`。
- Phase 5：可选的 `press-release`。
- Phase 6：`epic-breakdown-advisor`、`user-story`。
- 对话引导协议：`workshop-facilitation`，来源指定其为 interaction protocol，但本目录未包含该 supplement。

运行时、CLI、MCP、网络、凭据和脚本：当前目录未发现入口声明的运行时命令、CLI/MCP 调用、网络访问、凭据要求或脚本；dependency scan 亦未发现需要 review 的执行信号。External frameworks 和 Dean's Work 只作为来源中列出的引用文本，不在本任务中联网核验。

## Permissions and Side Effects

本次拆解只读取 `skills/product-strategy-session/` 的四个快照文件，并写入 `curation/dossiers/`、`curation/units/` 和 `curation/coverage.json`。不修改 `skills/` 原始快照，不安装依赖，不执行下游 Skills，不运行来源中描述的访谈、实验、外部服务或生产操作，不使用真实凭据。

若未来运行该 workflow，其声明的 side effects 是创建和更新 strategy artifacts、组织客户访谈/POC、收集 stakeholder feedback、形成 roadmap 和执行计划；这些属于 workflow 产物或外部协作影响，不代表本次拆解已执行。

## Gates

- `retain`：来源明确声明且可独立验收的 workflow、决策点、条件分支、输入/输出契约和不可绕过规则。
- `conditionalize`：只在来源明确给出条件的 optional activity 或 uncertainty branch 下承接，例如 journey map、Lean UX、story map、TAM/SAM/SOM、press release 和 solution experiments。
- `merge`：只用于示例中重复表达同一完整行为时；示例应作为 composite evidence，不按示例数字拆成独立能力。
- `needs-input`：缺少 product/strategic question，或需要确认是否属于高不确定性、跨 touchpoint、重大 launch、exec buy-in 等条件分支。
- `blocked`：没有可用的 executive sponsorship，或所需下游依赖在实际组合执行中不可用；本来源仅记录这一状态含义，不代替依赖安装或执行。
- `pass` 的直接证据：dossier 有 16 个规定 H2；每个 unit 有来源路径、1-based inclusive 行号和可重建的 exact `raw_excerpt`；coverage 登记四个已读文件；schema/source/test verifier 全部通过。

## Open Questions

- 来源没有定义 customer interview 的招募标准、访谈问题、同意和证据记录格式；应由 `discovery-interview-prep` 或项目规则补充，不能在本 dossier 中猜测。
- 来源没有定义“足够 customer context”“problem validated”“high uncertainty”的判定量表；组合时需要项目负责人或上游能力提供判定标准。
- `Success Metrics` 只在模板中出现，没有指标公式、数据源、基线或阈值。
- roadmap sequencing 没有规定 capacity、依赖、风险和发布日期的具体计算方法。
- External frameworks 的书目信息和 Dean's Work 链接没有在本任务中联网核验。
- 下游依赖的当前版本、实际入口和输出契约尚未在本来源 dossier 中读取；不能据此断言它们可直接组合。

## Unique Value

该来源的不可替代部分不是单个产品策略方法，而是把定位、客户问题验证、方案实验、优先级、路线、stakeholder approval 和首个 sprint 串成带自适应决策点的时间盒流程。它明确规定何时增加 discovery/experiment 时间、何时跳过可选活动、何时停止 strategy mode，并把策略输出连接到可执行的 epics、stories 和 release plan；单独的定位、发现或路线 Skill 不提供这条完整的跨阶段转接契约。

生命科学示例进一步提供了一个可迁移的约束决策模式：将内部 opportunity cost、合规交付物、services-in-disguise 风险、pilot scope、named exit、kill criterion 和 non-goals 写入路线决策。但示例中的事实和数字只承担证据作用，不能直接转为通用规则。

## Reading Coverage

- `skills/product-strategy-session/SKILL.md` — `read`；入口 workflow、边界、六阶段、分支、pitfalls、依赖和引用均已读取。
- `skills/product-strategy-session/template.md` — `read`；完整汇总模板已读取。
- `skills/product-strategy-session/examples/sample.md` — `read`；good/bad strategy session 及修复路径已读取。
- `skills/product-strategy-session/examples/sample-lifesciences.md` — `read`；受监管内部产品决策示例已读取。
- `skills/product-strategy-session/references/` — `excluded`；来源快照中不存在该目录。
- `skills/product-strategy-session/reference/` — `excluded`；来源快照中不存在该目录。
- `skills/product-strategy-session/sections/` — `excluded`；来源快照中不存在该目录。
- `skills/product-strategy-session/scripts/` — `excluded`；来源快照中不存在该目录，且 dependency scan 未发现脚本。
- `workshop-facilitation` supplement — `excluded`；这是被入口声明的外部 interaction protocol，本来源目录未提供；未安装、未读取、未执行。
- Related Skills listed in `SKILL.md:403-431` — `excluded` as source attachments；它们是下游依赖声明，不属于本来源可达附件，本任务不读取其内容。
