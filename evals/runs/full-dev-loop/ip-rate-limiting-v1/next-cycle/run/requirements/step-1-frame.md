Status: passed

## Classified items

1. **fact — Target user: system operator**
   - Statement: The user story identifies “系统运维者” as the target user.
   - Problem context: A single IP may make bulk LLM API calls through malicious scripts.
   - Intended impact: LLM API cost may become uncontrolled.
   - Evidence: `SRC-1`, Requirement 1 user story.

2. **fact — Primary protected behavior**
   - Statement: More than 10 `POST` requests from one client IP to `/v2/conversation/{id}/message` within one hour must receive HTTP `429`.
   - Required rejection body includes Chinese `detail` and `retry_after`.
   - Evidence: `SRC-1`, AC-1.

3. **fact — Global protected behavior**
   - Statement: More than 30 requests from one client IP to any API endpoint within one minute must receive HTTP `429`.
   - Evidence: `SRC-1`, AC-2.

4. **fact — Configuration requirement**
   - Statement: Conversation and global thresholds are configurable through `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE`.
   - Normative defaults are `10` per conversation hour and `30` per global minute.
   - Evidence: `SRC-1`, AC-3; authority decision `configuration_defaults`.

5. **fact — MVP storage boundary**
   - Statement: Requirement 1 requires in-memory storage and no Redis dependency for MVP.
   - Per-process storage is in scope; shared multi-worker storage is out of scope.
   - Evidence: `SRC-1`, AC-4; authority decision `in_memory_scope`.

6. **fact — Exempt endpoint behavior**
   - Statement: `/healthz` and `/metrics` requests are exempt from counting.
   - Authorized clarification: exempt requests also emit no rate-limit headers.
   - Evidence: `SRC-1`, AC-5; authority decisions `exempt_endpoints`, `internal_metrics_endpoints`.

7. **fact — Client identity boundary**
   - Statement: Client IP is `ASGI request.client.host`; `X-Forwarded-For` is not trusted.
   - Evidence: authority decision `client_ip_source`.

8. **fact — Window semantics**
   - Statement: Global and conversation limits use fixed one-minute and one-hour windows, respectively.
   - Each client-IP window begins with that client’s first counted request.
   - Evidence: authority decisions `window_semantics`, `fixed_window_alignment`.

9. **fact — Dual-counting rule**
   - Statement: Every qualifying conversation-message request increments both global and conversation counters, including attempts rejected by either limit.
   - Evidence: authority decision `dual_limit_counting`.

10. **fact — Dual-limit reporting rule**
    - Statement: When both limits apply, the reported limit is selected by lower remaining ratio; equal ratios select earlier reset; equal reset times select conversation.
    - The same selection governs rejection headers and HTTP `429` `retry_after`.
    - Evidence: authority decisions `dual_limit_headers`, `equal_ratio_tie_break`, `simultaneous_rejection`.

11. **fact — Retry and reset semantics**
    - Statement: `X-RateLimit-Reset` is Unix epoch seconds at the end of the selected blocking window.
    - `retry_after` is the ceiling of seconds until the blocking window ends.
    - Global rejection uses the same Chinese body structure and global-window `retry_after`.
    - Evidence: authority decisions `reset_header`, `retry_after`, `global_429_body`.

12. **fact — Route scope**
    - Statement: Conversation routing mounts at `/v2/conversation`; the message handler declares `/{session_id}/message`.
    - The verified exact limiting route is:
      ```text
      POST /v2/conversation/{single-segment}/message
      ```
    - Nested paths such as the following remain global-only:
      ```text
      POST /v2/conversation/a/nested/message
      ```
    - Evidence: `SRC-3`; `SRC-4`; LR-2; authority decision `route_evidence`.

13. **fact — Executed verification**
    - Statement: The supplied isolated test command exited with return code `0` and reported `12 passed in 1.21s`.
    - Evidence:
      ```text
      python -c import os,pytest; os.chdir('apps/api'); raise SystemExit(pytest.main(['-q','tests/test_ip_rate_limit_eval.py']))
      ```
      Source: LR-1, `actual-results`, `HOST PREFLIGHT EVIDENCE`.

