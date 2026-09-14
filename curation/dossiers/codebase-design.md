# codebase-design 来源能力档案

## Problem

在软件开发中，团队由于缺乏统一的架构设计语言与评价标尺，往往不自觉地陷入“浅模块堆砌”（Shallow Module Proliferation）与“面条式调用”的泥潭中。开发者常将模块划分等同于按代码行数切碎文件，导致接口庞大而内部逻辑单薄；同时对“可测试性”的误解引发了为测试而暴露内部细节、多层薄包装嵌套、以及单次重构破坏海量浅层单测等维护危机。

## When to Use

- **新模块或子系统接口设计（主要场景）**：在开始编写核心业务逻辑前，设计高内聚、小接口、宽实现的深模块（Deep Modules）。
- **重构既有浅模块与胶水层**：指导如何安全地将散落的薄层、数据透传包装器合并为功能集中的深模块。
- **决定系统接缝（Seam）与适配器（Adapter）位置**：判定何时真正需要定义接口隔离点，以及如何分类处理外部依赖。
- **探索多方案替代接口（Design It Twice）**：当关键核心模块存在多种接口设计路线时，派发多个并行智能体进行极端发散设计与多维权衡。
- **为其他架构技能提供基础词汇底座**：作为 `improve-codebase-architecture` 等高级技能的基础术语规范。

## When Not to Use

- **简单的纯静态脚本编写**：仅由两三行顺序命令组成的单次执行运维脚本。
- **现存成熟且不可变动的第三方外部 SDK 适配**：目标为严格遵循外部厂商硬性给定的 API 接口，而非设计自有领域模型。

## Role

代码库系统设计架构师（Codebase System Designer）。推崇深模块哲学（Deep Module Philosophy）与接缝力学，以“调用者的杠杆（Leverage）”、“维护者的内聚（Locality）”与“全员的可测试性（Testability）”为核心价值尺，指导系统接口与边界的高质量塑造。

## Inputs

- **待设计的业务功能规格或重构目标**：需要实现的业务逻辑、领域行为及数据处理链路。
- **依赖生态分类（Dependency Category）**：进程内计算、本地可替代依赖（如 PGLite）、自有远程服务（Ports & Adapters）、以及第三方外部不可控服务（Stripe/Twilio 等）。
- **既有领域模型（`CONTEXT.md`）**：对齐领域专有名词。

## Outputs

1. **深模块接口规格定义（Deep Module Interface Specification）**：
   - 极简的方法签名与参数定义（方法极少、参数简单）。
   - 完备的契约说明（包含调用不变量、调用时序约束、错误模式、必要配置及性能特征）。
2. **多方案对比与推荐裁决（Design It Twice Comparison & Verdict）**：
   - 3+ 种激进发散的接口方案（极简高杠杆型、高灵活性型、最常见调用优化型、端口适配型）。
   - 基于深度（Depth）、内聚力（Locality）与接缝定位（Seam Placement）的三维对比分析与明确结论。
3. **“替代而非分层”测试套件（Replace-Don't-Layer Test Suite）**：
   - 直接跨越外部接缝针对深模块公开接口进行全覆盖行为断言，删除过时浅层单测。

## Workflow

1. **统一架构设计语汇（Standard Glossary）**：
   - 严格使用：Module、Interface、Implementation、Depth、Seam、Adapter、Leverage、Locality。
   - 严厉排斥：Component、Service、Unit、API、Signature、Boundary、Layer、Wrapper。
2. **深模块三问自省（Deep vs Shallow Check）**：
   - 我能否进一步减少对外暴露的方法数量？
   - 我能否进一步简化调用参数？
   - 我能否将更多实现复杂度封装隐藏在模块内部？
3. **贯彻四大核心原则（Core Principles）**：
   - **深度是接口的属性，而非实现的属性**：内部可以由私有小组件构成（内部接缝），但不对外暴露。
   - **删除测试（The Deletion Test）**：若删除该模块复杂度直接消失，则属冗余透传；若复杂度重新散落至 N 个调用者，则该模块具备承重价值。
   - **接口即测试表面（The interface is the test surface）**：调用方与测试用例跨越同一道接缝进行交互；严禁为了测试穿透接口窥探内部私有状态。
   - **两套适配器法则（Two Adapters Rule）**：一套适配器代表假设性接缝（仅为过度抽象）；两套适配器（如生产真实环境 + 测试内存实现）才构成真实接缝。
4. **依赖分类与接缝落位（DEEPENING Protocol）**：
   - 进程内（In-process）：直接合并与测试，无需定义端口适配器。
   - 本地可替代（Local-substitutable）：在测试套件中运行测试替代件（如 in-memory fs），接缝收敛于内部。
   - 自有远程服务（Remote but owned）：在接缝处定义 Port，注入 HTTP 生产适配器与内存测试适配器。
   - 真实外部服务（True external）：在接缝处定义 Port，注入生产客户端与测试 Mock 适配器。
