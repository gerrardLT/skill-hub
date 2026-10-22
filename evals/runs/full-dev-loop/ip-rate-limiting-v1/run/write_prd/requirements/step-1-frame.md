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