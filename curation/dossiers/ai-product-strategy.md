# ai-product-strategy Dossier

> 本文件针对纳入范围的顶层 Skill `ai-product-strategy`。事实判断仅来自 `skills/ai-product-strategy/` 原始快照；分析判断与项目级状态映射明确标注。来源中的公司、产品、数字、日期和引语仅作为来源示例或观点证据，不作为当前项目事实。

## Problem

`ai-product-strategy` 解决的是：团队如何从真实用户问题中选择适合 AI 的高价值切入点，在技术可行性和输出质量均不确定的条件下设计产品，并通过受控自治、持续评估、数据学习循环和垂直工作流形成长期价值。它反对从“必须加 AI”出发，也反对把确定性软件的发布、测试和 UI 假设原样套到概率系统。

分析判断：该来源不是单一可直接执行的端到端工作流，而是一个由入口原则、95 个 artifacts 汇编和 69 条 guest insights 组成的策略知识库。实际使用时必须选择与当前问题直接相关的框架，不能把所有材料机械串联。

## When to Use

- 评估一个产品问题或人工工作流是否值得用 AI 解决，尤其是高频、高摩擦、回报明显且会重复发生的工作。
- 选择 AI 初始 wedge、判断 augment 还是 replace、评估 desirability、business viability 与 research/technical feasibility。
- 决定使用现成模型、自建能力、RAG、fine-tuning、prompting 或多模型编排时。
- 设计概率输出 UX、失败恢复、人类接管、自治升级、日志、评估和持续校准机制时。
- 评估 AI 产品差异化是否来自合法专有数据、深度垂直工作流、界面与持续学习，而不是暂时的模型缺陷。
- 制定面向模型能力改善的路线图，同时识别临时 scaffolding 的淘汰风险。

## When Not to Use

- 没有明确用户问题、痛点或人工任务，只因技术潮流想添加通用 AI 功能。
- 任务可由确定性规则以更低风险、更低成本、更高可解释性完成，却没有证据表明 AI 带来更好结果。
- 需要具体实现、模型训练、红队、安全审计、AI eval 执行或 AI-native UX 设计的完整操作手册；入口只把 `Ai Evals` 和 `Ai Native Ux` 列为相关能力，未提供其内容。
- 需要从外部链接核实案例、数字、当前模型能力或法律许可；本 snapshot 是汇编材料，本轮未联网验证。
- 高风险 agent action 缺少权限隔离、人类监督、回退和安全验证时；不能从策略建议直接授权真实外部动作。

## Role

- **主要执行者：** 产品负责人/PM 负责定义用户问题、目标、wedge、价值标准、自治边界、数据与学习策略，并与研究、工程和设计共同作出取舍。
- **研究与工程：** 验证当前技术/研究可行性、数据要求、模型与架构选择、延迟/成本、日志、eval 和安全机制；与 PM 共同落实算法目标、学习参数、数据/fine-tuning 和基础设施变化。
- **PM 的 AI 责任：** 直接定义算法目标，识别用于学习的 features/parameters，制定数据收集与 fine-tuning 策略，并判断哪些基础设施变化可能解锁产品结果；不把这些判断完全委托给工程。
- **设计：** 负责概率输出的可理解性、起点、编辑、反馈、接管和 workflow interface，而非只包装聊天框。
- **领域专家和运营者：** 提供正确示例、rubric、修订信号与高风险判断，尤其在医疗、法律、财务或 mission-critical 流程中。
- **用户/审批者：** 对 desirability、信任和真实结果提供证据；自治、生产动作和高风险权限升级必须由有权者批准。

## Inputs

