# 动态路由：Skill Router

**核心原则：不按固定顺序调用全部 skill。按任务实际状态路由。**

## 路由算法（每次任务执行）

```
1. INTAKE 识别（必做）
     ↓
2. 对照 .product/ 与用户提供材料，判断每个阶段的完成状态：
     DONE（有产出且有证据链）/ PARTIAL（有产出但 Gate 未过）/ TODO / SKIPPED
     ↓
3. 找到第一个非 DONE 的关键阶段作为切入点
     ↓
4. 根据任务目标（见下方场景表）确定本次执行的阶段序列
     ↓
5. 向用户展示：切入点 + 序列 + 预计调用哪些 skill + 为什么，确认后执行
```

## 判断"材料充分可跳过"的标准

一个阶段可标记 SKIPPED 当且仅当：该阶段的产出物已存在（文档或 `.product/` 记录中）**且** 其 Gate 当时已通过或本次快速复核通过。只"做过"但 Gate 没过的是 PARTIAL，不是 SKIPPED。

## 场景路由表

| 用户任务特征 | 切入点 | 执行序列 | 不需要 |
|-------------|--------|---------|--------|
| 从 0 到 1，什么都还没有 | INTAKE | 全流程按序 | — |
| "帮我判断这个产品值不值得做" | DISCOVERY | Discovery → competitive-strategy → Strategy → Prioritization → pre-mortem | 直接生成 PRD |
| "需求已验证，做完整需求设计" | DEFINITION（先复核） | 复核 Discovery Evidence → prd-development → outcome-roadmap → pre-mortem → metrics-dashboard | 重新跑 Discovery 全流程 |
| "产品上线后数据不好" | MEASUREMENT | 读 metrics.md 比对 Expected vs Actual → Diagnose（Gap 归因）→ Discovery / Strategy（视 Gap 类型）→ 重新 Prioritization | 默认加新功能 |
| "帮我排下一阶段优先级" | PRIORITIZATION | 复核 evidence/strategy → prioritization-frameworks | 全流程 |
| "上线前怕翻车" | VALIDATION | pre-mortem（+ product-red-team）→ 视风险回退 | 重写 PRD（除非风险源于 PRD） |
| "要一份访谈提纲" | 单环节 | 直接 interview-script，不走状态机 | 本 orchestrator |
| "做个竞品分析" | 单环节 | competitive-strategy（或 competitive-agent），结果写入 evidence.md | 本 orchestrator |
| "AI 产品该在哪用 AI" | 单环节/嵌入 STRATEGY | ai-product-strategy | — |

单环节任务直接用对应子 skill 即可，PM-OS 不接管；只有跨环节才需要本 orchestrator。

## 输入输出传递规则（阶段衔接）

上一阶段的这些产物**必须显式注入**下一阶段的输入：

| 传递物 | 从 | 到 | 用法 |
|--------|----|----|------|
| 已验证问题 + 证据引用 | DISCOVERY | STRATEGY | 战略必须建立在已验证问题上 |
| ICP / Thesis / 差异化 | STRATEGY | PRIORITIZATION | 排序的权重依据 |
| 优先级列表 + 约束 | PRIORITIZATION | DEFINITION | PRD 只定义优先级靠前的东西 |
| PRD + Risk Register 草稿 | DEFINITION/VALIDATION | PLANNING | roadmap 项对应 PRD scope |
| PRD + 指标三链 | DEFINITION | MEASUREMENT | 指标必须能衡量 PRD 的 Goals |
| Expected 基线 | MEASUREMENT | LEARNING | Expected vs Actual 比对的基准 |

实现方式：调度子 skill 时，把 `.product/` 中对应文件的关键内容（或文件路径，若子 skill 支持读文件）作为上下文一并传入，并在调用指令中明确"以下是从上游继承的输入"。
