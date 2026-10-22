# Capability Compiler V2 — Phase 1B Semantic Audit

**Repository:** `D:/project/skills-hub`  
**Assigned roots:** 10  
**Authority used:** read-only; no files changed, no commands executed, no network or remote Git used.

## Audit status and blocker

All ten assigned `SKILL.md` files were read completely in bounded chunks. A full support-file completion claim is **blocked for `qa-only`** because its workflow requires two shared semantic files that do not exist at the referenced repository paths:

- `skills/qa/templates/qa-report-template.md`
- `skills/qa/references/issue-taxonomy.md`

Both read probes returned `ENOENT`, and `skills/qa/` itself is absent. The references are behaviorally material: one defines the report template and the other the per-page issue taxonomy (`skills/qa-only/SKILL.md:686-755`). Thus the `qa-only` dossier below is source-grounded in its complete `SKILL.md`, but its promised report schema/taxonomy cannot be independently verified.

The Phase 1 contract requires root dossiers to cover triggers, responsibility, I/O, workflow, dependencies, permissions, strengths, weaknesses, failure modes, and parent/child relations; supporting files must be classified rather than excluded by extension alone (`.specs/capability-compiler-v2/phase-1/phase-plan.md:25-46`). It also forbids passing Phase 1 when a root or file remains unreviewed or unclassified (`.specs/capability-compiler-v2/phase-1/phase-plan.md:75-76`).

---

## 1. `audit-website`

### Exact root / skill path

- Root: `skills/audit-website/`
- Skill: `skills/audit-website/SKILL.md`

### Trigger and non-trigger

- **Trigger:** website or webapp health discovery, SEO/performance/security/content/accessibility auditing, or an audit-to-fix loop. It explicitly covers audits intended to culminate in source fixes (`skills/audit-website/SKILL.md:1-16`).
- **Non-trigger:** general squirrelscan installation, login, publishing, MCP, or generic CLI usage; those belong to the companion `squirrelscan` skill (`skills/audit-website/SKILL.md:13-16`). It is also not a generic browser exploration or test-authoring skill.

### Responsibility and non-responsibility

- **Responsibility:** run squirrelscan, interpret its LLM report, map findings to source, seek approval, fix in batches, rebuild, re-audit, and prove improvement (`skills/audit-website/SKILL.md:43-57`).
- **Non-responsibility:** guessing a URL, guessing broken-link intent, or silently making judgment calls. Missing URLs must be requested, and ambiguous link decisions go to the user (`skills/audit-website/SKILL.md:27-38`, `skills/audit-website/SKILL.md:60-73`).

### Inputs

- Target URL.
- Local source tree corresponding to the audited site.
- Optional bot-auth headers, audit ID, baseline audit ID, crawl mode, page cap, or score target.
- User approval for proposed source edits (`skills/audit-website/SKILL.md:25-38`, `skills/audit-website/SKILL.md:43-50`).

### Outputs

- Initial score/grade and prioritized findings.
- Approved code/content fixes.
- Build/check results.
- Refreshed audit and before/after score comparison.
- Optional published report through the companion skill.
- The report data model includes site metadata, score/category scores, issue rules, affected pages/items, and diff fingerprints (`skills/audit-website/SKILL.md:75-87`; `skills/audit-website/references/OUTPUT-FORMAT.md:13-111`).

### Core workflow

1. Verify `squirrel`.
2. Run a quick `--format llm` audit.
3. Present score, grade, and high-severity findings.
4. Propose fixable items and obtain approval.
5. Map findings to templates/components/content.
6. Fix in batches and run existing project checks.
7. Re-audit with `--refresh`.
8. Repeat until target or human judgment boundary.
9. Sign off using a full crawl and report the delta (`skills/audit-website/SKILL.md:20-38`, `skills/audit-website/SKILL.md:43-73`).

### Branches

- Crawl depth: `quick`, `surface`, or `full`.
- Cache reuse through `squirrel report <audit-id>`.
- Interrupted crawl continuation with `--resume`.
- Cloudflare/Shopify blocking handled by Web Bot Auth headers.
- Baseline comparison through `--diff` or `--regression-since`.
- Broken links and judgment calls are escalated rather than guessed (`skills/audit-website/SKILL.md:25-41`, `skills/audit-website/SKILL.md:60-79`).

### Rules, gates, and stop conditions

- Must use `--format llm`.
- Must confirm proposed fixes before editing.
- Must verify build/checks after each fix batch.
- Errors precede high-rank warnings.
- Final sign-off requires a `-C full` crawl.
- Completion requires all errors fixed, warnings fixed or explicitly deferred to human review, a confirming re-audit, and before/after disclosure (`skills/audit-website/SKILL.md:27-38`, `skills/audit-website/SKILL.md:43-73`, `skills/audit-website/SKILL.md:81-87`).

### Tools and dependencies

- External `squirrel` CLI in `PATH`.
- Network access to the target and squirrelscan rule documentation.
- Read/Edit/Grep/Glob and project build/test tooling.
- Companion `squirrelscan` skill for setup/publishing.
- Optional secret headers for Web Bot Auth (`skills/audit-website/SKILL.md:7-16`, `skills/audit-website/SKILL.md:20-41`).

### Permissions and side effects

- Crawls a live site and may transmit configured headers.
- Reads and edits local source after approval.
- Runs project build/check commands.
- May refresh cached audits and optionally publish a report.
- Header values are secrets and are stated to be redacted from output (`skills/audit-website/SKILL.md:35-41`, `skills/audit-website/SKILL.md:43-57`).

### Strongest unique methods

- Progressive crawl depth: cheap topology discovery before full verification.
- Rule-level audit output optimized for agent context.
- Deterministic baseline diff fingerprints.
- Explicit source-mapping and iterative score improvement, rather than report-only scanning.
- Clear score targets scaled by starting health (`skills/audit-website/SKILL.md:25-38`, `skills/audit-website/SKILL.md:43-73`; `skills/audit-website/references/OUTPUT-FORMAT.md:74-111`).

### Weaknesses and failure modes

- Heavily dependent on a proprietary external CLI and live network conditions.
- “Fix until score target” can incentivize score optimization over product intent; broken-link handling partly mitigates this.
- A quick crawl samples only part of the site, so completion without the required full crawl would be false confidence.
- The rule-output reference describes XML escaping and compact structure but does not define trust handling for hostile audited page content (`skills/audit-website/references/OUTPUT-FORMAT.md:185-222`).

### Overlap, duplicate, and dependency candidates

- **Complement:** `qa-only` performs user-flow browser QA; `audit-website` performs crawler/rule-based site analysis and can edit code.
- **Dependency candidate:** `playwright` can reproduce browser flows for findings squirrelscan cannot validate interactively.
- **Complement:** `canary` verifies post-deploy deltas, while this root discovers broad site-health defects.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `audit-website/SKILL.md` | semantic-read | Complete root contract and workflow. |
| `audit-website/references/OUTPUT-FORMAT.md` | semantic-read | Defines the LLM audit/diff payload consumed by the workflow. |
| `audit-website/README.md` | semantic-read | Product/capability summary; confirms rule categories and report modes. |
| `audit-website/agents/openai.yaml` | semantic-read | UI registration metadata only; no workflow behavior. |
| `audit-website/assets/icon-small.svg` | excluded | Decorative vector icon; inspected and contains only pixel-art rectangles. |
| `audit-website/assets/icon-large.png` | excluded | Binary UI asset, already classified inventory-only in coverage data; no semantic behavior. |

---

## 2. `canary`

### Exact root / skill path

- Root: `skills/canary/`
- Skill: `skills/canary/SKILL.md`

### Trigger and non-trigger

- **Trigger:** “monitor deploy,” “canary,” “post-deploy check,” “watch production,” or “verify deploy” (`skills/canary/SKILL.md:1-17`).
- **Non-trigger:** pre-deploy release preparation, code fixing, long-term observability, or incident command. It is explicitly read-only unless the user separately asks to investigate/fix (`skills/canary/SKILL.md:729-735`).

