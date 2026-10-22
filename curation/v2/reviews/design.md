# Capability Compiler V2 — Phase 1B Design / UX Semantic Audit

## Scope and method

Assigned roots audited:

1. `skills/design-taste-frontend`
2. `skills/extract-design-system`
3. `skills/frontend-design`
4. `skills/impeccable`
5. `skills/prototype`
6. `skills/redesign-existing-projects`
7. `skills/review-animations`
8. `skills/ui-ux-pro-max`
9. `skills/web-accessibility`
10. `skills/web-design-guidelines`

The Phase 1 contract requires root dossiers, complete `SKILL.md` semantic reads, support-file classification, explicit relationships, and no phase completion claim while any source, file classification, or conflict remains unresolved (`.specs/capability-compiler-v2/phase-1/phase-plan.md:1-17`, `:23-48`, `:60-84`). The coverage ledger currently classifies files as `semantic-review-required`, `behavior-review-required`, or excluded and records ownership and hashes (`curation/v2/coverage.json:1-13`, `:15-45`).

All ten assigned `SKILL.md` files were read completely. Supporting files were inspected according to their semantic or behavioral relevance. No old dossier was treated as proof. No network fetch, remote Git operation, mutation, test execution, merge, deployment, or subagent launch occurred.

---

## 1. `design-taste-frontend`

### Root and skill path

- Root: `skills/design-taste-frontend`
- Skill: `skills/design-taste-frontend/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Landing pages, portfolios, editorial/blog surfaces, and existing-site redesigns where the request calls for distinctive, non-templated frontend design. It begins by inferring page kind, audience, brand assets, reference signals, visual language, and accessibility/regulatory constraints (`skills/design-taste-frontend/SKILL.md:1-42`). |
| **Non-trigger** | Dashboards, dense product UI, data tables, multi-step forms, code editors, native mobile, and real-time collaboration UI are explicitly out of scope; the skill routes these to design systems or specialist components instead (`skills/design-taste-frontend/SKILL.md:999-1013`). |
| **Responsibility** | Infer a design direction, establish three numeric design dials, choose a design-system or aesthetic foundation, implement a React/Next/Tailwind-oriented marketing surface, resist repeated AI visual tells, add appropriate imagery and motion, preserve redesign invariants, and run a large pre-flight gate (`skills/design-taste-frontend/SKILL.md:15-98`, `:1015-1076`). |
| **Non-responsibility** | It does not deeply own product-task UI, complex forms, tabular applications, native mobile conventions, or collaborative interaction architecture. Its accessibility guidance is a visual/implementation guardrail, not a WCAG conformance method (`skills/design-taste-frontend/SKILL.md:999-1013`). |
| **Inputs** | User brief; page kind; audience; vibe words; URLs/screenshots/product references; existing logo, color, type and photography; current package dependencies; redesign IA, content, SEO, analytics, and accessibility baseline (`skills/design-taste-frontend/SKILL.md:15-40`, `:908-959`). |
| **Outputs** | One-line “Design Read”; explicit `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY`; chosen foundation; implemented frontend; real/generated imagery or explicit asset placeholders; mobile fallbacks; dark/light mode behavior; pre-flight result (`skills/design-taste-frontend/SKILL.md:30-47`, `:50-98`, `:1015-1076`). |
| **Core workflow** | 1. Infer brief. 2. Ask one clarifying question only if materially ambiguous. 3. Set dials. 4. Choose one official design system or an honestly labeled native aesthetic. 5. Implement using the prescribed architecture and visual rules. 6. Apply contextual motion/assets. 7. Audit redesign preservation when applicable. 8. Run the mechanical pre-flight checklist (`skills/design-taste-frontend/SKILL.md:15-98`, `:908-997`, `:1015-1076`). |
| **Branches** | Greenfield; redesign-preserve; redesign-overhaul. Real design-system versus aesthetic implementation. Motion bands 1-3, 4-7, and 8-10. Image-generation available, web-image fallback, or explicit placeholders. Public-sector and regulated contexts override aesthetic preferences (`skills/design-taste-frontend/SKILL.md:15-28`, `:78-98`, `:464-493`, `:908-959`). |
| **Rules, gates, stop conditions** | Ask exactly one design question only when ambiguity changes direction; one design system per project; verify dependencies before import; hero, navigation, CTA, eyebrow, bento, layout-family, copy, theme, image, motion, reduced-motion, mobile, and performance gates; every final checkbox must pass. Unsupported requested surface types must be routed elsewhere (`skills/design-taste-frontend/SKILL.md:30-47`, `:1015-1076`). |
| **Tools and dependencies** | React/Next.js, RSC and client leaves, Tailwind v4, Motion, GSAP/ScrollTrigger for pinned/scrubbed work, official design-system packages, `next/font` or self-hosted fonts, image-generation tooling or web images, Simple Icons/devicon for real logos, Lighthouse (`skills/design-taste-frontend/SKILL.md:128-186`, `:464-493`, `:533-595`). |
| **Permissions and side effects** | May install missing frontend packages after checking `package.json`; may generate or reference imagery; may change application code and styling. Redesign mode forbids silent route, nav-label, form-field, logo, legal-copy, analytics, or IA changes (`skills/design-taste-frontend/SKILL.md:128-186`, `:933-959`). |
| **Strongest unique methods** | The three-dial model; one-line Design Read; strict anti-default catalog; mechanical eyebrow count; hero text-stack limits; explicit image-source priority; preservation-aware redesign decision tree; exhaustive pre-flight matrix (`skills/design-taste-frontend/SKILL.md:30-98`, `:287-402`, `:464-519`, `:908-997`, `:1015-1076`). |
| **Weaknesses and failure modes** | The 1,200-line rule set is internally difficult to prioritize. Its many universal bans can override an otherwise valid brief despite an earlier claim that rules are contextual. The requirement for imagery even on restrained editorial work can force unnecessary assets. Mandatory consumer dual-mode conflicts with its page-level “one theme” language unless interpreted as one active theme with two available schemes. The predefined stack and icon preferences risk migrating an incumbent project rather than adapting to it (`skills/design-taste-frontend/SKILL.md:7-12`, `:128-186`, `:464-493`, `:571-595`). |
| **Overlap / duplicate / dependency candidates** | Strong duplicate of `frontend-design` and `redesign-existing-projects` for anti-template visual direction; overlaps `impeccable` new-work/craft floor, `ui-ux-pro-max` dials/search, and `review-animations`; should depend on `web-accessibility` for conformance depth and on `extract-design-system` or `impeccable document/extract` for incumbent token evidence. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/design-taste-frontend/SKILL.md` | semantic-read | Sole root file; contains the full trigger, architecture, visual rules, code skeletons, redesign protocol, exclusions, and final gate. |
| No support files present | excluded | Root contains no references, scripts, templates, examples, or assets beyond `SKILL.md`. |

---

## 2. `extract-design-system`

### Root and skill path

