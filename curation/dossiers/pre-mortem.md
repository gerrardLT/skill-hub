# Pre-Mortem Dossier

## Problem
产品发布前夕，团队往往由于乐观偏差、沟通壁垒或权威压力，对潜在的系统性故障、交付漏洞或用户采用阻力保持沉默或缺乏系统评估，导致上线后出现灾难性失败（如核心功能故障、监管合规阻断、关键客户流失、声誉受损）。常规的事后复盘（Post-Mortem）往往发生在损失已经造成之后，补救代价巨大。

## When to Use
- 在产品正式上线前 2-4 周，需要对 PRD、发布计划或重大里程碑进行系统性抗风险压力测试时；
- 面临重大版本发版、新产品上市或技术架构重大割接，存在高度不确定性与跨团队依赖时；
- 团队对方案存在隐性疑虑、但常规评审会未能有效暴露深层担忧时。

## When Not to Use
- 产品已在线上发生故障或事故（此时应立即执行故障响应 `incident-response` 与事后复盘 `retro`）；
- 处于早期模糊探索阶段，尚无明确的 PRD、范围定义或发布计划（应优先使用 `discovery-process` 或 `interview-script`）；
- 组织文化或管理层试图将风险评估作为追责或政治斗争工具的场景。

## Role
资深产品经理（Veteran Product Manager），扮演客观、前瞻、建设性的跨职能风险协调者，统合工程、设计、市场与运营等多方视角。

## Inputs
- **必备参数**：`$ARGUMENTS`（待分析的产品名称、项目标识或发布计划）；
- **基础文档**：PRD、产品规范或发布计划文档（包含产品定位、目标客群、核心假设、范围边界与里程碑时间线）；
- **上下文信息**：行业环境、竞品动态、过往发布事故或技术依赖清单。

## Outputs
- 独立的 Markdown 风险分析报告，文件命名格式为 `PreMortem-[product-name]-[date].md`；
- 报告必须包含四个核心部分：
  1. `Tigers (Real Risks)`：基于客观证据与逻辑的真实致命风险清单及其分类；
  2. `Paper Tigers (Overblown Concerns)`：表面看似严重但实际概率极低或被夸大的担忧，附带排除与对齐依据；
  3. `Elephants (Unspoken Worries)`：团队心存疑虑但未充分讨论的隐性假设，附带验证与调查建议；
  4. `Action Plans for Launch-Blocking Tigers`：针对所有上线阻断级真风险的明确行动计划（包含风险、缓解措施、责任人与截止日期）。

## Workflow
1. **收集与研读 PRD**：细读用户提供的产品文档，明确核心功能、目标市场、关键假设与时间线，必要时调研外部竞品与监管环境；
2. **逆向推演失败**：假定产品在 14 天后上线并遭遇彻底失败（用户零采用、指标崩盘、声誉受损），推演具体失败原因、遗漏环节与盲目自信点；
3. **风险三级定性归类**：将推演出的所有潜在问题归入 Tigers（真老虎）、Paper Tigers（纸老虎）、Elephants（房中大象）三类；
4. **Tigers 紧迫度分级**：对所有 Tigers 依据时间线与影响度划分为 Launch-Blocking（上线阻断）、Fast-Follow（上线 30 天内速跟）、Track（持续观察）；
5. **制定阻断风险行动计划**：针对每个 Launch-Blocking Tiger，逐项给出明确的缓解方案、责任归属与完成截止日；
6. **编排标准输出**：按照固定结构组织报告内容，保存至指定命名规范的文件；
7. **上线前走查核验**：在上线前 2-3 周重新核对缓解计划的推进与闭环状态。

## Branches
- **风险性质分类分支**：
  - *真实风险（Tigers）*：具备明确证据或因果逻辑，必须采取应对行动；
  - *表面担忧（Paper Tigers）*：外表骇人但实际影响小或发生概率低，记录说明以对齐认知，不分配大量资源；
  - *隐性问题（Elephants）*：未经验证的关键假说或未公开讨论的顾虑，列入调查追踪事项；
- **不确定性保守分支**：当无法确切判定某一问题是否为真实风险时，默认归入 Tigers 处理；
- **紧迫度应对分支**：
  - *Launch-Blocking*：必须在发版前解决，未闭环不得发版；
  - *Fast-Follow*：不阻断发版，但须在上线后 30 天内跟进解决；
  - *Track*：列入上线后监控看板，触发阈值后再行介入。

## Rules
- **真实与建设性原则**：分析旨在暴露系统薄弱环节并提升就绪度，严禁演变为追责或互相指责；
- **疑虑从真原则（Default to Tiger）**：对分类存在分歧或证据不足的潜在风险，默认划入 Tigers 优先处置；
- **跨职能多视角覆盖**：风险辨识必须涵盖工程实现、交互设计、GTM/运营及商业合规等多个维度；
- **阻断项四要素完整性**：针对 Launch-Blocking Tiger 的行动计划必须完备包含风险描述、具体缓解措施、责任人（Owner）、截止日期（Due Date）；
- **周期性回溯机制**：在正式上线前 2-3 周必须重新核验风险缓解措施的实际落地情况。

## Exceptions
- **缺少正式 PRD**：若用户未提供详尽文档，允许基于简要计划或提纲启动，但必须在报告中显著标注假设前提与信息盲区；
- **跨团队强依赖阻断**：若关键阻断风险依赖外部团队或第三方平台且无法在发版前自闭环，必须升级为管理层 Go/No-Go 决策项并制定降级兜底案。

## Dependencies
- **前置依赖**：PRD 或产品发布方案（通常由 `prd-development` 产出）；
- **协作依赖**：工程与设计输入（`codebase-design`, `ui-ux-pro-max`）；
- **下游消费**：质量验收与验证门禁（`testing-strategy`, `verification-before-completion`）、发布流程（`ship`）。

## Permissions and Side Effects
- 读取权限：只读读取用户提供的 PRD、架构图与发布说明；
- 写入权限：在工作区输出或更新 `PreMortem-[product-name]-[date].md`；
- 无系统配置变更、无网络调用或代码库侵入性副作用。

## Gates
- **分类覆盖度门禁（Tripartite Coverage Gate）**：所有推演出的风险必须明确归入 Tigers、Paper Tigers 或 Elephants，无遗漏无未分类项；
- **阻断项四要素门禁（Action Plan Four-Field Gate）**：所有 Launch-Blocking Tigers 的行动计划必须完整具备风险、缓解措施、责任人、完成期限四要素，缺失任意要素不得标记就绪；
- **跨职能视角门禁（Cross-Functional Perspective Gate）**：风险集合中必须包含工程技术、用户体验或商业市场中至少两个不同维度的风险源。

## Open Questions
- 当出现无法化解的 Launch-Blocking 风险时，与 dev-loop 发版门禁（Gate 4/5）的硬阻断联动机制在自动化管道中应如何触发？

## Unique Value
采用逆向推演（Assume Failure）的心智模型，结合直观生动的动物隐喻（Tigers/Paper Tigers/Elephants），打破团队乐观主义幻觉与沉默陷阱，将模糊焦虑提纯为高确定性的上线前阻断防御清单。

## Reading Coverage
- 完整阅读并覆盖 `skills/pre-mortem/SKILL.md`（行 1-93）。
- 外部参考链接（行 88-93）归入 Further Reading，标记为 defer 并在实践中按需引用。
