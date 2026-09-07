#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "control_plane"))

from sqlalchemy import delete
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

from agentic_sdlc_cp.costs import BudgetService
from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.jobs import JobQueue
from agentic_sdlc_cp.locks import LeaseLockManager
from agentic_sdlc_cp.models import Base, Budget, Job, OutboxEvent, Project, ProjectEvent, ProjectSnapshot, Run
from agentic_sdlc_cp.repository import ProjectRepository


def static_check() -> dict:
    dialect = postgresql.dialect()
    tables = []
    statements = []
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=dialect))
        if "CREATE TABLE" not in ddl:
            raise RuntimeError(f"Could not compile table: {table.name}")
        tables.append(table.name)
        statements.append(ddl)
        for index in table.indexes:
            statements.append(str(CreateIndex(index).compile(dialect=dialect)))
    migration = (ROOT / "control_plane" / "migrations" / "001_initial_postgresql.sql").read_text(encoding="utf-8")
    required = ["pgcrypto", "timezone", "statement_timeout", "idle_in_transaction_session_timeout"]
    missing = [item for item in required if item not in migration]
    return {
        "passed": not missing and len(tables) >= 12,
        "tables": tables,
        "table_count": len(tables),
        "ddl_statements": len(statements),
        "migration_missing": missing,
        "live": False,
    }


def live_check(url: str) -> dict:
    if not url.startswith("postgresql"):
        raise RuntimeError("Live URL must be PostgreSQL")
    database = create_database(url)
    init_database(database)
    repo = ProjectRepository(); queue = JobQueue(); budgets = BudgetService()
    suffix = uuid.uuid4().hex
    project_id = f"pg-conformance-{suffix}"
    lock_key = f"pg-lock-{suffix}"
    with database.session() as session:
        project = repo.create_project(session, name="PostgreSQL conformance", project_id=project_id, actor="conformance")
        budgets.upsert(session, project_id=project.id, soft_limit_usd=5, hard_limit_usd=10, token_limit=10000)
        job = queue.enqueue(session, project_id=project.id, job_type="conformance", payload={"ok": True}, idempotency_key=f"job-{suffix}")
    with database.session() as session:
        lease = queue.lease_next(session, worker_id="pg-worker", lease_seconds=30, job_types=["conformance"])
        if lease is None or lease.id != job.id:
            raise RuntimeError("PostgreSQL SKIP LOCKED job lease failed")
        queue.complete(session, job_id=lease.id, worker_id="pg-worker", fencing_token=lease.fencing_token, result={"ok": True})
    lock_manager = LeaseLockManager(database)
    token = lock_manager.acquire(lock_key, "pg-worker", ttl_seconds=10, wait_seconds=2)
    if not lock_manager.release(token):
        raise RuntimeError("PostgreSQL lease release failed")
    with database.session() as session:
        audit = repo.verify_audit_chain(session, project_id)
        if not audit["valid"]:
            raise RuntimeError("Audit chain invalid")
    with database.session() as session:
        session.execute(delete(Project).where(Project.id == project_id))
    result = static_check()
    result.update({"live": True, "database": database.engine.dialect.name, "audit": audit, "job": "passed", "lease": "passed"})
    database.engine.dispose()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static and optional live PostgreSQL conformance")
    parser.add_argument("--database-url", default=os.environ.get("SDLC_POSTGRES_TEST_URL"))
    parser.add_argument("--require-live", action="store_true")
    args = parser.parse_args(argv)
    try:
        payload = live_check(args.database_url) if args.database_url else static_check()
        if args.require_live and not payload.get("live"):
            payload["passed"] = False
            payload["reason"] = "SDLC_POSTGRES_TEST_URL is not configured"
        print(json.dumps(payload, indent=2))
        return 0 if payload.get("passed") else 2
    except Exception as exc:
        print(json.dumps({"passed": False, "live": bool(args.database_url), "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
