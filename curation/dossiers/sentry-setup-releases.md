# sentry-setup-releases 来源能力档案

## Problem

解决 Sentry 监控中事件缺失版本标签、生产问题无法关联引入提交、可疑提交（suspect commits）与代码映射缺失等静默失败问题，建立从源码提交、CI 构建/部署到生产事件归属的端到端可追溯性。

## When to Use

用于需要为项目配置 Sentry releases 追溯部署变更、通过提交排查引入 bug 的责任人/PR、修复监控控制台中 `unknown release` 或缺失 `suspect commit` 的诊断与搭建场景。

## When Not to Use

不用于尚未安装并捕获基本 Sentry 事件的空应用（应先进行基础 SDK 装配）；不用于排查未解析的源码映射/混淆堆栈错误（应优先排查 stack-traces 技能）；不在未排查两端版本名称一致性前盲目重写 CI 流程。

## Role

Sentry 发布与部署追踪编排器。负责诊断事件端与 CI 实体端的关联状态、确定发布名称命名方案、配置打包插件与 CI 发布流程、建立 Git 仓库代码映射与可疑提交推导链条。

## Inputs

项目运行时技术栈与打包配置（Vite, Webpack, Gradle 等）、CI 工作流配置（GitHub Actions 等）、本地与远端 Git 提交历史、Sentry MCP 工具检索返回的事件标签与 Release 对象详情。

## Outputs

统一规划的 Release 命名方案、更新的客户端 SDK 初始化配置与打包工具插件选项、增强的 CI/CD 工作流定义（含全量检出 `fetch-depth: 0` 与发布通知命令）、经由真实部署或 dry-run 验证的发布对象及部署记录。

## Workflow

1. 诊断现状：确认生产事件是否已打上 `release` 标签，以及 Sentry 服务端是否存在对应名称的 Release 对象；
2. 识别平台技术栈与构建工具，提取打包插件支持情况；
3. 统一命名规范：确立客户端 SDK 与 CI 构建阶段产出的版本号保持逐字符严格一致；
4. 补齐缺失端配置：补全 SDK 版本注入、CI 全量 Git 历史检出及凭据密钥；
5. 部署实测检验：通过真实或预发布事件校验 Sentry 后台 Release 与可疑提交呈现效果。

## Branches

若已有打包插件走插件自动注入分支；独立构建与微服务走 Sentry CLI 命令行发布分支；无 Git 自动化集成时提供用户在 Sentry Web 界面完成 SCM OAuth 授权指引分支。

## Rules

事件中的 `release` 标签与 CI 端创建的 Release 对象必须逐字节严格相等，任何大小写或哈希前缀失配均会导致静默断链；CI 阶段检出代码必须保留完整提交图谱（`fetch-depth: 0`）；敏感 `SENTRY_AUTH_TOKEN` 严禁提交至代码仓库，必须通过 CI 密钥安全注入。

## Exceptions

Sentry 历史既有 issue 不会根据新配置的 Release 追溯回填；若代码未开启 Source Maps 或堆栈混淆未还原，可能因无法识别调用栈中的源码文件而无法关联可疑提交。

## Dependencies

项目支持的打包插件（如 `@sentry/vite-plugin`）或 `sentry-cli`；CI 运行环境；Sentry MCP 诊断工具及 SCM 仓库绑定授权。

## Permissions and Side Effects

修改项目构建与 CI 配置文件；在 CI 执行期间向 Sentry 发起 API 交互创建 release/deploy 实体并上报 git commits 记录；读取远端 Sentry 发布列表。

## Gates

在配置 CI 前必须先完成事件端与服务端 Release 实体状态的二元诊断；修改前必须同用户确认全局 Release 命名规则；禁止向仓库直接硬编码鉴权令牌。

## Open Questions

顶层 SKILL.md 未详述在复杂多包（Monorepo）多子项目共存且发布周期不同步时，多子模块 Release 前缀隔离的最佳自动化模板。

## Unique Value

直击 Sentry 持续集成中最隐蔽的“两端配置各自有效却因命名或历史微小偏差导致静默失效”的痛点，给出了严谨的状态机诊断与端到端闭环验证标准。

## Reading Coverage

本轮只完整读取了顶层 `skills/sentry-setup-releases/SKILL.md`（共 120 行）。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
