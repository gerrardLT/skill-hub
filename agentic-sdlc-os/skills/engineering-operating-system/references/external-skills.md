# External Skill Candidates

这些是 **Engineering-OS** 的候选增强能力，不是运行依赖。默认只启用 `core`，出现明确能力缺口后再启用 `recommended`；`conditional` 必须由技术栈或平台触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `writing-plans` · obra/superpowers | core | 将规格拆成可验证的小步实施计划 | — |
| 2 | `test-driven-development` · obra/superpowers | core | 强制红-绿-重构和回归证据 | — |
| 3 | `systematic-debugging` · obra/superpowers | core | 先定位根因，再实施单一修复 | — |
| 4 | `requesting-code-review` · obra/superpowers | core | 使用独立上下文做代码审查 | — |
| 5 | `verification-before-completion` · obra/superpowers | core | 完成声明前必须有新鲜验证证据 | — |
| 6 | `executing-plans` · obra/superpowers | recommended | 按批次执行并在检查点复核 | — |
| 7 | `subagent-driven-development` · obra/superpowers | recommended | 将独立任务分派给隔离上下文并逐项审查 | — |
| 8 | `improve-codebase-architecture` · mattpocock/skills | recommended | 发现架构摩擦与深模块重构机会 | — |
| 9 | `codebase-design` · mattpocock/skills | recommended | 设计深模块、接口边界、可测试性与模块接缝 | 替代已废弃的 design-an-interface；包含 Design It Twice 参考 |
| 10 | `git-guardrails-claude-code` · mattpocock/skills | conditional | Git 操作与提交安全护栏 | — |

预览安装计划：

```bash
python <agentic-sdlc-os>/scripts/install_external_skills.py --os engineering --profile core
```

执行安装前必须审查源码、脚本、Hook、网络/写权限、依赖和许可证。第三方 Skill 不得覆盖 Gate、证据、授权或安全规则。
