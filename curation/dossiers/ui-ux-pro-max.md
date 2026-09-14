# ui-ux-pro-max Dossier

## Problem
Modern multi-platform application development (web, mobile, and desktop) suffers from fragmented design intelligence, inconsistent design token definitions, and a gap between high-level aesthetic guidelines and stack-specific front-end code implementation. Teams frequently encounter recurring UI/UX anti-patterns: low-contrast dark mode pairs, missing accessibility focus rings, unannounced screen-reader state changes, clumsy touch targets under 44pt, layout shifts caused by unreserved dimensions, and jarring animation state snaps. `ui-ux-pro-max` provides a systematic, searchable intelligence layer spanning 10 prioritized rule categories, 192 reasoning profiles, 74 font pairings, 119 UX guidelines, and 22 technology stack adapters to guide design systems from concept to implementation and pre-delivery verification.

## When to Use
- Designing new web, mobile, or desktop pages requiring a cohesive product-level design system (colors, typography, spacing, elevations, motion).
- Creating, styling, or refactoring UI components to adhere to platform accessibility (WCAG 2.2 AA) and ergonomic touch standards.
- Determining semantic design tokens (variance, motion, density scales) and persisting master design contracts with page-specific overrides.
- Conducting cross-platform design audits and UX reviews across 10 structured priority categories (Accessibility, Touch, Performance, Style, Layout, Typography/Color, Animation, Forms, Navigation, Charts).
- Running pre-delivery quality checks for mobile/native interfaces (iOS, Android, React Native, Flutter) against canonical checklists.

## When Not to Use
- Pure backend engineering tasks (database schema modeling, server-side business logic, message queue processing, microservice orchestrations).
- Non-visual scripts, terminal utility tools, and command-line data processing without user interfaces.
- DevOps, infrastructure-as-code, and cloud deployment pipelines (Kubernetes, Terraform, CI/CD runners).
- Server-side performance optimization that does not affect rendering, animations, perceived latency, or user interaction feedback.

## Role
Cross-Platform UI/UX Design System Architect and Quality Governance Specialist. Connects product intent, human ergonomic constraints, and platform idioms with production-grade UI implementations across 22 frontend frameworks.

## Inputs
- **Product Classification**: Product category (SaaS, e-commerce, portfolio, dashboard, entertainment, internal tool, consumer mobile).
- **Target Audience & Scene**: Demographic cohort, primary usage context (mobile commute, high-focus workstation, ambient lighting conditions).
- **Style Archetypes**: Visual tone keywords (playful, vibrant, minimal, dark mode, content-first, dense technical, luxury).
- **Target Technology Stack**: Detected or specified frontend platform out of 22 supported stacks (React, Next.js, Vue, Svelte, Nuxt, Angular, Laravel, Tailwind CSS, shadcn/ui, SwiftUI, Flutter, Jetpack Compose, React Native, WPF, WinUI, Avalonia, Uno, Three.js, etc.).
- **Design Sliders (Optional 1-10 Dials)**: Variance (aesthetic conservatism vs. asymmetric boldness), Motion (subtle micro-interactions vs. complex choreography), and Density (spacious luxury vs. compact dashboard).
- **Existing Design State**: Presence of `design-system/<project-slug>/MASTER.md` and page-level override manifests.

## Outputs
- **Product Design System Contract**: Structured token definitions for colors, type scales, font pairings, spacing ramps, elevation/shadow levels, component states, and explicit anti-patterns to avoid.
- **Master & Overrides Documentation**: Persisted `MASTER.md` and page-level override specifications (`pages/<page-name>.md`) under `design-system/<project-slug>/`.
- **Targeted UX Recommendations**: Ranked guidance for specific interactive outcomes across the 10 core categories (e.g., WCAG 2.2 focus management, inline validation, interruptible spring curves).
- **Stack-Specific Implementation Guides**: Framework-idiomatic code patterns, component library mappings, and performance safeguards.
- **Pre-Delivery Verification Report**: Checklist audit across Visual Quality, Interaction, Light/Dark Parity, Layout Safe Areas, and Accessibility compliance.