### Responsibility and non-responsibility

- **Responsibility:** establish or load a baseline, discover pages, repeatedly observe live pages, compare errors/performance/page health, collect screenshots, alert, and write a health report.
- **Non-responsibility:** modifying application code, deploying, or declaring absolute quality from industry thresholds. It assesses changes against a baseline (`skills/canary/SKILL.md:540-735`).

### Inputs

- URL.
- Optional duration from 1–30 minutes.
- Optional `--baseline`, `--pages`, and `--quick`.
- Existing `.gstack/canary-reports/baseline.json`, if any (`skills/canary/SKILL.md:520-537`).

### Outputs

- Baseline screenshots and manifest.
- Repeated screenshots.
- Alerts containing timestamp, page, severity, finding, evidence, baseline, and current value.
- Markdown and JSON canary reports.
- Review-dashboard JSONL entry.
- Optional updated baseline (`skills/canary/SKILL.md:540-735`).

### Core workflow

1. Initialize report directories.
2. In baseline mode, collect screenshot, console errors, navigation timing, and text, then stop.
3. Otherwise discover same-origin pages or use supplied pages.
4. Capture a reference if no baseline exists.
5. Poll each page every 60 seconds.
6. Compare to baseline and require persistence across two checks.
7. Alert for critical/high anomalies.
8. Produce health report.
9. Optionally promote healthy current results to the new baseline (`skills/canary/SKILL.md:540-735`).

### Branches

- Baseline-only mode.
- User-provided versus auto-discovered page set.
- Existing baseline versus immediate pre-monitor snapshot.
- Quick single pass versus timed loop.
- Alert decision: investigate, continue, rollback, or dismiss.
- Healthy completion can update or retain the old baseline (`skills/canary/SKILL.md:540-735`).

### Rules, gates, and stop conditions

- Baseline capture stops before deployment.
- Alert on change, not absolute error count.
- Require two consecutive anomalous checks.
- Performance regression threshold is greater than 2× baseline.
- Every alert must include screenshot evidence.
- Missing `GSTACK_STEP_OK` or an `[error` line is a page-load failure.
- Start monitoring within 30 seconds (`skills/canary/SKILL.md:559-584`, `skills/canary/SKILL.md:620-735`).

### Tools and dependencies

- Aside browser or gstack `$B` fallback.
- Local `gstack-skill-start`, slug, analytics, question, and telemetry helpers.
- Browser performance/navigation APIs.
- Filesystem for `.gstack/canary-reports`.
- Git branch detection for baseline metadata (`skills/canary/SKILL.md:19-518`, `skills/canary/SKILL.md:540-735`).

### Permissions and side effects

- Reads production pages and same-origin links.
- Takes screenshots.
- Writes local baseline/report artifacts and machine-local analytics.
- Can offer rollback, but the canary workflow itself contains no rollback implementation.
- Browser rules prohibit reading unrelated user tabs and credential extraction (`skills/canary/SKILL.md:341-447`, `skills/canary/SKILL.md:540-735`).

### Strongest unique methods

- Baseline-relative detection rather than absolute alerting.
- Two-check transient tolerance.
- Periodic screenshot evidence.
- Clear separation between baseline capture and post-deploy observation.
- Single-purpose extended monitoring complementary to one-shot deploy verification.

### Weaknesses and failure modes

- Baseline manifest stores only `console_errors` count, not error identities, although later logic requires detecting “errors not present in baseline.” Equal counts with different errors, or one replaced error, cannot be reliably compared (`skills/canary/SKILL.md:559-584`, `skills/canary/SKILL.md:620-632`).
- The continuous-monitor script does not run link checks, yet the comparison rules claim to detect “new 404s.” The page-discovery HEAD checks occur only before monitoring (`skills/canary/SKILL.md:586-608`, `skills/canary/SKILL.md:611-632`).
- Without a pre-deploy baseline, the “pre-deploy snapshot” is actually taken when monitoring starts; it may already reflect the deployed version.
- Automated page discovery only takes the top five links and may miss authenticated or client-side routes.

### Overlap, duplicate, and dependency candidates

- `curation/v2/coverage.json` identifies `skill-root:canary` and `skill-root:gstack/canary` as an exact duplicate-body group (`curation/v2/coverage.json:9-13`).
- **Strong dependency:** `land-and-deploy` performs a one-shot canary and recommends this root for extended monitoring.
- **Complement:** `incident-response` should receive persistent critical/high canary alerts.
- **Tool overlap:** `qa-only` also takes screenshots and captures console failures, but explores functionality rather than time-series deploy deltas.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `canary/SKILL.md` | semantic-read | Complete generated runtime workflow. |
| `canary/SKILL.md.tmpl` | semantic-read | Complete authoring template; confirms the canary-specific body and generated placeholders. |

---

## 3. `incident-response`

### Exact root / skill path

- Root: `skills/incident-response/`
- Skill: `skills/incident-response/SKILL.md`

### Trigger and non-trigger

- **Trigger:** active outage, production degradation, security incident, site/service down, P0/P1/SEV event, on-call procedure, severity framework, incident commander, or status-page work (`skills/incident-response/SKILL.md:1-31`).
- **Non-trigger:** after-the-fact retrospective, planned launch, or pre-launch QA. Those route to `after-action-report`, `launch-runbook`, and `qa-testing` respectively (`skills/incident-response/SKILL.md:23-31`).

### Responsibility and non-responsibility

- **Responsibility:** coordinate detection, triage, mitigation, communication, resolution, roles, decision authority, and handoff into an AAR.
- **Non-responsibility:** deep post-incident analysis, planned release execution, or stack-specific technical remediation. It remains stack/tool agnostic (`skills/incident-response/SKILL.md:11-18`, `skills/incident-response/SKILL.md:42-137`).

### Inputs

- Incident signal.
- Production/monitoring access.
- Defined roles and authority.
- Operational communication channels.
- Impact, scope, timeline, and observations as available (`skills/incident-response/SKILL.md:34-40`).

### Outputs

- Severity assignment.
- Incident channel and role assignment.
- Timestamped internal/external updates.
- Mitigation decision and verification record.
- Closing incident summary with timeline, mitigation, actions, and AAR date (`skills/incident-response/SKILL.md:139-224`).

### Core workflow

Acknowledge, assess severity, assign IC/comms/ops, communicate, investigate common causes, mitigate, verify via user flow, communicate resolution, close, and schedule AAR (`skills/incident-response/SKILL.md:164-177`).

### Branches

- Severity SEV-1 through SEV-4.
- Mitigation choice: rollback, feature flag, failover, scale, throttle, degrade, or maintenance.
- Public communication based on visible customer impact.
- Small teams may combine roles.
- Root cause may be deferred to AAR if restoration is complete (`skills/incident-response/SKILL.md:50-137`, `skills/incident-response/references/incident-playbook.md:8-63`).

### Rules, gates, and stop conditions

- Mitigate user impact before root-cause analysis.
- Re-evaluate severity as evidence changes.
- Maintain fixed communication cadence, even with no progress.
- Never speculate publicly.
- Never declare resolution before mitigation and customer flow verification.
- A stated data gap is acceptable; fabrication is not (`skills/incident-response/SKILL.md:81-137`, `skills/incident-response/SKILL.md:226-232`).

### Tools and dependencies

- No prescribed vendor.
- Depends on monitoring, logs, metrics, status page, incident channel, paging, production controls, and relevant SMEs.
- Reference playbook supplies detailed SLAs, templates, and decision rubrics (`skills/incident-response/references/incident-playbook.md:1-210`).

### Permissions and side effects

- Potentially high-impact operational actions: rollback, disable features, fail over, scale, throttle traffic, stop writes, isolate systems, rotate credentials, or enter maintenance mode.
- Public/internal communications may affect customers and organizational response.
- Authority rests with the IC, not implicitly with the skill (`skills/incident-response/SKILL.md:81-160`; `skills/incident-response/references/incident-playbook.md:139-193`).

