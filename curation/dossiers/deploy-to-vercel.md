# deploy-to-vercel 来源能力档案

## Problem

根据项目链接、Git remote、CLI 和认证状态选择最可持续的 Vercel 部署路径，并返回部署 URL。

## When to Use

用于部署应用、上线、创建 preview 或明确要求 production deployment。

## When Not to Use

不在未授权时 git push；默认不部署 production；不通过 curl/fetch 部署 URL 做验证。

## Role

Vercel 部署路径选择与执行器，优先建立项目链接和 git-push 自动部署。

## Inputs

项目路径、git remote、`.vercel` 链接状态、CLI/auth 状态、team scope，以及用户是否明确要求 production。

## Outputs

preview URL；无认证 fallback 还返回 claim URL；CLI 路径另报告 inspect 状态。

## Workflow

并行检查 remote、链接文件、CLI auth 和 teams；确定 scope；按 linked/remote/auth 状态选择 git push、CLI link+deploy 或 sandbox fallback；返回 URL。

## Branches

已链接且有 remote 走经确认的 commit/push；已链接无 remote 走 direct deploy；未链接且认证则先 link；无认证按 Claude/Codex fallback。

## Rules

默认 preview；已有链接以 orgId 决定 team；所有后续 CLI 带 scope；未链接目录不得用会交互或产生链接副作用的探测命令。

## Exceptions

用户明确要求 production 时才加 `--prod`；sandbox 认证不可行时使用对应 fallback script；网络限制仅对实际 deploy 请求升级权限。

## Dependencies

Git、Vercel CLI 与认证，或技能内 no-auth deploy script；安装路径可能需要 npm 和浏览器登录。

## Permissions and Side Effects

可能创建 `.vercel` 链接、Vercel project、commit/push、构建和部署；无认证 fallback 上传打包内容并创建可认领 preview。

## Gates

git push 前必须显式确认；多 team 时必须选 scope；production 必须明确要求；CLI 探测与实际 deploy 权限分离。

## Open Questions

顶层 SKILL.md 未明确 no-auth fallback 服务端的数据保留策略。

## Unique Value

以项目长期可维护的 git integration 为目标，同时为不同 agent sandbox 提供可恢复的部署决策树。

## Reading Coverage

本轮只完整读取了顶层 `skills/deploy-to-vercel/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
