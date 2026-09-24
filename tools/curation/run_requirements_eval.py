"""Run paired requirements-to-AC evaluations through isolated Pi processes."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

CANDIDATE_FILES = (
    "problem-framing/SKILL.md",
    "problem-framing/contract.json",
    "requirements-rules/SKILL.md",
    "requirements-rules/contract.json",
    "acceptance-criteria/SKILL.md",
    "acceptance-criteria/contract.json",
    "requirements-quality-gate/SKILL.md",
    "requirements-quality-gate/contract.json",
)
BASELINE_FILES = ("prd-development/SKILL.md", "prd-development/template.md")


def load_cases(path: Path) -> list[dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        raise ValueError("cases JSON must contain a cases array")
    return cases


def prompt_for(case: dict[str, object], files: list[Path], mode: str) -> str:
    materials = "\n\n".join(
        f"===== {path.as_posix()} =====\n{path.read_text(encoding='utf-8')}"
        for path in files
    )
    role = (
        "Apply the four candidate capability contracts in their declared order."
        if mode == "candidate"
        else "Apply only the original skill materials below as the baseline."
    )
    return f"""You are an isolated offline evaluation worker. {role}
Do not use tools, network, repository context, case files, rubrics, or prior outputs.
Use only the supplied task and method materials. Preserve unknowns and authority.
Return the complete artifact in Markdown. Start the first line with exactly `Status: passed`, `Status: needs-input`, `Status: blocked`, or `Status: failed`; you may repeat it at the end.

TASK:
{case['prompt']}

METHOD MATERIALS:
{materials}
"""


def pi_run(prompt: str, model: str | None) -> tuple[str, dict[str, object], float]:
    executable = shutil.which("pi") or shutil.which("pi.cmd")
    if executable is None:
        raise RuntimeError("pi executable is unavailable")
    command = [
        executable, "-p", "--mode", "json", "--no-tools", "--no-skills",
        "--no-extensions", "--no-context-files", "--no-session",
        "--system-prompt", "Follow the evaluation prompt exactly. Do not ask questions outside the requested artifact.",
    ]
    if model:
        command.extend(["--model", model])
    started = time.perf_counter()
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(prompt)
        prompt_path = Path(handle.name)
    try:
        process = subprocess.run(command + [f"@{prompt_path}"], capture_output=True, check=False)
    finally:
        prompt_path.unlink(missing_ok=True)
    duration_ms = round((time.perf_counter() - started) * 1000, 3)
    stdout = process.stdout.decode("utf-8", errors="replace")
    stderr = process.stderr.decode("utf-8", errors="replace")
    if process.returncode:
        raise RuntimeError(stderr.strip() or f"pi exited {process.returncode}")
    events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    ends = [event for event in events if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"]
    if not ends:
        raise RuntimeError("pi emitted no assistant result")
    message = ends[-1]["message"]
    output = "".join(part.get("text", "") for part in message.get("content", []) if part.get("type") == "text")
    usage = message.get("usage", {})
    metadata = {
        "provider": message.get("provider"),
        "model": message.get("model"),
        "response_model": message.get("responseModel"),
        "stop_reason": message.get("stopReason"),
        "usage": usage,
    }
    return output.strip() + "\n", metadata, duration_ms


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_one(case: dict[str, object], out: Path, files: list[Path], mode: str, model: str | None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    prompt = prompt_for(case, files, mode)
    output, metadata, duration_ms = pi_run(prompt, model)
    output_path = out / "full_output.md"
    raw_path = out / "tool_evidence.raw.json"
    evidence_path = out / "tool_evidence.json"
    run_path = out / "run.json"
    output_path.write_text(output, encoding="utf-8")
    raw = {
        "case_id": case["id"], "offline": True, "network_accessed": False,
        "skills_modified": False, "case_file_read": False, "rubric_read": False,
        "slots_read": mode == "candidate", "paths_read": [path.as_posix() for path in files],
        "paths_written": [output_path.as_posix(), raw_path.as_posix()], "errors": [],
        "runtime": metadata,
    }
    raw_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    evidence = {
        "case_id": case["id"], "offline": True, "network_accessed": False,
        "skills_modified": False,
        "artifacts": {
            "full_output": {"path": "full_output.md", "sha256": sha256(output_path)},
            "raw_tool_evidence": {"path": "tool_evidence.raw.json", "sha256": sha256(raw_path)},
        },
        "agent_evidence": raw,
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    usage = metadata.get("usage", {})
    total_tokens = usage.get("totalTokens", usage.get("total_tokens", 0)) if isinstance(usage, dict) else 0
    run = {
        "case_id": case["id"],
        "source_skill": "candidate:requirements-to-ac@0.2.0-candidate" if mode == "candidate" else "baseline:prd-development",
        "full_output": "full_output.md", "full_output_sha256": sha256(output_path),
        "tool_evidence": "tool_evidence.json", "tool_evidence_sha256": sha256(evidence_path),
        "model": "/".join(str(metadata.get(key)) for key in ("provider", "model")),
        "input_hash": hashlib.sha256(str(case["prompt"]).encode()).hexdigest(),
        "tool_permissions": [], "budget": {"agent_turns": 1, "network": False},
        "offline": True, "duration_ms": duration_ms,
        "token_usage": {"total_tokens": total_tokens}, "exit_status": "completed",
        "failure_reason": None, "batch_role": mode, "reported_tool_failures": [],
    }
    run_path.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "timing.json").write_text(json.dumps({
        "total_tokens": total_tokens, "duration_ms": duration_ms,
        "total_duration_seconds": duration_ms / 1000,
    }, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--skills-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--mode", choices=("candidate", "baseline", "paired"), default="paired")
    parser.add_argument("--model")
    parser.add_argument("--case-id", action="append")
    args = parser.parse_args()
    cases = load_cases(args.cases)
    if args.case_id:
        cases = [case for case in cases if case.get("id") in set(args.case_id)]
    configurations = []
    if args.mode in {"candidate", "paired"}:
        configurations.append(("candidate", args.candidate_root, CANDIDATE_FILES))
    if args.mode in {"baseline", "paired"}:
        configurations.append(("baseline", args.skills_root, BASELINE_FILES))
    for mode, root, relative_files in configurations:
        files = [root / relative for relative in relative_files]
        missing = [str(path) for path in files if not path.is_file()]
        if missing:
            raise FileNotFoundError(", ".join(missing))
        destination = args.output_root / mode
        for case in cases:
            run_one(case, destination / str(case["id"]), files, mode, args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
