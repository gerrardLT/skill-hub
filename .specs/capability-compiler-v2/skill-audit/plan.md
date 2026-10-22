# V2 1.0.0 原子 Skills 逐项审核合同

## 目标

逐一审核 157 个已发布原子 Skills，判断其是否达到最佳效果，并给出可执行的改进建议。只审不改：`slots/v2/1.0.0/` 与 `recipes/v2/1.0.0/` 不作任何修改。

## 冻结对象

- Release tree：`116651adca2b907b3629e7e1954cddcd15cf0388e3401facaf2e8cb5c210d852`
- Skill catalog：`slots/v2/catalog.json`（157 项）
- 既有证据：Phase 9 grading report、Phase 10 semantic review、Phase 1–2 dossiers / fusion decisions

## 预审已见的系统性疑点（重点验证）

- H1 增益不明：314 个 holdout 中 159 个 baseline 亦通过（tie），仅 155 个 candidate-win。
- H2 评测不敏感：157 个 skill mutation 中 144 survived、14 需行为挑战、5 killed。
- H3 模板化：全部 Skill 恰 2 个 anti-trigger、2 个 hard gate、4 个 output、4–5 步；Trigger 段复述 Responsibility。
- H4 样板化：Status Mapping 等段落被 54–93 个 Skill 逐字共享。

## 评分维度（每项 0–3）

1. 边界与原子性：单一职责，不承载 pipeline。
2. 触发精度：trigger / anti-trigger 可区分相邻 Skill，无重叠歧义。
3. 程序可操作性：步骤具体、领域化，可直接执行。
4. 输出可验证性：输出项可被确定性检查或明确判定。
5. Gate 领域性：hard gate 针对本领域失败模式，而非通用样板。
6. 权限匹配：permission identity 与 mutation scope 与职责相称。
7. 来源保真：关键技法、阈值、反模式自来源保留，未被稀释。
8. 实测效力：holdout 增益与 mutation 敏感度。

## 裁决

- `keep`：已达最佳或仅有微小改进余地。
- `improve`：需修订，附 P1（影响效果）/ P2（影响质量）具体条目。
- `merge` / `split`：边界需重划，指明对象。
- `retire`：无独立价值。

裁决须引用具体证据（文件行、Phase 9 run、来源片段）；不得以模型自报为据。

## 阶段

- A 合同（本文件）
- B 确定性静态扫描：`tools/curation/v2_skill_audit_scan.py` → `curation/v2/skill-audit/static-scan.json`
- C 只读子代理按域语义审核；父级复核裁决 → `curation/v2/skill-audit/semantic/*.json`
- D 全量真实模型重评测：设计先经用户确认；结果写 `evals/runs/capability-compiler-v2/skill-audit/`
- E 综合：`curation/v2/skill-audit/ledger.json` + `docs/skill-audit-v2-1.0.0.md` + 审核 Gate

## 用户决定（2026-10-03）

- 范围：只审不改。
- C：reviewer 子代理两次 `Connection error.`（证据见 `curation/v2/skill-audit/failures/`），改由父级直接逐一审核 157 个 Skill，按域写 `curation/v2/skill-audit/semantic/<domain>.json`。
- D：执行质量 A/B。每个 Skill 2 个新任务，分别在有/无 Skill 条件下执行（`router9-qoder/cx/gpt-5.6-sol`），由 `router9-qoder/kr/claude-opus-5.5` 盲评成对优劣。

## 不变量

- 1.0.0 release assets、Phase 0–12 证据、原始 `skills/` 均不修改；E 阶段以 Phase 12 Gate 复证。
- 子代理只读；失败 runs 与被拒结论保留。
- 无 commit、push、PR、merge、deploy、provider 或 production 动作。
