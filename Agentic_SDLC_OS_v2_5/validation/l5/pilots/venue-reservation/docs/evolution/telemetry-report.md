# Telemetry Report

## Objective

Compare measured runtime signals with the preregistered pilot thresholds.

## Facts and evidence

Observed 200 requests with capacity 20 and 32 workers. Reserved=20, waitlisted=180, oversold=false, throughput=1064.434 requests per second, p95=107.185 ms and audit_events=201. Test coverage is 96 percent.

## Decision and specification

All preregistered correctness thresholds passed. Local latency also passed the 500 ms guardrail.

## Risks and edge cases

This is generated traffic in a controlled container. It does not measure user behavior, real network latency, business conversion, multi-process coordination or long observation windows.

## Verification and acceptance criteria

Telemetry is accepted when raw JSON, parameters and source version are present and values reconcile with database state.

## Traceability and ownership

Owner: Evolution OS. Inputs: MP-001, PV-001 and PERF-001. Downstream: DIA-001 and IR-001.
