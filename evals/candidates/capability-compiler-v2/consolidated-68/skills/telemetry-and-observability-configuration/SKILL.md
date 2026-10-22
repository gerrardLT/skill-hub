---
name: telemetry-and-observability-configuration
description: "Consolidated capability with 7 selectable modes: ai-observability-configuration; apm-instrumentation-enablement; apm-instrumentation-troubleshooting; log-observability-configuration; monitoring-and-alert-configuration; observability-agent-installation; release-observability-configuration. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [ai-observability-configuration, apm-instrumentation-enablement, apm-instrumentation-troubleshooting, log-observability-configuration, monitoring-and-alert-configuration, observability-agent-installation, release-observability-configuration]
---

# Telemetry And Observability Configuration

## Responsibility

Consolidated capability covering 7 related modes: Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization.; Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization.; Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners.; Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization.; Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization.; Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization.; Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `ai-observability-configuration` | `remote-write-authorized-only` | An LLM or agent application needs its generation spans, token usage and tool calls traced in one provider under a telemetry governance policy; Someone asks which prompt, response and tool fields may b | Define the AI model, prompt, retrieval, and data architecture first (-> ai-model-and-data-architecture); Classify alread |
| `apm-instrumentation-enablement` | `remote-write-authorized-only` | One service needs APM tracing turned on through one approved instrumentation method after the agent is in place; Someone asks for the exact change that enables tracing for a service and environment wi | Verify that existing instrumentation emits correct traces and identity (-> apm-instrumentation-verification); Install th |
| `apm-instrumentation-troubleshooting` | `external-read` | Expected traces, service names or versions are missing, duplicated or wrong in the APM provider; Someone asks why instrumentation that was enabled is not producing the expected signals. | Enable or reconfigure APM instrumentation after diagnosis (-> apm-instrumentation-enablement); Verify expected service,  |
| `log-observability-configuration` | `remote-write-authorized-only` | Logs from exact services need collection, parsing, routing and retention set up in one provider with sensitive fields controlled; Someone asks for the pipeline, exclusion filters and cost estimate for | Define metrics, dashboards, and alert semantics from approved outcomes (-> metrics-system-and-observability); Install th |
| `monitoring-and-alert-configuration` | `remote-write-authorized-only` | A monitor or alert route must be created or changed from an approved SLO, threshold, window and owner; Someone asks for the exact alert definition with missing-data behavior, routing and runbook. | Define the metric system and threshold rationale first (-> metrics-system-and-observability); Coordinate an active incid |
| `observability-agent-installation` | `remote-write-authorized-only` | One observability agent must be installed on exact hosts or a cluster with a pinned artifact and least privilege; Someone asks for the exact install change, health check and uninstall path for an agen | Enable application-level APM instrumentation after the agent exists (-> apm-instrumentation-enablement); Verify emitted  |
| `release-observability-configuration` | `remote-write-authorized-only` | A release and its commits must be registered in an observability provider so new errors can be tied to a release; Someone asks for the exact release identifier, commit range and commands to associate  | Define and preserve source revision and provenance metadata locally (-> source-metadata-and-provenance); Deploy the rele |

## Mode: `ai-observability-configuration`

### ai-observability-configuration

#### Responsibility

Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization.

#### Trigger

Use when the request matches any of:
- An LLM or agent application needs its generation spans, token usage and tool calls traced in one provider under a telemetry governance policy
- Someone asks which prompt, response and tool fields may be collected, at what sampling, retention and access

