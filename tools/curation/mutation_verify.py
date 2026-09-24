"""Run deterministic requirements-to-AC candidate mutation checks offline."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Callable


SLOT_FILES = (
    "problem-framing/SKILL.md",
    "problem-framing/contract.json",
    "requirements-rules/SKILL.md",
    "requirements-rules/contract.json",
    "acceptance-criteria/SKILL.md",
    "acceptance-criteria/contract.json",
    "requirements-quality-gate/SKILL.md",
    "requirements-quality-gate/contract.json",
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_candidate(slots_root: Path | str) -> dict[str, object]:
    root = Path(slots_root)
    errors: list[str] = []
    try:
        ac_skill = (root / "acceptance-criteria/SKILL.md").read_text(encoding="utf-8")
        gate_skill = (root / "requirements-quality-gate/SKILL.md").read_text(encoding="utf-8")
        ac = _load(root / "acceptance-criteria/contract.json")
        gate = _load(root / "requirements-quality-gate/contract.json")
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "errors": [f"candidate-artifact-invalid: {exc}"]}

    if "Missing evidence cannot count as success." not in gate_skill:
        errors.append("evidence-insufficiency-rule")
    ac_outputs = ac.get("outputs")
    if not isinstance(ac_outputs, list) or not any(
        isinstance(value, str) and "unresolved inputs" in value.casefold()
        for value in ac_outputs
    ):
        errors.append("unknown-marker-requirement")
    if not isinstance(ac_outputs, list) or not any(
        isinstance(value, str) and "given/when/then acceptance criteria" in value.casefold()
        for value in ac_outputs
    ):
        errors.append("acceptance-criteria-field")
    statuses = gate.get("statuses")
    if not isinstance(statuses, list) or "blocked" not in statuses:
        errors.append("blocked-gate")
    combined = f"{ac_skill}\n{gate_skill}".casefold()
    if "commit to a queue implementation" in combined:
        errors.append("unsupported-implementation-commitment")

    return {"passed": not errors, "errors": errors}


def _replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise ValueError(f"mutation target missing in {path.as_posix()}: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _remove_unknown_marker(root: Path) -> None:
    path = root / "acceptance-criteria/contract.json"
    data = _load(path)
    data["outputs"] = [
        value for value in data["outputs"]
        if not isinstance(value, str) or "unresolved inputs" not in value.casefold()
    ]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _remove_ac_field(root: Path) -> None:
    path = root / "acceptance-criteria/contract.json"
    data = _load(path)
    data["outputs"] = [
        value for value in data["outputs"]
        if not isinstance(value, str) or "given/when/then acceptance criteria" not in value.casefold()
    ]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _replace_blocked_gate(root: Path) -> None:
    path = root / "requirements-quality-gate/contract.json"
    data = _load(path)
    data["statuses"] = ["passed" if value == "blocked" else value for value in data["statuses"]]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _add_implementation_commitment(root: Path) -> None:
    path = root / "acceptance-criteria/SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "\nCommit to a queue implementation before handoff.\n",
        encoding="utf-8",
    )


MUTATIONS: tuple[tuple[str, str, Callable[[Path], None]], ...] = (
    (
        "remove-evidence-insufficiency-rule",
        "evidence-insufficiency-rule",
        lambda root: _replace(
            root / "requirements-quality-gate/SKILL.md",
            "Missing evidence cannot count as success.",
            "",
        ),
    ),
    ("remove-unknown-marker-requirement", "unknown-marker-requirement", _remove_unknown_marker),
    ("remove-acceptance-criteria-field", "acceptance-criteria-field", _remove_ac_field),
    ("replace-blocked-gate-with-pass", "blocked-gate", _replace_blocked_gate),
    (
        "add-unsupported-implementation-commitment",
        "unsupported-implementation-commitment",
        _add_implementation_commitment,
    ),
)


def run_mutation_suite(slots_root: Path | str) -> dict[str, object]:
    source = Path(slots_root)
    baseline = verify_candidate(source)
    results: list[dict[str, object]] = []
    for mutation_id, expected_failure, mutate in MUTATIONS:
        with tempfile.TemporaryDirectory() as temporary:
            candidate = Path(temporary) / "slots"
            for relative in SLOT_FILES:
                target = candidate / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / relative, target)
            mutate(candidate)
            report = verify_candidate(candidate)
            detected = report["passed"] is False and expected_failure in report["errors"]
            results.append(
                {
                    "mutation": mutation_id,
                    "expected_failure": expected_failure,
                    "detected": detected,
                    "errors": report["errors"],
                }
            )
    return {
        "passed": baseline["passed"] is True and all(result["detected"] for result in results),
        "baseline": baseline,
        "mutations": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slots-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_mutation_suite(args.slots_root)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
