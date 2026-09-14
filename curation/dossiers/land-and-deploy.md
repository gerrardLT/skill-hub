# land-and-deploy 来源能力档案

## Problem

在现代软件工程中，从 PR 创建到代码最终安全合并并在生产环境生效，往往面临严重的操作与质量风险：合并未经充分测试或 CI 失败的分支导致生产事故；多开发者并发工作区合流导致版本号与 CHANGELOG 队列冲突漂移；缺乏对生产部署生命周期的自动追踪，导致部署失败未被及时发觉；发布后缺乏即时金丝雀验证与快速回滚能力，使线上故障扩散。传统发布依赖大量繁琐的手动 CLI 操作与人工盯盘，缺乏全自动化的合流前就绪度门禁、部署态势监听与确定性故障回滚机制。

## When to Use

- **PR 合并与全自动发布闭环**：承接 `/ship` 产物，自动解析关联 PR 并端到端管理合流、构建部署及线上验证。
- **发布基础设施试运行校验**：首次部署或配置变动时，自动探测部署工作流、平台 CLI 及预发环境并完成指纹审定。
- **并发版本冲突防范**：拦截多工作区并发合流导致的 VERSION 号抢占漂移，保障 CHANGELOG 演进线性有序。
- **生产环境单次健康金丝雀验证**：部署完成后立即探活线上站点，采集 HTTP 状态、控制台 Uncaught 错误、性能指标及带标注截图。
- **生产故障一键非破坏性回滚**：当部署失败或线上探针劣化时，快速执行 `git revert` 或生成回滚 PR 安全还原基线。

## When Not to Use

- **代码编写与功能分支单元测试开发阶段**：应使用 dev-loop 编码流程或 vitest/playwright 运行。
- **长时持续流量监控与灰度发布**：单次部署探针验证完成后应交由专用监控系统或 `/canary` 进行 10 分钟以上的长时观察。

## Role

发布工程与生产合流控制器（Release Engineer & Deployment Gatekeeper）。专职负责合流前状态审查、版本冲突拦截、合并触发、多云部署态势追踪、生产健康探针核验以及故障自动回滚。

## Inputs

- **PR 标识**：PR 编号（如 `#123`）或通过当前 Git 分支自动嗅探的关联 PR。
- **发布配置指纹**：`CLAUDE.md` 中的部署配置块与 `.github/workflows/` 中的部署流水线文件。
- **目标环境生产 URL**：从 CLI 参数传入或部署流水线输出中动态提取的线上探测基线地址。
- **平台认证状态**：GitHub CLI (`gh auth`) 或 GitLab CLI (`glab auth`) 的当前凭证。

## Outputs

- **代码合流提交或合并队列条目**：合并入主分支的代码提交，附带自动清理已合流特性分支。
- **部署结构化 ASCII 报表 (Land & Deploy Report)**：记录 PR 编号、合流 SHA、CI/队列/部署各项耗时、控制台错误统计及截图路径，归档于 `.gstack/deploy-reports/`。
- **生产健康探针证据**：`post-deploy.jpg` 全页截图与 `post-deploy-annotated.png` 标注图像。
- **紧急回滚产物（异常分支）**：Git 反向 revert 提交或针对受保护分支的自动化回滚 PR。

## Workflow

1. **Step 0 & 1: 平台探测与预检 (Platform & Pre-flight)**：
   - 探测宿主平台（GitHub/GitLab）与基线目标分支；验证 CLI 鉴权状态并检查 PR 开启状态。
2. **Step 1.5: 首运行试运行审定 (First-run Dry-run Validation)**：
   - 核验 `land-deploy-confirmed` 指纹；初次或配置变动时激活导师模式，全景探测并展示发布基础设施，经确认后保存指纹。
3. **Step 2 & 3: 合流前审查与 CI 等待 (Pre-merge Checks & CI Wait)**：
   - 检查 PR 冲突与 CI 检查状态；若 CI 仍处于 PENDING 则启动 `gh pr checks --watch --fail-fast` 阻塞等待（15 分钟超时）。
4. **Step 3.4: 版本号并发漂移拦截 (VERSION Drift Detection)**：
   - 比较当前分支 VERSION 与基线最新版本，防止兄弟工作区并发抢占；若冲突则安全阻断并提示在特性分支重走 `/ship`。
5. **Step 4 & 5: 执行合流与策略判定 (Merge Execution & Strategy Detection)**：
   - 依权限与配置执行自动合流/直接合流/队列合流，自动删除已合流分支；根据代码差异范围（文档/前端/后端/全量）判定部署及金丝雀深度。
6. **Step 6: 部署流水线监听 (Wait for Deploy)**：
   - 依检测策略（GitHub Actions 工作流 SHA 匹配、Fly.io/Render 等平台 CLI 或 HTTP 探活）按 30 秒间隔轮询部署状态。
