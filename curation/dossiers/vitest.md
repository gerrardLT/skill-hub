# vitest 来源能力档案

## Problem

在基于现代 ESM、TypeScript 和前端现代框架（React, Vue, Svelte 等）的项目中，传统的测试运行器（如基于 Webpack 或 Babel 的 Jest 配置）面临严重的转译阻抗与性能损耗：重复配置 Babel/ts-jest 规则繁琐易错；缺乏原生 ESM 模块解析支持；在大型代码库中冷启动极其缓慢且单机多核并行利用率低；并发执行测试时断言上下文混乱导致状态交叉污染；缺乏高效优雅的资源自动回收与参数化 Mock 机制。

## When to Use

- **全栈 TypeScript/JavaScript/JSX 单元与集成测试**：依托 Vite 原生管线与模块图，实现秒级冷启动与极速热更新测试。
- **并发用例上下文隔离验证**：在 `test.concurrent` 并发测试套件中，通过解构用例上下文（`{ expect }`）实现快照与断言的无干扰隔离执行。
- **自定义 Fixture 与强类型生命周期依赖注入**：利用 `.extend()` 构建具备 `onCleanup` 自动释放能力和文件/工作区作用域的通用测试夹具。
- **零运行时编译期静态类型测试**：使用 `expectTypeOf` 与 `assertType` 直接在 `.test-d.ts` 中对复杂泛型、重载及工具类型执行编译期健全性断言。
- **深度 Mock 与现代资源管理**：使用 `vi.fn()`、`vi.spyOn()`、`vi.when(...)` 声明式参数匹配器，配合 TypeScript `using` 关键字实现离开作用域自动恢复 Spy。

## When Not to Use

- **跨页面全生命周期真实浏览器 E2E 录制**：深层浏览器渲染与多窗口长流程应交给 Playwright。
- **黑盒网络爬虫与全站技术指标巡检**：无源码上下文的全站审计应使用 audit-website。

## Role

极速 Vite 原生测试运行器与质量保证引擎（Vite-Native Fast Testing Engine）。负责执行单元测试、集成测试、组件挂载测试、静态类型测试与代码覆盖率分析。

## Inputs

- **测试用例源码**：`*.test.ts`、`*.spec.ts`、`*.test-d.ts`。
- **测试与构建配置**：`vitest.config.ts` 或与 `vite.config.ts` 合并的配置对象。
- **运行控制参数**：CLI 参数（`--watch`、`--run`、`--coverage`、`--shard`、`--maxWorkers` 等）。

## Outputs

- **测试执行结果报告**：终端彩色摘要、详细调用栈帧，或导出为 JUnit、JSON、GitHub Actions 等结构化报表。
- **代码覆盖率报告**：基于 V8 或 Istanbul 的行、函数、分支覆盖率统计（支持 HTML 报告）。
- **快照比对基线**：`.snap` 文件或内联快照更新。

## Workflow

1. **配置探测与合并 (Config Resolution)**：
   - 自动加载 `vitest.config.ts` 或通过 `mergeConfig` 合并项目根目录 `vite.config.ts` 的插件与路径别名配置。
2. **测试文件收集与过滤 (Test Collection & Filtering)**：
   - 依据 `include` 模式（默认 `**/*.{test,spec}.?(c|m)[jt]s?(x)`）收集用例，响应 CLI 路径/标签/名称正则过滤。
3. **工作进程池分发 (Worker Pool Dispatch)**：
   - 启动 `forks` 进程池（或根据配置启动 `threads`、`vmForks`），分发测试文件并维持模块图隔离（`isolate: true`）。
4. **生命周期与 Fixture 装配 (Lifecycle & Fixture Setup)**：
   - 依次触发 `beforeAll`、`beforeEach` 钩子及夹具注入，构建用例上下文对象。
5. **断言执行与 Mocking 拦截 (Assertion & Mock Evaluation)**：
   - 执行用例代码，计算匹配器结果与快照差异，捕获异步未处理拒绝（Unhandled Rejections）。
6. **资源回收与 Spy 还原 (Cleanup & Teardown)**：
   - 触发 `onCleanup`、`afterEach` 钩子与 `using` 显式资源回收，重置 Fake Timers 与 Spy 还原。
7. **覆盖率收集与报表输出 (Coverage & Reporting)**：
   - 汇总各 Worker 采集的 AST/V8 覆盖率数据，输出最终退出码（Exit Code）。

## Branches

