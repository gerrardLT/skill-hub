#!/usr/bin/env python3
"""Compile the Capability Compiler V2 lifecycle taxonomy and candidate contracts."""
from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

DOMAINS=[
 ("domain:product-discovery-and-strategy","Product discovery and strategy","Evidence-backed problem discovery, market understanding, experiments, strategic choice, and human-owned prioritization."),
 ("domain:requirements-and-planning","Requirements and planning","Translate approved intent into traceable requirements, plans, governed artifacts, and executable handoffs."),
 ("domain:ux-ui-and-accessibility","UX, UI, and accessibility","Design complete user flows, interfaces, systems, interaction states, accessibility contracts, responsive behavior, and rendered review."),
 ("domain:architecture-data-api-and-security","Architecture, data, API, and security","Define system boundaries, data and API contracts, authorization, threat controls, reliability assumptions, and architecture decisions."),
 ("domain:implementation-and-code-quality","Implementation and code quality","Implement bounded changes with TDD, safe source mutation, debugging, code health, developer experience, and maintainable integration."),
 ("domain:testing-and-quality-assurance","Testing and quality assurance","Plan and execute independent, integration, browser, regression, accessibility, and completion verification without conflating review and repair identities."),
 ("domain:performance-and-reliability","Performance and reliability","Measure, diagnose, and improve web, application, cloud, and runtime performance, resilience, determinism, and readiness."),
 ("domain:delivery-deployment-and-release","Delivery, deployment, and release","Package, preflight, authorize, deploy, version, and verify changes with provider-specific adapters and no implicit remote writes."),
 ("domain:observability-operations-and-incidents","Observability, operations, and incidents","Instrument, observe, alert, investigate, canary, rollback, and coordinate incidents using bounded provider adapters."),
 ("domain:learning-retrospective-and-governance","Learning, retrospective, and governance","Preserve feedback, retrospectives, decisions, provenance, organizational learning, and governance for the next lifecycle pass."),
 ("domain:tool-runtime-and-artifact-support","Tool runtime and artifact support","Provide browser, model, context, document, and workflow runtime support without masquerading as user-facing product capability."),
]
STAGES=[
 ("stage:01-governance-intake",1,"Governance and intake","Bound authority, context, data governance, and routing before substantive work."),
 ("stage:02-discovery-research",2,"Discovery and research","Collect and validate user, market, system, and operational evidence."),
 ("stage:03-strategy-prioritization",3,"Strategy and prioritization","Choose evidence-backed direction while preserving human decision authority."),
 ("stage:04-requirements-planning",4,"Requirements and planning","Produce traceable requirements, specifications, plans, and handoffs."),
 ("stage:05-experience-design",5,"Experience design","Design flows, visual systems, interaction states, accessibility, and prototypes."),
 ("stage:06-architecture-risk-security",6,"Architecture, risk, and security","Define technical boundaries, data/API/security contracts, risks, and operational assumptions."),
 ("stage:07-implementation-integration",7,"Implementation and integration","Implement, integrate, debug, and self-check bounded source changes."),
 ("stage:08-verification-quality",8,"Verification and quality","Run independent review, tests, QA, regression, and evidence gates."),
 ("stage:09-performance-reliability",9,"Performance and reliability","Measure and improve performance, resilience, and deployment readiness."),
 ("stage:10-release-readiness",10,"Release readiness","Package and preflight a release without executing remote change."),
 ("stage:11-deployment-change",11,"Deployment change","Execute explicitly authorized remote deployment or configuration change."),
 ("stage:12-observation-canary",12,"Observation and canary","Observe production behavior, alerts, canaries, and post-deploy health."),
 ("stage:13-incident-recovery",13,"Incident and recovery","Investigate production failures, coordinate incidents, and execute rollback or recovery."),
 ("stage:14-learning-feedback",14,"Learning and feedback","Capture outcomes, retrospectives, decisions, and feedback for a new pass."),
 ("stage:15-tool-runtime-support",15,"Tool runtime support","Provide cross-cutting local runtime and artifact support; not a lifecycle approval step."),
]
DOMAIN_CLUSTERS={
 "domain:product-discovery-and-strategy":{
  "ai-product-opportunity-and-wedge","competitive-case-library","competitive-response-and-monitoring","customer-interview-execution","data-analysis-validation","decision-and-outcome-roadmapping","evidence-synthesis-and-opportunity-prioritization","market-positioning-and-competitive-power","market-segmentation-and-demand-intelligence","opportunity-prioritization-and-frameworks","persona-jtbd-and-journey-modeling","problem-framing-and-customer-research","qualitative-evidence-synthesis","research-planning-and-governance","results-analysis-and-decision-readout","solution-hypothesis-and-experiment-design","strategic-choice-and-differentiation","structural-power-and-moats"},
 "domain:requirements-and-planning":{"context-intake-and-routing","document-and-artifact-governance","facilitation-and-collaboration-protocols","implementation-planning-and-handoff","independent-plan-review","requirements-and-delivery-contract","risk-preflight-and-safety-governance","workflow-orchestration-and-lifecycle"},
 "domain:ux-ui-and-accessibility":{"accessibility-contracts-and-assistive-validation","ai-interaction-and-probabilistic-ux","content-copy-and-authentic-assets","cross-domain-ui-preflight-checklists","design-context-and-direction-contract","design-system-foundation-and-token-extraction","divergent-prototyping-and-variant-selection","evidence-based-ui-review-and-release-gates","existing-interface-redesign-and-preservation","external-design-token-extraction-and-normalization","interaction-states-forms-and-navigation","purposeful-motion-and-animation-engineering","rendered-ui-critique-and-release-disposition","responsive-layout-and-spatial-composition","ui-review-scope-and-evidence-acquisition","ui-task-routing-and-governance","visual-language-and-anti-template-controls"},
 "domain:architecture-data-api-and-security":{"ai-agent-autonomy-and-human-control","ai-capability-architecture-and-autonomy","ai-model-and-data-architecture","ai-safety-and-action-governance","architecture-candidate-reporting","architecture-deep-module-design","architecture-deepening-discovery","architecture-interface-alternative-evaluation","frontend-runtime-boundaries-and-dependency-safety"},
 "domain:implementation-and-code-quality":{"developer-self-check-and-fix","git-destructive-command-guard","plan-execution-control","root-cause-investigation","subagent-task-pipeline","tdd-change-loop"},
 "domain:testing-and-quality-assurance":{"baseline-regression-control","completion-evidence-gate","independent-blackbox-qa","independent-code-review","llm-quality-evaluation","playwright-test-engineering","safe-browser-probing","test-double-discipline","testing-portfolio-strategy","vitest-tooling","website-audit-remediation"},
 "domain:performance-and-reliability":{"frontend-rendering-and-interaction-performance","resilience-and-determinism","web-performance-diagnostics"},
 "domain:delivery-deployment-and-release":{"change-delivery-preflight","change-packaging-and-versioning","merge-and-deploy-readiness"},
 "domain:observability-operations-and-incidents":{"deployment-observation-and-recovery","incident-response-coordination","metrics-system-and-observability","production-canary-monitoring","release-rollback-execution"},
 "domain:learning-retrospective-and-governance":{"ai-organizational-adoption-and-leadership","engineering-retrospective-and-improvement","feedback-and-continuous-learning-loop","source-metadata-and-provenance"},
 "domain:tool-runtime-and-artifact-support":{"artifact-persistence-and-tool-actions","browser-session-and-runtime-configuration","reference-library-and-deferred-material","tool-runtime-readiness"},
}
STAGE_CLUSTERS={
 "stage:01-governance-intake":{"context-intake-and-routing","risk-preflight-and-safety-governance","ai-safety-and-action-governance"},
 "stage:02-discovery-research":{"ai-product-opportunity-and-wedge","competitive-case-library","competitive-response-and-monitoring","customer-interview-execution","data-analysis-validation","market-segmentation-and-demand-intelligence","persona-jtbd-and-journey-modeling","problem-framing-and-customer-research","qualitative-evidence-synthesis","research-planning-and-governance","solution-hypothesis-and-experiment-design"},
 "stage:03-strategy-prioritization":{"ai-organizational-adoption-and-leadership","decision-and-outcome-roadmapping","evidence-synthesis-and-opportunity-prioritization","market-positioning-and-competitive-power","opportunity-prioritization-and-frameworks","results-analysis-and-decision-readout","strategic-choice-and-differentiation","structural-power-and-moats"},
 "stage:04-requirements-planning":{"document-and-artifact-governance","facilitation-and-collaboration-protocols","implementation-planning-and-handoff","independent-plan-review","requirements-and-delivery-contract","workflow-orchestration-and-lifecycle"},
 "stage:05-experience-design":{"accessibility-contracts-and-assistive-validation","ai-interaction-and-probabilistic-ux","content-copy-and-authentic-assets","cross-domain-ui-preflight-checklists","design-context-and-direction-contract","design-system-foundation-and-token-extraction","divergent-prototyping-and-variant-selection","evidence-based-ui-review-and-release-gates","existing-interface-redesign-and-preservation","external-design-token-extraction-and-normalization","interaction-states-forms-and-navigation","purposeful-motion-and-animation-engineering","rendered-ui-critique-and-release-disposition","responsive-layout-and-spatial-composition","ui-review-scope-and-evidence-acquisition","ui-task-routing-and-governance","visual-language-and-anti-template-controls"},
 "stage:06-architecture-risk-security":{"ai-agent-autonomy-and-human-control","ai-capability-architecture-and-autonomy","ai-model-and-data-architecture","architecture-candidate-reporting","architecture-deep-module-design","architecture-deepening-discovery","architecture-interface-alternative-evaluation","frontend-runtime-boundaries-and-dependency-safety"},
 "stage:07-implementation-integration":{"developer-self-check-and-fix","git-destructive-command-guard","plan-execution-control","root-cause-investigation","subagent-task-pipeline","tdd-change-loop"},
 "stage:08-verification-quality":{"baseline-regression-control","completion-evidence-gate","independent-blackbox-qa","independent-code-review","llm-quality-evaluation","playwright-test-engineering","safe-browser-probing","test-double-discipline","testing-portfolio-strategy","vitest-tooling","website-audit-remediation"},
 "stage:09-performance-reliability":{"frontend-rendering-and-interaction-performance","resilience-and-determinism","web-performance-diagnostics"},
 "stage:10-release-readiness":{"change-delivery-preflight","change-packaging-and-versioning","merge-and-deploy-readiness"},
 "stage:11-deployment-change":set(),
 "stage:12-observation-canary":{"deployment-observation-and-recovery","metrics-system-and-observability","production-canary-monitoring"},
 "stage:13-incident-recovery":{"incident-response-coordination","release-rollback-execution"},
 "stage:14-learning-feedback":{"engineering-retrospective-and-improvement","feedback-and-continuous-learning-loop","source-metadata-and-provenance"},
 "stage:15-tool-runtime-support":{"artifact-persistence-and-tool-actions","browser-session-and-runtime-configuration","reference-library-and-deferred-material","tool-runtime-readiness"},
}
CLUSTER_CAPABILITY_OVERRIDES={
 "cluster:website-audit-remediation":"website-audit-assessment",
 "cluster:subagent-task-pipeline":"isolated-task-implementation",
 "cluster:deployment-observation-and-recovery":"deployment-observation",
}
SOURCE_FRAGMENT_SPLITS={
 "capability:pull-request-comment-response":["gstack/review/greptile-triage.md:97-111"],
 "capability:remote-pull-request-change":["gstack/ship/sections/pr-body.md:59-67","gstack/ship/sections/pr-body.md:180-225"],
 "capability:remote-pull-request-merge":["gstack/land-and-deploy/sections/merge-and-deploy.md:1-145"],
}
CANONICAL_UNIT_SPLITS={
 "capability:website-audit-remediation":["audit-website:unit-005"],
 "capability:workflow-orchestration-and-lifecycle":["subagent-driven-development:unit-001","subagent-driven-development:unit-003","subagent-driven-development:unit-004","subagent-driven-development:unit-007","subagent-driven-development:unit-008","subagent-driven-development:unit-010"],
 "capability:plan-execution-control":["subagent-driven-development:unit-002","subagent-driven-development:unit-006","subagent-driven-development:unit-009"],
 "capability:agent-workflow-runtime-support":["subagent-driven-development:unit-005"],
 "capability:implementation-spec-compliance-review":["subagent-driven-development:unit-017","subagent-driven-development:unit-018"],
}
CANONICAL_UNIT_TARGETS={unit_id:capability_id for capability_id,unit_ids in CANONICAL_UNIT_SPLITS.items() for unit_id in unit_ids}
SPLIT_CANONICAL_UNITS=set(CANONICAL_UNIT_TARGETS)
AUXILIARY_UNIT_SPLITS={
 "capability:workflow-orchestration-and-lifecycle":["skills/subagent-driven-development/SKILL.md:summary:parallel-tasks"],
}
SPLIT_AUXILIARY_UNITS={unit_id for unit_ids in AUXILIARY_UNIT_SPLITS.values() for unit_id in unit_ids}
NEW_CAPABILITIES={
 "production-trace-classification":("domain:observability-operations-and-incidents","stage:12-observation-canary","Classify authorized production LLM traces into evidence-backed behavior and failure categories.","Authorized trace scope, provider read access, time window, sampling policy, and data-governance boundary.","Trace classification, category evidence, sampling limitations, and unresolved observations.","external-read",7),
 "llm-evaluator-engineering":("domain:testing-and-quality-assurance","stage:08-verification-quality","Design and implement bounded offline or draft-online evaluators against an explicit quality contract.","Quality target, classified traces, evaluator mode, judge policy, local workspace, and data-governance boundary.","Evaluator definitions, executable checks, calibration evidence, and limitations; provider activation remains separately authorized.","workspace-write-local-exec",6),
 "evaluation-dataset-publication":("domain:testing-and-quality-assurance","stage:11-deployment-change","Create and publish a versioned evaluation dataset only after data-governance and explicit provider-write authorization.","Approved samples, schema, minimization and redaction policy, provider target, retention policy, and authorization.","Versioned dataset identity, publication receipt, hashes, governance evidence, and deletion path.","remote-write-authorized-only",6),
 "llm-experiment-execution":("domain:testing-and-quality-assurance","stage:11-deployment-change","Execute a reviewed LLM experiment against a frozen evaluator and dataset contract with explicit provider-write authorization.","Frozen experiment definition, dataset version, evaluator versions, provider target, budget, and authorization.","Experiment run identity, parameters, raw results, cost and duration evidence, and failure status.","remote-write-authorized-only",6),
 "evaluation-results-analysis":("domain:testing-and-quality-assurance","stage:12-observation-canary","Analyze frozen experiment results against declared metrics, variance, failure slices, and decision thresholds.","Experiment results, metric contract, baseline, statistical assumptions, and known data limits.","Evidence-bounded comparison, failure slices, uncertainty, and recommendation without automatic product approval.","local-exec",6),
 "production-llm-trace-root-cause-analysis":("domain:observability-operations-and-incidents","stage:13-incident-recovery","Diagnose production LLM traces to evidence-bounded root causes and remediation hypotheses.","Authorized trace data, incident scope, time window, privacy boundary, and service context.","Trace taxonomy, failure clusters, root-cause evidence, hypotheses, and unresolved gaps.","external-read",7),
 "kubernetes-application-deployment":("domain:delivery-deployment-and-release","stage:11-deployment-change","Deploy an application to an existing Kubernetes platform through provider-specific validated manifests and explicit authorization.","Application artifact, existing cluster context, provider adapter, manifests, credentials, and deployment authorization.","Validated manifests, deployment result, verification evidence, and rollback handle.","remote-write-authorized-only",7),
 "kubernetes-deployment-readiness":("domain:performance-and-reliability","stage:09-performance-reliability","Assess Kubernetes workload readiness, safeguards, identity, scaling, networking, and rollback prerequisites before deployment.","Cluster and workload configuration, provider controls, expected traffic, failure budget, and deployment plan.","Readiness findings, blocking safeguards, remediation plan, and residual risk.","external-read",7),
 "cloud-reliability-assessment":("domain:performance-and-reliability","stage:09-performance-reliability","Assess cloud architecture reliability against provider-specific failure, recovery, scaling, and operational practices.","Architecture evidence, provider, availability target, dependencies, traffic, and recovery objectives.","Reliability risks, prioritized remediations, verification plan, and accepted residual risk.","external-read",7),
 "observability-agent-installation":("domain:observability-operations-and-incidents","stage:11-deployment-change","Install an observability agent using an explicit platform variant and authorized remote change.","Platform, environment, provider account, credentials, desired instrumentation, and authorization.","Agent installation evidence, configuration, verification command, and rollback steps.","remote-write-authorized-only",7),
 "apm-instrumentation-enablement":("domain:observability-operations-and-incidents","stage:11-deployment-change","Enable APM instrumentation with platform-specific safeguards and no duplicate manual instrumentation.","Installed agent, service runtime, platform variant, environment, and authorization.","Instrumentation configuration, changed services, verification evidence, and rollback steps.","remote-write-authorized-only",7),
 "apm-instrumentation-verification":("domain:observability-operations-and-incidents","stage:12-observation-canary","Verify that APM instrumentation emits correct service, environment, version, and trace evidence.","Instrumented environment, expected service identity, provider read access, and observation window.","Verification verdict, missing signals, service identity findings, and next action.","external-read",7),
 "apm-instrumentation-troubleshooting":("domain:observability-operations-and-incidents","stage:13-incident-recovery","Troubleshoot missing or incorrect APM signals through platform-specific evidence and route remote fixes to the authorized installation or enablement capability.","Failed verification evidence, platform variant, service configuration, logs, and authority boundary.","Root cause, repair plan, handoff to an authorized mutating capability, and re-verification criteria.","external-read",7),
 "apm-onboarding-summary":("domain:observability-operations-and-incidents","stage:12-observation-canary","Summarize APM onboarding status, verified coverage, gaps, and owner actions without mutating systems.","Installation, enablement, verification, and troubleshooting evidence.","Service coverage summary, unresolved gaps, ownership, and next checks.","read-only",7),
 "service-identity-remapping":("domain:observability-operations-and-incidents","stage:11-deployment-change","Remap telemetry service identity through explicit provider configuration and collision checks.","Current service names, desired taxonomy, provider configuration, downstream dashboards, and authorization.","Remapping plan or applied configuration, affected signals, verification, and rollback.","remote-write-authorized-only",7),
 "log-observability-configuration":("domain:observability-operations-and-incidents","stage:11-deployment-change","Configure log collection, parsing, routing, retention, and sensitive-data controls using a provider adapter.","Log sources, schemas, provider, authorization, retention, redaction, and routing requirements.","Log pipeline configuration, validation evidence, governance checks, and rollback.","remote-write-authorized-only",7),
 "monitoring-and-alert-configuration":("domain:observability-operations-and-incidents","stage:11-deployment-change","Create or update monitors and alerts from explicit SLOs, thresholds, routing, and authorization.","Signal definition, threshold rationale, evaluation window, recipients, provider, and authorization.","Monitor or alert configuration, dry-run evidence, routing verification, and rollback.","remote-write-authorized-only",7),
 "web-hosting-deployment":("domain:delivery-deployment-and-release","stage:11-deployment-change","Deploy a web application through an explicitly selected hosting provider adapter and authorization gate.","Build artifact, provider project, environment, secrets boundary, deployment plan, and authorization.","Deployment result, URL, verification evidence, provider metadata, and rollback handle.","remote-write-authorized-only",7),
 "ci-pipeline-security-hardening":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Audit and harden CI workflows for least privilege, pinning, secret boundaries, injection, and supply-chain risk.","CI workflow files, repository policy, trust boundaries, permissions, and runner context.","Threat findings, hardened workflow candidate, verification, and residual risk.","workspace-write",5),
 "error-monitoring-issue-investigation":("domain:observability-operations-and-incidents","stage:13-incident-recovery","Investigate an error-monitoring issue from event evidence through root cause and bounded repair recommendation.","Issue identity, event context, release, environment, source access, and authority boundary.","Root-cause report, reproduction evidence, impacted releases, and remediation recommendation.","external-read",7),
 "ai-observability-configuration":("domain:observability-operations-and-incidents","stage:11-deployment-change","Configure AI or LLM monitoring with explicit data-governance and provider boundaries.","AI application, traces, sensitive-data policy, provider, evaluation signals, retention, and authorization.","Monitoring configuration, redaction controls, verification, and residual governance risk.","remote-write-authorized-only",7),
 "release-observability-configuration":("domain:observability-operations-and-incidents","stage:11-deployment-change","Configure release and commit association for observability using an explicit provider adapter.","Release naming, repository, build metadata, provider project, credentials, and authorization.","Release configuration, association evidence, verification, and rollback.","remote-write-authorized-only",7),
 "edge-worker-deployment":("domain:delivery-deployment-and-release","stage:11-deployment-change","Build, preflight, and explicitly authorize deployment of edge workers through a provider adapter.","Worker source, environment bindings, provider account, compatibility target, and authorization.","Build evidence, deployment result, route verification, and rollback handle.","remote-write-authorized-only",7),
 "test-case-design-and-export":("domain:testing-and-quality-assurance","stage:08-verification-quality","Derive executable test cases, coverage, data, priority, and consumer-specific export formats from approved requirements.","Approved requirements, risk profile, platform, test level, data constraints, and downstream format.","Traceable test cases, coverage gaps, quality score, data plan, and selected export.","workspace-write",6),
 "website-audit-remediation":("domain:implementation-and-code-quality","stage:07-implementation-integration","Repair an approved, source-mapped website audit finding without performing or approving the independent re-audit.","Confirmed audit finding, source mapping, approved repair scope, workspace, and local verification command.","Bounded source patch, local regression evidence, and handoff for independent website re-audit.","workspace-write-local-exec",6),
 "implementation-spec-compliance-review":("domain:testing-and-quality-assurance","stage:08-verification-quality","Independently compare an implementation to its approved requirements and identify missing, extra, or misunderstood behavior without editing source.","Approved task requirements, implementation diff, source snapshot, and implementer report as an untrusted claim.","Spec-compliance verdict with file and line evidence for every missing, extra, or misunderstood behavior.","read-only",6),
 "browser-agent-pairing-provisioning":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Provision scoped, expiring browser-pairing credentials for one selected local or remote agent after explicit local-system and network-exposure authorization.","Running browser daemon, selected agent, local or remote mode, scope restrictions, credential retention, and explicit authorization.","Scoped pairing identity, expiry, connection instructions or local config receipt, revocation command, and exposure boundary.","local-system-write-external-session-authorized-only",6),
 "browser-agent-pairing-verification":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Verify and diagnose a browser-agent pairing without creating credentials, widening scope, restarting the daemon, or changing configuration.","Pairing identity, browser status, expected scope, target platform, and permitted external read boundary.","Connection verdict, observed scope, diagnosis, and bounded re-provisioning recommendation.","local-exec-external-read",6),
 "local-branch-integration":("domain:implementation-and-code-quality","stage:07-implementation-integration","Integrate an approved base branch into an isolated local change branch, surface conflicts, and preserve a recoverable pre-integration reference without remote writes.","Isolated worktree, change branch, approved base reference, clean-state evidence, and local mutation authority.","Integrated local branch or conflict report, before and after refs, changed-file evidence, and recovery command.","workspace-write-local-exec",6),
 "remote-git-push":("domain:delivery-deployment-and-release","stage:11-deployment-change","Push one verified local branch to its approved remote ref without force after explicit per-action authorization.","Verified source ref, approved remote and target ref, current authorization, credential boundary, and redaction result.","Push receipt, local and remote refs, verification, or fail-closed error without retry escalation.","remote-write-authorized-only",7),
 "remote-pull-request-change":("domain:delivery-deployment-and-release","stage:11-deployment-change","Create or update one pull or merge request from a verified pushed ref only after redaction and explicit per-action authorization.","Verified remote refs, approved base, title and body artifacts, redaction result, provider, and current authorization.","Pull or merge request identity, URL, exact title and body hashes, provider receipt, or fail-closed error.","remote-write-authorized-only",7),
 "remote-pull-request-merge":("domain:delivery-deployment-and-release","stage:11-deployment-change","Merge one identified pull request using an allowed repository method only after a fresh readiness gate and explicit per-action authorization.","Pull request identity, fresh CI and review evidence, mergeability, approved method, current authorization, and rollback plan.","Merge receipt and resulting ref, or a fail-closed readiness, conflict, permission, or provider error.","remote-write-authorized-only",7),
 "deployment-trigger-execution":("domain:delivery-deployment-and-release","stage:11-deployment-change","Trigger one approved deployment workflow or hook with frozen parameters and explicit per-action authorization; provider-specific deployment remains an adapter variant.","Release identity, reviewed deployment target, frozen parameters, provider or hook adapter, credentials, and current authorization.","Trigger receipt, run identity, parameters, provider status handle, and rollback handle.","remote-write-authorized-only",7),
 "test-runtime-bootstrap":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Install and configure one approved project-local test runtime, prove it with a real example, and restore dependency files if setup fails.","Project runtime, selected test framework, package policy, workspace authority, install command, and rollback baseline.","Minimal test configuration, one passing real-behavior test, dependency diff, and rollback or failure evidence.","workspace-write-local-exec",6),
 "provider-cli-authentication-setup":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Install or authenticate one provider CLI only after local-system and credential authorization without exposing secret values.","Provider CLI, version or install source, local-system authority, credential owner, authentication method, and cleanup policy.","Verified CLI identity and non-secret auth status, storage boundary, expiry or revocation path, and failure evidence.","local-system-write-external-session-authorized-only",6),
 "code-review-evidence-acquisition":("domain:testing-and-quality-assurance","stage:08-verification-quality","Acquire bounded local and provider read-only evidence needed for a code review without posting comments, changing findings, or editing source.","Change identity, base and head refs, approved provider read access, review scope, and untrusted-content boundary.","Frozen diff, CI and review-comment evidence, refs, hashes, and acquisition gaps.","local-exec-external-read",6),
 "pull-request-comment-response":("domain:delivery-deployment-and-release","stage:11-deployment-change","Post one evidence-backed response to an identified pull-request review comment after explicit per-action authorization without changing source or resolving unrelated threads.","Comment identity, verified finding classification, response artifact, evidence links, provider, and current authorization.","Posted response receipt and URL, or explicit no-post outcome and reason.","remote-write-authorized-only",7),
 "local-learning-persistence":("domain:learning-retrospective-and-governance","stage:14-learning-feedback","Persist one evidence-bounded local learning, metric, review outcome, or project context record under explicit retention, privacy, and deletion controls.","Validated record, project identity, local destination, privacy and retention policy, and local-system write authorization.","Persisted local record identity and hash, validation result, retention and deletion path, or explicit no-write outcome.","local-system-write-authorized-only",7),
 "local-git-guard-setup":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Install or configure an approved repository-local Git guard without changing tracked source, renaming committed hooks, or enabling it silently.","Repository Git-dir evidence, hooks-path classification, guard artifact, user consent, and local-system write authorization.","Guard installation receipt and verification, declined state, or safe refusal for a committed or custom hooks directory.","local-system-write-authorized-only",6),
 "canary-baseline-management":("domain:observability-operations-and-incidents","stage:12-observation-canary","Create or update canary baselines and evidence artifacts only for explicitly selected production pages without changing application source.","Approved URL and pages, external read authority, artifact directory, prior baseline, and baseline-write decision.","Baseline manifest, screenshots, signal values, hashes, and staleness boundary.","artifact-write-local-exec-external-read",7),
 "agent-workflow-runtime-support":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Provide shared session, preamble, consent, artifact-sync, checkpoint, and host-tool runtime mechanics once per workflow.","Session identity, host capabilities, local project, consent state, and runtime configuration.","Runtime state, bounded directives, artifact pointers, and degradation notices.","local-exec",6),
 "project-context-and-learning-store":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Save, restore, search, prune, and synchronize project context and learnings under explicit privacy and retention controls.","Project identity, context artifacts, privacy boundary, retention, synchronization mode, and local-system write authorization when persistence is requested.","Restorable context, learning records, search results, and deletion or sync evidence.","local-system-write-authorized-only",6),
 "browser-data-acquisition-runtime":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Provide authenticated browser, cookie, scraping, and page-capture runtime support without treating acquired data as automatically authorized.","Target URL, authentication authority, data-governance boundary, browser runtime, and extraction scope.","Captured evidence or structured data, provenance, access limits, and cleanup status.","external-read",6),
 "documentation-authoring":("domain:requirements-and-planning","stage:04-requirements-planning","Author one requested documentation type using evidence-grounded Diataxis intent, source links, and reviewable structure.","Approved source facts, audience, documentation type, scope, style, and output path.","A reference, explanation, how-to, or tutorial artifact with source links and validation notes.","workspace-write",3),
 "document-rendering-and-validation":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Render an approved document source into a target artifact and validate layout, accessibility, links, and output integrity.","Approved document source, renderer, format, template, accessibility target, and output path.","Rendered document or PDF, validation evidence, hashes, and residual rendering limitations.","workspace-write-local-exec",6),
 "release-documentation-maintenance":("domain:learning-retrospective-and-governance","stage:14-learning-feedback","Update release-facing documentation from an evidence-bounded shipped diff and preserve a coverage map.","Shipped change evidence, documentation inventory, audience, release metadata, and write authority.","Updated release documentation, blast-radius coverage, links, and verification evidence.","workspace-write-local-exec",7),
 "model-and-workflow-benchmarking":("domain:testing-and-quality-assurance","stage:08-verification-quality","Benchmark models or workflows against frozen cases, metrics, variance, cost, and evidence.","Frozen cases, candidate variants, metric contract, environment, and budget.","Comparable benchmark results, variance, regressions, recommendation, and artifacts.","local-exec",6),
 "plan-review-decision-synthesis":("domain:requirements-and-planning","stage:04-requirements-planning","Synthesize independent plan-review findings, preserve disagreements, classify reversible versus taste decisions, and surface human approval points.","Independent review findings, plan version, decision policy, authority, and unresolved questions.","Decision matrix, preserved dissent, proposed plan amendments, and explicit human decisions required.","workspace-write",3),
 "security-audit-and-threat-modeling":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Audit infrastructure, application, CI, dependency, secret, AI, and skill-supply-chain threats with evidence-bounded verification.","Architecture, code, dependencies, infrastructure evidence, trust boundaries, and test authorization.","Threat model, verified findings, severity, remediation plan, and residual risk.","local-exec",5),
 "data-and-api-contract-design":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Define concrete data schemas, migrations, invariants, API interfaces, request/response shapes, versioning, and compatibility before implementation.","Approved requirements, domain entities, existing persistence and interfaces, consistency needs, and compatibility constraints.","Reviewable data model and migration contract plus API/interface schemas, errors, versioning, and validation plan.","workspace-write",5),
 "authorization-and-permission-contracts":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Define and verify actors, roles, permissions, trust boundaries, tenant isolation, privileged paths, and deny-by-default behavior.","Actors, resources, operations, trust boundaries, tenancy model, authentication context, and risk policy.","Authorization matrix, enforcement points, negative cases, audit requirements, and residual risk.","workspace-write",5),
 "secrets-and-environment-governance":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Define and verify secret, credential, environment, output, retention, and rotation boundaries without exposing values.","Secret classes, environments, providers, CI/runtime paths, owners, rotation requirements, and authorization.","Secrets and environment contract, least-exposure controls, verification plan, and rotation or revocation procedure.","workspace-write",5),
 "developer-experience-assessment":("domain:testing-and-quality-assurance","stage:08-verification-quality","Measure a live contributor journey across setup, feedback loops, commands, errors, documentation, upgrades, and ecosystem touchpoints without editing the product.","Repository, runnable setup path, common tasks, errors, timings, and contributor context.","DX findings, time-to-first-success evidence, reproducible friction, and repair handoff.","local-exec",6),
 "developer-experience-plan-review":("domain:requirements-and-planning","stage:04-requirements-planning","Review a plan for developer-facing setup, API, CLI, SDK, documentation, upgrade, and feedback-loop quality without implementing fixes.","Plan, approved product scope, current developer journey evidence, constraints, and decision owners.","DX plan review, applicability decision, challenged assumptions, scored gaps, and recommended amendments.","read-only",3),
 "design-plan-review":("domain:requirements-and-planning","stage:04-requirements-planning","Review the design scope and evidence in a plan, identify missing states and visual decisions, and preserve taste choices for human approval.","Plan, UX scope, existing design system, user flows, constraints, and decision owners.","Design plan review, missing states, optional evidence mockups, taste decisions, and recommended amendments.","read-only",3),
 "change-scope-freeze":("domain:implementation-and-code-quality","stage:07-implementation-integration","Establish and release explicit file or directory mutation boundaries for a change.","Authorized scope, protected paths, change identity, and expiry condition.","Enforced scope boundary, violations, and unfreeze evidence.","workspace-write",6),
 "code-health-assessment":("domain:implementation-and-code-quality","stage:07-implementation-integration","Assess code health, hotspots, quality trends, and maintenance risks from repository evidence.","Repository, time window, quality signals, ownership, and exclusions.","Health dashboard, hotspots, trends, and prioritized maintenance actions.","read-only",6),
 "executive-plan-review":("domain:product-discovery-and-strategy","stage:03-strategy-prioritization","Review a plan for strategic leverage, scope, user value, business risk, and one-way decisions while leaving approval to humans.","Plan, evidence, product context, constraints, and decision owners.","Strategic review, challenged assumptions, options, and human decisions required.","read-only",3),
 "engineering-plan-review":("domain:architecture-data-api-and-security","stage:06-architecture-risk-security","Review a plan for architecture, interfaces, failure modes, data, security, operability, and implementation risk.","Approved requirements, plan, architecture context, constraints, and existing system evidence.","Engineering review, risks, alternatives, missing tests, and revised plan recommendations.","read-only",5),
 "qa-finding-triage":("domain:testing-and-quality-assurance","stage:08-verification-quality","Triage independently observed QA findings by reproducibility, severity, scope, ownership, and repair readiness without editing source.","QA findings, evidence, affected surface, release context, and severity policy.","Deduplicated finding set, severity, reproduction confidence, ownership, and repair handoff.","read-only",6),
 "defect-remediation":("domain:implementation-and-code-quality","stage:07-implementation-integration","Implement a bounded correction for a confirmed defect and add the smallest regression evidence that proves the repair.","Confirmed finding, reproduction evidence, source workspace, repair authority, and regression contract.","Source patch, regression test or executable check, local verification, and residual risk.","workspace-write-local-exec",6),
 "ui-remediation":("domain:implementation-and-code-quality","stage:07-implementation-integration","Implement authorized UI repairs from evidence while preserving design, accessibility, and platform contracts.","UI findings, source workspace, design system, platform variant, and write authority.","UI patch, tests, rendered evidence, and unresolved design risks.","workspace-write-local-exec",6),
 "mobile-platform-runtime-support":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Provide mobile build, simulator, synchronization, cleanup, and capture runtime support as provider variants.","Mobile project, platform tools, simulator or device, local authority, and cleanup boundary.","Runtime state, synchronized assets, captures, diagnostics, and cleanup evidence.","local-exec",6),
 "diagram-and-architecture-artifact-generation":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Generate traceable diagrams from approved architecture or process evidence without inventing system facts.","Approved source facts, diagram purpose, notation, audience, and output format.","Diagram artifact, source mapping, validation, and unresolved assumptions.","workspace-write",5),
 "deployment-environment-setup":("domain:delivery-deployment-and-release","stage:10-release-readiness","Prepare local deployment configuration, provider selection, environment boundaries, and dry-run evidence without deploying.","Application, providers, environments, secrets policy, target, and deployment constraints.","Deployment configuration, preflight result, required authorization, and rollback plan.","workspace-write",7),
 "workflow-skill-authoring":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Author and validate one workflow skill from a bounded capability contract, fixture, provenance, and trigger policy.","Capability contract, source evidence, runtime target, fixtures, tests, and package boundary.","Validated skill candidate, triggers, tests, provenance, and packaging evidence.","workspace-write-local-exec",6),
 "workflow-runtime-upgrade":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Upgrade an installed workflow runtime with version detection, backup, migration, verification, and rollback.","Installed runtime, target version, local-system write authorization, compatibility constraints, and rollback path.","Upgraded runtime, migration and verification evidence, or restored prior version.","local-system-write-authorized-only",6),
 "browser-authentication-setup":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Configure authorized browser authentication material locally without exposing credential values or granting unrelated browsing authority.","Browser profile, target origin, credential authority, local-system write authorization, retention, and deletion policy.","Configured authentication state, validation, storage boundary, expiry, and cleanup instructions.","local-system-write-authorized-only",6),
 "local-agent-memory-setup":("domain:tool-runtime-and-artifact-support","stage:15-tool-runtime-support","Initialize local agent memory, MCP, or indexing runtime with project isolation, privacy, and rollback controls.","Project identity, runtime target, privacy choice, local-system write authorization, and retention policy.","Initialized local memory runtime, health evidence, isolation boundary, and removal instructions.","local-system-write-authorized-only",6),
}
ROOT_DEFAULTS={
 "agent-observability-trace-rca":"production-llm-trace-root-cause-analysis",
 "azure-kubernetes":"kubernetes-application-deployment","azure-kubernetes/azure-kubernetes-app-deploy":"kubernetes-application-deployment","azure-kubernetes/azure-kubernetes-automatic-readiness":"kubernetes-deployment-readiness","azure-reliability":"cloud-reliability-assessment",
 "dd-apm":"apm-instrumentation-enablement","dd-apm/k8s-ssi/agent-install":"observability-agent-installation","dd-apm/linux-ssi/agent-install":"observability-agent-installation","dd-apm/k8s-ssi/enable-ssi":"apm-instrumentation-enablement","dd-apm/linux-ssi/enable-ssi":"apm-instrumentation-enablement","dd-apm/k8s-ssi/onboarding-summary":"apm-onboarding-summary","dd-apm/linux-ssi/onboarding-summary":"apm-onboarding-summary","dd-apm/k8s-ssi/troubleshoot-ssi":"apm-instrumentation-troubleshooting","dd-apm/linux-ssi/troubleshoot-ssi":"apm-instrumentation-troubleshooting","dd-apm/k8s-ssi/verify-ssi":"apm-instrumentation-verification","dd-apm/linux-ssi/verify-ssi":"apm-instrumentation-verification","dd-apm/service-remapping":"service-identity-remapping","dd-logs":"log-observability-configuration","dd-monitors":"monitoring-and-alert-configuration",
 "deploy-to-vercel":"web-hosting-deployment","github-actions-hardening":"ci-pipeline-security-hardening","sentry-create-alert":"monitoring-and-alert-configuration","sentry-debug-issue":"error-monitoring-issue-investigation","sentry-setup-ai-monitoring":"ai-observability-configuration","sentry-setup-releases":"release-observability-configuration","vercel-optimize":"web-performance-diagnostics","wrangler":"edge-worker-deployment","test-case-generator":"test-case-design-and-export",
 "gstack":"agent-workflow-runtime-support","gstack/benchmark":"model-and-workflow-benchmarking","gstack/benchmark-models":"model-and-workflow-benchmarking","gstack/cso":"security-audit-and-threat-modeling","gstack/learn":"project-context-and-learning-store","gstack/office-hours":"problem-framing-and-customer-research","gstack/openclaw/skills/gstack-openclaw-office-hours":"problem-framing-and-customer-research","gstack/openclaw/skills/gstack-openclaw-retro":"engineering-retrospective-and-improvement","gstack/pair-agent":"browser-agent-pairing-provisioning","gstack/plan-tune":"independent-plan-review","gstack/retro":"engineering-retrospective-and-improvement","gstack/spec":"requirements-and-delivery-contract",
 "gstack/canary":"production-canary-monitoring","gstack/careful":"git-destructive-command-guard","gstack/devex-review":"developer-experience-assessment","gstack/freeze":"change-scope-freeze","gstack/unfreeze":"change-scope-freeze","gstack/guard":"git-destructive-command-guard","gstack/health":"code-health-assessment","gstack/investigate":"root-cause-investigation","gstack/openclaw/skills/gstack-openclaw-investigate":"root-cause-investigation","gstack/land-and-deploy":"merge-and-deploy-readiness","gstack/openclaw/skills/gstack-openclaw-ceo-review":"executive-plan-review","gstack/plan-ceo-review":"executive-plan-review","gstack/plan-devex-review":"developer-experience-plan-review","gstack/plan-eng-review":"engineering-plan-review","gstack/qa-only":"independent-blackbox-qa","gstack/review":"independent-code-review","gstack/ship":"change-delivery-preflight",
 "gstack/design-consultation":"design-context-and-direction-contract","gstack/design-html":"divergent-prototyping-and-variant-selection","gstack/design-review":"rendered-ui-critique-and-release-disposition","gstack/design-shotgun":"divergent-prototyping-and-variant-selection","gstack/diagram":"diagram-and-architecture-artifact-generation","gstack/ios-clean":"mobile-platform-runtime-support","gstack/ios-design-review":"rendered-ui-critique-and-release-disposition","gstack/ios-fix":"ui-remediation","gstack/ios-qa":"independent-blackbox-qa","gstack/ios-sync":"mobile-platform-runtime-support","gstack/plan-design-review":"design-plan-review",
 "gstack/browse":"browser-data-acquisition-runtime","gstack/browser-skills/hackernews-frontpage":"browser-data-acquisition-runtime","gstack/codex":"independent-code-review","gstack/context-restore":"project-context-and-learning-store","gstack/context-save":"project-context-and-learning-store","gstack/document-generate":"documentation-authoring","gstack/document-release":"release-documentation-maintenance","gstack/gstack-upgrade":"workflow-runtime-upgrade","gstack/landing-report":"change-delivery-preflight","gstack/make-pdf":"document-rendering-and-validation","gstack/open-gstack-browser":"browser-data-acquisition-runtime","gstack/scrape":"browser-data-acquisition-runtime","gstack/setup-browser-cookies":"browser-authentication-setup","gstack/setup-deploy":"deployment-environment-setup","gstack/setup-gbrain":"local-agent-memory-setup","gstack/skillify":"workflow-skill-authoring","gstack/sync-gbrain":"project-context-and-learning-store",
}
RUNTIME_TITLES=("artifacts sync","plan status footer","context health","prior learnings","capture learnings","decision audit trail")
ATOM_CAPABILITY_OVERRIDES={
 "v2-root:gstack/spec:014:8-schema-api-shapes-and-data-models":"data-and-api-contract-design",
 "v2-root:gstack/cso:010:phase-1-attack-surface-census":"authorization-and-permission-contracts",
 "v2-root:github-actions-hardening:006:step-4-audit-permissions":"authorization-and-permission-contracts",
 "v2-root:github-actions-hardening:008:step-6-check-secret-and-output-handling":"secrets-and-environment-governance",
 "v2-root:gstack/pair-agent:012:step-5-verify-connection":"browser-agent-pairing-verification",
 "v2-root:gstack/pair-agent:013:troubleshooting":"browser-agent-pairing-verification",
 # Read-only review evidence, finding judgment, mutation, and persistence stay separate.
 "v2-root:gstack/review:008:step-1-check-branch":"code-review-evidence-acquisition",
 "v2-root:gstack/review:009:step-1-5-scope-drift-detection":"independent-code-review",
 "v2-root:gstack/review:010:step-2-read-the-checklist":"independent-code-review",
 "v2-root:gstack/review:011:step-2-5-check-for-greptile-review-comments":"code-review-evidence-acquisition",
 "v2-root:gstack/review:012:step-3-get-the-diff":"code-review-evidence-acquisition",
 "v2-root:gstack/review:013:step-3-4-workspace-aware-queue-status-advisory":"code-review-evidence-acquisition",
 "v2-root:gstack/review:014:step-3-5-slop-scan-advisory":"independent-code-review",
 "v2-root:gstack/review:016:step-4-critical-pass-core-review":"independent-code-review",
 "v2-root:gstack/review:019:step-5-0-cross-review-finding-dedup":"independent-code-review",
 "v2-root:gstack/review:020:step-5a-classify-each-finding":"independent-code-review",
 "v2-root:gstack/review:018:step-5-fix-first-review":"qa-finding-triage",
 "v2-root:gstack/review:021:step-5b-auto-fix-all-auto-fix-items":"defect-remediation",
 "v2-root:gstack/review:022:step-5c-batch-ask-about-ask-items":"qa-finding-triage",
 "v2-root:gstack/review:023:step-5d-apply-user-approved-fixes":"defect-remediation",
 "v2-root:gstack/review:024:step-5-5-todos-cross-reference":"independent-code-review",
 "v2-root:gstack/review:025:step-5-6-documentation-staleness-check":"independent-code-review",
 "v2-root:gstack/review:026:step-5-8-persist-eng-review-result":"local-learning-persistence",
 "v2-root:gstack/review:027:capture-learnings":"local-learning-persistence",
 "v2-root:gstack/codex:016:write-to-the-plan-file":"artifact-persistence-and-tool-actions",
 "v2-root:gstack/plan-ceo-review:015:0d-post-persist-ceo-plan-expansion-and-selective-expansion-only":"local-learning-persistence",
 "v2-root:gstack/plan-ceo-review:016:for-each-stale-plan-mv-gstack-projects-slug-ceo-plans-old-plan-md-gstack":"local-learning-persistence",
 "v2-root:gstack/health:013:step-5-persist-to-health-history":"local-learning-persistence",
 # Rendered design audit, test bootstrap, remediation, and reporting identities.
 "v2-root:gstack/design-review:007:setup":"tool-runtime-readiness",
 "v2-root:gstack/design-review:008:check-opt-out-marker":"ui-review-scope-and-evidence-acquisition",
 "v2-root:gstack/design-review:009:b4-install-and-configure":"test-runtime-bootstrap",
 "v2-root:gstack/design-review:010:b5-verify":"tool-runtime-readiness",
 "v2-root:gstack/design-review:011:check-ci-provider":"tool-runtime-readiness",
 "v2-root:gstack/design-review:012:design-setup-run-this-check-before-any-design-mockup-command":"design-context-and-direction-contract",
 "v2-root:gstack/design-review:014:phases-1-6-design-audit-baseline":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:015:modes":"ui-task-routing-and-governance",
 "v2-root:gstack/design-review:016:phase-1-first-impression":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:017:phase-2-design-system-extraction":"design-system-foundation-and-token-extraction",
 "v2-root:gstack/design-review:018:phase-3-page-by-page-visual-audit":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:019:design-audit-checklist-10-categories-80-items":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:020:phase-4-interaction-flow-review":"interaction-states-forms-and-navigation",
 "v2-root:gstack/design-review:021:phase-5-cross-page-consistency":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:022:phase-6-compile-report":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:023:phase-7-triage":"qa-finding-triage",
 "v2-root:gstack/design-review:024:phase-8-fix-loop":"ui-remediation",
 "v2-root:gstack/design-review:025:8e-5-regression-test-design-review-variant":"playwright-test-engineering",
 "v2-root:gstack/design-review:026:phase-9-final-design-audit":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:027:phase-10-report":"rendered-ui-critique-and-release-disposition",
 "v2-root:gstack/design-review:028:phase-11-todos-md-update":"artifact-persistence-and-tool-actions",
 "v2-root:gstack/design-review:029:capture-learnings":"local-learning-persistence",
 "v2-root:gstack/design-review:030:additional-rules-design-review-specific":"rendered-ui-critique-and-release-disposition",
 # Ship preparation, local packaging, remote push, and local metrics are separate.
 "v2-root:gstack/ship:008:step-0-9-apple-target-detection":"change-delivery-preflight",
 "v2-root:gstack/ship:009:step-1-pre-flight":"change-delivery-preflight",
 "v2-root:gstack/ship:011:step-2-distribution-pipeline-check":"change-delivery-preflight",
 "v2-root:gstack/ship:012:step-3-merge-the-base-branch-before-tests":"local-branch-integration",
 "v2-root:gstack/ship:013:step-12-version-bump-auto-decide":"change-packaging-and-versioning",
 "v2-root:gstack/ship:014:step-14-todos-md-auto-update":"artifact-persistence-and-tool-actions",
 "v2-root:gstack/ship:015:step-15-commit-bisectable-chunks":"change-packaging-and-versioning",
 "v2-root:gstack/ship:016:step-15-0-wip-commit-squash-continuous-checkpoint-mode-only":"change-packaging-and-versioning",
 "v2-root:gstack/ship:017:nothing-non-wip-to-preserve-verify-first":"change-packaging-and-versioning",
 "v2-root:gstack/ship:018:step-15-1-bisectable-commits":"change-packaging-and-versioning",
 "v2-root:gstack/ship:019:step-16-verification-gate":"completion-evidence-gate",
 "v2-root:gstack/ship:020:step-17-push":"remote-git-push",
 "v2-root:gstack/ship:021:never-get-a-silent-install-the-chaining-installer-would-rename-the-team-":"local-git-guard-setup",
 "v2-root:gstack/ship:022:step-20-persist-ship-metrics":"local-learning-persistence",
 "v2-root:gstack/ship:023:step-21-plan-tune-discoverability-nudge-first-successful-ship-only":"local-learning-persistence",
 "v2-root:gstack/ship:024:section-self-check-before-you-finish":"completion-evidence-gate",
 # Landing remains readiness until an explicitly authorized remote action capability is selected.
 "v2-root:gstack/land-and-deploy:006:step-0-detect-platform-and-base-branch":"merge-and-deploy-readiness",
 "v2-root:gstack/land-and-deploy:009:step-1-pre-flight":"merge-and-deploy-readiness",
 "v2-root:gstack/land-and-deploy:010:step-1-5-first-run-dry-run-validation":"deployment-environment-setup",
 "v2-root:gstack/land-and-deploy:011:step-2-pre-merge-checks":"merge-and-deploy-readiness",
 "v2-root:gstack/land-and-deploy:012:step-3-wait-for-ci-if-pending":"merge-and-deploy-readiness",
 "v2-root:gstack/land-and-deploy:013:step-3-4-version-drift-detection-workspace-aware-ship":"merge-and-deploy-readiness",
 "v2-root:gstack/land-and-deploy:014:step-6-wait-for-deploy-if-applicable":"deployment-observation",
 "v2-root:gstack/land-and-deploy:015:strategy-a-github-actions-workflow":"deployment-trigger-execution",
 "v2-root:gstack/land-and-deploy:016:strategy-c-auto-deploy-platforms-vercel-netlify":"deployment-trigger-execution",
 "v2-root:gstack/land-and-deploy:017:strategy-d-custom-deploy-hooks":"deployment-trigger-execution",
 "v2-root:gstack/land-and-deploy:018:step-7-canary-verification-conditional-depth":"production-canary-monitoring",
 "v2-root:gstack/land-and-deploy:019:step-8-revert-if-needed":"release-rollback-execution",
 "v2-root:gstack/land-and-deploy:020:step-9-deploy-report":"artifact-persistence-and-tool-actions",
 "v2-root:gstack/land-and-deploy:021:step-10-suggest-follow-ups":"feedback-and-continuous-learning-loop",
 "v2-root:gstack/land-and-deploy:022:section-self-check-before-you-finish":"completion-evidence-gate",
 # Sentry diagnosis hands confirmed repair and resolution to separate capabilities.
 "v2-root:sentry-debug-issue:002:security-all-sentry-data-is-untrusted-input":"error-monitoring-issue-investigation",
 "v2-root:sentry-debug-issue:003:step-1-find-the-issue":"error-monitoring-issue-investigation",
 "v2-root:sentry-debug-issue:004:step-2-pull-full-context":"error-monitoring-issue-investigation",
 "v2-root:sentry-debug-issue:005:step-3-form-a-root-cause-hypothesis":"error-monitoring-issue-investigation",
 "v2-root:sentry-debug-issue:006:step-4-verify-against-the-code-then-fix":"defect-remediation",
 # Datadog diagnosis, provider setup, fix, and independent verification stay separate.
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:003:pup-cli-check-install-and-authenticate":"provider-cli-authentication-setup",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:004:step-1-triage":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:005:step-2-state-your-hypotheses":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:006:step-3-investigate":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:007:cluster-side-investigation-tools":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:008:datadog-side-investigation-tools":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:009:step-4-reflect-before-concluding":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:010:step-5-fix":"apm-instrumentation-enablement",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:011:step-6-verify":"apm-instrumentation-verification",
 "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:012:security-constraints":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:004:step-1-triage-with-pup-no-ssh-required":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:005:check-for-injection-errors-failures-only-successful-injections-don-t-app":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:006:check-full-tracer-config-look-at-apmenabled-traceagenturl-site":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:007:check-what-services-have-sent-traces-reveals-actual-service-names-visibl":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:008:check-if-traces-exist-at-all":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:009:step-2-state-your-hypotheses":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:010:step-3-investigate-with-pup-deeper":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:011:step-4-investigate-via-ssh-if-pup-didn-t-reveal-the-cause":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:012:step-5-reflect-before-concluding":"apm-instrumentation-troubleshooting",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:013:step-6-fix":"apm-instrumentation-enablement",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:014:re-run-install-now-it-will-actually-download-and-extract":"observability-agent-installation",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:015:step-7-verify":"apm-instrumentation-verification",
 "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:016:security-constraints":"apm-instrumentation-troubleshooting",
 "v2-root:gstack/canary:009:phase-2-baseline-capture-baseline-mode":"canary-baseline-management",
 "v2-root:gstack/canary:011:phase-4-pre-deploy-snapshot-if-no-baseline-exists":"canary-baseline-management",
 "v2-root:gstack/canary:014:phase-7-baseline-update":"canary-baseline-management",
 # Agent observability phases; the end-to-end shell is a Phase 8 recipe candidate.
 "v2-root:agent-observability-eval-pipeline:006:phase-1-classify-mlapp-traces":"production-trace-classification",
 "v2-root:agent-observability-eval-pipeline:009:phase-2-root-cause-analysis":"production-llm-trace-root-cause-analysis",
 "v2-root:agent-observability-eval-pipeline:012:phase-3-bootstrap-evaluators":"llm-evaluator-engineering",
 "v2-root:agent-observability-eval-pipeline:013:operating-mode-resolution":"llm-evaluator-engineering",
 "v2-root:agent-observability-eval-pipeline:016:phase-4-create-and-publish-dataset":"evaluation-dataset-publication",
 "v2-root:agent-observability-eval-pipeline:019:phase-5-generate-and-run-experiment":"llm-experiment-execution",
 "v2-root:agent-observability-eval-pipeline:020:phase-5-review-the-generated-experiment-before-running":"llm-experiment-execution",
 "v2-root:agent-observability-eval-pipeline:023:phase-6-analyze-experiment":"evaluation-results-analysis",
 # Autoplan phases; orchestration and final ordering remain a Phase 8 recipe candidate.
 "v2-root:gstack/autoplan:002:self-check-before-emitting":"completion-evidence-gate",
 "v2-root:gstack/autoplan:004:context-health-soft-directive":"agent-workflow-runtime-support",
 "v2-root:gstack/autoplan:006:step-0-detect-platform-and-base-branch":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:008:the-6-decision-principles":"plan-review-decision-synthesis",
 "v2-root:gstack/autoplan:009:decision-classification":"plan-review-decision-synthesis",
 "v2-root:gstack/autoplan:010:phase-0-intake-restore-point":"project-context-and-learning-store",
 "v2-root:gstack/autoplan:011:step-1-capture-restore-point":"project-context-and-learning-store",
 "v2-root:gstack/autoplan:012:autoplan-restore-point":"project-context-and-learning-store",
 "v2-root:gstack/autoplan:013:original-plan-state":"project-context-and-learning-store",
 "v2-root:gstack/autoplan:014:step-2-read-context":"project-context-and-learning-store",
 "v2-root:gstack/autoplan:015:step-3-load-skill-files-from-disk":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:016:phase-0-5-codex-auth-version-preflight":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:017:check-codex-binary-if-missing-tag-the-degradation-matrix-and-continue":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:018:round-trip-model-probe-2477-auth-can-pass-while-the-account-s-configured":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:019:model-is-rejected-with-an-http-400-stale-model-pin-in-codex-config-toml":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:020:exit-2-broken-install-2742-spawn-enoent-non-executable-binary":"tool-runtime-readiness",
 "v2-root:gstack/autoplan:021:phase-1-ceo-review-strategy-scope":"executive-plan-review",
 "v2-root:gstack/autoplan:022:phase-2-design-review-conditional-skip-if-no-ui-scope":"design-plan-review",
 "v2-root:gstack/autoplan:023:phase-2-5-dx-review-conditional-skip-if-no-developer-facing-scope":"developer-experience-plan-review",
 "v2-root:gstack/autoplan:024:phase-3-eng-review-dual-voices-always-runs-always-last-the-required-gate":"engineering-plan-review",
 "v2-root:gstack/autoplan:025:decision-audit-trail":"plan-review-decision-synthesis",
 "v2-root:gstack/autoplan:026:decision-audit-trail":"source-metadata-and-provenance",
 "v2-root:gstack/autoplan:027:pre-gate-verification":"completion-evidence-gate",
 "v2-root:gstack/autoplan:028:phase-4-final-approval-gate":"plan-review-decision-synthesis",
 "v2-root:gstack/autoplan:038:completion-write-review-logs":"artifact-persistence-and-tool-actions",
 # QA phases; test-fix-verify orchestration remains a Phase 8 recipe candidate.
 "v2-root:gstack/qa:008:setup":"tool-runtime-readiness",
 "v2-root:gstack/qa:009:prior-learnings":"project-context-and-learning-store",
 "v2-root:gstack/qa:010:test-plan-context":"independent-blackbox-qa",
 "v2-root:gstack/qa:011:phases-1-6-qa-baseline":"independent-blackbox-qa",
 "v2-root:gstack/qa:012:phase-7-triage":"qa-finding-triage",
 "v2-root:gstack/qa:013:refresh-learnings-for-the-component-page-where-the-bug-lives":"project-context-and-learning-store",
 "v2-root:gstack/qa:014:phase-8-fix-loop":"defect-remediation",
 "v2-root:gstack/qa:015:phase-9-final-qa":"independent-blackbox-qa",
 "v2-root:gstack/qa:016:phase-10-report":"independent-blackbox-qa",
 "v2-root:gstack/qa:017:phase-11-todos-md-update":"artifact-persistence-and-tool-actions",
 "v2-root:gstack/qa:018:capture-learnings":"project-context-and-learning-store",
 "v2-root:gstack/qa:019:additional-rules-qa-specific":"independent-blackbox-qa",
}
RECIPE_ROOTS={"agent-observability-eval-pipeline","gstack/autoplan","gstack/qa","gstack/review","gstack/design-review","gstack/ship","gstack/land-and-deploy","sentry-debug-issue","dd-apm/k8s-ssi/troubleshoot-ssi","dd-apm/linux-ssi/troubleshoot-ssi"}
EXPLICIT_DEPENDENCIES=[
 ("agent-workflow-runtime-support","workflow-orchestration-and-lifecycle","optional","Shared runtime support is selected only by workflows that require its session and artifact protocol."),
 ("release-observability-configuration","ai-observability-configuration","optional","AI telemetry extends a configured release-observability boundary when the product contains model calls."),
 ("ai-observability-configuration","metrics-system-and-observability","hard","Configured AI telemetry must feed the production observation contract."),
 ("observability-agent-installation","apm-instrumentation-enablement","optional","APM enablement uses an installed provider agent when that adapter is selected."),
 ("apm-instrumentation-enablement","apm-instrumentation-verification","hard","Enabled instrumentation requires an independent telemetry verification pass."),
 ("apm-instrumentation-verification","apm-onboarding-summary","optional","The onboarding summary packages verified service evidence without changing instrumentation."),
 ("apm-instrumentation-troubleshooting","engineering-retrospective-and-improvement","hard","Instrumentation incident findings feed the next engineering improvement pass."),
 ("authorization-and-permission-contracts","tdd-change-loop","hard","Implementation must inherit approved authorization and permission boundaries."),
 ("browser-authentication-setup","browser-data-acquisition-runtime","optional","Authenticated browser acquisition is selected only for an authorized protected origin."),
 ("browser-data-acquisition-runtime","safe-browser-probing","optional","Browser probing may use the acquisition runtime without making it universally mandatory."),
 ("change-scope-freeze","change-delivery-preflight","hard","A frozen authorized change scope is required for release preflight evidence."),
 ("ci-pipeline-security-hardening","baseline-regression-control","hard","Hardened CI controls must be exercised by regression evidence before release."),
 ("cloud-reliability-assessment","change-delivery-preflight","hard","Cloud reliability risks must be resolved or accepted before release preflight."),
 ("code-health-assessment","independent-code-review","hard","Measured code-health findings inform independent code review."),
 ("data-and-api-contract-design","tdd-change-loop","hard","Implementation consumes approved data and API contracts."),
 ("defect-remediation","independent-blackbox-qa","hard","A repaired defect returns to independent QA for fresh verification."),
 ("deployment-environment-setup","web-hosting-deployment","hard","Web deployment requires an explicitly prepared target environment."),
 ("deployment-environment-setup","kubernetes-application-deployment","hard","Kubernetes deployment requires an explicitly prepared target environment."),
 ("design-plan-review","plan-review-decision-synthesis","optional","Design review findings are one independent input to plan decision synthesis."),
 ("developer-experience-assessment","engineering-retrospective-and-improvement","hard","Measured DX friction feeds the next engineering improvement pass."),
 ("developer-experience-plan-review","plan-review-decision-synthesis","optional","DX plan findings are one independent input to plan decision synthesis."),
 ("diagram-and-architecture-artifact-generation","architecture-candidate-reporting","optional","Architecture reporting may render bounded diagrams as supporting evidence."),
 ("documentation-authoring","document-rendering-and-validation","optional","Approved documentation can be rendered into a validated distributable artifact."),
 ("edge-worker-deployment","production-canary-monitoring","hard","An authorized edge deployment must enter bounded canary observation."),
 ("engineering-plan-review","plan-review-decision-synthesis","feedback","Engineering review can return a plan to synthesis without becoming a same-run upstream prerequisite."),
 ("error-monitoring-issue-investigation","engineering-retrospective-and-improvement","hard","Confirmed production issue evidence feeds engineering improvement."),
 ("llm-evaluator-engineering","evaluation-dataset-publication","hard","Dataset publication requires a frozen evaluator and quality contract."),
 ("evaluation-dataset-publication","llm-experiment-execution","optional","A provider experiment consumes the approved versioned dataset selected for that run."),
 ("llm-experiment-execution","evaluation-results-analysis","hard","Only frozen experiment results may enter result analysis."),
 ("evaluation-results-analysis","llm-evaluator-engineering","feedback","Analysis findings refine evaluators in a future evaluation pass."),
 ("executive-plan-review","plan-review-decision-synthesis","hard","Strategic plan findings feed the bounded synthesis step."),
 ("kubernetes-deployment-readiness","kubernetes-application-deployment","hard","A Kubernetes release must pass provider-specific readiness before deployment."),
 ("kubernetes-application-deployment","production-canary-monitoring","hard","An authorized Kubernetes deployment must enter bounded canary observation."),
 ("local-agent-memory-setup","project-context-and-learning-store","optional","Project context persistence may use an explicitly initialized local memory runtime."),
 ("log-observability-configuration","metrics-system-and-observability","hard","Configured logs contribute to the production observation contract."),
 ("mobile-platform-runtime-support","independent-blackbox-qa","optional","Mobile QA may select platform runtime support without imposing it on non-mobile work."),
 ("model-and-workflow-benchmarking","completion-evidence-gate","optional","Benchmark evidence may contribute to completion when the work includes model or workflow changes."),
 ("monitoring-and-alert-configuration","production-canary-monitoring","hard","Canary monitoring requires configured signals and alerts."),
 ("plan-review-decision-synthesis","requirements-and-delivery-contract","optional","Approved review synthesis can amend the requirements and delivery contract."),
 ("production-trace-classification","production-llm-trace-root-cause-analysis","hard","Root-cause analysis consumes classified production traces."),
 ("production-llm-trace-root-cause-analysis","feedback-and-continuous-learning-loop","hard","Trace root causes feed governed learning for the next lifecycle pass."),
 ("project-context-and-learning-store","workflow-orchestration-and-lifecycle","optional","Workflow orchestration may restore and persist governed project context."),
 ("qa-finding-triage","defect-remediation","feedback","Confirmed QA findings return to implementation under a separate write identity."),
 ("release-documentation-maintenance","source-metadata-and-provenance","optional","Release documentation preserves shipped provenance and coverage links."),
 ("release-observability-configuration","production-canary-monitoring","hard","Canary monitoring requires release identity and observability linkage."),
 ("secrets-and-environment-governance","tdd-change-loop","hard","Implementation must preserve approved secret and environment boundaries."),
 ("security-audit-and-threat-modeling","change-delivery-preflight","hard","Release preflight consumes unresolved security risks and accepted exceptions."),
 ("service-identity-remapping","apm-instrumentation-verification","hard","Remapped service identity must be verified in emitted telemetry."),
 ("test-case-design-and-export","independent-blackbox-qa","optional","Independent QA may consume traceable test cases while retaining exploratory scope."),
 ("ui-remediation","independent-blackbox-qa","hard","UI repairs require independent behavior and regression verification."),
 ("web-hosting-deployment","production-canary-monitoring","hard","An authorized web deployment must enter bounded canary observation."),
 ("website-audit-remediation","website-audit-assessment","hard","Website repairs return to the independent audit identity for fresh scoring."),
 ("workflow-runtime-upgrade","tool-runtime-readiness","optional","An upgraded runtime must be rechecked before dependent workflows use it."),
 ("workflow-skill-authoring","model-and-workflow-benchmarking","optional","A new workflow skill may enter bounded benchmarking before release."),
 ("isolated-task-implementation","implementation-spec-compliance-review","hard","A bounded implementation must pass independent specification compliance review."),
 ("implementation-spec-compliance-review","independent-code-review","optional","Code-quality review follows only after specification compliance passes."),
 ("browser-agent-pairing-provisioning","browser-agent-pairing-verification","optional","A newly provisioned browser pairing should be verified without widening or recreating it."),
 ("browser-agent-pairing-verification","browser-data-acquisition-runtime","optional","Verified paired agents may use the browser acquisition runtime within their granted scope."),
 ("local-branch-integration","change-delivery-preflight","hard","Release preflight evaluates the exact locally integrated change candidate."),
 ("change-packaging-and-versioning","remote-git-push","hard","Only a verified packaged ref may be pushed remotely."),
 ("remote-git-push","remote-pull-request-change","optional","A pull request can be created or updated only after the intended ref exists remotely."),
 ("merge-and-deploy-readiness","remote-pull-request-merge","hard","Remote merge consumes a fresh passing readiness decision."),
 ("remote-pull-request-merge","deployment-trigger-execution","optional","An explicit deploy trigger is selected only when merge does not already start the approved deployment."),
 ("deployment-trigger-execution","deployment-observation","hard","A triggered deployment enters provider observation until terminal state."),
 ("canary-baseline-management","production-canary-monitoring","optional","Production canary compares against an approved baseline when one exists."),
 ("code-review-evidence-acquisition","independent-code-review","optional","Independent review consumes a frozen evidence snapshot when provider evidence is in scope."),
 ("independent-code-review","pull-request-comment-response","optional","A verified review finding may produce one separately authorized provider response."),
 ("test-runtime-bootstrap","playwright-test-engineering","optional","Browser test engineering may consume an approved bootstrapped project test runtime."),
 ("provider-cli-authentication-setup","apm-instrumentation-troubleshooting","optional","Provider troubleshooting may consume separately authorized CLI authentication."),
 ("local-learning-persistence","feedback-and-continuous-learning-loop","optional","Persisted local evidence may feed the next governed learning pass."),
 ("local-git-guard-setup","remote-git-push","optional","An approved local guard can protect a later push but never authorizes it."),
]
MUTATING_CAPABILITIES={
 "capability:change-packaging-and-versioning","capability:ci-pipeline-security-hardening","capability:developer-self-check-and-fix","capability:plan-execution-control","capability:qa-repair-loop","capability:root-cause-investigation","capability:subagent-task-pipeline","capability:tdd-change-loop","capability:ui-remediation","capability:website-audit-remediation","capability:change-scope-freeze"
}
REMOTE_WRITE_CAPABILITIES={"capability:release-rollback-execution"}
PERMISSION_OVERRIDES={
 "capability:artifact-persistence-and-tool-actions":"workspace-write-local-exec",
 "capability:baseline-regression-control":"local-exec",
 "capability:change-delivery-preflight":"local-exec-external-read",
 "capability:code-health-assessment":"artifact-write-local-exec",
 "capability:completion-evidence-gate":"local-exec",
 "capability:deployment-observation":"artifact-write-local-exec-external-read",
 "capability:independent-blackbox-qa":"artifact-write-local-exec-external-read",
 "capability:merge-and-deploy-readiness":"local-exec-external-read",
 "capability:production-canary-monitoring":"artifact-write-local-exec-external-read",
 "capability:project-context-and-learning-store":"local-system-write-authorized-only",
 "capability:rendered-ui-critique-and-release-disposition":"artifact-write-local-exec-external-read",
 "capability:ui-review-scope-and-evidence-acquisition":"artifact-write-local-exec-external-read",
}
WORKSPACE_EXTERNAL_READ_CAPABILITIES=set()
PERMISSIONS={
 "read-only":{"model_tools":["read"],"host_actions":[],"external":"none","remote_write":False},
 "workspace-write":{"model_tools":["read","edit","write"],"host_actions":[],"external":"none","remote_write":False},
 "workspace-write-local-exec":{"model_tools":["read","edit","write"],"host_actions":["approved-local-commands"],"external":"none","remote_write":False},
 "workspace-write-external-read":{"model_tools":["read","edit","write"],"host_actions":["approved-provider-read"],"external":"read-only","remote_write":False},
 "workspace-write-local-exec-external-read":{"model_tools":["read","edit","write"],"host_actions":["approved-local-commands","approved-provider-read"],"external":"read-only","remote_write":False},
 "artifact-write-local-exec":{"model_tools":["read"],"host_actions":["approved-local-commands","approved-artifact-write"],"external":"none","remote_write":False},
 "artifact-write-local-exec-external-read":{"model_tools":["read"],"host_actions":["approved-local-commands","approved-artifact-write","approved-provider-read"],"external":"read-only","remote_write":False},
 "local-exec-external-read":{"model_tools":["read"],"host_actions":["approved-local-commands","approved-provider-read"],"external":"read-only","remote_write":False},
 "local-system-write-external-session-authorized-only":{"model_tools":["read"],"host_actions":["approved-local-system-write","approved-network-exposure","approved-credential-mint"],"external":"scoped-session-write-with-per-action-authorization","remote_write":True},
 "local-system-write-authorized-only":{"model_tools":["read"],"host_actions":["approved-local-system-write"],"external":"none","remote_write":False},
 "local-exec":{"model_tools":["read"],"host_actions":["approved-local-commands"],"external":"none","remote_write":False},
 "external-read":{"model_tools":["read"],"host_actions":["approved-provider-read"],"external":"read-only","remote_write":False},
 "remote-write-authorized-only":{"model_tools":["read"],"host_actions":["approved-provider-write"],"external":"write-with-per-action-authorization","remote_write":True},
}

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def cid(slug:str)->str:return "capability:"+slug
def variant_record(value:str)->dict[str,str]:
    provider,separator,variant=value.partition(":")
    if not variant:variant="workflow" if provider=="github-actions" else "default"
    environment="kubernetes" if "k8s" in variant or "kubernetes" in variant else "linux" if "linux" in variant else "ci" if provider=="github-actions" else "edge" if provider=="cloudflare" else "managed-cloud"
    return {"id":f"variant:{provider}:{variant}","provider":provider,"environment":environment,"source_root":variant,"applies_when":f"Select only when provider={provider} and environment={environment}; otherwise route to another evidenced adapter or return needs-input."}