### Strongest unique methods

- Explicit command structure separating IC, comms, ops, scribe, and SMEs.
- “Stop the bleeding first” principle.
- Severity-specific response and communication cadence.
- Clear public-message progression: investigating, identified, monitoring, resolved.
- Data-gap rule preventing fabricated incident metrics.

### Weaknesses and failure modes

- No concrete integration with alerting, status-page, chat, paging, or ticket systems.
- “When in doubt: act” is useful under impact but risky without an explicit reversibility/safety check; the reference playbook partly constrains rollback and data-integrity cases.
- Security incidents receive only a short isolation/credential/log-preservation row; detailed evidence-preservation and legal/regulatory procedures are out of scope.
- Role/process guidance cannot itself obtain the required production authority.

### Overlap, duplicate, and dependency candidates

- **Receives:** persistent failures from `canary` and failed production health checks from `land-and-deploy`.
- **Complements:** `retro` analyzes engineering trends, but incident follow-up belongs first to an AAR.
- **Conditional dependency:** may direct `land-and-deploy` rollback patterns, but should not inherit its release automation.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `incident-response/SKILL.md` | semantic-read | Complete operational framework. |
| `incident-response/references/incident-playbook.md` | semantic-read | Severity SLAs, role details, templates, rollback/escalation rubrics, and anti-patterns materially extend the root. |

---

## 4. `land-and-deploy`

### Exact root / skill path

- Root: `skills/land-and-deploy/`
- Skill: `skills/land-and-deploy/SKILL.md`

### Trigger and non-trigger

- **Trigger:** merge/land an existing PR, deploy it, and verify production (`skills/land-and-deploy/SKILL.md:1-17`, `skills/land-and-deploy/SKILL.md:594-618`).
- **Non-trigger:** creating the PR; that belongs to `/ship`. GitLab/unknown hosts are explicitly unsupported and stop after directing manual merge (`skills/land-and-deploy/SKILL.md:586-593`, `skills/land-and-deploy/SKILL.md:619-643`).

### Responsibility and non-responsibility

- **Responsibility:** locate PR, gate readiness, wait for CI, detect version drift, merge, detect deploy strategy, monitor deploy, perform a one-shot canary, optionally revert, and produce a deploy report.
- **Non-responsibility:** extended monitoring (`canary`), initial PR preparation (`ship`), or unsupported GitLab merging (`skills/land-and-deploy/SKILL.md:619-1046`).

### Inputs

- Current branch or PR number.
- Optional production URL.
- GitHub CLI authentication.
- Existing PR.
- CI/check state.
- Optional deploy configuration in `CLAUDE.md`.
- Review/evidence ledgers and optional staging setup (`skills/land-and-deploy/SKILL.md:619-783`; `skills/land-and-deploy/sections/first-run-validation.md:1-180`).

### Outputs

- Merge commit and branch cleanup.
- Deployment status.
- Canary screenshot and health assessment.
- Optional revert commit/PR.
- Markdown deploy report and machine-local JSONL metrics (`skills/land-and-deploy/SKILL.md:850-1009`).

### Core workflow

1. Detect platform/base and require GitHub.
2. Authenticate and identify an open PR.
3. On first/config-changed run, validate deploy infrastructure and obtain confirmation.
4. Gate CI and mergeability.
5. Detect stale VERSION slot.
6. Run review/test/docs/PR-body readiness gate and obtain explicit merge confirmation.
7. Merge through auto-merge/queue or direct squash.
8. Detect deployment strategy.
9. Wait/poll deployment.
10. Run a scope-sensitive production canary.
11. Revert if chosen.
12. Write report and recommend extended monitoring (`skills/land-and-deploy/SKILL.md:619-1046`).

### Branches

- First run, changed config, or confirmed config.
- CI passing, pending, failed, or timed out.
- VERSION drift or offline drift checker.
- Current/stale/missing review with inline/full/skip options.
- Auto-merge, direct merge, merge queue, already merged after local error.
- GitHub Actions, Fly, Render, Heroku, Vercel, Netlify, custom hook, or no deploy.
- Optional staging-first, staging-only, or direct production.
- Healthy, expected warm-up, investigate, or revert (`skills/land-and-deploy/sections/first-run-validation.md:1-180`; `skills/land-and-deploy/sections/readiness-gate.md:1-234`; `skills/land-and-deploy/sections/merge-and-deploy.md:1-270`).

### Rules, gates, and stop conditions

- Stop for missing auth/PR, closed PR, failing CI, conflicts, version drift, blockers, deployment failure, or unhealthy production.
- First run and the final readiness gate require explicit approval.
- Never force-push.
- Never retry `gh pr merge` after non-zero exit; query server state first.
- Failing live free-test evidence blocks merge; stale evidence triggers a fresh run.
- Merge is irreversible except by a new revert commit (`skills/land-and-deploy/sections/readiness-gate.md:1-234`; `skills/land-and-deploy/sections/merge-and-deploy.md:1-154`).

### Tools and dependencies

- GitHub CLI, Git, Bash utilities, `jq`, Bun, gstack version/review/evidence/diff helpers.
- Optional Fly/Render/Heroku tooling.
- Aside or `$B` browser.
- Project tests and deploy workflow.
- GitHub repository settings and branch protections.

### Permissions and side effects

- Merges PRs, deletes branches, potentially updates local worktrees, deploys, polls production, takes screenshots, writes reports/analytics, and can revert/push base.
- Production browser mutation requires consent under the embedded browser contract.
- Third-party dashboard actions have a separate consent contract (`skills/land-and-deploy/SKILL.md:308-515`, `skills/land-and-deploy/sections/merge-and-deploy.md:1-154`).

### Strongest unique methods

- First-run infrastructure dry run with configuration fingerprint.
- Content-fingerprint-based review freshness.
- Server-authoritative recovery after ambiguous `gh pr merge` failure.
- VERSION queue-drift stop before merge.
- Staging-first option.
- Scope-sensitive canary depth and timed deploy report.

### Weaknesses and failure modes

- GitHub-only implementation sharply limits portability.
- Large external helper surface means the root cannot operate from this subtree alone.
- Several local/environment writes occur before the irreversible merge, increasing operational coupling.
- E2E and LLM eval failures are warnings rather than blockers in the readiness section; only the “free tests” lane is a hard blocker (`skills/land-and-deploy/sections/readiness-gate.md:94-145`).
- Direct rollback attempts a base checkout/revert/push, which may be unsuitable in multi-worktree or protected-branch environments; a fallback PR is provided but only after failure (`skills/land-and-deploy/SKILL.md:930-950`).

### Overlap, duplicate, and dependency candidates

- Exact duplicate-body candidate with `gstack/land-and-deploy` per coverage (`curation/v2/coverage.json:14-17`).
- **Strong predecessor:** `ship` creates and prepares the PR.
- **Strong successor:** `canary` provides extended monitoring after the one-shot health check.
- **Escalation complement:** `incident-response` handles an actual production incident.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `land-and-deploy/SKILL.md` | semantic-read | Complete generated runtime skeleton. |
| `land-and-deploy/SKILL.md.tmpl` | semantic-read | Complete authoring source with component placeholders. |
| `land-and-deploy/sections/first-run-validation.md` | semantic-read | First-run/config-change branch. |
| `land-and-deploy/sections/readiness-gate.md` | semantic-read | Final irreversible merge gate. |
| `land-and-deploy/sections/merge-and-deploy.md` | semantic-read | Merge recovery, queue, and deploy detection. |
| `land-and-deploy/sections/manifest.json` | semantic-read | Passive section registry and trigger map. |
| `land-and-deploy/sections/*.md.tmpl` | excluded | Generator source duplicates of inspected generated section bodies; no extra runtime branch claimed. |

---

## 5. `playwright-best-practices`

### Exact root / skill path

- Root: `skills/playwright-best-practices/`
- Skill: `skills/playwright-best-practices/SKILL.md`

### Trigger and non-trigger

