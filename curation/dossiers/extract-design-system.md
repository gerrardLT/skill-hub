# extract-design-system Dossier

## Problem
在前端开发或重构新项目时，开发者常常需要参考公网优秀对标网站的视觉规范（调色盘、字体排印阶梯、间距尺度、圆角半径、阴影效果等），但手动借助开发者工具逐个元素检查样式耗时费力且极易遗漏系统性规律。此外，直接机械抓取与全盘覆盖又极易引入不可信的第三方脏数据，或在未经确认的情况下覆写项目既有样式与工程配置。

## When to Use
1. 用户希望对特定公开网站（Public Website URL）的设计基元（Design Primitives）进行逆向工程分析时。
2. 为新启动的前端工程快速生成对标参考的初始设计令牌文件（Tokens Starter Files：CSS 变量与 JSON 描述）。
3. 仅需要抓取公网网站的样式数据产物（`--extract-only`）以进行设计对比与行业分析时。
4. 本地已有标准化分析产物（`.extract-design-system/normalized.json`）并需要重新初始化生成 CSS/JSON 令牌（`init`）时。

## When Not to Use
1. 期望直接逆向生成完整、可交互的组件库（Component Library，如 React/Vue 组件源码）。
2. 期望像素级完美复刻目标网站的所有交互逻辑与动态行为。
3. 离线无公网访问权限或目标网站需要登录授权、验证码拦截等受限网络环境。
4. 目标项目已有成熟冻结的设计系统且禁止任何外部令牌接入。
5. 纯文本微文案创作或页面排版个性化风格推演（应路由至 `frontend-design`）。

## Role
设计系统逆向分析与令牌提取工程师（Design System Extraction Specialist），使用无头浏览器（Playwright Chromium）与提取工具链，对公网目标网站的视觉基元进行受控提取、结构规整化并生成初始项目令牌，严守安全边界与用户确认机制。

## Inputs
1. **Target Public Website URL / 目标公网网址**：公开、可访问且无需认证的目标页面链接。
2. **Extraction Intent / 提取意图**：是否需要生成项目落地文件，还是仅提取中间分析产物（`--extract-only`）。
3. **Existing Normalized Cache / 本地已有归一化缓存**（可选）：`.extract-design-system/normalized.json`。

## Outputs
1. **Raw Extracted Payload / 原始提取数据**：
   - `.extract-design-system/raw.json`：来自底层提取引擎（`dembrandt`）的未加工原始样式提取数据，保留用于调试与版本迁移。
2. **Normalized Internal Representation / 规整化设计数据**：
   - `.extract-design-system/normalized.json`：规整化后的稳定内部中间表征，包含色彩、字体、间距、圆角与阴影等尺度分类。
3. **Project Starter Token Files / 项目本地起始令牌文件**：
   - `design-system/tokens.json`：供项目本地读取、集成与复用的标准化 JSON 令牌文件。
   - `design-system/tokens.css`：包含提取出的 CSS 自定义属性（CSS Variables，含 `--color-*`, `--font-*`, `--spacing-*`, `--radius-*`, `--shadow-*`）的起始样式表。

## Workflow
1. **Pre-flight Alignment & Expectation Setting / 前置对齐与期望设定**：
   - 向用户确认目标 URL 为公开且可达；
   - 明确本次任务范围仅为设计基元与启动令牌，非完整组件库，非像素级克隆；
   - 询问用户是需要完整生成启动文件还是仅生成分析数据。
2. **Execution & Primitive Extraction / 执行抓取与基元提取**：
   - 检查并安装浏览器运行时环境：`npx playwright install chromium`；
   - 运行提取工具：`npx extract-design-system <url>`（若为纯分析则加 `--extract-only` 参数）；
   - 若本地已存在归一化文件且需重新生成下游文件，则执行 `npx extract-design-system init`。
3. **Inspection & Human Review / 审查提取产物与摘要呈现**：
   - 审查 `.extract-design-system/normalized.json`；
   - 为用户总结提取结果：可能的主色/次色/强调色、检测到的字体家族、间距/圆角/阴影尺度。