14. **fact — Verified outcome scope**
    - Statement: The executed 12-test suite verified threshold-exceeding configured global and conversation requests receive `429`; covered rejection cases expose retry metadata and rate-limit headers; `/healthz` and `/metrics` bypass limiting; no Redis dependency was evidenced in that suite.
    - Evidence: LR-1.

15. **fact — Corrective-learning evidence**
    - Statement: Initial QA found over-broad conversation path classification. The correction retained exact single-segment matching, and the nested-path regression passed in the current isolated suite.
    - Evidence: LR-2; QA-2; DEL-6.

16. **fact — Delivery authority boundary**
    - Statement: Delivery is restricted to `local-review-package-only`; remote Git, merge, deploy, and network authority are false.
    - Working file scope is:
      ```text
      apps/api/app/core/rate_limit.py
      ```
    - Current patch SHA-256:
      ```text
      6b3a145486ed48946c2768e42292cd9be06a3892cebdbdf60121d254f056172d
      ```
    - Evidence: LR-3; DEL-1 through DEL-8.

17. **fact — Frozen scope**
    - Statement: Only frozen Requirement 1 scope is authorized. Threshold adjustment, Redis adoption, distributed-state design, documentation changes, merge, deployment, and remote publication are excluded.
    - Evidence: LR-5; `decisions[0]`.

18. **fact — Current quality calibration**
    - Statement: Health score is `82/100`; confidence is high within the executed 12-test black-box scope and incomplete for unexecuted acceptance-criterion edge semantics.
    - `PytestDeprecationWarning` is non-failing and remains a maintenance signal.
    - Evidence: LR-4; QA-1 through QA-5; DEL-5.

19. **assumption — Exact route classification remains correct beyond tested cases**
    - Statement: Exact single-segment classification is likely correct for the frozen scope.
    - Basis: Corrected nested-route regression passed.
    - Limit: Evidence covers the current isolated suite, not all possible route forms.
    - Evidence: HYP-1; QA-2; DEL-6.

20. **assumption — Local in-process limiting satisfies Requirement 1 outside isolated execution**
    - Statement: Local in-process behavior is likely sufficient within frozen Requirement 1.
    - Basis: Requirement and local verification support in-memory MVP behavior.
    - Limit: No production traffic, cost, topology, or multi-process evidence is supplied.
    - Evidence: HYP-2; LR-5; QA-3.

21. **assumption — Covered rejection metadata is adequate beyond tested cases**
    - Statement: Header and retry behavior is likely adequate for covered rejection cases.
    - Limit: Fractional timing, complete dual-limit selection permutations, and all acceptance edge semantics lack current execution evidence.
    - Evidence: HYP-3; QA-3.

22. **open-question — Default threshold boundaries**
    - Unknown: Current executable evidence for exact `10/30` default boundaries.
    - Why material: Boundary interpretation changes observable `429` behavior.
    - Evidence absent: UNK-2; QA-5.

23. **open-question — One-hour conversation recovery**
    - Unknown: Current executable evidence for full recovery after the conversation one-hour window.
    - Why material: Recovery timing changes observable availability.
    - Evidence absent: UNK-2; QA-5.

24. **open-question — Fractional `ceil` timing**
    - Unknown: Current executable evidence for fractional remaining-time `ceil` behavior.
    - Why material: It changes observable `retry_after`.
    - Evidence absent: UNK-2; QA-5.

25. **open-question — Complete selection permutations**
    - Unknown: Current executable evidence for lower-ratio, equal-ratio, earlier-reset, equal-reset, and simultaneous dual-rejection selection.
    - Why material: It changes selected headers and rejection metadata.
    - Evidence absent: UNK-2; QA-5.

26. **open-question — Direct per-process storage observation**
    - Unknown: Current executable evidence directly observing per-process storage behavior.
    - Why material: Per-process scope is an authorized MVP boundary.
    - Evidence absent: UNK-2; QA-5.

27. **open-question — Production operational impact**
    - Unknown: Traffic volume, request distribution, cost, process topology, and availability requirements.
    - Status: Known unavailable and non-blocking for frozen Requirement 1.
    - Evidence: OPEN-1; QA-5; `background_evidence_gap`.