Do not use when:
- Define the AI model, prompt, retrieval, and data architecture first. Route to `ai-model-and-data-architecture`.
- Classify already-collected production traces without changing configuration. Route to `production-trace-classification`.
- Configure log collection, parsing and routing. Route to `log-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

#### Required Inputs

- AI application, traces, sensitive-data policy, provider, evaluation signals, retention, and authorization.

#### Procedure

1. Verify provider, account, application, environments, models, traces, fields, data classes, consent, minimization, redaction, sampling, retention, region, access, cost, deletion, dashboards, alerts, and fresh authorization.
2. Preview exact instrumentation or provider settings and sample payload schema; block prompt, response, user, tool, or retrieved content that exceeds governance.
3. Perform one bounded configuration change without altering models, prompts, application behavior, unrelated services, or autonomous action rights.
4. Record provider receipt, configuration version, governed fields, sampling, validation, cost estimate, propagation, deletion, and rollback.

#### Domain Guidance

- Default schema: the gen_ai.* span attribute conventions (operation name, system, request and response model, token counts, finish reason, tool name). Record the convention version used.
- Detect a supported SDK or auto-instrumentation first and use it; add manual spans only when no supported SDK is detected, and never run both for the same call.
- Prompt, response, tool, user and retrieved content are denied by default; collect a field only when the governance record names it, with sampling, redaction, retention and access.
- Discriminator by signal type: this Skill handles model calls, prompts, traces and evaluation telemetry.

#### Output Contract

Produce:
- AI observability configuration receipt
- governed telemetry schema
- sampling, redaction, retention, and access record
- validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-application`
- `telemetry-schema`
- `minimization`
- `redaction`
- `sampling`
- `retention`
- `access`
- `deletion`

#### Hard Gates

- AI observability may collect only explicitly governed fields at approved sampling, retention, region, and access; prompt, response, tool, user, or retrieved content is denied by default.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ai-model-and-data-architecture`
- `production-trace-classification`
- `production-llm-trace-root-cause-analysis`
- `monitoring-and-alert-configuration`
- `log-observability-configuration`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `apm-instrumentation-enablement`

### apm-instrumentation-enablement

#### Responsibility

Enable one approved APM instrumentation variant for exact services and environments without duplicate agents or manual instrumentation under per-action authorization.

#### Trigger

Use when the request matches any of:
- One service needs APM tracing turned on through one approved instrumentation method after the agent is in place
- Someone asks for the exact change that enables tracing for a service and environment without duplicate instrumentation

Do not use when:
- Verify that existing instrumentation emits correct traces and identity. Route to `apm-instrumentation-verification`.
- Install the required observability agent on the target platform. Route to `observability-agent-installation`.

#### Required Inputs

- Installed agent, service runtime, platform variant, environment, and authorization.

#### Procedure

1. Verify provider, platform and runtime, service and environment, current agents and libraries, compatibility, identity tags, sampling, sensitive fields, overhead budget, release metadata, health, rollback, and fresh authorization.
2. Choose exactly one instrumentation path, reusing an existing exporter where present, and give the concrete change with its resource and cost impact.
3. Detect duplicate auto and manual instrumentation, conflicting versions, unsupported runtime, and unexpected data capture before previewing exact change.
4. Perform one bounded enablement through the provider or platform adapter without installing unrelated agents or modifying other services.
5. Record provider receipt, instrumentation version, affected service, config, restart or propagation, health, verification handoff, and rollback.

#### Domain Guidance

- Commit to exactly one instrumentation path. When an existing exporter or collector is already in use, reuse it and state why; leave no open alternative. Show the concrete change (for example a task-definition or manifest diff with the sidecar, dependency ordering and memory or cost increase for approval).
- Kubernetes variant preconditions: every context variable resolved before step 0, and the agent resource is extended in place rather than replaced with a second manifest.

#### Output Contract

Produce:
- APM enablement receipt
- instrumentation and service identity
- duplicate and compatibility evidence
- verification and rollback handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `single-instrumentation-path`
- `service-environment`
- `compatibility`
- `overhead-budget`
- `telemetry-governance`
- `rollback`

#### Hard Gates

- APM enablement requires a single known instrumentation path, exact service and environment identity, compatibility and overhead checks, governed telemetry, and rollback; duplicate instrumentation blocks change.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `apm-instrumentation-verification`
- `apm-instrumentation-troubleshooting`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `apm-instrumentation-troubleshooting`

### apm-instrumentation-troubleshooting

#### Responsibility

Diagnose missing, duplicate, malformed, or misidentified APM signals from read-only platform evidence and route fixes to authorized enablement or installation owners.

#### Trigger

Use when the request matches any of:
- Expected traces, service names or versions are missing, duplicated or wrong in the APM provider
- Someone asks why instrumentation that was enabled is not producing the expected signals

Do not use when:
- Enable or reconfigure APM instrumentation after diagnosis. Route to `apm-instrumentation-enablement`.
- Verify expected service, environment, version, and trace evidence after a change. Route to `apm-instrumentation-verification`.

#### Required Inputs

- Failed verification evidence, platform variant, service configuration, logs, and authority boundary.

#### Procedure

1. Freeze service, environment, version, platform, runtime, expected instrumentation, provider scope, read-only authority, symptom window, and sensitive-data boundary.
2. Inspect read-only status, agent or library versions, config metadata, startup evidence, network path, sampling, tags, trace routes, duplicate sources, and provider intake status.
3. Test competing hypotheses against timestamped evidence and separate missing emission, transport, sampling, identity, parsing, and provider-query failures.
4. Return root-cause confidence, evidence gaps, and exact enablement, installation, identity, or verification handoff; no remote fix.

#### Domain Guidance

- Order checks provider side first (is the tracer reporting, does the provider recognise the service, what SDK configuration is active), then host side. Before asking for host access, say what you will check and why.

#### Output Contract

Produce:
- APM troubleshooting evidence
- hypothesis and root-cause analysis
- signal-path diagnosis
- authorized fix and verification handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `read-only`
- `signal-path`
- `competing-hypotheses`
- `timestamped-evidence`
- `no-fix`
- `handoff`

#### Hard Gates

- Troubleshooting is read-only: it cannot install agents, change sampling or tags, restart services, remap identity, or claim a fix from diagnosis alone.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `apm-instrumentation-enablement`
- `apm-instrumentation-verification`
- `observability-agent-installation`
- `service-identity-remapping`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `log-observability-configuration`

### log-observability-configuration

#### Responsibility

Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization.

#### Trigger

Use when the request matches any of:
- Logs from exact services need collection, parsing, routing and retention set up in one provider with sensitive fields controlled
- Someone asks for the pipeline, exclusion filters and cost estimate for a log source

Do not use when:
- Define metrics, dashboards, and alert semantics from approved outcomes. Route to `metrics-system-and-observability`.
- Install the observability agent required to collect host logs. Route to `observability-agent-installation`.
- Configure AI or LLM trace spans and token telemetry. Route to `ai-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

