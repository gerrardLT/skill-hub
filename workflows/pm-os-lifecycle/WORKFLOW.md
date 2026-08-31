# PM-OS Lifecycle（产品全生命周期流水线）

> 本文件是 PM-OS 的 workflow 视图。权威实现与全部细节在 **skill：`pm-operating-system`**（[skills/pm-operating-system/](../../skills/pm-operating-system/)），本文件不重复其内容。

## 触发条件

用户提出跨环节的产品管理任务：从 0 到 1、判断值不值得做、完整需求设计、上线后数据不好复盘等。单环节任务不走本流水线。

## 步骤序列（状态机）

| # | 阶段 | 调用 | 输入 | 产出 | Gate |
|---|------|------|------|------|------|
| 0 | INTAKE | pm-operating-system 自身 | 用户材料 + `.product/` 记忆 | context.md + 本次阶段序列 | G1 |
| 1 | DISCOVERY | discovery-process, interview-script | 假设与已知证据 | 已验证问题清单（evidence.md） | G2 |
| 2 | STRATEGY | product-strategy-session, competitive-strategy, (ai-product-strategy)；可派 competitive-agent / research-agent | 已验证问题 | Thesis + ICP + 差异化（strategy.md） | G3 |
| 3 | PRIORITIZATION | prioritization-frameworks | 证据 + 战略 | 排序后的问题/机会清单 | G4 |
| 4 | DEFINITION | prd-development；可派 evidence-agent 复核 | 全部上游产出 | PRD（14 要素） | G5 |
| 5 | PLANNING | outcome-roadmap | PRD + 优先级 | Outcome Roadmap（roadmap.md） | G6 |
| 6 | VALIDATION | pre-mortem；可派 product-red-team | PRD + Roadmap | Risk Register（risks.md） | G7（上线前总闸） |
| 7 | MEASUREMENT | metrics-dashboard | PRD Goals | 指标三链 + Expected 基线（metrics.md） | G8 |
| 8 | LEARNING | pm-operating-system 自身 | 真实数据 + 反馈 + 市场变化 | Gap 归因 + 回退决策 + 新假设 | G9 |

阶段允许跳过（INTAKE 判定材料充分）与回退（Gate 失败 / Learning Loop 触发），实际序列按 `references/router.md` 动态路由。

## 失败分支

- 任一 Gate FAIL：按 `references/gates.md` 的回退映射回退（证据不足→DISCOVERY，方向错误→STRATEGY，定义缺陷→DEFINITION）
- 子 skill 产出两次不达标：中止流水线，向用户呈报缺口
- 连续 2 次回退到同一阶段：判定为结构性障碍，暂停并呈报
