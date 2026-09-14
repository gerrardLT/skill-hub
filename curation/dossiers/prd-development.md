# prd-development Dossier

> 本文件针对纳入范围的顶层 Skill `prd-development`。事实判断来自 `skills/prd-development/` 原始快照；交互协议判断来自已校验来源身份的 `workshop-facilitation` supplement。分析性判断均在正文中明确说明。

## Problem

`prd-development` 解决的是重大功能或产品计划从零散发现笔记、研究、Slack 讨论和隐性产品经理知识，转化为可供跨职能对齐与工程交接的完整 PRD 的问题。它要求文档同时回答问题、用户、战略时机、方案、指标、需求、范围边界、依赖风险和未知项，而不是只列功能。

如果团队只面对小型缺陷、琐碎功能、已完全对齐且只需用户故事的工作，完整 PRD 会制造不必要的流程负担；如果工作仍处于连续发现实验阶段，则应先使用 Lean UX Canvas 或发现类方法，而不是假装已经进入交付定义。

## When to Use

- 启动重大功能、产品计划或复杂跨职能交付，需要统一“为什么做、为谁做、做什么、如何验收”。
- 已完成或部分完成发现工作，需要把证据、persona、战略背景、指标和约束组织为工程可消费的来源真相。
- 需要显式记录范围内、范围外、决策理由、依赖、风险和开放问题，以控制范围蔓延并支持后续成员加入。
- 输入可以是完整 context dump，也可以只有功能名称；已有输入必须被视为已回答内容，不能重复追问。
- 硬件、工业或监管敏感项目也可使用，但必须把认证、安全回滚和不可逆物理交付前置为硬 Gate，而不能套用 SaaS 的边做边学节奏。

## When Not to Use

- 小型 bug 或琐碎功能；直接写修复说明或用户故事更合适。
- 问题和方案已经清楚并完成对齐，只差拆故事与验收标准。
- 连续发现、低成本假设实验或尚未决定是否建设；应先走发现或 Lean UX 路径。
- 用户要求像素级 UI、按钮颜色或实现细节；PRD 只定义高层方案和可验证行为，设计与工程细节由对应角色负责。
- 缺少事实但又不允许标记假设或开放问题的场景；该 Skill 禁止用编造数据填满模板。

## Role

- **主要执行者：** 产品经理负责汇总证据、主持对齐、维护 PRD，并确保各章节互相一致。
- **协作者：** 设计和工程应参与方案可行性、故事拆解、约束与风险识别；QA 应参与验收标准的可测试性评审，但不负责替产品经理创造业务事实。
- **证据与数据提供者：** 客户研究、支持、销售、分析和业务负责人提供问题证据、基线、目标与战略上下文。
- **审批者：** 利益相关方可在可选的 Day 4 评审中给出反馈或批准；源文没有授权执行者替审批人声明批准。
- **交互协议：** guided conversation 由 `workshop-facilitation` 约束节奏；`prd-development` 仍拥有领域流程和输出冲突时的优先权。

## Inputs

- **核心输入：** PRD 覆盖的 feature 或 initiative。
- **可选输入：** discovery notes、problem statement、user research、success metrics、constraints、OKR、战略 memo、竞品研究、wireframe、story map、依赖与风险信息。
- **上下文继承：** skill invocation 后的文本、粘贴的 context dump 或 `ARGUMENTS:` 均算已回答内容；必须先提取并跳过已覆盖问题。
- **空输入：** 允许从 problem definition 开始，但不能因此编造证据、数字、批准或承诺。
- **未知值：** 可合理推断但未验证的内容必须内联标记 `Assumption`；无法回答且需要发现、数据或利益相关方决策的内容必须内联标记 `Open Question`。
- **guided mode 输入：** 用户选择 Guided、Context dump 或 Best guess；Best guess 允许推断，但必须在结束时给出 `Assumptions to Validate`。

## Outputs

主要产物是使用 `template.md` 填写的 living PRD，包含：

1. Executive Summary；
2. Problem Statement；
3. Target Users & Personas；
4. Strategic Context；
5. Solution Overview；
6. Success Metrics；
7. User Stories & Requirements；
8. Out of Scope；
9. Dependencies & Risks；
10. Open Questions。

