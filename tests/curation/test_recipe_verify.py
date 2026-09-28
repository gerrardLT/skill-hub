import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / "tools" / "curation" / "recipe_verify.py"


def write_slot(
    root: Path,
    slot_id: str,
    *,
    status: str = "released",
    version: str = "1.0.0",
    permissions=None,
    gates=None,
    input_keys=None,
    output_keys=None,
) -> None:
    path = root / slot_id
    path.mkdir(parents=True, exist_ok=True)
    (path / "contract.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "id": slot_id,
                "version": version,
                "status": status,
                "responsibility": f"Execute {slot_id}.",
                "inputs": input_keys or [],
                "outputs": output_keys or [],
                "boundaries": {"input": "Declared input.", "output": "Declared output."},
                "dependencies": [],
                "permissions": {"default": permissions or []},
                "statuses": ["passed", "failed", "needs-input", "blocked"],
                "gates": gates or [],
                "forbidden_actions": ["invent evidence"],
                "hard_failures": ["fabricated-evidence"],
                "artifact_types": ["markdown"],
            }
        ),
        encoding="utf-8",
    )


def recipe() -> dict:
    return {
        "id": "build-and-check",
        "version": "1.0.0",
        "status": "released",
        "description": "Build and check an artifact.",
        "inputs": ["request"],
        "outputs": ["report"],
        "permissions": ["read", "test"],
        "steps": [
            {
                "id": "build",
                "slot": "builder",
                "ref": "builder@1.0.0",
                "input_map": {"request": "request"},
                "output_map": {"result": "artifact"},
                "depends_on": [],
                "gates": ["ready"],
                "permissions": ["read"],
            },
            {
                "id": "check",
                "slot": "checker",
                "ref": "checker@1.0.0",
                "input_map": {"subject": "artifact"},
                "output_map": {"report": "report"},
                "depends_on": ["build"],
                "gates": ["verified"],
                "permissions": ["test"],
            },
        ],
        "edges": [{"from": "build", "to": "check"}],
        "gates": ["ready", "verified"],
        "failure_routes": [
            {
                "from": "check",
                "to": "build",
                "on_status": ["needs-input", "failed", "blocked"],
                "action": "invalidate-and-rerun",
            }
        ],
        "evidence": {
            "composition_runs": [{"path": "evals/runs/composition/build-and-check/result.json", "sha256": "0" * 64}],
            "review": {"path": "evals/runs/composition/build-and-check/review.json", "sha256": "0" * 64},
        },
    }


def run_verify(tmp_path: Path, value: dict, *, one_file: bool = False):
    recipes = tmp_path / "recipes"
    slots = tmp_path / "slots"
    recipes.mkdir(exist_ok=True)
    (recipes / "schema.json").write_text((ROOT / "recipes" / "schema.json").read_text(encoding="utf-8"), encoding="utf-8")
    slots.mkdir(exist_ok=True)
    (slots / "schema.json").write_text((ROOT / "slots" / "schema.json").read_text(encoding="utf-8"), encoding="utf-8")
    write_slot(
        slots,
        "builder",
        permissions=["read"],
        gates=["ready"],
        input_keys=["request"],
        output_keys=["result"],
    )
    write_slot(
        slots,
        "checker",
        permissions=["test"],
        gates=["verified"],
        input_keys=["subject"],
        output_keys=["report"],
    )
    composition_run = tmp_path / "evals" / "runs" / "composition" / "build-and-check"
    composition_run.mkdir(parents=True, exist_ok=True)
    (composition_run / "result.json").write_text('{"passed": true, "recipe_id": "build-and-check"}\n', encoding="utf-8")
    review = composition_run / "review.json"
    review.write_text('{"verdict": "approved"}\n', encoding="utf-8")
    value["evidence"]["composition_runs"][0]["sha256"] = hashlib.sha256((composition_run / "result.json").read_bytes()).hexdigest()
    value["evidence"]["review"]["sha256"] = hashlib.sha256(review.read_bytes()).hexdigest()
    path = recipes / "recipe.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    args = [sys.executable, str(VERIFY), "--recipes-root", str(recipes), "--slots-root", str(slots), "--workspace-root", str(tmp_path)]
    if one_file:
        args += ["--recipe", str(path)]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env)
    return result, json.loads(result.stdout), slots


