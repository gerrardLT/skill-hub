# QA Test Handoff — Approved Copy Correction

## Operating contract

- QA is read-only: report findings and evidence; do not repair implementation, rewrite upstream records, or make product decisions.
- Test only the bounded correction authorized by the supplied product direction.
- Do not infer missing identifiers, token names, before/after text, behavior, layout, outcomes, error handling, permissions, or recovery behavior.
- If the execution dependencies do not provide the exact authorized values, stop the affected tests and report them as blocked rather than guessing.

## Source and authority

- `SRC-1` — Product input supplied for this run.
- `AUTH-1` — The approved content ticket is the authority for the exact misspelled word, its approved correction, and the affected existing content token. This handoff does not reproduce values that were not supplied.

The approved content ticket, not this handoff, is authoritative for the unresolved ticket identifier, token identifier, misspelled word, and approved spelling. Supplied product direction remains the authority for `RULE-4`.

## Preserved product facts and unknowns

- `FACT-1` — An approved content ticket authorizes correcting one misspelled word in an existing empty-state message. Evidence: `SRC-1`; authority: `AUTH-1`.
- `FACT-2` — No behavior or layout change is authorized. Evidence: `SRC-1`; authority: `AUTH-1`.
- `FACT-3` — The approved ticket and existing content token must remain dependencies. Evidence: `SRC-1`; authority: `AUTH-1`.
- `OPEN-1` — The ticket identifier, token identifier, misspelled word, and approved spelling are not present in `SRC-1`; they must be read from the approved ticket at execution time and must not be inferred. Execution requires access to `DEP-1` and `DEP-2`; if either dependency is unavailable or does not identify the exact before/after word, implementation and affected QA verification must stop rather than guess.

No target user is identified or needed for this bounded correction. No user, business, or quantitative outcome was supplied, so QA must not claim one. No conflicts were supplied.

## Requirements, rules, dependencies, and scope

- `REQ-1` — Correct exactly the one misspelled word identified by the approved content ticket in the existing empty-state message. Source: `FACT-1`; authority: `AUTH-1`; depends on `DEP-1` and `DEP-2`.
- `RULE-1` — The resulting word must exactly match the approved correction in the content ticket. Source: `FACT-1`; authority: `AUTH-1`.
- `RULE-2` — Do not change behavior. Source: `FACT-2`; authority: `AUTH-1`.
- `RULE-3` — Do not change layout. Source: `FACT-2`; authority: `AUTH-1`.
- `RULE-4` — Do not claim or infer outcomes. Source: `SRC-1`; authority: supplied product direction.
- `DEP-1` — Approved content ticket, required as the source of the exact correction and authorization. Source: `FACT-3`.
- `DEP-2` — Existing content token named by the approved ticket; modify that token rather than creating or substituting another token. Source: `FACT-3` and `AUTH-1`.
- `SCOPE-1` — Included: replacement of the single authorized misspelled word in the existing token value. Source: `FACT-1` and `FACT-3`.
- `SCOPE-2` — Excluded: any other copy edit, token change, behavior change, layout change, implementation redesign, or outcome claim. Source: `FACT-1`, `FACT-2`, and `RULE-4`.

## Entry gate and evidence capture

Before executing tests, QA must obtain without editing:

1. `DEP-1`, the approved content ticket.
2. From `DEP-1`: ticket identifier, affected existing content token identifier, exact misspelled word, and exact approved correction.
3. `DEP-2`, the existing token named by that ticket.
4. A pre-change implementation or equivalent diff baseline sufficient to compare content, token identity, behavior, and layout.
5. The resulting implementation/build under test.

Record the authoritative values exactly as written; do not normalize spelling, capitalization, punctuation, whitespace, or token identity. If items 1–3 are absent, inconsistent, or fail to identify an exact before/after word, mark `TC-1` and dependent tests `BLOCKED`, cite `OPEN-1`, and stop rather than infer. If comparison evidence in items 4–5 is unavailable, report the affected non-regression test as `BLOCKED`; do not claim a pass.

## Test cases

### `TC-1` — Dependency and authority gate

**Verifies:** `OPEN-1`, `DEP-1`, `DEP-2`, `AUTH-1`

**Preconditions:** Approved ticket and implementation artifacts are presented to QA.

**Steps:**

1. Confirm the approved content ticket is available and is the authorization source.
2. Confirm it identifies one existing content token.
3. Confirm it identifies one exact misspelled word and one exact approved correction.
4. Confirm the named existing token is available and can be inspected.
5. Record the values and evidence locations exactly, without filling any omission.

**Expected result:** All four unresolved values are supplied by `DEP-1`; the named token is the inspected `DEP-2`; no value is inferred.

**Report-only failure/block rule:** Report a mismatch as a finding. Report unavailable or insufficient authority/dependency evidence as `BLOCKED` under `OPEN-1`. Do not repair the ticket or choose a spelling/token.

### `TC-2` — Authorized spelling correction

**Verifies:** `AC-1`

**Maps to:** `REQ-1`, `RULE-1`, `DEP-1`, `DEP-2`, `SCOPE-1`

**Preconditions:** `TC-1` passes; the resulting token value is inspectable.

**Given** the approved content ticket identifies the existing content token, the misspelled word, and its approved correction  
**When** the authorized copy correction is applied  
**Then** that token's empty-state message contains the approved spelling in place of the identified misspelled word.

**Steps:**

1. Open the exact existing token identified by `DEP-1`.
2. Compare its resulting empty-state message with the exact before/after word pair from `DEP-1`.
3. Confirm the identified misspelled occurrence has been replaced by the exact approved spelling.
4. Confirm the inspected token is the existing `DEP-2`, not a new or substituted token.

