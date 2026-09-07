# L5-B 匹配对照实验协议

## 目标

检验 Agentic SDLC OS 相较普通 Agent 是否在**同一任务、模型族、工具权限、时间预算**下改善周期、返工、质量、追踪和验收结果，而不是只证明系统能运行。

## 设计

- 预注册、匹配任务、随机执行顺序、交叉设计。
- 每个任务同时产生 `baseline` 与 `sdlc` 两个制品。
- 制品使用盲码交给独立评审者；评审阶段不得看到实验组名称。
- 记录 Prompt、工具集、制品、运行日志 SHA-256，并使用链式哈希防篡改。
- 至少 5 个完整任务对；正式结论建议 10 个以上、覆盖多个项目类型。

## 核心指标

- 周期：`lead_time_minutes`
- 人力：`human_minutes`
- 成本：`token_cost_usd`
- 返工：`rework_fraction`
- 质量：`escaped_defects`、`critical_defects`、`maintainability_score`
- 追踪：`trace_coverage`
- 结果：`acceptance_pass_rate`

## 判定规则

只有同时满足以下条件才判为正向：

1. 至少两个主要类别平均改善不低于 5%；
2. 至少一个主要指标的配对 Bootstrap 95% CI 下界大于 0；
3. 不存在严重质量或验收退化；
4. 样本完整、无跨组污染、预注册与记录链校验通过。

合成数据只能验证工具链，永远不能作为提效证据。

## 执行

```bash
python scripts/l5b_matched_experiment.py init experiment.json --project PROJECT --target-pairs 5
python scripts/l5b_matched_experiment.py add-task experiment.json --task-id T1 --task-hash SHA256 --domain web --complexity 3 --time-budget-minutes 90
python scripts/l5b_matched_experiment.py freeze experiment.json
python scripts/l5b_matched_experiment.py record experiment.json ...
python scripts/l5b_matched_experiment.py review experiment.json ...
python scripts/l5b_matched_experiment.py validate experiment.json --json
python scripts/l5b_matched_experiment.py report experiment.json --output report.md
```

## 证据边界

当前仓库包含合成烟测和正式实验工具，但未伪造普通 Agent 对照数据。正式 L5-B 结论必须来自真实匹配任务执行。