def cluster_maps(clusters:list[dict[str,Any]])->tuple[dict[str,str],dict[str,str]]:
    domain={};stage={}
    for domain_id,names in DOMAIN_CLUSTERS.items():
        for name in names:domain["cluster:"+name]=domain_id
    for stage_id,names in STAGE_CLUSTERS.items():
        for name in names:stage["cluster:"+name]=stage_id
    expected={item["id"] for item in clusters}
    if set(domain)!=expected or set(stage)!=expected:raise ValueError(f"cluster mapping incomplete domain={sorted(expected-set(domain))} stage={sorted(expected-set(stage))}")
    return domain,stage
def permission_for(capability_id:str,domain_id:str,stage_id:str)->str:
    slug=capability_id.removeprefix("capability:")
    if capability_id in PERMISSION_OVERRIDES:return PERMISSION_OVERRIDES[capability_id]
    if capability_id in REMOTE_WRITE_CAPABILITIES:return "remote-write-authorized-only"
    if capability_id in WORKSPACE_EXTERNAL_READ_CAPABILITIES:return "workspace-write-external-read"
    if capability_id=="capability:website-audit-assessment":return "local-exec-external-read"
    if capability_id in MUTATING_CAPABILITIES:return "workspace-write-local-exec"
    if slug in {"independent-blackbox-qa","independent-code-review","independent-plan-review","rendered-ui-critique-and-release-disposition","ui-review-scope-and-evidence-acquisition"}:return "read-only"
    if stage_id in {"stage:02-discovery-research","stage:03-strategy-prioritization","stage:04-requirements-planning","stage:05-experience-design","stage:06-architecture-risk-security"}:return "workspace-write"
    if stage_id=="stage:07-implementation-integration":return "workspace-write-local-exec"
    if stage_id in {"stage:08-verification-quality","stage:09-performance-reliability"}:return "local-exec"
    if stage_id=="stage:10-release-readiness":return "read-only"
    if stage_id in {"stage:12-observation-canary","stage:13-incident-recovery"}:return "external-read"
    if stage_id=="stage:15-tool-runtime-support":return "local-exec"
    return "read-only"
