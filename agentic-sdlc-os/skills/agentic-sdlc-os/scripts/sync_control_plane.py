#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "control_plane"))

from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.repository import ProjectRepository, RevisionConflict


def metadata_path(project: Path) -> Path:
    return project / ".sdlc" / "control-plane.json"


def load_metadata(project: Path) -> dict:
    path = metadata_path(project)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_metadata(project: Path, payload: dict) -> None:
    metadata_path(project).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def push(project: Path, database_url: str, actor: str) -> dict:
    state_path = project / ".sdlc" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    meta = load_metadata(project)
    database = create_database(database_url); init_database(database); repo = ProjectRepository()
    with database.session() as session:
        if not meta.get("project_id"):
            row = repo.create_project(
                session,
                name=state.get("project", {}).get("name", project.name),
                project_type=state.get("project", {}).get("type", "greenfield"),
                criticality=state.get("project", {}).get("criticality", "medium"),
                profile=state.get("project", {}).get("profile", "standard"),
                actor=actor,
                state=state,
            )
        else:
            row = repo.update_state(
                session,
                project_id=meta["project_id"],
                expected_revision=int(meta["control_plane_revision"]),
                actor=actor,
                event_type="local-kernel-synced",
                mutate=lambda _current: state,
                event_payload={"local_revision": state.get("revision")},
            )
    payload = {"project_id": row.id, "control_plane_revision": row.revision, "local_revision": state.get("revision"), "database_url": database.engine.url.render_as_string(hide_password=True)}
    write_metadata(project, payload)
    return payload


def pull(project: Path, database_url: str, actor: str, force: bool) -> dict:
    meta = load_metadata(project)
    if not meta.get("project_id"):
        raise RuntimeError("No control-plane project mapping; push first")
    database = create_database(database_url); init_database(database); repo = ProjectRepository()
    with database.session() as session:
        row = repo.get_project(session, meta["project_id"])
        state = row.state_json
    local_path = project / ".sdlc" / "state.json"
    if local_path.exists() and not force:
        local = json.loads(local_path.read_text(encoding="utf-8"))
        if int(local.get("revision", 0)) != int(meta.get("local_revision", 0)):
            raise RuntimeError("Local state changed since last sync; use --force only after review")
    local_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    payload = {"project_id": row.id, "control_plane_revision": row.revision, "local_revision": state.get("revision"), "pulled_by": actor}
    write_metadata(project, payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synchronize local .sdlc state with the production control plane")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["push", "pull"]:
        p = sub.add_parser(name); p.add_argument("project"); p.add_argument("--database-url", required=True); p.add_argument("--actor", required=True)
        if name == "pull": p.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    try:
        payload = push(Path(args.project).resolve(), args.database_url, args.actor) if args.command == "push" else pull(Path(args.project).resolve(), args.database_url, args.actor, args.force)
        print(json.dumps(payload, indent=2)); return 0
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError, RevisionConflict) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
