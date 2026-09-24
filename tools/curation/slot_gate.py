"""Deterministic structural gates for the released requirements-to-AC slots."""
from __future__ import annotations

import re
from typing import Any


def _ac_blocks(text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?m)^###\s+AC-\d+\b", text)]
    return [text[start:end] for start, end in zip(starts, starts[1:] + [len(text)])]


def evaluate_gate(gate: str, output: str, inputs: dict[str, Any]) -> dict[str, object]:
    folded = output.casefold()
    evidence: list[str] = []

    if gate == "source-traceability":
        source_ids = set(re.findall(r"\bSRC-\d+\b", output))
        evidence = sorted(source_ids)
        passed = bool(source_ids) and "evidence:" in folded and "source" in folded
    elif gate == "unknown-preservation":
        requirements = set(re.findall(r"\bREQ-\d+\b", output))
        rules = set(re.findall(r"\bRULE-\d+\b", output))
        markers = [value for value in ("unknown", "parameterized", "unspecified") if value in folded]
        evidence = sorted(requirements | rules) + markers
        passed = bool(requirements) and bool(rules) and bool(markers)
    elif gate in {"given-when-then-structure", "observability"}:
        blocks = _ac_blocks(output)
        structured = [block for block in blocks if all(f"**{word}**" in block for word in ("Given", "When", "Then"))]
        evidence = [re.search(r"AC-\d+", block).group(0) for block in structured]
        if gate == "given-when-then-structure":
            passed = bool(blocks) and len(structured) == len(blocks)
        else:
            observable = ("available", "unavailable", "associated", "represented", "remains")
            passed = bool(structured) and all(any(word in block.casefold() for word in observable) for block in structured)
    elif gate == "applicable-success-coverage":
        blocks = _ac_blocks(output)
        evidence = [re.search(r"AC-\d+", block).group(0) for block in blocks if "success" in block.casefold()]
        passed = bool(evidence) and "success" in folded
    elif gate == "evidence-backed-verdict":
        evidence_ids = set(re.findall(r"\bEV-\d+\b", output))
        evidence = sorted(evidence_ids)
        passed = len(evidence_ids) >= 3 and "evidence citations" in folded and "verdict" in folded
    elif gate == "read-only-review":
        forbidden = ("modified product source", "rewrote upstream", "changed the requirement")
        evidence = ["read-only"] if "read-only" in folded else []
        passed = bool(evidence) and not any(value in folded for value in forbidden)
    else:
        return {"gate": gate, "passed": False, "evidence": [], "error": "no deterministic evaluator"}

    return {"gate": gate, "passed": passed, "evidence": evidence}


def evaluate_gates(gates: list[str], output: str, inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [evaluate_gate(gate, output, inputs) for gate in gates]
