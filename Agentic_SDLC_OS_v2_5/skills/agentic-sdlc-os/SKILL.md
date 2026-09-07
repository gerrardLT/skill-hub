---
name: agentic-sdlc-os
description: >-
  Orchestrate an evidence-driven software lifecycle across product, design, engineering, QA, release and production evolution. Use for greenfield or brownfield software projects, project rescue, end-to-end feature delivery, cross-functional handoffs, quality gates, release readiness, incident recovery, or continuous improvement. Routes work to the correct domain OS, maintains the .sdlc shared kernel, records evidence, assumptions, decisions, risks and traceability, enforces stage gates, invokes specialist skills or isolated subagents only when justified, and sends production learning back to the stage that owns the root cause.
---

# Agentic SDLC Operating System

Treat this Skill as the control plane for an entire software project. Route work; do not duplicate every specialist method inside this Skill.

## Operating protocol

1. Locate the project root and inspect `.sdlc/state.json`, `.sdlc/context.md`, accepted artifacts, open risks and traceability.
2. If the project has not been initialized and the request is project-level, prefer `scripts/bootstrap_project.py <root> --name <name>` so risk factors, domain packs and budgets are recorded. Otherwise run `scripts/sdlc.py init <root>`. Select the smallest safe profile: `lite`, `standard` or `high-assurance`; hard-risk escalations override convenience.
3. Classify the request as greenfield, brownfield, change, defect, release, incident or learning work. For a bounded change or defect, start a Work Item before execution with `work-start`, explicit affected paths and realistic risk factors. The project Profile is the default governance envelope; the active Work Item Profile controls execution depth. A bounded item may downshift only when its paths and risks permit it.
4. Run `scripts/sdlc.py route <root> "<task>"`; combine the result with current state, upstream evidence and the cost of a wrong decision. When `decision=abstain`, do not transition automatically: perform semantic classification from the full context, state assumptions, or obtain the missing context.
5. Invoke only the relevant domain Skill: `pm-operating-system`, `design-operating-system`, `engineering-operating-system`, `qa-operating-system`, `release-operating-system` or `evolution-operating-system`. Domain packs apply to the active Work Item only when its title, affected paths or explicit declaration show material impact.
6. Use installed third-party Skills only for bounded specialist work. Never run every Skill by default.
7. Register material artifacts, evidence, assumptions, decisions, risks and traceability in the shared kernel. During active work, records are scoped to that Work Item and cannot satisfy a different Work Item's Gate. Accept artifacts only after content-contract, concrete-signal, independent-verification and integrity checks; classify evidence source type and limitations.
8. Advance stages adjacently. Before BUILD or any cross-OS handoff, run the applicable Gate. A Gate requires accepted artifacts, qualifying evidence and directed trace paths. Never waive or force a Gate without a human approver, approval ID and recorded compensating control. Never waive an open critical risk.
9. Before consequential handoffs or release, run artifact quality, dependency impact, audit, health and cost checks. Apply active domain-pack overlays. A health score or low cost cannot compensate for a hard fail.
10. For concurrent Agents or human approvals, use the database control plane rather than direct shared-file writes. Enforce revision checks, leases, fencing tokens, RBAC, independent approvals, encrypted secrets and recovery.
11. Make completion claims only after fresh verification. Report `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED` or `NEEDS_CONTEXT` with evidence.

## Routing

| Intent | Primary OS |
| --- | --- |
| Problem discovery, strategy, PRD, prioritization, roadmap | PM |
| UX, UI, flows, states, prototype, accessibility | Design |
| Architecture, implementation, refactor, debugging, code review | Engineering |
| Test strategy, automation, regression, non-functional quality | QA |
| CI/CD, migration, rollout, production verification, rollback | Release |
| Metrics, feedback, incident, diagnosis, experiment, learning | Evolution |

For mixed requests, identify the **current bottleneck** and route there first. A downstream symptom does not prove a downstream root cause.

## Mandatory distinctions

Keep these separate in every material output:

- **Fact:** directly supported by a cited source, observed system behavior or reproducible command output.
- **Inference:** interpretation derived from facts.
- **Assumption:** unverified claim with an owner, risk and test.
- **Decision:** chosen action with rationale, alternatives, evidence and consequences.

Do not average away critical safety, security, privacy, legal, reliability or data-integrity failures.

## Project modes

### Greenfield

Start at PM unless accepted evidence already satisfies an upstream Gate. Prefer reversible experiments before expensive implementation.

### Brownfield or rescue

First establish a baseline: architecture, behavior, tests, deployment, observability, user outcomes and known risks. Route to the highest-leverage constraint rather than rewriting everything.

### Production incident

Route immediately to Evolution for triage and stabilization. Use Release for rollback and Engineering for technical remediation. Preserve evidence and defer blame or speculative redesign.

Initialization defaults reflect these paths: greenfield starts in PM, brownfield and migration start in Engineering, and incident work starts in Evolution. Override only when project evidence supports another start OS.

### Change request

Route to the OS owning the changed decision, then perform downstream impact analysis through traceability. Re-run affected Gates; do not assume an accepted artifact remains valid.

## Shared-kernel commands

