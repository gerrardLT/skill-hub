Status: passed

## problem-frame-artifact

Status: passed

## Classified items

1. **fact** — Scope is limited to Production Readiness Requirement 1: IP-level API rate limiting for MirrorMind.  
   Evidence: Supplied product context.

2. **fact** — Target user is the system operator.  
   Evidence: SRC-1 User Story: “作为系统运维者”.

3. **fact** — The stated problem is that malicious scripts may make bulk LLM API calls from a single IP, causing uncontrolled cost.  
   Evidence: SRC-1 User Story.

4. **fact** — A client IP exceeding 10 `POST` requests to `/v2/conversation/{id}/message` within one hour must receive HTTP 429.  
   Evidence: SRC-1 acceptance criterion 1.

5. **fact** — The conversation endpoint is mounted at `/v2/conversation/{session_id}/message`.  
   Evidence: SRC-3 mounts `conversation.router` at `/v2/conversation`; SRC-4 declares `@router.post("/{session_id}/message")`; source-and-authority metadata `route_evidence`.

6. **fact** — “More than 10” means the first 10 requests remain within the conversation threshold; the 11th request exceeds it.  
   Evidence: SRC-1 wording “more than 10 POST requests”.

7. **fact** — A client IP exceeding 30 requests to any API endpoint within one minute must receive HTTP 429.  
   Evidence: SRC-1 acceptance criterion 2.

8. **fact** — “More than 30” means the first 30 requests remain within the global threshold; the 31st request exceeds it.  
   Evidence: SRC-1 wording “more than 30 requests”.

9. **fact** — The normative default thresholds are 10 conversation requests per hour and 30 global requests per minute.  
   Evidence: SRC-1 acceptance criteria 1–3; source-and-authority metadata `configuration_defaults`.

10. **fact** — Thresholds are configurable through `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE`.  
    Evidence: SRC-1 acceptance criterion 3.

11. **fact** — Rate-limit storage is in-memory for MVP.  
    Evidence: SRC-1 acceptance criterion 4.

12. **fact** — In-memory rate-limit state is per process; shared multi-worker storage is outside this requirement’s scope.  
    Evidence: Source-and-authority metadata `in_memory_scope`.

13. **fact** — Redis is a documented future upgrade only; it is not current MVP behavior.  
    Evidence: SRC-1 acceptance criterion 4; source-and-authority metadata `redis_option`.

14. **fact** — `/healthz` and `/metrics` are exempt endpoints. Their requests are not counted and their responses do not include rate-limit headers.  
    Evidence: SRC-1 acceptance criterion 5; source-and-authority metadata `exempt_endpoints`, `internal_metrics_endpoints`.

15. **fact** — All non-exempt responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.  
    Evidence: SRC-1 acceptance criterion 6, clarified by source-and-authority metadata `exempt_endpoints`.

16. **fact** — Client IP identity uses `ASGI request.client.host`; `X-Forwarded-For` is not trusted.  
    Evidence: Source-and-authority metadata `client_ip_source`.

17. **fact** — Both rate limits use fixed windows: one minute for global counting and one hour for conversation counting.  
    Evidence: Source-and-authority metadata `window_semantics`.

18. **fact** — Each fixed window for a client IP starts on that client IP’s first counted request.  
    Evidence: Source-and-authority metadata `fixed_window_alignment`.

19. **fact** — Every conversation-message request increments both the global and conversation counters, including a request rejected by either threshold.  
    Evidence: Source-and-authority metadata `dual_limit_counting`.

20. **fact** — Conversation-limit HTTP 429 responses contain JSON body `{"detail": "请求过于频繁，请稍后再试", "retry_after": <seconds>}`.  
    Evidence: SRC-1 acceptance criterion 1.

21. **fact** — Global-limit HTTP 429 responses use the same Chinese `detail` and `retry_after` JSON fields; `retry_after` reflects the global blocking window when the global limit causes rejection.  
    Evidence: Source-and-authority metadata `global_429_body`.

22. **fact** — `retry_after` is the ceiling of seconds remaining until the blocking window ends.  
    Evidence: Source-and-authority metadata `retry_after`.

23. **fact** — `X-RateLimit-Reset` is Unix epoch seconds for the selected blocking or reported window end.  
    Evidence: Source-and-authority metadata `reset_header`.

