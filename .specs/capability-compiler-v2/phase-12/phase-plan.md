# Capability Compiler V2 — Phase 12 Final Approval and Controlled Local Release Plan

## Objective

Present the complete V2 evidence and residual-risk packet to the user. Only after an explicit final approval may the parent workflow perform a controlled **local repository release** of the accepted V2 candidates. Final approval does not authorize commit, push, pull request, merge, deployment, provider mutation, cloud change, browser login, credential action, production data access, or production release.

## Frozen Approval Inputs

- Phase 9 evidence tree: `7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152`
- Phase 10 evidence tree: `7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56`
- Phase 11 evidence tree: `275a2139cf207ac50105d3e65fd2138b371a3e2dbe0dce4b05ab043cb1cd5fbc`
- Accepted candidate: Revision 4, `0.1.4-v2-candidate`, still `evaluating` and unreleased.
- Atomic candidates: 157 across Phase 3–7; Phase 10 atomic revisions=0.
- Conditional orchestration: 15 stage Recipes, 5 composite Recipes, one router, plus the revised complete UI Recipe.
- Unified verification: 29/29 Gates; 390 tests passed; one third-party `dateutil` deprecation warning.
- Real acceptance case: BenchShare, 14 application tests, 12 browser captures, six code findings and two black-box evidence findings closed, local latency thresholds met, ten-way conflict invariant passed.
- BenchShare local package SHA-256: `8fb653c637294f2a10edd3f9d540d6dabf74a9d1d1dded71e6ab3c0445cf3309`.
- No remote/provider/production action; no commit/push/PR/merge/deploy.

## Residual Risks the User Must Accept or Reject

1. Phase 11 uses one local synthetic product case; it does not establish market demand or production capacity.
2. BenchShare uses demonstrative identity, local HTTP, `ThreadingHTTPServer`, and single-process SQLite; it is an acceptance fixture, not a production application.
3. Production-only abilities such as real provider deployment, canary observation, remote rollback, real incident handling, external sessions, credentials, and local-system setup were contract-tested but intentionally not executed.
4. The source repository working tree contains extensive uncommitted V1/V2 work. A local catalog release changes files but still does not create a commit or remote delivery.
5. The only warning is a third-party `dateutil` deprecation outside the V2 implementation.
6. Approval releases the candidate contracts and orchestration as repository assets; it does not authorize any future capability invocation that itself requires current action authorization.

## Proposed Local Release Mutation

If approved, execute one bounded, reversible repository-local release operation:

1. Recompute Phase 9–11 manifests and stop on drift.
2. Snapshot every target path before mutation.
3. Publish the 157 accepted atomic candidates to the canonical V2 release catalog using release version `1.0.0` and status `released`.
4. Publish the accepted conditional Recipes/router, including Revision 4 UI/lifecycle controls, at release version `1.0.0` and status `released`.
5. Preserve V1 released Slots/Recipes; do not overwrite unrelated V1 identities. If a canonical path collides, stop rather than silently replace.
6. Generate V2 release catalog, lock, provenance, source/candidate hash mapping, rollback manifest, and release notes.
7. Rewrite no original `skills/` source and no Phase 0–11 evidence.
8. Run release-specific schema, provenance, exact-count, route, mutation, rollback, and no-action Gates.
9. Run full repository tests and all repository Gates.
10. Produce Phase 12 manifest/report and mark V2 released only if all checks pass.

Exact release target paths and collision behavior must be compiled and previewed before any write. The preview itself is read-only. No commit is created.

## Approval Options

- **Approve local release:** accept the stated residual risks and authorize only the bounded local repository mutation above.
- **Approve with conditions:** provide exact conditions; no write occurs until they are incorporated and re-presented if material.
- **Reject / remain evaluating:** preserve all candidates and evidence; no release mutation.

## Stop Conditions

Stop before mutation on absent/ambiguous approval, manifest drift, target collision, release-map incompleteness, source/evidence write, version/status ambiguity, schema failure, any Gate regression, any request for remote/provider/production action, or any mismatch between approved and actual target paths.

## Execution Result

The user approved the exact previewed controlled local release. The release wrote 495 assets into the isolated V2 namespaces, preserved all V1 flat assets, generated lock/provenance/rollback controls, and passed 30/30 unified Gates with `395 passed, 1 warning`. No remote or Git delivery action occurred.

## Success State

A successful Phase 12 proves only:

- explicit user approval exists for the exact local release scope;
- V2 release assets are locally published and recomputable;
- all tests/Gates remain green;
- V1/source/evidence trees are preserved;
- rollback can restore the pre-release local catalog;
- remote/provider/production actions remain zero.