- **Trigger:** writing, debugging, structuring, configuring, or maintaining Playwright test suites across E2E, component, API, visual, accessibility, security, browser API, Electron, extension, and CI concerns (`skills/playwright-best-practices/SKILL.md:1-18`).
- **Non-trigger:** ad hoc terminal browser operation with no requested test files; `playwright` is the better root for that. It is guidance, not an autonomous QA report workflow.

### Responsibility and non-responsibility

- **Responsibility:** route a test-development activity to the appropriate focused reference, prescribe resilient patterns, and require validation/repetition.
- **Non-responsibility:** running a complete application QA audit, deploying, or owning application code. It does not provide a bundled executable.

### Inputs

- Playwright task type.
- Existing test/config/application context.
- Framework, environment, CI platform, browser/API feature, and failure symptoms.
- Existing suite conventions when modifying tests.

### Outputs

- Test specifications/configuration/advice.
- Locator, waiting, fixture, POM, data, auth, mocking, CI, and debugging patterns.
- A validation loop requiring normal test execution and repeat runs for critical tests (`skills/playwright-best-practices/SKILL.md:100-342`).

### Core workflow

1. Classify activity using the reference guide/decision tree.
2. Read only relevant branch references.
3. Select the cheapest appropriate test layer.
4. Implement resilient locators, web-first assertions, isolated fixtures, and targeted mocks.
5. Run `npx playwright test --reporter=list`.
6. Inspect trace and repair failures.
7. Repeat critical tests five times (`skills/playwright-best-practices/SKILL.md:100-342`; `skills/playwright-best-practices/architecture/test-architecture.md:1-281`).

### Branches

The root is primarily a dispatcher with branches for:

- E2E/component/API/visual testing.
- Mobile, browser APIs, realtime, multi-user, error states.
- Architecture: test type, POM versus fixtures, mock versus real.
- Framework: React/Vue/Angular/Next.js.
- Debugging by selector/timing/parallelism/state/console symptoms.
- CI, sharding, reports, coverage, tags, annotations, and projects (`skills/playwright-best-practices/SKILL.md:18-342`).

### Rules, gates, and stop conditions

- Prefer role/label/text/test-ID locators before CSS/XPath (`skills/playwright-best-practices/core/locators.md:1-45`).
- Prefer web-first assertions and condition waits over fixed sleeps (`skills/playwright-best-practices/core/assertions-waiting.md:1-250`).
- Keep tests isolated; use per-worker data when parallel workers mutate state (`skills/playwright-best-practices/core/fixtures-hooks.md:1-273`).
- Do not proceed until the modified tests pass; critical tests should be repeated (`skills/playwright-best-practices/SKILL.md:330-342`).

### Tools and dependencies

- Node/npm/npx.
- `@playwright/test`.
- Optional `@axe-core/playwright`, framework-specific component packages, Docker, CI providers, and project dependencies.
- External application services or mocks as selected.

### Permissions and side effects

- Writes tests/configuration and may install packages.
- Executes browsers, application servers, APIs, database setup/teardown, screenshots, traces, videos, and CI workflows.
- Auth state can contain tokens and must be gitignored (`skills/playwright-best-practices/advanced/authentication.md:44-105`).

### Strongest unique methods

- Activity-based routing over a broad reference corpus.
- Semantic locator priority and web-first waiting.
- Explicit test-layer economics: API for backend permutations, component for UI states, E2E for critical wiring (`skills/playwright-best-practices/architecture/test-architecture.md:13-281`).
- POM/fixture/helper selection based on interaction count, reuse, and lifecycle (`skills/playwright-best-practices/architecture/pom-vs-fixtures.md:1-287`).
- Flakiness categorization into UI, environment, data/parallelism, and suite-state causes (`skills/playwright-best-practices/debugging/flaky-tests.md:1-322`).

### Weaknesses and failure modes

- Corpus breadth creates retrieval risk: a caller that does not follow the route map may miss the decisive reference.
- Guidance is not version-pinned in the root, so examples can drift from installed Playwright behavior.
- Some examples include literal illustrative passwords or attack strings; they are pedagogical but must not be copied into production tests.
- It offers many optional dependencies and patterns without a repository-specific “reuse existing setup first” gate.

### Overlap, duplicate, and dependency candidates

- **Complement to `playwright`:** this root authors and maintains tests; `playwright` drives one-off browser sessions.
- **Dependency candidate for `qa-only`:** provides durable test patterns after QA finds a regression, but `qa-only` explicitly does not fix or write tests.
- **Complement to `vitest`:** Playwright covers browser/integration paths; Vitest covers fast Vite-native unit/type/component logic.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `playwright-best-practices/SKILL.md` | semantic-read | Complete routing/index contract. |
| `playwright-best-practices/core/*.md` | semantic-read | Entire core set reviewed: suite structure, locators, waits, POM, fixtures, configuration, setup/projects, data, annotations, tags. |
| `playwright-best-practices/architecture/test-architecture.md` | semantic-read | Test-layer decision method. |
| `playwright-best-practices/architecture/pom-vs-fixtures.md` | semantic-read | Reuse-pattern selection method. |
| `playwright-best-practices/architecture/when-to-mock.md` | excluded | Topic-specific semantic branch classified by the root’s route map; dossier makes no detailed claims from it. |
| `playwright-best-practices/advanced/authentication.md` | semantic-read | Auth/storage-state/per-worker security patterns. |
| `playwright-best-practices/advanced/{authentication-flows,clock-mocking,mobile-testing,multi-context,multi-user,network-advanced,third-party}.md` | excluded | Branch-specific semantic references; classified through the root index, not relied upon for detailed dossier claims. |
| `playwright-best-practices/browser-apis/websockets.md` | semantic-read | Representative realtime/browser API branch. |
| `playwright-best-practices/browser-apis/{browser-apis,iframes,service-workers}.md` | excluded | Branch-specific semantic references not needed for root-level claims. |
| `playwright-best-practices/debugging/flaky-tests.md` | semantic-read | Root-cause flake taxonomy and remediation. |
| `playwright-best-practices/debugging/{console-errors,debugging,error-testing}.md` | excluded | Topic-specific debugging branches classified by index. |
| `playwright-best-practices/frameworks/react.md` | semantic-read | Representative framework adapter. |
| `playwright-best-practices/frameworks/{angular,nextjs,vue}.md` | excluded | Framework variants; root index establishes their conditional role. |
| `playwright-best-practices/infrastructure-ci-cd/ci-cd.md` | semantic-read | Representative CI/sharding/reporting branch. |
| `playwright-best-practices/infrastructure-ci-cd/{docker,github-actions,gitlab,other-providers,parallel-sharding,performance,reporting,test-coverage}.md` | excluded | Provider/specialized variants, not used for unsupported detailed claims. |
| `playwright-best-practices/testing-patterns/accessibility.md` | semantic-read | Accessibility methods and automation limits. |
| `playwright-best-practices/testing-patterns/security-testing.md` | semantic-read | Security-test patterns and trust risks. |
| `playwright-best-practices/testing-patterns/{api-testing,browser-extensions,canvas-webgl,component-testing,drag-drop,electron,file-operations,file-upload-download,forms-validation,graphql-testing,i18n,performance-testing,visual-regression}.md` | excluded | Specialized semantic branches classified by the activity map; not deeply claimed here. |

---

## 6. `playwright`

### Exact root / skill path

- Root: `skills/playwright/`
- Skill: `skills/playwright/SKILL.md`

### Trigger and non-trigger

- **Trigger:** terminal-driven real-browser navigation, form interaction, snapshots, screenshots, extraction, tabs, traces, or UI debugging (`skills/playwright/SKILL.md:1-12`).
- **Non-trigger:** writing `@playwright/test` specs unless explicitly requested (`skills/playwright/SKILL.md:8-12`).

### Responsibility and non-responsibility

- **Responsibility:** expose a reliable CLI-first interaction loop using snapshots and stable element references.
- **Non-responsibility:** test-suite architecture and normal Playwright test generation; those belong to `playwright-best-practices`.

