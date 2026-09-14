# code-review 来源能力档案

## Problem

在代码合并进入主干分支前，仅凭自动化单元测试或 CI 编译检查无法完全识别深层次的代码隐患（如 OWASP Top 10 安全漏洞、N+1 数据库查询、高并发竞态条件、内存与资源泄漏、边缘异常未兜底及代码可维护性退化）。若缺乏系统化的结构化代码审查机制，高危安全缺陷与性能衰退往往会直接渗透至生产环境，导致高昂的修复成本与线上事故。

## When to Use

- **合并前代码安全性与质量审计（主要场景）**：当用户提交 PR URL、diff 补丁或指定文件路径，并请求“review this before I merge”或“is this code safe?”时。
- **专项性能隐患排查**：重点审查高频热点路径中的 N+1 查询、O(n²) 算法复杂度、缺失数据库索引及无界循环/查询。
- **安全合规深度扫描**：检测 SQL 注入、XSS、CSRF、权限与越权漏洞、明文硬编码密钥、不安全反序列化及路径穿越。
- **正确性与边界排查**：识别空指针、溢出、并发竞态、资源泄漏及错误传播丢失。

## When Not to Use

- **代码架构深层重构设计**：需要重新划分模块边界或下沉深层模块的架构设计工作（应使用 `codebase-design` 或 `improve-codebase-architecture`）。
- **自动化实时单元测试用例生成**：专门编写单元或集成测试用例（应使用 `test-driven-development` 或 `testing-strategy`）。

## Role

主任代码审查员与安全性能专家（Principal Code Reviewer & Security/Performance Auditor）。以多维结构化审查透镜，对代码变更实施涵盖安全性、性能表现、逻辑正确性与可维护性的全方位严苛审查，并输出具备确凿代码行列标记与可执行建议的裁决报告。

## Inputs

- **待审代码变更集（Code Target）**：PR URL（自动拉取差异）、本地 Git diff 文本或具体待审源文件路径（`@$1`）。
- **审查重点与上下文（可选）**：用户指定的关注重点（如“Focus on security”或“This is a hot path dealing with PII”）。
- **扩展连接器上下文（可选）**：版本控制系统（CI 状态与自动拉取）、任务追踪系统（关联 Issue/需求）、团队知识库（编码规范与样式指南）。

## Outputs

1. **结构化 Markdown 审查报告**：
   - 概览摘要（Summary，1-2 句变更与整体质量综述）。
   - 严重问题清单（Critical Issues 表格：序号、文件、行号、问题描述、红色严重度标识）。
   - 优化建议清单（Suggestions 表格：序号、文件、行号、建议内容、分类归属）。
   - 积极实践发现（What Looks Good，值得肯定的优秀代码设计）。
   - 终审裁决（Verdict：`Approve`、`Request Changes` 或 `Needs Discussion`）。
2. **带具体代码示例的可执行修复建议**：针对每个重大缺陷附带重构对比或补丁代码片段。

## Workflow

1. **获取代码目标与上下文（Acquire Target & Context）**：
   - 解析传入的 PR URL、diff 或文件路径；若未提供则主动询问。
   - 读取相关联的改动代码与伴随测试用例。
2. **独立多维交叉审查（Multidimensional Audit）**：
   - **安全维度（Security）**：核验 OWASP 核心威胁（SQL/XSS/CSRF/SSRF）、身份鉴权边界、密钥凭据硬编码、反序列化与路径穿越。
   - **性能维度（Performance）**：排查 ORM N+1 查询、热点路径算法复杂度（O(n²)）、内存非必要分配、缺失索引、无界查询及未关闭资源句柄。
   - **正确性维度（Correctness）**：验证空值/溢出等极端边界、并发竞态条件、错误向上传播链、差一错误（Off-by-one）及类型安全。
   - **可维护性维度（Maintainability）**：评估命名自解释性、单一职责原则、冗余代码、测试覆盖度及关键逻辑文档注释。
3. **严重度分类与影响定级（Triage Findings）**：
   - 阻断性破坏、安全漏洞与崩溃评定为 `Critical Issues`。
   - 优化建议与重构点评定为 `Suggestions`。
4. **生成审查报告与裁决建议（Format Report & Issue Verdict）**：
   - 组装包含摘要、缺陷表、建议表、优秀实践及终审裁决（Approve / Request Changes / Needs Discussion）的统一格式报告。

## Branches

- **独立单机审查分支（Standalone Branch，默认基线）**：基于用户粘贴的 diff、文件路径直接离线静态分析，不依赖外部集成环境，立即可用。
- **超强集成审查分支（Supercharged Branch）**：当连接 Source Control（GitHub/GitLab）、Project Tracker（Jira/Linear）或团队 Knowledge Base 时，自动抓取远端 PR 差异、校验 CI 测试状态并比对团队代码规约。

## Rules

- **结构化输出规则**：必须按固定 Markdown 模板输出，严禁随意自由散落发散评价。
- **精准行列证据原则**：每条 Critical Issue 与 Suggestion 必须明确指出具体的文件名与所在行号，并说明破坏影响与修复方案。
- **平衡建设性反馈原则**：审查不仅指出缺陷，还必须设立专门的“What Looks Good”章节肯定团队良好工程实践。
- **客观裁决原则**：裁决结果必须与 Critical Issues 严格匹配：存在任一未修复 Critical Issue 时严禁给出 Approve 裁决。

## Exceptions

- **缺少上下文时的降级提示**：若用户未指定审查关注点，需提醒用户提供背景信息（如是否为热点链路、是否涉及敏感数据）以深化审查效果。
- **外部连接器不可用降级**：若未配置 GitHub 等连接器，自动降级为 Standalone 纯本地模式，不影响核心审查能力。

## Dependencies

- **系统核心分析工具**：Read、Grep 等文件检索与代码阅读能力。
- **宿主 Git 环境**：在处理 PR 或分支 diff 时调用 `git diff`。

## Permissions and Side Effects

- **权限要求**：只读权限，无需对被审查文件进行写入修改。
- **副作用**：无代码库写入副作用；若连接了远端平台，可能向 PR 或 Issue 系统追加审查评论。

## Gates

- **Gate 1: Target Resolution Gate**：必须先确认有效的代码审查对象（文件、diff 或 PR），未明确时必须先完成澄清。
- **Gate 2: Critical Zero for Approve Gate**：若存在任何一条 Critical Issue，Verdict 必须标记为 `Request Changes` 或 `Needs Discussion`，绝对禁止判定为 `Approve`。
- **Gate 3: Actionable Fix Gate**：对列入 Critical 的问题必须给出明确的修复逻辑或代码示例，避免无指导性的空泛指责。

## Open Questions

- 在跨几十个微服务的大型多仓库（monorepo/polyrepo）复杂变更中，如何自动追踪接口契约向下游级联的破坏性影响？
- 如何在审查中兼顾团队自定义的技术债务容忍度（如明确声明的临时原型期代码）？

## Unique Value

建立了集安全性、性能、正确性与可维护性于一体的四维全景审查视盘。将碎片化的人工 Code Review 规范化为包含行列定位、严重度定级、正向反馈与最终裁决的可审计工程资产，有效筑牢进入主干分支前的质量堤坝。

## Reading Coverage

已对本能力来源全部规范文件完成 100% 逐行完整覆盖阅读：
1. `skills/code-review/SKILL.md`（共 119 行，完整覆盖能力定位、调用语法、单机与增强模式说明、安全/性能/正确性/可维护性四大审查维度、标准 Markdown 报告输出格式、连接器扩展及上下文提示最佳实践）。
