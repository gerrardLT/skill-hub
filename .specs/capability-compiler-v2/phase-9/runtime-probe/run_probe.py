from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parent
prompt = root / "prompt.md"
command = [
    r"C:\Program Files\nodejs\pi.cmd",
    "-p", "--mode", "json", "--model", "cx/gpt-5.6-sol", "--thinking", "low",
    "--no-tools", "--no-skills", "--no-extensions", "--no-context-files", "--no-session",
    "--system-prompt", "Obey the prompt exactly. Do not use tools.",
    f"@{prompt}",
]
started = time.time()
process = subprocess.run(command, capture_output=True, timeout=180)
duration_ms = round((time.time() - started) * 1000, 3)
(root / "events.jsonl").write_bytes(process.stdout)
(root / "stderr.txt").write_bytes(process.stderr)
events = [json.loads(line) for line in process.stdout.decode("utf-8", "replace").splitlines() if line.strip()]
ends = [event for event in events if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"]
message = ends[-1]["message"] if ends else {}
output = "".join(part.get("text", "") for part in message.get("content", []) if part.get("type") == "text")
receipt = {
    "argv": [*command[:-1], "@<prompt.md>"],
    "cwd_policy": "inherited-host-cwd-no-repository-tools",
    "prompt_sha256": hashlib.sha256(prompt.read_bytes()).hexdigest(),
    "events_sha256": hashlib.sha256(process.stdout).hexdigest(),
    "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
    "exit_code": process.returncode,
    "duration_ms": duration_ms,
    "provider": message.get("provider"),
    "model": message.get("model"),
    "response_model": message.get("responseModel"),
    "stop_reason": message.get("stopReason"),
    "usage": message.get("usage"),
    "output": output,
}
(root / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if process.returncode == 0 and ends else 1)