### Inputs

- URL and requested browser task.
- Optional headed mode, session name, configuration file, or artifact label.
- Fresh snapshot references for interaction.

### Outputs

- Browser state changes.
- Snapshots, screenshots, PDFs, traces, console/network output, extracted data.
- Commands or a reproducible operational script.

### Core workflow

1. Verify `npx`.
2. Set `CODEX_HOME` and wrapper path.
3. Open page.
4. Snapshot.
5. Interact through latest refs.
6. Re-snapshot after navigation/major DOM change.
7. Capture artifacts when useful (`skills/playwright/SKILL.md:13-117`).

### Branches

- Missing `npx` stops and gives Node/npm installation instructions.
- Wrapper versus optional global CLI.
- Headed versus headless.
- Single or named sessions.
- Forms, traces, and multi-tab workflows.
- Stale/missing ref triggers another snapshot (`skills/playwright/SKILL.md:13-117`; `skills/playwright/references/workflows.md:1-76`).

### Rules, gates, and stop conditions

- Always snapshot before using an element ref.
- Re-snapshot after navigation/significant DOM changes or stale-ref failure.
- Prefer explicit CLI commands over `eval`/`run-code`.
- Use placeholder `eX` only when no fresh snapshot exists and disclose why.
- Place artifacts under `output/playwright/`.
- Do not pivot to test specs without explicit request (`skills/playwright/SKILL.md:92-117`).

### Tools and dependencies

- `npx`, Node/npm.
- `@playwright/cli` fetched/executed through the bundled wrapper.
- Bash.
- Optional global `playwright-cli`.
- Real browser runtime.

### Permissions and side effects

- Navigates websites, fills forms, clicks controls, uploads files, manipulates dialogs/tabs, and writes browser artifacts.
- The root itself does not contain the more detailed consent/credential contract found in gstack browser skills.
- Named sessions persist browser state across commands.

### Strongest unique methods

- Snapshot-ref discipline prevents brittle selector improvisation.
- Very small command vocabulary for one-off automation.
- Bundled wrapper removes the global-install requirement.
- Named sessions isolate concurrent work.
- Clear artifact containment convention.

### Weaknesses and failure modes

- The preferred wrapper runs `npx --yes --package @playwright/cli`, which can perform a network package fetch and execute newly resolved package code (`skills/playwright/scripts/playwright_cli.sh:1-22`).
- No explicit non-local mutation consent or credential-handling contract.
- Example form data includes a literal password; safe as illustration, unsafe if copied as a real credential.
- State refs become invalid after DOM changes, requiring disciplined snapshots.

### Overlap, duplicate, and dependency candidates

- **Complement:** execution layer for `playwright-best-practices`.
- **Variant/conflict:** `qa-only`, `canary`, and `land-and-deploy` standardize on Aside/`$B`, not this wrapper; consolidation should preserve their stronger browser privacy contract.
- **Complement:** can reproduce a defect found by `audit-website`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `playwright/SKILL.md` | semantic-read | Complete CLI workflow. |
| `playwright/references/cli.md` | semantic-read | Command surface and session behavior. |
| `playwright/references/workflows.md` | semantic-read | Forms, extraction, trace, config, and troubleshooting patterns. |
| `playwright/scripts/playwright_cli.sh` | behavior-reviewed | Validates `npx`, injects optional session, and execs `npx --yes --package @playwright/cli`. |
| `playwright/agents/openai.yaml` | semantic-read | UI metadata/default prompt; no execution behavior. |
| `playwright/assets/*` | excluded | Binary/vector branding assets only. |
| `playwright/LICENSE.txt` | excluded | Third-party Apache licensing text, not operational semantics. |
| `playwright/NOTICE.txt` | semantic-read | Attribution and modification provenance relevant to reuse. |

---

## 7. `qa-only`

### Exact root / skill path

- Root: `skills/qa-only/`
- Skill: `skills/qa-only/SKILL.md`

### Trigger and non-trigger

- **Trigger:** “qa report only,” “just report bugs,” “test but don’t fix,” “bug report,” or “just check for bugs” (`skills/qa-only/SKILL.md:1-22`).
- **Non-trigger:** test-fix-verify loops; those route to `/qa`. It explicitly forbids fixes and fix suggestions (`skills/qa-only/SKILL.md:946-971`).

### Responsibility and non-responsibility

- **Responsibility:** browser-based black-box exploration, evidence capture, issue reproduction, health scoring, baseline/regression comparison, and report writing.
- **Non-responsibility:** source fixes, code edits, source-level diagnosis, or replacing browser QA with unit tests/evals (`skills/qa-only/SKILL.md:522-537`, `skills/qa-only/SKILL.md:881-971`).

### Inputs

- URL or feature-branch diff context.
- Mode: full, quick, regression, or diff-aware.
- Scope/output directory.
- Existing browser session or human-completed fallback sign-in.
- Optional ship/test-plan artifact and prior learnings (`skills/qa-only/SKILL.md:522-621`).

### Outputs

- Structured Markdown report.
- Per-issue screenshots and repro evidence.
- Health score and category scores.
- `baseline.json`.
- Project-scoped test-outcome artifact.
- Optional regression delta (`skills/qa-only/SKILL.md:755-971`).

### Core workflow

1. Resolve mode and URL.
2. Prefer an existing test plan; otherwise infer affected pages from branch diff.
3. Initialize browser and report directories.
4. Authenticate only through the user’s browser session/handoff.
5. Orient with snapshot, visible text, console capture, screenshot, and links.
6. Explore pages and interactions.
7. Confirm each defect by retry.
8. Document immediately with screenshot/diff evidence.
9. Compute weighted health score.
10. Save report/baseline and project outcome (`skills/qa-only/SKILL.md:522-971`).

### Branches

- Diff-aware, full, quick, or regression.
- Aside versus `$B`.
- Auth wall/2FA/CAPTCHA handoff.
- Local links may receive HEAD checks; non-local links remain unverified.
- Static bugs get one annotated screenshot; interactive bugs get before/after screenshots and snapshot diff.
- Non-local mutations require one consent gate (`skills/qa-only/SKILL.md:550-887`).

### Rules, gates, and stop conditions

- Every issue needs screenshot evidence.
- Reproduce each issue twice before documenting.
- Never type or expose credentials.
- Never read source code.
- Check console after every interaction.
- Prefer 5–10 evidenced issues over broad vague coverage.
- Never fix or suggest fixes.
- Browser testing is mandatory; unit tests/evals/curl are not substitutes (`skills/qa-only/SKILL.md:869-971`).

### Tools and dependencies

- Aside or gstack `$B`.
- Browser snapshot, screenshot, performance, console, and responsive-emulation APIs.
- Git for diff-aware scoping.
- Missing shared `qa` report template and issue taxonomy.
- gstack learnings, slug, question, telemetry, and project-artifact helpers.

### Permissions and side effects

- Reads application pages and may fill forms.
- Local targets permit mutating actions; non-local mutations require explicit consent.
- Writes `.gstack/qa-reports`, screenshots, baseline, project outcome, learnings, and telemetry.
- Explicitly does not modify product source.

### Strongest unique methods

- Strict report-only boundary.
- Evidence tiers tailored to interactive versus static defects.
- Weighted health score with transparent deductions.
- Diff-aware page selection plus fallback smoke coverage.
- Same-origin link privacy rule for non-local targets.
- Immediate issue documentation reduces context loss.

### Weaknesses and failure modes

- **Blocking source gap:** `qa/templates/qa-report-template.md` and `qa/references/issue-taxonomy.md` are required by the workflow but absent (`skills/qa-only/SKILL.md:686-755`; read probes returned `ENOENT`).
- Internal contradiction: diff-aware mode directs analysis of route/controller/component/source relationships, while the important rules state “Never read source code” (`skills/qa-only/SKILL.md:565-621`, `skills/qa-only/SKILL.md:881-887`).
- Full mode promises “every reachable page” and 5–10 issues in 5–15 minutes, which is not generally bounded for large/authenticated apps.
- The health score is finding-count-sensitive rather than coverage-sensitive; a shallow run can score highly despite unvisited pages.
- It asks to report “No test framework detected” while also forbidding source inspection; test-framework detection method is not defined in the root.

