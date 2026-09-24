# Skill Benchmark: requirements-to-ac

**Model**: general-purpose-agent/default
**Date**: 2026-09-14T06:27:53Z
**Evals**: 1, 2, 3, 4, 5, 6 (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 13% ± 5% | 16% ± 3% | -0.03 |
| Time | 112.5s ± 12.5s | 82.9s ± 15.3s | +29.6s |
| Tokens | 243755 ± 28109 | 253654 ± 65239 | -9899 |

## Notes

- Pass rates include mechanically proven run evidence and status checks; semantic criteria remain failed pending blind human review.
- Candidate formal holdout has two incorrect gates: h01 expected passed but returned needs-input; h02 expected needs-input but returned blocked.
- One run per configuration does not establish model-output variance; repeated volatile-case runs remain required.
- Token and duration values were verified run-by-run against timing.json captured from agent completion notifications.