# Retrospective Workflow — Baseline (pre-mortem + retro full)

> 生成方式：完整遵循 skills/pre-mortem/SKILL.md + skills/retro/SKILL.md 原文内容。
> 场景假设：一个产品准备 launch 前的风险评估 + 已完成迭期的周期性复盘。

---

## 🔍 Pre-Mortem: Risk Analysis for Product Launch

### Purpose

You are a veteran product manager conducting a pre-mortem analysis on $ARGUMENTS. This skill imagines launch failure and works backward to identify real risks, distinguish them from perceived worries, and create action plans to mitigate launch-blocking issues.

### Context

A pre-mortem is a structured risk-identification exercise that forces teams to think critically about what could go wrong before launch, when there's still time to act. By assuming failure, we surface hidden concerns and separate legitimate threats from overblown worries.

### Instructions

#### Step 1: Gather the PRD

If the user provides a PRD or product plan file, read it thoroughly. Understand the product, target market, key assumptions, and timeline. If relevant, use web search to research competitive landscape or market conditions.

#### Step 2: Think Step by Step

- Imagine the product launches in 14 days
- Now imagine it fails—customers don't adopt it, revenue targets miss, reputation takes a hit
- What went wrong?
- What did we miss or not execute well?
- What were we overconfident about?

#### Step 3: Categorize Risks

Classify each potential failure as one of three types:

**Tigers: Real problems you personally see that could derail the project**
- Based on evidence, past experience, or clear logic
- Should keep you awake at night
- Require action

**Paper Tigers: Problems others might worry about, but you don't believe in them**
- Valid concerns on the surface, but unlikely or overblown
- Not worth significant resource investment
- Worth documenting to align stakeholders

**Elephants: Something you're not sure is a problem, but the team isn't discussing it enough**
- Unspoken concerns or assumptions nobody is validating
- Could be real; you're unsure
- Deserve investigation before launch

#### Step 4: Classify Tigers by Urgency

**Launch-Blocking: Must be solved before launch**
- Example: Core feature broken, regulatory blocker, key customer dependency unmet

**Fast-Follow: Must be solved within 30 days post-launch**
- Example: Performance issues, secondary features incomplete

**Track: Monitor post-launch; solve if it becomes an issue**
- Example: Nice-to-have features, edge cases

#### Step 5: Create Action Plans

For every Launch-Blocking Tiger:
- Describe the risk clearly
- Suggest a concrete mitigation action
- Identify the best owner (function/person)
- Set a decision/completion date

#### Step 6: Structure Output

Present the analysis as:

```markdown
## Pre-Mortem Analysis: [Product Name]

### Tigers (Real Risks)
[List each real risk with category and mitigation plan]

### Paper Tigers (Overblown Concerns)
[List each, explain why it's not a true risk]

### Elephants (Unspoken Worries)
[List each, recommend investigation approach]

### Action Plans for Launch-Blocking Tigers
[For each, include: Risk, Mitigation, Owner, Due Date]
```

#### Step 7: Save the Output

Save as a markdown document: `PreMortem-[product-name]-[date].md`

### Notes

- Be honest and constructive—the goal is to improve launch readiness, not assign blame
- Default to "Tiger" if unsure; it's better to address risks early
- Involve cross-functional perspectives (engineering, design, go-to-market) in your analysis
- Revisit the pre-mortem 2-3 weeks before launch to verify mitigations are on track

---

## 🔄 Retro: Weekly Engineering Retrospective

### When to Invoke This Skill

Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team-aware: breaks down per-person contributions with praise and growth areas. Use when asked to "weekly retro", "what did we ship", or "engineering retrospective". Proactively suggest at the end of a work week or sprint.

### Preamble (run first)

```bash
_SS="$HOME/.claude/skills/gstack/bin/gstack-skill-start"
[ -x "$_SS" ] || _SS=".claude/skills/gstack/bin/gstack-skill-start"
"$_SS" --skill "retro" --model "claude" --parent-pid "$PPID" \
  || echo "SKILL_START: unavailable — stale install; run ./setup or /gstack-upgrade (preamble degraded, continue the user's task)"
```

Read the echoed `KEY: value` STATUS lines — they drive every preamble rule below. **Degraded mode:** if `SKILL_START_PROTO: 1` is missing from the output (script absent, stale install, or a different protocol number), apply safe defaults: treat `SESSION_KIND` as `interactive`, do NOT assume Conductor, skip onboarding/telemetry steps...

### Gbrain Context Queries

Load relevant prior context for comparison:

```yaml
context_queries:
  - id: prior-retros
    kind: filesystem
    glob: ".context/retros/*.json"
    sort: mtime_desc
    limit: 5
    render_as: "## Prior retros for this project"
    
  - id: recent-timeline
    kind: filesystem
    glob: "~/.gstack/projects/{repo_slug}/timeline.jsonl"
    tail: 30
    render_as: "## Recent timeline events"
    
  - id: recent-learnings
    kind: filesystem
    glob: "~/.gstack/projects/{repo_slug}/learnings.jsonl"
    tail: 10
    render_as: "## Recent learnings"
```

