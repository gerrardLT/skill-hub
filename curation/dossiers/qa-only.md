# qa-only 来源能力档案

## Problem

在软件交付与版本发布周期中，开发人员或产品团队常常需要对运行中的 Web 应用进行全面、无偏见的质量巡检，获取真实用户视角下的缺陷清单、健康评分与可复现步骤，但明确要求“只测不修”（Never fix anything）。若由负责编码的开发人员自行测试，容易陷入“自证其明”的思维盲区；若由具备自动修复权限的智能体介入，智能体往往会在测试报告阶段仓促引入未经设计的代码补丁，从而污染现有特性分支并增加发布风险。

## When to Use

- **交付前/发布前的纯报告质量巡检（主要场景）**：当用户明确下达“just report bugs”、“qa report only”或“test but don't fix”指令时。
- **特性分支改动的智能差异化验证（Diff-aware mode）**：开发者刚刚在特性分支上完成编码，未指定 URL 时自动分析 Git Diff，定位受影响的控制器、视图、路由与模型，精准对受波及的页面进行浏览器交互测试与邻近回归验证。
- **30秒极速冒烟验证（Quick mode）**：通过 `--quick` 快速核查首页及 Top 5 核心导航目标的加载状态、控制台报错与断链情况。
- **历史质量基线回归比对（Regression mode）**：通过 `--regression baseline.json` 对比历史快照，精确衡量缺陷修复率、新增缺陷数与综合健康得分增量。

## When Not to Use

- **需要自动化闭环修复代码的场景**：若用户需要执行完整的“测试-修复-回归验证”（test-fix-verify）循环，应使用 `/qa` 而非本技能。
- **无 UI 呈现的纯后端类库或微服务底层算法**：无 Web 界面或浏览器交互层，应直接通过单元测试或集成测试覆盖。

## Role

独立黑盒 QA 工程师（Independent Black-Box QA Engineer）。坚守真实终端用户视角，地毯式遍历页面交互、状态流转与边界输入，捕获视觉证据、控制台异常与网络时延，输出严谨量化的健康评分报告，坚决恪守“只汇报、绝不触碰源码”的专业底线。

## Inputs

- **目标访问 URL（Target URL）**：被测 Web 应用地址（如 `https://myapp.com` 或本地 `http://localhost:3000`）。若未提供，在特性分支上自动探测本地运行端口（3000/4000/8080 等）。
- **运行模式（Mode）**：全量模式（Full）、快速冒烟（Quick）、历史回归对比（Regression）。
- **测试范围（Scope）**：全应用覆盖或限定特定页面/模块（如“Focus on billing page”）。
- **真实会话上下文（Auth Session）**：继承用户本地真实 Aside 浏览器的已登录状态；无 Aside 时使用 fallback 浏览器的 Cookie 导入机制。
- **代码分支变更集（Git Diff）**：在 Diff-aware 模式下读取 `git diff main...HEAD --name-only` 与提交日志以推导受影响路径。

## Outputs

1. **结构化 Markdown QA 报告**：落盘至 `.gstack/qa-reports/qa-report-{domain}-{YYYY-MM-DD}.md`，包含：
   - 严重度最高的 Top 3 修复建议（Top 3 Things to Fix）。
   - 综合健康评分（0-100分）及控制台、链接、功能、视觉、UX、性能、内容、无障碍 8 项加权细项。
   - 逐项缺陷档案（Issue ID、严重度、分类、描述、前置截图、操作截图、Snapshot Diff、重现步骤）。
   - 全局控制台错误聚合分析表与被测框架元数据。
2. **多模态复现证据集**：存储于 `.gstack/qa-reports/screenshots/` 的初始页面截屏、操作步骤前后对照截屏及静态缺陷标注图。
3. **机器可读基线快照**：落盘为 `baseline.json`，供未来回归对比。
4. **跨会话项目级结果工件**：落盘至 `~/.gstack/projects/{slug}/{user}-{branch}-test-outcome-{datetime}.md`。

## Workflow

1. **Phase 1: 环境初始化（Initialize）**：
   - 探测并核验浏览器驱动就绪性（优先 Aside 真实浏览器；若不可用则降级至本地 headless Chromium `$B`）。
   - 严禁以单元测试或 curl 替代浏览器端到端测试。
   - 建立输出目录（`.gstack/qa-reports/screenshots`）并启动耗时追踪。
2. **Phase 2: 身份认证就绪（Authenticate）**：
   - 遵循用户隐私边界：若遭遇登录墙、双因子验证（2FA/OTP）或验证码（CAPTCHA），智能体暂停并引导人类在 Aside 窗口中自主完成操作，绝不接收、传输或打印用户密码与凭证。
3. **Phase 3: 架构定向与导航探测（Orient）**：
   - 访问首页并注入全局控制台错误监听钩子（捕获 `console.error`、`uncaught` 异常与 `unhandledrejection`）。
   - 抓取页面可交互快照树（Interactive Snapshot Tree）、可见文本并拍摄首屏截屏。
   - 运行同源链接扫描脚本映射导航骨架；对单页应用（SPA）通过交互元素树探测客户端路由。
   - 识别前端框架（Next.js、Rails、WordPress、SPA 等）并配置专项监控规则。
4. **Phase 4: 地毯式深度探索（Explore）**：
   - 遍历受影响或全站页面，执行标准六维巡检清单：
     1. 视觉扫描（排版错位、文字截断）；
     2. 交互控件（按钮、链接、状态切换响应）；
     3. 表单系统（空输入、非法格式、边界溢出用例）；
     4. 页面导航（前进后退、回退链路完整性）；
     5. 极端状态（空数据状态、加载中、错误兜底、超长文本溢出）；
     6. 控制台监控（每次交互后提取最新的 JS 运行时异常）；
     7. 响应式布局（切换移动端视口如 375x812 验证视口适配）。
