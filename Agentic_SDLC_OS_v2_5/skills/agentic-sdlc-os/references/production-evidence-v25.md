# Production Evidence v2.5

Use these controls before making a Production Candidate claim.

1. Third-party Skills: run `scripts/skill_supply_chain.py online-intake` in an internet-enabled target environment, review the immutable snapshots, run `audit`, and build the lock. Custom/plugin installers require runtime attestations from the actual harness.
2. L5-B: use `scripts/l5b_formal_runner.py`; use two independently attested execution contexts, the same frozen task/model/toolset/start state, and an independent blind reviewer. Synthetic runs are tooling smoke only.
3. PostgreSQL: run `scripts/postgres_live_validation.py --connection-fault` against a real PostgreSQL server. SQLite cannot satisfy this control.
4. Soak: start `scripts/soak_runner.py` without `--synthetic`, record fresh observations throughout the real 30-day interval, then seal. Backdated formal observations are rejected.
5. Organization drills: run `scripts/organization_drills.py --formal` on PostgreSQL with a non-local KMS/secret provider and real backup/restore/restore-verification commands.
6. Finally run `scripts/maturity_gate.py assess ... --target production-candidate`. The gate re-opens evidence artifacts and does not trust copied summary flags.

Never convert synthetic, local-only, static, or backdated evidence into a production claim.
