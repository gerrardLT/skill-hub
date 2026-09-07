# 使用

## 新项目

```bash
python scripts/bootstrap_project.py . --name demo --domain-pack saas --budget-usd 20
python skills/agentic-sdlc-os/scripts/sdlc.py next .
```

Orchestrator 每次执行：读取状态 → 判断瓶颈 → 路由一个 OS → 调用最少 Skills → 写入证据/制品/风险/追踪 → Gate → 验证。

## 常用命令

```bash
python skills/agentic-sdlc-os/scripts/sdlc.py route . "上线后留存下降" --json
python skills/agentic-sdlc-os/scripts/sdlc.py quality . --json
python skills/agentic-sdlc-os/scripts/sdlc.py impact . --artifact-id PRD-001 --json
python skills/agentic-sdlc-os/scripts/sdlc.py gate . --name pm-ready --check
python skills/agentic-sdlc-os/scripts/sdlc.py audit .
python skills/agentic-sdlc-os/scripts/sdlc.py metrics . --json
```

## 自动证据

```bash
python scripts/collect_evidence.py . \
  --test-command "python -m pytest" \
  --junit reports/junit.xml \
  --coverage reports/coverage.xml \
  --artifact dist/app.zip \
  --deployment deploy.json \
  --supports TEST-001 --register
```

自动证据仍需人工判断其语义是否真正支持目标 claim。

## 预算

```bash
python scripts/cost_governance.py set . --cost-usd 25 --tokens 500000
python scripts/cost_governance.py assess . --forecast-usd 3 --forecast-tokens 20000
```

## 领域包

```bash
python scripts/apply_domain_pack.py recommend "HarmonyOS AI SaaS"
python scripts/apply_domain_pack.py apply . --pack harmonyos
python scripts/apply_domain_pack.py apply . --pack ai-agent
```

## 控制面同步

```bash
python scripts/sync_control_plane.py push . --database-url "$SDLC_DATABASE_URL" --actor agent-a
python scripts/sync_control_plane.py pull . --database-url "$SDLC_DATABASE_URL" --actor agent-a
```

## v2.5 Specialist Skills

```bash
# 最小 Core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os design --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os qa --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core

# Provider 只能显式启用
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core --provider sentry --agent codex
```

Design 每个工作项只设一个主视觉导演；QA 不自修自验；Evolution Provider 只提供证据/受限动作，不拥有 `learning-decision`。

## L5-B

```bash
python scripts/l5b_matched_experiment.py init experiment.json --project demo --target-pairs 5
# 添加任务后冻结；按预注册顺序使用独立执行上下文记录两组运行；完成盲评
python scripts/l5b_matched_experiment.py validate experiment.json --json
python scripts/l5b_matched_experiment.py seal experiment.json
python scripts/l5b_matched_experiment.py report experiment.json --output report.md
```

严禁把 `synthetic=true`、未 Seal、起始状态/模型/工具/环境不一致或执行上下文污染的结果描述为真实提效。

## 成熟度 Gate

```bash
python scripts/control_plane_stress.py --jobs 50 --workers 10 --updates-per-worker 10 \
  --output validation/control_plane/sqlite-stress.json
python scripts/maturity_gate.py assess validation/maturity/current-evidence.json \
  --target production-candidate --json
```

成熟度声明只认可证据文件及其 SHA-256；Synthetic L5-B、SQLite 压测、短期 Dogfooding 均不能替代正式生产证据。
