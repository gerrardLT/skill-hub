# Impeccable Dossier

## Problem
在前端与用户界面研发过程中，AI 辅助或传统开发产出的界面极易陷入平庸（Bland）、保守（Timid）、千篇一律的“模板化与大模型俗套”（如无脑采用卡片堆叠、居中大字报、相同样式的毛玻璃与渐变文字）。同时，团队往往缺乏清晰的设计系统契约（DESIGN.md）与产品语境（PRODUCT.md），陷入无休止且高成本的“边改边看”微调循环（Open-ended self-QA），缺乏严格的质量底线（Craft Floor）以及客观、独立的审美与工程质量验收标准。

## When to Use
- 全面启动新页面设计（New Work）、重塑老旧项目视觉体系（Redesign）或扩展现有界面功能（Refinement）；
- 执行启发式 UX 深度审查（`critique`）、技术质量与无障碍走查（`audit`）；
- 发版前像素级终审（`polish`）、激进化提振平淡界面（`bolder`）、降噪收敛过激界面（`quieter`）或精简冗余（`distill`）；
- 增强界面的微动效（`animate`）、战略色彩（`colorize`）、排版层级（`typeset`）、视觉节奏（`layout`）与品牌记忆点（`delight`）；
- 生产环境加固（`harden`：错误态、空状态、极端数据边界与国际化适配）与多端响应式/原生系统适配（`adapt`：Web、iOS、Android）。

## When Not to Use
- 纯后端逻辑、底层分布式架构、无头服务或纯命令行工具研发（无任何 UI 呈现）；
- 简单的单行样式 Bug 修复且已有明确固定规范无需重新定调的场景；
- 试图规避设计审查，进行不受约束的无休止微调试错循环。

## Role
获奖级设计总监（Award-winning Design Director），具备极致的审美判断力、敏锐的文化世界构建能力、严谨的前端工程素养以及不妥协的工艺底线（Out-of-distribution craft）。

## Inputs
- **必备参数**：`$ARGUMENTS`（包含子命令如 `shape/audit/critique/polish/bolder` 与目标页面/组件路径 target）；
- **核心契约文档**：`PRODUCT.md`（产品真相、用户价值与业务约束）与 `DESIGN.md`（持久视觉世界决策、Design Tokens 与组件规范）；
- **上下文材料**：页面路由、现有代码、组件库、Token 体系、主题配置与资产文件；
- **平台类型**：Web 响应式或原生平台（iOS / Android / Adaptive）。

## Outputs
- 结构化设计决策产物：
  1. **开篇设计契约（Direction Contract）**：写入根组件 HTML 开头注释中的 5 段式契约（THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM, FINISH）；
  2. **生产就绪的前端代码**：兼具语义化 HTML、稳健 CSS/Tokens、自适应排版与交互动效的高保真实现；
  3. **视觉系统规范**：由 documenter 闭环生成的权威 `DESIGN.md` 及其 sidecar；
  4. **全套走查审查报告**：包含桌面/移动端（或多设备类）截图、质量底线核对、缺陷检测 findings 与最终评级处置（recapture/rebuild/fix/ship）。

## Workflow
1. **上下文建立与路由分发**：检查项目语境，定位子命令规范（或进入 `new-work.md` 世界构建流）；若缺失 `PRODUCT.md` 则引导 `init`，若已存在视觉系统则优先继承；
2. **确定用户心智模式（Mode Selection）**：基于受访页面属性划定为 Persuade（说服转化）、Operate（高效操作）、Read（深度阅读）或 Experience（沉浸体验）；
3. **视觉世界构建或继承**：
   - 继承模式：针对既有页面做局部扩展，继承原有设计语言，不擅自推翻全局系统；
   - 重建/新创模式：从目标受众的文化世界中提取 7 种物理/视觉系统，经由决策卡片与竞品卡牌对决，确定最终视觉路线；
4. **确立构建路径契约**：明确选择 Comp-led（效果图高保真像素级还原）或 Code-led（以首屏构图与物理微交互代码为契约），并在根节点写入 Direction Contract；
5. **全力以赴实施构建（Build with Full Commitment）**：
   - 跨过质量底线（Craft Floor）：严格遵从对比度、阴影深度、字体律动、系统原生细节（选区、光标、滚动条）等底层硬指标；
   - 恪守拒绝项（Refuse）：坚拒无脑卡片堆叠、无意义渐变文字、伪新丑硬阴影、Unicode 图标滥用及 eyebrow 眉题；
   - 首屏即论点：以首屏证明机制，严禁空洞的通用 Hero 壳子；
6. **有界两轮审查与闭环修复（Inspect and Finish）**：
   - 双端批次截图（桌面 + 移动端，或原生设备类），拒绝逐项琐碎截图；
   - 严格依据四种处置决策流转：`recapture`（证据失效重截）、`rebuild`（保真度彻底崩溃全量重构）、`fix`（单批次集中修复）、`ship`（质量达标放行）；
   - 最多两轮修复闭环，两轮后向用户透明展示待决表；
7. **自动化沉淀设计系统**：由 documenter 基于已验证的真实页面反向提取并落盘 `DESIGN.md`。

## Branches
- **四种访客模式分支**：
  - *Persuade（说服）*：视觉即产品，允许更大胆的色彩与形式，首屏即要求阐明主张并引导核心转化；
  - *Operate（操作）*：任务完成优先，可扫视性、一致性与系统原生预期高于张扬表现，采用克制配色；
  - *Read（阅读）*：以文本阅读与理解效率为第一优先级，注重排版网格、行宽（65-75ch）与舒适行高；
  - *Experience（体验）*：界面退居幕后，艺术品与交互对象占据视觉焦点；
