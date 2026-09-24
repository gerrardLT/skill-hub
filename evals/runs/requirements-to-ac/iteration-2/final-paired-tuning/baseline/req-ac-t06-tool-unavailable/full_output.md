Status: needs-input

# Product Requirements Document (PRD)

## Document Information

### Authors
- Product Management Team (Offline Evaluation Worker)

### Reviewers
- Engineering Lead
- Product Design Lead
- Data & Analytics Lead *(Review pending: analytics export unavailable)*

**Date:** 2026-03-30

### Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1 | 2026-03-30 | PM | Initial draft produced strictly from supplied discovery notes and facts. External analytics export is unavailable; no export attached. Analytics-dependent acceptance criteria marked as `[needs-input]`. No analytics tools queried. |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Target Users & Personas](#3-target-users--personas)
4. [Strategic Context](#4-strategic-context)
5. [Solution Overview](#5-solution-overview)
6. [Success Metrics](#6-success-metrics)
7. [User Stories & Requirements](#7-user-stories--requirements)
8. [Out of Scope](#8-out-of-scope)
9. [Dependencies & Risks](#9-dependencies--risks)
10. [Open Questions](#10-open-questions)
11. [PRD Self-Assessment](#prd-self-assessment)

---

## 1. Executive Summary

We are building a **guided onboarding checklist** for **non-technical small business owners (solopreneurs and teams of 1–10)** to solve the problem of **60% onboarding drop-off in the first 24 hours caused by a lack of first-run guidance**, which will increase the **24-hour activation rate from 40% to 60%** and reduce first-month churn.

*Note on Data Availability:* This artifact is developed strictly from supplied qualitative notes and baseline facts. An external analytics export was not attached, the analytics platform was unavailable, and no analytics tool was queried. All requirements and acceptance criteria dependent on telemetry schema or cohort exports are flagged as `[needs-input]`.

---

## 2. Problem Statement

### Who Has This Problem?
Non-technical small business owners (solopreneurs and small teams of 1–10 employees) who sign up for our SaaS product for the first time without dedicated technical support.

### What Is the Problem?
Users abandon onboarding within the first 24 hours of signup. Upon initial login, they encounter an empty dashboard with no structured guidance, become overwhelmed by configuration options, and abandon the application before taking a single meaningful action.

### Why Is It Painful?
- **User impact:** Users waste 30–60 minutes trying to navigate an empty interface, fail to experience the core product value ("aha moment"), and revert to manual tools or spreadsheets.
- **Business impact:** High first-day drop-off suppresses user activation, driving higher customer churn, depressed customer lifetime value (LTV), and negative word-of-mouth.

### Evidence
- **Customer Interviews:** 8 out of 10 churned users interviewed explicitly stated: *"I didn't know what to do first."* (Discovery interviews, Feb 2026).
- **Customer Quote:** *"I logged in, saw an empty dashboard, and thought 'now what?' I gave up and went back to my spreadsheet."*
- **Support Signals:** Support ticket analysis shows *"How do I get started?"* is the #1 inbound inquiry, accounting for approximately 350 tickets per month.
- **Historical Analytics Note:** Discovery records note that 60% of signups complete 0 core actions within the first 24 hours (Mixpanel discovery reference, Jan 2026).
  - 🔵 **Open Question / Data Notice:** The external analytics tool is currently unavailable and no export was attached. The tool was **not queried** for updated cohort tables, segment funnels, or current retention curves. Detailed validation of current drop-off points remains pending external data supply.

---

## 3. Target Users & Personas

### Primary Persona: Solo Entrepreneur Sam
- **Role:** Freelance consultant, solopreneur.
- **Context:** 1-person business, no IT or engineering support, utilizes basic SaaS productivity tools, email, and spreadsheets. Low technical savviness.
- **Goals:** Set up the workspace quickly, realize immediate software value without technical troubleshooting.
- **Pain points:** Overwhelmed by complex enterprise UIs; lacks time to read documentation or watch multi-minute video tutorials; requires immediate utility.
- **Current behaviour:** Registers for a product trial, explores for a brief period, and churns within 24 hours if the workflow is ambiguous.

### Secondary Persona: Small Business Owner
- **Role:** Owner-operator managing a team of 5–10 employees.
- **Context:** Time-constrained, manages operations, needs team members onboarded without repetitive manual training.
- **Differs from primary:** Slightly more tolerant of initial administrative setup, but requires frictionless delegation and team member invite workflows.

### Jobs-to-Be-Done
- **Functional Job:** When I sign up for the platform, I want a structured, step-by-step setup checklist so that I can configure my first project within 30 minutes.
- **Emotional Job:** Feel confident and competent in adopting new technology without feeling frustrated or overwhelmed.
- **Social Job:** Demonstrate competence to clients and collaborators by running professional workflows efficiently.

---

## 4. Strategic Context

### Business Goals
- **Strategic Alignment:** Supports Company Q1 OKR: *Reduce churn from 15% to 8%*. Onboarding activation is identified as the primary operational lever for retention.
- **Revenue Impact:** Reducing early-stage churn directly protects customer acquisition cost (CAC) efficiency and improves net revenue retention.

### Market Opportunity
- **TAM:** 50M small businesses globally *(🔶 Assumption: based on preliminary market research notes)*.
- **SAM:** 5M small businesses using SaaS productivity software.
- **SOM:** 500K solopreneurs in target launch segments.

### Competitive Landscape
- **Current Alternatives:** Primary competitors (Competitor A, Competitor B) provide guided first-run checklists and interactive walkthroughs upon account creation.
- **Our Gap:** Our product currently drops new accounts directly into an unpopulated dashboard with zero structured prompts.

### Why Now?
Churn increased significantly in Q4, with early onboarding drop-off identified as the primary failure point (60% drop-off in the first 30 days). Resolving first-run guidance is mandatory to arrest customer loss and achieve the retention OKR.

---

## 5. Solution Overview

### Solution Description
We are introducing a native, interactive **Guided Onboarding Checklist** displayed immediately upon a user's initial login. The checklist guides users through three sequential, high-impact setup steps:
1. Create your first project.
2. Invite a teammate (optional).
3. Complete a sample task.

The checklist provides transparent visual progression (progress bar), dynamic state persistence across sessions, non-intrusive dismissibility, and an encouraging completion milestone modal that directs the user to their next high-value action.

### Key Features
1. **Curated 3-Step Scope:** Limited to three critical activation actions to eliminate choice overload.
2. **Dismissible & Non-Blocking:** Users can dismiss or collapse the guide to explore independently without being hard-blocked.
3. **Persistent Progress Indicator:** Visual progress bar (1/3, 2/3, 3/3) with automatic checkmarks upon task completion, synchronized across user sessions.
4. **Completion Celebration Modal:** Positive reinforcement modal upon checklist completion providing context-sensitive next steps.

---

## 6. Success Metrics

| Metric Type | Metric Name | Baseline (Supplied Facts) | Target | Measurement Timeline | Data Status |
|---|---|---|---|---|---|
| **Primary** | 24-Hour User Activation Rate (% signups completing first core action within 24h) | 40% | 60% | 30 days post-launch | 🔵 **needs-input** (Baseline cited from discovery notes; live analytics tool unavailable and was not queried) |
| **Secondary** | Time-to-First-Action | 3 days | 1 day | 30 days post-launch | 🔵 **needs-input** (Cohort telemetry verification pending analytics export) |
| **Secondary** | Checklist Completion Rate | 0% (new feature) | 80% of active sessions | Ongoing | Instrument via feature telemetry |
| **Secondary** | Inbound "How do I get started?" Support Tickets | 350 tickets/month | < 175 tickets/month (50% reduction) | 60 days post-launch | Tracked via support ticketing system |
| **Guardrail** | Sign-up Funnel Conversion Rate | 10% | Maintain ≥ 10% (no friction added to registration) | Weekly monitoring | 🔵 **needs-input** (Export required to confirm current pre-login conversion baseline) |

---

## 7. User Stories & Requirements

### Epic Hypothesis
We believe that introducing a guided onboarding checklist for new non-technical users will increase the 24-hour activation rate from 40% to 60% because users currently abandon the application due to lack of immediate direction. Success will be evaluated 30 days post-release via cohort activation tracking.

---

### Story 1: Display Onboarding Checklist on First Login
**As a** new user logging into the platform for the first time,  
**I want** to see a clear setup checklist with 3 core steps,  
**So that** I know exactly what actions to take to get started.

**Acceptance Criteria:**
- [ ] 1.1: When an authenticated user logs into their workspace for the first time, the onboarding checklist modal displays prominently on the dashboard.
- [ ] 1.2: The modal clearly displays three discrete steps:
  - Step 1: "Create your first project"
  - Step 2: "Invite a teammate" *(marked as optional)*
  - Step 3: "Complete a sample task"
- [ ] 1.3: The user can dismiss the checklist via a close ("X") button or "I'll explore on my own" link.
- [ ] 1.4: If dismissed, the user's preference is recorded so the modal does not reappear on subsequent page refreshes or logins.
- [ ] 1.5: `[needs-input]` **Analytics Telemetry Event:** Client emits `onboarding_checklist_viewed` on initial display with attributes for `user_id`, `account_created_at`, and `experiment_cohort`. *(Status: needs-input; exact event schema, property types, and destination routing depend on external analytics export. Tool was unavailable and not queried).*
- [ ] 1.6: `[needs-input]` **Dismissal Telemetry Event:** Client emits `onboarding_checklist_dismissed` capturing time elapsed before dismissal and step completion state. *(Status: needs-input; pending analytics pipeline telemetry specification).*

---

### Story 2: Track and Persist Checklist Progress
**As a** new user working through onboarding,  
**I want** to see visual progress updates and have my state saved,  
**So that** I know how much setup remains even if I navigate away or log out.

**Acceptance Criteria:**
- [ ] 2.1: Completing any of the three designated tasks automatically marks that step with a visible checkmark and updates the visual progress bar (e.g., 0/3 → 1/3 → 2/3 → 3/3).
- [ ] 2.2: The checklist allows steps to be completed in any sequence without blocking the user.
- [ ] 2.3: Checklist completion state persists across sessions; logging out and logging back in maintains the completed checkmarks and progress bar state.
- [ ] 2.4: `[needs-input]` **Step Completion Telemetry Event:** Emits `onboarding_step_completed` with payloads `step_name`, `step_index`, and `time_since_signup_seconds`. *(Status: needs-input; telemetry property definition and export schema unavailable; tool was not queried).*
- [ ] 2.5: `[needs-input]` **Action Mapping Verification:** Explicit database/event trigger mapping linking the action "Create project" to the analytics activation event ID. *(Status: needs-input; external analytics dictionary and export missing).*

---

### Story 3: Celebrate Checklist Completion
**As a** new user who finishes all three onboarding steps,  
**I want** to see confirmation of setup completion and suggested next steps,  
**So that** I feel confident moving forward into day-to-day use.

**Acceptance Criteria:**
- [ ] 3.1: When the third checklist item is completed, a celebration modal is triggered within 500ms.
- [ ] 3.2: The modal displays confirmation copy: *"You're all set! Here's what to do next:"* along with a direct call-to-action button to navigate to the primary project dashboard.
- [ ] 3.3: The modal is dismissible and does not reappear once closed.
- [ ] 3.4: `[needs-input]` **Completion Telemetry Event:** Client emits `onboarding_checklist_completed` with duration from first view to completion. *(Status: needs-input; pending telemetry export for naming standard).*

---

### Story 4: Telemetry Pipeline & Activation Verification
**As a** product manager,  
**I want** all onboarding interaction events reliably transmitted to our downstream reporting store,  
**So that** we can calculate the 24-hour activation rate and evaluate performance against the 60% target.

**Acceptance Criteria:**
- [ ] 4.1: `[needs-input]` **Activation Event Definition:** Activation calculation logic must precisely match historical reporting definitions for "first core action within 24 hours". *(Status: needs-input; historical cohort definitions depend on the external analytics export, which is unavailable. Tool was not queried).*
- [ ] 4.2: `[needs-input]` **Downstream Destination Routing:** Telemetry payload schema validation for data warehouse ingestion. *(Status: needs-input; schema documentation requires external data export).*
- [ ] 4.3: `[needs-input]` **Baseline Cohort Reconciliation:** Reconciliation of active trial user funnel vs. previous 40% baseline. *(Status: needs-input; external analytics export not attached; tool unavailable).*

---

### Technical Constraints & Edge Cases
- **Constraints:** Must operate reliably across standard desktop web browsers (Chrome, Safari, Edge, Firefox). Minimal performance footprint (< 50ms render latency).
- **Edge Cases:**
  - *Out-of-order execution:* User completes step 3 before step 1. System must register step 3 as complete and display progress as 1/3 without error.
  - *Team invite skipped:* Step 2 is explicitly optional; if the user completes steps 1 and 3 and marks step 2 skipped, the system must trigger completion celebration.
  - *Network latency:* If network connectivity drops while completing a step, completion state must be queued locally and retried.

---

## 8. Out of Scope

### Not Included in This Release
1. **Multi-Persona Dynamic Branching:** Presenting customized checklists based on role or team size. (Adds initial complexity; test standardized 3-step baseline first).
2. **Embedded In-App Video Walkthroughs:** Hosting video players inside checklist modals. (High production overhead; validate textual/visual guidance first).
3. **Gamification Systems (Badges, Reward Points):** Focus remains on core utility and immediate functional activation.
4. **Mobile Web Optimization:** Initial implementation targets desktop web browsers; mobile responsive refinement is deferred.

### Future Considerations
- Role-specific checklist templates for multi-user enterprise accounts.
- Automated nudges/emails for users who abandon the checklist with 1 of 3 steps completed.

---

## 9. Dependencies & Risks

### Dependencies
- **Technical:** Existing in-app modal and notification UI components.
- **Design:** Final design components and asset handoff for checklist UI and celebration modal (Target: Week 1).
- **External / Data:** **External Analytics Export.** Telemetry naming conventions, event dictionary, and baseline validation depend on the analytics tool export.
  - *Status:* **BLOCKED / NEEDS-INPUT.** The analytics platform was unavailable, no export was attached, and the tool was not queried. Engineering cannot finalize data contracts until this export is provided.

### Risks & Mitigations
- **Risk 1 (Data Ambiguity):** Analytics-dependent acceptance criteria cannot be validated in staging or production without external telemetry specs.
  - *Mitigation:* Explicitly tagged criteria as `[needs-input]`. Feature logic will proceed using local event abstractions, with final telemetry binding paused until analytics export is provided.
- **Risk 2 (Immediate Dismissal):** Users may dismiss the checklist immediately without reading.
  - *Mitigation:* Ensure checklist is easily re-opened via a compact dashboard widget; monitor dismissal rate closely.
- **Risk 3 (Step Ambiguity):** Step descriptions could confuse non-technical users.
  - *Mitigation:* Copy grounded in user interview feedback; keep labels short, action-oriented, and jargon-free.

---

## 10. Open Questions

| ID | Open Question | Owner | Deadline | Status |
|---|---|---|---|---|
| Q1 | What is the exact telemetry schema, event naming convention, and destination pipeline from the analytics platform? | Analytics / BI Lead | Prior to Sprint Planning | 🔵 **needs-input** (External tool unavailable; no export attached; tool not queried) |
| Q2 | What are the exact cohort filter parameters previously used to measure the 40% 24-hour activation baseline in historical reports? | Product / Analytics | Prior to Sprint Planning | 🔵 **needs-input** (Pending export attachment) |
| Q3 | Should users who dismiss the checklist be able to re-launch it from a persistent dashboard banner or help menu? | Product Design | Design Review | Open |
| Q4 | Will this feature be evaluated via a 50/50 A/B test or a phased cohort rollout? | Product Lead | Release Planning | Open |

---

## PRD Self-Assessment

### Strongest Section
- **Section 2 (Problem Statement) & Section 5 (Solution Overview):** Solidly anchored in qualitative discovery findings, validated customer pain points ("empty dashboard"), direct quotes, and unambiguous functional scope for the 3-step checklist.

### Weakest Section
- **Section 6 (Success Metrics) & Section 7 (User Stories - Telemetry Criteria):** Highly dependent on external analytics specifications. Because the external analytics platform was unavailable, no export was attached, and no external query was conducted, exact baseline verification and event schemas could not be completed and are marked `[needs-input]`.

### Top Assumptions to Validate

| # | Assumption | Section | Risk if Wrong | Proposed Validation |
|---|---|---|---|---|
| 1 | 40% activation rate and 60% drop-off cited in discovery notes represent current steady-state performance. | Section 2 / Section 6 | Baseline could be inaccurate, misrepresenting true lift post-launch. | Obtain and inspect external analytics export once service is restored. |
| 2 | A 3-step checklist without embedded video is sufficient guidance to unblock non-technical solopreneurs. | Section 5 / Section 7 | Users may still abandon if individual steps lack micro-guidance. | Usability testing on prototype prior to engineering completion. |
| 3 | Solopreneurs are willing to complete sample tasks rather than jumping immediately to custom data entry. | Section 5 | Drop-off at Step 3 if users consider sample tasks unnecessary. | Monitor per-step drop-off telemetry post-launch. |

### Recommended Next Step
- **Data Team Action:** Provide the external analytics export (event catalog, cohort definitions, and recent 24-hour activation baseline data) to resolve all acceptance criteria and metrics currently marked as `[needs-input]`. Do not attempt to query or fabricate analytics data in the interim.

---

Status: needs-input
