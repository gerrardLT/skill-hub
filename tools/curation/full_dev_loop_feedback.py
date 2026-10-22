#!/usr/bin/env python3
"""Verify retrospective output is consumable by the next requirements cycle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REQUIRED_GAPS = ("Production traffic", "Customer or operator feedback", "Executable evidence")


def verify(run_root: Path) -> dict:
    errors: list[str] = []
    retro = run_root / "run/retro_to_requirements/retro.md"
    next_input = run_root / "next-cycle/input.json"
    next_result = run_root / "next-cycle/run/result.json"
    frame = run_root / "next-cycle/run/requirements/step-1-frame.md"
    for path in (retro, next_input, next_result, frame):
        if not path.is_file():
            errors.append(f"missing feedback artifact: {path}")
    if errors:
        return {"gate": "full-dev-loop-feedback", "ok": False, "errors": errors}
    supplied = json.loads(next_input.read_text(encoding="utf-8"))
    retro_text = retro.read_text(encoding="utf-8")
    if supplied.get("validated-product-brief") != retro_text:
        errors.append("retrospective output was not passed verbatim as next validated-product-brief")
    result = json.loads(next_result.read_text(encoding="utf-8"))
    if result.get("status") != "needs-input" or result.get("passed") is not False:
        errors.append("next cycle did not fail closed on missing production evidence")
    frame_text = frame.read_text(encoding="utf-8")
    if not all(value.casefold() in frame_text.casefold() for value in REQUIRED_GAPS):
        errors.append("next cycle did not preserve required evidence gaps")
    return {
        "gate": "full-dev-loop-feedback", "ok": not errors,
        "retro_sha256": hashlib.sha256(retro.read_bytes()).hexdigest(),
        "next_input_sha256": hashlib.sha256(next_input.read_bytes()).hexdigest(),
        "next_status": result.get("status"), "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.run_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