def owner_phase(domain_id:str)->int:
    if domain_id in {"domain:product-discovery-and-strategy","domain:requirements-and-planning"}:return 3
    if domain_id=="domain:ux-ui-and-accessibility":return 4
    if domain_id=="domain:architecture-data-api-and-security":return 5
    if domain_id in {"domain:implementation-and-code-quality","domain:testing-and-quality-assurance","domain:performance-and-reliability","domain:tool-runtime-and-artifact-support"}:return 6
    return 7
def policy_refs(capability_id:str,domain_id:str)->list[str]:
    refs=["V2-DEC-001","V2-DEC-006"]
    if domain_id=="domain:ux-ui-and-accessibility":refs.append("V2-DEC-002")
    if domain_id=="domain:product-discovery-and-strategy":refs.extend(["V2-DEC-003","V2-DEC-005"])
    if any(term in capability_id for term in ("interview","feedback","data-analysis","llm-quality","ai-observability","agent-observability","trace-root","production-trace","evaluator","evaluation-dataset","llm-experiment")):refs.append("V2-DEC-004")
    return sorted(set(refs))
def compile_all(workspace:Path)->dict[str,Any]:
    clusters_data=load(workspace/"curation/clusters.json");clusters=clusters_data["clusters"];domain_map,stage_map=cluster_maps(clusters);stage_order={item[0]:item[1] for item in STAGES};comparisons=workspace/"curation/v2/comparisons";root_atoms=load(workspace/"curation/v2/units/root-derived.json");aux=load(workspace/"curation/v2/units/auxiliary.json")["units"]
    lifecycle=workspace/"curation/v2/lifecycle";cap_root=workspace/"curation/v2/capabilities";fusion=workspace/"curation/v2/fusion"
    for path in (lifecycle,cap_root,fusion):
        if path.exists():shutil.rmtree(path)
        path.mkdir(parents=True)
    domains={"schema_version":"2.0","domains":[{"id":i,"name":n,"responsibility":r} for i,n,r in DOMAINS]};write(lifecycle/"domains.json",domains)
    stages={"schema_version":"2.0","stages":[{"id":i,"order":o,"name":n,"responsibility":r,"mandatory":o<15} for i,o,n,r in STAGES],"hard_stage_edges":[{"source":STAGES[i][0],"target":STAGES[i+1][0]} for i in range(13)],"support_stage":"stage:15-tool-runtime-support"};write(lifecycle/"stages.json",stages)
    capabilities={};cluster_records=[]
    for cluster in clusters:
        capability_id=cid(CLUSTER_CAPABILITY_OVERRIDES.get(cluster["id"],cluster["id"].removeprefix("cluster:")));domain_id=domain_map[cluster["id"]];stage_id=stage_map[cluster["id"]];comparison=load(comparisons/(cluster["id"].removeprefix("cluster:")+".json"));permission=permission_for(capability_id,domain_id,stage_id)
        cluster_decision_id=f"V2-FUSION-{len(cluster_records)+1:04d}";unit_ids=[item for item in cluster["unit_ids"] if item not in SPLIT_CANONICAL_UNITS or CANONICAL_UNIT_TARGETS[item]==capability_id]
        responsibility=cluster["candidate_responsibility"];input_boundary=cluster["input_boundary"];output_boundary=cluster["output_boundary"];hard_gates=[rule["rule"] for rule in comparison["fusion_rules"]];source_evidence=list(comparison["evidence_citations"])
        if cluster["id"]=="cluster:website-audit-remediation":
            responsibility="Run bounded website audits, parse and prioritize findings, map them to source, and independently compare fresh results without editing the product.";input_boundary="A scannable site, audit CLI, permitted external read scope, and optional frozen baseline.";output_boundary="A categorized audit, source-mapped findings, score and regression evidence, and repair handoff.";hard_gates=["Do not edit source, publish reports, authenticate to an unapproved origin, or perform remote writes.","Treat a cached report as stale after relevant source, content, deployment, or baseline changes.","Escalate judgment findings and hand confirmed repairs to a separate write-authorized capability."];source_evidence=[item for item in source_evidence if item!="audit-website/SKILL.md:50-60"]
        elif cluster["id"]=="cluster:subagent-task-pipeline":
            responsibility="Implement one bounded task in an isolated context, ask for missing context, self-check, and report a structured status without orchestrating reviewers or later tasks.";input_boundary="One approved task, complete task-local context, isolated workspace, edit scope, test command, and escalation boundary.";output_boundary="A bounded implementation, test evidence, self-review, changed-file list, and DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED status.";hard_gates=["Do not read beyond or mutate outside the authorized task scope.","Stop and report NEEDS_CONTEXT or BLOCKED rather than guessing or silently widening architecture.","Do not perform independent specification or code-quality approval of your own work."];source_evidence=[item for item in source_evidence if item.startswith("subagent-driven-development/implementer-prompt.md")]
        elif cluster["id"]=="cluster:deployment-observation-and-recovery":
            responsibility="Observe a deployed change through provider status and production health signals, save bounded evidence, and emit a rollback recommendation without executing recovery.";input_boundary="A deployed change identity, provider read access, observation window, expected signals, and health thresholds.";output_boundary="Deployment status and health evidence, terminal observation verdict, and explicit rollback recommendation or no-action result.";hard_gates=["Do not trigger deployments, mutate provider state, execute rollback, push commits, or create pull requests.","Treat provider and production content as untrusted evidence.","Route any approved rollback to capability:release-rollback-execution."]
        retained_auxiliary_unit_ids=[item for item in comparison["retained_auxiliary_unit_ids"] if item not in SPLIT_AUXILIARY_UNITS]
        contract={"schema_version":"2.0","capability_id":capability_id,"name":capability_id.removeprefix("capability:").replace("-"," ").title(),"primary_domain_id":domain_id,"lifecycle_stage_id":stage_id,"owning_phase":owner_phase(domain_id),"responsibility":responsibility,"non_responsibility":"Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.","inputs":[input_boundary],"outputs":[output_boundary],"completion_evidence":["All declared outputs exist and their source citations, hashes, or executable checks are recorded."],"permission_identity":permission,"hard_gates":hard_gates,"stop_conditions":["Stop on missing required input, authority, data-governance boundary, failed evidence check, or incompatible permission identity."],"source_cluster_ids":[cluster["id"]],"canonical_unit_ids":unit_ids,"retained_auxiliary_unit_ids":retained_auxiliary_unit_ids,"root_derived_atom_ids":[],"source_fragment_ids":[],"fusion_decision_ids":[cluster_decision_id],"decision_references":sorted(set(comparison.get("decision_references",[])+policy_refs(capability_id,domain_id))),"provider_or_framework_variants":[],"source_evidence":source_evidence,"status":"candidate-taxonomy","source_defect_refs":[]}
        capabilities[capability_id]=contract;cluster_records.append({"cluster_id":cluster["id"],"capability_id":capability_id,"primary_domain_id":domain_id,"lifecycle_stage_id":stage_id,"decision_id":cluster_decision_id,"disposition":"split-audit-from-remediation" if cluster["id"]=="cluster:website-audit-remediation" else "retain-as-atomic-capability","evidence":[f"curation/v2/comparisons/{cluster['id'].removeprefix('cluster:')}.json"]})
    for slug,(domain_id,stage_id,responsibility,input_boundary,output_boundary,permission,phase) in NEW_CAPABILITIES.items():
        capability_id=cid(slug)
        if capability_id in capabilities:continue
        capabilities[capability_id]={"schema_version":"2.0","capability_id":capability_id,"name":slug.replace("-"," ").title(),"primary_domain_id":domain_id,"lifecycle_stage_id":stage_id,"owning_phase":phase,"responsibility":responsibility,"non_responsibility":"Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.","inputs":[input_boundary],"outputs":[output_boundary],"completion_evidence":["Source-derived atoms and provider or framework variants are cited; required checks and authorization evidence are recorded."],"permission_identity":permission,"hard_gates":["Fail closed on missing authority, credentials, source evidence, required data governance, or verification."],"stop_conditions":["Stop before destructive, external-write, merge, deploy, or production action without current explicit authorization."],"source_cluster_ids":[],"canonical_unit_ids":[],"retained_auxiliary_unit_ids":[],"root_derived_atom_ids":[],"source_fragment_ids":[],"fusion_decision_ids":[],"decision_references":policy_refs(capability_id,domain_id),"provider_or_framework_variants":[],"source_evidence":[],"status":"candidate-taxonomy","source_defect_refs":[]}
    for target_id,fragments in SOURCE_FRAGMENT_SPLITS.items():
        capabilities[target_id]["source_fragment_ids"].extend(fragments);capabilities[target_id]["source_evidence"].extend(fragments)
    canonical_units,_=load_units(workspace/"curation/units");canonical_by_id={item["id"]:item for item in canonical_units}
    for target_id,unit_ids in CANONICAL_UNIT_SPLITS.items():
        capabilities[target_id]["canonical_unit_ids"].extend(unit_ids)
        for unit_id in unit_ids:
            unit=canonical_by_id[unit_id];capabilities[target_id]["source_evidence"].append(f"{unit['source_path']}:{unit['origin_line_start']}-{unit['origin_line_end']}")
    auxiliary_by_id={item["id"]:item for item in aux}
    for target_id,unit_ids in AUXILIARY_UNIT_SPLITS.items():
        capabilities[target_id]["retained_auxiliary_unit_ids"].extend(unit_ids)
        for unit_id in unit_ids:
            unit=auxiliary_by_id[unit_id];capabilities[target_id]["source_evidence"].append(f"{unit['source_path']}:{unit['validated_line_start']}-{unit['validated_line_end']}")
    records=[];by_id={item["id"]:item for item in root_atoms["units"]};assigned={}
    for atom in root_atoms["units"]:
        atom_id=atom["id"]
        if atom["v2_disposition"]=="merge":continue
        root=atom["root_id"].removeprefix("skill-root:");title=atom["title"].casefold();disposition="assign";reason="Root-specific source atom assigned to its bounded atomic capability."
        if root.startswith("gstack/test/fixtures/"):
            disposition="exclude";capability_id=None;reason="Fixture root is test data, not a production capability."
        elif atom_id in ATOM_CAPABILITY_OVERRIDES:
            capability_id=cid(ATOM_CAPABILITY_OVERRIDES[atom_id]);reason="Exact source atom is assigned to a narrower atomic contract instead of remaining inside a monolithic source workflow."
        elif root in RECIPE_ROOTS:
            disposition="defer";capability_id=None;reason="This source atom is an orchestration shell, checkpoint, aggregate report, or whole-workflow responsibility; preserve it for Phase 8 Recipe synthesis rather than mislabeling it as an atomic capability."
        elif any(term in title for term in RUNTIME_TITLES):
            capability_id=cid("agent-workflow-runtime-support");reason="Shared runtime, context, learning, or artifact protocol is centralized once rather than copied into each gstack capability."
        elif "self-check" in title or "verification" in title and root.startswith("gstack/"):
            capability_id=cid("completion-evidence-gate");reason="Cross-cutting verification protocol maps to the completion evidence capability."
        else:
            slug=ROOT_DEFAULTS.get(root)
            if not slug:
                disposition="defer";capability_id=None;reason="No approved Phase 2 semantic capability mapping exists; preserve exact source evidence for later classification."
            else:capability_id=cid(slug)
        record={"atom_id":atom_id,"root_id":atom["root_id"],"source_path":atom["source_path"],"disposition":disposition,"capability_id":capability_id,"target_atom_id":None,"decision_id":f"V2-FUSION-{len(cluster_records)+len(records)+1:04d}","rationale":reason,"evidence":atom["evidence"]}
        records.append(record);assigned[atom_id]=record
        if disposition=="assign":
            capabilities[capability_id]["root_derived_atom_ids"].append(atom_id);capabilities[capability_id]["source_evidence"].append(atom["evidence"][0]);capabilities[capability_id]["fusion_decision_ids"].append(record["decision_id"])
            if root.startswith("dd-apm/"):capabilities[capability_id]["provider_or_framework_variants"].append("datadog:"+root.removeprefix("dd-apm/"))
            elif root.startswith("azure-kubernetes/") or root=="azure-kubernetes":capabilities[capability_id]["provider_or_framework_variants"].append("azure:"+root)
            elif root.startswith("sentry-"):capabilities[capability_id]["provider_or_framework_variants"].append("sentry:"+root)
            elif root in {"deploy-to-vercel","vercel-optimize"}:capabilities[capability_id]["provider_or_framework_variants"].append("vercel:"+root)
            elif root=="wrangler":capabilities[capability_id]["provider_or_framework_variants"].append("cloudflare:wrangler")
            elif root=="github-actions-hardening":capabilities[capability_id]["provider_or_framework_variants"].append("github-actions")
    for atom in root_atoms["units"]:
        if atom["v2_disposition"]!="merge":continue
        target=assigned.get(atom["target_unit_id"])
        record={"atom_id":atom["id"],"root_id":atom["root_id"],"source_path":atom["source_path"],"disposition":"merge","capability_id":target.get("capability_id") if target else None,"target_atom_id":atom["target_unit_id"],"decision_id":f"V2-FUSION-{len(cluster_records)+len(records)+1:04d}","rationale":"Exact source duplicate inherits the representative atom classification.","evidence":atom["decision_evidence"]}
        records.append(record)
        if record["capability_id"]:capabilities[record["capability_id"]]["fusion_decision_ids"].append(record["decision_id"])
    split_decisions=[]
    for unit_id,target_id in sorted(CANONICAL_UNIT_TARGETS.items()):
        unit=canonical_by_id[unit_id];decision={"id":f"V2-FUSION-{len(cluster_records)+len(records)+len(split_decisions)+1:04d}","kind":"canonical-unit-split","subject":unit_id,"disposition":"split-to-atomic-capability","target":target_id,"rationale":"The source unit belongs to a narrower atomic responsibility or permission identity than its legacy multi-stage cluster.","evidence":[f"{unit['source_path']}:{unit['origin_line_start']}-{unit['origin_line_end']}"]}
        split_decisions.append(decision);capabilities[target_id]["fusion_decision_ids"].append(decision["id"])
    for target_id,unit_ids in sorted(AUXILIARY_UNIT_SPLITS.items()):
        for unit_id in unit_ids:
            unit=auxiliary_by_id[unit_id];decision={"id":f"V2-FUSION-{len(cluster_records)+len(records)+len(split_decisions)+1:04d}","kind":"auxiliary-unit-split","subject":unit_id,"disposition":"split-to-atomic-capability","target":target_id,"rationale":"The retained auxiliary method describes orchestration policy rather than isolated implementation and is assigned to the atomic workflow router.","evidence":unit["decision_evidence"]}
            split_decisions.append(decision);capabilities[target_id]["fusion_decision_ids"].append(decision["id"])
    for target_id,fragments in sorted(SOURCE_FRAGMENT_SPLITS.items()):
        for fragment in fragments:
            decision={"id":f"V2-FUSION-{len(cluster_records)+len(records)+len(split_decisions)+1:04d}","kind":"source-fragment-split","subject":fragment,"disposition":"split-to-atomic-capability","target":target_id,"rationale":"A semantically reviewed support-file fragment carries a remote side effect that requires its own explicit authorization identity.","evidence":[fragment]}
            split_decisions.append(decision);capabilities[target_id]["fusion_decision_ids"].append(decision["id"])
    defects=load(workspace/"curation/v2/source-defects.json")["items"]
    for defect in defects:
        source_root=defect["source"];slug=ROOT_DEFAULTS.get(source_root)
        if slug and cid(slug) in capabilities:capabilities[cid(slug)]["source_defect_refs"].append(defect["id"])
    for capability in capabilities.values():
        capability["root_derived_atom_ids"]=sorted(set(capability["root_derived_atom_ids"]));capability["source_fragment_ids"]=sorted(set(capability["source_fragment_ids"]));capability["source_evidence"]=sorted(set(capability["source_evidence"]));capability["fusion_decision_ids"]=sorted(set(capability["fusion_decision_ids"]));capability["provider_or_framework_variants"]=[variant_record(value) for value in sorted(set(capability["provider_or_framework_variants"]))];capability["source_defect_refs"]=sorted(set(capability["source_defect_refs"]));write(cap_root/(capability["capability_id"].removeprefix("capability:")+".json"),capability)
    catalog={"schema_version":"2.0","capability_count":len(capabilities),"capabilities":[{"capability_id":c["capability_id"],"primary_domain_id":c["primary_domain_id"],"lifecycle_stage_id":c["lifecycle_stage_id"],"owning_phase":c["owning_phase"],"permission_identity":c["permission_identity"],"status":c["status"]} for c in sorted(capabilities.values(),key=lambda x:x["capability_id"])]};write(cap_root/"catalog.json",catalog)
    write(lifecycle/"cluster-map.json",{"schema_version":"2.0","count":len(cluster_records),"records":cluster_records})
    write(lifecycle/"root-atom-map.json",{"schema_version":"2.0","count":len(records),"counts":dict(Counter(item["disposition"] for item in records)),"records":sorted(records,key=lambda x:x["atom_id"])})
    edges=set()
    for cluster in clusters:
        for upstream in cluster["upstream_dependencies"]:edges.add((upstream,cluster["id"]))
        for downstream in cluster["downstream_dependencies"]:edges.add((cluster["id"],downstream))
    dep_records=[];hard=[]
    for index,(source_cluster,target_cluster) in enumerate(sorted(edges),1):
        s=cid(CLUSTER_CAPABILITY_OVERRIDES.get(source_cluster,source_cluster.removeprefix("cluster:")));t=cid(CLUSTER_CAPABILITY_OVERRIDES.get(target_cluster,target_cluster.removeprefix("cluster:")));so=stage_order[capabilities[s]["lifecycle_stage_id"]];to=stage_order[capabilities[t]["lifecycle_stage_id"]]
        kind="hard" if so<to else "feedback" if so>to else "optional"
        rationale="Earlier-stage evidence is a hard prerequisite for the later-stage capability." if kind=="hard" else "Later-stage evidence feeds a future lifecycle pass; it is not a same-run prerequisite." if kind=="feedback" else "Capabilities share a stage; preserve coordination without imposing an unproven order."
        record={"id":f"V2-DEPENDENCY-{index:04d}","source_capability_id":s,"target_capability_id":t,"kind":kind,"legacy_source_cluster_id":source_cluster,"legacy_target_cluster_id":target_cluster,"rationale":rationale,"evidence":[f"curation/clusters.json:{source_cluster}",f"curation/clusters.json:{target_cluster}"]};dep_records.append(record)
        if kind=="hard":hard.append({"source_capability_id":s,"target_capability_id":t,"decision_id":record["id"]})
    for source_slug,target_slug,kind,rationale in EXPLICIT_DEPENDENCIES:
        source_capability_id=cid(source_slug);target_capability_id=cid(target_slug);index=len(dep_records)+1
        record={"id":f"V2-DEPENDENCY-{index:04d}","source_capability_id":source_capability_id,"target_capability_id":target_capability_id,"kind":kind,"legacy_source_cluster_id":None,"legacy_target_cluster_id":None,"rationale":rationale,"evidence":["curation/v2/fusion/decisions.jsonl",*capabilities[source_capability_id]["source_evidence"][:1],*capabilities[target_capability_id]["source_evidence"][:1]]};dep_records.append(record)
        if kind=="hard":hard.append({"source_capability_id":source_capability_id,"target_capability_id":target_capability_id,"decision_id":record["id"]})
    write(lifecycle/"dependencies.json",{"schema_version":"2.0","records":dep_records,"hard_dag_edges":hard,"counts":dict(Counter(item["kind"] for item in dep_records))})
    handoffs=[]
    for index in range(13):
        source_stage=STAGES[index][0];target_stage=STAGES[index+1][0]
        handoffs.append({"id":f"V2-HANDOFF-{index+1:03d}","source_stage_id":source_stage,"target_stage_id":target_stage,"artifact_contract":["artifact identities and hashes","decision and authority record","completion evidence","known gaps and residual risk"],"invalidation":["source artifact hash changes","source decision or authority changes","source capability re-runs","source evidence becomes stale or fails verification"]})
    write(lifecycle/"handoffs.json",{"schema_version":"2.0","count":len(handoffs),"records":handoffs})
    phase_inputs={str(phase):sorted(c["capability_id"] for c in capabilities.values() if c["owning_phase"]==phase) for phase in range(3,8)}
    write(lifecycle/"phase-ownership.json",{"schema_version":"2.0","phases":phase_inputs,"counts":{phase:len(ids) for phase,ids in phase_inputs.items()}})
    decisions=[]
    for record in cluster_records:decisions.append({"id":record["decision_id"],"kind":"legacy-cluster-mapping","subject":record["cluster_id"],"disposition":record["disposition"],"target":record["capability_id"],"rationale":"Phase 1 comparison defines a bounded single responsibility; retain it as an atomic V2 candidate and add lifecycle, permission, and policy contracts.","evidence":record["evidence"]})
    for record in records:decisions.append({"id":record["decision_id"],"kind":"root-derived-atom","subject":record["atom_id"],"disposition":record["disposition"],"target":record["capability_id"] or record["target_atom_id"],"rationale":record["rationale"],"evidence":record["evidence"]})
    decisions.extend(split_decisions)
    (fusion/"decisions.jsonl").write_text("".join(json.dumps(item,ensure_ascii=False,sort_keys=True)+"\n" for item in decisions),encoding="utf-8",newline="\n")
    write(lifecycle/"permission-identities.json",{"schema_version":"2.0","identities":[{"id":key,**value} for key,value in PERMISSIONS.items()]})
    return {"gate":"capability-compiler-v2-lifecycle-compile","ok":True,"domains":len(DOMAINS),"stages":len(STAGES),"capabilities":len(capabilities),"legacy_clusters":len(cluster_records),"root_atom_records":len(records),"root_atom_dispositions":dict(Counter(item["disposition"] for item in records)),"dependency_decisions":dict(Counter(item["kind"] for item in dep_records))}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));a=p.parse_args();r=compile_all(a.workspace_root.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
