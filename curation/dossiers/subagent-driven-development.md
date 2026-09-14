# subagent-driven-development 来源能力档案

## Problem

在大型技术方案落地过程中，单一会话执行容易导致上下文持续膨胀、历史对话污染、认知疲劳及对自身代码的盲目信任。同时，传统多智能体协作常面临任务交接摩擦大、子智能体自报成功虚假、实现过度或遗漏等问题。若缺乏结构化的两阶段质量闭环，局部缺陷将迅速蔓延，导致后期集成彻底失效。

## When to Use

- **拥有结构化实施方案且任务相对独立（主要场景）**：方案已拆解为相对解耦的 Task 单元，且希望在当前会话内实现快速闭环迭代。
- **支持子智能体（Subagent）调度的平台**：在具备子智能体派发能力的智能体环境（如 Claude Code 或 Codex）中作为首选执行工作流。
- **高确定性与高代码质量要求的交付场景**：需要通过“任务实现 -> 规格核验 -> 代码质量核验”的双重独立审查机制杜绝缺陷外溢。
- **追求高速自主推进（Continuous Execution）**：不需要在每个子任务间向人类寻求确认，追求端到端全自动流水线式施工。

## When Not to Use

- **任务间高度强耦合且无法切分的探索型开发**：修改一处导致全局多文件连锁动态震荡，无法确立独立任务边界的场景。
- **尚无书面技术方案的早期阶段**：尚未完成系统设计与任务划分时，应先执行 `brainstorming` 或 `writing-plans`。
- **不支持子智能体调度的单会话受限环境**：平台无法派发独立子进程或隔离会话时，应退回至 `executing-plans`。

## Role

多智能体交付流水线总控指挥官（Subagent Delivery Pipeline Controller）。负责解构总方案、为子智能体精密构造隔离上下文、调度双阶段审查门禁、分流处置阻碍，并在任务全闭环后交接分支发布。

## Inputs

- **实施方案全文（Implementation Plan）**：由 `writing-plans` 等前置能力产出的完备方案，包含各任务的详细规格、文件路径与验证指令。
- **隔离开发工作空间（Git Worktree）**：由 `using-git-worktrees` 准备的独立工作分支目录。
- **模型分级配置（Model Hierarchy）**：针对机械实现、系统集成与架构审查分配的不同算力模型规格。

## Outputs

1. **逐任务完整落地代码与 Git 提交**：每个 Task 均由独立的实现子智能体完成实现、单测编写、自审并生成原子提交。
2. **两阶段独立审查报告**：
   - 阶段 1：规格符合度报告（Spec Compliance Review），包含全需求比对、无多余功能判定及精准 `file:line` 缺陷。
   - 阶段 2：代码质量审查报告（Code Quality Review），包含架构、类型、异常、测试真实性与文件膨胀审计。
3. **全流程发布交接**：全量任务闭环后的整体交付终验报告，并无缝流转至 `finishing-a-development-branch`。

## Workflow

1. **总控前置准备与任务全量提取**：
   - 宣告启动：“I'm using Subagent-Driven Development to execute this plan.”
   - 一次性完整读取方案文件，抽取所有任务的完整文本与场景上下文，在任务跟踪器中建立全局任务清单。
2. **单任务实现调度循环（Per Task）**：
   - **派发实现子智能体（Implementer）**：
     - 注入完整任务文本（绝不让子智能体自行读取方案文件）与场景上下文。
     - 若子智能体提出前置疑问：立即清晰解答并补充上下文，切勿强行催促施工。
     - 实现者遵循 TDD 原则编写代码、运行测试通过、执行原子提交、完成四维自审（完整性/质量/克制/测试），产出状态报告（DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT）。
   - **派发规格审查子智能体（Stage 1: Spec Reviewer）**：
     - 奉行“零信任”原则，绝不轻信实现者自述。
     - 逐行比对代码与需求，排查缺项（Missing）、过度工程（Extra）及理解偏差（Misunderstandings）。
     - 若存在问题：返回实现者修复并重新审查，直至完全达成 ✅ Spec compliant。
   - **派发质量审查子智能体（Stage 2: Code Quality Reviewer）**：
     - **硬性门禁：仅在规格审查通过后方可启动**。
     - 调用 `requesting-code-review` 模板，结合任务 Git SHA 区间审查单一职责、单元解耦、文件膨胀、真实测试与代码坏味道。
     - 若存在 Critical/Important 问题：返回实现者修复并复审，直至通过。
   - **任务标记完成**：在跟踪器中将该任务标记为 `completed`。
3. **连续自主流转**：
   - 不在任务间向人类用户做无意义的“是否继续”请示，自主推进直至遇到无法化解的 BLOCKED、重大歧义或全量任务完成。
4. **全量终验与分支归并收尾**：
   - 所有任务完成后，派发全局审查智能体执行全量差异终验。
   - 激活 `superpowers:finishing-a-development-branch` 交付成果。

