# 六步研发极简能力映射表

`dev-loop` 不硬编码具体方法论，直接调度当前环境中成熟的各领域首选技能，并支持同类能力的自然平替。

---

## 阶段能力映射矩阵

| 研发阶段 | 首选核心 Skill | 备选/平替 Skill | 核心交付物 |
|---|---|---|---|
| **① 需求** | `product-management:PRD生成` | `pm-output-engine:需求文档撰写` | `docs/prd.md` |
| **② 设计** | `ui-ux-pro-max-skill:ui-ux-pro-max` | `product-design:flow-web` / `impeccable` | `docs/design.md` |
| **③ 实现** | `superpowers:writing-plans`<br>`superpowers:test-driven-development` | 叠加 `andrej-karpathy-skills:karpathy-guidelines` | `src/` + 自动化单测 |
| **④ 验收** | `design-review:design-qa`<br>`superpowers:verification-before-completion` | `test-case-generator`<br>`playwright` (MCP) | `docs/qa-report.md` |
| **⑤ 交付** | `shipping-artifacts` | `architecture-visualization:architecture-communicator` | `docs/` 交付集 + `README.md` |
| **⑥ 复盘** | `superpowers:systematic-debugging`<br>`product-management:产品指标复盘` | `product-design:retro` | `docs/retro.md` (回流至①) |

---

## 调度与降级规则

1. **就地取材**：优先调度当前已就绪的成熟 Skill（superpowers、product-management 等）；
2. **平替降级**：若首选不可用，自动使用备选平替；
3. **极简兜底**：若均无对应子 Skill，主编排器按 `stages.md` 标准自产对应文档并标注 `⚠️ 降级执行`，流程永不中断；
4. **单步开箱**：用户单独说"帮我写 PRD"、"做一下验收走查"时，无需全流程前置要求，直接进入单步执行。
