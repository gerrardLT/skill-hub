# playwright 来源能力档案

## Problem

在终端驱动或智能体自动化会话中，传统的无界面自动化脚本往往存在两个极端：要么需要编写厚重的 JavaScript/TypeScript 测试套件代码（如 `@playwright/test`），使得快速的交互式调试、页面抓取和轻量 UI 探索变得繁琐臃肿；要么缺乏命令行即时可控的浏览器运行时包装，使得在未全局安装重量级 npm 包的环境下无法直接从命令行操控真实浏览器。同时，页面 DOM 元素在异步渲染和路由跳转后极易发生选择器失效与陈旧引用（Stale Element References），导致自动化脚本脆弱易碎。

## When to Use

- **从终端直接自动化操控真实浏览器（主要场景）**：执行网页导航、表单填写、DOM 快照获取、全屏截屏、数据提取或 UI 流程交互调试。
- **免全局安装的便携 CLI 驱动**：使用内置的包装脚本 `playwright_cli.sh`，直接通过 `npx --package @playwright/cli playwright-cli` 即开即用。
- **基于稳定快照引用的轻量自动化循环**：通过 `snapshot` 获取短引用（如 `e1`、`e2`、`e15`）执行点击、填充与校验，而无需编写繁复的 XPath 或 CSS 选择器。
- **会话隔离与 UI 流程追踪**：利用 `--session` 隔离多项目浏览器上下文，或使用 `tracing-start` / `tracing-stop` 录制故障链路。

## When Not to Use

- **需要正式固化为工程级端到端测试用例**：若用户明确要求产出 `@playwright/test` 规范的 `.spec.ts` 文件并接入 CI 流水线，不应局限于 CLI 命令，而应转入规范的测试工程编写。
- **无 Node.js/npx 运行时的纯隔离环境**：依赖基础 Node 运行时支撑。

## Role

命令行浏览器驱动与自动化操纵专家（CLI Browser Automation Operator）。专注于通过极简的终端交互原语（open、snapshot、click、fill、type、screenshot），以低摩擦方式操控真实浏览器执行端到端探索与数据采集。

## Inputs

- **目标网址或操作指令（URL or Command）**：拟访问的 URL（如 `https://example.com`）及后续子命令。
- **元素引用代号（Element Ref）**：最新快照中生成的短引用（形如 `e3`、`e15`）。
- **运行参数与标志位（Flags）**：`--headed`（有头可见模式）、`--session <name>`（命名会话隔离）、`--config <file>`（配置载入）。
- **表单填充与按键载荷**：文本串、上传文件路径及特定按键标识（`Enter`、`Shift` 等）。

## Outputs

1. **终端交互快照与数据提取结果**：
   - 可交互 DOM 树快照（带有短引用的纯文本元素清单）。
   - JavaScript `eval` 执行的返回值（如 `document.title`、文本内容）。
2. **多模态物理工件（Artifacts）**：
   - 截屏文件（落盘至指定路径或 `output/playwright/`）。
   - PDF 页面导出文档。
   - 包含网络和控制台记录的 Trace 诊断追踪包（`tracing.zip`）。

## Workflow

1. **前置环境探测（Prerequisite Check）**：
   - 检查 `npx` 是否可用（`command -v npx`）；若缺失则暂停并提示用户安装 Node.js 与 npm。
2. **确定驱动脚本路径（Resolve CLI Path）**：
   - 设置并引用 `$PWCLI`（指向 `skills/playwright/scripts/playwright_cli.sh` 或已有的全局 `playwright-cli`）。
3. **核心操作闭环（Standard Interaction Loop）**：
   - **Step 1: Open**：打开目标页面（可携带 `--headed` 观察界面渲染）。
   - **Step 2: Snapshot**：拍摄当前 DOM 可交互快照，提取最新的元素引用（如 `e1`, `e2`）。
   - **Step 3: Interact**：基于最新快照中的引用执行动作（`click e3`、`fill e1 "text"`、`press Enter` 等）。
   - **Step 4: Re-snapshot**：页面发生导航、弹窗开启、菜单展开或大幅 DOM 变动后，**强制重新拍摄快照**更新引用，防止陈旧引用失效。
   - **Step 5: Capture Artifacts**：按需调用 `screenshot`、`pdf` 或 `tracing-stop` 保存最终证据。
4. **会话与标签页管理（Session & Tabs）**：
   - 通过 `--session <name>` 隔离不同项目状态或多账号登录态；
   - 通过 `tab-new`、`tab-list`、`tab-select` 进行跨多标签页协同操作。

## Branches

