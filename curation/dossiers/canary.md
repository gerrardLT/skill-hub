# canary 来源能力档案

## Problem

在现代软件交付后，传统发布流水线往往在部署脚本退出（Exit code 0）后即认定发布成功。然而，线上环境经常在部署后出现隐蔽而致命的次生故障：CDN 缓存未清理导致静态资源 404、后端接口 Schema 漂移导致前端静默抛出未捕获异常（Uncaught Exception）、客户端渲染水合（Hydration）失败导致白屏、关键业务页面响应耗时倍增。缺乏发布前基线比对与发布后持续长时监控，导致这些问题往往在真实用户投诉后才被发觉，极大增加了平均恢复时间（MTTR）。

## When to Use

- **生产发布后的长时灰度与稳定性监控**：在 `/land-and-deploy` 部署完成后，针对关键业务路由持续监控 10-30 分钟。
- **发布前基线数据采集与指纹归档**：在部署前执行 `--baseline`，捕获各核心页面的真实渲染截图、控制台错误数与性能基线。
- **关键页面自动发现与健康巡检**：自动扫描并过滤同源顶级导航链接，自动排除登出、注销等敏感危险动作。
- **基于相对差异（Differential）的生产告警**：杜绝绝对指标误报，仅对相对基线产生的新增控制台异常、2倍以上耗时退化或页面加载崩溃执行报警。
- **故障快速识别与回滚联动决策**：在捕获严重劣化时立即呈现实时证据与截图，提供一键回滚、深入调查或继续观测选项。

## When Not to Use

- **本地静态代码质量检查或单元测试**：应使用 vitest 或 eslint。
- **全站 SEO、技术标签与无障碍大范围爬虫审计**：应使用 audit-website。
- **代码合并与远程部署流程驱动**：应由 `/ship` 与 `/land-and-deploy` 处理。

## Role

生产金丝雀监控与线上健康守护者（Production Canary Observer & Health Guard）。专职负责捕获发布前质量基线、自动发现关键导航路由、执行发布后持续多页面探针轮询、进行相对差分回归告警并输出结构化健康报表。

## Inputs

- **监控目标网址 (Base URL)**：如 `https://example.com`。
- **监控持续时长**：默认 10 分钟，支持 `--duration 5m`（1m 至 30m）。
- **监控页面集合**：由 `--pages` 显式指定，或通过 Phase 3 自动发现的同源核心路由。
- **运行模式选项**：`--baseline`（仅抓取发布前基线）、`--quick`（单次快速探针核验）。

## Outputs

- **基线快照与元数据**：`.gstack/canary-reports/baselines/*.jpg` 与 `baseline.json`（包含时间戳、分支、各页面错误数与加载耗时）。
- **巡检过程视觉截图**：`.gstack/canary-reports/screenshots/<page>-<check-number>.jpg`。
- **金丝雀警报 (Canary Alert)**：发生连续 2 次以上异常时向用户呈现实时差异对比与证据路径。
- **终验健康报表 (Canary Report)**：Markdown 与 JSON 格式的 ASCII 结构化汇总报表，归档于 `.gstack/canary-reports/`。
- **项目级度量记录**：写入 `~/.gstack/projects/$SLUG` 的 JSONL 历史日志。

## Workflow

1. **Phase 1: 环境与目录初始化 (Setup)**：
   - 提取项目 Slug，创建 `.gstack/canary-reports` 及其 baselines 与 screenshots 子目录；解析参数与监控时长。
2. **Phase 2: 发布前基线抓取 (Baseline Capture)**：
   - 若携带 `--baseline`，注入全局错误捕获钩子，访问目标页面，记录错误数、导航计时（PerformanceNavigationTiming）、页面文本切片与整页截图，落盘 `baseline.json` 后退出。
3. **Phase 3: 页面自动发现 (Page Discovery)**：
   - 若未显式提供 `--pages`，通过探针扫描首页所有同源 `a[href]` 链接，过滤 `logout|signout|delete|remove|cancel` 等敏感动作，提取 Top 5 核心导航供用户选择。
4. **Phase 4: 预部署快照补全 (Pre-Deploy Snapshot)**：
   - 若先前未保存 `baseline.json`，则在持续监控前为待测页面现场抓取一份参考快照。
