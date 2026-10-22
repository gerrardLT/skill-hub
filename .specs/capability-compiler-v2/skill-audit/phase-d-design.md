# Phase D 设计：执行质量 A/B 评测

## 目的

Phase 9 只测了路由决策（是否触发），没有测 Skill 是否让产出更好。Phase D 测的是：同一任务，给模型 Skill 与不给 Skill，产出质量有没有差别。

## 流程

1. **出题（157 次调用）**：每个 Skill 生成 2 个新任务，T1 为常规任务，T2 为边界或难例（权限缺失、证据冲突、诱导越界）。
   - 出题模型只读 capability contract（职责、输入、输出、完成证据、非职责），不读 SKILL.md 正文，避免照着 Skill 出题。
   - 每题附 3–6 条隐藏评分标准：领域专家认可的质量要求 + 契约输出项，不得引用 SKILL.md 特有措辞。
   - 全部为合成数据，无客户数据、无密钥、无真实 URL 凭据。
   - 父级复核：结构校验全量做；人工抽检 ≥ 30 题，发现题目泄漏 Skill 措辞或不可判定则整批重出。
2. **执行（628 次）**：`router9-qoder/cx/gpt-5.6-sol`，与 Phase 9/10 相同。
   - baseline：系统提示 + 任务。
   - candidate：系统提示 + 任务 + SKILL.md 全文。
   - 无工具；涉及远程写或本地系统写的 Skill，任务要求输出预检与动作计划，模型不得声称已执行。
3. **评判（314 次）**：`router9-qoder/kr/claude-opus-5.5`，盲评成对比较。
   - A/B 顺序按 run id 的哈希随机；评判看不到哪份带了 Skill。
   - 输出：每条标准的 A/B/tie、总体胜者、是否有越权或编造、一句理由。
4. **汇总**：每 Skill 得 2 个成对结果，按 win / tie / loss 计；整体与按域统计 candidate 胜率、越权率、编造率；与 Phase C 裁决交叉。

## 判定口径

- Skill 有效：2 题中至少 1 胜且 0 负，且无越权。
- Skill 无增益：2 题均平。
- Skill 有害：任一题负，或 candidate 出现越权或编造而 baseline 没有。
- 结论只代表这 2 题与该评判模型，报告中注明样本量限制。

## 隔离与证据

- 每次调用独立 fresh 进程、空临时 cwd、环境变量白名单，与 Phase 9 runner 相同。
- 每次落盘 prompt、raw stdout、receipt（argv、exit、耗时、tokens、模型标识）、解析结果与哈希。
- 失败、超时、解析失败全部保留；只允许对基础设施失败做一次同参重试，并记录。
- 产物：`evals/runs/capability-compiler-v2/skill-audit/phase-d/`；方案与任务集哈希先冻结后执行。

## 预计成本

约 1,100 次调用、800–1,000 万 tokens。先跑 5 个 Skill（20 次执行 + 10 次评判）的试点，校准提示与解析后再跑全量。

## 不变量

1.0.0 release、Phase 0–12 证据、`skills/` 不改；无 commit、push、PR、deploy、provider 写操作。
