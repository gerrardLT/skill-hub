# 六步定义与 Gate 细则

以 71 个开源候选的交接契约为标准。每步五要素：目标 / 核心开源 Skill / 输入 / 产出 / Gate / 兜底。

## ① 需求

- **目标**：把模糊想法变成对齐过的问题定义、目标用户、成功标准与优先级。
- **核心 Skill**：`prd-development` + `discovery-process`（deanpeters）；备选 `prioritization-frameworks`（phuryn）、`competitive-strategy`（refoundai）。
- **输入**：用户口述 / 既有材料；无。
- **产出**：`docs/prd.md`（含问题陈述、目标用户、核心场景、Given/When/Then 验收标准、非目标）。
- **Gate**：
  1. 问题陈述指向具体人群的具体痛点，不是"做一个 X 平台"；
  2. 验收标准必须符合 Gherkin（Given/When/Then）或具备可独立测试的量化指标；
  3. 非目标明确列出（防止范围蔓延）；
  4. 核心假设已列出并与已知事实区分，不得把假设写成事实。
- **兜底**：自产 1 页 PRD；用户答不出的字段标注 `⚠️ 待验证`，不得编造。

## ② 设计

- **目标**：把 PRD 转化为可实现、可验收的设计规格。
- **核心 Skill**：`impeccable`（pbakaus，唯一主视觉导演）+ `ui-ux-pro-max`（组件与排版知识）+ `web-design-guidelines`（规范约束）+ `review-animations`（动效把关）。
- **输入**：`docs/prd.md`。
- **产出**：`docs/design.md`（页面清单、每页关键状态、交互要点、导航结构、Design Tokens）。
- **Gate**：
  1. 主流程完整可走通（入口→核心操作→完成）；
  2. 异常态完整设计：空 / 加载 / 错误 / 权限 / 边界数据（移动端加离线）；
  3. 遵守"单一视觉导演"铁律，不允许多个设计 skill 风格打架；
  4. 与 PRD 的验收标准一一对应，无遗漏场景。
- **兜底**：自产 1 页设计说明，重点是状态覆盖而非视觉修饰。

## ③ 实现

- **目标**：以 TDD 驱动按规格编码，拆解小步计划并自验。
- **核心 Skill**：`writing-plans` + `test-driven-development` + `systematic-debugging`（均为 obra/superpowers）；叠加 `andrej-karpathy-skills:karpathy-guidelines` 约束。
- **输入**：`docs/design.md` + `docs/prd.md` 验收标准。
- **产出**：`src/`（源码）+ 测试用例套件；运行方式写入 README。
- **Gate**：
  1. 严格红-绿-重构闭环：必须先写失败测试，再写实现，最后重构；
  2. 核心功能可跑通，测试全部 PASS；
  3. 无已知 P0 严重缺陷（崩溃 / 数据丢失 / 主流程断裂）；
  4. 遵循外科手术式修改，无凭空引入的抽象与无关重构。
- **兜底**：主 agent 手写实现 + 逐条运行单元测试自验。

## ④ 验收

- **目标**：独立验证实现是否符合设计与需求——**QA 不得自修自验**。
- **核心 Skill**：`testing-strategy`（anthropics）+ `verification-before-completion`（superpowers）+ `qa-only`（gstack，只报不修）+ `code-review`（anthropics）。
- **输入**：`src/` + `docs/design.md` + `docs/prd.md` 验收标准。
- **产出**：`docs/qa-report.md`（逐条结论：通过 / 不通过 + 截图 / 运行日志证据）。
- **Gate**：
  1. 禁止无新鲜证据的通过声明（严格遵守 verification-before-completion）；
  2. QA 仅输出报告，任何修复必须打回 ③ 由 Engineering 实施，严禁自修自验；
  3. 阻断级 Bug（P0/P1）必须为零才能放行；
  4. 不通过项明确指出回退目标（回③修实现 / 回②修设计 / 回①修需求）。
- **兜底**：按 PRD 验收标准逐条人工核对并生成报告。

## ⑤ 交付

- **目标**：让没参与开发的人能审查、部署、接手，并安全创建 PR。
- **核心 Skill**：`ship`（gstack）+ `github-actions-hardening`（github CI 安全）。
- **输入**：前四步全部产物。
- **产出**：`docs/` 交付集（架构说明、关键流程、权限/变量、测试覆盖说明）+ 生产就绪 PR。
- **Gate**：
  1. 架构：模块划分 + 依赖方向，一页能看懂；
  2. CI/CD 工作流已审查，无脚本注入与过度权限风险；
  3. 环境变量与密钥只列名不泄露值；
  4. 测试覆盖真实诚实标注，不隐藏未测边界。
- **兜底**：从代码扫描自产 README + 架构说明与启动指南。

## ⑥ 复盘

- **目标**：对照当初判断和实际结果，提炼下一轮要用的经验——闭环回流的关键步。
- **核心 Skill**：`systematic-debugging`（obra）+ `analyzing-user-feedback`（refoundai）+ `retro`（gstack）；需要时激活 Sentry / Datadog / PostHog 适配器拉取真实监控证据。
- **输入**：`docs/prd.md` 成功标准 + 真实运行指标 / 用户反馈 + 各步决策记录。
- **产出**：`docs/retro.md`（其中"下一轮需求输入"一节直接作为下一轮 ① 的输入）。
- **Gate**：
  1. Expected vs Actual 逐项对比，不报喜不报忧；
  2. 每个 Gap 有归因（当初判断错 / 执行走样 / 外部变化）；
  3. 产出至少 1 条下一轮明确的行动项（做 / 改 / 砍）；
  4. 经验写入 `.workflow/state.md` 决策记录回流第 ① 步。
- **兜底**：自产 Expected vs Actual 对比表 + 3 条行动建议。
