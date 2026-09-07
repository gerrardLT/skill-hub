# Gate: production-ready

Purpose: 确认线上版本可监控、可验证、可回滚、可响应。

## Required accepted artifacts

- `release-plan`
- `rollback-plan`
- `migration-plan`
- `deployment-evidence`
- `production-verification`
- `observability-ready`

## Additional high-criticality artifacts

- `disaster-recovery-plan`
- `failover-test`
- `on-call-plan`

## Evidence and risk policy

- Minimum evidence records: 0.
- Minimum high-quality evidence records: 0.
- Open critical risks block: true.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name production-ready
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