5. **双重/多重接口发散推演（Design It Twice Workflow）**：
   - 步骤 1：界定问题空间，呈现约束条件、依赖分类与不带接口结论的约束草图。
   - 步骤 2：并发派发 3+ 个子智能体分别按不同约束（极简高杠杆、高灵活扩展、最常见调用优化、端口适配架构）输出完整接口与权衡。
   - 步骤 3：顺序呈现各方案，从深度、内聚与接缝三个维度深入对比，给出具有鲜明倾向性的推荐结论或混合方案。
6. **测试重塑落地（Replace, Don't Layer）**：
   - 废弃并删除旧浅模块上的碎步测试，编写直接验证深模块行为表现的新测试套件。

## Branches

- **单一明确设计分支**：接口形态直观且无重大权衡分歧，直接按深模块三原则与测试三律完成定义。
- **Design-It-Twice 多智能体发散分支**：接口设计具有重大架构影响或存在多种分歧路线，派发 3+ 子智能体并发推演。
- **内部接缝 vs 外部接缝分支**：模块内部复杂度较高但不对外暴露，在模块内部建立私有测试接缝，外部接缝保持极简。

## Rules

- **术语纯洁性红线**：严禁在沟通、方案与代码注释中将 Module 称为 Component/Service，将 Interface 窄化为 API/Signature，或将 Seam 泛化为 Boundary。
- **两套适配器铁律**：严禁在仅有单一实现且无真实测试替换需求的地方凭空抽象 Interface 与 Adapter。
- **测试不穿透接口铁律**：测试用例必须断言通过接口产生的可观测结果，严禁测试内部实现细节或私有状态；内部重构不应破坏接口测试。
- **测试三律**：接受外部依赖而非在内部主动创建依赖（Accept dependencies, don't create them）；返回纯计算结果而非直接产生隐式副作用（Return results, don't produce side effects）；保持极小公开表面积（Small surface area）。

## Exceptions

- 在无法使用端口注入的极端遗留硬编码老系统接缝处，可临时允许采用环境变量或构建期条件编译进行适配器切换。

## Dependencies

- **`superpowers:subagent-driven-development` / `Agent` 工具**：用于在 Design It Twice 模式中并发派发多个并行智能体。
- **`improve-codebase-architecture`**：下游应用技能，调用本技能的词汇库与深化设计模式。

## Permissions and Side Effects

- **权限要求**：只读权限（读取现有接口与依赖）、子智能体派发权限（Task 工具）。
- **副作用**：在多智能体推演时产生并发模型调用消耗；在测试落地时触发冗余浅层单测文件的删除。

## Gates

- **Gate 1: Deletion Test Validation Gate**：新模块确立前必须通过删除测试，证实能有效收敛调用端复杂度。
- **Gate 2: Two Adapters Verification Gate**：任何公开接缝处若仅存在单一适配器，强制驳回抽象并内联实现。
- **Gate 3: Test Surface Invariant Gate**：新增测试套件必须 100% 作用于深模块公开接口，禁止出现刺探内部私有变量的非规范断言。

## Open Questions

- 当深模块内部状态机极其庞大时，如何在不破坏“接口即测试表面”铁律的前提下，对极深分支状态执行针对性错误注入测试？
- 在强类型语言（如 Rust/TypeScript）中，如何精准度量泛型参数与类型约束对“调用者认知接口复杂度”的实质膨胀影响？

## Unique Value

将约翰·欧斯特豪特（John Ousterhout）的深模块软件设计哲学与迈克尔·费瑟斯（Michael Feathers）的接缝力学深度融合，形成了一套具备极高辨识度与严谨语义的工程设计系统。通过严格的 8 大术语规约、删除测试、两套适配器法则、以及开创性的“Design It Twice 并行多智能体发散设计”工作流，为抵御软件熵增提供了最根本的架构方法论。

## Reading Coverage

已对本能力来源全部 3 篇规范文档完成 100% 逐行完整覆盖阅读：
1. `skills/codebase-design/SKILL.md`（共 114 行，覆盖深模块定位、8 大标准词汇释义、深浅模块对比、四大原则、可测试性三律、概念关系网络及被否决的概念视角）。
2. `skills/codebase-design/DEEPENING.md`（共 37 行，覆盖四大依赖分类法则、接缝纪律内外部接缝辨析、以及替代而非分层的测试重塑策略）。
3. `skills/codebase-design/DESIGN-IT-TWICE.md`（共 44 行，覆盖问题空间界定、3+ 并行子智能体发散提示词范式、五项报文契约与三维对比决策推荐流程）。
