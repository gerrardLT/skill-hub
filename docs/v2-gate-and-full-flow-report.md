# V2 门禁层修复与完整流程打通报告

**日期**：2026-10-12
**范围**：修复阻断完整流程的 V2 门禁评估器断层，并打通阶段与复合配方执行
**结论**：**可以走完整流程。** 已用真实本地模型跑通阶段内多步与复合跨阶段编排，门禁全部可机器复算。

---

## 一、修复前阻断的问题

上一轮实测发现：配方能加载、能排序、能调用模型，但**每一步都在门禁处失败**。

根因：V1 配方的门禁是短 ID（`source-traceability` 等 11 个），执行器有对应的确定性评估器；V2 配方的门禁是给人看的散文句子。

| | V1 已发布配方 | V2 合并配方（修复前） |
|---|---|---|
| 门禁形态 | `source-traceability` | "Preserve conflicts, counterevidence, unknowns..." |
| 机器可评估 | 7 / 7 | **0 / 340** |

不认识的字符串一律返回 `no deterministic evaluator` → 每一步 fail-closed 失败。

---

## 二、修复方案：两层门禁

没有用「让模型自己判门禁」这种破坏确定性的做法，也没有硬把散文塞进正则假装能判。改成两层：

### 第一层：阻断型机器门禁（5 个，可复算）

由**契约自身的结构属性**推导，不解释散文：

| 门禁 | 检查什么 | 何时适用 |
|---|---|---|
| `status-declared` | 前 8 行内声明四种状态之一（容忍加粗/标题/列表写法） | 总是 |
| `non-execution-stated` | 必须说明「没有执行什么」——用「否定词 + 动作动词」模式匹配，而非固定短语 | 总是 |
| `unknowns-preserved` | 必须有**带标签的**未知/冲突/假设登记表（标题或 `UNK-1:` 形式），不是文中偶然出现「gap」 | 契约声明关心不确定性时 |
| `authority-named` | 必须出现**具权威含义**的表述（未授权/需批准/决策负责人），不是文中偶然出现「owner」 | 契约声明 human_decision 时 |
| `evidence-binding` | 必须绑定稳定标识（ID/哈希/文件路径） | 契约声明 provenance 时 |

关键点：`evidence-binding` **只在契约声明 provenance 时**适用。当成通用门禁会误杀合法散文交付物。

### 第二层：记录型建议门禁（340 条散文义务）

原散文门禁**一条没删**，改为 `advisory_gates`：

- 写入步骤证据，并随提示词交给模型（"OBLIGATIONS TO SATISFY"）；
- 进入交接产物，**由独立审查环节判定**，而不是被正则假装判定。

这保住了架构原则：语义判断交给独立审查，不用模型自报冒充证据。

---

## 三、门禁标定（用 304 份真实模型输出实测）

不是拍脑袋定阈值，而是拿已有的 304 份真实输出标定：

| 门禁 | 通过率 | 说明 |
|---|---|---|
| `non-execution-stated` | **300 / 304（99%）** | 抓到 4 份真的没说未执行 |
| `authority-named` | 119 / 168（71%） | 抓到 49 份没有权威引用 |
| `unknowns-preserved` | 129 / 184（70%） | 抓到 55 份没有未知登记表 |
| `status-declared` | 175 / 304（58%） | 低是因为评测提示词没要求状态行；执行器提示词要求，实测 100% 通过 |
| `evidence-binding` | 26 / 56（46%） | 只在声明 provenance 的能力上适用 |

**36% 的输出通过其全部适用门禁。** 负向对照（只有完成声明、无任何证据的输出）**每一个门禁都失败**。

标定过程中修掉了三个真实缺陷：
1. 初始版 `unknowns-preserved` 与 `authority-named` 通过率 100% —— 等于没抓任何东西，收紧为「带标签的登记表 / 具权威含义的表述」；
2. `evidence-binding` 把行内代码 `` `needs-input` `` 当标识符计数，且阈值过高 —— 移除该模式并收窄触发条件；
3. `non-execution-stated` 用固定短语表，误杀真实输出（它写的是 "does not implement … or claim completion"）—— 改为「否定词 + 动作动词」模式，通过率 80% → 99%。

---

## 四、顺带修掉的四个执行语义缺陷

### 1. 条件步骤没有按声明语义执行

127 个步骤声明 `activation: conditional` + `default_state: skipped`，27 个声明 `disabled-pending-current-authorization`。执行器却无条件跑全部步骤。

修正后：
- 条件步骤**默认跳过**，只有调用方点名才运行；
- `disabled-pending-current-authorization` **永不自动运行**，即使被点名；
- 什么都没激活时返回 `needs-input` **并附上可选步骤菜单**，而不是报失败。