附加输出包括 document metadata/change log、每节内联的 Assumption/Open Question、跨章节一致性检查、风险 mitigation、可测试 acceptance criteria，以及 PRD Self-Assessment（最强章节、最弱章节、最高风险假设和单一 recommended next step）。硬件场景还应产出监管/安全 Gate、硬顺序约束、非回归路径和绝对 guardrail。

## Workflow

1. **吸收已有上下文。** 解析 invocation、context dump 和附加参数，标记已回答内容，避免重复提问。
2. **选择交互路径并维持协议。** Guided 逐题进行；Context dump 先完整吸收再只补缺口；Best guess 推断缺失信息但标记假设；single-shot 请求走压缩 fast path。常规问题在实用时提供简短、尽量互斥的 quick-select，并在答案开放时加入 `Other (specify)`；接受 `#1`、单选、多选和自定义文本，并综合多选结果。只有追问能实质改善建议质量时才追问，只在真正的决策点给 numbered recommendations。结束时汇总已做决定；若使用 Best guess，再列 `Assumptions to Validate`。
3. **Phase 1 — Executive Summary。** 先按 solution/persona/problem/impact 形成一段摘要以暴露模糊点，最后再根据完整 PRD 回写。
4. **Phase 2 — Problem Statement。** 明确谁遇到什么可观察问题、为何痛苦，并用访谈、数据、工单或原话支撑；可选补 journey map 和 JTBD。
5. **Phase 3 — Target Users & Personas。** 定义 primary/secondary persona、目标、痛点、行为和 JTBD，确保 persona 对应真实客户而非内部团队。
6. **Phase 4 — Strategic Context。** 连接业务目标，按需估算市场、评估竞品，并说明 why now；估算数字必须标记为假设。
7. **Phase 5 — Solution Overview。** 只描述高层方案、关键能力、可选 flow/wireframe/story map；每项能力必须回到问题或 JTBD，不规定像素级 UI。
8. **Phase 6 — Success Metrics。** 定义一个 primary metric、secondary metrics、guardrails，以及 baseline、target、timeline 和 instrumentation 缺口。
9. **Phase 7 — User Stories & Requirements。** 先写可检验 epic hypothesis，再拆分故事，为每个故事写可测试 AC，并把约束、错误态和边界条件放进可独立验收范围。
10. **Phase 8 — Out of Scope & Dependencies。** 写清本次不做什么及原因，列出 technical/external/team dependencies、四类风险、mitigation、owner 和 unresolved decisions。
11. **Review & Refine。** 通读全文，执行每节 `Before moving on` 的跨章节检查，与设计/工程/QA 评审，补充 feedback，不把文档冻结成不可变合同。
12. **Self-Assessment。** 汇总最强/最弱章节、最高风险假设及验证办法，给出分享前最重要的下一步。
13. **可选 stakeholder review。** 展示 PRD、吸收反馈并记录批准；没有真实批准证据时不得写成已批准。

## Branches

- **Guided / Context dump / Best guess：** 三种入口由 supplement 定义；只有 Guided 需要多轮一问一答，Context dump 跳过已覆盖问题，Best guess 必须输出待验证假设。
- **Empty-handed / pre-populated：** 空输入从问题定义开始；富输入直接从第一个真实缺口继续，progress label 必须反映已跳过的问题。
- **Single-shot：** 用户明确要求一次性输出时，不强制多轮 facilitation，但未知值规则、范围边界和 Gate 仍保留。
- **Optional artifacts：** journey map、JTBD、TAM/SAM/SOM、competitive landscape、wireframe 和 story map 仅在问题复杂度或决策需要时启用。
- **Fast / typical / complex schedule：** 源文提供 1.5-4 天区间作为计划参考，不应被当成固定 SLA；frontmatter 的 60-120 分钟与正文周期存在口径冲突。
- **Interruption / pause / resume：** 元问题先直接回答再恢复状态；用户说 stop/pause 时立即停止，等待明确 resume。
- **Industrial/hardware：** 监管判定、安全回滚、现场可用性和不可逆制造约束可在建设前阻断全部工作；绝对 guardrail 优先于 primary metric。

## Rules

