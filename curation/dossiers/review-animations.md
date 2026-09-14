# review-animations

## Problem
在现代前端界面开发中，动效代码常常存在盲目添加、物理感知失真、性能卡顿以及破坏可访问性等严峻问题。许多开发者误将“看起来炫酷”作为添加动效的标准，导致高频操作与快捷键响应迟滞、使用了导致浏览器全量重排的非 GPU 布局属性（如 `width`、`height`、`top`）、下拉浮层原点漂移（错误居中）、未正确处理可中断动画（导致打断时闪烁归零），或者忽略了前庭神经失调人群的减弱动态偏好（`prefers-reduced-motion`）。团队亟需一套基于顶级设计工程（Emil Kowalski 哲学）的高标准动效审查协议。

## When to Use
- 在前端 UI 代码审查、PR Review 或设计工程走查中，专门针对 CSS/JS 动效、过渡（transitions）、关键帧（keyframes）以及 Spring 物理动画进行代码审查时。
- 检查组件交互手感（如按钮按压反馈、抽屉收起、弹窗展开、Toast 提示、列表入场、微交互）是否符合自然物理规律与响应预算时。
- 排查动效掉帧、布局抖动（Layout Thrashing）、样式重算风暴（Style Recalculation Storms）等渲染性能瓶颈时。
- 审查系统是否完善支持 `prefers-reduced-motion` 与非鼠标触摸设备的 `:hover` 伪类保护时。

## When Not to Use
- 审查通用非动效前端业务逻辑、纯状态管理、数据获取或后端接口实现（应分流至通用代码审查技能）。
- 全新功能的端到端功能编写或非动画相关的功能开发。
- 纯静态设计稿走查或尚未形成代码实现的低保真线框图阶段。

## Role
作为具备极度苛刻品味的高级设计工程师（Senior Design Engineer with a brutal eye for craft），采取“默认质疑、严格标记；唯有达标方予通过（Default to flagging; approval is earned）”的审查姿态。以自然手感、物理真实度与无感性能为准绳，识别瑕疵并提供确定性的物理参数与降级方案。

## Inputs
- 代码差异（Git diff）或目标动效实现源码（CSS、SCSS、Tailwind 工具类、Framer Motion/Motion、Web Animations API 或原生 JS 动画代码）。
- 动效触发频次与业务上下文（快捷键触发、极高频操作、偶发交互或首次探索）。
- 伴随规范文件：`review-animations/STANDARDS.md`（提供权威缓动贝塞尔曲线、毫秒级时长预算、物理弹簧配置参数表）。

## Outputs
- **Part 1：发现表格（Findings Table）**：强制单一 Markdown 表格格式，包含 `| Before | After | Why |` 三列，逐项列出违规前代码、修复后代码以及基于物理/性能准则的原因。
- **Part 2：裁决报告（Verdict）**：按六层影响级别（Feel-breaking regressions、Missed simplifications、Performance、Interruptibility & timing、Origin/physicality & cohesion、Accessibility）归类诊断说明，并以带有 `file:line` 精确坐标的明确终审裁决（`Block` 或 `Approve`）收尾。

## Workflow
1. **触发必要性审查（Justification & Frequency Check）**：核验动效存在价值；对照频次表，确认是否属于 100+/天或快捷键触发操作，若是则直接阻断并建议彻底删除。
2. **缓动与时长核验（Easing & Duration Budgeting）**：审查缓动曲线，绝对阻断 UI 交互中的 `ease-in`；核查入场是否使用 `ease-out` 或高阶贝塞尔；检验时长是否收敛在 300ms 预算内。
3. **物理正确性与原点定位（Physicality & Origin Verification）**：检查浮层/气泡是否锚定触发器原点（`transform-origin`），严禁 `scale(0)`，强制采用 `scale(0.9~0.97) + opacity: 0` 起步；模态框居中例外检查。
4. **可中断性与交互韧性核验（Interruptibility Check）**：核查高频触发元素（如 Toast、Toggle 开关）是否使用可平滑重定向的 CSS transitions 或物理弹簧，严禁打断归零的 keyframes。
5. **GPU 硬件加速与性能审计（GPU Performance Audit）**：严格禁止动画化布局属性（`width/height/margin/padding/top/left`）；排查父级 CSS 变量驱动子级 transform 引发的重算风暴；防范 Framer Motion 快捷属性在重负载下的主线程掉帧。
6. **无障碍与环境匹配（A11y & Environment Gating）**：核查 `prefers-reduced-motion` 适配（弱化位移保留渐变透明度）；确保 `:hover` 仅在支持悬停与精准指针设备生效。
7. **综合裁决与表格生成（Output & Verdict Assembly）**：生成标准的 `Before/After/Why` 对照表与分层裁决决议。

