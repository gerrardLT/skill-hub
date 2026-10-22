# 从零用 AI 做高品质软件：执行手册

**版本日期：2026-09-29**  
**适用范围：** 以 Web 软件、SaaS、业务后台和工具型产品为主要例子。移动端、桌面软件可迁移产品与工程方法，但应另补相应平台规范。

配套资料库：`ai_software_quality_sources_2026-09-29.md`，包含 105 条去重文章、章节、标准条款、官方文档和资料入口。文中的 R 编号对应资料库条目，并在文末提供直接链接。

本手册是根据多源资料整理的执行方案，不是任何一家公司的原文流程。示例中的业务规则、文件名、分工和检查表是建议，应按项目风险与规模调整。它也不是“先做完所有文档，再开始开发”的瀑布式要求：需求验证、技术试验和设计探索可以并行，学习结果应及时改变方案。

## 一、先明确：高品质不是完成更多功能

把质量分成四个不可互相抵消的问题：

| 维度 | 要证明什么 | 不能拿什么冒充 |
|---|---|---|
| 值得做 | 目标用户确有重要问题，新方案有采用理由 | AI生成的用户画像、口头夸奖、功能数量 |
| 业务正确 | 角色、对象、流程、规则、状态和异常能组成完整结果 | 页面能打开、按钮能点击 |
| 体验优秀 | 用户理解任务与反馈；视觉服务于内容；交互一致 | 只有一张漂亮截图、只测正常状态 |
| 可可靠交付 | 关键行为可验证，权限与数据可控，失败可发现和恢复 | 构建成功、模型自评“全部完成” |

产品发现应同时考虑价值、可用性、可行性和商业可行性。[R001] 本手册据此建议：缩小功能范围，但不要把范围缩减变成已知业务错误、不可恢复操作或越权漏洞的借口。

## 二、全流程：每一步留下证据，而不只是留下文档

| 阶段 | 怎样做得好 | AI适合承担什么 | 下一步之前应具备什么 |
|---|---|---|---|
| 机会与定位 | 明确特定人群、真实问题、现有替代方案和采用理由 | 检索公开材料、整理访谈、反驳过早结论 | 有来源的机会说明；最大未知项被标出 |
| 需求验证 | 比较不同方案，先测高风险假设 | 帮助设计验证与分析资料 | 有判断依据，而不是只有团队意见 |
| 业务建模 | 定义对象、关系、角色、状态、规则和例外 | 补问题、生成正反例、检查模型矛盾 | 关键规则能解释给业务人员并转为测试 |
| 体验设计 | 先做完整任务，再设计页面；用真实内容测试 | 生成交互原型和测试数据 | 目标用户可以完成关键任务，阻断问题已处理 |
| 视觉探索 | 同一真实任务比较不同方向，再选择和精修 | 扩展方案、实现试验、生成局部对比 | 方向有理由，关键页与基础状态经过审查 |
| 设计系统 | 固化语义Token、组件行为与使用约束 | 编写规则、对齐样式与组件代码 | 后续页面可复用，不需要每次重新设计 |
| 实现 | 小批次、完整业务切片、真实持久化和权限 | 编码、执行检查、修复具体失败 | 有实际运行与测试证据，可审查和回退 |
| 验收 | 分开检查业务、体验、视觉、性能和安全 | 自动测试、截图、日志分析、辅助评审 | 必要底线全部通过，剩余风险透明 |
| 上线与学习 | 渐进发布、观察真实用户结果 | 分类反馈、定位问题、维护回归集 | 有监测、回滚与后续改进依据 |

这个表是工作地图，不是要求每个项目都做一整套大型组织流程。简单工具可以合并步骤，但不应跳过关键判断。

## 三、业务：从“听上去有用”做到“值得做且做得对”

### 3.1 先写机会说明，不要先写功能大全

建议用一页回答：具体服务谁；在什么场景触发问题；当前怎样完成；哪一步成本最高；现有替代方案是什么；为什么用户愿意改变；谁决定购买或部署；怎样判断成功。[R002][R011]

业务设计同时包括两层：

**商业层：** 使用者、付费者、采购或部署决策者、触达路径、切换成本、服务成本与收益来源。内部工具可以把重点放在任务结果、维护成本和组织采用，不必硬套订阅商业模式。

