# Capability Compiler V2 — Phase 9 Plan

## Objective

Execute real, isolated model evaluations for all 157 frozen candidate Skills and the Phase 4/8 candidate Recipe/router layer. Compare each candidate against its declared real baseline on physically separate holdout cases, execute semantic mutations, preserve every failed case, and produce recomputable run and grading evidence. Phase 9 measures behavior; it does not revise, approve, release, or execute candidate side effects.

## Frozen Inputs

- Phase 3 tree: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 tree: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase 5 tree: `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`
- Phase 6 tree: `7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561`
- Phase 7 tree: `c76902fd5df781db653e214268b044cb4a8cc389a4fce0a188f72a5fba829926`
- Phase 8 tree: `501d9cddfdc44fec4af8f17470c99b57b48ffced977e0fa7086cce568fa92f66`
- 157 Skill evaluation plans, 314 physically separate Skill holdouts, and 157 planned semantic mutations.
- Phase 4 specialized UI Recipe plus Phase 8 15 stage Recipes, 5 composite Recipes, and router fixtures/mutations.

## Evaluation Question

For each atomic Skill and unseen case, decide whether that one Skill should:

- `accept`: the request belongs to this exact atomic responsibility;
- `reject`: an adjacent capability owns the request;
- `needs-input`: the responsibility matches but a requestable prerequisite is missing;
- `blocked`: authority, governance, safety, or immutable scope forbids proceeding.

The prompt never includes the expected decision or adjacent target ID. The deterministic grader reads expected values only after the model run.

## Skill Matrix

For every candidate Skill:

1. Run its declared baseline on both frozen holdout cases.
2. Run the candidate on the same two holdout cases with the same model, system prompt, decoding settings, tool denial, and concurrency class.
3. Produce one mutated candidate by removing the exact frozen semantic marker.
4. Run the mutated candidate on one selected authored boundary/authority case whose expected outcome is causally tied to the removed marker.
5. Run the unmutated candidate on that same mutation-control case.

Planned Skill total: 157 × (2 baseline holdouts + 2 candidate holdouts + 1 mutation control + 1 mutated run) = 942 real model runs. Including specialized UI Recipe, Phase 8 router, Recipe assertions, and matched Recipe mutation controls yields exactly 1,002 planned runs.

## Recipe and Router Matrix

- Phase 4 specialized UI Recipe: run all frozen holdout cases and both frozen mutations with matched unmutated controls.
- Phase 8 router: run all 14 authored and 8 holdout routing cases without exposing expected targets.
- Phase 8 Recipe behavior: run all 8 authored and 6 holdout assertions as scenario decisions.
- Phase 8 mutations: run all 6 planned mutations with matched unmutated controls.

Recipe/router runs use the same no-tool isolated model protocol and structured decision schema. They do not execute referenced Skills or actions.

## Isolation

Every run uses a fresh `pi -p` process with:

- `--mode json`;
- exact pinned model identity recorded from the response;
- `--no-tools --no-skills --no-extensions --no-context-files --no-session`;
- no repository CWD dependency;
- one prompt file containing only system evaluation instructions, the case input, and the baseline/candidate/mutated material;
- no expected label, rubric, case file, sibling Skill, prior output, arbitrary network tool, browser, remote Git, local-system, or production access. The host uses only the declared `router9-qoder` inference channel to send synthetic benchmark input and frozen public repository material to the pinned model; this provider transfer is recorded and grants the evaluated capability no provider-action authority.

The runner must enforce a bounded timeout and bounded concurrency. A timeout, malformed response, missing assistant output, or nonzero exit remains a failed run; it is never retried into invisibility. A retry, if configured, is an additional immutable attempt with its own receipt.

## Run Evidence

Each attempt directory contains:

- `prompt.md` and SHA-256;
- `material.md` and SHA-256;
- `case.json` containing the frozen case only after prompt construction;
- `command.json` with redacted argv, CWD policy, start/end, exit code, duration, timeout, and environment allowlist;
- `events.jsonl` with raw Pi JSON events;
- `full_output.md` and SHA-256;
- `parsed.json` with strict structured-decision parse result;
- `run.json` with model/provider/response model, stop reason, token usage, configuration, artifact hashes, and failure reason;
- `grading.json` created after run completion from frozen expected values;
- `artifact-manifest.json` for the attempt.

