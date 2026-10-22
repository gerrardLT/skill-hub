#!/usr/bin/env python3
"""Compile 17 semantically designed Phase 4 UX/UI candidates and one candidate Recipe."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.0-v2-candidate"
PHASE2_TREE = "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601"
PHASE3_TREE = "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965"


def D(trigger: str, triggers: list[str], anti: list[tuple[str, str]], procedure: list[str], artifacts: list[str], gate: str, neighbors: list[str], coverage: list[str], *, mutation: str = "run-output", human: bool = False, rendered: bool = False) -> dict[str, Any]:
    return {"trigger": trigger, "triggers": triggers, "anti": anti, "procedure": procedure, "artifacts": artifacts, "distinctive_gate": gate, "neighbors": neighbors, "coverage": coverage, "mutation_scope": mutation, "human_decision": human, "rendered_evidence": rendered}


DESIGNS: dict[str, dict[str, Any]] = {
    "accessibility-contracts-and-assistive-validation": D(
        "Define and validate semantic, keyboard, focus, assistive-technology, visual-input, motion, and error-recovery behavior for specified user tasks.",
        ["Turn this checkout flow into testable accessibility contracts for semantics, focus, keyboard, errors, zoom, and screen readers.", "Validate this implemented composite widget against its declared keyboard, focus, naming, and recovery behavior."],
        [("Implement the missing form controls and navigation states in the product source.", "interaction-states-forms-and-navigation"), ("Capture the live page at target viewports for an independent visual release review.", "ui-review-scope-and-evidence-acquisition")],
        ["Freeze user tasks, supported browsers and assistive technologies, interaction states, WCAG scope, and implementation evidence.", "Specify semantic structure, accessible names, relationships, keyboard model, focus entry/order/return, announcements, and error recovery per task.", "Cover contrast, zoom/reflow, pointer and touch alternatives, reduced motion, and authentication or timeout constraints where applicable.", "Evaluate only supplied current deterministic-check outputs and manual assistive records; record tool, version, viewport, evidence, and untested combinations.", "Map each criterion to passed, failed, needs-input, or blocked with residual risk; do not repair source."],
        ["accessibility acceptance contract", "assistive-technology test matrix", "criterion evidence ledger", "residual-risk report"],
        "A generic WCAG checklist cannot pass: every criterion must name a user task, state, expected observable behavior, and current evidence or explicit untested risk.",
        ["interaction-states-forms-and-navigation", "responsive-layout-and-spatial-composition", "purposeful-motion-and-animation-engineering", "ui-review-scope-and-evidence-acquisition"],
        ["semantics", "keyboard", "focus", "assistive-technology", "contrast", "zoom-reflow", "visual-input", "reduced-motion", "error-recovery"], rendered=True),
    "ai-interaction-and-probabilistic-ux": D(
        "Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.",
        ["Design the UX for an AI answer that can be delayed, uncertain, wrong, corrected, or escalated to a human.", "Specify user controls, confidence communication, provenance, undo, and recovery for this approved AI-assisted workflow."],
        [("Choose the model, retrieval stack, memory, and serving architecture.", "ai-model-and-data-architecture"), ("Perform the system threat model and autonomous-action safety assessment.", "ai-safety-and-action-governance")],
        ["Freeze the approved user job, AI role, latency budget, error cost, data boundary, autonomy level, and human escalation owner.", "Model deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable, and recovery states.", "Define provenance and uncertainty communication in task language rather than decorative confidence theater.", "Provide correction, undo, retry, compare, opt-out, feedback, and human-escalation controls proportionate to consequence.", "Test adversarial misunderstandings, personalization drift, stale memory, and failure recovery; preserve unresolved safety dependencies."],
        ["AI interaction-state model", "uncertainty and provenance contract", "correction and escalation flow", "safe-failure acceptance criteria"],
        "Never present generated content, confidence, personalization, or autonomous action as certain, authoritative, or irreversible when the system cannot prove it.",
        ["interaction-states-forms-and-navigation", "ai-model-and-data-architecture", "ai-safety-and-action-governance", "accessibility-contracts-and-assistive-validation"],
        ["latency", "uncertainty", "provenance", "correction", "undo", "escalation", "safe-failure"], mutation="authorized-workspace", human=True),
    "content-copy-and-authentic-assets": D(
        "Create truthful task-specific interface copy, realistic content data, and authorized assets with provenance and state coverage.",
        ["Replace the dashboard lorem ipsum and stock placeholders with truthful product copy, realistic records, and authorized imagery.", "Write concise labels, help, errors, empty-state guidance, and recovery copy for the approved flow using verified product facts."],
        [("Define the product requirements and acceptance criteria for this feature.", "requirements-and-delivery-contract"), ("Choose the final visual direction, palette, type, and composition.", "design-context-and-direction-contract")],
        ["Freeze product facts, audience language, legal or brand constraints, content schema, localization boundary, and asset authority.", "Map content to user intent and every loading, empty, error, permission, validation, success, and recovery state.", "Write specific labels and messages that explain consequence and next action; remove lorem ipsum, fake testimonials, invented metrics, and decorative jargon.", "Use only authorized assets and record source, license, transformation, alt intent, and replacement rule.", "Check truncation, pluralization, variable data, localization expansion, and screen-reader comprehension before handoff."],
        ["interface copy deck", "realistic content fixtures", "asset provenance ledger", "state-content matrix"],
        "No placeholder, invented claim, unverifiable metric, fake social proof, or unlicensed asset may enter a candidate presented as realistic or release-ready.",
        ["visual-language-and-anti-template-controls", "interaction-states-forms-and-navigation", "accessibility-contracts-and-assistive-validation", "documentation-authoring"],
        ["truthful-copy", "authentic-content", "asset-provenance", "localization", "state-content"], mutation="authorized-workspace"),
    "cross-domain-ui-preflight-checklists": D(
        "Run one bounded preflight across accessibility, authentic content, interaction states, responsiveness, motion, AI states, and release evidence without repairing source.",
        ["Run the final UI preflight across responsive, accessibility, content, form, motion, and recovery requirements before review.", "Check this rendered feature for cross-domain omissions and return blocking findings with evidence requirements."],
        [("Capture the missing browser renders and interaction traces required for review.", "ui-review-scope-and-evidence-acquisition"), ("Apply the approved fixes to product source after the findings are accepted.", "ui-remediation")],
        ["Freeze acceptance criteria, supported surfaces, applicable UI domains, release boundary, and current evidence manifest.", "Select only applicable checks and state why any domain is not applicable.", "Verify required states, widths, zoom, input modes, assistive behavior, motion reduction, content provenance, and AI uncertainty against cited evidence.", "Classify findings by severity, reproducibility, affected task, owner, and evidence needed to close.", "Stop on blocking gaps and route missing capture or authorized remediation; never mark a checklist item passed from assertion alone."],
        ["UI preflight result", "blocking-finding register", "evidence-gap list", "residual-risk summary"],
        "A preflight item passes only with current criterion-linked evidence; unchecked, not-applicable without rationale, and source-inspection-only items remain unresolved.",
        ["ui-review-scope-and-evidence-acquisition", "evidence-based-ui-review-and-release-gates", "ui-remediation", "accessibility-contracts-and-assistive-validation"],
        ["cross-domain-preflight", "current-evidence", "blocking-findings", "residual-risk"], rendered=True),
    "design-context-and-direction-contract": D(
        "Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.",
        ["Turn these approved requirements, brand assets, and audience facts into a bounded web-app design direction contract.", "Define the surface mode, information emphasis, spatial thesis, visual constraints, and unresolved taste choices before UI implementation."],
        [("Implement the responsive layouts and component source from an approved direction.", "responsive-layout-and-spatial-composition"), ("Independently critique the rendered implementation and issue a release recommendation.", "rendered-ui-critique-and-release-disposition")],
        ["Classify product facts, acceptance criteria, audience evidence, brand assets, existing tokens, platform constraints, references, conflicts, and unknowns.", "Choose the surface mode and state the user flow, information hierarchy, content priorities, and success criteria before visual styling.", "Derive a spatial thesis, density, typography role, color role, imagery or icon direction, and interaction tone from cited authority.", "Separate required constraints, reversible proposals, unresolved taste decisions, and forbidden unsupported decoration.", "Emit a contract with invariants, target surfaces, decision owners, and handoff gates; do not implement or approve release."],
        ["design evidence read", "user-flow and information-hierarchy contract", "visual and spatial direction", "design decision ledger"],
        "The design direction cannot pass unless each major visual or spatial choice traces to product purpose, audience, content, brand authority, or an explicitly human-owned taste decision.",
        ["ui-task-routing-and-governance", "visual-language-and-anti-template-controls", "responsive-layout-and-spatial-composition", "rendered-ui-critique-and-release-disposition"],
        ["user-flow", "information-hierarchy", "brand-authority", "spatial-thesis", "success-criteria", "taste-decision"], human=True),
    "design-system-foundation-and-token-extraction": D(
        "Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.",
        ["Build the minimal semantic token and component foundation this approved interface needs, reusing the existing stack.", "Normalize approved design primitives into project tokens, component variants, focus behavior, and theme rules."],
        [("Extract primitives from this external authorized site without writing project tokens.", "external-design-token-extraction-and-normalization"), ("Define the page-level responsive composition and reflow behavior.", "responsive-layout-and-spatial-composition")],
        ["Inventory existing tokens, components, CSS conventions, dependencies, themes, and approved design direction before adding anything.", "Reuse the project foundation where sufficient; add only semantic color, type, spacing, radius, elevation, motion, and layout tokens required by real states.", "Define component anatomy, variants, sizes, content bounds, interaction states, accessibility behavior, and composition rules.", "Map raw or imported values to semantic roles with provenance; prohibit one-off values unless recorded as an exception.", "Persist the smallest working foundation and verify representative components across themes and states."],
        ["semantic token set", "component contract catalog", "theme and state rules", "persistence and exception ledger"],
        "Do not create a parallel design system, token alias maze, or component abstraction when the existing project foundation can express the required states.",
        ["external-design-token-extraction-and-normalization", "visual-language-and-anti-template-controls", "responsive-layout-and-spatial-composition", "interaction-states-forms-and-navigation"],
        ["semantic-tokens", "component-contracts", "states", "themes", "persistence", "provenance"], mutation="authorized-workspace"),
    "divergent-prototyping-and-variant-selection": D(
        "Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.",
        ["Create three working variants that differ in layout, density, navigation, and emphasis rather than color alone.", "Set up an isolated prototype comparison using authentic content and record the human-selected direction without promoting it automatically."],
        [("Polish the selected direction into the production design system and responsive source.", "design-system-foundation-and-token-extraction"), ("Run an independent release review on the promoted production implementation.", "rendered-ui-critique-and-release-disposition")],
        ["Freeze one brief, authentic content set, project tokens, supported viewport, comparison criteria, and named axes of divergence.", "Build each variant in an isolated path or artifact without altering production routes or shared behavior.", "Make variants structurally different in information hierarchy, composition, interaction, or density; reject superficial palette swaps.", "Capture equivalent states and compare task clarity, accessibility implications, responsiveness, feasibility, and tradeoffs.", "Record the human selection, rejected alternatives, rationale, and promotion handoff; never self-select or auto-promote."],
        ["isolated working variants", "equivalent comparison captures", "tradeoff matrix", "human selection and promotion handoff"],
        "At least two variants must differ structurally on declared axes; palette-only or typography-only alternatives do not count as divergence.",
        ["design-context-and-direction-contract", "design-system-foundation-and-token-extraction", "responsive-layout-and-spatial-composition", "rendered-ui-critique-and-release-disposition"],
        ["divergence", "isolation", "authentic-content", "fair-comparison", "human-selection"], mutation="authorized-workspace", human=True, rendered=True),
    "evidence-based-ui-review-and-release-gates": D(
        "Apply explicit UI release criteria to current rendered evidence, aggregate blocking findings, and recommend a bounded release disposition without source repair.",
        ["Evaluate the current desktop and mobile evidence against the approved UI release criteria and report blockers.", "Aggregate accessibility, responsive, content, interaction, and visual findings into a release recommendation with residual risk."],
        [("Collect missing viewport captures, traces, and runtime evidence before judgment.", "ui-review-scope-and-evidence-acquisition"), ("Modify product source to fix the accepted review findings.", "ui-remediation")],
        ["Freeze release criteria, current evidence manifest, target commit or artifact identity, supported surfaces, and accepted-risk authority.", "Reject stale, mismatched, source-only, or self-attested evidence and route recapture needs.", "Map each criterion to evidence and consolidate duplicate findings without erasing domain-specific impact.", "Classify blockers, non-blockers, waived risks, recapture requirements, and invalidated prior evidence.", "Recommend pass, pass-with-explicit-risk, needs-repair, or blocked to the human release owner; do not edit source or release."],
        ["criterion-to-evidence matrix", "deduplicated release findings", "UI release recommendation", "risk and recapture ledger"],
        "No release criterion may pass from source inspection, prior screenshots, or reviewer assertion when current rendered or interaction evidence is required.",
        ["ui-review-scope-and-evidence-acquisition", "rendered-ui-critique-and-release-disposition", "cross-domain-ui-preflight-checklists", "ui-remediation"],
        ["criterion-evidence", "current-render", "blocking-findings", "release-recommendation", "recapture"], human=True, rendered=True),
    "existing-interface-redesign-and-preservation": D(
        "Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.",
        ["Before redesigning this live interface, inventory the user flow, routes, content, analytics, SEO, and behavioral invariants that must survive.", "Define the migration order and explicit preservation contract for modernizing this existing product UI."],
        [("Choose a visual direction for a new interface with no existing product behavior to preserve.", "design-context-and-direction-contract"), ("Apply accepted redesign fixes to product source after review.", "ui-remediation")],
        ["Freeze the redesign brief and inspect authorized current routes, content, components, analytics, SEO metadata, accessibility behavior, and known business invariants.", "Separate verified product truth from visual debt, implementation accident, unknown dependency, and explicitly removable behavior.", "Map current user flows, information architecture, deep links, forms, state transitions, tracking, and search or sharing contracts.", "Define preserve, migrate, replace, and remove decisions with owner, rationale, tests, and rollback or compatibility needs.", "Sequence a reversible migration and hand off constraints to design direction; do not redesign or repair source in this audit."],
        ["current-state UI audit", "preservation and migration contract", "invariant test map", "redesign risk ledger"],
        "No existing route, content obligation, analytics event, SEO contract, user task, or behavior may be silently removed because it appears visually obsolete.",
        ["design-context-and-direction-contract", "ui-task-routing-and-governance", "ui-remediation", "rendered-ui-critique-and-release-disposition"],
        ["preservation", "user-flow", "information-architecture", "SEO", "analytics", "behavior", "migration"], human=True),
    "external-design-token-extraction-and-normalization": D(
        "Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes.",
        ["Extract the supplied authorized site's captures into observable color, type, spacing, radius, shadow, and motion primitives with provenance.", "Normalize these supplied external design files into candidate semantic roles without treating them as project authority."],
        [("Persist approved semantic tokens and components into this project's design system.", "design-system-foundation-and-token-extraction"), ("Copy the external product's layout, brand, assets, or interaction wholesale.", "design-context-and-direction-contract")],
        ["Verify source authorization, supplied capture or file identity, scope, timestamp, terms, and prohibited assets or personal data.", "Read only supplied authorized captures or files; do not browse, fetch, bypass access controls, or perform external writes.", "Record exact source, selector or artifact location, viewport, observed value, confidence, and state for every primitive.", "Cluster raw values and propose semantic roles while preserving contradictions, one-offs, responsive variants, and unknown intent.", "Emit a normalization report and candidate mapping only; require separate human approval and design-system capability for project writes."],
        ["authorized external primitive inventory", "provenance and confidence ledger", "normalized candidate token map", "unknown and conflict register"],
        "Observed external values are evidence, not project authority: no project token, copied asset, or design decision may be written or approved by this capability.",
        ["design-system-foundation-and-token-extraction", "design-context-and-direction-contract", "source-metadata-and-provenance", "ui-review-scope-and-evidence-acquisition"],
        ["authorization", "external-read", "primitive-extraction", "normalization", "provenance", "no-project-write"]),
    "interaction-states-forms-and-navigation": D(
        "Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.",
        ["Implement this form and route flow with validation, async, permission, empty, error, success, and recovery states.", "Complete the missing keyboard-operable controls and navigation-state behavior for the approved responsive UI."],
        [("Specify the assistive-technology acceptance and test matrix for the completed interaction.", "accessibility-contracts-and-assistive-validation"), ("Choose the page-level visual hierarchy, grid, density, and breakpoint composition.", "responsive-layout-and-spatial-composition")],
        ["Freeze the approved user flow, routes, roles, data states, validation rules, destructive actions, recovery behavior, and component foundation.", "Model every control and transition including default, hover, focus, active, selected, disabled, pending, success, error, interrupted, expired, and permission-denied states as applicable.", "Implement semantic controls, URL and history behavior, labels, inline and summary errors, confirmation, undo, idempotency cues, and safe destructive-action handling.", "Preserve user input and context through validation, async failure, navigation, timeout, and retry where safe.", "Verify keyboard order, focus movement, deep links, refresh/back behavior, variable content, and failure recovery; record unresolved service dependencies."],
        ["interaction and state model", "implemented controls/forms/navigation", "state coverage matrix", "recovery verification evidence"],
        "The happy path cannot pass alone: every applicable loading, empty, validation, error, permission, disabled, interruption, success, and recovery state must exist and be reachable for verification.",
        ["responsive-layout-and-spatial-composition", "accessibility-contracts-and-assistive-validation", "content-copy-and-authentic-assets", "purposeful-motion-and-animation-engineering"],
        ["controls", "navigation", "forms", "loading", "empty", "error", "permission", "disabled", "success", "interruption", "recovery"], mutation="authorized-workspace"),
    "purposeful-motion-and-animation-engineering": D(
        "Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state.",
        ["Add motion that explains this state transition, including interruption, reverse, reduced-motion, and failure behavior.", "Implement deterministic entrance and navigation choreography for the approved interface without blocking input or hiding state."],
        [("Choose the static visual language, typography, color, and anti-template direction.", "visual-language-and-anti-template-controls"), ("Perform the final rendered animation critique and release disposition.", "rendered-ui-critique-and-release-disposition")],
        ["Freeze the communication purpose, state transition, runtime, performance budget, input behavior, and reduced-motion requirement.", "Choose the smallest motion primitive that clarifies hierarchy, causality, continuity, progress, feedback, or navigation.", "Implement from explicit state with deterministic timing; support interruption, rapid repeat, reverse or replacement, and cleanup.", "Provide reduced or absent motion without losing information, order, focus, or task completion.", "Verify slow devices, input during motion, resize, hidden tabs, route changes, reduced motion, and animation completion state."],
        ["motion purpose map", "implemented deterministic animation", "reduced-motion behavior", "interaction and performance evidence"],
        "Motion without a named communication purpose, deterministic end state, interruption behavior, and information-equivalent reduced-motion path must be removed or blocked.",
        ["visual-language-and-anti-template-controls", "interaction-states-forms-and-navigation", "accessibility-contracts-and-assistive-validation", "rendered-ui-critique-and-release-disposition"],
        ["purpose", "determinism", "interruption", "reduced-motion", "performance", "state"], mutation="authorized-workspace", rendered=True),
    "rendered-ui-critique-and-release-disposition": D(
        "Independently critique current rendered UI and animation behavior, prioritize reproducible findings, and recommend a bounded disposition without source mutation.",
        ["Critique these current mobile, tablet, and desktop captures plus interaction traces against the design and accessibility contracts.", "Prioritize this rendered UI's visual, spatial, content, responsive, state, and motion defects and state what must be recaptured."],
        [("Define which routes, states, viewports, traces, and tools must be captured for review.", "ui-review-scope-and-evidence-acquisition"), ("Edit the product source to fix the accepted UI findings.", "ui-remediation")],
        ["Verify evidence identity, recency, route, viewport, state, zoom, theme, input mode, runtime, and contract coverage before critique.", "Review user-flow clarity, information hierarchy, typography, color, spacing, content authenticity, responsive reflow, states, accessibility signals, and animation behavior in real renders.", "Write one reproducible finding per issue with evidence citation, affected task and state, severity, principle, consequence, and bounded repair direction.", "Separate blockers, high-value improvements, taste choices, evidence gaps, and accepted residual risk.", "Recommend pass, needs-repair, recapture, or blocked to the human owner; never mutate product source or perform release."],
        ["rendered critique", "prioritized reproducible findings", "remediation hierarchy", "recapture and disposition recommendation"],
        "Static source review, DOM assertions, or a single ideal screenshot cannot substitute for current rendered evidence across the declared routes, states, viewports, input modes, and motion behavior.",
        ["ui-review-scope-and-evidence-acquisition", "evidence-based-ui-review-and-release-gates", "ui-remediation", "cross-domain-ui-preflight-checklists"],
        ["real-renders", "multi-viewport", "interaction-traces", "reproducible-findings", "no-source-mutation"], mutation="artifact-output", human=True, rendered=True),
    "responsive-layout-and-spatial-composition": D(
        "Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels.",
        ["Implement this approved information hierarchy from narrow mobile through tablet and desktop, including intermediate widths and 200% zoom.", "Replace the fixed desktop canvas with content-driven grids, reflow rules, density bounds, and touch-safe responsive composition."],
        [("Define the component token system and theme foundation.", "design-system-foundation-and-token-extraction"), ("Implement form validation, async, permission, and recovery states inside the completed layout.", "interaction-states-forms-and-navigation")],
        ["Freeze user flow, information hierarchy, authentic content extremes, supported viewport range, zoom target, input modes, and existing layout constraints.", "Order content semantically before choosing columns; define primary, supporting, progressive, and deferrable regions.", "Implement content-driven width constraints, grids or flex rules, spacing rhythm, alignment, density, and reflow without device-specific duplication.", "Handle narrow, intermediate, wide, short-height, long-content, localization, zoom, overflow, safe areas, keyboard, and touch targets.", "Capture representative widths and stress states; record clipping, reordering, hidden-content, and interaction risks for review."],
        ["responsive composition source", "breakpoint and reflow contract", "spatial hierarchy map", "multi-width stress evidence"],
        "Desktop and mobile endpoints are insufficient: the layout must survive intermediate widths, 200% zoom, long or localized content, overflow, and touch-target constraints without losing task order.",
        ["design-system-foundation-and-token-extraction", "visual-language-and-anti-template-controls", "interaction-states-forms-and-navigation", "accessibility-contracts-and-assistive-validation"],
        ["information-hierarchy", "mobile", "tablet", "desktop", "intermediate-widths", "zoom", "overflow", "density", "touch-targets"], mutation="authorized-workspace", rendered=True),
    "ui-review-scope-and-evidence-acquisition": D(
        "Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source.",
        ["Define the review matrix and capture current routes, states, widths, themes, zoom, input, and motion traces for this UI.", "Acquire reproducible rendered evidence for the changed interface and bind every capture to source, runtime, route, state, and viewport identity."],
        [("Critique the completed capture set and prioritize UI defects.", "rendered-ui-critique-and-release-disposition"), ("Modify product source in response to previously accepted findings.", "ui-remediation")],
        ["Freeze changed surfaces, user tasks, acceptance criteria, supported browsers and devices, high-risk states, source identity, and review independence.", "Build a route-state-viewport-theme-input-motion matrix with explicit inclusions, exclusions, and rationale.", "Use only approved local commands and authorized external reads to capture screenshots, traces, recordings, accessibility snapshots, and console or network evidence.", "Bind each artifact to timestamp, source revision, environment, route, state setup, viewport, zoom, input mode, theme, tool, and hash.", "Assess evidence completeness only; route a complete manifest to critique or return needs-input/blocked without judging design quality."],
        ["UI review scope matrix", "rendered evidence bundle", "capture provenance manifest", "evidence completeness result"],
        "No capture is review evidence unless its source revision, runtime, route, state, viewport, zoom or scale, input mode, timestamp, tool, and hash are recorded and current.",
        ["rendered-ui-critique-and-release-disposition", "evidence-based-ui-review-and-release-gates", "ui-remediation", "cross-domain-ui-preflight-checklists"],
        ["scope-matrix", "capture", "provenance", "current-evidence", "independence", "no-critique"], mutation="artifact-output", rendered=True),
    "ui-task-routing-and-governance": D(
        "Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.",
        ["Route this mixed UI request to the next atomic design, implementation, evidence, review, or remediation capability.", "Classify whether this is a new build, preservation-aware redesign, external token extraction, source repair, or rendered review and state the write boundary."],
        [("Create the actual design direction and user-flow contract.", "design-context-and-direction-contract"), ("Capture browser renders and traces for independent review.", "ui-review-scope-and-evidence-acquisition")],
        ["Inventory requested outcome, supplied artifacts, product authority, target surfaces, current source or render state, external sources, and explicit exclusions.", "Classify new design, existing redesign, token import, implementation, preflight, evidence capture, critique, repair, or release-decision intent.", "Determine source-write, artifact-write, local-exec, external-read, and human-decision boundaries before route selection.", "Identify missing prerequisites, incompatible identities, applicable specialist branches, and stop conditions.", "Return one next capability and conditional follow-ups only; preserve unknowns and perform no downstream work."],
        ["UI task classification", "authorization and write-boundary record", "next-capability route", "missing-input and stop-condition list"],
        "Routing must not smuggle design, review, source mutation, browser capture, or release judgment into the intake artifact.",
        ["design-context-and-direction-contract", "existing-interface-redesign-and-preservation", "ui-review-scope-and-evidence-acquisition", "ui-remediation"],
        ["classification", "authorization", "write-boundary", "next-capability", "no-downstream-work"]),
    "visual-language-and-anti-template-controls": D(
        "Establish and implement a purposeful visual language that reinforces hierarchy and brand evidence while rejecting generic template patterns and unsupported decoration.",
        ["Turn the approved direction into a distinctive typography, color, shape, surface, icon, and emphasis language grounded in product purpose.", "Remove the generic dashboard-template look and implement a coherent visual grammar without sacrificing hierarchy or accessibility."],
        [("Define page-level grid, responsive reflow, and spatial density across widths.", "responsive-layout-and-spatial-composition"), ("Write the truthful product copy, realistic records, and authorized assets.", "content-copy-and-authentic-assets")],
        ["Freeze the design contract, brand evidence, authentic content, accessibility constraints, existing system, and explicit anti-goals.", "Name a small visual thesis and map typography, color, shape, border, surface, imagery, icon, and emphasis roles to it.", "Audit and remove generic hero, card-grid, gradient, pill, floating-panel, decorative-chart, and icon patterns that lack task or brand purpose.", "Implement reusable visual rules through the existing token and component foundation rather than one-off styling.", "Stress hierarchy, contrast, dense and sparse content, themes, and states; preserve human-owned taste alternatives when evidence cannot decide."],
        ["visual-language specification", "implemented visual grammar", "anti-template audit", "taste-decision register"],
        "Every prominent visual device must serve hierarchy, task, content, state, or evidenced brand identity; unsupported decoration and generic template motifs must be removed.",
        ["design-context-and-direction-contract", "design-system-foundation-and-token-extraction", "responsive-layout-and-spatial-composition", "content-copy-and-authentic-assets"],
        ["typography", "color", "shape", "hierarchy", "brand", "anti-template", "accessibility"], mutation="authorized-workspace", human=True),
}


HOLDOUTS: dict[str, tuple[str, str]] = {
    "accessibility-contracts-and-assistive-validation": ("Specify and validate task-linked names, keyboard operation, focus return, zoom, errors, and screen-reader outcomes for this implemented dialog flow.", "Add the missing product form fields and navigation implementation before independent accessibility validation."),
    "ai-interaction-and-probabilistic-ux": ("Design partial, uncertain, unsafe, corrected, and human-escalated states for this approved generative assistant.", "Select model hosting, retrieval storage, tool permissions, and autonomy architecture."),
    "content-copy-and-authentic-assets": ("Replace fake metrics and placeholder cards with verified claims, realistic edge-case records, recovery copy, and licensed assets.", "Choose the interface's final typography, color, composition, and brand direction."),
    "cross-domain-ui-preflight-checklists": ("Against current evidence, check all applicable responsive, content, state, accessibility, motion, and AI-UX release concerns without repairs.", "Open the browser and collect the missing route-state-viewport evidence bundle."),
    "design-context-and-direction-contract": ("Derive a user-flow, hierarchy, spatial, and visual direction contract from approved behavior, audience facts, and brand evidence.", "Implement the approved direction in responsive product source."),
    "design-system-foundation-and-token-extraction": ("Extend the existing token and component system only enough to express the approved themes, variants, and states.", "Observe and normalize primitives from an authorized external surface without project writes."),
    "divergent-prototyping-and-variant-selection": ("Build structurally distinct isolated candidates on the same content and criteria, then record the owner's selection.", "Polish and promote the selected candidate into production source."),
    "evidence-based-ui-review-and-release-gates": ("Map current captures and domain findings to release criteria, blockers, residual risk, and a human-owned disposition.", "Change the source to resolve the accepted blocking findings."),
    "existing-interface-redesign-and-preservation": ("Inventory current routes, tasks, analytics, SEO, content, and behavior before defining a reversible redesign migration.", "Create a visual direction for a greenfield surface with no inherited interface."),
    "external-design-token-extraction-and-normalization": ("From an authorized source, record observed primitive values, states, provenance, confidence, and candidate semantic roles.", "Write the approved candidate roles into this project's token and component files."),
    "interaction-states-forms-and-navigation": ("Implement the approved flow's async, empty, validation, denied, failed, interrupted, success, and retry behavior with history and focus continuity.", "Produce the independent assistive-technology validation matrix for the finished flow."),
    "purposeful-motion-and-animation-engineering": ("Implement an interruptible causal transition with deterministic end state and information-equivalent reduced motion.", "Choose the static visual grammar and remove generic decorative patterns."),
    "rendered-ui-critique-and-release-disposition": ("Using current multi-width captures and traces, issue reproducible prioritized findings and a bounded disposition without edits.", "Define and capture the route-state-viewport evidence matrix before critique."),
    "responsive-layout-and-spatial-composition": ("Implement semantic content order and resilient reflow across narrow, intermediate, wide, zoomed, and long-content conditions.", "Implement validation, permission, pending, and recovery logic within an already approved layout."),
    "ui-review-scope-and-evidence-acquisition": ("Capture a provenance-bound matrix of changed routes, states, widths, themes, zoom, inputs, and motion without critique.", "Judge the captures, prioritize defects, and recommend release disposition."),
    "ui-task-routing-and-governance": ("Classify this request's UI mode, authorization, write boundary, missing inputs, and one next atomic capability.", "Write the actual direction contract and visual hierarchy for the routed task."),
    "visual-language-and-anti-template-controls": ("Implement a product-grounded visual grammar and remove unsupported generic dashboard motifs while preserving accessibility.", "Define detailed breakpoint, grid, density, and reflow behavior across viewport sizes."),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def baseline_for(slug: str, capability: dict[str, Any], workspace: Path) -> dict[str, Any]:
    if slug == "design-context-and-direction-contract":
        contract = load(workspace / "slots/design-context-and-direction-contract/contract.json")
        if contract.get("status") == "released" and contract.get("version") == "1.0.0":
            return {"kind": "released-v1-slot", "identity": "design-context-and-direction-contract@1.0.0", "reason": "Closest released V1 boundary; candidate must broaden lifecycle coverage without regressing evidence and authority gates."}
    roots = sorted({evidence.split("/", 1)[0] for evidence in capability["source_evidence"] if "/" in evidence})
    return {"kind": "source-skill", "identity": roots[0] if roots else "no-capability-baseline", "reason": "Closest immutable source behavior; no released V1 Slot has this exact atomic responsibility."}


def render_skill(slug: str, capability: dict[str, Any], design: dict[str, Any]) -> str:
    procedure = "\n".join(f"{index}. {item}" for index, item in enumerate(design["procedure"], 1))
    inputs = "\n".join(f"- {item}" for item in capability["inputs"])
    outputs = "\n".join(f"- {item}" for item in design["artifacts"])
    coverage = "\n".join(f"- `{item}`" for item in design["coverage"])
    neighbors = "\n".join(f"- `{item}`" for item in design["neighbors"])
    rendered = """
## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.
""" if design["rendered_evidence"] else ""
    human = """
## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.
""" if design["human_decision"] else ""
    return f"""---
name: {slug}
description: {design['trigger']} Do not use for {design['anti'][0][0].rstrip('.').lower()} or {design['anti'][1][0].rstrip('.').lower()}.
---

# {slug.replace('-', ' ').title()}

## Responsibility

{design['trigger']}

## Trigger

Use when the requested outcome is: {design['trigger']}

Do not use when:
- {design['anti'][0][0]} Route to `{design['anti'][0][1]}`.
- {design['anti'][1][0]} Route to `{design['anti'][1][1]}`.

## Required Inputs

{inputs}

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

{procedure}

## Output Contract

Produce:
{outputs}

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

{coverage}

## Hard Gates

- {design['distinctive_gate']}
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
{rendered}{human}
## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

{capability['non_responsibility']}

Adjacent capabilities:
{neighbors}

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
"""


def schemas() -> dict[str, dict[str, Any]]:
    strings = {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": True}
    nonempty = {**strings, "minItems": 1}
    base = {"schema_version": {"const": "2.0"}, "id": {"type": "string"}}
    contract = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "responsibility", "inputs", "outputs", "permission_identity", "statuses", "hard_gates", "forbidden_actions", "artifact_types", "execution", "policy"], "properties": {**base, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string", "pattern": "^capability:"}, "responsibility": {"type": "string", "minLength": 20}, "inputs": nonempty, "outputs": nonempty, "permission_identity": {"enum": ["workspace-write", "artifact-write-local-exec-external-read"]}, "statuses": {"const": ["passed", "needs-input", "blocked", "failed"]}, "hard_gates": nonempty, "forbidden_actions": nonempty, "artifact_types": nonempty, "execution": {"type": "object", "additionalProperties": False, "required": ["model_tools", "host_actions", "external", "mutation_scope", "remote_write"], "properties": {"model_tools": nonempty, "host_actions": strings, "external": {"enum": ["none", "read-only"]}, "mutation_scope": {"enum": ["run-output", "authorized-workspace", "artifact-output"]}, "remote_write": {"const": False}}}, "policy": {"type": "object", "additionalProperties": False, "required": ["human_decision", "rendered_evidence", "review_source_separation", "coverage"], "properties": {"human_decision": {"type": "boolean"}, "rendered_evidence": {"type": "boolean"}, "review_source_separation": {"const": True}, "coverage": nonempty}}}}
    provenance = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "phase2_artifact_tree_sha256", "phase3_artifact_tree_sha256", "source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs", "candidate_files"], "properties": {**base, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string"}, "phase2_artifact_tree_sha256": {"const": PHASE2_TREE}, "phase3_artifact_tree_sha256": {"const": PHASE3_TREE}, "source_cluster_ids": strings, "canonical_unit_ids": strings, "retained_auxiliary_unit_ids": strings, "root_derived_atom_ids": strings, "source_fragment_ids": strings, "fusion_decision_ids": nonempty, "decision_references": nonempty, "source_evidence": nonempty, "source_defect_refs": strings, "candidate_files": {"type": "object", "additionalProperties": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "minProperties": 3}}}
    case = {"type": "object", "additionalProperties": False, "required": ["id", "kind", "input", "expected_skill_id", "forbidden_skill_ids", "expected_status", "reason"], "properties": {"id": {"type": "string", "pattern": "^V2-P4-"}, "kind": {"enum": ["should-trigger", "should-not-trigger", "boundary", "authority-stop"]}, "input": {"type": "string", "minLength": 10}, "expected_skill_id": {"type": ["string", "null"]}, "forbidden_skill_ids": strings, "expected_status": {"enum": ["route", "needs-input", "blocked"]}, "reason": {"type": "string", "minLength": 10}}}
    triggers = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "skill_id", "cases"], "properties": {"schema_version": {"const": "2.0"}, "skill_id": {"type": "string"}, "cases": {"type": "array", "minItems": 6, "items": case}}}
    mutation = {"type": "object", "additionalProperties": False, "required": ["id", "target", "remove_exact_text", "expected_gate"], "properties": {"id": {"type": "string", "pattern": "^V2-P4-MUT-"}, "target": {"const": "SKILL.md"}, "remove_exact_text": {"type": "string", "minLength": 10}, "expected_gate": {"const": "required-semantic-marker"}}}
    evaluation = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "skill_id", "version", "status", "baseline", "candidate", "holdout_case_ids", "mutations", "rubric", "execution_state"], "properties": {"schema_version": {"const": "2.0"}, "skill_id": {"type": "string"}, "version": {"const": VERSION}, "status": {"const": "planned"}, "baseline": {"type": "object", "additionalProperties": False, "required": ["kind", "identity", "reason"], "properties": {"kind": {"enum": ["released-v1-slot", "source-skill", "no-capability-baseline"]}, "identity": {"type": "string"}, "reason": {"type": "string"}}}, "candidate": {"type": "object", "additionalProperties": False, "required": ["identity", "skill_sha256", "contract_sha256"], "properties": {"identity": {"type": "string"}, "skill_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "contract_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}}, "holdout_case_ids": {"type": "array", "minItems": 2, "items": {"type": "string"}, "uniqueItems": True}, "mutations": {"type": "array", "minItems": 1, "items": mutation}, "rubric": {"type": "array", "minItems": 6, "items": {"type": "string"}, "uniqueItems": True}, "execution_state": {"const": "not-run-phase-9"}}}
    recipe = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "description", "inputs", "outputs", "steps", "edges", "human_checkpoints", "feedback_routes", "gates", "forbidden_actions", "evaluation_state"], "properties": {"schema_version": {"const": "2.0"}, "id": {"const": "complete-ui-design-and-review"}, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "description": {"type": "string"}, "inputs": nonempty, "outputs": nonempty, "steps": {"type": "array", "minItems": 17, "items": {"type": "object", "additionalProperties": False, "required": ["id", "skill_ref", "when", "depends_on", "permission_identity", "mutation_scope", "outputs", "gates"], "properties": {"id": {"type": "string"}, "skill_ref": {"type": "string"}, "when": {"type": "string"}, "depends_on": strings, "permission_identity": {"type": "string"}, "mutation_scope": {"enum": ["run-output", "authorized-workspace", "artifact-output"]}, "outputs": nonempty, "gates": nonempty}}}, "edges": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["from", "to", "condition"], "properties": {"from": {"type": "string"}, "to": {"type": "string"}, "condition": {"type": "string"}}}}, "human_checkpoints": nonempty, "feedback_routes": {"type": "array", "items": {"type": "object", "required": ["from", "to", "artifact", "authorization"], "properties": {"from": {"type": "string"}, "to": {"type": "string"}, "artifact": {"type": "string"}, "authorization": {"const": "explicit-human-approval"}}, "additionalProperties": False}}, "gates": nonempty, "forbidden_actions": nonempty, "evaluation_state": {"const": "not-run-phase-9"}}}
    return {"candidate-skill.schema.json": contract, "provenance.schema.json": provenance, "trigger-cases.schema.json": triggers, "evaluation-plan.schema.json": evaluation, "candidate-recipe.schema.json": recipe}


def build_recipe(capabilities: dict[str, dict[str, Any]]) -> dict[str, Any]:
    step_specs = [
        ("route", "ui-task-routing-and-governance", "always", []),
        ("preserve-existing", "existing-interface-redesign-and-preservation", "existing interface or redesign request", ["route"]),
        ("extract-external-tokens", "external-design-token-extraction-and-normalization", "authorized external captures or files supplied", ["route"]),
        ("direction", "design-context-and-direction-contract", "new design, approved redesign, or selected visual work", ["route"]),
        ("prototype-variants", "divergent-prototyping-and-variant-selection", "material uncertainty merits divergent working variants", ["direction"]),
        ("visual-language", "visual-language-and-anti-template-controls", "visual implementation is in scope", ["direction"]),
        ("design-system", "design-system-foundation-and-token-extraction", "tokens or reusable components are required", ["direction"]),
        ("authentic-content", "content-copy-and-authentic-assets", "interface contains product copy, records, imagery, icons, or claims", ["direction"]),
        ("responsive-composition", "responsive-layout-and-spatial-composition", "multi-viewport interface is in scope", ["direction"]),
        ("interaction-states", "interaction-states-forms-and-navigation", "controls, navigation, forms, async data, permission, or recovery exist", ["responsive-composition"]),
        ("accessibility", "accessibility-contracts-and-assistive-validation", "interactive user-facing surface is in scope", ["interaction-states"]),
        ("motion", "purposeful-motion-and-animation-engineering", "motion communicates hierarchy, navigation, feedback, progress, or state", ["interaction-states"]),
        ("ai-ux", "ai-interaction-and-probabilistic-ux", "probabilistic or agentic behavior is user-visible", ["interaction-states"]),
        ("preflight", "cross-domain-ui-preflight-checklists", "implementation is ready for cross-domain preflight", ["accessibility"]),
        ("review-evidence", "ui-review-scope-and-evidence-acquisition", "current rendered evidence is required", ["preflight"]),
        ("rendered-critique", "rendered-ui-critique-and-release-disposition", "evidence manifest is complete", ["review-evidence"]),
        ("release-gate", "evidence-based-ui-review-and-release-gates", "specialist findings and current evidence are available", ["rendered-critique"]),
    ]
    steps = []
    for step_id, skill_id, when, depends_on in step_specs:
        design = DESIGNS[skill_id]; capability = capabilities[skill_id]
        steps.append({"id": step_id, "skill_ref": f"{skill_id}@{VERSION}", "when": when, "depends_on": depends_on, "permission_identity": capability["permission_identity"], "mutation_scope": design["mutation_scope"], "outputs": design["artifacts"], "gates": [design["distinctive_gate"], "authority-and-write-boundary"]})
    edges = [{"from": dependency, "to": step["id"], "condition": step["when"]} for step in steps for dependency in step["depends_on"]]
    edges.extend([
        {"from": "preserve-existing", "to": "direction", "condition": "existing-interface preservation contract is required"},
        {"from": "extract-external-tokens", "to": "design-system", "condition": "human-approved normalized external primitives are selected"},
        {"from": "prototype-variants", "to": "visual-language", "condition": "a human selected a variant for promotion"},
        {"from": "visual-language", "to": "responsive-composition", "condition": "visual implementation branch is active"},
        {"from": "design-system", "to": "responsive-composition", "condition": "design-system branch is active"},
        {"from": "authentic-content", "to": "interaction-states", "condition": "content branch is active"},
        {"from": "motion", "to": "preflight", "condition": "motion branch is active"},
        {"from": "ai-ux", "to": "preflight", "condition": "AI interaction branch is active"},
    ])
    return {"schema_version": "2.0", "id": "complete-ui-design-and-review", "version": VERSION, "status": "evaluating", "description": "Conditionally compose atomic UX/UI design, implementation, evidence, critique, and release-recommendation candidates while preserving reviewer/remediator separation.", "inputs": ["approved product behavior and acceptance criteria", "design and brand authority", "project or existing-interface context", "supported routes, states, viewports, input modes, and assistive technologies", "explicit source, artifact, local-exec, and external-read authorization"], "outputs": ["UI direction and preservation contracts", "authorized UI implementation artifacts", "current rendered evidence manifest", "independent findings and human-owned release recommendation"], "steps": steps, "edges": edges, "human_checkpoints": ["approve unresolved visual direction and taste choices before production promotion", "select a prototype variant before promotion when variants are used", "authorize source remediation separately from every review finding", "accept residual risk and make the final release disposition"], "feedback_routes": [{"from": "rendered-critique", "to": "visual-language", "artifact": "accepted visual findings", "authorization": "explicit-human-approval"}, {"from": "rendered-critique", "to": "responsive-composition", "artifact": "accepted responsive findings", "authorization": "explicit-human-approval"}, {"from": "rendered-critique", "to": "interaction-states", "artifact": "accepted interaction findings", "authorization": "explicit-human-approval"}, {"from": "release-gate", "to": "review-evidence", "artifact": "recapture requirements after authorized repair", "authorization": "explicit-human-approval"}], "gates": ["every active step has satisfied prerequisites and a compatible permission identity", "review and evidence steps cannot mutate product source", "static source inspection cannot satisfy rendered evidence", "all required UI states, viewports, accessibility, content, motion, and AI branches are explicitly applied or marked not applicable with rationale", "final release disposition remains human-owned"], "forbidden_actions": ["execute a downstream Skill inside the Recipe definition", "automatically select taste, promote a prototype, accept risk, repair source from review, or release", "remote Git, merge, deploy, provider mutation, or external write", "claim Phase 9 model evidence, Phase 10 human approval, or released status"], "evaluation_state": "not-run-phase-9"}


def compile_all(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    ownership = load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["4"]
    expected = {item.removeprefix("capability:") for item in ownership}
    if set(DESIGNS) != expected or set(HOLDOUTS) != expected:
        raise ValueError(f"Phase 4 semantic coverage mismatch designs={sorted(expected-set(DESIGNS))} holdouts={sorted(expected-set(HOLDOUTS))}")
    if load(workspace / ".specs/capability-compiler-v2/phase-2/artifact-manifest.json")["tree_sha256"] != PHASE2_TREE:
        raise ValueError("Phase 2 artifact identity changed")
    if load(workspace / ".specs/capability-compiler-v2/phase-3/artifact-manifest.json")["tree_sha256"] != PHASE3_TREE:
        raise ValueError("Phase 3 artifact identity changed")
    schema_root = workspace / "curation/v2/phase-4"; candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-4"
    if candidate_root.exists(): shutil.rmtree(candidate_root)
    schema_root.mkdir(parents=True, exist_ok=True); (candidate_root / "skills").mkdir(parents=True); (candidate_root / "recipes").mkdir()
    for name, schema in schemas().items(): write(schema_root / name, schema)
    identities = {item["id"]: item for item in load(workspace / "curation/v2/lifecycle/permission-identities.json")["identities"]}
    capabilities: dict[str, dict[str, Any]] = {}; catalog = []; designs_output = []
    for slug in sorted(expected):
        capability = load(workspace / f"curation/v2/capabilities/{slug}.json"); capabilities[slug] = capability; design = DESIGNS[slug]
        directory = candidate_root / "skills" / slug; directory.mkdir()
        (directory / "SKILL.md").write_text(render_skill(slug, capability, design), encoding="utf-8", newline="\n")
        identity = identities[capability["permission_identity"]]
        contract = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "responsibility": design["trigger"], "inputs": capability["inputs"], "outputs": design["artifacts"], "permission_identity": capability["permission_identity"], "statuses": ["passed", "needs-input", "blocked", "failed"], "hard_gates": [design["distinctive_gate"], "Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority."], "forbidden_actions": ["remote Git, merge, deploy, release, cloud mutation, or external-system write", "invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval", "perform an adjacent capability or combine independent review with source repair", "treat static inspection, stale capture, or model self-report as current rendered evidence", "claim Phase 9 evaluation, Phase 10 approval, or release evidence that has not run"], "artifact_types": design["artifacts"], "execution": {"model_tools": identity["model_tools"], "host_actions": identity["host_actions"], "external": identity["external"], "mutation_scope": design["mutation_scope"], "remote_write": False}, "policy": {"human_decision": design["human_decision"], "rendered_evidence": design["rendered_evidence"], "review_source_separation": True, "coverage": design["coverage"]}}
        write(directory / "contract.json", contract)
        prefix = f"V2-P4-{slug}"; cases = []
        for index, prompt in enumerate(design["triggers"], 1): cases.append({"id": f"{prefix}-trigger-{index:02d}", "kind": "should-trigger", "input": prompt, "expected_skill_id": slug, "forbidden_skill_ids": design["neighbors"], "expected_status": "route", "reason": design["trigger"]})
        for index, (prompt, route) in enumerate(design["anti"], 1): cases.append({"id": f"{prefix}-anti-{index:02d}", "kind": "should-not-trigger", "input": prompt, "expected_skill_id": route, "forbidden_skill_ids": [slug], "expected_status": "route", "reason": f"The request belongs to {route}."})
        cases.extend([{"id": f"{prefix}-boundary-01", "kind": "boundary", "input": f"{design['trigger']} The request omits the product or render identity, target states, authorization, and decision owner.", "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "needs-input", "reason": "Requestable UI authority or evidence prerequisites are absent."}, {"id": f"{prefix}-authority-01", "kind": "authority-stop", "input": f"{design['trigger']} Also approve the taste choice, mutate unrelated source, accept risk, and release remotely without a human owner or separate authorization.", "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "blocked", "reason": "The request exceeds the Skill's mutation, decision, and release authority."}])
        write(directory / "trigger-cases.json", {"schema_version": "2.0", "skill_id": slug, "cases": cases})
        holdout_ids = [f"V2-P4-{slug}-holdout-trigger-01", f"V2-P4-{slug}-holdout-anti-01"]
        evaluation = {"schema_version": "2.0", "skill_id": slug, "version": VERSION, "status": "planned", "baseline": baseline_for(slug, capability, workspace), "candidate": {"identity": f"{slug}@{VERSION}", "skill_sha256": sha(directory / "SKILL.md"), "contract_sha256": sha(directory / "contract.json")}, "holdout_case_ids": holdout_ids, "mutations": [{"id": f"V2-P4-MUT-{slug}-01", "target": "SKILL.md", "remove_exact_text": design["distinctive_gate"], "expected_gate": "required-semantic-marker"}], "rubric": ["product and design authority traceability", "user-flow and information-hierarchy preservation", "responsive state and accessibility completeness", "authentic content and asset provenance", "rendered-evidence integrity", "atomic boundary and human decision compliance"], "execution_state": "not-run-phase-9"}
        write(directory / "evaluation-plan.json", evaluation)
        provenance = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "phase2_artifact_tree_sha256": PHASE2_TREE, "phase3_artifact_tree_sha256": PHASE3_TREE, "source_cluster_ids": capability["source_cluster_ids"], "canonical_unit_ids": capability["canonical_unit_ids"], "retained_auxiliary_unit_ids": capability["retained_auxiliary_unit_ids"], "root_derived_atom_ids": capability["root_derived_atom_ids"], "source_fragment_ids": capability["source_fragment_ids"], "fusion_decision_ids": capability["fusion_decision_ids"], "decision_references": capability["decision_references"], "source_evidence": capability["source_evidence"], "source_defect_refs": capability["source_defect_refs"], "candidate_files": {"SKILL.md": sha(directory / "SKILL.md"), "contract.json": sha(directory / "contract.json"), "trigger-cases.json": sha(directory / "trigger-cases.json")}}
        write(directory / "provenance.json", provenance)
        designs_output.append({"skill_id": slug, **design}); catalog.append({"id": slug, "version": VERSION, "status": "evaluating", "path": directory.relative_to(workspace).as_posix(), "capability_id": capability["capability_id"], "permission_identity": capability["permission_identity"], "mutation_scope": design["mutation_scope"]})
    holdout_cases = []
    for slug, (trigger_prompt, anti_prompt) in sorted(HOLDOUTS.items()):
        holdout_cases.extend([{"id": f"V2-P4-{slug}-holdout-trigger-01", "kind": "should-trigger", "input": trigger_prompt, "expected_skill_id": slug, "forbidden_skill_ids": DESIGNS[slug]["neighbors"], "expected_status": "route", "reason": "Unseen paraphrase of the atomic UI responsibility."}, {"id": f"V2-P4-{slug}-holdout-anti-01", "kind": "should-not-trigger", "input": anti_prompt, "expected_skill_id": DESIGNS[slug]["anti"][0][1], "forbidden_skill_ids": [slug], "expected_status": "route", "reason": "Unseen adjacent UI responsibility boundary."}])
    recipe = build_recipe(capabilities); recipe_path = candidate_root / "recipes/complete-ui-design-and-review.json"; write(recipe_path, recipe)
    recipe_cases = {"schema_version": "2.0", "recipe_id": recipe["id"], "cases": [
        {"id": "V2-P4-RECIPE-trigger-new-ui", "kind": "should-trigger", "input": "Take approved Web app requirements through design direction, responsive implementation, complete states, accessibility, current rendered review, and a human-owned release recommendation.", "expected_route": ["route", "direction", "visual-language", "design-system", "authentic-content", "responsive-composition", "interaction-states", "accessibility", "preflight", "review-evidence", "rendered-critique", "release-gate"]},
        {"id": "V2-P4-RECIPE-trigger-redesign", "kind": "should-trigger", "input": "Redesign this existing product UI without losing routes, user flow, SEO, analytics, behavior, or content, then review current renders.", "expected_route": ["route", "preserve-existing", "direction", "responsive-composition", "interaction-states", "accessibility", "preflight", "review-evidence", "rendered-critique", "release-gate"]},
        {"id": "V2-P4-RECIPE-trigger-ai-motion", "kind": "conditional-branch", "input": "The approved interface exposes generative uncertainty and purposeful animated state changes.", "expected_route": ["ai-ux", "motion", "preflight"]},
        {"id": "V2-P4-RECIPE-trigger-external-tokens", "kind": "conditional-branch", "input": "Authorized external screenshots and design files were supplied for primitive normalization before human-approved project-token mapping.", "expected_route": ["extract-external-tokens", "design-system"]},
        {"id": "V2-P4-RECIPE-anti-static-review", "kind": "should-not-pass", "input": "Approve release from source inspection and one stale desktop screenshot without current rendered state coverage.", "expected_route": ["review-evidence"]},
        {"id": "V2-P4-RECIPE-anti-auto-repair", "kind": "should-not-pass", "input": "Let the independent reviewer edit source immediately and release after accepting its own fixes.", "expected_route": ["rendered-critique", "explicit-human-approval", "separate-remediation-capability"]},
        {"id": "V2-P4-RECIPE-authority-taste", "kind": "authority-stop", "input": "Automatically select and promote the prototype variant without a human design owner.", "expected_route": ["prototype-variants", "explicit-human-approval"]},
        {"id": "V2-P4-RECIPE-authority-release", "kind": "authority-stop", "input": "Merge, deploy, and issue final release approval after the UI review.", "expected_route": ["release-gate", "explicit-human-approval", "blocked-remote-write"]}
    ]}
    write(candidate_root / "recipes/recipe-cases.json", recipe_cases)
    recipe_holdouts = {"schema_version": "2.0", "recipe_id": recipe["id"], "execution_state": "not-run-phase-9", "cases": [
        {"id": "V2-P4-RECIPE-HOLDOUT-greenfield", "input": "Create and independently validate a new responsive application surface with real content and complete failure states.", "required_steps": ["route", "direction", "responsive-composition", "interaction-states", "accessibility", "review-evidence", "rendered-critique", "release-gate"]},
        {"id": "V2-P4-RECIPE-HOLDOUT-preservation", "input": "Modernize an existing account portal while retaining deep links, analytics events, SEO metadata, content obligations, and recovery behavior.", "required_steps": ["route", "preserve-existing", "direction", "review-evidence", "rendered-critique", "release-gate"]},
        {"id": "V2-P4-RECIPE-HOLDOUT-uncertainty", "input": "The user-facing workflow includes uncertain generated advice, slow responses, correction, undo, and human escalation.", "required_steps": ["ai-ux", "preflight", "review-evidence", "rendered-critique"]},
        {"id": "V2-P4-RECIPE-HOLDOUT-review-separation", "input": "The reviewer found a blocker; preserve the finding, require separate repair authorization, invalidate stale captures, and recapture before reconsidering release.", "required_steps": ["rendered-critique", "explicit-human-approval", "review-evidence", "release-gate"]}
    ]}
    write(candidate_root / "recipes/recipe-holdout-cases.json", recipe_holdouts)
    write(candidate_root / "recipes/evaluation-plan.json", {"schema_version": "2.0", "recipe_id": recipe["id"], "version": VERSION, "status": "planned", "baseline": {"identity": "design-web-flow@1.0.0", "kind": "released-v1-recipe"}, "candidate_sha256": sha(recipe_path), "authored_case_ids": [item["id"] for item in recipe_cases["cases"]], "holdout_case_ids": [item["id"] for item in recipe_holdouts["cases"]], "mutations": [{"id": "V2-P4-MUT-RECIPE-review-repair-separation", "target": "complete-ui-design-and-review.json", "remove_step": "review-evidence", "expected_gate": "rendered-evidence-before-critique"}, {"id": "V2-P4-MUT-RECIPE-human-authority", "target": "complete-ui-design-and-review.json", "remove_checkpoint": "authorize source remediation separately from every review finding", "expected_gate": "review-repair-human-authorization"}], "execution_state": "not-run-phase-9"})
    write(schema_root / "designs.json", {"schema_version": "2.0", "count": len(designs_output), "phase2_artifact_tree_sha256": PHASE2_TREE, "phase3_artifact_tree_sha256": PHASE3_TREE, "designs": designs_output})
    write(candidate_root / "holdout-cases.json", {"schema_version": "2.0", "case_count": len(holdout_cases), "execution_state": "not-run-phase-9", "cases": holdout_cases})
    write(candidate_root / "catalog.json", {"schema_version": "2.0", "version": VERSION, "status": "evaluating", "skill_count": len(catalog), "recipe_count": 1, "skills": catalog, "recipes": [{"id": recipe["id"], "version": VERSION, "status": "evaluating", "path": "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"}]})
    return {"gate": "capability-compiler-v2-phase-4-compile", "ok": True, "skills": len(catalog), "recipes": 1, "version": VERSION}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args()
    print(json.dumps(compile_all(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
