# 状态机：9 阶段完整定义

权威定义。SKILL.md 中表格是摘要，冲突时以本文为准。

```
INTAKE
↓
DISCOVERY
↓
STRATEGY
↓
PRIORITIZATION
↓
DEFINITION
↓
PLANNING
↓
VALIDATION
↓
MEASUREMENT
↓
LEARNING
↺（回退到任意阶段，见 learning-loop.md）
```

通用规则：
- **允许跳过**：INTAKE 判定材料充分的阶段直接标记 `SKIPPED-(理由)`，不重跑
- **允许回退**：Gate 失败或 Learning Loop 触发时回退，回退必须在 `decisions.md` 记录
- **单向默认**：无特殊信号时按箭头方向推进

---

## INTAKE

**目标**：建立项目全景，确定本次任务从哪个阶段切入。

**识别 9 项**（写入 `context.md`）：

1. 产品是什么
2. 用户是谁
3. 当前阶段（对照状态机自评）
4. 当前问题
5. 商业目标
6. 已有证据（列清单，标注质量：一手/二手/传闻）
7. 已有文档（PRD、调研报告等，读入并登记）
8. 已知约束（资源、时间、技术、合规）
9. 最大未知量（整个项目最要命的那个未知）

**产出**：`context.md` + 本次执行的阶段序列（见 router.md）。

**Gate**：9 项全部有答案（允许答案是"未知"，但必须显式写出）。

---

## DISCOVERY

**目标**：验证问题真实存在，而不是验证自己想做的方案。

**调用**：`discovery-process`（主流程）；`interview-script`（需要访谈时）。

**推理链**：假设 → 用户问题 → 用户证据（说出来的）→ 行为证据（做出来的）→ Problem Validation。

**输入**：context.md 中的假设与已知证据。

**产出**（写入 `evidence.md`、`assumptions.md`）：
- 已验证问题列表（每条附证据引用与证据类型）
- 被推翻/削弱的假设
- 访谈记录与行为数据摘要
- 仍未验证的关键假设清单

**Gate（进入下一阶段的硬条件）**：
1. 至少一个核心问题同时具备用户证据（访谈中用户主动描述的过去行为）与行为证据（数据/留存/流失等客观信号）
2. 访谈合规：无引导性提问、无推销、只问过去不问未来（Mom Test 标准）
3. 证据与问题的因果链能讲通，而不是"用户提到了 X 所以他们需要 X"

**不达标动作**：补访谈 / 补数据，禁止直接进入大规模 Solution Design。

---

## STRATEGY

**目标**：形成可辩护的 Product Thesis——为什么是我们、为什么是现在、凭什么赢。

**调用**：`product-strategy-session`（主流程）+ `competitive-strategy`；AI 产品加调 `ai-product-strategy`。

**并行建议**：3 个以上竞品时派 `competitive-agent`；需要外部市场数据时派 `research-agent`。

**产出**（写入 `strategy.md`）：
- ICP（理想客户画像）
- JTBD / 核心问题
- Positioning
- Alternatives（用户今天的替代方案，包括"什么都不做"）
- Competitive Landscape
- Differentiation
- Strategic Wedge（切入点）
- Product Thesis（一段话：我们相信【洞察】，因此为【ICP】做【产品】，凭【差异化】赢，从【wedge】切入）
- Strategic Risks

**Gate**：
1. Thesis 中每个核心假设都显式列在 `assumptions.md`（含验证状态）
2. Competitive Landscape 至少覆盖 3 个直接竞品 + 1 个替代方案（含 status quo）
3. Differentiation 回答了"为什么竞品不跟进就碾压我们 / 跟进了我们为什么还能赢"

---

## PRIORITIZATION

**目标**：排序 **问题与机会**，不是排序功能。

**调用**：`prioritization-frameworks`。

**场景选型**（禁止机械使用单一模型）：
- 机会多、证据足 → Opportunity Score
- 资源受限、需跨团队比较 → RICE
- 快速粗排 → ICE
- 早期探索、方向未定 → Value / Effort
- 高不确定性、赌博式投入 → Risk / Reward

