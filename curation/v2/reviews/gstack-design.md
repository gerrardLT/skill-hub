# Capability Compiler V2 — Phase 1B Semantic Audit

## Review

- **Correct:** All 11 assigned `SKILL.md` files were read completely. Nested support files were classified independently rather than inferred from the parent `gstack` root.
- **Correct:** The audit distinguishes semantic doctrine/templates, behavior-bearing scripts, vendored runtime code, generated mirrors, and test fixtures.
- **Finding:** Several source-contract inconsistencies remain, chiefly: `/ios-design-review` requests an `observe` token for `/session/acquire`, although the daemon requires `interact`; `/ios-sync` describes a lockfile-bearing cache key not implemented by either checked-in generator; `/design-review` simultaneously forbids reading source and requires source review/fixes.
- **Merge verdict:** **OK with notes.** This is a read-only semantic audit. No source was unreadable.

## Audit basis and method

Phase 1 requires every `SKILL.md` to be `semantic-read`, support files to receive explicit `semantic-read`, `behavior-reviewed`, or `excluded` dispositions, and scripts not to be excluded by extension alone. Root dossiers must cover triggers, responsibility, I/O, workflow, tools, permissions, strengths, weaknesses, failure modes, reusable units, and parent/child relationships (`.specs/capability-compiler-v2/phase-1/phase-plan.md:28-49`). The phase gate further requires root, file, unit, comparison, and relationship completeness without changing V1 assets (`.specs/capability-compiler-v2/phase-1/phase-plan.md:74-105`). The current coverage ledger declares 139 roots and 2,337 files, with statuses split among semantic review, behavior review, and exclusions (`curation/v2/coverage.json:1-14`).

Common generated gstack preamble material is not repeated in full below. It supplies skill-start protocol handling, plan-mode rules, `AskUserQuestion` gates, telemetry, artifacts sync, completion status, and, for higher tiers, context recovery and decision logging. Root-specific conclusions come from each root’s own workflow after that shared preamble.

---

## 1. `gstack/design-consultation`

### Exact root and skill path