### Overlap, duplicate, and dependency candidates

- Exact duplicate-body candidate with `gstack/qa-only` per coverage (`curation/v2/coverage.json:18-21`).
- **Complement:** `audit-website` provides crawler/rule coverage and can fix; this root provides black-box functional evidence and cannot fix.
- **Dependency:** `ship` invokes this workflow inline for plan verification.
- **Tool overlap:** `playwright` could serve as an alternate browser driver, but lacks this root’s reporting and consent rules.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `qa-only/SKILL.md` | semantic-read | Complete generated report-only workflow. |
| `qa-only/SKILL.md.tmpl` | semantic-read | Complete authoring template; confirms shared methodology placeholder. |
| `qa/templates/qa-report-template.md` | **unresolved / unreadable** | Required semantic template; repository path absent (`ENOENT`). |
| `qa/references/issue-taxonomy.md` | **unresolved / unreadable** | Required semantic taxonomy; repository path absent (`ENOENT`). |

---

## 8. `retro`

### Exact root / skill path

- Root: `skills/retro/`
- Skill: `skills/retro/SKILL.md`

### Trigger and non-trigger

- **Trigger:** weekly/sprint engineering retrospective, “what did we ship,” repo trend analysis, comparison, or cross-project global retro (`skills/retro/SKILL.md:1-38`, `skills/retro/SKILL.md:589-617`).
- **Non-trigger:** incident AAR, active production response, or release execution.

### Responsibility and non-responsibility

- **Responsibility:** derive engineering metrics and narrative from Git history, contributors, tests, review logs, learnings, TODOs, skill usage, and prior retros.
- **Non-responsibility:** alter product code, judge team members against each other, or write narrative files. Only JSON snapshots are persisted (`skills/retro/SKILL.md:1176-1253`).

### Inputs

- Time window, compare/global mode.
- Current date from session context.
- Git history and optional remote freshness.
- Optional prior snapshots, TODOs, review logs, learnings, Greptile history, and context notes (`skills/retro/SKILL.md:619-761`).

### Outputs

- Tweetable summary.
- Metrics tables, author leaderboard, histograms, session analysis, hotspots, test health, plan completion, wins, improvements, and habits.
- Repo-local `.context/retros/*.json` or global `~/.gstack/retros/*.json` snapshot (`skills/retro/SKILL.md:762-1253`; `skills/retro/sections/report-format.md:1-114`).

### Core workflow

1. Validate and normalize window.
2. Detect platform/base.
3. Fetch base when possible.
4. Run `gstack-retro-metrics`.
5. enforce stale-date/base guard.
6. Interpret metrics and optional inputs.
7. Analyze time, sessions, commit types, hotspots, size, focus, authors, test health, and shortcut debt.
8. Compare prior snapshot.
9. Save JSON snapshot.
10. Render the narrative through the report-format section (`skills/retro/SKILL.md:619-979`).

### Branches

- Normal repo retro.
- Compare mode with adjacent non-overlapping windows.
- Global cross-project mode.
- Offline/local-only disclosure.
- Solo versus team narrative.
- First retro versus trend comparison.
- 14-day-plus weekly trend branch.
- Optional input rows only when data exists (`skills/retro/SKILL.md:619-1253`).

### Rules, gates, and stop conditions

- Invalid arguments print usage and stop.
- Day/week windows align to local midnight.
- Session-context date, not system clock, anchors “today.”
- Stale remote/base mismatch blocks when freshness was verifiable.
- Zero commits produce a candid empty result.
- All claims must anchor in commits/metrics.
- The narrative is not written to disk; only snapshots are.
- Team members are not negatively compared (`skills/retro/SKILL.md:619-700`, `skills/retro/SKILL.md:1218-1253`).

### Tools and dependencies

- Git and optional remote fetch.
- `gstack-retro-metrics`, `gstack-global-discover`, decision/learning/review helpers.
- Bash text utilities.
- Read/Write for snapshots.
- Optional Codex/Claude/Gemini session-discovery data.

### Permissions and side effects

- Reads Git history and optional personal/project analytics.
- Fetches remotes in normal/global mode.
- Writes retro snapshots, learnings, telemetry, and temporary discovery diagnostics.
- Does not edit product code.

### Strongest unique methods

- Stale-date/base guard prevents polished retros over empty wrong windows.
- 45-minute session segmentation and deep/medium/micro classification.
- Logical SLOC and weighted commits de-emphasize raw AI-inflated LOC.
- Current-user versus teammate framing.
- Shortcut-debt marker harvesting.
- Cross-project context-switching and personal streak analysis.

### Weaknesses and failure modes

- Many productivity metrics are proxies; commit timing is not working time.
- LOC/session-hour can reward generated volume despite the logical-SLOC correction.
- Fetching remote history conflicts with strictly offline usage, though failure is disclosed.
- Global discovery relies on external gstack binaries and filesystem conventions.
- Narrative inference from commit subjects can misclassify product impact if messages are poor.

### Overlap, duplicate, and dependency candidates

- Exact duplicate-body candidate with `gstack/retro` per coverage (`curation/v2/coverage.json:22-25`).
- **Consumes:** `ship` coverage/plan metrics, canary/deploy review logs, learnings, and test health.
- **Distinct from:** incident AAR; it is cadence/trend analysis, not causal incident reconstruction.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `retro/SKILL.md` | semantic-read | Complete generated workflow. |
| `retro/SKILL.md.tmpl` | semantic-read | Complete authoring template and global-mode source. |
| `retro/sections/report-format.md` | semantic-read | Required narrative output schema. |
| `retro/sections/manifest.json` | semantic-read | Passive section trigger registry. |
| `retro/sections/report-format.md.tmpl` | excluded | Generator source duplicate of inspected generated report section. |

---

## 9. `ship`

### Exact root / skill path

- Root: `skills/ship/`
- Skill: `skills/ship/SKILL.md`

### Trigger and non-trigger

- **Trigger:** ship, deploy, push to main, create a PR, merge/push, or declare code ready (`skills/ship/SKILL.md:1-18`).
- **Non-trigger:** merging an already-created PR into production; that is `land-and-deploy`. Apple App Store/TestFlight distribution conditionally diverts into its own adapter before the normal branch gate (`skills/ship/SKILL.md:617-648`).

### Responsibility and non-responsibility

- **Responsibility:** prepare and push a release-ready branch, including base merge, tests/evals, coverage, plan completion, review, version, changelog, TODOs, commits, verification, docs sync, and PR/MR creation.
- **Non-responsibility:** ordinary production landing/monitoring after PR creation, except the separate Apple storefront path.

### Inputs

- Feature branch and base.
- Uncommitted changes.
- Project test/build conventions.
- Optional plan, TODO, review, Greptile, and documentation state.
- GitHub/GitLab CLI and remote.
- VERSION/package manifests.
- Optional Apple project and paid developer membership (`skills/ship/SKILL.md:580-648`; `skills/ship/sections/apple-release.md:1-92`).

### Outputs

- Merged-base feature branch.
- Tests/coverage/review evidence.
- Optional generated tests and fixes.
- VERSION, CHANGELOG, TODO updates.
- Bisectable commits.
- Pushed branch.
- Synchronized documentation.
- Created or updated PR/MR with redacted body and version-prefixed title.
- Ship metrics (`skills/ship/SKILL.md:580-1123`; `skills/ship/sections/pr-body.md:1-260`).

### Core workflow