```bash
python scripts/sdlc.py status <project>
python scripts/sdlc.py next <project>
python scripts/sdlc.py route <project> "task"
python scripts/sdlc.py gate <project> --name pm-ready
python scripts/sdlc.py audit <project>
python scripts/sdlc.py health <project>
python scripts/sdlc.py quality <project>
python scripts/sdlc.py impact <project> --artifact-id ART-001
python scripts/sdlc.py reconcile <project> --apply
python scripts/sdlc.py metrics <project>
python scripts/sdlc.py validate <project>
python scripts/sdlc.py migrate <project> --profile standard

# Bounded change: reassess risk inside a high-assurance project
python scripts/sdlc.py work-start <project> --id WORK-001 --title "bounded fix" --bounded --affected-path path/to/file
python scripts/sdlc.py work-status <project>
python scripts/sdlc.py work-end <project> --status completed --outcome "verified and released"

# One-command risk-tailored bootstrap
python scripts/bootstrap_project.py <project> --name my-project --domain-pack saas --budget-usd 25

# Automatic evidence collection
python scripts/collect_evidence.py <project> --test-command "python -m pytest" --artifact dist/app.zip --register

# Governance and control plane
python scripts/skill_governance.py verify-lock --lock manifest/skills.lock.json
python scripts/cost_governance.py assess <project> --forecast-usd 2 --forecast-tokens 10000
python scripts/control_plane.py serve --database-url "$SDLC_DATABASE_URL"
python scripts/control_plane_stress.py --database-url "$SDLC_DATABASE_URL" --output control-plane-stress.json
python scripts/maturity_gate.py assess maturity-evidence.json --target production-candidate --json
```

Use `new-artifact`, `add-evidence`, `add-assumption`, `add-decision`, `add-risk`, `update-risk`, `trace`, `record-run`, `transition` and `learn` as described in [shared-kernel.md](references/shared-kernel.md).

For `bounded + lite` work, prefer the compact path `Change Plan → Change Verification → Release Recommendation`; compress Engineering to `INTAKE → BUILD → HANDOFF` and QA to `INTAKE → EXECUTION → RECOMMENDATION`. Tests, static review and diff verification remain evidence requirements; compact flow means less duplicate paperwork, not lower verification quality.

Accepted local artifacts are content-hashed and scored against `artifact-contracts.json`. Missing, placeholder, undersized, repetitive, vague, insufficiently concrete, self-verified, stale or modified accepted artifacts cannot satisfy a Gate. Accepted upstream changes mark downstream derivatives stale; direct filesystem drift propagates during Gate assessment or `reconcile`. External artifacts require an explicit checksum. Duplicate evidence counts once; high-quality Gate evidence must use a qualifying source type. Trace coverage is directional: arbitrary links do not satisfy a required end-to-end path. Every state save appends a hash-chained audit event. Record material Agent executions so Token, tool, duration and cost budgets remain visible.

## Production and governance policy

Use local `.sdlc/` files for a single-writer repository. When writers can overlap, synchronize through the production control plane; never rely on filesystem last-write-wins. Treat third-party Skills as pinned dependencies: scan, lock, verify, measure and retire them. Preflight cost before parallel research or tool fan-out. Apply domain packs for HarmonyOS, SaaS, AI Agent, ecommerce or finance work. See the dedicated references below.

Specialist composition is also governed: Design uses one primary visual director per work item; QA must not repair product source and then approve its own repair; Evolution stays provider-neutral until repository/deployment evidence explicitly activates a Sentry, Datadog or PostHog adapter. Provider tools supply evidence/actions only and never own Gates or `learning-decision`.

## Effectiveness validation

Keep control correctness separate from productivity claims. Use L0-L4 tests and L5-A dogfooding to prove the system executes safely. Use the preregistered L5-B matched-pair harness for causal comparison with a baseline Agent. Formal L5-B evidence requires matched start state/environment/model/toolset, isolated execution contexts, balanced order, complete independent blind review and a final seal. Synthetic fixtures validate only the harness and must never be reported as efficiency evidence. Never label the system Production Candidate or Production Ready unless `maturity_gate.py` passes the corresponding evidence claim. For v2.5 production evidence, require immutable third-party Skill supply-chain audit, the isolated formal L5-B runner, live PostgreSQL fault validation, a real wall-clock soak, and organization-grade RBAC/secret/backup/audit drills. See [production-evidence-v25.md](references/production-evidence-v25.md).

## Specialist and subagent policy

Use a subagent only when the work benefits from independent context, parallel evidence collection, adversarial review or operational isolation. Give each subagent a bounded question, explicit inputs, output contract and stop condition. The orchestrator owns synthesis and final decisions. See [subagents.md](references/subagents.md).

## Cross-cutting constraints

At every OS, assess security, privacy, accessibility, reliability, performance, observability, data integrity and reversibility in proportion to project criticality. See [quality-attributes.md](references/quality-attributes.md).

## References

- Architecture and state flow: [architecture.md](references/architecture.md)
- Production control plane: [production-control-plane.md](references/production-control-plane.md)
- Dynamic tailoring: [process-tailoring.md](references/process-tailoring.md)
- Skill governance: [skill-governance.md](references/skill-governance.md)
- Cost governance: [cost-governance.md](references/cost-governance.md)
- Domain packs: [domain-packs.md](references/domain-packs.md)
- L5-B matched experiment: [l5b-matched-experiment.md](references/l5b-matched-experiment.md)
- Maturity claim gate: [maturity-gate.md](references/maturity-gate.md)
- Process profiles: [process-profiles.md](references/process-profiles.md)
- Routing and re-entry rules: [routing.md](references/routing.md)
- Shared kernel and CLI: [shared-kernel.md](references/shared-kernel.md)
- Gate policy: [gates.md](references/gates.md)
- Handoff/output contracts: [output-contracts.md](references/output-contracts.md)
- Artifact content contracts: [manifests/artifact-contracts.json](references/manifests/artifact-contracts.json)
- Third-party Skill policy: [external-skills.md](references/external-skills.md)
- Subagent protocol: [subagents.md](references/subagents.md)
- L5 real-project validation: [l5-validation-protocol.md](references/l5-validation-protocol.md)
- L5-A dogfooding protocol: [real-project-dogfood.md](references/real-project-dogfood.md)
- Worked scenarios: [examples.md](references/examples.md)
