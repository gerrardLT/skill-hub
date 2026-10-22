# Capability Compiler V2 — Phase 1B Semantic Audit: gstack Tooling Roots

## Audit scope and evidence policy

Assigned roots: 20. All assigned `SKILL.md` files were read completely in bounded chunks. Nested roots were reviewed independently; no parent-root summary is used as proof for a child root. Support files were classified as:

- **semantic-read**: prose, reference, template, or example contributes capability meaning.
- **behavior-reviewed**: executable code was inspected far enough to establish material behavior, gates, side effects, or dependency contracts.
- **excluded**: generated duplicates, test fixtures, historical plans, or implementation internals that do not add reusable semantic method. The exclusion reason is stated.

The Phase 1 contract requires per-root dossiers, explicit support-file classification, and source-backed relationship hypotheses; omitted roots or unclassified behavior-bearing scripts fail the phase gate [`.specs/capability-compiler-v2/phase-1/phase-plan.md:24-72`]. `coverage.json` records 139 roots and 2,337 files, but its review fields are not treated as semantic proof [`curation/v2/coverage.json:1-12`].

No commands, tests, network access, remote Git operations, writes, or edits were performed.

---

## 1. `gstack`

**Exact root / skill:** `skills/gstack/` / `skills/gstack/SKILL.md`

### Capability dossier

