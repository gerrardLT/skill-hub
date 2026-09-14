# requesting-code-review 来源能力档案

## Problem

在多智能体协同或快速迭代的代码开发过程中，主控智能体容易受制于自身的会话上下文与思维定势（confirmation bias），对自身实现中的架构缺陷、边界遗漏、类型风险及与原始规划的偏离产生盲区。若缺乏独立的闭环审查机制，微小缺陷将在后续任务中持续级联放大，导致返工成本剧增甚至破坏生产环境稳定性。

## When to Use

- **子任务完成后（强制）**：在子智能体驱动开发（Subagent-Driven Development）流程中，每个独立子任务（Task）代码编写完成后必须立即触发审查。
- **重大功能开发完毕（强制）**：在实现核心系统功能、大规模重构或模块落地后必须执行审查。
- **代码合并至主干前（强制）**：任何分支准备合并至 main/master 前必须执行严苛的全量差异审查。
- **任务遇阻或思维停滞（可选）**：当开发智能体在特定技术难点陷入僵局时，派发独立审查获取全局外部视角。
- **重构前基线核对（可选）**：在对遗留或复杂代码发起重构前，验证当前基线逻辑与测试的有效性。
- **复杂缺陷修复后（可选）**：在修复多组件耦合或复现路径复杂的 bug 后，验证修复是否存在副作用。

## When Not to Use

- **纯规划构思阶段**：尚未产生任何代码改动或 git commit/diff 时，不应派发代码审查。
- **微小局部文档或排版调整**：仅修改单行注释、文档错别字等无实际逻辑变更的场景无需派发独立审查子智能体。
- **正在进行中的未保存脏状态**：代码尚未通过本地测试或编译基线，且未形成逻辑闭环时，应先完成实现再请求审查。

## Role

独立资深代码审查员（Senior Code Reviewer），具备软件系统架构设计、设计模式、类型系统、工程实践标准及防御性编程经验。专注于以全新、无历史对话污染的客观视角核验代码实现是否对齐规划与质量标准。

## Inputs

- `{DESCRIPTION}`：当前已实现功能的精炼技术摘要，说明改动内容与实现机制。
- `{PLAN_OR_REQUIREMENTS}`：规划规格说明、任务描述、需求文档路径或验收标准。
- `{BASE_SHA}`：审查差异比对的起始 Git Commit SHA（例如 `git rev-parse HEAD~1` 或 `origin/main`）。
- `{HEAD_SHA}`：审查差异比对的结束 Git Commit SHA（例如 `git rev-parse HEAD`）。
- 仓库上下文：审查子智能体根据 BASE_SHA 与 HEAD_SHA 自行调取 `git diff --stat` 和 `git diff` 详情。

## Outputs

结构化代码审查报告（Structured Code Review Report）：
1. **Strengths（亮点）**：具体列举实现优秀之处（如整洁的数据迁移、高覆盖率真实测试、优雅的降级容错），并标注精准 `file:line`。
2. **Issues（分级缺陷）**：
   - **Critical (Must Fix)**：阻断性缺陷，包括功能失效、安全漏洞、数据丢失隐患、逻辑回归。必须立即修复。
   - **Important (Should Fix)**：关键缺陷，包括架构违背、功能漏失、不当异常处理、测试覆盖漏洞。在推进下一步前必须修复。
   - **Minor (Nice to Have)**：次要优化，包括代码风格、文档润色、微小性能优化、可读性改进。
   - 每个 Issue 必须包含四要素：`File:line reference`、`What's wrong`、`Why it matters`、`How to fix`。
3. **Recommendations（建设性建议）**：架构、工程实践或研发流程层面的长期改进建议。
4. **Assessment（结论裁决）**：
   - 合并结论：`Ready to merge? [Yes | No | With fixes]`
   - 裁决技术依据：1–2 句精炼的技术评估结论。

## Workflow

