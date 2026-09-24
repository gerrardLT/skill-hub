Status: passed

# PRD Section 7: User Stories & Acceptance Criteria — Batch Webhook Delivery

## Epic Hypothesis

We believe that providing reliable, idempotent batch webhook delivery—with per-destination retry isolation, strict preservation of supplied event IDs, observable delivery outcomes, and automated enforcement of concurrency thresholds—will eliminate duplicate webhook noise for API consumers and protect outbound network and destination infrastructure. We will measure success by reaching 100% ID preservation on valid events, 0% duplicate deliveries to already-successful destinations during retries, 100% audit observability across all delivery attempts, and zero executions exceeding the documented concurrency limit.

---

## User Stories & Acceptance Criteria

### Story 1: Preserve Supplied Event IDs for Valid Events

**As an** API consumer receiving batched event notifications,  
**I want** each delivered webhook payload to retain its original, client-supplied event ID,  
**So that** I can accurately correlate downstream actions, deduplicate events, and trace processing back to the originating event.

#### Acceptance Criteria

- [ ] **AC 1.1 — Verbatim ID Preservation:** When a batch containing valid events is processed, each delivered event payload must contain the exact, unmodified event ID supplied at event ingestion.
- [ ] **AC 1.2 — No Overwrites or Mutations:** The delivery pipeline must not overwrite, reformat, prefix, hash, or truncate the supplied event ID.
- [ ] **AC 1.3 — Header and Payload Consistency:** If the delivery specification includes the event ID in webhook request headers (e.g., `X-Event-ID`) and/or within the JSON payload body, both locations must reflect the supplied event ID identically.
- [ ] **AC 1.4 — Multi-Event Batch Integrity:** When multiple valid events are grouped into a single batch delivery to a destination, every individual event in the batch must preserve its distinct, supplied event ID in its respective payload record.
- [ ] **AC 1.5 — Verification Scenario:**
  - **Given** an ingested event has a valid supplied ID `evt_alpha_12345`,
  - **When** the batch delivery executes to a configured destination endpoint,
  - **Then** the received request contains `evt_alpha_12345` as the event identifier, matching the ingested value character-for-character.

---

### Story 2: Independent Destination Retries Without Duplicate Redelivery

**As an** API platform engineer,  
**I want** delivery failures to be retried strictly for the specific destinations that failed,  
**So that** destinations that already acknowledged receipt are not bombarded with duplicate webhooks during subsequent retry attempts.

#### Acceptance Criteria

- [ ] **AC 2.1 — Independent Destination Tracking:** For any batch dispatched to multiple destinations, the delivery status (e.g., `Pending`, `Success`, `Failed`) must be tracked independently per destination.
- [ ] **AC 2.2 — Selective Retry Isolation:** When a delivery attempt results in success (e.g., HTTP `2xx`) for Destination A and failure (e.g., HTTP `4xx`/`5xx`, network timeout, or connection dropped) for Destination B:
  - Destination A must be finalized as successful and marked as excluded from future retry attempts for this batch event.
  - Destination B must be marked eligible for subsequent retry attempts according to the retry schedule.
- [ ] **AC 2.3 — Zero Redelivery to Successful Endpoints:** When a retry attempt executes for failed Destination B, the delivery system must not re-dispatch or re-send the event to Destination A.
- [ ] **AC 2.4 — Partial Batch Failure Independence:** Failure of one or more destinations within a batch must not invalidate, roll back, or cause redelivery of events already acknowledged by other destinations.
- [ ] **AC 2.5 — Verification Scenario:**
  - **Given** a batch event targeting Endpoint 1 (`https://dest1.example.com`) and Endpoint 2 (`https://dest2.example.com`),
  - **When** the initial attempt yields HTTP `200 OK` from Endpoint 1 and HTTP `504 Gateway Timeout` from Endpoint 2,
  - **And** the retry policy initiates a second attempt,
  - **Then** a delivery request is sent only to Endpoint 2, and Endpoint 1 receives no outbound HTTP requests during this attempt or subsequent attempts for this event.

---

### Story 3: Observable Per-Destination Results for Every Delivery Attempt

**As an** operations engineer or platform integrator,  
**I want** every single delivery attempt to record structured, queryable telemetry and status metadata per destination,  
**So that** I have end-to-end visibility into delivery lifecycles, latency, failure causes, and retry sequences.

#### Acceptance Criteria

