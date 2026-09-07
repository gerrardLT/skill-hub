# 安装

## 1. 安装 7 个本地 Skills

```bash
python scripts/install_local_skills.py --agent generic --project /path/to/project
```

支持：`generic`、`claude`、`cursor`、`codex`、`copilot`、`opencode`。

也可使用：

- `dist/<skill-name>/skill.zip`：单个 Skill。
- `dist/agentic-sdlc-os-all-skills.zip`：7 个 Skill 汇总包。

## 2. 一键初始化

```bash
python scripts/bootstrap_project.py /path/to/project --name PROJECT \
  --type greenfield --domain-pack saas \
  --budget-usd 25 --token-budget 500000 \
  --blast-radius 2 --data-sensitivity 2 --user-exposure 3
```

风险因素均为 0–5。可重复使用 `--domain-pack`。

## 3. 有界变更使用 Work Item

已有项目中的小修复不要机械继承整个项目的 high-assurance 流程。先登记受影响路径，让 v2.5 重新评估工作项风险：

```bash
python skills/agentic-sdlc-os/scripts/sdlc.py work-start /path/to/project \
  --id WORK-001 --title "fix bounded defect" --bounded \
  --affected-path path/to/file
python skills/agentic-sdlc-os/scripts/sdlc.py work-status /path/to/project
```

Unbounded、受保护路径和硬风险仍会自动升级。工作项结束后使用 `work-end`。

## 4. 控制面

本地：

```bash
python scripts/control_plane.py generate-master-key
export SDLC_MASTER_KEY_B64='...'
export SDLC_BOOTSTRAP_TOKEN='...'
python scripts/control_plane.py serve --database-url sqlite+pysqlite:///control.db
```

生产：

```bash
docker compose up --build
```

必须修改 `docker-compose.yml` 中示例密码/Token，并使用外部 Secret Manager。Live PostgreSQL 验证：

```bash
SDLC_POSTGRES_TEST_URL='postgresql+psycopg://...' \
  python scripts/postgres_conformance.py --require-live
```

## 5. 第三方 Skills

默认只生成选择计划，不静默安装。Design / QA / Evolution v2.5 推荐：

```bash
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os design --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os qa --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core

# 仅当项目实际使用 Datadog 时
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core --provider datadog
```

锁与治理：

```bash
python scripts/skill_governance.py select --os engineering --profile standard --tiers core,recommended
python scripts/skill_governance.py select --os evolution --profile standard --tiers core,recommended --provider posthog
python scripts/skill_governance.py lock --offline --output manifest/skills.lock.json
python scripts/skill_governance.py verify-lock --lock manifest/skills.lock.json
```

外部 Skill 未解析到明确 Git SHA、未审查源码/权限/依赖/许可证前，严格模式禁止安装。Provider Adapter 也受相同规则约束。
## 6. v2.5 生产声明验证

本地先跑并发/恢复安全性：

```bash
python scripts/control_plane_stress.py --jobs 50 --workers 10 --updates-per-worker 10 \
  --output validation/control_plane/sqlite-stress.json
```

SQLite 结果只能证明本地安全性。正式生产证据必须对 Live PostgreSQL 重跑：

```bash
python scripts/control_plane_stress.py --database-url "$SDLC_DATABASE_URL" \
  --output validation/control_plane/postgresql-stress.json
```

所有 Production Candidate / Production Ready 声明必须经过成熟度 Gate：

```bash
python scripts/maturity_gate.py assess validation/maturity/current-evidence.json \
  --target production-candidate --json
```

Gate 未通过时禁止手工升级成熟度标签。

