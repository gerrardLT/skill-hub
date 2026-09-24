#!/usr/bin/env python3
"""
Generate curation semantic units for llm-evaluation.
Extracts units from skills/llm-evaluation/SKILL.md and skills/llm-evaluation/references/details.md.
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
    out_file = UNITS_ROOT / "llm-evaluation.jsonl"

    units_def = [
        # 1. llm-evaluation:unit-001 (method: core evaluation types taxonomy)
        {
            "id": "llm-evaluation:unit-001",
            "source_path": "llm-evaluation/SKILL.md",
            "origin_line_start": 20,
            "origin_line_end": 71,
            "type": "method",
            "meaning": "LLM 三维评测体系全景分类法：涵盖自动化指标（文本生成 BLEU/ROUGE/BERTScore、分类 F1/AUC、RAG 检索 MRR/NDCG）、人工专家评测（准确性、连贯性、相关性、流畅度、安全性、有益度）及 LLM-as-Judge（Pointwise/Pairwise/Reference-based/Reference-free）",
            "boundary_condition": "评估大语言模型系统质量时的多维度策略框架",
            "dependency_skills": [],
            "candidate_destination": "eval:evaluation-types-taxonomy",
            "validation_criteria": "覆盖自动化度量、人工标注与大模型裁判三种互补评测范式",
            "status": "retain"
        },
        # 2. llm-evaluation:unit-002 (template: evaluation suite architecture)
        {
            "id": "llm-evaluation:unit-002",
            "source_path": "llm-evaluation/SKILL.md",
            "origin_line_start": 74,
            "origin_line_end": 140,
            "type": "template",
            "meaning": "可扩展 EvaluationSuite 评测套件代码模板：通过封装 Metric 数据结构与异步 evaluate 执行流水线，并发驱动大模型预测并批量计算聚合均值与样本原始得分",
            "boundary_condition": "工程化集成多维指标进行批量模型推理打分",
            "dependency_skills": [],
            "candidate_destination": "eval:evaluation-suite-architecture",
            "validation_criteria": "支持内置指标与自定义 metric 回调，返回指标平均数与原始得分字典",
            "status": "retain"
        },
        # 3. llm-evaluation:unit-003 (method: automated nlp metrics implementation)
        {
            "id": "llm-evaluation:unit-003",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 5,
            "origin_line_end": 64,
            "type": "method",
            "meaning": "传统 NLP 与深度语义重合度指标实现规程：包含带平滑函数的 BLEU 翻译重合度、ROUGE 摘要召回 F1，以及基于 DeBERTa 预训练模型的 BERTScore 深度语义表征相似度计算",
            "boundary_condition": "针对标准参考答案计算字面与语义重合度",
            "dependency_skills": [],
            "candidate_destination": "eval:automated-nlp-metrics",
            "validation_criteria": "输出规范的 precision/recall/f1 或平滑后 0-1 float 得分",
            "status": "retain"
        },
        # 4. llm-evaluation:unit-004 (rule: groundedness and factuality verification)
        {
            "id": "llm-evaluation:unit-004",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 68,
            "origin_line_end": 103,
            "type": "rule",
            "meaning": "基于 NLI 模型的真实性与上下文溯源严谨性规则：利用 DeBERTa/BART 蕴含分类器验证大模型生成内容是否被上下文严格蕴含（Entailment），不可推导的断言判定为幻觉并置零",
            "boundary_condition": "RAG 检索增强系统回答的忠实度与真实性核验",
            "dependency_skills": [],
            "candidate_destination": "eval:groundedness-and-factuality-rule",
            "validation_criteria": "将文本蕴含置信度作为衡量幻觉的量化门禁",
            "status": "retain"
        },
        # 5. llm-evaluation:unit-005 (template: single output llm judge)
        {
            "id": "llm-evaluation:unit-005",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 109,
            "origin_line_end": 154,
            "type": "template",
            "meaning": "单回答 LLM-as-Judge 质量打分结构模板：借助 Pydantic QualityRating 强制模型输出 1-10 范围的准确性、有益性、清晰度评分以及强制性文字打分理由（Reasoning）",
            "boundary_condition": "无确定标准答案时的开放式大模型输出质量单点评审",
            "dependency_skills": [],
            "candidate_destination": "eval:single-output-judge-template",
            "validation_criteria": "输出严格校验的 JSON 对象，必须包含数值评分与理由依据",
            "status": "retain"
        },
        # 6. llm-evaluation:unit-006 (template: pairwise comparison llm judge)
        {
            "id": "llm-evaluation:unit-006",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 158,
            "origin_line_end": 199,
            "type": "template",
            "meaning": "双样本配对优选裁判模板（Pairwise Judge）：输入两个变体回答让大模型对比判定胜负（A/B/tie），输出决策分析与 1-10 置信度，消除绝对打分的尺度漂移",
            "boundary_condition": "模型选型、Prompt 版本迭代优劣对比",
            "dependency_skills": [],
            "candidate_destination": "eval:pairwise-judge-template",
            "validation_criteria": "给出明确的胜者判定与置信度评价",
            "status": "retain"
        },
        # 7. llm-evaluation:unit-007 (method: human annotation and inter-rater agreement)
        {
            "id": "llm-evaluation:unit-007",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 251,
            "origin_line_end": 320,
            "type": "method",
            "meaning": "人工评估表单与跨标注员一致性（Cohen's Kappa）核验流程：规范多维标注任务，通过计算 Cohen's Kappa 分级评估两名标注员打分一致性，低于 0.4 时判定一致性不足需重构标准",
            "boundary_condition": "人工评审与真实标注任务质量管理",
            "dependency_skills": [],
            "candidate_destination": "eval:inter-rater-agreement-kappa",
            "validation_criteria": "输出精确的 Kappa 统计值与对应的定性解释级别（Poor 至 Almost Perfect）",
            "status": "retain"
        },
        # 8. llm-evaluation:unit-008 (rule: statistical ab testing and effect size)
        {
            "id": "llm-evaluation:unit-008",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 326,
            "origin_line_end": 381,
            "type": "rule",
            "meaning": "统计学 A/B 假设检验与效应量铁律：在评测两个模型变体表现时，必须执行独立双样本 t 检验输出 p 值（阈值 alpha=0.05）并计算 Cohen's d 效应量，严禁在无统计显著性时宣布变体胜出",
            "boundary_condition": "严谨评定 A/B 实验优胜者的准则",
            "dependency_skills": [],
            "candidate_destination": "eval:statistical-ab-testing-rule",
            "validation_criteria": "提供 p-value 显著性判定与 Cohen's d 效应量规模定级（negligible/small/medium/large）",
            "status": "retain"
        },
        # 9. llm-evaluation:unit-009 (gate: regression detection guard)
        {
            "id": "llm-evaluation:unit-009",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 387,
            "origin_line_end": 433,
            "type": "gate",
            "meaning": "模型版本性能退化阻断门禁（Regression Detector）：对比新版模型与基线得分，当任何核心指标相对跌幅超过预设阈值（如 5%）时，立即触发回归告警并阻断发布",
            "boundary_condition": "发布前持续集成门禁检查",
            "dependency_skills": [],
            "candidate_destination": "eval:regression-detector-guard",
            "validation_criteria": "准确识别相对跌幅超过 threshold 的指标并输出回归摘要清单",
            "status": "retain"
        },
        # 10. llm-evaluation:unit-010 (method: benchmark dataset execution and statistics aggregation)
        {
            "id": "llm-evaluation:unit-010",
            "source_path": "llm-evaluation/references/details.md",
            "origin_line_start": 479,
            "origin_line_end": 527,
            "type": "method",
            "meaning": "基准测试集执行与统计分布聚合机制：遍历 Benchmark 数据集批量测试，按指标聚合均值（mean）、标准差（std）、最小值与最大值，输出 BenchmarkResult 结构体",
            "boundary_condition": "对模型整体表现进行基准统计建模",
            "dependency_skills": [],
            "candidate_destination": "eval:benchmark-runner-aggregation",
            "validation_criteria": "完整产出每个指标的均值、方差及极值分布",
            "status": "retain"
        }
    ]

    for u in units_def:
        u["raw_excerpt"] = extract_lines(u["source_path"], u["origin_line_start"], u["origin_line_end"])

    with open(out_file, "w", encoding="utf-8") as f:
        for u in units_def:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    print(f"Generated {len(units_def)} units for llm-evaluation at {out_file}")

if __name__ == "__main__":
    main()