## Branches
- **Block 分支**：存在破坏手感的严重退化（Feel-breaking regression）、在快捷键/高频场景滥用动画、UI 中出现 `scale(0)` 或 `ease-in`、或存在显著非 GPU 布局动画。强制输出阻断裁决。
- **Approve 分支**：无破坏性手感缺陷、无多余冗余动画、时长与曲线均严格处于预算范围内、具备完善的可中断机制与 a11y 降级处理。予以通过。
- **预设动画分支（Predetermined Motion）**：采用 CSS transitions、`@starting-style` 或 WAAPI 实现主线程解耦与高性能。
- **动态手势驱动分支（Gesture-driven Motion）**：采用 Apple 风格或物理弹簧（Springs）实现平滑速度承接与惯性滑移。

## Rules
- **十大不可妥协准则（Ten Non-Negotiable Standards）**：
  1. 动效必须有合理性支撑（Justified motion），拒绝单纯炫技。
  2. 频次适度（Frequency-appropriate）：键盘快捷键与 100+/天动作严禁动画。
  3. 响应式缓动（Responsive easing）：入场必须用强 `ease-out`，UI 严禁 `ease-in`。
  4. 300ms 预算（Sub-300ms UI）：除大型模态与长展开外，常规 UI 必须 ≤300ms。
  5. 物理真实原点（Origin & physical correctness）：气泡/下拉从触发源缩放，严禁 `scale(0)`。
  6. 可中断性（Interruptibility）：频繁触发/手势交互必须可平稳重定向。
  7. 纯 GPU 属性（GPU-only properties）：仅允许 `transform` 与 `opacity`。
  8. 无障碍优先（Accessibility）：必须适配 `prefers-reduced-motion` 与悬停设备门禁。
  9. 非对称进出（Asymmetric enter/exit）：主动操作沉稳克制，系统反馈干脆利落。
  10. 质感统一（Cohesion）：动效契合产品调性，无法确定手感时优先删除动效。
- **整改优先级阶梯（Remedial Hierarchy）**：
  1. 删除动画 -> 2. 缩减幅度与时长 -> 3. 修正缓动曲线 -> 4. 纠正原点与缩放起始值 -> 5. 改为可中断过渡 -> 6. 迁移至 GPU 属性 -> 7. 应用非对称时序 -> 8. 细节打磨（模糊过渡、交错延迟） -> 9. 补齐 a11y 与调性调优。
- **输出格式铁律**：Part 1 必须为单张 Markdown 表格（禁止出现 Before:/After: 文本列表）；Part 2 必须给出按层级归类的评语与 Block/Approve 判定，并精确引用 `file:line`。

## Exceptions
- 模态对话框（Modals）：由于其在视口正中呈现，免除“从触发源锚定原点”的约束，允许保持 `transform-origin: center`。
- 营销宣传页与新手引导（Marketing & Onboarding）：属于极低频（Rare/first-time）交互，允许突破 300ms 时长预算并融入探索性愉悦感。
- 减弱动态偏好（Reduced Motion）：并非完全消除所有动画，而是保留透明度（opacity）与色彩变化以辅助用户理解，剔除大幅度的空间位移与剧烈缩放。

## Dependencies
- 依赖标准文档：`review-animations/STANDARDS.md`（包含 `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` 等标准曲线、时长区间与 Spring 物理配置）。
- 外部缓动参考源：`easing.dev` 与 `easings.co`。

## Permissions and Side Effects
- 只读静态分析：审查流程纯属代码比对与静态评估，无代码写回或构建操作。
- 声明 `disable-model-invocation: true`，作为确定性的指令规范运作。

## Gates
- **阻断判定 Gate**：存在任何 feel-breaking 问题（包括 `scale(0)`、`ease-in`、快捷键动画、非 GPU 属性滥用）一票否决为 Block。
- **格式合规 Gate**：输出报告必须由单张 Markdown 发现表格与六层结构化裁决构成，缺少表格或裁决模糊视为未完成。

## Open Questions
- 在集成化 CI/CD 流水线中，如何通过 AST 静态扫描自动化拦截 `scale(0)` 与 `transition: all`，将人工审查精力收敛至纯手感调优。

## Unique Value
将世界顶级动效设计工程师（Emil Kowalski）的手感审美与严苛的工程审查纪律完美熔炼，提供了可量化的频次决策表、毫秒级时长规范、物理弹簧阻尼模型、GPU 性能防护网与结构化裁决协议。

## Reading Coverage
全量覆盖并提炼 `review-animations/SKILL.md`（第 1 行至第 112 行）与 `review-animations/STANDARDS.md`（第 1 行至第 187 行）两份核心资产的所有动效准则、数值标准、物理模型与审查输出规范。
