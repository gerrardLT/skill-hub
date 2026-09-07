# Domain extension packs

Domain packs add controls, required artifacts, evidence, Gate overlays, risk adjustment and budget multipliers without forking the core lifecycle.

Included packs:

- `harmonyos`: ArkTS/ArkUI, lifecycle, permissions, compatibility and AppGallery readiness.
- `saas`: tenancy isolation, billing, entitlements, migrations, SLOs and auditability.
- `ai-agent`: prompt injection, tool authorization, model fallback, evaluation and human override.
- `ecommerce`: inventory, order/payment consistency, refunds, promotions and peak traffic.
- `finance`: ledger integrity, reconciliation, authorization, audit retention and tested recovery.

```bash
python scripts/apply_domain_pack.py recommend "AI SaaS with payment ledger"
python scripts/apply_domain_pack.py apply . --pack ai-agent
python scripts/apply_domain_pack.py apply . --pack saas
```

A pack can only strengthen requirements. It must not silently remove core Gates. At `production-ready`, all active domain evidence requirements must be represented in the evidence ledger.
