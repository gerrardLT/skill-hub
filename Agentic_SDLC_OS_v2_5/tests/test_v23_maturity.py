from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


maturity = load_module("v23_maturity", ROOT / "scripts" / "maturity_gate.py")
l5b = load_module("v23_maturity_l5b_fixture", ROOT / "scripts" / "l5b_matched_experiment.py")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class V23MaturityCase(unittest.TestCase):
    def test_current_evidence_cannot_claim_production_candidate(self) -> None:
        result = maturity.assess(ROOT / "validation" / "maturity" / "current-evidence.json", "production-candidate")
        self.assertFalse(result["passed"])
        self.assertIsNone(result["claim_allowed"])
        self.assertIn("insufficient independently verified executable real projects", result["failures"])
        self.assertTrue(any("PostgreSQL" in item for item in result["failures"]))

    def test_synthetic_l5b_cannot_unlock_production_candidate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="sdlc-v23-maturity-") as temp:
            temp_path = Path(temp)
            exp = l5b.new_experiment("synthetic", 3, 1, "h", True)
            for i in range(3):
                l5b.add_task(exp, f"t{i}", f"{i+1:064x}", "web", 2, 10)
            l5b.freeze(exp)
            metrics = {
                "lead_time_minutes": 1, "human_minutes": 1, "token_cost_usd": 1,
                "rework_fraction": 0.1, "escaped_defects": 0, "critical_defects": 0,
                "trace_coverage": 1, "acceptance_pass_rate": 1, "maintainability_score": 8,
            }
            for i in range(3):
                assignment = l5b.assignment_for(exp, f"t{i}")
                for pos, arm in enumerate(assignment["order"]):
                    l5b.record_run(exp, task_id=f"t{i}", arm=arm, executor_code=f"x-{arm}", execution_context_id=f"ctx-{i}-{arm}-{pos}", model="m", prompt_hash=("1" if arm == "baseline" else "2")*64, toolset_hash="3"*64, start_state_hash=f"{i+5:064x}", environment_hash="4"*64, artifact_hash=("5" if arm == "baseline" else "6")*64, run_log_hash=("7" if arm == "baseline" else "8")*64, metrics=metrics)
                for arm in l5b.ARMS:
                    l5b.add_review(exp, blind_artifact_code=assignment["blind_artifact_codes"][arm], reviewer_code="reviewer", correctness=8, completeness=8, maintainability=8, usability=8)
            l5b.seal(exp)
            exp_path = temp_path / "exp.json"
            l5b.atomic_write(exp_path, exp)
            evidence = maturity.template()
            evidence["real_projects"] = [
                {"name": f"p{i}", "executable": True, "verified": True, "artifact": str(exp_path), "sha256": file_hash(exp_path)} for i in range(3)
            ]
            evidence["l5b"] = {"experiment_path": str(exp_path), "sha256": file_hash(exp_path)}
            pg_report = temp_path / "pg.json"; pg_report.write_text("{}")
            soak_report = temp_path / "soak.json"; soak_report.write_text("{}")
            org_report = temp_path / "org.json"; org_report.write_text("{}")
            evidence["postgresql"] = {"passed": True, "live": True, "concurrency_stress": True, "recovery_drill": True, "artifact": str(pg_report), "sha256": file_hash(pg_report)}
            evidence["soak"] = {"days": 30, "p0_incidents": 0, "p1_control_plane_incidents": 0, "artifact": str(soak_report), "sha256": file_hash(soak_report)}
            evidence["organization_drills"] = {"rbac": True, "secret_rotation": True, "backup_restore": True, "audit_export": True, "artifact": str(org_report), "sha256": file_hash(org_report)}
            evidence_path = temp_path / "evidence.json"; evidence_path.write_text(json.dumps(evidence))
            result = maturity.assess(evidence_path, "production-candidate")
            self.assertFalse(result["passed"])
            self.assertIn("l5b is synthetic", result["failures"])


if __name__ == "__main__":
    unittest.main()
