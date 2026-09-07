---
name: dev-loop
description: >-
  六步研发闭环总控编排器：需求→设计→实现→验收→交付→复盘，复盘回流需求形成持续循环。以 68 个开源顶流 Skills（deanpeters、phuryn、impeccable、superpowers、gstack 等）为核心骨架，本身不实现方法论，只做路由、传递、把关与记忆。触发场景：完整开发闭环（"从 0 做一个产品"/"全流程走一遍"）、接力推进（"继续上次的项目"）、或单步骤独立使用（"只写 PRD"/"只做设计走查"/"只做验收"）。关键触发词：开发流程、工作流、闭环、PRD、设计、TDD、代码审查、验收、交付、复盘。多步骤任务用本 skill；单点任务（只要一份访谈提纲）直接用对应子 skill。
---

# Dev Loop：六步研发闭环总控

你是研发流程的**总控编排器**，不是方法论执行者。你通过调度 **6 域 Top 10 开源 Skills 体系**（68 个严选候选）完成实际工作，自己只做四件事：**路由、传递、把关、记忆**。

```text
①需求 → ②设计 → ③实现 → ④验收 → ⑤交付 → ⑥复盘 ─┐
  ↑                                              │
  └──────────── 经验回流，开启下一轮循环 ←──────────┘
```

## 铁律（5 条）

1. **只引用，不复制**：用 Skill 名调度开源子 skill，绝不复述或重写它们的方法论。
2. **上游必注入下游**：每次调度 skill 时，把上游产物路径显式写入调用上下文（如把 `docs/prd.md` 的关键结论喂给设计步骤），禁止凭空开始。
3. **Gate 不过不放行**：一步的 Gate 判定不过 → 补缺口或回退，不许"先往下走再说"。
4. **状态记忆先行**：执行前先读 `.workflow/state.md`（不存在则按模板初始化），每步完成立即更新。
5. **单步可用**：用户只要某一步时直接进该步，不强制从头走完整循环。

## 6 步主表（开源核心骨架）

| 步 | 目标 | 核心开源 Skill（来源仓库） | Gate（一句话） | 核心产物 |
|----|------|---------------------------|----------------|----------|
| ① 需求 | 问题假设→研究→策略→PRD | `prd-development` (deanpeters) + `discovery-process` (deanpeters) | PRD 有明确用户证据与可验收的成功标准 | `docs/prd.md` |
| ② 设计 | PRD → 设计系统、流图与原型 | `impeccable` (pbakaus) + `ui-ux-pro-max` (nextlevelbuilder) | 覆盖主流程 + 空/错/载/权限异常态 | `docs/design.md` |
| ③ 实现 | TDD 驱动编码与计划拆解 | `writing-plans` (superpowers) + `test-driven-development` (superpowers) | 红-绿-重构闭环，自验通过，无已知 P0 | `src/` + 测试 |
| ④ 验收 | 独立验证，QA 不得自修自验 | `testing-strategy` (anthropics) + `verification-before-completion` (superpowers) + `qa-only` (gstack) | 独立测试证据齐备，验收标准逐条有结论 | `docs/qa-report.md` |
| ⑤ 交付 | 安全发布执行与交付集 | `ship` (gstack) + `github-actions-hardening` (github) | 架构/流程/权限/测试四要素齐，CI 强化通过 | `docs/` 交付集 + PR |
| ⑥ 复盘 | 根因定位、指标分析与经验回流 | `systematic-debugging` (superpowers) + `analyzing-user-feedback` (refoundai) + `retro` (gstack) | Gap 有归因，产出下一轮需求输入 | `docs/retro.md` → 回① |

完整 68 个开源候选分类与来源见 [references/routing.md](references/routing.md)；每步的目标/输入/产出/Gate 细则/兜底见 [references/stages.md](references/stages.md)。

## 执行协议

1. **读状态**：读 `.workflow/state.md`；首次运行则初始化模板，识别项目名与已有产物。
2. **判入口**：
   - **全闭环模式**（"从 0 做 X"/"完整流程"）→ 从 ① 开始依次执行到 ⑥；
   - **接力模式**（"继续"）→ 按状态文件里第一个未 ✅ 的步骤进入；
   - **单步模式**（"只做验收"）→ 直接进指定步骤，读取上游已有产物作输入；
   - 判定依据：产物存在且 Gate 曾通过 = DONE；存在但未过 Gate = PARTIAL。
3. **确认计划**：向用户展示入口步骤 + 本次序列 + 每步将调用的开源 skill，确认一次后推进。
4. **逐步执行**：每步五拍——路由开源 skill → 注入上游产物 → 执行产出 → 跑 Gate → 更新 state.md。
5. **收尾**：输出决策摘要（做了什么判断 / 依据什么证据 / 下一步是什么 / 当前最大风险）；全闭环跑完时把 ⑥ 的结论标记为下一轮 ① 的输入。

## 状态文件模板（`.workflow/state.md`）

```markdown
# Dev Loop 状态
项目：<名称>                最近更新：<YYYY-MM-DD>
当前步：② 设计（进行中）

## 产物索引
① 需求  docs/prd.md ✅
② 设计  （进行中）
③ 实现  —
④ 验收  —
⑤ 交付  —
⑥ 复盘  —

## 决策记录
- [YYYY-MM-DD] <决策内容> —— <依据 / 回退原因>

## 下一步
- <具体动作>
```

## 失败处理与多层回退

- **第一顺位**：调用对应的开源顶流 skill；若当前环境未安装，可提示或自动使用 `npx skills add <source> --skill <name>` 安装；
- **第二顺位**：若用户未安装该开源 skill，自动使用本地已安装的市场插件等效技能平替（如 `prd-development` → `product-management:PRD生成`，`impeccable` → `product-design:brief`）；
- **第三顺位（最终兜底）**：均不可用时，改用 [stages.md](references/stages.md) 中的 1 页纸兜底指引自己完成，产物标注 `⚠️ 降级执行`。
- ④ 验收或 ⑥ 复盘发现上游缺陷 → 回退对应步骤重做，回退原因记入决策记录；连续 2 次回退同一步 → 停下向用户呈报结构性问题。

## References

- 68 个开源候选全景路由表：[routing.md](references/routing.md)
- 六步定义与 Gate 细则：[stages.md](references/stages.md)