1. Detect host/base and branch gate.
2. Check distribution pipeline for new artifacts.
3. Fetch/merge base into feature branch.
4. Detect/bootstrap tests and run suites/evals.
5. Audit/generate coverage.
6. Audit plan completion, verification, and scope drift.
7. Run pre-landing and specialist review, then adversarial review.
8. Triage Greptile comments.
9. Determine and write version.
10. Generate changelog and update TODOs.
11. Create bisectable commits.
12. verify fresh evidence and build.
13. Install/offer credential pre-push guard.
14. Push.
15. Dispatch docs sync.
16. Redact and create/update PR/MR.
17. Persist metrics (`skills/ship/SKILL.md:580-1123`).

### Branches

- Repository landing versus Apple store distribution.
- GitHub versus GitLab.
- Existing versus absent test framework.
- In-branch versus pre-existing failures.
- Prompt changes trigger full evals.
- Coverage above target, between minimum/target, below minimum, or unknown.
- Plan items done/changed/partial/not done/unverifiable.
- Scope/specialist selection based on diff.
- Fresh/already-bumped/stale/unexpected version state.
- Existing PR update versus new PR creation.
- Docs subagent success, local-only commit, failure, or timeout.

### Rules, gates, and stop conditions

- Base branch is prohibited for normal repository landing.
- Never skip tests or pre-landing review.
- In-branch failure blocks.
- Coverage below threshold needs explicit override or more tests.
- Missing plan items and failed verification need a decision.
- Review fixes loop until clean, maximum three cycles.
- Never force-push.
- No completion without fresh fingerprint-bound evidence.
- PR body/title must pass redaction; high-confidence credential findings block.
- PR/MR title must begin with the released version (`skills/ship/SKILL.md:580-1123`; `skills/ship/sections/tests.md:1-280`; `skills/ship/sections/test-coverage.md:1-303`; `skills/ship/sections/review-army.md:1-375`; `skills/ship/sections/pr-body.md:110-260`).

### Tools and dependencies

- Git, GitHub/GitLab CLI, Bun, npm/project package managers, jq, Bash.
- gstack version, evidence, review, redaction, decision, learning, diff, and docs helpers.
- Agent/subagent mechanism for coverage, plan, specialists, adversarial, Greptile, and docs.
- Optional Codex.
- Project tests/evals/build.
- Fastlane/Xcode for Apple distribution.

### Permissions and side effects

- Merges remote base, modifies source/tests/docs/release metadata, installs dependencies/frameworks, commits, pushes, creates issues and PR/MRs, replies to review comments, and writes machine-local state.
- Apple adapter can create app records, certificates, profiles, API keys, upload builds, set pricing, and submit to App Review.
- Credential scanning and scoped Apple key handling are explicit security controls (`skills/ship/sections/apple-release.md:1-92`; `skills/ship/sections/pr-body.md:185-260`).

### Strongest unique methods

- Fingerprint-bound fresh-evidence ledger.
- Coverage audit based on changed execution paths and user flows rather than only instrumented line percentage.
- Plan completion distinguishes diff-verifiable, cross-repo, and external-state work.
- Specialist dispatch plus red-team/adversarial review.
- Deterministic version-state classifier and workspace-aware version queue.
- PR scan-at-sink: exact scanned bytes are sent.
- Recovery rules for failed/late documentation subagents.
- Apple durable-effect idempotency keys for upload/submission.

### Weaknesses and failure modes

- Extremely broad responsibility and helper dependency surface; one root combines testing, review, versioning, docs, Git, tracker, security, and distribution.
- Test bootstrap can add dependencies, config, tests, CI, and documentation during a release run, expanding scope materially (`skills/ship/sections/tests.md:1-174`).
- Heavy subagent dependency creates timeout, race, and malformed-JSON recovery complexity.
- The workflow claims to be fully automated but contains many legitimate judgment gates; “non-interactive” is therefore conditional rather than literal.
- Apple adapter carries high-impact account/credential/storefront authority that is semantically unlike ordinary repository shipping and is a strong candidate for separation.

### Overlap, duplicate, and dependency candidates

