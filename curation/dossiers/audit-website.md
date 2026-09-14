# audit-website 来源能力档案

## Problem

现代 Web 站点与 Web 应用在开发演进中极易积累各维度的质量隐患：SEO 标签缺失或重复、死链与 404 循环跳转、安全响应头缺失、核心性能指标劣化、无障碍不达标以及技术性渲染故障（260+ 项规则）。传统的综合体检工具往往存在两大痛点：要么报告臃肿繁复不适合 LLM 代理直接消费，要么仅提供静态诊断报告却缺乏与源码映射、批量修复、自动化二次审计与回归对比的闭环治理流程，导致发现的缺陷长期搁置无法转化为代码修复。

## When to Use

- **针对线上或本地 Web 站点/Web 应用执行多维度全面体检**：运行 SEO、性能、安全、无障碍、内容质量与技术指标等 260+ 条规则审查。
- **驱动基于 LLM 的“审计-映射-修复-再审”迭代修复闭环**：解析紧凑型 `--format llm` 报告，将问题自动映射到组件、模板与内容源文件，实施批量修复并复审提分。
- **检测版本升级或重构前后的质量回归**：通过 `squirrel report --diff <baseline-id>` 或 `--regression-since` 对比两次审计差异，确保不引入新的死链或技术缺陷。
- **绕过反爬机制执行生产环境合规审计**：对受 Cloudflare / Shopify 保护的站点注入 Web Bot Auth 鉴权头进行深度爬取。

## When Not to Use

- **纯代码语法或单元逻辑检查**：无真实 HTTP 服务或 HTML 渲染产物的纯函数、库或单测，应使用 eslint、vitest 或单元测试工具。
- **非 squirrel CLI 环境**：依赖终端安装并配置有 `squirrel` 命令行工具。

## Role

全站质量综合体检与迭代治理专家（Automated Website Quality Auditor & Remediation Driver）。专注于通过紧凑的 LLM 优化报告洞察全站 SEO、技术、安全与无障碍隐患，并主导从缺陷定位到源码修复的端到端提分闭环。

## Inputs

- **目标站点网址（Base URL）**：如 `https://example.com`（优先线上真实站点，以反映真实渲染、性能与重定向逻辑）。
- **爬取深度模式（Crawl Mode）**：`quick`（25页快速概览）、`surface`（100页模板级覆盖）、`full`（500页终验全量爬取）。
- **执行控制参数**：`--format llm`、`--refresh`（强制重新拉取）、`--resume`、`-m <n>`（页面上限）、`-H "Name: Value"`（Web Bot Auth 爬虫认证头）。
- **本地代码库上下文**：前端模板、页面组件、静态资源与内容 Markdown 文件。

## Outputs

- **Token 紧凑型 LLM 结构化诊断报告**：混合 XML/Text 格式，包含整体健康分（0-100）、等级（A-F）、按类别分组的规则项（id、severity、status、Desc、Fix、Pages、Items）。
- **代码修复补丁与批次变更**：对缺陷模板、路由文件、页面 meta 标签与内容链接实施的精准代码修改。
- **回归对比与提分报告（Diff / Regression Report）**：对比 baseline 与当前审计的指纹级新增（added）、移除（removed）与降级（regressions）清单。

## Workflow

1. **执行初轮快速审计（Run Quick Audit）**：
   - 运行 `squirrel audit <URL> --format llm`（默认快速扫描 25 页），评估整体结构与主要技术瓶颈。
2. **呈现报告与用户确认（Present & Propose）**：
   - 汇报总分、评级与按严重度排序的顶层问题（Errors > High-Rank Warnings）。
   - 列出拟修复的明确缺陷清单，与用户达成确认后再修改代码。
3. **缺陷溯源与代码映射（Map Issues to Source）**：
   - 将报告中的 URL 与 DOM 选择器定位到本地项目的具体模板、React/Vue 组件或 Markdown 内容文件。
4. **按批次实施代码修复（Batch Fixing）**：
   - 优先修复级别为 `error` 的阻断项，再处理高权重 `warning`；
   - 每次批量修改后，执行本地构建（`npm run build`）与基础单测，确保未破坏既有功能。
5. **二次审计与提分验证（Re-Audit Verification）**：
   - 重新运行 `squirrel audit <URL> --format llm --refresh`；
   - 呈现修复前后的分数对比（Before vs After）。
