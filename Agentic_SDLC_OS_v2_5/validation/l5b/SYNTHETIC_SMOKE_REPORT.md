# Agentic SDLC OS L5-B Matched Experiment

- Experiment: `l5b-ff25017b628d4b71b0c2a88843e65a5f`
- Project: **Agentic SDLC OS v2.3 harness smoke**
- Preregistration: `cf35c592e4023170beef857346cf743a4eaeebe6af05ed7657976342655981a3`
- Complete pairs: 5/5
- Synthetic: **True**
- Decision: **SYNTHETIC-SMOKE-ONLY**

## Paired metric effects

| Metric | Mean improvement | 95% CI | Sign-test p |
|---|---:|---:|---:|
| `lead_time_minutes` | 23.6% | [23.0%, 24.2%] | 0.0625 |
| `human_minutes` | 21.7% | [21.4%, 22.0%] | 0.0625 |
| `token_cost_usd` | 5.7% | [5.5%, 5.8%] | 0.0625 |
| `rework_fraction` | 50.0% | [50.0%, 50.0%] | 0.0625 |
| `escaped_defects` | 50.0% | [50.0%, 50.0%] | 0.0625 |
| `critical_defects` | 100.0% | [100.0%, 100.0%] | 0.0625 |
| `trace_coverage` | 56.9% | [56.9%, 56.9%] | 0.0625 |
| `acceptance_pass_rate` | 27.0% | [27.0%, 27.0%] | 0.0625 |
| `maintainability_score` | 35.0% | [35.0%, 35.0%] | 0.0625 |

## Decision controls

- Improved primary categories: cycle, rework, quality, traceability, outcome
- Significant positive metrics: lead_time_minutes, rework_fraction, escaped_defects, critical_defects, trace_coverage, acceptance_pass_rate, maintainability_score
- Severe regressions: none
- Contaminated runs: 0
- Sealed: True
- Formal evidence eligible: False
- Control errors: none

## Blind review

- Baseline: 7.0
- SDLC: 8.5

## Limitations

- A positive result applies only to the sampled tasks, executors, models, tools and time window.
- Synthetic data validates the harness only and is never effectiveness evidence.
- Small matched samples have low power; retain raw paired results and inspect heterogeneity.
