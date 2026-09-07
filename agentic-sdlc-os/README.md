# Agentic SDLC OS（Qoder Plugin）

证据驱动的软件全生命周期**治理内核**：以 `agentic-sdlc-os` 为主控制面（编排器），把工作路由到 **PM / Design / Engineering / QA / Release / Evolution** 六个域操作系统（各为一个独立 skill），并在项目 `.sdlc/` 共享内核中维护状态、证据、假设、决策、风险与哈希链审计；内置阶段 Gate、成本治理与 Skill 供应链治理。

**定位提醒**：本 plugin 是治理编排层，**不内置**六域真正执行的第三方专家 skill——71 个外部专家 / Provider Adapter 候选默认全部 `deny-unlocked`，需按 `SKILLS_RANKINGS.md` / `THIRD_PARTY_SKILLS.md` 完成供应链 intake 后另行安装（见下文 Setup）。

## 包含的 Skills（7）

| Skill | 角色 |
|---|---|
| `agentic-sdlc-os` | 主编排器/控制面：路由、Gate、证据、审计、共享内核 CLI |
| `pm-operating-system` | 产品：问题发现、策略、PRD、优先级 |
| `design-operating-system` | 设计：UX/UI、流程、原型、可访问性 |
| `engineering-operating-system` | 工程：架构、实现、重构、调试、代码审查 |
| `qa-operating-system` | 测试：测试策略、自动化、回归、非功能质量 |
| `release-operating-system` | 发布：CI/CD、迁移、灰度、回滚 |
| `evolution-operating-system` | 演化：指标、反馈、事故、实验、学习回流 |

每个 skill 均含 `SKILL.md`（Anthropic Agent Skills 规范 frontmatter）、`agents/openai.yaml`（Codex/Copilot 兼容元数据）与 `references/` 支持文档；主编排器另含自包含的 `scripts/`（20 个 Python CLI，含 `sdlc.py`）、`references/manifests/`（manifest/schema 镜像）与 `manifest/`、`domain-packs/`、`control_plane/` 内嵌副本。

## 来源（Provenance）

- **源**：本地仓库 `d:\project\skills-hub\Agentic_SDLC_OS_v2_5\skills\`（Agentic SDLC OS v2.5）。
- **拷贝方式**：源项目官方安装器 `python scripts/install_local_skills.py --target <plugin>/skills`（`copytree` 全量保真拷贝，含校验 `SKILL.md` + `agents/openai.yaml`）。
- **Logo**：`assets/avatar.svg` 为本次转换时**自生成**（六边形编排器 + 六域节点），非上游资产。
- **分发格式**：`.qoder-plugin/plugin.json`（Qoder plugin 规范）；安装态另见 `~/.qoder/plugins/cache/local-bundler/agentic-sdlc-os/plugin.json`。

## 省略与调整

- **未省略任何 skill 内容**；仅清除了拷贝带入的运行态残留（`__pycache__/`、`*.pyc`、`.DS_Store`）。
- `agents/openai.yaml` 保留为 skill 内部元数据（Codex 等平台兼容），**不**声明为 Qoder `agents` 组件（Qoder agent 是另一种组件类型）。
- 未声明 `rules/`、`commands/`、`hooks/`、`mcpServers/`——源项目不含对应的 Qoder 组件文件，遵循"只声明真实存在的组件"。

## Setup

1. **运行时**：Python 3.10+（CLI 内核使用 `X | None` 类型语法）。Windows 建议先 `$env:PYTHONUTF8=1`（避免 GBK 解码错误）。
2. **初始化一个被治理的项目**：

```bash
python scripts/bootstrap_project.py ./my-project --name my-project --domain-pack saas --budget-usd 25
python skills/agentic-sdlc-os/scripts/sdlc.py status ./my-project
python skills/agentic-sdlc-os/scripts/sdlc.py next ./my-project
```

> 注意：skill 装入 agent 后 `sdlc.py` 的相对路径为 `scripts/sdlc.py`（SKILL.md 中的写法即此视角）；在本仓库源码树中运行时需用全路径 `skills/agentic-sdlc-os/scripts/sdlc.py`。

3. **专家能力（可选）**：默认 fail-closed，需要时显式 intake：

```bash
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os design --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os qa --profile core
```

4. **触发方式**：当任务命中主编排器 description（greenfield/brownfield 项目、端到端交付、跨职能交接、质量门、发布就绪、事故恢复、持续改进）时由 Agent 自动加载；也可显式点名 `agentic-sdlc-os`。

## 验证证据（Validation）

离线验证器（create-plugin 自带）：

```bash
python c:\Users\gerrard\.qoder\plugins\cache\qoder-bundler\qoder-create-plugin\skills\create-plugin\scripts\validate_qoder_plugin.py d:\project\skills-hub\agentic-sdlc-os
```

输出：

```text
Validating Qoder plugin: D:\project\skills-hub\agentic-sdlc-os
OK: no issues found
```

退出码 `0`。附加核验：7 个 `SKILL.md` 均存在且含 `name`/`description` frontmatter；manifest 组件路径 `./skills/`、`./assets/avatar.svg` 均真实存在。