- 不得编造事实、数据、批准或承诺；所有推断和未知必须在出现位置内联标记。
- PRD 是沟通和对齐装置，也是 living document；它不是 waterfall contract、像素级 UI spec 或协作替代品。
- 每个章节都必须通过与前后章节的 traceability 检查：problem、persona、strategy、solution、metric、hypothesis、story、scope 和 risk 不能互相矛盾。
- Problem Statement 必须描述可观察问题并尽可能给出真实证据，不能用“用户想要更好体验”替代。
- Solution Overview 保持高层；没有回到问题/JTBD 的 feature 属于 scope creep。
- primary metric 必须直接测量核心问题，并配 baseline、target、timeline；secondary metric 不能取代 primary metric；至少有明确 guardrail。
- User Story 的 AC 必须可独立测试并覆盖相关边界，不能要求 QA 去其他章节猜测 done 的含义。
- Out of Scope 必须记录排除项和理由；风险必须有可执行 mitigation，而不是“持续关注”。
- guided conversation 每轮只问一个有针对性的问题，显示真实进度；常规问题可给 quick-select，只有决策点才给 recommendations。
- 用户已有上下文不得重问；stop/pause 必须立即生效。

## Exceptions

- “一个 primary metric”是源文的聚焦规则；若受监管或安全 guardrail 触发，guardrail 可以无条件停止功能，即使 primary metric 表现良好。
- 源文在故事示例中给出数量范围，并在 template 中用“5-6 个 AC”提示拆分；这些是经验启发，不应编译成机械数量 Gate。是否拆分应依据故事能否单独交付和验收。
- market sizing、journey map、JTBD、wireframe、story map 与 Day 4 approval 都是条件性步骤，不是所有 PRD 的硬要求。
- 组件 Skill 提供专门方法，但缺失组件时不应伪造其输出；可以标记 dependency/open question，或在保持方法边界的前提下人工完成。
- 工业示例改变的是 Gate 强度与顺序，不是另建一套无关模板；监管影响未知时应返回 `blocked`，而不是继续全部工程工作。

## Dependencies

### 已读取并纳入本 dossier 的文件

- `skills/prd-development/SKILL.md`
- `skills/prd-development/template.md`
- `skills/prd-development/examples/sample.md`
- `skills/prd-development/examples/sample-industrial.md`
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/SKILL.md`
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/examples/inline-input-flow.md`

### 已验证阻塞 supplement 身份

- repository: `deanpeters/Product-Manager-Skills`
- revision: `1b5a524ebb95e9497fa3f25002d8b8ec528d4444`
- root: `workshop-facilitation`
- manifest: `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/supplement.json`

### 源文声明的领域依赖

`problem-statement`、`discovery-process`、`problem-framing-canvas`、`customer-journey-mapping-workshop`/`customer-journey-map`、`jobs-to-be-done`、`proto-persona`、`tam-sam-som-calculator`、`positioning-statement`、`opportunity-solution-tree`、`user-story-mapping-workshop`、`epic-hypothesis`、`epic-breakdown-advisor`、`user-story`、`user-story-splitting`、`prioritization-advisor`、`pestel-analysis`、`feature-investment-advisor`、`pol-probe-advisor`、`business-health-diagnostic`、`saas-revenue-growth-metrics`、`recommendation-canvas`、`stakeholder-mapping` 等。它们是源文声明的可选或分阶段依赖；本 dossier 未把“目录存在”解释为“已完成语义和运行验证”。

该 Skill 本身不要求 CLI、MCP、网络或真实凭据。若实际读取 analytics、JIRA、客户数据或外部研究，必须另行获得对应权限并记录来源；本轮未执行这些动作。

## Permissions and Side Effects

- **默认读取：** 可读取用户提供的笔记、研究、指标、战略材料和模板；涉及客户数据或内部系统时仍受原系统权限约束。
- **文档写入：** 预期会创建或更新 PRD、change log 和 decision/open-question 记录；写入位置与发布目标必须由调用上下文明确。
- **外部调用：** 源文提到 analytics、JIRA、设计工具和研究来源，但未授权自动访问；缺少授权时只记录 dependency/open question。
- **审批与承诺：** 不得代表 reviewer、approver、监管或工程团队写入批准、日期、ETA 或承诺。
- **不可逆影响：** PRD 本身无生产变更，但其内容可能启动高成本实施；工业场景必须在监管 Gate 未关闭时阻断后续工作。
- **本轮 curation：** 只写 `curation/` 产物，不修改 `skills/`，不安装依赖，不执行第三方 Skill/script，不访问生产系统或真实凭据。

