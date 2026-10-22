#!/usr/bin/env python3
"""Materialize and release the reviewed minimum six-stage Slot closure."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

STAGE_CONFIG: dict[str, dict[str, Any]] = {
    "design": {
        "slots": ["design-context-and-direction-contract"],
        "adapter": "artifact", "tools": [], "mutation": "run-output", "scopes": [],
    },
    "implementation": {
        "slots": ["tdd-change-loop", "completion-evidence-gate"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash", "edit", "write", "run-tests"], "mutation": "isolated-worktree", "scopes": ["workspace-write"],
    },
    "qa": {
        "slots": ["independent-blackbox-qa"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash", "run-tests", "browser-readonly"], "mutation": "none", "scopes": [],
    },
    "delivery": {
        "slots": ["change-delivery-preflight"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash"], "mutation": "none", "scopes": [],
    },
    "retrospective": {
        "slots": ["feedback-and-continuous-learning-loop"],
        "adapter": "artifact", "tools": [], "mutation": "run-output", "scopes": [],
    },
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _method(slot_id: str, contract: dict[str, Any], stage: str) -> str:
    report_only = slot_id in {"independent-blackbox-qa", "independent-code-review", "baseline-regression-control"}
    return f"""# {slot_id}

Status: released 1.0.0

## Responsibility

{contract['responsibility']}

## Inputs

{contract['boundaries']['input']}

## Method

1. Classify every supplied statement as evidence, constraint, unknown, conflict, or authorized decision before acting.
2. Preserve stable IDs, source references, authority boundaries, and unresolved unknowns in every output.
3. Execute only the declared `{stage}` responsibility; do not absorb upstream or downstream work.
4. Produce numbered findings or records with direct evidence citations and an explicit per-Gate result.
5. Return `needs-input` for missing required facts, `blocked` for missing authority or tooling, and `failed` for observed execution or verification failure.
6. Return `passed` only when all declared Gates have current evidence.

## Output

{contract['boundaries']['output']}

## Safety

- {'Report only. Never modify product source or repair findings.' if report_only else 'Respect the execution adapter and explicit authorization boundary.'}
- Never fabricate evidence, silently resolve conflicts, erase unknowns, or treat a stale result as current.
- Never use remote Git, network, merge, or deployment authority unless the host supplied that exact authorization scope.

## Required Format

First line: `Status: passed|needs-input|blocked|failed`.
Then include `Evidence:`, numbered records, `Gate Results:`, and `Unknowns:` sections.
"""


def release(workspace: Path, *, human_approved: bool = False, reviewer: str | None = None) -> dict[str, Any]:
    """Legacy generator is disabled: it fabricated release results."""
    raise RuntimeError("release-disabled: evaluate real cases and obtain output-based review before publishing")

if __name__ == "__main__":
    raise SystemExit("release-disabled: generated PASS evidence cannot authorize release")
