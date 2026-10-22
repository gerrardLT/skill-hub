Status: passed

## Requirements

1. **REQ-1 — IP-level API rate limiting**
   - **Statement:** MirrorMind shall enforce IP-level API rate limiting within Production Readiness Requirement 1.
   - **Source links:** SRC-1; Problem frame item 1.
   - **Authority:** Frozen Requirement 1.
   - **Rationale:** Control LLM API cost exposure from bulk or malicious requests.
   - **Relationships:** REQ-2 through REQ-10; SCOPE-1.

2. **REQ-2 — Client identity**
   - **Statement:** Rate-limit identity shall use `ASGI request.client.host` only. `X-Forwarded-For` shall not be trusted.
   - **Source links:** Source-and-authority metadata `client_ip_source`; Problem frame item 16.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-1; RULE-1.

3. **REQ-3 — Conversation-message limit**
   - **Statement:** A client IP that exceeds 10 `POST` requests to `/v2/conversation/{session_id}/message` within its one-hour fixed window shall receive HTTP 429.
   - **Source links:** SRC-1 acceptance criterion 1; SRC-3; SRC-4; metadata `route_evidence`, `configuration_defaults`, `window_semantics`.
   - **Authority:** Frozen Requirement 1; explicit owner clarification for route and window semantics.
   - **Relationships:** RULE-2, RULE-3, RULE-6, RULE-7, RULE-9.

4. **REQ-4 — Global API limit**
   - **Statement:** A client IP that exceeds 30 requests to any non-exempt API endpoint within its one-minute fixed window shall receive HTTP 429.
   - **Source links:** SRC-1 acceptance criterion 2; metadata `configuration_defaults`, `window_semantics`.
   - **Authority:** Frozen Requirement 1; explicit owner clarification for window semantics.
   - **Relationships:** RULE-2, RULE-4, RULE-6, RULE-7, RULE-9.

5. **REQ-5 — Configurable thresholds**
   - **Statement:** Conversation and global thresholds shall be configurable through `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE`.
   - **Source links:** SRC-1 acceptance criterion 3; metadata `configuration_defaults`.
   - **Authority:** Frozen Requirement 1; explicit owner decision.
   - **Relationships:** RULE-5; DEP-1.

6. **REQ-6 — Default thresholds**
   - **Statement:** Default threshold values shall be 10 conversation requests per hour and 30 global requests per minute.
   - **Source links:** SRC-1 acceptance criteria 1–3; metadata `configuration_defaults`.
   - **Authority:** Frozen Requirement 1; explicit owner decision.
   - **Relationships:** REQ-3, REQ-4, REQ-5.

7. **REQ-7 — Exempt endpoints**
   - **Statement:** `/healthz` and `/metrics` shall be exempt from rate limiting. Their requests shall not increment rate-limit counters, and their responses shall not include rate-limit headers.
   - **Source links:** SRC-1 acceptance criterion 5; metadata `exempt_endpoints`, `internal_metrics_endpoints`.
   - **Authority:** Explicit owner decision clarifying SRC-1.
   - **Relationships:** RULE-1; RULE-8.

8. **REQ-8 — Rate-limit response headers**
   - **Statement:** Every non-exempt response shall include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.
   - **Source links:** SRC-1 acceptance criterion 6; metadata `exempt_endpoints`, `reset_header`.
   - **Authority:** Frozen Requirement 1; explicit owner clarification.
   - **Relationships:** RULE-8, RULE-9, RULE-10.

9. **REQ-9 — Conversation-limit rejection body**
   - **Statement:** A rejection caused by the conversation limit shall return HTTP 429 with JSON body `{"detail": "请求过于频繁，请稍后再试", "retry_after": <seconds>}`.
   - **Source links:** SRC-1 acceptance criterion 1; metadata `retry_after`.
   - **Authority:** Frozen Requirement 1; explicit owner clarification.
   - **Relationships:** RULE-9, RULE-10.

10. **REQ-10 — Global-limit rejection body**
    - **Statement:** A rejection caused by the global limit shall return HTTP 429 with JSON fields `detail` equal to `请求过于频繁，请稍后再试` and `retry_after` corresponding to the global blocking window.
    - **Source links:** Metadata `global_429_body`, `retry_after`.
    - **Authority:** Explicit owner decision.
    - **Relationships:** RULE-9, RULE-10.