#### Required Inputs

- Log sources, schemas, provider, authorization, retention, redaction, and routing requirements.

#### Procedure

1. Verify provider, account, sources, services, environments, log schemas, fields, PII and secret classes, minimization, redaction, parsing, routing, sampling, retention, region, access, cost, deletion, failure handling, and fresh authorization.
2. Preview exact sources, pipelines, indexes, destinations, transformations, and sample redacted events; block credential or sensitive-value capture.
3. Perform one bounded configuration change without modifying applications, unrelated pipelines, monitors, or retention outside scope.
4. Record provider receipt, config version, sample validation, volume and cost estimate, access, retention, deletion, propagation, and rollback.

#### Domain Guidance

- Cost control order: exclusion filters first (drop debug and health-check noise), then sampling, then shorter retention on low-value indexes. Estimate volume and cost per index before the change.
- Pipeline pattern: a filter selecting the service, a parser (for example grok for a known line format) with sample lines, then remappers for status, service and trace id.
- Troubleshooting map: logs not appearing (check agent and pipeline filters), high cost (add exclusions), slow search (narrow time range and use indexes), missing attributes (check the parser).
- Discriminator by signal type: this Skill handles log collection, parsing, routing and retention.

#### Output Contract

Produce:
- log configuration receipt
- source, parse, and route schema
- redaction, retention, access, and cost record
- sample validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-log-sources`
- `parsing`
- `routing`
- `redaction`
- `retention`
- `access`
- `volume-cost`
- `deletion`

#### Hard Gates

- Logs deny secret and sensitive fields by default and require exact source, parsing, routing, retention, access, deletion, volume, and cost boundaries before provider mutation.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `metrics-system-and-observability`
- `monitoring-and-alert-configuration`
- `observability-agent-installation`
- `source-metadata-and-provenance`
- `ai-observability-configuration`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `monitoring-and-alert-configuration`

### monitoring-and-alert-configuration

#### Responsibility

Create or update exact provider monitors and alert routes from approved SLOs, thresholds, windows, severity, ownership, and noise controls under per-action authorization.

#### Trigger

Use when the request matches any of:
- A monitor or alert route must be created or changed from an approved SLO, threshold, window and owner
- Someone asks for the exact alert definition with missing-data behavior, routing and runbook

Do not use when:
- Define the metric system and threshold rationale first. Route to `metrics-system-and-observability`.
- Coordinate an active incident after an alert fires. Route to `incident-response-coordination`.
- Handle model calls, prompts, traces and evaluation telemetry. Route to `ai-observability-configuration`.
- Handle log collection, parsing, routing and retention. Route to `log-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.

