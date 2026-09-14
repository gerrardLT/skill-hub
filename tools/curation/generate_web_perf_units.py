#!/usr/bin/env python3
"""
Generate curation semantic units for web-perf.
Extracts units from skills/web-perf/SKILL.md.
"""

import json
import sys
from pathlib import Path

SKILLS_ROOT = Path("skills")
UNITS_ROOT = Path("curation/units")

def extract_lines(file_rel_path: str, start: int, end: int) -> str:
    full_path = SKILLS_ROOT / file_rel_path
    lines = full_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1:end])

def main():
    UNITS_ROOT.mkdir(parents=True, exist_ok=True)
    out_file = UNITS_ROOT / "web-perf.jsonl"

    units_def = [
        # 1. web-perf:unit-001 (rule: assertive and evidence-based performance recommendations)
        {
            "id": "web-perf:unit-001",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 33,
            "origin_line_end": 39,
            "type": "rule",
            "meaning": "性能审计实证与收益量化核心准则：通过网络抓包与 DOM 校验事实并明确断言、确认资源完全无用后再建议移除、严格量化收益毫秒/字节并忽略 0ms 无效改动、对指标卓越（如 LCP<200ms）的站点直接认可无需过度优化",
            "boundary_condition": "性能审计全流程的专业判断与建议过滤准则",
            "dependency_skills": [],
            "candidate_destination": "perf:audit-discipline-and-impact-rule",
            "validation_criteria": "建议具备精确体积或毫秒收益估算，排除无影响的非问题",
            "status": "retain"
        },
        # 2. web-perf:unit-002 (method: 5-phase audit workflow)
        {
            "id": "web-perf:unit-002",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 56,
            "origin_line_end": 62,
            "type": "method",
            "meaning": "Web 性能五阶段全景审计流水线：依次执行性能冷加载 Trace 抓取、Core Web Vitals 洞察解析（含 CLS 元凶）、网络请求全链路分析、无障碍树快照与前端源码工程级打包分析",
            "boundary_condition": "执行完整网站性能体检的标准操作规程",
            "dependency_skills": [],
            "candidate_destination": "perf:five-phase-audit-workflow",
            "validation_criteria": "步骤覆盖运行时 Trace、指标归因、网络链路与源码构建四维度",
            "status": "retain"
        },
        # 3. web-perf:unit-003 (rule: core web vitals key thresholds)
        {
            "id": "web-perf:unit-003",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 103,
            "origin_line_end": 110,
            "type": "rule",
            "meaning": "Core Web Vitals 官方核心指标阈值标准：TTFB（<800ms/<1.8s）、FCP（<1.8s/<3s）、LCP（<2.5s/<4s）、INP（<200ms/<500ms）、TBT（<200ms/<600ms）、CLS（<0.1/<0.25）及 Speed Index（<3.4s/<5.8s）三档判定线",
            "boundary_condition": "量化评估网页加载与交互体验优劣的标准阈值",
            "dependency_skills": [],
            "candidate_destination": "perf:web-vitals-thresholds",
            "validation_criteria": "评级必须严格对照官方 good/needs-improvement/poor 分段区间",
            "status": "retain"
        },
        # 4. web-perf:unit-004 (method: network request diagnostic checklist)
        {
            "id": "web-perf:unit-004",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 119,
            "origin_line_end": 126,
            "type": "method",
            "meaning": "网络链路排查六大检查项：审查 head 内无 async/defer 属性的渲染阻塞资源、次级瀑布流依赖链（CSS import/JS 字体）、关键素材预加载缺失、弱缓存头、大体积未压缩包及无请求的废弃 preconnect",
            "boundary_condition": "网络资源加载瀑布流与 HTTP 传输效率专项诊断",
            "dependency_skills": [],
            "candidate_destination": "perf:network-analysis-checklist",
            "validation_criteria": "全量覆盖阻塞、依赖链、预加载、缓存、包体积及预连接六大点",
            "status": "retain"
        },
        # 5. web-perf:unit-005 (method: frontend codebase build optimization analysis)
        {
            "id": "web-perf:unit-005",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 150,
            "origin_line_end": 193,
            "type": "method",
            "meaning": "前端源码与构建配置优化审查法：自动探测构建工具（Webpack/Vite/Next.js/Astro），排查 Tree-shaking 边界（如 barrel 文件与全量引用）、CSS 冗余清洗（Tailwind content）、Babel 垫片与 core-js 膨胀、静态资源压缩与 Source Map 泄露",
            "boundary_condition": "拥有代码库访问权限时对编译产物与工程构建配置进行调优",
            "dependency_skills": [],
            "candidate_destination": "perf:codebase-build-optimization",
            "validation_criteria": "针对不同打包工具给出精确到文件与选项的工程级改造方案",
            "status": "retain"
        },
        # 6. web-perf:unit-006 (template: audit report structure)
        {
            "id": "web-perf:unit-006",
            "source_path": "web-perf/SKILL.md",
            "origin_line_start": 194,
            "origin_line_end": 200,
            "type": "template",
            "meaning": "性能审计交付三段式输出结构模板：包含 Core Web Vitals 汇总表（含实测值与官方评级）、按影响程度排期的 Top Issues 缺陷清单，以及带代码片段和配置示例的具体修复建议",
            "boundary_condition": "输出面向工程师与产品团队的性能审计结论",
            "dependency_skills": [],
            "candidate_destination": "perf:audit-report-template",
            "validation_criteria": "输出结构必须包含指标表、优先级清单与可执行代码配置建议",
            "status": "retain"
        }
    ]

    for u in units_def:
        u["raw_excerpt"] = extract_lines(u["source_path"], u["origin_line_start"], u["origin_line_end"])

    with open(out_file, "w", encoding="utf-8") as f:
        for u in units_def:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    print(f"Generated {len(units_def)} units for web-perf at {out_file}")

if __name__ == "__main__":
    main()