- 必填：待解决的用户问题或人工 workflow、目标用户、现有做法与摩擦、预期结果。
- 机会评估输入：频率、用户投入、潜在回报、重复使用、业务价值、非 AI 替代方案、研究/工程可行性。
- 架构输入：是否需要实时/内部/专门信息，是否需要稳定的特定行为，已有/相邻数据、许可状态、延迟和成本约束。
- 安全与自治输入：动作影响、可逆性、允许权限、人类接管点、失败模式、真实世界噪声下的行为信号。
- 学习循环输入：reference examples、ground truth、eval 指标、日志、用户接受/拒绝/编辑、fallback 与 reroute 信号。
- 防御性输入：领域知识、合法专有或独特结构化数据、workflow integration、distribution/interface 优势。
- Prompt/RAG 输入：任务问题、目标模型、必要 context、代表性示例、输出格式、检索语料、已观察的检索/回答失败和评测集。
- 组织采用输入：高层 sponsor、内部技术邻近采用者、可试点的 repeatable process、内部 proof point、失败最大损失、rollback 和可观察价值证据。
- 信息不足时，项目级映射为 `needs-input`；来源没有统一机器可读输入 schema，不得用案例数字或模板示例补齐。

## Outputs

- AI opportunity/wedge 判断：目标 workflow、价值理由、是否应使用 AI、首个最小切片。
- architecture/sourcing decision：build、best-in-class partner、developer ecosystem、RAG、fine-tuning、prompting 与 ensemble 的条件性建议及证据缺口。
- augment/replace decision：AI 增强或完全执行核心功能的分类、价值理由，以及独立的风险和 fallback 状态。
- agency ladder：每版 capability、agency/control、数据收集、eval、handoff 和 graduation criteria。
- probabilistic UX 与 failure plan：不确定输出的呈现、编辑、fallback、guardrail、权限和人工接管。
- CC/CD 计划：reference dataset、logging、eval、small-cohort deploy、error-pattern review、targeted fixes 和 repeat loop。
- defensibility thesis：licensed proprietary data、crafted vertical workflow、interface/product craft、learning/stickiness flywheel。
- model-curve roadmap：会随基础模型改善而增强的产品假设、临时 scaffolding 及复核点。
- prompt/RAG plan：按任务选择的方法、prompt 结构、代表性示例、自动评测，以及由检索失败驱动的语料准备步骤。
- adoption/buy-in plan：内部 proof point、sponsor、tiger team、bottom-up adoption、可观察价值、maximum downside、rollback 和研究商业化路径。
- 项目级状态分析：`passed`、`failed`、`needs-input`、`blocked`；这些状态并非来源自带输出格式。

## Workflow

1. **回到问题。** 描述真实痛点、现有人工步骤和 non-AI alternatives，拒绝 shiny-object 起点。
2. **扫描既有产品。** 对每个已发布产品询问能否 made smarter，区分持续机会扫描与首次 AI 集成判断。
3. **选择 wedge。** 优先高频 chore、合理尝试成本、高 promise-to-payoff 和 repeat use；先缩到最小可观察任务。
4. **验证三类可行性。** 同时检查用户 desirability、业务 viability 和 AI research/technical feasibility；AI-native 场景先原型验证“能否做、是否够好”。
5. **选择 sourcing/architecture。** 有数据优势的能力可 build，commodity 能力可选择 best-in-class partner，niche use case 可借助 developer ecosystem；实时/内部/专门知识偏向 RAG，特定稳定行为可考虑 fine-tuning，并可按成本、速度、推理拆给不同模型。
6. **确定 augment 或 replace。** 回到产品核心 premise，判断 AI 是增强人类工作还是完全执行核心功能；该产品策略分类不替代自治、风险和 fallback Gate。
7. **设计 prompt 与检索输入。** 按任务问题选择 prompting 方法，明确 role/context/examples/directive/output format；RAG 语料准备可用于初始建设或后续优化，并用 retrieval/answer eval 验证，而不是机械执行技巧清单。
8. **设计概率 UX。** 假设输出会错，提供起点、可编辑结果、反馈和透明 handoff；指标聚焦工作结果、接受率与用户是否更轻松，而非单纯 time-in-app。
9. **定义 agency v1。** 从低影响、高控制、建议/草稿类能力开始；物理限制权限并降低错误 downside。
10. **建立 CD 基础。** 为 scoped task 整理 reference examples，做最简应用，记录输入/输出/交互，设计 control handoff、guardrails 和 task-specific evals。
11. **小范围部署并校准。** 向 small cohort 发布，基于 live signals 抽样，人工检查弱项和错误模式，实施针对性修复并重跑 eval。
12. **以证据升级自治。** 只有真实噪声下的可靠行为和明确 graduation criteria 满足时才提高 agency、降低 control；每次循环重新评估权限与后果。
13. **建立组织采用条件。** 用内部相邻 proof point、maximum downside 和 rollback 争取 sponsor；由技术邻近的 tiger team 在 repeatable process 试点，以可观察价值连接 top-down support 与 bottom-up adoption。
14. **建设防御性。** 把使用产生的合法数据、用户修订、团队 workflow 与产品 craft 变成复利，而不是把临时模型 workaround 当 moat。
15. **面向能力曲线复核路线图。** 标记基础模型可能吸收的 scaffolding；允许已知临时补偿，但不能让它成为唯一差异化。

