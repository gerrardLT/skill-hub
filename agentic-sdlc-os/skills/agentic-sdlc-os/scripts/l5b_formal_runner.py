#!/usr/bin/env python3
"""Execute a preregistered L5-B matched experiment in isolated workspaces.

This runner is deliberately strict. It can automate execution and blind review, but
formal evidence still requires genuinely independent executor identities/contexts and
an independent reviewer. Synthetic fixtures can exercise the machinery but never
unlock a maturity claim.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = ROOT / "scripts" / "l5b_matched_experiment.py"


def load_harness() -> Any:
    spec = importlib.util.spec_from_file_location("l5b_harness_v25", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load L5-B harness")
    module = importlib.util.module_from_spec(spec)
    sys.modules["l5b_harness_v25"] = module
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_sha(root: Path, *, exclude_names: set[str] | None = None) -> str:
    exclude_names = exclude_names or {".git", "__pycache__", ".pytest_cache", "node_modules"}
    h = hashlib.sha256()
    if not root.is_dir():
        raise RuntimeError(f"Workspace/source directory not found: {root}")
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        rel = path.relative_to(root)
        if any(part in exclude_names for part in rel.parts):
            continue
        if path.is_symlink():
            h.update(b"L\0" + rel.as_posix().encode() + b"\0" + os.readlink(path).encode())
        elif path.is_file():
            h.update(b"F\0" + rel.as_posix().encode() + b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    h.update(chunk)
    return h.hexdigest()


def _command(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise RuntimeError(f"{label}.command must be a non-empty argv list")
    return list(value)


def validate_config(config: dict[str, Any]) -> None:
    required = ["project", "source_dir", "model", "toolset", "baseline", "sdlc", "reviewer", "tasks"]
    missing = [key for key in required if key not in config]
    if missing:
        raise RuntimeError("Missing config fields: " + ", ".join(missing))
    if not isinstance(config["tasks"], list) or len(config["tasks"]) < 3:
        raise RuntimeError("At least 3 tasks are required; 5+ is recommended")
    if len(config["tasks"]) != int(config.get("target_pairs", len(config["tasks"]))):
        raise RuntimeError("tasks length must equal target_pairs")
    source = Path(config["source_dir"]).expanduser().resolve()
    if not source.is_dir():
        raise RuntimeError(f"source_dir not found: {source}")
    if not isinstance(config["toolset"], list) or not config["toolset"]:
        raise RuntimeError("toolset must be a non-empty list")
    executor_codes = []
    for arm in ["baseline", "sdlc"]:
        item = config[arm]
        _command(item.get("command"), arm)
        code = str(item.get("executor_code", "")).strip()
        if not code:
            raise RuntimeError(f"{arm}.executor_code is required")
        executor_codes.append(code)
    if executor_codes[0] == executor_codes[1]:
        raise RuntimeError("baseline and sdlc executor_code must be distinct")
    reviewer = config["reviewer"]
    _command(reviewer.get("command"), "reviewer")
    reviewer_code = str(reviewer.get("reviewer_code", "")).strip()
    if not reviewer_code:
        raise RuntimeError("reviewer.reviewer_code is required")
    if reviewer_code in executor_codes:
        raise RuntimeError("reviewer_code must be independent from executor codes")
    ids: set[str] = set()
    for task in config["tasks"]:
        task_id = str(task.get("id", "")).strip()
        if not task_id or task_id in ids:
            raise RuntimeError("Task ids must be non-empty and unique")
        ids.add(task_id)
        spec_path = Path(task.get("spec_path", "")).expanduser().resolve()
        if not spec_path.is_file():
            raise RuntimeError(f"Task spec not found: {spec_path}")
        complexity = int(task.get("complexity", 0))
        if complexity < 1 or complexity > 5:
            raise RuntimeError(f"Task {task_id} complexity must be 1..5")
        if int(task.get("time_budget_minutes", 0)) <= 0:
            raise RuntimeError(f"Task {task_id} time_budget_minutes must be positive")


def _run(argv: list[str], *, cwd: Path, env: dict[str, str], timeout_seconds: int) -> tuple[int, bytes, float]:
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout_seconds, check=False)
        return int(proc.returncode), proc.stdout, time.monotonic() - started
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"") + b"\nL5B_TIMEOUT\n"
        return 124, output, time.monotonic() - started


def _metrics(path: Path, elapsed_seconds: float) -> dict[str, float]:
    if not path.is_file():
        raise RuntimeError(f"Executor did not write metrics result: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", payload)
    required = [
        "lead_time_minutes", "human_minutes", "token_cost_usd", "rework_fraction",
        "escaped_defects", "critical_defects", "trace_coverage", "acceptance_pass_rate",
        "maintainability_score",
    ]
    missing = [name for name in required if name not in metrics]
    if missing:
        raise RuntimeError("Missing executor metrics: " + ", ".join(missing))
    normalized = {name: float(metrics[name]) for name in required}
    if normalized["lead_time_minutes"] <= 0:
        normalized["lead_time_minutes"] = elapsed_seconds / 60.0
    return normalized


def _review_scores(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"Reviewer did not write result: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    for field in ["correctness", "completeness", "maintainability", "usability"]:
        if field not in payload:
            raise RuntimeError(f"Reviewer result missing {field}")
        value = float(payload[field])
        if value < 0 or value > 10:
            raise RuntimeError(f"Reviewer score out of range: {field}")
    return payload


def execute(config_path: Path, output_dir: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(config)
    harness = load_harness()
    source = Path(config["source_dir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    experiment_path = output_dir / "experiment.json"
    if experiment_path.exists():
        raise RuntimeError(f"Output already contains experiment.json: {output_dir}")

    synthetic = bool(config.get("synthetic", False))
    target_pairs = int(config.get("target_pairs", len(config["tasks"])))
    exp = harness.new_experiment(
        str(config["project"]), target_pairs, int(config.get("seed", 20260901)),
        str(config.get("hypothesis", "Agentic SDLC OS improves delivery outcomes without severe quality regression.")),
        synthetic,
    )
    task_specs: dict[str, Path] = {}
    for task in config["tasks"]:
        spec_path = Path(task["spec_path"]).expanduser().resolve()
        task_specs[str(task["id"])] = spec_path
        harness.add_task(
            exp, str(task["id"]), file_sha(spec_path), str(task.get("domain", "software")),
            int(task["complexity"]), int(task["time_budget_minutes"]),
        )
    harness.freeze(exp)
    harness.atomic_write(experiment_path, exp)

    start_state_hash = tree_sha(source)
    toolset_hash = digest(config["toolset"])
    environment_payload = {
        "platform": platform.platform(), "python": platform.python_version(),
        "model": config["model"], "toolset": config["toolset"],
        "environment_attestation": config.get("environment_attestation", {}),
    }
    environment_hash = digest(environment_payload)
    run_root = output_dir / "runs"
    blind_root = output_dir / "blind"
    run_root.mkdir(); blind_root.mkdir()
    execution_report: dict[str, Any] = {
        "schema_version": "2.5", "synthetic": synthetic, "experiment_path": str(experiment_path),
        "start_state_hash": start_state_hash, "toolset_hash": toolset_hash,
        "environment_hash": environment_hash, "runs": [], "reviews": [],
        "formal_context_attestation": bool(config.get("formal_context_attestation", False)),
    }

    for assignment in exp["assignments"]:
        task_id = str(assignment["task_id"])
        task_spec = task_specs[task_id]
        task = next(item for item in config["tasks"] if str(item["id"]) == task_id)
        timeout_seconds = int(task["time_budget_minutes"]) * 60
        for arm in assignment["order"]:
            arm_cfg = config[arm]
            context_id = f"ctx-{uuid.uuid4().hex}"
            workspace = run_root / task_id / arm / "workspace"
            workspace.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, workspace, symlinks=True)
            if tree_sha(workspace) != start_state_hash:
                raise RuntimeError(f"Start-state copy mismatch for {task_id}/{arm}")
            metrics_path = workspace.parent / "metrics.json"
            log_path = workspace.parent / "run.log"
            blind_code = assignment["blind_artifact_codes"][arm]
            env = os.environ.copy()
            env.update({
                "L5B_WORKSPACE": str(workspace), "L5B_TASK_SPEC": str(task_spec),
                "L5B_RESULT_JSON": str(metrics_path), "L5B_BLIND_CODE": str(blind_code),
                "L5B_EXECUTION_CONTEXT_ID": context_id, "L5B_MODEL": str(config["model"]),
                "L5B_TOOLSET_HASH": toolset_hash,
            })
            rc, output, elapsed = _run(_command(arm_cfg["command"], arm), cwd=workspace, env=env, timeout_seconds=timeout_seconds)
            log_path.write_bytes(output)
            if rc != 0:
                raise RuntimeError(f"Executor failed for {task_id}/{arm}: rc={rc}; see {log_path}")
            metrics = _metrics(metrics_path, elapsed)
            artifact_hash = tree_sha(workspace)
            run_log_hash = file_sha(log_path)
            harness.record_run(
                exp, task_id=task_id, arm=arm, executor_code=str(arm_cfg["executor_code"]),
                execution_context_id=context_id, model=str(config["model"]),
                prompt_hash=file_sha(task_spec), toolset_hash=toolset_hash,
                start_state_hash=start_state_hash, environment_hash=environment_hash,
                artifact_hash=artifact_hash, run_log_hash=run_log_hash, metrics=metrics,
                contamination=str(arm_cfg.get("contamination", "none")),
            )
            harness.atomic_write(experiment_path, exp)
            blind_dir = blind_root / str(blind_code)
            shutil.copytree(workspace, blind_dir, symlinks=True)
            execution_report["runs"].append({
                "task_id": task_id, "blind_artifact_code": blind_code, "executor_code": arm_cfg["executor_code"],
                "execution_context_id": context_id, "return_code": rc, "elapsed_seconds": round(elapsed, 3),
                "artifact_hash": artifact_hash, "run_log_hash": run_log_hash,
            })

    reviewer_cfg = config["reviewer"]
    reviewer_code = str(reviewer_cfg["reviewer_code"])
    for assignment in exp["assignments"]:
        task_id = str(assignment["task_id"])
        task_spec = task_specs[task_id]
        for blind_code in assignment["blind_artifact_codes"].values():
            blind_dir = blind_root / str(blind_code)
            result_path = output_dir / "reviews" / f"{blind_code}.json"
            log_path = output_dir / "reviews" / f"{blind_code}.log"
            result_path.parent.mkdir(parents=True, exist_ok=True)
            env = os.environ.copy()
            # Deliberately do NOT disclose arm identity to the reviewer.
            env.update({
                "L5B_BLIND_ARTIFACT": str(blind_dir), "L5B_BLIND_CODE": str(blind_code),
                "L5B_TASK_SPEC": str(task_spec), "L5B_REVIEW_RESULT_JSON": str(result_path),
            })
            rc, output, elapsed = _run(_command(reviewer_cfg["command"], "reviewer"), cwd=blind_dir, env=env, timeout_seconds=int(config.get("review_timeout_seconds", 900)))
            log_path.write_bytes(output)
            if rc != 0:
                raise RuntimeError(f"Blind reviewer failed for {blind_code}: rc={rc}; see {log_path}")
            scores = _review_scores(result_path)
            harness.add_review(
                exp, blind_artifact_code=str(blind_code), reviewer_code=reviewer_code,
                correctness=float(scores["correctness"]), completeness=float(scores["completeness"]),
                maintainability=float(scores["maintainability"]), usability=float(scores["usability"]),
                notes=str(scores.get("notes", "")),
            )
            execution_report["reviews"].append({"blind_artifact_code": blind_code, "reviewer_code": reviewer_code, "elapsed_seconds": round(elapsed, 3)})
            harness.atomic_write(experiment_path, exp)

    # Formal claims require an external attestation that the two executor contexts are genuinely independent.
    # Without it we intentionally mark runs contaminated before sealing. Synthetic runs may still seal for smoke testing.
    if not synthetic and not bool(config.get("formal_context_attestation", False)):
        for run in exp["runs"]:
            run["contamination"] = "independent-execution-context-not-attested"
        # Rebuild chain because contamination is part of the record. This makes the missing attestation tamper-evident.
        exp["runs"] = []
        exp["record_chain_head"] = "GENESIS"
        raise RuntimeError("formal_context_attestation=true is required for a non-synthetic formal run")

    seal_hash = harness.seal(exp)
    harness.atomic_write(experiment_path, exp)
    result = harness.analyze(exp)
    execution_report.update({
        "sealed": True, "seal_hash": seal_hash, "analysis": result,
        "formal_evidence_eligible": bool(result.get("formal_evidence_eligible") and config.get("formal_context_attestation", False)),
    })
    report_path = output_dir / "execution-report.json"
    report_path.write_text(json.dumps(execution_report, indent=2) + "\n", encoding="utf-8")
    (output_dir / "L5B_REPORT.md").write_text(harness.report_markdown(exp, result), encoding="utf-8")
    return execution_report


def template() -> dict[str, Any]:
    return {
        "project": "my-project", "source_dir": "/path/to/frozen/source", "model": "exact-model-id",
        "toolset": ["same-tool-a", "same-tool-b"], "target_pairs": 5, "seed": 20260901,
        "synthetic": False, "formal_context_attestation": False,
        "baseline": {"executor_code": "baseline-executor", "command": ["baseline-agent", "run"]},
        "sdlc": {"executor_code": "sdlc-executor", "command": ["sdlc-agent", "run"]},
        "reviewer": {"reviewer_code": "blind-reviewer", "command": ["blind-reviewer", "score"]},
        "tasks": [
            {"id": f"task-{i}", "spec_path": f"/path/to/task-{i}.md", "domain": "software", "complexity": 3, "time_budget_minutes": 60}
            for i in range(1, 6)
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Formal L5-B isolated execution runner")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("template"); p.add_argument("--output")
    p = sub.add_parser("run"); p.add_argument("config"); p.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "template":
            payload = template()
            if args.output:
                Path(args.output).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(payload, indent=2)); return 0
        result = execute(Path(args.config).resolve(), Path(args.output_dir).resolve())
        print(json.dumps(result, indent=2)); return 0
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
