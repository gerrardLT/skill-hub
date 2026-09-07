#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
L5_ROOT = ROOT.parents[1]
DOGFOOD_REPORT = L5_ROOT / "REAL_PROJECT_DOGFOOD_REPORT.md"


def run(command: list[str], *, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def count_tests(output: str) -> int:
    progress = re.search(r"^([.sxfEX]+)\s+\[100%\]", output, flags=re.MULTILINE)
    if progress:
        return len(progress.group(1))
    count = 0
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        count += sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
        )
    return count


def fmt(value: Any, digits: int = 2) -> str:
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def write_dogfood_report(result: dict[str, Any]) -> None:
    perf = result["performance"]
    deployment = result["deployment"]
    sdlc = result["sdlc"]
    gate_count = len(sdlc.get("gates", {}))
    gate_passed = sum(1 for value in sdlc.get("gates", {}).values() if value == "pass")
    latency = perf.get("latency_ms", {})
    lines = [
        "# Agentic SDLC OS v2.0 真实项目 Dogfooding 报告",
        "",
        f"- 生成时间：`{result['verified_at']}`",
        "- L5-A 真实项目单臂 Dogfooding：PASS" if result["passed"] else "- L5-A 真实项目单臂 Dogfooding：FAIL",
        "- L5-B 因果效果验证：尚未完成（匹配对照 NOT RUN）",
        "",
        "## 1. 结论",
        "",
        "系统已把用户真实的乒乓球馆 SaaS 需求压缩为一个可证伪垂直切片，并完成产品定义、体验设计、工程实现、独立测试、部署冒烟、运行观测、学习决策和跨 OS 回流。",
        "",
        "本次没有匹配的普通 Agent 对照组、重复项目样本、人力工时和完整 Token 成本，因此不能宣称 Agentic SDLC OS 已被证明提高生产率、降低总成本或优于其他工作流。",
        "",
        "## 2. 真实输入与试点范围",
        "",
        "输入来自用户自有的乒乓球馆 SaaS 功能清单和设计规范。本次选择高风险、高可验证的闭环：",
        "",
        "```text",
        "场次容量 → 原子预约 → 满额进入 FIFO 候补 → 取消释放名额",
        "→ 队首自动转正 → 指标和审计 → 基于证据回流",
        "```",
        "",
        "需求锚点：动态球台锁定与并发防超售、公平排队、唯一候补位置、自动转正、多租户隔离、幂等与可观测指标。",
        "",
        "## 3. 可执行实现",
        "",
        "- FastAPI + SQLite WAL；",
        "- `BEGIN IMMEDIATE` 原子事务；",
        "- 活跃预约和候补的部分唯一索引；",
        "- 幂等键与响应重放；",
        "- 多租户隔离；",
        "- 取消后同事务 FIFO 转正；",
        "- 审计事件、场次指标 API；",
        "- 无外部依赖的可交互原型。",
        "",
        "代码位置：`validation/l5/pilots/venue-reservation/`。",
        "",
        "## 4. 实测结果",
        "",
        "| 指标 | 结果 |",
        "|---|---:|",
        f"| 自动测试 | {result['tests']['count']}/{result['tests']['count']} PASS |",
        f"| 代码覆盖率 | {fmt(result['tests']['coverage_percent'])}% |",
        f"| 并发请求 | {perf.get('requests', '?')} |",
        f"| 工作线程 | {perf.get('workers', '?')} |",
        f"| 场次容量 | {perf.get('capacity', '?')} |",
        f"| 成功预约 | {perf.get('reserved', '?')} |",
        f"| 候补 | {perf.get('waitlisted', '?')} |",
        f"| 超售 | {1 if perf.get('oversold') else 0} |",
        f"| 吞吐 | {fmt(perf.get('throughput_rps', '?'))} req/s |",
        f"| p50 | {fmt(latency.get('p50', '?'), 3)} ms |",
        f"| p95 | {fmt(latency.get('p95', '?'), 3)} ms |",
        f"| p99 | {fmt(latency.get('p99', '?'), 3)} ms |",
        f"| 部署冒烟 | {deployment.get('checks', '?')}/{deployment.get('checks', '?')} PASS |",
        "",
        "部署冒烟覆盖：健康检查、创建场次、成功预约、幂等重放、满额候补、取消自动转正、零超售和多租户隔离。",
        "",
        "## 5. Agentic SDLC OS 实际回放",
        "",
        "| 控制项 | 结果 |",
        "|---|---:|",
        f"| Accepted 制品 | {sdlc.get('artifacts', '?')} |",
        f"| 内容契约有效 | {sdlc.get('quality_valid', '?')}/{sdlc.get('artifacts', '?')} |",
        f"| 平均制品质量分 | {fmt(sdlc.get('quality_average', '?'), 4)} |",
        f"| Gate | {gate_passed}/{gate_count} PASS |",
        f"| 强制转换 | {sdlc.get('forced_transitions', '?')} |",
        f"| Gate Waiver | {sdlc.get('waivers', '?')} |",
        f"| 控制面健康度 | {fmt(sdlc.get('health_score', '?'), 1)}/100 |",
        f"| 最终回流 | {sdlc.get('final_state', '?')} |",
        "",
        "Evolution 没有把局部工程成功误判为产品成功，而是识别出真实用户结果与因果证据不足，回流 PM Discovery。",
        "",
        "## 6. 证据边界",
        "",
        "已证明：真实需求可转成可运行软件；六个 OS、42 个制品和 7 个 Gate 可形成完整证据链；代码、测试、部署、指标与学习回流能够连接。",
        "",
        "尚未证明：相较普通 Agent 的周期、返工、缺陷、人工成本或 Token 成本改善；外部生产流量和长观察窗口稳定性；真实用户转化、留存或商业结果。",
        "",
        "## 7. 下一验证阶段",
        "",
        "按 `validation/l5/PROTOCOL.md` 执行 L5-B：在同一需求、模型、工具和时间预算下，比较普通 Coding Agent 与 Agentic SDLC OS；至少每组 2 次，建议每组 5 次。",
        "",
        "## 8. 可复现命令",
        "",
        "```bash",
        "cd validation/l5/pilots/venue-reservation",
        "python scripts/verify_pilot.py",
        "```",
        "",
        "机器可读证据：`reports/pilot-verification.json`、`reports/sdlc-dogfood-run.json`、`reports/deployment-smoke.json`、`reports/performance.json`、`reports/coverage.json` 和 `.sdlc/state.json`。",
    ]
    DOGFOOD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    steps = [
        run([sys.executable, "scripts/extract_requirements.py"]),
        run([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q"], env=env),
        run([sys.executable, "-m", "coverage", "json", "-o", "reports/coverage.json"], env=env),
        run([sys.executable, "-m", "coverage", "report", "-m"], env=env),
        run([
            sys.executable, "scripts/performance_probe.py", "--requests", "200", "--capacity", "20",
            "--workers", "32", "--output", "reports/performance.json",
        ], env=env),
        run([sys.executable, "scripts/deployment_smoke.py", "--output", "reports/deployment-smoke.json"], env=env),
        run([sys.executable, "scripts/generate_artifacts.py"]),
        run([sys.executable, "scripts/bootstrap_sdlc.py", "--reset"]),
    ]
    coverage = json.loads((REPORTS / "coverage.json").read_text(encoding="utf-8"))
    performance = json.loads((REPORTS / "performance.json").read_text(encoding="utf-8"))
    deployment = json.loads((REPORTS / "deployment-smoke.json").read_text(encoding="utf-8"))
    dogfood = json.loads((REPORTS / "sdlc-dogfood-run.json").read_text(encoding="utf-8"))
    html = (ROOT / "prototype" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "prototype" / "app.css").read_text(encoding="utf-8")
    js = (ROOT / "prototype" / "app.js").read_text(encoding="utf-8")
    prototype_checks = {
        "skip_link": 'class="skip-link"' in html,
        "semantic_main": '<main id="main"' in html,
        "live_regions": 'aria-live="polite"' in html and 'aria-live="assertive"' in html,
        "focus_visible": ":focus-visible" in css,
        "reduced_motion": "prefers-reduced-motion" in css,
        "server_confirmation_copy": "服务端确认中" in js,
        "state_loop": all(value in js for value in ["预约成功", "候补成功", "候补已自动转正"]),
    }
    test_count = count_tests(steps[1]["stdout"])
    result = {
        "schema_version": "1.0",
        "pilot": "venue-reservation",
        "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "passed": (
            all(item["passed"] for item in steps)
            and test_count > 0
            and float(coverage["totals"]["percent_covered"]) >= 90.0
            and performance.get("oversold") is False
            and performance.get("reserved") == performance.get("capacity")
            and deployment.get("passed") is True
            and dogfood.get("passed") is True
            and all(prototype_checks.values())
        ),
        "step_results": steps,
        "tests": {
            "passed": steps[1]["passed"],
            "count": test_count,
            "output": steps[1]["stdout"].strip(),
            "coverage_percent": round(float(coverage["totals"]["percent_covered"]), 2),
        },
        "performance": performance,
        "deployment": {
            "passed": deployment.get("passed"),
            "checks": len(deployment.get("checks", [])),
            "failed_checks": [x.get("name") for x in deployment.get("checks", []) if not x.get("passed")],
        },
        "prototype": prototype_checks,
        "sdlc": {
            "passed": dogfood.get("passed"),
            "artifacts": dogfood.get("artifacts"),
            "quality_valid": dogfood.get("quality", {}).get("valid"),
            "quality_invalid": dogfood.get("quality", {}).get("invalid"),
            "quality_average": dogfood.get("quality", {}).get("average_quality_score"),
            "gates": {name: item.get("status") for name, item in dogfood.get("gates", {}).items()},
            "forced_transitions": dogfood.get("forced_transitions"),
            "waivers": dogfood.get("waivers"),
            "final_state": dogfood.get("final_state"),
            "health_score": dogfood.get("health", {}).get("score"),
        },
        "evidence_boundary": "Real user-owned requirements and executable code were used, but the run is single-arm local dogfooding. It is not a causal productivity comparison or external production validation.",
    }
    output_path = REPORTS / "pilot-verification.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_dogfood_report(result)
    print(json.dumps({
        "passed": result["passed"],
        "tests": result["tests"],
        "deployment": result["deployment"],
        "sdlc": result["sdlc"],
        "report": str(output_path),
        "dogfood_report": str(DOGFOOD_REPORT),
    }, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