#### Required Inputs

- Signal definition, threshold rationale, evaluation window, recipients, provider, and authorization.

#### Procedure

1. Verify provider, account, environment, metric definitions, SLO, threshold or burn-rate rationale, windows, missing-data behavior, severity, routing, schedules, deduplication, suppression, runbook, test method, owner, rollback, and fresh authorization.
2. Preview exact monitor and notification diff and predicted behavior against historical data where available.
3. Perform one bounded provider configuration change without acknowledging incidents or altering unrelated monitors, dashboards, or integrations.
4. Record provider receipt, monitor IDs and version, test notification or dry-run evidence, routing, noise and cost risk, propagation, and rollback.

#### Domain Guidance

- An alert without an actionable named owner and a runbook is not ready: return the definition as a draft and name who must accept it before creation.
- Preview predicted alert volume from historical data where available and state the noise and cost risk.
- Discriminator by signal type: this Skill handles monitors and alert routes from approved SLOs.
- Rollback verification must check that the changed rule and routes have actually reverted in the exact authorized provider target, not merely that the rollback command returned successfully. Proposal-only outputs label this verification as pending.

#### Output Contract

Produce:
- monitor and alert configuration receipt
- threshold, window, and missing-data contract
- routing and runbook map
- validation, noise, and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `SLO-threshold`
- `window`
- `missing-data`
- `actionable-owner`
- `routing`
- `deduplication`
- `runbook`
- `rollback`

#### Hard Gates

