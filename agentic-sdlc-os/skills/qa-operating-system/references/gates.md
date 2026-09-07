# Gate: release-ready

Purpose: 确认残余风险已知、可接受，并有证据支持发布建议。

## Required accepted artifacts

- `test-strategy`
- `regression-report`
- `nonfunctional-report`
- `defect-disposition`
- `release-recommendation`

## Additional high-criticality artifacts

- `security-test-report`
- `resilience-test-report`
- `privacy-verification`

## Evidence and risk policy

- Minimum evidence records: 0.
- Minimum high-quality evidence records: 0.
- Open critical risks block: true.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name release-ready
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
