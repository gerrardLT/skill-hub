# executing-plans 来源能力档案

## Problem

在软件工程中，当技术规划方案（Implementation Plan）制定完成并交由执行者实施时，执行者容易产生自作主张、跳过中间验证、模糊任务状态、或在遇到未预见阻碍时盲目猜测修改代码的行为。这不仅破坏了既定方案的细粒度 TDD 节奏与安全边界，还容易在 main/master 主分支造成脏代码污染与返工。

## When to Use

- **已有结构化实施方案待执行时（主要场景）**：在通过 `writing-plans` 完成零上下文详细技术方案编写后，由当前执行会话逐项落地。
- **不支持子智能体并发调度的受限环境**：当开发平台缺乏多子智能体（Subagent）调度能力时，采用本技能在单一会话中通过严格的检查点与任务状态机推进实现。
- **需要强审查检查点（Review Checkpoints）的单体开发**：在不需要分布式多智能体但需要阶段性暂停、复核与分支交付的开发流程中。

## When Not to Use

- **支持高效多子智能体调度的平台环境**：当工作环境完全支持子智能体（如 Claude Code、Codex）时，应优先使用更高质量与完全隔离的 `superpowers:subagent-driven-development`。
- **实施方案尚未就绪的早期阶段**：在尚未形成细粒度、零占位符的技术方案前，应先运行 `writing-plans`。
- **无方案的即兴微小修改**：仅修复单行拼写或无需规划的单次操作。

## Role

方案严谨执行官（Disciplined Plan Executor），秉持契约精神与外科手术式执行纪律。严格遵循预定方案中的微任务（bite-sized steps），不擅自扩大变更范围，不跳过验证门禁，遇到阻碍时主动叫停求助而非凭空臆测。

## Inputs

- **实施方案文件（Plan File）**：由 `writing-plans` 等前置技能产出的结构化方案文档（通常包含 Goal、Architecture、Tech Stack 及包含 Red-Green-Refactor 步骤的 Task 序列）。
- **隔离工作空间（Git Worktree）**：由 `using-git-worktrees` 或版本管理规范创建的独立临时开发分支工作区。
- **人类伙伴的补充确认**：当方案存在疑问或执行遇阻时的交互反馈。

## Outputs

1. **逐任务履约与状态更新**：任务跟踪器（TodoWrite / TaskList）中每个 Task 严格经历 `in_progress` 到 `completed` 的可信流转。
2. **通过验证的完整代码实现**：各任务附带全绿测试输出与规范提交记录的代码增量。
3. **交付阶段流转声明**：向 `finishing-a-development-branch` 发起的标准交接握手（宣布启动收尾与分支集成）。

## Workflow

1. **声明启动与子智能体环境核查**：
   - 启动宣告：“I'm using the executing-plans skill to implement this plan.”
   - 若环境支持子智能体，提示用户优先考虑 `subagent-driven-development`。
2. **加载并批判性审查方案（Step 1: Load and Review Plan）**：
   - 完整读取方案文件内容。
   - 批判性审查方案是否存在逻辑盲区、不可行假设或遗漏依赖。
   - 若有顾虑或疑问：必须在动工前向人类伙伴提出并澄清。
   - 若无顾虑：将方案中的所有任务初始化录入任务跟踪器并推进。
3. **逐项执行任务状态机（Step 2: Execute Tasks）**：
   - 针对每个子任务：
     1. 将状态标记为 `in_progress`。
     2. 严格按方案定义的微步（bite-sized steps）逐步执行（测试先行、最小实现）。
     3. 运行方案指定的完整验证命令并核实输出。
     4. 将状态标记为 `completed`。
4. **触发分支交付收尾（Step 3: Complete Development）**：
   - 所有任务验证通过后，宣告启动 `superpowers:finishing-a-development-branch`。
   - 按照收尾规范核验测试、向用户呈现合并/PR选项并执行选择。