7. **Step 7 & 8: 生产金丝雀核验与按需回滚 (Canary Verification & Revert)**：
   - 探针检查 HTTP 200、控制台无 Uncaught 错误、首屏真实内容及加载耗时（<10s）；若异常则提示并执行原子 `git revert`。
8. **Step 9 & 10: 输出部署报表与后续引导 (Deploy Report & Follow-ups)**：
   - 生成完整 ASCII 部署总结报表，归档结构化元数据，并建议 `/canary` 长时监控或文档同步。

## Branches

- **首次运行审定分支 (First-run Branch)**：哈希不存在或变动时，中断静默流程，读取 `first-run-validation.md` 执行交互确认。
- **合并队列分支 (Merge Queue Branch)**：若仓库启用了 GitHub Merge Queue，自动调用 `gh pr merge --auto` 进入排队等待。
- **版本冲突退出分支 (Drift Abort Branch)**：检测到版本槽已被抢占时，立即退出并保护元数据一致性。
- **故障回滚分支 (Revert Branch)**：金丝雀探针失败时，执行非破坏性回滚操作。

## Rules

- **无感分支清理规程**：PR 合并后必须携带 `--delete-branch` 清理特性分支，避免远端分支膨胀。
- **全程状态通报原则**：每一步操作均向开发者即时汇报进度与耗时，消除等待焦虑与黑盒风险。
- **智能轮询与指数退避**：云平台状态查询间隔至少 30 秒，防止撞击 API 速率上限。
- **金丝雀深度自适应**：纯文档改动跳过金丝雀；仅涉及后端服务跳过全页截图；前端变动执行完整图像与控制台录制。

## Exceptions

- **受保护分支无法直接推送回滚**：自动降级生成 `revert: <title>` PR 并引导人工审核合流。
- **无显式部署流水线项目**：跳过 Step 6 部署等待，直接根据目标 URL 执行金丝雀探活。

## Dependencies

- **GitHub CLI (`gh`)**：用于读取 PR 元数据、审查 CI 状态、执行合流及监听 GitHub Actions 工作流。
- **Aside / Chromium Headless**：用于执行页面加载、注入错误捕获钩子、采集性能与截图。
- **可选平台 CLI**：`flyctl`、`heroku`、`curl`。

## Permissions and Side Effects

- **权限要求**：Git 仓库写权限、GitHub PR 合并权限、浏览器渲染探测环境。
- **副作用**：向主分支合并代码、关闭并删除特性分支、触发线上 CI/CD 部署流水线、向线上地址发送 HTTP 探测请求。

## Gates

- **Gate 1: Pre-flight Auth & PR State Gate**：CLI 必须登录有效，PR 必须处于 OPEN 态且无合并冲突。
- **Gate 2: First-run Config Fingerprint Gate**：配置哈希漂移或初次运行时必须获得人工确认方可继续。
- **Gate 3: Pre-merge CI Green Gate**：所有必需 CI 检查必须为 PASS，严禁带病合流。
- **Gate 4: VERSION Slot Free Gate**：当前 PR 声明的版本号必须为下一个未占用的空闲版本。
- **Gate 5: Canary Health Assessment Gate**：页面必须 200 响应、加载 < 10 秒且无致命 Console 异常。

## Open Questions

- 针对蓝绿发布与灰度金丝雀环境，如何更精准地将流量探针定向到新版本实例而非旧缓存节点？
- 微服务多仓库联动发布时，跨仓库的依赖版本对齐如何建立原子锁定机制？

## Unique Value

打通了从 Pull Request 到最终生产服务健康运行的“最后一公里”。通过首运行指纹审查、CI 阻塞轮询、版本漂移拦截、全自动多平台部署监听、生产金丝雀探针及一键 Git 回滚，构建了企业级高可用发布防线。

## Reading Coverage

本能力档案已 100% 覆盖以下来源文件及全套子模块：
- `skills/land-and-deploy/SKILL.md` (核心编排骨架与各步骤详细定义)
- `skills/land-and-deploy/SKILL.md.tmpl`
- `skills/land-and-deploy/sections/first-run-validation.md` (首运行试运行规范)
- `skills/land-and-deploy/sections/first-run-validation.md.tmpl`
- `skills/land-and-deploy/sections/manifest.json` (子模块清单索引)
- `skills/land-and-deploy/sections/merge-and-deploy.md` (合流与部署监听规范)
- `skills/land-and-deploy/sections/merge-and-deploy.md.tmpl`
- `skills/land-and-deploy/sections/readiness-gate.md` (合流前就绪度门禁)
- `skills/land-and-deploy/sections/readiness-gate.md.tmpl`
