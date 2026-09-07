# 生产事故提示词

```text
启动 Agentic SDLC OS Incident Path。

优先级：人员/数据安全 → 限制影响 → 恢复服务 → 保存证据 → 根因与预防。

1. Route 到 Evolution/TRIAGE，记录影响、开始时间、版本、变更、受影响用户和已知事实。
2. 不猜根因；建立竞争假设和验证信号。
3. 任何回滚、部署、数据修复或生产写操作都必须获得明确授权，由 Release OS 执行并记录。
4. 稳定后由 Incident Investigator 建时间线；Engineering 做根因修复，QA 做影响回归，Release 渐进上线。
5. Evolution 比较 Expected vs Actual，生成 incident-review 与 learning-decision，并路由系统性改进。
6. 输出 DONE/BLOCKED 状态和新鲜证据，不省略未解决风险。
```