## Branches

- **AI vs non-AI：** AI 不能明显优于规则/人工方案，或无真实问题时停止 AI 路径。
- **Prototype-first：** 当 AI feasibility 不确定时先验证技术可能性和输出质量；若只是争取 buy-in，可先做体验 prototype/demo，不声称模型已实现。
- **Build / partner / ecosystem：** 有独特数据优势的能力可自建；commodity 能力选择 best-in-class partner；niche capability 可借助 developer ecosystem。选择依据必须可审计，不能把来源公司示例当默认供应商。
- **RAG / fine-tuning / prompting：** live/internal knowledge 选择 runtime retrieval；特定行为选择 fine-tuning；prompting 是较低成本起点，复杂度按证据升级。
- **Augment / replace：** 根据产品核心 premise 判断 AI 是部分增强还是完全执行核心功能；高风险或低置信任务仍从 recommendation/draft 起步，只有已证明能力和安全 fallback 的 scoped work 才自动执行。
- **Open-ended / repeatable process：** 创造性知识工作容忍探索；SOP/运营流程要求更高 determinism、数据集成和边界控制。
- **Current-model / future-model：** 可构建可替换的临时补偿，但长期 differentiator 必须随模型改善仍成立。
- **Low-frequency / high-frequency cost：** 先让产品有效；只有频繁运行且成本显著时再通过更便宜模型或减少 context 优化。
- **Product prompt / interactive chat：** 产品 prompt 需用多样输入自动测试，示例提供指导逻辑的说明；常见格式负责区分指令、上下文和示例，不能代替质量评估。
- **Reasoning / standard models：** 来源建议比较模型类型与显式分步提示的效果；具体模型名仅作历史示例，不要求披露隐藏推理。
- **Coding flow / onboarding：** 编码建议需结合低延迟、附近代码上下文和多行建议；用户引导则按 persona 和情境减少学习摩擦，不能混为同一种 UX 方法。
- **Redesign / organizational convergence：** 回到原始目标重新设计解法，与组织先广泛实验再集中人才投入，是两个独立决策；均不授权删除现有代码或实际部署。
- **Future experiments / current capability：** 持续数小时的多步任务与原生音视频体验属于路线实验假设，必须与当前实测能力区分。
- **Prompt technique selection：** role/style/few-shot/synthetic bootstrap/CoT/RAG/judge 等按问题选用；来源一处推荐谨慎使用 emotion prompting，另一处认为现代模型不需要情绪操纵，必须以目标任务消融评测解决冲突。
- **Prompt context mode：** 对话模式可提供较多 context；产品模式需权衡成本和延迟，只保留必要输入。
- **RAG preparation：** chunk、metadata/summary、hypothetical questions、Q&A rewrite 与 AI-oriented annotation 都是初始建设或后续优化的候选处理；按语料和检索理由选择，并通过评测验证，不机械全做。
- **Leadership / enterprise adoption：** buy-in 材料负责 proof point、商业价值、maximum downside 与 rollback；企业采用另需 sponsor、内部 evangelists/tiger team 和 bottom-up adoption，不能互相替代。

