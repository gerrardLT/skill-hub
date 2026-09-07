#!/usr/bin/env python3
"""Tamper-evident long-running production soak evidence.

Formal evidence is wall-clock based. Backdated timestamps are supported only for
synthetic harness tests and can never become formal maturity evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "2.5.0"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False); fh.write("\n"); temp = Path(fh.name)
    os.replace(temp, path)


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("soak file must contain an object")
    return payload


def new_state(*, system_version: str, target_days: int = 30, synthetic: bool = False, started_at: datetime | None = None) -> dict[str, Any]:
    if target_days < 1:
        raise RuntimeError("target_days must be positive")
    start = started_at or utcnow()
    return {
        "schema_version": VERSION,
        "soak_id": f"soak-{uuid.uuid4().hex}",
        "system_version": system_version,
        "synthetic": synthetic,
        "target_days": target_days,
        "started_at": iso(start),
        "created_at": iso(utcnow()),
        "observations": [],
        "incidents": [],
        "record_chain_head": "GENESIS",
        "sealed_at": None,
        "seal_hash": None,
    }


def _append(state: dict[str, Any], collection: str, record: dict[str, Any]) -> None:
    if state.get("sealed_at"):
        raise RuntimeError("soak is sealed")
    record["previous_hash"] = state.get("record_chain_head", "GENESIS")
    record["record_hash"] = digest({k: v for k, v in record.items() if k != "record_hash"})
    state[collection].append(record)
    state["record_chain_head"] = record["record_hash"]


def add_observation(
    state: dict[str, Any], *, at: datetime | None = None, health_pass: bool, audit_pass: bool,
    stress_pass: bool, availability: float, notes: str = "", source_hash: str = "",
) -> None:
    when = at or utcnow()
    if at is not None and not state.get("synthetic"):
        raise RuntimeError("explicit timestamps are permitted only for synthetic soak evidence")
    if not math.isfinite(float(availability)) or availability < 0 or availability > 1:
        raise RuntimeError("availability must be between 0 and 1")
    _append(state, "observations", {
        "kind": "observation", "recorded_at": iso(when), "utc_date": when.astimezone(timezone.utc).date().isoformat(),
        "health_pass": bool(health_pass), "audit_pass": bool(audit_pass), "stress_pass": bool(stress_pass),
        "availability": float(availability), "source_hash": source_hash, "notes": notes,
    })


def add_incident(state: dict[str, Any], *, severity: str, summary: str, control_plane: bool, at: datetime | None = None) -> None:
    when = at or utcnow()
    if at is not None and not state.get("synthetic"):
        raise RuntimeError("explicit timestamps are permitted only for synthetic soak evidence")
    severity = severity.upper()
    if severity not in {"P0", "P1", "P2", "P3"}:
        raise RuntimeError("severity must be P0, P1, P2 or P3")
    _append(state, "incidents", {
        "kind": "incident", "recorded_at": iso(when), "severity": severity,
        "summary": summary, "control_plane": bool(control_plane),
    })


def verify_chain(state: dict[str, Any]) -> list[str]:
    merged = [*state.get("observations", []), *state.get("incidents", [])]
    merged.sort(key=lambda x: (parse_time(str(x.get("recorded_at"))), str(x.get("record_hash", ""))))
    # Chain order is append order, which may differ from timestamp sort in synthetic tests.
    by_hash = {str(r.get("record_hash")): r for r in merged}
    errors: list[str] = []
    previous = "GENESIS"
    seen: set[str] = set()
    for _ in range(len(merged)):
        candidates = [r for r in merged if str(r.get("previous_hash")) == previous and str(r.get("record_hash")) not in seen]
        if len(candidates) != 1:
            errors.append(f"chain successor count for {previous[:12]} is {len(candidates)}")
            break
        record = candidates[0]
        claimed = str(record.get("record_hash", ""))
        calculated = digest({k: v for k, v in record.items() if k != "record_hash"})
        if claimed != calculated:
            errors.append(f"record hash mismatch: {claimed[:12]}")
        seen.add(claimed); previous = claimed
    if len(seen) != len(merged):
        errors.append("chain does not cover all records")
    if previous != state.get("record_chain_head", "GENESIS"):
        errors.append("record_chain_head mismatch")
    return list(dict.fromkeys(errors))


def _seal_payload(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": state.get("schema_version"), "soak_id": state.get("soak_id"),
        "system_version": state.get("system_version"), "synthetic": state.get("synthetic"),
        "target_days": state.get("target_days"), "started_at": state.get("started_at"),
        "record_chain_head": state.get("record_chain_head"), "sealed_at": state.get("sealed_at"),
    }


def assess_state(state: dict[str, Any]) -> dict[str, Any]:
    errors = verify_chain(state)
    observations = list(state.get("observations", []))
    incidents = list(state.get("incidents", []))
    target = int(state.get("target_days", 30))
    start = parse_time(str(state.get("started_at")))
    last_time = max([parse_time(str(x["recorded_at"])) for x in observations], default=start)
    elapsed = (last_time - start).total_seconds() / 86400.0
    dates = sorted({str(x.get("utc_date")) for x in observations})
    bad_health = sum(1 for x in observations if not x.get("health_pass"))
    bad_audit = sum(1 for x in observations if not x.get("audit_pass"))
    bad_stress = sum(1 for x in observations if not x.get("stress_pass"))
    p0 = sum(1 for x in incidents if x.get("severity") == "P0")
    p1_cp = sum(1 for x in incidents if x.get("severity") == "P1" and x.get("control_plane") is True)
    ordered_times = sorted(parse_time(str(x["recorded_at"])) for x in observations)
    max_gap_hours = max([(b-a).total_seconds()/3600 for a, b in zip(ordered_times, ordered_times[1:])], default=0.0)
    readiness: list[str] = []
    if len(dates) < target:
        readiness.append(f"observation days {len(dates)} < target {target}")
    if elapsed < target:
        readiness.append(f"wall-clock elapsed {elapsed:.3f} days < target {target}")
    if max_gap_hours > 36.0:
        readiness.append(f"observation gap {max_gap_hours:.2f}h > 36h")
    if bad_health:
        readiness.append(f"health failures: {bad_health}")
    if bad_audit:
        readiness.append(f"audit failures: {bad_audit}")
    if bad_stress:
        readiness.append(f"stress failures: {bad_stress}")
    if p0:
        readiness.append(f"P0 incidents: {p0}")
    if p1_cp:
        readiness.append(f"P1 control-plane incidents: {p1_cp}")
    if errors:
        readiness.extend(errors)
    seal_valid = False
    if state.get("sealed_at") and state.get("seal_hash"):
        seal_valid = state.get("seal_hash") == digest(_seal_payload(state))
        if not seal_valid:
            readiness.append("seal hash mismatch")
    formal_eligible = bool(
        not state.get("synthetic") and state.get("sealed_at") and seal_valid and not readiness
    )
    return {
        "schema_version": VERSION, "soak_id": state.get("soak_id"), "system_version": state.get("system_version"),
        "synthetic": bool(state.get("synthetic")), "target_days": target,
        "observation_days": len(dates), "elapsed_days": round(elapsed, 6), "max_gap_hours": round(max_gap_hours, 3),
        "observations": len(observations), "p0_incidents": p0, "p1_control_plane_incidents": p1_cp,
        "health_failures": bad_health, "audit_failures": bad_audit, "stress_failures": bad_stress,
        "chain_valid": not errors, "sealed": bool(state.get("sealed_at")), "seal_valid": seal_valid,
        "formal_evidence_eligible": formal_eligible, "failures": list(dict.fromkeys(readiness)),
    }


def seal(state: dict[str, Any]) -> None:
    if state.get("sealed_at"):
        raise RuntimeError("already sealed")
    assessment = assess_state(state)
    blocking = list(assessment["failures"])
    # A missing seal itself is not part of pre-seal readiness. assess_state only
    # validates a seal when one exists.
    if blocking:
        raise RuntimeError("cannot seal: " + "; ".join(blocking))
    state["sealed_at"] = iso(utcnow())
    state["seal_hash"] = digest(_seal_payload(state))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentic SDLC OS 30-day soak evidence runner")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start"); p.add_argument("file"); p.add_argument("--system-version", default="2.5.0"); p.add_argument("--target-days", type=int, default=30); p.add_argument("--synthetic", action="store_true"); p.add_argument("--at")
    p = sub.add_parser("record"); p.add_argument("file"); p.add_argument("--health-pass", action="store_true"); p.add_argument("--audit-pass", action="store_true"); p.add_argument("--stress-pass", action="store_true"); p.add_argument("--availability", type=float, default=1.0); p.add_argument("--source-hash", default=""); p.add_argument("--notes", default=""); p.add_argument("--at")
    p = sub.add_parser("incident"); p.add_argument("file"); p.add_argument("--severity", required=True); p.add_argument("--summary", required=True); p.add_argument("--control-plane", action="store_true"); p.add_argument("--at")
    p = sub.add_parser("assess"); p.add_argument("file"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("seal"); p.add_argument("file")
    args = parser.parse_args(argv)
    try:
        path = Path(args.file).resolve()
        if args.command == "start":
            at = parse_time(args.at) if args.at else None
            if at is not None and not args.synthetic:
                raise RuntimeError("--at requires --synthetic")
            state = new_state(system_version=args.system_version, target_days=args.target_days, synthetic=args.synthetic, started_at=at)
            atomic_write(path, state); print(path); return 0
        state = load(path)
        if args.command == "record":
            add_observation(state, at=parse_time(args.at) if args.at else None, health_pass=args.health_pass, audit_pass=args.audit_pass, stress_pass=args.stress_pass, availability=args.availability, source_hash=args.source_hash, notes=args.notes)
            atomic_write(path, state); return 0
        if args.command == "incident":
            add_incident(state, severity=args.severity, summary=args.summary, control_plane=args.control_plane, at=parse_time(args.at) if args.at else None)
            atomic_write(path, state); return 0
        if args.command == "seal":
            seal(state); atomic_write(path, state); print(state["seal_hash"]); return 0
        result = assess_state(state)
        print(json.dumps(result, indent=2) if args.json else ("PASS" if result["formal_evidence_eligible"] else "BLOCKED\n- " + "\n- ".join(result["failures"])))
        return 0 if result["formal_evidence_eligible"] else 2
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
