# Subagent Protocol

## Use a subagent when

- independent judgment reduces confirmation bias;
- tasks can be researched in parallel without shared mutable state;
- a red team should not see the author’s reasoning;
- operational permissions must be isolated;
- a large context would otherwise pollute the main workflow.

Do not create one subagent per Skill. Skills encode reusable method; subagents create isolated execution contexts.

## Task contract

Give every subagent:

```text
Role:
Bounded question:
Inputs and accepted sources:
Excluded actions:
Required output:
Evidence standard:
Stop condition:
```

The output must separate facts, inferences, assumptions, risks and recommended action. The Orchestrator compares conflicts and owns synthesis.

## Default roles

- Evidence researcher
- Product/strategy red team
- Design critic and accessibility reviewer
- Architecture reviewer and code reviewer
- QA red team
- Release safety reviewer
- Incident investigator and experiment reviewer

Never give an exploratory or review subagent production write access by default.