## Workflow
1. **Analyze Requirements & Environment Context**:
   - Extract product type, audience context, and style keywords from the user prompt.
   - Automatically detect the target platform/stack by inspecting repository indicators (`package.json`, `pubspec.yaml`, `*.xcodeproj`, `composer.json`, `app.json`). Never assume a hardcoded stack default.
2. **Generate Master Design System**:
   - Synthesize design intelligence across product models, color palettes, landing structures, typography, and `ui-reasoning` rules.
   - Adjust optional Design Dials (`variance`, `motion`, `density` on 1-10 scales) to tune spacing scales (`--space-*`) and animation presets without altering queries.
3. **Persist Design System (Master + Overrides Pattern)**:
   - When requested, persist `MASTER.md` to `design-system/<project-slug>/` using project-root relative paths.
   - Check if an existing `MASTER.md` already exists; leave it untouched to protect prior human or team decisions unless explicit user authorization overrides it.
   - Isolate route-specific divergences in `pages/<page-name>.md` to override master rules without corrupting global invariants.
4. **Execute Targeted Domain Queries**:
   - For localized component design or bug remediation, formulate single-intent queries using 2–5 meaningful terms plus domain constraints (`--domain ux`, `color`, `typography`, `icons`, `gsap`, `chart`, `react`, `web`).
   - Prioritize semantic UX outcomes before framework implementation terms (e.g., query `"error summary validation" --domain ux` before searching stack-specific inputs).
5. **Apply Stack-Specific Implementation Guidelines**:
   - Query stack guidance (`--stack <stack>`) to map design tokens into native idioms (Tailwind utility classes, SwiftUI modifiers, Flutter widgets, Compose modifiers).
6. **Execute Pre-Delivery Quality Audit**:
   - Audit the built interface against the canonical Pre-Delivery Checklist in `pro-rules.md`, covering icon vector discipline, 80-150ms press feedback, 4.5:1 light/dark contrast, safe-area clearance, and keyboard/screen-reader navigation.

## Branches
- **New Project / Full Page Inception**: Follows Step 1 → Step 2 → Step 3 → Step 5. Produces global design system tokens, establishes Master/Page hierarchy, and validates core page architecture.
- **Component Refactoring / Bug Remediation**: Bypasses full design system generation; directly executes single-domain queries (Step 4) constrained by the existing `MASTER.md` and audits implementation via Step 5.
- **Mobile / Native App Final Signoff**: Enforces strict adherence to `references/pro-rules.md` (touch hit areas, Dynamic Type, hardware notches, bottom CTA clearance, haptics, and system gestures).
- **Zero-Result Search Recovery**: When a query yields no results, execute a single narrower retry. If still empty, fall back transparently to the canonical 10-category priority rules; explicitly declare to the user that default fallback rules are applied, and never fabricate synthetic database matches.

## Rules
- **No Emoji as Structural Icons**: Navigation, system actions, and control glyphs must use SVG or platform vector icons (Lucide, Material Symbols, SF Symbols). Emojis are platform-dependent, fail token scaling, and are strictly prohibited as functional icons.
- **Touch Target Dimensions**: Interactive elements must guarantee a minimum tap area of 44×44pt on iOS and 48×48dp on Android. Small visual icons must expand their invisible touch padding; touch spacing between targets must be ≥8px.
- **Contrast Ratios & Dark Mode Parity**: Body text must achieve ≥4.5:1 contrast against adjacent surfaces in both light and dark modes (large text and control borders ≥3:1). Dark mode colors must be tuned with desaturated tonal steps rather than simple color inversion; both modes must be verified independently.
- **Color Independence**: Color must never serve as the sole conveyor of status, error, or selection; functional color must always be accompanied by text labels, shape changes, or distinct iconography.
- **Responsive Layout & Viewport Safety**: Mobile viewports must use `width=device-width, initial-scale=1` and never disable pinch-to-zoom. Mobile horizontal scroll is prohibited. Primary UI must respect OS safe areas (notches, dynamic islands, home gesture bars).
- **Animation Purpose & Performance**: Every transition must communicate cause-effect or spatial continuity. Animate exclusively through `transform` and `opacity` (never animate width, height, or positional offsets). Exit animations should run ~60–70% faster than entrance animations. All animations must respect `prefers-reduced-motion` and remain interruptible.
- **Master Immutability Protection**: Existing `design-system/<project-slug>/MASTER.md` files must not be silently overwritten or modified without explicit user authorization.

