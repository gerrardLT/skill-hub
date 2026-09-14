# git-guardrails-claude-code 来源能力档案

## Problem

在自主式或半自主式 AI 智能体开发会话中，智能体可能由于上下文误解、尝试强行解决冲突或执行激进清理，无意间调用具备高破坏性且不可逆的 Git 命令（如 `git push --force`、`git reset --hard`、`git clean -fd`、`git branch -D` 或 `git restore .`）。若缺乏物理级执行拦截机制，可能直接抹除开发者未提交的工作区变更、丢弃历史提交甚至覆盖远程生产分支，造成灾难性数据丢失。

## When to Use

- **强化 AI 智能体执行安全边界（主要场景）**：在团队或个人环境中为 Claude Code / Qoder 等智能体配置前置保护门禁，从根源物理拦截危险 Git 操作。
- **防止不可逆工作区数据清除**：当开发者希望彻底封死智能体自行丢弃未暂存工作区改动（`git checkout .` / `git restore .`）的可能性时。
- **防止未经审查的代码直接推向远端**：确保所有分支推送（`git push`）必须由人类开发者在终端显式执行。
- **跨项目或项目级安全防护安装**：按需安装至项目级（`.claude/settings.json`）或全局级（`~/.claude/settings.json`）。

## When Not to Use

- **完全只读的审计分析环境**：平台本身未赋予任何 Bash 执行权限、或处于严格沙箱环境无需额外 Git 拦截的场景。
- **需要智能体全自动端到端执行 git push 的无人值守 CI 流程**：若流水线专门设计为由智能体直接完成远程代码推送，安装此拦截钩子将阻断流程。

## Role

代码库物理安全卫士（Codebase Physical Security Guard）。专注于在工具执行前（PreToolUse）设置底层截流网关，通过对输入命令的正则模式匹配拦截高危破坏性操作，保护物理版本控制资产与分支完整性。

## Inputs

- **安装作用域选择（Scope）**：用户选定的项目级范围（`this project only`，对应当前仓库 `.claude/`）或全局范围（`all projects`，对应用户主目录 `~/.claude/`）。
- **待执行 Bash 工具输入载荷（Tool Input JSON）**：包含智能体拟执行命令的 JSON 输入流（例如 `{"tool_input":{"command":"git push origin main"}}`）。
- **自定义阻断规则（可选）**：用户补充或定制的危险匹配模式。

## Outputs

1. **可执行物理防护钩子脚本**：安装至 `.claude/hooks/block-dangerous-git.sh` 或 `~/.claude/hooks/block-dangerous-git.sh` 并赋予 `+x` 权限。
2. **合并更新的配置文件**：安全合并入 `.claude/settings.json` 或 `~/.claude/settings.json` 的 `hooks.PreToolUse` 节点。
3. **拦截告警与状态码**：
   - 遭遇危险命令：退出码为 `2`，向标准错误输出详细阻断信息（`BLOCKED: ... The user has prevented you from doing this.`）。
   - 安全命令：退出码为 `0`，命令正常放行。

## Workflow

1. **询问并确认安装范围（Step 1: Ask scope）**：
   - 明确安装边界：仅当前项目（`.claude/settings.json`）还是全局所有项目（`~/.claude/settings.json`）。
2. **复制并部署物理防护脚本（Step 2: Copy the hook script）**：
   - 将捆绑的 `scripts/block-dangerous-git.sh` 复制到对应作用域目录：
     - 项目级：`.claude/hooks/block-dangerous-git.sh`
     - 全局级：`~/.claude/hooks/block-dangerous-git.sh`
   - 执行 `chmod +x` 赋予可执行权限。
3. **安全注入配置（Step 3: Add hook to settings）**：
   - 将 PreToolUse 钩子配置以非破坏性方式合并入目标 `settings.json` 中的 `hooks.PreToolUse` 数组。
   - 严禁覆盖用户已有的其他配置项。
4. **定制化咨询（Step 4: Ask about customization）**：
   - 询问用户是否需要向阻断清单中增删特定的正则模式，并按需就地调整脚本。
5. **执行干跑验证测试（Step 5: Verify）**：
   - 运行管道测试命令验证拦截生效性：
     ```bash
     echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
     ```
   - 必须确认其输出退出码为 2 并在 stderr 中正确打印 BLOCKED 告警。

