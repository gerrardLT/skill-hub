# V2 1.1.0 修订合同

## 输入

- 审核结论：`curation/v2/skill-audit/ledger.json`（157 个 Skill，P1 92 条、P2 139 条，147 个有发现）
- 执行 A/B 失分理由：`curation/v2/revision-1.1.0/phase-d-loss-reasons.json`
- 基线：已发布 1.0.0（release tree `116651ad…d852`），只读

## 用户决定（2026-10-04）

- 范围：全部 147 个有发现的 Skill；其余 10 个只做共性修复。
- 结构：执行 3 个合并、1 个拆分。
- 评测：D 阶段旧题 + 新出保留题，1.1.0 对 1.0.0 正面对比。
- 作者：父级直接逐个修订。

## 结构变更

| 变更 | 处理 | 影响 |
|---|---|---|
| `ai-capability-architecture-and-autonomy` → `ai-model-and-data-architecture` | 能力分类与非 AI 兜底并入目标 step 1 | stage 01/03/05/06 步骤与依赖记录改指向 |
| `cross-domain-ui-preflight-checklists` → `evidence-based-ui-review-and-release-gates` | 作为 preflight 模式并入，带入规范检查项 | stage 05、UI 专用 Recipe 去掉 preflight 步骤，accessibility 直连 review-evidence |
| `apm-onboarding-summary` → `apm-instrumentation-verification` | 多服务覆盖矩阵成为其输出 | stage 12 |
| `frontend-runtime-boundaries-and-dependency-safety` 拆分 | 改为只读审计；修复交给现有 `defect-remediation` | 不新增 Skill；1.1.0 共 154 个 |

## 修订方式

- 每个 Skill 一份修订记录 `curation/v2/revision-1.1.0/skills/<id>.json`：触发信号、新增 anti-trigger、程序与默认阈值、输出 schema、契约变更，以及 `resolves`——逐条对应 ledger 中的每个发现（`fixed` 或 `declined` 附理由）。
- 编译器 `tools/curation/v2_revision_compile.py` 从 1.0.0 + 修订记录生成候选：`evals/candidates/capability-compiler-v2/revision-1.1.0/`。版本 `1.1.0-candidate`，状态 `evaluating`。
- 共性修复（全部 Skill）：
  1. Trigger 改为具体触发信号，不再照抄 Responsibility。
  2. SKILL.md 写出 contract 的全部 hard gates 与 forbidden actions。
  3. 去掉发布前措辞 "claim … released status"。
  4. 修正悬空引用。
  5. 高重叠 Skill 对互设 anti-trigger。
  6. 状态口径改为"能做多少做多少"：缺的部分标 needs-input，其余照常交付并标注假设。这条直接针对 A/B 中"本可完成却停下"的失分。
  7. 删减跨 Skill 逐字共享的样板句。

## 不变量

- 1.0.0 release、Phase 0–12 证据、审核证据、原始 `skills/` 不改。
- 修订不得放宽权限、Gate 或数据治理；"能做多少做多少"只作用于交付范围，不作用于授权。
- 失败与被拒的尝试全部保留。
- 无 commit、push、PR、merge、deploy、provider 写操作。1.1.0 发布需你单独审批。

## 评测（R5）

- 题目：D 阶段 312 题（旧）+ 每 Skill 2 道新出保留题（出题只看 1.1.0 契约）。
- 对比：同一题分别用 1.0.0 与 1.1.0 SKILL.md 作答（gpt-5.6-sol），claude-opus-5.5 双顺序盲评；被合并的 Skill 的题目，1.1.0 一侧使用合并目标。
- 先 5 个 Skill 试点，再全量。预计约 3,000 次调用、2,500–3,000 万 tokens。
