# Decisions

| ID | Title | Choice | Rationale | Owner | Decided |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | Use atomic database transactions instead of in-memory capacity counters | SQLite transaction plus partial unique indexes and idempotency records | The choice makes oversell prevention executable and auditable under concurrent requests. | architecture-owner | 2026-08-31T09:12:11Z |

> Generated from `.sdlc/state.json`. Edit state through the CLI when possible.
