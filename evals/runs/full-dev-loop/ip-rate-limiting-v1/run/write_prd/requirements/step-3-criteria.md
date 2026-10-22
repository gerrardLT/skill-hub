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