- Root: `skills/extract-design-system`
- Skill: `skills/extract-design-system/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | User wants to reverse-engineer visual primitives from a public website, optionally producing project-local starter token files (`skills/extract-design-system/SKILL.md:1-9`). |
| **Non-trigger** | Full component-library recreation, pixel-perfect cloning, extraction from a private/unreachable site, automatic app restyling, or treating one page as the entire product system (`skills/extract-design-system/SKILL.md:10-18`, `:48-56`). |
| **Responsibility** | Gather URL and output intent, execute the extractor, review normalized output, summarize likely tokens, explain generated artifacts, and gate further app changes on confirmation (`skills/extract-design-system/SKILL.md:10-46`). |
| **Non-responsibility** | It does not infer unobserved components or semantic tokens, prove completeness, or modify existing application code/styles/config without a separate confirmation (`skills/extract-design-system/SKILL.md:48-56`). |
| **Inputs** | Public URL; extraction-only versus starter-file intent; optionally an existing `.extract-design-system/normalized.json` (`skills/extract-design-system/SKILL.md:10-18`, `:29-38`). |
| **Outputs** | `.extract-design-system/raw.json`, `.extract-design-system/normalized.json`, `design-system/tokens.json`, and `design-system/tokens.css`; user-facing summary of colors, fonts, spacing, radii, and shadows (`skills/extract-design-system/SKILL.md:20-46`; `skills/extract-design-system/references/outputs.md:1-19`). |
| **Core workflow** | Confirm public reachability; install Chromium if missing; run `npx extract-design-system <url>`; inspect normalized JSON; optionally use `--extract-only`; optionally regenerate files with `init`; explain artifacts; ask before integrating (`skills/extract-design-system/SKILL.md:20-46`; `skills/extract-design-system/references/workflow.md:1-14`). |
| **Branches** | Full extraction and starter generation; extraction-only; initialization from existing normalized output (`skills/extract-design-system/SKILL.md:20-38`). |
| **Rules, gates, stop conditions** | Target must be public and reachable. Extracted third-party content is untrusted. Existing design systems or application styles are not overwritten without confirmation. Completeness and authority must not be claimed from partial/dynamic content or one page (`skills/extract-design-system/SKILL.md:20-21`, `:48-56`; `skills/extract-design-system/references/workflow.md:1-14`). |
| **Tools and dependencies** | `npx`, Playwright Chromium, the external `extract-design-system` CLI, and underlying `dembrandt` raw extraction (`skills/extract-design-system/SKILL.md:20-38`; `skills/extract-design-system/references/outputs.md:1-7`). |
| **Permissions and side effects** | Network access to the public website and package registry may be required. `npx playwright install chromium` installs a browser. Full extraction writes two hidden extraction files and two design-system files. `init` rewrites generated token outputs. Existing app code remains gated (`skills/extract-design-system/SKILL.md:20-46`). |
| **Strongest unique methods** | Separates raw extraction from a stable normalized representation and from consumable token files; supports independent extraction and regeneration phases (`skills/extract-design-system/references/workflow.md:1-14`; `skills/extract-design-system/references/outputs.md:1-19`). |
| **Weaknesses and failure modes** | No local behavior-bearing implementation is present in this root, so the actual CLI schema, URL safety, overwrite semantics, crawl breadth, and normalization quality cannot be verified here. The package version is unpinned in the documented `npx` command. “Public and reachable” lacks a local protocol/host safety procedure. |
| **Overlap / duplicate / dependency candidates** | Complements `impeccable extract` and `impeccable document`: this root extracts from an external public site, while Impeccable extracts reusable patterns from local implementation. It can feed `ui-ux-pro-max` or frontend-building skills, but its output must remain evidence rather than authority. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/extract-design-system/references/workflow.md` | semantic-read | Defines command sequencing, trust boundary, extraction-only path, and regeneration precondition (`:1-14`). |
| `skills/extract-design-system/references/outputs.md` | semantic-read | Defines the meaning and consumer role of all four output artifacts (`:1-19`). |
| External `extract-design-system` / `dembrandt` implementation | excluded | Not present under the assigned root; external CLI behavior cannot be inferred from wrapper documentation. |

---

## 3. `frontend-design`

### Root and skill path

- Root: `skills/frontend-design`
- Skill: `skills/frontend-design/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | New or reshaped web UI needing an intentional visual identity, especially when templated or cliché output has been rejected (`skills/frontend-design/SKILL.md:1-10`). |
| **Non-trigger** | It does not present itself as an accessibility conformance audit, design-system extractor, motion-only reviewer, or implementation automation tool. |
| **Responsibility** | Ground the direction in subject matter, make deliberate type/palette/layout decisions, produce a compact design plan, self-check it against generic defaults, build only after that critique, and maintain a responsive/accessibility quality floor (`skills/frontend-design/SKILL.md:8-18`, `:20-69`). |
| **Non-responsibility** | It does not define package installation, a required stack, evidence-backed WCAG verification, browser automation protocol, or preservation mechanics for high-risk redesign details. |
| **Inputs** | Brief; subject; concrete audience; primary job; remembered client preferences; real content; screenshots when available (`skills/frontend-design/SKILL.md:8-18`, `:53-69`). |
| **Outputs** | A short plan containing 4-6 named colors with hex values, selected typefaces and roles, layout descriptions and ASCII wireframes, high-level principles, a uniqueness self-review, then code (`skills/frontend-design/SKILL.md:53-69`). |
| **Core workflow** | Identify or propose subject/audience/job; derive characteristic first-view content; choose deliberate type and structural devices; plan tokens/layout/principles; compare against generic defaults; revise; build; visually critique and remove excess (`skills/frontend-design/SKILL.md:8-18`, `:20-69`, `:71-77`). |
| **Branches** | Brief-specified direction wins; unspecified axes are used for subject-specific experimentation. Subject missing leads to a concrete proposal and client confirmation. Motion can be user-triggered, one orchestrated non-triggered moment, or omitted (`skills/frontend-design/SKILL.md:8-18`, `:20-52`). |
| **Rules, gates, stop conditions** | Real subject matter and content are required; structural devices must encode information; avoid generic one-word emphasis, all-caps labels, and unnecessary labels; non-user-triggered motion is sparse; revise any plan that could be reused unchanged for a similar brief; spend boldness in one place (`skills/frontend-design/SKILL.md:20-52`, `:53-77`). |
| **Tools and dependencies** | No mandatory package or framework. Screenshots are recommended when supported. Implementation follows the project’s existing CSS conventions (`skills/frontend-design/SKILL.md:64-77`). |
| **Permissions and side effects** | May propose and write UI code and copy. Subject invention is allowed only as a proposal requiring confirmation. It has no explicit destructive-operation or dependency-install permission. |
| **Strongest unique methods** | Two-pass “plan, then genericity critique” discipline; subject-world grounding; “one memorable thing” restraint; unusually strong UX-writing guidance for consistent action vocabulary, failures, and empty states (`skills/frontend-design/SKILL.md:53-77`, `:79-101`). |
| **Weaknesses and failure modes** | It lacks an explicit incumbent-code preservation protocol, technical pre-flight, state inventory, or evidence boundary. The typography rule rejects single-word emphasis broadly while `design-taste-frontend` endorses same-family italic/bold emphasis. Its design plan requires fixed hex values even when a project’s normative color format is not hex. |
| **Overlap / duplicate / dependency candidates** | Strong duplicate of `design-taste-frontend` and Impeccable new-work on anti-template direction and self-critique. Complement to `web-accessibility` for interaction contracts and `prototype` for evaluating multiple directions. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/frontend-design/LICENSE.txt` | excluded | Legal text; no reusable design method or behavior. |
| No references/scripts/examples/templates | excluded | Root has no other support content. |

---

## 4. `impeccable`

### Root and skill path

