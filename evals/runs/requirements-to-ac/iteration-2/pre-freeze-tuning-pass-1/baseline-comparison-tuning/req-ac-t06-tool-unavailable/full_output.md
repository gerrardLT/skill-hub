# Requirements Artifact

Status: needs-input

## Supplied Facts

- The requirements depend on an external analytics export.
- The analytics tool is unavailable.
- No analytics export is attached.

## Requirement

The product requirements must use the external analytics export as the source for analytics-dependent decisions and validation.

## Acceptance Criteria

| ID | Acceptance criterion | State |
|---|---|---|
| AC-1 | An external analytics export is provided as an input to requirements analysis. | needs-input |
| AC-2 | Analytics-dependent requirements and thresholds are derived only from the supplied export. | needs-input |
| AC-3 | Analytics-dependent requirements identify the relevant observed behaviors, segments, measures, and time period from the supplied export. | needs-input |
| AC-4 | Analytics-dependent acceptance criteria define verifiable expected outcomes and thresholds supported by the supplied export. | needs-input |

## Input Needed

Provide the external analytics export required by the product requirements. Until it is supplied, analytics-dependent behaviors, segments, measures, time periods, baselines, targets, and thresholds remain unspecified.

## Constraints

- Do not infer or invent analytics findings.
- Do not assign unsupported quantitative thresholds.
- Reassess all analytics-dependent acceptance criteria after the export is attached.
