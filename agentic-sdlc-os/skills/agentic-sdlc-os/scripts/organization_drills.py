#!/usr/bin/env python3
"""Organization-level control drills for RBAC, secrets, backup/restore and audit export.

Local SQLite mode proves the control mechanics. It is intentionally not sufficient
for Production Candidate. Formal evidence additionally requires PostgreSQL, a
non-local KMS/secret provider, and successful external backup/restore commands.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import sqlite3
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidTag
from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "control_plane"))

from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.models import ProjectEvent
from agentic_sdlc_cp.repository import ProjectRepository
from agentic_sdlc_cp.security import (
    Identity, authenticate, create_principal, enforce_separation_of_duties,
    generate_master_key, put_secret, require_permission, resolve_secret, rotate_secrets,
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def expect_denied(fn) -> bool:
    try:
        fn()
    except PermissionError:
        return True
    return False


def run_command(command: str, *, env: dict[str, str] | None = None) -> dict[str, Any]:
    result = subprocess.run(["bash", "-lc", command], text=True, capture_output=True, env=env, check=False)
    return {
        "command_hash": hashlib.sha256(command.encode("utf-8")).hexdigest(),
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "passed": result.returncode == 0,
    }


def sqlite_backup(source: Path, target: Path) -> None:
    with sqlite3.connect(source) as src, sqlite3.connect(target) as dst:
        src.backup(dst)


def export_audit(database, project_id: str, path: Path) -> dict[str, Any]:
    repository = ProjectRepository()
    with database.session() as session:
        verification = repository.verify_audit_chain(session, project_id)
        rows = session.scalars(select(ProjectEvent).where(ProjectEvent.project_id == project_id).order_by(ProjectEvent.sequence)).all()
        payload = {
            "project_id": project_id,
            "verification": verification,
            "events": [
                {
                    "sequence": row.sequence,
                    "event_type": row.event_type,
                    "actor": row.actor,
                    "payload": row.payload_json,
                    "state_hash": row.state_hash,
                    "previous_hash": row.previous_hash,
                    "event_hash": row.event_hash,
                    "created_at": row.created_at.isoformat(),
                }
                for row in rows
            ],
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"passed": verification.get("valid") is True and bool(payload["events"]), "events": len(payload["events"]), "sha256": sha256(path), "path": str(path)}


def run_drills(
    database_url: str, *, output_dir: Path, kms_provider: str,
    formal_requested: bool, backup_command: str = "", restore_command: str = "", restore_verify_command: str = "",
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    database = create_database(database_url)
    init_database(database)
    repository = ProjectRepository()
    project_id = f"org-drill-{uuid.uuid4().hex[:12]}"

    identities: dict[str, Identity] = {}
    with database.session() as session:
        repository.create_project(session, name="organization-drill", actor="bootstrap", project_id=project_id, profile="high-assurance", state={"counter": 0})
        for role in ["viewer", "contributor", "reviewer", "releaser", "service", "admin"]:
            principal, token = create_principal(session, f"drill-{role}", role)
            identity = authenticate(session, token)
            if identity is None:
                raise RuntimeError(f"authentication failed for {role}")
            identities[role] = identity

    # RBAC and separation of duties.
    rbac_checks = {
        "viewer_cannot_write": expect_denied(lambda: require_permission(identities["viewer"], "project:write")),
        "contributor_cannot_approve": expect_denied(lambda: require_permission(identities["contributor"], "gate:approve")),
        "reviewer_cannot_write": expect_denied(lambda: require_permission(identities["reviewer"], "project:write")),
        "service_cannot_approve": expect_denied(lambda: require_permission(identities["service"], "gate:approve")),
        "admin_can_write": True,
        "reviewer_can_approve": True,
        "self_approval_blocked": expect_denied(lambda: enforce_separation_of_duties(requester_id=identities["reviewer"].principal_id, approver=identities["reviewer"], profile="high-assurance")),
    }
    try:
        require_permission(identities["admin"], "project:write")
        require_permission(identities["reviewer"], "gate:approve")
    except PermissionError:
        rbac_checks["admin_can_write"] = False; rbac_checks["reviewer_can_approve"] = False
    rbac_passed = all(rbac_checks.values())

    # Real cryptographic secret rotation: old key -> new key, same plaintext,
    # old key can no longer decrypt the rotated ciphertext.
    old_key = generate_master_key(); new_key = generate_master_key()
    original_env = os.environ.get("SDLC_MASTER_KEY_B64")
    secret_value = "rotation-canary-" + uuid.uuid4().hex
    try:
        os.environ["SDLC_MASTER_KEY_B64"] = old_key
        with database.session() as session:
            put_secret(session, project_id=project_id, name="drill-secret", value=secret_value, actor=identities["admin"], key_version="v1")
        with database.session() as session:
            before = resolve_secret(session, project_id=project_id, name="drill-secret", actor=identities["service"])
        with database.session() as session:
            rotation = rotate_secrets(session, old_key_b64=old_key, new_key_b64=new_key, new_version="v2", actor=identities["admin"], project_id=project_id)
        os.environ["SDLC_MASTER_KEY_B64"] = new_key
        with database.session() as session:
            after = resolve_secret(session, project_id=project_id, name="drill-secret", actor=identities["service"])
        old_key_rejected = False
        os.environ["SDLC_MASTER_KEY_B64"] = old_key
        try:
            with database.session() as session:
                resolve_secret(session, project_id=project_id, name="drill-secret", actor=identities["service"])
        except (InvalidTag, RuntimeError, ValueError):
            old_key_rejected = True
        secret_rotation_passed = before == secret_value and after == secret_value and old_key_rejected and int(rotation.get("rotated", 0)) == 1
    finally:
        if original_env is None:
            os.environ.pop("SDLC_MASTER_KEY_B64", None)
        else:
            os.environ["SDLC_MASTER_KEY_B64"] = original_env

    # Generate state changes so backup and audit export have meaningful content.
    with database.session() as session:
        repository.update_state(session, project_id=project_id, expected_revision=0, actor="drill", event_type="pre-backup", mutate=lambda s: s | {"counter": 1})
    audit_path = output_dir / "audit-export.json"
    audit = export_audit(database, project_id, audit_path)

    dialect = database.engine.dialect.name
    backup: dict[str, Any]
    if dialect == "sqlite":
        # SQLite local drill is a real backup/restore mechanics test, but not org-level formal evidence.
        raw_db = database.engine.url.database
        if not raw_db:
            backup = {"passed": False, "reason": "SQLite database path unavailable"}
        else:
            database.engine.dispose()
            source = Path(raw_db).resolve(); backup_path = output_dir / "control-plane-backup.db"; restored_path = output_dir / "control-plane-restored.db"
            sqlite_backup(source, backup_path)
            restored_path.write_bytes(backup_path.read_bytes())
            restored = create_database(f"sqlite+pysqlite:///{restored_path}")
            with restored.session() as session:
                row = repository.get_project(session, project_id)
                restored_audit = repository.verify_audit_chain(session, project_id)
            backup = {
                "passed": row.state_json.get("counter") == 1 and restored_audit.get("valid") is True,
                "backup_sha256": sha256(backup_path), "restored_audit": restored_audit,
                "mode": "sqlite-native-backup",
            }
            restored.engine.dispose()
    else:
        if not backup_command or not restore_command or not restore_verify_command:
            backup = {"passed": False, "reason": "formal PostgreSQL drill requires --backup-command, --restore-command and --restore-verify-command"}
        else:
            env = os.environ.copy(); env["SDLC_DATABASE_URL"] = database_url
            first = run_command(backup_command, env=env); second = run_command(restore_command, env=env) if first["passed"] else {"passed": False, "returncode": -1}; third = run_command(restore_verify_command, env=env) if second.get("passed") else {"passed": False, "returncode": -1}
            backup = {"passed": bool(first["passed"] and second.get("passed") and third.get("passed")), "mode": "external-postgresql", "backup": first, "restore": second, "verify": third}

    formal_eligible = bool(
        formal_requested and dialect == "postgresql" and kms_provider not in {"", "local", "environment"}
        and rbac_passed and secret_rotation_passed and backup.get("passed") and audit.get("passed")
    )
    result = {
        "schema_version": "2.5.0",
        "passed": bool(rbac_passed and secret_rotation_passed and backup.get("passed") and audit.get("passed")),
        "formal_requested": formal_requested,
        "formal_evidence_eligible": formal_eligible,
        "environment_scope": "organization" if formal_eligible else "local-control-plane",
        "database": dialect,
        "kms_provider": kms_provider,
        "rbac": rbac_passed,
        "secret_rotation": secret_rotation_passed,
        "backup_restore": bool(backup.get("passed")),
        "audit_export": bool(audit.get("passed")),
        "details": {"rbac": rbac_checks, "secret_rotation": {"rotated": rotation.get("rotated", 0), "old_key_rejected": old_key_rejected}, "backup_restore": backup, "audit_export": audit},
    }
    try:
        database.engine.dispose()
    except Exception:
        pass
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentic SDLC organization control drills")
    parser.add_argument("--database-url")
    parser.add_argument("--output", required=True)
    parser.add_argument("--kms-provider", default="local")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--backup-command", default="")
    parser.add_argument("--restore-command", default="")
    parser.add_argument("--restore-verify-command", default="")
    args = parser.parse_args(argv)
    temp = None
    try:
        if args.database_url:
            url = args.database_url
            out_dir = Path(args.output).resolve().parent / "organization-drill-artifacts"
        else:
            temp = tempfile.TemporaryDirectory(prefix="sdlc-org-drill-")
            db_path = Path(temp.name) / "control.db"
            url = f"sqlite+pysqlite:///{db_path}"
            out_dir = Path(args.output).resolve().parent / "organization-drill-artifacts"
        result = run_drills(url, output_dir=out_dir, kms_provider=args.kms_provider, formal_requested=args.formal, backup_command=args.backup_command, restore_command=args.restore_command, restore_verify_command=args.restore_verify_command)
        output = Path(args.output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 2
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2
    finally:
        if temp is not None:
            temp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