- Root: `skills/impeccable`
- Skill: `skills/impeccable/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Broad frontend/UI lifecycle: initialize product context, plan, build, document, extract, critique, audit, refine, animate, adapt, optimize, visually iterate, and maintain Impeccable artifacts. Explicitly excludes backend-only/non-UI work (`skills/impeccable/SKILL.md:1-16`). |
| **Non-trigger** | Backend-only work, non-UI scripts, and actions not routed through its command model. No-argument invocation presents a menu rather than auto-running (`skills/impeccable/SKILL.md:1-16`, `:83-101`). |
| **Responsibility** | Own the full frontend design lifecycle: persistent `PRODUCT.md` and `DESIGN.md`, visual-authority decisions, visitor modes, new-work concept selection, scoped command routing, local detection, browser live variants, finish review, documentation, and drift maintenance (`skills/impeccable/SKILL.md:18-101`). |
| **Non-responsibility** | Individual command references constrain scope: audit reports but does not fix; shape stops before code; doctor maintains artifacts but does not redesign; extract requires demonstrated reuse; platform-specific work routes to native references (`skills/impeccable/reference/audit.md:1-7`, `skills/impeccable/reference/shape.md:1-55`, `skills/impeccable/reference/doctor.md:1-30`, `skills/impeccable/reference/extract.md:1-57`). |
| **Inputs** | User request and explicit command; target path/route; project source; `PRODUCT.md`; `DESIGN.md`; surface brief; tokens/theme/components/assets; platform; screenshots; approved comp; detector findings; user constraints and approvals (`skills/impeccable/SKILL.md:18-45`; `skills/impeccable/reference/new-work.md:1-42`). |
| **Outputs** | Depending on route: product record, confirmed design brief, visual direction, implemented UI, `DESIGN.md` and sidecar, audit/critique report, extracted components/tokens, live variants, screenshots, detector findings, finish-review disposition, or drift report (`skills/impeccable/SKILL.md:47-81`). |
| **Core workflow** | Run context loader once; select one command/playbook or new-work; inspect target plus incumbent visual truth; establish product/visual authority; choose visitor mode; plan or build; load craft floor before editing; inspect in bounded screenshot rounds; run detector where applicable; finish-review; document shipped system (`skills/impeccable/SKILL.md:18-45`; `skills/impeccable/reference/new-work.md:1-42`, `:151-228`). |
| **Branches** | Persuade, Operate, Read, Experience; web versus iOS/Android/adaptive; established world, incomplete brand, new world, or redesign; comp-led versus code-led; explicit command versus no-argument routing; hooks active versus manual detector; live variant versus ordinary build (`skills/impeccable/SKILL.md:47-101`; `skills/impeccable/reference/new-work.md:1-42`). |
| **Rules, gates, stop conditions** | Brief wins; refinement preserves while redesign replaces only visuals; no silent drift repair; `PRODUCT.md` required for new work; visual-world selection and concept-seed gate for replacement worlds; approved comp controls comp-led builds; bounded inspection rounds; reviewer disposition is binding; new world is unfinished until review and documentation (`skills/impeccable/SKILL.md:35-45`, `:83-116`; `skills/impeccable/reference/new-work.md:44-149`, `:151-228`). |
| **Tools and dependencies** | Node.js scripts, local detector, filesystem, optional image generation/conversion, browser automation/live HMR, platform simulators/emulators, optional Git-derived staleness checks, project package tooling. The root exposes many behavior-bearing scripts through constrained Bash allowances (`skills/impeccable/SKILL.md:10-16`, `:18-31`). |
| **Permissions and side effects** | Extensive: creates/updates `PRODUCT.md`, `DESIGN.md`, `.impeccable/*`, prototypes, generated assets, provider hooks, config and surface briefs; can install hook manifests; can run local servers and inject development scripts; can pin/unpin command skills; can edit application UI. Destructive or replacement actions are usually gated by explicit scope, approvals, or narrow markers (`skills/impeccable/SKILL.md:104-116`; `skills/impeccable/reference/hooks.md:1-44`; `skills/impeccable/reference/live.md:1-52`). |
| **Strongest unique methods** | Persistent separation of product truth, visual system, and surface strategy; visual-authority classification; random/dealt direction process to fight default convergence; comp-led fidelity inventory and provenance; four-word finish-review disposition; bounded two-round inspection; live element-level variant workflow; artifact drift doctor (`skills/impeccable/reference/new-work.md:1-149`, `:151-228`; `skills/impeccable/reference/visualize.md:1-112`; `skills/impeccable/reference/doctor.md:1-83`). |
| **Weaknesses and failure modes** | Very high operational complexity and many mandatory stateful artifacts. Several flows assume subagents, image generation, browser automation, or provider-specific hooks. The huge new-work protocol can dominate a modest UI request. Command rules are not always mutually consistent: craft floor bans all eyebrows while other roots merely ration them; animate permits bounded blur/mask/shadow while motion-review roots emphasize transform/opacity; new-work strongly prefers external decision machinery even when the user supplied a precise direction. `harden.md` currently contains no usable playbook beyond a clean-status fragment (`skills/impeccable/reference/harden.md:1-2`). |
| **Overlap / duplicate / dependency candidates** | Superset/orchestrator candidate over `frontend-design`, `redesign-existing-projects`, `prototype`, and parts of `design-taste-frontend`. Its audit should depend on `web-accessibility` for standards-depth rather than treating a score as conformance. Its animate command complements, but should not replace, `review-animations`. Its document/extract commands overlap `extract-design-system` only for local code, not remote extraction. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/impeccable/reference/new-work.md` | semantic-read | Governs visual authority, concept selection, comp/code build path, implementation, review, and documentation lifecycle (`:1-228`). |
| `skills/impeccable/reference/craft-floor.md` | semantic-read | Defines mandatory quality floor and default-pattern refusals (`:1-47`). |
| `skills/impeccable/reference/{shape,critique,audit,polish,animate,adapt,optimize,extract,document,live,init,doctor,hooks,operate}.md` | semantic-read | Command-specific semantic contracts, gates, outputs, and handoffs. Representative contracts were read directly; e.g. shape stops before code (`shape.md:1-55`), audit reports only (`audit.md:1-112`), and extract requires 3+ repeated uses (`extract.md:1-57`). |
| `skills/impeccable/reference/{bolder,quieter,distill,onboard,colorize,typeset,layout,delight,overdrive,clarify}.md` | semantic-read | Focused refinement/enhancement playbooks; directly affect routing, scope, and visual-rule conflict analysis. |
| `skills/impeccable/reference/{ios,android,adapt.native,audit.native}.md` | semantic-read | Native-platform variants; separate platform conformance from web detector logic (`ios.md:1-53`; `android.md:1-57`; `audit.native.md:1-119`). |
| `skills/impeccable/reference/visualize.md` | semantic-read | Comp generation, approval, fidelity inventory, asset media gate, and provenance contract (`:1-112`). |
| `skills/impeccable/reference/degraded/*.md` | semantic-read | Inline fallbacks for asset production, documentation, finish review, and manual-edit application; they preserve output contracts when subagents are unavailable. |
| `skills/impeccable/reference/harden.md` | semantic-read | Current content was read; it provides no substantive hardening workflow, only a two-line status fragment. |
| `skills/impeccable/scripts/context.mjs` | behavior-reviewed | Resolves project/workspace context, product/design/surface files, platform, staleness, and optional update checks (`:1-77`, `:79-190`). It may perform a throttled network update check, though failures are intended to be silent. |
| `skills/impeccable/scripts/detect.mjs` and `scripts/detector/**` | behavior-reviewed | Local entrypoint locates bundled detector implementation and executes it (`detect.mjs:1-20`); detector subtree is behavior-bearing rule/engine infrastructure. |
| `skills/impeccable/scripts/{doctor,hook-admin,pin,live}.mjs` | behavior-reviewed | Representative mutating lifecycle scripts: doctor inspects/fixes artifacts (`doctor.mjs:1-69`), hook-admin writes project/provider config (`hook-admin.mjs:1-80`), pin creates/removes skill shortcuts (`pin.mjs:1-153`), and live boots helper server/injection/context (`live.mjs:1-187`). |
| `skills/impeccable/scripts/live/**`, `scripts/live-*.mjs` | behavior-reviewed | Stateful live-edit protocol, source wrapping, event validation, browser injection, acceptance, cleanup, and session persistence. Behavior is semantically governed by `reference/live.md`. |
| `skills/impeccable/scripts/lib/**` | behavior-reviewed | Shared parsing, path resolution, staleness, artifact, config, provider, and surface-brief behavior used by command entrypoints. |
| `skills/impeccable/scripts/modern-screenshot.umd.js` | excluded | Vendored/generated browser bundle; implementation internal rather than reusable capability semantics. |
| `skills/impeccable/scripts/command-metadata.json` | semantic-read | Metadata used by `pin.mjs` to generate command shortcuts; directly affects generated skill descriptions (`pin.mjs:54-85`). |
| Test/fixture-like content under detector/live internals | excluded | Validation fixtures and framework adapters are implementation evidence, not standalone reusable UI methods; behavior is represented by the owning script contracts. |

---

## 5. `prototype`

### Root and skill path

- Root: `skills/prototype`
- Skill: `skills/prototype/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Explicit invocation to build several genuinely different variants of one described UI piece and let the user choose visually. Model auto-invocation is disabled (`skills/prototype/SKILL.md:1-10`). |
| **Non-trigger** | Existing-UI review, animation review, remediation planning, dependency selection, whole-dashboard exploration without narrowing, or silent production changes (`skills/prototype/SKILL.md:8-10`, `:24-31`). |
| **Responsibility** | Scope one UI piece, inspect product stack/tokens/personality/context, name divergent axes, build 3-5 complete variants in isolation, render one at a time behind a fixed picker, verify all interactions, wait for user selection, then optionally promote one (`skills/prototype/SKILL.md:8-31`, `:33-90`). |
| **Non-responsibility** | It does not choose the winner, touch production during exploration, or preserve prototypes after promotion unless requested (`skills/prototype/SKILL.md:24-31`, `:69-90`). |
| **Inputs** | Description of one UI piece; project stack and styling system; motion library; tokens; personality; surrounding context; optional variant count and follow-up command (`skills/prototype/SKILL.md:33-57`, `:92-101`). |
| **Outputs** | Isolated prototype route or self-contained HTML, default three working variants, fixed picker harness, comparison/trade-off table, URL/file path and keyboard instructions; after `keep`, integrated winner and deleted prototype (`skills/prototype/SKILL.md:59-101`). |
| **Core workflow** | Scope, recon, choose named axes, build picker harness, verify and hand off, stop for user choice, promote only after selection (`skills/prototype/SKILL.md:33-90`). |
| **Branches** | Existing project route versus standalone HTML; default three versus up to five variants; `riff`, `keep`, or `keep … leave the picker`; replay control only when motion exists (`skills/prototype/SKILL.md:59-101`; `skills/prototype/PICKER.md:1-18`). |
| **Rules, gates, stop conditions** | One UI thing per run; variants must differ on named axes; all variants must fully work with realistic content; picker copied verbatim; one full-size variant at a time; instant variant switching; stop after handoff until user chooses (`skills/prototype/SKILL.md:24-31`, `:48-90`). |
| **Tools and dependencies** | Existing framework/dev server or plain HTML/CSS/JS; project motion library if present; browser/console and optional screenshot tooling; keyboard and URL parameter state (`skills/prototype/SKILL.md:33-76`; `skills/prototype/PICKER.md:90-147`). |
| **Permissions and side effects** | Creates isolated prototype files/routes. No production imports are allowed during exploration. Promotion modifies production only after a user choice and deletes the prototype by default (`skills/prototype/SKILL.md:24-31`, `:80-90`). |
| **Strongest unique methods** | Divergence must be declared by axis before code; visual comparison occurs at real scale rather than thumbnails; picker chrome is standardized so it cannot bias the comparison; URL and keyboard state support repeated evaluation (`skills/prototype/SKILL.md:12-22`, `:48-76`; `skills/prototype/PICKER.md:90-147`). |
| **Weaknesses and failure modes** | No acceptance criteria beyond rendering/interactions/console. The fixed picker intentionally animates `width`, conflicting with the root’s own transform/opacity craft statement, though the exception is documented. Production integration testing is underspecified. There is no explicit accessibility contract for the prototype variants beyond reduced motion and picker semantics (`skills/prototype/PICKER.md:70-89`). |
| **Overlap / duplicate / dependency candidates** | Overlaps Impeccable live variants and new-work direction rounds. It is narrower and simpler: isolated one-component divergence without persistent product/design artifacts. It should depend on project design truth and can use `review-animations` for motion-heavy variants. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/prototype/PICKER.md` | semantic-read | Exact markup, CSS, accessibility states, keyboard behavior, URL persistence, replay behavior, and intentional width-animation exception (`:1-147`). |
| No scripts/examples/assets present | excluded | Picker behavior is specified as a semantic template rather than shipped executable files. |

---

## 6. `redesign-existing-projects`

### Root and skill path

- Root: `skills/redesign-existing-projects`
- Skill: `skills/redesign-existing-projects/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Existing website or application needs a premium visual upgrade without breaking functionality and regardless of styling framework (`skills/redesign-existing-projects/SKILL.md:1-9`). |
| **Non-trigger** | Greenfield product discovery, full framework migration, backend-only tasks, or an explicitly requested clean-sheet visual replacement. |
| **Responsibility** | Scan incumbent stack and visual patterns, diagnose a long anti-pattern checklist, apply targeted fixes in priority order, preserve functionality, and remain within the current stack (`skills/redesign-existing-projects/SKILL.md:7-14`, `:204-225`). |
| **Non-responsibility** | It does not deeply own IA research, product strategy, component extraction, formal accessibility evidence, or user approval for a new visual world. |
| **Inputs** | Existing codebase, framework and styling method, current design patterns, dependencies, Tailwind version, functional behavior (`skills/redesign-existing-projects/SKILL.md:7-14`, `:219-225`). |
| **Outputs** | Diagnostic list of generic patterns, missing states and weak points; focused code/style upgrades; tested preservation of behavior (`skills/redesign-existing-projects/SKILL.md:7-14`, `:204-225`). |
| **Core workflow** | Scan, diagnose by typography/color/layout/interactivity/content/components/icons/code/omissions, then fix in risk-weighted order: font, palette, states, layout, generic components, missing lifecycle states, final type polish (`skills/redesign-existing-projects/SKILL.md:7-14`, `:204-225`). |
| **Branches** | Tailwind versus another framework versus vanilla CSS; marketing versus dense dashboard guidance; alternative layout/component upgrades selected according to observed problem (`skills/redesign-existing-projects/SKILL.md:52-88`, `:219-225`). |
| **Rules, gates, stop conditions** | No framework migration; no functionality breakage; test after every change; check dependency file before imports; check Tailwind version; keep changes reviewable and focused (`skills/redesign-existing-projects/SKILL.md:219-225`). |
| **Tools and dependencies** | Existing stack; dependency manifest; optional placeholder photography; ordinary CSS/framework tooling. No bundled script (`skills/redesign-existing-projects/SKILL.md:40-51`, `:219-225`). |
| **Permissions and side effects** | Modifies current UI code and styles. May add imagery, interaction states, metadata, validation, legal links, skip links, consent, or a favicon where missing. New libraries require dependency inspection (`skills/redesign-existing-projects/SKILL.md:90-180`, `:219-225`). |
| **Strongest unique methods** | Broad audit taxonomy plus explicit visual-impact/minimum-risk ordering; strong focus on missing loading/empty/error states, semantic HTML, import verification, and quiet strategic omissions (`skills/redesign-existing-projects/SKILL.md:90-180`, `:204-225`). |
| **Weaknesses and failure modes** | Several prescriptions conflict with safer sibling roots: it encourages “organic, messy” fabricated numbers while `design-taste-frontend` bans fake precision unless real or labeled; it suggests blanket smooth scrolling without reduced-motion qualification; it says radii should vary while `design-taste-frontend` demands a documented shape scale; it recommends adding cookie consent/legal links without first establishing jurisdiction/product requirement. Its animation-upgrade section encourages broad stagger/spring/scroll reveals despite an earlier targeted-fix posture (`skills/redesign-existing-projects/SKILL.md:52-88`, `:112-164`, `:182-202`). |
| **Overlap / duplicate / dependency candidates** | Near-duplicate of the redesign protocol in `design-taste-frontend` and of Impeccable’s polish/bolder/layout/colorize commands. Best retained as a lightweight audit-and-fix variant; should depend on `web-accessibility` for a11y and on a product/brand authority source before changing visual identity. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/redesign-existing-projects/SKILL.md` | semantic-read | Sole root file; contains full scan/diagnose/fix taxonomy and priority model. |
| No support files present | excluded | No scripts, references, templates, examples, or assets. |

---

## 7. `review-animations`

### Root and skill path

- Root: `skills/review-animations`
- Skill: `skills/review-animations/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Explicit request to review animation or motion code against a strict craft standard. Auto-invocation is disabled (`skills/review-animations/SKILL.md:1-10`). |
| **Non-trigger** | General code review, unrelated bugs, new-feature implementation, or broad UI redesign; these should be declined or routed elsewhere (`skills/review-animations/SKILL.md:8-10`). |
| **Responsibility** | Review every animation in the diff for purpose, frequency, easing, duration, physical origin, interruptibility, performance, accessibility, asymmetric timing, and cohesion; emit a findings table and explicit block/approve verdict (`skills/review-animations/SKILL.md:12-53`, `:76-118`). |
| **Non-responsibility** | It does not implement fixes or review non-motion code (`skills/review-animations/SKILL.md:8-10`). |
| **Inputs** | Animation/motion code diff, component interaction context, usage frequency, trigger, platform/personality, and precise standards reference (`skills/review-animations/SKILL.md:12-53`). |
| **Outputs** | Required `Before | After | Why` table, tiered commentary, `file:line` citations, exact replacement values, and Block/Approve decision (`skills/review-animations/SKILL.md:76-118`). |
| **Core workflow** | Identify each animation; apply ten standards; escalate listed hard triggers; choose smallest remedy from delete through accessibility/cohesion; use standards for exact values; issue verdict (`skills/review-animations/SKILL.md:20-74`, `:76-118`). |
| **Branches** | Frequency bands; predetermined CSS/WAAPI motion versus dynamic JS/springs; modal versus trigger-anchored origin; reduced-motion alternative; deletion versus reduction versus repair (`skills/review-animations/STANDARDS.md:1-76`, `:78-157`). |
| **Rules, gates, stop conditions** | Blocks on feel-breaking regressions, high-frequency/keyboard animation, `scale(0)`, UI `ease-in`, or easily avoidable non-GPU layout animation. Approves only when purpose, duration, easing, interruptibility, and reduced motion all hold (`skills/review-animations/SKILL.md:42-53`, `:110-118`). |
| **Tools and dependencies** | Source inspection; optionally DevTools animation inspector, slow motion, frame-by-frame analysis, and real-device testing (`skills/review-animations/STANDARDS.md:145-157`). |
| **Permissions and side effects** | Review-only by contract; recommends edits but does not apply them. |
| **Strongest unique methods** | Frequency-based decision table; explicit physical-origin rules; interruptibility distinction between transitions and keyframes; asymmetric timing for deliberate action/system response; strict output and verdict contract (`skills/review-animations/STANDARDS.md:1-76`). |
| **Weaknesses and failure modes** | Some hard statements are overgeneralized: “Framer Motion shorthands are not hardware-accelerated” collapses implementation details into a universal rule; “pure-fade entrances” are escalated even though reduced-motion guidance retains opacity changes; the block policy can reject contextually acceptable long modal transitions despite a 200-500ms standards table. It reviews code, but no executable verification is required before approval (`skills/review-animations/SKILL.md:42-53`; `skills/review-animations/STANDARDS.md:31-40`, `:92-115`). |
| **Overlap / duplicate / dependency candidates** | Specialized complement to `impeccable animate` and `design-taste-frontend` motion gates. Duplicates parts of `ui-ux-pro-max` animation guidance but provides a much sharper review contract. Depends on caller-provided interaction frequency and product context. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/review-animations/STANDARDS.md` | semantic-read | Exact frequency, easing, duration, spring, physicality, interruptibility, performance, gesture, accessibility, and debugging values (`:1-157`). |
| No executable scripts present | excluded | Root is a review rubric, not an animation runtime. |

---

## 8. `ui-ux-pro-max`

### Root and skill path

- Root: `skills/ui-ux-pro-max`
- Skill: `skills/ui-ux-pro-max/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | Designing, building, reviewing, or fixing web/mobile/desktop interfaces, design systems, visual decisions, interaction, accessibility, responsive layout, charts, and stack-specific implementation (`skills/ui-ux-pro-max/SKILL.md:1-16`). |
| **Non-trigger** | Pure backend, API/database, infrastructure/DevOps, and non-visual scripts unless they change appearance or interaction (`skills/ui-ux-pro-max/SKILL.md:10-16`). |
| **Responsibility** | Query a curated local knowledge base by product/style/color/type/chart/UX/icon/motion/react/web or stack; generate and optionally persist a design system; apply reasoning profiles and dials; validate returned match before use; run a pre-delivery checklist (`skills/ui-ux-pro-max/SKILL.md:18-49`, `:54-190`). |
| **Non-responsibility** | It does not install packages, modify the OS, or authorize unrelated changes. Search output is recommendation, not authority (`skills/ui-ux-pro-max/SKILL.md:89-96`). |
| **Inputs** | Product type, industry, audience/context, style keywords, detected stack, focused concern, one dominant search intent, optional dials, project name/output directory/page (`skills/ui-ux-pro-max/SKILL.md:98-159`). |
| **Outputs** | Ranked search matches; design-system ASCII/Markdown/JSON; optional `design-system/<slug>/MASTER.md` and page overrides; optional GSAP snippet; stack guidance; explicit no-match fallback (`skills/ui-ux-pro-max/SKILL.md:113-190`, `:215-226`). |
| **Core workflow** | Analyze request and detect stack; choose smallest query mode; run design-system generation for new/system-wide work or one domain/stack search for focused work; verify result domain/top identity/fit; retry once if empty/off-topic; persist only with correct root and overwrite authorization; supplement only as needed; run delivery checks (`skills/ui-ux-pro-max/SKILL.md:54-96`, `:98-226`). |
| **Branches** | Design-system versus domain versus stack; web versus native/mobile checklist; explicit domain versus auto-detection; successful match versus one retry and fallback; persistence skip versus explicit `--force`; low/mid/high variance, motion, and density tiers (`skills/ui-ux-pro-max/SKILL.md:54-96`, `:113-159`). |
| **Rules, gates, stop conditions** | Accessibility is first priority; never assume stack; one dominant query with 2-5 terms; verify result; retry only once; no fabricated search output; do not persist unverified output; read existing Master before overwrite; never use `--force` without authorization (`skills/ui-ux-pro-max/SKILL.md:18-49`, `:54-96`, `:113-138`, `:192-213`). |
| **Tools and dependencies** | Python 3 standard library; local CSV/JSON data; BM25 implementation; optional filesystem persistence. No external Python dependency (`skills/ui-ux-pro-max/SKILL.md:51-52`; `skills/ui-ux-pro-max/scripts/core.py:1-15`). |
| **Permissions and side effects** | Searches are read-only. `--persist` writes Master/page files under the explicitly passed project root. `--force` can overwrite and is user-gated. The skill does not install packages or alter OS state (`skills/ui-ux-pro-max/SKILL.md:89-96`, `:113-138`). |
| **Strongest unique methods** | Local searchable corpus with abstention thresholds, domain routing, current-stack applicability, curated provenance, contrast/data validators, exact design-system reasoning rules, and three tunable dials. Persistence uses atomic writes and no-overwrite defaults (`skills/ui-ux-pro-max/scripts/core.py:1-118`, `:193-348`; `skills/ui-ux-pro-max/scripts/design_system.py:1-92`, `:408-609`, `:956-1109`). |
| **Weaknesses and failure modes** | Dataset breadth can create false authority: many reasoning profiles are derived rather than product-validated. Generated Master defaults inject generic shadows, cards, white modal surfaces, `transition: all`, and Lucide suggestions that conflict with sibling anti-slop/motion rules (`skills/ui-ux-pro-max/scripts/design_system.py:1110-1307`). Some old data rows prescribe categorical aesthetics or conformance claims, e.g. healthcare `wcag-aaa-compliance`, even though validation focuses structure more than truth of every recommendation (`skills/ui-ux-pro-max/data/ui-reasoning.csv:1-14`). Search correctness depends on corpus freshness and threshold calibration. |
| **Overlap / duplicate / dependency candidates** | The dial model overlaps `design-taste-frontend`. Design-system generation overlaps Impeccable new-work/document but is retrieval/reasoning-driven rather than project-evidence-driven. UX guidance overlaps `web-accessibility`, but the latter should control standards interpretation and evidence. Motion results overlap `review-animations`, but are implementation snippets rather than review verdicts. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/ui-ux-pro-max/references/quick-reference.md` | semantic-read | Static index of all ten guideline categories and 119 UX rules, including WCAG 2.2 outcomes, animation, forms, navigation, and charts (`:1-253`). |
| `skills/ui-ux-pro-max/references/pro-rules.md` | semantic-read | Native/mobile-specific professional UI guidance and canonical pre-delivery checklist (`:1-139`). |
| `skills/ui-ux-pro-max/scripts/search.py` | behavior-reviewed | CLI parsing, query modes, persistence flags, dial validation, output formatting, and dispatch (`:1-160`). |
| `skills/ui-ux-pro-max/scripts/core.py` | behavior-reviewed | BM25 index, domain/stack configuration, query rewriting, abstention, suggestions, stack/version filtering, and search result contracts (`:1-118`, `:193-348`, `:349-760`). |
| `skills/ui-ux-pro-max/scripts/design_system.py` | behavior-reviewed | Reasoning aggregation, mode/palette selection, dial application, output formatting, atomic persistence, and generated Master/page content (`:1-92`, `:408-609`, `:956-1307`). |
| `skills/ui-ux-pro-max/scripts/reasoning_contract.py` | behavior-reviewed | Closed JSON grammar for conditions/actions; validates and deterministically applies rules without executing data (`:1-105`). |
| `skills/ui-ux-pro-max/scripts/validate_data.py` | behavior-reviewed | Stdlib validation of schema, contrast, provenance, current stack applicability, claims, catalogs, and reasoning references (`:1-75`, `:1046-1096`). |
| `skills/ui-ux-pro-max/data/{styles,products,colors,landing,typography,charts,icons,motion,react-performance,app-interface,ux-guidelines,google-fonts}.csv` | semantic-read | Searchable semantic corpora. Schema and representative rows were inspected through `core.py`, quick reference, direct CSV samples, and validator contracts. |
| `skills/ui-ux-pro-max/data/stacks/*.csv` | semantic-read | Twenty-two stack-specific guidance corpora; bounded as one homogeneous schema family and validated through `_STACK_COLS`, applicability/status fields, and freshness rules (`core.py:80-174`; `validate_data.py:1046-1096`). |
| `skills/ui-ux-pro-max/data/ui-reasoning.csv` | semantic-read | Product-to-pattern/style/color/type/effect decision profiles and conditional actions; representative rows expose both value and opinionated risks (`:1-148`). |
| `skills/ui-ux-pro-max/data/{catalog-summary,data-provenance}.json` | semantic-read | Counts, snapshot hashes, promotion policy, source type, confidence, freshness, applicability, and official/derived evidence boundaries (`catalog-summary.json:1-72`; `data-provenance.json:1-1000`, `:1001-1349`). |
| `skills/ui-ux-pro-max/data/{google-font-licenses,phosphor-icons-upstream}.json` | semantic-read | Catalog/license and upstream icon snapshot inputs, validated as data rather than runtime behavior. |
| `skills/ui-ux-pro-max/scripts/tests/**` | excluded | Generated/test fixtures and test implementation; useful for maintainers but not reusable end-user semantic methods. |

---

## 9. `web-accessibility`

### Root and skill path

- Root: `skills/web-accessibility`
- Skill: `skills/web-accessibility/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | A11y, WCAG, ARIA, screen-reader, keyboard, focus, dialogs, forms, widgets, accessible authentication, target size, drag alternatives, reflow, contrast, motion, or accessibility review/evidence work (`skills/web-accessibility/SKILL.md:1-15`; `skills/web-accessibility/README.md:24-35`). |
| **Non-trigger** | Unrelated requests, CMS/theme architecture, general product scope, generic user-facing behavior outside accessibility, or framework API details before semantic requirements are defined (`skills/web-accessibility/SKILL.md:55-68`). |
| **Responsibility** | Define observable accessibility requirements; prefer native semantics; specify complete interaction/focus/recovery contracts; implement only after contract; verify in supported browser/AT combinations; bound all claims to evidence (`skills/web-accessibility/SKILL.md:13-26`, `:28-53`). |
| **Non-responsibility** | It does not issue automated WCAG conformance verdicts, substitute APG examples for production proof, or own product scope/framework APIs (`skills/web-accessibility/SKILL.md:13-26`, `:55-68`). |
| **Inputs** | User task and failure recovery; affected users; supported browsers/AT/input methods; target environment; interface source/live state; chosen widget pattern; applicable WCAG criteria (`skills/web-accessibility/SKILL.md:13-26`). |
| **Outputs** | Acceptance criteria; semantic/interaction contract; design and implementation review checklists; release evidence matrix; pass/fail/blocked/not-applicable result per criterion; residual risk and evidence boundary (`skills/web-accessibility/SKILL.md:13-26`, `:50-53`; `skills/web-accessibility/assets/acceptance-criteria-template.md:1-21`). |
| **Core workflow** | Define task/support environment; choose native HTML; specify every interactive state; design visual/input adaptation; evaluate maintained native/library alternatives before custom widgets; implement; run hybrid automated/manual/AT verification; stop only when every criterion has evidence or a recorded disposition (`skills/web-accessibility/SKILL.md:13-26`, `:50-53`). |
| **Branches** | Native element versus maintained component versus custom composite; modal `<dialog>` versus custom dialog; ordinary disclosure navigation versus application menu; automation versus manual/accessibility-tree/screen-reader evidence; criterion pass/fail/blocked/not-applicable (`skills/web-accessibility/SKILL.md:28-48`; `skills/web-accessibility/references/composite-widgets.md:1-27`). |
| **Rules, gates, stop conditions** | HTML first; ARIA only when native semantics are insufficient; ARIA does not create keyboard behavior; inspect computed accessible name; modal background inert/unavailable; web target-size criterion is 24×24 CSS px subject to exceptions; no conformance claim from scans; stop when each acceptance criterion is evidenced or explicitly unresolved (`skills/web-accessibility/SKILL.md:28-53`). |
| **Tools and dependencies** | No runtime dependency. Uses browser accessibility tree, keyboard protocols, selected browser/AT combinations, optional automated rules, standards and APG references (`skills/web-accessibility/SKILL.md:1-10`; `skills/web-accessibility/references/testing-and-evidence.md:1-55`). |
| **Permissions and side effects** | Framework-neutral planning/review by default; implementation may change UI only after the interaction contract exists. Release evidence records actual environment and failures. No network/package permission is implied. |
| **Strongest unique methods** | Separates normative standards, platform specs, APG patterns, and tutorials; treats accessibility as task completion/recovery; requires explicit focus entry/exit/return; makes evidence boundaries first-class; distinguishes WCAG minimums from larger product goals (`skills/web-accessibility/SKILL.md:28-53`; `skills/web-accessibility/references/source-index.md:1-32`). |
| **Weaknesses and failure modes** | Requires real supported browser/AT access for meaningful verification, which may be unavailable. It intentionally does not provide framework implementation APIs. The source-index retrieval dates are future-dated relative to many environments and should be refreshed before external standards claims (`skills/web-accessibility/references/source-index.md:1-17`). |
| **Overlap / duplicate / dependency candidates** | Canonical dependency for accessibility portions of all other nine roots. Overlaps `ui-ux-pro-max` quick-reference rules and Impeccable audit, but uniquely owns standards interpretation, complete interaction contracts, and evidence boundaries. Complements `web-design-guidelines`, whose fetched checklist cannot independently support conformance. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/web-accessibility/references/source-index.md` | semantic-read | Standards status/version, canonical URLs, and WCAG 2.2 change list (`:1-32`). |
| `skills/web-accessibility/references/semantics-and-names.md` | semantic-read | Native structure, accessible names/descriptions, tables/images, and dynamic updates (`:1-27`). |
| `skills/web-accessibility/references/keyboard-focus-and-routing.md` | semantic-read | Focus entry/operation/exit/recovery, route changes, and keyboard protocol (`:1-24`). |
| `skills/web-accessibility/references/forms-errors-authentication.md` | semantic-read | Form semantics, error recovery, redundant entry, and accessible authentication (`:1-31`). |
| `skills/web-accessibility/references/dialogs-disclosures-navigation.md` | semantic-read | Modal/disclosure/navigation behavior and prohibited ARIA misuse (`:1-24`). |
| `skills/web-accessibility/references/composite-widgets.md` | semantic-read | Native/library/custom decision path and full contracts for tabs, comboboxes, listboxes, menus, grids, and trees (`:1-30`). |
| `skills/web-accessibility/references/visual-input-and-motion.md` | semantic-read | Contrast, reflow, text spacing, target exceptions, drag alternatives, motion, media, and update controls (`:1-29`). |
| `skills/web-accessibility/references/testing-and-evidence.md` | semantic-read | Hybrid test protocol, evidence set, and release rule (`:1-55`). |
| `skills/web-accessibility/references/{routing,outcome-probes}.md` | semantic-read | Specialist boundaries and concrete review probes for dialogs, forms, navigation, comboboxes, and verdicts. |
| `skills/web-accessibility/assets/*.md` | semantic-read | Reusable acceptance, design-review, implementation-review, and release-evidence templates (`acceptance-criteria-template.md:1-21`; `review-checklist-implementation.md:1-10`; `review-checklist-release.md:1-25`). |
| `skills/web-accessibility/README.md` | semantic-read | Public overview, triggers, requirements, and package map (`:1-40`). |
| `skills/web-accessibility/evals/evals.json` | excluded | Evaluation/test fixture; assertions validate packaging behavior but do not add authoritative accessibility guidance. |
| No scripts present | excluded | Root is framework-neutral and has no behavior-bearing runtime. |

---

## 10. `web-design-guidelines`

### Root and skill path

- Root: `skills/web-design-guidelines`
- Skill: `skills/web-design-guidelines/SKILL.md`

### Dossier

| Field | Audit |
|---|---|
| **Trigger** | User asks to review UI, accessibility, design, UX, or site best practices against Vercel’s Web Interface Guidelines (`skills/web-design-guidelines/SKILL.md:1-12`). |
| **Non-trigger** | UI implementation, remediation, design generation, offline audit where the current remote guidelines cannot be fetched, or WCAG conformance claims. |
| **Responsibility** | Fetch the latest upstream command, read the user-specified files, apply all fetched rules, and report terse `file:line` findings (`skills/web-design-guidelines/SKILL.md:9-30`). |
| **Non-responsibility** | It does not define the guideline content locally, implement fixes, maintain an evidence matrix, or independently assess standards authority. |
| **Inputs** | Target file or pattern and current contents of one remote Markdown guideline document (`skills/web-design-guidelines/SKILL.md:9-30`). |
| **Outputs** | Findings using the format specified by the fetched upstream guideline (`skills/web-design-guidelines/SKILL.md:23-30`). |
| **Core workflow** | Fetch upstream guidelines; read specified files; apply all rules; output terse findings. If target absent, ask for files (`skills/web-design-guidelines/SKILL.md:9-30`). |
| **Branches** | File/pattern supplied versus absent. Successful network fetch versus unavailable upstream; the latter has no documented fallback. |
| **Rules, gates, stop conditions** | A fresh fetch is mandatory before every review. All fetched rules must be applied. Findings must use upstream formatting. Missing target blocks review until supplied (`skills/web-design-guidelines/SKILL.md:9-30`). |
| **Tools and dependencies** | Network/WebFetch and GitHub raw content at a mutable URL (`skills/web-design-guidelines/SKILL.md:15-21`). |
| **Permissions and side effects** | Read-only review, but necessarily performs network access. It does not authorize edits. |
| **Strongest unique methods** | Very small adapter that intentionally delegates rule freshness and output format to a single upstream authority. |
| **Weaknesses and failure modes** | No pinned version, hash, cached fallback, source validation, or offline mode. Behavior and semantics can change remotely between invocations. It is unusable under a no-network authority. “Check accessibility” trigger is too broad for a generic fetched guideline and must not be interpreted as WCAG conformance. The upstream file is not present locally, so its actual current rules were not auditable in this read-only/no-network pass. |
| **Overlap / duplicate / dependency candidates** | Lightweight duplicate of parts of Impeccable audit/critique and `ui-ux-pro-max` quick reference. Should complement, not supersede, `web-accessibility`. The remote guideline should be vendored/pinned if Capability Compiler requires durable semantic units. |

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/web-design-guidelines/SKILL.md` | semantic-read | Sole local source; defines trigger, remote dependency, workflow, and output form. |
| `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | excluded | Remote mutable source; network access was explicitly forbidden, so current contents could not be read. This does not block auditing the local root contract, but it leaves the delegated rule catalog unresolved. |
| No local support files | excluded | Root contains no vendored reference, script, asset, template, or example. |

---

# Cross-root relationship hypotheses

## A. Likely duplicates

### 1. Anti-template visual direction

- `design-taste-frontend`
- `frontend-design`
- Impeccable `new-work` plus `craft-floor`
- parts of `redesign-existing-projects`

All derive visual direction from context and reject recurring AI defaults. The distinction should be explicit:

- `frontend-design`: compact principle-and-plan layer.
- `design-taste-frontend`: prescriptive marketing/portfolio implementation rules and pre-flight.
- `impeccable`: stateful end-to-end lifecycle and artifact system.
- `redesign-existing-projects`: lightweight incumbent audit/fix path.

Without a routing decision, the same request can trigger four contradictory sets of aesthetic rules.

### 2. UI audit and review

- Impeccable `critique` / `audit`
- `web-design-guidelines`
- `ui-ux-pro-max` quick reference
- `web-accessibility`
- `review-animations` for motion subset

These are not exact duplicates, but current triggers overlap heavily. Suggested split:

- visual/heuristic critique: Impeccable critique;
- static technical implementation audit: Impeccable audit;
- standards-quality accessibility: `web-accessibility`;
- narrow motion-code review: `review-animations`;
- generic fresh Vercel checklist: `web-design-guidelines`;
- local retrieval/advice: `ui-ux-pro-max`.

### 3. Design-system extraction

- `extract-design-system`: external public website to starter tokens.
- Impeccable `extract`: repeated local components/tokens into a local system.
- Impeccable `document`: record current local visual system as `DESIGN.md`.
- `ui-ux-pro-max --design-system`: synthesize a recommended system from curated data.

They should remain separate conditional variants rather than be merged under one undifferentiated “extract design system” unit.

### 4. Variant prototyping

- `prototype`
- Impeccable live mode
- Impeccable new-work direction/structure rounds

`prototype` is the smallest coherent unit for one component. Impeccable live works on selected incumbent elements with persisted runtime state. New-work rounds choose surface/world direction. These are complements if routed by scope.

---

## B. Strong complements and dependencies

| Producer | Consumer / dependency hypothesis |
|---|---|
| `extract-design-system` | Feeds normalized evidence to `frontend-design`, `design-taste-frontend`, `redesign-existing-projects`, or Impeccable document/new-work; extracted data remains non-authoritative until reviewed. |
| `web-accessibility` | Required depth layer for all implementation, audit, prototype, animation, and redesign roots when accessibility is in scope. |
| `review-animations` | Final narrow review after `impeccable animate`, `design-taste-frontend`, or motion-heavy prototypes. |
| `prototype` | Exploration branch before production integration by another build skill. |
| `ui-ux-pro-max` | Local recommendation/search provider; caller must validate match and defer standards claims to `web-accessibility`. |
| Impeccable | Lifecycle/orchestration superset; should call narrower capabilities without importing their contradictory default aesthetics wholesale. |
| `web-design-guidelines` | Optional fresh checklist after local code is available; must not be the only accessibility evidence source. |

---

## C. Opinionated visual conflicts requiring explicit arbitration

### 1. Eyebrows and labels

- `design-taste-frontend` allows a mechanically rationed maximum of one eyebrow per three sections (`skills/design-taste-frontend/SKILL.md:337-350`).
- `frontend-design` says unnecessary labels and all-caps labels are generic tells but permits structural labels when informative (`skills/frontend-design/SKILL.md:31-42`).
- Impeccable craft floor imposes an absolute eyebrow ban, saying no brief earns it back (`skills/impeccable/reference/craft-floor.md:23-31`).

**Hypothesis:** retain three branches: informative structural label allowed; decorative eyebrow rejected; Impeccable’s absolute ban applies only inside Impeccable builds unless promoted as a global compiler rule by explicit decision.

### 2. Typography emphasis

- `frontend-design` rejects accenting a single word by italic/bold/color as a generated-page tell (`skills/frontend-design/SKILL.md:25-31`).
- `design-taste-frontend` specifically recommends italic or bold of the same family rather than injecting a second family (`skills/design-taste-frontend/SKILL.md:206-229`).

**Hypothesis:** conditional variant. Same-family emphasis is allowed only when it carries real semantic or compositional purpose; arbitrary single-word emphasis remains rejected.

### 3. Radius systems

- `design-taste-frontend` demands one consistent documented radius system (`skills/design-taste-frontend/SKILL.md:262-273`).
- `redesign-existing-projects` says uniform radius is generic and recommends varying inner/outer radii (`skills/redesign-existing-projects/SKILL.md:68-88`).

**Resolution candidate:** these need not conflict if “one system” permits role-based radii. Merge as: establish a small semantic radius scale; do not use one radius everywhere and do not vary without a rule.

### 4. Pure black

- `design-taste-frontend` and `redesign-existing-projects` ban pure black by default (`skills/design-taste-frontend/SKILL.md:601-607`; `skills/redesign-existing-projects/SKILL.md:31-51`).
- `frontend-design` identifies tinted near-black as another repeated AI tell (`skills/frontend-design/SKILL.md:44-52`).

**Resolution candidate:** no universal color ban. Let the selected physical scene and brand decide. Reject unexamined default black or tinted-black, not either literal value categorically.

### 5. Motion quantity

- `design-taste-frontend` requires visible motion when its motion dial exceeds 4 and offers hero entry, section reveal, and CTA physics as a minimum (`skills/design-taste-frontend/SKILL.md:521-545`).
- `frontend-design`, Impeccable craft floor, and `ui-ux-pro-max` favor one orchestrated moment or 1-2 animated elements (`skills/frontend-design/SKILL.md:38-42`; `skills/impeccable/reference/craft-floor.md:8-20`; `skills/ui-ux-pro-max/references/quick-reference.md:124-154`).
- `review-animations` rejects high-frequency or purposeless motion (`skills/review-animations/SKILL.md:20-53`).

**Resolution candidate:** the dial may increase technical ambition, not animation count. One focal sequence plus functional state transitions satisfies high motion without repeated reveals.

### 6. Animation property policy

- `review-animations` and `design-taste-frontend` largely prescribe transform/opacity only.
- Impeccable animate permits bounded blur, filter, clip-path, masks, shadow, color, and shaders when they carry meaning (`skills/impeccable/reference/animate.md:25-75`).
- The prototype picker intentionally animates width as a documented tiny isolated exception (`skills/prototype/PICKER.md:70-89`).

**Resolution candidate:** replace categorical “GPU-only” with a performance gate: transform/opacity are the baseline; other properties require bounded paint area, measured smoothness, and semantic value.

### 7. Imagery requirements

- `design-taste-frontend` requires real/generated imagery even for minimalist sites (`skills/design-taste-frontend/SKILL.md:464-493`).
- `frontend-design` allows the characteristic hero element to be headline, animation, live demo, interaction, or image (`skills/frontend-design/SKILL.md:14-24`).
- Impeccable requires assets when the committed world/comp calls for them, not categorically on every page (`skills/impeccable/reference/new-work.md:151-190`).

**Resolution candidate:** imagery is required when the subject or approved composition is image-native; otherwise a product-specific live demo, typography, data, or interaction may be the primary material.

### 8. Dark mode

- `design-taste-frontend` mandates both modes for consumer-facing pages while also imposing a page theme lock (`skills/design-taste-frontend/SKILL.md:571-595`).
- Other roots treat dark mode as context/product driven.
- Impeccable explicitly says light/dark should be selected from the physical usage scene rather than category (`skills/impeccable/reference/craft-floor.md:42-47`).

**Resolution candidate:** support multiple schemes only when product requirements justify them; within any active render, maintain coherent page-level theme. No universal dual-mode mandate.

### 9. Fabricated sample numbers

- `redesign-existing-projects` recommends messy numbers to avoid generic round values (`skills/redesign-existing-projects/SKILL.md:112-134`).
- `design-taste-frontend` bans invented precision unless real or explicitly labeled mock/sample (`skills/design-taste-frontend/SKILL.md:400-449`).

**Resolution candidate:** retain the latter. Realistic sample data must be explicitly synthetic; visual realism does not authorize unlabeled claims.

### 10. Smooth scrolling

- `redesign-existing-projects` recommends `scroll-behavior: smooth` as a general repair (`skills/redesign-existing-projects/SKILL.md:90-111`).
- `web-accessibility` requires motion controls/preferences according to applicability rather than universal smooth motion (`skills/web-accessibility/references/visual-input-and-motion.md:17-29`).

**Resolution candidate:** smooth scrolling only under `prefers-reduced-motion: no-preference`, with native instant behavior under reduced motion.

### 11. Accessibility target sizes

- `web-accessibility` correctly distinguishes WCAG 2.2 web minimum 24×24 CSS px with exceptions (`skills/web-accessibility/SKILL.md:45-48`).
- `ui-ux-pro-max` distinguishes web 24 CSS px from native 44pt/48dp in the full reference, while higher-level tables use 44×44 as a broader product goal (`skills/ui-ux-pro-max/references/quick-reference.md:22-48`).

**Resolution candidate:** preserve standards minimum and product goal as separate fields. Never present native target guidance as the web conformance threshold.

---

## D. UX/UI lifecycle gaps across the assigned set

1. **Research and outcome definition are thin outside Impeccable and web-accessibility.** Most visual roots begin from a brief but do not validate user problems, success metrics, or evidence.
2. **Content and asset provenance are inconsistent.** Impeccable has a strong asset provenance model; other roots freely invent draft copy, names, or visuals without a durable provenance record.
3. **State coverage varies.** `design-taste-frontend`, `redesign-existing-projects`, Impeccable polish, and web-accessibility address loading/empty/error/success, but `frontend-design` and `prototype` lack a systematic state matrix.
4. **Production handoff is uneven.** `prototype` has promotion/cleanup, Impeccable has finish review/documentation, while lightweight design roots can stop after implementation without evidence or system documentation.
5. **Accessibility verification is frequently reduced to visual checks.** `web-accessibility` alone requires browser/AT evidence and prohibits scan-based conformance conclusions.
6. **Internationalization and long-content stress are not consistently present.** Impeccable and web-accessibility cover them; marketing-focused roots mostly do not.
7. **Analytics, SEO, and route preservation are explicit only in `design-taste-frontend` redesign mode.**
8. **Rollback and data-loss safety are weak in most visual mutation roots.** Impeccable supplies bounded review and stateful cleanup; simpler roots rely on “test after change.”
9. **Remote/corpus freshness has two opposite risks.** `web-design-guidelines` is always fresh but non-durable and network-bound; `ui-ux-pro-max` is durable/offline but can become stale.
10. **No common conflict-resolution hierarchy exists.** “Brief wins,” incumbent design system, platform conventions, accessibility requirements, performance, and opinionated anti-slop rules need a shared precedence order.

A plausible shared precedence is:

1. User authority and factual product truth.
2. Safety, accessibility, legal, and platform requirements.
3. Existing approved brand/design-system invariants.
4. Task and visitor-mode usability.
5. Performance and maintainability.
6. Contextual craft guidance.
7. Anti-default preferences and aesthetic bans.

---

# Unresolved questions

1. Should Capability Compiler retain Impeccable as a monolithic lifecycle skill, or decompose its command playbooks into canonical units while keeping Impeccable only as a recipe/orchestrator?
2. Which root owns the canonical visual anti-slop rules: `design-taste-frontend`, `frontend-design`, or Impeccable craft floor? Their absolute bans cannot all be globally authoritative.
3. Is `web-design-guidelines` acceptable as a network-only, mutable-source skill, or must the upstream guideline be vendored with a version/hash for durable compilation?
4. Should `extract-design-system` pin the external package version and define URL/protocol/host safety before it is considered production-ready?
5. Is `ui-ux-pro-max` data intended as recommendation evidence or a design authority? The answer changes whether generated Masters may inject generic component code.
6. Should `ui-ux-pro-max` generated Master templates be corrected before reuse? Current generated CSS includes `transition: all`, generic card shadows, fixed white modal surfaces, and generic component defaults that conflict with several sibling skills.
7. Should the empty `impeccable/reference/harden.md` be considered an incomplete command contract and excluded/deferred until restored?
8. For motion, should the compiler preserve `review-animations`’ categorical GPU rules or adopt Impeccable animate’s measured bounded-effects model?
9. Should all accessibility-related audit units be made strong dependencies on `web-accessibility`, with explicit prohibition on inferring WCAG conformance from Impeccable scores, Vercel guidelines, or UI Pro Max searches?
10. Should sample/demo content have a shared provenance rule requiring explicit “synthetic/mock” labeling whenever names, metrics, testimonials, prices, or technical measurements are invented?
11. For redesign work, which preservation baseline is mandatory across roots: routes, IA, copy, analytics events, SEO metadata, form semantics, legal text, and existing accessibility behavior?
12. Should prototype variants be required to cover state and accessibility acceptance criteria, or remain intentionally optimized for visual divergence before production hardening?
13. How should conflicting theme rules be compiled: consumer dual-mode by default, context-selected single mode, or product requirement-driven scheme support?
14. Should absolute eyebrow, serif, pure-black, icon-family, and imagery bans survive as root-local variants rather than canonical global rules?
15. The current audit verified semantic classification but did not execute scripts or tests because authority was read-only. Maintainers should run the repository’s relevant local tests for Impeccable and UI Pro Max before using behavior-bearing code as validated implementation evidence.