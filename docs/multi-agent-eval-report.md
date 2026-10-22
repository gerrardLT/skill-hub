# 多模型子智能体（Claude / GPT-6 / Gemini）全景评估与交叉验证报告

**评估时间**：2026-10-08  
**评估架构**：Capability Compiler V2 抽样代表性原子能力切片  
**异构评审阵容**：
1. **Claude (Sonnet 5.5 / Opus 体系)**：专注 Fail-closed 防御哲学、逻辑一致性与严格安全边界
2. **GPT-6 Astra**：专注工业级自动化 CI/CD、状态机确定性与契约变异检测
3. **Gemini 3.8 Flash High**：专注敏捷落地、开发者体验（DX）、零漂移与流水线开销

---

## 一、统一量化基准与五维量表权重

三方子智能体在第一阶段共同确立了工业级 AI 技能五维评估标准与硬性否决门槛：

| 维度代号 | 维度名称 | 权重 | 核心关注点 | 一票否决线 (Hard Gate) |
|---|---|:---:|---|---|
| **D1** | 职责边界与单一职责 | 20% | 职责单一内聚、无侧漏副作用、审修严格物理分离 | < 3 分，或出现审修合并 |
| **D2** | 权限安全与防御性约束 | 25% | 最小特权原则、物理读写隔离、严禁凭证外泄、未授权动作静态硬阻断 | < 3 分，或发生越权 |
| **D3** | 事实依据与防幻觉纪律 | 20% | 缺信主动挂起 (needs-input)、结论强绑定证据 (hash/commit/line)、严禁脑补推断 | < 3 分，或伪造日志与执行结果 |
| **D4** | 可验证性与验收门禁 | 20% | 产物具备机器可读 Schema、硬门禁断言确定、独立第三方可复验 | < 3 分，或依赖自报 passed |
| **D5** | 编排与上下游交接 | 15% | 类型化 I/O、四要素交接（身份、决策、证据、风险）、状态机完备 | < 3 分 |

**综合得分公式**：
$$\text{Score} = (D1 \times 0.20 + D2 \times 0.25 + D3 \times 0.20 + D4 \times 0.20 + D5 \times 0.15) \times 20$$
*准入门槛*：综合分 $\ge 80$ 且五项维度均 $\ge 3$，且无一票否决违规。

---

## 二、多模型独立打分与交叉对比汇总

针对抽样的 5 项覆盖生命周期各阶段的关键 Skill，三模型打分矩阵如下：

| Skill 标识 | 核心职责阶段 | Claude 得分 | GPT-6 Astra 得分 | Gemini 得分 | **三模型均分** | 交叉门禁裁决 |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **independent-code-review** | 实现与集成 / 独立审查 | 89.0 | **93.0** | **96.9** | **93.0** | **PASSED (全票标杆)** |
| **git-destructive-command-guard** | 架构与安全 / 破坏性拦截 | 87.0 | 84.0 | **96.1** | **89.0** | **PASSED** |
| **requirements-and-delivery-contract** | 需求与计划 / 契约转化 | 83.0 | 88.0 | **93.8** | **88.3** | **PASSED** |
| **browser-session-and-runtime-configuration** | 工具与运行 / 运行时隔离 | 79.0 | 73.0 | **94.1** | **82.0** | **PASSED (警告)** |
| **completion-evidence-gate** | 验证与质量 / 完成门禁 | 75.0 | **75.0 (FAILED)** | **91.7** | **80.6** | **FAILED (Astra 否决 / Claude 警示)** |

---

## 三、三模型交叉捕获的核心高价值发现

本次多异构模型评测展现出极强的交叉印证价值：**三个模型在完全独立的上下文和评估提示下，同时命中了完全一致的两个 P1 级架构漏洞！**

### 1. 致命缺陷 P1：`completion-evidence-gate` 的权限过宽与“契约-提示词”语义漂移
- **发现事实**：
  - `contract.json` 机器契约声明：`permission_identity: "local-exec"`，`host_actions: ["approved-local-commands"]`；
  - 但 `SKILL.md` 提示词明确要求：“this Skill never runs the commands itself”、“never rerun commands”。
- **各模型裁决**：
  - **GPT-6 Astra**：判定 D2 仅得 2 分（< 3），直接触发 Hard Gate 否决（**FAILED**）——“既然只做证据核验而不运行命令，开放本地命令通道违反最小权限原则”。
  - **Claude**：判定 D2 得 3 分临界线（总分 75 为全场最低）——“权限声明与文字行为自相矛盾，必须在升格前降级为 read-only 并清空 host_actions”。
  - **Gemini**：明确标注为系统最大语义漂移风险（Semantic Drift）——“若模型与平台授权不一致，将带来未授权命令执行面隐患”。
- **统一修复方案**：将 `contract.json` 中的 `permission_identity` 降级为 `read-only` 或 `artifact`，移除 `host_actions`，做到真正的审执分离。

### 2. 逻辑漏洞 P1：`browser-session-and-runtime-configuration` 内的前置条件自相矛盾
- **发现事实**：
  - 文档 Domain Guidance 第 1 条要求：`confirm that npx is available (command -v npx); if not, pause and ask for Node.js and npm`；
  - 第 3 条却规定：`do not add npx, browser-binding or approval gates from other providers`。
- **各模型分析**：
  - **Claude**：“对于未声明需要 npx 的 wrapper，第 1 条要求强制检查阻断，第 3 条禁止添加，执行者无从判断”。
  - **GPT-6 Astra**：“存在规则冲突，不同执行者对同一输入会产生完全不同的阻塞/放行状态，破坏状态机确定性”。
- **统一修复方案**：修正为仅当 wrapper contract 显式声明依赖 npx 时才进行检查。

### 3. 全场最高标杆：`independent-code-review`
- 三模型一致给出最高分（89.0 / 93.0 / 96.9，均分 93.0）。
- **共同称赞**：
  - 做到彻底的“审修物理隔离（No-fix, Read-only）”，从根本上断绝了 Agent 边审边改导致的幻觉掩盖；
  - 严格限制不越权代行批准合并或发布评论；
  - 严格要求每个缺陷绑定具体场景、行号和契约违背。

---

## 四、各模型视角的整体工业化水平总评

### 1. Claude 视角（Fail-closed 安全哲学）
> **“当前体系属于预生产候选级（约 L3/L5）。长处在于职责分离彻底、防幻觉纪律系统化；短处在于‘文字门禁多、机器门禁少’。只要将契约与说明中的权限矛盾消除，并将关键词严格绑定到不可被滥用的机器凭据上，即可真正达到坚不可摧的工程安全标准。”**

### 2. GPT-6 Astra 视角（工业工程化与状态机）
> **“具备极好的声明式契约基础，但在状态机语义（将业务 verdict 与执行状态混用）及自动化执行器落实路径约束上仍有差距。必须坚持‘单 Skill 合格只是局部条件，Recipe 闭环验证才构成组合条件’，先清空 Hard Gate 阻断项。”**

### 3. Gemini 视角（敏捷落地与开发者体验 DX）
> **“安全深度与确定性极强，三权分立防御架构成型。在敏捷微代理（Micro-agent）流水线中，五大交付物同时吐出的开销略大，建议后续支持紧凑型原子交付模式，并在 CI 中增加静态 Schema 零成本校验拦截。”**
