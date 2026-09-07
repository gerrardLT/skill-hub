# Gate: design-ready

Purpose: 确认核心流程、状态、可访问性和交付规格达到可开发状态。

## Required accepted artifacts

- `information-architecture`
- `user-flows`
- `interaction-spec`
- `design-system`
- `prototype`
- `usability-report`
- `accessibility-report`
- `design-handoff`

## Additional high-criticality artifacts

- `content-model`
- `error-state-matrix`
- `localization-plan`

## Evidence and risk policy

- Minimum evidence records: 1.
- Minimum high-quality evidence records: 0.
- Open critical risks block: true.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name design-ready
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