**领域层：** 软件处理什么对象，谁可以做什么，何时可以做，失败后怎样继续，最终结果如何成立。

对收入、使用频率、获客成本等未知数，保留区间或“未知”，说明需要哪类数据。不要让AI用貌似精确的数字填平空白。

### 3.2 建立证据台账：区分事实、解释和猜测

访谈应围绕最近一次真实经历、具体操作、已有替代办法和已付出的成本，而非“假如做出这个产品，你会不会用”。把研究记录和现有业务资料作为证据，AI可帮助整理，但不能生成“用户原话”充当研究。[R005][R007][R029]

建议的台账结构：

| 字段 | 内容 |
|---|---|
| 证据编号 | 可回到访谈记录、观察记录、支持工单或业务数据的编号 |
| 观察到的事实 | 对方实际做了什么，不加解释 |
| 对问题的解释 | 团队或AI的推断，单独标注 |
| 反例与边界 | 哪些人没有这个问题；哪些场景不适用 |
| 决策影响 | 它会改变产品方向、任务流程，还是局部设计 |
| 下一次验证 | 用什么信息降低不确定性 |

一条证据可以支持多个需求，一个需求也应能追溯到依据。没有真实用户可接触时，可以制作假设原型，但应明确其需求尚未验证。

### 3.3 对最重要的机会比较方案，而不是自动选择“做更多功能”

机会解决方案树把目标结果、用户机会、候选方案和验证连接起来。[R008] 一个可操作的做法是：先比较明显不同的路径，例如简化现有流程、自动化其中一步、重做整个操作方式，而不是三个配色不同的同一方案。

把假设写成会影响决策的句子，例如“用户愿意把已有数据导入新工具”“审批者能理解系统解释的规则冲突”。优先验证后果严重、证据薄弱的假设，并在看结果之前约定如何判断。[R009]

AI的价值是帮助找反例、扩展方案、整理测试结果，而不是替团队宣布“市场已验证”。

### 3.4 建模对象和规则，再确定导航与页面

对象模型让团队先谈用户世界里的“东西”和关系；服务蓝图则补上界面背后的人员、系统与履约过程。[R018][R016]

建议至少检查：

| 模型 | 需要回答的具体问题 |
|---|---|
| 对象与关系 | 什么有独立身份和生命周期？哪些只是它的列表或视图？ |
| 角色与数据范围 | 谁能看、创建、修改、批准、导出？只限本人、团队还是组织？ |
| 状态与动作 | 什么状态允许什么操作？动作完成后转到哪里？ |
| 业务规则 | 哪些条件永远必须成立？规则冲突由谁决定？ |
| 异常与恢复 | 重复提交、超时、撤销、并发修改、外部失败怎样处理？ |
| 记录与解释 | 用户怎么知道发生了什么？支持人员如何追查？ |

不必为了完成这张表引入复杂建模工具，Markdown表格就能起步。复杂领域才考虑更深入的工作坊。[R015]

**假设示例：采购申请审批。** 这不是通用采购规则，而是演示需求如何变得可实现。

模糊需求：“支持申请审批。”

可实施的规格应进一步明确：申请单与审批记录如何关联；草稿何时允许提交；审批人依据什么被选中；申请人能否撤回；拒绝后是修改原单还是创建新版本；同一申请被同时处理时如何裁决。

若项目确认“申请人不得批准自己的申请”是一项规则，就至少生成两个验收例子：本人尝试批准会被服务端拒绝；符合资格的其他审批人可以批准。再检查记录、界面反馈和后续状态。

使用示例映射时，把“规则”“具体正反例”“仍待确认的问题”分开。结果尚不清楚的场景是问题，不是让AI自行编造答案的空格。[R021]

### 3.5 第一版交付一个完整结果，而不是一排半成品菜单

用用户故事地图确定最小完整任务。[R020] 对上面的假设产品，第一条切片可能是“创建申请—提交—由另一角色处理—申请人看到结果”，而不是分别生成仪表盘、通知中心、设置页和报表。

在扩大范围前检查：真实数据已保存；刷新后仍然成立；另一个角色看到正确内容；失败后有下一步；权限在服务端约束；操作有必要的记录。

