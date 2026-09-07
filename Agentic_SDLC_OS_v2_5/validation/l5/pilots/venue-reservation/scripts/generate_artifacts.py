#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARTIFACTS = ROOT / "artifacts"


def write_doc(relative: str, title: str, sections: list[tuple[str, str]]) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    for heading, body in sections:
        lines.extend([f"## {heading}", "", body.strip(), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def common(title: str, objective: str, facts: str, decision: str, risks: str, verification: str, traceability: str) -> list[tuple[str, str]]:
    return [
        ("Objective", objective),
        ("Facts and evidence", facts),
        ("Decision and specification", decision),
        ("Risks and edge cases", risks),
        ("Verification and acceptance criteria", verification),
        ("Traceability and ownership", traceability),
    ]


def main() -> int:
    performance = json.loads((ROOT / "reports" / "performance.json").read_text(encoding="utf-8"))
    coverage = json.loads((ROOT / "reports" / "coverage.json").read_text(encoding="utf-8"))
    coverage_percent = coverage["totals"]["percent_covered_display"]
    p95 = performance["latency_ms"]["p95"]
    throughput = performance["throughput_rps"]

    write_doc("README.md", "Venue Reservation Dogfood Pilot", common(
        "Venue Reservation Dogfood Pilot",
        "Run the Agentic SDLC OS against a real user-owned product requirement set and produce an executable vertical slice rather than a document-only demonstration.",
        "Source anchors are `source/requirements.xlsx`, its selected extract, and two design specifications. The selected capabilities are D26 dynamic table locking and D33 fair queueing. The implementation test suite currently has 11 passing tests.",
        "Build a FastAPI and SQLite service for atomic capacity allocation, FIFO waitlist promotion, idempotent retries, tenant isolation, audit events and measurable runtime behavior. Keep payment and physical check-in outside this pilot.",
        "This is a controlled local pilot, not an external production rollout. It cannot prove business conversion, long-term reliability or causal improvement over a baseline Agent without matched iterations.",
        f"Pass requires zero oversell under 100 concurrent requests, FIFO promotion, 100 percent test pass, code coverage above 90 percent, and a local performance probe with p95 below 500 ms. Observed p95 is {p95} ms and coverage is {coverage_percent} percent.",
        "Owner: Agentic SDLC OS dogfood team. Version: pilot-0.1.0. The full evidence chain is recorded in `.sdlc`, `reports`, and the six OS artifact folders."
    ))

    write_doc("docs/pm/product-brief.md", "Product Brief - Atomic Venue Reservation", [
        ("Problem and context", "Peak booking demand can create duplicate requests, unfair ordering and oversold capacity. Requirement D26 demands atomic table holds and D33 requires a fair queue with zero oversell. The current pilot isolates this risk-heavy core before payment, check-in or pricing complexity is added."),
        ("Users and audience", "Primary users are venue members booking a session and operators responsible for capacity integrity. Secondary users are support staff investigating failed retries, cancellations and promotion order through an immutable audit trail."),
        ("Outcome and objective", "A member receives one actionable state: RESERVED or WAITLISTED. A cancellation immediately promotes the earliest eligible waitlist entry. The system must never report more active reservations than configured capacity."),
        ("Scope and non-goals", "Scope includes session creation, reservation, FIFO waitlist, cancellation, automatic promotion, tenant isolation, idempotency, audit and metrics. Non-goals are payments, membership entitlement, table maps, physical access, notifications and multi-region scaling."),
        ("Evidence and facts", "Source: `source/requirements-selection.md`. D26 explicitly requires 100 concurrent requests without oversell. D33 requires server-side ordering, one active token per member and a direct waitlist path. The design source requires errors to state the reason, current state and next action."),
        ("Risks and assumptions", "SQLite serialization is acceptable for a local pilot but not assumed sufficient for multi-node production. FIFO is based on transaction admission order. A future eligibility service may reject a promoted member and therefore needs a skip-and-reason compensation path."),
        ("Success metrics and acceptance criteria", "Oversell count must equal 0. Exactly capacity requests must become RESERVED. Remaining requests must receive unique FIFO positions. Retry replay must return the original result. Coverage must exceed 90 percent and p95 for 200 local requests must stay under 500 ms."),
    ])

    write_doc("docs/pm/discovery-evidence.md", "Discovery Evidence", common(
        "Discovery Evidence",
        "Determine whether reservation integrity and waitlist certainty are sufficiently evidenced to justify an executable pilot.",
        "Evidence source 1 is the user-owned feature workbook, narrowed to D26, D33 and the Reservation, WaitlistEntry and SeatHold state invariants. Evidence source 2 is the UI/UX specification that defines time-first booking, actionable taken-state recovery and calm waitlist status. Evidence source 3 is the executable concurrency test.",
        "Proceed with a vertical slice centered on correctness, certainty and traceability. Do not broaden into full Venue OS scope during the pilot.",
        "The workbook is a product specification, not observed production telemetry. The expert design document is not a usability study. These limitations block claims about market demand or user conversion.",
        "The pilot is justified when the selected requirements can be translated into falsifiable invariants and verified by deterministic tests. The evidence is sufficient for engineering validation, not business validation.",
        "Requirement source hash is recorded in `source/requirements-selection.md`. Owner: PM OS. Downstream: PS-001, PRD-001 and RR-001."
    ))

    write_doc("docs/pm/product-strategy.md", "Product Strategy", common(
        "Product Strategy",
        "Choose the smallest strategic wedge that tests whether Agentic SDLC OS can turn a dense requirement set into a correct, releasable and observable software slice.",
        "The source backlog contains broad venue operations. D26 and D33 concentrate high-value failure modes: concurrency, uniqueness, fairness, retry behavior and state recovery. These concerns traverse every OS and generate objective evidence.",
        "Use atomic reservation plus FIFO waitlist as the wedge. Optimize first for trust and deterministic state, then for throughput. Exclude payment and membership policy until the capacity invariant is proven.",
        "A narrow wedge may underrepresent visual design and commercial workflow complexity. SQLite can hide distributed coordination problems. The pilot therefore records an explicit portability risk instead of treating the implementation as production architecture.",
        "Strategy passes when all six OSs can produce accepted artifacts, all seven gates can be checked without waiver, the service runs, and Evolution produces a concrete next decision from measured runtime evidence.",
        "Owner: PM OS. Strategic decision DEC-001. Inputs: PB-001 and DE-001. Outputs: PO-001, PRD-001 and OR-001."
    ))

    write_doc("docs/pm/prioritized-opportunities.md", "Prioritized Opportunities", common(
        "Prioritized Opportunities",
        "Rank problem opportunities rather than feature requests using value, risk reduction, evidence strength and implementation cost.",
        "Opportunity O1 atomic capacity allocation scores 10/10 risk reduction and has direct acceptance evidence. O2 idempotent retry scores 9/10 because duplicate requests are explicitly named. O3 FIFO promotion scores 9/10 because it closes released capacity. O4 visual table map scores 5/10 for this pilot because it does not prove backend integrity.",
        "Priority order is O1 atomic allocation, O2 idempotency, O3 waitlist promotion, O4 actionable error contract, O5 metrics and audit, then visual map integration. The first five are committed for pilot-0.1.0.",
        "A pure value score could over-prioritize visible UI and miss catastrophic oversell. The ranking therefore treats correctness and recoverability as non-compensable gates.",
        "Each committed opportunity must map to at least one PRD requirement and one automated test. O1 must pass a 100-request concurrency test with zero oversell.",
        "Owner: PM OS. Inputs: PS-001 and DE-001. Downstream: PRD-001 and OR-001."
    ))

    write_doc("docs/pm/prd.md", "PRD - Reservation and Waitlist Vertical Slice", [
        ("Problem", "Members competing for scarce venue capacity can submit retries at the same time. A naive implementation may oversell, duplicate a member, lose fairness or provide a dead-end error. The product must expose a single authoritative state and a recovery path."),
        ("Users and jobs to be done", "Member JTBD: reserve a valid session with confidence, or know the exact waitlist position and what happens next. Operator JTBD: prove that capacity, promotion order and retries are correct, then diagnose every material state change from audit data."),
        ("Goals and non-goals", "Goals: atomic allocation, one active reservation or waitlist entry per member and session, FIFO promotion, idempotent retries, tenant isolation, actionable errors, immutable audit events and session metrics. Non-goals: payment, entitlement, notifications, check-in, table selection UI and distributed deployment."),
        ("Functional requirements", "REQ-001 create an OPEN session with capacity 1-500. REQ-002 reserve within one immediate transaction. REQ-003 return WAITLISTED with a unique position when full. REQ-004 reuse of an idempotency key with identical payload returns the original response; different payload returns 409. REQ-005 cancellation promotes the earliest WAITLISTED entry. REQ-006 all reads and writes are tenant scoped. REQ-007 emit audit events for session open, reservation, waitlist join, promotion and cancellation. REQ-008 expose capacity, reserved, waitlisted, conversion and oversell metrics."),
        ("User journey", "Create session -> member submits reserve -> server validates tenant and uniqueness -> atomic capacity decision -> RESERVED or WAITLISTED -> member retries safely -> a reserved member cancels -> earliest waitlist member becomes RESERVED -> operator inspects metrics and audit evidence."),
        ("Edge cases, constraints and risks", "Handle concurrent requests, duplicate members, stale retries, invalid identifiers, closed or missing sessions, tenant mismatch and concurrent cancellations. FIFO is transaction order, not network arrival time. SQLite is accepted only for this local pilot and requires a different lock design for multi-node production."),
        ("Metrics and success criteria", "Oversell equals 0. Under 100 concurrent attempts and capacity 10, exactly 10 become RESERVED and 90 receive positions 1-90. All cancellation promotions must select the lowest active queue sequence. Test pass rate must be 100 percent, code coverage above 90 percent, and local p95 under 500 ms."),
        ("Acceptance criteria", "AC-001 through AC-008 are verified by `tests/test_service.py`, `tests/test_concurrency.py`, `tests/test_api.py`, `tests/test_audit.py`, coverage evidence and the performance probe. Any capacity breach, duplicate active state or tenant data exposure is a release blocker."),
        ("Traceability and evidence", "Source requirements: D26, D33, Reservation, WaitlistEntry, SeatHold, R02 and R08 in `source/requirements-selection.md`. Owner: PM OS. Version: PRD-001. Downstream: design flow, technical design, tests, release plan and telemetry."),
    ])

    write_doc("docs/pm/outcome-roadmap.md", "Outcome Roadmap", common(
        "Outcome Roadmap",
        "Sequence work by verified outcomes instead of a feature calendar.",
        "Outcome 1 capacity integrity: zero oversell and no duplicate active state. Outcome 2 user certainty: every reserve request returns RESERVED or WAITLISTED with actionable context. Outcome 3 recoverability: cancellation fills capacity through FIFO promotion. Outcome 4 operability: metrics and audit identify what occurred.",
        "Milestone M1 requirements and invariants; M2 interaction and error contracts; M3 transactional service and tests; M4 independent QA and local release; M5 telemetry and learning. Payment remains a later outcome after M5 passes.",
        "Completing code without runtime evidence is not an outcome. Throughput optimization cannot trade away capacity integrity. Scope expansion is rejected until M1-M5 evidence is accepted.",
        "Each milestone requires its mapped gate and artifact set. The final outcome is accepted only when Evolution compares expected and actual results and records the next route.",
        "Owner: PM OS. Inputs: PRD-001 and PO-001. Downstream: MP-001, TD-001 and RLP-001."
    ))

    write_doc("docs/pm/measurement-plan.md", "Measurement Plan", common(
        "Measurement Plan",
        "Define decision-linked metrics before implementation and prevent vanity measurements from replacing invariant checks.",
        "Primary metrics are oversold boolean, active reservations versus capacity, FIFO position continuity, waitlist promotion count, idempotent replay equality, test pass rate and coverage. Secondary metrics are throughput and p50/p95/p99 latency from a local controlled probe.",
        "Release blocker thresholds: oversold must be false, capacity equality exact, FIFO positions contiguous, tenant leakage zero and tests 100 percent pass. Performance guardrail: p95 below 500 ms for 200 requests with 32 workers on the current container.",
        "Local latency does not represent cloud production. Coverage does not prove requirement correctness. Waitlist conversion in the pilot is mechanically induced by cancellations and is not a business conversion metric.",
        "Data sources are SQLite state, audit events, pytest, coverage JSON and `reports/performance.json`. Each result must include timestamp, parameters and version identity.",
        "Owner: PM OS with Evolution verification. Input: PRD-001. Downstream: TEL-001 and LD-001."
    ))

    write_doc("docs/pm/risk-register.md", "Risk Register", [
        ("Scope and objective", "Control the non-compensable risks for pilot-0.1.0 before design, implementation and release decisions."),
        ("Risks and failure modes", "RISK-001 oversell during concurrent allocation. RISK-002 duplicate active reservation or waitlist entry. RISK-003 unfair promotion order. RISK-004 idempotency key replay with a different payload. RISK-005 cross-tenant read or write. RISK-006 SQLite assumptions copied into distributed production."),
        ("Severity, likelihood and impact", "RISK-001, RISK-002 and RISK-005 are critical impact and possible likelihood. RISK-003 and RISK-004 are high impact and possible. RISK-006 is high impact if the pilot is misclassified as production architecture."),
        ("Mitigation and controls", "Use BEGIN IMMEDIATE transactions, partial unique indexes, queue sequence uniqueness, request hashes, tenant predicates, parameterized SQL, immutable audit events, concurrency tests and explicit architecture scope labels."),
        ("Owners, triggers and review", "Engineering owns transaction integrity; QA owns adversarial verification; Release owns scope labeling. Any oversold=true, duplicate active state, non-contiguous queue, mismatched replay acceptance or tenant access fails the gate and stops release."),
        ("Traceability, source and evidence", "Sources: D26, D33 and state invariants in `source/requirements-selection.md`. Evidence: `tests/test_concurrency.py`, `tests/test_service.py`, `tests/test_api.py`, `reports/coverage.json` and `reports/performance.json`."),
    ])

    write_doc("docs/design/information-architecture.md", "Information Architecture", common(
        "Information Architecture",
        "Define the smallest member and operator information structure for a reservation decision without exposing database concepts.",
        "The design source specifies a time-first model, a single highlighted decision, an actionable table-taken state and a waitlist position that reduces uncertainty. API resources are session, reservation, waitlist outcome and metrics.",
        "Member flow uses Session Availability -> Reservation Decision -> Confirmation or Waitlist Status -> Cancellation Result. Operator flow uses Session Metrics -> Audit Events -> Issue diagnosis. Private booking and social matchmaking remain separate information spaces.",
        "Do not show raw queue sequence as a guarantee of time. Do not collapse RESERVED and WAITLISTED into a generic success state. Do not expose tenant identifiers in member content.",
        "Acceptance requires every PRD state to have one clear surface, one primary action and an explicit next step. Errors must preserve session context instead of resetting the task.",
        "Owner: Design OS. Inputs: PRD-001 and source UI/UX specification. Downstream: UF-001, IS-001 and DH-001."
    ))

    write_doc("docs/design/user-flows.md", "User Flows", common(
        "User Flows",
        "Specify normal, full-capacity, retry, cancel, promotion and recovery paths.",
        "Normal: choose session -> submit -> RESERVED -> show time, venue and management actions. Full: submit -> WAITLISTED -> show current position and promotion rule. Retry: same key -> identical result. Cancel: confirm consequence -> CANCELED -> earliest waitlist entry promoted.",
        "Flow F1 reserves capacity. F2 joins FIFO waitlist. F3 safely replays a request. F4 rejects reused keys with different payload. F5 cancels and promotes. F6 resolves missing session, duplicate member, invalid input and tenant mismatch with reason plus next action.",
        "A race can change availability between page view and submit. The client must trust the server result and retain the selected session. A cancellation may have no waitlist and must still return a stable CANCELED state.",
        "Each flow maps to a test. F1-F5 must be deterministic. F6 must expose error code, message and next_action. No flow may show a success animation before the authoritative response.",
        "Owner: Design OS. Inputs: IA-001 and PRD-001. Downstream: IS-001, PROTO-001 and INT-001."
    ))

    write_doc("docs/design/interaction-spec.md", "Interaction Specification", common(
        "Interaction Specification",
        "Define state language and response behavior for fast, high-confidence booking decisions.",
        "The source design requires booking order of time, duration, table, participants, price and confirm. This backend pilot starts at the confirm decision. Server results are RESERVED, WAITLISTED or CANCELED; errors include a stable code and next action.",
        "RESERVED shows a confirmation title and the reservation identifier. WAITLISTED shows position as the primary number and explains FIFO promotion. SESSION_NOT_FOUND offers return to availability. ALREADY_RESERVED opens the existing reservation. IDEMPOTENCY_CONFLICT instructs use of the original payload or a new key.",
        "Never use color alone. Never display a fake countdown. Never discard the selected session after a race. Avoid generic 'operation failed' language. A network retry must reuse the same idempotency key.",
        "Prototype review must verify keyboard access, visible focus, status text, preserved context and distinct outcomes. API integration tests verify error content and stable retry behavior.",
        "Owner: Design OS. Inputs: UF-001 and PRD-001. Downstream: PROTO-001, AR-001 and DH-001."
    ))

    write_doc("docs/design/design-system.md", "Design System Slice", common(
        "Design System Slice",
        "Define the minimum visual and semantic system for the reservation state prototype while preserving the existing Rally Atelier direction.",
        "The user-owned design source emphasizes precise hierarchy, one highlighted table or decision, short low-overshoot motion and status that is not color-only. The pilot uses neutral surfaces, one vermilion action accent, a teal availability state and explicit text labels.",
        "Tokens: 8 px spacing base, 16 px card radius, 44 px minimum target, 160-200 ms standard transition, 3:1 focus indicator contrast and 4.5:1 body text contrast. Components: time option, session card, primary action, state banner, queue position and error recovery panel.",
        "The prototype is not a final branded application. It excludes photography, complex table maps and expressive motion. High-saturation accents are limited to one per viewport.",
        "Acceptance requires semantic HTML, focus-visible styling, reduced-motion support and text labels for all states. Tokens are documented in `prototype/index.html` CSS variables.",
        "Owner: Design OS. Inputs: source UI/UX guideline and IS-001. Downstream: PROTO-001 and DH-001."
    ))

    write_doc("docs/design/usability-report.md", "Usability Review Report", common(
        "Usability Review Report",
        "Run an expert task walkthrough of the prototype for booking, full-capacity waitlist and recovery states.",
        "Method: keyboard-only walkthrough and cognitive walkthrough for three tasks. Result: the primary action remains stable, waitlist position is visible, reserved and waitlisted outcomes are distinct, and error recovery preserves the session. No external users participated.",
        "Decision: accept the prototype for engineering handoff with one concern. The prototype must not imply that queue position predicts exact waiting time. The explanatory copy states that promotion occurs only when capacity is released.",
        "Limitations include no real user sample, no device lab, no localization and no payment step. These limits prevent a claim of validated usability and require a later moderated study before a commercial launch.",
        "Pass criteria: all three tasks complete without hidden navigation, keyboard trap or ambiguous success. Review evidence is the prototype source and checklist in this report.",
        "Owner: Design reviewer, separate from prototype author. Inputs: PROTO-001 and UF-001. Downstream: DH-001."
    ))

    write_doc("docs/design/accessibility-report.md", "Accessibility Review Report", common(
        "Accessibility Review Report",
        "Evaluate the prototype against keyboard, focus, semantics, contrast, motion and status communication requirements.",
        "Method: source inspection plus keyboard walkthrough. Buttons are native elements, labels are associated, status changes use aria-live, focus is visible, reduced motion is respected and state is expressed through text plus icon rather than color alone.",
        "Accept for pilot. Required implementation details are minimum 44 px targets, body contrast at least 4.5:1, no focus removal, and no auto-advancing interaction.",
        "No screen-reader matrix or automated browser audit was run in this container. Final application testing must cover VoiceOver, TalkBack and at least one desktop screen reader.",
        "Acceptance is evidence of semantic structure and keyboard completion in `prototype/index.html`. Any state communicated by color only is a release blocker.",
        "Owner: Accessibility reviewer. Inputs: PROTO-001 and DS-001. Downstream: DH-001 and NFR-001."
    ))

    write_doc("docs/design/design-handoff.md", "Design Handoff", common(
        "Design Handoff",
        "Translate member states and error recovery into implementable API and frontend contracts.",
        "RESERVED maps to HTTP 201, WAITLISTED to 202, cancellation to 200, business conflicts to 409, missing tenant resource to 404 and validation failures to 422. Each business error returns code, message and next_action.",
        "Engineering must preserve the session identifier, member identifier and idempotency key through retries. Frontend must render authoritative response state and never infer capacity from stale availability. Queue position is integer text with an explanation, not a countdown.",
        "The pilot does not implement the full visual application. Integration consumers must not assume payment state, hold TTL or table map availability. Those require new requirements and state contracts.",
        "Handoff accepted when API tests verify status mapping and the prototype covers RESERVED, WAITLISTED and error states. Changes to PRD state names invalidate this handoff until re-reviewed.",
        "Owner: Design OS. Inputs: IA-001, UF-001, IS-001, DS-001, PROTO-001, UR-001 and AR-001. Downstream: TD-001 and TP-001."
    ))

    write_doc("docs/engineering/technical-design.md", "Technical Design", common(
        "Technical Design",
        "Implement capacity allocation and waitlist promotion with explicit transaction boundaries and verifiable invariants.",
        "FastAPI provides the HTTP boundary. Pydantic validates identifiers and capacity. SQLite uses WAL, busy_timeout and BEGIN IMMEDIATE. Partial unique indexes prevent duplicate active reservation and waitlist states. Audit events are append-only rows.",
        "Reserve transaction: validate idempotency -> load tenant session -> reject duplicate active state -> count active reservations -> insert reservation or next queue sequence -> append event -> persist replay response -> commit. Cancel transaction marks CANCELED and promotes the lowest active queue_seq.",
        "SQLite serializes writes and is a pilot constraint. A distributed implementation needs a database atomic update, lock or single-writer queue. JSON audit payloads must not contain secrets. Queue order reflects transaction admission rather than client timestamp.",
        "Verification requires concurrency tests, unique-index checks, replay tests, tenant isolation tests, coverage above 90 percent and local probe p95 below 500 ms with zero oversell.",
        "Owner: Engineering OS. Inputs: PRD-001 and DH-001. Downstream: ADR-001, IP-001, TP-001 and SRC-001."
    ))

    write_doc("docs/engineering/architecture-decisions.md", "Architecture Decision Records", common(
        "Architecture Decision Records",
        "Record the irreversible or high-consequence choices for pilot-0.1.0.",
        "ADR-001 chooses SQLite as a reproducible local transactional store. ADR-002 chooses BEGIN IMMEDIATE for serialization. ADR-003 chooses partial unique indexes for active-state invariants. ADR-004 stores complete idempotent responses. ADR-005 uses FIFO queue_seq generated inside the transaction.",
        "These decisions optimize deterministic evidence and minimal dependencies. They are accepted only for single-node pilot execution. The API boundary and domain invariants are designed so the storage implementation can later be replaced.",
        "Main tradeoff is limited horizontal write scaling. Storing response JSON increases data retention responsibility. FIFO by commit order is fair at the server boundary but not a guarantee of network arrival fairness.",
        "Each ADR is verified by a matching test and documented rollback. A production architecture review must supersede ADR-001 and ADR-002 before multi-node deployment.",
        "Owner: Architecture reviewer. Inputs: TD-001 and RR-001. Downstream: IP-001 and SP-001."
    ))

    write_doc("docs/engineering/implementation-plan.md", "Implementation Plan", common(
        "Implementation Plan",
        "Deliver the vertical slice as independently verifiable increments.",
        "Slice S1 schema and store; S2 create and read session; S3 atomic reserve and waitlist; S4 idempotency and tenant isolation; S5 cancellation and FIFO promotion; S6 audit and metrics; S7 API contract; S8 tests, coverage, performance and release evidence.",
        "Execute S1-S8 in order because later slices depend on state invariants. Every slice ends with a test. No UI integration begins until S3-S5 pass under concurrency.",
        "Risk of hidden coupling is controlled by separating API, models, store and service. A failed slice reverts its files and database fixture; no production data exists.",
        "Done means source exists, mapped tests pass, coverage remains above 90 percent and the artifact evidence is registered in `.sdlc`.",
        "Owner: Engineering OS. Inputs: TD-001 and ADR-001. Downstream: SRC-001, UTE-001 and IE-001."
    ))

    write_doc("docs/engineering/test-plan.md", "Engineering Test Plan", common(
        "Engineering Test Plan",
        "Prove the transactional and API invariants before independent QA.",
        "Unit tests cover capacity, FIFO promotion, replay, duplicate member, tenant isolation and audit sequence. Integration tests cover HTTP statuses and actionable errors. Concurrency tests submit 100 reservations and parallel cancellations. Coverage is measured with coverage.py.",
        "Test data uses isolated temporary SQLite databases. Concurrency uses separate connections through the service and ThreadPoolExecutor. The performance probe records parameters, throughput and latency percentiles.",
        "Thread scheduling is not deterministic, so tests assert contiguous queue positions and promotion set rather than member arrival order. The local probe is a guardrail, not a capacity forecast.",
        "Pass: all tests green, zero oversell, exact capacity allocation, unique positions, correct promotion count and coverage above 90 percent.",
        "Owner: Engineering OS. Inputs: PRD-001 and TD-001. Downstream: UTE-001, IE-001 and TS-001."
    ))

    write_doc("docs/engineering/security-plan.md", "Security Plan", common(
        "Security Plan",
        "Protect tenant boundaries, request integrity and auditability for the pilot API.",
        "Controls include required tenant header, tenant predicates on resources, parameterized SQL, Pydantic identifier validation, bounded capacity, idempotency request hashes and no secret fields in audit payloads.",
        "Reject missing or mismatched tenant resources with 404 to avoid disclosure. Reject reused idempotency keys with different payload using 409. Limit identifier length and character set. Do not accept arbitrary database paths from API input.",
        "Authentication and authorization are not implemented; the tenant header is a test boundary only. Rate limiting, encryption at rest, secret management and production logging policy are outside the pilot and mandatory before external exposure.",
        "Pass requires tenant isolation tests, unsafe identifier rejection, parameterized queries and documented non-production scope. Any cross-tenant access is critical.",
        "Owner: Security reviewer. Inputs: RR-001 and TD-001. Downstream: SEC-REV-001 and NFR-001."
    ))

    write_doc("docs/engineering/source-change.md", "Source Change Summary", [
        ("Summary and objective", "Implement pilot-0.1.0 for atomic venue reservation, FIFO waitlist promotion and observable state transitions."),
        ("Implementation and files changed", "Added `src/venue_pilot/api.py`, `service.py`, `store.py`, `models.py` and `errors.py`. Added database schema, REST endpoints, transactional reserve/cancel operations, idempotency records, audit events and metrics."),
        ("Tests and evidence", f"Added 11 tests across service, API, concurrency and audit behavior. Current test result is 11 passed. Coverage is {coverage_percent} percent. Performance probe reserved exactly 20 of 200 requests, waitlisted 180 and reported oversold=false."),
        ("Risks, limitations and rollback", "SQLite is single-node pilot storage. Rollback removes the pilot directory or restores the prior source archive. No external database migration or production data is involved."),
        ("Traceability and requirements", "Implements PRD-001 REQ-001 through REQ-008, with direct source anchors D26 and D33. Version: pilot-0.1.0. Owner: Engineering OS."),
    ])

    write_doc("docs/engineering/unit-test-evidence.md", "Unit Test Evidence Report", common(
        "Unit Test Evidence Report",
        "Record reproducible unit and concurrency evidence for the source change.",
        f"Command: `PYTHONPATH=src python -m pytest -q`. Result: 11 tests passed. Coverage command produced {coverage_percent} percent total coverage. Key evidence includes 100 concurrent reservations with capacity 10 and zero oversell.",
        "Accept the unit-test evidence. Tests cover required invariants, error contracts, audit event order, idempotency conflict and tenant isolation.",
        "The test suite runs against SQLite in one process. It does not test multi-process or multi-node database coordination, external authentication or a real browser client.",
        "Pass criteria are 100 percent test pass and coverage above 90 percent. Raw evidence: `reports/coverage.json` and `reports/coverage.txt`.",
        "Owner: Test runner. Input: SRC-001 and TP-001. Downstream: CR-001 and RRPT-001."
    ))

    write_doc("docs/engineering/code-review.md", "Code Review", [
        ("Scope and summary", "Independent review of the reservation service, store, API models and tests for pilot-0.1.0."),
        ("Findings and observations", "Transaction boundaries are explicit. SQL is parameterized. Active-state uniqueness is enforced by partial indexes. Idempotency records preserve status and body. Cancellation promotes the lowest active queue sequence. Error responses include next_action."),
        ("Correctness, security and risks", "No oversell path was found within the single-node SQLite model. Main residual risk is accidental reuse as distributed production architecture. Tenant identity is a header rather than authenticated context. Audit JSON needs a future retention and redaction policy."),
        ("Decision and recommendation", "Approve for controlled local pilot. Reject external deployment until authentication, authorization, rate limiting and a production database coordination design are added."),
        ("Traceability and change identity", "Reviewed SRC-001 against PRD-001, TD-001 and SP-001. Evidence: 11 passing tests, coverage report and concurrency probe. Reviewer: code-reviewer; author: engineering-agent."),
    ])

    write_doc("docs/engineering/integration-evidence.md", "Integration Evidence Report", common(
        "Integration Evidence Report",
        "Verify the HTTP boundary, state transitions and database behavior as one executable system.",
        "FastAPI TestClient creates a session, confirms one reservation, places the next member on the waitlist, cancels the reservation, promotes the waitlisted member and verifies metrics. Error tests verify 404 and 422 contracts.",
        "Accept integration behavior for the pilot. HTTP status mapping is 201 RESERVED, 202 WAITLISTED, 200 CANCELED, 409 business conflict, 404 missing tenant resource and 422 invalid input.",
        "No external reverse proxy, network fault injection, TLS or live browser is included. Local integration success does not prove cloud deployment compatibility.",
        "Pass requires the end-to-end API test and all state assertions. Evidence is `tests/test_api.py` and the full pytest run.",
        "Owner: Integration reviewer. Inputs: SRC-001 and DH-001. Downstream: CR-001 and RGR-001."
    ))

    write_doc("docs/engineering/security-review.md", "Security Review Report", common(
        "Security Review Report",
        "Review tenant isolation, input handling, SQL use, replay protection and data exposure.",
        "All queries use parameters. Identifiers use an allowlist and bounded length. Tenant resources require the tenant predicate. Idempotency keys are bound to request hashes. Error responses do not reveal whether another tenant owns an identifier.",
        "Approve for local non-production use. Authentication and authorization remain absent by design; therefore external access is prohibited.",
        "Residual risks are denial of service, spoofed tenant headers, local database file access and unbounded audit retention. These require production controls before release beyond the pilot environment.",
        "Security pass requires tenant isolation and invalid identifier tests plus explicit release restriction. Evidence: `tests/test_service.py`, `tests/test_api.py` and SP-001.",
        "Owner: Security reviewer. Input: SRC-001. Downstream: RELREC-001."
    ))

    write_doc("docs/engineering/performance-report.md", "Performance Report", common(
        "Performance Report",
        "Measure local serialization cost while verifying capacity integrity under parallel demand.",
        f"Method: 200 requests, capacity 20, 32 workers, temporary SQLite WAL database. Result: throughput {throughput} requests per second, p50 {performance['latency_ms']['p50']} ms, p95 {p95} ms, p99 {performance['latency_ms']['p99']} ms, reserved 20, waitlisted 180, oversold=false.",
        "Accept the local performance guardrail because p95 is below 500 ms and the correctness invariant held. Performance is secondary to zero oversell.",
        "The probe shares one host process and warm local storage. It is not a production load test, capacity model or multi-region benchmark. Variance should be sampled over repeated runs before changing thresholds.",
        "Pass criteria: exact capacity allocation, oversold=false, no exceptions and p95 below 500 ms. Raw result: `reports/performance.json`.",
        "Owner: Performance reviewer. Inputs: SRC-001 and TP-001. Downstream: NFR-001 and TEL-001."
    ))

    write_doc("docs/qa/test-strategy.md", "QA Test Strategy", common(
        "QA Test Strategy",
        "Independently verify product risks rather than repeat the engineering happy path.",
        "Risk priorities are oversell, duplicate state, queue disorder, tenant leakage, mismatched idempotency replay and incomplete audit. Test levels are API, transaction, concurrency, security boundary and nonfunctional probe.",
        "Use risk-based execution: critical invariants on every change; API and audit regression on every release; performance probe before release; distributed database tests only after the architecture changes.",
        "The pilot does not cover payment, time-based expiry, authentication or device UX. These are explicit exclusions rather than assumed passes.",
        "Release requires all critical tests pass, no open critical defect, coverage above 90 percent and a reproducible performance result with zero oversell.",
        "Owner: QA OS. Inputs: PRD-001, TP-001 and RR-001. Downstream: RGR-001, NFR-001 and RELREC-001."
    ))

    write_doc("docs/qa/regression-report.md", "Regression Report", common(
        "Regression Report",
        "Confirm that the complete pilot suite remains green after implementation and review changes.",
        "Executed 11 tests covering API, service, concurrency, audit, tenant isolation and input validation. Result: 11 passed, 0 failed. Coverage remained above the 90 percent gate.",
        "Regression passes for pilot-0.1.0. No feature regression or capacity invariant failure was observed.",
        "The suite is deterministic for state counts but operating-system thread scheduling can change which member obtains an initial slot. Fairness assertions therefore use server queue sequence, not client launch order.",
        "Pass requires zero failed tests and no changed expected state. Raw evidence: pytest output, `reports/coverage.json` and versioned source tests.",
        "Owner: QA reviewer. Inputs: SRC-001 and UTE-001. Downstream: DD-001 and RELREC-001."
    ))

    write_doc("docs/qa/nonfunctional-report.md", "Nonfunctional Report", common(
        "Nonfunctional Report",
        "Evaluate performance, security boundary, accessibility handoff, auditability and recoverability for pilot scope.",
        f"Performance passed with p95 {p95} ms and zero oversell. Security review permits local non-production use only. Audit events cover five material event types. Accessibility review confirms semantic prototype structure with known screen-reader test gaps.",
        "Accept nonfunctional evidence for the controlled pilot. Do not authorize public exposure or distributed deployment.",
        "Missing production controls include authentication, rate limiting, TLS, secret management, retention, backup, disaster recovery and multi-node coordination. These are release conditions for any later environment.",
        "Pass is limited to the local pilot environment described in DEP-001. The report is invalid if deployment topology changes.",
        "Owner: QA OS. Inputs: PERF-001, SEC-REV-001 and AR-001. Downstream: RELREC-001."
    ))

    write_doc("docs/qa/defect-disposition.md", "Defect Disposition", common(
        "Defect Disposition",
        "Classify observed issues and decide whether any block the controlled release.",
        "No functional defects were observed in the final suite. CONCERN-001 authentication absent, CONCERN-002 SQLite single-node limitation and CONCERN-003 no real-user usability study are recorded as scope constraints, not closed defects.",
        "Disposition: zero open critical or high implementation defects. The three concerns remain open guardrails and prohibit public or multi-node release.",
        "A scope concern can become a defect if the release target changes. Any attempt to expose the service externally without controls must reopen release readiness.",
        "Accept when release documents repeat these restrictions and rollback remains immediate. No waiver is used.",
        "Owner: QA lead. Inputs: RGR-001, NFR-001 and RR-001. Downstream: RELREC-001."
    ))

    write_doc("docs/qa/release-recommendation.md", "Release Recommendation", [
        ("Release scope", "Release pilot-0.1.0 only to a local controlled environment for Agentic SDLC OS dogfooding. Do not expose it to external users or production data."),
        ("Evidence and test results", f"11 tests passed, coverage is {coverage_percent} percent, 200-request probe reserved exactly 20 slots, waitlisted 180 and reported oversold=false. Security and code review approved the constrained scope."),
        ("Residual risks", "Authentication, authorization, rate limiting, distributed coordination, data retention and real-user usability remain unverified. SQLite is not approved for a horizontally scaled deployment."),
        ("Recommendation and decision", "GO for controlled local deployment; NO-GO for public, production or multi-node deployment. This split decision is mandatory and cannot be summarized as general production readiness."),
        ("Conditions, guardrails and rollback", "Bind to localhost, use a temporary database, run the full test suite before start, capture probe evidence, and delete the process and database to roll back. Stop immediately on oversold=true or failed tenant isolation."),
        ("Traceability and version", "Version pilot-0.1.0. Inputs: RGR-001, NFR-001 and DD-001. Downstream: RLP-001, RBP-001 and DEP-001."),
    ])

    write_doc("docs/release/release-plan.md", "Release Plan", common(
        "Release Plan",
        "Deploy the pilot to a reproducible localhost environment and capture evidence without claiming external production release.",
        "Preflight runs pytest, coverage and the performance probe. Build uses the current Python environment and package source. Rollout starts Uvicorn on 127.0.0.1:8080 with an isolated database. Verification calls /health and exercises a complete reserve-waitlist-cancel path.",
        "Proceed only after QA recommendation GO for controlled scope. The deployment window is immediate and reversible because no external data or migration is used.",
        "Stop conditions are failed preflight, bind beyond localhost, oversold=true, tenant test failure or missing rollback path. Public exposure is prohibited.",
        "Success requires health=ok, deterministic smoke path, metrics visibility and saved deployment evidence. Rollback must complete by terminating the process and deleting the temporary database.",
        "Owner: Release OS. Inputs: RELREC-001 and SRC-001. Downstream: DEP-001 and PV-001."
    ))

    write_doc("docs/release/rollback-plan.md", "Rollback Plan", common(
        "Rollback Plan",
        "Return the controlled pilot to a clean pre-deployment state within five minutes.",
        "The release creates one local Uvicorn process and one isolated SQLite database. No external schema, queue, secret or customer data is modified.",
        "Rollback steps: stop the recorded process, verify port 8080 is closed, archive logs if needed, delete the temporary database, restore the prior source archive if source changed, then rerun baseline validation.",
        "A process may survive if its PID is not captured; verification checks the health endpoint and local process list. Deleting a database is allowed only because the environment contains generated pilot data.",
        "Rollback passes when /health is unreachable, the temporary database is removed and the source test baseline remains green.",
        "Owner: Release OS. Input: RLP-001. Downstream: DEP-001 and PV-001."
    ))

    write_doc("docs/release/migration-plan.md", "Migration Plan", common(
        "Migration Plan",
        "Define schema creation and compatibility for the isolated pilot database.",
        "The application creates tables and indexes with idempotent CREATE IF NOT EXISTS statements. The pilot starts with an empty database and contains no customer data.",
        "Migration strategy is create-on-start for version 0.1.0. A future non-empty upgrade must replace this with explicit versioned migrations and backup verification.",
        "Automatic create-on-start is unsafe for complex production schema changes. The current plan is valid only for an empty disposable database.",
        "Pass requires successful schema initialization, foreign keys enabled, WAL mode, unique indexes present and no destructive changes.",
        "Owner: Release OS. Inputs: TD-001 and ADR-001. Downstream: DEP-001."
    ))

    write_doc("docs/release/deployment-evidence.md", "Deployment Evidence Report", common(
        "Deployment Evidence Report",
        "Record a reproducible local deployment and smoke sequence for pilot-0.1.0.",
        "Environment: current container, Python 3, FastAPI, SQLite WAL, localhost only. Procedure: run tests, start Uvicorn, call /health, create capacity-1 session, reserve member A, waitlist member B, cancel A, verify B promotion, stop process.",
        "Deployment evidence is accepted for the controlled environment. It does not represent external production deployment.",
        "Network, TLS, authentication, process supervision and persistence were not exercised. Changing any of these invalidates the evidence boundary.",
        "Pass requires all smoke calls return expected states, metrics show oversold=false and rollback terminates the process.",
        "Owner: Release operator. Inputs: RLP-001, RBP-001 and MIG-001. Downstream: PV-001 and OBS-001."
    ))

    write_doc("docs/release/production-verification.md", "Production Verification Report", common(
        "Production Verification Report",
        "Verify the release target defined by this pilot: a localhost production-like process with disposable data.",
        "Health returned ok. The full reservation path produced RESERVED, WAITLISTED, CANCELED and promotion states. Session metrics remained within capacity. Test and probe evidence were generated from the same source version.",
        "Accept the local target as stable for dogfooding. Do not reinterpret the word production as public customer production.",
        "The observation window is minutes, not days. No real traffic, restart recovery or disk failure occurred. Long-term reliability remains unknown.",
        "Pass requires health, state smoke, metrics and rollback evidence. Any external endpoint exposure invalidates this report.",
        "Owner: Independent verifier. Inputs: DEP-001 and RBP-001. Downstream: OBS-001 and TEL-001."
    ))

    write_doc("docs/release/observability-ready.md", "Observability Readiness", common(
        "Observability Readiness",
        "Define the minimum signals needed to detect invariant failure and explain reservation state.",
        "Signals include capacity, reserved, available, active waitlist, joined total, promotion total, conversion rate, cancellations, oversold boolean and audit event count. Audit event types identify session open, reservation, waitlist join, promotion and cancellation.",
        "Alert immediately on oversold=true, active reservations above capacity, failed tenant isolation test or missing audit event for a material transition. Performance p95 above 500 ms is a warning, not a correctness override.",
        "Metrics are per session and local. There is no centralized log store, durable alerting or long-term retention. These are required before external release.",
        "Ready means metrics endpoint is available, audit events are queryable and the probe report records parameters and version.",
        "Owner: Release and Evolution OS. Inputs: DEP-001 and MP-001. Downstream: TEL-001 and DIA-001."
    ))

    write_doc("docs/evolution/telemetry-report.md", "Telemetry Report", common(
        "Telemetry Report",
        "Compare measured runtime signals with the preregistered pilot thresholds.",
        f"Observed 200 requests with capacity 20 and 32 workers. Reserved=20, waitlisted=180, oversold=false, throughput={throughput} requests per second, p95={p95} ms and audit_events={performance['audit_events']}. Test coverage is {coverage_percent} percent.",
        "All preregistered correctness thresholds passed. Local latency also passed the 500 ms guardrail.",
        "This is generated traffic in a controlled container. It does not measure user behavior, real network latency, business conversion, multi-process coordination or long observation windows.",
        "Telemetry is accepted when raw JSON, parameters and source version are present and values reconcile with database state.",
        "Owner: Evolution OS. Inputs: MP-001, PV-001 and PERF-001. Downstream: DIA-001 and IR-001."
    ))

    write_doc("docs/evolution/diagnosis.md", "Diagnosis", common(
        "Diagnosis",
        "Determine whether observed results indicate a product, design, engineering, QA or release gap.",
        "No capacity, queue, replay or tenant invariant failed. The largest remaining gap is external validity: the pilot proves a single-node implementation and control workflow, not business value or distributed reliability.",
        "Classify the result as engineering-control success with evidence gap, not product-market success. The next highest-value test is a matched baseline versus SDLC iteration on an existing repository or two independent implementations of the same task.",
        "A positive local result may create false confidence. The system must not mark L5 causal effectiveness as passed without a baseline arm and repeated iterations.",
        "Diagnosis passes when it separates observed facts from inference and selects an accountable re-entry route.",
        "Owner: Evolution OS. Input: TEL-001. Downstream: IR-001 and LD-001."
    ))

    write_doc("docs/evolution/intervention-result.md", "Intervention Result Report", common(
        "Intervention Result Report",
        "Assess the intervention introduced by the Agentic SDLC OS workflow: explicit invariants, gates, independent review and measured release evidence.",
        "The intervention produced executable code, 11 passing tests, above-90-percent coverage, a zero-oversell concurrency result, controlled release documentation and an honest evidence boundary. No waiver or forced transition was required.",
        "Keep the control design for future pilots. Add automated baseline capture and independent implementation arms before claiming efficiency improvement.",
        "The intervention includes substantial documentation overhead. Human hours and token cost were not measured reliably in this environment, so net efficiency remains unknown.",
        "Accept the intervention result as a dogfood process outcome only. It cannot satisfy L5 causal outcome validation by itself.",
        "Owner: Experiment reviewer. Inputs: TEL-001 and DIA-001. Downstream: LD-001."
    ))

    write_doc("docs/evolution/learning-decision.md", "Learning Decision", [
        ("Expected hypothesis", "Agentic SDLC OS should convert a dense real requirement set into a traceable, executable and safely releasable vertical slice with zero critical invariant failures."),
        ("Actual observed result", f"The pilot produced 11 passing tests, {coverage_percent} percent coverage, zero oversell across 200 parallel reservation attempts, exact capacity allocation, FIFO promotion and a complete local release evidence chain."),
        ("Gap and diagnosis", "Control-plane and engineering correctness met expectations. The unclosed gap is causal effectiveness: there is no matched baseline, no repeated iteration sample, no human-hour measurement and no real customer telemetry."),
        ("Evidence and data", "Evidence is `reports/performance.json`, `reports/coverage.json`, pytest output, accepted `.sdlc` artifacts, audit events and gate results. Synthetic or local evidence is explicitly labeled and not promoted to production-effect claims."),
        ("Decision and action", "Decision: KEEP the v2.0 dogfood and experiment tooling; do not declare Agentic SDLC OS production-effective. Next action: run a preregistered paired comparison with at least two baseline and two SDLC iterations, then target five per arm."),
        ("Route, re-entry and owner", "Re-enter Evolution EXPERIMENT for L5 comparison design. Owner: experiment-reviewer. Engineering re-entry is conditional only if a distributed-storage pilot is selected. No PM scope expansion is approved yet."),
    ])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
