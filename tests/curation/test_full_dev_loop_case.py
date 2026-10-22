import json
from pathlib import Path

from tools.curation.full_dev_loop_case import verify

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "evals/cases/full-dev-loop/ip-rate-limiting-v1.json"

def test_frozen_rate_limit_case_is_complete() -> None:
    result = verify(CASE)
    assert result["ok"] is True, result

def test_case_rejects_missing_stage_cases(tmp_path: Path) -> None:
    value = json.loads(CASE.read_text(encoding="utf-8"))
    del value["stage_cases"]["qa"]
    path = tmp_path / "case.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert verify(path)["ok"] is False
