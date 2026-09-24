# Bulk Finance Export — Blocking Inputs Required

The request is not yet specific enough to draft implementable requirements or testable acceptance criteria without inventing policy, permissions, or operating limits.

Please provide the following minimum blocking inputs:

1. **Requester roles** — Which user roles may request and download the export?
2. **Permitted account scope** — Which accounts, entities, tenants, regions, or subsidiaries may each authorized requester export?
3. **Export fields** — Which exact fields and record types must the report contain, and are any sensitive fields prohibited or subject to masking?
4. **Retention policy** — How long may generated export files remain available, and when must they be deleted?
5. **Legal approval** — Which legal/compliance reviewer must approve the export, and is approval required before requirements are finalized or before release?
6. **Maximum export size** — What maximum row count, file size, or covered date range must the export support?
7. **Data owner** — Who owns the exported data and has authority to resolve field, access, and policy questions?
8. **Decision date** — By what date must these inputs be confirmed?

Until these answers are supplied, the only safe requirement is: authorized finance users need a downloadable report. Detailed functional requirements and acceptance criteria remain blocked because authorization, scope, contents, retention, compliance, capacity, ownership, and decision timing are undefined.
