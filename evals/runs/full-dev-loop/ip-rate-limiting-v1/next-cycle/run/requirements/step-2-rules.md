Status: needs-input

## Requirements

1. **REQ-1 — Per-IP conversation-message rate limiting**
   - Statement: A client identified by source IP making more than 10 `POST` requests to `POST /v2/conversation/{single-segment}/message` within its fixed one-hour conversation window shall receive HTTP `429`.
   - Source links: `SRC-1` AC-1; `SRC-3`; `SRC-4`; authority decisions `configuration_defaults`, `window_semantics`, `fixed_window_alignment`, `route_evidence`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Rationale: Limit malicious bulk LLM conversation requests and uncontrolled API cost.
   - Relationships: `RULE-1`, `RULE-2`, `RULE-4`, `RULE-5`, `RULE-7`, `RULE-8`, `RULE-10`, `REQ-4`.

2. **REQ-2 — Per-IP global API rate limiting**
   - Statement: A client identified by source IP making more than 30 requests to any non-exempt API endpoint within its fixed one-minute global window shall receive HTTP `429`.
   - Source links: `SRC-1` AC-2; authority decisions `configuration_defaults`, `window_semantics`, `fixed_window_alignment`, `global_429_body`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Rationale: Limit broad API abuse and uncontrolled LLM API cost exposure.
   - Relationships: `RULE-1`, `RULE-2`, `RULE-3`, `RULE-5`, `RULE-7`, `RULE-8`, `RULE-10`, `REQ-4`.

3. **REQ-3 — Configurable normative thresholds**
   - Statement: Conversation and global thresholds shall be configurable through `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE`. Default values shall be 10 conversation requests per hour and 30 global requests per minute.
   - Source links: `SRC-1` AC-3; authority decision `configuration_defaults`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-1`, `REQ-2`, `OPEN-1`.

4. **REQ-4 — Rejection response metadata**
   - Statement: A rate-limited request shall receive HTTP `429` with Chinese `detail`, `retry_after`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`, subject to the exempt-endpoint exception in `RULE-3`.
   - Source links: `SRC-1` AC-1, AC-2, AC-6; authority decisions `reset_header`, `retry_after`, `global_429_body`, `dual_limit_headers`, `simultaneous_rejection`, `exempt_endpoints`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Relationships: `RULE-3`, `RULE-7`, `RULE-8`, `RULE-9`, `RULE-10`, `CONFLICT-1`.

5. **REQ-5 — In-memory per-process MVP state**
   - Statement: Rate-limit state shall use in-memory per-process storage. Shared multi-worker state and Redis are not required for the MVP.
   - Source links: `SRC-1` AC-4; authority decisions `in_memory_scope`, `redis_option`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Relationships: `SCOPE-1`, `SCOPE-2`, `DEP-1`, `OPEN-5`.

6. **REQ-6 — Exempt operational endpoints**
   - Statement: Requests to `/healthz` and `/metrics` shall not be counted by either rate limit and shall not emit rate-limit headers.
   - Source links: `SRC-1` AC-5; authority decisions `exempt_endpoints`, `internal_metrics_endpoints`.
   - Authority: Explicit owner decision.
   - Relationships: `RULE-3`, `CONFLICT-1`.

7. **REQ-7 — Exact conversation route scope**
   - Statement: Conversation-specific limiting shall apply only to `POST /v2/conversation/{single-segment}/message`. Nested paths, including `POST /v2/conversation/a/nested/message`, shall remain subject only to global limiting.
   - Source links: `SRC-3`; `SRC-4`; LR-2; authority decision `route_evidence`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-1`, `REQ-2`, `RULE-4`, `OPEN-6`.

8. **REQ-8 — Next-cycle verification handoff**
   - Statement: Next-cycle work shall preserve evidence that tests observed RED before GREEN for changed behavior. This handoff shall not implement, merge, deploy, or claim production observations.
   - Source links: Supplied constraints and decisions.
   - Authority: Supplied execution constraint.
   - Relationships: `SCOPE-3`, `SCOPE-4`, `DEP-2`.

## Rules

1. **RULE-1 — Client identity**
   - Statement: Client IP shall be obtained solely from `ASGI request.client.host`. `X-Forwarded-For` shall not be trusted.
   - Source links: Authority decision `client_ip_source`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-1`, `REQ-2`.

