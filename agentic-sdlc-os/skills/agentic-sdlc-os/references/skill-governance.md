# Skill governance

Treat Skills as versioned supply-chain dependencies, not trusted prose.

## Controls

1. Scan `SKILL.md`, referenced resources and scripts.
2. Reject missing resources and critical destructive patterns.
3. Pin local content hashes and external Git commit SHAs.
4. Record source, license review, security status and lifecycle status.
5. Detect overlapping names/triggers and cap simultaneously active Skills.
6. Score effectiveness from real runs; promote, retain, canary, quarantine or retire.
7. Deny installation of unresolved external Skills under strict mode.

```bash
python scripts/skill_governance.py scan skills
python scripts/skill_governance.py lock --offline --output manifest/skills.lock.json
python scripts/skill_governance.py verify-lock --lock manifest/skills.lock.json
python scripts/skill_governance.py conflicts
python scripts/skill_governance.py select --os engineering --profile standard --tiers core,recommended
```

An offline lock intentionally leaves external Skills unresolved and not installable. Resolve against an approved source and review the license before enabling.
