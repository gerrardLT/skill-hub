# Retrospective Workflow — Purified v3 (复盘域提纯)

> 生成方式：retrospective-concise-v3 方法——单轮直出，质量底线 + 必要性过滤器。
> 场景假设：一个产品准备 launch 前的风险评估 + 已完成迭期的周期性复盘。

---

## 🔍 Pre-Mortem（发布前风险分析）

### Core Definition（核心定义原文保留）

**A pre-mortem is a structured risk-identification exercise that forces teams to think critically about what could go wrong before launch, when there's still time to act.** By assuming failure, we surface hidden concerns and separate legitimate threats from overblown worries.

---

### Step-by-Step Process（四步流程）

#### 1. Gather PRD → Understand Context
Read product/plan file thoroughly. Understand target market, key assumptions, timeline. Research competitive landscape if relevant.

#### 2. Think Backwards（逆向思维核心）
- Imagine product launches in X days
- Now imagine it fails—customers don't adopt, revenue misses, reputation takes hit
- What went wrong?
- What did we miss or not execute well?
- What were we overconfident about?

#### 3. Categorize Risks（三分法强制）

**Tigers: Real problems you personally see that could derail the project**
- Based on evidence/past experience/clear logic
- Should keep you awake at night
- Require action

**Paper Tigers: Problems others might worry about, but you don't believe in them**
- Valid concerns on surface, but unlikely or overblown
- Not worth significant resource investment
- Worth documenting to align stakeholders

**Elephants: Something you're not sure is a problem, but team isn't discussing enough**
- Unspoken concerns or assumptions nobody is validating
- Could be real; you're unsure
- Deserve investigation before launch

#### 4. Classify Urgency（急迫性三级分类）

| Type | Definition | Example |
|------|------------|---------|
| **Launch-Blocking** | Must be solved before launch | Core feature broken, regulatory blocker, key customer dependency unmet |
| **Fast-Follow** | Must be solved within 30 days post-launch | Performance issues, secondary features incomplete |
| **Track** | Monitor post-launch; solve if becomes issue | Nice-to-have features, edge cases |

#### 5. Action Plans for Launch-Blocking Tigers（必须的四字段模板）

For EACH Launch-Blocking Tiger:
- **Risk**: Describe clearly
- **Mitigation**: Suggest concrete action
- **Owner**: Identify best person/function
- **Due Date**: Set decision/completion date

#### 6. Output Format（结构化 Markdown）

```markdown
## Pre-Mortem Analysis: [Product Name]

### Tigers (Real Risks)
[List each with category and mitigation plan]

### Paper Tigers (Overblown Concerns)
[List each, explain why not true risk]

### Elephants (Unspoken Worries)
[List each, recommend investigation approach]

### Action Plans for Launch-Blocking Tigers
[For each: Risk, Mitigation, Owner, Due Date]
```

#### 7. Save & Revisit

Save as markdown: `PreMortem-[product-name]-[date].md`. Revisit 2-3 weeks before launch to verify mitigations on track.

### Notes（三条原则）

1. Be honest and constructive—goal is to improve launch readiness, not assign blame
2. Default to "Tiger" if unsure; better to address risks early
3. Involve cross-functional perspectives (engineering/design/go-to-market) in analysis

---

## 🔄 Retro（周期性工程复盘）

### Trigger Gate（触发门控原文）

Use when asked to "weekly retro", "what did we ship", or "engineering retrospective". Proactively suggest at end of work week or sprint.

### Gbrain Context Queries（上下文查询核心保留）

Load prior context for comparison:
- Prior retros: `.context/retros/*.json` (limit 5, mtime_desc)
- Recent timeline: `~/.gstack/projects/{slug}/timeline.jsonl` (tail 30)
- Recent learnings: `~/.gstack/projects/{slug}/learnings.jsonl` (tail 10)

### Analysis Framework（六维分析框架）

1. **Commit History**: git log --oneline since last retro
2. **Work Patterns**: PR count, review turnaround, build success rate
3. **Code Quality Metrics**: test coverage trends, bug count, technical debt
4. **Per-Person Breakdown**: contributions with praise and growth areas
5. **Trend Tracking**: compare against prior retros, identify recurring patterns
6. **Output Summary**: executive summary, detailed breakdown, top 3 celebrate, top 3 improve, actionable recommendations

### Key Metrics（六项核心指标）

| Metric | Description | Ideal Trend |
|--------|-------------|-------------|
| Commit Velocity | Commits per person | Stable or increasing |
| PR Turnaround Time | Draft to merge avg | Decreasing |
| Test Coverage | % code covered by tests | Increasing |
| Bug Count | New bugs per iteration | Decreasing |
| Technical Debt | Estimated hours to fix | Decreasing |
| Team Satisfaction | Self-reported morale (1-5) | Stable or increasing |