def assert_rejected(result, report, code: str) -> None:
    assert result.returncode == 1
    assert report["ok"] is False
    assert code in {error["code"] for error in report["errors"]}


def test_accepts_valid_graph_and_explicit_recipe_input(tmp_path: Path) -> None:
    result, report, _ = run_verify(tmp_path, recipe(), one_file=True)
    assert result.returncode == 0, report
    assert report["ok"] is True
    assert report["errors"] == []


def test_rejects_missing_slot(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["slot"] = "missing"
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "missing-slot")


def test_rejects_unreleased_slot(tmp_path: Path) -> None:
    value = recipe()
    result, report, slots = run_verify(tmp_path, value)
    write_slot(
        slots,
        "builder",
        status="evaluating",
        permissions=["read"],
        gates=["ready"],
        input_keys=["request"],
        output_keys=["result"],
    )
    result = subprocess.run(result.args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert_rejected(result, json.loads(result.stdout), "unreleased-slot")


def test_rejects_step_cycle(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["depends_on"] = ["check"]
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "step-cycle")


def test_rejects_input_without_external_or_upstream_producer(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][1]["input_map"] = {"subject": "missing-artifact"}
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "input-without-producer")


def test_rejects_parallel_writes_to_same_artifact(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][1]["input_map"] = {"subject": "request"}
    value["steps"][1]["output_map"] = {"report": "artifact"}
    value["steps"][1]["depends_on"] = []
    value["edges"] = []
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "parallel-artifact-write")


def test_rejects_unknown_gate(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["gates"] = ["invented"]
    value["gates"].append("invented")
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "unknown-gate")


def test_rejects_permission_escalation(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["permissions"] = ["deploy"]
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "permission-escalation")


def test_rejects_inline_method_body_or_instructions(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["instructions"] = "Copy and execute the complete method here."
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "schema")


def test_rejects_draft_recipe(tmp_path: Path) -> None:
    value = recipe()
    value["status"] = "draft"
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "unreleased-recipe")


def test_rejects_empty_recipe_set(tmp_path: Path) -> None:
    recipes = tmp_path / "recipes"
    slots = tmp_path / "slots"
    recipes.mkdir()
    slots.mkdir()
    (recipes / "schema.json").write_text("{}\n", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            str(VERIFY),
            "--recipes-root",
            str(recipes),
            "--slots-root",
            str(slots),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    report = json.loads(result.stdout)

    assert_rejected(result, report, "missing-recipe")
    assert report["checked"] == []


def test_rejects_duplicate_slot_identity(tmp_path: Path) -> None:
    value = recipe()
    result, _, slots = run_verify(tmp_path, value)
    duplicate = slots / "duplicate-builder"
    duplicate.mkdir()
    (duplicate / "contract.json").write_text((slots / "builder" / "contract.json").read_text(encoding="utf-8"), encoding="utf-8")

    repeated = subprocess.run(result.args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")

    assert_rejected(repeated, json.loads(repeated.stdout), "slot-id-mismatch")


def test_rejects_unsafe_evidence_path(tmp_path: Path) -> None:
    value = recipe()
    value["evidence"]["composition_runs"][0]["path"] = "../escape/result.json"
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "missing-release-evidence")


def test_rejects_slot_version_mismatch(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["ref"] = "builder@2.0.0"
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "slot-version-mismatch")


def test_rejects_unknown_slot_input_key(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["input_map"] = {"invented": "request"}
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "unknown-slot-input")


def test_rejects_unknown_slot_output_key(tmp_path: Path) -> None:
    value = recipe()
    value["steps"][0]["output_map"] = {"invented": "artifact"}
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "unknown-slot-output")


def test_rejects_recipe_output_without_producer(tmp_path: Path) -> None:
    value = recipe()
    value["outputs"] = ["unproduced-report"]
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "output-without-producer")


