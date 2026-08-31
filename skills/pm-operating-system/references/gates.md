# Stage Gates：判定细则与回退规则

Gate 是阶段间的硬检查点。本文是各 Gate 的可执行判定标准。

## 通用规则

1. Gate 判定由 orchestrator（本 skill）执行，不由产出该阶段的子 skill 自评——避免"运动员兼裁判"
2. Gate 结果三值：**PASS**（放行）/ **CONDITIONAL**（放行但登记遗留项到 `decisions.md`，仅限低风险缺口）/ **FAIL**（回退或补做）
3. 每次 Gate 判定记录到 `decisions.md`：阶段、结果、依据、遗留项
4. 重大 Gate（DISCOVERY、DEFINITION、VALIDATION）建议派 `evidence-agent` 或 `product-red-team` 独立复核

## 各阶段 Gate 判定表

### G1：INTAKE → 后续

| 检查项 | PASS 条件 |
|--------|----------|
| 9 项识别 | 全部显式回答（"未知"也算回答） |
| 最大未知量 | 已识别且唯一聚焦 |

### G2：DISCOVERY → STRATEGY

| 检查项 | PASS 条件 |
|--------|----------|
| 问题证据 | ≥1 个核心问题同时有用户证据 + 行为证据 |
| 访谈质量 | Mom Test 合规（无引导、无推销、问过去） |
| 因果链 | 证据 → 问题的推理成立，无"提及即需求" |
| 假设管理 | 未验证假设全部在 `assumptions.md` 登记 |

**FAIL 动作**：禁止进入大规模 Solution Design；列出证据缺口（缺什么类型的证据、找谁补、怎么补）。

### G3：STRATEGY → PRIORITIZATION

| 检查项 | PASS 条件 |
|--------|----------|
| Thesis 假设显式化 | Thesis 每个核心假设都在 `assumptions.md` 有条目与状态 |
| 竞争覆盖 | ≥3 直接竞品 + ≥1 替代方案（含 status quo） |
| 差异化可辩护 | 能回答"竞品跟进后我们凭什么继续赢" |

### G4：PRIORITIZATION → DEFINITION

| 检查项 | PASS 条件 |
|--------|----------|
| 排序对象 | 是问题/机会，不是功能 |
| 可追溯 | 每个排序项可指回 evidence.md 或 strategy.md |
| 取舍 | 存在明确的"不做"清单 |

### G5：DEFINITION → PLANNING

| 检查项 | PASS 条件 |
|--------|----------|
| 14 要素 | 齐全（Problem/Evidence/Users/JTBD/Goals/Non-goals/Requirements/User Journey/Edge Cases/Constraints/Success Metrics/Risks/Open Questions/Assumptions） |
| 需求追溯 | 每条 Requirement 有证据或优先级来源 |
| 事实纪律 | 无"假设写成事实"；无证据项全部带 `⚠️ UNVALIDATED` |
| Non-goals | 非空 |

### G6：PLANNING → VALIDATION

| 检查项 | PASS 条件 |
|--------|----------|
| Outcome 表达 | 层级为 Outcome→Opportunity→Initiative→Experiment/Feature |
| 可衡量 | 每项能回答"哪个指标动、动多少算成功" |
| 无功能日历 | 不存在裸的"Q1 功能 A"表述 |

### G7：VALIDATION → MEASUREMENT（上线前总闸）

| 检查项 | PASS 条件 |
|--------|----------|
| Risk Register | 八类风险维度都有检查记录（用户/市场/技术/商业/组织/依赖/错误假设/最大失败原因） |
| Launch-blocking | 全部有已商定的缓解方案 |

**FAIL 动作（强制回退映射）**：

| 风险根源 | 回退到 |
|---------|--------|
| 证据不足 | DISCOVERY |
| 战略方向错误 | STRATEGY |
| 定义缺陷 | DEFINITION（PRD） |

### G8：MEASUREMENT → LEARNING（上线）

| 检查项 | PASS 条件 |
|--------|----------|
| 三链完整 | 每个核心指标有 Metric→Hypothesis→Decision |
| Expected 基线 | 上线前已在 `metrics.md` 写入预期值（含时间窗口） |
| 无 vanity | 核心指标中无纯虚荣指标 |

### G9：LEARNING → 回退/前进

| 检查项 | PASS 条件 |
|--------|----------|
| Gap 归因 | Assumption/Evidence/Execution/Strategy 四类至少明确归因一类 |
| 决策 | 明确的回退目标阶段或前进决策，记录进 `decisions.md` |
| 新假设 | 产出至少一条新的可验证 Hypothesis |

## 回退的通用纪律

- 回退时被否决的产出标记 `SUPERSEDED (原因, 日期)`，**不删除**——保留决策考古线索
- 回退原因、目标阶段、触发证据写入 `decisions.md`
- 连续 2 次回退到同一阶段 → 升级为根本问题，暂停流水线向用户呈报结构性障碍
