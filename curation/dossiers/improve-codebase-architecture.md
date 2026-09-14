# improve-codebase-architecture 来源能力档案

## Problem

随着软件系统规模持续增长，代码库中极易滋生大量“浅模块”（Shallow Modules）——即接口复杂度几乎与内部实现等宽的胶水层、过度抽象的包装器以及缺乏内聚力（Locality）的薄层。这导致阅读或修改代码时需要在海量小文件间跳跃跳转，大幅降低了系统的可测试性（Testability）与 AI 智能体自主导航理解效率（AI-navigability）。

## When to Use

- **代码库重构与架构深化扫描（主要场景）**：对现有代码库进行整体架构巡检，识别浅模块并提出“深化重构机会”（Deepening Opportunities，将多个浅模块合并为高杠杆、宽实现、小接口的深模块）。
- **改善核心逻辑可测试性**：当现有模块接口难以测试，或为追求可测试性过度抽取了纯函数而导致调用上下文割裂失焦时。
- **提升代码库对 AI 智能体的可读性**：为使未来智能体开发更容易理解系统、更少出现跨文件迷失，需要将碎片化调用链收敛至核心深模块。
- **高频修改热点（Git Hotspots）架构加固**：在近期频繁变更的核心子系统周边进行架构防腐与深模块沉淀。

## When Not to Use

- **早期全新原型冷启动**：业务领域概念尚未稳定成型、尚未产生任何代码摩擦的极简原型阶段。
- **已由有效 ADR 明确锁定的既定决策**：架构决策记录（ADR）已有定论且当前无真实摩擦的场景，严禁无故翻案重议。
- **微小的单函数局部优化**：不涉及跨模块边界与接口深浅的细碎逻辑修整。

## Role

代码库架构深化顾问（Codebase Architecture Deepening Consultant）。精通深模块哲学（A Philosophy of Software Design）、领域驱动建模与系统力学，专注于以极简词汇、视觉化双栏比对报告与苏格拉底式质询（Grilling Loop）推动系统架构精进。

## Inputs

- **目标代码库源码与 Git 提交历史**：用于定位高频变更热点（Hot spots）与浅模块分布。
- **项目领域词汇表（`CONTEXT.md`）**：提供规范的领域语义实体名称。
- **既有架构决策记录（`docs/adr/*.md`）**：提供既定架构决策约束，防止无效争端。
- **人类伙伴指定的探索方向（可选）**：用户明确指出的特定子系统或痛点模块。

## Outputs

1. **单文件自包含 HTML 架构视觉报告**：
   - 存放于操作系统临时目录（`$TMPDIR` 或 `%TEMP%`，命名为 `architecture-review-<timestamp>.html`）。
   - 包含基于 Tailwind CDN 与 Mermaid CDN 的极简无脚本报告，渲染清晰图例。
   - 每个深化候选卡片包含：参与文件列表、一句话痛点（Problem）、一句话方案（Solution）、不超过 6 词的收益要点（Wins，基于 locality/leverage）、推荐强度徽章（Strong / Worth exploring / Speculative）、以及专属的 Before/After 视觉比对图。
   - 顶部核心推荐卡片（Top recommendation）。
2. **领域词表同步沉淀（`CONTEXT.md`）**：在重构深化讨论中产生的新概念实时增补入词表。
3. **架构决策记录（ADR）提案**：当人类伙伴因承重理由否决某项深化建议时，记录正式 ADR 防止未来重复建议。

## Workflow

1. **确定扫描范围（Step 1: Explore - YAGNI 原则）**：
   - 若用户指定了方向：直接采纳并聚焦该子系统。
   - 若未指定：通过 `git log --oneline` 逆向分析近期提交，寻找修改高频的热点区域作为主要突破口。
   - 读取该区域相关的 `CONTEXT.md` 领域词表与现有 ADR 文档。
   - 派发探索子智能体排查五大摩擦信号：
     1. 理解单一概念是否需要在大量小模块间反复跳转？
     2. 哪些模块属于“浅模块”（接口复杂度接近内部实现）？
     3. 是否为追求测试盲目提取纯函数，导致真正 bug 隐藏在无内聚力（no locality）的调用链中？
     4. 紧密耦合的模块是否在缝隙（seams）处泄漏细节？
     5. 哪些代码难以通过当前接口实施有效测试？
   - 对可疑浅模块施加“删除测试”（The Deletion Test）：删除它会凝聚复杂度，还是仅仅转移复杂度？“凝聚复杂度”即为值得深化的信号。
2. **生成并呈现自包含 HTML 报告（Step 2: Present candidates as an HTML report）**：
   - 将完整 HTML 写入系统临时目录，避免污染仓库。
   - 调用系统指令自动为用户打开报告（Windows 上使用 `start <path>`，macOS 使用 `open`，Linux 使用 `xdg-open`），并输出绝对文件路径。
   - 卡片中严格使用 `/codebase-design` 标准架构术语与 `CONTEXT.md` 领域术语。
   - 提供 5 种图表模式（Mermaid 依赖图、手工 div/SVG 深模块图、分层横切面图、接口/实现质量图、调用图折叠）。
   - 报告呈现后向用户提问：“Which of these would you like to explore?”（暂不提出具体接口实现）。
