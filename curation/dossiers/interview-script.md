# interview-script Dossier

## Problem

产品经理与 Product Trio 在探索阶段若直接向用户询问想法或推销功能，容易收集到无用的礼貌性意见与虚假承诺。该技能解决如何在无偏见的前提下，通过结构化访谈与挖掘历史行为，提炼真实的用户情境、痛点、未满足需求及支付意愿。

## When to Use

- 准备与真实客户、潜在买方或内部用户进行探索性访谈时。
- 编制标准化的客户访谈大纲、提问指南与现场速记模板时。
- 处于连续发现的 Stage 1 (Explore) 阶段，需要验证假设或澄清问题空间时。

## When Not to Use

- 需要大规模定量验证时（应使用问卷、埋点数据或 A/B 测试）。
- 处于销售演示、商业谈判或功能推介场景时（严禁在访谈中推销）。
- 仅需要利益相关者内部对齐或合规审批时。

## Role

产品经理（PM）作为访谈主导者，建议与 Product Trio（PM、产品设计师、工程师）无代理人隔阂地共同参与访谈与发现。

## Inputs

- 研究主题或业务领域参数（`$ARGUMENTS`）。
- 选填输入附件：用户画像（personas）、假设清单（hypotheses）、产品简报（product briefs）或历史访谈记录（previous interview notes）。
- 既定的研究目标与待验证假设。

## Outputs

1. Markdown 格式的结构化访谈大纲（包含 Opening、Warm-Up、Core Exploration、Probing Techniques、The Mom Test 约束及 Wrap-Up）。
2. 配套的 Markdown 访谈速记模板（包含参与者信息、Key Jobs、Current Solution、Biggest Pain、Desired Outcome、Willingness to Pay、Surprise Finding 与 Follow-up）。

## Workflow

1. **澄清研究目标**：明确团队需要解答的具体问题、研究支持的业务决策及待验证假设。
2. **查阅前置材料**：如有输入画像、假设清单或历史记录，优先通读。
3. **构建访谈大纲**：
   - Opening (2-3 min)：介绍目的（学习非销售）、声明无标准答案、确认录音许可与时长。
   - Warm-Up (5 min)：询问角色与日常工作，建立融洽关系。
   - Core Exploration (15-20 min)：围绕 JTBD 的四大维度（现状与过去行为、痛点、期望结果、支付意愿/优先级）提问。
   - Probing Techniques：在遇到关键线索时选用追问技巧深入挖掘。
   - Wrap-Up (3-5 min)：开放性收尾、询问推荐人选、致谢及说明后续。
4. **定制化适配**：根据产品领域、画像与可用时长增删问题或模块。
5. **附带速记模板并保存**：输出完整的脚本与结构化速记表格。

## Branches

- **附带背景资料分支**：若提供了 personas/hypotheses/briefs，则提取针对性问题；若未提供，则基于通用 JTBD 框架构建基础大纲。
- **访谈时长分支**：时长充裕（30+ min）展开全量核心探索与多轮追问；时长紧张（15-20 min）浓缩为核心痛点与替代方案。
- **发现新线索分支**：触及强烈情绪或反直觉事实时，切入 Probing 深度追问；若为表扬夸奖则作为噪音忽略。

## Rules

- **The Mom Test 核心法则**：
  - 询问对方的生活与过往行为，绝不询问对方对新想法的看法。
  - 询问具体发生过的历史事实，绝不询问虚构的未来意愿（“你会用 X 吗”毫无价值）。
  - 少说多听，严格遵守 80% 倾听 / 20% 提问的比例。
  - 访谈全程严禁推销产品或辩解。
  - 关注强烈情绪（痛苦或兴奋），这些是真实需求的信号。
  - 赞美即噪音（“听起来很酷”不代表真实价值）。
- **语言与问题表述**：
  - 使用过去时态与具体情境（“上次您做……时”）。
  - 期望结果必须使用用户自己的原话记录，不得替换为团队内部行话。
- **角色协同**：
  - 强调直面用户无代理人，主张 Product Trio 协同发现。

## Exceptions

- **用户给出赞美或泛化预测**：将其视为噪音标记，不作为需求证据，通过要求具体案例将对话拉回历史事实。
- **时间受限**：若受访者临时压缩时间，优先保留 Core Exploration 中的现状、替代方案与最大痛点，跳过宽泛的 Warm-Up。

## Dependencies

- 理论框架源于 Rob Fitzpatrick 的 *The Mom Test* 与 Teresa Torres 的 *Continuous Discovery Habits* (Product Trio)。
- 本地无代码或脚本依赖。
- 外部链接：Product Compass 的 User Interviews 指南与 CPDM 课程，仅作来源背景指针，未在本地包含。

## Permissions and Side Effects

- 静态策展产物生成未修改外部环境或执行任何写操作。
- 实际执行访谈前，若涉及录音或录屏，必须先征得受访者明确许可；涉及客户敏感信息时需遵守数据合规要求（策展安全保障）。

## Gates

### Source Gates

- **The Mom Test Gate**：大纲中不得包含推销产品、询问未来预测（如“你愿意购买吗”）或引导性问题；必须聚焦过去具体行为与生活情境。
- **No-Proxy Gate**：访谈必须由团队直接接触真实用户，不得仅依赖间接转述代理。

### [Curated acceptance check]

- **Output Completeness Check**：输出产物必须同时包含完整的访谈大纲与 8 项字段的速记模板。
- **Timing Gate**：访谈设计需明确各环节时间分配，核心探索需占整体时长的一半以上。

## Open Questions

- 来源未给出招募受访者的具体筛选问卷标准。
- 来源未定义如何将多份速记表格聚合为决策级综合洞察的方法论。

## Unique Value

将连续发现（Continuous Discovery）与 The Mom Test 原则无缝结合，提供了可直接执行的端到端提问范式与速记模板，防止产品团队构建出自欺欺人的伪需求大纲。

## Reading Coverage

- `skills/interview-script/SKILL.md` — `read`；105 行全量读取，无遗漏。
- 外部链接（Product Compass 指南与课程）— `excluded`；仅作参考指针。
