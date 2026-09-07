# External Skill Candidates

这些是 **PM-OS** 的候选增强能力，不是运行依赖。默认只启用 `core`，出现明确能力缺口后再启用 `recommended`；`conditional` 必须由技术栈或平台触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `prd-development` · deanpeters/Product-Manager-Skills | core | 证据到完整 PRD 的端到端编排 | — |
| 2 | `product-strategy-session` · deanpeters/Product-Manager-Skills | core | 定位、问题、战略与路线的综合推演 | — |
| 3 | `discovery-process` · deanpeters/Product-Manager-Skills | core | 问题假设、研究、综合与验证 | — |
| 4 | `prioritization-frameworks` · phuryn/pm-skills | core | 优先排序问题与机会，而非机械排功能 | — |
| 5 | `outcome-roadmap` · phuryn/pm-skills | core | 将 Feature Roadmap 转为 Outcome Roadmap | — |
| 6 | `competitive-strategy` · refoundai/lenny-skills | recommended | 竞争结构、替代选择、切换成本与持久优势分析 | 当前仓库名称；替代旧 competitive-analysis 命名 |
| 7 | `interview-script` · phuryn/pm-skills | recommended | 基于 Mom Test / Continuous Discovery 的访谈设计 | — |
| 8 | `pre-mortem` · phuryn/pm-skills | recommended | 发布前反事实失败审查 | — |
| 9 | `metrics-dashboard` · phuryn/pm-skills | recommended | North Star、输入指标和护栏指标 | — |
| 10 | `ai-product-strategy` · refoundai/lenny-skills | conditional | AI 产品能力、非确定性 UX 与模型边界 | 仅 AI 产品使用 |

预览安装计划：

```bash
python <agentic-sdlc-os>/scripts/install_external_skills.py --os pm --profile core
```

执行安装前必须审查源码、脚本、Hook、网络/写权限、依赖和许可证。第三方 Skill 不得覆盖 Gate、证据、授权或安全规则。