## Exceptions
- **Dynamic Type Text Expansion**: When system text scale increases, single-line text constraints must yield to wrapping; if truncation is strictly unavoidable, full text must be exposed via accessible tooltips or expandable disclosures.
- **Rapid Micro-Interaction Interruption**: High-frequency user interactions must cancel in-flight animations immediately and set destination states deterministically without relying on `animationend` or `transitionend` events.
- **Low-Bandwidth / Degraded Network Mode**: Heavy video backgrounds, complex animations, and high-resolution imagery must gracefully degrade to lightweight static assets and reduced-motion states.

## Dependencies
- Compatible with and provides design-system foundation for `impeccable` (visual direction), `web-accessibility` (WCAG compliance audits), `design-qa` (conformance testing), and `frontend-design` (scaffolding).

## Permissions and Side Effects
- **Read Operations**: Reads project files (`package.json`, source code, existing markdown design documents) and internal CSV datasets.
- **Write Operations**: Writes or updates `design-system/<project-slug>/MASTER.md` and `pages/*.md` only when `--persist` is requested. Does not modify external OS files or execute unauthorized destructive commands.
- **Execution**: Purely local Python evaluation; zero external network requests and zero package manager installations.

## Gates
- **Requirement Analysis Gate**: Product category, context, and technology stack must be concretely identified before design generation begins.
- **Master Protection Gate**: Halts persistence if `MASTER.md` already exists, requiring explicit user authorization (`--force`) to overwrite.
- **Pre-Delivery Checklist Gate**: Mobile and native app deliverables must pass 100% of the canonical Pre-Delivery Checklist items (Visual Quality, Interaction, Light/Dark Parity, Layout, and Accessibility).
- **WCAG 2.2 AA Contrast & Focus Gate**: All interactive surfaces and controls must verify visible focus rings (2–4px), unobscured focus states, and minimum 4.5:1 text contrast.

## Open Questions
- Establishing automated token synchronization between `MASTER.md` and heterogeneous mobile design tokens (SwiftUI Color Assets, Flutter ThemeData, Compose MaterialTheme) across monorepo boundaries.
- Continuous synchronization of emerging component libraries across the 22 supported frontend technology stacks.

## Unique Value
Provides a unified, offline-executable, cross-platform design intelligence engine that bridges abstract UX heuristics (WCAG 2.2, Apple HIG, Material Design 3) with concrete token scales, reasoning rules, and 22 technology stack implementation patterns.

## Reading Coverage
Exhaustively covers all specification and reference documents in the skill repository:
- `skills/ui-ux-pro-max/SKILL.md` (lines 1–214): Core intelligence architecture, 10 priority categories, query contracts, step-by-step workflow, Master/Page override persistence, design dials, and fallback policies.
- `skills/ui-ux-pro-max/references/pro-rules.md` (lines 1–117): Professional UI rules for icons, app interactions, light/dark contrast, safe-area layout, and the canonical multi-domain Pre-Delivery Checklist.
- `skills/ui-ux-pro-max/references/quick-reference.md` (lines 1–256): Detailed rule sets spanning accessibility, touch, performance, style, layout, typography/color, animation, forms/feedback, navigation, and charts.
