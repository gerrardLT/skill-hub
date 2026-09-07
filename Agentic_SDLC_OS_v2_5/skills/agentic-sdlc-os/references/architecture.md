# Architecture

## Layers

```text
User intent
  ↓
Agentic SDLC Orchestrator
  ├─ Shared Kernel: state, evidence, assumptions, decisions, risks, traceability, audit
  ├─ PM OS
  ├─ Design OS
  ├─ Engineering OS
  ├─ QA OS
  ├─ Release OS
  └─ Evolution OS
       ↓
Evidence-driven re-entry to the owning OS
```

The Orchestrator decides **where work belongs**. Domain OS Skills decide **how work is executed**. Third-party Skills provide bounded specialist methods. Subagents create independent contexts; they are not permanent departments.

## Control flow

```text
PM --pm-ready--> Design --design-ready--> Engineering
Engineering --build-ready--> BUILD --verification-ready--> QA
QA --release-ready--> Release --production-ready--> Evolution
Evolution --learning-decision--> any owning OS/stage
```

A Gate is a decision boundary, not a document checklist. It evaluates accepted artifacts, qualifying evidence, directed trace paths and non-compensable risks.

## Process profiles

- `lite`: low-criticality, reversible, contained work.
- `standard`: normal production software.
- `high-assurance`: regulated, irreversible or high-blast-radius work.

Profiles adjust Gate depth. They never remove critical-risk blocks, integrity checks, audit requirements or human approval. High-criticality projects cannot use `lite`.

## Data and audit flow

`.sdlc/state.json` is the machine-readable source of truth. Each successful mutation increments `revision`, keeps `state.prev.json`, and appends a hash-chained event to `.sdlc/audit/events.jsonl`. Markdown ledgers and `SUMMARY.md` are human views.

Use `audit` to verify the chain and `health` to inspect control-plane completeness. Hard failures such as an open critical risk or broken audit chain cannot be compensated by a high aggregate score.

## Design choices

- One global Orchestrator prevents six isolated workflows.
- Separate domain Skills keep context bounded and replaceable.
- External Skills are referenced, not vendored, reducing license and version drift.
- Gate pass, waiver and emergency force remain distinguishable.
- Trace coverage requires valid directed paths, not arbitrary edge counts.
- Production evidence can invalidate any prior artifact.