### 2. 依赖解析找不到步骤

依赖记录引用的是**能力 ID**，而步骤现在以**模式 ID** 为键。修正为同时按 `skill` 与 `id` 建索引。

### 3. 把 `optional` 当排序边会造环

实测发现 `requirements → implementation → review → plan-execution → requirements` 成环。修正为：**只有 `hard` 排序**；`optional` 是「有就用、不等」，`feedback` 是「下一轮生命周期」——配方原文也这么写。

### 4. 阶段内没有顺序，由调用方决定

阶段是「条件步骤菜单」，不是固定流水线。修正为：调用方给出**有序**激活列表即按其顺序执行。此前 `set()` 会丢顺序，已改为传列表。

---

## 五、新增复合配方执行器

复合配方用的不是 `steps` 而是 `stage_steps` + `handoffs`，此前完全没有执行路径。新增 `execute_composite`：

- 按 `depends_on` 拓扑排序阶段（并修正 `stage-NN` 与 `stage:NN` 的命名不一致）；
- 逐阶段执行，产物向前传递；
- **强制校验交接契约四要素**（产物身份与哈希、决策与权威记录、完成证据、已知缺口与残余风险），缺一即阻断；
- 任一阶段未通过，**整个复合立即停止**，后续阶段绝不启动；
- 携带 `human_checkpoints` 记录。

---

## 六、实测结果（真实本地模型，非 mock）

### 单步

```
recipe: stage-01-governance-intake | steps: 1/3
status: passed | passed: True
  context-intake-and-routing    passed   gates 4/4  advisory 2
skipped: 2 step(s)
```

### 阶段内多步链

```
recipe: stage-01-governance-intake | steps: 2/3
status: passed | passed: True
model calls: 2 | tokens: 32,162
  context-intake-and-routing             passed   gates 4/4  advisory 2
  risk-preflight-and-safety-governance   passed   gates 4/4  advisory 2
skipped: 1 step(s)
```

### 复合跨阶段

```
composite: product-discovery-and-planning | stages: 4
status: needs-input | passed: False
  1. stage:01-governance-intake   needs-input  steps=1/3
stopped at: stage:01-governance-intake
errors: ['stage:01-governance-intake: needs-input']
```

复合在第一个阶段未通过时**正确停止**，未启动下游阶段。

### 一次值得记录的「正确失败」

复合首步 `ai-safety-and-action-governance` 返回 `needs-input`，理由是：

> 请求描述的是**非 AI** 的 HTTP 限流器（Redis 租户配额）。全部输入中没有任何模型、提示词、Agent、工具调用面。AI 相关的输出契约项**无法从所给证据评估**，我不会为了填满它而虚构一个 AI 组件。分类问题（本次变更是否引入/依赖 AI 组件）属于**可索要的事实**，负责人 Nadia Osei。

这是能力在**正确工作**：拒绝编造，点名缺失事实与负责人。

---

## 七、最终验证

| 检查 | 结果 |
|---|---|
| 回归测试 | **32 passed** |
| 优化候选门禁（154 目录） | **6 / 6 通过** |
| 结构自检（68 项） | **0 问题** |
| 阻断型门禁可评估率 | **565 / 565（0 不可评估）** |
| 建议门禁保留 | **340 条，一条未删** |
| Token 预算 | 41,037,872 / 50,000,000（余 8,962,128） |
| 未对账 partial | **0** |

---

## 八、现在的真实能力边界

**可以走完整流程**，但要说清「完整」的含义：

1. **可以**：按阶段与复合配方真实驱动模型执行、按模式装载能力文档、机器门禁判定、产物与状态落盘、交接契约校验、未通过即停止。
2. **可以**：调用方按任务选择适用步骤（这是设计语义，不是缺陷）。全选会跑到不适用的步骤并得到 `needs-input`。
3. **仍需**：完整的操作者输入。技能要求「未知项登记 + 负责人」，所以真实项目里 `needs-input` 是**常见且正确**的终态，不是故障。要走到 `passed` 需要补齐缺失事实。
4. **仍未验证**：一次从阶段 01 贯通到阶段 15 的完整项目（需要逐阶段补齐输入，属于多轮人机迭代）。本次验证到「阶段内多步通过」与「复合跨阶段编排与正确停止」。
5. **未发布**：`slots/v2/1.0.0` 与 `recipes/v2/1.0.0` 未改动，正式发布仍需独立批准。
6. **建议门禁未经独立审查**：340 条散文义务已随产物传递，但尚未接一个真实的独立审查环节去判定它们。
