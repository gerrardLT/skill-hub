# playwright-best-practices 来源能力档案

## Problem

Playwright 作为功能极其强悍的现代端到端与跨层级自动化测试框架，覆盖了从 UI E2E、组件渲染、API 与 GraphQL 契约，到无障碍、视觉回归、安全攻防以及桌面 Electron/扩展等海量能力。但在真实团队工程落地中，开发者经常面临庞大的认知鸿沟与工程陷阱：不规范的脆弱选择器导致测试随 UI 变更频繁破裂；不当的硬编码延时（`waitForTimeout`）滋生严重的非确定性脆弱测试（Flaky Tests）；过度臃肿的 Page Object Model 与脆弱的共享状态破坏测试隔离性；缺乏高效的多 Worker 并行分片与缓存策略导致 CI 流水线运行缓慢甚至耗尽资源；复杂的真实网络服务（OAuth、三方支付、短信验证码）缺乏清晰的 Mock 判定标准与多上下文多角色隔离支撑。

## When to Use

- **编写各类型自动化测试套件**：E2E、Component、API、GraphQL、视觉回归（Visual Regression）、无障碍合规（Axe-core）、安全防御性验证（XSS/CSRF）。
- **定位与根治脆弱测试（Flaky Tests）**：排查多 Worker 并行运行下的状态泄漏、时序竞争（Race Condition）、选择器漂移与异步超时。
- **架构决策与设计模式落地**：在大型工程中评估 Page Object Model 与 Custom Fixtures 的适用边界、设计测试数据工厂、制定 Mock 与真实后端交互的划分边界。
- **CI/CD 流水线工程化加速**：配置 GitHub Actions / GitLab CI / Docker 分片并行运行（Sharding）、测试报告生成与失败工件回溯（Trace Viewer / Video / Screenshot）。
- **复杂前沿场景交互驱动**：时钟模拟（Clock Mocking）、WebSockets 实时通信、Service Worker / PWA 离线测试、多用户协同、文件上传下载及跨域 IFrame 穿透。

## When Not to Use

- **纯终端交互式快速探索与单命令排障**：无需正式编写代码工程或持久化 spec 文件时，优先使用轻量级的 `playwright` CLI 技能。
- **非 Playwright 生态的测试运行器专用特性**：纯单元测试场景若项目已深度绑定 Jest 或 Vitest，且无浏览器环境依赖时，不宜引入完整的 Playwright 运行时。

## Role

Playwright 自动化工程架构与最佳实践专家（Playwright Test Engineering & Architecture Specialist）。为团队建立工业级、确定性、高并行度的端到端与集成测试体系，涵盖规范用例编写、架构选型、稳定性治理与 CI/CD 效能加速。

## Inputs

- **待测业务应用与框架类型**：React、Angular、Vue/Nuxt、Next.js 或 Electron 客户端。
- **测试目标与层级定位**：E2E 全链路、组件快照、API/GraphQL 接口、无障碍或安全合规。
- **运行配置与环境变量**：`playwright.config.ts`、`projects` 矩阵、多环境 BaseURL、并行 Worker 数量与重试策略。
- **测试诊断现场数据**：Trace 压缩包（`trace.zip`）、Console/Network 错误日志、DOM 树快照与视频回放。

## Outputs

- **高可维护性测试用例代码**：遵循语义化 Locator、自动等待断言与纯净隔离断言的 `.spec.ts` 文件。
- **测试架构与工程支撑代码**：自定义 Fixtures、POM 类封装、全局 Setup/Teardown 脚本、测试数据生成器（Data Factories）。
- **CI/CD 流水线配置文件**：针对 GitHub Actions、GitLab CI、Docker 的矩阵分片与报告归档流水线定义。
- **排障与治理分析诊断报告**：根因分析（Flakiness Root Cause）、时序修复方案与稳定性回归验证记录。

## Workflow

1. **测试类型与场景决策（Decision & Scoping）**：根据需求目标查询活动决策树（Quick Decision Tree），确定采用 E2E、API、Component 或专项测试范式。
2. **测试架构与隔离设计（Architecture & Isolation）**：决定采用 Custom Fixtures 还是轻量 POM，设计数据工厂与环境隔离机制，配置独立 BrowserContext 规避状态泄漏。
3. **编写规范化测试实现（Writing Idiomatic Tests）**：
   - 采用用户可见的语义化 Locator（`getByRole`、`getByText`、`getByLabel`）；
   - 使用 Web-first 具备自动重试的异步断言（`await expect(locator).toBeVisible()`）；
   - 避免任何非必要的 `waitForTimeout`。
4. **复杂场景适配与桩注入（Advanced Mocking & Injection）**：按需引入 API 路由拦截（`page.route`）、HAR 回放、时钟步进（`clock.fastForward`）或 OAuth 弹窗处理。
5. **本地闭环验证循环（Validation Loop）**：
   - 运行测试：`npx playwright test --reporter=list`；
   - 失败排障：检查 Trace Viewer（`npx playwright show-trace`）微调定位器与断言；
   - 稳定性复测：针对关键路径执行重复验证（`--repeat-each=5`）。
6. **CI/CD 流水线配置与分片交付（Pipeline Delivery）**：配置基于 Commit / PR 的自动化触发矩阵与并行 Sharding，收敛测试报告与诊断工件。

## Branches

- **E2E 核心主流程分支**：基于 POM/Fixtures 驱动多页面导航、表单填写与全链路状态断言。
- **API 与网络测试分支**：绕过 UI 直接利用 `request` 上下文验证 REST/GraphQL 接口契约与响应模式。
- **视觉回归与多设备适配分支**：利用 `toHaveScreenshot` 对比基线截图，在移动视口与设备模拟下验证响应式布局。
- **稳定性与防脆弱专项治理分支**：针对多 Worker 并行竞争、状态泄漏与控制台隐蔽报错实施排查与隔离修复。