## Branches

- **执行顺畅主干分支**：所有任务依序通过 TDD 闭环与验证门禁，顺利进入 `finishing-a-development-branch`。
- **遇阻立即叫停分支（Hard Stop on Blocker）**：
  - 触发条件：依赖缺失、测试持续失败、指令模糊、方案存在重大缺口、连续验证失败。
  - 动作：立即停止执行，严禁盲目猜想尝试，如实向人类伙伴反馈具体现象并请求澄清。
- **回退审查分支（Revisit Earlier Steps）**：
  - 触发条件：人类伙伴因反馈更新了实施方案，或底层架构方案需要推倒重构。
  - 动作：回退至 Step 1，重新审查最新方案、调整任务跟踪器并重新起步。

## Rules

- **严禁主干无授权动工**：在未取得用户明确授权前，绝对禁止在 `main` 或 `master` 分支直接开始代码实现。
- **步骤严格遵从原则**：严禁随意调换或合并方案中细分的执行步骤，不得跳过红绿验证直接写业务代码。
- **零猜测原则**：遇到指令不清或阻碍时，“宁停勿猜”；向人类求助是标准动作，绝不通过试探性修改破坏代码库。
- **门禁不减免原则**：方案中声明的每一项验证指令必须新鲜执行并读取输出，严禁擅自减免。
- **关联技能协同响应**：方案中引用的配套技能（如特定的调试、重构或审查技能）必须在指定步骤准时加载与调用。

## Exceptions

- 若方案中的某个次要子任务经人类确认已由外部变更解决或被判定废弃，经人类授权后可跳过并更新方案记录。

## Dependencies

- **`superpowers:writing-plans`**：上游技能，负责产出执行所需的高质量方案。
- **`superpowers:using-git-worktrees`**：前置工作空间隔离技能，确保在独立 worktree/分支中安全执行。
- **`superpowers:finishing-a-development-branch`**：下游交付技能，负责在任务全量完成后执行测试终验与分支归并。
- **任务跟踪工具**：依赖平台的 TaskCreate / TaskUpdate / TodoWrite 机制维护执行可见性。

## Permissions and Side Effects

- **权限要求**：代码读写权限、文件修改权限、本地构建与测试命令执行权限、Git 分支只读及局部提交权限（主干推送需人类确认）。
- **副作用**：在工作分支创建临时代码文件、修改源码、产生 Git 提交历史。

## Gates

- **Gate 1: Critical Review Clear Gate**：在动工编写第一行代码前，必须完成方案批判性阅读并确保零未解疑问。
- **Gate 2: Branch Safety Gate**：验证当前工作目录绝不在未受保护的 main/master 分支。
- **Gate 3: Per-Task Verification Gate**：单项任务的测试与命令未全绿前，严禁将任务标记为 `completed` 或进入下一任务。
- **Gate 4: Handshake to Finish Gate**：全量任务状态必须 100% 达成 `completed` 且全量回归测试通过后，方可唤醒 `finishing-a-development-branch`。

## Open Questions

- 当长任务执行跨越上下文窗口压缩周期时，如何保证任务跟踪器中的细粒度执行进度不发生漂移或重复执行？
- 在单会话执行过程中若发生局部架构变更，如何标准化同步更新既定方案与关联任务树？

## Unique Value

确立了在非子智能体环境或受限单会话架构下落地复杂方案的高纪律性执行标准。通过将方案批判性审查、严苛的任务状态机、阻碍即叫停机制以及主分支保护原则融为一体，为单体智能体开发提供了媲美团队协同的代码质量与执行确定性。

## Reading Coverage

已对本能力来源全部 1 篇规范文档完成 100% 逐行完整覆盖阅读：
1. `skills/executing-plans/SKILL.md`（共 71 行，完整覆盖概览、三步执行流程、何时停步求助、何时回退上游、执行守则及三方工作流技能依赖网络）。
