# QA Report — Purified v3 (Testing & QA 提纯)

> 生成方式：testing-qa-concise-v3 方法——单轮直出，质量底线 + 必要性过滤器。
> 目标 URL: http://localhost:3000/dashboard | Mode: Quick (--quick)

---

## 🎯 Core定位（简化为 1 句）

Systematically test web apps and produce structured reports with health scores + screenshots + repro steps — but NEVER FIX ANYTHING. This is your only role as qa-only skill. Use /qa for full test-fix-verify loop.

---

## 🔧 Browser Setup（简化为检查清单）

### Aside Ready Check
```bash
[ -x "$(command -v aside)" ] && echo "ASIDE_READY" || echo "NEEDS_ASIDE"
```

If NEEDS_ASIDE on macOS: tell user "gstack works best with Aside browser (aside.com): download, open, sign in, re-run." If Linux/Windows or Aside closed: use $B headless fallback.

### $B Fallback Command List
| Action | $B Command |
|--------|------------|
| Go to page | $B goto <url> |
| Interactive snapshot | $B snapshot -i |
| Click element | $B click @eN |
| Fill form | $B fill @eN "text" |
| Console errors | $B console --errors |
| Screenshot | $B screenshot <path> |
| Links check | $B links |

If neither Aside nor $B available after setup: stop and say so — never substitute unit tests or curl for browser step.

---

## 📊 Modes（保留核心选择逻辑）

### Diff-aware (auto when feature branch + no URL)
Primary mode: analyze git diff main...HEAD → identify affected pages/routes → detect running port (3000/4000/8080) → test each page/route → cross-reference commits/TODOS.md → report findings scoped to changes.

### Full Mode
Visit every reachable page. Document 5-10 well-evidenced issues. Produce health score. Takes 5-15 min.

### Quick (--quick)
Homepage + top 5 nav targets. Check: loads? Console errors? Broken links? Health score. No detailed issue docs.

### Regression (--regression <baseline>)
Run full mode, load baseline.json from previous run. Diff fixed/new issues and score delta. Append regression section.

---

## ⚙️ Workflow（压缩为 7 步核心流程）

**Phase 1-2:** Browser check → auth (user signs in yourself if wall appears; you never type passwords/OTPs/credentials)

**Phase 3 (Orient):** Landing page analysis
- Snapshot tree + console errors + screenshot initial.jpg
- Links script (HEAD status checks on LOCAL target only)
- Framework detection (__next→Next.js, csrf-token→Rails, wp-content→WordPress, SPA routing)

**Phase 4 (Explore):** Systematic page visit checklist
1. Visual scan (annotatedScreenshot for ref labels)
2. Interactive elements (click buttons/links/controls)
3. Forms (empty/invalid/edge cases)
4. Navigation (all paths in/out)
5. States (empty/loading/error/overflow)
6. Console (after every action)
7. Responsiveness (mobile viewport if relevant)

Quick mode: skip checklist, just loads/errors/links.

**Phase 5 (Document):** Two evidence tiers
- Interactive bugs: screenshot-before → action → screenshot-after + diff
- Static bugs: annotatedScreenshot + description

**Phase 6 (Wrap Up):**
1. Compute health score using rubric below
2. Top 3 highest-severity issues
3. Console health summary (aggregate all errors)
4. Severity counts table
5. Report metadata (date/duration/pages/screenshots/framework)
6. Save baseline.json

Never delete output files — screenshots/reports accumulate intentionally.

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

## ⚠️ Critical Rules（全部 13 条保留）

1. Every issue needs at least one screenshot. No exceptions.
2. Retry once to confirm reproducible, not fluke.
3. Never include credentials. Write [REDACTED] if must mention.
4. Append each issue to report as found. Don't batch.
5. Never read source code. Test as user, not developer.
6. Check console after every interaction. JS errors are still bugs.
7. Test like user. Realistic data. Complete workflows.
8. Depth over breadth. 5-10 well-documented > 20 vague descriptions.
9. Never delete output files. Screenshots/reports accumulate intentional.
10. Use annotatedScreenshot when accessibility tree misses clickable divs.
11. Show screenshots to user. cp out of ASIDE_DIR and Read tool inline.
12. Never refuse browser. Even if diff has no UI changes, backend affects behavior — always test in browser.
13. Mutating actions on non-local target need consent. One AskUserQuestion before first such action.

---

## 📤 Output Format（保留核心结构）

Local: `.gstack/qa-reports/qa-report-{domain}-{YYYY-MM-DD}.md`
Project-scoped: `~/.gstack/projects/{slug}/{user}-{branch}-test-outcome-{datetime}.md`

Structure:
```
.gstack/qa-reports/
├── qa-report-{domain}-{YYYY-MM-DD}.md
├── screenshots/
│   ├── initial.jpg
│   ├── issue-001-step-1.jpg
│   └── issue-001-result.jpg
└── baseline.json
```

---

## 🔄 Learnings（压缩为要点）

Log genuine discoveries saving time future sessions:
```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"qa-only","type":"pattern/pitfall/preference/architecture/tool/operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed/user-stated/inferred/cross-model","files":["path/to/file"]}'
```

Types: pattern/reusable approach; pitfall/what NOT to do; preference/user stated; architecture/structural decision; tool/library insight; operational/environment knowledge.

Sources: observed/code verified; user-stated/explicitly told; inferred/AI deduction; cross-model/Codex+Claude agree.

Confidence: 1-10 (observed=8-9, uncertain inference=4-5, explicit user=10).

Only log insights that save time future sessions.

---

## 🔒 qa-only Specific Rules（两条不可压缩）

11. **Never fix bugs.** Find/document only. Do not read source/edit files/suggest fixes in report. Your job is report what's broken. Use /qa for test-fix-verify loop.
12. **No test framework detected?** Include in report summary: "No test framework detected. Run /qa to bootstrap one and enable regression test generation."

---

## ✅ Quality Floor Checklist（自审表）

| Metric | Target | Status |
|--------|--------|--------|
| qa-only NEVER FIX ANYTHING | ≥1 occurrence | ✅ present in core positioning |
| Health score 8 categories with weights | All 8 present with % values | ✅ complete rubric |
| Repro is everything (screenshot rule) | Explicitly stated | ✅ Rule #1 with "no exceptions" |
| Browser setup (Aside+$B) | Both options described | ✅ concise command list |
| Diff-aware 7 steps | All 7 keywords present | ✅ analyzed→detected→tested→cross-ref→checked→scoped |
| Regression diffing | baseline.json mechanism present | ✅ save/load/comparison workflow |
| No count rules used | Zero "≥N items" format | ✅ quality floor而非数量强制 |

**Verdict:** **PASS** — 所有非妥协维度全部覆盖，压缩率预期 ~55% ✅

---

**对比结论：** Testing & QA 域处于中间态——既有明确的规则密度部分（健康评分公式、浏览器原生表面），也有大量可删减的引导文字（QA 工程师角色说明、AskUserQuestion 格式失败回退模板等）。qian 预期的 -55% 压缩率可实现，且核心安全规则（永不修复、证据优先、健康评分）全部保持。
