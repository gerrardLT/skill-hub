"""Verify downstream QA handoff traceability and isolation offline."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ID_PATTERN = re.compile(r"\b(?:SRC|AUTH|FACT|OPEN|REQ|RULE|DEP|SCOPE|AC)-\d+\b")


def _refers_to(paths: object, expected: Path) -> bool:
    if not isinstance(paths, list):
        return False
    expected_posix = expected.as_posix()
    expected_resolved = expected.resolve()
    for value in paths:
        if not isinstance(value, str):
            continue
        candidate = Path(value)
        if value.replace("\\", "/") == expected_posix:
            return True
        try:
            if candidate.resolve() == expected_resolved:
                return True
        except OSError:
            continue
    return False


def verify_handoff(
    upstream_path: Path | str,
    handoff_path: Path | str,
    evidence_path: Path | str,
) -> dict[str, object]:
    upstream_file = Path(upstream_path)
    handoff_file = Path(handoff_path)
    evidence_file = Path(evidence_path)
    errors: list[str] = []

    try:
        upstream = upstream_file.read_text(encoding="utf-8")
        handoff = handoff_file.read_text(encoding="utf-8")
        evidence = json.loads(evidence_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "passed": False,
            "upstream_ids": [],
            "downstream_ids": [],
            "missing_ids": [],
            "errors": [f"handoff-artifact-invalid: {exc}"],
        }

    upstream_ids = sorted(set(ID_PATTERN.findall(upstream)))
    downstream_ids = sorted(set(ID_PATTERN.findall(handoff)))
    missing_ids = sorted(set(upstream_ids) - set(downstream_ids))
    if missing_ids:
        errors.append("upstream-id-loss")

    lower = handoff.casefold()
    if not (
        "qa is read-only" in lower
        and "do not repair" in lower
        and "do not" in lower
        and "product decisions" in lower
    ):
        errors.append("qa-read-only-rule-missing")
    if not (
        "missing evidence" in lower
        and "blocked" in lower
        and ("do not infer" in lower or "rather than guessing" in lower)
    ):
        errors.append("missing-evidence-block-rule-missing")

    required_false = {
        "network_accessed": "network-access-recorded",
        "skills_modified": "skills-modified-recorded",
        "case_file_read": "handoff-read-case-file",
        "rubric_read": "handoff-read-rubric",
    }
    if evidence.get("offline") is not True:
        errors.append("offline-evidence-missing")
    for field, error in required_false.items():
        if evidence.get(field) is not False:
            errors.append(error)
    if evidence.get("errors") != []:
        errors.append("agent-errors-recorded")
    if not _refers_to(evidence.get("paths_read"), upstream_file):
        errors.append("upstream-read-not-recorded")
    if not _refers_to(evidence.get("paths_written"), handoff_file):
        errors.append("handoff-write-not-recorded")
    if not _refers_to(evidence.get("paths_written"), evidence_file):
        errors.append("evidence-write-not-recorded")

    return {
        "passed": not errors,
        "upstream_ids": upstream_ids,
        "downstream_ids": downstream_ids,
        "missing_ids": missing_ids,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = verify_handoff(args.upstream, args.handoff, args.evidence)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
