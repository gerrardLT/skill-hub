# web-perf 来源能力档案

## Problem

在现代 Web 应用的开发与上线运维中，网站加载迟缓、布局抖动（Layout Shift）与交互卡顿不仅严重损害用户体验与留存，还直接打击搜索引擎 SEO 排名与商业转化率：
1. **主观模糊感觉代替客观数值指标**：仅凭“感觉打开挺快/挺卡”评价性能，缺乏行业标准 Core Web Vitals（LCP, CLS, INP, TTFB 等）的量化基准；
2. **缺乏全链路归因与链路依赖诊断**：难以区分白屏是由于后端响应延迟（TTFB 高）、渲染阻塞资源（Render-blocking CSS/JS）、字体闪烁（FOUT/FOIT），还是次级瀑布流依赖链（Network Dependency Chaining）所致；
3. **缺少工程代码层面的落地方案**：性能审计工具往往停留在浏览器端只报问题，未能深入项目源码（Webpack/Vite 构建配置、Tree-shaking、死代码、Tailwind Purge、动态分包）给出具体可落地的工程改造代码。

## When to Use

- **站点性能健康体检与 Core Web Vitals 达标审计**：全面检测目标网站的 TTFB、FCP、LCP、INP、TBT、CLS 及 Speed Index。
- **冷启动与网络瀑布流瓶颈诊断（Performance Trace）**：排查渲染阻塞资源（Render-blocking CSS/JS）、关键资源预加载（Preload/Preconnect）与缓存配置缺失。
- **布局抖动（CLS）与渲染阻塞根因溯源**：定位未指定尺寸的媒体元素、异步注入 DOM 内容及 Web 字体替换导致的累积位移元凶。
- **打包体积与现代前端构建优化（Codebase Analysis）**：针对 Vite/Webpack/Next.js/Astro 等工程，审查 Tree-shaking、Babel 垫片膨胀、动态分包及死代码。

## When Not to Use

- **纯后端 API 并发与微服务压力测试**：评估后端微服务集群并发吞吐与 QPS，应使用专门压测工具（如 k6, JMeter），而非前端页面审计。
- **非浏览器纯原生移动端应用（Native App）**：针对 iOS/Android 纯原生视图渲染优化，不适用 Web 前端性能指标体系。
- **传统单机应用内存泄漏深度调试**：针对底层 C/C++ 内存崩溃排查，不属于 Web 渲染生命周期。

## Role

Web 运行时与工程构建性能架构师（Web Performance & Core Web Vitals Specialist）。专职结合浏览器运行时 Trace、网络瀑布流深度洞察与前端打包编译栈代码分析，输出高精度、可度量、带预期收益毫秒数的专业调优方案。

## Inputs

- **目标页面 URL（Target URL）**：需要实施冷启动与运行时分析的 Web 页面地址。
- **浏览器与 DevTools 运行时探针**：Chrome DevTools MCP 工具链（`navigate_page`, `performance_start_trace`, `performance_analyze_insight`, `list_network_requests` 等）。
- **前端源码工程上下文（可选）**：构建配置文件（`vite.config.ts`, `next.config.js`, `webpack.config.js`）、`package.json` 及样式配置。

## Outputs

- **Core Web Vitals 评估摘要表**：列明各指标实测数值与官方阈值对比评级（Good / Needs Improvement / Poor）。
- **性能关键瓶颈优先级清单（Top Issues）**：按预估收益毫秒数或字节数严格量化排期的缺陷清单。
- **工程级优化改造实施建议（Actionable Recommendations）**：包含明确的代码片段、构建配置调整（如 dynamic import、Tree-shaking、Preload 声明）与缓存策略。

## Workflow

1. **环境与 MCP 工具能力验证（Verify Available Tools）**：
   - 嗅探当前会话可用的浏览器与 DevTools 工具链，明确测量边界。
2. **冷启动性能抓取与 Trace 录制（Phase 1: Performance Trace）**：
   - 导航目标页面并触发硬刷新，完整捕获初始冷加载 Trace 数据。
