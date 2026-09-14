# web-design-guidelines

## Problem
前端代码在快速迭代过程中极易引入违反 Web 界面规范的缺陷，例如可访问性（a11y）缺失、交互无障碍缺陷、排版与对比度违规以及不符合最佳实践的 UI 实现。开发者需要一种能够针对指定代码文件或 glob 模式进行自动化审查的机制，快速定位违规代码并输出紧凑精炼的定位清单。

## When to Use
- 用户明确请求审查前端 UI 代码、可访问性合规检查、设计走查或最佳实践审计时（如触发词："review my UI"、"check accessibility"、"audit design"、"review UX"、"check my site against best practices"）。
- 在前端代码提交流程或 CI/CD 审查阶段，需要按文件或文件模式进行规范审计时。
- 针对组件库、页面模版进行跨屏幕、无障碍及交互规范批量扫描时。

## When Not to Use
- 纯后端业务逻辑、数据库设计、运维基础设施或非 Web 界面相关代码的审查。
- 处于早期视觉概念探索或低保真草案阶段，尚未落地为可审查的代码文件时。
- 需要深入复杂的运行时状态调试或多页面端到端功能测试时（应使用 playwright 或 systematic-debugging）。

## Role
作为 Web 界面规范审查员与代码合规门禁执行器，负责接收待审查目标文件，拉取/引用 Web Interface Guidelines 规则集，逐项校验目标代码，并以标准紧凑格式输出精炼的问题诊断报告。

## Inputs
- `file-or-pattern`（参数/参数提示）：待审查的目标文件路径或 glob 文件匹配模式（例如 `src/components/**/*.tsx`）。若用户未显式提供，审查流程需交互式提示用户输入目标文件。
- Web Interface Guidelines 规范源：远端规范基线或本地缓存规范规则集。

## Outputs
- 采用紧凑的 `file:line` 格式输出的代码审查诊断清单，明确指出文件名、违规所在代码行号以及对应的界面规范违规描述与改进建议。

## Workflow
1. **参数解析与目标确认**：接收用户传入的文件路径或 glob 模式；若未提供，提示用户明确指定待审查代码文件。
2. **规范源获取**：通过 WebFetch 获取最新的 Web Interface Guidelines 规范内容（包含完整审查规则与输出格式指引）或读取本地镜像。
3. **文件读取与扫描**：定位并读取目标文件源码。
4. **规则应用与比对**：根据界面规范逐行/逐块核验目标代码中的语义化标签、属性配置、交互与无障碍细节。
5. **紧凑格式输出**：以 `file:line` 精简格式向用户汇总呈现审查发现与改进点。

## Branches
- **目标路径已提供分支**：直接加载目标文件列表，跳过交互提示，进入扫描与审查。
- **无目标参数分支**：暂停审查流程，向用户发出询问，要求补充待审查的目标文件或匹配模式后恢复流程。
- **单文件审查分支**：针对单个目标文件执行全量规则扫描。
- **批量/Glob 匹配分支**：展开所有匹配到的前端文件，按文件顺序执行审查并聚合诊断报告。

## Rules
- 必须遵循 Web Interface Guidelines 的全量规则清单进行合规性判定。
- 输出必须严格遵守精简紧凑的 `file:line` 定位格式，禁止无意义的套话与冗长铺垫。
- 每次审查前必须确保规则集为最新鲜有效的规范基线（Fetch fresh guidelines before each review）。
- 未指定目标文件时不得猜测或盲目扫描全库，必须明确提示用户指定范围。

## Exceptions
- 网络受限或离线环境：当无法通过 WebFetch 实时访问远端规范源时，必须平滑降级使用本地内置的 Web 界面规范或项目级设计规则。
- 目标路径无效或未匹配到文件：向用户明确反馈路径无效并终止审查，不得输出虚假通过报告。

## Dependencies
- 工具依赖：具备文件读取能力（Read）、模式匹配能力（Glob）以及网络获取能力（WebFetch 或本地等效回退）。
- 规范依赖：`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`。

## Permissions and Side Effects
- 只读权限：审查过程仅对工作区内的目标代码文件进行只读扫描，无文件修改、写入或删除副作用。
- 网络读取：若在线执行，会向 GitHub 发起规范文本的 GET 请求。

## Gates
- **目标文件确认 Gate**：待审查目标必须为真实存在的代码文件；文件未指定时必须完成用户交互确认。
- **格式合规 Gate**：输出报告中的每条缺陷项必须包含准确的 `file:line` 坐标定位与规则违反原因。

## Open Questions
- 在完全离线运行环境中，如何与本地设计系统规则库（如 ui-ux-pro-max 或 design-taste-frontend）建立规范同义映射与自动化规则回退机制。

## Unique Value
提供了极简、无侵入的 Web 界面规范代码级轻量审查协议，规范了输入参数模式（`<file-or-pattern>`）、统一拉取最新基准以及标准紧凑定位报告（`file:line`）的端到端自动化范式。

## Reading Coverage
覆盖并吸收源文件 `web-design-guidelines/SKILL.md` 全量内容（第 1 行至第 39 行），包括 Frontmatter 元数据定义、How It Works 机制、Guidelines Source 远端源说明及 Usage 交互与调用工作流。