**Expected result:** The exact authorized token contains the exact approved spelling in place of the exact misspelled word, satisfying `REQ-1` and `RULE-1` within `SCOPE-1`.

**Evidence to attach:** Ticket reference and quoted before/after values; token identifier; resulting token value or focused diff.

### `TC-3` — Copy-only diff boundary

**Verifies:** `AC-2` content and token scope

**Maps to:** `REQ-1`, `DEP-2`, `SCOPE-2`

**Preconditions:** `TC-1` passes; a pre-change comparison is available.

**Given** the pre-change implementation and the approved ticket  
**When** the resulting change is compared with the pre-change implementation  
**Then** the only product-content difference is the one authorized word replacement.

**Steps:**

1. Compare the complete resulting change with the pre-change implementation.
2. Confirm exactly one authorized word replacement occurs in the existing `DEP-2` value.
3. Confirm there are no other copy edits.
4. Confirm there is no token creation, deletion, rename, substitution, or unrelated token change.
5. Confirm there is no implementation redesign or outcome claim.

**Expected result:** The complete product-content delta is limited to the single ticket-authorized word replacement; all exclusions in `SCOPE-2` remain absent.

**Evidence to attach:** Complete focused change/diff evidence, including unchanged token identity and the absence of additional content changes.

### `TC-4` — Behavior non-regression

**Verifies:** `AC-2`, `RULE-2`

**Maps to:** `REQ-1`, `RULE-2`, `SCOPE-2`

**Preconditions:** `TC-1` passes; comparable pre-change and resulting behavior evidence is available for the affected empty state.

**Steps:**

1. Exercise or inspect the affected empty state under equivalent pre-change and resulting conditions.
2. Compare triggering conditions, state transitions, interactions, and observable functional results relevant to that state.
3. Record any behavior difference without proposing a fix.

**Expected result:** No behavior difference is present; only the authorized displayed word differs.

**Evidence to attach:** Comparable pre/post observations, logs, recordings, or implementation diff sufficient to establish unchanged behavior.

### `TC-5` — Layout non-regression

**Verifies:** `AC-2`, `RULE-3`

**Maps to:** `REQ-1`, `RULE-3`, `SCOPE-2`

**Preconditions:** `TC-1` passes; comparable pre-change and resulting layout evidence is available for the affected empty state.

**Steps:**

1. Render or inspect the affected empty state under equivalent pre-change and resulting conditions.
2. Compare element placement, dimensions, wrapping, spacing, and other observable layout characteristics.
3. Record any layout difference without proposing a fix.

**Expected result:** No layout difference is present; only the authorized word's spelling differs.

**Evidence to attach:** Comparable pre/post screenshots, measurements, or implementation evidence sufficient to establish unchanged layout.

## Acceptance decision

- `AC-1` passes only if `TC-1` and `TC-2` pass.
- `AC-2` passes only if `TC-1` and `TC-3` pass.
- `AC-3` passes only if `TC-1` and `TC-4` pass.
- `AC-4` passes only if `TC-1` and `TC-5` pass.
- The handoff passes only if `AC-1` through `AC-4` pass and no test is blocked.
- Any additional copy/token change, behavior change, layout change, redesign, or outcome claim is a failure against `SCOPE-2` and the mapped rule(s).
- Missing evidence is not evidence of absence. Use `BLOCKED`, not `PASS`, when a required dependency or comparison is unavailable.

## Coverage and non-applicable paths

- Success: `AC-1` via `TC-2`.
- Non-regression: `AC-2` via `TC-3` for out-of-scope content and token identity; `AC-3` via `TC-4` for behavior; `AC-4` via `TC-5` for layout.
- Boundary: `AC-2` via `TC-3`, limiting the change to one authorized word.
- Error: not applicable; the supplied contract authorizes a static copy correction and specifies no error path. Missing dependencies are an execution gate, not invented product error behavior.
- Permission: not applicable; approval is a prerequisite embodied by `DEP-1`, and no runtime permission behavior was supplied.
- Recovery: not applicable; no recovery behavior was supplied for this static correction.

## Traceability matrix

| Test | Acceptance criterion | Requirement/rule/dependency/scope | Fact/source/authority |
|---|---|---|---|
| `TC-1` | Entry gate for `AC-1`, `AC-2` | `DEP-1`, `DEP-2`, `OPEN-1` | `FACT-3`, `SRC-1`, `AUTH-1` |
| `TC-2` | `AC-1` | `REQ-1`, `RULE-1`, `DEP-1`, `DEP-2`, `SCOPE-1` | `FACT-1`, `FACT-3`, `SRC-1`, `AUTH-1` |
| `TC-3` | `AC-2` | `REQ-1`, `DEP-2`, `SCOPE-2` | `FACT-1`, `FACT-3`, `SRC-1`, `AUTH-1` |
| `TC-4` | `AC-3` | `REQ-1`, `RULE-2`, `SCOPE-2` | `FACT-2`, `SRC-1`, `AUTH-1` |
| `TC-5` | `AC-4` | `REQ-1`, `RULE-3`, `SCOPE-2` | `FACT-2`, `SRC-1`, `AUTH-1` |

End-to-end preserved mapping: `SRC-1` → `FACT-1..3` → `REQ-1` / `RULE-1..4` / `DEP-1..2` / `SCOPE-1..2` → `AC-1..2`. `OPEN-1` remains unresolved until authoritative execution-time dependency data is supplied.

## QA report format

For each test, report: `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`; exact evidence inspected; mapped IDs; observed result; and finding text if applicable. Findings must describe the discrepancy only. QA must not edit the implementation, alter dependencies, infer missing values, recommend an unapproved product choice, or claim unsupported outcomes.
