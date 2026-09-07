# Scenarios

## 普通 SaaS 发布

READINESS → BUILD → ENV → PLAN → CANARY → VERIFY → STABILIZE → REVIEW。

## 数据库大迁移

先双写/兼容设计和演练，再小批次迁移；无可验证回滚则不得直接全量。

## 紧急回滚

优先止损，执行已验证回滚；稳定后转 evolution 做事故调查。
