"""Generate exact Phase 3 semantic units for audit-website."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
UNITS_FILE = REPO_ROOT / "curation" / "units" / "audit-website.jsonl"

def get_excerpt(rel_path: str, start: int, end: int) -> str:
    full_path = SKILLS_DIR / rel_path
    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    selected = lines[start - 1 : end]
    return "\n".join(selected)

units_def = [
    # File 1: audit-website/SKILL.md
    {
        "id": "audit-website:unit-001",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 12,
        "origin_line_end": 16,
        "type": "gate",
        "meaning": "定义 audit-website 核心能力定位与环境强依赖门禁：依赖 PATH 中可执行的 squirrel CLI 命令行工具，前置通过 squirrel --version 校验",
        "boundary_condition": "执行全站体检与修复前必须通过环境门禁",
        "dependency_skills": [],
        "candidate_destination": "environment:squirrel-cli-prerequisite",
        "validation_criteria": "确认 squirrel CLI 已安装且可在终端直接调用",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-002",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 18,
        "origin_line_end": 23,
        "type": "rule",
        "meaning": "全网 260+ 条规则在线文档定位标准 URL 规范：通过 https://docs.squirrelscan.com/rules/{rule_category}/{rule_id} 精确查阅规则详情",
        "boundary_condition": "需要向用户解释特定规则背景或排障修复方案时查阅",
        "dependency_skills": [],
        "candidate_destination": "reference:audit-rule-documentation",
        "validation_criteria": "提供统一的规则分类与标识符在线文档路由规范",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-003",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 24,
        "origin_line_end": 34,
        "type": "tool-action",
        "meaning": "执行网站审计核心指令规范：使用 --format llm 紧凑格式，优先审计真实线上地址以反映真实渲染/重定向，支持基于本地缓存无网络重渲染",
        "boundary_condition": "发起任何站点审计或重新解析历史审计时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:website-audit-invocation",
        "validation_criteria": "携带 --format llm 产出 agent 优化报告，并优先选用线上环境执行",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-004",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 35,
        "origin_line_end": 49,
        "type": "method",
        "meaning": "扫描覆盖演进三阶段模型（quick 25页快速概览 -> surface 100页模板覆盖 -> full 500页终验），配套刷新控制与 Web Bot Auth 反爬鉴权头配置",
        "boundary_condition": "根据测试推进阶段动态选择爬取深度与认证参数",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:scan-progression-model",
        "validation_criteria": "按需合理分配爬取页数上限，突破 Cloudflare/Shopify 机器人阻断",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-005",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 50,
        "origin_line_end": 60,
        "type": "method",
        "meaning": "迭代修复飞轮六步法（呈现报告 -> 提案确认 -> 映射源码 -> 批量修复 -> 二次复测 -> 达标迭代）及批次构建校验强约束",
        "boundary_condition": "将审计报告转化为代码修复的全流程必须严格遵循此循环",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:iterative-fix-loop",
        "validation_criteria": "每次改动前后有分数对比，修改前有确认，改动后验证静态构建通过",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-006",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 61,
        "origin_line_end": 73,
        "type": "rule",
        "meaning": "健康分阶梯目标与缺陷处理准则：分级目标定义、严格先 error 后高权重 warning、内容修改与代码同等对待、死链必须人工决策禁止臆造删除",
        "boundary_condition": "制定修复目标与排序缺陷治理优先级时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:audit-score-targets-policy",
        "validation_criteria": "明确不同起始分数的治理目标线，严禁对死链进行私自删除",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-007",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 74,
        "origin_line_end": 82,
        "type": "tool-action",
        "meaning": "历史回归对比与退化检验指令：通过 --diff <baseline-id> 或 --regression-since 对比两次审计差异，捕获新增退化缺陷",
        "boundary_condition": "版本上线前或大规模重构后验证质量退化时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:regression-diff-verification",
        "validation_criteria": "直接输出两份审计记录之间的指纹级缺陷增量对比",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-008",
        "source_path": "audit-website/SKILL.md",
        "origin_line_start": 83,
        "origin_line_end": 86,
        "type": "gate",
        "meaning": "审计治理完结签署门禁（Definition of Done）：所有 error 必须修复、warning 修复或已明确归档、二次审计验证提升、用户已获得前后对比汇报",
        "boundary_condition": "任务标记完成前的终审卡点",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:audit-completion-gate",
        "validation_criteria": "满足四大完备性准则，杜绝未经验证的草率收尾",
        "status": "retain"
    },

    # File 2: audit-website/references/OUTPUT-FORMAT.md
    {
        "id": "audit-website:unit-009",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 3,
        "origin_line_end": 15,
        "type": "rule",
        "meaning": "LLM 格式设计特征与 Token 压缩标准：比冗长 XML 缩减 40-70% 体积，采用 1 空格缩进、混合 XML+前缀文本、属性内联与扁平层级",
        "boundary_condition": "在 AI Agent 消费审计数据时作为输出解析基准",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:llm-format-characteristics",
        "validation_criteria": "在兼顾结构化解析精度的同时极大降低 Context 窗口占用",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-010",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 18,
        "origin_line_end": 50,
        "type": "template",
        "meaning": "报告根节点、站点信息与综合健康分 XML 结构定义：<audit> 根标签、<site> 抓取元数据及 <score> 综合得分与分项子分类",
        "boundary_condition": "解析审计元数据与总览健康评级时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:audit-header-score-template",
        "validation_criteria": "准确提取 overall 分数、等级与各核心分类独立得分",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-011",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 51,
        "origin_line_end": 61,
        "type": "template",
        "meaning": "全站检查摘要统计标签规范：<summary passed='...' warnings='...' failed='...'/>",
        "boundary_condition": "获取检查项通过与失败总数统计时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:audit-summary-template",
        "validation_criteria": "提供高层级的通过与失败数量看板",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-012",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 63,
        "origin_line_end": 88,
        "type": "template",
        "meaning": "缺陷列表分区与按分类分组结构：<issues> 包含多个按分类分组的 <category> 节点及其 errors/warnings 汇总",
        "boundary_condition": "按业务分类检索问题列表时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:issues-category-template",
        "validation_criteria": "清晰呈现 Core SEO、Performance、Technical 等各大维度的缺陷归属",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-013",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 90,
        "origin_line_end": 106,
        "type": "template",
        "meaning": "具体规则项（<rule>）内部结构规范：包含 id/severity/status 属性，以及按序排列的 Message、Desc、Fix、Pages(n)、Items(n) 文本内容",
        "boundary_condition": "解析单项具体缺陷与修复建议时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:rule-element-template",
        "validation_criteria": "为代码修改提供精准的修复措施、描述与受波及页面清单",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-014",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 107,
        "origin_line_end": 122,
        "type": "template",
        "meaning": "受影响元素（Items）明细格式语法：包含主要标识符（URL/选择器）、可选人类可读标签、方括号元数据键值及来源页面溯源 (from: ...)",
        "boundary_condition": "定位具体死链来源、重复标题出现位置或异常元素时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:items-format-template",
        "validation_criteria": "提供精确的上下游关联线索，支持定位到代码或内容具体行",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-015",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 123,
        "origin_line_end": 160,
        "type": "template",
        "meaning": "回归对比 Diff 输出格式规范：包含 baseline/current 属性对比、summary 统计、added 新增缺陷、removed 移除项与 changed/regression 退化明细",
        "boundary_condition": "自动化解析版本回归报告时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:audit-diff-template",
        "validation_criteria": "通过 fp 确定性指纹准确判定缺陷是在修复还是发生恶化",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-016",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 189,
        "origin_line_end": 206,
        "type": "tool-action",
        "meaning": "LLM 格式调用方式与管道串联模式：单步直接输出（squirrel audit --format llm）、两步工作流（audit 后 report）以及直接管道输送给 AI 代理",
        "boundary_condition": "在自动化脚本中编排 squirrel CLI 审计流程时使用",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:llm-format-usage",
        "validation_criteria": "支持终端交互与自动化流水线无缝集成",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-017",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 207,
        "origin_line_end": 215,
        "type": "rule",
        "meaning": "报告格式选型对比矩阵：xml（企业级全量归档）、llm（AI 代理极致压缩）、json（程序化处理）与 text（简单流处理）",
        "boundary_condition": "针对不同调用方选择最优的输出格式",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:output-format-selection",
        "validation_criteria": "在 AI 场景下坚定选用 llm 格式，在企业归档选用 xml",
        "status": "retain"
    },
    {
        "id": "audit-website:unit-018",
        "source_path": "audit-website/references/OUTPUT-FORMAT.md",
        "origin_line_start": 235,
        "origin_line_end": 244,
        "type": "rule",
        "meaning": "LLM 格式设计哲学五大支柱：Token 效率、高可靠 XML 解析、自然语言可读性、渐进式信息展开（Summary -> Category -> Rule -> Item）与内联可执行建议",
        "boundary_condition": "指导大模型消费审计报告与进行自然交互时遵循的认知模型",
        "dependency_skills": [],
        "candidate_destination": "quality-assurance:design-philosophy-pillars",
        "validation_criteria": "确保 Agent 能够自顶向下逐层下钻并输出高执行度的修改行动",
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