- **类型测试执行分支 (Typecheck Branch)**：通过 `--typecheck` 触发静态类型测试引擎，解析 `.test-d.ts` 并不产生实际运行时消耗。
- **多项目工作区分支 (Workspaces Projects Branch)**：在单体多包（Monorepo）架构下，通过 `defineWorkspace` 并行驱动不同环境（Node、JSDOM、SSR）的子项目测试。
- **基准测试分支 (Benchmarking Branch)**：运行 `vitest bench` 针对高频算法执行每秒操作次数（ops/sec）性能评测。

## Rules

- **并发断言上下文隔离原则**：在 `test.concurrent` 中必须严格解构 `{ expect }`，严禁使用顶层共享的全局 expect。
- **Mock 全局还原原则**：必须在配置层或全局前置钩子中配置 `restoreMocks: true`，杜绝跨测试用例污染。
- **显式异步等待原则**：针对 Promise 结果的断言必须显式 `await expect(...)`，严禁遗漏异步调用。
- **测试幂等与自包含原则**：所有用例必须彼此独立，禁止依赖前置用例落盘的临时数据或全局内存状态。

## Exceptions

- **环境限制降级**：在无原生 Node.js Worker 线程支持的环境下，通过配置 `pool: 'forks'` 采用独立子进程平稳运行。
- **未捕获错误防御**：默认严格打断测试；仅当明确测试特定框架边界时可通过局部配置放行。

## Dependencies

- **核心包**：`vitest`。
- **覆盖率驱动**：`@vitest/coverage-v8` 或 `@vitest/coverage-istanbul`。
- **DOM 环境包**：`jsdom` 或 `happy-dom`。
- **类型检查器**：`typescript`（与 `tsc`）。

## Permissions and Side Effects

- **权限要求**：本地文件系统读取权限、创建子进程与并发 Worker 权限、生成覆盖率报告写权限。
- **副作用**：在内存中占用多进程/多线程资源、在文件系统写入快照文件与覆盖率报表。

## Gates

- **Gate 1: Concurrent Context Destructuring Gate**：所有并发测试必须解构用例作用域 expect，防止断言状态竞态。
- **Gate 2: Coverage Threshold Gate**：CI 构建时覆盖率指标必须达到预设阈值。
- **Gate 3: Mock Leak Prevention Gate**：每个用例生命周期结束后必须无未还原的全局 Spy。

## Open Questions

- 针对大型大型 Monorepo 项目中 cross-project 模块重叠引用，如何进一步优化公共依赖内存缓存命中率？
- 在极深层嵌套异步流中，如何更直观地可视化异步等待超时的根因挂起栈？

## Unique Value

将 Vite 的极速转译优势无缝带入自动化测试领域，以极低的配置成本、极高的一致性生态（100% 兼容 ESM/Vite 插件）与现代化的 Mock/类型测试体验，为全栈应用开发提供了极致快速的质量守护屏障。

## Reading Coverage

本能力档案已 100% 覆盖以下主干及参考文件：
- `skills/vitest/SKILL.md` (总览与核心入口)
- `skills/vitest/references/core-config.md` (配置全景与 Vite 融合)
- `skills/vitest/references/core-cli.md` (命令行选项与运行模式)
- `skills/vitest/references/core-test-api.md` (测试函数与修饰符 API)
- `skills/vitest/references/core-expect.md` (断言匹配器与软断言)
- `skills/vitest/references/core-hooks.md` (生命周期与装配卸载)
- `skills/vitest/references/core-describe.md` (套件组织与标签修饰)
- `skills/vitest/references/features-mocking.md` (模拟函数与 vi.when 模式)
- `skills/vitest/references/features-snapshots.md` (文件与内联快照)
- `skills/vitest/references/features-coverage.md` (V8 与 Istanbul 覆盖率)
- `skills/vitest/references/features-context.md` (测试上下文与 Fixture 扩展)
- `skills/vitest/references/features-concurrency.md` (并发控制与分片)
- `skills/vitest/references/features-filtering.md` (用例过滤与正则匹配)
- `skills/vitest/references/features-test-tags.md` (标签化分类运行)
- `skills/vitest/references/features-reporters.md` (多格式结果报告器)
- `skills/vitest/references/features-benchmarking.md` (性能基准测试)
- `skills/vitest/references/advanced-environments.md` (JSDOM/Happy-DOM 运行环境)
- `skills/vitest/references/advanced-type-testing.md` (TypeScript 编译期静态类型测试)
- `skills/vitest/references/advanced-projects.md` (多项目工作区配置)
- `skills/vitest/references/advanced-vi.md` (vi 实用工具全集)