24. **fact** — When both limits apply to a response, headers report the limit with the lower remaining ratio.  
    Evidence: Source-and-authority metadata `dual_limit_headers`.

25. **fact** — If remaining ratios tie, the reported limit is the one with the earlier reset. If both reset times tie, the conversation limit is selected.  
    Evidence: Source-and-authority metadata `equal_ratio_tie_break`.

26. **fact** — When both limits reject the same request, HTTP 429 headers and `retry_after` use the same selection rule: lower remaining ratio, then earlier reset, then conversation limit.  
    Evidence: Source-and-authority metadata `simultaneous_rejection`.

27. **fact** — SRC-2 is a non-binding reference design. Observable behavior and explicit owner decisions control; no new dependency is required by the supplied authority.  
    Evidence: Source-and-authority metadata `implementation_choice`.

28. **assumption** — SRC-2’s `slowapi>=0.1.9` excerpt may describe an earlier implementation preference, but it is not authoritative for current observable behavior.  
    Evidence: SRC-2 dependency and code excerpt; source-and-authority metadata `implementation_choice`.

29. **fact** — Traffic and cost measurements are unavailable. This does not block the stated behavior because the supplied authority classifies the gap as non-blocking context.  
    Evidence: Source-and-authority metadata `background_evidence_gap`.

## Target-user framing

- **Primary user:** System operator.  
  Evidence: SRC-1.
- **Affected external actor:** API client identified by ASGI client IP.  
  Evidence: SRC-1; source-and-authority metadata `client_ip_source`.
- **Protected system concern:** LLM API cost exposure from bulk or malicious API usage.  
  Evidence: SRC-1.

## Problem framing

A single client IP can make repeated API requests, including repeated conversation-message requests that invoke LLM-related processing. The supplied requirement frames this as an operational cost-control problem, specifically preventing malicious scripts from causing uncontrolled LLM API expense.

The required observable boundary comprises:

- Conversation-message request volume per client IP over a one-hour fixed window.
- API request volume per client IP over a one-minute fixed window.
- Exemption of `/healthz` and `/metrics`.
- Distinct HTTP 429 behavior and rate-limit response metadata for non-exempt requests.

## Impact framing

- **Business impact:** Potential uncontrolled LLM API cost.  
  Evidence: SRC-1.
- **Operational impact:** System operators lack the stated IP-level control over burst and sustained API consumption.  
  Evidence: SRC-1 User Story and acceptance criteria.
- **User-facing impact:** Clients exceeding defined thresholds receive HTTP 429, with the specified Chinese error detail and retry timing.  
  Evidence: SRC-1; source-and-authority metadata `global_429_body`, `retry_after`.

## Evidence links

| Source | Supported framing |
|---|---|
| SRC-1 | Normative Requirement 1 scope, user story, thresholds, configuration names, in-memory MVP constraint, exemptions, headers, conversation-limit 429 body |
| SRC-2 | Non-binding prior/reference design context, including `slowapi` and route/config examples |
| SRC-3 | V2 router prefix and conversation router mounting |
| SRC-4 | Concrete conversation message route declaration |
| Source-and-authority metadata | Binding clarifications for IP source, fixed windows, counter behavior, exemption behavior, dual-limit selection, retry and reset semantics, defaults, scope, and authority hierarchy |

## Conflicts

1. **No unresolved conflict.**  
   SRC-2 presents `slowapi>=0.1.9` as a dependency/reference design, while explicit owner authority states that the excerpt is non-binding and no new dependency is required. The authority hierarchy resolves implementation authority without changing Requirement 1 observable behavior.

2. **No unresolved conflict.**  
   SRC-1 requires headers “in all responses,” while explicit owner authority excludes `/healthz` and `/metrics` from both counting and header emission. The owner decision clarifies the exemption boundary.

## Critical gaps

- **Non-blocking evidence gap:** Actual traffic volume and LLM cost measurements are unavailable.  
  Evidence: Source-and-authority metadata `background_evidence_gap`.  
  Status: Does not prevent problem framing or alter required observable behavior.

- **No critical unresolved product, scope, authority, or safety gap identified.**

## requirements-artifact

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


## acceptance-criteria-artifact

Status: passed

## Acceptance Criteria

