"""Generate exact Phase 3 semantic units for playwright-best-practices."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
UNITS_FILE = REPO_ROOT / "curation" / "units" / "playwright-best-practices.jsonl"

def get_excerpt(rel_path: str, start: int, end: int) -> str:
    full_path = SKILLS_DIR / rel_path
    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    selected = lines[start - 1 : end]
    return "\n".join(selected)

units_def = [
    # SKILL.md units (1-13)
    {
        "id": "playwright-best-practices:unit-001",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 18,
        "origin_line_end": 45,
        "type": "method",
        "meaning": "新建测试场景参考指南矩阵：涵盖 E2E、组件、API、GraphQL、视觉回归、POM 架构、数据夹具、鉴权、时钟模拟、文件操作、表单、拖拽、无障碍、安全、注解、标签、iframe、canvas、i18n、Electron 与浏览器扩展等 21 类场景的参考文件映射",
        "boundary_condition": "新建测试文件、用例设计或实现具体测试场景时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:test-scenarios-routing",
        "validation_criteria": "提供完整覆盖 21 种测试用例类型的最佳实践参考文件定位路由",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-002",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 46,
        "origin_line_end": 56,
        "type": "method",
        "meaning": "移动端与响应式测试参考指南：涵盖设备仿真（Device Emulation）、触摸手势（Swipe/Tap）、视口断点与移动端特定 UI 的参考映射",
        "boundary_condition": "测试移动设备视图、响应式断点或移动手势交互时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:mobile-responsive-testing",
        "validation_criteria": "涵盖移动视口模拟、触控手势及移动专属选择器规范",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-003",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 57,
        "origin_line_end": 70,
        "type": "method",
        "meaning": "实时通信与底层浏览器 API 测试指南：涵盖 WebSocket、地理位置 Mock、权限授予、剪贴板、音视频设备 Mock 及多标签页/OAuth 弹窗流",
        "boundary_condition": "涉及浏览器高级特性、底层权限与弹窗跨上下文交互时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:browser-apis-testing",
        "validation_criteria": "覆盖现代 Web 应用实时数据流与设备硬件 API 仿真要求",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-004",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 71,
        "origin_line_end": 86,
        "type": "method",
        "meaning": "测试调试与排障活动指南：涵盖测试失败诊断、偶发脆弱测试根治、并行运行排障、多 Worker 状态泄漏隔离、选择器修复、超时调查、Trace 查看器、竞态排查与控制台报错捕获",
        "boundary_condition": "当用例失败、选择器漂移、超时报错或测试在 CI 中不稳定时查阅",
        "dependency_skills": [],
        "candidate_destination": "debugging:playwright-troubleshooting",
        "validation_criteria": "涵盖导致端到端测试不稳定的 9 大核心诱因及对应排障文档",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-005",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 87,
        "origin_line_end": 99,
        "type": "method",
        "meaning": "异常与边界条件测试指南：涵盖前端 Error Boundary 错误边界、网络故障模拟、离线模式、Service Worker、加载中状态与表单校验",
        "boundary_condition": "验证系统健壮性、弱网降级、断网提示与极端输入边界时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:error-and-edge-testing",
        "validation_criteria": "确保对弱网、断网、组件崩溃等异常具备自动化回归能力",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-006",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 101,
        "origin_line_end": 110,
        "type": "method",
        "meaning": "多用户协同与权限测试指南：涵盖单用例多用户上下文并发、实时协同编辑、RBAC 角色权限验证与并发操作竞争测试",
        "boundary_condition": "涉及协作白板、协同文档、聊天应用或权限矩阵测试时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:multi-user-collaboration",
        "validation_criteria": "支持在同一测试中维护多个隔离的 BrowserContext 进行角色交互验证",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-007",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 111,
        "origin_line_end": 121,
        "type": "rule",
        "meaning": "测试架构决策准则：评估 Page Object Model 与 Fixtures 的适用边界、测试类型选型金字塔、Mock 服务与真实后端的边界划分，以及测试套件目录结构设计",
        "boundary_condition": "规划工程化测试套件架构、设计测试模式与制定技术选型时适用",
        "dependency_skills": [],
        "candidate_destination": "architecture:playwright-test-architecture",
        "validation_criteria": "指导测试代码工程化分层，避免过度封装与共享状态反模式",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-008",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 122,
        "origin_line_end": 132,
        "type": "method",
        "meaning": "主流前端框架专项测试参考：覆盖 React（虚拟 DOM 与水合）、Angular（Zone.js 异步与组件）、Vue/Nuxt 及 Next.js（服务端渲染与路由）的应用测试映射",
        "boundary_condition": "针对特定前端技术栈应用实施端到端与组件级测试时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:framework-specific-testing",
        "validation_criteria": "针对不同前端框架的异步渲染机制提供定制化的测试策略",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-009",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 133,
        "origin_line_end": 146,
        "type": "rule",
        "meaning": "测试重构与维护指南：将陈旧用例重构为 POM、优化测试目录、提取通用 Setup/Teardown 夹具、替换易碎选择器、彻底消除硬编码显式等待、建立测试数据工厂",
        "boundary_condition": "在代码评审、技术债治理或测试用例持续维护时执行",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:test-refactoring-guide",
        "validation_criteria": "降低测试维护成本，消除测试坏味道与潜在脆弱性",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-010",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 147,
        "origin_line_end": 166,
        "type": "method",
        "meaning": "基础设施与 CI/CD 配置指南：Playwright 项目配置、流水线搭建、GitHub Actions / GitLab CI / Docker、全局 Setup/Teardown、工程依赖编排、测试性能优化、并行分片（Sharding）、Worker 数据隔离、覆盖率与测试报告工件归档",
        "boundary_condition": "搭建或优化持续集成自动化测试流水线时查阅",
        "dependency_skills": [],
        "candidate_destination": "infrastructure:playwright-ci-cd",
        "validation_criteria": "提供高并发、高弹性、易排查的工程化 CI/CD 交付流水线支撑",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-011",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 167,
        "origin_line_end": 189,
        "type": "method",
        "meaning": "高级测试模式参考：Mock API 响应、网络请求拦截、GraphQL Mock、HAR 流量录制与回放、自定义 Fixtures 拓展、高级等待策略、三方服务 Mock（OAuth/支付/短信）、控制台报错阻断、安全防护验证、性能预算与 Web Vitals/Lighthouse、测试用例注解（skip/fixme/slow）与标签过滤",
        "boundary_condition": "实现高复杂度业务流程、性能契约与深度网络模拟时查阅",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:advanced-testing-patterns",
        "validation_criteria": "为复杂业务逻辑提供安全、性能与多协议深层交互测试能力",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-012",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 190,
        "origin_line_end": 291,
        "type": "method",
        "meaning": "快速决策树（Quick Decision Tree）：以树状结构全面映射新测试类型、特定功能测试、架构选型、框架集成、鉴权模式、脆弱测试诊断、异常场景、重构维护、基础设施与用例组织运行全分支",
        "boundary_condition": "面对具体工程任务快速定位对应最佳实践指南与文档时适用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:decision-tree-navigator",
        "validation_criteria": "毫秒级索引具体任务至目标参考文件，杜绝盲目试错",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-013",
        "source_path": "playwright-best-practices/SKILL.md",
        "origin_line_start": 293,
        "origin_line_end": 303,
        "type": "gate",
        "meaning": "测试闭环验证循环门禁（Test Validation Loop）：编写或修改用例后必须执行测试；失败时查阅 trace 精准修复；仅在全量通过后方可推进；核心用例必须使用 --repeat-each=5 检验稳定性",
        "boundary_condition": "任何测试用例新增或重构提交前的强制闭环准则",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:validation-loop-gate",
        "validation_criteria": "用例可重现、无脆弱性，并通过多轮重复测试验证方可放行",
        "status": "retain"
    },

    # Deep dive units from core references (14-26)
    {
        "id": "playwright-best-practices:unit-014",
        "source_path": "playwright-best-practices/core/locators.md",
        "origin_line_start": 16,
        "origin_line_end": 20,
        "type": "rule",
        "meaning": "高可用定位器推荐优先级：1. Role 角色定位（最稳健）> 2. Label 标签/占位符 > 3. 文本/标题 > 4. TestID 测试专用标识 > 5. CSS/XPath（绝对兜底手段）",
        "boundary_condition": "在所有自动化测试用例中选取元素定位器时全局强制遵守",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:locator-priority-rule",
        "validation_criteria": "从根本上降低由于前端样式重构、类名变动引起的测试脆弱断裂",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-015",
        "source_path": "playwright-best-practices/core/locators.md",
        "origin_line_start": 230,
        "origin_line_end": 237,
        "type": "rule",
        "meaning": "定位器反模式黑名单：严禁直接依赖实现类名（如 .btn-primary）、动态自动生成 ID（如 #dynamic-id-123）以及测试非用户可见的底层实现细节",
        "boundary_condition": "编写或代码审查定位器代码时的硬性合规标准",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:locator-anti-patterns",
        "validation_criteria": "拦截所有具有重构脆弱性的选择器，保持测试对实现解耦",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-016",
        "source_path": "playwright-best-practices/core/assertions-waiting.md",
        "origin_line_start": 12,
        "origin_line_end": 29,
        "type": "rule",
        "meaning": "Web-First 自动重试断言准则：强制优先使用由 expect(locator) 提供的具备自动轮询等待的断言（toBeVisible, toBeEnabled 等），直至条件达成或超时",
        "boundary_condition": "验证所有 DOM 状态与元素交互效果时强制遵守",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:web-first-assertions",
        "validation_criteria": "彻底根除因异步 DOM 渲染延迟导致的假阴性断言失败",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-017",
        "source_path": "playwright-best-practices/core/assertions-waiting.md",
        "origin_line_start": 349,
        "origin_line_end": 355,
        "type": "gate",
        "meaning": "等待反模式绝对禁令：严禁在用例中使用 page.waitForTimeout()、手动 Promise setTimeout 或在 DOM 元素上使用无重试的原生 JavaScript 断言",
        "boundary_condition": "测试用例合并入库前的硬性门禁审查",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:no-arbitrary-timeout-gate",
        "validation_criteria": "杜绝硬编码时间睡眠，防止测试执行周期膨胀与脆弱竞态",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-018",
        "source_path": "playwright-best-practices/core/fixtures-hooks.md",
        "origin_line_start": 12,
        "origin_line_end": 26,
        "type": "method",
        "meaning": "内置隔离测试夹具（Built-in Fixtures）核心机制：为每个测试用例注入完全隔离的 page、context、browser 与 request 实例，确保用例间零状态泄漏",
        "boundary_condition": "构建任何 Playwright 测试用例与执行环境时的底层保证",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:isolated-fixture-pattern",
        "validation_criteria": "确保每一个测试 Worker 与用例获得干净独立的浏览器上下文",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-019",
        "source_path": "playwright-best-practices/debugging/flaky-tests.md",
        "origin_line_start": 17,
        "origin_line_end": 25,
        "type": "rule",
        "meaning": "脆弱测试四大根因分类与症状分析模型：UI驱动型（缺少等待/动画未结束）、环境驱动型（CI硬件受限/网络变慢）、数据/并行驱动型（共享后端状态冲突）及测试套件驱动型（跨用例泄漏状态）",
        "boundary_condition": "排查测试偶发失败与构建不稳定问题时使用",
        "dependency_skills": [],
        "candidate_destination": "debugging:flakiness-classification-model",
        "validation_criteria": "将偶发报错精确归类并应用对应的针对性治理策略",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-020",
        "source_path": "playwright-best-practices/infrastructure-ci-cd/parallel-sharding.md",
        "origin_line_start": 1,
        "origin_line_end": 10,
        "type": "method",
        "meaning": "分片并行（Sharding）架构与模式：通过在 CI 多台机器间按比例切分用例执行，大幅缩短测试整体反馈周期，配套 Worker 级别的独立配置与防冲突指引",
        "boundary_condition": "在大型项目或流水线耗时过长时进行 CI 提速优化",
        "dependency_skills": [],
        "candidate_destination": "infrastructure:ci-sharding-pattern",
        "validation_criteria": "实现线性可扩展的多机并行测试执行并统一聚合报告",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-021",
        "source_path": "playwright-best-practices/testing-patterns/visual-regression.md",
        "origin_line_start": 14,
        "origin_line_end": 26,
        "type": "method",
        "meaning": "视觉回归测试核心模式：支持局部元素与全页截图对比（toHaveScreenshot），支持配置 maxDiffPixelRatio 像素容差并利用 mask 遮罩动态易变内容",
        "boundary_condition": "验证关键 UI 界面样式、图表渲染与组件像素级一致性时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:visual-regression-pattern",
        "validation_criteria": "在像素级回归验证中有效屏蔽时间戳等干扰因素，避免假警报",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-022",
        "source_path": "playwright-best-practices/advanced/authentication.md",
        "origin_line_start": 19,
        "origin_line_end": 29,
        "type": "method",
        "meaning": "鉴权状态持久化与复用模式（storageState）：通过单次登录或 API 登录将 Cookies 与 LocalStorage 保存为 JSON 状态文件，后续测试直接载入，免去重复 UI 登录操作",
        "boundary_condition": "所有需要已登录态的高频端到端测试用例基础设置",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:auth-storage-state-pattern",
        "validation_criteria": "缩减用例执行耗时 50% 以上，并避免登录接口的过载限流",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-023",
        "source_path": "playwright-best-practices/testing-patterns/accessibility.md",
        "origin_line_start": 21,
        "origin_line_end": 31,
        "type": "method",
        "meaning": "无障碍（A11y）合规自动化审计模式：集成 @axe-core/playwright，对渲染后页面执行 WCAG 规则扫描并断言零违规（violations 必须为空）",
        "boundary_condition": "验证产品合规性、屏幕阅读器支持与无障碍基线时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:accessibility-audit-pattern",
        "validation_criteria": "在流水线中自动化捕获色彩对比度不足、ARIA 属性缺失等无障碍缺陷",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-024",
        "source_path": "playwright-best-practices/browser-apis/websockets.md",
        "origin_line_start": 34,
        "origin_line_end": 46,
        "type": "method",
        "meaning": "WebSocket 实时通信帧监听与校验模式：在页面跳转前预挂载 websocket 监听器，捕获 framereceived 消息负载并结合 expect.poll 执行轮询断言",
        "boundary_condition": "验证实时推送、即时通讯、行情看板等双向 WebSocket 通信功能",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:websocket-testing-pattern",
        "validation_criteria": "稳定捕获异步双向数据帧，杜绝时序竞争导致的断言漏判",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-025",
        "source_path": "playwright-best-practices/testing-patterns/security-testing.md",
        "origin_line_start": 5,
        "origin_line_end": 14,
        "type": "method",
        "meaning": "自动化安全测试维度与 XSS 注入验证：覆盖反射型/存储型 XSS 防御、CSRF 校验、认证与鉴权越权探测、输入过滤及安全响应头合规",
        "boundary_condition": "在功能回归中同步自动化验证 Web 应用安全边界",
        "dependency_skills": [],
        "candidate_destination": "security:automated-security-testing",
        "validation_criteria": "在 UI 与网络层构建自动化的常见 Web 漏洞防御检验网",
        "status": "retain"
    },
    {
        "id": "playwright-best-practices:unit-026",
        "source_path": "playwright-best-practices/advanced/clock-mocking.md",
        "origin_line_start": 13,
        "origin_line_end": 25,
        "type": "method",
        "meaning": "时钟模拟与时间旅行（Clock Mocking）模式：在页面导航前调用 page.clock.install 锁定固定时间基准，并在测试中验证与时间相关的渲染逻辑",
        "boundary_condition": "测试倒计时、会话过期、定时任务、日历组件或特定日期促销场景",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:clock-mocking-pattern",
        "validation_criteria": "完全消除由于真实系统时间流动与时区差异导致的测试非确定性",
        "status": "retain"
    }
]

def main():
    UNITS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(UNITS_FILE, "w", encoding="utf-8") as f:
        for u in units_def:
            excerpt = get_excerpt(u["source_path"], u["origin_line_start"], u["origin_line_end"])
            record = {
                "id": u["id"],
                "source_path": u["source_path"],
                "origin_line_start": u["origin_line_start"],
                "origin_line_end": u["origin_line_end"],
                "type": u["type"],
                "raw_excerpt": excerpt,
                "meaning": u["meaning"],
                "boundary_condition": u["boundary_condition"],
                "dependency_skills": u["dependency_skills"],
                "candidate_destination": u["candidate_destination"],
                "validation_criteria": u["validation_criteria"],
                "status": u["status"]
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Generated {len(units_def)} units in {UNITS_FILE}")

if __name__ == "__main__":
    main()
