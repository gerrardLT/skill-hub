# -*- coding: utf-8 -*-
"""
Generator for canary semantic units.
Extracts verbatim excerpts from skills/canary/SKILL.md
and validates each unit according to Phase 3 schema (12-key format).
"""

import json
import pathlib
import sys

sys.path.insert(0, "tools/curation")
from verify import verify_unit

def extract_lines(file_path: str, start: int, end: int) -> str:
    path = pathlib.Path("skills") / file_path
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1:end])

def build_units():
    units_def = [
        # 1. canary:unit-001 (gate: setup and directory initialization gate)
        {
            "id": "canary:unit-001",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 537,
            "origin_line_end": 547,
            "type": "gate",
            "meaning": "金丝雀探针运行环境与报告目录初始化门禁：解析项目 Slug 并初始化 canary-reports、baselines 与 screenshots 存储拓扑，设置默认监测时长与页面发现模式",
            "boundary_condition": "执行任何金丝雀基线采集或监控之前的初始化阶段",
            "dependency_skills": [],
            "candidate_destination": "canary:setup-and-directory-initialization",
            "validation_criteria": "本地报表与截图目录正确建立，参数合法解析",
            "status": "retain"
        },
        # 2. canary:unit-002 (method: baseline capture with error hook and performance timing)
        {
            "id": "canary:unit-002",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 548,
            "origin_line_end": 574,
            "type": "method",
            "meaning": "发布前生产质量基线捕获方法：在部署前注入全局控制台与未捕获异常监听钩子，抓取页面导航计时、文本切片与全页截图，落盘 baseline.json",
            "boundary_condition": "发布前携带 --baseline 参数运行时的基线抓取阶段",
            "dependency_skills": [],
            "candidate_destination": "canary:baseline-capture-engine",
            "validation_criteria": "成功生成包含截图、错误基数与加载耗时的基线配置并提示用户推进部署",
            "status": "retain"
        },
        # 3. canary:unit-003 (method: safe same-origin page discovery with action filtering)
        {
            "id": "canary:unit-003",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 593,
            "origin_line_end": 614,
            "type": "method",
            "meaning": "同源安全路由自动发现与敏感动作过滤方法：抓取首页同源链接并剔除注销、删除、退订等危险动作，提取 Top 5 核心导航供用户确认",
            "boundary_condition": "未显式指定 --pages 参数时的自动化路由探测阶段",
            "dependency_skills": [],
            "candidate_destination": "canary:safe-page-discovery",
            "validation_criteria": "安全筛选出同源有效页面，不触发任何破坏性状态变更",
            "status": "retain"
        },
        # 4. canary:unit-004 (method: continuous stateless monitoring loop)
        {
            "id": "canary:unit-004",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 625,
            "origin_line_end": 646,
            "type": "method",
            "meaning": "无状态高频金丝雀轮询监听方法：在监测周期内每 60 秒为各页面开启全新上下文，重新注入错误捕获钩子并采集新鲜截图与性能数据",
            "boundary_condition": "部署后持续长时观察阶段的执行循环",
            "dependency_skills": [],
            "candidate_destination": "canary:continuous-monitoring-loop",
            "validation_criteria": "按 60 秒固定周期无状态采集页面真实状态与新鲜证据",
            "status": "retain"
        },
        # 5. canary:unit-005 (rule: differential alerting and severity classification)
        {
            "id": "canary:unit-005",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 647,
            "origin_line_end": 655,
            "type": "rule",
            "meaning": "相对差分告警与严重度分级规则：只对相对基线产生的新增控制台异常、2倍以上耗时退化或页面加载崩溃报警，基线已有错误不误报",
            "boundary_condition": "单次轮询数据采集后的差分异常计算阶段",
            "dependency_skills": [],
            "candidate_destination": "canary:differential-alerting-rules",
            "validation_criteria": "准确识别相对基线的劣化，排除恒定旧缺陷造成的误报干扰",
            "status": "retain"
        },
        # 6. canary:unit-006 (gate: transient tolerance and two-strike alert gate)
        {
            "id": "canary:unit-006",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 656,
            "origin_line_end": 678,
            "type": "gate",
            "meaning": "瞬时抖动容忍与双击持续告警门禁：单次网络偶发抖动不告警，仅当缺陷在连续 2 次及以上检查中持续出现时才弹出严重报警并提供回滚决策",
            "boundary_condition": "触发高危用户中断警报前的容错校验门禁",
            "dependency_skills": [],
            "candidate_destination": "canary:transient-tolerance-gate",
            "validation_criteria": "过滤偶发单次网络噪点，仅在故障持续时弹出结构化警报",
            "status": "retain"
        },
        # 7. canary:unit-007 (rule: health report generation and metric logging)
        {
            "id": "canary:unit-007",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 680,
            "origin_line_end": 714,
            "type": "rule",
            "meaning": "金丝雀健康总结报表生成与度量归档规则：监测完成后输出包含各页面健康状态、平均耗时与告警统计的结构化报表并持久化写入项目日志",
            "boundary_condition": "监控结束或用户提前终止时的收尾报告阶段",
            "dependency_skills": [],
            "candidate_destination": "canary:health-report-and-metrics",
            "validation_criteria": "生成 ASCII/Markdown/JSON 多形态报表，准确给出线上健康终验裁决",
            "status": "retain"
        },
        # 8. canary:unit-008 (rule: baseline update and iteration protocol)
        {
            "id": "canary:unit-008",
            "source_path": "canary/SKILL.md",
            "origin_line_start": 715,
            "origin_line_end": 725,
            "type": "rule",
            "meaning": "生产基线迭代更新规程：当本次发布被确认健康无误后，交互引导用户将最新截图与性能指标更新为新的长期基准指纹",
            "boundary_condition": "发布健康终验完成后的基线生命周期维护",
            "dependency_skills": [],
            "candidate_destination": "canary:baseline-update-protocol",
            "validation_criteria": "在用户授权下原子更新 baseline.json 与基准截图，保障基线时效性",
            "status": "retain"
        }
    ]

    units = []
    for item in units_def:
        raw_excerpt = extract_lines(
            item["source_path"],
            item["origin_line_start"],
            item["origin_line_end"]
        )
        unit = {
            "id": item["id"],
            "source_path": item["source_path"],
            "origin_line_start": item["origin_line_start"],
            "origin_line_end": item["origin_line_end"],
            "type": item["type"],
            "raw_excerpt": raw_excerpt,
            "meaning": item["meaning"],
            "boundary_condition": item["boundary_condition"],
            "dependency_skills": item["dependency_skills"],
            "candidate_destination": item["candidate_destination"],
            "validation_criteria": item["validation_criteria"],
            "status": item["status"]
        }
        units.append(unit)

    return units

def main():
    skills_root = pathlib.Path("skills")
    units = build_units()
    print(f"Building {len(units)} units for canary...")

    output_path = pathlib.Path("curation/units/canary.jsonl")
    lines = []
    for u in units:
        errs, matches = verify_unit(u, skills_root)
        if errs or not matches:
            print(f"Unit {u['id']} validation failed: {errs}, matches={matches}")
            sys.exit(1)
        lines.append(json.dumps(u, ensure_ascii=False))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Successfully generated and validated {len(units)} units into {output_path}")

if __name__ == "__main__":
    main()
