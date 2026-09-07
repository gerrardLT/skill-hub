# Shared-kernel Commands

Locate the sibling `agentic-sdlc-os` Skill and use its `scripts/sdlc.py`.

```bash
python <agentic-sdlc-os>/scripts/sdlc.py status <project>
python <agentic-sdlc-os>/scripts/sdlc.py next <project>
python <agentic-sdlc-os>/scripts/sdlc.py new-artifact <project> --type <type> --status draft --owner <owner>
python <agentic-sdlc-os>/scripts/sdlc.py add-evidence <project> --claim "..." --source "..." --source-type test --quality high --supports <artifact-id> --method "reproducible check"
python <agentic-sdlc-os>/scripts/sdlc.py add-risk <project> --id <risk-id> --title "..." --severity high --mitigation "..." --owner <owner>
python <agentic-sdlc-os>/scripts/sdlc.py update-risk <project> --id <risk-id> --status closed --mitigation "verified"
python <agentic-sdlc-os>/scripts/sdlc.py trace <project> --from <upstream-id> --to <downstream-id> --relation <relation>
python <agentic-sdlc-os>/scripts/sdlc.py gate <project> --name learning-decision
```

The JSON state is authoritative; generated ledger tables are read views.
