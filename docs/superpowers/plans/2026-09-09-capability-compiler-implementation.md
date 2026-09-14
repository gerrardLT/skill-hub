# Dev Loop 能力编译器实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将已下载的通用研发 Skills 完整拆解、证据化提纯为可独立调用和组合的原子能力插槽，并通过来源覆盖、能力对照、变异、组合和人工评审后接入 dev-loop。

**Architecture:** `skills/` 作为不可改的原始快照；`curation/` 保存资产底账、逐份解读、语义单元、聚类和取舍；`slots/` 保存通过验证的能力包；`recipes/` 保存组合关系；`evals/` 保存冻结案例和实际证据。Python 标准库工具只执行哈希、身份、引用、契约、覆盖和依赖等机械检查，语义取舍由带来源记录的审计和对照评测完成。

**Tech Stack:** Python 3.12 标准库、pytest、JSON/JSONL、Markdown、Qoder Skill/Agent、skill-creator eval viewer、现有 browser-use MCP。

**Authorization:** 用户已授权按阶段 1–8 顺序执行。未授权 Git commit、push、安装依赖、执行第三方 Skill 脚本、访问生产系统或使用真实凭据；本计划不包含这些动作。

---

## 目标文件结构

```text
skills/                                      # 只读原始快照
curation/
  policy.json                                # 范围、不变量、平台排除与硬失败
  inventory.json                             # 能力项、物理入口、套件、文件和来源底账
  gaps.json                                  # 未知版本、许可证、缺失引用与依赖缺口
  baseline.json                              # skills/ 文件哈希基线
  dossiers/<source-id>.md                    # 每份纳入 Skill 的完整解读
  units/<source-id>.jsonl                    # 带来源位置的语义单元
  clusters.json                              # 能力簇、关系和依赖
  decisions.jsonl                            # 保留/合并/改写/条件化/排除/延期
  coverage.json                              # 来源到插槽、插槽到来源的双向覆盖
slots/<slot-id>/
  SKILL.md                                   # 独立调用入口与方法
  contract.json                              # 输入输出、边界、权限、状态和 Gate
  provenance.json                            # 来源和取舍映射
  references/                                # 按需存在
  scripts/                                   # 按需存在
recipes/<recipe-id>.json                     # 插槽顺序、映射和 Gate
evals/
  cases/tuning/                              # 可用于迭代的案例
  cases/holdout/                             # 冻结留出案例
  cases/composition/                         # 组合和回流案例
  rubrics/                                   # 硬失败和质量判据
  runs/                                      # 实际运行、评分、时间与人工反馈
tools/curation/
  inventory.py                               # 生成资产、基线和缺口机械事实
  verify.py                                  # 校验原料不变、契约、覆盖、依赖和禁入项
tests/curation/
  test_inventory.py
  test_verify.py
```

---

## 阶段 1：冻结原始资产基线

### Task 1.1：定义范围与不变量

**Files:**
- Create: `curation/policy.json`
- Test: `tests/curation/test_verify.py`

- [ ] 写失败测试：要求 policy 明确 `skills/` 只读、PostHog 禁入、平台专用能力延期、硬失败不可被评分抵消。
- [ ] 运行 `python -m pytest tests/curation/test_verify.py -v`，确认因文件不存在失败。
- [ ] 创建最小 `curation/policy.json`，包含 `source_root`、`immutable`、`forbidden_providers`、`deferred_platform_families`、`hard_failures` 和 `status_values`。
- [ ] 重跑测试，确认 policy 结构通过。

### Task 1.2：生成确定性文件基线

**Files:**
- Create: `tools/curation/inventory.py`
- Create: `curation/baseline.json`
- Test: `tests/curation/test_inventory.py`

- [ ] 写失败测试：同一 `skills/` 输入两次生成结果相同；每个文件记录 POSIX 相对路径、字节数和 SHA-256；排除 `.git` 元数据但不排除 Skill 内容。
- [ ] 运行测试并确认生成器尚不存在。
- [ ] 实现 `inventory.py baseline --root skills --output curation/baseline.json`。
- [ ] 生成基线并记录 `file_count`、`total_bytes`、`tree_sha256`、逐文件哈希。
- [ ] 重跑测试，确认确定性和字段完整。

