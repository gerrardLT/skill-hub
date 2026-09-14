# writing-plans Dossier

## Problem
在软件开发中，如果仅凭高层需求规格就仓促动手编写代码，工程师（或子代理 Agent）极易因缺乏全局上下文、边界认知模糊或技术选型偏差而陷入反复返工、遗漏测试、破坏既有架构或产生大面积破坏性修改。缺乏可操作细粒度分解的粗糙规划往往伴随着大量含糊不清的占位符（如“TODO/TBD/完善错误处理”），导致具体执行阶段卡死或产出质量参差不齐。

## When to Use
1. 当已具备明确的需求规格说明（Spec）或 PRD，且需要执行跨多个文件、模块的多步骤复杂实现时。
2. 在正式编写生产代码（Touching Code）前，建立严格可执行、自包含且零歧义的端到端实施计划。
3. 遵循测试驱动开发（TDD）与红绿重构周期，规划每个组件的失败测试用例、最小实现代码与验证命令时。
4. 准备将实施计划交由子代理驱动开发（`subagent-driven-development`）或行内执行引擎（`executing-plans`）时。

## When Not to Use
1. 需求尚不明确、仍处于前置头脑风暴或方案探索阶段（应路由至 `superpowers:brainstorming`）。
2. 单一简单文件、轻微单点重构或少于 3 个微小步骤的微型变更。
3. 纯代码审查阶段（应路由至 `requesting-code-review` 或 `receiving-code-review`）。
4. 已经处于执行实施阶段（应路由至 `executing-plans` 或 `subagent-driven-development`）。

## Role
首席架构师与资深规划工程顾问（Staff Software Architect & Planning Lead），假定执行工程师拥有扎实的通用编程能力，但对本地代码库零上下文且对测试设计缺乏经验；以“零占位符、细粒度任务、严格 TDD、明确文件坐标与逐字代码”为准则，制定确定性交付方案。

## Inputs
1. **Requirements / System Spec / 需求规格**：经过前期头脑风暴或 PRD 确认的高层功能规格与验收条件。
2. **Repository Baseline / 代码库基线**：现有模块边界、目录结构、测试框架及依赖定义。
3. **Workspace Context / 执行上下文**：是否处于隔离的 Git Worktree 中。

## Outputs
1. **Implementation Plan Document / 实施计划文档**：
   - 默认落盘至：`docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`。
   - 包含标准文档头：`Goal`, `Architecture`, `Tech Stack` 及子代理执行指引。
   - 包含 N 个细粒度组件任务（Task N），每个任务严格包含确切文件路径、Step 1（写失败测试）、Step 2（运行验证失败）、Step 3（写最小实现）、Step 4（运行验证通过）、Step 5（独立提交）。
2. **Review Checklist / 自审与评审模板产物**：
   - 规格覆盖核查、占位符扫描与类型一致性自检记录；
   - 可选子代理审查提示词：`plan-document-reviewer-prompt.md` 派发执行结果。

## Workflow
1. **Announce Skill / 声明介入**：
   - 在启动时明确声明："I'm using the writing-plans skill to create the implementation plan."。
2. **Scope Check / 范围核验**：
   - 检查规格是否横跨多个独立子系统；若涉及多个子系统，建议拆分为独立的子计划，确保每个计划能独立产出可测试的可用软件。
3. **File Structure Mapping / 文件结构与职责映射**：
   - 映射将新建或修改的文件及各自单一职责；
   - 坚持“共同变化的文件放在一起，按职责拆分而非技术层拆分”原则；
   - 遵循既有代码库模式，保持单个文件聚焦。
4. **Bite-Sized Task Decomposition / 细粒度任务分解**：
   - 将任务拆解为 2-5 分钟即可完成的极小颗粒度步骤；
   - 每个任务严格遵循 TDD 红绿循环（红测试 -> 验红 -> 写实现 -> 验绿 -> 提交代码）。
5. **Enforce "No Placeholders" Contract / 绝对零占位符铁律**：
   - 严禁任何 "TODO", "TBD", "implement later", "add validation", "similar to Task N" 等含糊托辞；
   - 每一步必须提供完整的、字面可用的真实代码块，不留任何空白让执行者猜测。
6. **Self-Review Checklist / 规划自审自查**：
   - 核验需求覆盖（每项需求均有对应任务承接）；
   - 扫描占位符特征；
   - 检查跨任务的类型名称、方法签名与属性定义一致性。
