# L5-B 匹配对照实验协议

## 目标

检验 Agentic SDLC OS 相较普通 Agent 是否在**相同任务起点、模型、工具权限、环境和时间预算**下改善周期、返工、质量、追踪和验收结果。

## 强制设计控制

- 预注册后冻结任务、指标、随机顺序和盲码。
- 每个任务同时产生 `baseline` 与 `sdlc` 两个制品，执行顺序在全样本内平衡。
- 两臂必须使用相同 `model`、`toolset_hash`、`start_state_hash`、`environment_hash`。
- 每次执行必须使用唯一 `execution_context_id`，禁止复用另一臂上下文。
- 执行必须遵守预注册的 arm 顺序。
- 两个盲码制品必须由相同的独立评审集合完成评审；评审者不得同时是执行者。
- Prompt、工具集、起始状态、环境、制品和运行日志均记录 SHA-256；运行记录使用链式哈希。
- 跨臂学习或其他污染必须显式记录，污染实验不能形成因果结论。
- 正式结果必须执行 `seal`；封存后禁止增加运行或评审。

至少 5 个完整任务对；正式结论建议 10 个以上。

## 判定

正向结论同时要求：

1. 至少两个主要类别平均改善 >=5%；
2. 至少一个主要指标的配对 Bootstrap 95% CI 下界 >0；
3. 不存在严重质量/验收退化；
4. 所有匹配控制、盲评、污染检查通过；
5. 实验已封存且 `formal_evidence_eligible=true`。

未封存的真实实验只能输出 `provisional-*`。合成实验永远输出 `synthetic-smoke-only`，不能作为提效证据。

## 执行

```bash
python scripts/l5b_matched_experiment.py init experiment.json --project PROJECT --target-pairs 5
python scripts/l5b_matched_experiment.py add-task experiment.json --task-id T1 --task-hash SHA256 --domain web --complexity 3 --time-budget-minutes 90
python scripts/l5b_matched_experiment.py freeze experiment.json
python scripts/l5b_matched_experiment.py record experiment.json --task-id T1 --arm baseline --executor-code E1 --execution-context-id CTX1 --model MODEL --prompt-hash SHA256 --toolset-hash SHA256 --start-state-hash SHA256 --environment-hash SHA256 --artifact-hash SHA256 --run-log-hash SHA256 ...
python scripts/l5b_matched_experiment.py review experiment.json ...
python scripts/l5b_matched_experiment.py seal experiment.json
python scripts/l5b_matched_experiment.py validate experiment.json --json
python scripts/l5b_matched_experiment.py report experiment.json --output report.md
```
