import json
from pathlib import Path

from tools.curation.full_dev_loop_security import verify

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "evals/runs/full-dev-loop/ip-rate-limiting-v1/run"


def test_real_run_has_no_dangerous_execution_authority() -> None:
    result = verify(RUN)
    assert result["ok"] is True, result
    assert result["checked_executions"] >= 4


def test_security_gate_rejects_network_tool(tmp_path: Path) -> None:
    run = tmp_path / "run"
    evidence = run / "step/execution.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text(json.dumps({
        "tools": ["read", "network"],
        "command_results": [],
        "source_head": "a",
        "isolated_head": "a",
        "incremental_patch_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }), encoding="utf-8")
    package = tmp_path / "delivery-package"
    package.mkdir()
    (package / "manifest.json").write_text(json.dumps({
        "remote_actions": [], "merge_performed": False, "deployment_performed": False,
    }), encoding="utf-8")
    result = verify(run)
    assert result["ok"] is False
    assert any("forbidden tool" in error for error in result["errors"])