## Branches

- **阻断分支（Command Blocked）**：拟执行命令匹配危险模式 -> 脚本输出错误信息并以退出码 2 终止 -> 平台拦截该 Bash 工具调用 -> 智能体获知权限受限并停止破坏动作。
- **放行分支（Command Permitted）**：拟执行命令为常规操作（如 `git status`、`git diff`、`git log`、`git add`、`git commit`） -> 脚本以退出码 0 顺畅退出 -> 正常执行。
- **自定义增删分支**：用户要求豁免某种特例或增加对 `git rebase` 的拦截 -> 针对性修订脚本中的 `DANGEROUS_PATTERNS` 数组。

## Rules

- **非破坏性配置合并原则**：修改 `settings.json` 时必须先读取并解析现有 JSON，将 PreToolUse 规则安全追加至数组中，绝对禁止全量覆盖配置文件。
- **硬性阻断协议**：拦截触发时必须返回进程退出码 `2`，并在 stderr 明确告警，确保主控平台能精准识别 PreToolUse 拦截信号。
- **默认危险命令黑名单**：默认必须覆盖 9 类高危正则：
  1. `git push`
  2. `git reset --hard`
  3. `git clean -fd`
  4. `git clean -f`
  5. `git branch -D`
  6. `git checkout \.`
  7. `git restore \.`
  8. `push --force`
  9. `reset --hard`
- **最小特权告知**：拦截后必须向智能体明确传递用户设防信号，彻底打消智能体尝试绕过的倾向。

## Exceptions

- 若用户由于特殊调试需要临时解除限制，可由用户显式在 `settings.json` 中注销该钩子或自行在终端执行危险命令。

## Dependencies

- **系统 Shell 环境**：Bash 运行时环境（`/bin/bash`）及 `grep -qE`。
- **命令行 JSON 解析器**：依赖 `jq` 命令行工具解析标准输入中的 `.tool_input.command`。
- **平台钩子机制**：依赖宿主平台支持的 `PreToolUse` 事件截流规范。

## Permissions and Side Effects

- **权限要求**：设置文件（`settings.json`）读写权限、钩子目录与脚本写入执行权限（`chmod +x`）。
- **副作用**：在当前项目或全局目录下新增 `.claude/hooks/` 脚本；对后续所有智能体发起的 Bash 工具调用注入毫秒级的管道正则预检开销。

## Gates

- **Gate 1: Scope Confirmation Gate**：必须经由人类伙伴确认安装作用域（项目级或全局级）后方可创建物理文件。
- **Gate 2: Executable Permission Gate**：脚本部署后必须验证拥有执行权限（`chmod +x`），防止因权限不足导致调用崩溃。
- **Gate 3: Dry-Run Exit Code 2 Gate**：安装完成后必须执行带 `git push` 载荷的验证命令，确保脚本精确返回退出码 2。

## Open Questions

- 当命令采用复杂的复合拼接（如 `eval "git "..."push"` 或重命名别名）时，纯基于正则表达式的简单匹配是否存在漏网或误杀可能？
- 在缺乏预装 `jq` 二进制工具的裸机或极简 Docker 容器中，如何提供零外部依赖的纯 Bash/Python JSON 字段提取后备方案？

## Unique Value

提供了一种独立于大模型注意力与幻觉波动的“物理硬门禁”（Hard Deterministic Gate）。将高危 Git 指令的防护从口头提示词规劝升格为确定性的进程级拦截，以极简轻量的单个 Shell 脚本构筑了工程资产免遭意外损毁的最后一道防火墙。

## Reading Coverage

已对本能力来源全部 2 篇规范文档与脚本完成 100% 逐行完整覆盖阅读：
1. `skills/git-guardrails-claude-code/SKILL.md`（共 95 行，完整覆盖能力定位、阻断清单、五步安装配置流程、项目级/全局级 settings.json 配置规范及验证方法）。
2. `skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh`（共 25 行，完整覆盖 stdin JSON 输入读取、jq 提取命令、9 大危险模式正则数组、grep 匹配循环、stderr 告警及退出码 2/0 协议）。
