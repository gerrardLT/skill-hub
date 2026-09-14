# Shipping Workflow — Purified v3 (交付域提纯)

> 生成方式：shipping-delivery-concise-v3 方法——单轮直出，质量底线 + 必要性过滤器。
> 场景假设：与 baseline 相同，功能分支准备发布到生产环境。

---

## 🎯 Ship 触发门控（六类关键词原文）

Use when asked to "ship", "deploy", "push to main", "create a PR", "merge and push", or "get it deployed". Proactively invoke when user says code is ready, asks about deploying, wants to push code up, or asks to create a PR. Do NOT push/PR directly — always use skill.

---

## 📦 Ship Work Flow（八步流程核心保留）

**Step 1: Detect & Merge Base**
git diff main...HEAD → identify affected pages/routes → detect running port (3000/4000/8080) → probe with curl

**Step 2: VERSION Bump + CHANGELOG Entry** ✅
bump semantic versioning (MAJOR.MINOR.PATCH), document in CHANGELOG with dates/authors

**Step 3: Review Diff** ✅
generate checklist for changed files, check security/performance/edge cases, request approvals

**Step 4: Commit & Push**
commit with descriptive message, push to remote (git push origin feature-branch)

**Step 5: Create PR**
open pull request with comprehensive description, link issues/tasks, wait for approvals + CI checks

**Step 6: Merge to Main**
squash/rebase merge based on workflow, delete branch after merge

**Step 7: Deploy**
trigger deployment pipeline (Vercel/AWS/GCP/etc.), monitor logs for errors

**Step 8: Canary Monitoring** ✅
post-deploy checks for console errors/performance/page failures vs baseline.json

**铁律：EVERY DEPLOY MUST BE MONITORED** — cannot skip step 8.

---

## 🔍 Pre-Mortem Risk Analysis

Before deploy, conduct pre-mortem:
1. Imagine launches/fails in X days → what went wrong?
2. Categorize as Tigers (real problems), Paper Tigers (overblown), Elephants (unspoken worries)
3. Classify urgency: Launch-Blocking, Fast-Follow (30 days post-launch), Track (monitor)
4. For each Launch-Blocking Tiger: describe risk, mitigation action, owner, due date
5. Save as markdown: `PreMortem-[product]-[date].md`
6. Revisit 2-3 weeks before launch to verify mitigations

**Gate: Launch-Blocking Tiger count > 0 → DEPLOY MUST WAIT.**

---

## 🖥️ Browser Setup（简化为检查清单）

### Aside First
```bash
command -v aside >/dev/null 2>&1 && echo "ASIDE_READY" || echo "NEEDS_ASIDE"
```

If NEEDS_ASIDE on macOS: "gstack works best with Aside browser (aside.com): download, open, sign in, re-run." If Linux/Windows/closed: use $B headless fallback.

### $B Fallback Command Map
| Action | $B Command |
|--------|------------|
| Go to page | $B goto <url> |
| Interactive snapshot | $B snapshot -i |
| Click element | $B click @e12 |
| Fill form | $B fill @eN "text" |
| Console errors | $B console --errors |
| Screenshot | $B screenshot <path> |
| Links | $B links |

Label output with evidence lines (URL=, CONSOLE_ERRORS=) so report reads identically.

---

## 📊 Monitored Issues（金丝雀三要素）

1. **Console Errors**: Any JS errors in browser console
2. **Performance Regressions**: Slower load times, longer TTI, higher LCP
3. **Page Failures**: 4xx/5xx responses, blank screens, broken layouts

### Periodic Screenshots
Capture every 5 minutes during critical period, then hourly. Compare against pre-deploy baseline using visual regression detection.

### Alerts on Anomalies (> thresholds)
- >3 console errors in 5 min → alert immediately via Slack/email
- >20% increase in page load time → alert
- Any 5xx server errors → alert

---

## ⚙️ Quick Workflow（压缩为 6 步）

**Phase 1:** Browser check (Aside READY or $B fallback)
**Phase 2:** Authenticate (user signs in; you never type passwords/OTPs)
**Phase 3:** Orient (landing page analysis: snapshot + console errors + initial.jpg)
**Phase 4:** Explore (systematic visit checklist: visual/interactive/forms/navigation/states/console/responsive)
**Phase 5:** Document (two tiers: interactive bugs→before-action screenshots+diff; static bugs→annotatedScreenshot)
**Phase 6:** Wrap Up (health score → Top 3 issues → console summary → severity table → metadata → baseline.json save)

Quick mode (--quick): only homepage + top 5 nav targets, check loads/errors/links. No detailed docs.

---

## 📈 Health Score Rubric（完整算法保留）

Compute each category score (0-100), then weighted average.

### Console (weight: 15%)
- 0 errors → 100
- 1-3 errors → 70
- 4-10 errors → 40
- 10+ errors → 10

### Links (weight: 10%)
- 0 broken → 100
- Each broken link → -15 (min 0)

### Per-Category Scoring (starts at 100, deduct per finding)
- Critical issue → -25
- High issue → -15
- Medium issue → -8
- Low issue → -3
Minimum 0 per category.

### Weights
| Category | Weight |
|----------|--------|
| Console | 15% |
| Links | 10% |
| Visual | 10% |
| Functional | 20% |
| UX | 15% |
| Performance | 10% |
| Content | 5% |
| Accessibility | 15% |

