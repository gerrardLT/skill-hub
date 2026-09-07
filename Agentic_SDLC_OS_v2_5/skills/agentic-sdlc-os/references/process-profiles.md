# Process Profiles

Choose the smallest process that matches consequence and uncertainty. The profile changes Gate evidence and trace requirements; it does not remove non-compensable safety controls.

| Profile | Default use | Characteristics |
|---|---|---|
| `lite` | Low-criticality, reversible prototypes and small internal changes | Minimal accepted artifacts and evidence; retains integrity, risk and handoff controls |
| `standard` | Normal production software | Balanced artifact, evidence, trace-path and review requirements |
| `high-assurance` | High-criticality, regulated, irreversible or high-blast-radius work | Additional security, privacy, reliability, migration, rollback and independent-verification evidence |

Defaults follow criticality: low → `lite`, medium → `standard`, high → `high-assurance`. A high-criticality project cannot use `lite`.

```bash
python scripts/sdlc.py init <project> --name <name> --criticality medium --profile standard
python scripts/sdlc.py migrate <project> --profile high-assurance
python scripts/sdlc.py status <project> --json
```

Use `lite` only when failure is inexpensive, reversible and contained. Escalate the profile when the blast radius, uncertainty, data sensitivity or irreversibility increases. Do not downgrade merely to pass a blocked Gate.
