from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import uvicorn

from .api import create_app
from .db import create_database, init_database
from .recovery import RecoveryService
from .security import create_principal, generate_master_key
from .worker import Worker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic SDLC OS production control plane")
    parser.add_argument("--database-url", default=os.environ.get("SDLC_DATABASE_URL"))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db")

    p = sub.add_parser("create-principal")
    p.add_argument("--name", required=True)
    p.add_argument("--role", required=True)

    p = sub.add_parser("serve")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)

    p = sub.add_parser("worker-once")
    p.add_argument("--worker-id", required=True)

    sub.add_parser("recover")
    sub.add_parser("generate-master-key")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "generate-master-key":
        print(generate_master_key())
        return 0
    database = create_database(args.database_url)
    init_database(database)
    if args.command == "init-db":
        print(database.engine.url.render_as_string(hide_password=True))
        return 0
    if args.command == "create-principal":
        with database.session() as session:
            principal, token = create_principal(session, args.name, args.role)
            print(json.dumps({"id": principal.id, "role": principal.role, "token": token}, indent=2))
        return 0
    if args.command == "serve":
        uvicorn.run(create_app(database), host=args.host, port=args.port)
        return 0
    if args.command == "worker-once":
        worker = Worker(database, args.worker_id, {"echo": lambda payload: payload})
        print("processed" if worker.run_once() else "idle")
        return 0
    if args.command == "recover":
        print(json.dumps(RecoveryService(database).payload(), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
