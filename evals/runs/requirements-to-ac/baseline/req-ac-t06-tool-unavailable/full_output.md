# Requirements Artifact

## Status

**needs-input**

The analytics-dependent acceptance criteria cannot be completed because the required external analytics export is unavailable and no export was supplied. No analytics tool query was performed.

## Supplied Facts

- The requirements depend on an external analytics export.
- The analytics tool is unavailable.
- No analytics export is attached.
- The artifact must use only supplied facts.

## Requirements

### R1. Evidence boundaries

The requirements artifact must distinguish supplied facts from analytics-dependent claims that cannot currently be verified.

### R2. Analytics dependency

Any requirement or acceptance criterion that depends on analytics event data, a baseline, or a tool query result must remain unresolved until an authorized analytics export is supplied or the analytics tool becomes available.

### R3. Claim restrictions

The artifact must not state or imply that analytics were reviewed, a baseline was confirmed, a metric passed, or the unavailable analytics tool was queried.

### R4. Evidence intake

When the missing analytics evidence becomes available, it must identify the relevant event data and provide enough context to establish the applicable baseline before analytics-dependent criteria can be evaluated.

## Acceptance Criteria

### AC1. Supplied-fact traceability — ready

**Given** the current input contains only the facts listed in this artifact,  
**When** the requirements artifact is reviewed,  
**Then** every factual assertion is traceable to those supplied facts, and no external analytics result appears as established evidence.

### AC2. Tool-unavailable disclosure — ready

**Given** the analytics tool is unavailable and no export is attached,  
**When** the artifact reports its evidence status,  
**Then** it explicitly records both conditions and states that no analytics tool query was performed.

### AC3. Analytics event evidence — needs-input

**Given** no analytics export is attached,  
**When** analytics-dependent behavior is evaluated,  
**Then** the criterion remains **needs-input** until the relevant analytics event data is supplied.

Missing input: analytics event data from the external analytics export.

### AC4. Baseline confirmation — needs-input

**Given** no analytics event data or export is available,  
**When** a baseline-dependent requirement is evaluated,  
**Then** the criterion remains **needs-input** and no baseline value or confirmation is asserted.

Missing input: a baseline supported by the supplied analytics export.

### AC5. Metric evaluation — needs-input

**Given** the analytics event data and baseline are unavailable,  
**When** any metric-based success criterion is assessed,  
**Then** no pass or fail result is reported and the criterion remains **needs-input**.

Missing input: the relevant event data, baseline, and evaluation rule or target if one is required.

## Open Inputs

- Analytics event data.
- Baseline derived from or supported by the analytics export.
- Tool query result, if querying the restored tool is the authorized evidence path.
- The specific product behavior, users, metric definition, target, and decision this artifact is intended to support; none were supplied, so no more specific product or solution requirements can be asserted.

## Next Evidence Step

Attach an authorized analytics export containing the relevant event data and baseline context, or restore authorized access to the analytics tool. After that evidence is supplied, review the analytics-dependent criteria without treating tool availability alone as proof that any metric passed.