范围可以减，完成定义不能模糊。投入边界和明确不做的内容有助于控制项目。[R013][R014]

## 四、交互：让AI帮助你更早测试，而不是更早自信

### 4.1 为研究问题选择原型保真度

需要检查内容顺序时，低保真草图可能已经足够；需要检查复杂筛选、动态编辑、分支状态或开放输入时，可运行原型更有价值。AI降低了这些复杂交互的原型制作门槛，但是否有用仍取决于它能回答什么研究问题。[R032]

不要为了“完整演示”把原型做成生产系统，也不要把只覆盖正常路径的演示当作完整产品。

### 4.2 用真实任务和真实感内容检查

测试任务描述用户的目的，不提示按钮或菜单路径。[R025] 观察用户在哪里停顿、误解、回退或需要求助，记录问题及触发条件，而不只记录“满意”。

原型数据可以是经过允许并脱敏的真实数据，也可以是按业务约束生成的合成数据。**合成数据用于测试界面承载能力，不是合成用户证据。**[R032][R029]

### 4.3 优先修复结构问题

如果用户不知道下一步是什么、分不清对象、找不到关键操作，先改信息架构、任务步骤和文案，不要先改阴影。

可用性测试提供行为证据，设计评审提供专业判断，内部试用发现日常摩擦；三者有不同作用，不能只靠一个环节替代全部验证。[R024][R031]

## 五、视觉：把“高级感”转成明确的设计决策

### 5.1 从使用语境选方向，不从流行风格选方向

先明确使用频率、用户熟练度、决策压力、信息量和品牌性格。高频专业工具可能需要更高信息密度；低频办理场景可能更需要解释、引导和渐进展示。[R028]

建议选取少量参考并逐项拆解，而不是把不同产品的好看部件拼起来：

| 参考维度 | 拆解问题 | 应转成的项目规则 |
|---|---|---|
| 信息层级 | 哪些内容先被看到？哪些内容后退？ | 页面关注顺序与操作主次 |
| 布局与密度 | 内容怎样分组？哪些留白承担结构？ | 区域、列宽、间距与响应策略 |
| 排版 | 字体、行距与字重怎样支持阅读？ | 文本角色与样式 |
| 颜色 | 哪些颜色表达品牌、状态或交互？ | 语义颜色，而不是任意色值集合 |
| 交互 | 焦点、选择、等待和失败怎样反馈？ | 状态、行为和恢复方式 |

层级可通过尺度、对比和分组形成；优秀视觉通常来自这些决定协同工作，而不是增加装饰。[R039][R041]

### 5.2 用同一真实内容比较几个方向

建议在同一个关键业务页面上比较两到三个有明显差异的方向，控制任务、文案和数据一致。这个数量是执行建议，不是行业标准。

评审时问：哪一种让当前任务更清楚？内容是否可扫读？业务重要性是否与视觉重要性一致？适合长时间使用吗？更复杂状态下是否仍成立？维护成本是多少？

在专业工具中，熟悉的操作模式往往比新奇布局更重要。差异化可以体现在排版、节奏、内容组织和品牌表达，而不是让用户重新学习基础操作。

### 5.3 精修一张能够检验系统的样板页

优先选择覆盖列表、筛选、状态、详情或表单的关键页面，而不是只精修宣传首屏。然后至少用正常内容、无内容和错误场景检查它。

建议将视觉修改分成三轮，避免不断随机“美化”：

| 轮次 | 关注点 |
|---|---|
| 结构轮 | 内容优先级、布局、分组、主次操作、信息密度 |
| 系统轮 | 字体、间距、语义颜色、组件一致性、内容规则 |
| 工艺轮 | 对齐、图标、截断、焦点、动效、边界状态与响应式 |

Linear的2026设计案例很适合学习“在真实产品中反复比较”的方法：团队调整注意力层级，并用内部工具降低颜色试验的成本。[R037] 借鉴它的比较机制，不等于照搬它的配色。

### 5.4 设计系统要规定“怎么用”，而不只是“有哪些值”

Token应表达语义，例如 `text-primary`、`surface-raised`、`border-subtle`、`status-danger`。组件说明应解释：什么情况下使用、什么时候不用、属性是什么、正确与错误示例是什么。[R066]

