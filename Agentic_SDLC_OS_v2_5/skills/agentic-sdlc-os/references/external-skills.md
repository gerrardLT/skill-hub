# Third-party Skill Policy

`external-skills.json` contains ten generic candidates per OS plus explicit Evolution observability `provider_adapters`.

- `core`: minimum high-value capability.
- `recommended`: add only after a demonstrated workflow gap.
- `conditional`: activate only from technology, platform, product or task evidence.
- `provider_adapters`: Evolution-only vendor integrations for Sentry, Datadog and PostHog; never activated merely because the Skill is installed.

Use `scripts/install_external_skills.py` in dry-run mode first. Installation is never a quality guarantee. Review source, instructions, scripts, dependencies, network behavior, permissions, license and maintenance state.

```bash
python scripts/install_external_skills.py --os design --profile core
python scripts/install_external_skills.py --os qa --profile core
python scripts/install_external_skills.py --os evolution --profile core
python scripts/install_external_skills.py --os evolution --profile core --provider posthog
```

Do not install every Skill globally. Large overlapping libraries create routing ambiguity, context overhead and contradictory instructions. Prefer the smallest set covering the current bottleneck; remove Skills that are not used or whose output repeatedly fails evaluation.

For Evolution, keep the generic reasoning core vendor-neutral. Provider adapters may collect/query evidence and perform bounded provider actions, but cannot override `learning-decision`, QA/Release Gates, authorization or evidence quality.

Third-party Skills remain subordinate to this OS’s evidence, Gate, safety and authorization rules.
