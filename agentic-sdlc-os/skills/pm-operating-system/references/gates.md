# Gate: pm-ready

Purpose: 确认问题、战略、范围、成功指标和关键风险足以进入设计。

## Required accepted artifacts

- `product-brief`
- `discovery-evidence`
- `product-strategy`
- `prioritized-opportunities`
- `prd`
- `outcome-roadmap`
- `measurement-plan`
- `risk-register`

## Additional high-criticality artifacts

- `privacy-impact`
- `security-requirements`
- `data-classification`

## Evidence and risk policy

- Minimum evidence records: 3.
- Minimum high-quality evidence records: 1.
- Open critical risks block: true.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name pm-ready
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
