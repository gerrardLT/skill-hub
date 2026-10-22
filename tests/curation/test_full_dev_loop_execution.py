import json
from pathlib import Path

from tools.curation.recipe_route import build_catalog, route_request

ROOT = Path(__file__).resolve().parents[2]


def artifact_output(slot: str) -> str:
    if slot == "problem-framing":
        return "Status: passed\nEvidence: Source SRC-1\nResponsibility: frame\nGate Results: passed\nUnknowns: none identified"
    if slot == "requirements-rules":
        return "Status: passed\nEvidence: SRC-1\nREQ-1 requirement\nRULE-1 unknown parameterized\nResponsibility: rules\nGate Results: passed\nUnknowns: unknown"
    if slot == "acceptance-criteria":
        return "Status: passed\nEvidence: EV-1\n### AC-1 success\n**Given** ready\n**When** used\n**Then** result remains available\nResponsibility: criteria\nGate Results: passed\nUnknowns: none identified"
    if slot == "requirements-quality-gate":
        return "Status: passed\nEvidence: EV-1 EV-2 EV-3\nEvidence Citations\nVerdict: passed\nread-only\nResponsibility: review\nGate Results: passed\nUnknowns: none identified"
    return "Status: passed\nEvidence: EV-1\nResponsibility: bounded\nAuthority: supplied\nGate Results: passed\nUnknowns: none identified"


def test_released_full_loop_is_executable_by_exact_ref(tmp_path: Path) -> None:
    catalog = build_catalog(ROOT / "recipes", ROOT / "slots", ROOT)
    assert route_request("", catalog, explicit_ref="full-dev-loop@1.0.0")["status"] == "matched"
