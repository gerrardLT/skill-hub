Status: passed

## next-requirements

Status: passed

Evidence:

1. **LR-1 — Supplied outcome verification**
   - Classification: evidence.
   - Source: `actual-results` records QA-1 through QA-4; `HOST PREFLIGHT EVIDENCE`.
   - Current command:
     ```text
     python -c import os,pytest; os.chdir('apps/api'); raise SystemExit(pytest.main(['-q','tests/test_ip_rate_limit_eval.py']))
     ```
   - Result: return code `0`; `12 passed in 1.21s`.
   - Verified outcomes:
     - Configured global and conversation limits reject threshold-exceeding requests with `429`.
     - Rejections expose retry metadata and rate-limit headers in the covered constrained scenario.
     - `/healthz` and `/metrics` bypass limiting.
     - No Redis dependency is evidenced by the executed black-box suite.
     - No remote side effect is claimed or evidenced.

2. **LR-2 — Corrective-learning signal**
   - Classification: evidence.
   - Source: feedback item `independent-blackbox-qa`; delivery record DEL-6; QA-2.
   - Initial QA found over-broad conversation path classification.
   - Correction preserves exact route classification:
     ```text
     POST /v2/conversation/{single-segment}/message
     ```
   - Nested route remains global-only:
     ```text
     POST /v2/conversation/a/nested/message
     ```
   - Correction passed the current isolated 12-test execution.

3. **LR-3 — Delivery and authority calibration**
   - Classification: evidence and constraint.
   - Source: feedback item `delivery-preflight`; DEL-1 through DEL-8.
   - Delivery mode remains `local-review-package-only`.
   - `remote_git`, merge, deploy, and network authority remain `false`.
   - Working scope remains:
     ```text
     apps/api/app/core/rate_limit.py
     ```
   - Current patch SHA-256:
     ```text
     6b3a145486ed48946c2768e42292cd9be06a3892cebdbdf60121d254f056172d
     ```

4. **LR-4 — Current quality calibration**
   - Classification: authorized decision.
   - Source: QA-1 through QA-5; DEL-5.
   - Health score: `82/100`.
   - Confidence is high for the executed 12-test black-box scope.
   - Confidence is incomplete for acceptance-criterion edge semantics not executed in supplied evidence.
   - `PytestDeprecationWarning` is non-failing but remains a maintenance signal.

5. **LR-5 — Frozen scope**
   - Classification: constraint and authorized decision.
   - Source: `decisions[0]`.
   - Decision:
     ```text
     Use only the frozen Requirement 1 scope.
     ```
   - No threshold adjustment, Redis adoption, distributed-state design, documentation change, merge, deployment, or remote publication follows from this retrospective.

Review Cadence:

1. **Per local review package**
   - Re-run:
     ```text
     python -c import os,pytest; os.chdir('apps/api'); raise SystemExit(pytest.main(['-q','tests/test_ip_rate_limit_eval.py']))
     ```
   - Record return code, test count, warning output, source HEAD, and patch SHA-256.
   - Reconfirm no unauthorized remote Git, merge, deploy, network, or documentation action.

2. **Before release assurance sign-off**
   - Obtain black-box evidence for currently unresolved AC-2, AC-4 through AC-8, AC-11 through AC-14, and AC-16 through AC-18 edge semantics.
   - Preserve separate evidence for default boundaries, one-hour recovery, fractional `ceil`, ratio tie-breaks, dual rejection selection, and per-process storage behavior.

3. **When production traffic or cost evidence becomes available**
   - Review `OPEN-1`.
   - Treat traffic, cost, and scaling evidence as new discovery input; do not infer a Redis or distributed-state requirement from current local verification.

Calibrated Hypotheses:

1. **HYP-1 — Exact conversation-route matching remains correct**
   - Classification: hypothesis, calibrated by evidence.
   - Evidence: QA-2; DEL-6; passed nested-path regression case.
   - Confidence: high within the executed suite.
   - Falsifier: a black-box case showing a non-exact or nested path receives conversation-specific limiting.

2. **HYP-2 — Local in-process limiting satisfies frozen Requirement 1**
   - Classification: hypothesis, calibrated by evidence and constraint.
   - Evidence: QA-3; LR-5; no Redis dependency observed.
   - Confidence: high for isolated local execution.
   - Ceiling: no production traffic, cost, multi-process, or distributed-state evidence exists.
   - Upgrade path: assess distributed-state requirements only after `OPEN-1` receives authoritative operational evidence.