### Task 1.3：验证原料不变

**Files:**
- Create: `tools/curation/verify.py`
- Modify: `tests/curation/test_verify.py`

- [ ] 写失败测试：修改临时原料文件后，`verify.py source` 必须报告 changed；删除和新增分别报告 removed/added。
- [ ] 实现 `verify.py source --root skills --baseline curation/baseline.json`。
- [ ] 对真实 `skills/` 运行验证，预期 `added=0 changed=0 removed=0`。

**Gate 1：** 基线可重复生成；当前 `skills/` 与基线一致；范围和禁入规则可机器检查。

---

## 阶段 2：建立资产底账与缺口报告

### Task 2.1：统一资产身份

**Files:**
- Modify: `tools/curation/inventory.py`
- Create: `curation/inventory.json`
- Modify: `tests/curation/test_inventory.py`

- [ ] 写失败测试：分别统计 catalog entry、顶层目录、全树 Skill root、embedded Skill、套件和重复组，不混用数量。
- [ ] 解析 `SKILLS.md` 的 68 项清单并关联物理入口；gstack 根套件单独登记，不冒充原 68 项。
- [ ] 为每个 `SKILL.md` 记录 frontmatter name/description、父套件、顶层来源、文件集合和本地哈希。
- [ ] 生成 `curation/inventory.json`，保存稳定 ID 和别名。
- [ ] 验证清单项全部有 `resolved`、`duplicate-reference`、`deferred` 或 `gap` 状态，禁止静默丢失。

### Task 2.2：核实附件、引用和运行依赖

**Files:**
- Modify: `tools/curation/inventory.py`
- Create: `curation/gaps.json`
- Modify: `tests/curation/test_inventory.py`

- [ ] 写失败测试：检测不存在的相对路径引用、目录外共享引用、命令/CLI、MCP、网络、凭据和安装动作。
- [ ] 实现 Markdown 链接、反引号相对路径和常见命令的保守扫描；无法确定的内容进入人工复核，不自动判可运行。
- [ ] 为每份 Skill 记录许可证来源；无法核实上游 commit 和许可证时标记 unknown。
- [ ] 生成 `curation/gaps.json`，按 `blocking`、`review-required`、`informational` 分类。

### Task 2.3：隔离平台专用范围

**Files:**
- Modify: `curation/inventory.json`
- Modify: `curation/gaps.json`
- Modify: `tests/curation/test_verify.py`

- [ ] 为 Sentry、Datadog、Azure、Vercel、Cloudflare 及其他证据表明为平台专用的入口标记 `deferred-platform`。
- [ ] 平台判断以实际 Skill 内容和依赖为准，不只按仓库名称。
- [ ] 添加 PostHog 名称、路径和内容扫描，任何命中使 Gate 失败。
- [ ] 修正 `SKILLS.md` 中未经证据支持的“100% 离线即可运行”表述，改为文件落盘与审计状态分开报告。
- [ ] 重建覆盖全部资产的 `skills-lock.json` 或等价完整来源锁定清单，不能仅锁一个 Skill。

**Gate 2：** 资产身份、来源、附件、许可证和依赖均有明确状态；68 项能力逐项对账；平台范围和 PostHog 禁入可验证。

---

## 阶段 3：全量拆解 Skills 细节

### Task 3.1：冻结 dossier 与 unit 模板

**Files:**
- Create: `curation/dossier-template.md`
- Create: `curation/unit-schema.json`
- Modify: `tools/curation/verify.py`
- Modify: `tests/curation/test_verify.py`

- [ ] 写失败测试：dossier 缺任一必需章节时失败；unit 缺 source path、line range、type、meaning、boundary、dependency、candidate destination 或 status 时失败。
- [ ] 创建模板与 schema；语义单元类型限定为 method/rule/exception/template/example/tool-action/gate。
- [ ] 实现 dossier 和 JSONL unit 验证。

