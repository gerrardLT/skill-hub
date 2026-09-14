# analyzing-user-feedback 来源能力档案

## Problem

在产品日常迭代和规模化运营中，团队常面临海量、多渠道、高噪音的用户反馈（支持工单、社交媒体发难、社群争鸣、销售前线转述等）。面对这些反馈，团队极易陷入多重陷阱：
1. **被“嗓门最大的少数派”（Vocal Minority）绑架**：团队将社交媒体或社区论坛上最激烈刺耳的声音误判为大盘主流诉求，投入宝贵工程资源开发后却发现绝大多数普通用户并无使用意愿；
2. **“脱离一线体验”的数字盲审**：产研团队完全依赖二手聚合报表和脱水指标做决策，自身从未像真实用户那样完整走完端到端复杂旅程，无法体感摩擦痛点；
3. **“过早进入解决方案”模式**：在审视体验走查或客诉时，团队急于争论技术实现方案，打断了对真实痛点严重性与交互摩擦的充分感知；
4. **单点反馈无法形成闭环**：收到反馈改完上线后从不主动回访用户，白白错失沉淀忠实拥趸与修复信任资产（Trust Vault）的契机。

## When to Use

- **海量多源定性/定量反馈综合聚类与提炼**：将分散在客服工单、NPS问卷、应用商店评价、访谈纪要及社区论坛的数据转化为高置信度决策输入。
- **代表性与影响力评估（Representation vs Influence）**：核验某项强烈抗议或呼声究竟属于“广泛真实需求”还是“少数意见领袖的特定诉求”，决定行动优先级。
- **全员沉浸式体验设计与“吃狗粮”制度落地**：搭建全员客服轮岗（如 WeDash）、跨职能关键旅程巡店走查（Walk the Store）、体验吐槽会（Complaint-Storms）及非核心产研人员强制深度使用产品机制。
- **大模型驱动的自动化语义聚类与智能体透镜**：利用 LLM 对海量非结构化文本进行语义聚类、情绪波动追踪，或构建代表真实客群画像的 AI Persona 用于需求草案即时初审。

## When Not to Use

- **确定性工程故障排查**：线上服务 500 报错、数据库死锁或网络异常阻断（应直接触发 incident-response 止血排查）。
- **纯静态代码与页面性能度量**：页面加载时间、打包体积优化等客观性能指标（应由 web-perf 或 APM 工具负责）。

## Role

用户反馈全景洞察与体验共情架构师（User Feedback Synthesizer & Empathy Architect）。擅长穿透表层噪音，运用代表性与影响力二维矩阵客观甄别信号价值，主导跨职能团队“不带解法”地沉浸体感交互摩擦，并借助大语言模型与知识图谱将散乱客诉转化为具有业务杠杆的长期价值决策。

## Inputs

- **原始客诉与反馈集**：客服 Support Tickets、应用商店评论、社群/Discord 讨论串、推特/社交媒体提及、销售会议纪要。
- **用户画像与分群元数据**：反馈者账户类型（免费/付费/KA）、活跃周期、社区影响力权重、历史净推荐值。
- **用户行为与遥测数据**：流失用户行为路径、漏斗中断点埋点日志。
- **内部组织与体验上下文**：团队当前 OKR 目标、现有产品核心工作流清单、组织全员使用制度底账。

## Outputs

- **反馈平衡组合全景图（Balanced Feedback Portfolio）**：标明各反馈渠道（社媒、工单、销售、调研）偏见与置信度的全渠道图谱。
- **代表性与影响力优先级判定矩阵（Representation × Influence Matrix）**：
  - 高代表性 × 高影响力：Top 优先级必须排期；
  - 高代表性 × 低影响力：普遍基础体验缺陷，批量治理；
  - 低代表性 × 高影响力：圈层领袖特异诉求，针对性沟通或赋能；
  - 低代表性 × 低影响力：暂缓投入并向用户解释原因。
- **走查摩擦清单与沉浸体检日志（Friction Log & Walk the Store Report）**：记录无干扰体验下截获的具体交互断点与困惑瞬间。
- **闭环行动计划与信任资产核算（Action Plan & Trust Vault Accounting）**：排期功能清单、回访联系人列表与用户信任度存款收益预估。

## Workflow

1. **采集与平衡组合构建（Assemble Balanced Portfolio）**：
   - 汇集多源输入，显式校正渠道固有偏差（如社媒偏重极客与重度用户，工单偏向受挫不满用户，销售纪要偏重成单阻断项）。
2. **语义聚类与大模型初筛（AI-Powered Semantic Clustering）**：
   - 借助 LLM 对海量工单与非结构化访谈进行语义归纳，提炼高频主题族群与突增趋势；
   - 提取用户描述痛点时使用的鲜活比喻（Metaphors）。
3. **二维矩阵过滤与代表性审查（Representation & Depth Filtering）**：
   - 应用 Representation × Influence 矩阵判定呼声受众占比（是否超过大盘 10%）及圈层号召力；
   - 结合 Depth of Effect × Breadth of Effect 矩阵核定影响烈度。
