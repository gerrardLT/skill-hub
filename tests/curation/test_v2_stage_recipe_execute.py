"""Verify recipe_execute can execute V2 consolidated stage recipes with skill_ref and dependency_records."""
import json
import tempfile
from pathlib import Path
from tools.curation.recipe_execute import _topological_steps, execute_recipe

def test_topological_steps_with_v2_dependency_records():
    recipe = {
        "id": "test-v2-stage",
        "version": "1.0.0",
        "steps": [
            {"id": "step-b", "skill_ref": "b@1.0.0"},
            {"id": "step-a", "skill_ref": "a@1.0.0"},
            {"id": "step-c", "skill_ref": "c@1.0.0"}
        ],
        "dependency_records": [
            {
                "id": "dep-1",
                "kind": "hard",
                "source_capability_id": "capability:step-a",
                "target_capability_id": "capability:step-b"
            },
            {
                "id": "dep-2",
                "kind": "hard",
                "source_capability_id": "capability:step-b",
                "target_capability_id": "capability:step-c"
            }
        ]
    }
    
    ordered = _topological_steps(recipe)
    order_ids = [s["id"] for s in ordered]
    assert order_ids == ["step-a", "step-b", "step-c"], f"Expected a, b, c but got {order_ids}"

def test_execute_v2_recipe_mock():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        
        # Create a mock V2 consolidated skill
        skill_dir = tdp / "mock-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "contract.json").write_text(json.dumps({
            "id": "mock-skill",
            "responsibility": "Mock capability",
            "inputs": ["test_input"],
            "outputs": ["mock-artifact"],
            "hard_gates": [],
            "execution": {"adapter": "artifact"}
        }))
        (skill_dir / "SKILL.md").write_text("# Mock Skill\nDo mock work.")
        
        # Create a mock V2 stage recipe
        recipe_p = tdp / "recipe.json"
        recipe_p.write_text(json.dumps({
            "id": "mock-stage",
            "version": "1.0.0",
            "inputs": ["test_input"],
            "steps": [
                {
                    "id": "mock-skill",
                    "skill_ref": "mock-skill@1.0.0",
                    "candidate_path": str(skill_dir),
                    "inputs": ["test_input"],
                    "outputs": ["mock-artifact"]
                }
            ],
            "dependency_records": []
        }))
        
        inp_p = tdp / "input.json"
        inp_p.write_text(json.dumps({"test_input": "hello"}))
        
        out_dir = tdp / "out"
        
        def mock_worker(prompt: str, timeout: int):
            return "Status: passed\n\n## Output\nSuccess", {}
            
        res = execute_recipe(
            recipe_p, inp_p, out_dir,
            workspace_root=tdp,
            require_release_evidence=False,
            allow_evaluating=True,
            worker=mock_worker
        )
def test_execute_v2_end_to_end_3step_pipeline():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        workspace = Path('.').resolve()
        
        # Build a 3-step V2 composite recipe using real consolidated-68 skills
        stage4_dir = workspace / 'evals/candidates/capability-compiler-v2/consolidated-68/skills'
        
        recipe_p = tdp / "test-v2-pipeline.json"
        recipe_p.write_text(json.dumps({
            "id": "v2-e2e-feature-intake",
            "version": "1.0.0",
            "inputs": ["feature_intent"],
            "steps": [
                {
                    "id": "requirements-and-delivery-contract",
                    "skill_ref": "requirements-and-delivery-contract@1.1.0-consolidated",
                    "candidate_path": str((stage4_dir / "requirements-and-delivery-contract").relative_to(workspace).as_posix()),
                    "inputs": ["feature_intent"],
                    "outputs": ["requirements_contract"]
                },
                {
                    "id": "implementation-planning-and-handoff",
                    "skill_ref": "implementation-planning-and-handoff@1.1.0-consolidated",
                    "candidate_path": str((stage4_dir / "implementation-planning-and-handoff").relative_to(workspace).as_posix()),
                    "inputs": ["requirements_contract"],
                    "outputs": ["implementation_plan"]
                },
                {
                    "id": "independent-plan-review",
                    "skill_ref": "independent-plan-review@1.1.0-consolidated",
                    "candidate_path": str((stage4_dir / "independent-plan-review").relative_to(workspace).as_posix()),
                    "inputs": ["implementation_plan"],
                    "outputs": ["review_recommendation"]
                }
            ],
            "dependency_records": [
                {
                    "id": "dep-req-to-plan",
                    "kind": "hard",
                    "source_capability_id": "capability:requirements-and-delivery-contract",
                    "target_capability_id": "capability:implementation-planning-and-handoff"
                },
                {
                    "id": "dep-plan-to-review",
                    "kind": "hard",
                    "source_capability_id": "capability:implementation-planning-and-handoff",
                    "target_capability_id": "capability:independent-plan-review"
                }
            ]
        }))
        
        inp_p = tdp / "input.json"
        inp_p.write_text(json.dumps({"feature_intent": "Implement rate limiting middleware with Redis token bucket"}))
        
        out_dir = tdp / "out"
        state_dir = tdp / "state"
        
        step_outputs = {
            "requirements-and-delivery-contract": "Status: passed\n\n## Requirements\n- Rate limit 100 req/min per IP\n- Return HTTP 429 when exceeded",
            "implementation-planning-and-handoff": "Status: passed\n\n## Implementation Plan\n1. Add Redis client\n2. Add rate limit middleware\n3. Write unit tests",
            "independent-plan-review": "Status: passed\n\n## Review Recommendation\nVerdict: PASSED without remediation"
        }
        
        def mock_worker(prompt: str, timeout: int):
            for sid, out in step_outputs.items():
                if f"executing slot: {sid}" in prompt:
                    return out, {}
            return "Status: passed\n\nDefault output", {}
            
        res = execute_recipe(
            recipe_p, inp_p, out_dir,
            workspace_root=workspace,
            state_dir=state_dir,
            require_release_evidence=False,
            allow_evaluating=True,
            worker=mock_worker
        )
        
        assert res["passed"] is True
        assert res["status"] == "passed"
        assert len(res["steps_run"]) == 3
        
        # Verify topological execution order
        executed_steps = [s["step_id"] for s in res["steps_run"]]
        assert executed_steps == [
            "requirements-and-delivery-contract",
            "implementation-planning-and-handoff",
            "independent-plan-review"
        ]
        
        # Verify state persistence
        assert (state_dir / "state.json").exists()
        assert (state_dir / "state.md").exists()
        assert (out_dir / "result.json").exists()
        assert (out_dir / "requirements-and-delivery-contract.md").exists()
        assert (out_dir / "implementation-planning-and-handoff.md").exists()
        assert (out_dir / "independent-plan-review.md").exists()