### Task 3.2：逐份完整阅读与拆解

**Files:**
- Create: `curation/dossiers/<source-id>.md`
- Create: `curation/units/<source-id>.jsonl`

- [ ] 按 inventory 中稳定 ID 顺序处理全部纳入范围入口。
- [ ] 读取入口 `SKILL.md`、所有可达 references/reference、templates、examples、sections 和脚本；仅记录脚本行为，不执行。
- [ ] 每份 dossier 写明问题、适用/非适用场景、角色、输入、输出、完整流程、分支、规则、例外、依赖、权限、副作用、Gate、疑点和独特价值。
- [ ] 将每个有实际作用的语义单元写入 JSONL，并给出真实来源文件和行范围。
- [ ] 记录读取覆盖；二进制、生成产物或无关仓库文件说明排除原因。
- [ ] 每完成一个来源，运行 dossier/unit 验证和 source baseline 验证。

### Task 3.3：全量阅读覆盖审计

**Files:**
- Modify: `curation/coverage.json`
- Modify: `tools/curation/verify.py`

- [ ] 对 inventory 中每个纳入入口核对 dossier、units 和附件阅读状态。
- [ ] 抽查语义单元与原文含义，发现机械切段、遗漏条件或错误行号时回退修正。
- [ ] 平台延期项只生成范围 dossier，不进行语义提纯。

**Gate 3：** 全部纳入来源均有完整 dossier、语义单元和阅读覆盖；每个单元可回到真实原文位置。

---

## 阶段 4：构建跨域能力地图

### Task 4.1：建立候选能力簇

**Files:**
- Create: `curation/clusters.json`
- Modify: `tools/curation/verify.py`
- Modify: `tests/curation/test_verify.py`

- [ ] 写失败测试：每个纳入 unit 必须属于一个能力簇或有明确 defer/exclude 决策。
- [ ] 按解决的问题聚类，不按来源仓库或旧六阶段机械分组。
- [ ] 记录 unit 间 `duplicate`、`complementary`、`conditional-variant`、`conflict`、`strong-dependency` 关系。
- [ ] 为每个簇定义候选职责、输入输出边界、上游和下游依赖。

### Task 4.2：冲突与强耦合审查

**Files:**
- Create: `curation/decisions.jsonl`

- [ ] 对每个冲突写出双方原文、适用条件、当前证据和待设计案例。
- [ ] 将“开发自检可修复”与“独立 QA 只报不修”等职责冲突拆成条件边界，而非互相覆盖。
- [ ] 强耦合方法保持为完整能力包或显式依赖，不为追求数量强拆。
- [ ] 所有 merge/rewrite/exclude 决策记录潜在损失和验证方式。

**Gate 4：** 所有纳入 unit 均有去向；未解决冲突显式可见；候选插槽边界无已知职责重叠。

---

## 阶段 5：完成“需求到验收标准”提纯试点

### Task 5.1：冻结评测标准与案例

**Files:**
- Create: `evals/rubrics/requirements-to-ac.json`
- Create: `evals/cases/tuning/requirements-to-ac.json`
- Create: `evals/cases/holdout/requirements-to-ac.json`
- Create: `evals/evals.json`

- [ ] 从 cluster 结果确定完整来源集合，不能只选方便的 PRD Skill。
- [ ] 先定义硬失败：编造事实、遗漏关键规则、不可测试 AC、丢失未知项、技术/设计越权、错误放行。
- [ ] 写正常、信息不足、边界、不适用、冲突和工具不可用案例。
- [ ] 标记 tuning 与 holdout；holdout 内容在候选冻结前不用于改写。

### Task 5.2：建立原始基线运行

**Files:**
- Create: `evals/runs/requirements-to-ac/baseline/...`

