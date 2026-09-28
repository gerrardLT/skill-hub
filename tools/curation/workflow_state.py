#!/usr/bin/env python3
"""Durable machine workflow state with a generated Markdown view."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STATE_VERSION = "1.0"
VALID_STATUSES = {"pending", "running", "passed", "needs-input", "failed", "blocked", "invalidated"}

class StateError(ValueError):
    pass

def new_state(project: str, intent: str, recipe_ref: str) -> dict[str, Any]:
    return {
        "schema_version": STATE_VERSION,
        "project": project,
        "updated_at": datetime.now(UTC).isoformat(),
        "intent": intent,
        "recipe_ref": recipe_ref,
        "status": "pending",
        "steps": [],
        "invalidated_evidence": [],
        "attempts": {},
        "failure_fingerprints": [],
        "next_action": "start",
    }

def validate_state(state: object) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise StateError("state must be an object")
    required = {
        "schema_version", "project", "updated_at", "intent", "recipe_ref",
        "status", "steps", "invalidated_evidence", "attempts",
        "failure_fingerprints", "next_action",
    }
    missing = sorted(required - state.keys())
    if missing:
        raise StateError(f"missing state fields: {missing}")
    if state["schema_version"] != STATE_VERSION:
        raise StateError(f"unsupported state version: {state['schema_version']}")
    if state["status"] not in VALID_STATUSES:
        raise StateError(f"invalid state status: {state['status']}")
    if not isinstance(state["steps"], list) or not isinstance(state["invalidated_evidence"], list):
        raise StateError("steps and invalidated_evidence must be arrays")
    if not isinstance(state["attempts"], dict) or not all(isinstance(v, int) and v >= 0 for v in state["attempts"].values()):
        raise StateError("attempts must be non-negative integers")
    if not isinstance(state["failure_fingerprints"], list):
        raise StateError("failure_fingerprints must be an array")
    for index, step in enumerate(state["steps"]):
        if not isinstance(step, dict):
            raise StateError(f"step {index} must be an object")
        for field in ("step_id", "ref", "status", "input_sha256", "artifacts", "evidence", "attempts"):
            if field not in step:
                raise StateError(f"step {index} missing {field}")
        if step["status"] not in VALID_STATUSES or not isinstance(step["attempts"], int):
            raise StateError(f"step {index} invalid status or attempts")
    return state

def render_markdown(state: dict[str, Any]) -> str:
    validate_state(state)
    lines = [
        "# Dev Loop State",
        "",
        f"project: {state['project']}",
        f"updated: {state['updated_at']}",
        f"intent: {state['intent']}",
        f"recipe: {state['recipe_ref']}",
        f"status: {state['status']}",
        "",
        "## Steps",
    ]
    if state["steps"]:
        for step in state["steps"]:
            artifacts = ", ".join(step["artifacts"]) or "—"
            evidence = ", ".join(step["evidence"]) or "—"
            lines.append(f"- {step['step_id']}: {step['ref']} | {step['status']} | attempts={step['attempts']} | input={step['input_sha256']} | artifacts={artifacts} | evidence={evidence}")
    else:
        lines.append("- none")
    lines += ["", "## Invalidated Evidence"]
    if state["invalidated_evidence"]:
        for item in state["invalidated_evidence"]:
            lines.append(f"- {item['path']}: {item['reason']}")
    else:
        lines.append("- none")
    lines += ["", "## Next Action", f"- {state['next_action']}", ""]
    return "\n".join(lines)

def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)

def save_state(state_dir: Path, state: dict[str, Any]) -> None:
    state = validate_state(state)
    state["updated_at"] = datetime.now(UTC).isoformat()
    encoded = (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _atomic_write(state_dir / "state.json", encoded)
    _atomic_write(state_dir / "state.md", render_markdown(state).encode("utf-8"))

def load_state(state_dir: Path) -> dict[str, Any] | None:
    path = state_dir / "state.json"
    if not path.exists():
        return None
    try:
        return validate_state(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError, StateError) as exc:
        diagnostic = state_dir / f"state.corrupt-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.json"
        state_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(path, diagnostic)
        except OSError:
            pass
        raise StateError(f"cannot load workflow state: {exc}") from exc
