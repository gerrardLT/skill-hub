# Outputs and Acceptance

Use one artifact per independently reviewable decision. Avoid giant documents that hide status and ownership.

| Artifact or Gate | Minimum content | Acceptance evidence |
| --- | --- | --- |
| `release-intake` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to INTAKE. | Independent review or reproducible verification appropriate to the stage. |
| `release-readiness` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to READINESS. | Independent review or reproducible verification appropriate to the stage. |
| `build-artifact` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to BUILD_ARTIFACT. | Independent review or reproducible verification appropriate to the stage. |
| `environment-verification` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to ENVIRONMENT. | Independent review or reproducible verification appropriate to the stage. |
| `migration-plan` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to MIGRATION. | Independent review or reproducible verification appropriate to the stage. |
| `release-plan / rollback-plan` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to DEPLOYMENT_PLAN. | Independent review or reproducible verification appropriate to the stage. |
| `deployment-evidence` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to ROLLOUT. | Independent review or reproducible verification appropriate to the stage. |
| `production-verification` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to PRODUCTION_VERIFICATION. | Independent review or reproducible verification appropriate to the stage. |
| `observability-ready` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to STABILIZATION. | Independent review or reproducible verification appropriate to the stage. |
| `production-ready` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to REVIEW. | Independent review or reproducible verification appropriate to the stage. |

## Artifact status

- `draft`: incomplete or unreviewed.
- `review`: ready for independent assessment.
- `accepted`: decision owner has accepted scope and evidence.
- `rejected`: does not satisfy acceptance.
- `superseded`: replaced; retain history and trace links.