6. **深度扫描与终验签署（Deep Crawl & Sign-off）**：
   - 达到目标分数（如 90+ A 级）后，执行 `-C full` 深度爬取（500页），确保无遗漏残留缺陷；
   - 存在人工裁决项（如死链是否保留/替换）时显式标记待用户审核，不妄加臆测。

## Branches

- **模板级覆盖分支（Surface Crawl Branch）**：使用 `-C surface` 对每个 URL 模式（如 `/blog/{slug}`）采样 1 页，快速治理全站共享模板缺陷。
- **反爬突破分支（Web Bot Auth Branch）**：对受 Cloudflare / Shopify 保护站点附加 `-H "X-Bot-Token: ..."` 执行合规渗透爬取。
- **回归比对分支（Regression Diff Branch）**：调用 `squirrel report --diff <audit-id> --format llm` 输出确定性指纹差异，核验新功能引入的退化。

## Rules

- **LLM 格式输出原则**：在代理自动化场景下必须始终携带 `--format llm`，以获得相比原生 XML 节省 40-70% Token 的极简 XML/Text 混合输出。
- **先确认后修改原则**：在对本地源码实施修改前，必须向用户汇报拟修复的问题清单与修改方案，严禁擅自进行大范围代码覆写。
- **分级修复顺序原则**：严格按照 `error` > `warning`（按权重 Rank 降序）> `notice` 顺序处理；内容修正与代码修正同等对待。
- **严禁妄断死链处理**：对于失效死链（Broken Links），通常涉及业务决策（删除、重定向或替换真实链接），必须向用户明确标出并征求决策，禁止擅自批量剔除。
- **改后必验构建原则**：每完成一个批次的代码修改，必须在重新审计前运行项目的静态构建与已有测试，防止语法错误导致站点崩溃。

## Exceptions

- 若同时存在本地开发服务（localhost）与线上生产/预发地址，优先审计线上地址以获得真实的 CDN、重定向与性能表现，但代码修复统一落盘至本地源码。
- 若部分第三方外链因目标服务器网络波动偶发超时，可在复测 `--refresh` 时标记为外部网络依赖异常。

## Dependencies

- **系统环境依赖**：系统 PATH 中可执行的 `squirrel` CLI 命令行工具。
- **网络连通依赖**：能够访问目标站点并执行 HTTP/HTTPS 页面抓取。

## Permissions and Side Effects

- **权限要求**：网络抓取权限、本地代码库读写权限、执行本地构建命令权限。
- **副作用**：对目标 Web 站点产生一定频次的 HTTP 页面爬取请求；在本地缓存审计数据；修改本地前端源码。

## Gates

- **Gate 1: CLI Availability Gate**：在执行任何审计指令前必须确保 `squirrel --version` 可用。
- **Gate 2: User Proposal Confirmation Gate**：在改动本地代码前必须获得用户对拟修复 issue 清单的授权。
- **Gate 3: Full Scan Sign-off Gate**：最终收官验收必须基于 `-C full` 深度爬取的结果签署，确认目标健康分达成且零遗留未确认 error。

## Open Questions

- 对于需要复杂登录态与多步交互的前端 SPA 单页应用，纯 CLI 爬虫与带鉴权 Cookie 的深层路由抓取覆盖边界如何划分？
- 动态由客户端 JavaScript 延迟水合渲染的异步数据指标与服务端静态 SEO 的权重分配比例如何自适应调整？

## Unique Value

将海量 260+ 条全站体检规则浓缩进极致节省 Token 的 `--format llm` 格式，打通了“扫描报告 -> 源码定位 -> 批量修复 -> 增量重测 -> 回归比对”的完整自动化治理飞轮，让大模型能够真正作为全栈网站质量工程专家端到端消除技术债。

## Reading Coverage

已对本能力来源全部 2 篇核心文档完成 100% 逐行完整覆盖阅读：
1. `skills/audit-website/SKILL.md`（共 90 行，完整覆盖能力定位、squirrel CLI 命令、Scan progression、The fix loop 六步法、分数目标阶梯及回归比对）。
2. `skills/audit-website/references/OUTPUT-FORMAT.md`（共 250 行，完整覆盖 `--format llm` 规范、XML/Text 混合语法、Site/Score/Summary/Issues/Items 标签结构、Diff 输出模型、Token 压缩机制与实现细节）。
