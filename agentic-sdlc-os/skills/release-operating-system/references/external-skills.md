# External Skill Candidates

这些是 **Release-OS** 的候选增强能力，不是运行依赖。默认只启用 `core`，出现明确能力缺口后再启用 `recommended`；`conditional` 必须由技术栈或平台触发。

| Rank | Skill | Tier | Role | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `ship` · garrytan/gstack | core | 从验证、同步到 PR 的发布执行 | gstack 为整套安装，令牌开销较高；仅 Claude Code / 支持环境启用 gstack is installed as a suite; run setup once. |
| 2 | `land-and-deploy` · garrytan/gstack | recommended | 合并、部署与发布状态闭环 | gstack is installed as a suite; run setup once. |
| 3 | `canary` · garrytan/gstack | recommended | 金丝雀验证与异常阻断 | gstack is installed as a suite; run setup once. |
| 4 | `deploy-to-vercel` · vercel-labs/agent-skills | conditional | Vercel 部署与结果检查 | 仅 Vercel |
| 5 | `vercel-optimize` · vercel-labs/agent-skills | conditional | Vercel 上线后的性能与配置优化 | 仅 Vercel |
| 6 | `wrangler` · cloudflare/skills | conditional | Cloudflare Workers 部署、环境、Secrets、版本与回滚 | 仅 Cloudflare Workers 项目 |
| 7 | `azure-reliability` · microsoft/azure-skills | conditional | Azure PaaS 高可用、健康探针与跨区恢复 | 仅支持清单声明的 Azure 服务 |
| 8 | `azure-kubernetes` · microsoft/azure-skills | conditional | AKS/Kubernetes 部署知识 | 仅 Azure/AKS |
| 9 | `github-actions-hardening` · github/awesome-copilot | core | CI/CD 安全强化 | — |
| 10 | `sentry-setup-releases` · getsentry/plugin-claude | recommended | 为发布建立 Sentry release、deploy、commit 关联与验证 | 需要完整 MCP 能力时优先采用 Sentry 官方平台插件 |

预览安装计划：

```bash
python <agentic-sdlc-os>/scripts/install_external_skills.py --os release --profile core
```

执行安装前必须审查源码、脚本、Hook、网络/写权限、依赖和许可证。第三方 Skill 不得覆盖 Gate、证据、授权或安全规则。