def test_rejects_released_recipe_without_evidence(tmp_path: Path) -> None:
    value = recipe()
    value["evidence"] = {
        "composition_runs": [{"path": "evals/runs/composition/missing/result.json", "sha256": "0" * 64}],
        "review": {"path": "evals/runs/composition/missing/review.json", "sha256": "0" * 64},
    }
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "missing-release-evidence")


def test_rejects_failure_route_without_status_or_action(tmp_path: Path) -> None:
    value = recipe()
    value["failure_routes"] = [{"from": "check", "to": "build"}]
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "schema")


def test_rejects_failure_route_that_does_not_invalidate_evidence(tmp_path: Path) -> None:
    value = recipe()
    value["failure_routes"][0]["action"] = "continue"
    result, report, _ = run_verify(tmp_path, value)
    assert_rejected(result, report, "schema")


def test_legacy_released_recipe_remains_schema_compatible(tmp_path: Path) -> None:
    value = recipe()
    assert "routing" not in value
    assert "retry_policy" not in value

    result, report, _ = run_verify(tmp_path, value)

    assert result.returncode == 0, report


def test_rejects_recursive_subrecipe_cycle(tmp_path: Path) -> None:
    value = recipe()
    recipes = tmp_path / "recipes"
    slots = tmp_path / "slots"
    recipes.mkdir()
    slots.mkdir()
    (recipes / "schema.json").write_text((ROOT / "recipes/schema.json").read_text(encoding="utf-8"), encoding="utf-8")
    (slots / "schema.json").write_text((ROOT / "slots/schema.json").read_text(encoding="utf-8"), encoding="utf-8")
    evidence_root = tmp_path / "evals/runs/composition/cycle"
    evidence_root.mkdir(parents=True)
    result_file = evidence_root / "result.json"
    result_file.write_text('{"passed": true}\n', encoding="utf-8")
    review = evidence_root / "review.json"
    review.write_text('{"verdict": "approved"}\n', encoding="utf-8")
    evidence = {
        "composition_runs": [{"path": result_file.relative_to(tmp_path).as_posix(), "sha256": hashlib.sha256(result_file.read_bytes()).hexdigest()}],
        "review": {"path": review.relative_to(tmp_path).as_posix(), "sha256": hashlib.sha256(review.read_bytes()).hexdigest()},
    }
    def composite(recipe_id: str, child: str) -> dict:
        return {
            "id": recipe_id, "version": "1.0.0", "status": "released", "description": recipe_id,
            "inputs": ["request"], "outputs": ["report"], "permissions": ["read"],
            "steps": [{"id": "child", "recipe": f"{child}@1.0.0", "input_map": {"request": "request"}, "output_map": {"report": "report"}, "depends_on": [], "gates": ["ready"], "permissions": ["read"]}],
            "edges": [], "gates": ["ready"], "failure_routes": [], "evidence": evidence,
        }
    (recipes / "a.json").write_text(json.dumps(composite("a", "b")), encoding="utf-8")
    (recipes / "b.json").write_text(json.dumps(composite("b", "a")), encoding="utf-8")

    process = subprocess.run([sys.executable, str(VERIFY), "--recipes-root", str(recipes), "--slots-root", str(slots), "--workspace-root", str(tmp_path)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    report = json.loads(process.stdout)

    assert_rejected(process, report, "recipe-cycle")


def test_retry_policy_requires_unique_failure_routes_for_every_status(tmp_path: Path) -> None:
    value = recipe()
    value["retry_policy"] = {"max_attempts": 2, "stop_on_repeated_failure": True}

    result, report, _ = run_verify(tmp_path, value)

    assert_rejected(result, report, "missing-failure-route")


def test_recipe_step_cannot_exceed_recipe_permission_boundary(tmp_path: Path) -> None:
    value = recipe()
    value["permissions"] = ["test"]

    result, report, _ = run_verify(tmp_path, value)

    assert_rejected(result, report, "permission-escalation")
