from collections import Counter
from pathlib import Path

from tools.curation.v2_auxiliary_dispositions import apply
from tools.curation.v2_auxiliary_units import verify_disposed

ROOT = Path(__file__).resolve().parents[2]


def result() -> dict:
    return apply(
        ROOT,
        ROOT / "curation/v2/units/auxiliary.json",
        ROOT / "curation/v2/units/auxiliary-matches.json",
    )


def test_all_auxiliary_units_receive_evidence_bounded_dispositions() -> None:
    data = result()

    assert data["ok"] is True, data["errors"]
    assert data["count"] == 114
    assert Counter(unit["v2_disposition"] for unit in data["units"]) == {"retain": 104, "defer": 8, "merge": 2}
    assert verify_disposed(data) == []
    assert all(unit["decision_id"] == f"V2-AUX-{index:03d}" for index, unit in enumerate(data["units"], 1))


def test_only_exact_canonical_match_is_merged() -> None:
    data = result()
    merged = [unit for unit in data["units"] if unit["v2_disposition"] == "merge"]

    assert sorted((unit["id"], unit["target_unit_id"], unit["target_cluster_id"]) for unit in merged) == sorted([
        ("skills/qa-only/SKILL.md:429-431", "qao-rule-blackbox-identity", "cluster:independent-blackbox-qa"),
        ("skills/ship/SKILL.md:5-5-review", "skills/ship/SKILL.md:5-5", "cluster:change-delivery-preflight"),
    ])


def test_unsupported_legacy_summaries_are_deferred_not_silently_retained() -> None:
    data = result()
    deferred = [unit for unit in data["units"] if unit["v2_disposition"] == "defer"]

    assert len(deferred) == 8
    assert all(unit["source_validation"] == "unsupported-summary" for unit in deferred)
    assert all(unit["source_support_score"] < 0.75 and unit["defer_reason"] for unit in deferred)


def test_aesthetic_rules_remain_contextual_variants() -> None:
    data = result()
    aesthetic = [
        unit for unit in data["units"]
        if unit["id"].startswith("impeccable:craft-floor:refuse-")
    ]

    assert aesthetic
    assert all(unit["v2_disposition"] == "retain" for unit in aesthetic)
    assert all("Contextual aesthetic variant" in unit["decision_rationale"] for unit in aesthetic)
    assert all(unit["target_cluster_id"] in {
        "cluster:design-context-and-direction-contract",
        "cluster:interaction-states-forms-and-navigation",
        "cluster:design-system-foundation-and-token-extraction",
    } for unit in aesthetic)
