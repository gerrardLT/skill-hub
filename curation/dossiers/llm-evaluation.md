# llm-evaluation 来源能力档案

## Problem

在基于大语言模型（LLM）的应用研发与交付过程中，AI 生成内容的非确定性（Non-deterministic）、幻觉（Hallucination）以及缺乏金标准标注，给系统质量评估带来巨大挑战：
1. **评估手段单一或碎片化**：仅依赖简单的字符串匹配或主观人工抽查，无法覆盖文本生成、语义蕴含、检索相关性与安全有害性等多维质量指标；
2. **模型与提示词迭代缺乏基准保护**：对 Prompt 进行微调或更换底层模型时，缺乏系统性回归测试（Regression Testing），导致修复旧缺陷时引入未知的性能倒退；
3. **主观人工评估缺乏一致性度量**：人工标注打分标准不一，缺乏跨标注员一致性（Cohen's Kappa）核验，导致评估结果置信度低且难以规模化；
4. **统计对比缺乏严谨性**：在 A/B 测试或方案优选时，仅对比平均数绝对值，缺乏统计显著性检验（t-test）与效应量（Cohen's d）分析。

## When to Use

- **LLM 应用端到端质量系统性度量**：上线前对大模型生成文本、RAG 检索质量、分类准确率等进行全面基准评测。
- **模型选型与 Prompt 变更比对（A/B Testing）**：在多个候选模型或不同 Prompt 版本之间进行配对对比或单点打分，确定优胜方案。
- **发布前回归测试与阈值告警（Regression Detection）**：在 CI/CD 流水线中持续运行黄金测试集，自动拦截性能退化超过指定阈值的变更。
- **建立基准套件与时序追踪（Benchmarking）**：聚合均值、方差、极值等统计量，持续监控线上模型表现。

## When Not to Use

- **传统确定性单元测试与集成测试**：针对传统业务逻辑、API 协议契约或前端 UI 行为测试，应直接使用 `vitest`、`playwright` 等工具。
- **纯代码语法与静态检查**：代码格式、类型检查与常规 Lint 应交由编译器或静态分析器处理。
- **生产线上实时链路监控（APM / Observability）**：针对毫秒级系统吞吐、网络时延及底层硬件指标的监控，应交由专业 APM 平台负责。

## Role

大模型应用评测与质量保障专家（LLM Evaluation & Benchmarking Specialist）。负责构建涵盖自动化统计指标、自然语言推理（NLI）事实性校验、LLM-as-Judge 评审、人工标注一致性审查及统计学假设检验的完整大模型评测闭环。

## Inputs

- **待评测模型或链（Model / Chain to Evaluate）**：提供预测推理接口的模型客户端或执行链。
- **黄金评测数据集（Benchmark Dataset / Test Cases）**：包含输入提示词（Input/Question）、标准答案（Expected/Reference）及可选上下文（Context）的测试样本集合。
- **度量指标配置集合（Metric Suite）**：指定选用的自动化指标（BLEU、ROUGE、BERTScore、Groundedness、Factuality 等）或评测大模型配置。
- **历史基线数据（Baseline Results）**：用于回归检测的历史指标得分快照与容忍阈值（Threshold，如 5%）。

## Outputs

- **评测聚合得分报告（Evaluation Results）**：按指标输出平均分（Mean）、标准差（Std）及各样本原始打分明细。
- **LLM-as-Judge 结构化评定结果**：单样本质量评分（Accuracy、Helpfulness、Clarity 及 Reasoning）或双样本优胜裁决（Winner: A/B/Tie、Confidence）。
- **A/B 测试统计检验报告**：包含均值差、相对增益百分比、p 值（p-value）、统计显著性判定、Cohen's d 效应量分级与优胜方。
- **回归测试告警清单（Regression Report）**：标记出相对历史基准退化超过阈值的受损指标列表。

## Workflow

1. **构建评测测试集与用例（Prepare Evaluation Dataset）**：
   - 组织标准格式测试集，包含 input、expected 参照以及 context 依据。
2. **装配指标度量套件（Assemble Evaluation Suite）**：
   - 组合文本生成重合度指标（BLEU/ROUGE）、语义向量指标（BERTScore）、检索指标（MRR/NDCG）及 NLI 上下文溯源指标（Groundedness/Factuality）。
3. **批量执行推理与多维打分（Run Prediction & Scoring Pipeline）**：
   - 驱动模型产出预测结果，将结果、参考答案与上下文注入各指标函数并发计算得分。
4. **引入 LLM-as-Judge 深度评审（Execute LLM-as-Judge）**：
   - 调用更高级别大模型，采用 Pointwise（单点打分）或 Pairwise（两两对比）提示词，强制输出符合 Pydantic Schema 的 JSON 评语。
