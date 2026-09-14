#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


def cluster(
    responsibility: str,
    input_boundary: str,
    output_boundary: str,
    *,
    upstream: tuple[str, ...] = (),
    downstream: tuple[str, ...] = (),
) -> dict[str, object]:
    return {
        "candidate_responsibility": responsibility,
        "input_boundary": input_boundary,
        "output_boundary": output_boundary,
        "upstream_dependencies": list(upstream),
        "downstream_dependencies": list(downstream),
    }


CLUSTERS: dict[str, dict[str, object]] = {
    "cluster:context-intake-and-routing": cluster(
        "Deduplicate available context, identify missing inputs, and route work to the applicable capability.",
        "A request, existing artifacts, project context, and known constraints.",
        "A routing decision, explicit unknowns, applicable boundaries, and an invocation path.",
        downstream=(
            "cluster:market-positioning-and-competitive-power",
            "cluster:problem-framing-and-customer-research",
            "cluster:requirements-and-delivery-contract",
            "cluster:ui-task-routing-and-governance",
        ),
    ),
    "cluster:market-positioning-and-competitive-power": cluster(
        "Define target markets, positioning, alternatives, switching costs, structural power, and durable advantage.",
        "Market questions, customer alternatives, competitive evidence, and business constraints.",
        "A supported market choice, positioning, differentiation, power hypotheses, and competitive structure.",
        upstream=("cluster:context-intake-and-routing",),
        downstream=(
            "cluster:problem-framing-and-customer-research",
            "cluster:decision-and-outcome-roadmapping",
        ),
    ),
    "cluster:problem-framing-and-customer-research": cluster(
        "Frame customer problems and collect traceable, non-leading qualitative and quantitative evidence.",
        "A problem hypothesis, target users, prior research, access constraints, and a decision to support.",
        "A problem statement, research plan, behavioral evidence, personas or jobs, and evidence gaps.",
        upstream=(
            "cluster:context-intake-and-routing",
            "cluster:market-positioning-and-competitive-power",
        ),
        downstream=(
            "cluster:evidence-synthesis-and-opportunity-prioritization",
            "cluster:solution-hypothesis-and-experiment-design",
        ),
    ),
    "cluster:evidence-synthesis-and-opportunity-prioritization": cluster(
        "Synthesize multi-source evidence into patterns and rank opportunities with methods suited to the data.",
        "Research notes, behavior data, support signals, competitive evidence, and candidate opportunities.",
        "Themes, evidence strength, opportunity scores, priorities, rationale, and uncertainty.",
        upstream=("cluster:problem-framing-and-customer-research",),
        downstream=(
            "cluster:solution-hypothesis-and-experiment-design",
            "cluster:decision-and-outcome-roadmapping",
        ),
    ),
    "cluster:solution-hypothesis-and-experiment-design": cluster(
        "Generate distinguishable solution hypotheses and design experiments that maximize learning at minimum cost.",
        "A framed problem, prioritized opportunity, assumptions, risks, and available experiment conditions.",
        "Solution options, falsifiable hypotheses, experiment protocols, preregistered criteria, and limitations.",
        upstream=(
            "cluster:problem-framing-and-customer-research",
            "cluster:evidence-synthesis-and-opportunity-prioritization",
        ),
        downstream=(
            "cluster:results-analysis-and-decision-readout",
            "cluster:requirements-and-delivery-contract",
        ),
    ),
    "cluster:decision-and-outcome-roadmapping": cluster(
        "Make evidence-backed choices and sequence measurable outcomes, dependencies, and capacity constraints.",
        "Strategy, candidate initiatives, experiment conclusions, priorities, capacity, and dependencies.",
        "A go, pivot, or kill decision; an outcome roadmap; sequencing; and a decision record.",
        upstream=(
            "cluster:market-positioning-and-competitive-power",
            "cluster:evidence-synthesis-and-opportunity-prioritization",
            "cluster:results-analysis-and-decision-readout",
        ),
        downstream=("cluster:requirements-and-delivery-contract",),
    ),
    "cluster:requirements-and-delivery-contract": cluster(
        "Turn validated strategy, problems, and solutions into evolvable requirements and acceptance contracts.",
        "Problem and solution evidence, target users, strategy, metrics, risks, and delivery constraints.",
        "A PRD, stories, acceptance criteria, scope, open questions, dependencies, and change history.",
        upstream=(
            "cluster:solution-hypothesis-and-experiment-design",
            "cluster:decision-and-outcome-roadmapping",
            "cluster:results-analysis-and-decision-readout",
        ),
        downstream=(
            "cluster:risk-preflight-and-safety-governance",
            "cluster:metrics-system-and-observability",
            "cluster:implementation-planning-and-handoff",
        ),
    ),
    "cluster:risk-preflight-and-safety-governance": cluster(
        "Identify failure modes, hard gates, safety boundaries, mitigations, owners, and stop conditions before commitment.",
        "Requirements, a solution, release plans, dependencies, permissions, and high-consequence assumptions.",
        "Risks, owners, triggers, mitigations, hard gates, kill criteria, and residual risk.",
        upstream=(
            "cluster:requirements-and-delivery-contract",
            "cluster:ai-capability-architecture-and-autonomy",
        ),
        downstream=("cluster:results-analysis-and-decision-readout",),
    ),
    "cluster:metrics-system-and-observability": cluster(
        "Define outcome, input, secondary, and guardrail metrics with baselines, instrumentation, dashboards, and alerts.",
        "Business goals, user outcomes, risks, data sources, and observable events.",
        "A metric hierarchy, definitions, instrumentation plan, dashboard, alerts, and review cadence.",
        upstream=(
            "cluster:requirements-and-delivery-contract",
            "cluster:solution-hypothesis-and-experiment-design",
        ),
        downstream=(
            "cluster:results-analysis-and-decision-readout",
            "cluster:feedback-and-continuous-learning-loop",
        ),
    ),
    "cluster:results-analysis-and-decision-readout": cluster(
        "Interpret results against preset criteria and communicate evidence, limits, disagreements, and recommendations.",
        "Experiment or research data, metrics, baselines, bias checks, and decision criteria.",
        "An analysis, go/pivot/kill recommendation, stakeholder readout, limitations, and next steps.",
        upstream=(
            "cluster:solution-hypothesis-and-experiment-design",
            "cluster:metrics-system-and-observability",
        ),
        downstream=(
            "cluster:decision-and-outcome-roadmapping",
            "cluster:requirements-and-delivery-contract",
            "cluster:feedback-and-continuous-learning-loop",
        ),
    ),
    "cluster:feedback-and-continuous-learning-loop": cluster(
        "Maintain customer contact, feedback synthesis, metric review, calibration, and the next learning cycle.",
        "Runtime metrics, customer feedback, experiment results, alerts, and residual assumptions.",
        "A review cadence, learning record, calibrated hypotheses, priorities, and the next discovery input.",
        upstream=(
            "cluster:metrics-system-and-observability",
            "cluster:results-analysis-and-decision-readout",
        ),
        downstream=(
            "cluster:problem-framing-and-customer-research",
            "cluster:ai-capability-architecture-and-autonomy",
        ),
    ),
    "cluster:ai-capability-architecture-and-autonomy": cluster(
        "Route an AI opportunity to the appropriate architecture, autonomy, interaction, and safety capability without reimplementing those specialist contracts.",
        "A customer problem, AI opportunity thesis, quality target, cost constraint, and capability-selection question.",
        "A bounded AI architecture choice, specialist handoff map, and explicit unresolved capability risks.",
        upstream=(
            "cluster:market-positioning-and-competitive-power",
            "cluster:feedback-and-continuous-learning-loop",
        ),
        downstream=(
            "cluster:ai-model-and-data-architecture",
            "cluster:ai-agent-autonomy-and-human-control",
            "cluster:ai-interaction-and-probabilistic-ux",
            "cluster:ai-safety-and-action-governance",
        ),
    ),
    "cluster:ui-task-routing-and-governance": cluster(
        "Classify UI work and establish the applicable playbook, authorization, target files, and write boundaries.",
        "A UI request, project state, existing interface, target files, authorization, and design artifacts.",
        "A task route, required references, execution mode, tool plan, and boundary statement.",
        upstream=("cluster:context-intake-and-routing",),
        downstream=(
            "cluster:design-context-and-direction-contract",
            "cluster:existing-interface-redesign-and-preservation",
        ),
    ),
    "cluster:design-context-and-direction-contract": cluster(
        "Read product and visual authority and define the audience, surface mode, direction, and design contract.",
        "Product facts, a brief, design assets, tokens, components, surface context, and references.",
        "A design read, selected direction, constraints, spatial thesis, and auditable direction contract.",
        upstream=(
            "cluster:ui-task-routing-and-governance",
            "cluster:existing-interface-redesign-and-preservation",
        ),
        downstream=(
            "cluster:design-system-foundation-and-token-extraction",
            "cluster:visual-language-and-anti-template-controls",
            "cluster:divergent-prototyping-and-variant-selection",
        ),
    ),
    "cluster:design-system-foundation-and-token-extraction": cluster(
        "Choose or generate an in-project design-system foundation, including component rules, theme decisions, and persistence policy.",
        "A UI brief, stack, design references, existing tokens, and project conventions.",
        "A selected or generated system foundation, component rules, theme decisions, and persistence contract.",
        upstream=("cluster:design-context-and-direction-contract",),
        downstream=(
            "cluster:visual-language-and-anti-template-controls",
            "cluster:responsive-layout-and-spatial-composition",
            "cluster:frontend-runtime-boundaries-and-dependency-safety",
        ),
    ),
    "cluster:visual-language-and-anti-template-controls": cluster(
        "Establish a distinctive visual language and suppress generic template patterns and unsupported decoration.",
        "A direction contract, brand, tokens, audience, surface mode, and content.",
        "Typography, color, material, composition, style decisions, and anti-template constraints.",
        upstream=(
            "cluster:design-context-and-direction-contract",
            "cluster:design-system-foundation-and-token-extraction",
        ),
        downstream=(
            "cluster:responsive-layout-and-spatial-composition",
            "cluster:content-copy-and-authentic-assets",
        ),
    ),
    "cluster:responsive-layout-and-spatial-composition": cluster(
        "Design layout, hierarchy, density, grids, reflow, and content rhythm across supported viewports.",
        "A visual direction, content structure, device classes, breakpoints, and existing layout constraints.",
        "Desktop and mobile composition, responsive rules, spatial hierarchy, and reflow behavior.",
        upstream=(
            "cluster:design-system-foundation-and-token-extraction",
            "cluster:visual-language-and-anti-template-controls",
        ),
        downstream=(
            "cluster:interaction-states-forms-and-navigation",
            "cluster:evidence-based-ui-review-and-release-gates",
        ),
    ),
    "cluster:content-copy-and-authentic-assets": cluster(
        "Create truthful, comprehensible product copy, content data, and assets with explicit provenance.",
        "Product facts, brand voice, content needs, licensed material, and asset-generation capability.",
        "Publishable copy, authentic or traceable assets, alt text, and explicit placeholders where unavoidable.",
        upstream=("cluster:visual-language-and-anti-template-controls",),
        downstream=(
            "cluster:interaction-states-forms-and-navigation",
            "cluster:evidence-based-ui-review-and-release-gates",
        ),
    ),
    "cluster:interaction-states-forms-and-navigation": cluster(
        "Define and implement controls, navigation, forms, loading, empty, error, disabled, and recovery states.",
        "User flows, acceptance criteria, a component system, content, state model, and platform behavior.",
        "Complete interaction states, recovery behavior, navigation, focus paths, and state feedback.",
        upstream=(
            "cluster:responsive-layout-and-spatial-composition",
            "cluster:content-copy-and-authentic-assets",
        ),
        downstream=(
            "cluster:accessibility-contracts-and-assistive-validation",
            "cluster:purposeful-motion-and-animation-engineering",
        ),
    ),
    "cluster:accessibility-contracts-and-assistive-validation": cluster(
        "Define semantic, keyboard, focus, assistive-technology, visual-input, and error-recovery contracts.",
        "User tasks, supported browser and assistive technology, interaction states, WCAG scope, and an implementation.",
        "Accessibility acceptance criteria, semantics, focus behavior, a test matrix, evidence, and residual risk.",
        upstream=("cluster:interaction-states-forms-and-navigation",),
        downstream=("cluster:evidence-based-ui-review-and-release-gates",),
    ),
    "cluster:purposeful-motion-and-animation-engineering": cluster(
        "Use motion for hierarchy, narrative, feedback, and state while controlling timing, interruption, and reduction.",
        "Interaction states, motion intent, frequency, platform capability, and accessibility constraints.",
        "A motion specification, implementation pattern, reduced-motion fallback, and performance boundary.",
        upstream=("cluster:interaction-states-forms-and-navigation",),
        downstream=(
            "cluster:frontend-rendering-and-interaction-performance",
            "cluster:evidence-based-ui-review-and-release-gates",
        ),
    ),
    "cluster:divergent-prototyping-and-variant-selection": cluster(
        "Build genuinely different working UI variants in isolation and support fair comparison and promotion.",
        "One UI brief, project tokens, authentic context, and named axes of divergence.",
        "Isolated variants, a picker, tradeoffs, a user selection, and a promotion handoff.",
        upstream=("cluster:design-context-and-direction-contract",),
        downstream=(
            "cluster:existing-interface-redesign-and-preservation",
            "cluster:evidence-based-ui-review-and-release-gates",
        ),
    ),
    "cluster:existing-interface-redesign-and-preservation": cluster(
        "Audit an existing interface and preserve product truth, information architecture, SEO, analytics, and behavior.",
        "An existing UI, brand, tokens, information architecture, content, routes, analytics, and redesign brief.",
        "A current-state audit, preservation contract, redesign scope, migration order, and risks.",
        upstream=(
            "cluster:ui-task-routing-and-governance",
            "cluster:divergent-prototyping-and-variant-selection",
        ),
        downstream=(
            "cluster:design-context-and-direction-contract",
            "cluster:evidence-based-ui-review-and-release-gates",
        ),
    ),
    "cluster:evidence-based-ui-review-and-release-gates": cluster(
        "Review real renders against explicit criteria and issue evidence-bounded findings and release dispositions.",
        "An implementation, desktop and mobile captures, a brief, direction contract, target files, and findings.",
        "Prioritized findings, fix or rebuild dispositions, recapture evidence, a verdict, and residual risk.",
        upstream=(
            "cluster:responsive-layout-and-spatial-composition",
            "cluster:accessibility-contracts-and-assistive-validation",
            "cluster:purposeful-motion-and-animation-engineering",
            "cluster:frontend-rendering-and-interaction-performance",
        ),
    ),
    "cluster:architecture-deep-module-design": cluster(
        "Design module boundaries and interfaces using information hiding, deep modules, seams, and dependency direction.",
        "A module, its interfaces and dependencies, or evidenced architectural friction.",
        "Module boundaries, interface contracts, seams, dependency direction, and testability decisions.",
        upstream=("cluster:architecture-deepening-discovery",),
        downstream=(
            "cluster:architecture-interface-alternative-evaluation",
            "cluster:implementation-planning-and-handoff",
        ),
    ),
    "cluster:architecture-deepening-discovery": cluster(
        "Find shallow modules, leaked boundaries, repeated orchestration, and other evidence-backed deepening candidates.",
        "A codebase, change hotspots, repeated logic, and maintenance-friction evidence.",
        "Scoped architectural candidates, evidence, and a YAGNI-aware recommendation to deepen or leave unchanged.",
        downstream=(
            "cluster:architecture-candidate-reporting",
            "cluster:architecture-deep-module-design",
        ),
    ),
    "cluster:architecture-candidate-reporting": cluster(
        "Present architecture candidates as comparable cards, diagrams, rankings, and recommendations.",
        "Already discovered architecture candidates with code evidence.",
        "A visual candidate report and comparison material, not an implementation.",
        upstream=("cluster:architecture-deepening-discovery",),
        downstream=(
            "cluster:architecture-interface-alternative-evaluation",
            "cluster:implementation-planning-and-handoff",
        ),
    ),
    "cluster:architecture-interface-alternative-evaluation": cluster(
        "Generate independent interface alternatives and compare hiding, complexity, dependencies, tests, and migration cost.",
        "A bounded module problem, constraints, and an interface-design objective.",
        "At least two structured alternatives, tradeoffs, and a recommendation, not execution.",
        upstream=(
            "cluster:architecture-deep-module-design",
            "cluster:architecture-candidate-reporting",
        ),
        downstream=("cluster:implementation-planning-and-handoff",),
    ),
    "cluster:implementation-planning-and-handoff": cluster(
        "Convert specifications and architecture decisions into file-specific, test-first, executable micro-steps.",
        "A confirmed specification, architecture boundaries, repository conventions, and test requirements.",
        "A placeholder-free implementation plan with exact files, commands, expected results, and an execution handoff.",
        upstream=(
            "cluster:requirements-and-delivery-contract",
            "cluster:architecture-deep-module-design",
            "cluster:architecture-interface-alternative-evaluation",
            "cluster:engineering-retrospective-and-improvement",
        ),
        downstream=(
            "cluster:plan-execution-control",
            "cluster:subagent-task-pipeline",
            "cluster:tdd-change-loop",
        ),
    ),
    "cluster:plan-execution-control": cluster(
        "Load and review a plan, execute task states with checkpoints, stop on blockers, and hand off branch completion.",
        "An executable implementation plan and an isolated work environment.",
        "Plan-aligned implementation status with task-level verification and explicit blockers.",
        upstream=("cluster:implementation-planning-and-handoff",),
        downstream=(
            "cluster:independent-code-review",
            "cluster:completion-evidence-gate",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:subagent-task-pipeline": cluster(
        "Dispatch plan tasks to isolated implementers and sequence status, specification review, and quality review.",
        "A complete plan, one task context, and an authorized edit scope.",
        "Per-task implementations, structured status, review flow, and resolved blockers.",
        upstream=("cluster:implementation-planning-and-handoff",),
        downstream=(
            "cluster:developer-self-check-and-fix",
            "cluster:independent-code-review",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:developer-self-check-and-fix": cluster(
        "Have the implementer inspect specification coverage, quality, scope, and test truth, then fix discovered issues.",
        "Implemented code, its task specification, test output, and change list.",
        "A corrected implementation and structured self-review evidence, not an independent verdict.",
        upstream=("cluster:subagent-task-pipeline",),
        downstream=(
            "cluster:independent-code-review",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:git-destructive-command-guard": cluster(
        "Intercept destructive Git commands before execution and provide a configurable, verifiable local guardrail.",
        "A command hook environment, dangerous-command policy, and local configuration.",
        "An installed and tested command guard; normal release packaging remains out of scope.",
        downstream=(
            "cluster:change-packaging-and-versioning",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:tdd-change-loop": cluster(
        "Drive behavior changes through a real red-green-refactor loop and a final fresh verification.",
        "A feature, defect, refactor, or other behavior change.",
        "Minimal code supported by observed RED, GREEN, cleanup, and completion evidence.",
        upstream=("cluster:implementation-planning-and-handoff",),
        downstream=(
            "cluster:developer-self-check-and-fix",
            "cluster:independent-code-review",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:test-double-discipline": cluster(
        "Constrain mocks, spies, and test-only interfaces so tests exercise meaningful behavior and complete data shapes.",
        "A test design that requires dependency isolation or an existing test double.",
        "A minimal, behavior-focused test-double strategy that does not pollute production APIs.",
        upstream=(
            "cluster:tdd-change-loop",
            "cluster:testing-portfolio-strategy",
        ),
        downstream=(
            "cluster:vitest-tooling",
            "cluster:playwright-test-engineering",
        ),
    ),
    "cluster:testing-portfolio-strategy": cluster(
        "Design a layered test portfolio from business risk, feedback speed, maintenance cost, and component type.",
        "System architecture, risks, component types, environments, and data constraints.",
        "A test pyramid, coverage priorities, skip boundaries, and an executable test plan.",
        downstream=(
            "cluster:tdd-change-loop",
            "cluster:vitest-tooling",
            "cluster:playwright-test-engineering",
            "cluster:independent-blackbox-qa",
        ),
    ),
    "cluster:vitest-tooling": cluster(
        "Apply Vitest configuration, workers, fixtures, mocks, timers, snapshots, type tests, coverage, and CLI controls.",
        "A JavaScript or TypeScript unit or integration test project using Vitest.",
        "Runnable Vitest tests and configuration, not the cross-layer portfolio strategy.",
        upstream=(
            "cluster:testing-portfolio-strategy",
            "cluster:test-double-discipline",
        ),
        downstream=("cluster:completion-evidence-gate",),
    ),
    "cluster:root-cause-investigation": cluster(
        "Reproduce failures, trace data to its source, compare working patterns, form one hypothesis, and test it minimally.",
        "A test failure, production incident, unexpected behavior, build issue, or performance problem.",
        "An evidence-backed root cause and a bounded correction path, never a symptom-only guess.",
        downstream=(
            "cluster:tdd-change-loop",
            "cluster:resilience-and-determinism",
            "cluster:incident-response-coordination",
        ),
    ),
    "cluster:resilience-and-determinism": cluster(
        "Use layered defenses, condition waits, isolated fixtures, stable assertions, and controlled time to prevent flakiness.",
        "A confirmed cause involving invalid data, races, environment contamination, fragile waits, or flaky tests.",
        "Defensive validation, deterministic synchronization, and isolation mechanisms.",
        upstream=("cluster:root-cause-investigation",),
        downstream=(
            "cluster:playwright-test-engineering",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:independent-code-review": cluster(
        "Independently compare specifications and diffs for correctness, security, performance, architecture, tests, and maintainability.",
        "A specification, change description, and precise code-diff boundary.",
        "Prioritized findings with locations, rationale, remediation, and a merge verdict; no direct repair by default.",
        upstream=(
            "cluster:plan-execution-control",
            "cluster:subagent-task-pipeline",
            "cluster:developer-self-check-and-fix",
        ),
        downstream=(
            "cluster:completion-evidence-gate",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:completion-evidence-gate": cluster(
        "Require a fresh complete command, output inspection, and exit-code check before any success or completion claim.",
        "A proposed status claim and the command capable of proving it.",
        "An evidence-supported conclusion or an explicit failure, never confidence or delegated self-report.",
        upstream=(
            "cluster:tdd-change-loop",
            "cluster:vitest-tooling",
            "cluster:playwright-test-engineering",
            "cluster:independent-code-review",
        ),
        downstream=(
            "cluster:change-packaging-and-versioning",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:tool-runtime-readiness": cluster(
        "Validate that a requested browser, audit, or test tool is available and its invocation boundary is safe before setup.",
        "A tool request, project path, shell environment, and declared prerequisite contract.",
        "A prerequisite verdict, supported wrapper boundary, or explicit unavailable-tool failure.",
        downstream=(
            "cluster:browser-session-and-runtime-configuration",
            "cluster:safe-browser-probing",
            "cluster:playwright-test-engineering",
            "cluster:website-audit-remediation",
        ),
    ),
    "cluster:safe-browser-probing": cluster(
        "Use constrained browser sessions for navigation, snapshots, interaction, tracing, and extraction with safe references.",
        "A target page, authorized interactions, and a ready browser runtime.",
        "Browser observations, screenshots, snapshots, traces, and interaction evidence, not an independent QA verdict.",
        upstream=("cluster:tool-runtime-readiness",),
        downstream=(
            "cluster:independent-blackbox-qa",
            "cluster:playwright-test-engineering",
            "cluster:production-canary-monitoring",
        ),
    ),
    "cluster:independent-blackbox-qa": cluster(
        "Run diff-aware, quick, or regression black-box QA without modifying product source.",
        "An accessible application, change scope, QA mode, and authorized interaction boundary.",
        "Report-only defects, screenshots, console evidence, and a health score; never a product-code repair.",
        upstream=(
            "cluster:testing-portfolio-strategy",
            "cluster:safe-browser-probing",
        ),
        downstream=(
            "cluster:completion-evidence-gate",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:playwright-test-engineering": cluster(
        "Engineer maintainable Playwright browser, API, visual, accessibility, security, and collaboration tests.",
        "Browser behaviors, test environments, risks, data, and automation acceptance goals.",
        "Isolated Playwright tests, fixtures, locators, assertions, authentication, CI, and flake controls.",
        upstream=(
            "cluster:testing-portfolio-strategy",
            "cluster:tool-runtime-readiness",
            "cluster:safe-browser-probing",
            "cluster:resilience-and-determinism",
        ),
        downstream=(
            "cluster:baseline-regression-control",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:website-audit-remediation": cluster(
        "Run broad website audits, map SEO, performance, security, content, and accessibility findings to source, and recheck fixes.",
        "A scannable site, audit CLI, and an authorized source-edit scope.",
        "A categorized report, remediation loop, score targets, and fresh audit evidence.",
        upstream=("cluster:tool-runtime-readiness",),
        downstream=(
            "cluster:baseline-regression-control",
            "cluster:completion-evidence-gate",
        ),
    ),
    "cluster:web-performance-diagnostics": cluster(
        "Measure web vitals, network behavior, and build output to identify bottlenecks and sustained optimizations.",
        "A web application, controlled sampling environment, network waterfall, and build information.",
        "Performance metrics, bottleneck evidence, recommendations, budgets, and an audit report.",
        upstream=(
            "cluster:tool-runtime-readiness",
            "cluster:safe-browser-probing",
        ),
        downstream=(
            "cluster:baseline-regression-control",
            "cluster:merge-and-deploy-readiness",
        ),
    ),
    "cluster:baseline-regression-control": cluster(
        "Compare current audit, visual, performance, model, or production measures with trusted baselines and control updates.",
        "A trusted historical baseline and a current measurement made under the same contract.",
        "A diff, regression decision, and controlled baseline-update decision.",
        upstream=(
            "cluster:playwright-test-engineering",
            "cluster:website-audit-remediation",
            "cluster:web-performance-diagnostics",
            "cluster:llm-quality-evaluation",
        ),
        downstream=(
            "cluster:merge-and-deploy-readiness",
            "cluster:production-canary-monitoring",
        ),
    ),
    "cluster:change-packaging-and-versioning": cluster(
        "Package verified changes into bisectable commits, coherent versions, changelogs, credential checks, and PR metadata.",
        "Implemented and reviewed changes with fresh verification evidence.",
        "A safe, traceable, version-consistent change package and pull-request description.",
        upstream=(
            "cluster:completion-evidence-gate",
            "cluster:git-destructive-command-guard",
        ),
        downstream=("cluster:merge-and-deploy-readiness",),
    ),
    "cluster:merge-and-deploy-readiness": cluster(
        "Check branch, authentication, pull-request state, conflicts, CI, version drift, and deployment dry runs.",
        "A pull request, target branch, CI state, version state, and deployment configuration.",
        "A merge/deploy authorization or explicit blockers; post-deploy observation remains downstream.",
        upstream=(
            "cluster:change-packaging-and-versioning",
            "cluster:independent-code-review",
            "cluster:completion-evidence-gate",
        ),
        downstream=(
            "cluster:deployment-observation-and-recovery",
            "cluster:production-canary-monitoring",
        ),
    ),
    "cluster:deployment-observation-and-recovery": cluster(
        "Observe deployment providers, assess post-deploy health, and produce auditable rollback or revert recovery changes.",
        "A merged change, provider status, and post-deploy health signals.",
        "Deployment evidence, a failure decision, or a reviewable rollback and recovery pull request.",
        upstream=("cluster:merge-and-deploy-readiness",),
        downstream=(
            "cluster:production-canary-monitoring",
            "cluster:incident-response-coordination",
        ),
    ),
    "cluster:production-canary-monitoring": cluster(
        "Capture a production baseline, discover safe pages, sample continuously, diff signals, and control alert noise.",
        "A deployed application, safely accessible pages, and a trusted initial baseline.",
        "Ongoing health status, differential alerts, evidence, and controlled baseline updates.",
        upstream=(
            "cluster:deployment-observation-and-recovery",
            "cluster:baseline-regression-control",
            "cluster:safe-browser-probing",
        ),
        downstream=("cluster:incident-response-coordination",),
    ),
    "cluster:incident-response-coordination": cluster(
        "Coordinate incident acknowledgement, severity, roles, mitigation-first action, communication, recovery, and closure.",
        "An active production anomaly, impact evidence, alerts, and available mitigation controls.",
        "A structured response, mitigation, communications, escalation, recovery evidence, and closure record.",
        upstream=(
            "cluster:production-canary-monitoring",
            "cluster:deployment-observation-and-recovery",
        ),
        downstream=(
            "cluster:root-cause-investigation",
            "cluster:engineering-retrospective-and-improvement",
        ),
    ),
    "cluster:llm-quality-evaluation": cluster(
        "Evaluate language models with automated metrics, factuality checks, judges, human agreement, statistics, and regressions.",
        "Model outputs, references, criteria, annotations, and trusted historical baselines.",
        "Repeatable scores, grounded quality judgments, statistical confidence, benchmarks, and regression signals.",
        upstream=("cluster:data-analysis-validation",),
        downstream=(
            "cluster:baseline-regression-control",
            "cluster:engineering-retrospective-and-improvement",
        ),
    ),
    "cluster:data-analysis-validation": cluster(
        "Validate metrics, feedback, and experiment analysis for method, representation, aggregation, bias, and reproducibility.",
        "Product metrics, feedback, queries, an experiment design, or experiment results.",
        "Method-checked insights, experiment designs or readouts, limitations, and actionable recommendations.",
        downstream=(
            "cluster:llm-quality-evaluation",
            "cluster:engineering-retrospective-and-improvement",
        ),
    ),
    "cluster:engineering-retrospective-and-improvement": cluster(
        "Review engineering delivery from fresh repository history, test health, plan completion, and team evidence.",
        "A time window, Git history, test health, plan state, delivery outcomes, and prior retrospectives.",
        "Individual and team feedback, technical-debt signals, trends, and tracked improvement actions.",
        upstream=(
            "cluster:incident-response-coordination",
            "cluster:data-analysis-validation",
            "cluster:llm-quality-evaluation",
        ),
        downstream=(
            "cluster:implementation-planning-and-handoff",
            "cluster:testing-portfolio-strategy",
        ),
    ),
}

CLUSTERS.update({
    "cluster:source-metadata-and-provenance": cluster(
        "Preserve source identity, revision context, licensing or provenance facts, and the boundary between evidence and interpretation.",
        "A curated unit, source declaration, citation context, or provenance concern.",
        "Traceable source metadata and explicit evidence-status limits.",
        downstream=("cluster:reference-library-and-deferred-material",),
    ),
    "cluster:reference-library-and-deferred-material": cluster(
        "Retain references, historical material, and deferred frameworks without presenting them as current operational guidance.",
        "A source reference, historical claim, external framework, or material outside the active execution path.",
        "A bounded reference or deferral record with applicability and freshness limits.",
        upstream=("cluster:source-metadata-and-provenance",),
    ),
    "cluster:artifact-persistence-and-tool-actions": cluster(
        "Select authorized tools and persist the resulting specification or artifact at the correct lifecycle point.",
        "A validated task, tool boundary, output location, and write authorization.",
        "A tool action, saved artifact, or explicit no-write outcome.",
        upstream=("cluster:workflow-orchestration-and-lifecycle",),
    ),
    "cluster:workflow-orchestration-and-lifecycle": cluster(
        "Sequence a capability workflow, route sub-capabilities, and preserve lifecycle state without performing the downstream work itself.",
        "A request, phase state, available capabilities, and execution constraints.",
        "An ordered workflow, routing decision, handoff state, and stop or retry condition.",
        downstream=("cluster:facilitation-and-collaboration-protocols",),
    ),
    "cluster:facilitation-and-collaboration-protocols": cluster(
        "Run explicit collaboration, participation, clarification, and decision protocols across roles.",
        "A multi-role task, incomplete context, stakeholder set, and decision boundary.",
        "Facilitated inputs, aligned decisions, unresolved questions, and ownership.",
        upstream=("cluster:workflow-orchestration-and-lifecycle",),
    ),
    "cluster:document-and-artifact-governance": cluster(
        "Define durable document structure, artifact fields, authorship rules, and output comprehension checks.",
        "A document or artifact purpose, audience, source evidence, and required fields.",
        "A governed artifact contract, readable output, and explicit unknowns.",
        upstream=("cluster:source-metadata-and-provenance",),
        downstream=("cluster:requirements-and-delivery-contract",),
    ),
    "cluster:market-segmentation-and-demand-intelligence": cluster(
        "Identify demand-side alternatives, market segments, incumbent signals, and the customer situations that define competition.",
        "Customer situations, alternatives, segment constraints, incumbent observations, and market evidence.",
        "A demand-side map, segment choice, market signal interpretation, and evidence gaps.",
        upstream=("cluster:market-positioning-and-competitive-power",),
        downstream=("cluster:problem-framing-and-customer-research",),
    ),
    "cluster:structural-power-and-moats": cluster(
        "Test whether advantage comes from durable structural mechanisms, switching costs, operational asymmetry, or business rules rather than surface features.",
        "A proposed advantage, customer evidence, cost structure, workflow, and imitation scenario.",
        "A mechanism-backed moat hypothesis, imitation limits, and residual vulnerability.",
        upstream=("cluster:market-segmentation-and-demand-intelligence",),
        downstream=("cluster:decision-and-outcome-roadmapping",),
    ),
    "cluster:ai-product-opportunity-and-wedge": cluster(
        "Identify an AI product wedge, defensible application layer, and model-curve-aware opportunity before committing to architecture.",
        "A validated customer problem, workflow friction, model trajectory, data advantage, and business constraint.",
        "An AI opportunity thesis, wedge choice, defensibility hypothesis, and feasibility questions.",
        upstream=("cluster:market-positioning-and-competitive-power",),
        downstream=("cluster:ai-capability-architecture-and-autonomy",),
    ),
    "cluster:strategic-choice-and-differentiation": cluster(
        "Choose a coherent competitive position and differentiation axis, then test whether the choice is operationally supportable.",
        "A market position, baseline utility, cost structure, strategic strength, and candidate differentiation.",
        "A chosen strategic position, differentiation thesis, tradeoffs, and validation criteria.",
        upstream=("cluster:market-segmentation-and-demand-intelligence",),
        downstream=("cluster:structural-power-and-moats", "cluster:decision-and-outcome-roadmapping"),
    ),
    "cluster:competitive-case-library": cluster(
        "Use bounded competitive cases and historical examples to generate hypotheses without treating examples as current evidence.",
        "A competitive question, case material, historical context, and applicability boundary.",
        "A case-backed hypothesis, analogy limits, and follow-up evidence requirements.",
        upstream=("cluster:source-metadata-and-provenance",),
        downstream=("cluster:strategic-choice-and-differentiation",),
    ),
    "cluster:competitive-response-and-monitoring": cluster(
        "Monitor competitors and platform shifts, analyze response options, and keep competitive claims tied to verifiable observations.",
        "Competitor releases, market signals, comparable products, and monitoring evidence.",
        "A verified competitive intelligence brief, response choice, and follow-up observation plan.",
        upstream=("cluster:market-segmentation-and-demand-intelligence",),
        downstream=("cluster:decision-and-outcome-roadmapping",),
    ),
    "cluster:research-planning-and-governance": cluster(
        "Define research context, recruitment, consent, cadence, saturation, and phase handoffs before collecting evidence.",
        "A research question, target population, access constraints, ethical boundary, and timebox.",
        "A governed research plan, participant protocol, saturation decision, and phase handoff.",
        upstream=("cluster:problem-framing-and-customer-research",),
        downstream=("cluster:customer-interview-execution",),
    ),
    "cluster:customer-interview-execution": cluster(
        "Prepare and conduct non-leading customer interviews with context, probes, notes, and evidence-preserving closure.",
        "A research objective, participant context, consent boundary, and interview script.",
        "Interview evidence, direct observations, notes, and explicit follow-up gaps.",
        upstream=("cluster:research-planning-and-governance",),
        downstream=("cluster:qualitative-evidence-synthesis",),
    ),
    "cluster:persona-jtbd-and-journey-modeling": cluster(
        "Model users, jobs, pain points, and cross-touchpoint journeys without upgrading hypotheses into facts.",
        "Interview evidence, behavioral context, user hypotheses, and touchpoint observations.",
        "Traceable personas, jobs, journey maps, problem statements, and validation needs.",
        upstream=("cluster:customer-interview-execution",),
        downstream=("cluster:qualitative-evidence-synthesis",),
    ),
    "cluster:qualitative-evidence-synthesis": cluster(
        "Synthesize qualitative evidence into patterns, contradictions, pain priorities, and updated problem statements.",
        "Interview notes, direct quotes, affinity material, journey evidence, and known bias.",
        "Evidence-backed themes, counterexamples, prioritized pains, and uncertainty.",
        upstream=("cluster:customer-interview-execution", "cluster:persona-jtbd-and-journey-modeling"),
        downstream=("cluster:opportunity-prioritization-and-frameworks",),
    ),
    "cluster:opportunity-prioritization-and-frameworks": cluster(
        "Select and apply an appropriate prioritization method, score opportunities, and preserve the assumptions behind ranking.",
        "Validated problems, opportunities, evidence strength, constraints, and decision criteria.",
        "A ranked opportunity set, selected framework, scores, rationale, and uncertainty.",
        upstream=("cluster:qualitative-evidence-synthesis",),
        downstream=("cluster:solution-hypothesis-and-experiment-design",),
    ),
    "cluster:ai-model-and-data-architecture": cluster(
        "Choose model routing, data sizing and freshness, retrieval preparation, prompt implementation, and evaluation boundaries.",
        "An AI task, data sources, latency and cost constraints, model options, and quality targets.",
        "A model/data architecture, routing rationale, data contract, prompt strategy, and evaluation plan.",
        upstream=("cluster:ai-capability-architecture-and-autonomy",),
        downstream=("cluster:solution-hypothesis-and-experiment-design",),
    ),
    "cluster:ai-agent-autonomy-and-human-control": cluster(
        "Scope agent behavior, control handoffs, graduated autonomy, and evidence required before expanding action rights.",
        "A task definition, agent capabilities, human roles, failure cost, and observed behavior.",
        "An agency contract, control boundary, graduation criteria, and fallback path.",
        upstream=("cluster:ai-model-and-data-architecture",),
        downstream=("cluster:ai-safety-and-action-governance",),
    ),
    "cluster:ai-interaction-and-probabilistic-ux": cluster(
        "Design human-agent interaction for latency, uncertainty, personalization, correction, and comprehensible recovery.",
        "Probabilistic outputs, user context, interaction latency, correction signals, and accessibility needs.",
        "A human-agent interaction contract, uncertainty presentation, recovery path, and UX evidence.",
        upstream=("cluster:ai-model-and-data-architecture",),
        downstream=("cluster:ai-safety-and-action-governance",),
    ),
    "cluster:ai-safety-and-action-governance": cluster(
        "Assess prompt and action risks, preserve human checkpoints, and prevent unsafe autonomy or unsupported safety claims.",
        "An AI capability, tools and permissions, threat scenarios, failure evidence, and consequence level.",
        "A safety boundary, red-team scope, human checkpoint, stop condition, and residual risk.",
        upstream=("cluster:ai-agent-autonomy-and-human-control", "cluster:ai-interaction-and-probabilistic-ux"),
        downstream=("cluster:risk-preflight-and-safety-governance",),
    ),
    "cluster:ai-organizational-adoption-and-leadership": cluster(
        "Align product leadership, sponsors, pilot teams, adoption paths, and measurable organizational value for AI work.",
        "An AI initiative, organizational constraints, leadership questions, pilot candidates, and value hypotheses.",
        "An adoption plan, leadership decision material, pilot evidence, and ownership model.",
        upstream=("cluster:ai-capability-architecture-and-autonomy",),
        downstream=("cluster:decision-and-outcome-roadmapping",),
    ),
    "cluster:ui-review-scope-and-evidence-acquisition": cluster(
        "Define UI review scope, collect the correct rendered evidence, and route findings without confusing inspection with repair.",
        "A UI brief, target files, runtime, rendered surfaces, and review criteria.",
        "A bounded review set, captures, evidence inventory, and review route.",
        upstream=("cluster:ui-task-routing-and-governance",),
        downstream=("cluster:rendered-ui-critique-and-release-disposition",),
    ),
    "cluster:rendered-ui-critique-and-release-disposition": cluster(
        "Critique real UI renders and animation behavior, prioritize evidence-backed findings, and issue a bounded disposition.",
        "Rendered captures, interaction traces, design criteria, accessibility context, and implementation constraints.",
        "Prioritized findings, remediation hierarchy, verdict, recapture requirements, and residual risk.",
        upstream=("cluster:ui-review-scope-and-evidence-acquisition",),
        downstream=("cluster:evidence-based-ui-review-and-release-gates",),
    ),
    "cluster:independent-plan-review": cluster(
        "Review an implementation plan independently for completeness, executable boundaries, testability, and hidden scope.",
        "A proposed plan, repository constraints, task boundaries, and verification requirements.",
        "Plan findings, required corrections, and an independent readiness verdict.",
        upstream=("cluster:implementation-planning-and-handoff",),
        downstream=("cluster:plan-execution-control",),
    ),
    "cluster:change-delivery-preflight": cluster(
        "Prepare a verified change for delivery by checking branch state, merge base, credentials, automation stops, and documentation invariants.",
        "A reviewed change, repository state, delivery policy, and intended publication boundary.",
        "A delivery-ready package or explicit preflight blockers; no merge or deployment action.",
        upstream=("cluster:completion-evidence-gate",),
        downstream=("cluster:change-packaging-and-versioning",),
    ),
    "cluster:release-rollback-execution": cluster(
        "Execute or prepare a reviewable release rollback when post-deploy evidence meets the rollback condition.",
        "A deployed change, health evidence, provider state, and rollback authorization.",
        "A bounded revert or rollback pull request with evidence and recovery status.",
        upstream=("cluster:deployment-observation-and-recovery",),
        downstream=("cluster:incident-response-coordination",),
    ),
    "cluster:browser-session-and-runtime-configuration": cluster(
        "Configure browser sessions, wrapper dispatch, CLI settings, and isolated project context after prerequisites pass.",
        "A validated browser task, session identifier, project path, wrapper contract, and CLI configuration.",
        "A configured isolated session and reproducible browser invocation settings.",
        upstream=("cluster:tool-runtime-readiness",),
        downstream=("cluster:safe-browser-probing", "cluster:playwright-test-engineering"),
    ),
    "cluster:external-design-token-extraction-and-normalization": cluster(
        "Extract and normalize design primitives from an authorized external surface without treating them as project authority or writing project tokens.",
        "An authorized public reference, extraction runtime, and requested analysis mode.",
        "Reviewed normalized primitives, raw/normalized evidence, provenance, and explicit write-approval state.",
        upstream=("cluster:source-metadata-and-provenance",),
        downstream=("cluster:design-system-foundation-and-token-extraction",),
    ),
    "cluster:frontend-runtime-boundaries-and-dependency-safety": cluster(
        "Keep frontend dependencies, client-server boundaries, assets, and runtime assumptions safe and explicit.",
        "A frontend implementation, dependency graph, rendering environment, and integration constraints.",
        "A bounded runtime design, dependency decision, and safety evidence.",
        upstream=("cluster:design-system-foundation-and-token-extraction",),
        downstream=("cluster:frontend-rendering-and-interaction-performance",),
    ),
    "cluster:frontend-rendering-and-interaction-performance": cluster(
        "Optimize rendering, interaction, animation, and layout performance against measured runtime behavior.",
        "A rendered frontend, interaction traces, performance measurements, and device constraints.",
        "Performance findings, budgets, implementation constraints, and regression evidence.",
        upstream=("cluster:frontend-runtime-boundaries-and-dependency-safety",),
        downstream=("cluster:evidence-based-ui-review-and-release-gates",),
    ),
    "cluster:cross-domain-ui-preflight-checklists": cluster(
        "Run cross-cutting UI preflight checks for accessibility, content, interaction states, responsive behavior, and release readiness.",
        "A rendered UI, acceptance criteria, content, supported devices, and release boundary.",
        "A checklist result, blocking findings, evidence requirements, and residual risk.",
        upstream=("cluster:interaction-states-forms-and-navigation",),
        downstream=("cluster:evidence-based-ui-review-and-release-gates",),
    ),
})

UNIT_RANGES: dict[str, tuple[tuple[int, int, str], ...]] = {
    "prd-development": ((1, 51, "cluster:requirements-and-delivery-contract"),),
    "product-strategy-session": ((1, 48, "cluster:decision-and-outcome-roadmapping"),),
    "discovery-process": ((1, 57, "cluster:problem-framing-and-customer-research"),),
    "prioritization-frameworks": ((1, 23, "cluster:evidence-synthesis-and-opportunity-prioritization"),),
    "outcome-roadmap": ((1, 20, "cluster:decision-and-outcome-roadmapping"),),
    "competitive-strategy": ((1, 119, "cluster:market-positioning-and-competitive-power"),),
    "interview-script": ((1, 16, "cluster:problem-framing-and-customer-research"),),
    "pre-mortem": ((1, 16, "cluster:risk-preflight-and-safety-governance"),),
    "metrics-dashboard": ((1, 16, "cluster:metrics-system-and-observability"),),
    "ai-product-strategy": ((1, 59, "cluster:ai-capability-architecture-and-autonomy"),),
    "impeccable": ((1, 15, "cluster:visual-language-and-anti-template-controls"),),
    "ui-ux-pro-max": ((1, 20, "cluster:design-system-foundation-and-token-extraction"),),
    "web-design-guidelines": ((1, 4, "cluster:evidence-based-ui-review-and-release-gates"),),
    "review-animations": ((1, 22, "cluster:purposeful-motion-and-animation-engineering"),),
    "redesign-existing-projects": ((1, 13, "cluster:existing-interface-redesign-and-preservation"),),
    "web-accessibility": ((1, 20, "cluster:accessibility-contracts-and-assistive-validation"),),
    "prototype": ((1, 19, "cluster:divergent-prototyping-and-variant-selection"),),
    "frontend-design": ((1, 16, "cluster:visual-language-and-anti-template-controls"),),
    "extract-design-system": ((1, 11, "cluster:design-system-foundation-and-token-extraction"),),
    "design-taste-frontend": ((1, 23, "cluster:visual-language-and-anti-template-controls"),),
    "writing-plans": (
        (1, 8, "cluster:implementation-planning-and-handoff"),
        (9, 9, "cluster:developer-self-check-and-fix"),
        (10, 10, "cluster:implementation-planning-and-handoff"),
        (11, 11, "cluster:independent-code-review"),
    ),
    "test-driven-development": (
        (1, 13, "cluster:tdd-change-loop"),
        (14, 14, "cluster:completion-evidence-gate"),
        (15, 15, "cluster:tdd-change-loop"),
        (16, 21, "cluster:test-double-discipline"),
    ),
    "systematic-debugging": (
        (1, 15, "cluster:root-cause-investigation"),
        (16, 23, "cluster:resilience-and-determinism"),
    ),
    "requesting-code-review": ((1, 20, "cluster:independent-code-review"),),
    "verification-before-completion": ((1, 14, "cluster:completion-evidence-gate"),),
    "executing-plans": ((1, 9, "cluster:plan-execution-control"),),
    "subagent-driven-development": (
        (1, 14, "cluster:subagent-task-pipeline"),
        (15, 16, "cluster:developer-self-check-and-fix"),
        (17, 20, "cluster:independent-code-review"),
    ),
    "improve-codebase-architecture": (
        (1, 3, "cluster:architecture-deepening-discovery"),
        (4, 5, "cluster:architecture-candidate-reporting"),
        (6, 6, "cluster:architecture-interface-alternative-evaluation"),
        (7, 12, "cluster:architecture-candidate-reporting"),
    ),
    "codebase-design": (
        (1, 9, "cluster:architecture-deep-module-design"),
        (10, 12, "cluster:architecture-interface-alternative-evaluation"),
    ),
    "playwright": (
        (1, 1, "cluster:safe-browser-probing"),
        (2, 3, "cluster:tool-runtime-readiness"),
        (4, 9, "cluster:safe-browser-probing"),
        (10, 10, "cluster:tool-runtime-readiness"),
        (11, 11, "cluster:safe-browser-probing"),
        (12, 13, "cluster:tool-runtime-readiness"),
        (14, 26, "cluster:safe-browser-probing"),
    ),
    "playwright-best-practices": (
        (1, 3, "cluster:playwright-test-engineering"),
        (4, 4, "cluster:root-cause-investigation"),
        (5, 12, "cluster:playwright-test-engineering"),
        (13, 13, "cluster:completion-evidence-gate"),
        (14, 16, "cluster:playwright-test-engineering"),
        (17, 19, "cluster:resilience-and-determinism"),
        (20, 25, "cluster:playwright-test-engineering"),
        (26, 26, "cluster:resilience-and-determinism"),
    ),
    "audit-website": (
        (1, 1, "cluster:tool-runtime-readiness"),
        (2, 6, "cluster:website-audit-remediation"),
        (7, 7, "cluster:baseline-regression-control"),
        (8, 8, "cluster:completion-evidence-gate"),
        (9, 18, "cluster:website-audit-remediation"),
    ),
    "vitest": (
        (1, 4, "cluster:vitest-tooling"),
        (5, 8, "cluster:test-double-discipline"),
        (9, 12, "cluster:resilience-and-determinism"),
        (13, 13, "cluster:vitest-tooling"),
        (14, 16, "cluster:test-double-discipline"),
        (17, 18, "cluster:vitest-tooling"),
        (19, 19, "cluster:completion-evidence-gate"),
        (20, 20, "cluster:vitest-tooling"),
    ),
    "ship": (
        (1, 3, "cluster:merge-and-deploy-readiness"),
        (4, 5, "cluster:change-packaging-and-versioning"),
        (6, 6, "cluster:completion-evidence-gate"),
        (7, 7, "cluster:merge-and-deploy-readiness"),
        (8, 8, "cluster:change-packaging-and-versioning"),
    ),
    "land-and-deploy": (
        (1, 6, "cluster:merge-and-deploy-readiness"),
        (7, 7, "cluster:deployment-observation-and-recovery"),
        (8, 9, "cluster:production-canary-monitoring"),
        (10, 10, "cluster:deployment-observation-and-recovery"),
    ),
    "canary": (
        (1, 1, "cluster:production-canary-monitoring"),
        (2, 2, "cluster:baseline-regression-control"),
        (3, 7, "cluster:production-canary-monitoring"),
        (8, 8, "cluster:baseline-regression-control"),
    ),
    "incident-response": ((1, 9, "cluster:incident-response-coordination"),),
    "metrics-review": ((1, 10, "cluster:metrics-system-and-observability"),),
    "analyzing-user-feedback": (
        (1, 5, "cluster:feedback-and-continuous-learning-loop"),
        (6, 8, "cluster:evidence-synthesis-and-opportunity-prioritization"),
        (9, 10, "cluster:feedback-and-continuous-learning-loop"),
    ),
    "validate-data": ((1, 10, "cluster:data-analysis-validation"),),
    "craft-experiment-design": ((1, 7, "cluster:solution-hypothesis-and-experiment-design"),),
    "craft-experiment-readout": ((1, 7, "cluster:results-analysis-and-decision-readout"),),
    "retro": ((1, 10, "cluster:engineering-retrospective-and-improvement"),),
    "llm-evaluation": ((1, 10, "cluster:llm-quality-evaluation"),),
    "web-perf": ((1, 6, "cluster:web-performance-diagnostics"),),
}


UNIT_OVERRIDES: dict[str, str] = {
    "ggcc-desc-intercept-overview": "cluster:git-destructive-command-guard",
    "ggcc-rule-blocked-patterns-spec": "cluster:git-destructive-command-guard",
    "ggcc-method-step1-ask-scope": "cluster:git-destructive-command-guard",
    "ggcc-method-step2-copy-script": "cluster:git-destructive-command-guard",
    "ggcc-template-step3-settings-injection": "cluster:git-destructive-command-guard",
    "ggcc-method-step4-customization": "cluster:git-destructive-command-guard",
    "ggcc-gate-step5-verification-test": "cluster:git-destructive-command-guard",
    "ggcc-rule-script-pattern-matching": "cluster:git-destructive-command-guard",
    "ggcc-method-script-execution-loop": "cluster:git-destructive-command-guard",
    "ts-goal-balance-triangle": "cluster:testing-portfolio-strategy",
    "ts-model-testing-pyramid": "cluster:testing-portfolio-strategy",
    "ts-method-component-api-endpoints": "cluster:testing-portfolio-strategy",
    "ts-method-component-data-pipelines": "cluster:testing-portfolio-strategy",
    "ts-method-component-frontend": "cluster:testing-portfolio-strategy",
    "ts-method-component-infrastructure": "cluster:testing-portfolio-strategy",
    "ts-rule-coverage-focus-areas": "cluster:testing-portfolio-strategy",
    "ts-rule-coverage-skip-areas": "cluster:testing-portfolio-strategy",
    "ts-template-output-test-plan": "cluster:testing-portfolio-strategy",
    "qao-desc-report-only-purpose": "cluster:independent-blackbox-qa",
    "qao-rule-blackbox-identity": "cluster:independent-blackbox-qa",
    "qao-rule-tab-isolation": "cluster:safe-browser-probing",
    "qao-rule-look-not-act-consent": "cluster:safe-browser-probing",
    "qao-rule-credentials-privacy": "cluster:safe-browser-probing",
    "qao-method-diff-aware-mode": "cluster:independent-blackbox-qa",
    "qao-method-quick-and-regression-modes": "cluster:baseline-regression-control",
    "qao-method-console-error-hook": "cluster:independent-blackbox-qa",
    "qao-template-per-page-checklist": "cluster:independent-blackbox-qa",
    "qao-gate-interactive-evidence-chain": "cluster:completion-evidence-gate",
    "qao-template-health-rubric-weights": "cluster:independent-blackbox-qa",
    "qao-rule-twelve-qa-commandments": "cluster:independent-blackbox-qa",
    "qao-rule-never-fix-bugs-boundary": "cluster:independent-blackbox-qa",
    "cr-desc-review-lens-overview": "cluster:independent-code-review",
    "cr-method-usage-invocation": "cluster:independent-code-review",
    "cr-rule-standalone-capabilities": "cluster:independent-code-review",
    "cr-template-security-checklist": "cluster:independent-code-review",
    "cr-template-performance-checklist": "cluster:independent-code-review",
    "cr-template-correctness-checklist": "cluster:independent-code-review",
    "cr-template-maintainability-checklist": "cluster:independent-code-review",
    "cr-template-report-format": "cluster:independent-code-review",
    "cr-rule-tips-context-focus": "cluster:independent-code-review",
}


for _cluster_id, _unit_ids in {
    "cluster:context-intake-and-routing": (
        "prd-development:unit-002", "prd-development:unit-004",
        "prd-development:unit-005", "prd-development:unit-006",
        "prd-development:unit-015", "prd-development:unit-021",
        "prd-development:unit-030", "prd-development:unit-039",
        "prd-development:unit-048", "prd-development:unit-051",
        "product-strategy-session:unit-001", "product-strategy-session:unit-002",
        "product-strategy-session:unit-003", "product-strategy-session:unit-004",
        "product-strategy-session:unit-005", "product-strategy-session:unit-006",
        "product-strategy-session:unit-007", "product-strategy-session:unit-008",
        "product-strategy-session:unit-009", "product-strategy-session:unit-032",
        "product-strategy-session:unit-034", "product-strategy-session:unit-035",
        "product-strategy-session:unit-036", "product-strategy-session:unit-037",
        "product-strategy-session:unit-038", "product-strategy-session:unit-039",
        "product-strategy-session:unit-040", "discovery-process:unit-001",
        "discovery-process:unit-002", "discovery-process:unit-003",
        "discovery-process:unit-005", "discovery-process:unit-006",
        "discovery-process:unit-007", "discovery-process:unit-037",
        "discovery-process:unit-038", "discovery-process:unit-039",
        "discovery-process:unit-043", "discovery-process:unit-044",
        "discovery-process:unit-045", "discovery-process:unit-046",
        "discovery-process:unit-047", "discovery-process:unit-048",
        "discovery-process:unit-049", "outcome-roadmap:unit-001",
        "outcome-roadmap:unit-004", "outcome-roadmap:unit-005",
        "outcome-roadmap:unit-013", "outcome-roadmap:unit-018",
        "outcome-roadmap:unit-019", "outcome-roadmap:unit-020",
        "interview-script:unit-003", "interview-script:unit-004",
        "interview-script:unit-014", "interview-script:unit-016",
        "pre-mortem:unit-004", "pre-mortem:unit-014",
        "pre-mortem:unit-016", "metrics-dashboard:unit-003",
        "metrics-dashboard:unit-014", "metrics-dashboard:unit-015",
        "metrics-dashboard:unit-016", "ai-product-strategy:unit-001",
        "ai-product-strategy:unit-007", "ai-product-strategy:unit-008",
        "ai-product-strategy:unit-009", "ai-product-strategy:unit-023",
        "ai-product-strategy:unit-024", "ai-product-strategy:unit-038",
        "ai-product-strategy:unit-046", "ai-product-strategy:unit-052",
        "ai-product-strategy:unit-053", "ai-product-strategy:unit-054",
    ),
    "cluster:market-positioning-and-competitive-power": (
        "prd-development:unit-010", "prd-development:unit-019",
        "prd-development:unit-024", "prd-development:unit-049",
        "product-strategy-session:unit-010", "product-strategy-session:unit-026",
        "product-strategy-session:unit-043", "product-strategy-session:unit-044",
        "product-strategy-session:unit-045", "product-strategy-session:unit-046",
        "product-strategy-session:unit-048", "competitive-strategy:unit-026",
        "competitive-strategy:unit-040", "competitive-strategy:unit-043",
        "competitive-strategy:unit-055", "competitive-strategy:unit-057",
        "competitive-strategy:unit-060", "competitive-strategy:unit-065",
        "competitive-strategy:unit-081", "competitive-strategy:unit-083",
        "competitive-strategy:unit-086", "competitive-strategy:unit-089",
        "competitive-strategy:unit-114", "competitive-strategy:unit-116",
        "ai-product-strategy:unit-004", "ai-product-strategy:unit-005",
        "ai-product-strategy:unit-006", "ai-product-strategy:unit-010",
        "ai-product-strategy:unit-012", "ai-product-strategy:unit-013",
        "ai-product-strategy:unit-034", "ai-product-strategy:unit-045",
        "ai-product-strategy:unit-048",
    ),
    "cluster:problem-framing-and-customer-research": (
        "prd-development:unit-008", "prd-development:unit-009",
        "prd-development:unit-016", "prd-development:unit-022",
        "prd-development:unit-023", "prd-development:unit-032",
        "prd-development:unit-034", "prd-development:unit-040",
        "prd-development:unit-041", "prd-development:unit-042",
        "product-strategy-session:unit-011", "product-strategy-session:unit-012",
        "product-strategy-session:unit-013", "product-strategy-session:unit-014",
        "product-strategy-session:unit-015", "product-strategy-session:unit-016",
        "product-strategy-session:unit-017", "product-strategy-session:unit-033",
        "product-strategy-session:unit-042", "competitive-strategy:unit-003",
        "competitive-strategy:unit-007", "competitive-strategy:unit-022",
        "competitive-strategy:unit-054", "competitive-strategy:unit-076",
        "competitive-strategy:unit-078", "competitive-strategy:unit-095",
        "competitive-strategy:unit-102", "competitive-strategy:unit-109",
    ),
    "cluster:evidence-synthesis-and-opportunity-prioritization": (
        "prd-development:unit-031", "product-strategy-session:unit-023",
        "product-strategy-session:unit-024", "discovery-process:unit-004",
        "discovery-process:unit-013", "discovery-process:unit-019",
        "discovery-process:unit-020", "discovery-process:unit-021",
        "discovery-process:unit-022", "discovery-process:unit-023",
        "discovery-process:unit-024", "discovery-process:unit-025",
        "discovery-process:unit-040", "discovery-process:unit-042",
        "discovery-process:unit-050", "discovery-process:unit-052",
        "discovery-process:unit-057", "competitive-strategy:unit-037",
        "competitive-strategy:unit-042", "competitive-strategy:unit-053",
        "competitive-strategy:unit-056", "competitive-strategy:unit-062",
        "competitive-strategy:unit-080",
        "competitive-strategy:unit-088", "competitive-strategy:unit-096",
        "competitive-strategy:unit-097", "competitive-strategy:unit-098",
        "competitive-strategy:unit-119",
    ),
    "cluster:solution-hypothesis-and-experiment-design": (
        "prd-development:unit-011", "prd-development:unit-025",
        "prd-development:unit-035", "prd-development:unit-043",
        "product-strategy-session:unit-018", "product-strategy-session:unit-019",
        "product-strategy-session:unit-020", "product-strategy-session:unit-021",
        "product-strategy-session:unit-022", "product-strategy-session:unit-041",
        "discovery-process:unit-026", "discovery-process:unit-027",
        "discovery-process:unit-028", "discovery-process:unit-029",
        "discovery-process:unit-030", "discovery-process:unit-031",
        "discovery-process:unit-053", "ai-product-strategy:unit-011",
        "ai-product-strategy:unit-025", "ai-product-strategy:unit-026",
        "ai-product-strategy:unit-027", "ai-product-strategy:unit-028",
        "ai-product-strategy:unit-029", "ai-product-strategy:unit-032",
        "ai-product-strategy:unit-036", "ai-product-strategy:unit-041",
        "ai-product-strategy:unit-042", "ai-product-strategy:unit-043",
        "ai-product-strategy:unit-047", "ai-product-strategy:unit-049",
        "ai-product-strategy:unit-050", "ai-product-strategy:unit-051",
        "ai-product-strategy:unit-055",
    ),
    "cluster:decision-and-outcome-roadmapping": (
        "product-strategy-session:unit-025", "product-strategy-session:unit-027",
        "product-strategy-session:unit-028",
    ),
    "cluster:requirements-and-delivery-contract": (
        "product-strategy-session:unit-029", "product-strategy-session:unit-030",
        "product-strategy-session:unit-031", "discovery-process:unit-033",
        "discovery-process:unit-034",
    ),
    "cluster:risk-preflight-and-safety-governance": (
        "prd-development:unit-014", "prd-development:unit-028",
        "prd-development:unit-029", "prd-development:unit-036",
        "prd-development:unit-037", "prd-development:unit-038",
        "prd-development:unit-046", "prd-development:unit-047",
        "product-strategy-session:unit-047", "competitive-strategy:unit-038",
        "competitive-strategy:unit-039", "competitive-strategy:unit-044",
        "competitive-strategy:unit-046", "competitive-strategy:unit-071",
        "competitive-strategy:unit-077", "competitive-strategy:unit-118",
        "ai-product-strategy:unit-022", "ai-product-strategy:unit-030",
        "ai-product-strategy:unit-031", "ai-product-strategy:unit-033",
        "ai-product-strategy:unit-035", "ai-product-strategy:unit-039",
        "ai-product-strategy:unit-044", "ai-product-strategy:unit-056",
        "ai-product-strategy:unit-057",
    ),
    "cluster:metrics-system-and-observability": (
        "prd-development:unit-012", "prd-development:unit-018",
        "prd-development:unit-026", "prd-development:unit-033",
        "prd-development:unit-044", "prd-development:unit-050",
        "outcome-roadmap:unit-014", "ai-product-strategy:unit-016",
        "ai-product-strategy:unit-017",
    ),
    "cluster:results-analysis-and-decision-readout": (
        "discovery-process:unit-032", "discovery-process:unit-035",
        "discovery-process:unit-036", "discovery-process:unit-051",
        "discovery-process:unit-054", "discovery-process:unit-055",
        "discovery-process:unit-056",
    ),
    "cluster:feedback-and-continuous-learning-loop": (
        "metrics-dashboard:unit-012", "metrics-dashboard:unit-013",
        "ai-product-strategy:unit-003", "ai-product-strategy:unit-015",
        "ai-product-strategy:unit-018", "ai-product-strategy:unit-019",
        "ai-product-strategy:unit-020", "ai-product-strategy:unit-037",
    ),
    "cluster:ui-task-routing-and-governance": (
        "impeccable:unit-001", "impeccable:unit-004", "impeccable:unit-007",
        "impeccable:unit-008", "impeccable:unit-009", "ui-ux-pro-max:unit-001",
        "ui-ux-pro-max:unit-002", "ui-ux-pro-max:unit-003",
        "ui-ux-pro-max:unit-004", "ui-ux-pro-max:unit-008",
        "ui-ux-pro-max:unit-009", "extract-design-system:unit-001",
        "extract-design-system:unit-002", "extract-design-system:unit-006",
        "extract-design-system:unit-007", "extract-design-system:unit-008",
        "design-taste-frontend:unit-001",
    ),
    "cluster:design-context-and-direction-contract": (
        "impeccable:unit-005", "impeccable:unit-006", "impeccable:unit-012",
        "impeccable:unit-013", "ui-ux-pro-max:unit-007", "prototype:unit-004",
        "prototype:unit-005", "frontend-design:unit-002",
        "frontend-design:unit-003", "frontend-design:unit-011",
        "frontend-design:unit-012", "extract-design-system:unit-009",
        "design-taste-frontend:unit-002", "design-taste-frontend:unit-003",
    ),
    "cluster:design-system-foundation-and-token-extraction": (
        "redesign-existing-projects:unit-002", "redesign-existing-projects:unit-003",
        "redesign-existing-projects:unit-007", "redesign-existing-projects:unit-008",
        "design-taste-frontend:unit-004",
    ),
    "cluster:visual-language-and-anti-template-controls": (
        "ui-ux-pro-max:unit-011", "ui-ux-pro-max:unit-013",
    ),
    "cluster:responsive-layout-and-spatial-composition": (
        "ui-ux-pro-max:unit-014", "ui-ux-pro-max:unit-019",
        "redesign-existing-projects:unit-004", "frontend-design:unit-006",
        "design-taste-frontend:unit-008", "design-taste-frontend:unit-010",
        "design-taste-frontend:unit-018",
    ),
    "cluster:content-copy-and-authentic-assets": (
        "impeccable:unit-014", "redesign-existing-projects:unit-006",
        "frontend-design:unit-008", "frontend-design:unit-013",
        "frontend-design:unit-014", "design-taste-frontend:unit-011",
        "design-taste-frontend:unit-012", "design-taste-frontend:unit-013",
    ),
    "cluster:interaction-states-forms-and-navigation": (
        "ui-ux-pro-max:unit-012", "ui-ux-pro-max:unit-017",
        "redesign-existing-projects:unit-005", "prototype:unit-012",
        "prototype:unit-013", "prototype:unit-014", "prototype:unit-016",
        "prototype:unit-017", "prototype:unit-018", "prototype:unit-019",
        "frontend-design:unit-015", "design-taste-frontend:unit-009",
    ),
    "cluster:accessibility-contracts-and-assistive-validation": (
        "ui-ux-pro-max:unit-016", "review-animations:unit-021",
        "design-taste-frontend:unit-019",
    ),
    "cluster:purposeful-motion-and-animation-engineering": (
        "ui-ux-pro-max:unit-020", "prototype:unit-015",
        "frontend-design:unit-007", "design-taste-frontend:unit-014",
        "design-taste-frontend:unit-015",
    ),
    "cluster:existing-interface-redesign-and-preservation": (
        "prototype:unit-009", "design-taste-frontend:unit-022",
    ),
    "cluster:evidence-based-ui-review-and-release-gates": (
        "impeccable:unit-003", "impeccable:unit-010", "impeccable:unit-015",
        "ui-ux-pro-max:unit-010", "ui-ux-pro-max:unit-015",
        "review-animations:unit-001", "review-animations:unit-002",
        "review-animations:unit-004", "review-animations:unit-005",
        "review-animations:unit-006", "review-animations:unit-007",
        "review-animations:unit-008", "review-animations:unit-009",
        "review-animations:unit-022", "redesign-existing-projects:unit-010",
        "redesign-existing-projects:unit-012", "prototype:unit-008",
        "design-taste-frontend:unit-021", "design-taste-frontend:unit-023",
    ),
}.items():
    UNIT_OVERRIDES.update({_unit_id: _cluster_id for _unit_id in _unit_ids})


SEMANTIC_OVERRIDE_GROUPS: dict[str, tuple[str, ...]] = {
    "cluster:ai-capability-architecture-and-autonomy": (
        "ai-product-strategy:unit-001",
    ),
    "cluster:source-metadata-and-provenance": (
        "competitive-strategy:unit-001",
        "discovery-process:unit-048",
        "prioritization-frameworks:unit-001",
        "outcome-roadmap:unit-001",
        "frontend-design:unit-016",
    ),
    "cluster:reference-library-and-deferred-material": (
        "competitive-strategy:unit-021", "competitive-strategy:unit-032",
        "competitive-strategy:unit-085", "competitive-strategy:unit-103",
        "competitive-strategy:unit-110", "competitive-strategy:unit-111",
        "competitive-strategy:unit-117", "discovery-process:unit-046",
        "discovery-process:unit-047", "discovery-process:unit-007",
        "interview-script:unit-016",
        "prioritization-frameworks:unit-017", "prioritization-frameworks:unit-018",
        "prioritization-frameworks:unit-019", "prioritization-frameworks:unit-020",
        "prioritization-frameworks:unit-021", "prioritization-frameworks:unit-022",
        "prioritization-frameworks:unit-023", "outcome-roadmap:unit-018",
        "outcome-roadmap:unit-019", "outcome-roadmap:unit-020",
        "ai-product-strategy:unit-038",
    ),
    "cluster:artifact-persistence-and-tool-actions": (
        "pre-mortem:unit-014", "metrics-dashboard:unit-015",
        "outcome-roadmap:unit-005", "outcome-roadmap:unit-013",
    ),
    "cluster:workflow-orchestration-and-lifecycle": (
        "prd-development:unit-006", "prd-development:unit-015",
        "prd-development:unit-021", "prd-development:unit-030",
        "prd-development:unit-039", "product-strategy-session:unit-001",
        "product-strategy-session:unit-004", "product-strategy-session:unit-007",
        "product-strategy-session:unit-032", "product-strategy-session:unit-038",
        "discovery-process:unit-001", "discovery-process:unit-003",
        "discovery-process:unit-045", "outcome-roadmap:unit-004",
    ),
    "cluster:facilitation-and-collaboration-protocols": (
        "prd-development:unit-005", "prd-development:unit-048",
        "product-strategy-session:unit-002", "product-strategy-session:unit-003",
        "product-strategy-session:unit-005", "product-strategy-session:unit-006",
        "product-strategy-session:unit-008", "product-strategy-session:unit-009",
        "product-strategy-session:unit-034", "product-strategy-session:unit-035",
        "product-strategy-session:unit-036", "product-strategy-session:unit-037",
        "discovery-process:unit-002", "discovery-process:unit-005",
        "discovery-process:unit-006", "discovery-process:unit-043",
        "discovery-process:unit-044",
    ),
    "cluster:document-and-artifact-governance": (
        "prd-development:unit-003", "prd-development:unit-019",
        "prd-development:unit-051", "product-strategy-session:unit-040",
        "discovery-process:unit-049", "outcome-roadmap:unit-009",
        "outcome-roadmap:unit-011", "outcome-roadmap:unit-012",
        "metrics-dashboard:unit-010", "metrics-dashboard:unit-011",
    ),
    "cluster:market-segmentation-and-demand-intelligence": (
        "competitive-strategy:unit-003", "competitive-strategy:unit-007",
        "competitive-strategy:unit-022", "competitive-strategy:unit-078",
        "competitive-strategy:unit-008", "competitive-strategy:unit-079",
        "competitive-strategy:unit-061", "competitive-strategy:unit-063",
        "competitive-strategy:unit-064", "competitive-strategy:unit-090",
        "competitive-strategy:unit-092",
    ),
    "cluster:structural-power-and-moats": (
        "competitive-strategy:unit-004", "competitive-strategy:unit-081",
        "competitive-strategy:unit-005", "competitive-strategy:unit-010",
        "competitive-strategy:unit-031", "competitive-strategy:unit-107",
        "competitive-strategy:unit-017", "competitive-strategy:unit-025",
        "competitive-strategy:unit-049", "competitive-strategy:unit-091",
        "competitive-strategy:unit-060", "competitive-strategy:unit-066",
        "competitive-strategy:unit-083", "competitive-strategy:unit-009",
        "competitive-strategy:unit-023", "competitive-strategy:unit-050",
        "competitive-strategy:unit-082", "competitive-strategy:unit-006",
        "competitive-strategy:unit-013", "competitive-strategy:unit-026",
        "competitive-strategy:unit-030", "competitive-strategy:unit-055",
        "competitive-strategy:unit-065", "competitive-strategy:unit-089",
        "competitive-strategy:unit-014", "competitive-strategy:unit-059",
        "competitive-strategy:unit-016", "competitive-strategy:unit-024",
        "competitive-strategy:unit-041", "competitive-strategy:unit-067",
        "competitive-strategy:unit-074", "competitive-strategy:unit-019",
        "competitive-strategy:unit-040", "competitive-strategy:unit-114",
        "competitive-strategy:unit-018", "competitive-strategy:unit-057",
        "competitive-strategy:unit-058", "competitive-strategy:unit-093",
        "competitive-strategy:unit-011", "competitive-strategy:unit-015",
        "competitive-strategy:unit-052", "competitive-strategy:unit-099",
        "competitive-strategy:unit-104",
    ),
    "cluster:competitive-response-and-monitoring": (
        "competitive-strategy:unit-020", "competitive-strategy:unit-028",
        "competitive-strategy:unit-043", "competitive-strategy:unit-116",
        "competitive-strategy:unit-012", "competitive-strategy:unit-105",
        "competitive-strategy:unit-042", "competitive-strategy:unit-119",
        "competitive-strategy:unit-056", "competitive-strategy:unit-098",
        "competitive-strategy:unit-096", "competitive-strategy:unit-097",
    ),
    "cluster:research-planning-and-governance": (
        "discovery-process:unit-013", "discovery-process:unit-014",
        "discovery-process:unit-015", "discovery-process:unit-016",
        "discovery-process:unit-017", "discovery-process:unit-020",
        "discovery-process:unit-037", "discovery-process:unit-038",
        "discovery-process:unit-039", "discovery-process:unit-042",
    ),
    "cluster:customer-interview-execution": (
        "interview-script:unit-001", "interview-script:unit-002",
        "interview-script:unit-005", "interview-script:unit-006",
        "interview-script:unit-007", "interview-script:unit-008",
        "interview-script:unit-009", "interview-script:unit-010",
        "interview-script:unit-011", "interview-script:unit-012",
        "interview-script:unit-013", "interview-script:unit-015",
        "discovery-process:unit-041",
    ),
    "cluster:persona-jtbd-and-journey-modeling": (
        "product-strategy-session:unit-011", "product-strategy-session:unit-012",
        "product-strategy-session:unit-013", "product-strategy-session:unit-014",
        "product-strategy-session:unit-015", "product-strategy-session:unit-016",
        "product-strategy-session:unit-017",
        "discovery-process:unit-008", "discovery-process:unit-009",
        "discovery-process:unit-010", "discovery-process:unit-011",
        "discovery-process:unit-012",
    ),
    "cluster:qualitative-evidence-synthesis": (
        "discovery-process:unit-018", "discovery-process:unit-019",
        "discovery-process:unit-021", "discovery-process:unit-022",
        "discovery-process:unit-023", "discovery-process:unit-024",
        "discovery-process:unit-025", "discovery-process:unit-040",
        "discovery-process:unit-057", "analyzing-user-feedback:unit-006",
        "analyzing-user-feedback:unit-007", "analyzing-user-feedback:unit-008",
    ),
    "cluster:opportunity-prioritization-and-frameworks": (
        "prioritization-frameworks:unit-002", "prioritization-frameworks:unit-003",
        "prioritization-frameworks:unit-004", "prioritization-frameworks:unit-005",
        "prioritization-frameworks:unit-006", "prioritization-frameworks:unit-007",
        "prioritization-frameworks:unit-008", "prioritization-frameworks:unit-009",
        "prioritization-frameworks:unit-010", "prioritization-frameworks:unit-011",
        "prioritization-frameworks:unit-012", "prioritization-frameworks:unit-013",
        "prioritization-frameworks:unit-014", "prioritization-frameworks:unit-015",
        "prioritization-frameworks:unit-016", "product-strategy-session:unit-023",
        "product-strategy-session:unit-024",
    ),
    "cluster:ai-product-opportunity-and-wedge": (
        "ai-product-strategy:unit-004", "ai-product-strategy:unit-005",
        "ai-product-strategy:unit-006", "ai-product-strategy:unit-010",
        "ai-product-strategy:unit-012", "ai-product-strategy:unit-013",
        "ai-product-strategy:unit-034", "ai-product-strategy:unit-048",
    ),
    "cluster:ai-model-and-data-architecture": (
        "ai-product-strategy:unit-016", "ai-product-strategy:unit-017",
        "ai-product-strategy:unit-027", "ai-product-strategy:unit-031",
        "ai-product-strategy:unit-041", "ai-product-strategy:unit-042",
        "ai-product-strategy:unit-043", "ai-product-strategy:unit-049",
        "ai-product-strategy:unit-050", "ai-product-strategy:unit-051",
    ),
    "cluster:strategic-choice-and-differentiation": (
        "competitive-strategy:unit-047", "competitive-strategy:unit-048",
        "competitive-strategy:unit-087", "competitive-strategy:unit-108",
        "competitive-strategy:unit-115", "product-strategy-session:unit-010",
        "product-strategy-session:unit-026", "prd-development:unit-010",
        "prd-development:unit-024", "prd-development:unit-049",
    ),
    "cluster:competitive-case-library": (
        "competitive-strategy:unit-045", "competitive-strategy:unit-051",
        "competitive-strategy:unit-068", "competitive-strategy:unit-069",
        "competitive-strategy:unit-070", "competitive-strategy:unit-071",
        "competitive-strategy:unit-072", "competitive-strategy:unit-073",
        "competitive-strategy:unit-075",
    ),
    "cluster:ai-agent-autonomy-and-human-control": (
        "ai-product-strategy:unit-014", "ai-product-strategy:unit-015",
        "ai-product-strategy:unit-021", "ai-product-strategy:unit-029",
        "ai-product-strategy:unit-033", "ai-product-strategy:unit-039",
    ),
    "cluster:ai-interaction-and-probabilistic-ux": (
        "ai-product-strategy:unit-002", "ai-product-strategy:unit-040",
        "ai-product-strategy:unit-044", "ai-product-strategy:unit-045",
    ),
    "cluster:ai-safety-and-action-governance": (
        "ai-product-strategy:unit-022", "ai-product-strategy:unit-030",
        "ai-product-strategy:unit-035", "ai-product-strategy:unit-057",
    ),
    "cluster:ai-organizational-adoption-and-leadership": (
        "ai-product-strategy:unit-036", "ai-product-strategy:unit-052",
        "ai-product-strategy:unit-053", "ai-product-strategy:unit-058",
        "ai-product-strategy:unit-059",
    ),
    "cluster:ui-review-scope-and-evidence-acquisition": (
        "web-design-guidelines:unit-001", "web-design-guidelines:unit-002",
        "web-design-guidelines:unit-003", "web-design-guidelines:unit-004",
    ),
    "cluster:rendered-ui-critique-and-release-disposition": (
        "impeccable:unit-003", "impeccable:unit-010", "impeccable:unit-015",
        "review-animations:unit-001", "review-animations:unit-002",
        "review-animations:unit-004", "review-animations:unit-005",
        "review-animations:unit-006", "review-animations:unit-007",
        "review-animations:unit-008", "review-animations:unit-022",
        "redesign-existing-projects:unit-010", "redesign-existing-projects:unit-012",
    ),
    "cluster:independent-plan-review": ("writing-plans:unit-011",),
    "cluster:change-delivery-preflight": (
        "ship:unit-001", "ship:unit-002", "ship:unit-003", "ship:unit-007",
    ),
    "cluster:release-rollback-execution": ("land-and-deploy:unit-0010",),
    "cluster:tool-runtime-readiness": ("playwright:unit-013",),
    "cluster:browser-session-and-runtime-configuration": (
        "playwright:unit-002", "playwright:unit-003", "playwright:unit-010",
        "playwright:unit-012", "playwright:unit-025", "audit-website:unit-001",
    ),
    "cluster:design-system-foundation-and-token-extraction": (
        "ui-ux-pro-max:unit-005", "ui-ux-pro-max:unit-006",
        "extract-design-system:unit-011", "redesign-existing-projects:unit-002",
        "redesign-existing-projects:unit-003", "redesign-existing-projects:unit-007",
        "redesign-existing-projects:unit-008",
    ),
    "cluster:external-design-token-extraction-and-normalization": (
        "extract-design-system:unit-001", "extract-design-system:unit-002",
        "extract-design-system:unit-003", "extract-design-system:unit-004",
        "extract-design-system:unit-005", "extract-design-system:unit-006",
        "extract-design-system:unit-007", "extract-design-system:unit-008",
        "extract-design-system:unit-009", "extract-design-system:unit-010",
    ),
    "cluster:frontend-runtime-boundaries-and-dependency-safety": (
        "redesign-existing-projects:unit-009", "redesign-existing-projects:unit-013",
        "frontend-design:unit-010", "design-taste-frontend:unit-005",
    ),
    "cluster:frontend-rendering-and-interaction-performance": (
        "ui-ux-pro-max:unit-018", "review-animations:unit-016",
        "design-taste-frontend:unit-016",
    ),
    "cluster:cross-domain-ui-preflight-checklists": (
        "ui-ux-pro-max:unit-010", "ui-ux-pro-max:unit-015",
        "web-accessibility:unit-005", "web-accessibility:unit-014",
        "web-accessibility:unit-019", "frontend-design:unit-011",
        "design-taste-frontend:unit-017", "design-taste-frontend:unit-023",
    ),
    "cluster:divergent-prototyping-and-variant-selection": (
        "prototype:unit-012", "prototype:unit-013", "prototype:unit-014",
        "prototype:unit-015", "prototype:unit-016", "prototype:unit-017",
        "prototype:unit-018", "prototype:unit-019",
    ),
}

SEMANTIC_OVERRIDES: dict[str, str] = {}
for _cluster_id, _unit_ids in SEMANTIC_OVERRIDE_GROUPS.items():
    for _unit_id in _unit_ids:
        if _unit_id in SEMANTIC_OVERRIDES:
            raise ValueError(f"duplicate semantic override: {_unit_id}")
        SEMANTIC_OVERRIDES[_unit_id] = _cluster_id
UNIT_OVERRIDES.update(SEMANTIC_OVERRIDES)


INVENTORY_SCOPES = {"included", "deferred-platform"}
INVENTORY_RESOLUTIONS = {"resolved", "duplicate-reference", "gap", "deferred"}
NONSTANDARD_UNIT_PREFIXES = {
    "code-review": "cr-",
    "git-guardrails-claude-code": "ggcc-",
    "qa-only": "qao-",
    "testing-strategy": "ts-",
}


RELATIONSHIPS: tuple[dict[str, object], ...] = (
    {
        "id": "relationship:ai-leadership-duplicate",
        "type": "duplicate",
        "source_unit_id": "ai-product-strategy:unit-058",
        "target_unit_id": "ai-product-strategy:unit-059",
        "cluster_id": "cluster:ai-organizational-adoption-and-leadership",
    },
    {
        "id": "relationship:prototype-directions-and-verification",
        "type": "complementary",
        "source_unit_id": "prototype:unit-006",
        "target_unit_id": "prototype:unit-008",
        "cluster_id": "cluster:divergent-prototyping-and-variant-selection",
    },
    {
        "id": "relationship:ost-or-lean-ux",
        "type": "conditional-variant",
        "source_unit_id": "discovery-process:unit-026",
        "target_unit_id": "discovery-process:unit-027",
        "cluster_id": "cluster:solution-hypothesis-and-experiment-design",
        "condition": {
            "source": {
                "applicability": "Use an opportunity solution tree to expand prioritized pains into opportunities and solution options."
            },
            "target": {
                "applicability": "Use Lean UX Canvas instead when the team explicitly prefers a hypothesis-driven approach."
            },
        },
    },
    {
        "id": "relationship:self-check-versus-independent-qa",
        "type": "conflict",
        "source_unit_id": "subagent-driven-development:unit-015",
        "target_unit_id": "qao-rule-never-fix-bugs-boundary",
        "cluster_id": "cluster:developer-self-check-and-fix",
        "resolution_status": "resolved",
        "applicability_conditions": {
            "source": {"execution_mode": "developer-self-check"},
            "target": {"execution_mode": "independent-qa"},
        },
        "evidence": (
            "The developer self-check explicitly requires fixing discovered issues before reporting, "
            "while independent black-box QA explicitly forbids reading or editing source and remains report-only."
        ),
        "design_case": (
            "Route by execution identity before inspection: developer self-check may repair its own work; "
            "independent QA records evidence and never repairs the product."
        ),
        "resolution": (
            "Preserve both capabilities and select exactly one permission contract from the execution identity: "
            "developer-self-check may modify and fix; independent-qa is report-only and may not modify."
        ),
    },
    {
        "id": "relationship:go-decision-before-prd",
        "type": "strong-dependency",
        "source_unit_id": "discovery-process:unit-032",
        "target_unit_id": "discovery-process:unit-034",
        "cluster_id": "cluster:requirements-and-delivery-contract",
    },
    {
        "id": "relationship:solution-validation-before-decision",
        "type": "strong-dependency",
        "source_unit_id": "discovery-process:unit-031",
        "target_unit_id": "discovery-process:unit-032",
        "cluster_id": "cluster:results-analysis-and-decision-readout",
    },
    {
        "id": "relationship:go-decision-before-epic-hypotheses",
        "type": "conditional-variant",
        "source_unit_id": "discovery-process:unit-032",
        "target_unit_id": "discovery-process:unit-033",
        "cluster_id": "cluster:results-analysis-and-decision-readout",
        "condition": {
            "source": {
                "applicability": "Use the decision gate to select GO, PIVOT, or KILL after problem, solution, strategic-fit, and feasibility evidence is reviewed."
            },
            "target": {
                "applicability": "Use this branch only after the decision is GO; skip it for PIVOT or KILL."
            },
        },
    },
    {
        "id": "relationship:experiment-design-before-execution",
        "type": "strong-dependency",
        "source_unit_id": "discovery-process:unit-028",
        "target_unit_id": "discovery-process:unit-029",
        "cluster_id": "cluster:solution-hypothesis-and-experiment-design",
    },
    {
        "id": "relationship:ost-before-learning-experiment",
        "type": "complementary",
        "source_unit_id": "discovery-process:unit-026",
        "target_unit_id": "discovery-process:unit-028",
        "cluster_id": "cluster:solution-hypothesis-and-experiment-design",
    },
    {
        "id": "relationship:iron-law-before-red-test",
        "type": "strong-dependency",
        "source_unit_id": "test-driven-development:unit-003",
        "target_unit_id": "test-driven-development:unit-005",
        "cluster_id": "cluster:tdd-change-loop",
    },
    {
        "id": "relationship:tdd-cycle-and-completion-evidence",
        "type": "complementary",
        "source_unit_id": "test-driven-development:unit-004",
        "target_unit_id": "verification-before-completion:unit-002",
        "cluster_id": "cluster:tdd-change-loop",
    },
    {
        "id": "relationship:fresh-evidence-before-ship",
        "type": "strong-dependency",
        "source_unit_id": "verification-before-completion:unit-002",
        "target_unit_id": "ship:unit-006",
        "cluster_id": "cluster:completion-evidence-gate",
    },
    {
        "id": "relationship:baseline-before-post-deploy-verification",
        "type": "strong-dependency",
        "source_unit_id": "canary:unit-002",
        "target_unit_id": "land-and-deploy:unit-008",
        "cluster_id": "cluster:baseline-regression-control",
    },
    {
        "id": "relationship:baseline-capture-before-update",
        "type": "complementary",
        "source_unit_id": "canary:unit-002",
        "target_unit_id": "canary:unit-008",
        "cluster_id": "cluster:baseline-regression-control",
    },
    {
        "id": "relationship:pets-failure-and-timing-contrast",
        "type": "complementary",
        "source_unit_id": "competitive-strategy:unit-069",
        "target_unit_id": "competitive-strategy:unit-070",
        "cluster_id": "cluster:competitive-case-library",
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the audited Phase 4 capability map"
    )
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--units-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label}: {type(error).__name__}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label}: top level must be an object")
    return value


def valid_skill_name(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value not in {".", ".."}
        and "/" not in value
        and "\\" not in value
        and ":" not in value
    )


def included_skills(inventory: dict[str, object]) -> list[str]:
    entries = inventory.get("catalog_entries")
    if not isinstance(entries, list):
        raise ValueError("inventory: catalog_entries must be a list")
    skills = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"inventory: catalog entry {index} must be an object")
        if entry.get("scope") not in INVENTORY_SCOPES:
            raise ValueError(f"inventory: invalid scope at entry {index}")
        if entry.get("resolution") not in INVENTORY_RESOLUTIONS:
            raise ValueError(f"inventory: invalid resolution at entry {index}")
        skill = entry.get("skill")
        if not valid_skill_name(skill):
            raise ValueError(f"inventory: invalid skill at entry {index}")
        if entry["scope"] == "included" and entry["resolution"] == "resolved":
            skills.append(skill)
    if len(skills) != len(set(skills)):
        raise ValueError("inventory: duplicate included skill")
    return sorted(skills)


def unit_id_belongs_to_skill(unit_id: str, skill: str) -> bool:
    if unit_id == "land-and-deploy:unit-0010" and skill == "land-and-deploy":
        return True
    if re.fullmatch(rf"{re.escape(skill)}:unit-\d{{3}}", unit_id):
        return True
    prefix = NONSTANDARD_UNIT_PREFIXES.get(skill)
    return prefix is not None and unit_id.startswith(prefix) and unit_id in UNIT_OVERRIDES


def load_units(units_root: Path, skills: list[str]) -> dict[str, dict[str, object]]:
    units: dict[str, dict[str, object]] = {}
    for skill in skills:
        path = units_root / f"{skill}.jsonl"
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            raise ValueError(f"units:{skill}: {type(error).__name__}") from error
        for line_number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                unit = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"units:{skill}:{line_number}: {error.msg}"
                ) from error
            if not isinstance(unit, dict):
                raise ValueError(f"units:{skill}:{line_number}: record must be an object")
            unit_id = unit.get("id")
            if not isinstance(unit_id, str) or not unit_id.strip():
                raise ValueError(f"units:{skill}:{line_number}: invalid id")
            if not unit_id_belongs_to_skill(unit_id, skill):
                raise ValueError(
                    f"units:{skill}:{line_number}: id does not belong to skill: {unit_id}"
                )
            if unit_id in units:
                raise ValueError(f"duplicate unit: {unit_id}")
            units[unit_id] = unit
    return units


def validate_cluster_definitions() -> None:
    text_fields = {
        "candidate_responsibility",
        "input_boundary",
        "output_boundary",
    }
    dependency_fields = {
        "upstream_dependencies": "upstream",
        "downstream_dependencies": "downstream",
    }
    for cluster_id, metadata in CLUSTERS.items():
        for field in text_fields:
            value = metadata.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"cluster {cluster_id} uses invalid {field}")
        for field, label in dependency_fields.items():
            values = metadata.get(field)
            if not isinstance(values, list):
                raise ValueError(f"cluster {cluster_id} uses invalid {label} dependencies")
            if len(values) != len(set(values)):
                raise ValueError(f"cluster {cluster_id} repeats a {label} dependency")
            for dependency in values:
                if dependency == cluster_id:
                    raise ValueError(f"cluster {cluster_id} uses itself as {label} dependency")
                if dependency not in CLUSTERS:
                    raise ValueError(
                        f"cluster {cluster_id} uses unknown {label} dependency: {dependency}"
                    )


def validate_unit_ranges(skills: list[str], units: dict[str, dict[str, object]]) -> None:
    numeric_skills = set(skills) - set(NONSTANDARD_UNIT_PREFIXES)
    if set(UNIT_RANGES) != numeric_skills:
        missing = sorted(numeric_skills - set(UNIT_RANGES))
        stale = sorted(set(UNIT_RANGES) - numeric_skills)
        detail = ", ".join(
            part
            for part in (
                f"missing {','.join(missing)}" if missing else "",
                f"stale {','.join(stale)}" if stale else "",
            )
            if part
        )
        raise ValueError(f"unit range skill mismatch: {detail}")

    expected_numbers = {}
    for skill, ranges in UNIT_RANGES.items():
        numbers = set()
        for start, end, cluster_id in ranges:
            if type(start) is not int or type(end) is not int or start < 1 or end < start:
                raise ValueError(f"invalid unit range: {skill}:{start}-{end}")
            if cluster_id not in CLUSTERS:
                raise ValueError(f"unit range {skill}:{start}-{end} uses unknown cluster: {cluster_id}")
            for number in range(start, end + 1):
                if number in numbers:
                    raise ValueError(f"overlapping unit range: {skill}:{number}")
                numbers.add(number)
        expected_numbers[skill] = numbers

    observed_numbers = {skill: set() for skill in numeric_skills}
    for unit_id in units:
        skill, separator, suffix = unit_id.partition(":unit-")
        if separator and skill in observed_numbers:
            observed_numbers[skill].add(int(suffix))
    for skill in sorted(numeric_skills):
        if observed_numbers[skill] != expected_numbers[skill]:
            missing = sorted(expected_numbers[skill] - observed_numbers[skill])
            extra = sorted(observed_numbers[skill] - expected_numbers[skill])
            raise ValueError(
                f"unit range coverage mismatch: {skill}:missing={missing}:extra={extra}"
            )


def cluster_for_unit(unit_id: str) -> str:
    override = UNIT_OVERRIDES.get(unit_id)
    if override is not None:
        return override
    skill, separator, suffix = unit_id.partition(":unit-")
    if not separator or not suffix.isdigit():
        raise ValueError(f"unmapped unit: {unit_id}")
    number = int(suffix)
    matches = [
        cluster_id
        for start, end, cluster_id in UNIT_RANGES.get(skill, ())
        if start <= number <= end
    ]
    if len(matches) != 1:
        reason = "unmapped" if not matches else "multiply mapped"
        raise ValueError(f"{reason} unit: {unit_id}")
    return matches[0]


def build_relationships(
    units: dict[str, dict[str, object]],
    cluster_by_unit: dict[str, str],
) -> list[dict[str, object]]:
    valid_types = {
        "duplicate",
        "complementary",
        "conditional-variant",
        "conflict",
        "strong-dependency",
    }
    seen_ids = set()
    seen_edges = set()
    relationships = []
    for relationship in RELATIONSHIPS:
        relationship_id = relationship.get("id")
        if not isinstance(relationship_id, str) or not relationship_id.strip():
            raise ValueError("relationship uses invalid id")
        if relationship_id in seen_ids:
            raise ValueError(f"duplicate relationship id: {relationship_id}")
        seen_ids.add(relationship_id)

        kind = relationship.get("type")
        if kind not in valid_types:
            raise ValueError(f"relationship {relationship_id} uses invalid type: {kind}")
        source = relationship.get("source_unit_id")
        target = relationship.get("target_unit_id")
        for unit_id in (source, target):
            if not isinstance(unit_id, str) or unit_id not in units:
                raise ValueError(
                    f"relationship {relationship_id} uses unknown unit: {unit_id}"
                )
        if source == target:
            raise ValueError(f"relationship {relationship_id} is self-referential")

        cluster_id = relationship.get("cluster_id")
        if cluster_id not in CLUSTERS:
            raise ValueError(
                f"relationship {relationship_id} uses unknown cluster: {cluster_id}"
            )
        if cluster_id not in {cluster_by_unit[source], cluster_by_unit[target]}:
            raise ValueError(
                f"relationship {relationship_id} uses unrelated cluster: {cluster_id}"
            )

        endpoints = (source, target) if kind == "strong-dependency" else tuple(
            sorted((source, target))
        )
        edge = (kind, *endpoints)
        if edge in seen_edges:
            raise ValueError(f"duplicate relationship edge: {relationship_id}")
        seen_edges.add(edge)

        generated = dict(relationship)
        if kind == "conflict":
            for side, unit_id in (("source", source), ("target", target)):
                excerpt = units[unit_id].get("raw_excerpt")
                if not isinstance(excerpt, str) or not excerpt.strip():
                    raise ValueError(
                        f"relationship {relationship_id} uses unit without raw excerpt: {unit_id}"
                    )
                generated[f"{side}_excerpt"] = excerpt
        relationships.append(generated)
    return sorted(relationships, key=lambda relationship: str(relationship["id"]))


def build_capability_map(
    inventory_path: Path,
    units_root: Path,
) -> dict[str, object]:
    validate_cluster_definitions()
    inventory = load_json_object(inventory_path, "inventory")
    skills = included_skills(inventory)
    units = load_units(units_root, skills)
    validate_unit_ranges(skills, units)
    stale_overrides = sorted(set(UNIT_OVERRIDES) - set(units))
    if stale_overrides:
        raise ValueError(f"stale unit override: {', '.join(stale_overrides)}")

    members = {cluster_id: [] for cluster_id in CLUSTERS}
    cluster_by_unit = {}
    for unit_id in sorted(units):
        cluster_id = cluster_for_unit(unit_id)
        if cluster_id not in CLUSTERS:
            raise ValueError(f"unit {unit_id} uses unknown cluster: {cluster_id}")
        members[cluster_id].append(unit_id)
        cluster_by_unit[unit_id] = cluster_id

    empty = sorted(cluster_id for cluster_id, unit_ids in members.items() if not unit_ids)
    if empty:
        raise ValueError(f"empty clusters: {', '.join(empty)}")

    clusters = []
    for cluster_id in sorted(CLUSTERS):
        cluster = {"id": cluster_id, **CLUSTERS[cluster_id]}
        cluster["unit_ids"] = members[cluster_id]
        clusters.append(cluster)

    return {
        "version": 1,
        "clusters": clusters,
        "relationships": build_relationships(units, cluster_by_unit),
    }


def write_atomic(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    args = parse_args()
    try:
        data = build_capability_map(args.inventory, args.units_root)
        write_atomic(args.output, data)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(
        f"Generated {len(data['clusters'])} clusters and "
        f"{len(data['relationships'])} relationships at {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