5. **Phase 5: 持续探针监听循环 (Continuous Monitoring Loop)**：
   - 在设定期限内每 60 秒轮询一次待测页面，无状态独立开启新标签，重新注入错误钩子、采集性能与截图。
   - 差分比对：判定页面崩溃（Critical）、新增控制台错误（High）、性能劣化超 2 倍（Medium）、新增死链（Low）。
   - 瞬时容错判定：仅当同一问题在连续 2 次及以上检查中复现时才判定为真实警报，弹出 AskUserQuestion 决策对话。
6. **Phase 6: 健康报表输出与归档 (Health Report)**：
   - 监控结束或提前终止时，输出包含各页面状态（HEALTHY/DEGRADED/BROKEN）、平均加载耗时与告警统计的结构化报表。
7. **Phase 7: 基线迭代更新 (Baseline Update)**：
   - 若本次发布被确认健康，提示用户是否用当前最新截图更新持久化基线库。

## Branches

- **发布前基线模式分支 (Baseline Mode Branch)**：执行 Phase 2 后直接终止，提示用户完成部署后再启动监控。
- **快速单次核验分支 (Quick Mode Branch)**：执行单次多页面快速扫描后直接输出报表，不进入长时循环。
- **严重警报拦截分支 (Critical Alert Branch)**：检测到生产白屏或服务不可用时，立即挂起并给出立即回滚选项。

## Rules

- **相对差分告警原则 (Alert on changes, not absolutes)**：只对相对基线产生的新增缺陷报警；基线已有错误保持恒定时不误报。
- **瞬时网络抖动容忍铁律 (Transient Tolerance)**：单次偶发网络超时或微小抖动不触发警报，必须跨 2 次及以上连续检查复现才告警。
- **截图即凭证原则 (Screenshots are evidence)**：所有告警与健康判定必须绑定磁盘上的真实截图路径。
- **无破坏纯只读观测原则 (Read-only observation)**：仅作为只读旁路探针，严禁在页面执行消费、删除或破坏性交互。
- **性能基准倍率原则**：耗时超过基线 2 倍以上确认为性能回归，1.5 倍以内视为正常网络波动。

## Exceptions

- **无头浏览器缺失或环境受限**：降级为自带 Headless Chromium 或执行纯 HTTP 状态码与耗时探活。
- **外链与第三方埋点干扰**：错误捕获钩子优先过滤非本域脚本抛出的跨域混杂错误。

## Dependencies

- **Aside AI Browser / Headless Chromium**：执行页面真实渲染、DOM 查询与整页截图。
- **Node.js / Bash / jq**：驱动脚本解析与指标持久化。

## Permissions and Side Effects

- **权限要求**：网络 HTTP/HTTPS 访问权限、本地报表与截图目录写权限。
- **副作用**：以 60 秒为周期向目标站点发起页面加载请求，在 `.gstack/canary-reports` 生成图片与 JSON 数据。

## Gates

- **Gate 1: Pre-monitoring Target Reachable Gate**：目标站点必须能够成功建立 HTTP 连接。
- **Gate 2: Two-Strike Persistence Gate**：任何非致命异常必须满足“连续两次命中”方可通过告警判定门禁。
- **Gate 3: Baseline Comparison Gate**：无基线状态下只能作为单次探活，强制提示用户建立 baseline。

## Open Questions

- 针对需要复杂手机验证码或硬件 Key 鉴权的后台深层页面，如何更安全地传递免密会话而不污染审计环境？
- 在单页应用客户端路由跳转与服务端完整刷新混合场景下，如何自适应区分导航计时口径？

## Unique Value

彻底打破了“CI 跑通即代表发布健康”的盲目假设。通过“发布前基线指纹抓取 -> 敏感动作安全过滤 -> 60秒无状态差分轮询 -> 连续异常精准告警 -> 终验截图存证”的完整闭环，为生产环境发布构建了免误报、高保真的自动化哨兵。

## Reading Coverage

本能力档案已 100% 覆盖以下来源文件：
- `skills/canary/SKILL.md` (全套 7 阶段操作流程、监听循环与核心规则)
- `skills/canary/SKILL.md.tmpl`