5. **实施人工评估与一致性校准（Conduct Human Evaluation & Agreement Check）**：
   - 制定结构化标注指南，使用 Cohen's Kappa 统计量检验双人标注一致性，剔除主观偏置。
6. **统计学假设检验与回归守卫（Perform Statistical A/B & Regression Guard）**：
   - 运行独立样本 t 检验与 Cohen's d 效应量计算确认 A/B 测试有效性；
   - 运行回归探测器，对比当前得分与基准历史得分，相对衰减超阈值即刻告警。

## Branches

- **自动化轻量打分分支（Automated Metrics Branch）**：全自动计算快速指标，适合 CI/CD 高频构建快速冒烟。
- **LLM-as-Judge 评审分支（LLM Judge Branch）**：在缺乏确定标准答案或需评估逻辑自洽性时，调用大模型充当裁判。
- **人工质检抽测分支（Human Annotation Branch）**：针对高风险或关键领域样本，由人类专家进行 1-5 分打分并计算一致性 Kappa。
- **A/B 变体对比分支（Statistical A/B Branch）**：输入 Variant A 与 Variant B 样本集，开展双尾显著性检验。

## Rules

- **上下文溯源严谨性铁律（Groundedness Invariant）**：RAG 场景下的生成内容必须与检索出的 Context 保持严格蕴含（Entailment），不可引入外部未经验证事实。
- **结构化裁判输出法则（Structured Judge Output）**：LLM-as-Judge 必须使用强类型 Schema（如 Pydantic）约束输出格式，必须包含打分理由（Reasoning），严禁无理由纯打分。
- **双人标注一致性门禁（Inter-Rater Agreement Rule）**：人工标注数据在用于模型基准前，必须通过 Cohen's Kappa 核验，Kappa < 0.4 时必须重构标注指南与重新培训。
- **统计学显著性防伪原则（Statistical Significance Mandate）**：A/B 测试宣布胜出方前，必须确保 p 值低于显著性水平（alpha=0.05），避免将采样噪声误判为算法优化。
- **基线防退化守卫铁律（Zero Silent Regression）**：核心业务指标若出现超过配置阈值（如 5%）的相对下滑，必须标记为 regression 并阻断上线。

## Exceptions

- **开放式创意生成场景（Creative Generation）**：当评测创意写作或开放对话时，放行精确词汇重合度（BLEU/ROUGE），改用语义相似度与 LLM Judge。
- **小样本探索性快速验证**：在样本量低于 30 的极早期实验中，放行 t 检验严格要求，但必须在报告中声明样本不足、统计效力受限。

## Dependencies

- **自动化 NLP 与机器学习算法库**：`nltk`、`rouge_score`、`bert_score`、`transformers`、`scikit-learn`、`scipy`、`numpy`。
- **LLM 客户端与数据校验**：`anthropic`、`pydantic`、可选平台集成 `langsmith`。

## Permissions and Side Effects

- **权限要求**：本地文件只读、评测 API 远程调用网络访问权限。
- **副作用**：向本地或评测平台输出评估日志、测试结果 JSON 与告警事件；无代码库破坏性写入。

## Gates

- **Gate 1: Metric Reproducibility Gate**：所有自动化评测函数必须无随机种子漂移，确保同一输入输出一致打分。
- **Gate 2: Statistical Rigor Gate**：A/B 对比必须输出 p 值与效应量，杜绝无统计学意义的虚假胜出声明。
- **Gate 3: Baseline Regression Gate**：当前测试得分与基线相比跌幅超过阈值时触发阻断。

## Open Questions

- 当 LLM-as-Judge 自身存在位置偏见（Position Bias，偏向选 A 或 B）或长度偏见（Verbosity Bias）时，如何通过反转输入顺序与长度归一化更低成本地消解？
- 多轮复杂 Agent 任务交互链路中，如何将单步评估与最终目标达成度进行合理的权重衰减融合？

## Unique Value

打通从经典 NLP 统计重合度、NLI 逻辑蕴含推理，到大模型裁判员（LLM-as-Judge）及严格统计学 A/B 假设检验的完整工业级评测技术栈，为大模型应用建立可量化、可追溯、防退化的质量防线。

## Reading Coverage

- `skills/llm-evaluation/SKILL.md`: 涵盖自动化指标矩阵（BLEU、ROUGE、BERTScore、MRR、NDCG 等）、人工评估维度、LLM 裁判三大模式、EvaluationSuite 架构设计与快速上手规范。
- `skills/llm-evaluation/references/details.md`: 涵盖 BLEU/ROUGE/BERTScore 具体实现、Groundedness 与事实性 NLI 校验、LLM-as-Judge 单点/双两比较实现、人工标注表单与 Cohen's Kappa 检验、A/B 测试 t 检验与 Cohen's d、回归检测器及 LangSmith 评测集成。
