# systematic-debugging Dossier

## Problem
在排查软件缺陷、测试失败或线上突发异常时，工程师往往因时间紧迫或惯性思维而凭直觉进行“随机盲猜与试错修改（Guess-and-check）”。这种针对表面症状的快速打补丁（Symptom fixes）不仅无法根除真实诱因，反而会掩盖底层隐患、破坏调用契约并在其他模块引入二次缺陷。同时，缺乏科学排查体系会导致在深层调用栈回溯、跨多组件边界数据流追踪、异步竞态条件等待以及测试污染源二分定位上面临巨大耗时与反复折腾。

## When to Use
1. 遭遇任何技术故障、测试失败、构建崩溃或线上生产事故时。
2. 面对复杂的深层调用栈错误，需要从症状发生点向后回溯（Trace backward）至原始触发源时。
3. 多组件/多层级系统（如 CI -> 构建 -> 签名，API -> 服务 -> 数据库）发生故障，需要在组件边界添加诊断探针时。
4. 修复数据污染或非法数据传播漏洞，需要实施四层深度防御校验（Defense-in-depth）时。
5. 针对异步多线程、事件驱动或时间竞争导致的偶发测试失败（Flaky tests），需要以条件轮询替代固定延迟（Condition-based waiting）时。
6. 测试套件中出现污染外部环境的幽灵状态，需要快速二分排查污染源测试（`find-polluter.sh`）时。

## When Not to Use
1. 需求尚未明确的高层业务头脑风暴或 PRD 阶段。
2. 架构设计与正常业务功能开发编码（在无 Bug 或未失败的前提下应路由至 `writing-plans` 与 `test-driven-development`）。
3. 纯静态设计样式走查或可访问性合规性审查（应路由至 `design-review` 或 `web-accessibility`）。

## Role
资深系统故障诊断专家与根因分析专家（Principal Debugging Specialist），坚决贯彻“铁律：未完成根因调查，绝不提出修复代码”，坚持运用科学假说验证法、多层防御机制与条件等待范式，确保任何缺陷均在根源被彻底消除且结构性不可复现。

## Inputs
1. **Failure Symptom & Error Payload / 失败症状与报错信息**：完整的终端控制台输出、错误代码、异常堆栈（Stack traces）与复现步骤。
2. **Recent Changes & Environmental Context / 近期改动与环境上下文**：近期 Git 提交、配置漂移、环境差异与依赖变更。
3. **Target System Baseline / 目标系统基线**：涉及的组件边界、架构设计与测试套件。

## Outputs
1. **Root Cause Diagnosis / 根因诊断报告**：明确陈述缺陷诱因何在（What）、为何发生（Why）以及完整的回溯数据流路径。
2. **Minimal Failing Reproduction Test / 最小失败复现测试**：在动手修复前建立的、可稳定触发缺陷的自动化测试或脚本。
3. **Root-Cause Surgical Fix / 根因外科手术级修复**：精准作用于原始触发源的最小代码改动，坚决不包含非相关改动。
4. **Defense-in-Depth Hardening / 深度防御加固产物**：API 边界校验（Layer 1）、业务逻辑校验（Layer 2）、环境防护卫士（Layer 3）及取证调试日志（Layer 4）。
5. **Deterministic Verification Evidence / 确定性验证凭据**：复现测试从失败转为通过，所有存量用例保持全绿且输出纯净。

## Workflow
1. **Phase 1: Root Cause Investigation / 根因调查（强制前置）**：
   - 仔细阅读完整错误堆栈与行号，不跳过任何告警；
   - 建立稳定一致的复现路径；若不可稳定复现，继续收集数据而非凭空猜测；
   - 检查近期 Git 改动、依赖更新与环境差异；
   - 在多组件系统边界注入结构化诊断日志，确定断裂发生在哪一层；
   - 运用 `root-cause-tracing.md` 向后回溯调用链路至脏数据起源。
2. **Phase 2: Pattern Analysis / 模式对比分析**：
   - 在同项目中寻找同类正常运行的代码样本；
   - 完整、逐行研读参考实现的每一处细节；
   - 详尽列出正常与异常路径的所有细微差异，分析隐含假设与依赖关系。
3. **Phase 3: Hypothesis and Testing / 假说构建与最小测试**：
   - 形成单一、具体的假说（"I think X is the root cause because Y"）；
   - 执行最小化的单变量验证实验；
   - 若验证成功推进至 Phase 4；若推翻假说，形成新假说，严禁在错误方向上叠加补丁；不知晓时坦率承认并深入调研。
4. **Phase 4: Implementation & Verification / 根因修复与深度加固**：
   - 先编写失败复现测试（严格遵循 `superpowers:test-driven-development`）；
   - 针对根因实施单一、精准修复（无无关重构）；
   - 验证测试通过且全套用例无回归；
   - 若尝试修复累计达到 3 次均失败，立即**中止盲目修补，质询基础架构缺陷**（Coupling/Shared state），并与人类协作者展开架构重构讨论。
5. **Supporting Hardening / 支撑技术加固**：
   - 依据 `defense-in-depth.md` 在四个层级布设检查点；
   - 依据 `condition-based-waiting.md` 将测试中的硬编码 sleep 替换为高效条件轮询；
   - 必要时运行 `find-polluter.sh` 二分剔除测试环境污染源。