## Rules

- 从 problem 和 workflow 开始，不从 AI technology 或 demo 开始。
- 不把 probabilistic output 当成 100% 正确；必须定义“good enough”、eval、编辑/反馈和 failure handling。
- 数据质量、时效和许可是产品边界；“能抓取”不等于有权使用。
- agent 权限与 agency 必须渐进；涉及金钱、基础设施、个人或高后果系统必须保留严格 human oversight。
- 安全测试同时区分外部 prompt injection 和 internal misalignment；监测 agent 为目标得分作弊、忽略规则或自主升级危害。
- 自治升级靠真实行为信号和 graduation criteria，不靠版本日程或信心；未解决的规则规避会阻断升级。
- 保持接近原始客户信号；AI 可遍历、聚类和清理，但不能用无来源总结替代 direct quote/link。
- 评价工作结果而不只评价 engagement；高效 AI 可能减少 time-in-app。
- 避免过度 scaffolding；临时 workaround 必须标记为可淘汰，不能冒充持久 moat。
- 差异化优先来自合法专有数据、垂直 workflow、interface/product craft 与累积学习。
- 例子、benchmark、公司结果和预测只是来源材料，不得直接写成调用项目事实或 Gate 阈值。

## Exceptions

- “先从问题出发”与 AI-native prototype-first 不冲突：前者防止无痛点加 AI，后者承认 feasibility 不能像传统软件一样预设；需要并行验证 problem value 与 technological possibility。
- “使用通用模型、少做 scaffolding”不是禁止 fine-tuning/custom model；当特定 magic moment 遇到现成模型 ceiling 且有数据优势时可升级。
- “快速发布”仅适用于可控 downside 和 small cohort；mission-critical automation、安全与合规不能以速度绕过 robustness、expert data 和 human oversight。
- “迭代部署”不等于允许未经授权的生产实验；来源未授予网络、生产或数据访问权限。
- 入口写 26 guests/45 insights，而附件写 34 sources/69 insights 和 95 artifacts；这些计数口径冲突，不能据此宣称完整或精确来源规模。

## Dependencies

- 已完整读取：`skills/ai-product-strategy/SKILL.md`、`skills/ai-product-strategy/references/artifacts.md`、`skills/ai-product-strategy/references/guest-insights.md`。
- inventory 将 root 标为 `included`/`resolved`，3 files，snapshot SHA-256 为 `96a9b6550223c9002804fc02c401c9f408048ccde8e18319e309d80e02056869`。
- `curation/reference-review.json` 没有该来源的 missing-relative-reference 分类；`curation/dependency-scan.json` 标记 `requires_review: false` 且无 CLI/MCP/network/credential signals。
- 没有该来源所需的 validated supplement，也没有 blocking supplement；目录存在不被解释为依赖已运行验证。
- 入口相关能力 `Ai Evals`、`Ai Native Ux` 只有名称，未提供路径或内容，属于未验证的下游/互补依赖。
- artifacts 中出现外部文章、视频、工具与产品 URL，只是参考材料；本轮未联网核实、未调用工具。

## Permissions and Side Effects

- 本来源本身主要生成策略、架构、路线图和评估建议，不包含必须执行的本地脚本。
- 若实际进行 prototype、logging、live-data RAG、small-cohort deployment、A/B test、agent action、数据采集或模型训练，会产生代码/数据写入、网络调用、推理成本、隐私/许可和生产影响；每项需独立授权。
- real-world actions 必须最小权限，并优先 recommendation、draft、append 或可回退操作；高风险动作保留人工批准。
- 不得把来源中的“访问 web、CRM、Slack、GitHub、Linear”等 agent 行为描述视为当前授权。
- 本轮仅修改指定 curation 产物；未执行 `skills/` 脚本、未联网、未安装依赖、未访问凭据或生产。

## Gates