11. **REQ-11 — In-memory MVP state**
    - **Statement:** Rate-limit state shall be in-memory for the MVP and shall operate per process.
    - **Source links:** SRC-1 acceptance criterion 4; metadata `in_memory_scope`.
    - **Authority:** Frozen Requirement 1; explicit owner clarification.
    - **Relationships:** SCOPE-2; SCOPE-3; DEP-1.

12. **REQ-12 — Existing application target**
    - **Statement:** The requirement applies to the existing FastAPI application at `apps/api`.
    - **Source links:** Supplied constraints and decisions.
    - **Authority:** Supplied execution constraint.
    - **Relationships:** DEP-1; SCOPE-1.

13. **REQ-13 — Observed test progression**
    - **Statement:** Tests for the change shall demonstrate observed RED before GREEN.
    - **Source links:** Supplied constraints and decisions.
    - **Authority:** Supplied execution constraint.
    - **Relationships:** DEP-2.

## Rules

1. **RULE-1 — Counted request boundary**
   - **Statement:** Only non-exempt requests participate in rate-limit counting and rate-limit response metadata.
   - **Source links:** SRC-1 acceptance criterion 5; metadata `exempt_endpoints`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-2, REQ-4, REQ-7, REQ-8.

2. **RULE-2 — Fixed-window duration**
   - **Statement:** Global counting uses a fixed one-minute window. Conversation counting uses a fixed one-hour window.
   - **Source links:** Metadata `window_semantics`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-3, REQ-4.

3. **RULE-3 — Fixed-window alignment**
   - **Statement:** Each fixed window for a client IP begins on that client IP’s first counted request.
   - **Source links:** Metadata `fixed_window_alignment`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-3, REQ-4, RULE-2.

4. **RULE-4 — Global threshold boundary**
   - **Statement:** The first 30 global requests within a client IP’s global window remain within the threshold. The 31st request exceeds the threshold.
   - **Source links:** SRC-1 wording “more than 30 requests”; Problem frame item 8.
   - **Authority:** Frozen Requirement 1.
   - **Relationships:** REQ-4.

5. **RULE-5 — Conversation threshold boundary**
   - **Statement:** The first 10 conversation-message requests within a client IP’s conversation window remain within the threshold. The 11th request exceeds the threshold.
   - **Source links:** SRC-1 wording “more than 10 POST requests”; Problem frame item 6.
   - **Authority:** Frozen Requirement 1.
   - **Relationships:** REQ-3.

6. **RULE-6 — Dual counter increment**
   - **Statement:** Every non-exempt conversation-message request shall increment both the global and conversation counters, including an attempt rejected by either threshold.
   - **Source links:** Metadata `dual_limit_counting`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-3, REQ-4, RULE-1.

7. **RULE-7 — Applicable-limit reporting**
   - **Statement:** When both limits apply to a response, rate-limit headers shall report the limit with the lower remaining ratio.
   - **Source links:** Metadata `dual_limit_headers`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-8; RULE-8.

8. **RULE-8 — Applicable-limit tie break**
   - **Statement:** If applicable limits have equal remaining ratios, reporting shall select the earlier reset. If reset times also tie, reporting shall select the conversation limit.
   - **Source links:** Metadata `equal_ratio_tie_break`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-8; RULE-7.

9. **RULE-9 — Simultaneous rejection selection**
   - **Statement:** When both limits reject one request, HTTP 429 headers and `retry_after` shall select the limit using lower remaining ratio, then earlier reset, then conversation limit.
   - **Source links:** Metadata `simultaneous_rejection`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-8, REQ-9, REQ-10; RULE-7, RULE-8.

10. **RULE-10 — Retry and reset values**
    - **Statement:** `retry_after` shall equal the ceiling of seconds remaining until the selected blocking window ends. `X-RateLimit-Reset` shall be Unix epoch seconds for the selected blocking or reported window end.
    - **Source links:** Metadata `retry_after`, `reset_header`.
    - **Authority:** Explicit owner decision.
    - **Relationships:** REQ-8, REQ-9, REQ-10; RULE-9.

