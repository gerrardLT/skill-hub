# prototype

## Problem
在前端交互与核心组件设计过程中，开发者或团队往往容易陷入“过早收敛”（Premature Convergence）的陷阱——对一个交互组件（如 Toast、操作卡片、长按删除按钮）仅构建单一默认方案或微调色调的假性变体，无法直观对比截然不同的布局、时序与交互心智。此外，直接在生产代码上试验变体会造成代码污染与回归隐患。团队需要一种在完全隔离的环境下针对特定 UI 组件快速并发孵化多个真正发散、工业级水准的设计变体，并通过统一的悬浮切换器（Visual Picker）全尺寸动态比选与一键晋升的方法论。

## When to Use
- 需要针对某个具体 UI 组件或交互模式（如 Toast 堆叠、定价卡片、手势拖拽抽屉、长按确认按钮）探索多个具有实质差异的设计方案时。
- 探索过程中需要支持在真实尺寸与真实业务上下文中无感即时切换（Instant Switch）对比多个变体手感时。
- 用户通过显式指令调用（如 `<description>`、`<description> x5`、`riff <variant>`、`keep <variant>`）触发原型发散与比选时。

## When Not to Use
- 审查现存动效代码质量（应使用 review-animations）。
- 全局大范围页面的架构重构或全站设计系统抽取（应使用 redesign-existing-projects 或 extract-design-system）。
- 挑选底座 UI 依赖库或技术栈迁移选型。
- 纯非视觉的后端服务、数据接口或基础设施编码。

## Role
作为资深设计工程探索专家（Senior Design Engineer running a design exploration），核心职责在于驱动**实质发散（Divergence）**与**顶级工艺（Craft Bar）**并重。为同一个需求提供 3 到 5 个各自具备独立立足点的差异化变体，并通过标准悬浮切换器为用户交付客观决策权。

## Inputs
- 目标 UI 组件的自然语言描述（Brief，例如“一个支持滑动撤销的 Toast 堆叠”或“具备层级质感的定价卡片”）。
- 既有项目技术与设计上下文（Stack, Design Tokens, Product Personality, Context）。
- 伴随规范文件：`prototype/PICKER.md`（定义标准悬浮胶囊切换器的 HTML 结构、CSS 样式、快捷键与状态接线标准）。

## Outputs
- **隔离原型测试场（Isolated Prototype Surface）**：项目内独立路由页面（如 `/prototypes/<slug>`）或零外部依赖的单个自包含 HTML 文件。
- **全功能交互变体集（Fully-working Variants）**：3 到 5 个具有真实动效、完整按压状态与真实模拟数据的可交互变体组件。
- **逐字照搬的悬浮切换器（Standard Picker Chrome）**：支持 1~N 数字键、左右方向键、R 键重放动效与 URL 参数记忆的暗黑半透明胶囊选择器。
- **客观决策权衡表（Variant Tradeoff Table）**：清晰列出各变体的编号、名称、发散维度、胜出场景与付出代价。

## Workflow
1. **范围收敛（Phase 1 — Scope）**：单次运行仅聚焦单个高杠杆核心组件；若描述过宽，主动收敛并以单句陈述需求定位。
2. **勘察与对齐（Phase 2 — Recon）**：映射现有项目技术栈、设计变量（色彩、字阶、圆角、阴影）、产品性格（活泼消费级 vs 严肃控制台）以及组件渲染上下文；无项目时降级使用克制的中性灰与系统字体基线。
3. **确定发散维度（Phase 3 — Choose Directions）**：默认规划 3 个（最多 5 个）变体；为每个变体赋予性格化命名（如 Quiet, Editorial, Playful, Dense，严禁使用 Option A/B）与明确的独占发散轴（布局、密度、手感、物理模型），杜绝仅换强调色的假发散。
4. **构建原型测试场与装配切换器（Phase 4 — Build the Picker Harness）**：
   - 在独立路由或单 HTML 文件中构建宿主；
   - 逐字复制 `PICKER.md` 的 HTML、CSS 与 JS 逻辑装配悬浮胶囊；
   - 在真实上下文（非邮票缩略图）中全尺寸渲染单变体，保持变体间切换绝对即时（0ms 无过渡）。