Aggregate files never replace per-attempt evidence.

## Structured Output

The model returns exactly one JSON object:

```json
{
  "decision": "accept|reject|needs-input|blocked",
  "reason": "one evidence-bounded sentence",
  "matched_boundary": "short boundary phrase",
  "would_execute": false
}
```

For router runs, `decision` is replaced by `target`; for Recipe scenario runs it is `satisfied|violated|needs-input|blocked`. Any prose outside the object, unknown key, invalid enum, or `would_execute: true` fails parsing.

## Deterministic Grading

- Skill holdout positive → `accept`.
- Skill holdout adjacent negative → `reject`.
- Boundary → `needs-input`.
- Authority stop → `blocked`.
- `would_execute` must always be false.
- Candidate improvement is reported as paired accuracy delta over its declared baseline; no minimum is silently invented after results.
- Mutation detection requires the unmutated control to pass and the mutated run to fail the expected decision or required boundary marker. If both pass, mutation is survived. If control fails, the mutation result is invalid rather than credited.
- Router target must equal the frozen expected target.
- Recipe scenario decision must match the frozen assertion-to-decision mapping and preserve protected-action stops.

No model self-score is accepted. No external LLM Judge is used, avoiding an additional data-transfer boundary. Subjective quality remains for Phase 10 human review.

Predeclared quality thresholds, frozen before the first benchmark run:

- candidate Skill holdout accuracy: at least 95% overall and 90% within every Phase 3–7 cohort;
- candidate Skill accuracy must not trail its declared baseline within any Phase 3–7 cohort;
- Phase 4 specialized UI Recipe candidate route coverage: 100% on four holdouts and not below its released baseline;
- Phase 8 router target accuracy: 100% on authored and holdout sets;
- Phase 8 Recipe assertion accuracy: 100% on authored and holdout sets;
- evidence completeness and zero action execution: 100%.

A threshold miss is retained as a Phase 10 revision finding; thresholds are not lowered after observing results. Behavioral mutation kill rate is diagnostic, not a release threshold, because the frozen mutation markers were designed for deterministic Gate deletion and many have no independently authored causally matched prompt. Each mutation is therefore reported as killed, survived, invalid-control, or behavioral-challenge-needed. Deterministic mutation Gates remain 100% required.

## Aggregation

Report at least:

- totals and completion/failure counts;
- accuracy by phase, lifecycle stage, domain, case kind, baseline kind, permission identity, and mutation scope;
- paired baseline/candidate wins, ties, and regressions;
- bootstrap or exact binomial confidence intervals where applicable;
- duration and token mean, median, standard deviation, p95, and matched deltas;
- mutation kill/survival/invalid-control counts;
- router and Recipe accuracy;
- every failed or malformed case ID with evidence path;
- model identity and concurrency configuration;
- zero action-execution evidence.

## Gates

Phase 9 fails closed on:

- Phase 3–8 tree drift;
- missing declared baseline material or candidate/mutation hash mismatch;
- holdout leakage into prompts or cross-case context;
- prompt containing expected decision/target;
- missing command, raw events, output, parse, grade, duration, token, exit, or hash evidence;
- run directory reuse across baseline/candidate/control/mutation;
- tools, network, browser, remote Git, provider, local-system, or production authority;
- dropped, overwritten, or deleted failed cases;
- aggregate counts not exactly recomputable from attempt manifests;
- false claim that behavioral evaluation equals Phase 10 approval or release.

## Outputs

- `tools/curation/v2_phase9_runner.py`
- `tools/curation/v2_phase9_grade.py`
- `tools/curation/v2_phase9_gate.py`
- `tools/curation/v2_phase9_report.py`
- `tests/curation/test_v2_phase9_gate.py`
- `evals/runs/capability-compiler-v2/phase-9/`
- `curation/v2/phase-9/semantic-review.json`
- `.specs/capability-compiler-v2/phase-9/{gate-report,artifact-manifest,phase-report}.json`

## Stop Conditions

Stop on unavailable authenticated model runtime, prior-tree drift, unbounded cost/concurrency, evidence loss, hidden retry, prompt leakage, undeclared data transfer, or any attempt to execute candidate side effects. A model-runtime blocker must be reported with the exact failed probe and must not be replaced by simulated output.