3. **Core Web Vitals 洞察解析（Phase 2: Core Web Vitals Analysis）**：
   - 提取 `LCPBreakdown`（拆解 TTFB、资源下载与渲染延迟）；
   - 提取 `CLSCulprits`（精确定位导致位移的无尺寸图片、字体切换或异步注入组件）；
   - 提取 `RenderBlocking` 与 `NetworkRequestsDepGraph`。
4. **网络请求全链路与缓存审查（Phase 3: Network Analysis）**：
   - 审查 `<head>` 内无 `async`/`defer` 的阻塞资源、链式依赖、缺失预加载与弱 Cache-Control 头；
   - 验证预连接（Preconnect）有效性，排除 0 请求的无效声明。
5. **无障碍快照辅助核查（Phase 4: Accessibility Snapshot）**：
   - 抓取 a11y 树快照，排查高对比度缺失与交互元素无名漏洞。
6. **前端源码工程构建深挖（Phase 5: Codebase Analysis）**：
   - 识别工程框架与打包器，审查生产模式配置、Tree-shaking 边界、Babel 垫片与冗余依赖。

## Branches

- **全流程含源码分析分支（Full Audit Branch）**：本地拥有前端代码库权限，串联 Trace 测量与源码配置文件重构。
- **第三方在线只读审计分支（Third-Party Site Branch）**：无本地源码权限时，跳过 Phase 5 代码库分析，聚焦浏览器端网络与 DOM 收益。
- **无 Trace 工具降级运行分支（Degraded Network Branch）**：在缺乏高级 Trace 接口时，降级执行基础网络请求与源码静态打包分析，并如实披露测量限制。

## Rules

- **实测数据断言铁律（Be Assertive & Evidence-Based）**：所有性能论断必须核对真实网络请求、DOM 结构或编译配置，拒绝模棱两可的主观揣测。
- **收益毫秒量化原则（Quantify Impact）**：必须使用毫秒（ms）或体积（KB）标定调优收益，严禁推荐预期收益为 0ms 的空洞改动。
- **无证据不优化法则（Verify Before Recommending）**：在建议移除冗余资源或预连接前，必须确认其调用频次确为零。
- **无隐患不纠缠原则（Skip Non-Issues）**：若关键指标（如 LCP < 200ms, CLS = 0）已达卓越标准，直接予以认可，严禁为凑篇幅强行制造问题。

## Exceptions

- **第三方无源码站点**：自动放行 Phase 5 代码工程分析，仅基于 DevTools 接口输出优化建议。
- **微前端与动态脚本加载场景**：针对按需懒加载的动态脚本，放行部分非阻塞 preconnect 预连接调用。

## Dependencies

- **工具链依赖**：Chrome DevTools MCP 协议工具或等效 Headless 浏览器环境。
- **规范标准参考**：web.dev Core Web Vitals 最新指标阈值标准、WCAG AA 对比度规范。

## Permissions and Side Effects

- **权限要求**：外部或本地 Web 站点 HTTP/HTTPS 访问权限、本地前端工程代码只读权限。
- **副作用**：向目标服务器发起页面抓取请求与网络流量探测；无本地代码破坏性篡改。

## Gates

- **Gate 1: Metric Threshold Gate**：各核心指标必须依照官方 Good/Needs-Improvement/Poor 阈值精确分级。
- **Gate 2: Zero-Impact Filter Gate**：自动过滤预期收益低于测量误差或为 0ms 的无效改进项。
- **Gate 3: Codebase Alignment Gate**：针对源码工程的建议必须符合对应打包器（Vite/Webpack/Next.js）的语法规范。

## Open Questions

- 当第三方分析埋点脚本（如营销追踪 Tag）成为主要主线程阻塞源但业务部门强依赖时，如何在合规前提下最大程度隔离其对 INP 的负面影响？
- 在极低网速与高丢包的弱网移动环境下，如何动态自适应降级高精度媒体素材？

## Unique Value

将高深抽象的浏览器性能底层原理与真实项目的前端打包构建实践无缝联通，兼具 DevTools 毫秒级归因能力与工程源码级重构方案，实现立竿见影的性能提升。

## Reading Coverage

- `skills/web-perf/SKILL.md`: 涵盖性能工具准备、核心指标健康阈值（TTFB, FCP, LCP, INP, TBT, CLS）、五阶段完整审计流水线、网络链路诊断、代码工程打包分析及结构化输出模版。