3. **HYP-3 — Header and retry behavior is adequate for covered rejection cases**
   - Classification: hypothesis, calibrated by evidence.
   - Evidence: QA-3.
   - Confidence: moderate.
   - Falsifier: targeted black-box coverage exposes incorrect selected-limit headers, retry metadata, or fractional `ceil` behavior.

Priorities:

1. **P1 — Preserve current correction**
   - Keep exact single-segment conversation-message classification.
   - Do not broaden route matching without a failing black-box case and authorized scope change.

2. **P2 — Close edge-semantics evidence gaps when release assurance requires it**
   - Add or execute targeted black-box cases for:
     - exact default `10/30` boundaries;
     - full one-hour conversation recovery;
     - fractional remaining-time `ceil`;
     - lower-ratio and equal-ratio tie-break permutations;
     - simultaneous dual rejection selection;
     - direct per-process storage inspection.

3. **P3 — Resolve test configuration warning separately**
   - `pytest_asyncio` reports unset `asyncio_default_fixture_loop_scope`.
   - Current suite passes; warning does not invalidate LR-1.
   - Address only with explicit authorization for test configuration maintenance.

Next Discovery Input:

1. **DISC-1 — Required release-assurance evidence**
   - Classification: unknown.
   - Request current executable results for the unresolved acceptance-criterion cases listed in P2.
   - Preserve command, return code, stdout, stderr, source HEAD, patch SHA-256, and direct assertion-to-criterion mapping.

2. **DISC-2 — Operational evidence**
   - Classification: unknown.
   - Request authoritative traffic volume, request distribution, cost, process topology, and availability requirements for `OPEN-1`.
   - No threshold change or distributed-state conclusion may be made before such evidence exists.

3. **DISC-3 — Customer feedback continuity**
   - Classification: unknown.
   - No direct customer feedback is supplied; current feedback is QA and delivery-preflight only.
   - Request customer or operator reports concerning `429` usability, retry behavior, false positives, and health-route accessibility.

Gate Results:

1. **evidence-present: passed**
   - Current isolated execution evidence exists: command, return code `0`, `12 passed`, warning output, source head, and patch SHA-256.
   - Corrective-learning evidence exists from initial nested-route defect through passing correction verification.
   - Delivery-boundary evidence exists in DEL-1 through DEL-8.

2. **unknowns-preserved: passed**
   - `OPEN-1 — Traffic and cost measurements unavailable` remains known unavailable and non-blocking.
   - QA-5 coverage gaps remain unresolved and are not represented as verified.
   - Direct customer feedback remains absent, not inferred.
   - `PytestDeprecationWarning` remains recorded as a non-failing warning.

3. **authority-boundary: passed**
   - Retrospective uses supplied local QA and delivery-preflight evidence only.
   - No remote Git, network, merge, deployment, threshold adjustment, or operational decision is claimed.
   - `SRC-2` remains non-binding per supplied QA evidence.

4. **responsibility-boundary: passed**
   - This artifact performs feedback synthesis, metric review, calibration, and next-cycle input definition only.
   - No source modification, QA execution, delivery action, requirements revision, merge, or deployment is performed or claimed.

Unknowns:

1. **OPEN-1 — Traffic and cost measurements unavailable**
   - Status: known unavailable; non-blocking.
   - Source: requirements-artifact `OPEN-1`; QA-5; DEL unknowns.
   - No production traffic inference, threshold adjustment, Redis requirement, or distributed-state requirement follows.

2. **UNK-2 — Coverage outside the current 12-test execution**
   - Status: unresolved.
   - Source: QA-5; DEL unknowns.
   - Missing current execution evidence: exact default boundaries, full one-hour recovery, fractional `ceil`, complete tie-break permutations, simultaneous dual rejection selection, and direct per-process storage inspection.

3. **UNK-3 — Direct customer or operator feedback**
   - Status: not supplied.
   - Source: `feedback` contains `independent-blackbox-qa` and `delivery-preflight` only.
   - No customer satisfaction, retry usability, false-positive rate, or production-impact conclusion is supported.

4. **UNK-4 — Pytest async fixture-loop configuration**
   - Status: unresolved maintenance warning.
   - Source: `HOST PREFLIGHT EVIDENCE.stderr`; DEL-5.
   - Current verification passed; future fixture-loop behavior remains configuration-sensitive.