建议按四层组织：

**基础值 → 语义Token → 组件规则 → 页面/任务模式。**

AI新增页面应优先使用已有组件与规则。发现规则不足时，先说明缺口和影响范围，再扩展设计系统，避免每个页面各自发明新尺寸、新颜色和新按钮。

DESIGN.md可以作为视觉身份描述的一种格式；但它处于草案生态。文件名不是重点，关键是准确数值、使用理由和实际组件能否一致。[R073][R074]

### 5.5 把状态和内容当成设计的一部分

建议建立状态矩阵，按业务选择适用项，而不是机械全部实现：

| 场景 | 需要设计的内容 |
|---|---|
| 首次使用 | 为什么没有数据，第一步是什么 |
| 筛选无结果 | 当前条件是什么，如何恢复 |
| 加载与后台更新 | 用户知道系统在做什么，能否继续其他操作 |
| 无权限 | 为什么看不到或不能做；可提供何种下一步 |
| 输入错误 | 具体错在哪里，如何修正，已填内容是否保留 |
| 网络失败或超时 | 操作是否已发生，能否安全重试 |
| 成功、撤销与恢复 | 结果是否持久成立，哪些操作可撤回 |
| 内容极端值 | 很长名称、多语言、零值、大数值、很多行、缺少图片 |
| 协作变化 | 内容被他人修改、删除或状态已经变化 |

成熟组件规范会分别处理表格行为和空状态，而不是用一个通用界面覆盖所有情况。[R050][R051]

### 5.6 中文排版要单独检查

准备中文、英文、数字、日期、长组织名和标点混排样本，检查字体回退、字重差异、行高、断行、截断和数字对齐。西文排版建议不能直接按字符数搬到中文。[R043][R048][R060]

Ant Design中的14px等方案是特定设计系统的选择，不是所有中文软件必须遵守的最佳字号。最终取值应由实际使用环境和阅读测试支持。

### 5.7 动效首先帮助理解状态变化

每一类动效先写目的：提示发生了变化、保留空间关系、说明操作结果，还是提供必要的等待反馈。没有清楚目的的重复动效应重新审视。

检查进入、退出、中断、连续触发与减少动态效果偏好。标准型和更具表现力的运动可以服务不同语境，不需要全产品统一使用夸张弹性。[R047][R062]

## 六、区分硬性要求、测量目标和审美偏好

| 类别 | 示例 | 怎样使用 |
|---|---|---|
| 可判定的规范要求 | WCAG条款、明确的安全要求、业务不变量 | 按适用范围逐项验证 |
| 项目质量目标 | 任务成功、响应时间、阅读清晰度、可恢复性 | 结合基线和风险设置目标 |
| 设计系统约定 | 字阶、间距、组件变体、语义颜色 | 项目内保持一致，允许有理由地演进 |
| 审美选择 | 暖灰或冷灰、衬线或无衬线、克制或活泼 | 用目标用户、品牌和任务语境判断 |

### 容易被误写的可访问性数值

| 项目 | WCAG 2.2 AA相关条款 | AAA增强条款 |
|---|---|---|
| 文本对比度 | SC 1.4.3：普通文本至少4.5:1，大文本至少3:1 | SC 1.4.6：普通文本至少7:1，大文本至少4.5:1 |
| 指针目标大小 | SC 2.5.8：24×24 CSS像素，或满足条款规定的例外 | SC 2.5.5：44×44 CSS像素，亦有规定例外 |

“大文本”的定义和目标间距等例外应直接核对原文。表中只列两个方面，不能据此宣称整个产品达到AA或AAA。[R055][R056][R057][R058][R059]

Vercel等团队的界面检查表很有用，但其中也有设计偏好和补充方法；不能把APCA建议代替WCAG 2.2的合规检查。[R062]

中文排版CLREQ在本次检索时为Group Note Draft；DTCG 2025.10是社区组技术报告。二者都有参考价值，但其文档状态与WCAG推荐标准不同。[R060][R061]

## 七、给AI一个可理解、可验证的项目环境

### 7.1 文档最小化，但不要让关键知识只留在聊天里

