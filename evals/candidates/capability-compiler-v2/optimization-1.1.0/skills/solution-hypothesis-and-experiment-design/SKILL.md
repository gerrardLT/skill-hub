---
name: solution-hypothesis-and-experiment-design
description: "Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria. Use when A validated problem needs falsifiable solution hypotheses and the cheapest experiment that could disprove them; Someone asks how to test an idea with predeclared success and kill criteria. Do not use for: Frame whether the customer problem is real from raw notes (-> problem-framing-and-customer-research); Analyze the completed experiment and make a recommendation (-> results-analysis-and-decision-readout)."
---

# Solution Hypothesis And Experiment Design

## Responsibility

Turn a validated problem into falsifiable solution hypotheses and proportionate experiments with predeclared evidence and stopping criteria.

## Trigger

Use when the request matches any of:
- A validated problem needs falsifiable solution hypotheses and the cheapest experiment that could disprove them
- Someone asks how to test an idea with predeclared success and kill criteria

Do not use when:
- Frame whether the customer problem is real from raw notes. Route to `problem-framing-and-customer-research`.
- Analyze the completed experiment and make a recommendation. Route to `results-analysis-and-decision-readout`.

## Required Inputs

- A framed problem, prioritized opportunity, assumptions, risks, and available experiment conditions.

## Procedure

1. Verify the problem frame, target behavior, current evidence, ethical boundary, and decision to be informed.
2. Write hypothesis, mechanism, predicted observable change, counterfactual, and failure interpretation.
3. Generate experiment options ranked by learning value, risk, cost, and reversibility.
4. Declare population, method, metrics, guardrails, thresholds, duration, stopping, and analysis plan before execution.
5. Return experiment contract, risks, and authorization needs without running it.

## Domain Guidance

- Experiment menu by risk and cost: fake door or landing page (low cost, demand), concierge test (manual delivery, value), prototype test (usability), A/B test (effect size, needs traffic). Pick the cheapest that could falsify the hypothesis and say why cheaper ones are insufficient.
- Write the hypothesis as: we believe <change> for <audience> will <measurable effect> because <mechanism>; declare the counterfactual, the metric and threshold, the guardrails and the stopping rule before running.

## Output Contract

Produce:
- hypothesis register
- experiment options
- selected experiment contract
- stopping and analysis criteria

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A test without a falsifiable prediction, counterfactual, and predeclared success or kill criterion is not an experiment contract.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `problem-framing-and-customer-research`
- `results-analysis-and-decision-readout`
- `ai-product-opportunity-and-wedge`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
