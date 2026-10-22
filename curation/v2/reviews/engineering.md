# Capability Compiler V2 — Phase 1B Engineering Semantic Audit

## Scope and method

Assigned roots audited: 13/13. Every assigned `SKILL.md` was read completely. Directly relevant references, templates, examples, metadata, and scripts were then read and classified. No old dossier was used as proof. No files were edited; no commands, tests, network access, remote Git operations, or subagents were invoked.

The Phase 1 contract requires every `SKILL.md` to be `semantic-read`, support files to receive one of `semantic-read`, `behavior-reviewed`, or `excluded`, and each root dossier to capture triggers, responsibilities, I/O, workflow, dependencies, side effects, strengths, weaknesses, failure modes, and root relationships (`.specs/capability-compiler-v2/phase-1/phase-plan.md:29-52`). The coverage ledger presently describes 139 roots and 2,337 files, with review-required rather than completed statuses (`curation/v2/coverage.json:2-10`).

---

## 1. `code-review`

### Exact root / skill path

- Root: `skills/code-review/`
- Skill: `skills/code-review/SKILL.md`

### Trigger and non-trigger

- **Trigger:** A PR URL, pasted diff, file path, pre-merge review request, safety question, or concern about N+1 queries, injection, edge cases, or error handling (`skills/code-review/SKILL.md:1-5`).
- **Non-trigger:** Implementing the change, creating the implementation plan, debugging an unexplained failure before evidence collection, or requesting/orchestrating a reviewer subagent. Those belong respectively to implementation, `writing-plans`, `systematic-debugging`, and `requesting-code-review`.

### Responsibility and non-responsibility

- **Responsibility:** Review a supplied change across security, performance, correctness, and maintainability; produce actionable findings and a verdict (`skills/code-review/SKILL.md:12-13`, `skills/code-review/SKILL.md:40-77`).
- **Non-responsibility:** It does not define how to edit/fix code, enforce TDD, independently verify tests, manage review loops, or finish a branch.

### Inputs

- PR URL, diff, or file path.
- Optional context such as hot-path status, PII handling, named concerns, and tests (`skills/code-review/SKILL.md:15-22`, `skills/code-review/SKILL.md:108-112`).
- Optional source-control, project-tracker, and knowledge-base connectors (`skills/code-review/SKILL.md:25-37`, `skills/code-review/SKILL.md:94-105`).

### Outputs

- Markdown review with summary, critical-issue table, suggestion table, positive observations, and one of `Approve`, `Request Changes`, or `Needs Discussion` (`skills/code-review/SKILL.md:67-91`).

### Core workflow

1. Require a concrete review target; ask if absent.
2. Obtain supplied changes or fetch a PR through a connector.
3. Inspect security, performance, correctness, and maintainability dimensions.
4. Optionally check CI, tickets, and team standards.
5. Emit actionable findings and verdict.

### Branches

- Standalone mode accepts pasted/local material.
- Connector mode can fetch PR/CI data and related organizational context.
- User-provided focus can narrow the review (`skills/code-review/SKILL.md:25-37`, `skills/code-review/SKILL.md:94-112`).

### Rules, gates, and stop conditions

- No-target gate: ask what to review (`skills/code-review/SKILL.md:19-22`).
- No explicit evidence threshold, severity calibration rule, source-line requirement, or “no findings” convention is defined.
- No explicit stop condition for unreadable code, unavailable PRs, or failing connectors.

### Tools and dependencies

- Standalone file/diff access.
- Optional source-control, project-tracker, and knowledge-base connectors.
- The referenced `../../CONNECTORS.md` was not present in the repository root listing, so connector discovery depends on an unresolved external or missing document (`skills/code-review/SKILL.md:9`).

### Permissions and side effects

- Intended as read-only analysis.
- Connector mode may read PR, CI, ticket, and knowledge-base data.
- No code mutation, commit, push, or deployment is prescribed.

### Strongest unique methods

- Compact four-dimension review lens.
- Explicit standalone/connector capability split.
- Review output reserves space for positive evidence as well as defects.

### Weaknesses and failure modes

- The review dimensions are checklists, not an evidence discipline: the skill does not require reading the actual diff, tracing affected call sites, checking requirements, or reproducing suspected defects.
- Output has only “Critical Issues” and undifferentiated “Suggestions”; it lacks calibrated important/minor classes found in `requesting-code-review`.
- It says connectors can check CI but does not require fresh verification before approval.
- The unresolved `CONNECTORS.md` link may leave unfamiliar connector syntax unexplained.
- Generic OWASP/performance lists can induce speculative findings if not paired with proof.

### Overlap, duplicate, and dependency candidates

- **Complement:** `requesting-code-review` supplies orchestration and a stronger reviewer prompt; this root supplies a user-facing review capability.
- **Dependency candidate:** `verification-before-completion` should gate claims that CI/tests pass.
- **Overlap:** Maintainability and testing checks overlap with `testing-strategy`; root-cause questions overlap with `systematic-debugging`, but this root should report defects rather than diagnose by speculative repair.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/code-review/SKILL.md` | semantic-read | Complete governing skill text; defines triggers, review dimensions, connector branches, and output contract. |
| No other files in root | excluded | Root listing contains no references, templates, examples, scripts, or assets beyond `SKILL.md`. |

---

## 2. `codebase-design`

### Exact root / skill path

- Root: `skills/codebase-design/`
- Skill: `skills/codebase-design/SKILL.md`

### Trigger and non-trigger

- **Trigger:** Designing or improving a module interface, placing a seam, finding deepening opportunities, improving testability/AI navigability, or supplying shared architecture vocabulary to another skill (`skills/codebase-design/SKILL.md:1-4`).
- **Non-trigger:** Broad codebase scanning and report generation without a selected design question; that is `improve-codebase-architecture`. It is also not an implementation planner or refactoring executor.

### Responsibility and non-responsibility

- **Responsibility:** Define and consistently apply the deep-module vocabulary: module, interface, implementation, depth, seam, adapter, leverage, and locality; guide testable interface design (`skills/codebase-design/SKILL.md:8-33`, `skills/codebase-design/SKILL.md:69-112`).
- **Non-responsibility:** It does not inspect a repository, choose a concrete refactor, implement it, or validate runtime behavior.

### Inputs

- A module/interface design question.
- Callers and their required knowledge.
- Dependency types, existing adapters, invariants, ordering, error modes, configuration, and performance characteristics.
- For design-it-twice: code paths, coupling details, dependency category, project domain vocabulary, and seam contents (`skills/codebase-design/DESIGN-IT-TWICE.md:7-33`).

### Outputs

- Shared terminology and design assessment.
- Deepening recommendation based on dependency category.
- Optionally, three or more radically different interface proposals and a comparative recommendation (`skills/codebase-design/DESIGN-IT-TWICE.md:16-47`).

### Core workflow

1. Model the candidate as module/interface/implementation.
2. Assess interface depth and apply the deletion test.
3. Locate the seam; avoid hypothetical indirection.
4. Classify dependencies as in-process, local-substitutable, remote-owned, or true external.
5. Make the interface the test surface.
6. If alternatives are requested, frame constraints, generate contrasting interfaces, then compare depth, locality, and seam placement.

### Branches

- Dependency branch:
  - In-process: merge and test directly.
  - Local-substitutable: use a local stand-in.
  - Remote-owned: port plus production/test adapters.
  - True external: injected port with mock adapter (`skills/codebase-design/DEEPENING.md:7-30`).
- Design-it-twice branch only when alternative interfaces are wanted (`skills/codebase-design/DESIGN-IT-TWICE.md:1-5`).

### Rules, gates, and stop conditions

- Use glossary terms exactly; reject overloaded substitutes (`skills/codebase-design/SKILL.md:12-33`, `skills/codebase-design/SKILL.md:114-119`).
- One adapter means a hypothetical seam; two adapters justify a real seam (`skills/codebase-design/SKILL.md:72-76`, `skills/codebase-design/DEEPENING.md:32-36`).
- Test through the external interface and delete superseded shallow-module tests (`skills/codebase-design/DEEPENING.md:38-44`).
- No explicit stop condition for insufficient caller/dependency evidence.

### Tools and dependencies

- No runtime tool required for the core vocabulary.
- Design-it-twice explicitly depends on parallel subagents and project `CONTEXT.md` vocabulary (`skills/codebase-design/DESIGN-IT-TWICE.md:16-36`).
- OpenAI agent metadata exposes the skill under a concise display name.

### Permissions and side effects

- Core skill is advisory/read-only.
- Design-it-twice dispatches subagents but prescribes no repository mutations.
- Actual refactoring remains downstream.

### Strongest unique methods

- **Depth-as-leverage**, avoiding implementation-line-count proxies.
- **Deletion test** for shallow modules.
- **Interface is the test surface**.
- Dependency-category-specific seam and testing policy.
- **Replace, don’t layer** migration of tests.
- Deliberately divergent “design it twice” briefs.

### Weaknesses and failure modes

- “A Module has exactly one Interface” is intentionally simplifying but can obscure role-specific interfaces exposed to different caller classes (`skills/codebase-design/SKILL.md:105-112`).
- “Two adapters means a real seam” is useful anti-abstraction guidance, yet a single production adapter may still require a seam for ownership, policy, or external-system isolation; the text admits no conditional exception.
- Design-it-twice requires 3+ subagents and therefore is unavailable on runtimes without delegation.
- No measurement rubric translates “leverage” and “locality” into comparable evidence beyond expert judgment.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `improve-codebase-architecture` explicitly imports this vocabulary and principles.
- **Complement:** `testing-strategy` can determine tests once the external interface is chosen.
- **Conflict candidate:** `writing-plans` favors smaller focused files, while this root may recommend consolidating shallow modules. Resolve by distinguishing file size from interface depth.
- **Variant:** design-it-twice is an optional exploration mode, not a duplicate root.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/codebase-design/SKILL.md` | semantic-read | Complete vocabulary, principles, testability rules, and relationships. |
| `skills/codebase-design/DEEPENING.md` | semantic-read | Normative dependency taxonomy, seam discipline, and replace-don’t-layer test policy. |
| `skills/codebase-design/DESIGN-IT-TWICE.md` | semantic-read | Normative multi-design workflow and comparison criteria. |
| `skills/codebase-design/agents/openai.yaml` | semantic-read | Invocation/display metadata; no behavior beyond exposing the root (`skills/codebase-design/agents/openai.yaml:1-3`). |