下面是一种建议的组织方式，不是固定标准；小项目可合并为更少文件。

```text
project/
  AGENTS.md                  # 工作入口；也可按工具使用其对应入口文件
  docs/
    product.md               # 用户、问题、目标、边界、证据索引
    domain.md                # 对象、角色、状态、规则、未决问题
    ux.md                    # 核心任务、术语、交互与内容规则
    design.md                # 视觉方向、Token、参考页、组件使用原则
    plan.md                  # 当前可独立验收的小批次任务
    decisions/               # 少量重要决策及理由
    acceptance.md            # 验收场景和真实检查证据的索引
  tests/
  src/
```

入口文件应像地图，把代理引向当前任务有关的信息，而不是每次都加载全项目长篇资料。上下文管理与仓库知识维护本身就是工程工作。[R083][R086]

UX.md在相关文章中是上下文组织设想；使用同名文件并不会自动带来研究质量或工具兼容性。[R028]

### 7.2 每个任务先约定完成条件

建议的单任务结构：

```text
目标：用户完成什么结果。
依据：相关证据、规则、设计与现有代码位置。
范围：这次做什么、明确不做什么。
行为：输入、权限、状态变化、输出、失败与恢复。
实现约束：必须复用的组件、不能破坏的接口与数据规则。
验收：测试场景、截图状态、运行检查命令、需要人工判断的部分。
交付：变更说明、实际运行结果、未验证项与剩余风险。
```

具体检查比“认真写代码”更有约束力。编码代理需要能运行的测试、构建或界面对照检查，才能根据反馈修正，而不是只根据“看起来做完了”停止。[R081]

### 7.3 分离实现与评审，但不要把多代理当魔法

另一个会话或代理可以提供审查视角，但它依然可能漏错。要求评审给出可复现问题、运行证据和对应规则，而不是笼统打分。

Anthropic的应用开发实验中，评审者使用运行中的应用检查功能，并通过人工校准改善判断；文章也报告了仍未解决的问题。[R085] 因此建议用人工认可的样例和明确门槛校准评审，并保留需要真实用户和专业人员判断的部分。

## 八、编码：一条完整业务切片、一组验证、一份可回退变更

开发循环建议如下：

**读相关规格和代码 → 确认已有测试基线 → 写或补能约束行为的测试 → 实现小批次变化 → 启动应用检查 → 审阅差异 → 提交。**

先确认失败再实现到通过，有助于发现“测试根本没有测试到问题”的情况；浏览器实际操作则补充只看代码或测试输出的盲区。[R079][R080]

审查时尤其注意：是否换成了假数据；是否删掉或削弱断言；是否把服务端权限检查改成隐藏按钮；是否只做成功路径；是否新增了不必要的依赖；是否重复实现已有组件。

架构应首先匹配领域边界、风险和维护能力。早期项目通常值得认真考虑较简单的结构，但“单体优先”是有适用条件的架构观点，不是禁止服务拆分。[R089] 对真正重要的选择，保留背景、决定和代价。[R088]

## 九、上线：运行证据要覆盖页面之外

| 验收方面 | 建议检查 |
|---|---|
| 业务 | 核心结果真正保存；跨角色行为正确；非法状态被拒绝；重复与并发处理符合约定 |
| 权限和数据 | 服务端访问控制、数据隔离、敏感信息处理与必要审计 |
| 视觉 | 关键页面与组件状态有经审核的基准，变化能被发现 |
| 可访问性 | 键盘、焦点、名称、对比度和适用的其他条款 |
| 性能 | 真实用户加载、响应与布局稳定性，而不只看一次实验室得分 |
| 运行维护 | 可发现失败，支持追踪问题；发布范围可控制；回滚或恢复方法经过验证 |

应用安全可以借助OWASP ASVS按风险组织要求，但不应把一次AI代码审查或扫描通过当成安全保证。[R095]

Playwright截图比较和Storybook组件视觉测试适合发现回归；它们并不会自动判断一个设计是否具有好的审美或业务含义。[R090][R091]

Core Web Vitals的“良好”阈值为LCP不超过2.5秒、INP不超过200毫秒、CLS不超过0.1，应按实际用户第75百分位评估，并关注移动端与桌面端差异。它们是性能基线，不是“顶级软件”的完整定义。[R094]

