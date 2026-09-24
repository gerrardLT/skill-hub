"""Verify and summarize paired repeated holdout runs offline."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from tools.curation.eval_runner import _extract_status


CONFIGS = ("with_skill", "without_skill")


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _stats(values: list[float]) -> dict[str, float]:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1) if len(values) > 1 else 0.0
    return {
        "mean": round(mean, 4),
        "stddev": round(math.sqrt(variance), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def _validate_run(
    run_dir: Path,
    config: str,
    expected_reads: list[str] | None = None,
) -> tuple[dict[str, object] | None, str | None]:
    for name in ("full_output.md", "tool_evidence.raw.json", "timing.json"):
        if not (run_dir / name).is_file():
            return None, f"missing {name}"
    try:
        output = (run_dir / "full_output.md").read_text(encoding="utf-8")
        evidence = _load(run_dir / "tool_evidence.raw.json")
        timing = _load(run_dir / "timing.json")
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"invalid run artifact: {exc}"
    if not isinstance(evidence, dict) or not isinstance(timing, dict):
        return None, "evidence and timing must be objects"
    for field, expected in (
        ("offline", True),
        ("network_accessed", False),
        ("skills_modified", False),
        ("case_file_read", False),
        ("rubric_read", False),
    ):
        if evidence.get(field) is not expected:
            return None, f"invalid isolation field {field}"
    if config == "without_skill" and evidence.get("slots_read") is not False:
        return None, "baseline slots_read must be false"
    if evidence.get("errors") not in ([], None):
        return None, "agent errors recorded"
    if expected_reads is not None:
        actual_reads = evidence.get("paths_read")
        if not isinstance(actual_reads, list) or sorted(actual_reads) != sorted(expected_reads):
            return None, "paths_read does not match expected configuration"
    tokens = timing.get("total_tokens")
    duration_ms = timing.get("duration_ms")
    duration_seconds = timing.get("total_duration_seconds")
    if not isinstance(tokens, (int, float)) or isinstance(tokens, bool) or tokens < 0:
        return None, "invalid total_tokens"
    if not isinstance(duration_ms, (int, float)) or isinstance(duration_ms, bool) or duration_ms < 0:
        return None, "invalid duration_ms"
    if not isinstance(duration_seconds, (int, float)) or isinstance(duration_seconds, bool):
        return None, "invalid total_duration_seconds"
    if abs(duration_seconds - duration_ms / 1000) > 1e-9:
        return None, "duration fields disagree"
    status = _extract_status(output)
    if status is None:
        return None, "status not parseable"
    return {
        "status": status,
        "tokens": float(tokens),
        "duration_seconds": float(duration_seconds),
    }, None


def verify_variance(
    cases_path: Path | str,
    runs_root: Path | str,
    case_ids: list[str],
    minimum_pairs: int,
    expected_configuration: dict[str, dict[str, list[str]]] | None = None,
) -> dict[str, object]:
    data = _load(Path(cases_path))
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        return {"passed": False, "cases": [], "errors": ["cases array missing"]}
    case_map = {case.get("id"): case for case in cases if isinstance(case, dict)}
    root = Path(runs_root)
    errors: list[str] = []
    case_reports: list[dict[str, object]] = []

    for case_id in case_ids:
        case = case_map.get(case_id)
        if not isinstance(case, dict) or not isinstance(case.get("expected_status"), str):
            errors.append(f"{case_id}: case or expected_status missing")
            continue
        expected = case["expected_status"]
        numbers: set[int] = set()
        for config in CONFIGS:
            config_dir = root / case_id / config
            for run_dir in config_dir.glob("run-*"):
                try:
                    numbers.add(int(run_dir.name.split("-", 1)[1]))
                except ValueError:
                    continue
        included: list[dict[str, object]] = []
        excluded: list[dict[str, object]] = []
        for number in sorted(numbers):
            pair: dict[str, object] = {"run_number": number}
            pair_error = None
            for config in CONFIGS:
                expected_reads = None
                if expected_configuration is not None:
                    expected_reads = expected_configuration.get(case_id, {}).get(config)
                result, reason = _validate_run(
                    root / case_id / config / f"run-{number}",
                    config,
                    expected_reads,
                )
                if reason:
                    pair_error = f"{config}: {reason}"
                    break
                pair[config] = result
            if pair_error:
                excluded.append({"run_number": number, "reason": pair_error})
            else:
                included.append(pair)
        if len(included) < minimum_pairs:
            errors.append(f"{case_id}: only {len(included)} valid paired runs; require {minimum_pairs}")

        config_reports: dict[str, object] = {}
        for config in CONFIGS:
            valid = [pair[config] for pair in included]
            if valid:
                config_reports[config] = {
                    "statuses": [item["status"] for item in valid],
                    "status_match": _stats([1.0 if item["status"] == expected else 0.0 for item in valid]),
                    "time_seconds": _stats([item["duration_seconds"] for item in valid]),
                    "tokens": _stats([item["tokens"] for item in valid]),
                }
            else:
                config_reports[config] = None
        case_reports.append(
            {
                "case_id": case_id,
                "expected_status": expected,
                "paired_run_count": len(included),
                "included_run_numbers": [pair["run_number"] for pair in included],
                "excluded_pairs": excluded,
                **config_reports,
            }
        )

    return {"passed": not errors, "minimum_pairs": minimum_pairs, "cases": case_reports, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--minimum-pairs", type=int, default=2)
    parser.add_argument("--configuration", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    expected_configuration = _load(args.configuration) if args.configuration else None
    if expected_configuration is not None and not isinstance(expected_configuration, dict):
        parser.error("configuration JSON must contain an object")
    report = verify_variance(
        args.cases,
        args.runs_root,
        args.case_id,
        args.minimum_pairs,
        expected_configuration,
    )
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