---

## 3. `executing-plans`

### Exact root / skill path

- Root: `skills/executing-plans/`
- Skill: `skills/executing-plans/SKILL.md`

### Trigger and non-trigger

- **Trigger:** A written implementation plan is ready for execution in a separate session with checkpoints (`skills/executing-plans/SKILL.md:1-4`).
- **Non-trigger:** No written plan, tightly coupled work needing design, same-session independent tasks when subagents are available, or writing the plan itself.

### Responsibility and non-responsibility

- **Responsibility:** Critically review a plan, execute its tasks exactly, run specified verification, and hand off to branch finishing (`skills/executing-plans/SKILL.md:7-33`).
- **Non-responsibility:** It does not author the plan, define TDD details, review implementation quality itself, or choose merge/deployment outcomes.

### Inputs

- Written implementation plan.
- Workspace/branch context.
- Human clarification when the plan is ambiguous or blocked.

### Outputs

- Completed plan tasks with tracked status.
- Verification evidence prescribed by the plan.
- Handoff to `finishing-a-development-branch`.

### Core workflow

1. Read and critically review plan.
2. Raise concerns before starting.
3. Create task tracking.
4. For each task: mark in progress, follow steps, verify, mark complete.
5. Invoke branch-finishing workflow after all tasks verify.

### Branches

- If subagents are available, prefer `subagent-driven-development`.
- Concern branch asks the human before execution.
- Blocker branch stops immediately.
- Plan updates or fundamental rethink return to review (`skills/executing-plans/SKILL.md:11-20`, `skills/executing-plans/SKILL.md:35-53`).

### Rules, gates, and stop conditions

- Never start implementation on `main`/`master` without explicit consent.
- Do not skip plan-prescribed verification.
- Stop for missing dependencies, failing tests, unclear instructions, critical plan gaps, or repeated verification failure (`skills/executing-plans/SKILL.md:35-59`).

### Tools and dependencies

- Task tracking (`TodoWrite` in the source vocabulary).
- Plan-specified development/test tools.
- Required workflow skills: `using-git-worktrees`, `writing-plans`, `finishing-a-development-branch` (`skills/executing-plans/SKILL.md:61-66`).

### Permissions and side effects

- Broad repository mutation: code edits, tests, commits, and branch completion according to the plan.
- Worktree setup may create directories/branches.
- Final branch workflow may offer merge-related actions, but this skill itself does not choose them.

### Strongest unique methods

- Critical plan review before execution.
- Immediate stop rather than improvisation when blocked.
- Clear alternative to same-session subagent execution.

### Weaknesses and failure modes

- The description promises “review checkpoints,” but the core per-task process only marks state and runs specified verification; it does not itself require code review at checkpoints (`skills/executing-plans/SKILL.md:21-33`).
- “Follow each step exactly” can preserve defects in a stale or over-specified plan unless critical review detects them.
- No explicit independent final diff review appears before branch finishing.
- Depends on three other workflow skills; unavailable dependencies block completion.

### Overlap, duplicate, and dependency candidates