高风险变更应有合适的分阶段发布与回退方式。[R096] 对数据迁移，还应单独设计备份、恢复、兼容与验证步骤；不是“把前端版本退回去”就一定恢复所有状态。

## 十、上线后的指标与学习

优先从用户目标推导信号和指标，而不是因为工具容易统计就收集全部数据。[R097]

例如，任务工具可以关注用户是否完成第一次有效操作、完成关键任务所需的时间、失败与求助发生在哪里、是否在下一次需要时回来。具体指标必须与产品使用频率和业务结果相匹配。

评估AI工作流，也应记录端到端耗时、检查和返工成本、实际交付缺陷，而非只看生成速度。METR的早期实验和后续更新说明：工具版本、任务选择、熟悉程度及并行工作都会影响结果，不能用单个百分比代表所有场景。[R098][R099]

若产品本身含有AI，则另建代表性输入集、重复运行、失败分类及人工校准的评估。一次成功只说明它能成功一次，并不说明稳定程度。[R104][R105]

## 十一、四份可直接改写的工作提示

以下提示需要配合真实材料、实际工具权限和人工判断使用。它们不是保证输出质量的“神奇提示词”。

### 提示一：业务证据与机会审查

```text
你要帮助我判断这个项目值不值得做，而不是替它写宣传文案。

输入：
- 项目设想
- 目标用户与使用场景
- 已有访谈、观察或业务数据
- 现有替代办法
- 技术、预算、隐私和部署约束

先输出：
1. 已有事实、合理推断、尚未验证假设，严格分列。
2. 使用者、付费者、管理者及各自的目标。
3. 最重要的用户任务与当前替代办法。
4. 会改变是否投入的关键风险，以及支持或反对的证据。
5. 明显不同的候选解决路径和各自代价。
6. 下一轮最低成本的验证，以及预先约定的判断方式。

每个证据结论注明来源；没有来源的不要编造。
不要虚构访谈引语、市场数字、付费意愿或验证结果。
先判断问题，不要直接生成一份庞大的功能清单。
```

### 提示二：业务规则与验收例子

```text
根据已确认的业务材料，为当前核心任务建立可实施规格。

依次整理：
- 领域术语、对象、属性、关系
- 角色与数据范围
- 状态、允许动作和状态变化
- 需要始终成立的业务规则
- 每条规则的正常例子、反例与边界例子
- 失败、重试、撤销、并发和记录要求

把不能确定的结果标为“待业务确认”，不要擅自定规则。
检查对象、界面、接口和验收用例之间的名称是否一致。
最后指出最有可能导致返工的歧义，以及最小完整业务切片。
```

### 提示三：视觉方向与样板页

```text
先阅读用户场景、核心任务、已有组件和内容样本，再开始设计。

先用同一关键页面、同一文案、同一数据比较2—3个不同方向。
每个方向说明：
- 服务哪类使用情境
- 主要信息和操作的关注顺序
- 排版、密度、颜色、布局和动效的具体选择
- 参考材料中借鉴了什么原则、没有照搬什么
- 对可用性、可访问性和维护成本的取舍

选定方向后，精修能覆盖主要组件的样板页。
同时展示正常、空、错误、加载及适用的交互状态。
使用真实中文和长内容检查，不用占位词掩盖布局问题。
先修结构和层级，再修装饰；不得擅自扩大功能范围。
```

### 提示四：实现与独立验收

```text
先读取当前任务的业务、交互、视觉约束和现有测试。
写出本次范围与可验证的完成条件，然后再修改代码。

实现时复用既有组件和Token，遵守已确认的权限与状态规则。
不得以假数据、空回调、弱化断言或隐藏按钮冒充实现。
完成后实际运行适用的检查，并报告：
- 执行过的命令、实际结果
- 测过的用户场景和页面状态
- 发现并修复的问题
- 尚未运行的检查及原因
- 剩余风险和需要人工判断的事项

视觉评审应指出具体位置、问题、影响和修改方向；
不要用“整体9/10”代替证据。
如改变规格或公共组件，说明影响范围并重新验证。
```

## 十二、推荐的实际起步方式