7. **Execution Handoff / 执行交接**：
   - 提示计划已落盘，并提供执行选项选择：Subagent-Driven（推荐，路由至 `subagent-driven-development`）或 Inline Execution（路由至 `executing-plans`）。

## Branches
- **Branch A: Subagent-Driven Execution / 子代理驱动分支（推荐）**：计划批准后，每个 Task 派发全新的上下文隔离子代理，并在任务间实施两阶段审查与快速迭代。
- **Branch B: Inline Execution / 会话内批量执行分支**：在当前会话中通过 `executing-plans` 执行批处理并在设定检查点进行人工复核。

## Rules
1. **零上下文假设法则**：假定执行工程师对代码库完全陌生且品味不可测，所有信息（文件路径、代码、依赖、测试命令、预期输出）必须完整写出。
2. **零占位符铁律（No Placeholders）**：严禁出现任何 "TODO", "TBD", "后续实现", "添加适当错误处理", "参考任务 N"；缺少完整代码块即判定为规划失败（Plan Failure）。
3. **严格 TDD 颗粒度（Bite-Sized TDD）**：每个步骤必须分解为 2–5 分钟的微操作：写失败测试 -> 验证失败 -> 写通过代码 -> 验证通过 -> 细粒度原子提交。
4. **确切文件与行号定位**：明确指定 `Create: exact/path`、`Modify: exact/path:line_start-line_end`、`Test: tests/exact/path`。
5. **按职责拆分文件**：单一文件单一职责，共同修改的文件归置一处，避免过度按技术分层导致改动发散。
6. **工程准则遵从**：严格贯彻 DRY（不重复）、YAGNI（不过度设计）、TDD（测试驱动）、Frequent Commits（高频提交）。

## Exceptions
1. **用户显式路径覆盖**：若用户在指令或配置中指定了替代的计划保存路径，优先遵循用户指定路径覆盖默认的 `docs/superpowers/plans/`。
2. **既有大型遗留文件惯例**：若目标代码库普遍采用大型单文件组织且暂不适宜全量重构，方案应优先保持模式一致，仅在改动范围确有必要时安排局部分离。

## Dependencies
- `superpowers:using-git-worktrees`：提供隔离工作树环境。
- `superpowers:subagent-driven-development`：子代理驱动执行实施的承接技能。
- `superpowers:executing-plans`：行内批量执行实施的承接技能。
- 语言相关测试运行器（如 `pytest`, `vitest` 等）。

## Permissions and Side Effects
- **只读操作**：阅读代码库现有文件结构、测试配置、需求规格文档。
- **写文件**：在 `docs/superpowers/plans/` 路径下持久化写入完整的 Markdown 计划文件。
- **无破坏性修改**：在计划阶段绝对不修改任何生产业务逻辑代码或执行 git 提交。

## Gates
- **G-Scope-Boundary**：确认规格是否应拆分为多个子项目计划。
- **G-Document-Header**：计划文件必须以包含 Goal, Architecture, Tech Stack 的标准头部开启。
- **G-No-Placeholders**：自审通过绝对零占位符检查（无 TODO/TBD/含糊描述，全真实代码块）。
- **G-TDD-Steps-Complete**：每个任务必须严格包含写红测试、验红、写绿实现、验绿、提交 5 步闭环。
- **G-Handoff-Selection**：计划生成完成后必须由用户明确选择执行流分支（Subagent-driven vs Inline）。

## Open Questions
1. 针对前端复杂可视化交互或动画组件，如何在计划的 Step 1–4 中提供轻量且确定性的自动化测试验证脚本？
2. 在大规模多仓库微服务依赖变动中，如何让单份计划在维持 Bite-Sized 的同时兼顾跨仓协调？

## Unique Value
将软件架构规划提升到完全可程序化、确定性推演的高度；通过“假定执行者零上下文”的极致详尽度与“绝对零占位符、强内联代码、强 TDD 颗粒度”标准，消除了从高层需求到代码落地之间的所有语义漂移与理解黑洞。

## Reading Coverage
- `skills/writing-plans/SKILL.md`: lines 1-153 (全部 153 行，包含定位、范围检查、文件结构、极小颗粒度分解、标准头部、任务结构、零占位符准则、自审清单与交接分支)
- `skills/writing-plans/plan-document-reviewer-prompt.md`: lines 1-50 (全部 50 行，包含子代理评审员提示词模板、完整度/对齐度/分解/可构建性四维检查标准与校准输出格式)
- 覆盖率：100% (2/2 文件全部覆盖，无遗漏)