- **Conditional variant:** `subagent-driven-development` for same-session, mostly independent tasks with subagents.
- **Strong dependencies:** `writing-plans`, `using-git-worktrees`, `finishing-a-development-branch`.
- **Recommended complement:** `requesting-code-review` at natural checkpoints.
- **Cross-cutting gate:** `verification-before-completion`.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/executing-plans/SKILL.md` | semantic-read | Complete workflow; no support files or executable scripts exist in this root. |

---

## 4. `git-guardrails-claude-code`

### Exact root / skill path

- Root: `skills/git-guardrails-claude-code/`
- Skill: `skills/git-guardrails-claude-code/SKILL.md`

### Trigger and non-trigger

- **Trigger:** User asks to block destructive Git commands, prevent pushes/resets, or install Claude Code Git safety hooks (`skills/git-guardrails-claude-code/SKILL.md:1-4`).
- **Non-trigger:** General Git policy discussion, repository recovery after a destructive command, non-Claude-Code tooling, or authorization for Git operations.

### Responsibility and non-responsibility

- **Responsibility:** Install a Claude Code `PreToolUse` Bash hook that rejects named command patterns (`skills/git-guardrails-claude-code/SKILL.md:7-19`).
- **Non-responsibility:** It does not provide a complete shell parser, Git server-side enforcement, repository permissions, recovery, or protection outside Claude Code Bash tool invocations.

### Inputs

- Installation scope: project or global.
- Existing Claude settings file.
- Optional additions/removals to blocked patterns.

### Outputs

- Copied executable hook script.
- Merged `hooks.PreToolUse` settings entry.
- Verification result showing exit code 2 and a block message.

### Core workflow

1. Ask project/global scope.
2. Copy bundled script to corresponding hooks directory.
3. Make executable.
4. Merge hook into settings without overwriting existing settings.
5. Ask for customization.
6. Pipe sample JSON into hook and verify rejection.

### Branches

- Project path: `.claude/settings.json` and `$CLAUDE_PROJECT_DIR/.claude/hooks/...`.
- Global path: `~/.claude/settings.json` and `~/.claude/hooks/...`.
- Optional customized pattern set (`skills/git-guardrails-claude-code/SKILL.md:21-86`).

### Rules, gates, and stop conditions

- Must ask scope before mutation.
- Must merge rather than replace settings.
- Verification gate expects exit 2 and `BLOCKED` on stderr (`skills/git-guardrails-claude-code/SKILL.md:21-29`, `skills/git-guardrails-claude-code/SKILL.md:70-86`).

### Tools and dependencies

- Bash, `jq`, `grep`, `chmod`, file copy/edit tools, and Claude Code `PreToolUse`.
- The script reads all stdin, extracts `.tool_input.command` with `jq`, regex-matches patterns, and exits 2 on a match (`skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh:1-26`).

### Permissions and side effects

- Writes project or home-directory Claude settings and hooks.
- Changes executable permission.
- Does not execute Git itself during installation except the simulated echo test.

### Strongest unique methods

- Preventive pre-execution control rather than post-hoc warning.
- Project/global scope branch.
- Preserves existing settings through an explicit merge rule.
- Bundled behavior is short and inspectable.

### Weaknesses and failure modes

- Claim “`git push` all variants” exceeds implementation. The regex requires the literal substring `git push`; forms such as `git -C repo push`, shell variables, aliases, or an alternate Git binary path evade it (`skills/git-guardrails-claude-code/SKILL.md:10-18`; `skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh:6-17`).
- Regex scans the entire shell string without parsing command structure, so harmless text such as `echo "git push"` is also blocked.
- Block list is narrow: equivalent destructive forms such as `git switch` plus deletion, `git checkout -- <path>`, `git restore --source`, and `git clean -x` variants are not comprehensively modeled.
- Missing/invalid JSON or absent `jq` is not handled explicitly.
- Verification covers only one positive block case; no allowed-command or bypass regression checks are prescribed.
- Global command uses `~` inside a JSON command string; expansion behavior depends on the shell used by the hook runner.

### Overlap, duplicate, and dependency candidates

- **Complement:** `verification-before-completion` can ensure the installed hook actually blocks and permits intended commands.
- **Dependency candidate:** A generic settings-merge/install utility would reduce risk, but none is present in this root.
- No substantive duplicate among assigned roots.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/git-guardrails-claude-code/SKILL.md` | semantic-read | Installation and behavior contract. |
| `skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | behavior-reviewed | Executable enforcement logic; read completely and compared with claimed blocked variants. |
| `skills/git-guardrails-claude-code/agents/openai.yaml` | semantic-read | Invocation metadata only; names and describes the skill (`skills/git-guardrails-claude-code/agents/openai.yaml:1-3`). |

---

## 5. `improve-codebase-architecture`

### Exact root / skill path

- Root: `skills/improve-codebase-architecture/`
- Skill: `skills/improve-codebase-architecture/SKILL.md`

### Trigger and non-trigger

- **Trigger:** Explicit request to scan a codebase for architecture/deepening opportunities and present/refine candidates. Implicit model invocation is disabled (`skills/improve-codebase-architecture/SKILL.md:1-5`; `skills/improve-codebase-architecture/agents/openai.yaml:1-5`).
- **Non-trigger:** A single known interface design question, direct refactoring request, or routine code review.

### Responsibility and non-responsibility

- **Responsibility:** Scope a repository architecture scan, identify shallow modules and seam leakage, generate a visual candidate report, then facilitate selection and deeper design (`skills/improve-codebase-architecture/SKILL.md:8-39`, `skills/improve-codebase-architecture/SKILL.md:41-84`).
- **Non-responsibility:** It must not propose concrete interfaces in the initial report and does not implement the refactors (`skills/improve-codebase-architecture/SKILL.md:70-74`).

### Inputs

- Optional user-named subsystem or pain point.
- Otherwise commit history for hotspots.
- `CONTEXT.md`, relevant ADRs, repository code, tests, and coupling/dependency evidence.
- `codebase-design` vocabulary.

### Outputs

- Fresh temp-directory HTML report with candidate cards, before/after diagrams, recommendation strengths, and top recommendation.
- User-selected candidate enters a grilling/design loop.
- Potential updates to `CONTEXT.md` and optional ADR proposal after selection.

### Core workflow

1. Scope scan by user direction or commit-history hotspot.
2. Read domain glossary and relevant ADRs.
3. Delegate repository exploration.
4. Apply shallow-module questions and deletion test.
5. Generate/open visual report in OS temp directory.
6. Ask user to select a candidate.
7. Run grilling loop; update domain vocabulary as decisions crystallize.
8. Optionally use design-it-twice for interface alternatives.

### Branches

- Named scope bypasses commit-history inference.
- ADR-conflicting candidate appears only when friction justifies reopening.
- Rejected candidate may produce an ADR offer only for durable reasons.
- New/fuzzy domain terms update `CONTEXT.md`.
- Alternative-interface request delegates to `codebase-design` (`skills/improve-codebase-architecture/SKILL.md:17-39`, `skills/improve-codebase-architecture/SKILL.md:75-92`).

### Rules, gates, and stop conditions

- YAGNI scope before scanning.
- Use exact `codebase-design` vocabulary.
- Respect existing ADRs unless real friction warrants reconsideration.
- Do not propose interfaces before candidate selection.
- Initial stop point is the user’s candidate choice.

### Tools and dependencies

- Git history, repository reader, subagent support, Skill tool, temp-file writer, OS opener.
- `codebase-design`, `grilling`, and `domain-modeling`.
- Tailwind and Mermaid loaded from CDNs (`skills/improve-codebase-architecture/HTML-REPORT.md:1-30`).

### Permissions and side effects

- Reads Git history, source, tests, domain context, and ADRs.
- Writes an HTML file outside the repository and opens it.
- Later loop may create/update `CONTEXT.md`; may offer an ADR.
- CDN report entails network access when opened.

### Strongest unique methods

- Hotspot-first architecture scan.
- Organic “experienced friction” exploration rather than rigid metrics.
- Deletion-test candidate validation.
- Visual before/after architecture report.
- Clear separation between candidate discovery and interface design.
- Inline domain-language maintenance tied to concrete decisions.

### Weaknesses and failure modes

- Calls the report “self-contained,” yet requires Tailwind and Mermaid CDNs; offline rendering is not self-contained (`skills/improve-codebase-architecture/SKILL.md:41-48`; `skills/improve-codebase-architecture/HTML-REPORT.md:1-30`).
- Mandatory subagent exploration blocks environments without delegation.
- Commit frequency is only a proxy for architectural value; stable but critical areas can be missed.
- Opening generated HTML is an OS side effect and may fail in headless runtimes.
- The workflow can mutate `CONTEXT.md` during an exploratory conversation without a separate explicit write approval.
- No mechanical gate verifies that candidate evidence actually supports recommendation strength.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `codebase-design`.
- **Complement:** `writing-plans` should begin only after a candidate/interface is accepted.
- **Complement:** `testing-strategy` helps specify surviving tests for the deepened interface.
- **Conditional dependency:** `requesting-code-review` after implementation, not during candidate discovery.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/improve-codebase-architecture/SKILL.md` | semantic-read | Governing scan, report, and grilling workflow. |
| `skills/improve-codebase-architecture/HTML-REPORT.md` | semantic-read | Normative HTML scaffold, visual grammar, candidate-card schema, and vocabulary restrictions. |
| `skills/improve-codebase-architecture/agents/openai.yaml` | semantic-read | Invocation policy and display metadata; confirms implicit invocation is disabled. |

---

## 6. `requesting-code-review`

### Exact root / skill path

- Root: `skills/requesting-code-review/`
- Skill: `skills/requesting-code-review/SKILL.md`

### Trigger and non-trigger

- **Trigger:** After each delegated task, after a major feature, before merge, when stuck, before refactoring, or after a complex bug fix (`skills/requesting-code-review/SKILL.md:13-27`).
- **Non-trigger:** Performing a direct user-facing code review without orchestration, reviewing before any concrete work product exists, or replacing verification with reviewer testimony.

### Responsibility and non-responsibility

- **Responsibility:** Build a context-isolated reviewer request from implementation summary, requirements, and Git range; act on severity-calibrated feedback (`skills/requesting-code-review/SKILL.md:7-11`, `skills/requesting-code-review/SKILL.md:29-50`).
- **Non-responsibility:** It does not itself inspect code, implement fixes, or prove tests pass.

### Inputs

- Description of implementation.
- Full plan or requirements.
- Base and head SHAs.
- Actual code/diff available to the reviewer.

### Outputs

- Reviewer report with strengths, critical/important/minor issues, recommendations, and merge readiness.
- Fix or reasoned pushback loop.

### Core workflow

1. Resolve base/head SHAs.
2. Fill reviewer prompt template.
3. Dispatch fresh reviewer with explicit context.
4. Fix critical and important findings; optionally note minor ones.
5. Push back only with technical evidence.

### Branches

- Mandatory vs optional request timing.
- Valid finding gets fixed.
- Incorrect finding gets reasoned challenge and evidence.
- Workflow integration differs for subagent-driven, executing-plan, and ad hoc development (`skills/requesting-code-review/SKILL.md:71-89`).

### Rules, gates, and stop conditions

- Never skip review because work seems simple.
- Do not ignore critical issues or proceed with important issues open.
- Reviewer must inspect actual code and classify severity accurately (`skills/requesting-code-review/SKILL.md:91-105`; `skills/requesting-code-review/code-reviewer.md:24-98`).

### Tools and dependencies

- Git (`rev-parse`, `diff`).
- Subagent/Task tool.
- `code-reviewer.md` template.

### Permissions and side effects

- Reads Git history and diffs.
- Dispatches a subagent.
- Subsequent remediation changes code; reviewer itself should be read-only.
- Does not push or merge.

### Strongest unique methods

- Fresh context rather than inherited deliberation.
- Exact requirement/diff range packaging.
- Severity-calibrated reviewer contract.
- Explicit praise, file-line evidence, why-it-matters, fix guidance, and verdict (`skills/requesting-code-review/code-reviewer.md:49-98`).

### Weaknesses and failure modes

- SHA-range review excludes uncommitted working-tree changes unless separately provided.
- `HEAD~1` is offered as a default despite multi-commit tasks; selecting the wrong base can hide changes (`skills/requesting-code-review/SKILL.md:31-35`).
- The template asks whether all tests pass but does not itself require the reviewer to run a fresh verification command.
- Dependence on a subagent makes it unusable in runtimes without delegation.
- “Fix Important issues before proceeding” is strong, but no explicit re-review requirement appears in this root; `subagent-driven-development` supplies that loop.