先用一个真实问题做机会说明和证据台账；再建对象、规则和一个完整任务；用一张有代表性的业务页比较视觉方向；固定可复用规则；实现一条可运行、可持久化、可测试的切片；观察用户如何使用，再决定扩大什么。

不需要先学会资料库里的一切。真正要形成的是：**研究结果改变设计，设计约束进入代码，运行结果反过来校正规格和AI工作方式。**

## 引用索引

以下为本手册实际使用的资料链接。完整105条资料及适用边界见配套资料库。


- **R001** — [The Four Big Risks](https://www.svpg.com/four-big-risks/)
- **R002** — [Assessing Product Opportunities](https://www.svpg.com/assessing-product-opportunities/)
- **R005** — [How to talk to users](https://www.ycombinator.com/library/Iq-how-to-talk-to-users)
- **R007** — [Learning about users and their needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
- **R008** — [Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/)
- **R009** — [Assumption Testing: Everything You Need to Know to Get Started](https://www.producttalk.org/assumption-testing/)
- **R011** — [Positioning and Competition](https://www.aprildunford.com/post/positioning-and-competition)
- **R013** — [Set Boundaries — Shape Up](https://basecamp.com/shapeup/1.2-chapter-03)
- **R014** — [Risks and Rabbit Holes — Shape Up](https://basecamp.com/shapeup/1.4-chapter-05)
- **R015** — [EventStorming](https://www.eventstorming.com/)
- **R016** — [Service Blueprints: Definition](https://www.nngroup.com/articles/service-blueprints-definition/)
- **R018** — [Object-Oriented UX](https://alistapart.com/article/object-oriented-ux/)
- **R020** — [User Story Mapping](https://jpattonassociates.com/story-mapping/)
- **R021** — [Introducing Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/)
- **R024** — [Usability (User) Testing 101](https://www.nngroup.com/articles/usability-testing-101/)
- **R025** — [Turn User Goals into Task Scenarios for Usability Testing](https://www.nngroup.com/articles/task-scenarios-usability-testing/)
- **R028** — [UX-Context Design: Using UX Knowledge to Inform AI-Generated Design](https://www.nngroup.com/articles/ux-context-design/)
- **R029** — [Synthetic Users: If, When, and How to Use AI-Generated “Research”](https://www.nngroup.com/articles/synthetic-users/)
- **R031** — [Good from Afar, But Far from Good: AI Prototyping in Real Design Contexts](https://www.nngroup.com/articles/ai-prototyping/)
- **R032** — [Test Complex Interactions Earlier with AI Prototyping](https://www.nngroup.com/articles/test-earlier-with-ai/)
- **R037** — [A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh)
- **R039** — [Good Visual Design, Explained](https://www.nngroup.com/articles/good-visual-design/)
- **R041** — [Visual Hierarchy in UX: Definition](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
- **R043** — [Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html)
- **R047** — [Motion: How it works — Material Design 3](https://m3.material.io/styles/motion/overview/how-it-works)
- **R048** — [字体 — Ant Design](https://ant.design/docs/spec/font-cn.md)
- **R050** — [Data table — Carbon Design System](https://preview.carbondesignsystem.com/building-blocks/core/components/data-table)
- **R051** — [Empty states — Carbon Design System](https://carbondesignsystem.com/patterns/empty-states-pattern/)
- **R055** — [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)
- **R056** — [Understanding SC 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- **R057** — [Understanding SC 1.4.6: Contrast (Enhanced)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html)
- **R058** — [Understanding SC 2.5.8: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- **R059** — [Understanding SC 2.5.5: Target Size (Enhanced)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)
- **R060** — [Requirements for Chinese Text Layout / 中文排版需求](https://www.w3.org/TR/clreq/)
- **R061** — [Design Tokens Technical Reports 2025.10](https://www.designtokens.org/tr/2025.10/)
- **R062** — [Web Interface Guidelines](https://vercel.com/design/guidelines)
- **R066** — [Write design system guidelines for Make kits](https://help.figma.com/hc/en-us/articles/43602393097239-Write-design-system-guidelines-for-Make-kits)
- **R073** — [Stitch’s DESIGN.md format is now open-source](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/)
- **R074** — [google-labs-code/design.md](https://github.com/google-labs-code/design.md)
- **R079** — [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)
- **R080** — [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/)
- **R081** — [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- **R083** — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **R085** — [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- **R086** — [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- **R088** — [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- **R089** — [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)
- **R090** — [Visual comparisons — Playwright](https://playwright.dev/docs/test-snapshots)
- **R091** — [Visual tests — Storybook](https://storybook.js.org/docs/writing-tests/visual-testing)
- **R094** — [Web Vitals](https://web.dev/articles/vitals)
- **R095** — [OWASP Application Security Verification Standard](https://owasp.org/projects/asvs)
- **R096** — [Canarying Releases — SRE Workbook](https://sre.google/workbook/canarying-releases/)
- **R097** — [Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/)
- **R098** — [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- **R099** — [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/)
- **R104** — [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- **R105** — [One AI Output Is an Example, Not an Evaluation](https://www.nngroup.com/articles/eval-ai-output/)

[R001]: https://www.svpg.com/four-big-risks/
[R002]: https://www.svpg.com/assessing-product-opportunities/
[R005]: https://www.ycombinator.com/library/Iq-how-to-talk-to-users
[R007]: https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs
[R008]: https://www.producttalk.org/opportunity-solution-trees/
[R009]: https://www.producttalk.org/assumption-testing/
[R011]: https://www.aprildunford.com/post/positioning-and-competition
[R013]: https://basecamp.com/shapeup/1.2-chapter-03
[R014]: https://basecamp.com/shapeup/1.4-chapter-05
[R015]: https://www.eventstorming.com/
[R016]: https://www.nngroup.com/articles/service-blueprints-definition/
[R018]: https://alistapart.com/article/object-oriented-ux/
[R020]: https://jpattonassociates.com/story-mapping/
[R021]: https://cucumber.io/blog/bdd/example-mapping-introduction/
[R024]: https://www.nngroup.com/articles/usability-testing-101/
[R025]: https://www.nngroup.com/articles/task-scenarios-usability-testing/
[R028]: https://www.nngroup.com/articles/ux-context-design/
[R029]: https://www.nngroup.com/articles/synthetic-users/
[R031]: https://www.nngroup.com/articles/ai-prototyping/
[R032]: https://www.nngroup.com/articles/test-earlier-with-ai/
[R037]: https://linear.app/now/behind-the-latest-design-refresh
[R039]: https://www.nngroup.com/articles/good-visual-design/
[R041]: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
[R043]: https://practicaltypography.com/typography-in-ten-minutes.html
[R047]: https://m3.material.io/styles/motion/overview/how-it-works
[R048]: https://ant.design/docs/spec/font-cn.md
[R050]: https://preview.carbondesignsystem.com/building-blocks/core/components/data-table
[R051]: https://carbondesignsystem.com/patterns/empty-states-pattern/
[R055]: https://www.w3.org/TR/WCAG22/
[R056]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
[R057]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
[R058]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
[R059]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
[R060]: https://www.w3.org/TR/clreq/
[R061]: https://www.designtokens.org/tr/2025.10/
[R062]: https://vercel.com/design/guidelines
[R066]: https://help.figma.com/hc/en-us/articles/43602393097239-Write-design-system-guidelines-for-Make-kits
[R073]: https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/
[R074]: https://github.com/google-labs-code/design.md
[R079]: https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
[R080]: https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/
[R081]: https://code.claude.com/docs/en/best-practices
[R083]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[R085]: https://www.anthropic.com/engineering/harness-design-long-running-apps
[R086]: https://openai.com/index/harness-engineering/
[R088]: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
[R089]: https://martinfowler.com/bliki/MonolithFirst.html
[R090]: https://playwright.dev/docs/test-snapshots
[R091]: https://storybook.js.org/docs/writing-tests/visual-testing
[R094]: https://web.dev/articles/vitals
[R095]: https://owasp.org/projects/asvs
[R096]: https://sre.google/workbook/canarying-releases/
[R097]: https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/
[R098]: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
[R099]: https://metr.org/blog/2026-02-24-uplift-update/
[R104]: https://developers.openai.com/api/docs/guides/evaluation-best-practices
[R105]: https://www.nngroup.com/articles/eval-ai-output/
