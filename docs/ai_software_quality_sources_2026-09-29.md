# 从零用 AI 做高品质软件：105 条研究资料与阅读地图

**检索日期：2026-09-29**  
**重点：业务与产品判断、领域建模、交互、视觉工艺，以及从 AI 原型走向可靠软件。**

## 怎么使用这份资料库

不要先读完全部资料才开始项目。先从下面的关键阅读路线建立工作方式，随后按当前遇到的问题查阅对应类别。配套执行手册：`ai_software_quality_playbook_2026-09-29.md`。

这里的“高品质”不是生成很多页面，也不是只把首屏做漂亮，而是：解决值得解决的问题；关键业务规则成立；真实用户可以顺畅完成任务；视觉和交互一致；上线后可观察、可维护、可恢复。

### 检索与证据说明

本次围绕商业与用户证据、业务建模、AI 原型、视觉工艺、设计系统、设计转代码、代理工程、测试上线和效果评估进行多轮检索，并对核心页面补读关键正文或相关章节。优先采用方法原作者、产品团队的一手案例、官方文档与标准。

**105 条指去重后的文章、章节、规范条款、官方工具文档和资源库入口，不代表 105 项独立研究，也不代表每个长篇文档都已逐字通读。** 某些主题同时收录长文和速查文档，是为了不同使用目的，已在边界说明中标识。没有把相同文章的中英文版本、镜像站或跟踪参数链接重复计数。

规范按相关章节查阅；商业书籍和资料库只核验公开介绍或目录；论文介绍与未逐页审读的报告单独标明。工具文档持续更新，实施时应重新核对版本。案例和厂商实验可学习方法，但不能被当成普遍的生产率或产品成功保证。

“必读/按需/扩展”是为本任务安排的阅读优先级，不是对所有产品的统一规定。“产品本身包含 AI”一类只对内置 AI 功能或自建代理的项目适用。

## 关键阅读路线

