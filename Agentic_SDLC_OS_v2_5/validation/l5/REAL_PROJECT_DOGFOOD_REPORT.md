# Agentic SDLC OS v2.0 真实项目 Dogfooding 报告

- 生成时间：`2026-08-31T09:12:15+00:00`
- L5-A 真实项目单臂 Dogfooding：PASS
- L5-B 因果效果验证：尚未完成（匹配对照 NOT RUN）

## 1. 结论

系统已把用户真实的乒乓球馆 SaaS 需求压缩为一个可证伪垂直切片，并完成产品定义、体验设计、工程实现、独立测试、部署冒烟、运行观测、学习决策和跨 OS 回流。

本次没有匹配的普通 Agent 对照组、重复项目样本、人力工时和完整 Token 成本，因此不能宣称 Agentic SDLC OS 已被证明提高生产率、降低总成本或优于其他工作流。

## 2. 真实输入与试点范围

输入来自用户自有的乒乓球馆 SaaS 功能清单和设计规范。本次选择高风险、高可验证的闭环：

```text
场次容量 → 原子预约 → 满额进入 FIFO 候补 → 取消释放名额
→ 队首自动转正 → 指标和审计 → 基于证据回流
```

需求锚点：动态球台锁定与并发防超售、公平排队、唯一候补位置、自动转正、多租户隔离、幂等与可观测指标。

## 3. 可执行实现

- FastAPI + SQLite WAL；
- `BEGIN IMMEDIATE` 原子事务；
- 活跃预约和候补的部分唯一索引；
- 幂等键与响应重放；
- 多租户隔离；
- 取消后同事务 FIFO 转正；
- 审计事件、场次指标 API；
- 无外部依赖的可交互原型。

代码位置：`validation/l5/pilots/venue-reservation/`。

## 4. 实测结果

| 指标 | 结果 |
|---|---:|
| 自动测试 | 11/11 PASS |
| 代码覆盖率 | 95.69% |
| 并发请求 | 200 |
| 工作线程 | 32 |
| 场次容量 | 20 |
| 成功预约 | 20 |
| 候补 | 180 |
| 超售 | 0 |
| 吞吐 | 1064.43 req/s |
| p50 | 1.857 ms |
| p95 | 107.185 ms |
| p99 | 133.551 ms |
| 部署冒烟 | 8/8 PASS |

部署冒烟覆盖：健康检查、创建场次、成功预约、幂等重放、满额候补、取消自动转正、零超售和多租户隔离。

## 5. Agentic SDLC OS 实际回放

| 控制项 | 结果 |
|---|---:|
| Accepted 制品 | 42 |
| 内容契约有效 | 42/42 |
| 平均制品质量分 | 0.9596 |
| Gate | 7/7 PASS |
| 强制转换 | 0 |
| Gate Waiver | 0 |
| 控制面健康度 | 90.8/100 |
| 最终回流 | pm/DISCOVERY |

Evolution 没有把局部工程成功误判为产品成功，而是识别出真实用户结果与因果证据不足，回流 PM Discovery。

## 6. 证据边界

已证明：真实需求可转成可运行软件；六个 OS、42 个制品和 7 个 Gate 可形成完整证据链；代码、测试、部署、指标与学习回流能够连接。

尚未证明：相较普通 Agent 的周期、返工、缺陷、人工成本或 Token 成本改善；外部生产流量和长观察窗口稳定性；真实用户转化、留存或商业结果。

## 7. 下一验证阶段

按 `validation/l5/PROTOCOL.md` 执行 L5-B：在同一需求、模型、工具和时间预算下，比较普通 Coding Agent 与 Agentic SDLC OS；至少每组 2 次，建议每组 5 次。

## 8. 可复现命令

```bash
cd validation/l5/pilots/venue-reservation
python scripts/verify_pilot.py
```

机器可读证据：`reports/pilot-verification.json`、`reports/sdlc-dogfood-run.json`、`reports/deployment-smoke.json`、`reports/performance.json`、`reports/coverage.json` 和 `.sdlc/state.json`。