### Overlap, duplicate, and dependency candidates

- **Overlap/complement:** `code-review` provides review subject matter; this root provides orchestration and a stronger prompt.
- **Strong dependency:** `subagent-driven-development` invokes this template for quality review.
- **Complement:** `verification-before-completion` independently validates reviewer/test claims.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/requesting-code-review/SKILL.md` | semantic-read | Trigger, request assembly, severity response, and workflow integration. |
| `skills/requesting-code-review/code-reviewer.md` | semantic-read | Reviewer prompt template and evidence/severity/output contract; not executable behavior. |

---

## 7. `subagent-driven-development`

### Exact root / skill path

- Root: `skills/subagent-driven-development/`
- Skill: `skills/subagent-driven-development/SKILL.md`

### Trigger and non-trigger

- **Trigger:** A written implementation plan has mostly independent tasks, work remains in the current session, and subagents are available (`skills/subagent-driven-development/SKILL.md:1-4`, `skills/subagent-driven-development/SKILL.md:17-37`).
- **Non-trigger:** No plan, tightly coupled tasks, separate-session execution, unavailable subagents, or read-only work.

### Responsibility and non-responsibility

- **Responsibility:** Coordinate one fresh implementer per task, then spec-compliance and code-quality reviews in order, with repair/re-review loops and final review (`skills/subagent-driven-development/SKILL.md:7-14`, `skills/subagent-driven-development/SKILL.md:48-88`).
- **Non-responsibility:** It does not author the plan, directly implement tasks, or replace branch finishing.

### Inputs

- Complete plan.
- Full task text extracted once by the controller.
- Scene-setting context, directory, requirements, and acceptance criteria.
- Model availability by capability/cost.

### Outputs

- Per-task commits and test results.
- Implementer status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
- Spec approval, then quality approval.
- Final whole-implementation review and branch-finishing handoff.

### Core workflow

1. Read plan once; extract all tasks and context.
2. Create task tracking.
3. Dispatch fresh implementer with full task text.
4. Answer pre-work or mid-work questions.
5. Implementer codes, tests, commits, self-reviews.
6. Dispatch independent spec reviewer.
7. Loop implementer fixes and spec re-review until compliant.
8. Dispatch quality reviewer only after spec approval.
9. Loop fixes and quality re-review until approved.
10. Mark task complete; repeat serially.
11. Final whole-change review.
12. Invoke branch finishing.

### Branches

- Model class varies by mechanical, integration, or architecture/review work (`skills/subagent-driven-development/SKILL.md:91-108`).
- Status handling varies for done, concerns, context, or blockage (`skills/subagent-driven-development/SKILL.md:109-133`).
- Same-session/independent branch chooses this root; separate session chooses `executing-plans`.

### Rules, gates, and stop conditions

- Do not pause between tasks except unresolved blocker, genuine ambiguity, or completion.
- Never implement on `main`/`master` without consent.
- Never dispatch implementation tasks in parallel.
- Spec review must pass before quality review.
- Every issue requires fix and re-review; self-review cannot replace independent review.
- Never make a subagent read the plan file; provide full task text (`skills/subagent-driven-development/SKILL.md:237-275`).

### Tools and dependencies

- Subagent/Task tool, task tracker, Git, test tools.
- Required: `using-git-worktrees`, `writing-plans`, `requesting-code-review`, `finishing-a-development-branch`.
- Implementers should use TDD (`skills/subagent-driven-development/SKILL.md:277-289`).

### Permissions and side effects

- Creates code, tests, commits, and potentially worktrees.
- Dispatches many subagents.
- Reads Git ranges and may modify files repeatedly through fix loops.
- Branch completion remains delegated.

### Strongest unique methods

- Fresh isolated context per task.
- Serial implementers to avoid edit conflicts.
- Strict two-stage review ordering.
- Explicit implementer status protocol and escalation ladder.
- Controller curates task context rather than outsourcing plan interpretation.
- Independent final whole-change review.

### Weaknesses and failure modes

- High invocation and review cost is intrinsic and acknowledged (`skills/subagent-driven-development/SKILL.md:228-235`).
- The same implementer is expected to fix reviewer findings, yet the red-flag section later says to dispatch a fix subagent if a subagent fails; distinction between review failure and task failure could be clearer (`skills/subagent-driven-development/SKILL.md:263-275`).
- Each implementer commits, making task rollback and history cleanup a downstream concern.
- Strict serial execution leaves safe independent parallelism unused by design.
- Controller-supplied context may omit relevant repository facts because implementers are discouraged from reading the plan and inherit no history.
- Quality depends on availability of three role-capable agents per task.

### Overlap, duplicate, and dependency candidates

- **Conditional variant:** `executing-plans`.
- **Strong dependencies:** `writing-plans`, `requesting-code-review`, `test-driven-development`, `verification-before-completion`, worktrees, and branch finishing.
- **Internal duplication:** Quality reviewer prompt delegates to `requesting-code-review/code-reviewer.md`, correctly reusing rather than copying that contract (`skills/subagent-driven-development/code-quality-reviewer-prompt.md:1-25`).

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/subagent-driven-development/SKILL.md` | semantic-read | Complete orchestration state machine, gates, status handling, and dependencies. |
| `skills/subagent-driven-development/implementer-prompt.md` | semantic-read | Normative implementer instructions, escalation states, self-review, and report schema. |
| `skills/subagent-driven-development/spec-reviewer-prompt.md` | semantic-read | Independent “do not trust report” compliance-review contract. |
| `skills/subagent-driven-development/code-quality-reviewer-prompt.md` | semantic-read | Quality-review adapter that reuses the requesting-code-review template after spec approval. |

---

## 8. `systematic-debugging`

### Exact root / skill path

- Root: `skills/systematic-debugging/`
- Skill: `skills/systematic-debugging/SKILL.md`

### Trigger and non-trigger

- **Trigger:** Any bug, test/build/integration failure, performance problem, or unexpected behavior, before proposing fixes (`skills/systematic-debugging/SKILL.md:1-4`, `skills/systematic-debugging/SKILL.md:21-41`).
- **Non-trigger:** Known implementation work with no failure, speculative refactoring, or test-plan design.

### Responsibility and non-responsibility

- **Responsibility:** Establish root cause before repair using four ordered phases: investigation, pattern analysis, hypothesis testing, and implementation (`skills/systematic-debugging/SKILL.md:8-18`, `skills/systematic-debugging/SKILL.md:43-190`).
- **Non-responsibility:** It does not replace full architecture design, general code review, or final completion verification.

### Inputs

- Exact errors, warnings, stack traces, reproduction steps, recent changes, environment/config, data flowing across system seams, working comparisons, and prior attempted fixes.

### Outputs

- Evidence-backed root-cause statement.
- One minimally tested hypothesis.
- Failing regression case.
- Single root-cause fix plus verification.
- Investigation record/monitoring if the root cause is genuinely external or timing-dependent.

### Core workflow

1. Read errors fully.
2. Reproduce or gather more evidence.
3. Inspect recent changes and environmental differences.
4. Instrument every relevant system seam.
5. Trace bad values backward to their origin.
6. Compare broken behavior with complete working references.
7. State one specific hypothesis.
8. Test one variable minimally.
9. Create failing regression case.
10. Apply one root-cause fix.
11. Verify symptom and wider tests.
12. After repeated failure, return to investigation or question architecture.

### Branches

- Multi-module systems require seam instrumentation.
- Deep-stack failures use backward root-cause tracing.
- Failed hypothesis yields a new hypothesis, not accumulated edits.
- Under three failed fixes returns to Phase 1; three or more requires architectural discussion.
- Genuine external/timing cause permits retry/timeout/error handling plus monitoring only after completed investigation (`skills/systematic-debugging/SKILL.md:63-113`, `skills/systematic-debugging/SKILL.md:139-190`, `skills/systematic-debugging/SKILL.md:258-268`).

### Rules, gates, and stop conditions

- No fix before Phase 1.
- Phases are ordered.
- One hypothesis and one variable at a time.
- Failing test before repair.
- No “while here” refactors.
- Stop after three failed fixes and discuss architecture.
- If not understood, say so and ask/research (`skills/systematic-debugging/SKILL.md:14-18`, `skills/systematic-debugging/SKILL.md:125-190`).

### Tools and dependencies

- Error logs, stack traces, Git diff/history, diagnostic instrumentation, test runner.
- `test-driven-development` and `verification-before-completion`.
- Optional `find-polluter.sh` for test pollution.
- TypeScript condition-wait helpers are example behavior, not a generic drop-in because they import Lace-specific types (`skills/systematic-debugging/condition-based-waiting-example.ts:1-18`).

