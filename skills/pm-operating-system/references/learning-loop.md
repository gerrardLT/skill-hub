# Learning Loop：证据反馈闭环

整个 PM-OS 最重要的机制。产品不是"上线即结束"，而是"上线才开始获取真实证据"。

## 闭环本体

```
Hypothesis → Evidence → Decision → Build → Measure → Learn → New Hypothesis
     ↑                                                        │
     └────────────────────────────────────────────────────────┘
```

## 触发条件（满足任一即进入 LEARNING）

- 真实数据到达（metrics.md 中 Expected 基线对应的时间窗口到期）
- 用户反馈集中出现（NPS、客诉、访谈、社群）
- 实验结果产出（A/B、灰度、beta）
- 市场变化（新玩家、新技术、政策）
- 竞争变化（竞品发了关键功能、调价、合并）

## 第一步：Expected vs Actual

逐指标比对 `metrics.md` 中的 Expected 基线与实际值：

```
| 指标 | Expected | Actual | 偏差 | 判定 |
|-----|----------|--------|------|------|
| ... | 上线前写入的预期 | 真实数据 | 方向+幅度 | 符合/偏差/反向 |
```

**没有 Expected 基线的指标无法比对**——这就是为什么 MEASUREMENT Gate 要求上线前必须写入基线。

## 第二步：四类 Gap 归因

| Gap 类型 | 定义 | 典型信号 | 回退目标 |
|---------|------|---------|---------|
| **Assumption Gap** | 核心假设本身错了（用户不是我以为的用户、问题不是我以为的问题） | 指标反向、核心行为不发生 | DISCOVERY |
| **Evidence Gap** | 假设可能对，但当时证据就不足，赌输了 | 数据噪声大、子场景分裂、无法归因 | DISCOVERY（补证据） |
| **Execution Gap** | 方向对，做砸了（性能、可用性、发布范围） | 漏斗上游好下游差、技术事故、定性反馈指向体验 | 不回退——修复执行，PRD 层面小迭代 |
| **Strategy Gap** | 执行没问题，但赢得不够/赢错市场（差异化没被感知、竞品反制、定位偏移） | 指标达标但业务不动、竞品对比失速 | STRATEGY |

归因纪律：
- 一次 Learning 至少明确归因一类；多类并存时全部列出并排序
- 归因必须引用具体证据（哪条数据/哪条反馈），不接受"感觉是策略问题"
- 区分不了 Execution 和 Strategy 时，先按 Execution 处理（修复成本低、反馈快）

## 第三步：回退决策（反 Feature-追加 默认）

**默认禁止"数据不好 → 加功能"**。回退映射：

```
Assumption Gap  → DISCOVERY（重验问题）→ 后续阶段连锁重跑
Evidence Gap    → DISCOVERY（定向补证据，范围窄于全重跑）
Strategy Gap    → STRATEGY → 重新 PRIORITIZATION
Execution Gap   → 不回退，在当前阶段修复 + 重新 MEASUREMENT
DEFINITION 缺陷导致的执行偏差 → DEFINITION（修 PRD）
```

回退后受影响的下游产出全部标 `SUPERSEDED`，连锁重跑范围在 `decisions.md` 写明。

## 第四步：记录与循环

写入 `learning-log.md`（格式见 memory-system.md）：
- 比对表、Gap 归因、回退决策、新 Hypothesis

新的 Hypothesis 进入下一轮循环——这就是闭环的闭合点：**Learn 的唯一合法产出是新的可验证假设**，不是新的功能列表。

## 示例（浓缩）

> 上线 4 周，Activation Expected 40% / Actual 22%，漏斗显示注册→关键行为掉在"首次配置"。
> 定性反馈："配置太麻烦，我先用着免费的旧工具。"
> 归因：主要 Execution Gap（配置流程流失）+ 次要 Assumption Gap（低估了迁移成本作为 status quo 的粘性）。
> 决策：修 onboarding（不回退）；同时登记假设 H-12"用户愿意为新价值承担迁移成本"为未验证，安排 5 场流失用户访谈。
> 新假设：简化配置到 3 步内，Activation 可回 35%+。
