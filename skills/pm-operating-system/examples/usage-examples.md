# PM-OS 使用示例

> 配合 `SKILL.md`（职责与执行协议）、`references/router.md`（路由表）阅读。本文示范三类典型任务的实际走法。

## 如何触发

在**产品项目**中用自然语言直接说任务即可，PM-OS 按语义自动接管：

- 跨环节任务（从 0 到 1、值不值得做、完整需求设计、上线复盘）→ 触发 `pm-operating-system`
- 单环节任务（"要一份访谈提纲"、"做个竞品分析"）→ 直接路由到对应子 skill，不启动状态机
- 每次执行前 PM-OS 自动读取产品项目的 `.product/` 记忆；首次自动初始化

---

## 示例 1：「帮我判断这个产品值不值得做」

**任务特征**：0→1 决策，没有证据，不该直接产出 PRD。

**路由**（按 router.md）：

```
DISCOVERY → competitive-strategy → STRATEGY → PRIORITIZATION → pre-mortem
（不需要：prd-development、outcome-roadmap、metrics-dashboard）
```

**执行**：

1. INTAKE：识别 9 项 → 初始化 `.product/`，登记现有材料与最大未知量
2. DISCOVERY：`interview-script` 生成 Mom Test 提纲 → 用户完成访谈后回填；`discovery-process` 综合
   - G2 检查：核心问题需同时有用户证据 + 行为证据；不过则列证据缺口，到此为止
3. STRATEGY：`competitive-strategy` 拆竞品与 status quo（3+ 竞品时可派 `competitive-agent` 并行）
   → `product-strategy-session` 产出 Thesis / ICP / 差异化
4. PRIORITIZATION：`prioritization-frameworks` 排序问题/机会（如 Opportunity Score）
5. VALIDATION（轻量）：`pre-mortem` 假设已失败，倒推最大死因

**决策摘要（示意）**：

> Go / No-Go / 有条件 Go + 前提条件清单（需要补的证据、必须成立的假设 H-xx）、最大风险 R-xx。
> 不产出 PRD——问题没被证明前，写 PRD 是浪费。

---

## 示例 2：「需求已经验证了，帮我做完整需求设计」

**任务特征**：声称已验证 → 先复核证据，再进入 DEFINITION。

**路由**：

```
复核 Discovery Evidence（evidence-agent）→ prd-development → outcome-roadmap → pre-mortem → metrics-dashboard
（不重跑 Discovery 全流程）
```

**执行**：

1. 读 `.product/`：evidence.md 是否支撑"已验证"声明
   - 派 `evidence-agent` 独立审计：事实/推断/假设逐句归类，访谈证据按 Mom Test 核验
   - 审计不通过 → 回 DISCOVERY 补证据，PRD 暂缓
2. DEFINITION：`prd-development`，输入显式注入证据、战略、优先级、约束
   - G5 检查：14 要素齐全；每条 Requirement 可追溯；无证据项标 `⚠️ UNVALIDATED`；Non-goals 非空
3. PLANNING：`outcome-roadmap` 把优先级转成 Outcome→Opportunity→Initiative→Experiment 层级
4. VALIDATION：`pre-mortem` 产出 Risk Register；重要 PRD 加派 `product-red-team` 独立挑战
   - G7：launch-blocking 风险全部有缓解方案，否则回退（证据不足→DISCOVERY / 方向错→STRATEGY / 定义缺陷→PRD）
5. MEASUREMENT：`metrics-dashboard` 建指标三链 + 上线前写入 Expected 基线

**决策摘要（示意）**：

> PRD 与 Roadmap 就绪，X 条 launch-blocking 风险已有缓解方案；
> Y 条需求基于未验证假设（H-xx 清单），建议上线前补验证；下一步进入执行。

---

## 示例 3：「产品上线 4 周了，数据不好」

**任务特征**：LEARNING 触发；默认禁止"加功能"，先归因。

**路由**：

```
读 metrics.md 比对 Expected vs Actual → Diagnose（四类 Gap 归因）→ 按 Gap 类型回退或修复 → 重新 PRIORITIZATION
```

**执行**：

1. 比对：逐指标 Expected vs Actual（依赖上线前写好的基线；缺基线的指标只能定性分析并补登记）
2. 归因（须引用证据编号 E-xx，不接受"感觉是策略问题"）：

| Gap | 判断信号 | 动作 |
|-----|---------|------|
| Assumption Gap | 指标反向、核心行为不发生 | 回 DISCOVERY 重验问题 |
| Evidence Gap | 噪声大、子场景分裂、无法归因 | DISCOVERY 定向补证据 |
| Execution Gap | 漏斗上游好下游差、体验类反馈 | 不回退，修执行 + 重新 MEASUREMENT |
| Strategy Gap | 指标达标但业务不动、竞品对比失速 | 回 STRATEGY → 重新 PRIORITIZATION |

3. 记录：比对表、归因、决策、新 Hypothesis 追加到 `learning-log.md`；回退决策与 SUPERSEDED 标记记入 `decisions.md`

**决策摘要（示意）**：

> Activation Expected 40% / Actual 22%，流失集中在首次配置。
> 归因：主要 Execution Gap（修复 onboarding，不回退）+ 次要 Assumption Gap（H-12"用户愿为价值承担迁移成本"未验证，安排 5 场流失访谈）。
> 新假设：配置≤3 步，Activation 回 35%+。本轮不加新功能。
