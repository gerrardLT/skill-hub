# redesign-existing-projects

## Problem
现存的许多前端项目和 Web 应用程序充斥着泛滥的通用 AI 生成痕迹与模板化平庸设计（如到处滥用 Inter 字体、纯黑背景、过度饱和的三色混杂、三张等宽卡片构成的死板功能区、缺乏交互微反馈以及缺失加载/空白/错误状态等），使得产品显得廉价、死板且缺乏设计灵魂。然而，直接推倒重写会破坏原有的业务逻辑、带来沉重的回归风险。团队需要一套针对既有项目进行外科手术式无损改造（In-place Upgrade）、识别并清除 AI 设计指纹、注入高水准工艺标准的方法论。

## When to Use
- 针对既有网站或应用程序进行高保真重构与视觉品质升级时。
- 走查代码并系统性识别、清除通用 AI 模板模式（Generic AI patterns）与排版缺陷时。
- 在保持既有技术栈（Tailwind v3/v4、原生 CSS、CSS-in-JS 等）与业务功能完好无损的前提下，提升界面质感、交互反馈与无障碍水平时。

## When Not to Use
- 绿地全新项目的早期从零探索（应使用 prototype 或 design-taste-frontend）。
- 纯后端逻辑、数据库重构、API 设计或非视觉界面的重构工作。
- 架构全面颠覆或需要跨框架大迁移（如从 Vue 完全重写为 Next.js）的场景。

## Role
作为高级前端设计工程重构专家（Senior Design Engineer & Upgrade Specialist），坚持“尊重既有技术栈、坚守功能不破坏、外科手术式升级（Improve what's there, do not rewrite from scratch）”原则，通过系统审计清单逐项消除模板俗套，赋予产品独特的性格与现代工业级质感。

## Inputs
- 既有项目前端代码库（包含 HTML/JSX/TSX 结构、CSS/Tailwind 样式表、组件实现及依赖文件 `package.json`）。
- 既有项目的技术栈上下文（识别 Tailwind 版本、CSS-in-JS 方案或原生 CSS 结构）。

## Outputs
- **审计诊断清单（Diagnostic Audit Findings）**：按排版、色彩表面、布局、交互状态、内容文案、组件模式、图标与代码质量分类列出的违规与薄弱点。
- **定向升级代码补丁（Targeted Code Upgrades）**：按修复优先级（字体替换 -> 配色净化 -> 交互反馈 -> 布局呼吸感 -> 组件重构 -> 三态补全 -> 排版微调）实施的增量代码变更。

## Workflow
1. **代码扫描（Scan）**：阅读代码库，快速锁定框架类型、样式方案（Tailwind v3/v4、styled-components、原生 CSS）以及当前设计模式与依赖。
2. **系统诊断（Diagnose）**：严格对照设计审计八大维度（Typography、Color and Surfaces、Layout、Interactivity and States、Content、Component Patterns、Iconography、Code Quality、Strategic Omissions），逐项列出所有泛型模式、软肋与缺失状态。
3. **分步定向修复（Fix with Priority）**：
   - 步骤 1：字体升级（Font swap，换用 Geist/Outfit/Satoshi 等有性格的字体，开启 `tabular-nums` 与 `text-wrap: balance`）。
   - 步骤 2：色彩净化（Color palette cleanup，纯黑转炭黑，单一强调色，饱和度收敛至 80% 以下，消除 AI 蓝紫渐变，色彩阴影染色）。
   - 步骤 3：交互按压与焦点反馈（Hover/active states，添加 `scale(0.98)` / `translateY(1px)` 按压模拟与 200-300ms 平滑过渡，补全可见焦点环）。
   - 步骤 4：布局破局与留白（Layout & spacing，消除等宽三卡片，改用不对称网格/锯齿交错，改用 `min-height: 100dvh`，容器限宽 1200-1440px，对齐卡片底部按钮与 Y 轴基线）。
   - 步骤 5：替换陈旧组件模式（Replace generic components，去边框浮动、非药丸徽章、并列式 FAQ、非模态编辑）。
   - 步骤 6：状态补全（Loading/empty/error states，骨架屏替换通用转圈、精心设计空状态、内联表单校验错误）。
   - 步骤 7：排版微调与战略性补全（Polish typography & strategic omissions，补齐法律链接、返回导航、404、跳转内容 skip-link）。