- [ ] 对每个案例选择实际适用的原始 Skill；保留原始入口，不合并提示词。
- [ ] 相同模型、输入、工具权限和预算下运行基线。
- [ ] 保存完整输出、工具调用证据、耗时和 token；原始 Skill 失败也如实保存。

### Task 5.3：编写候选原子插槽

**Files:**
- Create: `slots/problem-framing/{SKILL.md,contract.json,provenance.json}`
- Create: `slots/requirements-rules/{SKILL.md,contract.json,provenance.json}`
- Create: `slots/acceptance-criteria/{SKILL.md,contract.json,provenance.json}`
- Create: `slots/requirements-quality-gate/{SKILL.md,contract.json,provenance.json}`
- Modify: `curation/decisions.jsonl`
- Modify: `curation/coverage.json`

- [ ] 按 cluster 实际边界调整最终插槽列表；上述名称是首选而非强制数量。
- [ ] 每个 `SKILL.md` 保持单一职责并使用渐进披露；详细参考放 references。
- [ ] 每个 contract 定义输入、输出、边界、依赖、权限、状态、Gate 和禁止事项。
- [ ] provenance 双向关联来源 unit 和取舍决策。

### Task 5.4：候选、留出和变异评测

**Files:**
- Create: `evals/runs/requirements-to-ac/iteration-1/...`
- Create: `tests/mutations/requirements-to-ac/...`

- [ ] 同时运行候选和原始基线，避免时序/环境偏差。
- [ ] 对客观断言使用脚本评分；主观质量使用盲化评审。
- [ ] 在候选冻结后运行 holdout，多次运行波动型案例并报告均值与离散度。
- [ ] 删除“证据不足不得通过”、破坏 AC 字段、放宽 Gate，确认对应测试变红。
- [ ] 将输出交给下游测试用例生成/QA 检查，验证编号、假设和规则没有丢失。

### Task 5.5：生成 Viewer 并收集人工反馈

**Files:**
- Create: `evals/runs/requirements-to-ac/iteration-1/benchmark.json`
- Create: `evals/runs/requirements-to-ac/iteration-1/review.html`
- Create after review: `evals/runs/requirements-to-ac/iteration-1/feedback.json`

- [ ] 使用 skill-creator 的 aggregation 工具生成 benchmark。
- [ ] 使用 `eval-viewer/generate_review.py`，不得自造替代 Viewer。
- [ ] 发给用户前验证 HTTP/静态页面和真实浏览器内容。
- [ ] 根据反馈迭代，直到硬失败为零、留出和人工评审达标。

**Gate 5：** 提纯方法、契约、来源追踪、对照、留出、变异、交接和人工评审全部可用；试点结论不得外推为全量完成。

---

## 阶段 6：全量逐能力簇提纯

### Task 6.1：确定依赖顺序和批次

**Files:**
- Modify: `curation/clusters.json`

- [ ] 基于簇依赖图排序：基础约束与证据能力优先，组合/发布能力后置。
- [ ] 独立清点可并行；接口、冲突和最终取舍统一审查。
- [ ] 每批只包含能在同一 Gate 下完整验收的能力簇。

### Task 6.2：逐簇生成并验证插槽

**Files:**
- Create: `slots/<slot-id>/...`
- Modify: `curation/decisions.jsonl`
- Modify: `curation/coverage.json`
- Create: `evals/runs/<cluster-id>/...`

- [ ] 为每簇冻结 rubric、tuning、holdout 和 mutation 案例。
- [ ] 建立原始基线，生成候选插槽，完成来源覆盖。
- [ ] 运行相同环境的候选/基线对照、留出和变异测试。
- [ ] 生成 Viewer 并完成必要人工评审。
- [ ] 若退化，保留旧能力或标记未发布，不能靠总分掩盖。
- [ ] 每批完成后验证原始 `skills/` 未变化。

**Gate 6：** 所有通用能力 unit 均有决策；所有已发布插槽满足 Gate；未通过项明确保留为 deferred/unreleased。

---

## 阶段 7：构建配方并组合验证

### Task 7.1：定义 recipe schema

