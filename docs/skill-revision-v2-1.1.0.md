# Capability Compiler V2 1.1.0 修订报告

## 结论

**修订与评测已完成；当前候选不满足发布条件，不建议发布。** 1.0.0 仍是发布版本。没有 commit、push、PR、merge、deploy 或 1.1.0 发布动作。

候选包含 154 个 Skill、15 个 stage Recipes、5 个 composites、1 个 UI specialized Recipe、router 与 skill-index，共 485 个编译产物（另有 compile-manifest）。三个合并使 157 变为 154；frontend runtime 的拆分通过现有 defect-remediation 承接修复，不新增 Skill。

## 修订内容

- 154 个 Skill 改为具体 trigger signals；补齐全部 contract hard gates 和 forbidden actions；去除过期阶段措辞，修复悬空引用，重叠对互设 anti-trigger。
- 每域修订记录保存出处、补充技法、输出要求与发现处置。231 条单 Skill 发现、16 条跨 Skill 发现均有记录。记录 closed 不等于效果已证明；deferred-to-eval 仅代表交由本轮评测。
- 合并：ai-capability-architecture-and-autonomy 并入 ai-model-and-data-architecture；cross-domain-ui-preflight-checklists 并入 evidence-based-ui-review-and-release-gates；apm-onboarding-summary 并入 apm-instrumentation-verification。
- frontend-runtime-boundaries-and-dependency-safety 窄化为只读审计，修复交给 defect-remediation。
- 权限只窄化；reference-library-and-deferred-material 最终为 read-only，避免从 local-exec 增加 write 工具。27 个 protected steps 仍 disabled-pending-current-authorization。
- Recipes、依赖、router、contract hash 按候选重新编译。原始来源、已发布 1.0.0 与既有失败证据不改。

## 执行质量结果

执行模型：router9-qoder/cx/gpt-5.6-sol。出题、双顺序评判模型：router9-qoder/kr/claude-opus-5.5。每次调用使用 fresh 无工具 pi 进程、空 cwd 与环境白名单。

| 比较 | 题数 | 胜 | 平 | 负 |
|---|---:|---:|---:|---:|
| old：1.1.0 对 1.0.0 | 312 | 40 | 244 | 28 |
| fresh：1.1.0 对 1.0.0 | 306 | 31 | 243 | 32 |
| fresh：1.1.0 对无 Skill baseline | 306 | 108 | 150 | 48 |

old 执行 312/312、评判 624/624；fresh 执行 918/918、评判 1224/1224。独立完整性校验核对当前 prompt hash、执行输出 hash 与 judge 输入绑定后通过。fresh 只覆盖 153 个 Skill：browser-data-acquisition-runtime 出题反复 provider 中断，单列 incomplete，没有填平或算通过。

### 发布阈值

1. old 胜不低于负：通过，40 ≥ 28。
2. fresh 胜不低于负：失败，31 < 32。
3. 不得有 Skill 在两个题集均出现负：失败，共六个：deployment-trigger-execution、evidence-synthesis-and-opportunity-prioritization、kubernetes-application-deployment、purposeful-motion-and-animation-engineering、test-runtime-bootstrap、website-audit-remediation。
4. 新增编造标记人工复核：remote-pull-request-merge 的“Reported open”没有题面依据，确认为无依据断言。evidence-synthesis 的禁止 composite ranking 确实来自候选方法，人工不同意“凭空捏造方法”的理由，但其拒绝交付请求排名的回退仍成立；保留评判标记及异议，不抹去失败。

无事后放宽阈值。old 当前有 33 improved、95 unchanged、25 regressed、3 mixed；两题集每 Skill 仅两题、单一 judge，两顺序不同则记平，不构成统计显著的性能结论。35 个 Phase D negative/mixed 的逐项恢复结果见 report.json 的 threshold_check.recovery_of_phase_d_negative_or_mixed。

## routing 回归

原冻结题集 20/22。两条 runtime 题预期为 stage-15，但 1.0.0 和候选均选择同一个更窄的原子 Skill，且 would_execute=false。用户批准独立纠正题集，仅改这两条预期，全部 22 题重新运行，22/22 通过。原计划、失败、1.0.0 对照和纠正结果均保留。新 routing 通过不替代执行质量阈值。

## 失败、调优与成本披露

- round-1 试点不通过，保留全部证据；依据失分改文后，round-2 使用新 fresh 题试点。
- old 题曾用于修订，不能称为独立 holdout。round-1 fresh 用于调优后也不再称 holdout。
- 全量执行遭遇两批 429 用量限制；用户选择等待，模型和任务未换。失败及中断目录原样隔离，恢复后续跑。
- 六个 Skill 后续改文，其作废输出及相应 judge 已隔离并重新执行；最终仅使用匹配当前候选的证据。
- 总记录调用 3693 次：3436 completed、257 failed；记录 totalTokens 为 41,054,239。包括试点、探针、隔离失败与重跑。缺失 usage 的失败或部分调用不能假定免费；未提供美元估算。
- 累加调用耗时 88,254,051.485 ms，为并发调用之和，不是墙钟总时长。

## 交付与审批边界

候选：evals/candidates/capability-compiler-v2/revision-1.1.0/。

预览：curation/v2/revision-1.1.0/release-preview.json，状态 blocked-not-release-ready，仅列候选库存和可能目标路径。尚无转换为 released 1.1.0 的 exact postimage、catalog、lock 与 rollback 包，不能直接把 candidate 字节复制成正式版本。没有请求批准一个未过验收的发布。

下一步应修复六个跨题集回退与无依据状态断言，补齐出题失败项，再用新的未见题评测；这属于后续修订迭代，不在本报告中伪作完成。

## 证据索引

- curation/v2/revision-1.1.0/records/：11 域修订记录。
- curation/v2/revision-1.1.0/gate-report.json：结构与权限 Gate。
- curation/v2/revision-1.1.0/r5-final-evidence-summary.json：最终完整性、调用与 hash。
- curation/v2/revision-1.1.0/r5-final-threshold-disposition.json：不建议发布裁决及14条复核记录。
- curation/v2/revision-1.1.0/r5-manual-review.json：人工复核。
- evals/runs/capability-compiler-v2/revision-1.1.0-eval/round-2/report.json：逐 Skill、逐题、双顺序结果。
- evals/runs/capability-compiler-v2/revision-1.1.0-eval/routing-v2/report.json：批准后22题routing结果。
- .specs/capability-compiler-v2/revision-1.1.0/r5-design.md：运行前冻结阈值。

候选 compile-manifest SHA-256：f7a5a2d0eef9d9db53e98d0dcf874ae1ce02ba48f2973c0fefc53677f2e41c40。

最终 report SHA-256：e60ad6b2956995032fcec12f8b793181717442f7f25f1db31d134da255ef7ae6。