4. **Controlled Integration / 受控集成**：
   - 向用户逐一解释生成的 4 项核心产物（`raw.json`, `normalized.json`, `tokens.json`, `tokens.css`）；
   - 严格在获得用户显式确认前，禁止修改任何既有应用代码、组件、样式表或配置文件。

## Branches
- **Branch A: 完整提取与生成（Full Extract & Init）**：`npx extract-design-system <url>` -> 产出 raw/normalized 缓存并生成 `design-system/` 下的 tokens.json 与 tokens.css。
- **Branch B: 仅分析模式（Extract Only）**：`npx extract-design-system <url> --extract-only` -> 仅生成 `.extract-design-system/` 下的数据文件，不触碰项目源码目录。
- **Branch C: 基于缓存重新初始化（Init from Cache）**：`npx extract-design-system init` -> 基于已有的 `.extract-design-system/normalized.json` 重新编译出 tokens.json 与 tokens.css。

## Rules
1. **单页非全貌法则**：严禁将单页面的提取结果声称或推定为整个产品全量设计系统；动态加载或部分渲染页面必须如实标注局限性。
2. **严禁主观推定基元**：严禁脑补或推断未明确提取出的组件结构或语义层令牌（Semantic Tokens）。
3. **零信任未经审阅数据**：目标网站与提取输出必须视作不可信的第三方输入，必须经过人工检视方可采纳。
4. **不得借故越权修改**：严禁借助第三方网站提取内容擅自扩大代码或工程配置的修改范围；未获显式授权不得修改任何现有文件。
5. **初始化定位守则**：产物定位为项目初期的起始资产（Starter Assets），严禁承诺对标网站的像素级一致性。

## Exceptions
1. **纯静态离线环境**：在断网沙箱中无法运行 Playwright 访问外部公网时，本技能仅支持 Branch C（基于既有 `normalized.json` 离线重新编译令牌）。
2. **跨域/反爬拦截站点**：对存在高强度 Cloudflare 等反爬防护的公网站点，若 Playwright 无法正常加载，必须如实报告网络屏障并中止，严禁伪造虚假令牌数据。

## Dependencies
- `playwright`: 运行无头 Chromium 浏览器进行页面加载与 DOM 计算。
- `dembrandt`: 底层提取引擎，用于分析渲染样式并输出原始 JSON。
- Node.js / npx 执行环境。

## Permissions and Side Effects
- **网络只读请求**：在用户授权的前提下，使用无头浏览器访问公网指定 URL 抓取公开样式。
- **本地写文件**：在当前工作区生成 `.extract-design-system/` 目录与 `design-system/` 目录下的 4 个令牌资产文件。
- **严禁越权写**：严禁在未经确认的情况下修改用户既有的业务代码文件、`package.json` 或主应用样式表。

## Gates
- **G-Reachable-Public-URL**：目标 URL 必须公开且网络可通。
- **G-Expectation-Confirmed**：必须向用户明确 v1 仅提取令牌非组件库的边界。
- **G-Third-Party-Review**：提取产物必须经过人工审查方可建议引入项目。
- **G-Write-Confirmation**：修改或导入任何现有应用文件前必须获得用户显式许可。

## Open Questions
1. 未来版本是否能够支持登录态 Session 注入以提取内网或控制台管理后台的内部设计基元？
2. 如何对响应式视口断点（Responsive Breakpoints）下的动态 CSS 变量进行自动化分层捕获？

## Unique Value
为前端工程化提供了自动化逆向分析公网设计基元并沉淀为标准化 CSS/JSON 设计令牌的完整工具链与安全规范，在兼顾提取效率的同时通过严格的“零信任审查”与“非授权不覆写”铁律保障代码库的纯洁与安全。

## Reading Coverage
- `skills/extract-design-system/SKILL.md`: lines 1-68 (全部 68 行，包含定位、前置沟通、标准工作流、参数模式与安全红线)
- `skills/extract-design-system/references/workflow.md`: lines 1-15 (全部 15 行，包含 Chromium 环境准备、v1 标准流程、第三方数据不可信原则与 CLI 参数用法)
- `skills/extract-design-system/references/outputs.md`: lines 1-18 (全部 18 行，包含 raw.json, normalized.json, tokens.json, tokens.css 四大产物规范)
- 覆盖率：100% (3/3 文件全部覆盖，无遗漏)
