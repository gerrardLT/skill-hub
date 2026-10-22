import json
from pathlib import Path

from tools.curation.v2_fusion_policy_gate import verify

ROOT = Path(__file__).resolve().parents[2]


def test_owner_approved_fusion_policy_is_complete() -> None:
    result = verify(ROOT)

    assert result == {"gate": "capability-compiler-v2-fusion-policy", "ok": True, "approved_decisions": 7, "errors": []}


def test_fusion_policy_cannot_promote_aesthetic_preferences_to_global_rules(tmp_path: Path) -> None:
    (tmp_path / "curation/v2").mkdir(parents=True)
    policy = json.loads((ROOT / "curation/v2/fusion-policy.json").read_text(encoding="utf-8"))
    policy["global_hard_rules"]["aesthetic_rules"] = "global-hard-rules"
    (tmp_path / "curation/v2/fusion-policy.json").write_text(json.dumps(policy), encoding="utf-8")
    (tmp_path / "curation/v2/decisions.jsonl").write_bytes((ROOT / "curation/v2/decisions.jsonl").read_bytes())

    result = verify(tmp_path)

    assert result["ok"] is False
    assert "aesthetic rules were promoted globally" in result["errors"]