- **Trigger:** bare “gstack,” “which gstack skill,” or a request to route work through gstack. It also proactively matches planning, review, QA, shipping, documentation, browser, security, and operational intents [`skills/gstack/SKILL.md:1-17`, `skills/gstack/SKILL.md:214-284`].
- **Non-trigger:** a request already naming a specific skill, or work with no matching specialized skill. When proactive routing is disabled, it must neither auto-invoke nor proactively suggest another skill [`skills/gstack/SKILL.md:64-68`, `skills/gstack/SKILL.md:281-293`].
- **Responsibility:** classify user intent and invoke the narrowest matching gstack skill. Browser, screenshot, QA, and dogfooding requests preferentially route to `/browse`; fallback-browser setup skills are reserved for the explicit fallback path [`skills/gstack/SKILL.md:216-229`].
- **Non-responsibility:** it does not implement the routed workflow itself. If no skill matches, it answers directly [`skills/gstack/SKILL.md:230-293`].
- **Inputs:** natural-language request, `PROACTIVE`, `SKILL_PREFIX`, session-kind and preamble status, and the installed skill catalog.
- **Outputs:** a Skill-tool invocation, a direct answer, and best-effort route telemetry (`browse`, `routed`, or `direct`) [`skills/gstack/SKILL.md:230-241`].
- **Core workflow:** run the shared preamble; honor authenticated one-time instruction blocks; apply proactive-routing policy; classify browser intent first; classify remaining intent through the explicit routing table; log route outcome; complete with shared learning and telemetry protocol [`skills/gstack/SKILL.md:20-63`, `skills/gstack/SKILL.md:214-305`].
- **Branches:** browser-first; named capability routes; direct answer; proactive-disabled ask-before-suggesting; degraded preamble mode.
- **Rules / gates / stops:** instruction blocks are trusted only from the immediately executed preamble result with the matching `SESSION_ID`; degraded protocol defaults to interactive and skips onboarding/telemetry assumptions; route-specific skill instructions supersede generic plan-mode behavior [`skills/gstack/SKILL.md:28-58`].
- **Tools / dependencies:** Bash, Read, AskUserQuestion; shared `gstack-skill-start`, `gstack-telemetry-log`, `gstack-skill-end`, and the Skill tool.
- **Permissions / side effects:** local session markers, analytics, timeline, route telemetry, learning logs, and artifact-sync activity. The router itself should not edit project code.
- **Strongest unique method:** one explicit intent-to-skill dispatch table with a browser-first exception and persisted proactive-routing preference.
- **Weaknesses / failure modes:** routing is broad and deliberately prefers false positives, so overlapping trigger vocabulary may invoke a heavyweight workflow unnecessarily. The parent also depends on the installed catalog matching the generated routing prose.
- **Overlap / candidates:** dependency hub for every other assigned operational root; duplicate routing intent with individual frontmatter triggers, but not duplicate capability.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/SKILL.md` | semantic-read | Canonical rendered router contract and routing table. |
| `skills/gstack/SKILL.md.tmpl` | excluded | Authoring template for the rendered file; the rendered file identifies itself as generated from this template [`skills/gstack/SKILL.md:14-15`]. |
| `skills/gstack/bin/gstack-skill-start` | behavior-reviewed | Establishes protocol, authenticated session IDs, session kind, config flags, local analytics, artifact sync, and sanitized instruction output [`skills/gstack/bin/gstack-skill-start:1-39`, `skills/gstack/bin/gstack-skill-start:66-163`, `skills/gstack/bin/gstack-skill-start:225-300`]. |
| `skills/gstack/bin/gstack-skill-end` | behavior-reviewed | Drains artifact sync and writes timeline/local/optional remote telemetry at completion [`skills/gstack/bin/gstack-skill-end:1-82`]. |
| `skills/gstack/*/SKILL.md` | excluded from parent dossier | Independent nested skill roots, not evidence that the parent implements their workflows. Assigned nested roots are audited separately below. |
| `skills/gstack/{agents,claude,openclaw,extension,lib,test}/**` | excluded | Host adapters, implementation internals, or tests; not part of the router’s semantic responsibility. |

---

## 2. `gstack/browse`

**Exact root / skill:** `skills/gstack/browse/` / `skills/gstack/browse/SKILL.md`

### Capability dossier

- **Trigger:** opening a page, testing a page or flow, taking screenshots, checking console errors, or one-off browser dogfooding [`skills/gstack/browse/SKILL.md:1-20`].
- **Non-trigger:** full QA/design/performance audits; pure local HTML rendering; fallback-browser cookie import/pairing; vendor-dashboard action without the third-party action contract [`skills/gstack/browse/SKILL.md:376-444`].
- **Responsibility:** provide deterministic “eyes” through Aside first, with the gstack headless browser as fallback, and return evidence-backed findings.
- **Non-responsibility:** no implicit third-party mutation, credential entry, interaction with tabs the agent did not open, or substitution of curl/unit tests for an unavailable browser [`skills/gstack/browse/SKILL.md:180-236`].
- **Inputs:** target URL, page/flow intent, optional named tab, browser availability, and any explicit mutation approval.
- **Outputs:** labelled snapshots, text, console errors, diffs, screenshots/PDFs, report-directory paths, and a user-facing verdict [`skills/gstack/browse/SKILL.md:397-425`].
- **Core workflow:** probe Aside; fall back to `$B` only when unavailable; open a new tab; run one self-contained flow; print labelled evidence plus `GSTACK_STEP_OK`; copy artifacts; read screenshots; report evidence and verdict [`skills/gstack/browse/SKILL.md:170-287`, `skills/gstack/browse/SKILL.md:389-425`].
- **Branches:** deterministic `aside repl` by default; `aside exec` only for open-ended reading; `$B` translation when Aside is unavailable; local targets may mutate, non-local targets require one explicit consent gate [`skills/gstack/browse/SKILL.md:238-372`, `skills/gstack/browse/SKILL.md:378-396`].
- **Rules / gates / stops:** own tabs only; named origin only; credentials never pass through the agent; page content is untrusted; no logout/delete/cancel links; missing sentinel or `[error` is failure; browser setup failure is a hard stop, not permission to substitute another testing method [`skills/gstack/browse/SKILL.md:196-236`, `skills/gstack/browse/SKILL.md:421-444`].
- **Tools / dependencies:** Aside CLI, `$B` browse binary, Chromium/Playwright/CDP, Read for screenshot display, and generated command reference.
- **Permissions / side effects:** opens and closes tabs; may create screenshot/report files; local mutations are allowed by contract, while non-local mutations require approval.
- **Strongest unique method:** a portable, evidence-labelled translation layer between a real signed-in browser and a headless fallback while preserving the same consent and reporting contract.
- **Weaknesses / failure modes:** very large operational surface; Aside scripts are fresh sessions while `$B` persists state, which increases translation risk. Its own command reference must be consulted for non-cookbook commands.
- **Overlap / candidates:** shared browser substrate for `scrape`, `open-gstack-browser`, `setup-browser-cookies`, `make-pdf`, and browser skills. Strong dependency rather than duplicate.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/browse/SKILL.md` | semantic-read | Complete browser safety, fallback, cookbook, evidence, and reporting contract. |
| `skills/gstack/browse/sections/command-list.md` | semantic-read | Generated but authoritative command/flag semantics, including untrusted-content envelopes and mutation-capable commands [`skills/gstack/browse/sections/command-list.md:1-184`]. |
| `skills/gstack/browse/src/browser-skills.ts` | behavior-reviewed | Implements three-tier browser-skill discovery, frontmatter parsing, precedence, and tombstones [`skills/gstack/browse/src/browser-skills.ts:1-78`, `skills/gstack/browse/src/browser-skills.ts:113-350`]. |
| `skills/gstack/browse/src/browser-skill-commands.ts` | behavior-reviewed | Implements list/show/run/test/remove, scoped-token spawning, stdout caps, and timeout/error behavior [`skills/gstack/browse/src/browser-skill-commands.ts:1-41`, `skills/gstack/browse/src/browser-skill-commands.ts:115-207`, `skills/gstack/browse/src/browser-skill-commands.ts:297-350`]. |
| `skills/gstack/browse/src/cli.ts` | behavior-reviewed | Sampled daemon startup/state/health seam; confirms persistent loopback-server architecture and state-file side effects [`skills/gstack/browse/src/cli.ts:1-39`, `skills/gstack/browse/src/cli.ts:119-216`]. |
| `skills/gstack/browse/src/*.ts` excluding files above | excluded | Browser daemon implementation internals. They support the command contract but do not add a separate semantic workflow to `/browse`. |
| `skills/gstack/browse/test/**` | excluded | Test fixtures and implementation verification, not reusable capability content. |
| `skills/gstack/browse/PLAN-snapshot-dropdown-interactive.md` | excluded | Historical implementation plan, not current runtime contract. |
| `skills/gstack/browse/SKILL.md.tmpl`, `sections/*.tmpl`, `sections/manifest.json` | excluded | Generated-source duplicates and render metadata. |

---

## 3. `gstack/browser-skills/hackernews-frontpage`

**Exact root / skill:** `skills/gstack/browser-skills/hackernews-frontpage/` / `skills/gstack/browser-skills/hackernews-frontpage/SKILL.md`

### Capability dossier

- **Trigger:** Hacker News front-page scrape/top-story requests matching the declared phrases [`skills/gstack/browser-skills/hackernews-frontpage/SKILL.md:1-14`].
- **Non-trigger:** other HN pages, arbitrary sites, authenticated flows, mutation, or generalized crawling.
- **Responsibility:** navigate to HN, parse story rows, and emit a single JSON object containing ranked stories and count [`skills/gstack/browser-skills/hackernews-frontpage/SKILL.md:16-39`].
- **Non-responsibility:** browser setup, user interaction, multiple pages, or adaptable selector discovery.
- **Inputs:** no declared arguments; live HTML from `https://news.ycombinator.com/`.
- **Outputs:** `{stories:[{rank,id,title,url,points,comments}],count}`; job rows may have null points/comments [`skills/gstack/browser-skills/hackernews-frontpage/script.ts:15-38`, `skills/gstack/browser-skills/hackernews-frontpage/script.ts:139-148`].
- **Core workflow:** use the sibling browser SDK to `goto` and retrieve HTML; parse `tr.athing` rows; bound score/comment lookup before the next story; decode limited HTML entities; emit JSON [`skills/gstack/browser-skills/hackernews-frontpage/script.ts:40-113`, `skills/gstack/browser-skills/hackernews-frontpage/script.ts:139-148`].
- **Branches:** scored story, zero-comment “discuss,” and job posting with absent score/comments.
- **Rules / gates / stops:** trusted bundled skill; stable host; pure parser for fixture replay; nonzero runtime failure on daemon/network/parse failure.
- **Tools / dependencies:** Bun, bundled `browse-client`, gstack browser daemon, fixture-based Bun tests.
- **Permissions / side effects:** read-only page navigation and daemon commands; no repo writes.
- **Strongest unique method:** a small reference implementation pairing a pure fixture-testable parser with a scoped browser runtime.
- **Weaknesses / failure modes:** regex-based HTML parsing is tied to quoted attributes and HN’s current row shape; the entity decoder is intentionally incomplete. Fixture replay cannot detect a live-site markup change until the captured fixture is refreshed.
- **Overlap / candidates:** concrete example/template for `skillify`; dependency on `browse`; specialized variant of `scrape`, not a duplicate because it is deterministic and host-specific.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `.../SKILL.md` | semantic-read | Trigger, host, output, and reference-skill rationale. |
| `.../script.ts` | behavior-reviewed | Full parser and live execution path reviewed [`skills/gstack/browser-skills/hackernews-frontpage/script.ts:1-148`]. |
| `.../script.test.ts` | behavior-reviewed | Fixture assertions cover shape, entities, scores, comments, jobs, and malformed rows [`skills/gstack/browser-skills/hackernews-frontpage/script.test.ts:1-100`]. |
| `.../_lib/browse-client.ts` | behavior-reviewed | Scoped token/state-file auth, loopback dispatch, timeouts, and daemon command methods [`skills/gstack/browser-skills/hackernews-frontpage/_lib/browse-client.ts:1-77`, `skills/gstack/browser-skills/hackernews-frontpage/_lib/browse-client.ts:99-245`]. |
| `.../fixtures/hn-2026-04-26.html` | excluded | Captured test fixture; evidence for parser tests, not reusable semantic guidance. |

---

## 4. `gstack/codex`

**Exact root / skill:** `skills/gstack/codex/` / `skills/gstack/codex/SKILL.md`

### Capability dossier

- **Trigger:** Codex review, challenge, consultation, second opinion, or outside-model critique [`skills/gstack/codex/SKILL.md:1-23`].
- **Non-trigger:** ordinary in-model review where no independent model is requested; invocation from inside Codex unless explicitly forced.
- **Responsibility:** probe Codex CLI/auth/model/version; select one mutually exclusive mode; run in read-only sandbox; present output verbatim; add one actionable synthesis recommendation [`skills/gstack/codex/SKILL.md:501-596`, `skills/gstack/codex/SKILL.md:611-647`].
- **Non-responsibility:** modifying repository files, silently deciding based on Codex, or re-running the same Claude review.
- **Inputs:** user mode/focus/prompt, branch/base, diff or plan content, optional model and `--xhigh`, optional prior session ID.
- **Outputs:** full Codex reasoning/tool/final stream, token count, recommendation, optional session continuity file, and plan review report when a plan file is active.
- **Core workflow:** detect host/base; reject nested Codex; probe binary/auth/model/version; resolve portable roots; choose review/challenge/consult; apply filesystem boundary; execute with timeout and read-only sandbox; present full output; emit synthesis; update plan review status when applicable [`skills/gstack/codex/SKILL.md:501-647`, `skills/gstack/codex/SKILL.md:649-798`].
- **Branches:** review, challenge, consult; fresh vs resumed consult; plan review vs free-form consult; known model/auth/timeout failures.
- **Rules / gates / stops:** never modify files; output must be verbatim; scope flags must not be combined with a prompt; nested Codex is skipped; unavailable binary/auth/model is a hard stop; plan mode has a terminal review-report gate [`skills/gstack/codex/SKILL.md:796-853`].
- **Tools / dependencies:** Codex CLI, Python JSONL parser, Git/GitHub/GitLab base detection, shared Codex probe, timeout wrapper, plan/review logs.
- **Permissions / side effects:** intended repository access is read-only; consult writes `.context/codex-session-id`; telemetry and review logs may be written.
- **Strongest unique method:** independent-model review with explicit mode exclusivity, sandboxing, streamed reasoning, and a mandatory synthesis line.
- **Weaknesses / failure modes:** current Review-mode section is unusable: the generated support file consists only of Codex’s CLI error text, `error: the argument '[PROMPT]' cannot be used with '--base <BRANCH>'` [`skills/gstack/codex/sections/review-mode.md:1`]. Thus the skeleton’s hard STOP into that file cannot supply a working review procedure.
- **Overlap / candidates:** complements `/review` rather than duplicating it; document-release optionally depends on the same Codex probe/review pattern.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/codex/SKILL.md` | semantic-read | Mode selection, safety, error, reporting, and plan-report contract. |
| `skills/gstack/codex/sections/review-mode.md` | semantic-read | Read in full; currently malformed one-line CLI error, a concrete capability defect. |
| `skills/gstack/codex/sections/challenge-mode.md` | semantic-read | Complete adversarial prompt, JSONL streaming, timeout, and synthesis procedure [`skills/gstack/codex/sections/challenge-mode.md:1-134`]. |
| `skills/gstack/codex/sections/consult-mode.md` | semantic-read | Full session continuity, plan embedding, JSONL execution, and synthesis procedure [`skills/gstack/codex/sections/consult-mode.md:1-260`]. |
| `skills/gstack/codex/SKILL.md.tmpl`, `sections/*.tmpl`, `sections/manifest.json` | excluded | Generated-source duplicates and render metadata. |

---

## 5. `gstack/context-restore`

**Exact root / skill:** `skills/gstack/context-restore/` / `skills/gstack/context-restore/SKILL.md`

### Capability dossier

- **Trigger:** resume, restore context, “where was I,” or pick up saved work [`skills/gstack/context-restore/SKILL.md:1-23`].
- **Non-trigger:** saving state, implementing remaining work, or listing via the restore command; listing is redirected to `/context-save list`.
- **Responsibility:** select and present the correct saved checkpoint, preferring the current branch while retaining cross-branch fallback.
- **Non-responsibility:** code changes or checkpoint creation [`skills/gstack/context-restore/SKILL.md:390-414`, `skills/gstack/context-restore/SKILL.md:548-562`].
- **Inputs:** optional title fragment/number, current branch, checkpoint directory, checkpoint frontmatter/body.
- **Outputs:** structured resume summary, branch mismatch warning, and next-step choice.
- **Core workflow:** enumerate up to 200 filename-sorted checkpoints; partition current-branch files before others; cap candidates at 20; choose explicit match or first candidate; read and present; ask whether to continue, show full file, or stop [`skills/gstack/context-restore/SKILL.md:415-546`].
- **Branches:** explicit checkpoint; latest current-branch checkpoint; latest other-branch fallback; no checkpoints; `list` redirect.
- **Rules / gates / stops:** filename timestamp, not mtime, is canonical; do not hard-filter other branches; never implement code.
- **Tools / dependencies:** Git branch lookup, shared slug/paths helpers, find/sort/grep, Read, AskUserQuestion.
- **Permissions / side effects:** read-only apart from common preamble/telemetry.
- **Strongest unique method:** stable current-branch-first ordering without sacrificing cross-worktree handoff.
- **Weaknesses / failure modes:** matching a title fragment among only the capped 20 candidates can miss an older requested checkpoint; the 200-file scan ceiling can also hide an older current-branch checkpoint during extreme sibling-worktree bursts.
- **Overlap / candidates:** strong pair/dependency with `context-save`; former `/checkpoint` naming is intentionally retired.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/context-restore/SKILL.md` | semantic-read | Entire checkpoint selection and presentation contract. |
| `skills/gstack/context-restore/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| Shared `bin/gstack-{slug,paths}` | excluded | External shared path-resolution internals; invocation contract is fully stated in the skill. |

---

## 6. `gstack/context-save`

**Exact root / skill:** `skills/gstack/context-save/` / `skills/gstack/context-save/SKILL.md`

### Capability dossier

- **Trigger:** save progress/state/work, or context save [`skills/gstack/context-save/SKILL.md:1-22`].
- **Non-trigger:** restore/resume, which is redirected to `/context-restore`; ordinary code implementation.
- **Responsibility:** capture branch, modified files, decisions, remaining work, notes, and optional duration in an append-only Markdown checkpoint.
- **Non-responsibility:** modifying project code or overwriting/deleting prior checkpoints [`skills/gstack/context-save/SKILL.md:388-409`, `skills/gstack/context-save/SKILL.md:628-647`].
- **Inputs:** optional title, conversation context, Git state/log/diff stats, session start time.
- **Outputs:** a new timestamped checkpoint file or a branch-filtered checkpoint listing.
- **Core workflow:** detect save/list; collect Git state; synthesize summary; compute duration; sanitize title in Bash; create collision-safe filename; write frontmatter/body; confirm restore command. List mode reads checkpoint frontmatter and defaults to current branch [`skills/gstack/context-save/SKILL.md:410-627`].
- **Branches:** inferred/provided title; save/list/all-branches list; same-second collision; unknown duration.
- **Rules / gates / stops:** filenames are append-only; shell-side allowlist sanitization; branch always recorded; infer rather than interrogate; code stays untouched.
- **Tools / dependencies:** Git, shared slug/paths helpers, filesystem write, `/dev/urandom`, AskUserQuestion only if title cannot be inferred.
- **Permissions / side effects:** writes under the user’s gstack checkpoint state, not the project source tree.
- **Strongest unique method:** collision-safe, sanitized, branch-aware durable context packets.
- **Weaknesses / failure modes:** quality depends on conversation-derived summarization; `files_modified` captures Git status, not untracked conversational artifacts outside Git.
- **Overlap / candidates:** complements and is a strong dependency of `context-restore`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/context-save/SKILL.md` | semantic-read | Full save/list schemas, sanitization, and append-only rules. |
| `skills/gstack/context-save/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| Shared `bin/gstack-{slug,paths}` | excluded | External path helpers, not additional checkpoint semantics. |

---

## 7. `gstack/document-generate`

**Exact root / skill:** `skills/gstack/document-generate/` / `skills/gstack/document-generate/SKILL.md`

### Capability dossier

- **Trigger:** write/generate documentation, document a feature/module/project, create tutorial/how-to, or explain a module [`skills/gstack/document-generate/SKILL.md:1-25`].
- **Non-trigger:** post-release synchronization of existing documentation, which belongs to `document-release`.
- **Responsibility:** research code and tests, partition documentation by Diataxis, produce accurate docs, cross-link them, verify quality, and optionally commit/push.
- **Non-responsibility:** release-diff auditing, CHANGELOG preservation policy, or merely flagging gaps.
- **Inputs:** target scope, project/source/test files, existing documentation conventions, output-placement choice.
- **Outputs:** reference, explanation, how-to, and/or tutorial files; updated entry points; commit/PR documentation table [`skills/gstack/document-generate/SKILL.md:477-872`].
- **Core workflow:** confirm scope/location; map codebase; read implementation/tests/dependencies; build concept map; choose Diataxis quadrants; write reference first, then explanation/how-to/tutorial; cross-link; self-review; redact staged content; commit/push and update PR [`skills/gstack/document-generate/SKILL.md:477-832`].
- **Branches:** standalone vs called from release; entity type determines quadrants; more than five documents requires confirmation; existing docs framework vs plain Markdown.
- **Rules / gates / stops:** research before writing; every claim traceable to code; tutorial result within three steps; how-to troubleshooting where failure is possible; staged secret scan blocks HIGH findings.
- **Tools / dependencies:** Read/Grep/Glob, Git, docs framework conventions, redaction helper, GitHub PR tooling.
- **Permissions / side effects:** creates/edits docs, stages named files, commits, pushes, and may update PR body.
- **Strongest unique method:** explicit “research the whole, then write the parts” concept map followed by quadrant-specific templates and gates.
- **Weaknesses / failure modes:** default workflow is large and publication-oriented even for small documentation requests; pushing is built into the standard flow and therefore needs repository authority.
- **Overlap / candidates:** `document-release` should delegate critical coverage gaps here; `make-pdf` may publish the generated Markdown but does not author it.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/document-generate/SKILL.md` | semantic-read | Complete Diataxis production workflow and quality gates. |
| `skills/gstack/document-generate/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| No local references/scripts/examples | excluded | Root contains only rendered skill and template; execution uses shared repo tools. |

---

## 8. `gstack/document-release`

**Exact root / skill:** `skills/gstack/document-release/` / `skills/gstack/document-release/SKILL.md`

### Capability dossier

- **Trigger:** update/sync docs after shipping, document what changed, or post-ship docs [`skills/gstack/document-release/SKILL.md:1-22`].
- **Non-trigger:** authoring missing documentation from scratch, pre-feature documentation, or general copywriting.
- **Responsibility:** compare branch diff to all relevant docs, build a Diataxis coverage map, apply safe factual updates, preserve CHANGELOG history, clean TODOs, gate VERSION changes, commit/push, and report documentation debt.
- **Non-responsibility:** auto-generating missing pages; architecture diagram edits; silent VERSION changes [`skills/gstack/document-release/SKILL.md:501-599`].
- **Inputs:** base branch, branch diff/log/file list, all project docs, VERSION, CHANGELOG, TODOs, optional Codex availability.
- **Outputs:** updated documentation commit, PR/MR Documentation section/title, coverage/debt report, and optional cross-model findings.
- **Core workflow:** abort on base branch; classify diff; map public-surface coverage; inspect each doc; auto-fix factual drift; ask on narrative risk; voice-polish but never clobber CHANGELOG; cross-check docs; clean TODOs; gate VERSION; commit/push; update PR/MR; run informational independent review [`skills/gstack/document-release/SKILL.md:466-599`, `skills/gstack/document-release/sections/release-body.md:1-191`, `skills/gstack/document-release/sections/release-body.md:193-500`].
- **Branches:** GitHub/GitLab; no docs changed; VERSION already bumped/not bumped; spawned mode; Codex ready/disabled/unavailable; apply-all/per-finding/skip findings.
- **Rules / gates / stops:** full-file read before editing; no CHANGELOG overwrite; exact-string edits only; VERSION always gated; architecture diagrams advisory; base-branch execution aborts.
- **Tools / dependencies:** Git, gh/glab, Codex or fallback reviewer, redact/issue-guard/review-log helpers, AskUserQuestion.
- **Permissions / side effects:** edits docs/TODO/VERSION when approved, commits, pushes, and mutates PR/MR body/title.
- **Strongest unique method:** blast-radius coverage map plus a conservative auto-update boundary separating factual drift from narrative decisions.
- **Weaknesses / failure modes:** despite claiming post-ship scope, it performs commits/pushes and PR mutations, so it is not a pure audit. The optional fallback reviewer described in the support section requires subagent capability, introducing host dependence.
- **Overlap / candidates:** complementary with `document-generate`; overlaps ship/release automation but owns documentation consistency.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/document-release/SKILL.md` | semantic-read | Entry, coverage-map, boundaries, and delegated section index. |
| `skills/gstack/document-release/sections/release-body.md` | semantic-read | Full per-file audit, CHANGELOG/TODO/VERSION/commit/PR/review procedure [`skills/gstack/document-release/sections/release-body.md:1-500`, `skills/gstack/document-release/sections/release-body.md:501-567`]. |
| `skills/gstack/document-release/SKILL.md.tmpl`, `sections/release-body.md.tmpl`, `sections/manifest.json` | excluded | Generated-source duplicates and render metadata. |

---

## 9. `gstack/gstack-upgrade`

**Exact root / skill:** `skills/gstack/gstack-upgrade/` / `skills/gstack/gstack-upgrade/SKILL.md`

### Capability dossier

- **Trigger:** upgrade/update gstack or get the latest version [`skills/gstack/gstack-upgrade/SKILL.md:1-18`].
- **Non-trigger:** general dependency updates or application upgrades.
- **Responsibility:** detect install type, update safely, run setup and version migrations, reconcile vendored copies, stop stale browser daemon, clear markers, and summarize release notes.
- **Non-responsibility:** updating arbitrary project dependencies or discarding local gstack changes without a destructive confirmation.
- **Inputs:** update-check result, install layout, old/new VERSION, Git dirt/unpushed commits, team mode, migration set.
- **Outputs:** upgraded install, optional vendored-copy sync/removal, migrated state, stopped stale daemon, update markers, changelog summary.
- **Core workflow:** optional auto-upgrade gate; detect global/local git or vendored install; save old version; fast-forward with autostash; gate hard-reset fallback; transactional vendored swap; reconcile local vendored copy; run newer migrations; stop stale responsive daemon; write markers; summarize changelog [`skills/gstack/gstack-upgrade/SKILL.md:20-354`].
- **Branches:** auto/manual; git/vendored; clean/diverged; team/non-team; stale backup; responsive/busy/current daemon; already-current install.
- **Rules / gates / stops:** stale `.bak` aborts; hard reset requires proof or explicit one-way consent; failed vendored swap restores old install; busy daemon is not killed.
- **Tools / dependencies:** Git, Bash, setup script, update checker, config, filesystem, curl for daemon health, migration scripts.
- **Permissions / side effects:** network fetch/clone, install replacement, Git reset/stash, setup execution, local repo `.gitignore` changes, daemon stop, state-marker writes.
- **Strongest unique method:** fail-safe upgrade across multiple installation topologies with explicit backup and divergence handling.
- **Weaknesses / failure modes:** `sort -V` and Bash/Unix utilities constrain portability; version migration comparison assumes comparable dotted-version structure.
- **Overlap / candidates:** shared maintenance dependency referenced by every degraded preamble; distinct from app deployment.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/gstack-upgrade/SKILL.md` | semantic-read | Complete upgrade and rollback contract. |
| `skills/gstack/gstack-upgrade/migrations/v*.sh` | behavior-reviewed | Migration execution contract reviewed in the skill; newest migration sampled to verify idempotent, state-only behavior [`skills/gstack/gstack-upgrade/SKILL.md:239-268`, `skills/gstack/gstack-upgrade/migrations/v1.78.0.0.sh:1-30`]. |
| `skills/gstack/gstack-upgrade/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |

---

## 10. `gstack/landing-report`

**Exact root / skill:** `skills/gstack/landing-report/` / `skills/gstack/landing-report/SKILL.md`

### Capability dossier

- **Trigger:** landing report, version/ship queue, open PR versions, or next version slot [`skills/gstack/landing-report/SKILL.md:1-20`].
- **Non-trigger:** claiming, bumping, merging, or deploying a version.
- **Responsibility:** render a read-only snapshot of claimed versions, active sibling worktrees, collisions, and next candidate versions.
- **Non-responsibility:** mutate VERSION, refs, PRs, or worktrees.
- **Inputs:** base/current VERSION, open PR/MR queue, workspace root, sibling branches and last-commit times.
- **Outputs:** fixed dashboard with online/offline status, claims, sibling activity, proposed micro/patch/minor/major slots, and one next-action note [`skills/gstack/landing-report/SKILL.md:393-539`].
- **Core workflow:** detect base; read branch/base versions; invoke `gstack-next-version` for each bump level; use patch JSON as canonical queue/sibling data; render collision and active-sibling indicators.
- **Branches:** online/unknown/offline host; collision; active sibling outranks branch; clean queue.
- **Rules / gates / stops:** declared read-only; plan-mode safe; offline mode must disclose missing queue awareness.
- **Tools / dependencies:** Git, gh, Bun, jq, `gstack-next-version`.
- **Permissions / side effects:** the skill claims no mutation, but Step 2 runs `git fetch`, which updates remote-tracking refs and contradicts the “no git mutations” description [`skills/gstack/landing-report/SKILL.md:382-391`, `skills/gstack/landing-report/SKILL.md:404-411`]. The shared utility also performs best-effort fetches and remote/API reads.
- **Strongest unique method:** version collision analysis that combines PR claims and fresh un-PR’d Conductor sibling work.
- **Weaknesses / failure modes:** the skill-level claim of complete read-only behavior conflicts with its explicit `git fetch`; offline display can be conservative because stale refs may count deleted branches.
- **Overlap / candidates:** read-only frontend to the same allocator used by `/ship`; dependency on `gstack-next-version`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/landing-report/SKILL.md` | semantic-read | Dashboard contract and exact display format. |
| `skills/gstack/bin/gstack-next-version` | behavior-reviewed | Host-aware queue, git fallback, sibling scan, width-preserving version arithmetic, and warnings reviewed [`skills/gstack/bin/gstack-next-version:1-90`, `skills/gstack/bin/gstack-next-version:351-824`]. |
| `skills/gstack/landing-report/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |

---

## 11. `gstack/make-pdf`

**Exact root / skill:** `skills/gstack/make-pdf/` / `skills/gstack/make-pdf/SKILL.md`

### Capability dossier

- **Trigger:** Markdown-to-PDF/export/generate document requests [`skills/gstack/make-pdf/SKILL.md:1-27`].
- **Non-trigger:** authoring document content, local design generation, or arbitrary webpage QA.
- **Responsibility:** render Markdown into polished PDF, self-contained HTML, or content-fidelity DOCX with layout, image, diagram, accessibility, and offline-network controls.
- **Non-responsibility:** create new diagram source from prose, silently fetch remote images, or guarantee identical Word layout.
- **Inputs:** Markdown path, output path/format, page/layout/branding/network/strict flags.
- **Outputs:** one output path on stdout; progress on stderr; PDF/HTML/DOCX artifact and documented exit code [`skills/gstack/make-pdf/SKILL.md:55-77`, `skills/gstack/make-pdf/SKILL.md:379-397`].
- **Core workflow:** resolve built binary; read Markdown; extract diagram fences; render/sanitize HTML; render diagram slots; inline and policy-check images; emit HTML/DOCX directly or print PDF through Aside/headless fallback [`skills/gstack/make-pdf/SKILL.md:230-378`, `skills/gstack/make-pdf/src/orchestrator.ts:68-244`].
- **Branches:** PDF/HTML/DOCX; Aside/fallback browser; strict/warn image handling; remote image blocked/allowed; forced/automatic landscape; preview/generate/setup.
- **Rules / gates / stops:** no browser means exit 4 for PDF; remote images blocked by default; out-of-tree/oversized/non-regular files warn or fail under `--strict`; stdout path-only contract; diagrams fail visibly, not silently.
- **Tools / dependencies:** Bun binary, Aside or gstack browser, Paged.js, Mermaid/Excalidraw bundle, `html-to-docx`, optional fonts and `pdftotext`.
- **Permissions / side effects:** reads local/optional remote images, writes artifacts under explicit path or temp, opens preview browser, may install fonts during setup.
- **Strongest unique method:** secure, offline-first publication pipeline with visible diagram diagnostics and conservative per-image landscape promotion.
- **Weaknesses / failure modes:** preview intentionally skips full diagram/image preprocessing, so preview is not pixel-equivalent to generated output [`skills/gstack/make-pdf/src/orchestrator.ts:250-310`]. Linux emoji/font quality depends on optional system fonts.
- **Overlap / candidates:** depends on browser rendering but is not browser QA; complements `document-generate`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/make-pdf/SKILL.md` | semantic-read | Complete usage, flags, security posture, output, and troubleshooting reference. |
| `skills/gstack/make-pdf/src/cli.ts` | behavior-reviewed | Argument parser, boolean flags, output-format validation, exit mapping, stdout contract [`skills/gstack/make-pdf/src/cli.ts:1-211`]. |
| `skills/gstack/make-pdf/src/orchestrator.ts` | behavior-reviewed | End-to-end format/render/browser/file pipeline [`skills/gstack/make-pdf/src/orchestrator.ts:1-244`]. |
| `skills/gstack/make-pdf/src/image-policy.ts` | behavior-reviewed | Directive grammar and conservative landscape/width policy [`skills/gstack/make-pdf/src/image-policy.ts:1-217`]. |
| `skills/gstack/make-pdf/src/diagram-prepass.ts` | behavior-reviewed | Fence extraction, placeholder/sanitization architecture, strict image ceilings [`skills/gstack/make-pdf/src/diagram-prepass.ts:1-220`]. |
| Remaining `src/*.ts` | excluded | Supporting render/CSS/engine implementation; no additional user workflow beyond reviewed seams. |
| `skills/gstack/make-pdf/test/**` | excluded | Tests and fixtures, not reusable semantic content. |
| `skills/gstack/make-pdf/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |

---

## 12. `gstack/open-gstack-browser`

**Exact root / skill:** `skills/gstack/open-gstack-browser/` / `skills/gstack/open-gstack-browser/SKILL.md`

### Capability dossier

- **Trigger:** open/launch GStack Browser or Chromium, show/control the browser, side panel [`skills/gstack/open-gstack-browser/SKILL.md:1-21`].
- **Non-trigger:** ordinary Aside-first browsing when the user has not explicitly chosen the fallback browser path.
- **Responsibility:** build if approved, clean stale browser state, launch headed gstack Chromium, verify mode/port/extension, guide side-panel setup, and demonstrate live activity.
- **Non-responsibility:** general page audit or cookie import; user’s regular Chrome remains untouched.
- **Inputs:** built browse binary, repo state file, extension path, user confirmation that side panel is visible.
- **Outputs:** visible headed browser, status/port/extension details, HN demonstration, and operational next steps.
- **Core workflow:** locate binary; ask before setup; kill stale server and lock files; `$B connect`; verify headed mode and port 34567; guide extension; branch on user-visible result; demo `goto`/`snapshot`; explain sidebar chat [`skills/gstack/open-gstack-browser/SKILL.md:181-386`].
- **Branches:** setup needed; extension missing; server unhealthy; browser invisible; successful side panel.
- **Rules / gates / stops:** setup requires consent; mode must be headed; errors/status are shown before proceeding.
- **Tools / dependencies:** `$B`, Chromium/Playwright, extension manifest, optional Bun installer with pinned checksum.
- **Permissions / side effects:** kills existing browse daemon by PID, removes state/lock files, launches persistent browser/profile and sidebar agent, visits HN.
- **Strongest unique method:** observable headed browser plus extension activity feed and isolated sidebar agent.
- **Weaknesses / failure modes:** pre-flight unconditionally terminates an existing browse server and then uses `kill -9`; this can destroy live tabs/session state and is more aggressive than the busy-daemon deferral rule in upgrade/browser workflows [`skills/gstack/open-gstack-browser/SKILL.md:218-235`].
- **Overlap / candidates:** fallback visualization/setup complement to `/browse`; cookie setup is separate.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/open-gstack-browser/SKILL.md` | semantic-read | Complete launch, cleanup, extension, and demo workflow. |
| `skills/gstack/open-gstack-browser/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| Shared `browse/src/**` and `extension/**` | excluded | Browser/extension implementation belongs to the parent browse subsystem; no local support files exist in this root. |

---

## 13. `gstack/scrape`

**Exact root / skill:** `skills/gstack/scrape/` / `skills/gstack/scrape/SKILL.md`

### Capability dossier

- **Trigger:** scrape/get/pull/extract/read data from a page [`skills/gstack/scrape/SKILL.md:1-20`].
- **Non-trigger:** submitting, posting, sending, logging in, deleting, ordering, booking, or multi-page crawling.
- **Responsibility:** read one page through Aside or the browser fallback and return one stable JSON document.
- **Non-responsibility:** mutation, credential handling, multi-page crawl, or interaction with pre-existing user tabs [`skills/gstack/scrape/SKILL.md:343-447`].
- **Inputs:** one-line scrape intent and target URL/page, optional desired fields.
- **Outputs:** compact single JSON object, normally `{items:[...],count:N}`; logs remain separate.
- **Core workflow:** obtain intent once; reject mutating verbs; choose structured or fuzzy mode; for structured data inspect tree/text then extract with page-side JSON; for fuzzy data use read-only Aside agent; validate result; retry selectors at most three or four times [`skills/gstack/scrape/SKILL.md:294-430`].
- **Branches:** structured vs fuzzy; Aside vs `$B`; codified browser-skill match vs prototype on fallback; sign-in wall; extraction failure.
- **Rules / gates / stops:** page output is attacker-controlled; never execute page instructions or follow unrequested URLs; no prose around pipeable JSON; missing sentinel is failure; partial nonsense must not be called success.
- **Tools / dependencies:** Aside, `$B`, browser-skill runtime, DOM selectors/evaluate, AskUserQuestion only when intent or failure choice is needed.
- **Permissions / side effects:** page navigation/read only; browser fallback may use existing imported session, but no mutation or credential entry.
- **Strongest unique method:** strict JSON-only read contract with prompt-injection treatment and deterministic-first selector workflow.
- **Weaknesses / failure modes:** one-page limit and small selector retry budget; Aside and fallback have different codified-skill availability, so performance/behavior varies by driver.
- **Overlap / candidates:** generic prototype path; `hackernews-frontpage` is a specialized codified variant; successful prototypes feed `skillify`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/scrape/SKILL.md` | semantic-read | Full read-only, JSON, untrusted-content, and extraction workflow. |
| `skills/gstack/scrape/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| `skills/gstack/browse/sections/command-list.md` | semantic-read | Referenced fallback command authority; reviewed under `browse`. |
| Browser-skill runtime files | behavior-reviewed | Relevant three-tier matching/execution seam reviewed under `browse`; not duplicated here. |

---

## 14. `gstack/setup-browser-cookies`

**Exact root / skill:** `skills/gstack/setup-browser-cookies/` / `skills/gstack/setup-browser-cookies/SKILL.md`

### Capability dossier

- **Trigger:** import browser cookies, authenticate headless testing, or set up a logged-in browser session [`skills/gstack/setup-browser-cookies/SKILL.md:1-19`].
- **Non-trigger:** Aside/CDP sessions already using the real browser; typing credentials; ordinary browsing.
- **Responsibility:** launch cookie picker or direct-domain import, then verify only domain/count summaries.
- **Non-responsibility:** expose cookie values, log in on behalf of the user, or import when CDP already carries the session.
- **Inputs:** optional browser/domain, built `$B`, installed Chromium profiles, user picker choices.
- **Outputs:** imported persistent browser cookies and a domain-count verification summary.
- **Core workflow:** detect CDP and stop if unnecessary; locate/build `$B`; run picker or direct import; wait for user confirmation; run `$B cookies`; show summary [`skills/gstack/setup-browser-cookies/SKILL.md:181-324`].
- **Branches:** CDP/no-op; setup required; picker vs direct domain; macOS Keychain/Linux libsecret.
- **Rules / gates / stops:** build requires approval; only domain names/counts shown; cookie values not exposed.
- **Tools / dependencies:** browse binary, Chromium cookie stores, OS credential decryption, interactive picker.
- **Permissions / side effects:** decrypts selected browser cookies and writes them into the persistent Playwright session.
- **Strongest unique method:** user-controlled domain picker that avoids exposing cookie values to the agent.
- **Weaknesses / failure modes:** direct example hardcodes `comet` unless the browser is specified/detected; OS keychain/libsecret availability may block import.
- **Overlap / candidates:** fallback-only authentication dependency for `browse`/`scrape`; unnecessary with Aside/CDP.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/setup-browser-cookies/SKILL.md` | semantic-read | Complete setup/import/verification contract. |
| `skills/gstack/setup-browser-cookies/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| `skills/gstack/browse/src/cookie-import-browser.ts` and `cookie-picker-*.ts` | excluded | Direct implementation internals; user-visible semantics are fully specified in the skill. |
| `skills/gstack/browse/test/cookie-*.test.ts` | excluded | Test fixtures and implementation verification. |

---

## 15. `gstack/setup-deploy`

**Exact root / skill:** `skills/gstack/setup-deploy/` / `skills/gstack/setup-deploy/SKILL.md`

### Capability dossier

- **Trigger:** configure/setup deployment, deploy platform, or land-and-deploy integration [`skills/gstack/setup-deploy/SKILL.md:1-21`].
- **Non-trigger:** perform the deploy/merge itself.
- **Responsibility:** detect platform, production URL, deploy workflow/status/health checks/hooks, confirm them, and persist a normalized block in `CLAUDE.md`.
- **Non-responsibility:** deploy application code, install vendor tools, expose credentials, or silently operate external dashboards.
- **Inputs:** existing `CLAUDE.md`, platform config files, workflows, project type, optional vendor/browser choices and user confirmations.
- **Outputs:** `## Deploy Configuration` block, verification results, and next-step summary [`skills/gstack/setup-deploy/SKILL.md:501-629`].
- **Core workflow:** inspect existing config; detect Fly/Render/Vercel/Netlify/Heroku/Railway/workflows/project type; gather missing data; optionally drive vendor site under explicit consent; write/replace config; probe health/status; summarize.
- **Branches:** existing configuration; platform-specific automatic inference; custom/manual/no-deploy; Aside/gstack/manual third-party action; health verification failure.
- **Rules / gates / stops:** always confirm detected config before writing; third-party browsing requires one explicit site/action choice; payment/credentials/CAPTCHA remain human; secrets never enter chat/log/history.
- **Tools / dependencies:** Git/file detection, platform CLIs, curl, Aside or headed `$B`, CLAUDE.md.
- **Permissions / side effects:** writes project `CLAUDE.md`; may browse vendor dashboards after consent; health checks and CLI status calls may contact production.
- **Strongest unique method:** one project-local, human-auditable deployment contract consumed by later land-and-deploy runs.
- **Weaknesses / failure modes:** platform inference is filename-driven and can misclassify mixed deployments; verification failures are non-blocking, so stale/bad configuration can still be persisted.
- **Overlap / candidates:** dependency of `land-and-deploy`; shares third-party browser contract with `/browse`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/setup-deploy/SKILL.md` | semantic-read | Full platform detection, third-party action, persistence, and verification flow. |
| `skills/gstack/setup-deploy/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |
| Platform files in target repos | excluded | Runtime inputs, not support files in this skill root. |

---

## 16. `gstack/setup-gbrain`

**Exact root / skill:** `skills/gstack/setup-gbrain/` / `skills/gstack/setup-gbrain/SKILL.md`

### Capability dossier

- **Trigger:** setup/install/connect/start/configure gbrain; shortcut modes for repo policy, engine switch, provision resume, and orphan cleanup [`skills/gstack/setup-gbrain/SKILL.md:1-20`, `skills/gstack/setup-gbrain/SKILL.md:477-507`].
- **Non-trigger:** routine reindex/refresh of an already configured brain, which belongs to `sync-gbrain`.
- **Responsibility:** detect state, remediate broken local engines, select local/Supabase/remote topology, install/init, register MCP, set per-remote policy, configure artifact/transcript sync, persist `CLAUDE.md`, smoke-test, and report health.
- **Non-responsibility:** silently choose a storage topology, bypass repo trust, expose secrets, or auto-run server-admin commands.
- **Inputs:** detect JSON, topology choice, optional Supabase PAT/pooler URL or MCP URL/token, repo origin/policy, artifact/transcript choices.
- **Outputs:** working local or remote gbrain integration; MCP registration; trust-policy and sync configuration; `CLAUDE.md` blocks; GREEN/YELLOW/RED verdict.
- **Core workflow:** acquire single-run lock; detect state; branch shortcuts; remediate broken engine if needed; select path; install local CLI where required; initialize chosen path; doctor/remote verify; register MCP; set repo policy; initialize artifact repo; gate transcript ingest; persist config; smoke test; set endpoint trust; emit verdict [`skills/gstack/setup-gbrain/SKILL.md:508-1000`, `skills/gstack/setup-gbrain/SKILL.md:1001-1068`].
- **Branches:** existing Supabase; auto/manual Supabase; local PGLite; remote MCP with optional split local code index; engine switch; broken-engine retry/switch/quit; cleanup orphans.
- **Rules / gates / stops:** PAT/DB/token via environment only; remote non-loopback requires TLS; failed verify/doctor/PATH validation/migration/smoke test stops; destructive orphan deletion is per-project; repo `deny` prohibits interaction.
- **Tools / dependencies:** gbrain CLI, Bun, Claude MCP CLI, Git, jq/curl/openssl, Supabase Management API, numerous shared gstack helpers.
- **Permissions / side effects:** can clone/install/link gbrain, create/delete Supabase projects, write `~/.gbrain`, `~/.claude.json`, `~/.gstack`, project `CLAUDE.md`, private Git artifact repo, and MCP credentials.
- **Strongest unique methods:** explicit topology decision tree; split remote knowledge/local code-index model; per-remote trust tiers; secret-env handling; idempotent doctor-style verdict.
- **Weaknesses / failure modes:** largest operational surface in the assignment and therefore high partial-state risk. Scope text says local Mac, while portions support other platforms; documentation contains forward-looking/deferred recovery details that can be mistaken for shipped behavior.
- **Overlap / candidates:** setup prerequisite and strong dependency of `sync-gbrain`; artifact sync also intersects every skill preamble.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/setup-gbrain/SKILL.md` | semantic-read | Complete decision skeleton, shortcut modes, trust, smoke test, and verdict. |
| `sections/engine-remediation.md` | semantic-read | Broken-engine retry/PGLite/switch/quit gates and rollback semantics [`skills/gstack/setup-gbrain/sections/engine-remediation.md:1-72`]. |
| `sections/brain-init.md` | semantic-read | All local/Supabase/remote/switch initialization paths and secret handling [`skills/gstack/setup-gbrain/sections/brain-init.md:1-271`]. |
| `sections/transcript-gate.md` | semantic-read | Probe thresholds, historical-ingest consent, and mode persistence [`skills/gstack/setup-gbrain/sections/transcript-gate.md:1-67`]. |
| `sections/claude-md-persist.md` | semantic-read | Local/remote configuration schemas and smoke-gated guidance block [`skills/gstack/setup-gbrain/sections/claude-md-persist.md:1-80`]. |
| `skills/gstack/setup-gbrain/memory.md` | semantic-read | User-facing data inventory, privacy, retention, trust-policy, remote-MCP, and token-storage semantics [`skills/gstack/setup-gbrain/memory.md:1-196`, `skills/gstack/setup-gbrain/memory.md:197-341`]. |
| `bin/gstack-gbrain-detect` | behavior-reviewed | Detect JSON, local-status classifier, MCP transport, pooler and artifact state [`skills/gstack/bin/gstack-gbrain-detect:1-300`]. |
| `bin/gstack-gbrain-install` | behavior-reviewed | Detect-first install, network/prerequisite gates, PATH-shadow validation and version floor [`skills/gstack/bin/gstack-gbrain-install:1-250`]. |
| `bin/gstack-gbrain-repo-policy` | behavior-reviewed | Trust-store normalization, migration, fail-closed batch reads, set/list behavior [`skills/gstack/bin/gstack-gbrain-repo-policy:1-300`]. |
| `bin/gstack-gbrain-mcp-verify` | behavior-reviewed | Receipted remote probe, NETWORK/AUTH/MALFORMED classification, capability probe [`skills/gstack/bin/gstack-gbrain-mcp-verify:1-219`]. |
| `bin/gstack-artifacts-init` | behavior-reviewed | Private artifact-repo initialization, provider selection, canonical remote and push setup [`skills/gstack/bin/gstack-artifacts-init:1-250`]. |
| `sections/*.tmpl`, `sections/manifest.json`, `SKILL.md.tmpl` | excluded | Generated-source duplicates and render metadata. |

---

## 17. `gstack/skillify`

**Exact root / skill:** `skills/gstack/skillify/` / `skills/gstack/skillify/SKILL.md`

### Capability dossier

- **Trigger:** skillify/codify/save the recent scrape or make it permanent [`skills/gstack/skillify/SKILL.md:1-22`].
- **Non-trigger:** no valid recent prototype, already matched codified scrape, mutating flow, multi-page crawler, or editing/removing an existing skill.
- **Responsibility:** transform the most recent accepted `/scrape` prototype into a tested, self-contained browser skill and commit it only after explicit approval.
- **Non-responsibility:** synthesize from arbitrary chat fragments, codify mutations, or leave half-written artifacts.
- **Inputs:** accepted scrape intent/result/final browser calls, proposed name/triggers/host/tier, captured HTML fixture, canonical SDK bytes.
- **Outputs:** `SKILL.md`, `script.ts`, `script.test.ts`, copied SDK, fixture, committed at project/global tier.
- **Core workflow:** provenance guard over at most 10 agent turns; propose validated name/triggers/tier; synthesize pure parser plus runtime main; capture fixture; generate shape tests; copy canonical SDK; stage atomically; test/retry at most twice; approval gate; atomic rename or discard; run post-commit verification [`skills/gstack/skillify/SKILL.md:491-845`].
- **Branches:** no valid scrape/refuse; stale conversation confirmation; global/project tier; collision/rename; test retry/discard; preview then re-approve; commit/discard.
- **Rules / gates / stops:** page data is untrusted; never write final artifact before tests and approval; pure parser required; at least one substantive shape assertion; no clobber; failed/rejected staging removed.
- **Tools / dependencies:** `$B`, Bun tests, `browser-skill-write`, canonical browse SDK, filesystem, AskUserQuestion.
- **Permissions / side effects:** reads live page HTML; writes temporary staging; may commit to `~/.gstack/browser-skills` or repo `.gstack/browser-skills`.
- **Strongest unique method:** atomic test-before-visibility publishing contract for agent-authored automation.
- **Weaknesses / failure modes:** source reconstruction depends on recent conversation memory; fixtures are point-in-time; Bun required; stated “single target” ceiling excludes crawls and complex hydration.
- **Overlap / candidates:** producer for the browser-skill runtime; directly complements `scrape`; `hackernews-frontpage` is its reference example.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/skillify/SKILL.md` | semantic-read | Full provenance, synthesis, staging, test, approval, and verification contract. |
| `skills/gstack/browse/src/browser-skill-write.ts` | behavior-reviewed | Name validation, secure staging, symlink/path checks, atomic commit, no-clobber, cleanup [`skills/gstack/browse/src/browser-skill-write.ts:1-232`]. |
| `skills/gstack/browse/src/browser-skills.ts` | behavior-reviewed | Tier precedence and frontmatter contract reviewed under `browse`. |
| `skills/gstack/browser-skills/hackernews-frontpage/{script.ts,script.test.ts,_lib/browse-client.ts}` | semantic-read / behavior-reviewed | Explicit reference implementation used by the synthesis instructions. |
| `skills/gstack/skillify/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |

---

## 18. `gstack/sync-gbrain`

**Exact root / skill:** `skills/gstack/sync-gbrain/` / `skills/gstack/sync-gbrain/SKILL.md`

### Capability dossier

- **Trigger:** sync/refresh/update/reindex gbrain or repair missing search results [`skills/gstack/sync-gbrain/SKILL.md:1-21`].
- **Non-trigger:** first-time setup, engine/topology selection, or MCP registration.
- **Responsibility:** preflight current gbrain state and trust, run code/memory/artifact sync stages, optionally build call graph, refresh search guidance, and emit a health verdict.
- **Non-responsibility:** initialize a missing/broken local engine; it routes those cases to `setup-gbrain`.
- **Inputs:** user mode flags, detect JSON, repo policy, endpoint trust, source/page/cycle state.
- **Outputs:** synchronized source/memory/artifacts, `.gbrain-source`, atomic sync state, refreshed/removed `CLAUDE.md` guidance, GREEN/YELLOW/RED completion.
- **Core workflow:** detect setup and endpoint trust; fail/skip according to local status; pass arguments unchanged to orchestrator; check page count and offer full reindex; check call graph and offer dream; capability-test write/search; atomically update or remove guidance block; report verdict [`skills/gstack/sync-gbrain/SKILL.md:477-873`].
- **Branches:** incremental/full/dream/no-dream/code-only/dry-run/cache refresh/audit; local/remote thin client; timeout/locked/missing/broken; page-count zero; graph never/completed/unknown.
- **Rules / gates / stops:** repo `deny` stops; missing/broken local engine stops or degrades only in defined remote cases; dry-run writes nowhere; source graph claims must reflect actual stage result; guidance exists only after successful capability check.
- **Tools / dependencies:** gbrain CLI, Bun orchestrator, shared detect/config/cache/sync/memory helpers, Git, jq, CLAUDE.md.
- **Permissions / side effects:** indexes code, ingests transcripts/artifacts, may push artifact Git data, writes state/locks/source pin and `CLAUDE.md`; dry-run/audit are read-only.
- **Strongest unique method:** staged idempotent synchronization with independently nonfatal code/memory/artifact stages, plus capability-gated agent guidance.
- **Weaknesses / failure modes:** full runs can take 25–35 minutes; call graph depends on an external code-aware schema pack; `engine-locked` reflects PGLite’s single-process ceiling.
- **Overlap / candidates:** operational continuation of `setup-gbrain`; shares artifact sync with common skill preamble but adds code and memory indexing.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/gstack/sync-gbrain/SKILL.md` | semantic-read | Complete preflight, stages, health checks, guidance, and verdict. |
| `skills/gstack/bin/gstack-gbrain-sync.ts` | behavior-reviewed | Mode parser, stage architecture, lock/state atomicity, resume guard, timeouts, code/memory/artifact orchestration [`skills/gstack/bin/gstack-gbrain-sync.ts:1-96`, `skills/gstack/bin/gstack-gbrain-sync.ts:102-350`]. |
| `skills/gstack/bin/gstack-memory-ingest.ts` | behavior-reviewed | Transcript/artifact source inventory, trust filtering, state, modes, optional secret scan [`skills/gstack/bin/gstack-memory-ingest.ts:1-100`, `skills/gstack/bin/gstack-memory-ingest.ts:151-250`]. |
| `skills/gstack/bin/gstack-gbrain-detect` | behavior-reviewed | Shared setup/health classifier; reviewed under `setup-gbrain`. |
| `skills/gstack/sync-gbrain/SKILL.md.tmpl` | excluded | Generated authoring duplicate. |

---

## 19. Fixture root `gstack/test/fixtures/context-bill/tree-a/alpha`

**Exact root / skill:** `skills/gstack/test/fixtures/context-bill/tree-a/alpha/` / `skills/gstack/test/fixtures/context-bill/tree-a/alpha/SKILL.md`

### Capability dossier

- **Fixture status:** explicit scanner/context-billing fixture, not a production capability.
- **Trigger:** synthetic trigger `a-key-the-upstream-router-DOES-read`; `x-dead-key` is deliberately not router-consumed [`skills/gstack/test/fixtures/context-bill/tree-a/alpha/SKILL.md:1-7`].
- **Non-trigger:** all real user workflows.
- **Responsibility:** exercise context-bill detection of forced references, optional references, mode tables, dead frontmatter keys, and specialist-path strings.
- **Non-responsibility:** perform discovery, full-chain automation, web work, or invoke real specialists.
- **Inputs:** fixture request/mode and scanner treatment.
- **Outputs:** test-observable eager/conditional reference accounting.
- **Core workflow:** infer mode; always read `CORE.md` and `POLICY.md`; read `OPTIONAL.md` only before public-web work; mode table names candidate legacy specialists [`skills/gstack/test/fixtures/context-bill/tree-a/alpha/SKILL.md:9-18`].
- **Branches:** Discovery, Full chain, public-web optional read.
- **Rules / gates / stops:** two references are forced every invocation; optional reference is conditional.
- **Tools / dependencies:** fixture scanner only.
- **Permissions / side effects:** none.
- **Strongest unique method:** useful test pattern distinguishing eager references from conditional references and dead metadata.
- **Weaknesses / failure modes:** candidate paths `references/legacy/office.md` and `references/legacy/auto.md` do not exist in the fixture subtree. It is intentionally incomplete and must not be promoted as reusable workflow.
- **Overlap / candidates:** test-only analogue of router/mode-table semantics. **Reusable capability contribution: none.** Reusable test-design pattern only.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `.../alpha/SKILL.md` | semantic-read | Fixture contract and forced/conditional reads. |
| `.../alpha/references/CORE.md` | semantic-read | Explicit forced-read fixture number one [`skills/gstack/test/fixtures/context-bill/tree-a/alpha/references/CORE.md:1-3`]. |
| `.../alpha/references/POLICY.md` | semantic-read | Explicit forced-read fixture number two [`skills/gstack/test/fixtures/context-bill/tree-a/alpha/references/POLICY.md:1-3`]. |
| `.../alpha/references/OPTIONAL.md` | semantic-read | Explicit conditional, non-eager fixture [`skills/gstack/test/fixtures/context-bill/tree-a/alpha/references/OPTIONAL.md:1-3`]. |
| `.../alpha/references/legacy/*` | excluded | Paths are mentioned as candidate specialists but absent; no readable support artifact exists. |

---

## 20. Fixture root `gstack/test/fixtures/context-bill/tree-a/beta`

**Exact root / skill:** `skills/gstack/test/fixtures/context-bill/tree-a/beta/` / `skills/gstack/test/fixtures/context-bill/tree-a/beta/SKILL.md`

### Capability dossier

- **Fixture status:** explicit scanner/context-billing fixture, not a production capability.
- **Trigger:** none declared beyond fixture discovery.
- **Non-trigger:** all actual user tasks.
- **Responsibility:** represent a minimal skill with no forced reads and no mode table [`skills/gstack/test/fixtures/context-bill/tree-a/beta/SKILL.md:1-8`].
- **Non-responsibility:** route, execute tools, or provide domain guidance.
- **Inputs:** scanner traversal only.
- **Outputs:** baseline context-billing observation.
- **Core workflow:** one-command fixture; no eager or lazy support reads.
- **Branches:** none.
- **Rules / gates / stops:** none beyond frontmatter parsing.
- **Tools / dependencies:** none.
- **Permissions / side effects:** none.
- **Strongest unique method:** negative-control fixture for a clean minimal skill.
- **Weaknesses / failure modes:** no functional method exists; therefore it cannot contribute reusable capability.
- **Overlap / candidates:** contrasts with alpha. `agents.md` is intentionally a foreign-host scanner-scope file, not beta semantics.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `.../beta/SKILL.md` | semantic-read | Minimal negative-control fixture. |
| `.../beta/agents.md` | excluded | States it is a foreign host file dropped into scanner scope, not skill guidance [`skills/gstack/test/fixtures/context-bill/tree-a/beta/agents.md:1-3`]. |

---

# Cross-root semantic hypotheses

## Duplicate hypotheses

1. **Generated SKILL/template pairs are textual build duplicates, not capability duplicates.** Rendered `SKILL.md` is the audit authority; `.tmpl` files are authoring sources and should not create separate Units.
2. **Common preamble/voice/telemetry blocks across operational skills are shared protocol Units.** They should be normalized once and referenced, not emitted as unique per-root capabilities. The runtime implementation is centralized in `gstack-skill-start` and `gstack-skill-end` [`skills/gstack/bin/gstack-skill-start:1-39`, `skills/gstack/bin/gstack-skill-end:1-20`].
3. **`browse` and `scrape` repeat the same Aside-first setup, safety, fallback, and untrusted-content contract.** This is a duplicate protocol layer; `scrape` adds a JSON-only read specialization.
4. **`setup-gbrain`, `sync-gbrain`, `codex`, `document-generate`, `document-release`, `setup-deploy`, and `skillify` repeat AskUserQuestion formatting/tuning prose.** Treat as shared interaction protocol, not seven unique methods.

## Complement hypotheses

1. **`context-save` + `context-restore`:** lifecycle pair; save creates append-only branch-tagged packets, restore selects current-branch-first with cross-branch fallback.
2. **`scrape` + `skillify` + browser-skill runtime:** prototype, codify, then deterministic replay. `hackernews-frontpage` is the reference instance.
3. **`document-release` + `document-generate`:** release audits and flags coverage; generate authors missing quadrants. Their “map but do not generate” versus “research and generate” boundary is clean.
4. **`setup-gbrain` + `sync-gbrain`:** one-time topology/trust/MCP setup followed by repeatable repository synchronization.
5. **`browse` + `open-gstack-browser` + `setup-browser-cookies`:** browser operation, headed fallback visibility, and fallback authentication are complementary.
6. **`document-generate` + `make-pdf`:** authoring and publication are separate capabilities.

## Conflict hypotheses

1. **Landing-report read-only contract conflict:** `landing-report` declares no Git mutation but explicitly runs `git fetch`, which mutates remote-tracking refs [`skills/gstack/landing-report/SKILL.md:382-411`]. Resolution candidate: either remove fetch from the report skill or narrow the contract to “no project-file/version/PR mutations.”
2. **Open-browser session preservation conflict:** `open-gstack-browser` force-kills the existing daemon, whereas upgrade/browser contracts preserve or defer busy sessions [`skills/gstack/open-gstack-browser/SKILL.md:218-235`; `skills/gstack/gstack-upgrade/SKILL.md:269-323`]. Resolution candidate: use the shared busy-daemon status/stop path and require confirmation before destructive cleanup.
3. **Codex Review-mode contract conflict:** the skeleton hard-requires `sections/review-mode.md`, but that file is only a CLI error line [`skills/gstack/codex/SKILL.md:633-637`; `skills/gstack/codex/sections/review-mode.md:1`]. The Review capability is presently incomplete.
4. **Scrape browser asymmetry:** codified browser skills are available only on `$B` fallback, while Aside has its own separate skill system [`skills/gstack/scrape/SKILL.md:270-293`]. Same trigger can therefore select a deterministic skill on one driver and prototype extraction on another.

## Conditional-variant hypotheses

1. **Browser driver variant:** Aside is preferred for real sessions; `$B` is the Linux/Windows/closed-Aside fallback. Same evidence and consent contract, different state model.
2. **Gbrain topology variants:** local PGLite, existing/auto/manual Supabase, and remote HTTP MCP are legitimate conditional variants. Remote MCP may pair with local code-only PGLite.
3. **Documentation variants:** `document-generate` chooses Diataxis quadrants by entity type; not every entity needs all four.
4. **Version-allocation variants:** GitHub, GitLab, unknown/offline Git fallback, 3-digit versus 4-digit version width, and active-sibling advancement are conditional variants of one allocator.
5. **Checkpoint restore variants:** current-branch checkpoint preferred; cross-branch fallback only when needed.

## Strong-dependency hypotheses

- `gstack` → every routed skill.
- `browse` → `scrape`, `open-gstack-browser`, `setup-browser-cookies`, browser skills, and PDF browser fallback.
- `scrape` → `skillify` provenance.
- `skillify` → browser-skill storage/write/runtime and canonical SDK.
- `context-save` → `context-restore`.
- `setup-gbrain` → `sync-gbrain`.
- `document-release` → `document-generate` for substantial gaps.
- `landing-report` → `gstack-next-version`.
- All generated skills → `gstack-skill-start` / `gstack-skill-end`.

# Unresolved questions

1. Was `skills/gstack/codex/sections/review-mode.md` accidentally overwritten by captured CLI stderr during generation? Its current one-line content cannot implement Review mode.
2. Should “read-only” in `landing-report` prohibit ref updates, or only project-file/PR/version mutations?
3. Should `open-gstack-browser` preserve a healthy existing daemon and offer reconnect/focus before force cleanup?
4. Is parity between Aside skills and `$B` browser-skills planned, or is driver-dependent scrape acceleration intentional?
5. Should checkpoint lookup permit explicit title/number searches beyond the 20-candidate presentation cap?
6. Do setup-gbrain’s Mac-specific audience statement and Windows-supporting helper behavior represent a deliberate support boundary or documentation drift?
7. Should the fixture alpha’s absent `references/legacy/*` paths remain intentionally dangling, or should fixture files exist to test specialist-reference billing separately?

## Audit completion

All 20 assigned roots have an independently cited dossier and support-file classification. No old dossier or coverage status was used as proof. Fixture roots contribute scanner/test-design patterns only; neither contributes reusable production capability.