**输入**：evidence.md（已验证问题）+ strategy.md（战略方向）。

**产出**（写入 `strategy.md` 优先级区块）：
- 排序后的问题/机会列表（含分数、所用框架、选择理由）
- 明确的"本轮不做"清单及理由

**Gate**：每个进入排序的对象都能追溯到 evidence.md 的证据或 strategy.md 的战略主张；无来源的功能项一律退回。

---

## DEFINITION

**目标**：产出一份继承全部上游、可交给工程的 PRD。

**调用**：`prd-development`。

**输入（必须显式注入）**：Discovery 证据 + Strategy + Priorities + Constraints。禁止凭空生成 PRD。

**PRD 至少包含 14 要素**：Problem / Evidence / Users / JTBD / Goals / Non-goals / Requirements / User Journey / Edge Cases / Constraints / Success Metrics / Risks / Open Questions /（第 14 项）Assumptions 与验证状态。

**产出**：PRD 文档 + `assumptions.md`、`decisions.md` 更新。

**Gate**：
1. 14 要素齐全
2. 每条 Requirement 可追溯到证据或优先级决策
3. **无证据的假设一律标注 `⚠️ UNVALIDATED`，不得写成事实**
4. Non-goals 非空（没有 Non-goals 的 PRD 说明没做取舍）

---

## PLANNING

**目标**：把优先级转化为表达战略意图的 Outcome Roadmap。

**调用**：`outcome-roadmap`。

**表达层级**：Outcome → Opportunity → Initiative → Experiment / Feature。

**禁止形态**：`Q1 做功能 A / Q2 做功能 B / Q3 做功能 C` 这种纯功能日历。

**产出**：roadmap.md（含每条 initiative 对应的 outcome 与衡量方式）。

**Gate**：每条 roadmap 项都能回答"成功时哪个指标会动、动了多少算成功"。

---

## VALIDATION

**目标**：在投入执行前系统性地找死法。

**调用**：`pre-mortem`。重大 PRD 建议同时派 `product-red-team` 独立挑战。

**方法**：假设项目**已经失败**，倒推死因。

**倒推维度**：最大失败原因 / 错误假设 / 用户风险 / 市场风险 / 技术风险 / 商业风险 / 组织风险 / 依赖风险。

**产出**：Risk Register（写入 `risks.md`），每条风险含：描述、概率、影响、类别、缓解方案、责任人、是否 launch-blocking。

**Gate**：所有 launch-blocking 风险必须有已商定的缓解方案。**存在未缓解的 launch-blocking 风险 → 强制回退**：
- 风险源于证据不足 → 回 DISCOVERY
- 风险源于战略方向 → 回 STRATEGY
- 风险源于定义缺陷 → 回 DEFINITION（PRD）

---

## MEASUREMENT

**目标**：建立上线前就定义好的、能支持决策的指标体系。

**调用**：`metrics-dashboard`。

**定义范围**：North Star Metric / Input Metrics / Leading & Lagging Indicators / Guardrail Metrics / Adoption / Activation / Retention / Engagement / Revenue / Quality。

**核心约束——每个核心指标必须对应三链**：

```
Metric → Hypothesis（这个指标动了对业务意味着什么）
       → Decision（指标涨/跌/不动时分别做什么决策）
```

**禁止**：Vanity Metrics（下载量、注册数等只涨不指导决策的指标不得作为核心指标）。

**产出**：metrics.md（指标定义、数据源、看板结构、告警阈值）+ Expected 基线（供 LEARNING 阶段比对）。

**Gate**：三链完整率 100%（核心指标缺 Hypothesis 或 Decision 的补齐前不放行）。

---

## MEASUREMENT 上线与 LEARNING

**LEARNING 触发输入**：真实数据 + 用户反馈 + 实验结果 + 市场变化 + 竞争变化。

**流程**：见 `learning-loop.md`（Expected vs Actual → 四类 Gap 归因 → 回退决策）。

**Gate**：本次 Learning 必须产出：Gap 归因（至少一类）、明确的回退/前进决策、新的 Hypothesis。
