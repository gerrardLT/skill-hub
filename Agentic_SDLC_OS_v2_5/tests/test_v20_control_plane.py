from __future__ import annotations

import os
import tempfile
import threading
import time
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
os.sys.path.insert(0, str(ROOT / "control_plane"))

from agentic_sdlc_cp.api import create_app
from agentic_sdlc_cp.approvals import ApprovalService
from agentic_sdlc_cp.costs import BudgetService
from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.jobs import JobQueue
from agentic_sdlc_cp.locks import LeaseLockManager
from agentic_sdlc_cp.models import ProjectEvent
from agentic_sdlc_cp.repository import ProjectRepository, RevisionConflict
from agentic_sdlc_cp.security import Identity, generate_master_key, put_secret, resolve_secret


class ControlPlaneCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "control.db"
        self.database = create_database(f"sqlite+pysqlite:///{self.db_path}")
        init_database(self.database)
        self.repo = ProjectRepository()
        with self.database.session() as session:
            self.project = self.repo.create_project(
                session,
                name="Control Plane Test",
                project_id="project-test",
                actor="admin",
                profile="high-assurance",
            )

    def tearDown(self) -> None:
        self.database.engine.dispose()
        self.temp.cleanup()

    def test_revision_audit_restore_and_tamper_detection(self) -> None:
        with self.database.session() as session:
            updated = self.repo.update_state(
                session,
                project_id=self.project.id,
                expected_revision=0,
                actor="agent-a",
                event_type="advance",
                mutate=lambda state: state | {"current_os": "engineering", "current_stage": "BUILD"},
            )
            self.assertEqual(updated.revision, 1)
        with self.database.session() as session:
            with self.assertRaises(RevisionConflict):
                self.repo.update_state(
                    session,
                    project_id=self.project.id,
                    expected_revision=0,
                    actor="agent-b",
                    event_type="stale-write",
                    mutate=lambda state: state,
                )
        with self.database.session() as session:
            result = self.repo.verify_audit_chain(session, self.project.id)
            self.assertTrue(result["valid"], result)
            restored = self.repo.restore_revision(
                session,
                project_id=self.project.id,
                source_revision=0,
                expected_revision=1,
                actor="recovery-admin",
                reason="verified recovery drill",
            )
            self.assertEqual(restored.revision, 2)
            self.assertEqual(restored.current_os, "pm")
        with self.database.session() as session:
            event = session.scalar(select(ProjectEvent).where(ProjectEvent.project_id == self.project.id).order_by(ProjectEvent.sequence).limit(1))
            assert event is not None
            event.payload_json = {"tampered": True}
        with self.database.session() as session:
            result = self.repo.verify_audit_chain(session, self.project.id)
            self.assertFalse(result["valid"])
            self.assertTrue(any("event-hash" in item for item in result["errors"]))

    def test_lease_fencing_and_stale_release(self) -> None:
        manager = LeaseLockManager(self.database)
        first = manager.acquire("project-test", "worker-a", ttl_seconds=0.05, wait_seconds=0.2)
        time.sleep(0.08)
        second = manager.acquire("project-test", "worker-b", ttl_seconds=1, wait_seconds=0.2)
        self.assertGreater(second.fencing_token, first.fencing_token)
        self.assertFalse(manager.release(first))
        renewed = manager.renew(second, ttl_seconds=1)
        self.assertEqual(renewed.fencing_token, second.fencing_token)
        self.assertTrue(manager.release(renewed))

    def test_job_queue_idempotency_retry_and_fencing(self) -> None:
        queue = JobQueue()
        with self.database.session() as session:
            a = queue.enqueue(session, project_id=self.project.id, job_type="build", payload={"x": 1}, idempotency_key="same")
            b = queue.enqueue(session, project_id=self.project.id, job_type="build", payload={"x": 2}, idempotency_key="same")
            self.assertEqual(a.id, b.id)
        with self.database.session() as session:
            lease = queue.lease_next(session, worker_id="worker-a", lease_seconds=5)
            self.assertIsNotNone(lease)
            assert lease is not None
            with self.assertRaises(RuntimeError):
                queue.complete(session, job_id=lease.id, worker_id="worker-b", fencing_token=lease.fencing_token, result={})
            queue.heartbeat(session, job_id=lease.id, worker_id="worker-a", fencing_token=lease.fencing_token, lease_seconds=5)
            row = queue.fail(session, job_id=lease.id, worker_id="worker-a", fencing_token=lease.fencing_token, error="transient")
            self.assertEqual(row.status, "retry")
            row.available_at = row.updated_at
        with self.database.session() as session:
            lease2 = queue.lease_next(session, worker_id="worker-b", lease_seconds=5)
            self.assertIsNotNone(lease2)
            assert lease2 is not None
            self.assertGreater(lease2.fencing_token, lease.fencing_token)
            row = queue.complete(session, job_id=lease2.id, worker_id="worker-b", fencing_token=lease2.fencing_token, result={"ok": True})
            self.assertEqual(row.status, "succeeded")

    def test_approval_separation_staleness_secret_and_budget(self) -> None:
        service = ApprovalService()
        requester = Identity("reviewer-a", "Reviewer A", "reviewer")
        other = Identity("reviewer-b", "Reviewer B", "reviewer")
        with self.database.session() as session:
            approval = service.request(
                session,
                project_id=self.project.id,
                gate_name="release-ready",
                reason="request release review",
                requester=requester,
                idempotency_key="gate-1",
            )
            approval_id = approval.id
        with self.database.session() as session:
            with self.assertRaises(PermissionError):
                service.decide(session, approval_id=approval_id, decision="approved", reason="self approval", approver=requester)
        with self.database.session() as session:
            row = service.decide(session, approval_id=approval_id, decision="approved", reason="independent review", approver=other)
            self.assertEqual(row.status, "approved")

        with self.database.session() as session:
            stale = service.request(
                session,
                project_id=self.project.id,
                gate_name="production-ready",
                reason="request production review",
                requester=requester,
                idempotency_key="gate-2",
            )
            stale_id = stale.id
        with self.database.session() as session:
            current = self.repo.get_project(session, self.project.id)
            self.repo.update_state(
                session,
                project_id=self.project.id,
                expected_revision=current.revision,
                actor="agent",
                event_type="artifact-changed",
                mutate=lambda state: state | {"change": True},
            )
        with self.database.session() as session:
            with self.assertRaises(RuntimeError):
                service.decide(session, approval_id=stale_id, decision="approved", reason="now stale", approver=other)

        old_key = os.environ.get("SDLC_MASTER_KEY_B64")
        os.environ["SDLC_MASTER_KEY_B64"] = generate_master_key()
        try:
            admin = Identity("admin", "Admin", "admin")
            service_identity = Identity("svc", "Service", "service")
            with self.database.session() as session:
                put_secret(session, project_id=self.project.id, name="API_KEY", value="secret-value", actor=admin)
            with self.database.session() as session:
                self.assertEqual(resolve_secret(session, project_id=self.project.id, name="API_KEY", actor=service_identity), "secret-value")
        finally:
            if old_key is None:
                os.environ.pop("SDLC_MASTER_KEY_B64", None)
            else:
                os.environ["SDLC_MASTER_KEY_B64"] = old_key

        budgets = BudgetService()
        with self.database.session() as session:
            budgets.upsert(session, project_id=self.project.id, soft_limit_usd=5, hard_limit_usd=10, token_limit=1000)
            normal = budgets.assess(session, project_id=self.project.id, estimated_cost_usd=2, estimated_tokens=100)
            degraded = budgets.assess(session, project_id=self.project.id, estimated_cost_usd=8, estimated_tokens=100)
            blocked = budgets.assess(session, project_id=self.project.id, estimated_cost_usd=11, estimated_tokens=100)
            self.assertEqual(normal.level, "normal")
            self.assertEqual(degraded.level, "degraded")
            self.assertFalse(blocked.allowed)
            budgets.record_run(session, project_id=self.project.id, actor="agent", os_name="engineering", skill="build", model="m", outcome="success", cost_usd=3, tokens_input=100, tokens_output=50, tool_calls=2, human_hours=0.5)
        with self.database.session() as session:
            watch = budgets.assess(session, project_id=self.project.id, estimated_cost_usd=3, estimated_tokens=100)
            self.assertEqual(watch.level, "degraded")

    def test_http_api_auth_optimistic_conflict_and_dashboard(self) -> None:
        old = os.environ.get("SDLC_BOOTSTRAP_TOKEN")
        os.environ["SDLC_BOOTSTRAP_TOKEN"] = "bootstrap-token"
        try:
            client = TestClient(create_app(self.database))
            self.assertEqual(client.get("/health").status_code, 200)
            self.assertIn("Pending gate approvals", client.get("/dashboard").text)
            self.assertEqual(client.get("/api/projects").status_code, 401)
            headers = {"Authorization": "Bearer bootstrap-token"}
            created = client.post("/api/projects", headers=headers, json={"name": "API Project", "project_id": "api-project"})
            self.assertEqual(created.status_code, 201, created.text)
            payload = created.json()
            state = payload["state"] | {"current_os": "design", "current_stage": "RESEARCH"}
            ok = client.put("/api/projects/api-project/state", headers=headers, json={"expected_revision": 0, "state": state})
            self.assertEqual(ok.status_code, 200, ok.text)
            conflict = client.put("/api/projects/api-project/state", headers=headers, json={"expected_revision": 0, "state": state})
            self.assertEqual(conflict.status_code, 409)
            self.assertTrue(client.get("/api/projects/api-project/audit", headers=headers).json()["valid"])
            principal = client.post("/api/principals", headers=headers, json={"display_name": "Reader", "role": "viewer"})
            self.assertEqual(principal.status_code, 201, principal.text)
            reader_headers = {"Authorization": f"Bearer {principal.json()['token']}"}
            self.assertEqual(client.get("/api/projects", headers=reader_headers).status_code, 200)
            self.assertEqual(client.post("/api/projects", headers=reader_headers, json={"name": "Denied"}).status_code, 403)
        finally:
            if old is None:
                os.environ.pop("SDLC_BOOTSTRAP_TOKEN", None)
            else:
                os.environ["SDLC_BOOTSTRAP_TOKEN"] = old


if __name__ == "__main__":
    unittest.main()
