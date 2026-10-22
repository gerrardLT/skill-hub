# R5 设计：1.1.0 候选对 1.0.0 的正面评测

## 比较对象

- v100：冻结的 1.0.0 SKILL.md（`slots/v2/1.0.0`）。
- v110：1.1.0 候选 SKILL.md（`evals/candidates/capability-compiler-v2/revision-1.1.0`）。被合并的三个 Skill，v110 一侧用合并目标的 SKILL.md 作答，题目仍是被合并项的旧题。
- baseline：不带 Skill 的对照。

## 两个题集

| 题集 | 来源 | 规模 | 执行的变体 | 评判的配对 |
|---|---|---|---|---|
| old | Phase D 冻结任务集（sha `4e1dc73e…`） | 156 Skill、312 题 | 仅新跑 v110；v100 与 baseline 复用 Phase D 已落盘输出 | v110 对 v100 |
| fresh | 本轮新出，只读 1.0.0 capability 契约，并被要求避开旧题的行业、产物与场景 | 154 Skill、308 题 | baseline、v100、v110 全部新跑 | v110 对 v100；v110 对 baseline |

- 出题模型不读任何 SKILL.md，避免照着 1.1.0 新增内容出题。冻结时检查题面和评分标准是否复述 v100 或 v110 的 Skill 专有措辞，命中则标记。
- 旧题的 v100 输出是 Phase D 时跑的，v110 是本轮跑的，二者存在模型非确定性差异。fresh 题集三个变体同期新跑，用来抵消这个混杂。

## 执行与评判

- 执行模型 `router9-qoder/cx/gpt-5.6-sol`，评判模型 `router9-qoder/kr/claude-opus-5.5`。
- 每次调用为 fresh `pi -p --mode json` 进程，无工具，空 cwd，环境变量白名单。
- 每个配对两种呈现顺序各评一次；两次结论一致才计胜或负，否则记平。overreach、fabrication 须双顺序均标记才计。

## 判定阈值（运行前冻结，不得事后调整）

1. old 题集：v110 对 v100 的胜数不低于负数。
2. fresh 题集：v110 对 v100 的胜数不低于负数。
3. 任一 Skill 在 old 与 fresh 两个题集都出现负（双顺序一致）：列为回退，发布前须逐个处理。
4. v110 新增 overreach 或 fabrication（v110 双顺序均标、v100 不是）：逐条人工复核，不得忽略。
5. 仅报告、不设硬阈值：
   - Phase D 判为 negative 或 mixed 的 35 个 Skill 的恢复情况。
   - fresh 题集上 v110 对 baseline 的胜负。
6. 第 1 至 3 条任一不满足，报告写明"不建议发布"，并如实列出原因。

## 规模与节奏

- 先试点 6 个 Skill：`completion-evidence-gate`、`test-case-design-and-export`、`customer-interview-execution`、`opportunity-prioritization-and-frameworks`、`ai-model-and-data-architecture`、`cross-domain-ui-preflight-checklists`（后者仅 old）。
- 试点通过后放量：全量约 3,200 次调用，约 2,500–3,000 万 tokens。
- 失败、超时、被拒的试点全部保留，不覆盖；仅基础设施失败允许同参重试一次并记录。
- `browser-data-acquisition-runtime` 的出题曾连续 4 次 provider 流中断，再次失败则标 incomplete。

## 限制

每 Skill 每题集只有 2 题，一个评判模型，结论为方向性信号，不是统计显著。
