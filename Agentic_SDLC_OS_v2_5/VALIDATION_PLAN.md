# 验证计划

| 层级 | 验证内容 |
|---|---|
| L0 | Skill、Manifest、Schema、依赖、打包和文档一致性 |
| L1 | 状态、Gate、审计、预算、审批、队列、密钥、领域包 |
| L2 | 跳级、篡改、伪证据、自批、过期 lease、预算绕过、QA 自修自验、Provider 越界等红队 |
| L3 | 已知、改写、歧义和跨语言路由 |
| L4 | 绿地、旧系统、事故、五类项目场景回放 |
| L5-A | 真实需求到可运行代码、测试、发布和学习回流 |
| L5-B | 普通 Agent 与 SDLC OS 匹配对照 |
| L6 | Live PostgreSQL、并发压测、故障恢复、30 天持续运行 |

通过条件：

- 所有硬 Gate 和红队用例通过。
- Design 单主导、QA 独立验收、Evolution Provider opt-in 组合规则通过专项测试。
- 无错误高置信自动路由；歧义安全拒绝。
- L5-B 不允许合成数据替代真实对照。
- Production Candidate 需 live PostgreSQL、真实多项目、30 天无严重控制面事故和正向成本收益。
