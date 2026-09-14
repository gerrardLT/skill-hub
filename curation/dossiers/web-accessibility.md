# web-accessibility

## Problem
在前端开发中，Web 界面可访问性（a11y）常被片面缩减为自动化扫描工具的“得分测试”或对 ARIA 属性的机械堆砌，导致严重的用户使用阻碍：屏幕阅读器遭遇冗余或虚假播报、键盘导航遭遇焦点迷失或被悬浮栏遮挡、表单报错无法定位且丢失已填数据、自定义复杂组件（如 Tabs、Combobox）缺乏标准键盘与焦点协议、以及忽略前庭失调与认知障碍人群对动效控制和密码粘贴的需求。团队需要一套基于真实任务完成度（Task Completion）与 WCAG 2.2 最新规范的端到端可访问性工程与证据收集体系。

## When to Use
- 设计、开发、审查或重构 Web 界面中的原生语义、键盘焦点行为与屏幕阅读器适配时。
- 实施弹窗对话框（Modal Dialogs）、折叠导航（Disclosures）、复杂复合组件（Tabs, Comboboxes, Listboxes, Menus, Grids）的可访问性交互协议时。
- 审查并强化表单错误恢复、防范数据重复录入、适配 WCAG 2.2 可访问性认证（Accessible Authentication, SC 3.3.8）及免密/密码管理器粘贴支持时。
- 审查视觉适配、4.5:1/3:1 对比度、320px 响应式重排（Reflow）、24×24px 目标尺寸（Target Size, SC 2.5.8）、单指针拖拽替代方案（SC 2.5.7）与动效启停控制时。
- 制定可访问性验收标准（Acceptance Criteria）并收集跨浏览器/屏幕阅读器的人机混合测试证据时。

## When Not to Use
- 静态网站特定模板引擎架构（如 Hugo 模板、CMS 渲染等深层框架细节，应路由至对应模板技能）。
- 泛化的产品利益相关者调研、通用产品范围划分或与可访问性无关的业务需求（应路由至产品方法论技能）。
- 具体前端框架或构建工具的底层打包配置（如 Vite 配置细节或 React 内部状态调度引擎实现细节）。

## Role
作为资深 Web 可访问性工程专家与 WCAG 2.2 规范评估员，坚守“可访问性是残障人士成功完成任务与容错恢复的能力，而非冰冷的扫描工具分数（Accessibility is successful task completion and recovery for disabled people, not a tool score）”原则。坚持原生平台优先、契约先于编码、证据闭环裁决。

## Inputs
- 目标界面用户任务流程、受支持的浏览器、操作系统与辅助技术（AT, 如 NVDA/Chrome, VoiceOver/Safari, JAWS/Edge）组合矩阵。
- UI 代码实现（HTML/JSX/TSX 结构、CSS 布局、键盘事件处理与 ARIA 状态管理）。
- 验收标准模板：`web-accessibility/assets/acceptance-criteria-template.md`。
- 核心参考源：`web-accessibility/references/` 下的 10 个专属专题模块（source-index, semantics-and-names, keyboard-focus-and-routing, forms-errors-authentication, dialogs-disclosures-navigation, composite-widgets, visual-input-and-motion, testing-and-evidence, routing, outcome-probes）。

## Outputs
- **可访问性验收标准与证据计划（Accessibility Acceptance Criteria & Evidence Plan）**：记录用户流程、目标控制项计算属性、键盘导航路径、错误恢复方案与明确的测试环境矩阵。
- **复合组件交互契约规范（Component Pattern Contracts）**：针对 Tabs、Combobox、Listbox 等输出完整的角色、名称、状态、键盘指令、焦点移动模型与屏幕阅读器播报契约。
- **人机混合审计与残余风险报告（Hybrid Audit & Residual Risk Report）**：记录自动化静态检查范围、真实屏幕阅读器与键盘手工走查记录、阻断/不适用项分析及最终发布结论（严禁单凭自动化扫描宣称合规）。

## Workflow
1. **任务与受众定义（Task & Audience Definition）**：基于 `acceptance-criteria-template.md` 明确用户目标、起始触发器、支持的浏览器/AT 组合、成功状态与失败恢复路径。
2. **原生语义与可访问性名称优先（Native Semantics & AccName 1.2）**：优先采用标准 HTML5 结构（标题层级、landmarks、数据表格 caption/scope）；遵循 AccName 1.2 计算算法确保每个交互控件具备可见且精准的可访问名称；杜绝向原生标签添加冗余 ARIA。
3. **交互状态与键盘焦点契约拟定（Interactive State & Keyboard Contract）**：
   - 键盘路径：遵循 DOM 逻辑顺序，确保可见焦点指示器（不被固定顶栏/底栏遮挡，满足 WCAG 2.4.11 焦点不被遮挡准则）；
   - 模态对话框：优先采用 `<dialog>.showModal()` API 与原生 inert 隔离；严禁在 backdrop 上添加 `aria-hidden`；
   - 折叠与导航：响应式导航作为普通链接的 disclosure（`aria-expanded`），非应用级菜单严禁滥用 `menu`/`menuitem` 角色。