### Permissions and side effects

- Investigation may add temporary logging/instrumentation.
- Implementation writes regression tests and code.
- `find-polluter.sh` runs test files sequentially.
- No deployment or remote action is prescribed.

### Strongest unique methods

- Root-cause iron law.
- Explicit seam-by-seam evidence capture.
- Backward value tracing.
- Single-hypothesis scientific loop.
- Three-failed-fixes architecture escalation.
- Condition-based waiting instead of arbitrary sleeps.
- Defense-in-depth guidance after source repair.

### Weaknesses and failure modes

- `defense-in-depth.md` says validate at “EVERY layer” and that all four layers are necessary; applied literally, this can duplicate validation and conflict with minimal-fix/YAGNI guidance (`skills/systematic-debugging/defense-in-depth.md:1-16`, `skills/systematic-debugging/defense-in-depth.md:94-108`).
- `find-polluter.sh` is described as bisection in prose, but behavior is a linear per-file scan (`skills/systematic-debugging/root-cause-tracing.md:72-80`; `skills/systematic-debugging/find-polluter.sh:20-62`).
- The pollution script does not clean between tests and skips remaining tests if pollution already exists, so it cannot reliably isolate multiple polluters (`skills/systematic-debugging/find-polluter.sh:29-38`).
- `condition-based-waiting-example.ts` is tied to project-specific `~/threads/...` imports, limiting reuse.
- Debug instrumentation can leak secrets if the advice to log environment/data at seams is followed without redaction.
- The process is intentionally strict; incidents requiring immediate rollback/traffic failover are not separately modeled from code-fix investigation.

### Overlap, duplicate, and dependency candidates

- **Strong dependency:** `test-driven-development` in Phase 4.
- **Strong complement:** `verification-before-completion`.
- **Architecture escalation:** after three failed fixes, hand off to `codebase-design` or `improve-codebase-architecture`.
- **Complement:** `code-review` can inspect the resulting fix, but should not replace diagnosis.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/systematic-debugging/SKILL.md` | semantic-read | Complete normative debugging process. |
| `skills/systematic-debugging/root-cause-tracing.md` | semantic-read | Normative backward-tracing and instrumentation technique. |
| `skills/systematic-debugging/defense-in-depth.md` | semantic-read | Normative post-root-cause multi-layer validation guidance. |
| `skills/systematic-debugging/condition-based-waiting.md` | semantic-read | Normative replacement for arbitrary async sleeps, including timeout rules. |
| `skills/systematic-debugging/condition-based-waiting-example.ts` | behavior-reviewed | Compilable-style polling helper behavior, timeouts, event matching, and project-specific imports inspected. |
| `skills/systematic-debugging/find-polluter.sh` | behavior-reviewed | Executable test runner/pollution detector; loop, exit behavior, and limitations inspected. |
| `skills/systematic-debugging/CREATION-LOG.md` | excluded | Provenance/process narrative about creating and pressure-testing the skill; not current runtime semantics. |
| `skills/systematic-debugging/test-academic.md` | excluded | Skill-validation question fixture, not user-facing debugging behavior. |
| `skills/systematic-debugging/test-pressure-*.md` | excluded | Three adversarial skill-compliance fixtures; useful test provenance, but not normative operational instructions. |

---

## 9. `test-case-generator`

### Exact root / skill path

- Root: `skills/test-case-generator/`
- Skill: `skills/test-case-generator/SKILL.md`

### Trigger and non-trigger

- **Trigger:** User supplies textual or `.txt`/`.docx`/`.pdf` requirements and asks for structured test cases, export, quality scoring, test data, review, or incremental updates (`skills/test-case-generator/SKILL.md:1-18`).
- **Non-trigger:** Writing automated executable tests directly, choosing repository-level test architecture, or enforcing TDD during implementation.

### Responsibility and non-responsibility

- **Responsibility:** Generate manual/structured test-case specifications; extract requirement text; export formats; score heuristic quality; generate data; detect similar cases; update priorities/stages; compare requirement revisions.
- **Non-responsibility:** It does not execute the product under test, prove requirement coverage semantically, generate runnable test code, or replace human review.

### Inputs

- Direct requirement prose or document path.
- Optional prompt profile and export format.
- Canonical script data shape is inconsistent:
  - exporter expects stdin JSON as nine-element row arrays;
  - scoring/review/data scripts expect object dictionaries.
- Optional old/new requirement files and testcase JSON.

### Outputs

- Test cases covering positive, negative, boundary, combination, E2E, and non-functional concerns.
- CSV, Markdown, JSON, XMind-compatible JSON, or TestLink XML.
- Quality report and exit status.
- Generated test data.
- Duplicate/statistics/filter/update results.
- `incremental_update_plan.md`.

### Core workflow

1. Check optional dependencies.
2. Extract or accept requirements.
3. Analyze features, rules, roles, inputs, boundaries, failures, and non-functional needs.
4. Generate atomic, independent, traceable, executable cases with priority and concrete data.
5. Score/review cases.
6. Export selected format.
7. When requirements change, compare lines and generate an update plan.

### Branches

- Basic vs advanced prompt.
- Direct text vs txt/docx/pdf extraction.
- Output format branch.
- Test-data heuristics branch by title/type: authentication, search, boundary, exception, performance, default.
- Review branch: stats, duplicates, update priority/stage, filters.
- Diff branch with or without testcase impact analysis.

### Rules, gates, and stop conditions

- Advanced prompt requires every template field, traceability, concrete steps/results/data, normal/abnormal/boundary coverage, and ambiguity disclosure (`skills/test-case-generator/references/advanced-prompt.md:12-58`, `skills/test-case-generator/references/advanced-prompt.md:91-145`).
- Default prompt requires at least 5/10/15 cases by simple/medium/complex feature, while config specifies a different minimum of three per feature (`skills/test-case-generator/references/default-prompt.md:51-64`; `skills/test-case-generator/config.json:1-18`).
- Quality script exits nonzero below aggregate 60.
- No explicit stop on ambiguous requirements; advanced prompt instead permits assumptions and multiple interpretations.

### Tools and dependencies

- Python 3.7+ claimed.
- Stdlib: `json`, `csv`, `difflib`, `random`, `string`, `subprocess`, filesystem.
- Optional `python-docx`, `pdfplumber`; `openpyxl` is checked despite no Excel exporter in the reviewed scripts (`skills/test-case-generator/scripts/check_dependencies.py:23-46`).
- Shell required by `run_all_tests.py`.

### Permissions and side effects

- Reads requirement and testcase files.
- Writes exports, generated data, updated testcase files, `incremental_update_plan.md`, and user config under `~/.openclaw/skills/test-case-generator/config.json`.
- `config_manager.py update-priority/update-stage` paths overwrite the input testcase file through the review script.
- Dependency guidance asks users to run `pip install`; the checker itself does not install.

### Strongest unique methods

- Broad test-design prompt with boundary values, equivalence classes, combinations, E2E, external dependency failures, and non-functional dimensions.
- Multiple management/export utilities.
- Requirement-diff impact hypothesis.
- Test-data generation includes security-adversarial strings.
- Quality scoring exposes several maintainability dimensions, albeit heuristically.

### Weaknesses and failure modes

- **Data-model incompatibility:** `export_testcases.py` consumes nine-position arrays and emits object JSON, while `quality_score.py`, `review_testcases.py`, and `generate_testdata.py` consume objects. Re-exporting emitted JSON through the same exporter will index dictionaries numerically and fail (`skills/test-case-generator/scripts/export_testcases.py:11-45`, `skills/test-case-generator/scripts/export_testcases.py:48-66`; `skills/test-case-generator/scripts/quality_score.py:134-156`).
- **Requirements argument bug:** `quality_score.py` documents one optional requirements file but reads it only when `len(sys.argv) > 3`; a normal two-file invocation has length 3, so requirements are silently ignored (`skills/test-case-generator/scripts/quality_score.py:127-131`, `skills/test-case-generator/scripts/quality_score.py:158-162`).
- **False coverage score:** with no loaded requirements, coverage is automatically 100, so the argument bug inflates aggregate quality.
- **Export safety:** Markdown cells are not escaped; TestLink XML attributes interpolate `tc_id` and title without XML escaping, and arbitrary `]]>` can break CDATA (`skills/test-case-generator/scripts/export_testcases.py:39-45`, `skills/test-case-generator/scripts/export_testcases.py:125-143`).
- `.doc` is accepted but handed to `python-docx`, which generally supports `.docx`, not legacy binary `.doc` (`skills/test-case-generator/scripts/extract_requirements.py:45-59`).
- Repository `config.json` defaults to `advanced-prompt`, whereas `config_manager.py`’s user default is `default-prompt`; runtime location and effective precedence are unexplained (`skills/test-case-generator/config.json:1-3`; `skills/test-case-generator/scripts/config_manager.py:10-14`).
- `diff_requirements.py` imports `difflib` but compares exact line sets, ignores bullet lines, and matches testcases using only ten-character substrings. Rewording appears as delete/add rather than semantic change (`skills/test-case-generator/scripts/diff_requirements.py:7-35`, `skills/test-case-generator/scripts/diff_requirements.py:37-72`).
- Test-data generation is random and unseeded, reducing reproducibility.
- XMind export is merely “compatible JSON,” not an `.xmind` package.
- `run_all_tests.py` masks quality-score failure with `|| echo '跳过'`, uses `/dev/stdin`, exercises only three shallow paths, and therefore cannot validate Windows compatibility or core export/diff/review behavior (`skills/test-case-generator/scripts/run_all_tests.py:39-71`).
- `_meta.json` identifies upstream version `1.0.1`, while `SKILL.md` claims version 2.0; provenance/version semantics conflict (`skills/test-case-generator/_meta.json:1-11`; `skills/test-case-generator/SKILL.md:280-283`).

### Overlap, duplicate, and dependency candidates

- **Complement:** `testing-strategy` selects architecture and priorities; this root materializes detailed cases and data.
- **Distinct from:** `test-driven-development`, which governs implementation order and runnable tests.
- **Potential dependency:** generated cases should feed `writing-plans` only after schema normalization and human requirement review.
- **Potential duplicate:** Prompt templates repeat parts of default/advanced prompts and could become named variants behind one canonical schema.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/test-case-generator/SKILL.md` | semantic-read | Complete user workflow, claimed features, formats, and file inventory. |
| `skills/test-case-generator/config.json` | semantic-read | Effective configuration vocabulary, defaults, field schema, thresholds, and formats. |
| `skills/test-case-generator/references/default-prompt.md` | semantic-read | Normative basic generation rules and output template. |
| `skills/test-case-generator/references/advanced-prompt.md` | semantic-read | Normative comprehensive coverage, ambiguity, data, and non-functional rules. |
| `skills/test-case-generator/references/prompt-templates.md` | semantic-read | Eight concrete generation variants: functional, suite, agile, API, UI, performance, BDD, JSON. |
| `skills/test-case-generator/references/format-examples.md` | semantic-read | Semantic examples and claimed output-format contracts. |
| `skills/test-case-generator/scripts/check_dependencies.py` | behavior-reviewed | Imports optional packages, reports install guidance, and returns status. |
| `skills/test-case-generator/scripts/config_manager.py` | behavior-reviewed | Reads/writes user-level config, performs simple type coercion, and resets defaults. |
| `skills/test-case-generator/scripts/diff_requirements.py` | behavior-reviewed | Exact-line requirement comparison, heuristic impact matching, and update-plan write behavior. |
| `skills/test-case-generator/scripts/export_testcases.py` | behavior-reviewed | All five serializers and positional input schema inspected. |
| `skills/test-case-generator/scripts/extract_requirements.py` | behavior-reviewed | File-type dispatch, optional parsers, and error-as-text behavior inspected. |
| `skills/test-case-generator/scripts/generate_testdata.py` | behavior-reviewed | Heuristic data generation, random behavior, and JSON/CSV writes inspected. |
| `skills/test-case-generator/scripts/quality_score.py` | behavior-reviewed | Five scoring formulas, optional-argument bug, grade, and exit condition inspected. |
| `skills/test-case-generator/scripts/review_testcases.py` | behavior-reviewed | Duplicate scan, mutation commands, filters, statistics, and overwrite behavior inspected. |
| `skills/test-case-generator/scripts/run_all_tests.py` | behavior-reviewed | Shell-based smoke runner and failure-masking behavior inspected. |
| `skills/test-case-generator/_meta.json` | excluded | Upstream ownership/version provenance; not runtime or generation semantics, though version conflict is noted. |

