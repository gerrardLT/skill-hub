from pathlib import Path

from tools.curation.v2_phase1_gate import verify

ROOT = Path(__file__).resolve().parents[2]


def test_phase1_gate_requires_every_semantic_evidence_layer() -> None:
    result = verify(ROOT)

    assert result["ok"] is True, result["errors"]
    checks = {item["name"]: item["ok"] for item in result["checks"]}
    assert checks == {
        "source-and-v1-compatibility": True,
        "root-dossiers": True,
        "file-review-ledger": True,
        "auxiliary-unit-dispositions": True,
        "previously-uncovered-root-atoms": True,
        "cluster-comparisons": True,
        "owner-fusion-policy": True,
    }
