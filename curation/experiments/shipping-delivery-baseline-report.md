# Shipping Workflow — Baseline (ship + canary full)

> 生成方式：完整遵循 skills/ship/SKILL.md + skills/canary/SKILL.md 原文内容。
> 场景假设：一个已完成的功能分支准备发布到生产环境。

---

## 🎯 When to Invoke This Skill (ship)

Use when asked to "ship", "deploy", "push to main", "create a PR", "merge and push", or "get it deployed". Proactively invoke this skill (do NOT push/PR directly) when the user says code is ready, asks about deploying, wants to push code up, or asks to create a PR.

---

## 🔧 Preamble (run first)

```bash
_SS="$HOME/.claude/skills/gstack/bin/gstack-skill-start"
[ -x "$_SS" ] || _SS=".claude/skills/gstack/bin/gstack-skill-start"
"$_SS" --skill "ship" --model "claude" --parent-pid "$PPID" \
  || echo "SKILL_START: unavailable — stale install; run ./setup or /gstack-upgrade (preamble degraded, continue the user's task)"
```

Read the echoed `KEY: value` STATUS lines — they drive every preamble rule below. **Degraded mode:** if `SKILL_START_PROTO: 1` is missing from the output (script absent, stale install, or a different protocol number), apply safe defaults: treat `SESSION_KIND` as `interactive`, do NOT assume Conductor, skip onboarding/telemetry steps...

---

## 📦 Ship Workflow (八步流程)

