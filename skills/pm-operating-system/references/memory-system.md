# 项目记忆系统：`.product/`

产品项目的长期记忆。**orchestrator 每次执行前读取，每次重大决策后更新。**

## 位置与初始化

- 位置：当前产品项目的仓库根目录 `.product/`（不是 skills-hub）
- 初始化：首次运行时从本 skill 的 `templates/product/` 复制
- 约定：`.product/` 提交到产品项目 git（它就是产品决策历史的载体）

## 文件清单与更新时机

| 文件 | 内容 | 更新时机 |
|------|------|---------|
| `context.md` | INTAKE 9 项 + 当前阶段 + 项目一句话 | 每次 INTAKE；阶段变更时 |
| `evidence.md` | 全部证据：来源、类型（用户/行为/市场）、质量、支撑的问题 | 每次获得新证据（skill 产出、访谈、subagent 报告） |
| `assumptions.md` | 假设登记簿：编号、内容、状态（未验证/验证中/已验证/已推翻）、验证方式 | 任何阶段产生新假设或状态变化 |
| `decisions.md` | 决策日志：Gate 判定、阶段跳过/回退、取舍决策、SUPERSEDED 标记 | 每次决策后立即追加（只追加不修改） |
| `strategy.md` | ICP/JTBD/Positioning/竞争/差异化/Thesis/战略风险 + 优先级区块 | STRATEGY、PRIORITIZATION 阶段 |
| `roadmap.md` | Outcome 型路线图 | PLANNING 阶段及后续调整 |
| `metrics.md` | 指标三链 + Expected 基线 + 看板定义 | MEASUREMENT 阶段；LEARNING 比对时只读 |
| `risks.md` | Risk Register | VALIDATION；重大新风险随时 |
| `learning-log.md` | Learning 记录：比对表、Gap 归因、回退决策、新假设 | 每次 LEARNING |

## 使用规则

1. **读**：执行协议第 1 步全量读取；判断阶段状态（DONE/PARTIAL/TODO/SKIPPED）以这些文件为准
2. **写**：谁产出谁登记——skill 产出由 orchestrator 摘要写入；subagent 报告回收后写入对应文件
3. **不覆盖历史**：`decisions.md` 与 `learning-log.md` 只追加；被推翻的结论在原文档标 `SUPERSEDED` 后新开条目
4. **证据引用格式**：所有文档中引用证据一律用 `evidence.md` 的编号（如 `E-07`），保证可追溯
5. **假设引用格式**：同上，用 `H-01` 式编号引用 `assumptions.md`

## 与 Subagent 的数据交换

派发 subagent 时传入：`context.md`（必）+ 与任务相关的文件（如 competitive-agent 附 `strategy.md`）。
回收时要求 subagent 按固定结构返回报告，由 orchestrator 写入记忆，**subagent 不直接写 `.product/`**（保持记忆一致性）。
