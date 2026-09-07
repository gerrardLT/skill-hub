# v2.2 Real Project Matrix

| 项目 | 类型 | 验证重点 | 真实发现 | Gate 结论 |
|---|---|---|---|---|
| aus-ele | Brownfield, FastAPI + React | bounded change、测试、Release/Production 边界 | lockfile 镜像污染；反向发现 v2.0 过度治理 | Release-ready PASS；Production BLOCKED |
| zwzz | Greenfield, EV charging research/design | 实施就绪、监管/协议/支付前置 | 设计完整但关键外部契约未闭合 | PM-ready BLOCKED |
| ZW-Insight | Brownfield enterprise SaaS, Spring/Vue | 高风险鉴权修复、环境阻断、跨项目规则隔离 | supplier JWT 默认 signing secret；credential-like literal | Verification-ready BLOCKED |

`BLOCKED` 是控制正确性的正向证据：系统在关键证据缺失时没有自动放行。