- **passed（项目级映射）：** 有证据支持的用户问题和 wedge；AI 相对替代方案的价值成立；架构选择与数据/行为需求匹配；概率 UX、eval、logging、handoff 和 guardrail 明确；自治级别与真实证据匹配；数据许可和 defensibility 假设可审计。
- **needs-input：** 缺问题证据、workflow、数据来源/许可、ground truth、eval 定义、成本/延迟、权限或失败后果；保留未知并索取最小必要输入。
- **blocked：** 高风险动作无人工监督/权限隔离/回退；数据无合法使用依据；关键安全或合规边界未知；不能安全建立 ground truth/eval 却要求自动执行；发现目标作弊、忽略规则或自主升级危害但尚未解决。
- **failed：** generic bolt-on AI；假设 100% accuracy；用 demo/公司案例代替用户价值证据；只优化 prompt/model 而忽略数据和 workflow；直接跳到高 agency；用当前模型缺陷作为唯一 moat；把来源示例数字当项目事实。
- **graduation gate：** 每次提高 agency 前必须看到足够真实行为信号、已知弱项、可接受 eval、有效 handoff/fallback 和与新增权限匹配的 guardrail。

## Open Questions

- 入口的 “26 guests / 45 insights” 与附件的 “34 sources / 69 insights / 95 artifacts” 不一致；可能是生成版本或计数口径漂移，snapshot 未解释。
- `guest-insights.md` 中 Cam Adams、Dharmesh Shah、Peter Deng 及一条 glossary insight 为空，不能从标题推断其含义。
- 入口称在 live data 与 specific behavior 间选择 RAG/fine-tuning，但附件同时强调 prompting、off-the-shelf、ensemble 和 custom model；实际 architecture decision 需要更完整条件矩阵。
- “build for 12–18 months / 1–2 years / 6 months / 2 months”是多位来源观点，不是可靠 roadmap 时间承诺；当前能力和发布日期需另行核实。
- 来源没有统一风险等级、minimum eval threshold、dataset size、cost budget、privacy checklist 或机器可读输出 schema。
- `Ai Evals` 和 `Ai Native Ux` 未解析到本来源附件；后续 capability map 应判断实际 skill identity 和接口。
- 多个案例和 benchmark 未在本轮联网验证，不能作为当前决策的事实依据。
- ASL 段落把 ASL-3 标为 current state，却没有提供时点或完整现行标准；对应 unit-038 保留历史引文并 `defer`，不用于当前模型评级或部署许可。
- 平台风险被夸大、模型与界面贡献 50/50、基础设施价值转移等均为受访者观点；不作为风险豁免、资源比例配额或无条件转型指令。

## Unique Value

该来源的独特价值是把 AI 产品策略的多个常被割裂的决策连成一条证据链：从 problem-first wedge 和 prototype-first feasibility，到 RAG/fine-tuning/build-buy 条件、概率 UX、agency-control ladder、CC/CD 真实数据校准，再到 licensed data、vertical workflow、interface craft 和 model-curve defensibility。尤其有价值的是它同时保留两组张力：既不要 shiny-object AI，也不能假设传统 design-first 的技术可行性；既应利用未来模型改善，也必须用当下的 guardrail、eval 和 human handoff 控制真实风险。

## Reading Coverage

- `skills/ai-product-strategy/SKILL.md` — `read`；完整读取 89 个物理行（末尾含换行；`wc -l` 为 88），覆盖入口目的、四步帮助法、六项原则、框架索引、引导问题、常见错误和相关能力。
- `skills/ai-product-strategy/references/artifacts.md` — `read`；完整读取 800 个物理行（`wc -l` 为 799），覆盖 95 artifacts 汇编中的 frameworks、templates、checklists、examples 和 tools；外部 URL 仅作为快照文本阅读，未访问。
- `skills/ai-product-strategy/references/guest-insights.md` — `read`；完整读取 873 个物理行（`wc -l` 为 872），覆盖文件所列 34 sources、69 insights、tactical advice、引语和空缺条目；未联网核实外部来源。
- `reachable_skill_files` 结果与上述 3 个文件完全一致；无二进制、生成物、scripts、templates、examples 或其他可达文件需要排除。
