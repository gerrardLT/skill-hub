"""Deterministic, offline-only evaluator for curated run artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_REQUIRED_FIELDS = (
    "case_id",
    "source_skill",
    "full_output",
    "tool_evidence",
    "model",
    "input_hash",
    "tool_permissions",
    "budget",
    "duration_ms",
    "token_usage",
    "exit_status",
    "failure_reason",
)
NETWORK_PERMISSION_WORDS = ("network", "internet", "web", "http", "browser")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def _status_value(value: str) -> str | None:
    normalized = _normalized(value.strip(" *_`#:-"))
    if re.match(r"^needs[ -]?input\b", normalized):
        return "needs-input"
    if re.match(r"^blocked\b", normalized):
        return "blocked"
    if re.match(r"^failed\b", normalized):
        return "failed"
    if re.match(r"^(?:pass|passed|ready)\b", normalized):
        return "passed"
    return None


def _extract_status(text: str) -> str | None:
    lines = text.splitlines()
    for index, raw_line in enumerate(lines[:80]):
        line = re.sub(r"[*_`]", "", raw_line).lstrip("#").strip()
        inline = re.match(r"^(?:overall\s+)?status\s*:\s*(.+)$", line, flags=re.IGNORECASE)
        if inline:
            return _status_value(inline.group(1))
        if line.casefold() in {"status", "overall status"}:
            for candidate in lines[index + 1:index + 5]:
                if candidate.strip():
                    return _status_value(candidate)
    return None


def _cases(path: Path) -> list[dict[str, Any]]:
    data = _load_json(path)
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        raise ValueError("cases JSON must contain a cases array")
    return cases


def _manifest_for(cases_path: Path, explicit: Path | None) -> Path | None:
    if explicit is not None:
        return explicit
    for parent in cases_path.resolve().parents:
        candidate = parent / "evals.json"
        if candidate.is_file():
            return candidate
    return None


def _required_fields(manifest_path: Path | None) -> tuple[str, ...]:
    if manifest_path is None:
        return DEFAULT_REQUIRED_FIELDS
    manifest = _load_json(manifest_path)
    baseline = manifest.get("baseline") if isinstance(manifest, dict) else None
    if not isinstance(baseline, dict) or baseline.get("required") is not True:
        raise ValueError("eval manifest must require a baseline")
    fields = baseline.get("must_record")
    if not isinstance(fields, list) or not fields or not all(isinstance(x, str) for x in fields):
        raise ValueError("baseline.must_record must be a non-empty string array")
    missing_semantics = set(DEFAULT_REQUIRED_FIELDS) - set(fields)
    if missing_semantics:
        raise ValueError(
            "baseline.must_record omits required fields: " + ", ".join(sorted(missing_semantics))
        )
    return tuple(fields)


def _artifact(run_dir: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"missing {label} path")
        return None
    candidate = (run_dir / value).resolve()
    try:
        candidate.relative_to(run_dir.resolve())
    except ValueError:
        errors.append(f"{label} path escapes case directory")
        return None
    if not candidate.is_file():
        errors.append(f"missing {label}")
        return None
    return candidate


def _verify_case(case: dict[str, Any], runs_root: Path, required: tuple[str, ...]) -> dict[str, Any]:
    case_id = case.get("id")
    errors: list[str] = []
    result: dict[str, Any] = {"case_id": case_id, "valid": False, "errors": errors}
    if not isinstance(case_id, str) or not case_id:
        errors.append("case has no valid id")
        return result
    run_dir = runs_root / case_id
    run_path = run_dir / "run.json"
    if not run_path.is_file():
        errors.append("missing run.json")
        return result
    try:
        run = _load_json(run_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid run.json: {exc}")
        return result
    if not isinstance(run, dict):
        errors.append("run.json must contain an object")
        return result
    for field in required:
        if field not in run:
            errors.append(f"missing required run field: {field}")
    if run.get("case_id") != case_id:
        errors.append("run case_id does not match case")
    prompt = case.get("prompt")
    expected_prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest() if isinstance(prompt, str) else None
    if expected_prompt_hash is None or run.get("input_hash") != expected_prompt_hash:
        errors.append("prompt SHA-256 mismatch")

    output_path = _artifact(run_dir, run.get("full_output"), "full_output.md", errors)
    evidence_path = _artifact(run_dir, run.get("tool_evidence"), "tool_evidence.json", errors)
    for label, path, field in (
        ("full_output.md", output_path, "full_output_sha256"),
        ("tool_evidence.json", evidence_path, "tool_evidence_sha256"),
    ):
        expected = run.get(field)
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"missing or invalid {label} hash")
        elif path is not None and _sha256(path) != expected:
            errors.append(f"{label} hash mismatch")

    permissions = run.get("tool_permissions")
    if not isinstance(permissions, list) or any(
        not isinstance(permission, str) for permission in permissions
    ):
        errors.append("tool_permissions must be a string array")
    elif any(word in permission.casefold() for permission in permissions for word in NETWORK_PERMISSION_WORDS):
        errors.append("network-capable tool permission is not disabled")
    budget = run.get("budget")
    if run.get("offline") is not True:
        errors.append("run offline must be true")
    if not isinstance(budget, dict) or budget.get("network") is not False:
        errors.append("run budget.network must be false")
    duration = run.get("duration_ms")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0:
        errors.append("duration_ms must be a non-negative number")
    token_usage = run.get("token_usage")
    if not isinstance(token_usage, dict) or not token_usage or any(
        not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0
        for value in token_usage.values()
    ):
        errors.append("token_usage must contain non-negative numeric usage")
    exit_status = run.get("exit_status")
    if exit_status not in {"completed", "success", "passed", "failed"}:
        errors.append("exit_status is invalid")
    if exit_status == "failed" and not isinstance(run.get("failure_reason"), str):
        errors.append("failed run requires failure_reason")
    if exit_status in {"completed", "success", "passed"} and run.get("failure_reason") is not None:
        errors.append("successful run must not have failure_reason")

    evidence: dict[str, Any] | None = None
    if evidence_path is not None:
        try:
            loaded = _load_json(evidence_path)
            evidence = loaded if isinstance(loaded, dict) else None
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid tool_evidence.json: {exc}")
        if evidence is None:
            errors.append("tool_evidence.json must contain an object")
        else:
            if evidence.get("case_id") != case_id:
                errors.append("tool evidence case_id does not match case")
            if evidence.get("offline") is not True:
                errors.append("tool evidence offline must be true")
            if evidence.get("network_accessed") is not False:
                errors.append("tool evidence network_accessed must be false")
            artifact = evidence.get("artifacts", {}).get("full_output") if isinstance(evidence.get("artifacts"), dict) else None
            if not isinstance(artifact, dict):
                errors.append("tool evidence lacks full_output artifact evidence")
            else:
                if artifact.get("path") != run.get("full_output"):
                    errors.append("tool evidence full_output path mismatch")
                if output_path is not None and artifact.get("sha256") != _sha256(output_path):
                    errors.append("tool evidence full_output hash mismatch")

    result.update({"valid": not errors, "run": run, "output_path": output_path, "evidence_path": evidence_path})
    return result


def verify_runs(cases_path: Path | str, runs_root: Path | str, manifest_path: Path | str | None = None) -> dict[str, Any]:
    cases_path = Path(cases_path)
    manifest = _manifest_for(cases_path, Path(manifest_path) if manifest_path else None)
    required = _required_fields(manifest)
    results = [_verify_case(case, Path(runs_root), required) for case in _cases(cases_path)]
    public = [{key: value for key, value in item.items() if key not in {"run", "output_path", "evidence_path"}} for item in results]
    return {"passed": bool(public) and all(item["valid"] for item in public), "cases": public}


def verify_candidate_freeze(
    freeze_path: Path | str,
    workspace_root: Path | str,
) -> dict[str, Any]:
    root = Path(workspace_root).resolve()
    freeze = _load_json(Path(freeze_path))
    errors: list[str] = []
    files = freeze.get("files") if isinstance(freeze, dict) else None
    if not isinstance(files, list) or not files:
        return {"passed": False, "file_count": 0, "errors": ["freeze files must be a non-empty array"]}

    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict):
            errors.append("freeze file entry must be an object")
            continue
        relative = entry.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append("freeze file entry has no valid path")
            continue
        if relative in seen:
            errors.append(f"{relative}: duplicate freeze path")
            continue
        seen.add(relative)
        artifact = (root / relative).resolve()
        try:
            artifact.relative_to(root)
        except ValueError:
            errors.append(f"{relative}: path escapes workspace root")
            continue
        if not artifact.is_file():
            errors.append(f"{relative}: missing frozen artifact")
            continue

        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            errors.append(f"{relative}: invalid recorded SHA-256")
        elif _sha256(artifact) != expected_hash:
            errors.append(f"{relative}: SHA-256 mismatch")
        expected_bytes = entry.get("bytes")
        if not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool) or expected_bytes < 0:
            errors.append(f"{relative}: invalid recorded byte count")
        elif artifact.stat().st_size != expected_bytes:
            errors.append(f"{relative}: byte count mismatch")

    return {"passed": not errors, "file_count": len(files), "errors": errors}


def _presence_checks(values: Any, output: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return [{"criterion": "<invalid case field>", "passed": False, "evidence": [], "review_status": "invalid"}]
    normalized_output = _normalized(output)
    checks: list[dict[str, Any]] = []
    for value in values:
        if isinstance(value, dict) and value.get("assertion") == "contains" and isinstance(value.get("value"), str):
            needle = _normalized(value["value"])
            matched = bool(needle) and needle in normalized_output
            checks.append({
                "criterion": value.get("criterion", value["value"]),
                "passed": matched,
                "evidence": ([{"source": "full_output.md", "text": value["value"]}] if matched else []),
                "review_status": "automatic",
            })
        else:
            checks.append({
                "criterion": value,
                "passed": False,
                "evidence": [],
                "review_status": "pending-human-review",
            })
    return checks


def _behavior_checks(values: Any, output: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return [{"criterion": "<invalid case field>", "passed": False, "evidence": [], "review_status": "invalid"}]
    normalized_output = _normalized(output)
    checks: list[dict[str, Any]] = []
    for value in values:
        if isinstance(value, dict) and value.get("assertion") == "contains" and isinstance(value.get("value"), str):
            needle = _normalized(value["value"])
            matched = bool(needle) and needle in normalized_output
            checks.append({
                "criterion": value.get("criterion", value["value"]),
                "passed": matched,
                "evidence": ([{"source": "full_output.md", "text": value["value"]}] if matched else []),
                "review_status": "automatic",
            })
        else:
            checks.append({
                "criterion": value,
                "passed": False,
                "evidence": [],
                "review_status": "pending-human-review",
            })
    return checks


def _negated_occurrence(line: str, start: int, end: int) -> bool:
    prefix = line[max(0, start - 120):start].casefold()
    suffix = _normalized(line[end:end + 120])
    clause = re.split(r"[.;:!?]|\b(?:but|however|yet)\b", prefix)[-1]
    normalized_clause = _normalized(clause)
    prefix_negated = (
        normalized_clause.startswith(("no ", "not ", "never ", "without "))
        or any(
            marker in f" {normalized_clause} "
            for marker in (
                " no ",
                " not ",
                " never ",
                " without ",
                " cannot ",
                " can't ",
                " must not ",
                " does not ",
                " do not ",
                " is not ",
                " are not ",
                " isn't ",
                " aren't ",
                " prohibited ",
                " forbidden ",
            )
        )
    )
    suffix_negated = any(
        marker in suffix
        for marker in (
            "is not claimed",
            "are not claimed",
            "is not approved",
            "are not approved",
            "not claimed",
            "out of scope",
            "prohibited",
            "forbidden",
        )
    )
    return prefix_negated or suffix_negated


def _forbidden_checks(values: Any, output: str) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return [{"criterion": "<invalid case field>", "passed": False, "evidence": [], "review_status": "invalid"}]
    lines = output.splitlines()
    results: list[dict[str, Any]] = []
    for value in values:
        if not isinstance(value, dict) or value.get("assertion") != "absent" or not isinstance(value.get("value"), str):
            results.append({
                "criterion": value,
                "passed": False,
                "evidence": [],
                "review_status": "pending-human-review",
            })
            continue
        affirmative: list[dict[str, str]] = []
        pattern = re.compile(re.escape(value["value"]), flags=re.IGNORECASE)
        for line in lines:
            for match in pattern.finditer(line):
                if not _negated_occurrence(line, match.start(), match.end()):
                    affirmative.append({"source": "full_output.md", "text": line.strip()})
        results.append({
            "criterion": value.get("criterion", value["value"]),
            "passed": not affirmative,
            "evidence": affirmative,
            "review_status": "automatic",
        })
    return results


def grade(cases_path: Path | str, rubric_path: Path | str, runs_root: Path | str) -> dict[str, Any]:
    cases = _cases(Path(cases_path))
    rubric = _load_json(Path(rubric_path))
    if not isinstance(rubric, dict) or not isinstance(rubric.get("hard_failures"), list):
        raise ValueError("rubric must contain hard_failures")
    required = _required_fields(_manifest_for(Path(cases_path), None))
    results: list[dict[str, Any]] = []
    for case in cases:
        verified = _verify_case(case, Path(runs_root), required)
        output = ""
        if verified.get("output_path") is not None:
            output = verified["output_path"].read_text(encoding="utf-8")
        behavior = _behavior_checks(case.get("required_behaviors"), output)
        unknowns = _presence_checks(case.get("must_preserve_unknowns"), output)
        forbidden = _forbidden_checks(case.get("must_not_claim"), output)
        actual_status = _extract_status(output)
        expected_status = case.get("expected_status")
        status_match = {
            "expected": expected_status,
            "actual": actual_status,
            "passed": isinstance(expected_status, str) and actual_status == expected_status.casefold(),
        }
        failures: list[str] = []
        if not verified["valid"]:
            failures.append("invalid-run-evidence")
        if verified.get("run", {}).get("exit_status") == "failed":
            failures.append("run-execution-failed")
        if any(item.get("review_status") == "automatic" and not item["passed"] for item in behavior):
            failures.append("missing-required-behavior")
        if any(item.get("review_status") == "automatic" and not item["passed"] for item in unknowns):
            failures.append("unknown-loss")
        if any(item.get("review_status") == "automatic" and not item["passed"] for item in forbidden):
            failures.append("forbidden-claim")
        if any(
            item.get("review_status") == "pending-human-review"
            for group in (behavior, unknowns, forbidden)
            for item in group
        ):
            failures.append("pending-human-review")
        if not status_match["passed"]:
            failures.append("incorrect-gate")
        evidence = [entry for group in (behavior, unknowns) for item in group for entry in item["evidence"]]
        result = {
            "case_id": case.get("id"),
            "passed": not failures,
            "objective_checks": {
                "required_behaviors": behavior,
                "must_preserve_unknowns": unknowns,
                "must_not_claim": forbidden,
            },
            "hard_failures": failures,
            "status_match": status_match,
            "evidence": evidence,
            "run_validation_errors": verified["errors"],
        }
        results.append(result)
    return {"passed": bool(results) and all(item["passed"] for item in results), "cases": results}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    grade_parser = commands.add_parser("grade")
    grade_parser.add_argument("--cases", type=Path, required=True)
    grade_parser.add_argument("--rubric", type=Path, required=True)
    grade_parser.add_argument("--runs-root", type=Path, required=True)
    grade_parser.add_argument("--output", type=Path, required=True)
    verify_parser = commands.add_parser("verify-runs")
    verify_parser.add_argument("--cases", type=Path, required=True)
    verify_parser.add_argument("--runs-root", type=Path, required=True)
    freeze_parser = commands.add_parser("verify-freeze")
    freeze_parser.add_argument("--freeze", type=Path, required=True)
    freeze_parser.add_argument("--workspace-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "grade":
            report = grade(args.cases, args.rubric, args.runs_root)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        elif args.command == "verify-runs":
            report = verify_runs(args.cases, args.runs_root)
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            report = verify_candidate_freeze(args.freeze, args.workspace_root)
            print(json.dumps(report, indent=2, ensure_ascii=False))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"eval runner error: {exc}", file=sys.stderr)
        return 2
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