- **Root:** `skills/gstack/design-consultation/`
- **Skill:** `skills/gstack/design-consultation/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Requests for a new design system, brand guidelines, or `DESIGN.md`.
- New-project UI work where no design system exists.
- Product-level visual direction covering aesthetic, typography, color, layout, spacing, and motion (`skills/gstack/design-consultation/SKILL.md:1-22`, `skills/gstack/design-consultation/SKILL.md:488-516`).

**Non-trigger**

- Inferring or auditing an already implemented site; the skill redirects that case to `/plan-design-review`.
- Implementing a chosen design in HTML; that belongs to `/design-html`.
- Pure variant exploration without establishing a full system; that belongs to `/design-shotgun`.

### Responsibility and non-responsibility

**Responsibility**

- Gather product, audience, project-type, category, and memorable-first-impression context.
- Optionally research comparable products.
- Propose one coherent system with explicit safe conventions and deliberate creative risks.
- Produce visual previews and ultimately a structured `DESIGN.md`.
- Preserve user taste history while allowing explicit departures (`skills/gstack/design-consultation/SKILL.md:652-765`; `skills/gstack/design-consultation/sections/proposal-and-preview.md:1-81`).

**Non-responsibility**

- It does not implement application UI.
- It does not perform rendered-site QA.
- In plan mode it embeds proposed `DESIGN.md` content into the plan rather than writing the actual root file (`skills/gstack/design-consultation/sections/proposal-and-preview.md:326-361`).

### Inputs

- Repository `README.md`, `package.json`, source/component layout, existing `DESIGN.md`, and office-hours artifacts.
- User confirmation of product, users, industry, project type, research preference, and the one memorable thing.
- Optional taste profile and prior approved design sessions.
- Optional competitive URLs and external-model design opinions (`skills/gstack/design-consultation/SKILL.md:493-579`, `skills/gstack/design-consultation/SKILL.md:652-850`).

### Outputs

- Opinionated design proposal with aesthetic, decoration, layout, palette, typography, spacing, motion, safe choices, and risks.
- AI mockups and comparison-board feedback, or a self-contained HTML preview fallback.
- `DESIGN.md`; optionally a `CLAUDE.md` design-system instruction.
- In plan mode, “Approved Design Direction” and “Proposed DESIGN.md” plan sections (`skills/gstack/design-consultation/sections/proposal-and-preview.md:1-81`, `skills/gstack/design-consultation/sections/proposal-and-preview.md:111-361`).

### Core workflow

1. Detect an existing design system and gather repository/product context.
2. Check browser and design-binary availability.
3. Load prior learnings and taste profile.
4. Ask one consolidated product-context question plus the memorable-thing question.
5. Optionally conduct category and visual research.
6. Optionally solicit outside design voices.
7. Read the deferred proposal section.
8. Present the complete coherent proposal.
9. Handle focused drill-downs.
10. Generate mockups or HTML preview.
11. Confirm choices and write or stage `DESIGN.md` (`skills/gstack/design-consultation/SKILL.md:488-943`; `skills/gstack/design-consultation/sections/proposal-and-preview.md:1-361`).

### Branches

- Existing `DESIGN.md`: update, start fresh, or cancel.
- Empty/unclear product: recommend `/office-hours`.
- Research requested or skipped.
- Aside browser, headless browser, WebSearch-only, or in-distribution fallback.
- `$D` available: AI mockups; unavailable: HTML preview.
- Plan mode: write proposal into plan; implementation mode: write repository files.
- User can accept, adjust one dimension, request different risks, restart, or skip preview.

### Rules, gates, and stop conditions

- Every recommendation needs a rationale.
- Coherence outranks isolated “best” choices.
- At least two explicit creative risks must be proposed.
- Blacklisted and overused fonts are not primary recommendations unless user-requested.
- Comparison-board feedback must be confirmed before saving.
- Design artifacts belong under `~/.gstack/projects/$SLUG/designs/`.
- Existing design-system changes require a user choice.
- External URLs must be user-confirmed before being opened in the real browser.
- User’s final aesthetic choice is accepted even when the skill warns of incoherence (`skills/gstack/design-consultation/sections/proposal-and-preview.md:1-109`, `skills/gstack/design-consultation/SKILL.md:918-943`).

### Tools and dependencies

- File reads, edits, writes, glob/grep.
- Aside or gstack headless browser.
- Optional `WebSearch`.
- Optional gstack design binary `$D`.
- `gstack-taste-update`, learnings tools, review log, telemetry.
- Optional Codex and a Claude design voice.

### Permissions and side effects

- May open browser tabs and perform read-only external research after URL confirmation.
- Writes design artifacts to user-scoped `~/.gstack`.
- Writes `DESIGN.md` and may update/create `CLAUDE.md` outside plan mode.
- Writes plan content in plan mode.
- May log taste, decisions, learnings, reviews, and telemetry.
- Does not deploy or mutate third-party sites.

### Strongest unique methods

- **Memorable-thing forcing question:** all later decisions must serve one remembered impression.
- **Safe/risk split:** distinguishes category literacy from deliberate differentiation.
- **Three-layer research synthesis:** established conventions, current patterns, then first-principles departure.
- **Coherence validation:** user overrides are checked against the remainder of the system.
- **Approved-mockup token extraction:** exact design tokens come from the chosen visual, not prose alone.

### Weaknesses and failure modes

- Very broad workflow combines research, strategy, design-system definition, visual generation, and repository documentation; partial completion is easy if a downstream browser or design tool fails.
- “For existing sites, use `/plan-design-review` to infer the system” overstates that dependency: `/plan-design-review` primarily improves a plan and may merely flag a missing `DESIGN.md`, rather than infer and create one.
- HTML fallback uses external font links, so it is not fully offline.
- External design voices add cost and latency without being required for a complete system.
- The plan-mode branch may leave the actual `DESIGN.md` absent until a later implementation step.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `/design-shotgun` for variant exploration and approval.
- **Strong dependency:** `/design-html` for production-like HTML from an approved direction.
- **Complement:** `/plan-design-review` evaluates whether a UI plan specifies enough design.
- **Complement:** `/design-review` validates the resulting live site.
- **Duplicate candidate:** taste-profile loading and comparison-board feedback machinery are substantially shared with `/design-shotgun`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `design-consultation/SKILL.md` | semantic-read | Canonical generated execution contract; read completely. |
| `design-consultation/sections/proposal-and-preview.md` | semantic-read | Contains Phases 3–6, safe/risk method, preview branches, and `DESIGN.md` output contract. |
| `design-consultation/sections/manifest.json` | semantic-read | Declares the on-demand section trigger and ownership. |
| `design-consultation/SKILL.md.tmpl` | excluded | Generator source for the canonical `SKILL.md`; sampled to verify provenance and root-specific frontmatter, but not separate behavior. |
| `design-consultation/sections/proposal-and-preview.md.tmpl` | excluded | Generator source duplicate of the rendered semantic section. |

---

## 2. `gstack/design-html`

### Exact root and skill path

- **Root:** `skills/gstack/design-html/`
- **Skill:** `skills/gstack/design-html/SKILL.md`

### Trigger and non-trigger

**Trigger**

- “Build the design,” “code the mockup,” “make it real,” “turn this into HTML,” or “implement this design.”
- Approved `/design-shotgun` mockup, CEO plan, plan-design-review context, or a sufficiently detailed freeform description (`skills/gstack/design-html/SKILL.md:1-24`, `skills/gstack/design-html/SKILL.md:364-413`).

**Non-trigger**

- Open-ended brand/system creation.
- Variant exploration before a direction is selected.
- Multi-page generation in one invocation; the skill is explicitly one page per invocation.

### Responsibility and non-responsibility

**Responsibility**

- Produce one Pretext-native HTML page or framework component.
- Preserve approved-mockup fidelity.
- Route text layout to the appropriate Pretext API tier.
- Verify at mobile, tablet, and desktop widths.
- Iteratively refine through surgical edits.

**Non-responsibility**

- It is not the initial product strategy or design-system consultation.
- It does not extract a production component architecture for an entire application.
- It does not process multiple pages in one run (`skills/gstack/design-html/SKILL.md:658-696`).

### Inputs

- Latest approved mockup and `approved.json`.
- CEO plan or design-review artifacts.
- Existing `DESIGN.md`.
- Prior `finalized.html` for evolve mode.
- Freeform purpose, audience, visual feel, structure, references, and screen name.
- Detected framework and language preference (`skills/gstack/design-html/SKILL.md:381-520`).

### Outputs

- `finalized.html` or a framework-native `.tsx`, `.svelte`, or `.vue` component under the project’s user-scoped design directory.
- Three viewport screenshots.
- `finalized.json` metadata.
- Optional `DESIGN.md` extracted from generated tokens.
- Optional copy into the application codebase after explicit next-step selection (`skills/gstack/design-html/SKILL.md:521-680`).

### Core workflow

1. Read UX doctrine.
2. Detect approved mockups, plans, variants, prior HTML, and `DESIGN.md`.
3. Route to approved-mockup, plan-driven, freeform, or evolve mode.
4. Derive an implementation specification.
5. Select a Pretext tier.
6. Detect framework and output language.
7. Read exact Pretext wiring patterns.
8. Embed vendored Pretext or use fallback/import.
9. Write one output file.
10. Run local preview and viewport verification.
11. Refine surgically, at most ten rounds before a continuation decision.
12. Save metadata and offer next steps (`skills/gstack/design-html/SKILL.md:360-696`).

### Branches

- Approved mockup versus plan-only versus clean slate.
- Evolve prior finalized HTML versus regenerate fresh.
- `$D prompt` analysis versus human visual analysis.
- Vanilla HTML versus framework component.
- Vendored Pretext versus CDN fallback.
- Browser verification available versus documented skip.
- Create `DESIGN.md` versus defer.

### Rules, gates, and stop conditions

- Doctrine must be read before design decisions.
- Pretext patterns must be read before writing layout code.
- `DESIGN.md` system tokens override visual extraction.
- Use real content, not placeholders.
- Include semantic HTML, ARIA, focus states, dark mode, reduced motion, breakpoints, `ResizeObserver`, and `MutationObserver`.
- Refinement edits must be surgical, not whole-file rewrites.
- Maximum ten refinement rounds before asking whether to continue.
- One page per invocation (`skills/gstack/design-html/SKILL.md:349-358`, `skills/gstack/design-html/SKILL.md:520-696`).

### Tools and dependencies

- Vendored `@chenglou/pretext` runtime.
- Optional gstack design binary.
- `gstack-render`.
- Local Python HTTP server or default browser.
- Framework package manager when framework-native output is selected.
- Google Fonts in generated vanilla HTML.

### Permissions and side effects

- Writes user-scoped design artifacts.
- May install `@chenglou/pretext` in the target project for framework output.
- May create `DESIGN.md`.
- Starts and kills a local HTTP server.
- May copy the finalized output into project source only after the user chooses that next step.

### Strongest unique methods

- **Text-layout tier routing:** basic height, card/grid, shrink-wrap chat, obstacle-aware editorial, or line-by-line editorial.
- **Pretext relayout contract:** prepare after fonts load, then cheap resize-aware layout.
- **Editable preview:** `contenteditable` plus mutation-triggered re-preparation.
- **Source-of-truth fidelity:** approved mockup wins over abstract code elegance.

### Weaknesses and failure modes

- “Zero deps” is only true for vendored vanilla output; framework mode installs a dependency, and vendor-missing mode uses a CDN.
- “Fully self-contained” vanilla output still requires Google Fonts unless fonts are already local.
- The vendored bundle is minified and difficult to audit or patch manually.
- The mandatory Pretext rule may be unnecessary for layouts where native CSS fully solves sizing; it creates a 30 KB runtime and JavaScript dependence.
- Server-port detection relies on `lsof`, which is not given a fallback if Python starts but `lsof` is absent.
- Manual `contenteditable` edits are not explicitly persisted back to source before metadata save.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** consumes `/design-shotgun`, `/design-consultation`, and `/plan-design-review` artifacts.
- **Complement:** `/design-review` can audit the generated live page.
- **Duplicate candidate:** UX doctrine is textually shared with `/design-shotgun`.
- **Conditional variant:** framework output and vanilla output share one capability but have materially different dependency and side-effect contracts.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `design-html/SKILL.md` | semantic-read | Canonical workflow read completely. |
| `design-html/sections/doctrine.md` | semantic-read | Governs every layout and visual decision. |
| `design-html/sections/pretext-patterns.md` | semantic-read | Defines exact behavior-bearing API wiring patterns. |
| `design-html/sections/manifest.json` | semantic-read | Declares mandatory read triggers. |
| `design-html/vendor/pretext.js` | behavior-reviewed | Vendored minified runtime implementing segmentation, measurement, layout, locale, and cache behavior; inspected as executable dependency. |
| `design-html/SKILL.md.tmpl` | excluded | Generator source duplicate of canonical `SKILL.md`. |
| `design-html/sections/*.md.tmpl` | excluded | Generated-section sources duplicating rendered semantic files. |

---

## 3. `gstack/design-review`

### Exact root and skill path

- **Root:** `skills/gstack/design-review/`
- **Skill:** `skills/gstack/design-review/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Live-site visual audit, design QA, design polish, or requests to fix rendered visual issues.
- Feature branch with no URL, which invokes diff-aware mode (`skills/gstack/design-review/SKILL.md:1-22`, `skills/gstack/design-review/SKILL.md:485-522`).

**Non-trigger**

- Plan-stage UI review; use `/plan-design-review`.
- iOS app visual review; use `/ios-design-review`.
- Pure design-system creation.

### Responsibility and non-responsibility

**Responsibility**

- Inspect rendered pages and interaction flows.
- Score design quality and AI-slop risk.
- Produce screenshot-backed findings.
- Triage and apply minimal fixes atomically.
- Verify each fix with before/after evidence and revert regressions.

**Non-responsibility**

- It is not meant to redesign unrelated code or add product features.
- It does not fix third-party widgets or copy requiring team input.
- CSS-only fixes do not receive unit regression tests; visual reruns are the verification path (`skills/gstack/design-review/SKILL.md:1629-1750`).

### Inputs

- URL or feature-branch diff.
- Optional scope/depth/auth overrides.
- `DESIGN.md`.
- Live Aside/headless browser session.
- Existing tests and project testing guidance.
- Prior design baseline and learnings.

### Outputs

- Full design-audit report and project-index summary.
- Screenshot evidence by page, viewport, flow, and finding.
- `design-baseline.json`.
- Atomic fix commits and optional JS regression tests.
- `TODOS.md` annotations for deferred findings.
- Final score deltas and PR summary (`skills/gstack/design-review/SKILL.md:1040-1400`, `skills/gstack/design-review/SKILL.md:1629-1727`).

### Core workflow

1. Resolve URL, mode, scope, and clean-tree gate.
2. Configure browser and detect or bootstrap tests.
3. Load `DESIGN.md`, prior learnings, and optional designer.
4. Capture first impression before analytical review.
5. Extract rendered design system.
6. Audit pages at three viewports across ten categories.
7. Walk two or three interaction flows and track goodwill.
8. Compare cross-page consistency.
9. Compile scored report and optional regression comparison.
10. Run outside voices.
11. Triage findings.
12. Locate source, minimally fix, commit, re-test, classify, and monitor cumulative risk.
13. Re-audit and publish final report/TODO updates (`skills/gstack/design-review/SKILL.md:485-1628`, `skills/gstack/design-review/SKILL.md:1629-1750`).

### Branches

- Full, quick, deep, diff-aware, or regression mode.
- Aside browser versus headless fallback.
- Existing test framework versus explicit bootstrap.
- Designer available versus no target mockup.
- Fix status: verified, best-effort, reverted, or deferred.
- JS behavior fix versus CSS-only fix.
- Risk score above 20% causes a user continuation gate.

### Rules, gates, and stop conditions

- Dirty working tree is a hard gate.
- Screenshots are required evidence for findings.
- One commit per fix.
- CSS-first and smallest related change.
- New console errors constitute regression.
- Revert immediately when a fix worsens behavior.
- Risk check every five fixes or after any revert.
- Stop when design-fix risk exceeds 20%.
- Hard cap of 30 fixes.
- External non-local mutations require consent.
- Never type credentials or expose browser private data (`skills/gstack/design-review/SKILL.md:508-653`, `skills/gstack/design-review/SKILL.md:1510-1750`).

### Tools and dependencies

- Aside or gstack browser.
- Git and project test runner.
- Optional gstack designer.
- Optional Codex/independent design review.
- `gstack-review-log`, learnings, telemetry.
- Test framework package installation when the user chooses bootstrap.

### Permissions and side effects

- Reads live sites and authenticated sessions subject to origin restrictions.
- May commit or stash pre-existing work after explicit choice.
- May install/configure a test framework and CI workflow if no tests exist and user accepts.
- Writes reports, screenshots, baseline, tests, TODOs, and source fixes.
- Makes one Git commit per fix.
- Can revert commits after failed verification.

### Strongest unique methods

- **First-impression narration:** captures visual hierarchy before checklist bias.
- **Page-area and trunk tests:** evaluates wayfinding independently of polish.
- **Goodwill reservoir:** records cumulative user-friction impact through a flow.
- **Dual scores:** overall design and independent AI-slop grade.
- **Fix-risk heuristic:** stops a visual cleanup from becoming uncontrolled application churn.
- **Before/after screenshot requirement:** ties every accepted fix to rendered evidence.

### Weaknesses and failure modes

- Internal contradiction: “Never read source code” is an important rule in the audit section, but outside voices explicitly review frontend source and Phase 8 requires reading and editing source (`skills/gstack/design-review/SKILL.md:1280-1410`, `skills/gstack/design-review/SKILL.md:1450-1665`). The smallest semantic fix is to narrow the rule to “do not substitute source inspection for rendered evidence during baseline audit.”
- Test-framework bootstrap is much broader than visual QA and can create package, CI, documentation, and test churn before any design finding exists.
- The scoring formula uses half-letter reductions but does not define a numeric mapping for weighted aggregation.
- Several hard rules conflict contextually: the AI-slop blacklist rejects gradients, while landing-page rules require avoiding flat single-color backgrounds and permit gradients.
- It claims a rendered-site evaluation posture, yet automated outside voices may judge source without screenshot evidence.
- Real-site coverage depends on browser availability, authentication state, and deterministic navigation.

### Overlap, duplicate, and dependency candidates

- **Conditional variant:** `/ios-design-review` is the real-device iOS equivalent.
- **Complement:** `/plan-design-review` prevents design omissions before implementation.
- **Dependency candidate:** `/design-consultation` provides `DESIGN.md`.
- **Dependency candidate:** `/design-shotgun` can generate target directions before fixes.
- **Duplicate candidate:** substantial design doctrine, AI-slop rules, and outside-voice scorecards overlap `/plan-design-review`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `design-review/SKILL.md` | semantic-read | Entire audit, scoring, fix, and report contract. |
| `design-review/SKILL.md.tmpl` | excluded | Generator source duplicate of canonical generated skill. |

---

## 4. `gstack/design-shotgun`

### Exact root and skill path

- **Root:** `skills/gstack/design-shotgun/`
- **Skill:** `skills/gstack/design-shotgun/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Explore design variants, show design options, visual brainstorm, or improve a named current screen.
- UI feature exists conceptually but has not yet been visualized (`skills/gstack/design-shotgun/SKILL.md:1-25`, `skills/gstack/design-shotgun/SKILL.md:486-525`).

**Non-trigger**

- Full design-system definition.
- Production HTML generation.
- Quality review of an already implemented site.

### Responsibility and non-responsibility

**Responsibility**

- Generate intentionally distinct visual directions.
- Present them inline and through a comparison board.
- Capture structured approval, ratings, comments, remix requests, and taste memory.
- Return approved visual context to a calling skill.

**Non-responsibility**

- It is explicitly brainstorming, not review.
- It does not implement the chosen visual.
- It does not establish a complete design system unless constrained by an existing `DESIGN.md`.

### Inputs

- Five context dimensions: user, job, existing UI, flow, and edge cases.
- `DESIGN.md`, office-hours output, source structure, and optional live URL.
- Number of variants.
- Persistent taste profile and recent approved sessions.
- Optional current screenshot for evolve mode (`skills/gstack/design-shotgun/SKILL.md:515-660`).

### Outputs

- Distinct variant PNGs.
- Comparison-board HTML and feedback JSON.
- `approved.json`.
- Updated persistent taste profile.
- Structured feedback for caller or a next-step selection (`skills/gstack/design-shotgun/SKILL.md:661-929`).

### Core workflow

1. Read UX doctrine.
2. Detect prior sessions.
3. Gather missing context in no more than two rounds.
4. Load persistent and recent taste memory.
5. Generate clearly differentiated text concepts.
6. Confirm concepts before API cost.
7. Generate variants in parallel, quality-check, retry, and report failures.
8. Show variants inline.
9. Build and serve comparison board.
10. Process final or pending feedback.
11. Confirm interpretation.
12. Save approval and update taste.
13. Offer iteration, `/design-html`, plan reference, or done (`skills/gstack/design-shotgun/SKILL.md:486-929`).

### Branches

- Revisit prior board versus new exploration.
- Existing-screen evolve path versus new variants.
- Design binary available versus HTML wireframe fallback.
- Feedback submit versus regenerate/remix/more-like.
- Board server versus inline polling fallback.
- Standalone versus called by another skill.

### Rules, gates, and stop conditions

- Doctrine must be read before concepts or briefs.
- Each variant must differ in font, palette, and layout.
- Confirm concepts before spending API credits.
- Context gathering is capped at two rounds.
- Generation retries are bounded.
- Failures must be reported, never silently omitted.
- Zero parallel successes triggers sequential fallback.
- User feedback must be summarized and confirmed before saving.
- Design artifacts may not live in repository-local design folders or `/tmp` as their final location (`skills/gstack/design-shotgun/SKILL.md:650-929`).

### Tools and dependencies

- Gstack design binary.
- Agent-based parallel generation.
- Aside for current-screen capture.
- Local comparison-board server.
- `gstack-taste-update`.
- `DESIGN.md` and project taste profile.

### Permissions and side effects

- Opens local comparison board.
- Writes multiple user-scoped PNG/HTML/JSON artifacts.
- May screenshot a user-named URL.
- Updates persistent taste profile.
- Makes potentially costly design-generation API calls only after confirmation.

### Strongest unique methods

- **Anti-convergence test:** variants must look like different design teams, not minor siblings.
- **Concept-before-credits gate:** approves semantic directions before image generation.
- **Taste decay and conflict handling:** old preferences weaken over time and current contradictions are surfaced.
- **Structured remix loop:** combines layout/colors from different variants rather than requiring binary selection.

### Weaknesses and failure modes

- Requires external generation capability for its principal value; the fallback is referenced but not actually specified within this root.
- The comparison-board command is shown with hardcoded A/B/C paths even after instructing the workflow to build a dynamic existing-image list.
- Feedback confirmation appears both at the end of Step 4 and again as Step 5, creating duplicate interaction.
- Parallel subagent orchestration and retries make the flow operationally heavy.
- Taste inference from approved images can overfit aesthetic preferences to one product context.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** feeds `/design-html`.
- **Complement:** can be invoked from `/design-consultation` or `/plan-design-review`.
- **Duplicate candidate:** comparison-board and taste-profile logic overlap `/design-consultation`.
- **Shared unit candidate:** anti-convergence concept generation plus feedback persistence.
- **Variant relationship:** evolve mode is a conditional variant for existing screens.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `design-shotgun/SKILL.md` | semantic-read | Complete brainstorming and approval workflow. |
| `design-shotgun/sections/doctrine.md` | semantic-read | Required visual-decision doctrine. |
| `design-shotgun/sections/manifest.json` | semantic-read | Section ownership and trigger. |
| `design-shotgun/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `design-shotgun/sections/doctrine.md.tmpl` | excluded | Generator source duplicate of rendered doctrine. |

---

## 5. `gstack/diagram`

### Exact root and skill path

- **Root:** `skills/gstack/diagram/`
- **Skill:** `skills/gstack/diagram/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Make/draw/create a diagram or flowchart.
- Visualize a flow or architecture.
- Convert supplied Mermaid source into editable and rendered forms (`skills/gstack/diagram/SKILL.md:1-24`, `skills/gstack/diagram/SKILL.md:154-187`).

**Non-trigger**

- General UI design.
- A static image-only request when source/editability is not desired still routes here, but the skill refuses to emit only pixels.
- PDF generation itself belongs to `/make-pdf`.

### Responsibility and non-responsibility

**Responsibility**

- Author readable Mermaid.
- Produce Mermaid source, Excalidraw scene, SVG, and PNG.
- Preserve Mermaid as the source of truth until the user edits the Excalidraw scene.
- Render fully offline through the bundled renderer.

**Non-responsibility**

- It does not install a missing renderer/browser.
- It does not guarantee element-level Excalidraw editability for unsupported Mermaid families.
- It does not directly assemble PDFs.

### Inputs

- English diagram description or Mermaid source.
- Current working directory/repository status.
- Optional edited `.excalidraw` for round-trip rendering.

### Outputs

- `<slug>.mmd`
- `<slug>.excalidraw`
- `<slug>.svg`
- `<slug>.png`
- Inline PNG display and editability note (`skills/gstack/diagram/SKILL.md:154-305`).

### Core workflow

1. Author concise Mermaid, choosing direction and diagram type.
2. Select repository `./diagrams/` or temporary output directory.
3. Locate and securely stage the content-addressed renderer bundle.
4. Base64-transport Mermaid into one `gstack-render` call.
5. Produce SVG, PNG, and Excalidraw outputs.
6. Interpret parse errors and converter fallback errors.
7. Display PNG and list artifacts.
8. Re-render edits from Mermaid or, after user round-trip, from Excalidraw JSON.

### Branches

- Flowchart/sequence: element-editable Excalidraw.
- State/class/gantt/other: image element inside Excalidraw.
- Git repository versus non-repository output path.
- ASCII versus non-ASCII Mermaid labels.
- Aside browser versus gstack headless browser.
- Mermaid-source revision versus edited-Excalidraw round trip.

### Rules, gates, and stop conditions

- Prefer 5–15 short-label nodes; split larger diagrams.
- Renderer staging defends against symlink/foreign-owner paths.
- Base64 transport is mandatory to avoid JavaScript interpolation corruption.
- All render outputs must be produced in one pass.
- Mermaid parse errors must be fixed before delivery.
- Missing bundle or browser is blocking.
- Never ship only `.mmd`.
- No CDN fallback; offline rendering is contractual (`skills/gstack/diagram/SKILL.md:188-305`).

### Tools and dependencies

- Mermaid, Excalidraw conversion, and rasterization bundled into `diagram-render.html`.
- `gstack-render`.
- Aside or bundled headless browser.
- `base64`, `shasum`, filesystem tools.

### Permissions and side effects

- Writes commit-ready files under `./diagrams/` when in a Git repository.
- Otherwise writes under `/tmp/gstack-diagrams/`.
- Creates secure temporary staging files.
- Opens a loopback server indirectly through `gstack-render`.
- No network rendering.

### Strongest unique methods

- **Source/editable/rendered package:** preserves both LLM-friendly source and human-editable output.
- **Content-addressed secure staging:** avoids mixed versions and unsafe shared temporary paths.
- **Single-call rendering:** keeps SVG, PNG, and Excalidraw consistent.
- **Explicit editability degradation:** unsupported Mermaid types are delivered with an honest image-only note.

### Weaknesses and failure modes

- The skill calls the result a “triplet,” but physically emits four files; the intended three representations are source, editable scene, and rendered pair.
- Mermaid is the source of truth only until an Excalidraw round trip; after manual scene edits, Mermaid and scene can diverge.
- Requires Bun and an available browser even though rendering is “offline.”
- Uses deprecated browser-side `escape()` for non-ASCII recovery.
- Large diagrams are handled by manual splitting rather than an explicit multi-file naming/index contract.

### Overlap, duplicate, and dependency candidates

- **Complement:** `/make-pdf` can render Mermaid fences directly.
- **Dependency:** shared `gstack-render` and browser fallback infrastructure.
- **Unique:** no substantial functional duplicate among the assigned roots.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `diagram/SKILL.md` | semantic-read | Entire author/render/delivery contract. |
| `diagram/SKILL.md.tmpl` | excluded | Generator source duplicate of canonical skill. |
| `skills/gstack/lib/diagram-render/dist/diagram-render.html` | excluded | Cross-root runtime dependency outside the assigned root; existence and role were verified through the root contract, but its implementation is owned by the parent/shared renderer root. |

---

## 6. `gstack/ios-clean`

### Exact root and skill path

- **Root:** `skills/gstack/ios-clean/`
- **Skill:** `skills/gstack/ios-clean/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Clean/remove/strip DebugBridge and gstack iOS instrumentation.
- Security-audit cleanup or migration away from gstack (`skills/gstack/ios-clean/SKILL.md:1-23`, `skills/gstack/ios-clean/SKILL.md:391-423`).

**Non-trigger**

- Routine Release safety; source and build guards are the real safety mechanism.
- General iOS cleanup.
- Removing unrelated test/QA infrastructure.

### Responsibility and non-responsibility

**Responsibility**

- Inventory and remove DebugBridge package references, debug-only startup wiring, snapshot markers, generated accessors, and best-effort device token.
- Verify release build and symbol absence.

**Non-responsibility**

- Does not modify business logic, views, view models, non-debug blocks, or unrelated testing.
- Does not force-push, amend, or delete SPM caches (`skills/gstack/ios-clean/SKILL.md:397-475`).

### Inputs

- iOS app source directory.
- `Package.swift`.
- App `@main` entry and generated `StateAccessor.swift`.
- Scheme and device UDID.
- User choice: proceed, dry-run, or abort.

### Outputs

- Removed DebugBridge wiring and generated files.
- Release build verification.
- Grep and symbol checks.
- Summary of removed material.

### Core workflow

1. Inventory imports, debug blocks, generated headers, and package references.
2. Present exact files/line counts and obtain confirmation.
3. Remove only approved instrumentation.
4. Build/install Release.
5. Verify no DebugBridge or snapshot markers remain.
6. Run release package build and binary symbol inspection.

### Branches

- Proceed, dry-run, or abort.
- Connected-device token removal versus best-effort skip.
- Incomplete removal produces missing-symbol build failure and stops.

### Rules, gates, and stop conditions

- Every removal category requires confirmation.
- Preserve surrounding code.
- Release-build failure on a missing DebugBridge symbol is a hard stop.
- No business-logic or non-debug modification.
- Git restore is the rollback path.

### Tools and dependencies

- Glob, grep, read, edit.
- SwiftPM, `xcodebuild`, `nm`.
- Connected iPhone for device token cleanup and install verification.

### Permissions and side effects

- Destructively removes generated files and source/package wiring after confirmation.
- Builds and installs a Release app on a real device.
- Best-effort removes the temporary token.
- Changes are intended to remain Git-reversible.

### Strongest unique methods

- **Explicit removal boundary:** enumerates what may and may not be touched.
- **Binary-level verification:** source grep is supplemented by `nm`.
- **Dry-run gate:** supports audit without mutation.

### Weaknesses and failure modes

- The root says `.when(configuration: .debug)` is the structural safety path, while the actual package template states source-level `#if DEBUG` is the guard that protects all integration forms and the package condition is insufficient for `.xcodeproj` consumers (`skills/gstack/ios-clean/SKILL.md:391-400`; `skills/gstack/ios-qa/templates/Package.swift.template:1-32`).
- `allowed-tools` lacks `Write`, yet the flow requires deleting generated files; the mechanism for deletion is not specified.
- `! grep -r` checks can produce false positives from docs, caches, or unrelated fixtures unless scoped narrowly.
- `xcodebuild ... build install` syntax is assumed and scheme discovery is unspecified.
- The token-removal step is listed in “what it removes” but no concrete device command is given.

### Overlap, duplicate, and dependency candidates

- **Inverse dependency:** reverses `/ios-qa` installation.
- **Conflict/variant:** `/ios-sync` regenerates the same bridge artifacts that this root removes.
- **Strong dependency:** release-safety truth lives in `/ios-qa` templates, not this root.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ios-clean/SKILL.md` | semantic-read | Entire inventory/removal/verification contract. |
| `ios-clean/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `ios-qa/templates/Package.swift.template` | semantic-read | Directly relevant external dependency needed to verify the claimed Release safety mechanism. |

---

## 7. `gstack/ios-design-review`

### Exact root and skill path

- **Root:** `skills/gstack/ios-design-review/`
- **Skill:** `skills/gstack/ios-design-review/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Review/audit/design-QA an iPhone app’s visuals on real hardware (`skills/gstack/ios-design-review/SKILL.md:1-24`, `skills/gstack/ios-design-review/SKILL.md:392-408`).

**Non-trigger**

- Plan-stage review: `/plan-design-review`.
- Live web visual audit: `/design-review`.
- Functional iOS bug fixing: `/ios-fix`.

### Responsibility and non-responsibility

**Responsibility**

- Capture each major iOS screen on a real device.
- Score ten iOS-specific design dimensions.
- Explain what would make each score a ten.
- Produce a screenshot-backed report and surface low scores.

**Non-responsibility**

- Read-only by default; no automated source fixes.
- Does not replace functional `/ios-qa`.
- Does not create product strategy or a web design system.

### Inputs

- Running iOS QA daemon or bootstrap capability.
- Real-device screenshots and accessibility elements.
- User-provided screen list or auto-discovered screens.
- `DESIGN.md`, Apple HIG expectations, and app state.

### Outputs

- Markdown report under `~/.gstack/projects/<slug>/`.
- Screenshots, per-screen ten-dimension scores, and leverage fixes.
- User decisions for dimensions below seven (`skills/gstack/ios-design-review/SKILL.md:409-478`).

### Core workflow

1. Connect to or spawn the iOS QA daemon.
2. Acquire a session.
3. Enumerate major screens.
4. Fetch screenshot and accessibility elements per screen.
5. Score typography, spacing, color, touch targets, states, accessibility, animation, iOS idioms, density, and AI-slop.
6. Write report.
7. Ask about recommended fixes for every score below seven.

### Branches

- User-provided screen list versus accessibility auto-discovery.
- Existing daemon versus `/ios-qa` bootstrap.
- Black/blank screenshot confirmation.
- Missing expected screens triggers a hidden-state question.
- Tailnet capability error requires owner-minted higher token.

### Rules, gates, and stop conditions

- Device interaction is read-only by default.
- Every dimension receives a score and “what makes it ten.”
- Any score below seven triggers a decision.
- Capability and missing-screen mismatches must be surfaced, not silently ignored.

### Tools and dependencies

- `gstack-ios-qa-daemon`.
- StateServer `/screenshot`, `/elements`, and session APIs.
- Real iPhone, Xcode/CoreDevice, and `/ios-qa` bootstrap.
- Apple HIG and `DESIGN.md`.

### Permissions and side effects

- Reads screenshots and accessibility tree.
- Writes local report and screenshots.
- May spawn the daemon and bootstrap bridge infrastructure if absent.
- It does not itself edit the app.

### Strongest unique methods

- **iOS-native ten-dimension rubric:** includes HIG idioms, Dynamic Type, VoiceOver, native navigation, and Material-design leakage.
- **What-would-make-it-ten framing:** converts a score into an actionable target.
- **Screen-count reconciliation:** detects hidden/unreached states against a known ground truth.

### Weaknesses and failure modes

- **Concrete capability contradiction:** the loop says `POST /session/acquire` with capability `observe`, but the daemon maps `/session/acquire` to `interact` (`skills/gstack/ios-design-review/SKILL.md:444-455`; `skills/gstack/ios-qa/daemon/src/types.ts:43-62`). An observe-only tailnet token will receive `403 capability_insufficient`. Smallest fix: either do not acquire for pure reads or require `interact`.
- The skill says “screenshots every screen,” but auto-discovery from the current accessibility tree cannot discover screens behind unexplored navigation without mutating interactions.
- “No tappable text smaller than 24pt” is not an Apple HIG touch-target rule; target size and glyph size are conflated.
- It says screenshots are included inline but does not specify durable screenshot paths or report-relative linking.
- Animation and hidden-state scoring cannot be established from one screenshot/tree per screen.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `/ios-qa`.
- **Platform variant:** `/design-review` for real iOS hardware.
- **Complement:** `/plan-design-review` before implementation.
- **Dependency candidate:** findings may feed `/ios-fix`, although `/ios-fix` is function-bug oriented rather than design-polish oriented.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ios-design-review/SKILL.md` | semantic-read | Complete device-design audit contract. |
| `ios-design-review/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `ios-qa/daemon/src/types.ts` | behavior-reviewed | Direct dependency defining actual capability requirements and exposing the observe/interact mismatch. |

---

## 8. `gstack/ios-fix`

### Exact root and skill path

- **Root:** `skills/gstack/ios-fix/`
- **Skill:** `skills/gstack/ios-fix/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Fix/patch/auto-fix an iOS bug, especially one found by `/ios-qa` (`skills/gstack/ios-fix/SKILL.md:1-25`, `skills/gstack/ios-fix/SKILL.md:390-410`).

**Non-trigger**

- Bug cannot be reproduced as a state snapshot.
- General refactoring or non-iOS fixes.
- Visual critique without a concrete behavioral bug.

### Responsibility and non-responsibility

**Responsibility**

- Reproduce a bug on a real device.
- Capture immutable pre-fix state and screenshot evidence.
- Trace the source root cause.
- Apply the smallest Swift fix.
- Rebuild, redeploy, restore the same state, verify visually, and add a real-device regression test.

**Non-responsibility**

- It does not guess at fixes without reproduction/root cause.
- It does not continue indefinitely after failed attempts.
- It does not treat a screenshot-only difference as sufficient state reproduction.

### Inputs

- `/ios-qa` finding, screenshot, and suspected accessibility node.
- Real-device session and state schema.
- Swift source, scheme, UDID, and app build.
- User decision if multiple plausible root causes exist.

### Outputs

- Pre-fix JSON snapshot and PNG.
- One-line bug/expected-behavior record.
- Minimal Swift fix.
- Post-fix PNG.
- Device-gated TypeScript regression test and committed fixtures (`skills/gstack/ios-fix/SKILL.md:407-474`).

### Core workflow

1. Drive device into failing state.
2. Capture snapshot and screenshot before editing.
3. Trace view, view model, data flow, and state mutation.
4. Ask only when multiple root causes remain plausible.
5. Edit Swift.
6. Build/install/redeploy.
7. Restore pre-bug snapshot.
8. Compare fresh screenshot.
9. Revert and retry if still failing, at most three iterations.
10. Add a `GSTACK_HAS_IOS_DEVICE=1` periodic regression test and commit.

### Branches

- UI actions versus direct snapshot-eligible state write for reproduction.
- Single root cause versus user-selected plausible cause.
- Success, build failure, schema mismatch, device disconnect, or three-iteration escalation.

### Rules, gates, and stop conditions

- Iron law: no fix without reproducing snapshot.
- Root cause required before edit.
- Diff must remain minimal.
- Three failed iterations is a hard stop.
- Build failure causes Swift edit reversion before investigation.
- Schema mismatch requires re-codegen and re-snapshot.
- Regression test is mandatory on success.

### Tools and dependencies

- `/ios-qa` daemon and StateServer APIs.
- Swift source tools.
- `xcodebuild`.
- Real iPhone.
- TypeScript/Bun test fixture environment.
- Git commit.

### Permissions and side effects

- Mutates device UI/state.
- Writes application Swift.
- Builds, installs, and launches app on physical hardware.
- Writes tests and binary/image fixtures.
- Commits the fix and evidence.
- May revert edits.

### Strongest unique methods

- **Snapshot-before-fix iron law:** makes a device state a durable regression fixture.
- **Same-state post-build restoration:** verifies the fix against the exact precondition.
- **Closed loop:** finding, root cause, fix, redeploy, restore, verify, test.
- **Schema-aware recovery:** recognizes accessor drift after rebuild.

### Weaknesses and failure modes

- Description promises “zero human intervention,” yet the workflow asks the user to choose among plausible root causes.
- A screenshot comparison is not defined as pixel, vision, or semantic comparison; “visibly persists” remains subjective.
- The test contract says it asserts post-fix behavior on a real device but does not specify the assertion API or expected value derived from the one-line record.
- `xcodebuild ... build install` assumes a deployment form not valid for every project.
- The regression fixture is stored under `test/fixtures`, but no cleanup or sensitive-data review is specified before committing state snapshots/screenshots.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `/ios-qa` and its snapshot/restore schema.
- **Dependency:** `/ios-sync` on `409 schema_mismatch`.
- **Complement:** `/ios-design-review` may surface visual issues but does not itself repair them.
- **Shared method candidate:** root-cause tracing overlaps `/investigate`, explicitly referenced by the skill.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ios-fix/SKILL.md` | semantic-read | Complete reproduce/fix/verify/test contract. |
| `ios-fix/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `ios-qa/templates/StateServer.swift.template` | behavior-reviewed | Direct dependency defining snapshot/restore, schema mismatch, sessions, and mutation behavior. |
| `ios-qa/scripts/gen-accessors.ts` | behavior-reviewed | Direct dependency producing the schema/accessors needed after rebuild. |

---

## 9. `gstack/ios-qa`

### Exact root and skill path

- **Root:** `skills/gstack/ios-qa/`
- **Skill:** `skills/gstack/ios-qa/SKILL.md`

### Trigger and non-trigger

**Trigger**

- iOS QA, test an iPhone app, find device bugs, or QA a SwiftUI app on real hardware (`skills/gstack/ios-qa/SKILL.md:1-27`, `skills/gstack/ios-qa/SKILL.md:399-433`).

**Non-trigger**

- Simulator-only testing.
- Apps lacking supported file-scope `@Observable` state unless an existing real-device harness is used.
- Projects where the skill would have to invent unsupported `.xcodeproj`/workspace package wiring.
- Production/TestFlight app replacement without an isolated safe QA build.

### Responsibility and non-responsibility

**Responsibility**

- Generate a Debug-only bridge and typed snapshot accessors.
- Build/deploy a debug app to a paired iPhone.
- Establish a CoreDevice tunnel and rotate the bootstrap token.
- Drive screenshot/tree/state/action verification loops.
- Optionally expose capability-scoped remote QA through Tailscale.
- Provide audit trails, session locking, and demo-mode attribution.

**Non-responsibility**

- No simulator, XCTest, or WebDriverAgent.
- Does not claim external provider success from fixture-driven state.
- Does not wire unsupported project forms by guesswork.
- Release safety is handled by source guards and invariant checks, not cleanup alone (`skills/gstack/ios-qa/SKILL.md:399-501`).

### Inputs

- macOS, Xcode/Swift ≥5.9, paired/unlocked USB iPhone.
- Swift app source and bundle/scheme information.
- File-scope `@Observable` classes.
- Explicit `// @Snapshotable` fields using supported JSON-native types.
- Optional Tailscale setup and allowlist.
- Optional warm-session cache or `--cold`.
- Test goal and optional demo/recording mode.

### Outputs

- Local DebugBridge SwiftPM package.
- Generated `StateAccessor.swift` and version marker.
- Installed debug app.
- Running daemon/session cache.
- Screenshots, accessibility trees, snapshots, findings, and audit logs.
- Optional remote tokens and allowlist entries.

### Core workflow

1. Warm-start if cache and daemon/device remain valid.
2. Validate observation model and packaging compatibility before modification.
3. Discover marked state and ask before bridge installation.
4. Run deterministic regenerator.
5. Wire DebugBridge products and debug startup.
6. Build/install/launch app.
7. Read file-based boot token and rotate to in-memory bearer.
8. Start single-instance daemon and CoreDevice keepalive.
9. For each QA iteration: screenshot, elements, snapshot, decide, acquire, mutate, re-screenshot, record, release.
10. Optionally bind tailnet listener after fail-closed WhoIs probe.
11. Enforce capability tiers and audit mutations.
12. In demo mode, prohibit direct state shortcuts (`skills/gstack/ios-qa/SKILL.md:399-501`).

### Branches

- Warm versus cold bootstrap.
- SwiftPM-compatible app versus stop/preserve installed production build.
- Local USB versus tailnet.
- Observe/interact/mutate/restore capability tiers.
- Normal versus recording versus demo mode.
- Cached tunnel versus one-time refresh after stale bearer/route.
- Accessibility activation versus synthesized private-API touch.
- TypeScript fast generator versus SwiftSyntax generator parity path.

### Rules, gates, and stop conditions

- Validate project compatibility before altering or replacing app.
- Only standalone marker comments opt fields into snapshots.
- Unsupported/custom/nested/private/untyped/duplicate-key declarations fail before generation.
- StateServer bearer rotates after bootstrap.
- Tailnet listener opens only after usable tailscaled LocalAPI probe.
- Remote identities require allowlist and minimum capability.
- Body sizes and screenshot sizes are capped.
- Mutations require an exclusive session lock.
- Ambiguous failed mutations are not replayed after tunnel refresh.
- Demo mode forbids direct state writes.
- Release code must not contain private DebugBridge symbols (`skills/gstack/ios-qa/SKILL.md:433-501`; `skills/gstack/ios-qa/daemon/src/index.ts:190-300`; `skills/gstack/ios-qa/templates/Package.swift.template:1-32`).

### Tools and dependencies

- Bun/TypeScript daemon and tests.
- Xcode `devicectl`, SwiftPM, SwiftSyntax, CryptoKit.
- Network.framework and UIKit.
- KIF-derived touch synthesis and dynamically loaded private iOS APIs, Debug-only.
- Tailscale LocalAPI.
- HTTP/JSON, accessibility APIs, `UIGraphicsImageRenderer`.
- Filesystem-backed allowlist/audit data.

### Permissions and side effects

- Adds DebugBridge source/package and app startup wiring.
- Reads app source.
- Builds, installs, launches, screenshots, and interacts with a physical iPhone.
- Opens loopback listeners; optionally opens a Tailscale-interface listener.
- Writes allowlist, audit, attempt, cache, PID, and session files under `~/.gstack`.
- Remote mutations are identity-attributed and audited.
- Uses private iOS APIs only in Debug builds.

### Strongest unique methods

- **Typed state snapshots from opt-in source markers.**
- **Two-phase cross-model restore:** validate every model before any application.
- **Schema-only accessor hash:** independent of unrelated source/build churn.
- **Boot-token rotation:** file bootstrap credential is one-use and replaced in memory.
- **Capability-scoped tailnet proxy:** observe/interact/mutate/restore tiers.
- **WhoIs canonicalization plus explicit allowlist.**
- **No replay of ambiguous mutations after tunnel loss.**
- **Front-most multi-window screenshot, accessibility, and interaction handling.**
- **Source-level Release guards around private APIs.**
- **Visible demo mode:** every operation goes through UI and carries attribution.

### Weaknesses and failure modes

- The skill describes StateServer as “loopback only,” but the current IPv6 listener binds wildcard and admits RFC 4193 ULA peers after a connection-level check so CoreDevice can reach it (`skills/gstack/ios-qa/SKILL.md:424-431`; `skills/gstack/ios-qa/templates/StateServer.swift.template:99-177`). The security boundary is restricted-peer acceptance, not literal loopback-only binding.
- The remote-tailnet listener defaults to `127.0.0.1` unless `GSTACK_IOS_TAILNET_BIND` is supplied; the skill does not document how the actual Tailscale address is selected.
- Private iOS selectors and dynamically loaded IOKit/Accessibility symbols are inherently OS-version fragile (`skills/gstack/ios-qa/templates/DebugBridgeTouch.m.template:1-54`, `skills/gstack/ios-qa/templates/DebugBridgeTouch.m.template:200-365`).
- `SessionTokenStore.heartbeat` can repeatedly extend a token by up to 24 hours from the current time; the comment’s “original max” is not stored or enforced (`skills/gstack/ios-qa/daemon/src/session-tokens.ts:52-72`).
- The local loopback daemon deliberately has no auth; any local process can control the device, with loopback binding as the sole boundary (`skills/gstack/ios-qa/daemon/src/index.ts:300-388`).
- Generator implementations are duplicated in TypeScript and SwiftSyntax, increasing parity risk despite tests.
- UI typing directly assigns `UITextField.text`/`UITextView.text`; it does not synthesize keystrokes and may miss application behavior tied to keyboard/input delegates.
- Programmatic swipe changes `contentOffset` rather than generating a real gesture.
- Full reliable operation is macOS/Xcode/device dependent and cannot be reproduced on ordinary CI.

### Overlap, duplicate, and dependency candidates

- **Platform foundation:** `/ios-design-review`, `/ios-fix`, `/ios-sync`, and `/ios-clean` all depend on this root.
- **Duplicate implementation candidate:** TypeScript scanner and SwiftSyntax generator implement the same schema rules.
- **Conditional variants:** local USB, tailnet, recording, and demo modes.
- **Complement:** `/ios-sync` maintains installed artifacts; `/ios-clean` removes them.
- **Complement:** `/ios-fix` converts findings into fixes and fixtures.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ios-qa/SKILL.md` | semantic-read | Complete bootstrap, runtime, security, and QA contract. |
| `ios-qa/docs/tailscale-acl-example.md` | semantic-read | Remote threat model, allowlist schema, ACL example, token lifetime, and audit contract. |
| `ios-qa/daemon/src/*.ts` | behavior-reviewed | All daemon runtime sources reviewed: allowlist, audit, minting, CLI, devicectl, listeners, proxy, tokens, singleton, WhoIs, bootstrap, and route types. |
| `ios-qa/templates/*.swift.template` | behavior-reviewed | State server, UI bridge, manager, wiring, overlay, and accessor behavior used in the app. |
| `ios-qa/templates/Package.swift.template` | semantic-read | Build products and Release-safety contract. |
| `ios-qa/templates/DebugBridgeTouch.h.template` | behavior-reviewed | Public touch-synthesis interface and platform conditions. |
| `ios-qa/templates/DebugBridgeTouch.m.template` | behavior-reviewed | Private-API touch implementation and actual source-level Release guard. |
| `ios-qa/scripts/gen-accessors.ts` | behavior-reviewed | TypeScript scanner, validation, cache, schema hash, rendering, and pruning. |
| `ios-qa/scripts/gen-accessors.test.ts` | behavior-reviewed | Directly validates parser isolation, cache identity, schema hash, optionals, restore atomicity, and SwiftSyntax parity. |
| `ios-qa/scripts/gen-accessors-tool/Package.swift` | semantic-read | Declares SwiftSyntax/SwiftParser behavior dependency. |
| `ios-qa/scripts/gen-accessors-tool/Sources/GenAccessors/main.swift` | behavior-reviewed | Complete SwiftSyntax generator implementation. |
| `ios-qa/daemon/test/*.test.ts` | excluded | Test-only fixtures/suites; corresponding production modules were behavior-reviewed. Their existence and bounded file set were inventoried. |
| `ios-qa/templates/*.template` not listed separately above | behavior-reviewed | Every listed template was read; rows are grouped by implementation role. |
| `ios-qa/SKILL.md.tmpl` | excluded | Generator source duplicate of canonical skill. |

---

## 10. `gstack/ios-sync`

### Exact root and skill path

- **Root:** `skills/gstack/ios-sync/`
- **Skill:** `skills/gstack/ios-sync/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Resync/update/regenerate the installed iOS debug bridge.
- Gstack upgrade.
- New observable classes/properties or moved snapshot markers (`skills/gstack/ios-sync/SKILL.md:1-24`, `skills/gstack/ios-sync/SKILL.md:390-415`).

**Non-trigger**

- First-time bridge installation; use `/ios-qa`.
- Full bridge removal; use `/ios-clean`.
- App-source feature changes unrelated to generated instrumentation.

### Responsibility and non-responsibility

**Responsibility**

- Detect installed versus upstream version.
- Deterministically regenerate supported bridge files and state accessor.
- Review that only generated bridge outputs changed.
- Build and verify the new schema on-device.

**Non-responsibility**

- It does not hand-edit canonical generated package files.
- It does not modify handwritten application Swift.
- It does not fetch arbitrary upstream files over HTTP.

### Inputs

- `.gstack-version`, upstream `VERSION`.
- App source and bridge directory.
- `@Observable` source and snapshot markers.
- Scheme and connected device.

### Outputs

- Refreshed bridge package.
- Refreshed generated accessor and completion/version marker.
- Verified package/app build.
- Relaunched bridge with new accessor hash.

### Core workflow

1. Compare installed and upstream versions.
2. Exit early if version and observable coverage are unchanged.
3. Run `gstack-ios-qa-regen` once.
4. Review generated diff.
5. Assert handwritten source untouched.
6. Run SwiftPM and Xcode builds.
7. Relaunch device app.
8. Verify snapshot returns new schema hash.

### Branches

- Up-to-date no-op versus regeneration.
- Compile success versus revert and user gate.
- Invalid marked declaration versus source correction/removal.
- Unchanged hash because no markers versus expected changed schema.
- Overbroad app-source scan versus narrow-source retry.

### Rules, gates, and stop conditions

- Upstream templates are authoritative.
- Only known obsolete flat files are removed.
- Generated bridge package must not be hand-edited.
- Invalid snapshot declarations fail before completion marker.
- Compile failure requires Git restore and surfaced error.
- Narrow app source is required to avoid scanning generated bridge files.

### Tools and dependencies

- `gstack-ios-qa-regen`.
- Generator implementations under `/ios-qa`.
- SwiftPM, `xcodebuild`.
- Git diff/restore.
- Real-device daemon and snapshot endpoint.

### Permissions and side effects

- Rewrites generated bridge files and accessor.
- Deletes known obsolete generated layout files.
- Builds and relaunches the app.
- Changes installed instrumentation version.
- Does not intentionally change handwritten app code.

### Strongest unique methods

- **Version plus semantic-change no-op gate.**
- **Narrow copy policy:** only supported upstream templates, not wildcard or HTTP fetch.
- **Generated-diff boundary:** handwritten source must remain unchanged.
- **Composite cache and strict source diagnostics.**

### Weaknesses and failure modes

- The skill says the cache key includes a lockfile, but both reviewed generator implementations hash generator version/tool rev, Swift version, platform, build ID, and Swift source content, not a lockfile (`skills/gstack/ios-sync/SKILL.md:425-439`; `skills/gstack/ios-qa/scripts/gen-accessors.ts:333-365`; `skills/gstack/ios-qa/scripts/gen-accessors-tool/Sources/GenAccessors/main.swift:107-135`). Either the claim should be removed or the launcher’s additional key material must be documented and verified.
- “No new `@Observable` classes” is not enough to detect marker/type/property changes; the later content hash does, but the early-exit criterion is underspecified.
- Installed-version equality does not prove generated templates are unmodified.
- Verification assumes a connected physical device and a known scheme.
- Reverting generated output after partial regeneration depends on a clean Git state but no clean-tree gate is specified.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `/ios-qa` generators and templates.
- **Inverse relation:** `/ios-clean`.
- **Dependency:** `/ios-fix` invokes this on schema mismatch.
- **Duplicate candidate:** version detection and regeneration could be a reusable `/ios-qa` maintenance unit rather than a separate independent implementation.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `ios-sync/SKILL.md` | semantic-read | Complete maintenance workflow. |
| `ios-sync/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `ios-qa/scripts/gen-accessors.ts` | behavior-reviewed | Direct regeneration/cache dependency. |
| `ios-qa/scripts/gen-accessors-tool/Sources/GenAccessors/main.swift` | behavior-reviewed | SwiftSyntax parity implementation. |
| `ios-qa/templates/*` | behavior-reviewed | Authoritative files copied by the regenerator; reviewed under the nested `/ios-qa` root. |

---

## 11. `gstack/plan-design-review`

### Exact root and skill path

- **Root:** `skills/gstack/plan-design-review/`
- **Skill:** `skills/gstack/plan-design-review/SKILL.md`

### Trigger and non-trigger

**Trigger**

- Review a design/UX plan, critique design decisions, or pre-implementation UI plan review.
- UI/UX-bearing plan in plan mode (`skills/gstack/plan-design-review/SKILL.md:1-23`, `skills/gstack/plan-design-review/SKILL.md:485-548`).

**Non-trigger**

- Live site visual audit.
- Pure backend/API/infrastructure plans with zero UI scope.
- Implementation itself.

### Responsibility and non-responsibility

**Responsibility**

- Select and confirm the review target.
- Audit design completeness before implementation.
- Generate and approve mockups by default when UI and designer exist.
- Run seven interactive review passes.
- Edit the plan with accepted design decisions.
- Produce implementation tasks, review logs/dashboard, and terminal review report.

**Non-responsibility**

- Does not implement application code.
- Does not silently decide unresolved design choices.
- Does not force design review onto a no-UI plan.

### Inputs

- Explicit plan/path/page/branch diff or active host plan.
- Git base branch and repository history/diff.
- `CLAUDE.md`, `DESIGN.md`, `TODOS.md`, prior review log.
- Brain product/brand/recent-decision digests.
- Optional designer and external design voices.
- User decisions at every non-trivial issue.

### Outputs

- Improved plan file.
- Approved mockup paths and constraints.
- “NOT in scope,” “What already exists,” state matrix, hierarchy diagrams, journey storyboard, responsive/accessibility specifications, unresolved decisions, and implementation tasks.
- JSONL tasks artifact.
- Review log/readiness dashboard.
- Terminal `## GSTACK REVIEW REPORT` with mandatory unresolved-decision sentinel (`skills/gstack/plan-design-review/SKILL.md:724-1142`; `skills/gstack/plan-design-review/sections/review-sections.md:1-430`).

### Core workflow

1. Resolve scope gate before any other tool call unless plan-mode/user-named exception applies.
2. Detect platform and base branch.
3. Run pre-review system audit and UI-scope check.
4. Load brain context.
5. Rate initial completeness and identify focus gaps.
6. Stop for user focus choice.
7. Generate sequential mockup variants by default when available.
8. Collect comparison-board approval.
9. Optionally gather outside voices.
10. Read review section and run all seven passes:
    - information architecture;
    - interaction states;
    - emotional journey;
    - AI-slop risk;
    - design-system alignment;
    - responsive/accessibility;
    - unresolved decisions.
11. Ask once per issue and edit the plan after each decision.
12. Optionally refresh mockups.
13. Propose TODOs individually.
14. Emit Markdown and JSONL implementation tasks.
15. Log review, display dashboard, append terminal report.
16. Run blocking exit-plan-mode self-check (`skills/gstack/plan-design-review/SKILL.md:485-1142`; `skills/gstack/plan-design-review/sections/review-sections.md:1-430`).

### Branches

- Plan-mode auto-selected active plan, explicit user target, or mandatory scope question.
- No UI scope early exit.
- Designer available versus text-only review.
- Mockup feedback submit versus regenerate/remix.
- Outside voices accepted versus skipped.
- Every issue can be accepted, deferred, or resolved by another option.
- Zero tasks still produces an empty JSONL file.
- Plan file present versus no-plan diff review.
- Next review recommendation varies with dashboard state.

### Rules, gates, and stop conditions

- Scope gate precedes all reads/commands unless an explicit exception applies.
- Step 0 focus question is a hard stop.
- Mockups precede detailed passes when UI and designer exist.
- All seven passes are mandatory; “no issues” must be stated explicitly.
- Every non-trivial issue gets its own `AskUserQuestion`; no batching.
- Plan file is the output, not a substitute for interaction.
- Comparison board, not chat, chooses mockups.
- TODO candidates are individually gated.
- Final report must be the last `##` section.
- Final non-whitespace line must be exact unresolved status.
- Review log and review-read are mandatory when a plan file exists.
- ExitPlanMode is blocked until all checks pass (`skills/gstack/plan-design-review/SKILL.md:505-548`, `skills/gstack/plan-design-review/SKILL.md:1090-1142`; `skills/gstack/plan-design-review/sections/review-sections.md:1-18`, `skills/gstack/plan-design-review/sections/review-sections.md:330-430`).

### Tools and dependencies

- Git, GitHub/GitLab CLI where available.
- Gstack designer and comparison board.
- Brain cache.
- Optional Codex and independent design voice.
- `jq` for task JSONL.
- Review log/read tools.
- Learnings, telemetry, plan editor.

### Permissions and side effects

- Reads repository history, diff, plans, conventions, design system, and TODOs.
- Writes only the plan while in plan mode, plus user-scoped design/task/review artifacts.
- May update `TODOS.md` outside restrictive plan contexts after individual approval.
- Opens local comparison boards.
- Logs review status and may refresh local brain cache.
- Does not implement code.

### Strongest unique methods

- **First-call scope gate:** prevents auditing the wrong target.
- **Interactive seven-pass ratchet:** rate, explain ten, decide, edit, re-rate.
- **State matrix and journey storyboard:** forces user-visible behavior rather than backend descriptions.
- **Mockups as planning evidence:** visuals are part of the plan, not post-plan polish.
- **Terminal review-report invariant:** protects plan readers from stale or buried review status.
- **Actionable task synthesis:** every task traces back to a specific finding.
- **Cross-review readiness dashboard:** situates design review against shipping gates.

### Weaknesses and failure modes

- The workflow is exceptionally long and has many stop points; interruption can leave a partially edited plan and incomplete terminal report.
- It says no code changes, but branch-diff target review can lack a plan file, limiting its promised “better plan” output.
- The “all seven passes for every plan type” rule conflicts with the earlier correct no-UI early exit; wording should preserve that explicit exception.
- It permits GitHub/GitLab remote CLI discovery in Step 0, creating network dependence for what can usually be resolved with local refs.
- “Run `$D setup`” is suggested when the design binary is unavailable even though `$D` is empty in that branch.
- JSONL artifact generation depends on `jq`; absence silently weakens `/autoplan` interoperability.
- The skill duplicates substantial review doctrine, AI-slop rules, comparison-board logic, and outside-voice machinery from other design roots.

### Overlap, duplicate, and dependency candidates

- **Complement:** `/design-review` validates implementation after plan completion.
- **Complement:** `/design-consultation` establishes missing `DESIGN.md`.
- **Dependency candidate:** `/design-shotgun` for broader visual exploration.
- **Dependency candidate:** `/design-html` after mockup approval.
- **Duplicate candidate:** seven-pass design hard rules overlap `/design-review`.
- **Shared unit candidate:** comparison-board feedback loop is duplicated with `/design-shotgun` and `/design-consultation`.
- **Strong dependency:** review-log/dashboard ecosystem and active plan file.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `plan-design-review/SKILL.md` | semantic-read | Complete scope, mockup, review, report, and exit-gate contract. |
| `plan-design-review/sections/review-sections.md` | semantic-read | Defines all seven passes, question contract, tasks, dashboard, and report. |
| `plan-design-review/sections/manifest.json` | semantic-read | Declares required section trigger. |
| `plan-design-review/SKILL.md.tmpl` | excluded | Generator source duplicate. |
| `plan-design-review/sections/review-sections.md.tmpl` | excluded | Generator source duplicate of rendered semantic section. |

---

# Cross-root relationship hypotheses

## Duplicate hypotheses

1. **Comparison-board feedback loop**
   - Repeated across `design-consultation`, `design-shotgun`, and `plan-design-review`.
   - Same board serving, `feedback.json`/`feedback-pending.json`, remix/reload, confirmation, and `approved.json` flow.
   - Candidate reusable unit: `design-variant-feedback-loop`.

2. **Taste-profile loading**
   - Near-duplicate logic in `design-consultation` and `design-shotgun`.
   - Candidate reusable unit: `load-and-rank-design-taste`, including decay and conflict handling.

3. **UX doctrine**
   - `design-html/sections/doctrine.md` and `design-shotgun/sections/doctrine.md` are semantically identical.
   - `design-review` and `plan-design-review` embed substantially the same usability doctrine directly.
   - Candidate canonical doctrine with root-specific application rules.

4. **AI-slop and hard design rules**
   - Strong duplication between `design-review` and `plan-design-review`.
   - Candidate common rubric with platform/context adapters.

5. **iOS accessor generation**
   - TypeScript and SwiftSyntax implementations intentionally duplicate parser, type-validation, schema-hash, cache, and Swift emission behavior.
   - Retain only as a justified implementation variant if parity tests remain mandatory; otherwise one implementation should become canonical.

## Complement hypotheses

1. `design-consultation` defines the system.
2. `plan-design-review` makes a UI plan implementation-ready.
3. `design-shotgun` explores visual alternatives.
4. `design-html` materializes an approved page.
5. `design-review` audits and fixes the live web result.

This is a coherent lifecycle rather than duplication if boundaries remain explicit.

For iOS:

1. `ios-qa` installs and operates the real-device harness.
2. `ios-design-review` performs read-oriented visual scoring.
3. `ios-fix` repairs a reproduced behavioral bug.
4. `ios-sync` maintains generated bridge artifacts.
5. `ios-clean` removes the instrumentation.

## Conflict hypotheses

1. **`ios-design-review` capability mismatch**
   - Requests `observe` while calling an `interact` endpoint.
   - This is a present contract conflict, not merely overlap.

2. **`design-review` rendered-only versus source-fix posture**
   - “Never read source” conflicts with source-based outside voices and the mandatory fix loop.
   - Likely intended rule: rendered evidence is authoritative during discovery.

3. **`ios-qa` loopback wording**
   - Skill-level “loopback only” conflicts with the template’s wildcard IPv6 bind plus ULA peer filter.
   - Security intent is consistent, terminology is not.

4. **`ios-clean` stated safety mechanism**
   - It emphasizes package conditional wiring, while the package template says source guards are the actual reliable protection.

5. **`ios-sync` cache-key claim**
   - Lockfile inclusion is not present in either reviewed generator.

6. **Design gradient policy**
   - General anti-slop rules reject default purple/blue gradients; landing-page rules encourage non-flat backgrounds and permit gradients.
   - This is resolvable as a conditional variant: purposeful non-purple gradient/image/texture for marketing only.

## Conditional variants

- Web live audit (`design-review`) versus iOS live audit (`ios-design-review`).
- Vanilla HTML versus framework component in `design-html`.
- New variant generation versus existing-screen evolve mode in `design-shotgun`.
- Local USB versus tailnet, normal versus recording, and normal versus demo in `ios-qa`.
- Flowchart/sequence element-editability versus image-element Excalidraw for other Mermaid types.
- Plan-file review versus branch-diff review in `plan-design-review`.

## Strong dependencies

| Consumer | Dependency | Reason |
|---|---|---|
| `design-html` | `design-shotgun`, `design-consultation`, or planning artifacts | Needs approved or sufficiently specified visual context. |
| `design-review` | Browser runtime and preferably `DESIGN.md` | Rendered evidence and calibration source. |
| `ios-design-review` | `ios-qa` | Uses daemon, StateServer, screenshots, and elements. |
| `ios-fix` | `ios-qa` | Requires snapshot, restore, interaction, and device tunnel. |
| `ios-sync` | `ios-qa` templates/generators | Regenerates the installed harness. |
| `ios-clean` | `ios-qa` artifact layout | Removes what `/ios-qa` installs. |
| `plan-design-review` | Active plan, review log, optional designer | Its durable output and exit gate depend on these. |
| `diagram` | Shared diagram-render bundle and `gstack-render` | Cannot fulfill output contract without them. |

# Unresolved questions

1. Should Capability Compiler model the large shared gstack preamble once as a dependency, or duplicate its permissions/gates into every root unit?
2. Should generated `.tmpl` files remain excluded as duplicate generator sources, or receive a distinct `generator-source` disposition beyond the current three-state Phase 1 contract?
3. Is the design comparison-board flow intended to be one canonical capability shared by three roots?
4. Is `design-html`’s mandatory Pretext use a product requirement, or may native CSS be selected when it satisfies the exact layout?
5. Which statement is authoritative for iOS StateServer exposure: literal loopback-only binding, or wildcard IPv6 with ULA peer admission?
6. Should pure-read `/ios-design-review` omit session acquisition, or should its minimum capability officially become `interact`?
7. Is lockfile material added by the external `gstack-ios-qa-regen` launcher? If so, the skill should cite that launcher rather than attributing the key to the checked-in generators.
8. Should `/ios-fix` fixtures undergo redaction before committing screenshots and state snapshots?
9. Is `/design-review` test-framework bootstrap intentionally part of design QA, or should it be delegated to a separate testing capability?
10. For `/plan-design-review` against a branch diff with no plan file, what durable artifact replaces the promised improved plan and terminal review report?

## Audit status

- Assigned roots with cited dossier sections: **11/11**
- Assigned `SKILL.md` files read completely: **11/11**
- Unreadable assigned sources: **0**
- Source mutations, network calls, remote Git operations, deployments, or subagent launches performed during this audit: **0**