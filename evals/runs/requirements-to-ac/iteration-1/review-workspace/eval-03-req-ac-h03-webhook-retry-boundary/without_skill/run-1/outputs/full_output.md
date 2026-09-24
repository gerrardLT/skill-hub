Status: needs-input

# Batch Webhook Delivery Acceptance Criteria

## Scope and interpretation

These criteria cover batch delivery of valid webhook events to one or more destinations, preservation of supplied event IDs, destination-scoped retries, observable attempt results, and enforcement of a documented concurrency cap. They intentionally do not prescribe a queueing technology.

🔶 **Assumption:** A batch identifies a set of valid events and a set of destinations, with each event eligible for delivery to each intended destination.

🔶 **Assumption:** "Above the documented concurrency cap" means a request that would require more concurrent processing than the configured/documented cap is rejected before any event-destination delivery attempt starts; it is not partially processed or silently queued.

🔵 **Open Question (blocking final approval):** What numeric concurrency cap must be documented and enforced? Replace `<CAP>` in AC-10 through AC-12 before implementation approval.

## Acceptance criteria

### Event ID preservation

**AC-01 — Preserve supplied IDs for valid events**

- **Given** a batch contains a valid event with supplied event ID `E1`
- **When** the event is delivered to any intended destination
- **Then** the delivered webhook identifies the event as `E1`
- **And** the system does not replace, regenerate, normalize, or otherwise alter `E1`.

**AC-02 — Preserve distinct IDs across a batch**

- **Given** a valid batch contains events with supplied IDs `E1` and `E2`
- **When** the batch is processed
- **Then** every delivery attempt and per-destination result for the first event references `E1`
- **And** every delivery attempt and per-destination result for the second event references `E2`
- **And** neither event is reported under the other event's ID.

### Destination-scoped delivery and retry

**AC-03 — Record mixed destination outcomes independently**

- **Given** event `E1` is sent to destinations `D1` and `D2`
- **When** delivery to `D1` succeeds and delivery to `D2` fails
- **Then** the result for `D1` is recorded as successful
- **And** the result for `D2` is recorded as failed
- **And** the failure at `D2` does not change the successful result for `D1`.

**AC-04 — Retry only failed destinations**

- **Given** event `E1` previously succeeded at `D1` and failed at `D2`
- **When** the failed delivery is retried
- **Then** a new attempt is made for `E1` at `D2`
- **And** no new attempt is made for `E1` at `D1` as part of that retry.

**AC-05 — Preserve event ID on retry**

- **Given** delivery of event `E1` to destination `D2` failed
- **When** delivery to `D2` is retried one or more times
- **Then** every retry uses supplied event ID `E1`
- **And** no retry creates a replacement event ID.

**AC-06 — Do not redeliver successful destinations after other retries fail**

- **Given** event `E1` succeeded at `D1` and failed at `D2`
- **And** one or more retries to `D2` also fail
- **When** another retry is initiated for the outstanding failure
- **Then** only `D2` receives the next attempt
- **And** `D1` receives no duplicate delivery from any of those retries.

### Observable per-destination attempt results

**AC-07 — Emit a result for every attempt**

- **Given** an event-destination delivery attempt starts
- **When** that attempt reaches a terminal outcome
- **Then** exactly one observable result is produced for that attempt
- **And** the result identifies the supplied event ID, destination, attempt identity or attempt number, and terminal outcome.

**AC-08 — Represent success and failure observably**

- **Given** attempts are made to multiple destinations
- **When** one attempt succeeds and another fails
- **Then** each destination has its own observable result
- **And** each result distinguishes success from failure
- **And** a failed result contains sufficient failure information to diagnose or classify the failure without changing the event ID.

**AC-09 — Emit a separate result for each retry attempt**

- **Given** an initial delivery attempt for event `E1` at `D2` fails
- **When** `D2` is retried twice
- **Then** the initial attempt and both retry attempts each produce a distinct observable per-destination result
- **And** all three results reference `E1` and `D2`
- **And** results from earlier attempts remain observable rather than being overwritten by the latest result.

### Concurrency boundary

**AC-10 — Process at or below the cap**

- **Given** the documented concurrency cap is `<CAP>`
- **And** requested concurrent processing is less than or equal to `<CAP>`
- **When** the batch is accepted
- **Then** processing may proceed
- **And** observed active processing never exceeds `<CAP>`.

**AC-11 — Stop before processing above the cap**

- **Given** the documented concurrency cap is `<CAP>`
- **And** a request would require concurrent processing greater than `<CAP>`
- **When** the request is evaluated
- **Then** processing is stopped before any event-destination delivery attempt begins
- **And** no destination receives a webhook from that rejected request
- **And** the caller receives an observable result indicating that the concurrency cap was exceeded.

**AC-12 — Enforce the exact boundary without an off-by-one error**

- **Given** the documented concurrency cap is `<CAP>`
- **When** one request requires exactly `<CAP>` concurrent units and another requires `<CAP> + 1`
- **Then** the request at `<CAP>` is eligible for processing
- **And** the request at `<CAP> + 1` is stopped according to AC-11.

**AC-13 — Cap rejection creates no delivery-attempt results**

- **Given** a request is stopped before processing because it exceeds `<CAP>`
- **When** observability records are inspected
- **Then** the cap rejection itself is observable
- **And** no per-destination delivery-attempt result is reported for that request, because no delivery attempt started.

## Out of scope

- Selection or prescription of queueing technology.
- Retry schedule, delay, backoff, jitter, and maximum retry count.
- Destination authentication, payload schema beyond event ID preservation, and invalid-event handling.
- A numeric cap until the documented `<CAP>` value is supplied.

## Required decision

Supply and document the numeric concurrency cap `<CAP>`. AC-10 through AC-13 become executable without placeholders once that value is provided. Confirm the stated interpretation if "stop above the cap" is intended to mean something other than atomic pre-processing rejection (for example, processing only up to the cap while deferring excess work).
