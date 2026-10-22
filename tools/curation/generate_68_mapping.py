"""Generate the consolidated 154 -> 68 mapping adhering strictly to fail-closed permissions."""
import json
from pathlib import Path
from collections import defaultdict

def main():
    root = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')
    idx = json.loads((root / 'skill-index.json').read_text(encoding='utf-8'))['skills']

    mapping = {}

    # Stage 01 (4 -> 3):
    mapping['context-intake-and-routing'] = 'context-intake-and-routing'
    mapping['risk-preflight-and-safety-governance'] = 'risk-preflight-and-safety-governance'
    mapping['ai-safety-and-action-governance'] = 'ai-safety-and-action-governance'
    mapping['ai-agent-autonomy-and-human-control'] = 'ai-safety-and-action-governance'

    # Stage 02 (11 -> 4):
    mapping['customer-interview-execution'] = 'customer-research-and-synthesis'
    mapping['qualitative-evidence-synthesis'] = 'customer-research-and-synthesis'
    mapping['problem-framing-and-customer-research'] = 'customer-research-and-synthesis'
    mapping['evidence-synthesis-and-opportunity-prioritization'] = 'customer-research-and-synthesis'
    mapping['persona-jtbd-and-journey-modeling'] = 'persona-and-journey-modeling'
    mapping['research-planning-and-governance'] = 'research-planning-and-governance'
    mapping['architecture-deepening-discovery'] = 'research-planning-and-governance'
    mapping['data-analysis-validation'] = 'data-analysis-and-validation'
    mapping['results-analysis-and-decision-readout'] = 'data-analysis-and-validation'
    mapping['evaluation-dataset-publication'] = 'data-analysis-and-validation'
    mapping['solution-hypothesis-and-experiment-design'] = 'solution-hypothesis-and-experiment-design'

    # Stage 03 (9 -> 3):
    mapping['structural-power-and-moats'] = 'structural-power-and-moats'
    mapping['market-positioning-and-competitive-power'] = 'market-and-competitive-intelligence'
    mapping['market-segmentation-and-demand-intelligence'] = 'market-and-competitive-intelligence'
    mapping['strategic-choice-and-differentiation'] = 'market-and-competitive-intelligence'
    mapping['competitive-case-library'] = 'market-and-competitive-intelligence'
    mapping['competitive-response-and-monitoring'] = 'market-and-competitive-intelligence'
    mapping['opportunity-prioritization-and-frameworks'] = 'opportunity-and-roadmap-prioritization'
    mapping['decision-and-outcome-roadmapping'] = 'opportunity-and-roadmap-prioritization'
    mapping['ai-product-opportunity-and-wedge'] = 'opportunity-and-roadmap-prioritization'
    mapping['ai-organizational-adoption-and-leadership'] = 'opportunity-and-roadmap-prioritization'

    # Stage 04 (10 -> 5):
    mapping['independent-plan-review'] = 'independent-plan-review'
    mapping['engineering-plan-review'] = 'independent-plan-review'
    mapping['executive-plan-review'] = 'independent-plan-review'
    mapping['design-plan-review'] = 'design-and-dx-plan-refinement'
    mapping['developer-experience-plan-review'] = 'design-and-dx-plan-refinement'
    mapping['requirements-and-delivery-contract'] = 'requirements-and-delivery-contract'
    mapping['change-scope-freeze'] = 'change-scope-freeze'
    mapping['implementation-planning-and-handoff'] = 'implementation-planning-and-handoff'
    mapping['plan-execution-control'] = 'plan-execution-control'
    mapping['plan-review-decision-synthesis'] = 'plan-execution-control'

    # Stage 05 (16 -> 8):
    mapping['content-copy-and-authentic-assets'] = 'content-copy-and-authentic-assets'
    mapping['documentation-authoring'] = 'content-copy-and-authentic-assets'
    mapping['external-design-token-extraction-and-normalization'] = 'design-token-engineering'
    mapping['design-system-foundation-and-token-extraction'] = 'design-token-engineering'
    mapping['design-context-and-direction-contract'] = 'design-context-and-direction-contract'
    mapping['ui-task-routing-and-governance'] = 'design-context-and-direction-contract'
    mapping['document-and-artifact-governance'] = 'design-context-and-direction-contract'
    mapping['responsive-layout-and-spatial-composition'] = 'responsive-layout-and-spatial-composition'
    mapping['interaction-states-forms-and-navigation'] = 'interaction-states-forms-and-navigation'
    mapping['diagram-and-architecture-artifact-generation'] = 'interaction-states-forms-and-navigation'
    mapping['document-rendering-and-validation'] = 'interaction-states-forms-and-navigation'
    mapping['ai-interaction-and-probabilistic-ux'] = 'interaction-states-forms-and-navigation'
    mapping['purposeful-motion-and-animation-engineering'] = 'purposeful-motion-and-animation-engineering'
    mapping['accessibility-contracts-and-assistive-validation'] = 'accessibility-contracts-and-assistive-validation'
    mapping['divergent-prototyping-and-variant-selection'] = 'prototyping-and-variant-selection'
    mapping['existing-interface-redesign-and-preservation'] = 'prototyping-and-variant-selection'
    mapping['visual-language-and-anti-template-controls'] = 'prototyping-and-variant-selection'

    # Stage 06 (13 -> 6):
    mapping['security-audit-and-threat-modeling'] = 'security-audit-and-threat-modeling'
    mapping['source-metadata-and-provenance'] = 'source-metadata-and-provenance'
    mapping['ci-pipeline-security-hardening'] = 'ci-pipeline-security-hardening'
    mapping['architecture-candidate-reporting'] = 'architecture-design-and-evaluation'
    mapping['architecture-deep-module-design'] = 'architecture-design-and-evaluation'
    mapping['architecture-interface-alternative-evaluation'] = 'architecture-design-and-evaluation'
    mapping['frontend-runtime-boundaries-and-dependency-safety'] = 'architecture-design-and-evaluation'
    mapping['resilience-and-determinism'] = 'architecture-design-and-evaluation'
    mapping['data-and-api-contract-design'] = 'data-and-api-contract-design'
    mapping['service-identity-remapping'] = 'data-and-api-contract-design'
    mapping['authorization-and-permission-contracts'] = 'authorization-and-permission-contracts'
    mapping['secrets-and-environment-governance'] = 'authorization-and-permission-contracts'
    mapping['ai-model-and-data-architecture'] = 'ai-model-and-data-architecture'

    # Stage 07 (12 -> 4):
    mapping['code-health-assessment'] = 'code-health-assessment'
    mapping['facilitation-and-collaboration-protocols'] = 'isolated-task-implementation'
    mapping['tdd-change-loop'] = 'tdd-change-loop'
    mapping['isolated-task-implementation'] = 'isolated-task-implementation'
    mapping['developer-experience-assessment'] = 'isolated-task-implementation'
    mapping['workflow-skill-authoring'] = 'isolated-task-implementation'
    mapping['local-branch-integration'] = 'local-branch-integration'
    mapping['defect-remediation'] = 'code-and-asset-remediation'
    mapping['ui-remediation'] = 'code-and-asset-remediation'
    mapping['website-audit-remediation'] = 'code-and-asset-remediation'
    mapping['developer-self-check-and-fix'] = 'code-and-asset-remediation'
    mapping['pull-request-comment-response'] = 'code-and-asset-remediation'

    # Stage 08 (18 -> 8):
    mapping['independent-code-review'] = 'independent-code-review'
    mapping['code-review-evidence-acquisition'] = 'independent-code-review'
    mapping['independent-blackbox-qa'] = 'independent-blackbox-qa'
    mapping['qa-finding-triage'] = 'qa-finding-triage'
    mapping['test-case-design-and-export'] = 'test-design-and-strategy'
    mapping['testing-portfolio-strategy'] = 'test-design-and-strategy'
    mapping['completion-evidence-gate'] = 'completion-evidence-gate'
    mapping['baseline-regression-control'] = 'completion-evidence-gate'
    mapping['implementation-spec-compliance-review'] = 'completion-evidence-gate'
    mapping['rendered-ui-critique-and-release-disposition'] = 'completion-evidence-gate'
    mapping['playwright-test-engineering'] = 'test-framework-tooling'
    mapping['vitest-tooling'] = 'test-framework-tooling'
    mapping['test-double-discipline'] = 'test-framework-tooling'
    mapping['website-audit-assessment'] = 'test-framework-tooling'
    mapping['llm-evaluator-engineering'] = 'llm-quality-and-evaluator-engineering'
    mapping['apm-instrumentation-verification'] = 'apm-instrumentation-verification'
    mapping['llm-quality-evaluation'] = 'llm-quality-and-evaluator-engineering'
    mapping['evidence-based-ui-review-and-release-gates'] = 'evidence-based-ui-review-and-release-gates'
    mapping['ui-review-scope-and-evidence-acquisition'] = 'evidence-based-ui-review-and-release-gates'

    # Stage 09 (5 -> 3):
    mapping['cloud-reliability-assessment'] = 'cloud-reliability-assessment'
    mapping['web-performance-diagnostics'] = 'performance-and-reliability-diagnostics'
    mapping['frontend-rendering-and-interaction-performance'] = 'performance-and-reliability-diagnostics'
    mapping['model-and-workflow-benchmarking'] = 'performance-and-reliability-diagnostics'
    mapping['evaluation-results-analysis'] = 'performance-and-reliability-diagnostics'

    # Stage 10 (4 -> 2):
    mapping['release-documentation-maintenance'] = 'release-documentation-maintenance'
    mapping['change-packaging-and-versioning'] = 'release-packaging-and-preflight'
    mapping['change-delivery-preflight'] = 'release-packaging-and-preflight'
    mapping['merge-and-deploy-readiness'] = 'release-packaging-and-preflight'

    # Stage 11 (17 -> 6):
    mapping['remote-git-push'] = 'git-remote-delivery'
    mapping['remote-pull-request-change'] = 'git-remote-delivery'
    mapping['remote-pull-request-merge'] = 'git-remote-delivery'
    mapping['deployment-trigger-execution'] = 'deployment-trigger-execution'
    mapping['edge-worker-deployment'] = 'cloud-and-edge-application-deployment'
    mapping['web-hosting-deployment'] = 'cloud-and-edge-application-deployment'
    mapping['kubernetes-application-deployment'] = 'cloud-and-edge-application-deployment'
    mapping['kubernetes-deployment-readiness'] = 'cloud-and-edge-application-deployment'
    mapping['deployment-environment-setup'] = 'cloud-and-edge-application-deployment'
    mapping['ai-observability-configuration'] = 'telemetry-and-observability-configuration'
    mapping['log-observability-configuration'] = 'telemetry-and-observability-configuration'
    mapping['release-observability-configuration'] = 'telemetry-and-observability-configuration'
    mapping['monitoring-and-alert-configuration'] = 'telemetry-and-observability-configuration'
    mapping['observability-agent-installation'] = 'telemetry-and-observability-configuration'
    mapping['apm-instrumentation-enablement'] = 'telemetry-and-observability-configuration'
    mapping['apm-instrumentation-troubleshooting'] = 'telemetry-and-observability-configuration'
    mapping['llm-experiment-execution'] = 'llm-experiment-execution'

    # Stage 12 (7 -> 4):
    mapping['metrics-system-and-observability'] = 'metrics-and-canary-observation'
    mapping['production-trace-classification'] = 'metrics-and-canary-observation'
    mapping['safe-browser-probing'] = 'safe-browser-probing'
    mapping['canary-baseline-management'] = 'canary-baseline-and-monitoring'
    mapping['deployment-observation'] = 'canary-baseline-and-monitoring'
    mapping['production-canary-monitoring'] = 'canary-baseline-and-monitoring'
    mapping['production-llm-trace-root-cause-analysis'] = 'production-llm-trace-root-cause-analysis'

    # Stage 13 (5 -> 3):
    mapping['release-rollback-execution'] = 'release-rollback-execution'
    mapping['incident-response-coordination'] = 'incident-response-coordination'
    # mapping['deployment-observation-and-recovery'] = 'incident-response-coordination'
    mapping['root-cause-investigation'] = 'root-cause-investigation'
    mapping['error-monitoring-issue-investigation'] = 'root-cause-investigation'

    # Stage 14 (5 -> 2):
    mapping['engineering-retrospective-and-improvement'] = 'engineering-retrospective-and-learning'
    mapping['feedback-and-continuous-learning-loop'] = 'engineering-retrospective-and-learning'
    mapping['reference-library-and-deferred-material'] = 'engineering-retrospective-and-learning'
    mapping['local-learning-persistence'] = 'project-context-and-learning-store'
    mapping['project-context-and-learning-store'] = 'project-context-and-learning-store'

    # Stage 15 (19 -> 5):
    mapping['browser-data-acquisition-runtime'] = 'browser-data-acquisition-runtime'
    mapping['git-destructive-command-guard'] = 'git-destructive-command-guard'
    mapping['local-git-guard-setup'] = 'git-destructive-command-guard'
    mapping['browser-session-and-runtime-configuration'] = 'browser-runtime-environment'
    mapping['browser-authentication-setup'] = 'browser-runtime-environment'
    mapping['browser-agent-pairing-provisioning'] = 'browser-runtime-environment'
    mapping['browser-agent-pairing-verification'] = 'browser-runtime-environment'
    mapping['test-runtime-bootstrap'] = 'tool-and-runtime-bootstrap'
    mapping['tool-runtime-readiness'] = 'tool-and-runtime-bootstrap'
    mapping['workflow-runtime-upgrade'] = 'tool-and-runtime-bootstrap'
    mapping['artifact-persistence-and-tool-actions'] = 'tool-and-runtime-bootstrap'
    mapping['agent-workflow-runtime-support'] = 'tool-and-runtime-bootstrap'
    mapping['mobile-platform-runtime-support'] = 'tool-and-runtime-bootstrap'
    mapping['provider-cli-authentication-setup'] = 'tool-and-runtime-bootstrap'
    # mapping['subagent-task-pipeline'] = 'tool-and-runtime-bootstrap'
    mapping['local-agent-memory-setup'] = 'tool-and-runtime-bootstrap'
    mapping['workflow-orchestration-and-lifecycle'] = 'tool-and-runtime-bootstrap'

    # Validation
    source_ids = {s['id'] for s in idx}
    missing = source_ids - set(mapping.keys())
    extra = set(mapping.keys()) - source_ids
    assert not missing and not extra, f"Missing: {missing}, Extra: {extra}"
    target_skills = sorted(set(mapping.values()))
    
    out_file = Path('curation/v2/optimization-1.1.0/consolidated-68-mapping.json')
    out_file.write_text(json.dumps({
        'schema_version': '2.0',
        'status': 'consolidated-68-candidate-architecture',
        'total_source_skills': len(mapping),
        'total_target_skills': len(target_skills),
        'mapping': mapping,
        'target_skills': target_skills
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Validated: {len(mapping)} source skills -> {len(target_skills)} target skills.")
    print(f"Output written to: {out_file}")

if __name__ == '__main__':
    main()
