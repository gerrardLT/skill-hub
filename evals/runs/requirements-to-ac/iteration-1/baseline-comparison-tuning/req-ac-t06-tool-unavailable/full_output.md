Status: needs-input

# Requirements Artifact

## Supplied facts

- The requirements depend on an external analytics export.
- The analytics tool is unavailable.
- No analytics export is attached.

## Known requirements

- The artifact must not treat analytics-dependent claims as validated until the required export is available and reviewed.
- The unavailable analytics dependency must remain explicit in downstream decisions.
- Any requirement that can be established without analytics must be based only on separately supplied facts; none were supplied in this request.

## Analytics-dependent acceptance criteria

Status: needs-input

1. Given the analytics export is unavailable, when this artifact is reviewed, then no analytics event result, baseline, or metric outcome is represented as confirmed.
2. Given an authorized analytics export is later attached, when the relevant event data is reviewed, then the applicable event definitions, observation period, population, baseline calculation, and result can be recorded with their source.
3. Given any required field or event needed for the calculation is absent or undefined, when the export is assessed, then the affected criterion remains needs-input and identifies the missing evidence rather than assigning a result.
4. Given the export and definitions are sufficient, when an analytics-dependent criterion is evaluated, then its result is traceable to the supplied export and the agreed calculation; no pass threshold can be evaluated because none was supplied.

## Missing evidence

- Analytics event data
- Baseline
- Tool query result
- Event definitions, observation period, population, and any success threshold needed to turn analytics evidence into testable outcome criteria
- An attached export from an authorized source

## Next decision

Provide the analytics export and the governing metric definitions, period, population, and threshold. Until then, analytics-dependent acceptance criteria remain needs-input. The analytics tool was not queried.
