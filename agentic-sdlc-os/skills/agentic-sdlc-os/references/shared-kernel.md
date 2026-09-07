# Shared Kernel

## Directory

```text
.sdlc/
├── state.json
├── state.prev.json
├── config.json
├── context.md
├── SUMMARY.md
├── audit/events.jsonl
├── artifacts/
├── evidence/
├── reviews/
├── gates/
├── migrations/
├── ledgers/
│   ├── artifacts.md
│   ├── evidence.md
│   ├── assumptions.md
│   ├── decisions.md
│   ├── risks.md
│   ├── traceability.md
│   ├── learning-log.md
│   ├── routing-log.md
│   └── runs.md
└── os/{pm,design,engineering,qa,release,evolution}.md
```


## Work Item isolation

`work_items` and `active_work_id` live in `.sdlc/state.json`. While a Work Item is active, newly recorded artifacts, evidence, assumptions, decisions, risks, traces, runs and learning records carry its `work_item_id`. Gate evaluation for that change ignores project-history and other Work Items, except that project-global critical risks remain blocking. This prevents a new change from passing by reusing old evidence.

Historical artifacts are revalidated with the governance Profile of the Work Item that produced them.

## Source of truth

Use `.sdlc/state.json` as authoritative state. Markdown ledgers are regenerated views. Every successful mutation increments `revision`, writes `state.prev.json` and appends a hash-chained audit event. Do not manually edit generated tables and assume the JSON changed.

## Core commands

```bash
# Initialize; defaults map low→lite, medium→standard, high→high-assurance
python scripts/sdlc.py init . --name product --type greenfield --criticality medium --profile standard

# Inspect, audit, health and route
python scripts/sdlc.py status .
python scripts/sdlc.py audit .
python scripts/sdlc.py health . --json
python scripts/sdlc.py quality . --json
python scripts/sdlc.py metrics . --json
python scripts/sdlc.py route . "Design the onboarding flow" --json  # honor decision=abstain
python scripts/sdlc.py next .

# Work Item lifecycle for bounded changes
python scripts/sdlc.py work-start . --id WORK-001 --title "bounded change" --bounded --affected-path src/file.py
python scripts/sdlc.py work-status . --json
python scripts/sdlc.py work-end . --status completed --outcome "verified"

# Create/register artifacts
python scripts/sdlc.py new-artifact . --type prd --status draft --owner pm
python scripts/sdlc.py add-artifact . --type prd --path docs/prd.md --status accepted --owner pm --verified-by "PM owner"

# Evidence and reasoning
python scripts/sdlc.py add-evidence . --claim "Users abandon at payment" --source analytics://funnel/checkout --source-type telemetry --quality high --supports art-123 --method "production funnel query"
python scripts/sdlc.py add-assumption . --text "One-click checkout improves completion" --risk high --owner pm --test "A/B test"
python scripts/sdlc.py add-decision . --title "Checkout direction" --choice "One-click" --rationale "..." --evidence ev-123
python scripts/sdlc.py add-risk . --id risk-payment --title "Payment duplication" --severity critical --mitigation "Idempotency key" --owner eng
python scripts/sdlc.py update-risk . --id risk-payment --status closed --mitigation "Fix and recovery test verified"
python scripts/sdlc.py trace . --from goal:checkout --to art-123 --relation implements --evidence ev-123
python scripts/sdlc.py impact . --artifact-id art-123 --json
python scripts/sdlc.py reconcile . --apply --json

# Agent execution economics
python scripts/sdlc.py record-run . --actor engineering-agent --os engineering \
  --skill implementation --model model-x --outcome success \
  --duration-ms 42000 --tokens-input 8000 --tokens-output 2400 \
  --tool-calls 12 --cost-usd 0.18 --artifacts src-1,test-1

# Gate and transition
python scripts/sdlc.py gate . --name pm-ready
python scripts/sdlc.py transition . --to-os design --to-stage INTAKE --reason "pm-ready passed"

# Learning loop and migration
python scripts/sdlc.py learn . --expected "Activation +10%" --actual "+1%" --gap "Value not clear" --gap-type strategy --decision "Revisit segment" --route-os pm --route-stage DISCOVERY
python scripts/sdlc.py migrate . --profile standard
python scripts/sdlc.py validate .
```

## Integrity, waivers and force

Accepted local artifacts are hashed and scored against content contracts. Gate evaluation fails when an accepted file is missing, empty, still contains template placeholders, repeats vague boilerplate, lacks concrete signals, is self-verified under High-Assurance, becomes stale, or changes after acceptance. External artifacts require an explicit SHA-256 checksum.

An accepted upstream change marks reachable downstream accepted artifacts stale. `impact` shows the blast radius; `reconcile --apply` persists drift detected outside the CLI. Reaccept a stale artifact only after reviewing it against the changed upstream source.

A Gate waiver requires a human approver, approval record, compensating control and bounded expiry:

```bash
python scripts/sdlc.py gate . --name pm-ready --waive \
  --reason "reversible prototype" \
  --approver "Alice Chen" --approval-id CR-123 \
  --compensating-control "daily review and automatic rollback" \
  --expires 2026-09-03T00:00:00Z
```

Open critical risks cannot be waived. Relevant artifact, evidence, trace or critical-risk changes invalidate an existing waiver. A forced transition additionally requires `--approver` and `--approval-id` and remains visible in history and audit.

## Evidence quality

- High: direct observation, reproducible system output, primary data, signed approval or strong experiment.
- Medium: credible but indirect source, small sample or partially controlled observation.
- Low: anecdote, unverified statement, synthetic example or weak proxy.

For Gate purposes, `high` evidence counts as high quality only when its `source-type` is primary, official, user-research, telemetry, experiment, test, audit, code or incident. Duplicate claim/source/target combinations count once. Quality labels do not replace source details, method and limitations.
