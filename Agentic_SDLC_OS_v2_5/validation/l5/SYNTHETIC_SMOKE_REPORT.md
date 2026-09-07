# Agentic SDLC OS — L5 Experiment Report

- Project: **synthetic-smoke**
- Comparison: `parallel`
- Registered: `2026-08-31T03:23:17Z`
- Generated: `2026-08-31T03:23:17Z`
- Synthetic: **YES — SMOKE TEST ONLY**
- Decision: **POSITIVE**
- Iterations: baseline=2, sdlc=2, target=2 each

## Preregistered hypothesis

Synthetic data should exercise all calculations.

## Metric results

| Metric | Baseline | SDLC | Relative improvement | Direction |
|---|---:|---:|---:|---|
| `lead_time_hours` | 102.5 | 77.0 | 24.9% | lower |
| `rework_rate` | 0.3 | 0.18 | 40.0% | lower |
| `escaped_defects` | 5.0 | 3.0 | 40.0% | lower |
| `incidents` | 2.0 | 1.0 | 50.0% | lower |
| `rollback_rate` | 0.2 | 0.1 | 50.0% | lower |
| `trace_coverage` | 0.45 | 0.85 | 88.9% | higher |
| `evidence_decision_rate` | 0.4 | 0.8 | 100.0% | higher |
| `goal_attainment` | 0.55 | 0.72 | 30.9% | higher |
| `human_hours` | 80.0 | 65.0 | 18.8% | lower |
| `token_cost_usd` | 0.0 | 35.0 | -100.0% | lower |
| `actionability_score` | 6.0 | 8.0 | 33.3% | higher |

## Category decision

| Category | Mean relative improvement | Status |
|---|---:|---|
| cycle | 24.9% | improved |
| rework | 40.0% | improved |
| quality | 46.7% | improved |
| traceability | 94.4% | improved |
| outcome | 30.9% | improved |
| effort | 18.8% | improved |
| cost | -100.0% | regressed |
| usability | 33.3% | improved |

## Blind review

- Baseline composite: 6.1667
- SDLC composite: 8.0

## Decision basis

- Improved primary categories: cycle, rework, quality, traceability, outcome
- Regressed primary categories: none
- Severe regressions: none

## Limitations

- This analysis does not establish causality unless allocation, matching, and confounders are controlled.
- Synthetic data is a tooling smoke test only and cannot validate real-project effectiveness.
- Means hide variance; inspect individual iterations before acting on small samples.