## Branches

- **任务常规闭环分支**：实现 -> 自审 -> 规格通过 -> 质量通过 -> 推进下一任务。
- **规格偏离重审分支**：规格审查发现漏项或过度设计 -> 实现者返工修复 -> 规格复审 -> 恢复主线。
- **质量缺陷重审分支**：质量审查指出架构/代码缺陷 -> 实现者重构修复 -> 质量复审 -> 恢复主线。
- **状态分流阻碍处置分支（Implementer Status Handling）**：
  - `DONE`：直接进入规格审查。
  - `DONE_WITH_CONCERNS`：总控评估其疑虑；若涉及正确性先解决再审查，若属客观观测则带入审查。
  - `NEEDS_CONTEXT`：总控补充上下文并重新派发。
  - `BLOCKED`：四步分流——缺上下文补上下文；需高推理换高阶模型；任务过大拆分为细任务；方案有误升级交由人类处理。严禁在不改动条件的情况下盲目重试。

## Rules

- **上下文完全隔离铁律**：子智能体绝不继承主会话的历史记录，总控必须为其精密构造自包含的上下文与完整任务文本。
- **审查阶段顺序铁律**：严禁在规格审查（Spec Review）未完全通过前启动代码质量审查（Code Quality Review）。
- **零信任代码审计原则**：审查者必须独立阅读实际代码差异，绝对禁止听信实现者的口头宣称。
- **任务严格串行推进**：禁止并发派发多个实现子智能体，以防止同一代码库发生文件修改冲突与逻辑竞态。
- **连续自主执行原则**：主控禁止在每个任务间停下来向人类发送进度汇报或询问“是否继续”，除非触发不可化解的阻断。
- **主分支动工保护**：严禁在未获人类明确许可前在 main/master 主分支直接开始实现。

## Exceptions

- 若实现者因平台外部网络或依赖损坏触发 BLOCKED，且属于环境级偶发故障，可修复环境后原样重派。

## Dependencies

- **`superpowers:writing-plans`**：方案源头输入。
- **`superpowers:using-git-worktrees`**：隔离工作空间基座。
- **`superpowers:requesting-code-review`**：质量审查员提示词核心基座。
- **`superpowers:finishing-a-development-branch`**：交付落地终点。
- **`superpowers:test-driven-development`**：实现子智能体的单测执行规范。

## Permissions and Side Effects

- **权限要求**：多子智能体调度权限（Task 工具）、代码与文件读写、Git 分支提交、本地测试执行。
- **副作用**：消耗较多的智能体调度 Token；在工作树产生细粒度的原子 Git 提交历史。

## Gates

- **Gate 1: Context Self-Containment Gate**：派发实现者前，核验任务文本已完整粘贴，严禁令子智能体自行读取方案文件。
- **Gate 2: Spec Compliance Clearance Gate**：实现必须 100% 满足规格且无多余代码，未获 ✅ 前禁止流转至质量审查。
- **Gate 3: Code Quality Clearance Gate**：代码必须达到无 Critical/Important 缺陷标准，未通过前禁止标记任务完成。
- **Gate 4: Final Implementation Verdict Gate**：全案全部任务必须全绿，且全局复审确认无回归后，方可唤醒分支归并。

## Open Questions

- 当项目包含大量互不干扰的完全独立模块时，如何在保证无写冲突的前提下探索跨模块的受控并行调度？
- 如何在极其漫长的流水线中建立低成本的子智能体性能与 Token 消耗审计跟踪？

## Unique Value

建立了业界领先的多智能体软件流水线生产范式。通过“上下文绝对隔离”、“模型按需分级梯次”、“自审 + 规格审查 + 质量审查”的三重质量过滤网，以及“连续自主执行不打扰用户”的高效运转机制，彻底消除了单会话幻觉与上下文衰减，为复杂系统的自动化工程交付树立了极高标杆。

## Reading Coverage

已对本能力来源全部 4 篇规范文档完成 100% 逐行完整覆盖阅读：
1. `skills/subagent-driven-development/SKILL.md`（共 279 行，完整覆盖子智能体架构、连续执行原则、状态机流程图、模型梯次分级、状态处置协议、全流程范例、优势成本分析与红线准则）。
2. `skills/subagent-driven-development/implementer-prompt.md`（共 113 行，覆盖实现者提示词模板、代码组织守则、能力超出升级安全阀、四维自审清单与四状态汇报规范）。
3. `skills/subagent-driven-development/spec-reviewer-prompt.md`（共 61 行，覆盖规格审查员提示词模板、零信任阅读代码原则、三维比对清单与输出规范）。
4. `skills/subagent-driven-development/code-quality-reviewer-prompt.md`（共 25 行，覆盖质量审查员前置门禁、接口适配与四项专属架构质量核查项）。