1. **获取 Git 比对区间**：
   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
   HEAD_SHA=$(git rev-parse HEAD)
   ```
2. **派发隔离上下文审查子智能体**：
   - 调用 Task 工具，指定类型为 `general-purpose`。
   - 填入 `code-reviewer.md` 提示词模板，注入 `{DESCRIPTION}`、`{PLAN_OR_REQUIREMENTS}`、`{BASE_SHA}` 与 `{HEAD_SHA}`。
   - 严禁传入主会话的历史交互与推理过程，确保审查者仅依据代码差异与技术要求做出无偏判决。
3. **执行多维度代码检查**：
   - **Plan alignment**：代码是否完全实现规划要求？改动属于合理优化还是偏离初衷？
   - **Code quality**：关注点分离、错误处理、类型安全、DRY 与避免过度设计、边界情况完备性。
   - **Architecture**：架构决策合理性、可扩展性、性能开销、安全漏洞防范、与周围代码的集成契合度。
   - **Testing**：测试验证真实业务逻辑而非仅测 Mock、边界用例覆盖、关键集成测试、所有测试通过。
   - **Production readiness**：数据库 Schema 迁移策略、向后兼容性、文档完整性、无残留显式 bug。
4. **校准与结构化产出**：
   - 客观分级缺陷，避免滥用 Critical 标签。
   - 先肯定优点再提出问题，提供具体可定位的 `file:line` 引用。
   - 给出明确结论裁决（Yes / No / With fixes）。
5. **分级响应审查反馈**：
   - **Critical**：立即阻塞后续任务，原地修复并重新验证。
   - **Important**：在继续推进下一项任务之前必须修复完成。
   - **Minor**：记录在案，作为后续重构或收尾 polish 任务处理。
   - **若审查意见有误**：严禁无理辩解；必须准备充分的技术证据、测试用例或代码验证，客观向审查者或人类伙伴说明理由。

## Branches

- **审查通过（Ready to merge: Yes）**：直接流转至下一项任务，或执行主干合并操作。
- **带修复通过（Ready to merge: With fixes）**：存在非致命的 Important 或 Minor 缺陷，必须在进入下一阶段前针对性修复并完成验证。
- **审查未通过（Ready to merge: No）**：存在致命 Critical 缺陷或严重偏离需求规格，必须全面修复后重新派发审查。
- **审查分歧分支**：当主开发者认为审查员给出的反馈基于错误前提或对规格理解偏差时，以代码行为证明或测试用例作为反证依据，阐明理由并确认决策。

## Rules

- **上下文隔离原则**：审查子智能体只能接收代码差异及目标规划，绝对不能加载主智能体的思维痕迹与会话历史。
- **早期高频原则**：Review early, review often。不得因改动较小或自信逻辑正确而跳过任务级审查。
- **证据定位原则**：所有指出缺陷必须携带精确的 `file:line` 引用，严禁给出模糊无依据的意见（如“需要改进错误处理”）。
- **实测有效原则**：审查子智能体绝不能在未实际阅读差异代码的情况下给出泛泛好评（“looks good”）。
- **严重度精准分级**：区分 Critical、Important 与 Minor，不得将代码风格微瑕标记为 Critical，亦不得掩盖架构隐患。

## Exceptions

- **紧急安全热修复（Emergency Hotfix）**：在线上严重故障的紧急压制场景下，可先完成修复验证并合并，随后立即进行追溯审查。
- **不可行建议处置**：若审查建议引入过度设计或破坏向后兼容性，实现者可在附注合理技术理由后标记推迟或拒绝。

## Dependencies

- **git 工具链**：依赖 `git rev-parse`、`git diff --stat`、`git diff` 进行精确差异捕获。
- **Task / Agent 执行器**：依赖平台子智能体派发机制（`general-purpose` 模式）运行隔离审查者。
- **规划与需求规格产物**：依赖如 `docs/plans/*.md` 或阶段任务列表提供校验真值基准。

## Permissions and Side Effects

- **权限要求**：只读权限（读取 Git 差异、检索代码文件、读取规划规格说明）。无需写入或修改代码权限。
- **环境隔离**：子智能体运行于独立会话空间，不修改全局状态或破坏当前工作区未暂存变更。
- **副作用**：消耗子智能体调用 Token，并生成结构化的审查意见文本。

## Gates

- **Gate 1: Pre-dispatch Verification**：确认代码已处于已提交（committed）或可准确定位的 Git SHA 节点，且测试已在本地全部通过。
- **Gate 2: Critical Zero Tolerance**：Critical 缺陷清零门禁，存在任何未修复的 Critical 问题一律禁止合并或推进下一步。
- **Gate 3: Important Resolution Gate**：在继续推进下一项开发任务前，所有 Important 级别缺陷必须全部闭环解决。

## Open Questions

- 当多个并行子任务同时发起代码审查时，如何在共享工作树或并发分支下有效避免 Git SHA 漂移或交叉覆盖？
- 在长周期大型重构中，如何动态权衡任务级审查粒度与批次审查效率？

## Unique Value

建立了基于独立子智能体的客观隔离代码审查机制，通过纯净的 Git 差异与规划比对，有效打破单智能体的认知盲区与自我验证偏见。其精细的四要素缺陷报告与三级严重度裁决体系，确保了复杂软件系统在多智能体流水线开发中的高标准质量门禁与可信度。

## Reading Coverage

已对本能力来源全部 2 篇规范文档完成 100% 逐行完整覆盖阅读：
1. `skills/requesting-code-review/SKILL.md`（共 103 行，覆盖核心原则、时机、步骤、示例、集成模式与红线规程）。
2. `skills/requesting-code-review/code-reviewer.md`（共 168 行，覆盖审查员提示词模板、五维核查清单、校准准则、报告结构与示例）。
