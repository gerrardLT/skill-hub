# External Skill Candidates

这些是 **QA-OS** 的候选增强能力，不是运行依赖。v2.4 使用 **Core + bounded Recommended + Conditional**：默认只启用最小 Core；出现明确能力缺口后再加 Recommended；Conditional 必须由项目、技术栈或具体任务证据触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `testing-strategy` · anthropics/knowledge-work-plugins | core | 按业务风险设计测试层级、覆盖边界、环境、数据与退出标准 | — |
| 2 | `verification-before-completion` · obra/superpowers | core | 禁止没有新鲜可复现证据的完成/通过声明 | — |
| 3 | `qa-only` · garrytan/gstack | core | 独立的 report-only Web QA：截图、复现、健康分，不修改产品源码 | gstack 套件安装；QA-OS 只调用 qa-only，不调用会自行修复的 qa；安装器会去重 |
| 4 | `code-review` · anthropics/knowledge-work-plugins | core | 从 correctness/security/performance/maintainability 独立审查变更 | QA 只报告发现；产品源码修复归 Engineering |
| 5 | `playwright` · openai/skills | core | 真实浏览器交互、快照、截图、UI 流程与运行时证据 | 作为可靠执行层；不等同于测试策略 |
| 6 | `playwright-best-practices` · currents-dev/playwright-best-practices-skill | recommended | Playwright E2E、flaky、fixtures、selector、CI 和高级测试模式知识 | 2026-07 曾出现 skills CLI 丢失非标准引用目录的问题；启用前必须验证安装完整性，失败则保持禁用 |
| 7 | `web-accessibility` · magnus919/agent-skills | recommended | WCAG 2.2 导向的可访问性任务验证与证据记录 | 自动扫描不能单独给出 WCAG 合规结论 |
| 8 | `audit-website` · squirrelscan/skills | conditional | SEO、性能、安全、技术与无障碍综合扫描 | 需要额外 CLI；先审查权限与扫描行为 |
| 9 | `vitest` · antfu/skills | conditional | Vitest 项目的单元与集成测试知识 | 仅 Vitest 技术栈 |
| 10 | `github-actions-hardening` · github/awesome-copilot | recommended | 审查 CI 工作流脚本注入、权限与供应链风险 | CI 安全专项；不替代 Release-OS 的发布决策 |

## v2.4 separation-of-duties rule

- QA Core 负责：测试策略、独立验证、浏览器证据、独立代码审查。
- QA 可以修改测试、fixture、测试工具和报告；**不得修改产品源码来让自己的验收通过**。
- 产品源码修复路由到 Engineering，然后由独立 QA 复验。
- `test-driven-development` 与 `systematic-debugging` 保留在 Engineering 为主，不再作为 QA Core。
- `playwright-best-practices` 启用前必须检查安装资源完整性。

预览安装计划：

```bash
python <agentic-sdlc-os>/scripts/install_external_skills.py --os qa --profile core
```

执行安装前必须审查源码、脚本、Hook、网络/写权限、依赖和许可证。第三方 Skill 不得覆盖 Gate、证据、授权或安全规则。