- An alert requires an actionable owner, justified threshold and window, missing-data behavior, deduplication, runbook, validation, and rollback; alert volume alone is not coverage.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `metrics-system-and-observability`
- `incident-response-coordination`
- `release-observability-configuration`
- `production-canary-monitoring`
- `ai-observability-configuration`
- `log-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `observability-agent-installation`

### observability-agent-installation

#### Responsibility

Install one approved observability agent variant on exact hosts or cluster scope with pinned artifact, least privilege, governed data, health, and rollback under per-action authorization.

#### Trigger

Use when the request matches any of:
- One observability agent must be installed on exact hosts or a cluster with a pinned artifact and least privilege
- Someone asks for the exact install change, health check and uninstall path for an agent

Do not use when:
- Enable application-level APM instrumentation after the agent exists. Route to `apm-instrumentation-enablement`.
- Verify emitted APM signals read-only after installation. Route to `apm-instrumentation-verification`.

#### Required Inputs

- Platform, environment, provider account, credentials, desired instrumentation, and authorization.

#### Procedure

1. Verify provider and platform variant, targets, OS or cluster versions, pinned package or image digest, integrity, identities, permissions, secret references, network, ports, resources, telemetry fields, redaction, sampling, retention, cost, health, upgrade, rollback, and fresh authorization.
2. Preview exact package, daemon, workload, RBAC, network, and config changes; block duplicate agents, privilege escalation, mutable latest, or uncontrolled telemetry.
3. Perform one bounded install with timeout and stop conditions without changing application code or unrelated platform resources.
4. Record installation receipt, artifact identity, target inventory, permissions, health, emitted-signal handoff, partial failure cleanup, uninstall, and rollback.

#### Domain Guidance

- Cluster-type variant: self-hosted clusters (minikube, kind) need kubelet TLS verification disabled in the agent configuration; managed clusters (GKE, EKS, AKS) omit that setting.
- Health verification requires one healthy agent pod per node, naming every node by architecture (including arm64 nodes) and naming any node that has no pod yet.

#### Output Contract

Produce:
- agent installation receipt
- pinned artifact and target inventory
- permission and telemetry governance evidence
- health, uninstall, and rollback record
- per-node health check list by architecture

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `pinned-agent`
- `exact-targets`
- `least-privilege`
- `telemetry-governance`
- `health`
- `uninstall`
- `rollback`

#### Hard Gates

- Agent installation requires a pinned verified artifact, exact targets, least privilege, governed telemetry, resource and network bounds, health evidence, and uninstall or rollback; mutable latest and duplicate agents are blocked.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `apm-instrumentation-enablement`
- `apm-instrumentation-verification`
- `log-observability-configuration`
- `kubernetes-deployment-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `release-observability-configuration`

### release-observability-configuration

#### Responsibility

Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source.

#### Trigger

Use when the request matches any of:
- A release and its commits must be registered in an observability provider so new errors can be tied to a release
- Someone asks for the exact release identifier, commit range and commands to associate a build with its services

Do not use when:
- Define and preserve source revision and provenance metadata locally. Route to `source-metadata-and-provenance`.
- Deploy the release artifact to the provider environment. Route to `deployment-trigger-execution`.
- Handle model calls, prompts, traces and evaluation telemetry. Route to `ai-observability-configuration`.
- Handle log collection, parsing, routing and retention. Route to `log-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

#### Required Inputs

- Release naming, repository, build metadata, provider project, credentials, and authorization.

#### Procedure

1. Diagnose which half of release wiring already exists and plan only the missing half; use the exact, untruncated release identifier throughout.
2. Verify provider, account, services, environments, repository, exact commit and release IDs, version scheme, artifact digest, source-map or metadata references, retention, access, collision, historical continuity, rollback, and fresh authorization.
3. Preview exact release create or association diff and reject ambiguous, duplicate, mutable, or mismatched identities.
4. Perform one bounded provider configuration action without deployment, source write, service remap, unrelated release change, or issue mutation.
5. Record provider receipt, release identity, linked commits, services and environments, propagation validation, collision status, and rollback or deletion path.

#### Domain Guidance

- Diagnose which half of release wiring exists before changing anything: the release tag on events in the SDK, or the release created in CI with commits and a deploy. Do only the missing half.
- Derive the release identifier from the supplied full commit SHA or version exactly; never truncate it, and use the same identifier in every command, verification and rollback step. Use the exact commit range between the previous and current release.
- Discriminator by signal type: this Skill handles release and commit association for services and environments.

#### Output Contract

Produce:
- release association receipt
- release, commit, service, and environment map
- propagation and collision evidence
- rollback or deletion record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-release`
- `commit-identity`
- `artifact-digest`
- `service-environment`
- `collision-check`
- `no-deploy`
- `rollback`

#### Hard Gates

- Release observability requires exact immutable release, commit, artifact, service, and environment identities; association does not prove deployment or authorize provider actions beyond the mapping.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `source-metadata-and-provenance`
- `deployment-trigger-execution`
- `service-identity-remapping`
- `deployment-observation`
- `ai-observability-configuration`
- `log-observability-configuration`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