1. **AC-1 — Client identity uses ASGI peer host**
   - **Given** two requests arrive with the same `ASGI request.client.host` and different `X-Forwarded-For` values
   - **When** the requests are evaluated for rate limiting
   - **Then** they share the same rate-limit identity and counter state.
   - **Given** two requests arrive with different `ASGI request.client.host` values and the same `X-Forwarded-For` value
   - **When** the requests are evaluated for rate limiting
   - **Then** they use separate rate-limit identity and counter state.
   - **Maps to:** REQ-1, REQ-2, RULE-1.

2. **AC-2 — Default configuration values**
   - **Given** `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE` are not configured
   - **When** the FastAPI application at `apps/api` evaluates non-exempt requests
   - **Then** the conversation threshold is 10 requests per one-hour fixed window and the global threshold is 30 requests per one-minute fixed window.
   - **Maps to:** REQ-5, REQ-6, REQ-12, DEP-1.

3. **AC-3 — Configured threshold values govern enforcement**
   - **Given** `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE` are configured with observable test values
   - **When** non-exempt requests are evaluated
   - **Then** conversation enforcement uses `RATE_LIMIT_CONVERSATION_PER_HOUR` and global enforcement uses `RATE_LIMIT_GLOBAL_PER_MINUTE`, rather than the default values.
   - **Maps to:** REQ-5, DEP-1.

4. **AC-4 — Conversation fixed-window boundary**
   - **Given** a client IP sends its first counted `POST` request to `/v2/conversation/{session_id}/message`
   - **When** the client sends the first 10 such requests before one hour has elapsed from that first counted request
   - **Then** none of those 10 requests is rejected by the conversation limit.
   - **When** the same client sends the 11th such request before that one-hour window ends
   - **Then** the response is HTTP 429.
   - **Maps to:** REQ-1, REQ-3, REQ-6, RULE-2, RULE-3, RULE-5.

5. **AC-5 — Conversation rejection response**
   - **Given** a conversation-message request exceeds the conversation threshold and the global limit does not select the rejection
   - **When** the request is evaluated
   - **Then** the response status is HTTP 429.
   - **And Then** the JSON response body is `{"detail": "请求过于频繁，请稍后再试", "retry_after": <seconds>}`.
   - **And Then** `retry_after` equals the ceiling of seconds remaining until the conversation window ends.
   - **And Then** `X-RateLimit-Reset` is the Unix epoch second at the conversation window end.
   - **Maps to:** REQ-3, REQ-8, REQ-9, RULE-9, RULE-10.

6. **AC-6 — Global fixed-window boundary**
   - **Given** a client IP sends its first counted request to a non-exempt API endpoint
   - **When** the client sends the first 30 counted requests before one minute has elapsed from that first counted request
   - **Then** none of those 30 requests is rejected by the global limit.
   - **When** the same client sends the 31st counted request before that one-minute window ends
   - **Then** the response is HTTP 429.
   - **Maps to:** REQ-1, REQ-4, RULE-2, RULE-3, RULE-4.

7. **AC-7 — Global rejection response**
   - **Given** a non-exempt API request exceeds the global threshold and the conversation limit does not select the rejection
   - **When** the request is evaluated
   - **Then** the response status is HTTP 429.
   - **And Then** the JSON response contains `detail` equal to `请求过于频繁，请稍后再试`.
   - **And Then** the JSON response contains `retry_after` equal to the ceiling of seconds remaining until the global window ends.
   - **And Then** `X-RateLimit-Reset` is the Unix epoch second at the global window end.
   - **Maps to:** REQ-4, REQ-8, REQ-10, RULE-9, RULE-10.

8. **AC-8 — Window recovery**
   - **Given** a client IP has exhausted either its conversation or global fixed window
   - **When** the selected blocking window ends and the client makes the next applicable request
   - **Then** that request is evaluated in a new fixed window beginning with that request.
   - **And Then** the prior window’s exhausted count does not cause rejection in the new window.
   - **Maps to:** REQ-3, REQ-4, RULE-2, RULE-3.

9. **AC-9 — Conversation requests increment both counters**
   - **Given** a client IP sends a non-exempt `POST` request to `/v2/conversation/{session_id}/message`
   - **When** the request is evaluated, whether accepted or rejected by either threshold
   - **Then** both that client IP’s conversation counter and global counter increment for the applicable fixed windows.
   - **Maps to:** REQ-3, REQ-4, RULE-6.