2. **RULE-2 — Fixed-window alignment**
   - Statement: Global limits use fixed one-minute windows and conversation limits use fixed one-hour windows. Each window for a client IP begins with that client IP's first counted request.
   - Source links: Authority decisions `window_semantics`, `fixed_window_alignment`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-1`, `REQ-2`, `RULE-7`, `RULE-8`, `OPEN-2`.

3. **RULE-3 — Exemption precedence**
   - Statement: `/healthz` and `/metrics` are exempt from counting and rate-limit headers. This exemption overrides the broad requirement that rate-limit headers appear in all responses.
   - Source links: `SRC-1` AC-5, AC-6; authority decisions `exempt_endpoints`, `internal_metrics_endpoints`.
   - Authority: Explicit owner clarification.
   - Relationships: `REQ-4`, `REQ-6`, `CONFLICT-1`.

4. **RULE-4 — Conversation qualification**
   - Statement: Only the verified exact route `POST /v2/conversation/{single-segment}/message` qualifies for conversation counting. A qualifying request increments both the conversation and global counters.
   - Source links: `SRC-3`; `SRC-4`; LR-2; authority decisions `route_evidence`, `dual_limit_counting`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-1`, `REQ-2`, `REQ-7`, `RULE-5`.

5. **RULE-5 — Rejected conversation attempts remain counted**
   - Statement: Every qualifying conversation-message request increments both counters, including an attempt rejected by either the global or conversation limit.
   - Source links: Authority decision `dual_limit_counting`.
   - Authority: Explicit owner decision.
   - Relationships: `RULE-4`, `RULE-6`, `RULE-7`, `RULE-8`.

6. **RULE-6 — Dual-limit applicability**
   - Statement: A qualifying conversation-message request is evaluated against both global and conversation limits. Either exceeded limit may cause HTTP `429`.
   - Source links: `SRC-1` AC-1, AC-2; authority decisions `dual_limit_counting`, `simultaneous_rejection`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Relationships: `RULE-5`, `RULE-7`, `RULE-8`, `RULE-9`.

7. **RULE-7 — Dual-limit report selection**
   - Statement: When both limits apply, select the reported limit by lower remaining ratio. If ratios are equal, select the earlier reset. If reset times are equal, select the conversation limit.
   - Source links: Authority decisions `dual_limit_headers`, `equal_ratio_tie_break`, `simultaneous_rejection`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-4`, `RULE-6`, `RULE-8`, `RULE-9`, `OPEN-4`.

8. **RULE-8 — Reset and retry semantics**
   - Statement: `X-RateLimit-Reset` shall be Unix epoch seconds at the end of the selected blocking window. `retry_after` shall be the ceiling of seconds until that window ends.
   - Source links: Authority decisions `reset_header`, `retry_after`, `global_429_body`, `simultaneous_rejection`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-4`, `RULE-7`, `RULE-9`, `OPEN-3`.