| 顺序 | 资料 | 阅读后应该留下什么 |
|---|---|---|
| 1 | [R001 · The Four Big Risks](https://www.svpg.com/four-big-risks/) | 把四类产品风险与证据分开。 |
| 2 | [R005 · How to talk to users](https://www.ycombinator.com/library/Iq-how-to-talk-to-users) | 得到能追溯到真实行为的研究记录。 |
| 3 | [R008 · Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/) | 为目标机会设计备选方案与验证。 |
| 4 | [R018 · Object-Oriented UX](https://alistapart.com/article/object-oriented-ux/) | 形成业务对象、关系与术语。 |
| 5 | [R021 · Introducing Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/) | 把规则变成可讨论、可测试的例子。 |
| 6 | [R028 · UX-Context Design: Using UX Knowledge to Inform AI-Generated Design](https://www.nngroup.com/articles/ux-context-design/) | 把业务与用户知识组织成AI上下文。 |
| 7 | [R037 · A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh) | 为视觉微调建立真实界面上的比较机制。 |
| 8 | [R039 · Good Visual Design, Explained](https://www.nngroup.com/articles/good-visual-design/) | 把“好看”拆成可描述的设计决策。 |
| 9 | [R066 · Write design system guidelines for Make kits](https://help.figma.com/hc/en-us/articles/43602393097239-Write-design-system-guidelines-for-Make-kits) | 写出组件与Token怎样使用，而不只是有什么。 |
| 10 | [R076 · My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/) | 形成小步实现、验证、提交的工作习惯。 |
| 11 | [R085 · Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 写清完成条件，并校准评审方式。 |
| 12 | [R062 · Web Interface Guidelines](https://vercel.com/design/guidelines) | 建立细节走查清单，再对照正式标准。 |

## 分类概览

| 主题 | 条数 |
|---|---:|
| 商业定位与需求证据 | 12 |
| 业务建模与范围控制 | 11 |
| 用户研究与AI原型 | 13 |
| 视觉审美与界面工艺 | 18 |
| 标准与质量底线 | 8 |
| 设计上下文与设计转代码 | 13 |
| AI开发工作流与代理工程 | 14 |
| 验证上线与运行质量 | 8 |
| 研究证据与效率判断 | 3 |
| 产品本身包含AI时的补充 | 5 |
| **合计** | **105** |


# 商业定位与需求证据


## R001 · The Four Big Risks

**来源与类型**：SVPG · 产品方法　**阅读优先级**：必读　[原文/官方入口](https://www.svpg.com/four-big-risks/)

**重点学习**：分别验证价值、可用性、技术可行性、商业可行性，不把交付功能等同于成功。

**建议转成的项目产物**：四类风险表；每类风险对应证据和下一次验证。

**适用边界**：方法框架，不是产品成功的保证。


## R002 · Assessing Product Opportunities

**来源与类型**：SVPG · 产品方法　**阅读优先级**：必读　[原文/官方入口](https://www.svpg.com/assessing-product-opportunities/)

**重点学习**：把机会说明与解决方案分开，检查用户、替代方案、渠道、差异化和成功指标。

**建议转成的项目产物**：一页机会评估，而不是先写长篇功能清单。

**适用边界**：2006年的经典文章；保留方法，不照搬市场假设。


## R003 · Product Discovery

**来源与类型**：SVPG · 产品方法　**阅读优先级**：扩展　[原文/官方入口](https://www.svpg.com/product-discovery/)

**重点学习**：把需求发现视为持续学习，而不是一次性收集需求后交给开发。

**建议转成的项目产物**：把验证任务和交付任务分开管理。

**适用边界**：经典方法，不是新的AI工具教程。


## R004 · Value and Viability

**来源与类型**：SVPG · 产品方法　**阅读优先级**：扩展　[原文/官方入口](https://www.svpg.com/value-and-viability/)

**重点学习**：区分用户获得的价值与组织能否持续提供这种价值。

**建议转成的项目产物**：说明谁受益、谁付费、谁承担交付成本。

**适用边界**：不提供特定行业的商业预测。


## R005 · How to talk to users

**来源与类型**：Y Combinator · 讲座与文字稿　**阅读优先级**：必读　[原文/官方入口](https://www.ycombinator.com/library/Iq-how-to-talk-to-users)

**重点学习**：围绕真实行为和最近发生的事件访谈，而非诱导用户认可设想。

**建议转成的项目产物**：访谈提纲、原始记录、行为证据表。

**适用边界**：用户口头喜欢不等于采用或付款。


## R006 · How to Start a Startup: Talking to users

**来源与类型**：Y Combinator · 讲座与文字稿　**阅读优先级**：扩展　[原文/官方入口](https://www.ycombinator.com/library/JQ-how-to-start-a-startup-talking-to-users)

**重点学习**：识别不同用户与利益相关者，避免只采访最容易接触的一类人。

**建议转成的项目产物**：区分使用者、购买者、管理者与服务人员。

**适用边界**：结合自己的产品环境，不把讲座案例当普遍定律。


## R007 · Learning about users and their needs

**来源与类型**：GOV.UK · 服务手册　**阅读优先级**：必读　[原文/官方入口](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)

**重点学习**：从真实用户、现有研究、业务记录和观察建立需求，区分证据与意见。

**建议转成的项目产物**：可追溯需求台账，保留反例与未知项。

**适用边界**：政府服务背景，商业项目需要适配。


## R008 · Opportunity Solution Trees

**来源与类型**：Teresa Torres / Product Talk · 方法原作者　**阅读优先级**：必读　[原文/官方入口](https://www.producttalk.org/opportunity-solution-trees/)

**重点学习**：连接业务结果、用户机会、备选方案与假设验证。

**建议转成的项目产物**：为一个机会提出不同解决路径，而不是只优化第一个想法。

**适用边界**：树形图帮助思考，不是需求真实性的证据。


## R009 · Assumption Testing: Everything You Need to Know to Get Started

**来源与类型**：Product Talk · 方法文章　**阅读优先级**：必读　[原文/官方入口](https://www.producttalk.org/assumption-testing/)

**重点学习**：优先检验影响大、证据弱的假设，并预先约定判断方式。

**建议转成的项目产物**：假设清单、最小验证实验、通过与否的判据。

**适用边界**：早期定性探索与正式统计实验不要混为一谈。


## R010 · The Value Proposition Canvas

**来源与类型**：Strategyzer · 原创框架与模板　**阅读优先级**：按需　[原文/官方入口](https://www.strategyzer.com/library/the-value-proposition-canvas)

**重点学习**：用任务、痛点、收益组织价值主张，检查产品承诺是否对应真实需求。

**建议转成的项目产物**：用户侧与价值侧的匹配图。

**适用边界**：画布里写出的内容仍可能只是待验证假设；页面含商业服务。


## R011 · Positioning and Competition

**来源与类型**：April Dunford · 定位方法原作者　**阅读优先级**：必读　[原文/官方入口](https://www.aprildunford.com/post/positioning-and-competition)

**重点学习**：竞争替代品不只有同类软件，还包括表格、人工流程、现状与不采取行动。

**建议转成的项目产物**：真实替代方案对照表及切换理由。

**适用边界**：作者实践观点，不是某行业当前市场份额数据。


## R012 · RICE: Simple prioritization for product managers

**来源与类型**：Intercom · 团队实践　**阅读优先级**：按需　[原文/官方入口](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)

**重点学习**：在覆盖范围、影响、信心与成本之间做透明取舍。

**建议转成的项目产物**：带证据来源和不确定性的优先级表。

**适用边界**：没有数据时不应让AI虚构精确分数。


# 业务建模与范围控制


## R013 · Set Boundaries — Shape Up

**来源与类型**：Basecamp · 公开在线书章节　**阅读优先级**：必读　[原文/官方入口](https://basecamp.com/shapeup/1.2-chapter-03)

**重点学习**：先明确问题、投入上限与范围，避免把模糊大愿望直接变成承诺。

**建议转成的项目产物**：项目边界、明确不做的事、可缩减的范围。

**适用边界**：具体团队周期是Basecamp实践，不是所有项目的硬标准。


## R014 · Risks and Rabbit Holes — Shape Up

**来源与类型**：Basecamp · 公开在线书章节　**阅读优先级**：必读　[原文/官方入口](https://basecamp.com/shapeup/1.4-chapter-05)

**重点学习**：在投入实现前识别会让项目失控的设计与技术难点。

**建议转成的项目产物**：风险清单、技术探针、复杂需求的裁剪方案。

**适用边界**：不能用控制范围作为省略安全和必要正确性的理由。


## R015 · EventStorming

**来源与类型**：Alberto Brandolini / 官方方法入口　**阅读优先级**：按需　[原文/官方入口](https://www.eventstorming.com/)

**重点学习**：让业务、设计与工程围绕真实业务变化建立共同理解。

**建议转成的项目产物**：业务事件时间线、角色、争议点与流程边界。

**适用边界**：多种工作坊风格；不意味着必须采用微服务或事件溯源。


## R016 · Service Blueprints: Definition

**来源与类型**：Nielsen Norman Group · 服务设计方法　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/service-blueprints-definition/)

**重点学习**：把用户接触点与后台人员、流程和系统依赖放在一起检查。

**建议转成的项目产物**：前台体验—后台履约—支持系统的服务蓝图。

**适用边界**：界面顺畅不能替代后台真正完成服务。


## R017 · Service Blueprinting in Practice: Who, When, What

**来源与类型**：Nielsen Norman Group · 实践研究　**阅读优先级**：扩展　[原文/官方入口](https://www.nngroup.com/articles/service-blueprinting-practice/)

**重点学习**：理解何时做蓝图、哪些角色需要参与，以及如何用于团队协作。

**建议转成的项目产物**：跨职能评审安排与具体场景蓝图。

**适用边界**：应围绕一个场景工作，不追求一张包罗万象的大图。


## R018 · Object-Oriented UX

**来源与类型**：Sophia V. Prater · 原创方法文章　**阅读优先级**：必读　[原文/官方入口](https://alistapart.com/article/object-oriented-ux/)

**重点学习**：先定义用户理解的对象、内容、关系和重要性，再安排页面与操作。

**建议转成的项目产物**：领域术语表、对象关系表、对象内容优先级。

**适用边界**：这是UX建模方法，不要求使用面向对象编程。


## R019 · OOUX: A Foundation for Interaction Design

**来源与类型**：Sophia V. Prater · 原创方法文章　**阅读优先级**：必读　[原文/官方入口](https://alistapart.com/article/ooux-a-foundation-for-interaction-design/)

**重点学习**：把对象模型进一步连接到动作与交互，补齐对象可执行的操作。

**建议转成的项目产物**：对象—操作清单及上下文导航。

**适用边界**：对象模型只是基础，交互仍需用户验证。


## R020 · User Story Mapping

**来源与类型**：Jeff Patton · 方法原作者资源页　**阅读优先级**：必读　[原文/官方入口](https://jpattonassociates.com/story-mapping/)

**重点学习**：用完整用户活动组织需求和发布范围，而不是一张扁平任务清单。

**建议转成的项目产物**：一条从触发到结果的最小完整用户旅程。

**适用边界**：公开资源入口；没有声称通读付费书籍。


## R021 · Introducing Example Mapping

**来源与类型**：Cucumber / Matt Wynne · 方法原文　**阅读优先级**：必读　[原文/官方入口](https://cucumber.io/blog/bdd/example-mapping-introduction/)

**重点学习**：把用户故事拆成规则、实例与未决问题，消除编码前的业务歧义。

**建议转成的项目产物**：规则—正反例—问题清单，再转验收用例。

**适用边界**：先达成共同理解，不必一开始就写正式Gherkin。


## R022 · Example Mapping documentation

**来源与类型**：Cucumber · 官方文档　**阅读优先级**：按需　[原文/官方入口](https://cucumber.io/docs/bdd/example-mapping/)

**重点学习**：用简洁的操作说明复现示例映射讨论。

**建议转成的项目产物**：需求评审时可直接使用的检查步骤。

**适用边界**：与原文相关，但用途是简版操作参考；不是新的独立研究。


## R023 · Complete multiple tasks

**来源与类型**：GOV.UK Design System · 交互模式　**阅读优先级**：按需　[原文/官方入口](https://design-system.service.gov.uk/patterns/complete-multiple-tasks/)

**重点学习**：检查跨会话、多步骤任务是否真的需要任务清单，以及状态如何保持一致。

**建议转成的项目产物**：复杂表单或办理流程的任务状态设计。

**适用边界**：先简化流程，再考虑增加任务清单。


# 用户研究与AI原型


## R024 · Usability (User) Testing 101

**来源与类型**：Nielsen Norman Group · 方法指南　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/usability-testing-101/)

**重点学习**：通过任务和观察发现问题，不把问用户喜不喜欢当可用性测试。

**建议转成的项目产物**：测试计划、观察记录、问题严重度与复测结果。

**适用边界**：少量定性测试不能直接推导总体转化率。


## R025 · Turn User Goals into Task Scenarios for Usability Testing

**来源与类型**：Nielsen Norman Group · 实操文章　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/task-scenarios-usability-testing/)

**重点学习**：写真实目标场景，避免在题目里泄露按钮名称和操作路径。

**建议转成的项目产物**：不带提示的任务脚本及完成判据。

**适用边界**：任务需要对应目标人群的真实工作。


## R026 · User research — Service Manual

**来源与类型**：GOV.UK · 研究方法资料库　**阅读优先级**：按需　[原文/官方入口](https://www.gov.uk/service-manual/user-research)

**重点学习**：查阅研究计划、招募、隐私、访谈、观察和分析的方法。

**建议转成的项目产物**：研究操作清单及数据处理约束。

**适用边界**：资料库入口，不按其中每篇文章额外计数。


## R027 · Onboarding Tutorials vs. Contextual Help

**来源与类型**：Nielsen Norman Group · 用户研究与建议　**阅读优先级**：按需　[原文/官方入口](https://www.nngroup.com/articles/onboarding-tutorials/)

**重点学习**：把帮助放在用户需要的场景中，而不是靠启动时的大段教程弥补复杂设计。

**建议转成的项目产物**：首次使用流程、就地帮助和可重访的指导。

**适用边界**：不是禁止所有教程；复杂任务需要适当指导。


## R028 · UX-Context Design: Using UX Knowledge to Inform AI-Generated Design

**来源与类型**：Nielsen Norman Group · 2026方法文章　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/ux-context-design/)

**重点学习**：把研究结论、术语、使用环境和交互规则整理为AI能够使用的上下文。

**建议转成的项目产物**：研究结论与设计约束的可读取索引。

**适用边界**：文中的UX.md是设想，不是正式行业标准。


## R029 · Synthetic Users: If, When, and How to Use AI-Generated “Research”

**来源与类型**：Nielsen Norman Group · 研究与方法讨论　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/synthetic-users/)

**重点学习**：识别AI模拟用户反馈的边界，避免把生成结果伪装为真实用户证据。

**建议转成的项目产物**：在研究记录中明确标注真实证据、假设与模拟材料。

**适用边界**：可辅助探索假设，但不能直接证明需求成立。


## R030 · AI Can’t Replace Real Research in Empathy Mapping

**来源与类型**：Nielsen Norman Group · 2026方法文章　**阅读优先级**：按需　[原文/官方入口](https://www.nngroup.com/articles/ai-empathy-mapping/)

**重点学习**：用AI整理已有研究，而不是生成貌似具体、实际无来源的用户想法。

**建议转成的项目产物**：带原始证据引用的共情图。

**适用边界**：生成的用户引语不能当成访谈记录。


## R031 · Good from Afar, But Far from Good: AI Prototyping in Real Design Contexts

**来源与类型**：Nielsen Norman Group · 真实项目评估　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/ai-prototyping/)

**重点学习**：观察不同上下文输入对AI设计的影响，以及分组、层级和语义细节仍会怎样出错。

**建议转成的项目产物**：针对具体设计任务的输入清单与人工检查表。

**适用边界**：项目评估，不是所有工具和版本的永久排名。


## R032 · Test Complex Interactions Earlier with AI Prototyping

**来源与类型**：Nielsen Norman Group · 2026案例文章　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/test-earlier-with-ai/)

**重点学习**：用可运行原型提前测试筛选、编辑器、动态状态等难以静态模拟的交互。

**建议转成的项目产物**：带脱敏或合成数据的可测试原型及用户问题记录。

**适用边界**：原型保真度应由研究问题决定；案例不是普遍因果证明。


## R033 · User-Centered Design with AI in the Loop: A Case Study of Rapid User Interface Prototyping with “Vibe Coding”

**来源与类型**：Li / Maheshwari / Voelker · 研究论文HTML　**阅读优先级**：按需　[原文/官方入口](https://arxiv.org/html/2507.21012v1)

**重点学习**：研究交通工程领域中，AI交互原型怎样与领域专家反馈形成迭代。

**建议转成的项目产物**：把专业数据和真实任务放进原型验证。

**适用边界**：单项目、顺序式案例研究；不是随机对照实验。


## R034 · The Custodial Era of UX: Cleaning Up After AI

**来源与类型**：Nielsen Norman Group · 2026分析文章　**阅读优先级**：按需　[原文/官方入口](https://www.nngroup.com/articles/ai-ux-debt/)

**重点学习**：识别生成速度超过评估能力时积累的体验问题。

**建议转成的项目产物**：为每次生成安排检查与整改，而不是只统计页面产量。

**适用边界**：观点与方法讨论，不是量化生产率实验。


## R035 · Evaluating AI-Simulated Behavior: Insights from Three Studies on Digital Twins and Synthetic Users

**来源与类型**：Nielsen Norman Group · 研究综述　**阅读优先级**：扩展　[原文/官方入口](https://www.nngroup.com/articles/ai-simulations-studies/)

**重点学习**：理解模拟效果为何受任务、数据来源和评估方式影响。

**建议转成的项目产物**：对模拟研究设置适用条件与验证方法。

**适用边界**：不要把能预测某类问卷等同于能替代可用性研究。


## R036 · Digital Twins: Simulating Humans with Generative AI

**来源与类型**：Nielsen Norman Group · 概念与方法　**阅读优先级**：扩展　[原文/官方入口](https://www.nngroup.com/articles/digital-twins/)

**重点学习**：区分泛化的合成人物和基于特定个体资料的模拟。

**建议转成的项目产物**：记录模拟数据来源、授权及适用范围。

**适用边界**：涉及隐私与代表性限制；不能冒充真实个体反馈。


# 视觉审美与界面工艺


## R037 · A calmer interface for a product in motion

**来源与类型**：Linear · 一手产品设计案例　**阅读优先级**：必读　[原文/官方入口](https://linear.app/now/behind-the-latest-design-refresh)

**重点学习**：观察如何在高信息密度中重排注意力，并用AI开发内部工具支持真实界面迭代。

**建议转成的项目产物**：关键页前后对照、语义颜色调整、设计与代码同步。

**适用边界**：2026-03-12；案例中的配色与密度不是所有产品的答案。


## R038 · Why is quality so rare?

**来源与类型**：Linear · 团队产品理念　**阅读优先级**：按需　[原文/官方入口](https://linear.app/now/why-is-quality-so-rare)

**重点学习**：把质量看成贯穿完整体验的责任，而不是最后一次视觉润色。

**建议转成的项目产物**：团队质量原则和需要持续修复的体验细节。

**适用边界**：公司实践与价值判断，不是通用实验结论。


## R039 · Good Visual Design, Explained

**来源与类型**：Nielsen Norman Group · 设计实例讲解　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/good-visual-design/)

**重点学习**：通过实际页面理解网格、排版、用色与图像如何共同建立秩序。

**建议转成的项目产物**：参考页面拆解表：原则、证据、应用位置。

**适用边界**：审美建议应结合产品语境，不照搬具体视觉样式。


## R040 · 5 Principles of Visual Design in UX

**来源与类型**：Nielsen Norman Group · 设计原则　**阅读优先级**：按需　[原文/官方入口](https://www.nngroup.com/articles/principles-visual-design/)

**重点学习**：用尺度、层级、平衡、对比与格式塔解释设计决策。

**建议转成的项目产物**：视觉评审维度与问题描述语言。

**适用边界**：文章中的数量建议是启发式，不是合规标准。


## R041 · Visual Hierarchy in UX: Definition

**来源与类型**：Nielsen Norman Group · 方法文章　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)

**重点学习**：通过颜色、尺度、分组引导注意力，而不是让所有元素同时突出。

**建议转成的项目产物**：页面关注顺序与主次操作层级。

**适用边界**：不能只靠颜色表达业务状态。


## R042 · Refactoring UI

**来源与类型**：Adam Wathan / Steve Schoger · 书籍与公开介绍　**阅读优先级**：按需　[原文/官方入口](https://www.refactoringui.com/)

**重点学习**：系统学习层级、留白、文字、颜色、深度和收尾细节。

**建议转成的项目产物**：视觉修改清单；优先从层级与内容结构修改。

**适用边界**：付费书；本次只核验官网公开目录与介绍，未声称阅读全书。


## R043 · Typography in ten minutes

**来源与类型**：Matthew Butterick · 原作者排版指南　**阅读优先级**：按需　[原文/官方入口](https://practicaltypography.com/typography-in-ten-minutes.html)

**重点学习**：学习字体、字号、行距和行长的基本控制。

**建议转成的项目产物**：排版样式及阅读测试样张。

**适用边界**：主要面向西文排版，不能把字数和尺度直接套到中文。


## R044 · 16 little UI design tips that make a big impact

**来源与类型**：Adham Dannaway · 设计师一手教程　**阅读优先级**：按需　[原文/官方入口](https://www.adhamdannaway.com/blog/ui-design/ui-design-tips)

**重点学习**：学习通过具体对比发现界面细节问题。

**建议转成的项目产物**：给自己的关键页做逐项视觉审查。

**适用边界**：个人设计建议，不是统一行业验收规范。


## R045 · Foundations — Atlassian Design System

**来源与类型**：Atlassian · 官方设计系统　**阅读优先级**：按需　[原文/官方入口](https://atlassian.design/foundations)

**重点学习**：理解基础样式如何组织成统一语言。

**建议转成的项目产物**：字体、颜色、间距、图标、层次等基础约束。

**适用边界**：资料库入口；借鉴组织方式，不直接套用品牌。


## R046 · Spacing — Atlassian Design System

**来源与类型**：Atlassian · 官方设计系统章节　**阅读优先级**：按需　[原文/官方入口](https://atlassian.design/foundations/spacing)

**重点学习**：让间距遵循系统而非每次临时猜测。

**建议转成的项目产物**：间距Token与组件间距规则。

**适用边界**：特定系统的取值并非所有项目的最优值。


## R047 · Motion: How it works — Material Design 3

**来源与类型**：Google Material Design · 官方指南　**阅读优先级**：按需　[原文/官方入口](https://m3.material.io/styles/motion/overview/how-it-works)

**重点学习**：把运动用于表达变化与关系，理解标准和更具表现力的运动选择。

**建议转成的项目产物**：动作目的、进入退出行为和动效参数。

**适用边界**：平台设计建议；避免给所有交互强加同一种弹性或时长。


## R048 · 字体 — Ant Design

**来源与类型**：Ant Design · 官方中文设计规范　**阅读优先级**：必读　[原文/官方入口](https://ant.design/docs/spec/font-cn.md)

**重点学习**：综合处理字体家族、字阶、行高、字重、颜色与数字对齐。

**建议转成的项目产物**：中文界面字体方案及跨平台测试页面。

**适用边界**：14px等数值属于该设计系统方案，不是WCAG要求。


## R049 · Design Values — Ant Design

**来源与类型**：Ant Design · 官方设计原则　**阅读优先级**：按需　[原文/官方入口](https://ant.design/docs/spec/values.md)

**重点学习**：将自然、确定性、意义与成长转化为业务界面决策。

**建议转成的项目产物**：一致的术语、反馈和跨界面操作规则。

**适用边界**：框架性设计理念，不引用其中未经单独核实的通用统计说法。


## R050 · Data table — Carbon Design System

**来源与类型**：IBM Carbon · 官方组件规范　**阅读优先级**：必读　[原文/官方入口](https://preview.carbondesignsystem.com/building-blocks/core/components/data-table)

**重点学习**：系统处理排序、筛选、选择、批量操作与行内操作。

**建议转成的项目产物**：复杂表格交互与状态矩阵。

**适用边界**：按自己的组件版本核对API；不能只复制外观。


## R051 · Empty states — Carbon Design System

**来源与类型**：IBM Carbon · 官方交互模式　**阅读优先级**：必读　[原文/官方入口](https://carbondesignsystem.com/patterns/empty-states-pattern/)

**重点学习**：把空状态作为具有原因和下一步的体验，而不是统一放一张插画。

**建议转成的项目产物**：首次使用、筛选为空、无权限、失败等不同状态。

**适用边界**：状态需要按产品真实语义设计。


## R052 · GOV.UK Design System

**来源与类型**：GOV.UK · 官方设计系统　**阅读优先级**：按需　[原文/官方入口](https://design-system.service.gov.uk/)

**重点学习**：学习面向真实办理任务的组件、表单与内容模式。

**建议转成的项目产物**：可访问且一致的表单和任务流程。

**适用边界**：公共服务风格不等于商业品牌风格。


## R053 · Mobbin — Web Flows

**来源与类型**：真实产品界面参考库　**阅读优先级**：按需　[原文/官方入口](https://mobbin.com/explore/web/flows)

**重点学习**：按完整流程查参考，而不是只收集漂亮首屏。

**建议转成的项目产物**：竞品步骤与状态的对照记录。

**适用边界**：部分内容需账户或付费；公开入口核验，不宣称已浏览付费全库。


## R054 · Page Flows — User flow library

**来源与类型**：真实产品交互录像资料库　**阅读优先级**：按需　[原文/官方入口](https://pageflows.com/all-userflows/)

**重点学习**：观察进入、操作、反馈、退出的动态过程。

**建议转成的项目产物**：借鉴适合自己任务的交互模式。

**适用边界**：商业资料库；出现于成熟产品不等于已适配你的用户。


# 标准与质量底线


## R055 · Web Content Accessibility Guidelines (WCAG) 2.2

**来源与类型**：W3C · 推荐标准　**阅读优先级**：必读　[原文/官方入口](https://www.w3.org/TR/WCAG22/)

**重点学习**：把可访问性转成分级且可检查的要求。

**建议转成的项目产物**：与目标等级对应的完整检查清单。

**适用边界**：通过某一个条款，不等于整体符合AA或AAA。


## R056 · Understanding SC 1.4.3: Contrast (Minimum)

**来源与类型**：W3C WAI · AA条款解释　**阅读优先级**：必读　[原文/官方入口](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

**重点学习**：普通文本4.5:1、大文本3:1，并注意适用范围和例外。

**建议转成的项目产物**：文本与背景组合的对比度核查。

**适用边界**：“大文本”有正式定义；理解文档是解释材料。


## R057 · Understanding SC 1.4.6: Contrast (Enhanced)

**来源与类型**：W3C WAI · AAA条款解释　**阅读优先级**：按需　[原文/官方入口](https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html)

**重点学习**：区分增强对比度与最低对比度要求。

**建议转成的项目产物**：需要更高可读性时的对比度目标。

**适用边界**：普通文本7:1、大文本4.5:1；不能误标为AA最低要求。


## R058 · Understanding SC 2.5.8: Target Size (Minimum)

**来源与类型**：W3C WAI · AA条款解释　**阅读优先级**：必读　[原文/官方入口](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

**重点学习**：准确理解24×24 CSS像素及间距等例外。

**建议转成的项目产物**：紧凑工具栏、图标按钮和密集表格的可点选审查。

**适用边界**：不是所有目标都机械套用24×24；必须检查条款例外。


## R059 · Understanding SC 2.5.5: Target Size (Enhanced)

**来源与类型**：W3C WAI · AAA条款解释　**阅读优先级**：按需　[原文/官方入口](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)

**重点学习**：理解44×44 CSS像素增强目标及其例外。

**建议转成的项目产物**：移动端和更高可操作性目标的检查。

**适用边界**：44×44不应被写成WCAG 2.2 AA统一最低要求。


## R060 · Requirements for Chinese Text Layout / 中文排版需求

**来源与类型**：W3C · 中文排版文档　**阅读优先级**：必读　[原文/官方入口](https://www.w3.org/TR/clreq/)

**重点学习**：核对中文标点、换行、混排与地域排版习惯。

**建议转成的项目产物**：真实中文、英文、数字、标点混排测试样本。

**适用边界**：检索时版本为2026-09-01 Group Note Draft，不是已通过的推荐标准。


## R061 · Design Tokens Technical Reports 2025.10

**来源与类型**：Design Tokens Community Group · 技术报告　**阅读优先级**：按需　[原文/官方入口](https://www.designtokens.org/tr/2025.10/)

**重点学习**：了解跨工具Token格式、颜色及解析规范的组织方式。

**建议转成的项目产物**：可版本管理、可交换的Token数据。

**适用边界**：Final Community Group Report，不是W3C推荐标准。


## R062 · Web Interface Guidelines

**来源与类型**：Vercel · 工程化界面检查表　**阅读优先级**：必读　[原文/官方入口](https://vercel.com/design/guidelines)

**重点学习**：集中检查键盘、焦点、表单、状态、布局、动效和性能细节。

**建议转成的项目产物**：界面走查和自动化检查的基础清单。

**适用边界**：包含团队偏好；APCA等建议不能替代WCAG 2.2合规计算。


# 设计上下文与设计转代码


## R063 · Improving frontend design through Skills

**来源与类型**：Anthropic · 一手设计工程文章　**阅读优先级**：必读　[原文/官方入口](https://claude.com/blog/improving-frontend-design-through-skills)

**重点学习**：给生成过程明确的视觉方向与可复用设计指导。

**建议转成的项目产物**：项目设计简报、风格约束与上下文模块。

**适用边界**：反对特定模板风格是审美策略，不是所有产品的禁用清单。


## R064 · frontend-design / SKILL.md

**来源与类型**：Anthropic · 官方开源提示与工作流　**阅读优先级**：按需　[原文/官方入口](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

**重点学习**：研究如何把设计判断表达成给编码代理使用的可执行指导。

**建议转成的项目产物**：结合项目改写的视觉工作流，不是照抄整套偏好。

**适用边界**：活跃仓库；需要自行验证输出，不能把其文本当质量证明。


## R065 · Figma MCP Server

**来源与类型**：Figma · 官方开发文档　**阅读优先级**：按需　[原文/官方入口](https://developers.figma.com/docs/figma-mcp-server/)

**重点学习**：把设计结构、变量和组件上下文提供给开发代理。

**建议转成的项目产物**：设计稿到既有代码组件的映射。

**适用边界**：连接成功不代表像素、交互与业务已经正确。


## R066 · Write design system guidelines for Make kits

**来源与类型**：Figma · 官方指南与示例　**阅读优先级**：必读　[原文/官方入口](https://help.figma.com/hc/en-us/articles/43602393097239-Write-design-system-guidelines-for-Make-kits)

**重点学习**：说明Token的语义、组件的用途、正确错误示例和API，而不只列数值。

**建议转成的项目产物**：模块化设计系统使用说明。

**适用边界**：示例中的具体组件与颜色只适用于相应示例系统。


## R067 · Add guidelines to Figma Make

**来源与类型**：Figma · 官方操作文档　**阅读优先级**：按需　[原文/官方入口](https://help.figma.com/hc/en-us/articles/33665861260823-Add-guidelines-to-Figma-Make)

**重点学习**：用项目指导文件持续影响生成结果。

**建议转成的项目产物**：精简入口文件与按需引用的设计规则。

**适用边界**：工具功能与入口以实际版本为准。


## R068 · How to prompt v0

**来源与类型**：Vercel · 官方使用方法　**阅读优先级**：按需　[原文/官方入口](https://vercel.com/blog/how-to-prompt-v0)

**重点学习**：同时提供产品功能面、使用语境和约束，而不是只给模糊风格词。

**建议转成的项目产物**：可复用的页面或组件任务说明。

**适用边界**：教程和厂商实践，不引用其效果宣传为普遍定量结论。


## R069 · Design Systems 2.0 — v0

**来源与类型**：v0 · 官方设计系统文档　**阅读优先级**：按需　[原文/官方入口](https://v0.app/docs/design-systems-2)

**重点学习**：让生成结果利用组件包、参考应用、Token与设计文档。

**建议转成的项目产物**：现有设计系统的生成工具适配。

**适用边界**：按产品版本核对可用功能。


## R070 · v0 Vibecoding Guide

**来源与类型**：Vercel · 官方教程　**阅读优先级**：按需　[原文/官方入口](https://vercel.com/academy/v0-foundations/vibecoding-guide)

**重点学习**：使用参考材料、增量修改和版本控制推进生成。

**建议转成的项目产物**：局部修改任务及迭代记录。

**适用边界**：基础工具教程，不能单独覆盖业务与生产安全。


## R071 · Prompting best practices — Lovable

**来源与类型**：Lovable · 官方文档　**阅读优先级**：按需　[原文/官方入口](https://docs.lovable.dev/prompting/prompting-one)

**重点学习**：提供真实内容、视觉方向和明确组件行为，分块生成。

**建议转成的项目产物**：输入上下文模板和逐块验收清单。

**适用边界**：工具教程中的审美示例不是统一最佳风格。


## R072 · Introducing “vibe design” with Stitch

**来源与类型**：Google Labs · 官方产品文章　**阅读优先级**：扩展　[原文/官方入口](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)

**重点学习**：了解多方案探索与设计上下文工作的工具形态。

**建议转成的项目产物**：选型时核对自己的设计探索需求。

**适用边界**：功能介绍，不是设计质量的独立评测。


## R073 · Stitch’s DESIGN.md format is now open-source

**来源与类型**：Google Labs · 官方格式介绍　**阅读优先级**：按需　[原文/官方入口](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/)

**重点学习**：理解为什么要同时保存视觉数值与使用意图。

**建议转成的项目产物**：项目视觉身份的可读取描述。

**适用边界**：草案格式，不是全行业强制标准。


## R074 · google-labs-code/design.md

**来源与类型**：Google Labs · 格式规范源码　**阅读优先级**：按需　[原文/官方入口](https://github.com/google-labs-code/design.md)

**重点学习**：直接查阅结构化视觉身份格式及示例。

**建议转成的项目产物**：版本化设计描述与Token之间的对应。

**适用边界**：活跃草案；按实际工具支持情况采用。


## R075 · Design-to-Code with Antigravity and Stitch MCP

**来源与类型**：Google Codelabs · 实操教程　**阅读优先级**：按需　[原文/官方入口](https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch)

**重点学习**：练习设计元数据到代码，再到浏览器检查的连接。

**建议转成的项目产物**：小型设计转代码练习。

**适用边界**：示例以落地页为主；跑通教程不等于业务系统已生产就绪。


# AI开发工作流与代理工程


## R076 · My LLM coding workflow going into 2026

**来源与类型**：Addy Osmani · 一手工程实践　**阅读优先级**：必读　[原文/官方入口](https://addyosmani.com/blog/ai-coding-workflow/)

**重点学习**：先澄清规格，再小步实现、验证、提交，并保持对代码的理解。

**建议转成的项目产物**：规格、分步计划、测试和小提交记录。

**适用边界**：2026-01-04；作者经验不是所有团队的效率定律。


## R077 · My LLM codegen workflow atm

**来源与类型**：Harper Reed · 一手工作流　**阅读优先级**：按需　[原文/官方入口](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)

**重点学习**：研究从问答澄清到计划、实现提示的连贯过程。

**建议转成的项目产物**：自己的规格到任务生成模板。

**适用边界**：2025工具细节可能变化，重点学流程。


## R078 · Agentic Engineering Patterns

**来源与类型**：Simon Willison · 持续更新工程指南　**阅读优先级**：必读　[原文/官方入口](https://simonwillison.net/guides/agentic-engineering-patterns/)

**重点学习**：把编码代理纳入工程纪律，覆盖版本控制、测试、理解代码和反模式。

**建议转成的项目产物**：一套实际使用代理的操作习惯。

**适用边界**：指南入口，下面两章单列供针对性阅读。


## R079 · Red/green TDD

**来源与类型**：Simon Willison · 实操章节　**阅读优先级**：必读　[原文/官方入口](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)

**重点学习**：先确认测试能失败，再实现到通过，防止测试没有真正约束功能。

**建议转成的项目产物**：带失败证据与通过证据的回归用例。

**适用边界**：测试本身也需检查，不能为了通过而削弱断言。


## R080 · Agentic manual testing

**来源与类型**：Simon Willison · 实操章节　**阅读优先级**：必读　[原文/官方入口](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/)

**重点学习**：让代理实际启动应用、执行操作并留下检查记录。

**建议转成的项目产物**：浏览器或命令行运行证据。

**适用边界**：自动化探索不能保证发现所有业务或审美问题。


## R081 · Best practices for Claude Code

**来源与类型**：Anthropic · 官方开发文档　**阅读优先级**：必读　[原文/官方入口](https://code.claude.com/docs/en/best-practices)

**重点学习**：优先提供可运行的验证方式，再管理计划、上下文、权限与评审。

**建议转成的项目产物**：项目入口规则、验证命令和可回退的小任务。

**适用边界**：不同工具入口文件不同；不要机械增加大量上下文。


## R082 · Building verification loops in Claude Code with skills

**来源与类型**：Anthropic · 2026工程文章　**阅读优先级**：按需　[原文/官方入口](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)

**重点学习**：把反复执行的人工检查逐步变成可复用验证流程。

**建议转成的项目产物**：稳定、能重复执行的验证脚本和反馈记录。

**适用边界**：先验证检查本身有效，再自动化放大。


## R083 · Effective context engineering for AI agents

**来源与类型**：Anthropic · 工程方法　**阅读优先级**：必读　[原文/官方入口](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**重点学习**：管理与当前任务最相关的高信号上下文，而非无限堆积聊天历史。

**建议转成的项目产物**：模块化资料索引、按需读取和状态交接。

**适用边界**：上下文更长不等于质量更高。


## R084 · Effective harnesses for long-running agents

**来源与类型**：Anthropic · 一手工程实验　**阅读优先级**：按需　[原文/官方入口](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**重点学习**：为长期任务提供进展记录、增量开发与端到端验证机制。

**建议转成的项目产物**：功能清单、进度文件、提交和运行检查。

**适用边界**：具体编排依赖模型能力，不能照搬为永远最优架构。


## R085 · Harness design for long-running application development

**来源与类型**：Anthropic · 2026工程实验　**阅读优先级**：必读　[原文/官方入口](https://www.anthropic.com/engineering/harness-design-long-running-apps)

**重点学习**：研究生成与评审分离、可测试完成条件、浏览器验证及人工校准。

**建议转成的项目产物**：单任务验收契约、分项质量门槛和缺陷反馈。

**适用边界**：2026-03-24；仍有残留缺陷，更多代理也不是无条件更好。


## R086 · Harness engineering: leveraging Codex in an agent-first world

**来源与类型**：OpenAI · 一手工程案例　**阅读优先级**：必读　[原文/官方入口](https://openai.com/index/harness-engineering/)

**重点学习**：把项目知识、架构约束、浏览器与运行信息整理成代理可访问的环境。

**建议转成的项目产物**：短入口索引、仓库内知识、自动化约束与可观察运行环境。

**适用边界**：2026-02-11；特定内部项目经验，不直接泛化效率或放宽安全审查。


## R087 · Spec Kit

**来源与类型**：GitHub · 官方规格驱动开发工具文档　**阅读优先级**：按需　[原文/官方入口](https://github.github.com/spec-kit/)

**重点学习**：检查如何将规格、计划与可执行任务连接。

**建议转成的项目产物**：一套轻量规格到实施的任务结构。

**适用边界**：工具不是需求发现的替代品，简单项目不必全套采用。


## R088 · Documenting Architecture Decisions

**来源与类型**：Michael Nygard · ADR原始文章　**阅读优先级**：按需　[原文/官方入口](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

**重点学习**：用小型记录保留架构决策的背景与取舍，而不是只留结论。

**建议转成的项目产物**：关键架构决策记录。

**适用边界**：记录真正重要的决定，不给每行代码写文档。


## R089 · Monolith First

**来源与类型**：Martin Fowler · 架构观点　**阅读优先级**：按需　[原文/官方入口](https://martinfowler.com/bliki/MonolithFirst.html)

**重点学习**：在领域边界尚未清晰时重视简单架构与后续可拆分性。

**建议转成的项目产物**：适合项目规模和团队能力的架构选择。

**适用边界**：作者也说明经验基础的限制；不是禁止微服务。


# 验证上线与运行质量


## R090 · Visual comparisons — Playwright

**来源与类型**：Playwright · 官方测试文档　**阅读优先级**：必读　[原文/官方入口](https://playwright.dev/docs/test-snapshots)

**重点学习**：使用截图比较发现回归，并控制测试环境和基准更新。

**建议转成的项目产物**：关键页面与状态的视觉回归用例。

**适用边界**：截图差异不是审美评分，基准需要人工批准。


## R091 · Visual tests — Storybook

**来源与类型**：Storybook · 官方测试文档　**阅读优先级**：按需　[原文/官方入口](https://storybook.js.org/docs/writing-tests/visual-testing)

**重点学习**：针对组件状态保存和审查视觉变更。

**建议转成的项目产物**：组件状态样例与经审核的基准。

**适用边界**：云服务是实现选项，不是唯一选择。


## R092 · ARIA snapshot testing — Playwright

**来源与类型**：Playwright · 官方测试文档　**阅读优先级**：按需　[原文/官方入口](https://playwright.dev/docs/aria-snapshots)

**重点学习**：对可访问性树做语义层面的回归检查。

**建议转成的项目产物**：重要界面结构和名称的语义检查。

**适用边界**：不能替代完整无障碍审查，也不能检查所有视觉细节。


## R093 · Snapshots — Playwright MCP

**来源与类型**：Playwright · 官方代理浏览器文档　**阅读优先级**：按需　[原文/官方入口](https://playwright.dev/mcp/snapshots)

**重点学习**：区分语义快照与截图对代理提供的信息。

**建议转成的项目产物**：既有操作结构又有视觉上下文的验证输入。

**适用边界**：代理只读取DOM或语义树，不代表看过实际视觉效果。


## R094 · Web Vitals

**来源与类型**：Google web.dev · 官方性能指南　**阅读优先级**：必读　[原文/官方入口](https://web.dev/articles/vitals)

**重点学习**：把加载、交互响应与稳定性落实到实际用户指标。

**建议转成的项目产物**：LCP、INP、CLS的真实用户监测。

**适用边界**：“良好”阈值按第75百分位评估；实验室分数不等于真实用户体验。


## R095 · OWASP Application Security Verification Standard

**来源与类型**：OWASP · 应用安全验证标准　**阅读优先级**：必读　[原文/官方入口](https://owasp.org/projects/asvs)

**重点学习**：按风险组织可核查的应用安全要求，而不是只让AI说代码安全。

**建议转成的项目产物**：权限、认证、数据处理等安全验收清单。

**适用边界**：检索时稳定版5.0.0；清单与扫描通过不等于自动获得安全保证。


## R096 · Canarying Releases — SRE Workbook

**来源与类型**：Google SRE · 公开在线书章节　**阅读优先级**：按需　[原文/官方入口](https://sre.google/workbook/canarying-releases/)

**重点学习**：用有限范围发布、观测和回退降低变更风险。

**建议转成的项目产物**：分阶段发布、监测指标与回滚条件。

**适用边界**：实现复杂度应匹配项目风险；不是每个小产品都要大型平台。


## R097 · Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications

**来源与类型**：Google Research · CHI 2010论文介绍　**阅读优先级**：按需　[原文/官方入口](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/)

**重点学习**：从用户目标选择体验指标，而不是只统计页面浏览量。

**建议转成的项目产物**：目标—信号—指标的映射。

**适用边界**：本次核阅论文介绍；不要机械收集框架里的全部指标。


# 研究证据与效率判断


## R098 · Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity

**来源与类型**：METR · 随机对照实验说明　**阅读优先级**：按需　[原文/官方入口](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)

**重点学习**：看到任务情境和实际测量可能与主观提效感不同。

**建议转成的项目产物**：把端到端耗时、返工和质量纳入AI效果评估。

**适用边界**：2025早期工具、熟悉仓库的资深开发者；不能泛化为2026所有AI必然变慢。


## R099 · We are Changing our Developer Productivity Experiment Design

**来源与类型**：METR · 后续实验与方法更新　**阅读优先级**：必读　[原文/官方入口](https://metr.org/blog/2026-02-24-uplift-update/)

**重点学习**：了解新工具下选择偏差和并行工作如何改变生产率测量。

**建议转成的项目产物**：记录任务选择、并行处理与测量局限。

**适用边界**：作者明确表示新实验的选择效应使速度提升幅度难以可靠估计。


## R100 · DORA AI Capabilities Model report

**来源与类型**：DORA · 研究报告官方入口　**阅读优先级**：按需　[原文/官方入口](https://dora.dev/research/2025/ai-capabilities-model/)

**重点学习**：进一步研究怎样建设支持AI开发的团队能力与改进路径。

**建议转成的项目产物**：团队能力盘点和改善行动。

**适用边界**：本次核验官方介绍，未逐页审读PDF；观察性研究不应简单表述为因果证明。


# 产品本身包含AI时的补充


## R101 · Building Effective AI Agents

**来源与类型**：Anthropic · 工程方法　**阅读优先级**：按需　[原文/官方入口](https://www.anthropic.com/engineering/building-effective-agents)

**重点学习**：从足够简单的方案开始，根据评估增加代理工作流复杂度。

**建议转成的项目产物**：按任务风险选择确定性流程或代理。

**适用边界**：用于内置AI功能或自建代理，不是普通软件必须具备的架构。


## R102 · The HAX Toolkit Project

**来源与类型**：Microsoft Research · 人机交互工具包　**阅读优先级**：按需　[原文/官方入口](https://www.microsoft.com/en-us/research/project/hax-toolkit/)

**重点学习**：规划AI如何向用户表达能力、接受纠正并处理失败。

**建议转成的项目产物**：人机协作场景与失败交互检查。

**适用边界**：只在产品本身含AI时扩展使用。


## R103 · Guidelines for Human-AI Interaction

**来源与类型**：Microsoft Research · CHI 2019研究介绍　**阅读优先级**：扩展　[原文/官方入口](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/?lang=zh-cn)

**重点学习**：研究经过评估的人机交互原则及其适用场景。

**建议转成的项目产物**：与HAX工具包结合的人机交互规则。

**适用边界**：本次核阅公开研究介绍，不声称审读整篇PDF。


## R104 · Evaluation best practices

**来源与类型**：OpenAI · 官方评估指南　**阅读优先级**：必读　[原文/官方入口](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

**重点学习**：用代表性任务、明确判据和持续评估衡量AI输出。

**建议转成的项目产物**：基准任务集、人工标签、失败类别和发布评估。

**适用边界**：示例阈值不是你项目的验收标准；模型评委需用人工标签校准。


## R105 · One AI Output Is an Example, Not an Evaluation

**来源与类型**：Nielsen Norman Group · 2026评估方法　**阅读优先级**：必读　[原文/官方入口](https://www.nngroup.com/articles/eval-ai-output/)

**重点学习**：通过多种输入和重复运行，区分任务差异与随机输出差异。

**建议转成的项目产物**：可重复评估计划及不确定性报告。

**适用边界**：一次成功演示不能证明可靠性。


# 不建议从这些材料直接推出的结论

“某团队使用 AI 很成功”不等于任何人使用相同工具都能成功；“原型可运行”不等于业务、安全与运维已准备好；“模型评分提高”不等于真实用户体验同步提高。

资料中有些建议会互相冲突，例如高密度与大留白、标准组件与视觉独特性、多代理编排与简单单代理。应先看产品目标、用户熟练度、使用频率、任务风险及维护能力，再决定采用哪一种。不要把特定设计语言、具体字号、某种渐变或某个框架包装成普遍的“顶级标准”。

特别区分：WCAG 的规范等级；CLREQ 的草案文档状态；DTCG 社区技术报告；DESIGN.md 的草案格式；UX.md 作为上下文组织设想。它们具有不同的约束性质。