## Rules

- **Web-First 自动重试断言原则**：强制使用 `await expect(locator).toHaveText(...)` 等自带轮询重试的 Web-First 断言，严禁使用原生 JavaScript `expect(await locator.textContent()).toBe(...)`，避免时序竞态。
- **语义化定位器优先原则**：优先使用 `getByRole`、`getByLabel`、`getByText` 等面向真实用户感知的 Locator，尽量杜绝基于脆弱 DOM 结构路径（XPath、多层 CSS class）的选择器。
- **硬编码延时绝对禁令**：严禁在生产用例中出现 `page.waitForTimeout()`；必须通过状态监听、网络响应捕获或显式 Locator 断言代替无意义睡眠。
- **用例完全隔离原则（Test Isolation）**：每个用例必须拥有独立的 BrowserContext 与数据状态，严禁跨测试用例共享全局状态或产生顺序依赖。
- **验证通过门禁（Pass Gate）**：新编写或重构的测试用例必须通过完整验证循环，并在核心流程中通过 `--repeat-each` 重复验证方可合并。

## Exceptions

- 当与不受控的第三方外部服务（如黑盒支付网关、物理外设驱动）对接且无法拦截网络事件时，可设立特定隔离标志并附带详尽的 timeout 说明。
- 在执行视觉回归比对时，若存在动态时间戳、轮播图或微小像素抗锯齿抖动，允许通过 `mask`、`threshold` 或 `maxDiffPixelRatio` 进行容差配置。

## Dependencies

- **核心框架环境**：`@playwright/test`、Node.js LTS。
- **辅助测试库**：`@axe-core/playwright`（无障碍审计）、`faker`（测试数据构造）、`allure-playwright`（高级报告生成）。
- **CI/CD 运行环境**：GitHub Actions Runner、GitLab Runner 或 Playwright 官方 Docker 镜像容器。

## Permissions and Side Effects

- **权限要求**：网络监听与端口绑定权限、测试环境数据写入权限、系统文件生成权限（用于保存 traces/screenshots/videos）。
- **副作用**：在测试数据库或 Mock 服务产生临时测试数据；在本地或 CI 节点落盘追踪文件与覆盖率报告；高并发 Worker 会消耗显著的 CPU 与内存资源。

## Gates

- **Gate 1: Selector Robustness Gate**：提交前必须审查 Locator，确保未包含易碎的绝对 DOM 路径或无语义的 CSS 属性。
- **Gate 2: No-Sleep Gate**：全局扫描测试代码，确保零 `waitForTimeout` 遗留。
- **Gate 3: Repeat-Pass Gate**：对修改或新增的用例必须运行 `--repeat-each=5` 连续无报错通过，确认无偶发脆弱隐患。

## Open Questions

- 在超大规模微服务拓扑中，端到端测试是优先全链路集成还是优先通过网络路由拦截（`page.route`）与契约测试解耦？
- 视觉回归在跨操作系统（Linux CI vs macOS Local）下的跨平台字体渲染差异如何达到最优平滑补偿？

## Unique Value

汇聚了业界顶尖的 Playwright 自动化工程全景知识库，从 8 大活动场景、58 个专项参考维度系统性规范了用例设计、高可用选择器、架构模式选择（POM vs Fixtures）、深层网络拦截与高并发 CI 分片优化，是构建高信赖度、零脆弱性端到端自动化测试体系的决定性指南。

## Reading Coverage

已对本能力来源全部 59 篇规范与参考文档完成 100% 逐行完整覆盖阅读：
1. `skills/playwright-best-practices/SKILL.md`（共 304 行，覆盖全域测试活动目录、决策树及验证循环）。
2. `core/` 目录 11 篇（`annotations.md`、`assertions-waiting.md`、`configuration.md`、`fixtures-hooks.md`、`global-setup.md`、`locators.md`、`page-object-model.md`、`projects-dependencies.md`、`test-data.md`、`test-suite-structure.md`、`test-tags.md`）。
3. `advanced/` 目录 8 篇（`authentication-flows.md`、`authentication.md`、`clock-mocking.md`、`mobile-testing.md`、`multi-context.md`、`multi-user.md`、`network-advanced.md`、`third-party.md`）。
4. `architecture/` 目录 3 篇（`pom-vs-fixtures.md`、`test-architecture.md`、`when-to-mock.md`）。
5. `browser-apis/` 目录 4 篇（`browser-apis.md`、`iframes.md`、`service-workers.md`、`websockets.md`）。
6. `debugging/` 目录 4 篇（`console-errors.md`、`debugging.md`、`error-testing.md`、`flaky-tests.md`）。
7. `frameworks/` 目录 4 篇（`angular.md`、`nextjs.md`、`react.md`、`vue.md`）。
8. `infrastructure-ci-cd/` 目录 9 篇（`ci-cd.md`、`docker.md`、`github-actions.md`、`gitlab.md`、`other-providers.md`、`parallel-sharding.md`、`performance.md`、`reporting.md`、`test-coverage.md`）。
9. `testing-patterns/` 目录 15 篇（`accessibility.md`、`api-testing.md`、`browser-extensions.md`、`canvas-webgl.md`、`component-testing.md`、`drag-drop.md`、`electron.md`、`file-operations.md`、`file-upload-download.md`、`forms-validation.md`、`graphql-testing.md`、`i18n.md`、`performance-testing.md`、`security-testing.md`、`visual-regression.md`）。