**Files:**
- Create: `recipes/schema.json`
- Modify: `tools/curation/verify.py`
- Modify: `tests/curation/test_verify.py`

- [ ] 写失败测试：缺 slot、循环依赖、输入无生产者、同产物并行写、未知 Gate 和权限升级必须失败。
- [ ] 实现最小 recipe schema 与验证。

### Task 7.2：建立场景配方

**Files:**
- Create: `recipes/write-prd.json`
- Create: `recipes/design-web-flow.json`
- Create: `recipes/build-feature-tdd.json`
- Create: `recipes/qa-only.json`
- Create: `recipes/ship-release.json`
- Create: `recipes/retro-to-requirements.json`
- Create: `recipes/full-dev-loop.json`

- [ ] 配方只声明插槽、顺序、映射、权限和 Gate，不复制方法正文。
- [ ] 单步配方与全闭环配方使用同一插槽契约。
- [ ] 平台专用能力不进入第一期配方；PostHog 扫描为零。

### Task 7.3：组合、替换与回流测试

**Files:**
- Create: `evals/cases/composition/*.json`
- Create: `evals/runs/composition/...`

- [ ] 验证上游字段、未知项、证据来源和编号完整传递。
- [ ] 注入 `needs-input`、`failed`、`blocked`，确认下游不执行。
- [ ] 替换同契约插槽，确认配方不依赖内部措辞。
- [ ] 修改上游产物，确认下游旧证据失效并重跑。
- [ ] 验证复盘输出成为下一轮需求输入，而不是仅生成 `retro.md`。
- [ ] 验证 QA 失败只记录和回退，不修改产品源码。

**Gate 7：** 所有配方通过结构、组合、替换、失败阻断和闭环回流测试。

---

## 阶段 8：接入 dev-loop 并终验

### Task 8.1：更新总控路由

**Files:**
- Modify: `dev-loop/skills/dev-loop/SKILL.md`
- Modify: `dev-loop/skills/dev-loop/references/routing.md`
- Modify: `dev-loop/skills/dev-loop/references/stages.md`
- Modify: `dev-loop/README.md`

- [ ] 将阶段级硬编码 Skill 路由替换为 recipe 选择和 slot contract 调用。
- [ ] 保留总控的路由、传递、Gate、状态职责，不复制 slot 方法。
- [ ] 明确单步、接力、全闭环、失败回流和证据失效规则。

### Task 8.2：同步本地插件副本

**Files:**
- Modify after source verification: `C:/Users/gerrard/.qoder/plugins/cache/local/dev-loop/1.0.0/...`
- Modify after source verification: `C:/Users/gerrard/.qoder/skills/dev-loop/...`

- [ ] 先比较源插件和两个安装副本，报告非预期差异。
- [ ] 仅同步已验证文件，不覆盖用户无关修改。
- [ ] 再次比较哈希，确认源与安装副本一致。

### Task 8.3：全量回归与完成审计

**Files:**
- Create: `curation/final-audit.json`
- Update: `SKILLS.md`
- Update: `skills-lock.json`

- [ ] 运行全部 pytest、source baseline、inventory、contract、coverage、recipe、PostHog、mutation 和 composition 验证。
- [ ] 构建 prompt-to-artifact 清单，将方案 1–8、每个 named file、Gate 和交付物映射到实际证据。
- [ ] 核对所有通用来源 unit：已发布、明确排除或未发布待解决；不得遗漏。
- [ ] 核对平台专用范围只登记未提纯；PostHog 全树零命中（历史说明和禁入策略允许单独标注，不进入能力资产）。
- [ ] 核对 `skills/` 与阶段 1 基线完全一致。
- [ ] 更新 `SKILLS.md`，严格区分文件落盘、来源核验、依赖状态、提纯状态和评测状态。
- [ ] 只有完成审计无缺口时才声明目标完成。

**Gate 8：** prompt-to-artifact 清单全部有证据；全套验证通过；所有要求无缺失、弱验证或未覆盖项。
