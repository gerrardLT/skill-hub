# 生产成熟度

## 当前等级

**Beta Candidate / 有条件通过。Production Candidate = 否；Production Ready = 否。**

当前 v2.5 工程回归：116/116 tests + 7 subtests PASS；68/68 红队 PASS；7/7 OS Skills PASS。Skill 组合升级不改变生产成熟度门槛。

禁止凭人工判断升级成熟度标签。必须运行：

```bash
python scripts/maturity_gate.py assess validation/maturity/current-evidence.json --target production-candidate --json
```

Production Candidate 最低要求：

1. >=3 个独立且可执行的真实项目关键生命周期验证；
2. >=5 对真实 L5-B，非 Synthetic，已封存，`decision=positive` 且 `formal_evidence_eligible=true`；
3. Live PostgreSQL 并发压力 + 故障恢复通过；
4. >=30 天生产 soak，0 P0、0 P1 控制面事故；
5. RBAC、Secret Rotation、Backup/Restore、Audit Export 组织级演练通过。

当前只有 SQLite 本地压力与恢复验证；它不能替代 PostgreSQL 生产证据。