---

## 10. `test-driven-development`

### Exact root / skill path

- Root: `skills/test-driven-development/`
- Skill: `skills/test-driven-development/SKILL.md`

### Trigger and non-trigger

- **Trigger:** Before implementing any feature, bug fix, refactor, or behavior change (`skills/test-driven-development/SKILL.md:1-4`, `skills/test-driven-development/SKILL.md:14-29`).
- **Non-trigger:** Pure requirements analysis, test-plan design without implementation, or exceptions explicitly approved for throwaway prototypes, generated code, and configuration.

### Responsibility and non-responsibility

- **Responsibility:** Enforce red-green-refactor with observed failure, minimum passing implementation, clean refactor, and real-behavior tests (`skills/test-driven-development/SKILL.md:8-12`, `skills/test-driven-development/SKILL.md:39-157`).
- **Non-responsibility:** It does not diagnose root cause before a bug fix, select overall test architecture, perform final deployment verification, or generate manual test cases.

### Inputs

- One desired behavior or reproduced bug.
- Existing test framework and code interface.
- Expected outcome and edge/error conditions.
- Human approval for an exception.

### Outputs

- Minimal failing test.
- Observed expected failure.
- Minimal production change.
- Passing focused and wider test runs.
- Refactored code with tests remaining green.

### Core workflow

1. Write one clear test against real behavior.
2. Run and confirm expected failure rather than test error.
3. Write minimum production code.
4. Run focused and full relevant tests.
5. Refactor only while green.
6. Repeat per behavior.

### Branches

- Passing red test means test existing behavior; revise it.
- Erroring red test means repair the test until it fails correctly.
- Failed green run means fix production code, not expectation.
- Hard-to-test code signals interface simplification/dependency injection.
- Mock/test-utility work loads anti-pattern guidance.

### Rules, gates, and stop conditions

- No production code before a failing test.
- Existing pre-test code must be deleted and reimplemented from tests.
- Tests target one behavior with clear names and real code.
- Mocks only when unavoidable.
- No behavior expansion in green/refactor.
- Completion checklist must be fully satisfied (`skills/test-driven-development/SKILL.md:31-37`, `skills/test-driven-development/SKILL.md:76-157`, `skills/test-driven-development/SKILL.md:284-327`).

### Tools and dependencies

- Project test runner.
- Optional mocks and dependency injection.
- `testing-anti-patterns.md`.
- For bugs, depends on `systematic-debugging` to establish cause before repair.

### Permissions and side effects

- Writes tests and production code.
- Runs focused and wider tests.
- May delete production code written before its test.
- No commit/push/deploy behavior prescribed.

### Strongest unique methods

- Observed-red proof that a test can detect missing behavior.
- Minimal green implementation.
- Clear distinction between test failure and test error.
- Strong resistance to sunk-cost and tests-after rationalizations.
- Explicit mock and test-only-production-method anti-patterns.

### Weaknesses and failure modes

- Universal “delete code written first” rule can cause disproportionate rework for inherited or exploratory code, though throwaway exploration is permitted only if discarded (`skills/test-driven-development/SKILL.md:31-37`, `skills/test-driven-development/SKILL.md:198-244`).
- “Every new function/method has a test” encourages implementation-shaped coverage, while the same root says to test behavior and `codebase-design` says the interface is the test surface (`skills/test-driven-development/SKILL.md:284-295`).
- No explicit guidance for characterization tests around legacy behavior before refactoring.
- The mock-completeness law can be expensive and brittle for large external schemas (`skills/test-driven-development/testing-anti-patterns.md:126-174`).
- Full-suite verification scope is unspecified for very large repositories.

### Overlap, duplicate, and dependency candidates

