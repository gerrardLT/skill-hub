#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "domain-packs"


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def load_pack(pack_id: str) -> dict[str, Any]:
    path = PACK_ROOT / pack_id / "pack.json"
    if not path.exists():
        raise RuntimeError(f"Unknown domain pack: {pack_id}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_pack(payload)
    return payload


def validate_pack(pack: dict[str, Any]) -> None:
    required = ["id", "name", "version", "keywords", "risk_adjustment", "required_controls", "required_artifacts", "required_evidence", "gate_overlays"]
    missing = [name for name in required if name not in pack]
    if missing:
        raise RuntimeError("Invalid domain pack, missing: " + ", ".join(missing))
    if not isinstance(pack["gate_overlays"], dict):
        raise RuntimeError("gate_overlays must be an object")
    for name in ["required_controls", "required_artifacts", "required_evidence", "keywords"]:
        if not isinstance(pack[name], list) or not all(isinstance(item, str) and item for item in pack[name]):
            raise RuntimeError(f"{name} must be a non-empty string array")


def recommend(text: str) -> list[dict[str, Any]]:
    lowered = text.lower()
    results = []
    for path in sorted(PACK_ROOT.glob("*/pack.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        hits = [keyword for keyword in pack["keywords"] if keyword.lower() in lowered]
        if hits:
            results.append({"pack": pack["id"], "score": len(hits), "hits": hits})
    return sorted(results, key=lambda item: (-item["score"], item["pack"]))


def apply(project: Path, pack_id: str) -> dict[str, Any]:
    base = project.resolve() / ".sdlc"
    if not (base / "state.json").exists():
        raise RuntimeError("Project is not initialized; run sdlc.py init first")
    pack = load_pack(pack_id)
    destination = base / "domain-packs" / pack_id
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(PACK_ROOT / pack_id, destination)
    config_path = base / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    packs = list(dict.fromkeys([*config.get("domain_packs", []), pack_id]))
    controls = list(dict.fromkeys([*config.get("domain_required_controls", []), *pack["required_controls"]]))
    artifacts = list(dict.fromkeys([*config.get("domain_required_artifacts", []), *pack["required_artifacts"]]))
    evidence = list(dict.fromkeys([*config.get("domain_required_evidence", []), *pack["required_evidence"]]))
    overlays = dict(config.get("domain_gate_overlays", {}))
    for gate, values in pack["gate_overlays"].items():
        overlays[gate] = list(dict.fromkeys([*overlays.get(gate, []), *values]))
    config.update({
        "domain_packs": packs,
        "domain_required_controls": controls,
        "domain_required_artifacts": artifacts,
        "domain_required_evidence": evidence,
        "domain_gate_overlays": overlays,
        "domain_risk_adjustment": round(sum(load_pack(item)["risk_adjustment"] for item in packs), 2),
        "domain_budget_multiplier": round(max(load_pack(item).get("budget_multiplier", 1.0) for item in packs), 2),
    })
    atomic_json(config_path, config)
    checklist = base / "domain-checklist.md"
    sections = ["# Active domain controls", "", "## Packs", ""]
    sections.extend(f"- `{item}`" for item in packs)
    sections.extend(["", "## Required controls", ""])
    sections.extend(f"- [ ] `{item}`" for item in controls)
    sections.extend(["", "## Required artifacts", ""])
    sections.extend(f"- [ ] `{item}`" for item in artifacts)
    sections.extend(["", "## Required evidence", ""])
    sections.extend(f"- [ ] `{item}`" for item in evidence)
    checklist.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return {
        "project": str(project.resolve()),
        "active_packs": packs,
        "risk_adjustment": config["domain_risk_adjustment"],
        "budget_multiplier": config["domain_budget_multiplier"],
        "required_controls": len(controls),
        "required_artifacts": len(artifacts),
        "required_evidence": len(evidence),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agentic SDLC OS domain extension packs")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p = sub.add_parser("recommend")
    p.add_argument("text")
    p = sub.add_parser("validate")
    p.add_argument("--pack", required=True)
    p = sub.add_parser("apply")
    p.add_argument("project")
    p.add_argument("--pack", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            payload = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(PACK_ROOT.glob("*/pack.json"))]
        elif args.command == "recommend":
            payload = recommend(args.text)
        elif args.command == "validate":
            payload = load_pack(args.pack)
        else:
            payload = apply(Path(args.project), args.pack)
        print(json.dumps(payload, indent=2))
        return 0
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
