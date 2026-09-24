"""Rearrange paired run artifacts into the variance verifier layout."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def prepare(paired_roots: list[Path], cases_path: Path, output: Path, case_ids: list[str]) -> dict[str, object]:
    cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
    known = {case["id"] for case in cases}
    errors = [f"unknown case: {case_id}" for case_id in case_ids if case_id not in known]
    copied = []
    for number, root in enumerate(paired_roots, 1):
        for case_id in case_ids:
            for source_name, target_name in (("candidate", "with_skill"), ("baseline", "without_skill")):
                source = root / source_name / case_id
                target = output / case_id / target_name / f"run-{number}"
                if not source.is_dir():
                    errors.append(f"missing run: {source}")
                    continue
                target.mkdir(parents=True, exist_ok=True)
                for name in ("full_output.md", "tool_evidence.raw.json", "timing.json"):
                    if not (source / name).is_file():
                        errors.append(f"missing {name}: {source}")
                    else:
                        shutil.copyfile(source / name, target / name)
                copied.append(target.as_posix())
    return {"passed": not errors, "copied": copied, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paired-root", type=Path, action="append", required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case-id", action="append", required=True)
    args = parser.parse_args()
    report = prepare(args.paired_root, args.cases, args.output, args.case_id)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
