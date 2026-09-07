# L5 真实项目效果验证协议

L0–L4 证明控制系统可运行且主要绕过路径受控。L5 分为两个不可混淆的层级。

## L5-A：真实项目单臂 Dogfooding

目标：证明系统能处理真实需求、生成可执行软件，并跑通六个 OS、Gate、部署、观测和学习回流。

最低要求：

- 使用真实项目资料，不使用为测试编造的需求；
- 选择有业务价值且可证伪的垂直切片；
- 必须包含可运行代码，而非仅生成文档；
- 执行功能、并发/异常、部署冒烟和运行指标验证；
- 从 PM 运行到 Evolution，并产生明确 re-entry；
- 记录所有强制转换和 Waiver；
- 明确真实生产、用户结果和因果结论的证据边界。

L5-A 通过只代表“真实项目闭环可运行”，不代表“相比其他工作流更有效”。

参考实现：

```bash
cd validation/l5/pilots/venue-reservation
python scripts/verify_pilot.py
```

报告：`validation/l5/REAL_PROJECT_DOGFOOD_REPORT.md`。

## L5-B：匹配对照效果验证

目标：判断 Agentic SDLC OS 是否在真实项目中产生净收益。

### 1. 预注册

项目开始前固定：

- 对照方式：匹配历史项目、并行对照或顺序交叉；
- 纳入与排除标准；
- 每组至少 2 次迭代，建议 5 次以上；
- 指标口径、数据来源、观察窗口；
- 决策规则和允许的中止条件；
- 混杂变量：人员经验、项目规模、技术栈、模型版本和需求不确定性。

```bash
python scripts/l5_experiment.py init validation/l5/real-project.json \
  --project "项目名称" \
  --comparison historical-matched \
  --target-iterations 5
```

### 2. 记录两组迭代

每次记录：周期、返工、逃逸缺陷、事故、回滚、追踪覆盖、证据驱动决策比例、目标达成、人力、模型成本和可操作性。

```bash
python scripts/l5_experiment.py record validation/l5/real-project.json \
  --arm baseline --iteration-id B01 --artifact-id baseline-B01 \
  --lead-time-hours 120 --rework-rate 0.30 --escaped-defects 5 \
  --incidents 1 --rollback-rate 0.10 --trace-coverage 0.40 \
  --evidence-decision-rate 0.35 --goal-attainment 0.55 \
  --human-hours 90 --token-cost-usd 0 --actionability-score 6.0
```

SDLC 组使用同一命令，把 `--arm` 改为 `sdlc`。

### 3. 盲评

将关键制品匿名标记为 A/B，不向评审者透露所属组：

```bash
python scripts/l5_experiment.py review validation/l5/real-project.json \
  --artifact-id baseline-B01 --reviewer-code R01 --arm-code A \
  --actionability 6 --correctness 7 --clarity 6
```

### 4. 报告

```bash
python scripts/l5_experiment.py validate validation/l5/real-project.json
python scripts/l5_experiment.py report validation/l5/real-project.json \
  --output validation/l5/REAL_PROJECT_REPORT.md
```

### 5. 判定边界

- **Positive**：至少两个主要类别改善 5% 以上，且没有严重回归；
- **Negative**：出现严重质量/结果回归，或至少两个主要类别恶化 5% 以上；
- **Inconclusive**：样本足够但差异不稳定；
- **Insufficient data**：任一组未达到预注册样本量。

工具只进行透明算术，不自动证明因果。合成数据只验证工具链；L5-A 单臂结果也不能替代 L5-B。