28. **open-question — Customer and operator impact**
    - Unknown: Direct customer or operator reports regarding `429` usability, retry behavior, false positives, and health-route accessibility.
    - Evidence absent: UNK-3; supplied feedback contains QA and delivery-preflight feedback only.

29. **open-question — Async fixture-loop maintenance risk**
    - Unknown: Whether unset `asyncio_default_fixture_loop_scope` will affect future fixture-loop behavior.
    - Current status: The warning is non-failing in supplied verification.
    - Evidence: UNK-4; `HOST PREFLIGHT EVIDENCE.stderr`; DEL-5.

30. **conflict — Header scope**
    - Requirement claim:
      ```text
      THE rate limiter SHALL include X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset headers in all responses
      ```
    - Authorized clarification:
      ```text
      Do not count requests and do not emit rate-limit headers.
      ```
      for exempt endpoints.
    - Authority status: Explicit owner decision clarifies the ambiguous broad requirement wording; exempt endpoints have no rate-limit headers.
    - Evidence: `SRC-1`, AC-6; authority decision `exempt_endpoints`; authority hierarchy.

31. **conflict — Reference implementation versus binding behavior**
    - Reference design claim: `slowapi>=0.1.9`, related file changes, and a particular limiter integration.
    - Authorized decision: The `slowapi` excerpt is non-binding; observable behavior controls; no new dependency is required.
    - Authority status: `SRC-2` does not establish implementation scope or dependency authority.
    - Evidence: `SRC-2`; authority decision `implementation_choice`; LR-3; LR-5.

## Target-user framing

- **Primary user:** System operator managing API abuse and LLM API cost exposure.
- **Affected external actor:** Client identified by source IP.
- **Unverified affected users:** Customers and operators receiving `429` responses; no direct feedback is supplied.
- **Scope boundary:** Local, per-process MVP behavior only; no production topology conclusion is supported.

## Problem framing

A single client IP may issue high-volume API requests, including conversation-message requests, causing potential LLM API cost loss. The frozen requirement defines observable rate-limiting behavior for per-IP request volume, exempt operational endpoints, rejection metadata, and local in-memory scope.

The supplied evidence supports current isolated behavior for 12 tested cases. It does not establish complete acceptance-criterion edge behavior, production impact, customer usability, or distributed-state needs.

## Impact framing

- **Supported business impact:** Unrestricted malicious bulk requests may cause LLM API costs to become uncontrolled. Evidence: `SRC-1`.
- **Supported user impact:** Threshold-exceeding requests receive HTTP `429` in covered cases. Evidence: LR-1.
- **Supported operational impact:** `/healthz` and `/metrics` remain accessible without rate-limit counting in covered cases. Evidence: LR-1; authority decision `exempt_endpoints`.
- **Unsupported impact conclusions:** False-positive rate, customer satisfaction, retry usability, production traffic reduction, cost reduction, multi-worker behavior, and availability impact. Evidence absent: UNK-2, UNK-3, OPEN-1.

## Evidence links

| Evidence | Supported frame |
|---|---|
| `SRC-1` | User, cost-control problem, thresholds, configuration, in-memory MVP, endpoint exemptions, broad header requirement |
| `SRC-2` | Non-binding reference design and implementation claims |
| `SRC-3`, `SRC-4` | Mounted conversation route and declared message route |
| LR-1 | Isolated command result and covered black-box outcomes |
| LR-2 | Nested-path classification defect and correction evidence |
| LR-3, LR-5 | Delivery authority, file scope, frozen Requirement 1 boundary |
| LR-4 | Health score, confidence limit, maintenance warning |
| Authority decisions | IP source, windows, selection rules, headers, retry/reset behavior, defaults, scope clarifications |

## Critical gaps

1. Executable evidence for unresolved AC edge semantics: default boundaries, one-hour recovery, fractional `ceil`, complete tie-break behavior, simultaneous rejection, and direct per-process storage.
2. Production traffic, request distribution, cost, topology, and availability evidence.
3. Customer or operator feedback on rejection usability and false positives.
4. Future impact of `PytestDeprecationWarning` on fixture-loop behavior.