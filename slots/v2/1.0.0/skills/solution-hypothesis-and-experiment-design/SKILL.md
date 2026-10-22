---
name: solution-hypothesis-and-experiment-design
description: Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria. Do not use for frame whether the customer problem is real from raw notes or analyze the completed experiment and make a recommendation.
---

# Solution Hypothesis And Experiment Design

## Responsibility

Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria.

## Trigger

Use when the requested outcome is: Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria.

Do not use when:
- Frame whether the customer problem is real from raw notes. Route to `problem-framing-and-customer-research`.
- Analyze the completed experiment and make a recommendation. Route to `results-analysis-and-decision-readout`.

## Required Inputs

- A framed problem, prioritized opportunity, assumptions, risks, and available experiment conditions.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify the problem frame, target behavior, current evidence, ethical boundary, and decision to be informed.
2. Write hypothesis, mechanism, predicted observable change, counterfactual, and failure interpretation.
3. Generate experiment options ranked by learning value, risk, cost, and reversibility.
4. Declare population, method, metrics, guardrails, thresholds, duration, stopping, and analysis plan before execution.
5. Return experiment contract, risks, and authorization needs without running it.

## Output Contract

Produce:
- hypothesis register
- experiment options
- selected experiment contract
- stopping and analysis criteria

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- A test without a falsifiable prediction, counterfactual, and predeclared success or kill criterion is not an experiment contract.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `problem-framing-and-customer-research`
- `results-analysis-and-decision-readout`
- `ai-product-opportunity-and-wedge`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
