# Cost governance

Track cost as an engineering constraint, not an after-action estimate.

Budgets cover USD, input/output Tokens, tool calls and human hours. Preflight before multi-agent fan-out or expensive tools. Apply controls in this order:

1. Reuse existing evidence.
2. Disable speculative subagents.
3. Reduce parallelism.
4. Route routine work to an economy model.
5. Cap optional tool calls.
6. Require budget-owner approval.

Never degrade protected work: security/privacy review, critical-risk mitigation, rollback validation or incident response.

```bash
python scripts/cost_governance.py set . --cost-usd 25 --tokens 500000
python scripts/cost_governance.py assess . --forecast-usd 4 --forecast-tokens 20000
python scripts/sdlc.py record-run . --actor agent-a --os engineering --skill build --model model-x --outcome success --tokens-input 1000 --tokens-output 400 --tool-calls 5 --cost-usd 0.12 --human-hours 0.1
```

`lite` and `standard` may warn/degrade before the hard limit unless explicitly configured. `high-assurance` bootstraps with hard enforcement.
