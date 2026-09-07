# Gate: learning-decision

Purpose: 把真实结果转成明确的继续、停止、修复或回流决策。

## Required accepted artifacts

- `telemetry-report`
- `diagnosis`
- `intervention-result`
- `learning-decision`

## Additional high-criticality artifacts

- `incident-review`

## Evidence and risk policy

- Minimum evidence records: 1.
- Minimum high-quality evidence records: 0.
- Open critical risks block: false.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name learning-decision
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