- **构建路径分支**：
  - *Comp-led*：具备图像生成能力时，以效果图为绝对空间契约，经历像素级分块重构，严禁打折；
  - *Code-led*：无图环境直接在代码中兑现首屏构图与动效语法，严守行为与排版承诺；
- **任务边界分支**：
  - *Refinement（精雕）*：保留现有品牌资产、行为与文案；
  - *Redesign（重塑）*：彻底推翻旧世界，将旧视觉作为反向证据，重新确立 DESIGN.md；
  - *New Work（新创）*：无前置约束或开拓全新独立表面。

## Rules
- **简报至上规则（The Brief Wins）**：明确锁定的风格、时代感、材料、字体与色板高于模型预设偏好；
- **质量底线机械硬指标（Craft Floor Mechanics）**：
  - 正文对比度 ≥4.5:1，大号文字 ≥3:1；二次文字必须从底色或前景色中提色，禁止无脑中性灰；
  - 阴影必须具备位移（offset）与柔和模糊（soft blur），拒绝无位移彩色光晕与伪复古无模糊硬块；
  - 正文行宽严格保持在 65–75ch，标题行距均衡且上方间距显著大于下方；
  - 系统原生边角料重绘：文本选区（selection）、输入光标（caret）、自定义滚动条（scrollbars）与聚焦环（focus rings）必须由专属配色重绘；
- **绝对禁令与反模式拒绝（Absolute Refusals）**：
  - 严禁在标题上方添加 kicker/eyebrow 标签；
  - 严禁全页面使用无差异相同尺寸的卡片堆叠（Cards are the lazy container）；
  - 严禁非新丑主义世界中使用 `4px 4px 0` 的生硬无模糊描边阴影；
  - 严禁使用 Emoji 或 Unicode 符号冒充专业图标库；
  - 严禁无目的使用文字渐变（Gradient text）或为了装饰而装饰的毛玻璃（Glass blur）；
- **有界审查两轮封顶法则（Bounded Passes Ceiling）**：审查必须在有界轮次中批次运行，两轮修复为绝对上限，严禁陷入单项微调的无尽循环；
- **零脚本执行与快照只读不变量**：完全保持 `skills/` 快照只读，严禁在本地执行来源目录中的 Node/JS 自动化脚本或外部探测器。

## Exceptions
- **缺少 PRODUCT.md**：在新页面或世界构建时必须前置触发 `init` 补充语境；但在狭窄的代码局部精修时，允许基于既有实现直接推进并在事后提供补齐选项；
- **原生多端平台适配（iOS/Android）**：当目标为移动原生平台时，自动切换至对应的原生设计规范（`audit.native.md`、`adapt.native.md`），以平台原生手势与容器规范为准；
- **不可恢复的保真度偏差**：当审核给出 `rebuild` 裁决时，跳过琐碎修补，必须整块重构指定区域。

## Dependencies
- **前置需求输入**：功能定义、用户故事与 PRD（来自 `prd-development` 或产品套件）；
- **下游协同产出**：前端代码实现、`DESIGN.md` 设计契约、测试走查输入（提供给 `web-accessibility`, `playwright`, `design-review`）。

## Permissions and Side Effects
- 读取权限：只读检索工作区中的源码、样式、Token、布局与资产文件；
- 写入权限：创建或修改前端界面代码文件、写入 Direction Contract 注释、生成/更新 `DESIGN.md`；
- 禁止权限：严禁运行来源包中的不可信执行脚本（`scripts/*.mjs`），严禁篡改技能快照基线。

## Gates
- **首屏论点门禁（First Viewport Thesis Gate）**：首屏必须直接阐明产品核心机制，严禁交付空洞模式化 Hero 壳子；
- **质量底线门禁（Craft Floor Compliance Gate）**：所有界面交付物必须 100% 满足对比度、排版行宽、阴影真实感及系统边角料重绘要求；
- **反模式零容忍门禁（Anti-Pattern Zero-Tolerance Gate）**：交付代码中不得包含 kicker 眉题、纯卡片懒惰布局或伪新丑生硬阴影；
- **审查四态闭环门禁（Four-Disposition Review Gate）**：审查过程必须明确归入 recapture、rebuild、fix 或 ship 四大处置状态，未达到 ship 状态且未经过两轮封顶仲裁前不得标记交付。

## Open Questions
- 当设计总监的高保真诉求（如复杂物理动效、全屏 WebGL 渲染）与低端设备的运行性能预算发生剧烈冲突时，自动化的降级阶梯与 dev-loop 验收门禁如何做动态权衡？

## Unique Value
打破 AI 大模型代码生成在设计领域的“平庸保守”与“套模死穴”，建立起一套集世界构建、四维心智模式、机械化质量底线、反模式绝杀清单与有界双轮独立审查于一体的获奖级设计中枢。

## Reading Coverage
- 完整阅读并覆盖 `skills/impeccable/SKILL.md`（86 行）、`reference/craft-floor.md`（44 行）、`reference/new-work.md`（120 行）以及 37 个相关子命令与原生规范。
- 108 个内部 Node/JS 自动化运行期探测与服务器脚本标记为 excluded，从语义规范中剥离以保障离线安全纯洁性。