def test_select_mode_loads_only_requested_mode():
    from tools.curation.recipe_execute import select_mode
    doc = """---
name: x
---

# X

## Mode selection

| Mode | Use when |
| --- | --- |
| `a` | alpha |

## Mode: `a`

### A title

A body.

## Mode: `b`

### B title

B body.
"""
    out = select_mode(doc, 'a')
    assert '## Mode selection' in out, "preamble with mode table must survive"
    assert 'A body.' in out
    assert 'B body.' not in out, "unselected mode must not be loaded"

    # an unknown mode on a document with no such section returns the document unchanged;
    # the executor is what rejects an unknown mode for a skill that declares modes.
    assert select_mode(doc, 'missing') == doc
    assert select_mode('single mode doc', 'anything') == 'single mode doc'


def test_resolve_permission_uses_selected_mode_and_never_widens():
    from tools.curation.recipe_execute import resolve_permission
    contract = {
        'permission_identity': 'remote-write-authorized-only',
        'mode_permissions': {
            'read-only-mode': 'read-only',
            'write-mode': 'workspace-write',
            'deploy-mode': 'remote-write-authorized-only',
        },
    }
    assert resolve_permission(contract, 'read-only-mode') == 'read-only'
    assert resolve_permission(contract, 'write-mode') == 'workspace-write'
    assert resolve_permission(contract, 'deploy-mode') == 'remote-write-authorized-only'
    # an unknown or absent mode falls back to the document default
    assert resolve_permission(contract, None) == 'remote-write-authorized-only'
    assert resolve_permission(contract, 'unknown') == 'remote-write-authorized-only'


def test_machine_gates_are_deterministic_and_discriminating():
    from tools.curation.v2_machine_gates import evaluate_machine_gate, compile_machine_gates

    good = (
        "Status: needs-input\n\n"
        "## Unknowns\n"
        "- UNK-1: approval record not supplied\n"
        "- UNK-2: window semantics unspecified\n\n"
        "## Authority\n"
        "Approval is required from the platform owner; not authorized to deploy.\n\n"
        "## Evidence\n"
        "Refs: SRC-1, EV-2, src/app.py:41\n\n"
        "No tools were available; nothing was executed and no changes were made.\n"
    )
    for gate in ('status-declared', 'non-execution-stated', 'unknowns-preserved',
                 'authority-named', 'evidence-binding'):
        assert evaluate_machine_gate(gate, good, {})['passed'] is True, gate

    bad = "# Report\n\nEverything is complete and the feature is deployed.\n"
    for gate in ('status-declared', 'non-execution-stated', 'unknowns-preserved',
                 'authority-named', 'evidence-binding'):
        assert evaluate_machine_gate(gate, bad, {})['passed'] is False, gate

    # an unknown gate id is a defect, never a silent pass
    result = evaluate_machine_gate('not-a-gate', good, {})
    assert result['passed'] is False and 'error' in result

    contract = {'permission_identity': 'read-only',
                'policy': {'human_decision': True, 'coverage': ['provenance', 'uncertainty']}}
    gates = compile_machine_gates(contract)
    assert 'status-declared' in gates and 'non-execution-stated' in gates
    assert 'unknowns-preserved' in gates and 'authority-named' in gates
    assert 'evidence-binding' in gates

    lean = {'permission_identity': 'workspace-write', 'policy': {'coverage': []}}
    assert compile_machine_gates(lean) == ['status-declared', 'non-execution-stated']


def test_conditional_steps_are_opt_in_and_disabled_steps_never_run():
    from tools.curation.recipe_execute import _step_is_runnable
    conditional = {'id': 'a', 'activation': 'conditional', 'default_state': 'skipped'}
    disabled = {'id': 'b', 'activation': 'disabled-pending-current-authorization'}
    plain = {'id': 'c'}

    # conditional steps are skipped unless the caller names them
    assert _step_is_runnable(conditional, None) is False
    assert _step_is_runnable(conditional, set()) is False
    assert _step_is_runnable(conditional, {'other'}) is False
    assert _step_is_runnable(conditional, {'a'}) is True

    # a disabled step never runs, even when explicitly requested
    assert _step_is_runnable(disabled, None) is False
    assert _step_is_runnable(disabled, {'b'}) is False

    # a step with no activation runs by default
    assert _step_is_runnable(plain, None) is True