9. **RULE-9 — Global rejection body**
   - Statement: Global-limit rejection shall use the same Chinese `detail` and `retry_after` body structure as conversation-limit rejection. Its `retry_after` shall correspond to the selected global blocking window when global is selected.
   - Source links: Authority decision `global_429_body`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-4`, `RULE-7`, `RULE-8`.

10. **RULE-10 — Threshold interpretation**
    - Statement: Requests exceeding the configured limit shall be rejected; requests at the configured limit remain permitted within the applicable window.
    - Source links: `SRC-1` AC-1, AC-2; authority decision `configuration_defaults`.
    - Authority: Frozen Requirement 1.
    - Relationships: `REQ-1`, `REQ-2`, `REQ-3`, `OPEN-1`.
    - Uncertainty: Exact default-boundary execution evidence is currently absent.

11. **RULE-11 — Implementation authority**
    - Statement: Observable behavior controls. The `slowapi>=0.1.9` reference design is non-binding; no new dependency is required.
    - Source links: `SRC-2`; authority decision `implementation_choice`; LR-3; LR-5.
    - Authority: Explicit owner decision.
    - Relationships: `DEP-1`, `CONFLICT-2`.

## Dependencies

1. **DEP-1 — Existing FastAPI application**
   - Statement: Work is constrained to the existing FastAPI application at `apps/api`.
   - Source links: Supplied constraints and decisions.
   - Authority: Supplied execution constraint.
   - Relationships: `REQ-5`, `RULE-11`.

2. **DEP-2 — Local verification environment**
   - Statement: Verification depends on local execution only; network access, remote Git, merge, and deployment authority are unavailable.
   - Source links: Supplied constraints and decisions; source and authority metadata.
   - Authority: Supplied execution constraint.
   - Relationships: `REQ-8`, `SCOPE-3`, `SCOPE-4`.

3. **DEP-3 — Existing route declarations**
   - Statement: Exact conversation-route classification depends on `apps/api/app/api/v2/__init__.py` mounting `conversation.router` at `/v2/conversation` and `conversation.py` declaring `/{session_id}/message`.
   - Source links: `SRC-3`; `SRC-4`; authority decision `route_evidence`.
   - Authority: Explicit owner decision.
   - Relationships: `REQ-7`, `RULE-4`.

4. **DEP-4 — Current isolated verification evidence**
   - Statement: The supplied isolated suite executed successfully with `12 passed in 1.21s`.
   - Source links: LR-1; `actual-results`; `HOST PREFLIGHT EVIDENCE`.
   - Authority: Executed local evidence.
   - Relationships: `OPEN-1`, `OPEN-2`, `OPEN-3`, `OPEN-4`, `OPEN-5`, `OPEN-6`.
   - Limitation: This evidence does not cover all required edge semantics.

## Scope

1. **SCOPE-1 — Included MVP scope**
   - Statement: Frozen Requirement 1 local, in-memory, per-process IP rate-limiting behavior is included.
   - Source links: `SRC-1`; LR-5; authority decision `in_memory_scope`.
   - Authority: Frozen Requirement 1; explicit owner decision.
   - Relationships: `REQ-1` through `REQ-7`.

2. **SCOPE-2 — Excluded architecture scope**
   - Statement: Redis adoption, distributed/shared multi-worker state, threshold adjustment, documentation changes, and new rate-limit dependencies are excluded.
   - Source links: LR-5; `decisions[0]`; authority decisions `in_memory_scope`, `redis_option`, `implementation_choice`.
   - Authority: Frozen Requirement 1; explicit owner decisions.
   - Relationships: `REQ-5`, `RULE-11`, `CONFLICT-2`.

3. **SCOPE-3 — Excluded delivery scope**
   - Statement: Remote Git, merge, deployment, remote publication, and network actions are excluded.
   - Source links: LR-3; DEL-1 through DEL-8; supplied constraints and decisions.
   - Authority: Delivery authority metadata.
   - Relationships: `DEP-2`, `REQ-8`.

4. **SCOPE-4 — Worktree boundary**
   - Statement: The original `D:/tem_projects/MirrorMind` worktree shall not be modified.
   - Source links: Supplied constraints and decisions.
   - Authority: Supplied execution constraint.
   - Relationships: `REQ-8`.

5. **SCOPE-5 — Current working-file boundary**
   - Statement: Current patch evidence is limited to `apps/api/app/core/rate_limit.py`, SHA-256 `6b3a145486ed48946c2768e42292cd9be06a3892cebdbdf60121d254f056172d`.
   - Source links: LR-3; DEL-1 through DEL-8.
   - Authority: Delivery evidence.
   - Relationships: `SCOPE-1`.
   - Limitation: This is delivery evidence, not permission for implementation in this handoff.

6. **SCOPE-6 — Unsupported production conclusions**
   - Statement: Production traffic volume, request distribution, cost reduction, process topology, availability impact, customer usability, false-positive rate, and multi-worker behavior are not established by supplied evidence.
   - Source links: OPEN-1; UNK-2; UNK-3; QA-3; QA-5.
   - Authority: Evidence limitation.
   - Relationships: `OPEN-7`, `OPEN-8`.

## Conflicts

1. **CONFLICT-1 — Broad header wording versus exempt endpoints**
   - Statement: The broad claim requiring rate-limit headers in all responses conflicts with the authorized exemption for `/healthz` and `/metrics`.
   - Resolution: `RULE-3` governs. Exempt endpoints are not counted and emit no rate-limit headers.
   - Source links: `SRC-1` AC-5, AC-6; authority decision `exempt_endpoints`; authority hierarchy.
   - Authority: Explicit owner clarification overrides ambiguous broad wording only.
   - Relationships: `REQ-4`, `REQ-6`, `RULE-3`.

2. **CONFLICT-2 — Reference implementation versus observable contract**
   - Statement: The `slowapi>=0.1.9` reference design conflicts with the decision that no new dependency is required and observable behavior controls.
   - Resolution: `RULE-11` governs. The reference implementation is non-binding.
   - Source links: `SRC-2`; authority decision `implementation_choice`; LR-3; LR-5.
   - Authority: Explicit owner decision.
   - Relationships: `DEP-1`, `SCOPE-2`, `RULE-11`.

## Open Items

1. **OPEN-1 — Default-threshold boundary evidence**
   - Statement: Executable evidence for exact default `10/30` threshold boundaries is absent.
   - Why material: Boundary interpretation changes observable `429` behavior.
   - Source links: UNK-2; QA-5.
   - Authority needed: No new policy authority identified; next-cycle verification evidence is needed.
   - Relationships: `REQ-3`, `RULE-10`.
   - Status: Needs input.

2. **OPEN-2 — Conversation-window recovery evidence**
   - Statement: Executable evidence for availability restoration after the complete one-hour conversation window is absent.
   - Why material: Recovery timing changes observable availability.
   - Source links: UNK-2; QA-5.
   - Authority needed: No new policy authority identified; next-cycle verification evidence is needed.
   - Relationships: `RULE-2`, `RULE-8`.
   - Status: Needs input.

3. **OPEN-3 — Fractional retry timing evidence**
   - Statement: Executable evidence for fractional remaining-time ceiling behavior is absent.
   - Why material: It changes observable `retry_after`.
   - Source links: UNK-2; QA-5.
   - Authority needed: No new policy authority identified; next-cycle verification evidence is needed.
   - Relationships: `RULE-8`.
   - Status: Needs input.

4. **OPEN-4 — Complete dual-limit selection evidence**
   - Statement: Executable evidence is absent for lower-ratio selection, equal-ratio earlier-reset selection, equal-reset conversation selection, and simultaneous dual rejection.
   - Why material: These conditions determine selected headers and rejection metadata.
   - Source links: UNK-2; QA-5.
   - Authority needed: No new policy authority identified; next-cycle verification evidence is needed.
   - Relationships: `RULE-6`, `RULE-7`, `RULE-8`, `RULE-9`.
   - Status: Needs input.

5. **OPEN-5 — Direct per-process storage evidence**
   - Statement: Executable evidence directly observing per-process storage behavior is absent.
   - Why material: Per-process state is the authorized MVP boundary.
   - Source links: UNK-2; QA-5.
   - Authority needed: No new policy authority identified; next-cycle verification evidence is needed.
   - Relationships: `REQ-5`, `SCOPE-1`.
   - Status: Needs input.

6. **OPEN-6 — Exact-route generalization evidence**
   - Statement: Exact single-segment route classification is supported by the corrected nested-path regression but not by evidence covering all possible route forms.
   - Why material: Route classification determines whether conversation limiting applies.
   - Source links: HYP-1; QA-2; DEL-6.
   - Authority needed: No new policy authority identified; additional verification evidence is needed if route forms beyond current scope are relevant.
   - Relationships: `REQ-7`, `RULE-4`.
   - Status: Needs input.

7. **OPEN-7 — Production operational context**
   - Statement: Traffic volume, request distribution, cost, process topology, and availability requirements are unavailable.
   - Why material: These facts would affect future distributed-state and operational decisions.
   - Source links: OPEN-1; QA-5; authority decision `background_evidence_gap`.
   - Authority needed: Product and operations authority, if scope expands beyond frozen Requirement 1.
   - Relationships: `SCOPE-6`.
   - Status: Non-blocking for frozen Requirement 1; needs input for production-scope decisions.

8. **OPEN-8 — Customer and operator impact**
   - Statement: Direct feedback on `429` usability, retry behavior, false positives, and health-route accessibility is absent.
   - Why material: It affects future usability and operational policy decisions.
   - Source links: UNK-3; supplied feedback.
   - Authority needed: Customer and operator evidence, if usability or production policy enters scope.
   - Relationships: `SCOPE-6`.
   - Status: Non-blocking for frozen Requirement 1; needs input for customer-impact conclusions.

9. **OPEN-9 — Async fixture-loop maintenance risk**
   - Statement: The future effect of unset `asyncio_default_fixture_loop_scope` is unknown. The current `PytestDeprecationWarning` is non-failing.
   - Source links: UNK-4; `HOST PREFLIGHT EVIDENCE.stderr`; DEL-5.
   - Authority needed: Test-maintenance ownership if warning remediation enters scope.
   - Relationships: `DEP-4`.
   - Status: Non-blocking maintenance item.