- [ ] **AC 3.1 — Atomic Per-Attempt Telemetry:** Every delivery attempt (both initial dispatches and individual retries) must immediately produce an observable record/log event partitioned by destination.
- [ ] **AC 3.2 — Required Audit Attributes:** Each recorded result must contain at minimum:
  - `event_id`: The supplied event ID (preserved from ingestion).
  - `destination_id` / `destination_url`: The target endpoint identity.
  - `attempt_number`: Monotonically increasing attempt index for that destination (e.g., `1`, `2`, `3`).
  - `timestamp_started` and `timestamp_completed`: Execution timestamps (ISO 8601 UTC).
  - `duration_ms`: Total network round-trip time.
  - `status`: Outcome classification (`SUCCESS`, `FAILED`, `TIMED_OUT`).
  - `response_code`: HTTP status code returned (or null if network transport failed prior to HTTP handshake).
  - `error_details`: Error classification/message if the attempt failed (e.g., connection refused, read timeout, invalid TLS certificate).
- [ ] **AC 3.3 — External Accessibility:** Delivery results must be observable through platform query interfaces (e.g., status logs, delivery event feeds, or audit query APIs) without requiring access to destination-side infrastructure or unexposed internal execution containers.
- [ ] **AC 3.4 — Granular Failure Visibility:** If an attempt fails due to request timeout or protocol negotiation failure before receiving an HTTP response, the observable record must distinctly differentiate between connection timeout, read timeout, DNS resolution failure, and non-2xx HTTP responses.

---

### Story 4: Concurrency Limiting and In-Flight Cap Enforcement

**As a** system reliability engineer,  
**I want** batch webhook dispatching to halt new outbound calls when active in-flight executions reach the documented concurrency cap,  
**So that** outbound network resources, internal worker capacity, and destination systems are protected from saturation.

#### Acceptance Criteria

- [ ] **AC 4.1 — Dynamic Concurrency Tracking:** The delivery engine must continuously monitor total active in-flight outbound requests against the documented concurrency cap.
- [ ] **AC 4.2 — Immediate Halt Above Cap:** When active in-flight webhook delivery operations equal or exceed the documented concurrency cap, the system must immediately stop dispatching new outbound webhook delivery tasks.
- [ ] **AC 4.3 — Safe State Ingestion:** Ingested batches and scheduled retries ready for execution while the system is at or above capacity must remain safely held in a pending state without being dropped, lost, or rejected.
- [ ] **AC 4.4 — Automatic Resume Below Cap:** As soon as active in-flight operations complete and concurrency drops below the documented concurrency cap, pending dispatches must resume in accordance with their scheduled priority and timestamps.
- [ ] **AC 4.5 — Strict Technology Agnosticism:** Delivery coordination must be defined purely through dispatch lifecycle states and concurrency rate controls, without mandating or hardcoding any specific queueing technology or messaging broker.
- [ ] **AC 4.6 — Verification Scenario:**
  - **Given** the documented concurrency cap is set to limit `[N]` 🔵 *(see Open Questions)*,
  - **When** the count of concurrent in-flight requests reaches `[N]`,
  - **Then** attempt `[N + 1]` is paused in `PENDING` state and no outbound socket/connection is initialized,
  - **And When** an active request completes, dropping in-flight requests to `[N - 1]`,
  - **Then** the pending attempt is immediately released for dispatch.

---

## Constraints & Edge Cases

### Constraints
- **Technology Neutrality:** No proprietary or specific queueing implementation (e.g., message broker brands, proprietary stream engines) is specified or constrained by these criteria; requirements apply strictly to behavior, state tracking, and observable outputs.
- **Idempotency Standards:** Event ID preservation and per-destination attempt logging must function consistently across all destinations regardless of their protocol implementation (HTTP/1.1 vs. HTTP/2).

### Edge Cases
- **Destination Timeout During Response Transmission:** If a destination accepts connection and headers but hangs before returning a body, the attempt must terminate at the configured client timeout, log as `TIMED_OUT`, and leave successful sibling destinations unaffected.
- **Race Condition on Retry Cancellation:** If a destination succeeds on Attempt 1 right as a retry timeout trigger evaluates, state verification must confirm the recorded success before initiating any secondary dispatch.
- **Malformed vs. Valid Events in Same Ingest Batch:** Valid events must proceed with their supplied IDs preserved even if sibling events in the same ingest batch fail validation checks.

---

## Inline Gap Tags: Assumptions & Open Questions

- 🔵 **Open Question (Concurrency Cap Value):** What is the exact numeric limit for the documented concurrency cap (global and per-destination, if partitioned)? *Needs discovery with Platform Infrastructure & Architecture teams.*
- 🔵 **Open Question (Maximum Retry Attempts):** What is the documented ceiling for retry attempts per destination before marking an endpoint permanently failed?
- 🔶 **Assumption (ID Character Set):** Client-supplied event IDs consist of standard ASCII/UTF-8 alphanumeric characters, hyphens, and underscores up to 128 characters, requiring no custom URL-encoding modifications by the dispatch layer.

---

Status: passed