11. **RULE-11 — Authority precedence**
    - **Statement:** Explicit owner decisions clarify and override ambiguous Requirement 1 wording only. Otherwise, frozen Requirement 1 controls. SRC-2 does not control observable behavior or dependency selection.
    - **Source links:** Metadata `authority_hierarchy`, `implementation_choice`; Problem frame items 27–28.
    - **Authority:** Explicit owner decision.
    - **Relationships:** DEP-1; SCOPE-4.

12. **RULE-12 — Execution restrictions**
    - **Statement:** Work shall not use network access, remote Git, merge operations, deployment operations, or modifications to the original `D:/tem_projects/MirrorMind` worktree.
    - **Source links:** Supplied constraints and decisions; source-and-authority metadata `network`, `remote_git`, `merge`, `deploy`.
    - **Authority:** Supplied execution constraint.
    - **Relationships:** SCOPE-5.

## Dependencies

1. **DEP-1 — Existing FastAPI application and local implementation choice**
   - **Statement:** The rate limiting behavior depends on the existing FastAPI application at `apps/api`. The implementation shall use in-memory state and shall not add Redis or any dependency solely because SRC-2 references `slowapi>=0.1.9`.
   - **Source links:** Supplied constraints; SRC-2; metadata `implementation_choice`, `in_memory_scope`, `redis_option`.
   - **Authority:** Supplied constraint; explicit owner decision.
   - **Relationships:** REQ-5, REQ-11, REQ-12; RULE-11; SCOPE-2.

2. **DEP-2 — Local test capability**
   - **Statement:** Completion depends on local test execution capable of recording observed RED and subsequent GREEN results.
   - **Source links:** Supplied constraints and decisions.
   - **Authority:** Supplied execution constraint.
   - **Relationships:** REQ-13.

## Scope

1. **SCOPE-1 — Included product scope**
   - **Statement:** Included scope is Production Readiness Requirement 1 for IP-level API rate limiting of MirrorMind, covering global API request volume and conversation-message request volume by client IP.
   - **Source links:** SRC-1; Problem frame items 1–4 and 7.
   - **Authority:** Frozen Requirement 1.
   - **Relationships:** REQ-1 through REQ-10.

2. **SCOPE-2 — Included storage scope**
   - **Statement:** Included MVP storage scope is in-memory, per-process rate-limit state.
   - **Source links:** SRC-1 acceptance criterion 4; metadata `in_memory_scope`.
   - **Authority:** Frozen Requirement 1; explicit owner clarification.
   - **Relationships:** REQ-11; DEP-1.

3. **SCOPE-3 — Excluded distributed storage scope**
   - **Statement:** Shared multi-worker rate-limit storage and Redis-backed rate limiting are excluded from the current requirement. Redis remains a documented future upgrade only.
   - **Source links:** SRC-1 acceptance criterion 4; metadata `in_memory_scope`, `redis_option`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** REQ-11; DEP-1.

4. **SCOPE-4 — Excluded reference-design authority**
   - **Statement:** SRC-2’s `slowapi>=0.1.9` dependency and code excerpt are non-binding reference context. They do not require a dependency, design, or behavior not established by higher authority.
   - **Source links:** SRC-2; metadata `implementation_choice`.
   - **Authority:** Explicit owner decision.
   - **Relationships:** RULE-11; DEP-1.

5. **SCOPE-5 — Excluded execution operations**
   - **Statement:** Network access, remote Git operations, merges, deployments, and changes to `D:/tem_projects/MirrorMind` are excluded.
   - **Source links:** Supplied constraints; source-and-authority metadata.
   - **Authority:** Supplied execution constraint.
   - **Relationships:** RULE-12.

## Open Items

1. **OPEN-1 — Traffic and cost measurements unavailable**
   - **Statement:** Actual traffic volume and LLM cost measurements are unavailable.
   - **Source links:** Metadata `background_evidence_gap`; Problem frame critical gaps.
   - **Authority:** Explicit owner decision.
   - **Uncertainty status:** Known unavailable; non-blocking.
   - **Impact:** Does not alter the required thresholds, scope, authority, or observable behavior.
   - **Relationships:** REQ-1.
