# Outputs and Acceptance

Use one artifact per independently reviewable decision. Avoid giant documents that hide status and ownership.

| Artifact or Gate | Minimum content | Acceptance evidence |
| --- | --- | --- |
| `engineering-intake` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to INTAKE. | Independent review or reproducible verification appropriate to the stage. |
| `requirements-review` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to REQUIREMENTS_REVIEW. | Independent review or reproducible verification appropriate to the stage. |
| `technical-design` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to TECHNICAL_DESIGN. | Independent review or reproducible verification appropriate to the stage. |
| `architecture-decisions` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to ARCHITECTURE. | Independent review or reproducible verification appropriate to the stage. |
| `implementation-plan / test-plan / security-plan` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to PLAN. | Independent review or reproducible verification appropriate to the stage. |
| `source-change / unit-test-evidence` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to BUILD. | Independent review or reproducible verification appropriate to the stage. |
| `code-review` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to CODE_REVIEW. | Independent review or reproducible verification appropriate to the stage. |
| `integration-evidence` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to INTEGRATION. | Independent review or reproducible verification appropriate to the stage. |
| `security-review / performance-report` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to HARDENING. | Independent review or reproducible verification appropriate to the stage. |
| `verification-ready` | Objective, inputs, facts/evidence, inferences, assumptions, result, risks, acceptance criteria and traceability relevant to HANDOFF. | Independent review or reproducible verification appropriate to the stage. |

## Artifact status

- `draft`: incomplete or unreviewed.
- `review`: ready for independent assessment.
- `accepted`: decision owner has accepted scope and evidence.
- `rejected`: does not satisfy acceptance.
- `superseded`: replaced; retain history and trace links.