3. **质询与领域建模闭环（Step 3: Grilling loop）**：
   - 用户选择候选方案后，调用 `grilling` 技能与用户推演决策树（约束、依赖、接缝、测试保留）。
   - 调用 `domain-modeling` 技能就地同步更新 `CONTEXT.md`。
   - 若用户因强理由否决，主动建议录入 ADR 以免未来重复建议。
   - 若需探索深化模块的多种接口形态，调用 `codebase-design` 的 design-it-twice 并行子智能体模式。

## Branches

- **用户采纳深化方案**：进入 `grilling` 深入质询，随后转入 `codebase-design` 与 `writing-plans` 编制实施落地方案。
- **用户对深化接口存疑**：派发并行子智能体探索双重接口设计方案（Design-it-twice）。
- **用户否决并给出承重理由（Load-bearing Reason）**：主动发起记录 ADR 流程，固化决策边界。
- **ADR 冲突分支**：若某候选方案违背现有 ADR 但现实摩擦极其显著，在卡片中标注警告呼吁重新评估，否则自动抑制。

## Rules

- **术语绝对一致性铁律**：必须严格使用 7 大核心架构术语（module、interface、depth、seam、adapter、leverage、locality）。严禁替换为 component、service、unit、API、signature、boundary、layer、wrapper。
- **领域词汇对齐**：必须遵循 `CONTEXT.md` 的实体名称（如称呼“Order intake module”，绝不称“Order service”或“FooBarHandler”）。
- **零仓库污染原则**：HTML 审查报告必须写入系统临时目录，严禁提交或写入工作区源码仓库。
- **先视觉后接口原则**：在 HTML 报告呈现阶段仅展示痛点、方案与架构图，绝对不要提前编写具体的代码接口定义。
- **精炼要点原则**：收益清单（Wins）每条不得超过 6 个词，且必须基于 locality 或 leverage 等术语说明实质收益，严禁使用“更容易维护”或“更干净”等无意义套话。

## Exceptions

- 若用户机器缺少图形界面或浏览器环境，可退化为在控制台输出 Markdown 格式的候选卡片与 Mermaid 代码块。

## Dependencies

- **`codebase-design`**：架构基础术语表（module/interface/seam/adapter）与设计范式来源。
- **`grilling`**：审查报告后针对所选候选方案的深度决策推演技能。
- **`domain-modeling`**：同步更新 `CONTEXT.md` 领域词表的配套技能。
- **外部 CDN 资源**：报告依赖 Tailwind CSS CDN 与 Mermaid.js ESM CDN 进行静态渲染。

## Permissions and Side Effects

- **权限要求**：代码只读权限、系统临时文件目录写入权限、系统默认浏览器拉起权限（`start`/`open`/`xdg-open`）、`CONTEXT.md` 与 `docs/adr/` 写权限。
- **副作用**：在临时目录生成静态 HTML 文件，可能拉起用户本地浏览器窗口；在达成共识时就地更新 `CONTEXT.md` 或创建 ADR 文件。

## Gates

- **Gate 1: YAGNI Scoping Gate**：扫描前必须确立明确方向或基于 Git 热点分析界定范围，严禁无目标盲目全盘扫描。
- **Gate 2: Deletion Test Clearance Gate**：候选深化项必须通过删除测试，确信删除浅层包装能够真正凝聚复杂度。
- **Gate 3: Pure-Visual Pre-Interface Gate**：在用户于 HTML 报告中明确选定探索项前，严禁输出具体代码接口实现。

## Open Questions

- 当代码库极为庞大且缺乏 Git 提交历史（如全新导入的压缩包）时，如何高效建立热点与摩擦扫描的替代度量算法？
- 在企业无外网访问环境（无法加载 Tailwind/Mermaid CDN）下，如何优雅支持本地内联的 CSS/SVG 静态降级渲染？

## Unique Value

彻底打破了传统代码异味分析工具“重度依赖静态语法警告却无视系统架构深浅”的局限。通过引入深模块哲学、删除测试、高辨识度自包含 HTML 双栏比对图，以及将架构深化决策无缝衔接至领域建模（CONTEXT.md）与 ADR 固化的闭环，提供了兼具审美质感与高工程密度的系统演进方案。

## Reading Coverage

已对本能力来源全部 2 篇规范文档完成 100% 逐行完整覆盖阅读：
1. `skills/improve-codebase-architecture/SKILL.md`（共 71 行，覆盖深模块定位、术语守则、YAGNI 热点扫描、五大摩擦排查、删除测试、HTML 报告机制、质询循环与 ADR 联动）。
2. `skills/improve-codebase-architecture/HTML-REPORT.md`（共 123 行，覆盖完整 HTML 脚手架、头部图例、卡片结构、五大图表模式、排版美学与严厉禁止的术语替换清单）。