4. **内部沉浸走查与一线体感（Experiential Empathy & Dogfooding）**：
   - 组织“不以解决问题为目的”的端到端体验沉浸（如 Stripe 角色扮演、DoorDash 全员跑单、Slack 屏幕逐页吐槽会）；
   - 记录原生摩擦点（Friction），严禁在体验阶段过早推演解法。
5. **决策裁决与透明闭环（Prioritize, Act & Close the Loop）**：
   - 产出高确定性改动清单并与研发排期挂钩；
   - 对暂缓处理的需求向提出者阐明缘由；对已上线修复主动触达初始反馈者，实现信任资产存储（Trust Vault Deposit）。

## Branches

- **社群领袖诉求沟通分支（Influential Minority Branch）**：针对影响力极高但占比较小的核心圈层（如社区版主、创作者），不盲目全局改版，建立专有交流通道或定制高级配置。
- **全员强制狗粮分支（Mandatory Dogfooding Branch）**：在核心版本上线前部署员工内测版，设计特定引导机制（如定向测试沉默用户召回流程、新用户新手引导）。
- **AI 角色透镜初审分支（AI Persona Simulation Branch）**：在编写 PRD 阶段，挂载注入真实研究上下文的 AI 模拟用户角色，秒级产出反向质疑与视角补充。

## Rules

- **声量审查铁律（Examine Who Is Loud）**：大嗓门不等于大多数；评估反馈前必须核查反馈发起者的账号类型、活跃度及整体人群占比。
- **体验与解法分离铁律（Empathy First, No Early Solutioning）**：在开展走查与体验沉浸会期间，严格遵守“我们不是来解决问题的”规则，彻底杜绝过早争论技术方案打断摩擦记录。
- **全渠道互补原则（No Blind Spots Portfolio）**：禁止仅采纳单一反馈源（如仅看工单或仅看社媒），必须构建覆盖广谱用户的组合。
- **必须闭环原则（Always Close the Loop）**：上线基于用户反馈的改进后，必须有一道机制通知初始提出反馈的用户，将产品迭代转化为忠诚度沉淀。

## Exceptions

- **重大安全与隐私漏洞反弹**：即便提出者仅为 1 名极客用户，涉及安全越权、数据泄露或合规风险的反馈享有最高级别越级通道，不受代表性占比阈值限制。
- **战略探索期先锋客户**：新开辟业务线在寻找 PMF 时，早期先锋领航客户的深度个性化痛点可单点响应，不要求大盘代表性。

## Dependencies

- **工具生态依赖**：客诉工单系统（Zendesk/Intercom）、数据分析系统、社群工具、LLM 文本聚类处理脚本或 CLI 智能体。
- **组织文化依赖**：管理层支持全员业务走查与沉浸制度的时间与资源保障。

## Permissions and Side Effects

- **权限要求**：客服历史数据只读权限、社区管理权限、用户回访触达权限。
- **副作用**：全员沉浸体验会短暂占用产研团队的一线开发工时；对低优先级反馈的透明拒绝可能引发个别极客的不满。

## Gates

- **Gate 1: Noise-to-Signal Qualification Gate**：在将客诉升级为产品需求前，必须通过代表性（>10%）或高影响力圈层验证。
- **Gate 2: First-Hand Immersion Gate**：涉及重大核心工作流重构时，负责人必须亲历端到端真实操作旅程并落盘 Friction Log。
- **Gate 3: Closed-Loop Notification Gate**：基于用户反馈交付的新特性发布时，必须输出对应的触达用户闭环通告清单。

## Open Questions

- 当大模型生成的内容导致用户产生新型虚幻满意度（AI Placating）时，传统文本情绪分析如何校正其虚高打分？
- 极高价值企业客户（贡献 30% ARR）的定制化诉求与 99% 长尾普惠体验发生冲突时，如何在产品架构上实施干净的解耦隔离？

## Unique Value

汇聚 19 位一线顶级产品操盘手（Stripe、DoorDash、Reddit、Duolingo、Figma、Slack 等）的实战心法，建立从“声量去噪 -> 矩阵过滤 -> 沉浸体感 -> 闭环跟进”的全链条体系，根治产研团队易受嗓门绑架和脱离真实体验的顽疾。

## Reading Coverage

- `skills/analyzing-user-feedback/SKILL.md`: 涵盖四大核心原则（Experiential Empathy, Mandatory Service Participation, Creator Mindset Immersion, Statistical Representation Filtering）、核心模板索引与避坑清单。
- `skills/analyzing-user-feedback/references/artifacts.md`: 涵盖 39 个具体框架、模板与清单（包括 Balanced Feedback Portfolio, Complaint-Storms, Duolingo Dogfooding, Representation × Influence Matrix, The Trust Vault, Walk the Store 等）。
- `skills/analyzing-user-feedback/references/guest-insights.md`: 涵盖 19 位嘉宾的 26 项战术建议（包括 Boris Cherny, Brian Tolkin, Christine Itwaru, Dan Shipper 等）。