## Branches
- **Branch A: Standard Root-Cause Cycle / 标准单组件根因修复**：堆栈定位 -> 回溯分析 -> 假说验证 -> TDD 红绿修复 -> 存量校验。
- **Branch B: Multi-Component Boundary Diagnostic / 多组件边界穿透分支**：在工作流、构建脚本、环境配置及底层运行时各边界逐层输出状态日志，定位故障组件后再收敛调查。
- **Branch C: Architectural Impasse Escalation / 架构死局升级分支（3+ 修复失败）**：当连续 3 次修复均在不同位置引爆新症状或需要巨型重构时，判定为架构性耦合问题，停止修补并提交重构讨论。
- **Branch D: Flaky Test Synchronization / 偶发异步测试治理分支**：识别任意 `setTimeout/sleep`，引入基于 10ms 步进与超时守护的 `waitFor` / `waitForEvent` 条件轮询。

## Rules
1. **铁律（The Iron Law）**：**未完成阶段 1 根因调查，绝不提出修复方案（NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST）**。严禁仅凭直觉打补丁。
2. **严禁仅修症状（Never Fix Symptoms）**：错误暴露在调用栈深处时，必须层层追问“谁调用了它、传入了什么值、该值源自何处”，直到在源头解决问题。
3. **三次失败停止法则（Three Strikes Rule）**：累计尝试 3 次修复仍未奏效，必须立即停手！这绝非假说失败，而是暴露出系统架构级耦合与状态混乱，必须质询基础架构而非尝试第 4 次盲修。
4. **四层深度防御原则（Defense-in-Depth）**：修复脏数据缺陷时，必须在数据穿透的每个节点施加校验（入口校验、领域校验、环境防护、调试捕获），使 Bug 在结构上不可复现。
5. **坚决根除测试硬编码超时（Condition-Based Waiting）**：严禁在异步测试中使用随意的 `sleep/setTimeout` 赌时序；必须通过条件断言轮询，兼顾速度与稳定性。
6. **红旗警告一票否决**：一旦出现“先临时修一个应急”、“一次性改多处试试”、“参考实现太长我先随意改改”等心态，立即停止并重返 Phase 1。

## Exceptions
1. **真·外部环境/不可抗力因素**：在严格执行阶段 1–3 排查后，若确认故障纯属外部第三方基础设施宕机或外部物理网络阻断，记录完整调查证据链，转为引入合理的降级重试与超时熔断保护。
2. **测试特定时序行为**：仅在测试针对 debounce/throttle 等纯时间间隔特性时，允许在条件等待后附加经充分注释说明的固定延时。

## Dependencies
- `superpowers:test-driven-development`：承接 Phase 4 Step 1 编写失败复现测试。
- `superpowers:verification-before-completion`：在宣布故障彻底修复前进行完工闭环验证。
- 基础命令行工具（`find`, `sort`, `bash`）。

## Permissions and Side Effects
- **只读分析**：阅读日志、堆栈、源代码、Git 历史。
- **诊断性注入**：在受限边界添加临时性 `console.error` 或环境日志进行取证。
- **代码重构与加固**：创建自动化复现测试、在根源位置应用修复、在多层级写入防御性断言。

## Gates
- **G-Phase-1-Complete**：在提出任何代码变更前，必须完整回答根因所在与证据链。
- **G-Single-Hypothesis**：每次验证必须为单变量最小改动。
- **G-Failing-Repro-Test**：编写修复前必须已存在能稳定复现故障的失败测试。
- **G-Three-Fixes-Halt**：修复失败达到 3 次时，强制阻断进一步修补并转入架构评审。

## Open Questions
1. 在高并发内存泄漏或底层垃圾回收异常场景中，如何以最小开销固化自动化回归测试？
2. 如何在跨微服务异步消息网状拓扑中自动化推导数据流向后回溯链？

## Unique Value
提供了工业级确定性的故障排查与根因解决规范体系。彻底终结了靠运气猜错修补的恶性循环，通过“四阶段科学假说、反向回溯追踪、三次失败质询架构、四层深度防御与条件轮询”组合拳，使复杂故障排查周期缩短 80% 以上，并从根本上阻断了缺陷的二次蔓延。

## Reading Coverage
- `skills/systematic-debugging/SKILL.md`: lines 1-296 (全部 296 行，四阶段科学调试、铁律、多组件诊断、反借口、红旗与三次失败架构质询)
- `skills/systematic-debugging/root-cause-tracing.md`: lines 1-169 (全部 169 行，反向追溯链推演、堆栈注入取证、空目录实战案例与不可仅修症状原则)
- `skills/systematic-debugging/defense-in-depth.md`: lines 1-122 (全部 122 行，多层防御哲学、四层校验架构代码范式与实战收益)
- `skills/systematic-debugging/condition-based-waiting.md`: lines 1-115 (全部 115 行，条件等待原则、轮询模式、常见陷阱与合法延时场景)
- `skills/systematic-debugging/condition-based-waiting-example.ts`: lines 1-158 (全部 158 行，waitForEvent, waitForEventCount, waitForEventMatch 完整实现与前后对比)
- `skills/systematic-debugging/find-polluter.sh`: lines 1-63 (全部 63 行，二分查找测试污染源脚本完整实现)
- 覆盖率：100% (6/6 核心可达文件全部覆盖，无遗漏)
