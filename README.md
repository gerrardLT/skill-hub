# skills-hub

个人 AI 资产创作中心：集中创建、管理并向 Qoder 分发 skills、plugins、subagents、workflows。

## 目录结构

```
skills-hub/
├── skills/       # 独立 Agent Skill（SKILL.md + 可选资源文件）
├── plugins/      # Qoder 原生插件（可打包分发的完整单元）
├── subagents/    # 专用子代理定义
├── workflows/    # 多步骤工作流（编排多个 skill）
└── docs/
    └── conventions.md   # 命名规范与编写标准（创建任何资产前先读）
```

## 四类资产怎么选

| 资产类型 | 适用场景 | 创建方式 |
|---------|---------|---------|
| **skill** | 教 agent 一套固定做法（流程、模板、规范），按需触发 | `/create-skill` |
| **plugin** | 需要分发安装的完整包（可含多个 skill/命令/MCP） | `/create-plugin` |
| **subagent** | 需要独立上下文、专用工具集的专属代理 | `/create-subagent` |
| **workflow** | 跨多个 skill 的编排流程，串联成一条流水线 | 手写或由 skill 生成后存入 |

判断口诀：**做法 → skill，分发 → plugin，分身 → subagent，串联 → workflow。**

## 标准工作流

### 1. 创建新资产

在本项目中发起，让 agent 读取 `docs/conventions.md` 后按对应模板创建：

```
帮我创建一个 skill，用来 ______
```

新资产放入对应目录，从 `_template/` 复制起步。

### 2. 本地迭代

- 直接编辑本仓库中的资产文件
- 在实际任务中试触发、试运行，回填改进
- 用 git 管理版本：每个资产一个有意义的提交

### 3. 分发到 Qoder

- **skill / plugin**：在 Qoder 中用 `/create-plugin` 将本仓库的资产转成 Qoder 原生插件安装（注册至 `~/.qoder/plugins/`）
- **subagent**：按 `docs/conventions.md` 中的安装说明放入对应位置
- **workflow**：本质是 skill 编排，随所在 skill 一同分发

分发后以 Qoder 内实际触发的效果为准，问题回本仓库修，再重新分发。

## 内置系统：PM-OS（产品经理操作系统）

本仓库已落地一套完整的产品经理操作系统，详见 [skills/pm-operating-system/SKILL.md](skills/pm-operating-system/SKILL.md)：

- **10 个路由层 PM skill**（deanpeters / phuryn / refoundai）安装在 `skills/`，由 `pm-operating-system` 总控调度；另补装 17 个子依赖 skill（被 workflow 型 skill 内部引用），合计 28 个
- **状态机**：INTAKE → DISCOVERY → STRATEGY → PRIORITIZATION → DEFINITION → PLANNING → VALIDATION → MEASUREMENT → LEARNING ↺
- **阶段 Gate + 回退规则**、**动态路由**、**Learning Loop**、**`.product/` 项目记忆**均定义在 skill 的 `references/` 内
- **4 个 subagent**（research / competitive / red-team / evidence）在 `subagents/`，仅在需要独立上下文/红队审查时才派
- 第三方 skill 统一用 `npx skills add <repo> --skill <name> -a openclaw -y` 安装到本项目 `skills/`（openclaw 目标即 `skills/` 目录）

在产品项目中使用时直接说产品任务（如“帮我判断这个产品值不值得做”），PM-OS 会接管路由；单环节任务（如“要一份访谈提纲”）会直接走对应子 skill。

## 维护原则

1. 本仓库是唯一创作源（single source of truth），Qoder 里的是部署副本
2. 任何资产先在 `docs/conventions.md` 框架下命名，再动手写
3. 报废资产直接删除目录，不留 `*-old`、`*-backup`
4. 第三方 skill（`npx skills add` 安装的）同样纳入本仓库 git 管理；升级时重跑安装命令后提交