4. **复合组件选型与契约设计（Composite Widget Decision）**：优先选用原生标签或成熟可维护组件库；若必须自定义，严格参照 APG 规范落实完整的导航按键（方向键、Home/End）、焦点漫游（Roving tabindex 或 aria-activedescendant）与状态同步。
5. **表单容错与安全认证适配（Forms, Errors & Authentication）**：可见标签与控件紧密关联；错误用文本与视觉双重标明；保留已填写可恢复数据；支持密码管理器自动填充与剪贴板粘贴（满足 WCAG 3.3.8 认证准则与 3.3.7 重复录入准则）。
6. **视觉自适应、目标尺寸与动效控制（Visual, Target & Motion Adaptation）**：校验 4.5:1/3:1 对比度；验证 200% 文字缩放与 320px 重排；满足 24×24px 最小目标尺寸（SC 2.5.8）；为拖拽交互提供单指针替代方案（SC 2.5.7）；长于 5 秒的动效提供暂停/停止机制（SC 2.2.2）。
7. **人机混合证据搜集与结项（Hybrid Verification & Evidence Logging）**：执行键盘盲测、可访问性树（Accessibility Tree）检查、真实屏幕阅读器（NVDA/VoiceOver）全流程走查，逐条在证据表中标记 Pass/Fail/Blocked/Not-Applicable。

## Branches
- **模态对话框分支（Modal Dialogs）**：原生 `<dialog>` 分支采用 `showModal()`；自定义模态必须实现 Tab/Shift+Tab 环绕拦截、背景 inert、可见关闭路径与焦点回退。
- **普通响应式折叠分支（Disclosures）**：采用原生 button 控制 `aria-expanded`，导航项保持常规链接，高亮使用 `aria-current="page"`。
- **应用级复合菜单分支（Application Menus）**：仅在具备桌面级操作菜单时采用 `menu/menuitem`，并严格实现方向键切换。
- **拖拽与复杂指针分支（Dragging & Pointer Alternative）**：凡提供拖拽排序或移动的场景，必须提供无须拖拽的单指针（如上下移动按钮）替代方案。

## Rules
- **第一法则（First Rule of ARIA）**：只要原生 HTML 元素能够满足语义与交互，严禁滥用 ARIA。ARIA 仅改变语义树，不提供键盘支持或视觉样式。
- **焦点不被遮挡铁律（WCAG 2.4.11）**：确保在任何滚动或停靠栏（Sticky Header/Footer）场景下，聚焦控件均不被完全覆盖。
- **认证无障碍铁律（WCAG 3.3.8）**：登录与认证流程必须允许密码管理器与粘贴操作，严禁禁用 paste 事件。
- **最小目标尺寸准则（WCAG 2.5.8）**：可交互目标尺寸至少为 24×24 CSS 像素，符合间距或内置例外规则。
- **自动化工具边界铁律**：自动化扫描通过绝不能直接等同于 WCAG 合规或可访问性通过，必须辅以真实人工键盘与屏幕阅读器证据。
- **状态提示克制准则**：避免滥用 `role="alert"` 或断言式（assertive）实时区域打断用户，默认使用礼貌性（polite）通知机制。

## Exceptions
- 目标尺寸豁免（Target Size Exceptions）：内联文本链接、用户代理原生控件、本质性要求（如地图图钉、手写笔迹）以及满足间距偏移要求的控件，豁免 24×24px 限制。
- 拖拽替代豁免（Dragging Exceptions）：当拖拽属于操作的本质特征（例如自由涂鸦绘画）或由操作系统用户代理控制时，免于提供单指针替代方案。
- 认知函数测试豁免：当存在密码管理器自动填充、第三方 OAuth 认证对象或基于实物/对象的非认知验证方式时，满足可访问认证合规。

## Dependencies
- 规范基准：WCAG 2.2 (W3C Recommendation 2023-10-05)、WAI-ARIA 1.2 (W3C Recommendation 2023-06-06)、HTML Living Standard (WHATWG)、Accessible Name and Description Computation 1.2。
- 参考资产：`assets/` 与 `references/` 下的 11 份规范指引。

## Permissions and Side Effects
- 只读审查与设计制定：分析界面结构、生成验收标准与证据日志，不擅自向外部测试平台提交私有数据。

## Gates
- **验收标准完整性 Gate**：每个受审组件必须具备可观察的角色、名称、状态、键盘导航与错误恢复契约。
- **合规裁决 Gate**：无真实屏幕阅读器和键盘走查证据时，严禁输出“WCAG Conformance Pass”裁决。

## Open Questions
- 如何在现代 SPA 路由切换时，针对不同用户心智模型（保持在主要内容 vs 宣告新页面标题）建立自适应的焦点管理策略。

## Unique Value
跳脱出将可访问性作为机械检查清单的传统偏见，将最新的 WCAG 2.2 核心增量（焦点不被遮挡、拖拽替代、目标尺寸、认证可访问性、重复录入）深度工程化，提供具备法律与工程双重严密性的人机混合证据体系。

## Reading Coverage
全量阅读并吸纳 `skills/web-accessibility/` 目录下全部 12 个可达规范文件：
1. `SKILL.md`（第 1 行至第 62 行）
2. `assets/acceptance-criteria-template.md`（第 1 行至第 23 行）
3. `references/composite-widgets.md`（第 1 行至第 23 行）
4. `references/dialogs-disclosures-navigation.md`（第 1 行至第 15 行）
5. `references/forms-errors-authentication.md`（第 1 行至第 24 行）
6. `references/keyboard-focus-and-routing.md`（第 1 行至第 18 行）
7. `references/outcome-probes.md`（第 1 行至第 23 行）
8. `references/routing.md`（第 1 行至第 15 行）
9. `references/semantics-and-names.md`（第 1 行至第 22 行）
10. `references/source-index.md`（第 1 行至第 32 行）
11. `references/testing-and-evidence.md`（第 1 行至第 35 行）
12. `references/visual-input-and-motion.md`（第 1 行至第 17 行）
涵盖 WCAG 2.2 规范层、WAI-ARIA 1.2、原生 HTML 行为、键盘与焦点模型、表单恢复、复合组件契约、人机混合测试证据标准及 5 类 outcome probes 判定。