### Common Patterns（三种常用模式）

#### "What Went Well" Pattern
Focus on positive reinforcement:
1. Each member shares 1-2 wins
2. Group discusses common threads
3. Celebrate collective achievements

#### "Problem Tree" Pattern
Structure negative feedback constructively:
1. Root cause identification
2. Effect branches mapping
3. Solution pruning
4. Action item selection

#### "Start/Stop/Continue" Pattern
Simple actionable framework:
1. What should we start doing?
2. What should we stop doing?
3. What should we continue doing?

---

## ⚙️ Cross-Session Mechanisms

### Decision Log Handling

If active decisions listed:
- Treat as prior settled calls with their rationale
- Do NOT silently re-litigate them
- If reversing one, say so explicitly
- Use gstack-decision-search whenever question touches past decision

When making DURABLE decision (architecture/scope/tool/vendor choice/reversal):
- Log with gstack-decision-log (--supersede <id> for reversal)
- Reliable and local; gbrain not required

---

## 💡 Learnings Capture（关键洞察记录）

Log genuine discoveries saving time future sessions:
```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"retro","type":"pattern/pitfall/preference/architecture/tool/operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed/user-stated/inferred/cross-model","files":["path/to/file"]}'
```

Types: pattern/reusable approach; pitfall/what NOT to do; preference/user stated; architecture/structural decision; tool/library insight; operational/environment knowledge.

Sources: observed/code verified; user-stated/explicitly told; inferred/AI deduction; cross-model/Codex+Claude agree.

Confidence: 1-10 (observed=8-9, uncertain inference=4-5, explicit user=10).

Only log insights that save time future sessions.

---

## ✅ Completion Protocol（完成状态协议）

Report status using one of:
- DONE — completed with evidence
- DONE_WITH_CONCERNS — completed, list concerns
- BLOCKED — cannot proceed; state blocker and what was tried
- NEEDS_CONTEXT — missing info; state exactly what is needed

Escalate after 3 failed attempts, uncertain security-sensitive changes, or unverifiable scope. Format: STATUS, REASON, ATTEMPTED, RECOMMENDATION.

---

## 🔄 Operational Self-Improvement

Before completing, review session for durable learnings and log each one — this step ALWAYS runs, not conditional on something feeling noteworthy (#2402: 43 of 44 learnings came from explicit /learn because "if you discovered" read as optional). If review genuinely surfaces none, state "No durable learnings this session" in completion summary — explicit empty result, not skipped step.

```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"SKILL_NAME","type":"operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed"}'
```

Do not log obvious facts or one-time transient errors.

---

## 📡 Telemetry（遥测日志）

After workflow completion, log telemetry with ONE command:
```bash
~/.claude/skills/gstack/bin/gstack-skill-end --skill "retro" --outcome OUTCOME \
  --session-id "SESSION_ID" --tel-start "TEL_START" --used-browse yes/no \
  --error-message "" --failed-step "" 2>/dev/null || true
```

OUTCOME is success/error/abort/unknown; SESSION_ID and TEL_START are values preamble's skill-start output echoed. Replace before running. If command missing (stale install), skip telemetry — never blocks workflow.

---

## ✅ Quality Floor Checklist（自审表）

| Metric | Target | Status |
|--------|--------|--------|
| Premortem core definition | Original text present | ✅ "structured risk-identification...think critically about what could go wrong" |
| Tiger classification three-way | All 3 types with definitions | ✅ Tigers/Paper Tigers/Elephants each has criteria |
| Urgency labels (3 types) | Launch-Blocking/Fast-Follow/Track | ✅ All present with examples |
| Action Plan template | 4 fields complete | ✅ Risk/Mitigation/Owner/Due Date quadruple |
| Retro trigger gate | ≥1 keyword present | ✅ "weekly retro" "what did we ship" "engineering retrospective" |
| Gbrain context queries | timeline.jsonl + learnings.jsonl | ✅ Both mentioned |
| No count rules used | Zero "≥N items" format | ✅ Quality floor而非数量强制 |
| 6 core pattern checks | All pass | ✅ 6/6 metrics pass |

**Verdict:** **PASS** — 所有非妥协维度全部覆盖，压缩率预期 ~40% ✅

---

**对比结论：** Retrospective 域处于**方法论独立型**类别——pre-mortem 的五步结构本身紧凑，retro 的上下文查询机制可简化但保留核心逻辑。预期的 -40% 压缩率可实现，且关键方法论步骤（Tiger 三分法、急迫性分类、Action Plan 四字段）全部保持。

关键特征：相比 implementation 域的"-66%"（解释文字多），retrospective 作为**方法论文档**（本身已结构化）压缩收益居中；相比 shipping-delivery 的"-22%"（脚本命令密集），retrospective 的技术规范密度更低，有更多压缩空间。