5. **Phase 5: 缺陷即时结构化建档（Document）**：
   - 发现缺陷立即落盘，严禁批量积攒。
   - 对交互类缺陷执行双层证据采集：动作前截屏 -> 触发动作 -> 动作后截屏 -> 打印 DOM Snapshot Diff -> 记录清晰重现步骤。
   - 对静态类缺陷拍摄单张标注截屏（Annotated Screenshot）。
6. **Phase 6: 汇总评分与收尾（Wrap Up）**：
   - 按照加权准则计算综合健康评分（功能 20%，控制台/UX/无障碍各 15%，视觉/链接/性能各 10%，内容 5%）。
   - 提炼 Top 3 核心修复项，输出完整的 QA 报告与 `baseline.json`。
   - 若处于回归模式，对比基线输出修复项、新引入缺陷及分值变化。

## Branches

- **分支改动感知分支（Diff-aware Branch）**：在未显式传递 URL 的特性分支上自动触发，通过 Git 差异反查关联页面并自动探测本地运行服务端口，实现增量定向打靶。
- **全量深度探索分支（Full Exploration Branch）**：传递具体 URL 时的默认分支，遍历全站可达链接与深层表单，构建完整质量图谱。
- **极速冒烟分支（Quick Smoke Branch）**：以 `--quick` 触发，仅覆盖首页与 5 大主干入口，30 秒内出具核心健康分与阻断性错误。
- **历史回归对比分支（Regression Diff Branch）**：以 `--regression` 触发，加载已有 `baseline.json`，输出跨版本修复与恶化对比。

## Rules

- **绝对禁止修复原则（Never Fix Anything）**：本技能定位为只读审计，严禁读取源码文件、严禁修改任何业务代码、严禁在报告中编写补丁实现。
- **凭据零接触原则（No Credentials Through Agent）**：智能体严禁要求或接收密码、密钥与支付凭证，所有受保护会话均由人类直接在浏览器操作登录。
- **端到端必须使用真实浏览器（No Browser Substitutes）**：坚决禁止使用 curl 或接口 mock 冒充前端端到端验证，即使后端改动也必须在浏览器中验证前台表现。
- **复现即证据原则（Repro is Everything）**：每个报告的缺陷必须配备至少一张图片证据与确凿复现路径，且在记录前至少重试一次以排除偶发网络波动。
- **即时记录禁止批量原则（Write Incrementally）**：每探查到一个确凿 Issue 必须立即追加写入报告文件，防止长会话中断导致测试资产丢失。
- **非本地环境变更操作授权规则**：在非本地（Non-local）环境执行可能产生副作用的动作（如创建、修改、删除、结算）前，必须触发 AskUserQuestion 获得人类伙伴明确许可。

## Exceptions

- **无测试基建提示**：若检测到项目完全缺乏测试框架配置，需在报告摘要中友好提示可运行 `/qa` 进行工程化引导。
- **SPA 客户端路由降级**：当同源 `<a>` 标签抓取不到深层路由时，自动降级为基于 Accessibility 树的按钮与菜单扫描。

## Dependencies

- **浏览器自动化运行时**：Aside AI 浏览器客户端环境，或本地编译好的 `$B`（Chromium Headless）。
- **Shell 与网络工具**：Bash、curl（用于端口探活）、jq。
- **报告模板资源**：`qa/templates/qa-report-template.md`。

## Permissions and Side Effects

- **文件系统权限**：对 `.gstack/qa-reports/` 及其子目录的读写权限，以及对 `~/.gstack/projects/` 的持久化写入权限。
- **网络与浏览器交互**：对目标 Web 应用的主动 HTTP 请求、DOM 交互与屏幕截图。

## Gates

- **Gate 1: Browser Readiness Gate**：必须确认 Aside 处于 READY 状态或 `$B` fallback 编译就绪，若均缺失必须阻断并引导安装，严禁越过浏览器。
- **Gate 2: Non-Local Mutating Action Gate**：对非 localhost/非 test 的生产或预发环境，在执行第一笔可能改变远端数据状态的操作前必须取得人类授权。
- **Gate 3: Multi-Modal Repro Evidence Gate**：每条 Issue 必须通过本地文件写入确认截图存在并使用 Read 工具回读校验，无证据不得建档。

## Open Questions

- 面对高度动态渲染的 WebGL、Canvas 图表或复杂金融 K 线图时，如何更精确地提取其内部语义缺陷而非仅依赖整屏视觉比对？
- 在极复杂的单点登录（SSO）与多租户隔离架构中，如何更加丝滑地协调自动化流程与人工二次验证授权？

## Unique Value

彻底解耦了“质量探查”与“代码修改”，为交付决策提供了无预设立场、高置信度的第三方视角。通过严格的双层证据链（前置/后置截屏 + Snapshot Diff）、差异感知算法与八维量化评分体系，将传统耗时且难以标准化的前端黑盒验收转变为工业级、确定性的自动化巡检资产。

## Reading Coverage

已对本能力来源全部 2 篇规范及模板文件完成 100% 逐行完整覆盖阅读：
1. `skills/qa-only/SKILL.md`（共 971 行，完整覆盖能力定义、Preamble 前置协议、Plan Mode 保护规则、AUQ 交互规范、Aside 浏览器驱动与本地 `$B` 降级、Diff-aware/Quick/Regression 三种模式、六阶段巡检工作流、八维健康评分准则、各框架专属指南及不可逾越的“只测不修”原则）。
2. `skills/qa-only/SKILL.md.tmpl`（共 536 行，完整核验参数定义、Aside 配置模板与基础流程骨架）。