5. **验证并交付决策（Phase 5 — Verify and Hand Off）**：自检所有变体的交互与控制台无报错；输出标准权衡表，交付给用户决策。
6. **晋升与清理（Phase 6 — Promote on Selection）**：用户选定后，将胜出变体集成至生产代码中，并彻底删除临时原型测试场。

## Branches
- **项目既有环境分支**：在具备本地开发服务器的项目中，开辟独立路由（如 `/prototypes/<slug>`），每个变体单独成文件。
- **无项目/独立探索分支**：生成单个包含内联 CSS 与原生 JS 的 HTML 文件，双击即可在浏览器中运行。
- **变体迭代 Riff 分支**：用户执行 `riff <variant>` 时，保留测试场并在胜出方向周围展开新一轮细分发散。
- **常驻测试场分支**：用户指示 `keep <variant>, leave the picker` 时，晋升代码同时保留原型测试场。
- **顶部停靠分支**：当被测试组件位于屏幕底部中央（如 Dock 栏、底部 Toast）时，切换器添加 `data-position="top"` 移至顶部。

## Rules
- **硬性隔离铁律**：原型探索期间严禁改动任何生产代码，所有实验逻辑严格局限于原型宿主中。
- **真机功能完整性**：所有变体必须完全可交互、动效真实、文案具象，严禁使用 Lorem Ipsum 或未接事件的死按钮。
- **切实发散原则**：所有变体必须具备明确的命名轴；两个仅差强调色或文案的变体必须合并或替换。
- **切换器不可定制**：悬浮切换器属于测试工具的固定仪表盘（Chrome），其 HTML/CSS 必须逐字照搬，严禁针对具体项目样式进行主题化适配。
- **即时切换无过渡**：切换器自身的高亮滑块允许 250ms 过渡，但变体内容的切换必须瞬间完成（Instant Switch），杜绝切换动画干扰手感比对。
- **事后必清理**：晋升完成后默认删除测试文件，不留冗余废代码。

## Exceptions
- 切换器位置微调：若测试组件自身渲染在屏幕底部中央，允许通过 `data-position="top"` 属性将切换器改置于屏幕顶部，防止遮挡。
- 重放按钮显隐：若所有变体皆为纯静态展示、无任何入场或状态动效，允许隐藏重放按钮（↻）与分割线。
- 变体数量弹性：默认 3 个，但在设计探索空间宽广或用户明确要求时可扩充至最多 5 个。

## Dependencies
- 依赖规范规范：`prototype/PICKER.md`（提供权威 HTML 结构、CSS 磨砂玻璃阴影与快捷键驱动脚本）。
- 运行依赖：现代浏览器原生 DOM API（支持 querySelector、requestAnimationFrame、URLSearchParams）。

## Permissions and Side Effects
- 文件写入与清理：在 `/prototypes/` 目录下创建原型组件与测试场，并在用户完成挑选后删除该目录。
- 生产代码写入：仅在 Phase 6 阶段根据用户显式指定的胜出变体，将其定向写入生产目录。

## Gates
- **发散性审核 Gate**：所有候选变体必须各自拥有独立、不重合的发散维度。
- **完整性自检 Gate**：开发者在交付前必须自行完整走查并验证全部变体可操作无报错。
- **决策保留 Gate**：权衡表必须客观呈现优劣，绝不能替用户预先指定胜出者。

## Open Questions
- 如何在复杂全局状态（如 Redux/Pinia）驱动的项目中，以最轻量级的 Mock 状态注入隔离的原型测试场。

## Unique Value
颠覆了“直接改代码看效果”的粗糙探索流，通过严格隔离的测试场、标准化的即时切换黑胶囊与诚实客观的双刃剑权衡表，将顶级设计工程的高发散探索与无污染交付完美闭环。

## Reading Coverage
全量阅读并吸纳 `skills/prototype/` 下的全部核心文件：
- `prototype/SKILL.md`（第 1 行至第 90 行）：包含 Operating Posture、5 大 Hard Rules、6 阶段工作流、调用变体命令与客观基调；
- `prototype/PICKER.md`（第 1 行至第 197 行）：包含悬浮切换器固定外观规范、标准 HTML 结构、CSS 磨砂样式、行为契约与原生 JS 参考接线实现。