- Exact duplicate-body candidate with `gstack/ship` per coverage (`curation/v2/coverage.json:26-30`).
- **Strong successor:** `land-and-deploy`.
- **Dependency:** invokes `qa-only` for plan verification.
- **Complements:** `vitest` and `playwright-best-practices` supply detailed framework knowledge.
- **Feeds:** `retro` consumes ship metrics and review logs.
- **Variant candidate:** Apple store release should remain a conditional adapter or separate root, not be flattened into generic Git shipping.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ship/SKILL.md` | semantic-read | Complete generated release skeleton. |
| `ship/SKILL.md.tmpl` | semantic-read | Complete authoring source and section routing. |
| `ship/sections/tests.md` | semantic-read | Test bootstrap/run/failure ownership/eval behavior. |
| `ship/sections/test-coverage.md` | semantic-read | Coverage analysis, generation, and gate. |
| `ship/sections/plan-completion.md` | semantic-read | Plan, verification, and scope audit. |
| `ship/sections/review-army.md` | semantic-read | Review and specialist behavior. |
| `ship/sections/greptile.md` | semantic-read | Review-comment classification and mutation flow. |
| `ship/sections/adversarial.md` | semantic-read | Claude/Codex adversarial passes and persistence. |
| `ship/sections/apple-release.md` | semantic-read | Conditional App Store/TestFlight release adapter. |
| `ship/sections/changelog.md` | semantic-read | Generated section inspected; current rendered content is minimal. |
| `ship/sections/pr-body.md` | semantic-read | Docs dispatch, PR assembly, redaction, create/update behavior. |
| `ship/sections/manifest.json` | semantic-read | Passive section registry and trigger mapping. |
| `ship/sections/*.md.tmpl` | excluded | Generator sources duplicating reviewed generated section bodies; no extra runtime branch claimed. |

---

## 10. `vitest`

### Exact root / skill path

- Root: `skills/vitest/`
- Skill: `skills/vitest/SKILL.md`

### Trigger and non-trigger

- **Trigger:** writing Vitest tests, configuring the runner, mocking, coverage, filtering, fixtures, concurrency, projects, type tests, reporters, snapshots, or benchmarks (`skills/vitest/SKILL.md:1-19`).
- **Non-trigger:** browser E2E orchestration, black-box application QA, or deployment.

### Responsibility and non-responsibility

- **Responsibility:** serve as a version-oriented Vitest reference index and give syntax/pattern guidance for Vitest 4/5-era APIs.
- **Non-responsibility:** run tests autonomously, modify a repository as a workflow, or decide application test scope.

### Inputs

- Vitest topic.
- Existing Vite/Vitest config and package version.
- Runtime/environment needs: Node, jsdom, happy-dom, browser mode, projects, or CI.
- Test code and mocking/coverage requirements.

### Outputs

- Configuration and CLI instructions.
- Test, suite, assertion, hook, fixture, mock, coverage, snapshot, filtering, reporting, concurrency, project, type-test, and benchmark patterns.

### Core workflow

1. Select reference from the root index.
2. Align guidance to installed Vitest/Vite/Node version.
3. Configure test environment and discovery.
4. Implement tests/hooks/fixtures/mocks.
5. Run in watch or one-shot mode.
6. Filter, shard, report, or collect coverage as required.

### Branches

- `vite.config.ts` versus `vitest.config.ts`.
- Node/jsdom/happy-dom/custom/browser environment.
- V8 versus Istanbul coverage.
- Watch, run, related, changed, list, benchmark, or typecheck.
- File/test/tag/project filtering.
- Fork/thread/VM pools, concurrency, sharding, and isolation.
- Single versus multi-project/monorepo.
- Runtime versus type-only tests.

### Rules, gates, and stop conditions

- V4/V5 migration rules are explicit: no `workspace`, no `poolOptions`, no `coverage.all`, and v5 removes sequential modifiers (`skills/vitest/references/core-config.md:57-115`; `skills/vitest/references/core-test-api.md:46-78`).
- Concurrent tests should use context-bound `expect`.
- Async assertions must be awaited.
- Fake timers and stubs require restoration.
- Coverage requires `include` to report untouched source files.
- Undefined tags fail by default.
- CI should reject focused tests and obsolete/missing snapshots (`skills/vitest/references/core-expect.md:1-195`; `skills/vitest/references/features-mocking.md:1-228`; `skills/vitest/references/features-coverage.md:1-140`; `skills/vitest/references/features-test-tags.md:1-101`; `skills/vitest/references/features-snapshots.md:1-152`).

### Tools and dependencies

- Vitest and Vite.
- Node 20+ for v4 guidance; v5 is described as beta.
- Optional jsdom, happy-dom, browser provider, coverage provider, UI, TypeScript checker, and CI tooling.
- No behavior-bearing script in this root.

### Permissions and side effects

- Normal test/config/source writes if guidance is applied.
- Test execution can create `.vitest`, coverage, snapshots, reports, or benchmark baselines.
- Mocks and environments may alter globals, timers, env variables, or module cache inside test processes.
- The skill itself is documentation-only.

### Strongest unique methods

- Clear V4/V5 migration notes.
- Builder-style inferred fixtures with `onCleanup`.
- `vi.when` conditional mocking and `using` auto-restoration.
- AI-agent-aware minimal reporter.
- Project-level environment/pool/isolation configuration.
- Type narrowing through `expect.assert`.
- Tag-level shared timeout/retry semantics.

### Weaknesses and failure modes

- Root says it is based on Vitest 5.x beta and generated on `2026-06-22`; this is future/beta-sensitive guidance and may not match a stable installed project (`skills/vitest/SKILL.md:20-21`; `skills/vitest/GENERATION.md:1-5`).
- Some references mix v4 stable and v5 beta APIs; callers must branch on actual installed version.
- Generated documentation lacks a repository-first check for existing config/conventions.
- No executable validation loop is imposed by the root itself.

### Overlap, duplicate, and dependency candidates

- **Complement:** fast unit/type/component layer under `ship`.
- **Complement:** `playwright-best-practices` handles browser E2E and full-stack flows.
- **Conditional overlap:** both Vitest Browser Mode and Playwright can run real-browser component tests; selection should depend on existing project tooling and desired E2E scope.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `vitest/SKILL.md` | semantic-read | Complete root index. |
| `vitest/GENERATION.md` | semantic-read | Source SHA and generation provenance. |
| `vitest/references/core-*.md` | semantic-read | All six core API/config/CLI/hook/assertion/suite references reviewed. |
| `vitest/references/features-*.md` | semantic-read | All feature references reviewed: mocking, snapshots, coverage, context, concurrency, filtering, tags, reporters, benchmarks. |
| `vitest/references/advanced-*.md` | semantic-read | All advanced references reviewed: `vi`, environments, type tests, and projects. |

---

# Cross-root hypotheses

## Duplicate hypotheses

1. **Exact duplicate bodies already recorded in coverage**
   - `canary` ↔ `gstack/canary`
   - `land-and-deploy` ↔ `gstack/land-and-deploy`
   - `qa-only` ↔ `gstack/qa-only`
   - `retro` ↔ `gstack/retro`
   - `ship` ↔ `gstack/ship`  
   Evidence: `curation/v2/coverage.json:9-30`. These are duplicate candidates, not proof that their parent subtrees are semantically interchangeable; each nested root still needs its own subtree audit.

2. `SKILL.md` and `.tmpl` pairs in gstack-derived roots are generation pairs, not independent capabilities. They should retain provenance but not become duplicate capability units.

## Complement hypotheses

1. **Delivery chain:** `ship` prepares and opens the PR; `land-and-deploy` merges/deploys; `canary` performs extended monitoring; `incident-response` handles confirmed production impact.
2. **Web quality stack:** `audit-website` supplies crawler/rule coverage; `qa-only` supplies user-flow evidence; `playwright` supplies ad hoc reproducibility; `playwright-best-practices` supplies durable automated regression patterns.
3. **Test pyramid:** `vitest` supplies fast unit/type/component coverage while `playwright-best-practices` supplies cross-page/browser/integration confidence.
4. **Feedback loop:** `ship`, QA, deploy, and canary artifacts feed `retro`.

## Conflict hypotheses

1. **Browser-driver conflict:** `playwright` prefers `playwright-cli`; gstack roots prefer Aside with `$B` fallback. A fused capability should expose a driver adapter rather than silently replacing the stronger gstack privacy/consent contract.
2. **QA source-reading conflict:** `qa-only` says never read source, yet diff-aware scoping requires tracing controllers/components/routes. This needs an explicit branch:
   - pure black-box mode forbids source reads;
   - diff-aware mode permits read-only source mapping but not source diagnosis/fixes.
3. **Canary comparison conflict:** alert semantics require identifying new errors and 404s, but persisted baseline/loop data do not support those comparisons fully.
4. **Ship scope conflict:** automatic test-framework bootstrap during release preparation can introduce unrelated infrastructure. Prefer a precondition or separate bootstrap dependency when no framework exists.

## Conditional-variant hypotheses

1. `audit-website` and `qa-only` are not duplicates:
   - choose `audit-website` for site-wide machine rules and source remediation;
   - choose `qa-only` for black-box functional evidence with no fixes.
2. `playwright` and `playwright-best-practices` are execution versus authoring variants.
3. Vitest Browser Mode and Playwright component testing are conditional variants selected by existing stack, browser fidelity, and whether full E2E wiring is required.
4. `retro global` is a cross-project variant of repo retro, with distinct storage and freshness behavior.
5. Apple distribution is a release-channel variant inside `ship`, but its account authority and durable external effects may justify an independent root.

## Strong-dependency hypotheses

1. `land-and-deploy` strongly depends on `ship` for a prepared PR and version/changelog consistency.
2. `land-and-deploy` depends on `canary` semantics for post-deploy health, but currently embeds a one-pass subset.
3. `ship` depends on `qa-only` for plan verification and on test-framework knowledge represented by `vitest`/Playwright references.
4. `retro` depends on stable machine-readable logs from `ship`, deploy, review, QA, and learnings.
5. `playwright` depends on `npx` and dynamically resolved `@playwright/cli`.

# Unresolved questions

1. Where were `qa/templates/qa-report-template.md` and `qa/references/issue-taxonomy.md` intended to live? Their absence blocks full `qa-only` support verification.
2. Should `qa-only` diff-aware mode formally permit read-only source mapping, resolving its contradiction with “Never read source code”?
3. Should canary baseline JSON persist normalized console-error identities and per-page link status so its advertised delta rules are executable?
4. Should `ship` test bootstrap be split into a prerequisite capability rather than mutating test infrastructure during release?
5. Are standalone/gstack duplicate roots intentionally retained for packaging compatibility, and which path is canonical for V2 provenance?
6. Should the Apple release adapter become a separate capability because it has different triggers, authority, credentials, side effects, and stop gates from repository shipping?
7. What installed Vitest version should govern V2 synthesis when this root mixes v4 guidance with v5 beta features?
8. Should the CLI-first `playwright` root inherit the non-local mutation, credential, and tab-privacy contract used by `qa-only` and `canary`?

---

## Review

- **Correct:** Every assigned root has a cited dossier; all ten `SKILL.md` files were read completely. Behavior-bearing `playwright_cli.sh` was reviewed rather than excluded by extension.
- **Finding: P1:** `qa-only` depends on two absent semantic support files, preventing full source verification. Smallest fix: restore `skills/qa/templates/qa-report-template.md` and `skills/qa/references/issue-taxonomy.md`, or update the root to valid paths.
- **Finding: P1:** `canary` promises identity-based console and link deltas that its persisted baseline and monitoring loop cannot compute. Smallest fix: persist normalized error/link sets and run link checks during each monitoring pass.
- **Finding: P2:** `qa-only` has a source-reading contract conflict between diff-aware mapping and black-box-only rules. Smallest fix: define separate black-box and diff-aware permissions.
- **Merge verdict:** **BLOCK** for Phase 1B completion of this assigned set until the missing `qa-only` sources are resolved or explicitly dispositioned by the authority.