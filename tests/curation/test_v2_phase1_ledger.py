import json
from pathlib import Path

from tools.curation.v2_phase1_ledger import build, verify_reviewed

ROOT = Path(__file__).resolve().parents[2]


def test_phase1_ledger_covers_every_source_file_and_root() -> None:
    ledger = build(ROOT)

    assert ledger["ok"] is True, ledger["errors"]
    assert ledger["counts"] == {
        "roots": 139,
        "unique_skill_bodies": 134,
        "duplicate_body_groups": 5,
        "files": 2337,
        "semantic-review-required": 1094,
        "behavior-review-required": 1229,
        "excluded": 14,
    }
    assert all(item["owner_roots"] for item in ledger["files"])
    assert {item["path"] for item in ledger["files"] if Path(item["path"]).name == "SKILL.md"} == {item["skill_path"] for item in ledger["roots"]}


def test_phase1_does_not_treat_legacy_read_claims_as_v2_review() -> None:
    ledger = build(ROOT)
    prd = next(item for item in ledger["files"] if item["path"] == "prd-development/SKILL.md")

    assert prd["legacy_coverage"][0]["status"] == "read"
    assert prd["v2_status"] == "semantic-review-required"
    assert prd["review_evidence"] == []


def test_phase1_review_gate_rejects_pending_files_and_roots() -> None:
    ledger = build(ROOT)
    errors = verify_reviewed(ledger)

    assert any(error.startswith("root not semantically reviewed") for error in errors)
    assert any(error.startswith("file not reviewed") for error in errors)


def test_phase1_review_gate_accepts_evidenced_review() -> None:
    ledger = {
        "roots": [{"id": "skill-root:x", "v2_status": "semantic-read", "dossier": "x.md", "review_evidence": ["review.json"]}],
        "files": [
            {"path": "x/SKILL.md", "v2_status": "semantic-read", "reason": None, "review_evidence": ["review.json"]},
            {"path": "x/icon.png", "v2_status": "excluded", "reason": "binary-asset-inventory-only", "subkind": "binary", "review_evidence": []},
            {"path": "x/script.py", "v2_status": "behavior-reviewed", "reason": None, "review_evidence": ["script-review.json"]},
        ],
    }

    assert verify_reviewed(ledger) == []
