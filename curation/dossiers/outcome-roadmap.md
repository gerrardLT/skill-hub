# outcome-roadmap Dossier

## Problem

`outcome-roadmap` 将强调 features/projects 的 output-focused roadmap 改写为强调 customer 与 business impact 的 outcome-focused roadmap。来源认为 output roadmap 会制造 false precision，并让团队围绕 features 而非 results 对齐；outcome roadmap 则澄清要解决的 customer problem 和预期 business value，使执行方式更灵活（`skills/outcome-roadmap/SKILL.md:8`、`skills/outcome-roadmap/SKILL.md:12`）。

它的能力边界是“转换已有 initiative 表达并补充战略语境”，不是制定公司战略、验证 customer need、承诺具体 feature、生成完整 delivery plan 或证明示例指标可达。

## When to Use

- 将 feature/project 列表改写为 outcome statements。
- 从 output roadmap 转向 outcome roadmap。
- 希望 roadmap 更清楚表达 strategic intent、customer impact 与 business impact。
- 需要为 initiative 补充可衡量 success metric、dependencies/sequencing 和 flexible release window。
- 不确定某 feature 带来什么 outcome，需要持续追问 “So what?” 直到触达真实 customer/business value。

## When Not to Use

- 没有任何 initiative、roadmap 或可转换对象，却要求凭空生成已验证 roadmap。
- 需要证明 customer problem 或 business metric；本来源要求揭示它们，但不提供 research/validation 方法。
- 需要精确发布日期或 delivery commitment；来源偏好 quarter 等 flexible windows。
- 需要选择唯一 feature solution；来源允许多个 outputs 达成同一 outcome。
- 需要访问未授权、私有或不可搜索的 strategy documents；不得把 “use web search” 当作绕过访问控制的许可。
- 只想保留 feature list 而不讨论影响；这与来源的转换目标不符。

以上反向边界是依据来源目的与副作用约束作出的策展解释；来源没有单独列出 When Not to Use。

## Role

来源显式将执行者描述为 experienced product manager，帮助 `$ARGUMENTS` 从 output-focused roadmap 转向 outcome-focused roadmap（`skills/outcome-roadmap/SKILL.md:10`）。来源没有定义 design、engineering、executive 或 customer research 等其他正式角色。

实际采用时，initiative owner、metric owner、strategy owner 和 dependency owner 可能需要核验转换结果，但这是策展推导的治理 safeguard，不是来源规定的参与者模型。

## Inputs

核心输入是 current roadmap 或其中按 quarter/phase 排列的 initiatives。可选输入包括 strategy documents、company objectives，以及能解释 customer problem、business metric、customer/business impact、alternative path 的上下文。

`$ARGUMENTS` 表示被帮助的用户/上下文占位符，不是默认公司名或事实。来源没有规定 roadmap 格式、initiative 数量、指标 baseline、目标值、数据来源或文档访问方式；缺失时必须保持未知或追问，不能借用示例数字。

## Outputs

- 按 quarter/phase 列出的 original initiatives。
- 每项 initiative 的 outcome statement，格式为 `Enable [customer segment] to [desired customer outcome] so that [business impact]`。
- 表示成功的 key metrics。
- dependencies 或 sequencing notes。
- overall roadmap 的 strategy alignment、customer-need assumptions 与 flexible release windows。
- 结果 substantial 时保存为 `Outcome-Roadmap-[year].md`。

这些是来源声明的输出结构；文件写入是条件性 side effect。实际写入前检查权限是策展 safeguard，不是来源原文，不能仅因能生成内容就视为已获授权。

## Workflow

1. 若用户提供 current roadmap，仔细读取；若提及 strategy documents 或 company objectives，来源要求通过 web search 理解 broader goals。网络访问与可见性需先满足环境授权，这是策展权限 safeguard，不是来源原文。
2. 对每项 initiative 追问目标 outcome、customer problem、将改善的 business metric、customer/business impact，以及是否存在更好的替代实现。
3. 识别 planned feature/project 这一 output。
4. 揭示为什么构建、对 customer 或 business 会发生什么变化这一 outcome。
5. 使用来源句式将 initiative 改写为 outcome statement：`Enable [customer segment] to [desired customer outcome] so that [business impact]`。
6. 按 quarter/phase 同时呈现 original initiative、outcome statement、key metric 和 dependency/sequencing note。
7. 为整体 roadmap 增加 company-strategy alignment、customer-need assumptions 和 quarter-level flexible windows。
8. 若结果 substantial，则按来源要求保存为 `Outcome-Roadmap-[year].md`。

## Branches

- 已提供 roadmap：仔细读取并逐 initiative 转换。
- 提及 strategy documents/company objectives：条件性 web search 以理解 broader goals；私有或未授权内容不得访问。
- outcome 明确：直接按模板改写并配置 metric。
- outcome 不明确：重复追问 “So what?”，直到触达 real customer/business value；仍无证据时保留未知。
- 一个 outcome 可由多个 outputs 达成：避免把当前 feature 写成唯一实现。
- 输出 substantial：保存 markdown；不 substantial 时来源不强制落盘。
- 时间表达：使用 quarters/flexible release windows，而不是 specific dates。

## Rules

