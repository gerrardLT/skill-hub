from pathlib import Path

from tools.curation import mutation_verify


ROOT = Path(__file__).resolve().parents[3]


def test_unmutated_candidate_satisfies_objective_contract_checks() -> None:
    report = mutation_verify.verify_candidate(ROOT / "slots")

    assert report == {"passed": True, "errors": []}


def test_each_required_mutation_is_detected() -> None:
    report = mutation_verify.run_mutation_suite(ROOT / "slots")

    assert report["passed"] is True
    assert len(report["mutations"]) == 5
    assert all(result["detected"] is True for result in report["mutations"])
