# Gates

| Gate | From → To | Core required artifacts | High-assurance add-ons |
| --- | --- | --- | --- |
| `pm-ready` | pm → design | product-brief, discovery-evidence, product-strategy, prioritized-opportunities, prd, outcome-roadmap, measurement-plan, risk-register | privacy-impact, security-requirements, data-classification |
| `design-ready` | design → engineering | information-architecture, user-flows, interaction-spec, design-system, prototype, usability-report, accessibility-report, design-handoff | content-model, error-state-matrix, localization-plan |
| `build-ready` | engineering → engineering | technical-design, architecture-decisions, implementation-plan, test-plan, security-plan | threat-model, capacity-plan, migration-strategy |
| `verification-ready` | engineering → qa | source-change, unit-test-evidence, code-review, integration-evidence, security-review, performance-report | dependency-scan, sbom, data-migration-evidence |
| `release-ready` | qa → release | test-strategy, regression-report, nonfunctional-report, defect-disposition, release-recommendation | security-test-report, resilience-test-report, privacy-verification |
| `production-ready` | release → evolution | release-plan, rollback-plan, migration-plan, deployment-evidence, production-verification, observability-ready | disaster-recovery-plan, failover-test, on-call-plan |
| `learning-decision` | evolution → * | telemetry-report, diagnosis, intervention-result, learning-decision | incident-review |

The manifest defines effective requirements separately for `lite`, `standard` and `high-assurance`. Treat this table as an overview; use the bundled manifest as the executable policy.

## Rules

1. Required artifacts count only when registered as `accepted`, substantive and integrity-verified.
2. Missing paths, template placeholders, empty files and post-acceptance changes invalidate artifacts.
3. Evidence is deduplicated and evaluated for source type, expiry, distinct-source count and target coverage.
4. Traceability must satisfy configured **directed type paths**. Unknown endpoints, self-links, invalid relations, duplicate edges and arbitrary unrelated links do not count.
5. Open critical risks block configured Gates and cannot be waived.
6. A waiver is not a pass. It requires a named human approver, approval ID, compensating control and bounded expiry; relevant state changes invalidate it.
7. Re-check a Gate whenever an upstream artifact, evidence item, risk, trace edge or material assumption changes.
8. `build-ready` is an internal Engineering Gate before BUILD; other Gates control OS handoffs.
9. A high-criticality project cannot use the `lite` process profile.
10. Verify `audit`, `health` and the applicable Gate before consequential handoffs.
## Bounded-lite Gate profile

For an active bounded `lite` Work Item, Gate requirements are scoped to that Work Item and compacted:

- `build-ready`: `change-plan` + qualifying test/code evidence.
- `verification-ready`: `change-verification` + at least two evidence records, including one high-quality source.
- `release-ready`: `release-recommendation` + qualifying release evidence.
- `production-ready`: rollback, deployment and production-verification evidence remain mandatory.
- `learning-decision`: record the resulting learning decision.

Compact Gate schemas reduce duplicate documents; they do not permit unrelated historical evidence, stale artifacts, open critical risks, integrity failures or unverified production claims.

