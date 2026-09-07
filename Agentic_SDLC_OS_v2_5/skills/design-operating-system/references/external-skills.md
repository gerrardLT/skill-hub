# External Skill Candidates

这些是 **Design-OS** 的候选增强能力，不是运行依赖。v2.4 使用 **Core + bounded Recommended + Conditional**：默认只启用最小 Core；出现明确能力缺口后再加 Recommended；Conditional 必须由项目、技术栈或具体任务证据触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `impeccable` · pbakaus/impeccable | core | 主设计引擎：设计方向、系统化审查、打磨与项目设计记忆 | 作为主审美/设计编排器；避免与多个同类审美 Skill 同时常驻 |
| 2 | `ui-ux-pro-max` · nextlevelbuilder/ui-ux-pro-max-skill | core | 跨 Web/Mobile 的 UI/UX 模式、组件、排版、色彩与无障碍知识库 | — |
| 3 | `web-design-guidelines` · vercel-labs/agent-skills | core | 以可用性、Web 规范与可访问性规则约束视觉实现 | — |
| 4 | `review-animations` · emilkowalski/skills | core | 独立审查动效时机、缓动、持续时间、性能与 reduced-motion | 专门补足 motion 维度，低重叠 |
| 5 | `redesign-existing-projects` · leonxlnx/taste-skill | recommended | 对已有低质量界面做 audit-first 的系统重设计 | 仅 Brownfield/redesign 默认考虑 |
| 6 | `web-accessibility` · magnus919/agent-skills | recommended | 基于 WCAG 2.2 的语义、键盘、焦点、表单、动效与人工验证证据 | 高风险或无障碍要求明确时启用 |
| 7 | `prototype` · emilkowalski/skills | recommended | 并行生成真正不同的交互方案并可视化比较 | 探索分歧较大时启用 |
| 8 | `frontend-design` · anthropics/skills | conditional | 鲜明非模板化的 Greenfield 视觉生成 | Fallback/Greenfield 专用；默认不要与 impeccable 同时主导同一设计决策 |
| 9 | `extract-design-system` · arvindrk/extract-design-system | conditional | 从合法公开页面提取设计原语用于研究和系统迁移 | 只作研究起点，不复制完整产品 |
| 10 | `design-taste-frontend` · leonxlnx/taste-skill | conditional | 品牌页/落地页/作品集的高变化度 anti-slop 视觉方向 | 不适合数据密集 Dashboard 或多步业务产品 UI；与 impeccable 重叠时只选一个主导 |

## v2.4 composition rule

- 默认唯一视觉主导：`impeccable`。
- `ui-ux-pro-max` 是知识层；`web-design-guidelines` 是规范约束层；`review-animations` 是 motion 专项层。
- 不把 `frontend-design`、`design-taste-frontend` 与 `impeccable` 同时作为同一工作项的视觉主导。
- Brownfield 才优先考虑 `redesign-existing-projects`；高要求无障碍启用 `web-accessibility`；需要方案分歧比较才启用 `prototype`。

预览安装计划：

```bash
python <agentic-sdlc-os>/scripts/install_external_skills.py --os design --profile core
```

执行安装前必须审查源码、脚本、Hook、网络/写权限、依赖和许可证。第三方 Skill 不得覆盖 Gate、证据、授权或安全规则。