- 从 features/projects 的 output 表达转向 customer 与 business impact 的 outcome 表达。
- 每个 outcome 应 testable、measurable。
- outcome statement 同时包含 customer segment、desired customer outcome 和 business impact。
- 多个 outputs 可以实现一个 outcome；roadmap 不锁死 feature list。
- 保持 flexible execution，避免 specific-date false precision。
- 示例中的 Q2、50%、20%、80% 等只说明改写形式，不是默认 target、baseline 或通用门槛。
- 外部 Further Reading 本轮未访问，不能将链接标题当作已核验方法内容。

## Exceptions

来源原文只规定 strategy-context 分支触发 web search、substantial 分支保存 markdown；以下访问控制、失败降级和写入前检查是策展 safeguards，不是来源原文：

- web search 不等于允许访问私有文档、认证内容或任何未授权网络资源；无法访问时让用户提供上下文或标记 alignment 未核验。
- “Save the Output” 只在 substantial 时触发；`[year]` 需要在保存时替换，但来源未定义采用当前年份、roadmap 年份或其他年份口径。
- metric 未给 baseline、target 或数据源时，可输出待定义 metric 字段，但不能伪造可衡量性证据。
- 一个 initiative 可能映射到多个 outcomes，多个 initiatives 也可能映射到一个 outcome；来源未规定拆并规则，应显式记录转换判断。
- 来源示例把 feature 与结果放在同一句中，不代表 feature 已经验证或必然导致该结果。

## Dependencies

当前来源目录只有 `SKILL.md`，没有本地 template、reference、example 或 script 文件。来源没有声明其他本地 Skill dependency。

`SKILL.md:66-68` 提供 Product Compass 的三个 HTTPS Further Reading 链接，分别涉及 vision/strategy/objectives/roadmap、OKRs 和 business/product/customer outcomes；本轮未联网读取，它们不是本地 reachable attachments。实际 web search 与 markdown 文件写入依赖运行环境工具和授权，而不是本地 Skill dependency。

## Permissions and Side Effects

本轮 Phase 3 策展只读取 `skills/outcome-roadmap/SKILL.md`，并写对应 dossier、units 与 coverage；没有修改 `skills/`、访问外链、执行 web search、读取私有战略文档或创建实际 `Outcome-Roadmap-[year].md`。

未来执行包含两个来源显式声明的副作用：在 strategy context 分支发起 web search，以及 substantial-output 分支写 markdown 文件。前者可能产生网络访问与外部信息处理，后者会修改文件系统。遵循当次环境权限、目标路径和用户授权是策展权限 safeguard，不是来源原文。roadmap 转换还可能影响战略沟通，但来源没有授予发布或 commitment 权限。

## Gates

来源没有声明 formal Gates；以下是为保持其边界而策展推导的检查点，不是来源原文：

- Input Gate：是否存在可读取的 current roadmap/initiative；没有时不得声称完成转换。
- Outcome Gate：每项改写是否能回答 customer problem、customer impact 与 business impact；不确定时使用 “So what?” 或保留未知。
- Measurability Gate：outcome 是否有可检验 metric；没有数据时只记录待定义项。
- Flexibility Gate：是否允许 alternative outputs，并避免 specific-date false precision。
- Permission Gate：web search 与文件保存是否满足当次网络、文档访问和写入授权。
- Phase 3 策展 Gate：dossier 恰有 16 个规定 H2；units 字段、类型、状态、路径和逐字 excerpt 合同通过；coverage 登记唯一 reachable source file。

## Open Questions

- current roadmap 缺失时是先追问、停止，还是允许 best-effort 草拟，来源没有定义。
- company strategy 与 objectives 的权威来源、访问权限、冲突处理和 freshness 没有定义。
- outcome metric 的 baseline、target、time horizon、owner、instrumentation 和 counter-metric 没有定义。
- initiative 到 outcome 的一对多/多对一拆并规则没有定义。
- dependencies/sequencing 的分析方法和资源/capacity 约束没有定义。
- “substantial” 的阈值、保存目录、覆盖策略和年份选择没有定义。
- 三个 Further Reading 链接的当前内容和可用性未联网核验。

## Unique Value

该来源的独特价值是提供一条紧凑的 output-to-outcome 转换链：从 planned feature/project 出发，连续追问 customer problem、business metric 和 impact，再用包含 segment、customer outcome、business impact 的固定句式改写，同时保留 original initiative 便于对照。它不是删除 delivery 信息，而是把 feature 从目的降为可能手段。

它还把可衡量 outcome、alternative outputs、quarter-level flexibility、strategy alignment、assumptions 与 sequencing 放进同一 roadmap 表达中，从而减少 feature commitment 和 date precision 对战略意图的遮蔽。

## Reading Coverage

- `skills/outcome-roadmap/SKILL.md` — `read`；frontmatter、Purpose、Context、七步 Instructions、example、Notes 与 Further Reading 已完整读取。
- `skills/outcome-roadmap/references/` — `excluded`；来源快照中不存在该目录。
- `skills/outcome-roadmap/reference/` — `excluded`；来源快照中不存在该目录。
- `skills/outcome-roadmap/templates/` — `excluded`；来源只有 inline outcome statement 格式，没有本地模板目录。
- `skills/outcome-roadmap/examples/` — `excluded`；示例内嵌于 `SKILL.md`，不存在本地目录。
- `skills/outcome-roadmap/scripts/` — `excluded`；来源快照中不存在该目录，未执行任何脚本。
- `SKILL.md:66-68` 的三个 Further Reading URLs — `excluded`；外部链接未访问，非本地 reachable files。