10. **AC-10 — Global counting includes non-conversation endpoints**
    - **Given** a client IP sends a request to a non-exempt API endpoint other than `/v2/conversation/{session_id}/message`
    - **When** the request is evaluated
    - **Then** the request increments the global counter.
    - **And Then** it does not increment the conversation-message counter.
    - **Maps to:** REQ-4, RULE-1, RULE-6.

11. **AC-11 — Non-exempt response headers**
    - **Given** a request is made to any non-exempt API endpoint
    - **When** the application returns either a non-429 response or an HTTP 429 response
    - **Then** the response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.
    - **And Then** `X-RateLimit-Reset` is a Unix epoch second for the reported or blocking window end.
    - **Maps to:** REQ-8, RULE-1, RULE-10.

12. **AC-12 — Applicable limit reporting for conversation requests**
    - **Given** a non-exempt conversation-message request has both a global limit and a conversation limit applicable
    - **When** the response is produced
    - **Then** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` describe the limit with the lower remaining ratio.
    - **Maps to:** REQ-8, RULE-7.

13. **AC-13 — Applicable-limit tie breaking**
    - **Given** both applicable limits have equal remaining ratios for a conversation-message response
    - **When** one limit has an earlier reset time
    - **Then** the rate-limit headers describe the limit with the earlier reset time.
    - **Given** both applicable limits have equal remaining ratios and equal reset times
    - **When** the response is produced
    - **Then** the rate-limit headers describe the conversation limit.
    - **Maps to:** REQ-8, RULE-8.

14. **AC-14 — Simultaneous rejection selection**
    - **Given** one conversation-message request exceeds both the global and conversation thresholds
    - **When** the HTTP 429 response is produced
    - **Then** the response headers and JSON `retry_after` describe the selected blocking limit with the lower remaining ratio.
    - **Given** both blocking limits have equal remaining ratios
    - **When** their reset times differ
    - **Then** the response headers and JSON `retry_after` describe the limit with the earlier reset.
    - **Given** both blocking limits have equal remaining ratios and equal reset times
    - **When** the HTTP 429 response is produced
    - **Then** the response headers and JSON `retry_after` describe the conversation limit.
    - **Maps to:** REQ-8, REQ-9, REQ-10, RULE-7, RULE-8, RULE-9, RULE-10.

15. **AC-15 — Exempt endpoints neither count nor expose metadata**
    - **Given** a client IP makes requests to `/healthz` or `/metrics`
    - **When** those requests are evaluated
    - **Then** they do not increment either rate-limit counter.
    - **And Then** their responses do not include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, or `X-RateLimit-Reset`.
    - **Given** a client IP exhausts a relevant non-exempt rate limit
    - **When** that client requests `/healthz` or `/metrics`
    - **Then** the endpoint is not rejected by that rate limit.
    - **Maps to:** REQ-7, RULE-1.

16. **AC-16 — Per-process in-memory state**
    - **Given** rate-limit state is created for a running application process
    - **When** requests from a client IP are evaluated by that process
    - **Then** enforcement uses rate-limit state held in that process’s memory.
    - **And Then** no shared multi-worker or Redis-backed state is required for the MVP behavior.
    - **Maps to:** REQ-11, DEP-1, SCOPE-2, SCOPE-3, SCOPE-4.

17. **AC-17 — Observed RED-before-GREEN test evidence**
    - **Given** the rate-limiting change is tested locally
    - **When** completion evidence is recorded
    - **Then** it contains an observed failing test result before the implementing change and an observed passing result after the change.
    - **Maps to:** REQ-13, DEP-2.

18. **AC-18 — Execution scope preservation**
    - **Given** the rate-limiting work is performed
    - **When** the resulting local change set and execution record are inspected
    - **Then** the application target is `apps/api`.
    - **And Then** no modification is made to `D:/tem_projects/MirrorMind`.
    - **And Then** no network access, remote Git operation, merge operation, or deployment operation is used.
    - **Maps to:** REQ-12, RULE-12, SCOPE-5.

## Requirement Mapping

| Requirement or rule | Acceptance criteria |
|---|---|
| REQ-1 | AC-1, AC-4, AC-6 |
| REQ-2 | AC-1 |
| REQ-3 | AC-4, AC-5, AC-8, AC-9 |
| REQ-4 | AC-6, AC-7, AC-8, AC-9, AC-10 |
| REQ-5 | AC-2, AC-3 |
| REQ-6 | AC-2 |
| REQ-7 | AC-15 |
| REQ-8 | AC-5, AC-7, AC-11, AC-12, AC-13, AC-14 |
| REQ-9 | AC-5, AC-14 |
| REQ-10 | AC-7, AC-14 |
| REQ-11 | AC-16 |
| REQ-12 | AC-2, AC-18 |
| REQ-13 | AC-17 |
| RULE-1 | AC-1, AC-10, AC-11, AC-15 |
| RULE-2 | AC-4, AC-6, AC-8 |
| RULE-3 | AC-4, AC-6, AC-8 |
| RULE-4 | AC-6 |
| RULE-5 | AC-4 |
| RULE-6 | AC-9, AC-10 |
| RULE-7 | AC-12, AC-14 |
| RULE-8 | AC-13, AC-14 |
| RULE-9 | AC-5, AC-7, AC-14 |
| RULE-10 | AC-5, AC-7, AC-11, AC-14 |
| RULE-11 | AC-16 |
| RULE-12 | AC-18 |
| DEP-1 | AC-2, AC-3, AC-16 |
| DEP-2 | AC-17 |

## Coverage

| Applicable class | Coverage | Evidence |
|---|---|---|
| Success | covered | AC-2, AC-3, AC-4, AC-6, AC-8, AC-10, AC-11, AC-12, AC-13, AC-15, AC-16 |
| Error | covered | AC-5, AC-7, AC-14 |
| Boundary | covered | AC-4, AC-6 |
| Permission | not-applicable | Supplied contract defines client-IP limits, not user roles or permission decisions. |
| Recovery | covered | AC-8 |
| Non-regression | covered | AC-15, AC-18 |

## Unresolved Inputs

None. `OPEN-1` is known unavailable and explicitly non-blocking; it does not change required observable behavior.

## gate-report

Status: passed

## Findings

None.

## Evidence citations

- **Problem frame:** Items 1–26 establish scope, authority, client identity, thresholds, fixed-window semantics, exemptions, response behavior, counter behavior, and simultaneous-limit selection.
- **Requirements and rules:** REQ-1 through REQ-13, RULE-1 through RULE-12, DEP-1 through DEP-2, and SCOPE-1 through SCOPE-5 retain the declared product and execution contracts.
- **Acceptance criteria:** AC-1 through AC-18 provide Given/When/Then-observable coverage for all applicable requirements and rules.
- **Declared contracts and evidence:** `decisions` supplies binding clarification for ambiguous or parameterized behavior; `authority_hierarchy` resolves SRC-2 as non-binding reference context.

## Gate results

| Gate | Result | Positive evidence |
|---|---|---|
| evidence-backed-verdict | passed | Every product requirement traces to SRC-1, route evidence, or an explicit owner decision. Authority is declared in each requirement and rule; SRC-2’s non-binding status is retained in RULE-11, DEP-1, and SCOPE-4. |
| read-only-review | passed | Review contains no product-source, upstream-artifact, rule, requirement, or acceptance-criteria modification. |
| Traceability | passed | REQ-1 through REQ-13 and RULE-1 through RULE-12 map to AC-1 through AC-18 in the supplied Requirement Mapping table. |
| Critical-rule retention | passed | Client IP source, fixed-window alignment, threshold boundaries, dual-counter increment, exemptions, header selection, tie breaks, simultaneous rejection, retry timing, reset timing, and per-process storage are retained from framing through AC. |
| Scope and authority | passed | SCOPE-1 through SCOPE-5 delimit the MVP, exclude distributed storage and non-binding `slowapi` design authority, and preserve execution restrictions. |
| Unknown preservation | passed | OPEN-1 preserves unavailable traffic and cost measurements as known non-blocking context; no unsupported threshold, fallback, or product decision is invented. |
| Acceptance-criteria observability | passed | AC-1 through AC-16 define externally observable request identity, HTTP status, JSON body, headers, counter behavior, exemption behavior, configuration behavior, recovery, and process-local state. AC-17 and AC-18 define observable execution evidence. |
| Applicable coverage | passed | Success, error, boundary, recovery, and non-regression coverage are present. Permission coverage is correctly marked not-applicable because the contract defines client-IP behavior, not role or authorization policy. |

## Unresolved inputs

None. `OPEN-1` remains explicitly non-blocking and does not alter the observable requirement contract.