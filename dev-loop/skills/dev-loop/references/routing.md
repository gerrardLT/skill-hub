# 场景路由表

每步先按"首选"调用；命中特定场景时切换到对应备选。**所有 skill 名以本表为准，逐字使用**。被调度的 skill 不存在时，执行该步兜底（见 [stages.md](stages.md) 各步末尾）。

## ① 需求

| 场景 | 调用 |
|------|------|
| **默认：产出正式 PRD** | `product-management:PRD生成` |
| 方向不明，需要先发散 | `product-management:产品脑暴` |
| 已有方向，要拆用户故事 | `product-management:用户故事拆解` |
| 需求太多，要排序取舍 | `product-management:需求优先级排序` |
| 需要竞品参照定位 | `product-management:竞品分析` |
| 拿到别人的 PRD 要做设计 | `product-design:scope`（设计侧解读，归②前置） |

兜底：编排器自产 1 页 PRD（问题 / 用户 / 场景 / 验收标准 / 非目标）。

## ② 设计

| 场景 | 调用 |
|------|------|
| **默认入口锚点：设计简报** | `product-design:brief` |
| Web 端多屏流程 | `product-design:flow-web` |
| 移动端 / H5 多屏流程 | `product-design:flow-mobile` |
| 只要信息架构 / 页面结构 | `product-design:sitemap` |
| 视觉方向 / 设计系统起点 | `product-design:board` |
| 数据看板 / 图表页 | `product-design:chart` |
| 补全异常态（空/错/载/权限/离线） | `product-design:edge` |
| 细化打磨已有界面 | `impeccable` |
| 需要跨平台规范速查 | `ui-ux-pro-max-skill:ui-ux-pro-max` |

典型组合：`brief` 先行 → 按平台选 `flow-web` / `flow-mobile` → `edge` 补异常态；视觉用 `board`，图表页加 `chart`。

兜底：编排器自产 1 页设计说明（页面清单 + 每页关键状态 + 交互要点 + 导航结构）。

## ③ 实现

| 场景 | 调用 |
|------|------|
| **默认：主 agent 直接编码** | 遵循 `andrej-karpathy-skills:karpathy-guidelines`（克制、外科手术式修改、可验证） |
| 查库 / 框架 API 用法 | `context7:context7-mcp` |
| 写 SQL | `sql-queries` |
| 造测试数据 | `dummy-dataset` |

兜底：本身就是兜底——主 agent 按②的设计规格逐条实现 + 自测。

## ④ 验收

| 场景 | 调用 |
|------|------|
| **默认：设计还原度核查** | `product-design:qa` |
| 像素级对齐设计稿 | `design-review:ui-alignment-review` |
| 无障碍（WCAG） | `design-review:accessibility-review` |
| 视觉回归（对比基线图） | `design-review:visual-regression-review` |
| 生成测试用例 | `test-case-generator` |
| 怀疑实现偏离意图 | `intended-vs-implemented` |
| 设计整体走查 | `product-design:check` |
| 真实用户可用性测试 | `product-design:test` |

兜底：编排器按 PRD 验收标准逐条人工核对，产出核对表。

## ⑤ 交付

| 场景 | 调用 |
|------|------|
| **默认：可审查交付文档集** | `shipping-artifacts`（架构 / 流程 / 权限 / 测试覆盖） |
| 工程交接 PRD | `product-design:prd` |

兜底：编排器从代码扫描自产 README + 架构说明。

## ⑥ 复盘

| 场景 | 调用 |
|------|------|
| **默认：项目复盘（决策 vs 结果）** | `product-design:retro` |
| 数据指标复盘 | `product-management:产品指标复盘` |
| 用户反馈分析 | `product-management:用户反馈分析` |
| 更新路线图 | `product-management:路线图更新` |

兜底：编排器自产 Expected vs Actual 对比 + 3 条行动项。