Final Score = Σ (category_score × weight)

---

## ⚠️ Critical Rules（全部保留）

1. Every issue needs at least one screenshot. No exceptions.
2. Verify before documenting. Retry once to confirm reproducible, not fluke.
3. Never include credentials. Write [REDACTED] if must mention.
4. Write incrementally. Append each issue to report. Don't batch.
5. Never read source code. Test as user, not developer.
6. Check console after every interaction. JS errors are still bugs.
7. Test like user. Realistic data. Complete workflows.
8. Depth over breadth. 5-10 well-documented > 20 vague descriptions.
9. Never delete output files. Screenshots/reports accumulate intentional.
10. Show screenshots to user. cp out of ASIDE_DIR and Read tool inline.
11. Mutating actions on non-local target need consent. One AskUserQuestion before first action.

---

## 💡 Learnings（压缩为要点）

Log genuine discoveries saving time future sessions:
```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"ship","type":"pattern/pitfall/preference/architecture/tool/operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed/user-stated/inferred/cross-model","files":["path/to/file"]}'
```

Types: pattern/reusable approach; pitfall/what NOT to do; preference/user stated; architecture/structural decision; tool/library insight; operational/environment knowledge.

Sources: observed/code verified; user-stated/explicitly told; inferred/AI deduction; cross-model/Codex+Claude agree.

Confidence: 1-10 (observed=8-9, uncertain inference=4-5, explicit user=10).

Only log insights that save time future sessions.

---

## 🔄 Telemetry（保留命令示例）

After workflow completion, log telemetry with ONE command:
```bash
~/.claude/skills/gstack/bin/gstack-skill-end --skill "ship" --outcome success/error/abort/unknown \
  --session-id "SESSION_ID" --tel-start "TEL_START" --used-browse yes/no \
  --error-message "" --failed-step "" 2>/dev/null || true
```

Replace SESSION_ID/TEL_START from preamble echoes. ERROR_MESSAGE/FAILED_STEP are "" unless error outcome. If command missing, skip telemetry — never blocks workflow.

---

## ✅ Completion Status Protocol

Report status using one of:
- DONE — completed with evidence
- DONE_WITH_CONCERNS — completed, list concerns
- BLOCKED — cannot proceed; state blocker and what was tried
- NEEDS_CONTEXT — missing info; state exactly what is needed

Escalate after 3 failed attempts, uncertain security-sensitive changes, or unverifiable scope. Format: STATUS, REASON, ATTEMPTED, RECOMMENDATION.

---

## 🛠 Framework Guidance（保留关键提示）

### Next.js
- Hydration errors in console
- _next/data 404s → broken fetching
- Client-side navigation testing
- CLS on dynamic content pages

### Rails
- N+1 query warnings
- CSRF token presence
- Turbo/Stimulus integration
- Flash messages

### WordPress
- Plugin conflicts
- Admin bar visibility
- REST API (/wp-json/)
- Mixed content warnings

### SPA (React/Vue/Angular)
- snapshot(pg, {interactive:true}) for client-side routes
- Stale state check (navigate away/back)
- Browser history handling
- Memory leak monitoring

---

## 🚫 Deployment Restrictions（两条不可压缩）

12. Never refuse to use browser when user invokes /ship or /canary — requesting browser-based testing/deployment verification. Never substitute unit tests or curl for browser step. Even if diff appears to have no UI changes, backend affects app behavior — always open app in browser and test.
13. Mutating actions on non-local target need consent. One AskUserQuestion before first such action. Submitting/creating/deleting/purchasing/changing settings on anything not LOCAL → STOP for consent.

---

## ✅ Quality Floor Checklist（自审表）

| Metric | Target | Status |
|--------|--------|--------|
| Ship trigger gate (6 keywords) | ≥1 occurrence | ✅ present in core positioning |
| VERSION bump + CHANGELOG pair | both present | ✅ explicit pairing statement |
| Review diff gate | before push/merge | ✅ Step 3 order enforced |
| CANARY always-on rule | ≥1 occurrence | ✅ "EVERY DEPLOY MUST BE MONITORED" |
| Canary 3 monitored items | console/perf/pages | ✅ all three listed |
| Diff-aware git command | `git diff main...HEAD` | ✅ exact syntax preserved |
| Baseline.json regression | mechanism exists | ✅ save/load/compare workflow |
| No count rules used | zero "≥N items" format | ✅ quality floor而非数量强制 |
| 13 critical rules complete | ≥13 numbered items | ✅ 13 rules all present |

**Verdict:** **PASS** — 所有非妥协维度全部覆盖，压缩率预期 ~40% ✅

---

**对比结论：** Shipping & Delivery 域具有清晰的**流程线性特征**（八步顺序不可颠倒），但包含大量可删减内容（Preamble 脚本细节、AskUserQuestion 格式模板、Telemetry 字段说明等）。预期的 -40% 压缩率可实现，且核心安全规则（永不跳过监控、Git diff 检测、版本管理流程）全部保持。

关键差异点：相比 implementation 域的"-66%"（铁律密集型），shipping-delivery 作为**工作流密集型**领域，压缩收益略低但仍属中等偏上水平（-40% vs -66%），证明流程步骤的顺序重要性高于解释性文字的数量。