### Step 1: Detect & Merge Base Branch
- Analyze branch diff: git diff main...HEAD --name-only → identify changed files
- Identify affected pages/routes from controllers/views/models/styles/APIs/static pages
- Check running app: probe common dev ports (curl -sI --max-time 3 http://localhost:3000; ... port 4000/8080)
- Open first URL that answers in Aside

### Step 2: VERSION Bump
- Increment version number following semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes
- Update package.json, Cargo.toml, etc. as applicable

### Step 3: Update CHANGELOG
- Document all changes since last release with dates and authors
- Use conventional commits format where available
- Include link to full changelog history

### Step 4: Review Diff
- Generate review checklist for all changed files
- Check for security issues, performance regressions, edge cases
- Request formal code reviews if team requires approvals

### Step 5: Commit & Push
- Create commit with descriptive message referencing PR/task numbers
- Push to remote repository (git push origin feature-branch)

### Step 6: Create PR
- Open pull request with comprehensive description
- Link to related issues/tasks
- Wait for approvals and CI checks to pass

### Step 7: Merge to Main
- Squash merge or rebase merge based on team workflow
- Delete feature branch after merge

### Step 8: Deploy
- Trigger deployment pipeline (Vercel/AWS/GCP/etc.)
- Monitor deployment logs for errors

---

## 🚀 Canary Monitoring (post-deploy)

Watch the live app for console errors, performance regressions, and page failures. Takes periodic screenshots, compares against pre-deploy baselines, and alerts on anomalies. Use when: "monitor deploy", "canary", "post-deploy check", "watch production", "verify deploy".

### Browser Setup (Aside First)

Check Aside availability before any browser step:
```bash
_T=""; command -v gtimeout >/dev/null 2>&1 && _T="gtimeout 30"
[ -z "$_T" ] && command -v timeout >/dev/null 2>&1 && _T="timeout 30"
if [ "${GSTACK_SKIP_ASIDE:-}" = "1" ] || ! command -v aside >/dev/null 2>&1; then
  echo "NEEDS_ASIDE"
elif $_T aside repl 'console.log("ASIDE_READY " + pwd)' 2>&1 | grep -q '^ASIDE_READY'; then
  echo "READY: aside $(aside --version 2>/dev/null)"
else
  echo "ASIDE_NOT_RUNNING"
fi
```

If NEEDS_ASIDE on macOS: "gstack works best with Aside browser (aside.com): download, open, sign in, re-run." If Linux/Windows or Aside closed: use $B headless fallback.

### $B Fallback Commands

Translate Aside scripts to $B commands:
| Aside Step | $B Command |
|---|---|
| openTab(url)/pg.goto(url) | $B goto <url> |
| snapshot(pg,{interactive:true}) | $B snapshot -i |
| pg.locator("e12").click() | $B click @e12 |
| pg.fill(sel,text) | $B fill @eN "text" |
| console errors | $B console --errors |
| screenshot | $B screenshot <path> |
| links | $B links |

Label output with evidence lines (URL=, CONSOLE_ERRORS=, DIFF_START/DIFF_END) so report reads identically.

### Monitored Issues Types

1. Console Errors: Any JS errors in browser console
2. Performance Regressions: Slower load times, longer TTI, higher LCP
3. Page Failures: 4xx/5xx responses, blank screens, broken layouts

### Periodic Screenshots

Capture screenshots at regular intervals (every 5 minutes during critical period, then hourly). Compare against pre-deploy baseline using visual regression detection.

### Alerts on Anomalies

If any monitored issue exceeds thresholds:
- >3 console errors in 5-minute window
- >20% increase in page load time
- Any 5xx server errors

Alert immediately via configured notification channel (Slack/email).

---

## 📊 Pre-Mortem Integration

Before deploy, conduct pre-mortem risk analysis:

1. Imagine product launches/fails in X days
2. Categorize risks as Tigers (real problems), Paper Tigers (overblown concerns), Elephants (unspoken worries)
3. Classify by urgency: Launch-Blocking, Fast-Follow (30 days post-launch), Track (monitor)
4. For each Launch-Blocking Tiger: describe risk, suggest mitigation action, identify owner, set due date
5. Save output as markdown document: `PreMortem-[product-name]-[date].md`
6. Revisit 2-3 weeks before launch to verify mitigations are on track

Launch-Blocking Tiger count > 0 means DEPLOY MUST WAIT until resolved.

---

## ⚙️ Detailed Workflow Steps

### Phase 1: Initialize
1. Confirm Aside READY or use $B fallback
2. Create output directory: mkdir -p ".gstack/qa-reports/screenshots"
3. Start timer for duration tracking

### Phase 2: Authenticate (if needed)
Aside is user's real browser, session already signed in wherever user is signed in. Never authenticate yourself — user does. If sign-in wall appears, tell user: "Sign in to <origin> in Aside yourself (open new tab), then tell me you're done." Then re-run. Never type passwords/OTPs/payment details/cookies/tokens/localStorage.

If 2FA/OTP required: User completes it in Aside window, then tells you to continue.

If CAPTCHA blocks you: Tell user: "Please complete CAPTCHA in Aside, then tell me to continue."

### Phase 3: Orient
Get map of application. One script reads landing page — console errors from load, interactive snapshot tree, visible text, screenshot:
```bash
aside repl '
const HOOK = `(() => { window.__gstackErrs = window.__gstackErrs || []; const oe = console.error; console.error = (...a) => { window.__gstackErrs.push(a.map(String).join(" ")); oe.apply(console, a); }; window.addEventListener("error", e => window.__gstackErrs.push("uncaught: " + e.message)); })();`;
const pg = await openTab("about:blank");
await pg._sendToTarget("Page.addScriptToEvaluateOnNewDocument", { source: HOOK });
await pg.goto("<target-url>");
const s = await snapshot(pg, { interactive: true });
console.log(s.tree);
console.log("CONSOLE_ERRORS=" + JSON.stringify(await pg.evaluate(() => window.__gstackErrs)));
await pg.screenshot({ path: "initial.jpg", type: "jpeg", quality: 60, fullPage: true });
console.log("ASIDE_DIR=" + pwd); await closeTab(pg); console.log("GSTACK_STEP_OK");
'
```

Detect framework (__next→Next.js, csrf-token→Rails, wp-content→WordPress, SPA client-side routing).

### Phase 4: Explore
Visit pages systematically. At each page:
1. Visual scan (annotatedScreenshot for ref labels)
2. Interactive elements (buttons/links/controls)
3. Forms (empty/invalid/edge cases)
4. Navigation (all paths)
5. States (empty/loading/error/overflow)
6. Console (after every interaction)
7. Responsiveness (mobile viewport)

Quick mode: only homepage + top 5 nav targets, check loads/errors/links.

### Phase 5: Document
Document each issue immediately — don't batch.

Two evidence tiers:

**Interactive bugs**: one script per flow:
1. Screenshot before action
2. Perform action
3. Screenshot showing result
4. Print snapshot diff
5. Write repro steps

**Static bugs**: annotatedScreenshot + description.

Write each issue to report using template from qa/templates/qa-report-template.md.

### Phase 6: Wrap Up
1. Compute health score using rubric below
2. Write "Top 3 Things to Fix"
3. Write console health summary
4. Update severity counts in table
5. Fill metadata (date/duration/pages/screenshots/framework)
6. Save baseline.json: {"date":"YYYY-MM-DD","url":"<target>","healthScore":N,"issues":[],"categoryScores":{}}

---

## 📈 Health Score Rubric (same as qa-only)

Compute each category score (0-100), then weighted average.

### Console (15%)
- 0 errors → 100
- 1-3 errors → 70
- 4-10 errors → 40
- 10+ errors → 10

### Links (10%)
- 0 broken → 100
- Each broken link → -15 (min 0)

### Per-Category Scoring (starts at 100, deduct per finding)
- Critical → -25
- High → -15
- Medium → -8
- Low → -3
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

## ⚠️ Important Rules

1. Repro is everything. Every issue needs at least one screenshot. No exceptions.
2. Verify before documenting. Retry once to confirm reproducible, not fluke.
3. Never include credentials. Write [REDACTED] if must mention.
4. Write incrementally. Append each issue to report. Don't batch.
5. Never read source code. Test as user, not developer.
6. Check console after every interaction. JS errors are still bugs.
7. Test like user. Realistic data. Complete workflows.
8. Depth over breadth. 5-10 well-documented > 20 vague descriptions.
9. Never delete output files. Screenshots/reports accumulate intentional.
10. Show screenshots to user. cp out of ASIDE_DIR and Read tool inline.
11. Mutating actions on non-local target need consent. One AskUserQuestion before first such action.

---

## 💡 Capture Learnings

Log genuine discoveries saving time future sessions:
```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{"skill":"ship/canary","type":"pattern/pitfall/preference/architecture/tool/operational","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"observed/user-stated/inferred/cross-model","files":["path/to/file"]}'
```

Types: pattern/reusable approach; pitfall/what NOT to do; preference/user stated; architecture/structural decision; tool/library insight; operational/environment knowledge.

Sources: observed/code verified; user-stated/explicitly told; inferred/AI deduction; cross-model/Codex+Claude agree.

Confidence: 1-10 (observed=8-9, uncertain inference=4-5, explicit user=10).

Only log insights that save time future sessions.

---

## 🔄 Telemetry (run last)

After workflow completion, log telemetry with ONE command:
```bash
~/.claude/skills/gstack/bin/gstack-skill-end --skill "ship" --outcome success/error/abort/unknown \
  --session-id "SESSION_ID" --tel-start "TEL_START" --used-browse yes/no \
  --error-message "ERROR_MESSAGE" --failed-step "FAILED_STEP" 2>/dev/null || true
```

OUTCOME is success/error/abort/unknown; SESSION_ID and TEL_START are values preamble's skill-start output echoed. Replace before running; substitute SESSION_ID/TEL_START from echoes. ERROR_MESSAGE/FAILED_STEP are "" unless outcome is error. If command missing (stale install), skip telemetry — never blocks workflow.

---

## ✅ Completion Status Protocol

When completing skill workflow, report status using one of:
- DONE — completed with evidence
- DONE_WITH_CONCERNS — completed, but list concerns
- BLOCKED — cannot proceed; state blocker and what was tried
- NEEDS_CONTEXT — missing info; state exactly what is needed

Escalate after 3 failed attempts, uncertain security-sensitive changes, or scope you cannot verify. Format: STATUS, REASON, ATTEMPTED, RECOMMENDATION.

---

## 🛠 Framework-Specific Guidance

### Next.js
- Check console for hydration errors
- Monitor _next/data requests — 404s indicate broken fetching
- Test client-side navigation (click links, don't just goto)
- Check for CLS on pages with dynamic content

### Rails
- Check N+1 query warnings (if development mode)
- Verify CSRF token presence in forms
- Test Turbo/Stimulus integration
- Check flash messages appearing/dismissing

### WordPress
- Plugin conflicts (JS errors from different plugins)
- Admin bar visibility for logged-in users
- REST API endpoints (/wp-json/)
- Mixed content warnings

### General SPA (React/Vue/Angular)
- snapshot(pg, {interactive:true}) for client-side routes
- Stale state check (navigate away/back — does data refresh?)
- Browser back/forward history handling
- Memory leak monitoring (extended use console)

---

## 🚫 Deployment Restrictions

Never refuse to use browser when user invokes /ship or /canary — they requesting browser-based testing/deployment verification. Never substitute unit tests or curl for browser step. Even if diff appears to have no UI changes, backend changes affect app behavior — always open app in browser and test.