- **Strong dependency from:** `systematic-debugging` Phase 4, `writing-plans`, and implementers in `subagent-driven-development`.
- **Complement:** `testing-strategy` determines which test levels are appropriate.
- **Strong complement:** `verification-before-completion` supplies the final evidence gate.
- **Potential conflict:** Per-function checklist versus interface-level behavior testing should be resolved in favor of observable behavior at meaningful seams.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/test-driven-development/SKILL.md` | semantic-read | Complete TDD lifecycle, gates, examples, rationalization defenses, and checklist. |
| `skills/test-driven-development/testing-anti-patterns.md` | semantic-read | Normative mock/test-utility rules and gate functions; not executable behavior. |

---

## 11. `testing-strategy`

### Exact root / skill path

- Root: `skills/testing-strategy/`
- Skill: `skills/testing-strategy/SKILL.md`

### Trigger and non-trigger

- **Trigger:** “How should we test,” test strategy/plan requests, coverage questions, test architecture, or requests for example cases (`skills/testing-strategy/SKILL.md:1-4`).
- **Non-trigger:** Generating a full managed testcase corpus, implementing tests under TDD, debugging a failure, or verifying completion.

### Responsibility and non-responsibility

- **Responsibility:** Select a balanced test mix by system type and identify coverage gaps.
- **Non-responsibility:** It does not inspect an existing suite by prescribed method, write executable tests, define environments/data ownership, or execute verification.

### Inputs

- Target architecture/component type.
- Business-critical paths, error conditions, security seams, data-integrity risks, and existing coverage.
- Implicit constraints of speed and maintenance.

### Outputs

- Test plan stating what to test, test level, coverage targets, example cases, and current gaps (`skills/testing-strategy/SKILL.md:29-31`).

### Core workflow

1. Apply unit/integration/E2E pyramid.
2. Select patterns by API, pipeline, frontend, or infrastructure.
3. Prioritize critical paths, errors, edges, security, and integrity.
4. Skip trivial/framework/one-off implementation.
5. Produce plan and identify gaps.

### Branches

- API: business unit, HTTP integration, consumer contract.
- Pipeline: input, transformation, idempotency.
- Frontend: component, interaction, visual regression, accessibility.
- Infrastructure: smoke, chaos, load (`skills/testing-strategy/SKILL.md:15-24`).

### Rules, gates, and stop conditions

- Optimize coverage, speed, and maintenance.
- Skip trivial getters/setters, framework code, and one-off scripts (`skills/testing-strategy/SKILL.md:8-9`, `skills/testing-strategy/SKILL.md:25-27`).
- No explicit readiness gate, stop condition, or risk threshold.

### Tools and dependencies

- None named.
- Actual strategy may require framework-specific test runners, contract tooling, browsers, accessibility tools, load generators, or infrastructure harnesses, but the skill does not select them.

### Permissions and side effects

- Advisory/read-only unless the user separately asks to write tests.
- No files, commands, network, or subagents prescribed.

### Strongest unique methods

- Concise component-type matrix.
- Explicit coverage/speed/maintenance balance.
- Inclusion of contract, idempotency, accessibility, chaos, and load testing.

### Weaknesses and failure modes

- Too terse to guarantee a buildable strategy: no required inputs for risk, environment, fixtures, ownership, observability, flake control, or release gates.
- Testing pyramid is presented as universal despite event-driven, data-heavy, and UI-heavy systems often needing different shapes.
- “Skip one-off scripts” can miss high-risk migration/deployment scripts.
- Coverage targets are required in output but no method defines whether targets are behavior, risk, branch, mutation, or line based.
- No distinction between pre-merge, post-deploy, and production verification.

### Overlap, duplicate, and dependency candidates

- **Complement:** `test-case-generator` expands the strategy into detailed case artifacts.
- **Complement:** `test-driven-development` implements selected cases.
- **Dependency candidate:** `codebase-design` identifies testable seams.
- **Complement:** `verification-before-completion` turns strategy checks into release evidence.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/testing-strategy/SKILL.md` | semantic-read | Entire root; defines all strategy semantics and contains no support files. |

---

## 12. `verification-before-completion`

### Exact root / skill path

- Root: `skills/verification-before-completion/`
- Skill: `skills/verification-before-completion/SKILL.md`

### Trigger and non-trigger

- **Trigger:** Immediately before any claim that work is complete, fixed, clean, passing, ready, or suitable for commit/PR; also before moving to the next task or trusting delegated work (`skills/verification-before-completion/SKILL.md:1-4`, `skills/verification-before-completion/SKILL.md:104-119`).
- **Non-trigger:** Initial diagnosis, planning, implementation, or general test strategy.

### Responsibility and non-responsibility

- **Responsibility:** Tie every status claim to fresh, full, directly relevant verification output.
- **Non-responsibility:** It does not choose implementation, fix failures, define the entire test suite, or approve product requirements by inference.

### Inputs

- Proposed claim.
- Command that directly proves it.
- Full current output, exit code, failure count.
- Requirement checklist where the claim is requirements completion.

### Outputs

- Evidence-backed success claim, or accurate failure/status statement with evidence.

### Core workflow

1. Identify proof command.
2. Run full command fresh.
3. Read complete output and exit status.
4. Compare evidence to claim.
5. Claim only what evidence establishes.

### Branches

- Evidence confirms claim: state claim with evidence.
- Evidence contradicts claim: state actual status.
- Claim type selects proof: tests, lint, build, original symptom, red-green regression, diff plus verification, or requirement checklist (`skills/verification-before-completion/SKILL.md:21-50`).

### Rules, gates, and stop conditions

- No completion claim without fresh evidence.
- Partial checks and previous runs are insufficient.
- Agent reports require independent diff and verification.
- Requirements completion requires line-by-line checklist, not merely tests.
- Commit/PR/task transition is gated (`skills/verification-before-completion/SKILL.md:13-31`, `skills/verification-before-completion/SKILL.md:33-50`, `skills/verification-before-completion/SKILL.md:74-101`).

### Tools and dependencies

- Claim-specific test, build, lint, symptom, VCS, and checklist tools.
- No single framework dependency.

### Permissions and side effects

- Runs verification commands and reads output.
- May inspect VCS diff.
- Does not authorize commit, push, PR, merge, or deploy by itself.

### Strongest unique methods

- Claim-to-proof mapping.
- Freshness requirement.
- Full-output and exit-code requirement.
- Explicit delegation distrust.
- Requirements checklist separated from test success.
- Red-green regression verification by temporarily reverting/restoring the fix (`skills/verification-before-completion/SKILL.md:74-88`).

### Weaknesses and failure modes

- “In this message” freshness language couples semantics to a chat turn rather than an evidence timestamp/session and may force unnecessary reruns during long but unchanged verification discussions (`skills/verification-before-completion/SKILL.md:17-18`).
- No guidance for flaky/non-deterministic checks beyond refusing unsupported claims.
- No provenance format records command, cwd, revision, environment, and timestamp.
- Full-suite commands may be impractical; the skill offers no risk-based fallback other than not claiming success.
- Temporary fix reversion for red-green proof can be unsafe in a dirty working tree unless isolated.

### Overlap, duplicate, and dependency candidates

