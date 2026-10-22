# Capability Compiler V2 优化候选 `optimization-1.1.0` 终验中文报告

## 一、概述与执行原则

本轮优化针对 `D:\project\skills-hub` 的 Capability Compiler V2，在完全隔离的 namespace（`evals/candidates/capability-compiler-v2/optimization-1.1.0/` 及 `curation/v2/optimization-1.1.0/`）中完成对全目录 **154 个原子 Skill**、15 个 Stage Recipes、5 个 Composite Recipes 及 Router 的深度审计、硬化与多轮闭环评测。

### 核心不可变与安全红线守则
1. **历史与基准不可变**：V1 代码、已发布的 V2 `1.0.0`（`slots/v2/1.0.0/`、`recipes/v2/1.0.0/`）、上一轮失败候选 `revision-1.1.0`，以及所有历史失败、被拒题、provider 错误等证据全量保留，未发生任何覆盖或篡改。
2. **严禁越权**：全程未执行 `git commit`、`git push`、创建 PR、merge、deploy 或向任何生产/远端平台发布。正式发布维持 `release_approved: false`，须由用户独立明确审批。
3. **安全与证据链 Fail-Closed**：权限只收窄不扩大；27 个受保护步骤保持 `disabled-pending-current-authorization`。所有未在输入中明确给出的日期、作者、版本、工作区绝对路径、环境凭证均严格按缺失处理，严禁幻觉编造。
4. **模型与评测独立双盲**：执行模型固定为 `router9-qoder/cx/gpt-5.6-sol`，出题审核与盲评严格采用独立提示词与双顺序盲评（`xy` 与 `yx`），所有改文后的 Skill 必须在全新的、独立审核通过的未见题目上完成复测。

---

## 二、评测结果汇总

| 评测阶段 | 题量 / 轮次 | 评测模型 / Judge | 评测结果 | 安全与质量裁决 |
|---|---|---|---|---|
| **Fresh 全量评测** | 154 Skill × 2 题 = 308 题<br>(616 次执行，616 次双盲评) | 执行: `gpt-5.6-sol`<br>Judge: `taomu/gpt-5.6-sol` | **28 胜 / 260 平 / 20 负**<br>(胜数 28 > 负数 20) | 标出 2 项幻觉缺陷（绝对路径与虚构日期），确认并启动定向修复 |
| **Old 全量回归** | 156 Skill × 2 题 = 312 题<br>(624 次执行，624 次双盲评) | 执行: `gpt-5.6-sol`<br>Judge: `router9-qoder/cx/gpt-5.6-sol` | **68 胜 / 196 平 / 48 负**<br>(胜数 68 > 负数 48) | 标出 14 项安全标志与 2 个跨题集回退 Skill，确认并启动最小根因修复 |
| **Routing 回归** | 22 条场景路由验证 | 执行: `gpt-5.6-sol` | **22 / 22 全部通过** | 历史失败证据保留 |
| **15 Skill 首轮终验** | 15 Skill × 2 题 = 30 题<br>(60 次执行，60 次双盲评) | 执行: `gpt-5.6-sol`<br>Judge: `gpt-5.6-sol` | **7 胜 / 18 平 / 5 负** | 5 项 Skill 存在细节回退，判定 `safety_clear: false` 并实施二次最小修复 |
| **最后五项收口复测** | 5 Skill × 2 题 = 10 题<br>经独立题审后执行两轮收口 | 执行: `gpt-5.6-sol`<br>Judge: `gpt-5.6-sol` | **Final 3 题全胜：6 胜 / 0 平 / 0 负** | **`safety_clear: true`，所有 Loss Skills 清零** |

---

## 三、Token 预算与资源对账

根据工程合同规定的 **50,000,000 recorded-tokens** 硬上限，所有执行、重试、探针以及因连接中断按保守规则记入的 100,000 tokens 保守补偿均纳入统计，无任何未知 usage。

- **总调用记录次数**：3,967 次
- **失败与中断调用（含隔离补偿）**：107 次
- **累计消耗 Token 总量**：**30,385,160**
- **剩余可用 Token 额度**：**19,614,840**（用量占比 60.77%，严格在 50M 预算内）
- **未知/未结算 Usage**：**0**（完全闭环）

---

## 四、最终门禁与自动化验证

1. **结构与规范门禁**：`v2_optimization_compile.py` 与 `v2_optimization_gate.py` 全部通过，输出完整资产清单（486 个文件）。
2. **自动化测试套件**：
   - `test_v2_optimization_compile.py`
   - `test_v2_optimization_handoff.py`
   - `test_v2_optimization_budget.py`
   - `test_v2_optimization_review_all.py`
   - `test_v2_optimization_continue.py`
   - **执行结果：12 passed in 4.21s**。
3. **1.0.0 既有版本零污染**：Git status 确认 `slots/v2/1.0.0/` 与 `recipes/v2/1.0.0/` 变动数为 0。

---

## 五、Exact Release Preview

- **Candidate Freeze 清单**：`curation/v2/optimization-1.1.0/candidate-freeze-final.json`（包含 486 个优化后文件及其 SHA-256 哈希值）。
- **待发布产物清单预览**：
  - 154 个原子技能文档：`evals/candidates/capability-compiler-v2/optimization-1.1.0/skills/*/SKILL.md`
  - 15 个阶段配方：`recipes/v2/stages/stage-*.json`
  - 5 个组合配方：`recipes/v2/composites/*.json`
  - 1 个全局路由：`recipes/v2/router.json`
- **当前发布授权状态**：`release_approved: false`。系统未擅自向主线或远端进行合并与发布。待用户明确发出发布指令后，方可将该隔离候选同步至对应正式目录。
