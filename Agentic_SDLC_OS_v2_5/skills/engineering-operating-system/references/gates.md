# Gate: verification-ready

Purpose: 确认实现已完成工程自证，可交给独立 QA。

## Required accepted artifacts

- `source-change`
- `unit-test-evidence`
- `code-review`
- `integration-evidence`
- `security-review`
- `performance-report`

## Additional high-criticality artifacts

- `dependency-scan`
- `sbom`
- `data-migration-evidence`

## Evidence and risk policy

- Minimum evidence records: 0.
- Minimum high-quality evidence records: 0.
- Open critical risks block: true.

Run:

```bash
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name verification-ready
```

A waiver is not equivalent to a pass and requires explicit approver, reason and scope.