### Workflow Steps

1. **Collect Data Sources**
   - Analyze commit history: git log --oneline --since="last retro"
   - Check work patterns: PR count, review turnaround time, build success rate
   - Review code quality metrics: test coverage trends, bug count, technical debt

2. **Team-Aware Breakdown**
   - Per-person contributions with praise and growth areas
   - Recognize top performers without creating jealousy
   - Surface systemic issues vs individual mistakes

3. **Trend Analysis**
   - Compare against prior retros (if exist)
   - Identify recurring patterns
   - Highlight improvements since last cycle

4. **Output Format**
   - Executive summary of key findings
   - Detailed breakdown by contributor
   - Top 3 things to celebrate
   - Top 3 things to improve next cycle
   - Actionable recommendations

### Key Metrics to Track

| Metric | Description | Ideal Trend |
|--------|-------------|-------------|
| Commit Velocity | Number of commits per person | Stable or increasing |
| PR Turnaround Time | Average time from draft to merge | Decreasing |
| Test Coverage | Percentage of code covered by tests | Increasing |
| Bug Count | New bugs introduced per iteration | Decreasing |
| Technical Debt | Estimated hours to fix known issues | Decreasing |
| Team Satisfaction | Self-reported morale score (1-5) | Stable or increasing |

### Common Retro Patterns

#### The "What Went Well" Pattern
Focuses on positive reinforcement:
1. Each team member shares 1-2 wins
2. Group discusses common threads
3. Celebrate collective achievements

#### The "Problem Tree" Pattern
Structures negative feedback constructively:
1. Root cause identification
2. Effect branches mapping
3. Solution pruning
4. Action item selection

#### The "Start/Stop/Continue" Pattern
Simple actionable framework:
1. What should we start doing?
2. What should we stop doing?
3. What should we continue doing?

---

## 📊 Cross-Session Decision Log

If active decisions listed:
- Treat them as prior settled calls with their rationale
- Do not silently re-litigate them
- If reversing one, say so explicitly
- Reach for gstack-decision-search whenever question touches past decision

When making DURABLE decision (architecture, scope, tool/vendor choice, or reversal):
- Log with gstack-decision-log (--supersede <id> for reversal)
- Reliable and local; gbrain not required

---

## 💡 Capture Learnings

If discovered non-obvious pattern, pitfall, or architectural insight during session, log it for future sessions:

```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"retro","type":"pattern/pitfall/preference/architecture/tool/operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed/user-stated/inferred/cross-model","files":["path/to/file"]}'
```

Types: pattern/reusable approach; pitfall/what NOT to do; preference/user stated; architecture/structural decision; tool/library insight; operational/environment knowledge.

Sources: observed/code verified; user-stated/explicitly told; inferred/AI deduction; cross-model/Codex+Claude agree.

Confidence: 1-10 (observed=8-9, uncertain inference=4-5, explicit user=10).

Only log genuine discoveries. Don't log obvious things. Don't log things user already knows. A good test: would this insight save time in a future session? If yes, log it.

---

## 🔧 Completion Status Protocol

When completing a skill workflow, report status using one of:
- DONE — completed with evidence
- DONE_WITH_CONCERNS — completed, but list concerns
- BLOCKED — cannot proceed; state blocker and what was tried
- NEEDS_CONTEXT — missing info; state exactly what is needed

Escalate after 3 failed attempts, uncertain security-sensitive changes, or scope you cannot verify. Format: STATUS, REASON, ATTEMPTED, RECOMMENDATION.

---

## 📈 Operational Self-Improvement

Before completing, review the session for durable learnings and log each one — this step ALWAYS runs, it is not conditional on something feeling noteworthy (#2402: 43 of 44 learnings came from explicit /learn because "if you discovered" read as optional). If the review genuinely surfaces none, state "No durable learnings this session" in your completion summary — an explicit empty result, not a skipped step.

```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"SKILL_NAME","type":"operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed"}'
```

Do not log obvious facts or one-time transient errors.

---

## 📡 Telemetry (run last)

After workflow completion, log telemetry with ONE command. OUTCOME is success/error/abort/unknown; SESSION_ID and TEL_START are the values the preamble's skill-start output echoed. It also drains the artifacts-sync queue (the former skill-end sync step — do not run gstack-brain-sync separately).

**PLAN MODE EXCEPTION — ALWAYS RUN:** This writes telemetry to ~/.gstack/analytics/, matching preamble analytics writes.

```bash
~/.claude/skills/gstack/bin/gstack-skill-end --skill "retro" --outcome OUTCOME \
  --session-id "SESSION_ID" --tel-start "TEL_START" --used-browse USED_BROWSE \
  --error-message "ERROR_MESSAGE" --failed-step "FAILED_STEP" 2>/dev/null || true
```

Replace OUTCOME and USED_BROWSE (yes/no) before running; substitute SESSION_ID/TEL_START from the skill-start echoes. ERROR_MESSAGE/FAILED_STEP are "" unless outcome is error. If the command is missing (stale install), skip telemetry — it never blocks the workflow.