- **Cross-cutting dependency:** All execution, review, TDD, debugging, and plan workflows should use this before success claims.
- **Complement:** `requesting-code-review` validates quality, while this root validates factual state.
- **Not duplicate:** TDD verifies behavior during construction; this root verifies claims at handoff.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/verification-before-completion/SKILL.md` | semantic-read | Entire root and complete evidence-gate contract; no support files. |

---

## 13. `writing-plans`

### Exact root / skill path

- Root: `skills/writing-plans/`
- Skill: `skills/writing-plans/SKILL.md`

### Trigger and non-trigger

- **Trigger:** A specification or requirements set exists for a multi-step task, before code changes begin (`skills/writing-plans/SKILL.md:1-4`).
- **Non-trigger:** Requirements are unresolved, work is truly one trivial action, implementation has already begun without agreement, or architecture spans independent subsystems that should first be split.

### Responsibility and non-responsibility

- **Responsibility:** Produce a self-contained, implementation-ready, TDD-oriented plan with exact files, code, commands, expected outputs, and frequent commits (`skills/writing-plans/SKILL.md:7-17`, `skills/writing-plans/SKILL.md:38-103`).
- **Non-responsibility:** It does not execute the plan, resolve missing product requirements by invention, or finish the branch.

### Inputs

- Specification/requirements.
- Repository architecture and established patterns.
- Existing files and exact line regions.
- Tech stack and desired plan destination.

### Outputs

- `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` unless overridden.
- Mandatory goal/architecture/stack header.
- File map.
- Bite-sized checkbox tasks with failing tests, commands, minimum code, passing tests, and commits.
- Self-review results and execution-choice handoff.

### Core workflow

1. Announce plan creation.
2. Check whether scope should be split by independent subsystem.
3. Map files and responsibilities before tasks.
4. Decompose into self-contained tasks.
5. Write 2–5 minute action steps with exact code and expected command output.
6. Eliminate placeholders.
7. Self-review spec coverage, placeholders, and type/name consistency.
8. Save plan.
9. Offer subagent-driven or inline execution.

### Branches

- User path preference overrides default.
- Multi-subsystem spec should split into separate plans.
- Existing repository structure takes precedence over unilateral restructuring.
- Execution branch chooses `subagent-driven-development` or `executing-plans` (`skills/writing-plans/SKILL.md:14-26`, `skills/writing-plans/SKILL.md:134-153`).

### Rules, gates, and stop conditions

- Exact file paths and line ranges.
- Complete code for every code-changing step.
- Exact commands and expected output.
- No TODO/TBD, vague validation, “similar to,” or undefined symbols.
- DRY, YAGNI, TDD, frequent commits.
- Self-review must cover spec, placeholders, and type consistency (`skills/writing-plans/SKILL.md:87-132`).

### Tools and dependencies

- Repository readers/search.
- Plan file writer.
- `subagent-driven-development` or `executing-plans` for handoff.
- Worktrees expected at execution time, not necessarily plan-writing time.

### Permissions and side effects

- Writes plan document only.
- Does not alter production code.
- Handoff may initiate implementation only after user choice.

### Strongest unique methods

- File-responsibility map before task decomposition.
- One-action steps with explicit red/green evidence.
- No-placeholder rule.
- Internal spec-coverage and type-consistency review.
- Explicit handoff contract for two execution modes.

### Weaknesses and failure modes

- Requiring complete implementation code inside every plan can duplicate the implementation, make plans stale quickly, and consume more effort than the actual change.
- Universal 2–5 minute granularity can create excessive ceremony and obscure the larger dependency structure.
- Mandatory frequent commits are unsuitable for some repository policies or non-Git environments.
- The plan embeds expected failure strings that may vary by tool/version.
- The included `plan-document-reviewer-prompt.md` describes a post-plan subagent review, while the skill’s current self-review explicitly says not to dispatch a subagent; the support template is therefore dormant or conflicting (`skills/writing-plans/SKILL.md:113-132`; `skills/writing-plans/plan-document-reviewer-prompt.md:1-38`).
- Assumption that engineers need complete repeated code conflicts with DRY at the document level.

### Overlap, duplicate, and dependency candidates

- **Strong downstream variants:** `subagent-driven-development` and `executing-plans`.
- **Strong dependency:** `test-driven-development` shapes every implementation task.
- **Complement:** `codebase-design` should settle seams/interfaces before detailed file planning.
- **Complement:** `testing-strategy` should settle test levels for broad changes.
- **Dormant duplicate:** plan reviewer template overlaps the built-in self-review; choose one authoritative gate.

### Support-file review

| Path or bounded glob | Disposition | Concrete reason |
|---|---|---|
| `skills/writing-plans/SKILL.md` | semantic-read | Complete plan schema, granularity, gates, self-review, and handoff. |
| `skills/writing-plans/plan-document-reviewer-prompt.md` | semantic-read | Semantic reviewer template; classified despite conflict with current “self-review, not subagent” instruction. |

---

# Cross-root semantic relationship hypotheses

## Duplicate hypotheses

1. **`code-review` and `requesting-code-review` partially duplicate review criteria.**
   - `code-review` is the direct capability: security/performance/correctness/maintainability and verdict.
   - `requesting-code-review` is orchestration plus a richer reviewer prompt.
   - **Fusion hypothesis:** retain one canonical review rubric; expose direct-review and delegated-review invocation variants.

2. **`writing-plans` self-review and `plan-document-reviewer-prompt.md` duplicate plan validation.**
   - They conflict on whether review is local/self or delegated.
   - **Decision hypothesis:** canonical rule should require the same checks; delegation remains an optional runtime adapter.

3. **`test-case-generator` prompt files overlap heavily.**
   - Default, advanced, and prompt-template variants repeat fields, priorities, and coverage dimensions.
   - **Fusion hypothesis:** one canonical testcase schema plus named depth/format variants.

## Complement hypotheses

1. **Architecture chain:** `improve-codebase-architecture` discovers candidates; `codebase-design` chooses seam/interface; `testing-strategy` chooses test levels; `writing-plans` converts the accepted design into tasks.
2. **Implementation chain:** `writing-plans` feeds either `subagent-driven-development` or `executing-plans`; both depend on TDD and completion verification.
3. **Bug-fix chain:** `systematic-debugging` establishes cause; `test-driven-development` creates the regression proof and fix; `requesting-code-review` evaluates it; `verification-before-completion` gates the final claim.
4. **Testing chain:** `testing-strategy` defines risk and architecture; `test-case-generator` creates detailed case artifacts/data; TDD creates runnable implementation tests.
5. **Review chain:** `requesting-code-review` packages context and dispatches; `code-review` supplies the semantic rubric; `verification-before-completion` checks factual claims independently.

## Conflict hypotheses

1. **Per-function tests versus interface test surface.**
   - `test-driven-development` asks for every new function/method to have a test.
   - `codebase-design` says tests should cross the module interface and not test past it.
   - **Recommended ruling:** observable behavior at a deliberate interface is authoritative; private helper coverage need not be one-test-per-method.

2. **Small files versus deep modules.**
   - `writing-plans` favors small focused files.
   - `codebase-design` favors deep modules and deletion of shallow pass-throughs.
   - **Recommended ruling:** file size is secondary; avoid public shallow modules even when implementation remains split internally.

3. **Minimal single fix versus validation at every layer.**
   - `systematic-debugging/SKILL.md` demands one root-cause fix with no bundled refactor.
   - `defense-in-depth.md` demands validation at every layer.
   - **Recommended ruling:** repair source first; add only independently justified trust-boundary or destructive-operation guards.

4. **Self-contained HTML versus CDN dependencies.**
   - `improve-codebase-architecture` calls its report self-contained while requiring Tailwind/Mermaid CDNs.
   - **Recommended ruling:** rename to single-file report with network dependencies, or inline required assets.

5. **Testcase minimums conflict.**
   - Default prompt says 5/10/15 cases by complexity.
   - Config and advanced practices use at least 3 per feature.
   - **Recommended ruling:** make risk/complexity policy explicit and single-sourced.

## Conditional variants

1. `subagent-driven-development` and `executing-plans` are conditional execution variants:
   - same session + independent tasks + subagents: subagent-driven;
   - separate session or no subagent path: executing-plans.
2. `code-review` has standalone and connector-enhanced variants.
3. `codebase-design` has core vocabulary, dependency-aware deepening, and design-it-twice variants.
4. `test-case-generator` has prompt-depth, input-document, and export-format variants.
5. `testing-strategy` branches by system type rather than representing separate capabilities.

## Strong dependency hypotheses

| Root | Strong dependency candidates |
|---|---|
| `improve-codebase-architecture` | `codebase-design`, domain-modeling, grilling, repository history |
| `writing-plans` | settled requirements/design, `test-driven-development` |
| `executing-plans` | `writing-plans`, worktrees, branch finishing, completion verification |
| `subagent-driven-development` | `writing-plans`, worktrees, TDD, requesting-code-review, branch finishing |
| `requesting-code-review` | Git range, reviewer rubric, completion verification |
| `systematic-debugging` | TDD for repair, completion verification, architecture review after repeated failed fixes |
| `test-case-generator` | normalized testcase schema, requirement source, optional document parsers |
| `git-guardrails-claude-code` | Bash, `jq`, Claude Code hook semantics, safe settings merge |

---

# Unresolved questions

1. Is `CONNECTORS.md` intentionally external to this repository, or is `skills/code-review/SKILL.md` carrying a broken relative link?
2. Should Capability Compiler preserve `code-review` and `requesting-code-review` as separate user-facing capabilities, or compile them as direct/delegated adapters over one review unit?
3. Which plan-review policy is authoritative: `writing-plans` self-review only, or the bundled plan-reviewer subagent template?
4. Should `executing-plans` require an explicit code-review checkpoint, given its description promises review checkpoints but its core loop does not?
5. Is the Git guardrail intended as best-effort pattern blocking or as a security boundary? The present regex behavior supports only the former.
6. Is architecture-report offline operation required? If yes, CDN-based Tailwind/Mermaid violates the desired artifact contract.
7. Which testcase representation is canonical: nine-position arrays or named objects? The scripts cannot form a reliable pipeline until this is settled.
8. Should legacy `.doc` input remain claimed when the implementation uses `python-docx`?
9. Which `test-case-generator` version is authoritative: upstream metadata `1.0.1` or skill text `2.0`?
10. Should generated XMind output be advertised as importable JSON rather than a native XMind file?
11. Should TDD’s “every function/method has a test” be superseded by codebase-design’s interface-level testing rule?
12. During production incidents, does `systematic-debugging` permit immediate rollback/failover before root-cause investigation, while still forbidding speculative code fixes?
13. Should verification evidence record revision, working directory, environment, command, timestamp, and exit code so “fresh” is durable beyond one chat message?
14. Should generated/vendor/test fixtures receive a dedicated disposition code distinct from generic `excluded` in the V2 ledger? The Phase 1 contract currently exposes only the three high-level dispositions.
15. No assigned root was nested beneath another assigned root. Thus no parent summary was used to cover a nested skill; if ownership in `coverage.json` assigns shared support files across roots, the compiler still needs an explicit many-root-to-one-file evidence model as anticipated by the Phase 1 plan (`.specs/capability-compiler-v2/phase-1/phase-plan.md:75-79`).