4. **功能验证与防退化走查**：每次修改后验证交互与现有功能，确保零回归。

## Branches
- **Tailwind v4 分支**：遵循 `@theme` 与原生级 CSS 配置，杜绝遗留 `tailwind.config.js` 冲突。
- **Tailwind v3 分支**：遵循 `tailwind.config.js` 配置扩展，保持工具类兼容性。
- **原生 CSS / 无框架分支**：采用标准现代 CSS 变量、Flex/Grid 与 `@starting-style` 推进，不引入多余构建步骤。
- **渐进增强升级分支**：根据项目复杂度可选引入高阶技术（变体字体动画、视差卡片堆叠、平滑惯性滚动、真实玻璃拟态微边框、聚光灯边框与噪点纹理）。

## Rules
- **绝不推倒重写**：严禁推倒现有框架或强行更换样式方案，必须在现有代码基础上外科手术式改良。
- **功能不可破坏**：所有现存业务逻辑、表单提交、路由导航在重构后必须完好可用。
- **依赖预检铁律**：引入任何第三方字体或图标前，必须预检 `package.json`，严禁产生 import 幻觉。
- **AI 痕迹清除规则**：
  - 严禁纯黑 `#000000` 背景与泛滥的紫色/蓝色发光渐变。
  - 严禁假大空 AI 文案（绝对禁用 Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve, Tapestry 等）。
  - 严禁死板的等宽三卡片陈列。
  - 严禁所有标头无脑大写（Title Case），改用句子大小写（Sentence case）。
  - 严禁未染色的纯黑投射阴影。
  - 严禁 `height: 100vh` 移动端跳动。
- **严格遵循七级修复次序**：以最低风险换取最大视觉跃迁。

## Exceptions
- 数据密集型控制台/仪表盘：数字密集显示时，可提升视觉密度并强制启用等宽数字（`tabular-nums`），允许保留密集排版，但不适用于营销落地页。
- 模态弹窗豁免：对于极简操作或复杂多步设置，鼓励转化为内联编辑或抽屉；但对于破坏性二次确认，仍允许使用标准模态框。

## Dependencies
- 工具与平台依赖：支持现代 CSS 特性（Grid、`dvh`、`text-wrap: balance`、CSS Variables、`backdrop-filter`）。
- 外部占位资源依赖：图片占位符推荐 `https://picsum.photos/seed/{name}/1920/1080`。

## Permissions and Side Effects
- 文件修改权限：对现有组件与样式文件执行定点重构与修改。
- 零依赖破坏：不改动底层数据协议或接口签名。

## Gates
- **功能无损 Gate**：每次改造提交前必须确认原有交互、表单提交与路由未被破坏。
- **AI 痕迹清零 Gate**：检查是否彻底清除了禁用词汇、纯黑背景、无微按压反馈和等宽三卡片等特征反模式。

## Open Questions
- 如何在高度遗留且具有全局 CSS 污染的大型项目中，最安全地实施样式作用域隔离并逐步应用现代设计体系。

## Unique Value
构建了工业级现存前端重构指南，将虚浮的设计审美转化为清晰的八大维度走查表与七级可落地的递进实施次序，让开发者能够在不破坏业务连续性的前提下，将平庸或 AI 味道浓重的页面外科手术般提升为大师级作品。

## Reading Coverage
全量覆盖并融合源文件 `redesign-existing-projects/SKILL.md`（第 1 行至第 178 行）的全部核心章节，包括 How This Works 三步法、Design Audit 八大维度走查项、Upgrade Techniques 高阶进阶手法、Fix Priority 优先级排序以及核心工程纪律。
