# 1.1.0 修订报告待填项

状态：报告骨架，非最终修订报告，非发布预览，非发布批准。

## 范围与结构

- 原始 Skill roots、1.0.0 released assets 和既有审计证据只读。
- 157 个原子 Skill 经三个合并变为 154 个。
- frontend-runtime-boundaries-and-dependency-safety 保持 ID，窄化为只读审计；修复归现有 defect-remediation，不新增 Skill。
- 231 条单 Skill 发现、16 条跨 Skill 发现各有处置记录；deferred-to-eval 只是待评测状态，不等同于已证明有效。
- 候选目录：evals/candidates/capability-compiler-v2/revision-1.1.0/。

## 必须披露的评测过程

1. 第一轮试点未过阈值；保留 round-1-finding.json 和完整 runs。
2. 修订候选后，第二轮试点通过；第一轮 fresh 题已用于调优，不再称为 holdout。
3. old 题曾用于 Phase D 失分分析及候选修订，只作回归比较，不作为独立 holdout。
4. fresh 全量执行遭遇 provider 429；失败及中断目录保留于 infra-failed。恢复后仍使用原模型、原任务、原参数续跑。
5. 六个 Skill 在 old 全量之后进一步改文，其旧输出及依赖评判已隔离；最终报告必须只使用匹配当前候选 prompt hash 的证据。
6. browser-data-acquisition-runtime 无可用新题，单列 incomplete，不填平、不算通过。
7. routing 原冻结题集 20/22。1.0.0 对照在两条失败题上与候选一致；用户批准独立纠正题集，重新运行全部 22 题，得到 22/22。两套结果并列披露，原失败不覆写。

## 最终验收仍需填入

- 冻结候选 compile-manifest、记录、设计和 task-set 的 SHA-256。
- R4 Gate、测试实际命令、退出码、耗时与结果。
- old 和 fresh：预期/有效 exec 与 judge 数量、所有输入输出 hash 校验。
- 两题集胜/平/负、顺序一致性、逐 Skill 回退、新增 overreach/fabrication 人工复核。
- Phase D negative/mixed 35 个 Skill 的恢复明细。
- token 与调用成本，包括失败、探针、试点、重试；不能仅统计成功 run。
- 1.0.0 Phase 12 Gate 复核与未变 hash。
- incomplete 和未满足阈值的发布影响。

## 发布预览边界

- 只产出预览，不写 slots/v2/1.1.0 或 recipes/v2/1.1.0。
- 最终发布另需用户对 exact preview 单独批准。
- commit、push、PR、merge、deploy、provider mutation、browser login、credential action 和生产数据访问均未授权。
- 27 个 protected steps 必须仍为 disabled-pending-current-authorization。
