from collections import Counter
from pathlib import Path

from tools.curation.v2_root_atomic_units import compile_units, verify

ROOT = Path(__file__).resolve().parents[2]


def test_missing_90_roots_get_exact_source_grounded_atomic_candidates(tmp_path: Path) -> None:
    data = compile_units(ROOT)

    assert data["ok"] is True, data["errors"]
    assert data["previously_clustered_roots"] == 49
    assert data["derived_root_count"] == 90
    assert data["derived_unit_count"] == 1138
    assert data["distinct_excerpt_count"] == 930
    assert data["merged_exact_duplicates"] == 208
    assert set(data["root_unit_counts"]) == {unit["root_id"] for unit in data["units"]}


def test_shared_runtime_sections_are_exactly_merged_not_counted_as_unique_capabilities() -> None:
    data = compile_units(ROOT)
    dispositions = Counter(unit["v2_disposition"] for unit in data["units"])

    assert dispositions == {"defer": 930, "merge": 208}
    assert all(unit["target_cluster_id"] is None for unit in data["units"])
    assert all(unit["target_unit_id"] for unit in data["units"] if unit["v2_disposition"] == "merge")


def test_derived_unit_file_revalidates_source_hash_lines_and_merges(tmp_path: Path) -> None:
    from tools.curation.v2_root_atomic_units import write

    output = tmp_path / "root-derived.json"
    write(output, compile_units(ROOT))

    result = verify(ROOT, output)

    assert result["ok"] is True, result["errors"]
    assert result["derived_root_count"] == 90
    assert result["derived_unit_count"] == 1138