- **表单自动化提交分支（Form Submission Branch）**：`open` -> `snapshot` -> `fill e1` -> `fill e2` -> `click e3` -> `snapshot` -> `screenshot`。
- **无头数据采集分支（Data Extraction Branch）**：`open` -> `snapshot` -> `eval "document.title"` -> `eval "el => el.textContent" e12`。
- **故障排查与链路追踪分支（Debugging & Tracing Branch）**：`open --headed` -> `tracing-start` -> 触发重现步骤 -> `tracing-stop` -> `console warning` -> `network`。
- **多会话并行分支（Multi-Session Branch）**：通过 `--session marketing` 与 `--session checkout` 分离不同的持久化上下文。

## Rules

- **快照先行原则（Snapshot First）**：在引用如 `e12` 等具体元素代号前，必须先执行过 `snapshot`；严禁在没有最新快照的情况下臆造引用。
- **失效重拍原则（Re-snapshot on Stale）**：页面导航、状态突变或命令因缺少引用失败时，第一排查动作必须是重新执行 `snapshot`。
- **CLI 原生优先原则**：优先使用 `click`、`fill`、`select` 等显式 CLI 原语，尽量避免滥用 `eval` 或 `run-code` 绕过控制。
- **禁止私自转向测试规范**：本能力定位为终端交互自动化，除非用户明确要求编写测试文件，否则禁止主动退回编写 `@playwright/test` 的规格代码。
- **产物目录收敛规范**：生成的截屏、PDF 或追踪产物统一归档至 `output/playwright/<label>/`，禁止在项目根目录随意散落临时文件。

## Exceptions

- 若缺乏全新快照但需给出示例，必须显式说明并使用 `eX` 占位符标明待确认。
- 若页面排版异常或点击未命中，可临时添加 `--headed` 标志打开可见窗口直观诊断。

## Dependencies

- **Node.js 运行时环境**：依赖系统 PATH 中包含 `node` 与 `npx`。
- **Playwright CLI 依赖包**：运行时由 `npx --package @playwright/cli playwright-cli` 自动拉取或全局预装。
- **底层浏览器二进制**：依赖 Playwright 支持的 Chromium/Firefox/WebKit 浏览器内核。

## Permissions and Side Effects

- **权限要求**：网络访问权限（用于下载网页资源与运行浏览器）、文件系统读写权限（用于写出截屏与 trace 产物）。
- **副作用**：在本地启动无头或有头浏览器进程；在 `output/playwright/` 生成测试产物；对目标网站产生 HTTP/WebSocket 流量。

## Gates

- **Gate 1: npx Prerequisite Gate**：在执行任何命令前必须检查 `command -v npx`，缺失时必须暂停并提示用户安装 Node.js。
- **Gate 2: Fresh Snapshot Gate**：执行交互指令前必须确保已取得当前页面的有效 Snapshot，并在页面跳变后执行再刷新。
- **Gate 3: Safe Artifact Output Gate**：所有落盘文件必须限制在 `output/playwright/` 约定目录下，保持工作区整洁。

## Open Questions

- 在多进程并发运行多个 `playwright_cli.sh` 脚本时，底层 CDP 端口和 session 存储目录是否存在冲突可能？
- 遇到复杂 Shadow DOM 或跨域 iframe 嵌套结构时，纯 CLI 的 flat 快照树引用提取深度上限如何？

## Unique Value

将庞大复杂的浏览器端到端自动化能力浓缩为一套优雅的 Unix-like 命令行交互工具链。通过基于短引用的 Snapshot-Interact-ReSnapshot 模式与无需全局安装的脚本包装，大幅降低了在终端环境中操控真实浏览器的认知负荷与搭建门槛。

## Reading Coverage

已对本能力来源全部 4 篇规范、参考与包装脚本完成 100% 逐行完整覆盖阅读：
1. `skills/playwright/SKILL.md`（共 148 行，完整覆盖能力定位、npx 前置校验、核心 Snapshot 交互循环、重拍快照时机、推荐表单/Trace/多标签工作流及防护守则）。
2. `skills/playwright/scripts/playwright_cli.sh`（共 26 行，完整覆盖 npx 检查、session 标志解析、npx 包装调用及 exec 参数传递）。
3. `skills/playwright/references/cli.md`（共 100 行，完整覆盖 Core、Navigation、Keyboard、Mouse、Save as、Tabs、DevTools 等全量子命令参数）。
4. `skills/playwright/references/workflows.md`（共 96 行，完整覆盖标准交互、表单提交、数据提取、控制台与网络调试、Tracing 追踪、多 Session 隔离与配置文件样例）。
