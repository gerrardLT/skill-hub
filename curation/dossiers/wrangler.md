# wrangler 来源能力档案

## Problem

规范 Cloudflare Workers 运行时与边缘生态的项目初始化、本地开发调试、资源绑定配置与多环境部署上线，防止因脱离本地依赖版本、混淆本地模拟与远程生产绑定、或误用已废弃 CLI 命令而导致线上服务事故或数据丢失。

## When to Use

用于运行或排查 Wrangler CLI 命令、配置 Worker 边缘项目、管理 Cloudflare 平台资源（KV, D1, R2, Queues, Vectorize 等）、打通本地仿真与多环境部署（staging/production）的研发与运维场景。

## When Not to Use

不用于脱离 Cloudflare Workers/Pages 体系的通用 Node 传统后端部署；不用于在没有确认目标环境与操作对象前直接执行会产生线上副作用的资源写操作或秘密删除；不用于在用户未明确授权时直接触发线上全量部署。

## Role

Cloudflare Wrangler 边缘资源与部署控制器。负责解析项目本地 Wrangler 依赖版本、校验 `wrangler.jsonc` 配置文件、推导环境变量继承关系、规划资源绑定并在隔离保护下执行部署与版本追踪。

## Inputs

项目本地包管理与依赖配置（`package.json` 中的 wrangler 版本）、现有的 Wrangler 配置文件（推荐 `wrangler.jsonc`）、目标 Cloudflare 账户、Worker 名称与环境变量、资源绑定声明以及敏感密钥配置。

## Outputs

校验无误的 `wrangler.jsonc` 配置文件、通过 `wrangler types` 生成的 TypeScript 运行时类型声明、通过 `--dry-run` 验证的构建打包工件，以及清晰记录环境与执行参数的部署指令或执行记录。

## Workflow

1. 检查项目技术栈与环境：探查包管理器、已安装 Wrangler 版本与构建脚本，严禁盲目静默升级；
2. 获取权威参考：通过本地 `wrangler --help` 或安装目录下的 `config-schema.json` 确定确切语法与字段；
3. 规划配置与绑定：优先采用 `wrangler.jsonc`，明确区分不同环境的继承规则，准确设置 `compatibility_date`；
4. 区分本地仿真与远端实体：清晰界定数据写操作的目标边界（Local vs Remote）；
5. 实施与验证：针对 TS 项目运行 `wrangler types` 重新生成类型定义，部署前执行 `wrangler deploy --dry-run` 进行打包校验。

## Branches

常规部署走标准的构建校验分支；使用 Cloudflare Vite 插件时通过 `CLOUDFLARE_ENV` 环境变量注入分支；Pages 项目迁移走静态资源适配分支；临时未认证原型走快速 Claim 部署分支。

## Rules

优先使用本地安装的 Wrangler 版本而非全局或最新版；严禁将密钥明文写入命令参数、源码或日志中；`wrangler secret put` 与 `secret delete` 会直接创建并立即生效新版本，必须谨慎对待；回滚前必须知晓关联资源（如 KV/D1 数据库）的数据不会随代码回滚。

## Exceptions

若使用 Cloudflare Vite 插件，环境必须在 dev/build 时通过 `CLOUDFLARE_ENV` 指定，在 deploy 阶段无法重新重定向扁平化配置；若缺少必要功能需升级 Wrangler 时，必须显式声明升级依赖，不可擅自静默更改。

## Dependencies

本地项目安装的 `wrangler` 依赖库、Node.js 运行时、对应框架的 Cloudflare 适配器或 Vite 插件。

## Permissions and Side Effects

本地修改 `wrangler.jsonc` 配置文件及自动生成类型定义；读取 Cloudflare 账户与资源元数据；执行部署时将向 Cloudflare 边缘网络分发 Worker 脚本并创建版本实体。

## Gates

写操作前必须向用户核实目标账户、Worker 与部署环境（Local/Staging/Production）；敏感配置必须经由标准受保护机制注入；部署前必须通过本地构建与 `--dry-run` 打包验证。

## Open Questions

顶层 SKILL.md 未明确当存在多个微前端 Worker 通过 Service Bindings 相互调用时，跨 Worker 调用的本地联合模拟（Multi-Worker local simulation）最佳编排规范。

## Unique Value

全面梳理了边缘计算领域最核心的 CLI 与配置规范，建立了区分本地仿真与真实资源、防止配置漂移、守护密钥安全的坚固操作护栏。

## Reading Coverage

本轮只完整读取了顶层 `skills/wrangler/SKILL.md`（共 58 行）。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