## Gates

- **通过：** 10 个核心章节均存在；问题有证据或明确未知；persona、方案、指标、故事、范围、风险可追溯；AC 可测试；假设和开放问题内联可见；Self-Assessment 给出最高风险假设和下一步。
- **章节 Gate：** 每个 `Before moving on` 检查必须处理矛盾或将其显式升级为 Assumption/Open Question，不能静默跨过。
- **needs-input：** 核心事实缺失且无法安全推断时，保留 Open Question、owner/deadline（若已知）并请求必要输入；不得用示例数字代替真实数据。
- **blocked：** 监管、认证、安全、关键依赖或无可接受缓解措施的风险阻断建设时，明确标记阻断范围和解除条件。工业示例中的 UL assessment 是全局阻断 Gate。
- **失败：** feature list 冒充 PRD；无证据、persona、metric、AC、out-of-scope、risk mitigation 或 unknown tagging；方案写成像素级 UI；已有上下文被重复追问；Best guess 未列待验证假设。
- **交互 Gate：** guided mode 必须一轮一个问题、进度真实、pause 立即停止；single-shot 可跳过多轮，但不能跳过证据诚实性和边界检查。
- **批准 Gate：** 只有存在真实 reviewer/approver 反馈时才能记录批准；模板中的占位符不构成批准证据。

## Open Questions

- frontmatter 给出 `60-120 min`，正文则给出 `1.5-4 days`；两者可能分别表示纯写作与端到端协作，但源文未明确，需要调用方给出计划口径。
- `SKILL.md` 的 Dean's Work 仍是占位符，不能作为真实来源引用。
- `SKILL.md` 与 `template.md` 对部分依赖命名不完全一致，例如 `customer-journey-mapping-workshop` 与 `customer-journey-map`；后续 capability map 需要决定是否为别名、不同 Skill 或来源漂移。
- 源文没有规定默认 PRD 文件名、存储位置、版本控制策略或发布渠道；实际写入前需要调用上下文给出。
- 源文没有统一的 `needs-input`/`blocked` 机器可读输出 schema；本 dossier 根据项目级 fail-closed 约束映射了这些状态，后续 Slot 设计需冻结字段。
- SaaS 示例中的百分比、票据量、日期和客户引语均为示例内容，不能复制为真实项目事实。
- 模板的“故事超过 5-6 个 AC 就考虑拆分”是启发式，不应成为机械数量 Gate；后续提纯需改写为独立可交付/可验收判定。

## Unique Value

该来源的不可替代价值不是“有一个 PRD 模板”，而是把 PRD 变成带内联未知值标记、跨章节 traceability、组件方法路由和最终自诊断的执行契约。`SKILL.md` 提供端到端八阶段编排，`template.md` 在每节内嵌 instructions/steps/contributing skills/activities/transition checks，使模板脱离 workflow 也能自指导；SaaS 正反例说明证据、指标和诚实性，工业例则补上监管硬 Gate、不可逆交付、安全回滚、离线非回归与绝对 guardrail。阻塞 supplement 进一步提供可恢复、可中断、不会重复追问的交互协议。

## Reading Coverage

- `skills/prd-development/SKILL.md` — `read`；完整读取 674 行，覆盖输入、边界、10 节结构、八阶段编排、pitfalls、引用和依赖。
- `skills/prd-development/template.md` — `read`；完整读取 659 行，覆盖文档说明、gap tagging、10 节模板、跨章节检查和 Self-Assessment。
- `skills/prd-development/examples/sample.md` — `read`；完整读取 118 行，覆盖 evidence-backed 正例、inline unknown tagging、自评和 feature-list 反例。
- `skills/prd-development/examples/sample-industrial.md` — `read`；完整读取 124 行，覆盖硬件/监管例外、硬 Gate、rollback、离线非回归和绝对 guardrail。
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/SKILL.md` — `read`；完整读取 100 行，覆盖入口模式、一问一答、进度、决策点、pause/resume 和 fast path。
- `curation/supplements/deanpeters_Product-Manager-Skills/workshop-facilitation/examples/inline-input-flow.md` — `read`；完整读取 80 行，覆盖 invocation context 去重、诚实进度和反例。
