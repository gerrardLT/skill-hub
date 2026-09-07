#!/usr/bin/env python3
"""Agentic SDLC OS project-state CLI.

The CLI is dependency-free and treats .sdlc/state.json as the source of truth.
Markdown ledgers are generated for human review and version control.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

VERSION = "2.5.0"
OS_SEQUENCE = ["pm", "design", "engineering", "qa", "release", "evolution"]
QUALITY_ORDER = {"low": 0, "medium": 1, "high": 2}
EVIDENCE_SOURCE_TYPES = {
    "primary", "official", "user-research", "telemetry", "experiment", "test",
    "audit", "code", "incident", "secondary", "opinion", "other",
}
HIGH_QUALITY_SOURCE_TYPES = {
    "primary", "official", "user-research", "telemetry", "experiment", "test",
    "audit", "code", "incident",
}
OPEN_RISK_STATUSES = {"open", "investigating", "unmitigated"}
ARTIFACT_STATUSES = {"draft", "review", "accepted", "rejected", "superseded"}
RISK_SEVERITIES = {"low", "medium", "high", "critical"}
PROJECT_TYPES = {"greenfield", "brownfield", "incident", "migration"}
CRITICALITIES = {"low", "medium", "high"}
PROCESS_PROFILES = {"lite", "standard", "high-assurance"}
TRACE_RELATIONS = {
    "derives", "supports", "satisfies", "implements", "verifies", "deploys",
    "measures", "informs", "mitigates", "depends-on", "supersedes", "contradicts",
}
TRACE_FORWARD_RELATIONS = {
    "derives", "supports", "satisfies", "implements", "verifies", "deploys",
    "measures", "informs", "mitigates", "depends-on",
}
TRACE_NODE_PREFIXES = {
    "problem", "goal", "requirement", "design", "adr", "code", "test",
    "release", "metric", "learning", "external",
}
MUTATING_COMMANDS = {
    "init", "migrate", "route", "transition", "add-artifact", "new-artifact", "add-evidence",
    "add-assumption", "add-decision", "add-risk", "update-risk", "trace", "gate", "learn", "summary",
    "record-run", "reconcile", "work-start", "work-end",
}
NON_HUMAN_APPROVER_TOKENS = {
    "ai", "agent", "assistant", "bot", "automation", "system", "chatgpt", "claude",
    "copilot", "gemini", "cursor", "codex", "opencode",
}
PLACEHOLDER_MARKERS = {
    "state what this artifact is intended to decide or enable",
    "record verifiable facts with sources",
    "record interpretations derived from the evidence",
    "record unverified claims and how they will be tested",
    "provide the domain-specific content",
    "record failure modes, constraints and unresolved risks",
    "define observable conditions for acceptance",
    "link upstream intent and downstream implementation",
}

LEDGER_CONFIG = {
    "artifacts": ("Artifacts", ["ID", "Type", "Status", "Stale", "Quality", "Owner", "Path", "SHA-256", "Updated"]),
    "evidence": ("Evidence", ["ID", "Claim", "Source", "Source Type", "Quality", "Supports", "Observed", "Expires"]),
    "assumptions": ("Assumptions", ["ID", "Assumption", "Risk", "Status", "Owner", "Updated"]),
    "decisions": ("Decisions", ["ID", "Title", "Choice", "Rationale", "Owner", "Decided"]),
    "risks": ("Risks", ["ID", "Risk", "Severity", "Likelihood", "Status", "Mitigation", "Owner"]),
    "traceability": ("Traceability", ["ID", "From", "Relation", "To", "Evidence", "Added"]),
    "learning": ("Learning Log", ["ID", "Expected", "Actual", "Gap", "Decision", "Route", "Added"]),
    "routing": ("Routing Log", ["ID", "Task", "Recommended OS", "Reason", "Added"]),
    "runs": ("Agent Runs", ["ID", "Actor", "OS", "Skill", "Model", "Outcome", "Tokens", "Tools", "Cost USD", "Human h", "Duration ms", "Added"]),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def uid(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def script_root() -> Path:
    return Path(__file__).resolve().parent


def find_manifest(name: str) -> Path:
    candidates = [
        script_root().parent / "manifest" / name,
        script_root().parent / "references" / "manifests" / name,
        script_root().parents[3] / "manifest" / name if len(script_root().parents) >= 4 else Path("/__missing__"),
        Path.cwd() / "manifest" / name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Cannot locate manifest: {name}")


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected JSON object in {path}")
    return data


def atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def state_content_hash(state: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(state).encode("utf-8")).hexdigest()


def audit_log_path(root: Path) -> Path:
    return root / ".sdlc" / "audit" / "events.jsonl"


def read_audit_events(root: Path) -> List[Dict[str, Any]]:
    path = audit_log_path(root)
    if not path.exists():
        return []
    events: List[Dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid audit event at line {line_number}: {exc}") from exc
        if not isinstance(event, dict):
            raise RuntimeError(f"Invalid audit event at line {line_number}: expected object")
        events.append(event)
    return events


def append_audit_event(root: Path, state: Dict[str, Any], event_name: str = "") -> None:
    if not bool(load_config(root).get("audit_chain", True)):
        return
    events = read_audit_events(root)
    previous_hash = str(events[-1].get("event_hash", "")) if events else "GENESIS"
    payload: Dict[str, Any] = {
        "sequence": len(events) + 1,
        "timestamp": now(),
        "event": event_name or str((state.get("history") or [{}])[-1].get("event", "state-updated")),
        "actor": os.environ.get("SDLC_ACTOR", "local-cli"),
        "revision": int(state.get("revision", 0)),
        "current_os": state.get("current_os"),
        "current_stage": state.get("current_stage"),
        "state_hash": state_content_hash(state),
        "previous_hash": previous_hash,
    }
    payload["event_hash"] = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    path = audit_log_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(canonical_json(payload) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def validate_audit_chain(root: Path, state: Dict[str, Any]) -> List[str]:
    if not bool(load_config(root).get("audit_chain", True)):
        return []
    errors: List[str] = []
    try:
        events = read_audit_events(root)
    except RuntimeError as exc:
        return [str(exc)]
    if not events:
        return ["Missing audit hash chain: .sdlc/audit/events.jsonl"]
    previous_hash = "GENESIS"
    for expected_sequence, event in enumerate(events, 1):
        if event.get("sequence") != expected_sequence:
            errors.append(f"Audit sequence gap: expected {expected_sequence}, got {event.get('sequence')}")
        if event.get("previous_hash") != previous_hash:
            errors.append(f"Audit previous_hash mismatch at sequence {expected_sequence}")
        claimed = str(event.get("event_hash", ""))
        payload = dict(event)
        payload.pop("event_hash", None)
        calculated = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
        if claimed != calculated:
            errors.append(f"Audit event hash mismatch at sequence {expected_sequence}")
        previous_hash = claimed
    if str(events[-1].get("state_hash", "")) != state_content_hash(state):
        errors.append("Current state does not match the latest audited state hash")
    return errors


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def project_root(value: str) -> Path:
    return Path(value).expanduser().resolve()


def is_uri(value: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*://", value, re.IGNORECASE))


def parse_time(value: str) -> Optional[datetime]:
    value = str(value or "").strip()
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def load_config(root: Path) -> Dict[str, Any]:
    defaults: Dict[str, Any] = {
        "schema_version": VERSION,
        "gate_policy": "strict",
        "allow_waiver": True,
        "max_waiver_days": 14,
        "allow_force_transition": True,
        "force_requires_human_approval": True,
        "artifact_status_required_for_gates": "accepted",
        "gate_artifact_min_bytes": 64,
        "gate_require_integrity": True,
        "stage_policy": "adjacent",
        "evidence_deduplicate": True,
        "process_profile": "standard",
        "audit_chain": True,
        "artifact_contract_enforcement": True,
        "independent_verification": "risk-based",
        "cost_budget_usd": None,
        "token_budget": None,
        "budget_hard_enforcement": False,
        "domain_packs": [],
        "domain_required_controls": [],
        "domain_required_artifacts": [],
        "domain_required_evidence": [],
        "domain_gate_overlays": {},
        "domain_risk_adjustment": 0.0,
        "domain_budget_multiplier": 1.0,
    }
    path = root / ".sdlc" / "config.json"
    if not path.exists():
        return defaults
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid .sdlc/config.json: {exc}") from exc
    if not isinstance(raw, dict):
        raise RuntimeError("Invalid .sdlc/config.json: expected object")
    return {**defaults, **raw}


def process_profile(state: Optional[Dict[str, Any]] = None, root: Optional[Path] = None) -> str:
    configured = str(load_config(root).get("process_profile", "")).strip() if root is not None else ""
    project_value = str((state or {}).get("project", {}).get("profile", "")).strip()
    profile = configured or project_value or "standard"
    if profile not in PROCESS_PROFILES:
        raise RuntimeError(f"Invalid process profile: {profile}")
    if str((state or {}).get("project", {}).get("criticality", "medium")) == "high" and profile == "lite":
        raise RuntimeError("High-criticality projects cannot use the lite process profile")
    return profile


WORK_FACTOR_NAMES = [
    "blast_radius", "data_sensitivity", "regulatory_exposure", "irreversibility",
    "technical_novelty", "problem_uncertainty", "user_exposure", "change_size",
    "operational_complexity",
]
DEFAULT_WORK_FACTORS = {
    "blast_radius": 1, "data_sensitivity": 0, "regulatory_exposure": 0, "irreversibility": 1,
    "technical_novelty": 0, "problem_uncertainty": 1, "user_exposure": 1, "change_size": 1,
    "operational_complexity": 1,
}
PROFILE_ORDER = {"lite": 0, "standard": 1, "high-assurance": 2}
PROFILE_CRITICALITY = {"lite": "low", "standard": "medium", "high-assurance": "high"}
WORK_PROTECTED_PATTERNS = (
    ".github/workflows/", "deploy/", "infra/", "terraform/", "auth", "permission", "security",
    "database", "schema", "dockerfile", "docker-compose",
)
WORK_HIGH_ASSURANCE_PATTERNS = (
    "migration", "migrations/", "secret", "credential", "payment", "billing", "ledger",
)


def active_work_item(state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    work_id = str(state.get("active_work_id", "") or "")
    if not work_id:
        return None
    item = state.get("work_items", {}).get(work_id)
    return item if isinstance(item, dict) and item.get("status") == "active" else None


def record_matches_active_work(state: Dict[str, Any], item: Dict[str, Any]) -> bool:
    work = active_work_item(state)
    if work is None:
        return True
    return str(item.get("work_item_id", "")) == str(work.get("id", ""))


def active_work_id(state: Dict[str, Any]) -> str:
    work = active_work_item(state)
    return str(work.get("id", "")) if work else ""


def work_scope_fields(state: Dict[str, Any]) -> Dict[str, str]:
    work_id = active_work_id(state)
    return {"scope": "work" if work_id else "project", "work_item_id": work_id}


def governance_for_record(state: Dict[str, Any], root: Path, item: Dict[str, Any]) -> Dict[str, str]:
    work_id = str(item.get("work_item_id", ""))
    work = state.get("work_items", {}).get(work_id) if work_id else None
    if isinstance(work, dict):
        profile = str(work.get("profile", process_profile(state, root)))
        return {"profile": profile, "criticality": str(work.get("criticality", PROFILE_CRITICALITY.get(profile, "medium")))}
    return {
        "profile": process_profile(state, root),
        "criticality": str(state.get("project", {}).get("criticality", "medium")),
    }


def _domain_pack_path(pack_id: str) -> Optional[Path]:
    candidates = [
        script_root().parent / "domain-packs" / pack_id / "pack.json",
        script_root().parents[3] / "domain-packs" / pack_id / "pack.json" if len(script_root().parents) >= 4 else Path("/__missing__"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def effective_governance(state: Dict[str, Any], root: Path) -> Dict[str, Any]:
    project_profile = process_profile(state, root)
    project_criticality = str(state.get("project", {}).get("criticality", "medium"))
    work = active_work_item(state)
    if work is None:
        return {
            "profile": project_profile, "criticality": project_criticality, "work_item_id": "",
            "bounded": False, "domain_impacts": list(load_config(root).get("domain_packs", [])),
        }
    profile = str(work.get("profile", project_profile))
    if not bool(work.get("bounded")) and PROFILE_ORDER.get(profile, 1) < PROFILE_ORDER.get(project_profile, 1):
        profile = project_profile
    criticality = PROFILE_CRITICALITY.get(profile, project_criticality)
    return {
        "profile": profile, "criticality": criticality, "work_item_id": str(work.get("id", "")),
        "bounded": bool(work.get("bounded")), "domain_impacts": list(work.get("domain_impacts", [])),
    }


def work_domain_gate_overlays(state: Dict[str, Any], root: Path, gate_name: str) -> List[str]:
    work = active_work_item(state)
    if work is None:
        config = load_config(root)
        overlays = config.get("domain_gate_overlays", {}) if isinstance(config.get("domain_gate_overlays", {}), dict) else {}
        return [str(x) for x in overlays.get(gate_name, [])]
    required: List[str] = []
    for pack_id in work.get("domain_impacts", []):
        pack_path = _domain_pack_path(str(pack_id))
        if not pack_path:
            continue
        pack = load_json(pack_path)
        overlays = pack.get("gate_overlays", {}) if isinstance(pack.get("gate_overlays", {}), dict) else {}
        required.extend(str(x) for x in overlays.get(gate_name, []))
    return list(dict.fromkeys(required))


def work_domain_required_evidence(state: Dict[str, Any], root: Path) -> List[str]:
    work = active_work_item(state)
    if work is None:
        return [str(x) for x in load_config(root).get("domain_required_evidence", [])]
    required: List[str] = []
    for pack_id in work.get("domain_impacts", []):
        pack_path = _domain_pack_path(str(pack_id))
        if pack_path:
            required.extend(str(x) for x in load_json(pack_path).get("required_evidence", []))
    return list(dict.fromkeys(required))


def _work_tailoring(factors: Dict[str, int], domain_risk: float = 0.0) -> Dict[str, Any]:
    spec = load_json(find_manifest("process-tailoring.json"))
    normalized: Dict[str, int] = {}
    for name in WORK_FACTOR_NAMES:
        value = int(factors.get(name, DEFAULT_WORK_FACTORS[name]))
        if value < 0 or value > 5:
            raise RuntimeError(f"{name} must be between 0 and 5")
        normalized[name] = value
    score = sum(normalized[name] * float(spec["factors"][name]["weight"]) for name in WORK_FACTOR_NAMES) + float(domain_risk)
    thresholds = spec["thresholds"]
    profile = "lite" if score <= float(thresholds["lite_max"]) else "standard" if score <= float(thresholds["standard_max"]) else "high-assurance"
    escalations: List[str] = []
    for rule in spec.get("hard_escalations", []):
        factor = str(rule["factor"])
        if normalized[factor] >= int(rule["minimum"]):
            target = str(rule["profile"])
            escalations.append(f"{factor}>={rule['minimum']}")
            if PROFILE_ORDER[target] > PROFILE_ORDER[profile]:
                profile = target
    return {"profile": profile, "risk_score": round(score, 2), "hard_escalations": escalations, "factors": normalized}


def blocking_critical_risks(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    work = active_work_item(state)
    if work is None:
        return open_critical_risks(state)
    work_id = str(work.get("id", ""))
    result = []
    for risk in state.get("risks", []):
        if not isinstance(risk, dict) or risk.get("severity") != "critical" or risk.get("status") not in OPEN_RISK_STATUSES:
            continue
        risk_work = str(risk.get("work_item_id", ""))
        if not risk_work or risk_work == work_id:
            result.append(risk)
    return result


def resolve_gate_spec(base: Dict[str, Any], profile: str, criticality: str) -> Dict[str, Any]:
    spec = deepcopy(base)
    override = deepcopy(spec.get("profiles", {}).get(profile, {}))
    for key, value in override.items():
        spec[key] = value
    required = list(spec.get("required", []))
    if criticality == "high":
        for item in base.get("required_high_criticality", []):
            if item not in required:
                required.append(item)
    spec["required"] = required
    spec["effective_profile"] = profile
    spec["effective_criticality"] = criticality
    return spec


@contextmanager
def project_lock(root: Path, timeout_seconds: float = 10.0):
    """Prevent concurrent agents from silently overwriting project state."""
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".sdlc.lock"
    deadline = time.monotonic() + timeout_seconds
    fd: Optional[int] = None
    while fd is None:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.write(fd, f"pid={os.getpid()} created={now()}\n".encode("utf-8"))
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > 300:
                    lock_path.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            if time.monotonic() >= deadline:
                raise RuntimeError(f"Project is locked by another process: {lock_path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock_path.unlink(missing_ok=True)


def _hash_file(path: Path, digest: "hashlib._Hash") -> int:
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
    return size


def path_fingerprint(path: Path) -> Tuple[str, int, int]:
    """Return deterministic content hash, total bytes and file count."""
    digest = hashlib.sha256()
    if path.is_file():
        total = _hash_file(path, digest)
        return digest.hexdigest(), total, 1
    if not path.is_dir():
        raise RuntimeError(f"Artifact path is not a regular file or directory: {path}")
    excluded = {".git", ".sdlc", "__pycache__", "node_modules", ".venv", "venv"}
    total = 0
    count = 0
    for child in sorted(path.rglob("*")):
        if not child.is_file() or any(part in excluded for part in child.relative_to(path).parts):
            continue
        rel = child.relative_to(path).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        total += _hash_file(child, digest)
        count += 1
    return digest.hexdigest(), total, count
def artifact_path(root: Path, item: Dict[str, Any]) -> Optional[Path]:
    value = str(item.get("path", "")).strip()
    if not value or is_uri(value):
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else (root / path).resolve()


def load_artifact_contracts() -> Dict[str, Any]:
    return load_json(find_manifest("artifact-contracts.json"))


def artifact_contract(artifact_type: str) -> Dict[str, Any]:
    contracts = load_artifact_contracts()
    contract = deepcopy(contracts.get("default", {}))
    if artifact_type in set(str(x) for x in contracts.get("report_types", [])):
        contract.update(deepcopy(contracts.get("report_contract", {})))
    contract.update(deepcopy(contracts.get("type_overrides", {}).get(artifact_type, {})))
    return contract


def quality_threshold(profile: str, criticality: str) -> float:
    contracts = load_artifact_contracts()
    threshold = float(contracts.get("profile_thresholds", {}).get(profile, 0.75))
    if criticality == "high":
        threshold = max(threshold, float(contracts.get("high_criticality_floor", 0.85)))
    return threshold


def normalize_heading(value: str) -> str:
    value = re.sub(r"[`*_]", "", str(value)).strip().lower()
    return re.sub(r"\s+", " ", value)


def markdown_sections(text: str) -> List[Tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*$", text))
    if not matches:
        return [("body", text)]
    sections: List[Tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((normalize_heading(match.group(1)), text[start:end].strip()))
    return sections


def substantive_chars(text: str) -> int:
    stripped = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", text)
    stripped = re.sub(r"[`*_>|\-\[\](){}]", "", stripped)
    stripped = re.sub(r"\s+", "", stripped)
    return len(stripped)


def heading_group_matches(headings: Iterable[str], group: Iterable[str]) -> bool:
    normalized = [normalize_heading(x) for x in headings]
    for candidate in group:
        needle = normalize_heading(str(candidate))
        if any(needle in heading or heading in needle for heading in normalized if heading):
            return True
    return False


def concrete_signal_coverage(text: str) -> Tuple[float, Dict[str, bool]]:
    lowered = text.lower()
    signals = {
        "evidence_anchor": bool(re.search(
            r"https?://|\b(?:source|evidence|facts?|verified|interview|telemetry|log|experiment|test result|citation|reference)\b|"
            r"(?:来源|证据|访谈|埋点|日志|实验|测试结果|引用)",
            lowered,
        )),
        "decision_commitment": bool(re.search(
            r"\b(?:must|shall|will|reject|accept|choose|exclude|commit|decision)\b|(?:必须|应当|将会|采用|拒绝|不包含|决定)",
            lowered,
        )),
        "measurable_condition": bool(re.search(
            r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|min|hours?|days?|users?|requests?|mb|gb)?\b|"
            r"\b(?:threshold|metric|pass|fail|within|at least|no more than)\b|(?:阈值|指标|通过|失败|至少|不超过|以内)",
            lowered,
        )),
        "ownership_or_identity": bool(re.search(
            r"\b(?:owners?|responsible|ticket|requirement|commit|version|id[:\s-])\b|(?:负责人|责任人|需求编号|版本|工单)",
            lowered,
        )),
    }
    return sum(1 for value in signals.values() if value) / len(signals), signals


def section_repetition_ratio(sections: Sequence[Tuple[str, str]]) -> float:
    bodies = [
        re.sub(r"\s+", " ", body.strip().lower())
        for _, body in sections
        if substantive_chars(body) >= 20
    ]
    if len(bodies) < 2:
        return 0.0
    unique = len(set(bodies))
    return round(1.0 - unique / len(bodies), 4)


def artifact_content_quality(
    path: Path,
    artifact_type: str,
    profile: str,
    criticality: str,
    minimum_bytes: int,
) -> Dict[str, Any]:
    contracts = load_artifact_contracts()
    result: Dict[str, Any] = {
        "contract": artifact_type if artifact_type in contracts.get("type_overrides", {}) else "default",
        "quality_score": 1.0,
        "quality_threshold": quality_threshold(profile, criticality),
        "issues": [],
        "metrics": {},
    }
    if path.is_dir():
        result["contract"] = "directory-integrity"
        return result
    if path.suffix.lower() not in set(str(x) for x in contracts.get("text_extensions", [])):
        result["contract"] = "binary-integrity"
        return result
    try:
        if path.stat().st_size > 2 * 1024 * 1024:
            result["contract"] = "large-text-integrity"
            return result
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        result["contract"] = "binary-integrity"
        return result

    markers = sorted(marker for marker in PLACEHOLDER_MARKERS if marker in text.lower())
    contract = artifact_contract(artifact_type)
    minimum_chars = max(int(contract.get("minimum_substantive_chars", minimum_bytes)), minimum_bytes)
    minimum_sections = int(contract.get("minimum_nonempty_sections", 1))
    minimum_group_coverage = float(contract.get("minimum_group_coverage", 0.0))
    profile_signal_threshold = float(
        contracts.get("profile_signal_thresholds", {}).get(profile, 0.5)
    )
    minimum_signal_coverage = max(
        float(contract.get("minimum_concrete_signal_coverage", 0.5)),
        profile_signal_threshold,
    )
    groups = list(contract.get("required_section_groups", []))
    sections = markdown_sections(text)
    headings = [name for name, _ in sections]
    nonempty_sections = sum(1 for _, body in sections if substantive_chars(body) >= 20)
    chars = substantive_chars(text)
    matched_indexes = {
        index for index, group in enumerate(groups)
        if heading_group_matches(headings, group)
    }
    group_coverage = len(matched_indexes) / len(groups) if groups else 1.0
    body_text = "\n".join(body for _, body in sections)
    signal_coverage, signals = concrete_signal_coverage(body_text)
    repetition_ratio = section_repetition_ratio(sections)
    vague_markers = [
        marker for marker in [
            "tbd", "to be determined", "details to follow", "as appropriate", "as needed",
            "relevant stakeholders", "best practices", "should be good", "待定", "后续补充",
            "视情况", "相关人员", "酌情处理",
        ] if marker in text.lower()
    ]
    length_score = min(1.0, chars / max(1, minimum_chars))
    section_score = min(1.0, nonempty_sections / max(1, minimum_sections))
    nonrepetition_score = max(0.0, 1.0 - repetition_ratio)
    score = (
        0.20 * length_score
        + 0.20 * section_score
        + 0.35 * group_coverage
        + 0.15 * signal_coverage
        + 0.10 * nonrepetition_score
    )
    if markers:
        score = max(0.0, score - 0.35)
    score = round(score, 4)
    threshold = quality_threshold(profile, criticality)
    issues: List[str] = []
    if markers:
        issues.append("contains_template_placeholders")
    if chars < minimum_chars:
        issues.append("insufficient_substantive_content")
    if nonempty_sections < minimum_sections:
        issues.append("insufficient_nonempty_sections")
    if group_coverage + 1e-9 < minimum_group_coverage:
        missing = [
            "/".join(str(x) for x in group)
            for index, group in enumerate(groups)
            if index not in matched_indexes
        ]
        issues.append("missing_required_sections:" + ";".join(missing))
    if signal_coverage + 1e-9 < minimum_signal_coverage:
        issues.append("insufficient_concrete_signals")
    if repetition_ratio > 0.5:
        issues.append("repetitive_section_content")
    if len(vague_markers) >= 3:
        issues.append("excessive_vague_language")
    if score + 1e-9 < threshold:
        issues.append("quality_score_below_threshold")
    result.update({
        "quality_score": score,
        "quality_threshold": threshold,
        "issues": issues,
        "metrics": {
            "substantive_chars": chars,
            "minimum_substantive_chars": minimum_chars,
            "nonempty_sections": nonempty_sections,
            "minimum_nonempty_sections": minimum_sections,
            "required_group_coverage": round(group_coverage, 4),
            "minimum_group_coverage": minimum_group_coverage,
            "concrete_signal_coverage": round(signal_coverage, 4),
            "minimum_concrete_signal_coverage": minimum_signal_coverage,
            "concrete_signals": signals,
            "section_repetition_ratio": repetition_ratio,
            "vague_markers": vague_markers,
            "headings": headings,
        },
    })
    return result


def verification_required(config: Dict[str, Any], profile: str, criticality: str) -> bool:
    mode = str(config.get("independent_verification", "risk-based")).strip().lower()
    if mode in {"off", "false", "none"}:
        return False
    if mode in {"always", "required"}:
        return True
    return profile == "high-assurance" or criticality == "high"


def inspect_artifact(
    root: Path,
    item: Dict[str, Any],
    minimum_bytes: int = 64,
    profile: Optional[str] = None,
    criticality: str = "medium",
) -> Dict[str, Any]:
    value = str(item.get("path", "")).strip()
    config = load_config(root)
    profile = profile or str(config.get("process_profile", "standard"))
    result: Dict[str, Any] = {
        "id": item.get("id"),
        "type": item.get("type"),
        "path": value,
        "valid": True,
        "issues": [],
        "quality_score": item.get("quality_score"),
        "quality_threshold": quality_threshold(profile, criticality),
    }
    if item.get("stale"):
        result["valid"] = False
        result["issues"].append("artifact_marked_stale")
    if not value:
        result["valid"] = False
        result["issues"].append("missing_path")
        return result
    expected = str(item.get("content_hash", "")).strip().lower()
    if is_uri(value):
        if not expected:
            result["valid"] = False
            result["issues"].append("unverified_external_artifact")
        result["quality_score"] = 1.0
    else:
        path = artifact_path(root, item)
        if path is None or not path.exists():
            result["valid"] = False
            result["issues"].append("path_not_found")
            return result
        try:
            current_hash, total_bytes, file_count = path_fingerprint(path)
        except (OSError, RuntimeError) as exc:
            result["valid"] = False
            result["issues"].append(f"unreadable:{exc}")
            return result
        result.update({"current_hash": current_hash, "total_bytes": total_bytes, "file_count": file_count})
        if total_bytes < minimum_bytes:
            result["valid"] = False
            result["issues"].append("artifact_too_small")
        if file_count == 0:
            result["valid"] = False
            result["issues"].append("empty_directory")
        if bool(config.get("artifact_contract_enforcement", True)):
            quality = artifact_content_quality(path, str(item.get("type", "")), profile, criticality, minimum_bytes)
            result["quality_score"] = quality.get("quality_score")
            result["quality_threshold"] = quality.get("quality_threshold")
            result["quality_contract"] = quality.get("contract")
            result["quality_metrics"] = quality.get("metrics", {})
            if quality.get("issues"):
                result["valid"] = False
                result["issues"].extend(str(x) for x in quality["issues"])
        if expected and current_hash.lower() != expected:
            result["valid"] = False
            result["issues"].append("content_changed_since_acceptance")
        if not expected:
            result["valid"] = False
            result["issues"].append("missing_integrity_hash")

    if verification_required(config, profile, criticality):
        verified_by = str(item.get("verified_by", "")).strip()
        owner = str(item.get("owner", "")).strip()
        if not verified_by:
            result["valid"] = False
            result["issues"].append("missing_independent_verification")
        elif owner and normalize_heading(owner) == normalize_heading(verified_by):
            result["valid"] = False
            result["issues"].append("self_verified_artifact")
    result["issues"] = list(dict.fromkeys(result["issues"]))
    return result


def record_artifact_integrity(
    root: Path,
    path_value: str,
    checksum: str = "",
    artifact_type: str = "",
    profile: str = "standard",
    criticality: str = "medium",
    owner: str = "",
    verified_by: str = "",
) -> Dict[str, Any]:
    config = load_config(root)
    if verification_required(config, profile, criticality):
        if not str(verified_by).strip():
            raise RuntimeError("Accepted artifact requires independent --verified-by under this process profile")
        if owner and normalize_heading(owner) == normalize_heading(verified_by):
            raise RuntimeError("Artifact owner cannot independently verify the same artifact")
    if is_uri(path_value):
        if not checksum:
            raise RuntimeError("Accepted external artifact requires --checksum")
        return {
            "content_hash": checksum.lower(),
            "size_bytes": None,
            "file_count": None,
            "quality_score": 1.0,
            "quality_contract": "external-integrity",
        }
    item = {"path": normalize_path(root, path_value)}
    path = artifact_path(root, item)
    if path is None or not path.exists():
        raise RuntimeError(f"Accepted artifact path does not exist: {path_value}")
    digest, total, count = path_fingerprint(path)
    minimum = int(config.get("gate_artifact_min_bytes", 64))
    quality = artifact_content_quality(path, artifact_type, profile, criticality, minimum)
    issues = list(quality.get("issues", [])) if bool(config.get("artifact_contract_enforcement", True)) else []
    if total < minimum or count == 0 or issues:
        detail = ", ".join(issues or ["artifact_too_small_or_empty"])
        raise RuntimeError(f"Accepted artifact is not substantive: {path_value} ({detail})")
    if checksum and checksum.lower() != digest.lower():
        raise RuntimeError("Provided checksum does not match artifact content")
    return {
        "content_hash": digest,
        "size_bytes": total,
        "file_count": count,
        "quality_score": quality.get("quality_score"),
        "quality_contract": quality.get("contract"),
    }


def normalized_evidence_key(item: Dict[str, Any]) -> Tuple[str, str, Tuple[str, ...]]:
    return (
        re.sub(r"\s+", " ", str(item.get("claim", "")).strip().lower()),
        re.sub(r"\s+", " ", str(item.get("source", "")).strip().lower()),
        tuple(sorted(str(x).strip().lower() for x in item.get("supports", []) if str(x).strip())),
    )


def approval_is_human(value: str) -> bool:
    lowered = re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()
    if not lowered:
        return False
    tokens = set(lowered.split())
    return not bool(tokens & NON_HUMAN_APPROVER_TOKENS)


def require_human_approval(approver: str, approval_id: str, purpose: str) -> None:
    if not approval_is_human(approver):
        raise RuntimeError(f"{purpose} requires an identifiable human approver")
    if not str(approval_id or "").strip():
        raise RuntimeError(f"{purpose} requires --approval-id")


def state_path(root: Path) -> Path:
    return root / ".sdlc" / "state.json"


def require_state(root: Path) -> Dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        raise RuntimeError(f"No .sdlc/state.json under {root}. Run `sdlc.py init {root}` first.")
    state = load_json(path)
    return state


def save_state(root: Path, state: Dict[str, Any], event_name: str = "") -> None:
    state["revision"] = int(state.get("revision", 0)) + 1
    state["project"]["updated_at"] = now()
    current = state_path(root)
    if current.exists():
        backup = root / ".sdlc" / "state.prev.json"
        shutil.copy2(current, backup)
    atomic_write_json(state_path(root), state)
    append_audit_event(root, state, event_name)
    sync_all_ledgers(root, state)
    write_summary(root, state)


def escape_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\n", "<br>").replace("|", "\\|")


def table(title: str, headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    lines = [f"# {title}", "", "| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    count = 0
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(v) for v in row) + " |")
        count += 1
    if count == 0:
        lines.append("| " + " | ".join(["—"] * len(headers)) + " |")
    lines.extend(["", "> Generated from `.sdlc/state.json`. Edit state through the CLI when possible."])
    return "\n".join(lines) + "\n"


def sync_all_ledgers(root: Path, state: Dict[str, Any]) -> None:
    ledger_dir = root / ".sdlc" / "ledgers"
    ledger_dir.mkdir(parents=True, exist_ok=True)

    artifacts = sorted(state.get("artifacts", {}).values(), key=lambda x: x.get("updated_at", ""))
    write_text(ledger_dir / "artifacts.md", table(*LEDGER_CONFIG["artifacts"], (
        (
            x.get("id"), x.get("type"), x.get("status"), x.get("stale", False),
            x.get("quality_score"), x.get("owner"), x.get("path"),
            x.get("content_hash"), x.get("updated_at")
        ) for x in artifacts
    )))
    write_text(ledger_dir / "evidence.md", table(*LEDGER_CONFIG["evidence"], (
        (x.get("id"), x.get("claim"), x.get("source"), x.get("source_type"), x.get("quality"), ", ".join(x.get("supports", [])), x.get("observed_at"), x.get("expires_at")) for x in state.get("evidence", [])
    )))
    write_text(ledger_dir / "assumptions.md", table(*LEDGER_CONFIG["assumptions"], (
        (x.get("id"), x.get("text"), x.get("risk"), x.get("status"), x.get("owner"), x.get("updated_at")) for x in state.get("assumptions", [])
    )))
    write_text(ledger_dir / "decisions.md", table(*LEDGER_CONFIG["decisions"], (
        (x.get("id"), x.get("title"), x.get("choice"), x.get("rationale"), x.get("owner"), x.get("created_at")) for x in state.get("decisions", [])
    )))
    write_text(ledger_dir / "risks.md", table(*LEDGER_CONFIG["risks"], (
        (x.get("id"), x.get("title"), x.get("severity"), x.get("likelihood"), x.get("status"), x.get("mitigation"), x.get("owner")) for x in state.get("risks", [])
    )))
    write_text(ledger_dir / "traceability.md", table(*LEDGER_CONFIG["traceability"], (
        (x.get("id"), x.get("from"), x.get("relation"), x.get("to"), ", ".join(x.get("evidence", [])), x.get("created_at")) for x in state.get("traceability", [])
    )))
    write_text(ledger_dir / "learning-log.md", table(*LEDGER_CONFIG["learning"], (
        (x.get("id"), x.get("expected"), x.get("actual"), x.get("gap"), x.get("decision"), f"{x.get('route_os')}:{x.get('route_stage')}", x.get("created_at")) for x in state.get("learning", [])
    )))
    write_text(ledger_dir / "routing-log.md", table(*LEDGER_CONFIG["routing"], (
        (x.get("id"), x.get("task"), x.get("recommended_os"), x.get("reason"), x.get("created_at")) for x in state.get("routing_log", [])
    )))
    write_text(ledger_dir / "runs.md", table(*LEDGER_CONFIG["runs"], (
        (
            x.get("id"), x.get("actor"), x.get("os"), x.get("skill"), x.get("model"),
            x.get("outcome"), int(x.get("tokens_input", 0)) + int(x.get("tokens_output", 0)),
            x.get("tool_calls", 0), x.get("cost_usd", 0), x.get("human_hours", 0), x.get("duration_ms", 0), x.get("created_at")
        ) for x in state.get("runs", [])
    )))


def accepted_artifact_types(state: Dict[str, Any]) -> set[str]:
    return {
        str(item.get("type"))
        for item in state.get("artifacts", {}).values()
        if item.get("status") == "accepted" and not item.get("stale")
    }


def open_critical_risks(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        risk for risk in state.get("risks", [])
        if risk.get("severity") == "critical" and risk.get("status") in OPEN_RISK_STATUSES
    ]


def state_project_root(state: Dict[str, Any], root: Optional[Path] = None) -> Path:
    if root is not None:
        return root.resolve()
    value = state.get("project", {}).get("root")
    if not value:
        raise RuntimeError("State has no project.root")
    return Path(str(value)).expanduser().resolve()


def accepted_artifact_inspections(
    state: Dict[str, Any], root: Path, minimum_bytes: int
) -> Dict[str, Dict[str, Any]]:
    inspections: Dict[str, Dict[str, Any]] = {}
    for artifact_id, item in state.get("artifacts", {}).items():
        if not isinstance(item, dict) or item.get("status") != "accepted":
            continue
        governance = governance_for_record(state, root, item)
        inspections[str(artifact_id)] = inspect_artifact(
            root, item, minimum_bytes, str(governance["profile"]), str(governance["criticality"])
        )
    return inspections


def artifact_trace_graph(state: Dict[str, Any]) -> Dict[str, set[str]]:
    artifact_ids = set(str(x) for x in state.get("artifacts", {}).keys())
    graph: Dict[str, set[str]] = {artifact_id: set() for artifact_id in artifact_ids}
    for edge in state.get("traceability", []):
        if not isinstance(edge, dict) or str(edge.get("relation", "")) not in TRACE_FORWARD_RELATIONS:
            continue
        source = str(edge.get("from", ""))
        target = str(edge.get("to", ""))
        if source in artifact_ids and target in artifact_ids and source != target:
            graph.setdefault(source, set()).add(target)
    return graph


def downstream_artifact_ids(state: Dict[str, Any], source_ids: Iterable[str]) -> set[str]:
    graph = artifact_trace_graph(state)
    queue = [str(x) for x in source_ids if str(x) in graph]
    seen = set(queue)
    descendants: set[str] = set()
    while queue:
        node = queue.pop(0)
        for child in graph.get(node, set()):
            if child in seen:
                continue
            seen.add(child)
            descendants.add(child)
            queue.append(child)
    return descendants


def mark_downstream_stale(
    state: Dict[str, Any], source_ids: Iterable[str], reason: str
) -> List[str]:
    sources = sorted(set(str(x) for x in source_ids if str(x)))
    affected: List[str] = []
    stamp = now()
    for artifact_id in sorted(downstream_artifact_ids(state, sources)):
        item = state.get("artifacts", {}).get(artifact_id)
        if not isinstance(item, dict) or item.get("status") != "accepted":
            continue
        existing_sources = set(str(x) for x in item.get("stale_from", []))
        item["stale"] = True
        item["stale_from"] = sorted(existing_sources | set(sources))
        item["stale_at"] = stamp
        item["stale_reason"] = reason
        item["updated_at"] = stamp
        affected.append(artifact_id)
    return affected


def transitive_invalid_sources(
    state: Dict[str, Any], inspections: Dict[str, Dict[str, Any]]
) -> Dict[str, set[str]]:
    direct_invalid = {
        artifact_id for artifact_id, inspection in inspections.items()
        if not bool(inspection.get("valid"))
    }
    impacted: Dict[str, set[str]] = {}
    for source_id in direct_invalid:
        for descendant in downstream_artifact_ids(state, [source_id]):
            impacted.setdefault(descendant, set()).add(source_id)
    return impacted


def affected_gates_for_artifacts(state: Dict[str, Any], artifact_ids: Iterable[str]) -> List[str]:
    types = {
        str(state.get("artifacts", {}).get(artifact_id, {}).get("type", ""))
        for artifact_id in artifact_ids
    }
    profile = str(state.get("project", {}).get("profile", "standard"))
    criticality = str(state.get("project", {}).get("criticality", "medium"))
    affected: List[str] = []
    for gate_name, base in load_json(find_manifest("gates.json")).items():
        spec = resolve_gate_spec(base, profile, criticality)
        if types & set(str(x) for x in spec.get("required", [])):
            affected.append(gate_name)
    return sorted(affected)


def trace_endpoint_valid(state: Dict[str, Any], endpoint: str) -> bool:
    endpoint = str(endpoint or "").strip()
    if not endpoint:
        return False
    if endpoint in all_record_ids(state):
        return True
    if ":" not in endpoint:
        return False
    prefix, value = endpoint.split(":", 1)
    return prefix in TRACE_NODE_PREFIXES and bool(value.strip())


def trace_adjacency(state: Dict[str, Any], allowed_nodes: Optional[set[str]] = None) -> Dict[str, set[str]]:
    graph: Dict[str, set[str]] = {}
    for edge in state.get("traceability", []):
        if not isinstance(edge, dict) or str(edge.get("relation", "")) not in TRACE_FORWARD_RELATIONS:
            continue
        source = str(edge.get("from", ""))
        target = str(edge.get("to", ""))
        if not source or not target or source == target:
            continue
        if allowed_nodes is not None and (source not in allowed_nodes or target not in allowed_nodes):
            continue
        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set())
    return graph


def has_directed_path(
    graph: Dict[str, set[str]], sources: Iterable[str], targets: Iterable[str], max_depth: int = 12
) -> bool:
    target_set = {str(x) for x in targets}
    queue: List[Tuple[str, int]] = [(str(x), 0) for x in sources]
    seen = {node for node, _ in queue}
    while queue:
        node, depth = queue.pop(0)
        if node in target_set:
            return True
        if depth >= max_depth:
            continue
        for child in graph.get(node, set()):
            if child not in seen:
                seen.add(child)
                queue.append((child, depth + 1))
    return False


def trace_path_assessment(
    state: Dict[str, Any], accepted_items: Sequence[Dict[str, Any]], paths: Sequence[Sequence[str]]
) -> Dict[str, Any]:
    ids_by_type: Dict[str, set[str]] = {}
    valid_ids: set[str] = set()
    for item in accepted_items:
        artifact_id = str(item.get("id", ""))
        artifact_type = str(item.get("type", ""))
        if artifact_id and artifact_type:
            ids_by_type.setdefault(artifact_type, set()).add(artifact_id)
            valid_ids.add(artifact_id)
    graph = trace_adjacency(state, valid_ids)
    path_results: List[Dict[str, Any]] = []
    passed_paths = 0
    for raw_path in paths:
        path_types = [str(x) for x in raw_path if str(x)]
        segments: List[Dict[str, Any]] = []
        passed = bool(path_types)
        for source_type, target_type in zip(path_types, path_types[1:]):
            sources = ids_by_type.get(source_type, set())
            targets = ids_by_type.get(target_type, set())
            segment_passed = bool(sources and targets and has_directed_path(graph, sources, targets))
            segments.append({
                "from_type": source_type,
                "to_type": target_type,
                "from_ids": sorted(sources),
                "to_ids": sorted(targets),
                "passed": segment_passed,
            })
            passed = passed and segment_passed
        if len(path_types) == 1:
            passed = bool(ids_by_type.get(path_types[0]))
        if passed:
            passed_paths += 1
        path_results.append({"path": path_types, "passed": passed, "segments": segments})
    coverage = passed_paths / len(path_results) if path_results else 1.0
    return {
        "paths": path_results,
        "passed_paths": passed_paths,
        "total_paths": len(path_results),
        "coverage": coverage,
    }


def gate_state_snapshot(
    state: Dict[str, Any],
    gate_name: str,
    artifact_ids: Iterable[str],
    artifact_observations: Dict[str, Dict[str, Any]],
    evidence_ids: Iterable[str],
    critical_risk_ids: Iterable[str],
    trace_edges: Iterable[Dict[str, Any]],
    profile: str,
    effective_policy: Dict[str, Any],
) -> str:
    payload = {
        "gate": gate_name,
        "profile": profile,
        "project_criticality": state.get("project", {}).get("criticality"),
        "effective_criticality": effective_policy.get("effective_criticality", state.get("project", {}).get("criticality")),
        "work_item_id": active_work_id(state),
        "policy": effective_policy,
        "artifacts": sorted(
            {
                artifact_id: {
                    "status": state.get("artifacts", {}).get(artifact_id, {}).get("status"),
                    "content_hash": state.get("artifacts", {}).get(artifact_id, {}).get("content_hash"),
                    "current_hash": artifact_observations.get(artifact_id, {}).get("current_hash"),
                    "valid": artifact_observations.get(artifact_id, {}).get("valid"),
                    "issues": artifact_observations.get(artifact_id, {}).get("issues", []),
                    "quality_score": artifact_observations.get(artifact_id, {}).get("quality_score"),
                    "stale": state.get("artifacts", {}).get(artifact_id, {}).get("stale", False),
                    "updated_at": state.get("artifacts", {}).get(artifact_id, {}).get("updated_at"),
                }
                for artifact_id in artifact_ids
            }.items()
        ),
        "evidence": sorted(set(evidence_ids)),
        "critical_risks": sorted(set(critical_risk_ids)),
        "trace_edges": sorted(
            [
                {
                    "from": str(edge.get("from", "")),
                    "relation": str(edge.get("relation", "")),
                    "to": str(edge.get("to", "")),
                }
                for edge in trace_edges
                if isinstance(edge, dict)
            ],
            key=lambda x: (x["from"], x["relation"], x["to"]),
        ),
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def assess_gate(
    state: Dict[str, Any],
    gate_name: str,
    gates_manifest: Optional[Dict[str, Any]] = None,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    gates = gates_manifest or load_json(find_manifest("gates.json"))
    if gate_name not in gates:
        raise RuntimeError(f"Unknown gate: {gate_name}")
    root = state_project_root(state, root)
    config = load_config(root)
    governance = effective_governance(state, root)
    profile = str(governance["profile"])
    criticality = str(governance["criticality"])
    base_gate = gates[gate_name]
    spec = resolve_gate_spec(base_gate, profile, criticality)
    work = active_work_item(state)
    if work is not None and bool(work.get("bounded")) and profile == "lite" and isinstance(base_gate.get("bounded_lite"), dict):
        for key, value in deepcopy(base_gate["bounded_lite"]).items():
            spec[key] = value
        spec["effective_work_profile"] = "bounded-lite"
    domain_required = work_domain_gate_overlays(state, root, gate_name)
    required = list(dict.fromkeys([*(str(x) for x in spec.get("required", [])), *domain_required]))
    minimum_bytes = int(config.get("gate_artifact_min_bytes", 64))

    all_inspections = accepted_artifact_inspections(state, root, minimum_bytes)
    if active_work_item(state) is not None:
        all_inspections = {
            artifact_id: inspection for artifact_id, inspection in all_inspections.items()
            if record_matches_active_work(state, state.get("artifacts", {}).get(artifact_id, {}))
        }
    impacted_by_invalid = transitive_invalid_sources(state, all_inspections)
    accepted_items: List[Dict[str, Any]] = []
    invalid_artifacts: List[Dict[str, Any]] = []
    valid_types: set[str] = set()
    required_artifact_ids: set[str] = set()
    for item in state.get("artifacts", {}).values():
        if not isinstance(item, dict) or item.get("status") != "accepted" or item.get("type") not in required:
            continue
        if active_work_item(state) is not None and not record_matches_active_work(state, item):
            continue
        artifact_id = str(item.get("id", ""))
        required_artifact_ids.add(artifact_id)
        inspection = deepcopy(
            all_inspections.get(artifact_id)
            or inspect_artifact(root, item, minimum_bytes, profile, criticality)
        )
        upstream_sources = sorted(impacted_by_invalid.get(artifact_id, set()))
        if upstream_sources and inspection.get("valid"):
            inspection["valid"] = False
            inspection.setdefault("issues", []).append(
                "upstream_artifact_invalid:" + ",".join(upstream_sources)
            )
            inspection["upstream_invalid_sources"] = upstream_sources
        if inspection["valid"]:
            accepted_items.append(item)
            valid_types.add(str(item.get("type")))
        else:
            invalid_artifacts.append(inspection)
    missing = [x for x in required if x not in valid_types]

    evidence_targets = {gate_name, *required}
    domain_evidence_required = work_domain_required_evidence(state, root) if gate_name == "production-ready" else []
    evidence_targets.update(domain_evidence_required)
    evidence_targets.update(str(item.get("id")) for item in accepted_items if item.get("id"))
    all_evidence = [
        item for item in state.get("evidence", [])
        if isinstance(item, dict) and (active_work_item(state) is None or record_matches_active_work(state, item))
    ]
    evidence: List[Dict[str, Any]] = []
    invalid_evidence: List[str] = []
    duplicate_evidence: List[str] = []
    seen_evidence: set[Tuple[str, str, Tuple[str, ...]]] = set()
    current_time = datetime.now(timezone.utc)
    for item in all_evidence:
        if not isinstance(item, dict):
            invalid_evidence.append("<non-object>")
            continue
        if active_work_item(state) is not None and not record_matches_active_work(state, item):
            continue
        evidence_id = str(item.get("id", ""))
        if not str(item.get("claim", "")).strip() or not str(item.get("source", "")).strip():
            invalid_evidence.append(evidence_id or "<missing-id>")
            continue
        if item.get("quality") not in QUALITY_ORDER or item.get("source_type", "other") not in EVIDENCE_SOURCE_TYPES:
            invalid_evidence.append(evidence_id or "<missing-id>")
            continue
        expiry = parse_time(str(item.get("expires_at", "")))
        if expiry and expiry <= current_time:
            invalid_evidence.append(evidence_id or "<missing-id>")
            continue
        supports = {str(x) for x in item.get("supports", [])}
        if not supports & evidence_targets:
            continue
        key = normalized_evidence_key(item)
        if bool(config.get("evidence_deduplicate", True)) and key in seen_evidence:
            duplicate_evidence.append(evidence_id or "<missing-id>")
            continue
        seen_evidence.add(key)
        evidence.append(item)

    high_quality = [
        x for x in evidence
        if x.get("quality") == "high" and x.get("source_type", "other") in HIGH_QUALITY_SOURCE_TYPES
    ]
    evidence_shortfall = max(0, int(spec.get("minimum_evidence", 0)) - len(evidence))
    high_quality_shortfall = max(0, int(spec.get("minimum_high_quality_evidence", 0)) - len(high_quality))
    distinct_sources = {
        re.sub(r"\s+", " ", str(x.get("source", "")).strip().lower()) for x in evidence
    }
    source_shortfall = max(0, int(spec.get("minimum_distinct_sources", 0)) - len(distinct_sources))
    covered_targets: set[str] = set()
    for item in evidence:
        covered_targets.update(str(x) for x in item.get("supports", []) if str(x) in evidence_targets)
    evidence_target_shortfall = max(0, int(spec.get("minimum_evidence_targets", 0)) - len(covered_targets))
    missing_domain_evidence = [target for target in domain_evidence_required if target not in covered_targets]

    valid_artifact_ids = {str(item.get("id")) for item in accepted_items if item.get("id")}
    traced_artifacts: set[str] = set()
    relevant_trace_edges: List[Dict[str, Any]] = []
    trace_source = [
        edge for edge in state.get("traceability", [])
        if isinstance(edge, dict) and (active_work_item(state) is None or record_matches_active_work(state, edge))
    ]
    for edge in trace_source:
        if not isinstance(edge, dict) or str(edge.get("relation", "")) not in TRACE_FORWARD_RELATIONS:
            continue
        source = str(edge.get("from", ""))
        target = str(edge.get("to", ""))
        if source == target:
            continue
        if source in valid_artifact_ids or target in valid_artifact_ids:
            relevant_trace_edges.append(edge)
        if source in valid_artifact_ids:
            traced_artifacts.add(source)
        if target in valid_artifact_ids:
            traced_artifacts.add(target)
    trace_coverage = len(traced_artifacts) / len(valid_artifact_ids) if valid_artifact_ids else 0.0
    minimum_trace_coverage = float(spec.get("minimum_trace_coverage", 0.0))
    trace_shortfall = max(0.0, minimum_trace_coverage - trace_coverage)

    path_state = state if active_work_item(state) is None else {**state, "traceability": trace_source}
    path_assessment = trace_path_assessment(path_state, accepted_items, spec.get("trace_paths", []))
    trace_path_coverage = float(path_assessment["coverage"])
    minimum_trace_path_coverage = float(spec.get("minimum_trace_path_coverage", 0.0))
    trace_path_shortfall = max(0.0, minimum_trace_path_coverage - trace_path_coverage)

    critical = blocking_critical_risks(state) if spec.get("blocks_open_critical_risks", False) else []
    passed = (
        not missing
        and not invalid_artifacts
        and evidence_shortfall == 0
        and high_quality_shortfall == 0
        and source_shortfall == 0
        and evidence_target_shortfall == 0
        and not missing_domain_evidence
        and trace_shortfall <= 1e-9
        and trace_path_shortfall <= 1e-9
        and not critical
    )
    policy_snapshot = {
        key: value for key, value in spec.items()
        if key not in {"profiles", "purpose"}
    }
    result = {
        "gate": gate_name,
        "status": "pass" if passed else "fail",
        "checked_at": now(),
        "purpose": spec.get("purpose", ""),
        "profile": profile,
        "criticality": criticality,
        "project_profile": process_profile(state, root),
        "project_criticality": str(state.get("project", {}).get("criticality", "medium")),
        "work_item_id": str(governance.get("work_item_id", "")),
        "required": required,
        "domain_required_artifacts": domain_required,
        "missing_artifacts": missing,
        "invalid_artifacts": invalid_artifacts,
        "upstream_invalidations": {
            artifact_id: sorted(sources)
            for artifact_id, sources in impacted_by_invalid.items()
            if artifact_id in required_artifact_ids
        },
        "total_evidence_count": len(all_evidence),
        "evidence_count": len(evidence),
        "evidence_shortfall": evidence_shortfall,
        "duplicate_evidence": duplicate_evidence,
        "invalid_evidence": invalid_evidence,
        "high_quality_evidence_count": len(high_quality),
        "high_quality_evidence_shortfall": high_quality_shortfall,
        "distinct_source_count": len(distinct_sources),
        "distinct_source_shortfall": source_shortfall,
        "evidence_target_count": len(covered_targets),
        "evidence_target_shortfall": evidence_target_shortfall,
        "missing_domain_evidence": missing_domain_evidence,
        "trace_coverage": round(trace_coverage, 4),
        "minimum_trace_coverage": minimum_trace_coverage,
        "trace_coverage_shortfall": round(trace_shortfall, 4),
        "trace_path_results": path_assessment["paths"],
        "trace_paths_passed": path_assessment["passed_paths"],
        "trace_paths_total": path_assessment["total_paths"],
        "trace_path_coverage": round(trace_path_coverage, 4),
        "minimum_trace_path_coverage": minimum_trace_path_coverage,
        "trace_path_coverage_shortfall": round(trace_path_shortfall, 4),
        "blocking_critical_risks": [x.get("id") for x in critical],
    }
    snapshot_artifact_ids = set(required_artifact_ids)
    for sources in impacted_by_invalid.values():
        snapshot_artifact_ids.update(sources)
    result["state_snapshot"] = gate_state_snapshot(
        state,
        gate_name,
        snapshot_artifact_ids,
        all_inspections,
        [str(x.get("id")) for x in evidence if x.get("id")],
        [str(x.get("id")) for x in critical if x.get("id")],
        relevant_trace_edges,
        profile,
        policy_snapshot,
    )
    return result


def latest_gate_outcome(state: Dict[str, Any], gate_name: str) -> Optional[Dict[str, Any]]:
    entries = state.get("gates", {}).get(gate_name, [])
    return entries[-1] if entries else None


def waiver_is_active(waiver: Dict[str, Any], current_snapshot: str = "") -> bool:
    expiry = parse_time(str(waiver.get("expires", "")))
    if expiry is None or expiry <= datetime.now(timezone.utc):
        return False
    if not approval_is_human(str(waiver.get("approver", ""))):
        return False
    if not str(waiver.get("approval_id", "")).strip():
        return False
    if not str(waiver.get("compensating_control", "")).strip():
        return False
    snapshot = str(waiver.get("state_snapshot", ""))
    if current_snapshot and snapshot != current_snapshot:
        return False
    return True


def gate_allows_transition(state: Dict[str, Any], gate_name: str, root: Optional[Path] = None) -> Tuple[bool, Dict[str, Any]]:
    result = assess_gate(state, gate_name, root=root)
    if result["status"] == "pass":
        return True, result
    latest = latest_gate_outcome(state, gate_name)
    if latest and latest.get("status") == "waived" and waiver_is_active(latest, result.get("state_snapshot", "")):
        result["status"] = "waived"
        result["waiver"] = latest
        return True, result
    return False, result


def write_summary(root: Path, state: Dict[str, Any]) -> Path:
    os_states = state.get("os_states", {})
    accepted = sorted(accepted_artifact_types(state))
    critical = open_critical_risks(state)
    metrics = project_metrics(state, root) if "runs" in state else {"runs": 0, "cost_usd": 0, "stale_artifacts": []}
    route = next_recommendation(state, root)
    governance = effective_governance(state, root)
    work = active_work_item(state)
    lines = [
        f"# {state['project']['name']} — SDLC Summary",
        "",
        f"- Status: **{state.get('status')}**",
        f"- Active OS: **{state.get('current_os')}**",
        f"- Stage: **{state.get('current_stage')}**",
        f"- Criticality: **{state['project'].get('criticality')}**",
        f"- Project process profile: **{state['project'].get('profile', 'standard')}**",
        f"- Effective process profile: **{governance['profile']} / {governance['criticality']}**",
        f"- Active work: **{work.get('id') + ' — ' + work.get('title') if work else 'none'}**",
        f"- Agent runs / cost: **{metrics.get('runs', 0)} / ${metrics.get('cost_usd', 0)}**",
        f"- Stale accepted artifacts: **{len(metrics.get('stale_artifacts', []))}**",
        f"- Updated: {state['project'].get('updated_at')}",
        "",
        "## OS progress",
        "",
        "| OS | Stage | Status |",
        "| --- | --- | --- |",
    ]
    for os_name in OS_SEQUENCE:
        entry = os_states.get(os_name, {})
        lines.append(f"| {os_name} | {entry.get('stage', '—')} | {entry.get('status', 'pending')} |")
    lines.extend([
        "",
        "## Current recommendation",
        "",
        route["text"],
        "",
        "## Accepted artifacts",
        "",
    ])
    lines.extend([f"- `{x}`" for x in accepted] or ["- None"])
    lines.extend(["", "## Open critical risks", ""])
    lines.extend([f"- `{x.get('id')}` {x.get('title')}" for x in critical] or ["- None"])
    lines.extend(["", "> Generated from `.sdlc/state.json`."])
    path = root / ".sdlc" / "SUMMARY.md"
    write_text(path, "\n".join(lines))
    return path


def initial_state(
    name: str,
    project_type: str,
    criticality: str,
    root: Path,
    start_os: Optional[str] = None,
    profile: str = "standard",
) -> Dict[str, Any]:
    routing = load_json(find_manifest("os-routing.json"))
    stamp = now()
    default_start = {
        "greenfield": "pm",
        "brownfield": "engineering",
        "incident": "evolution",
        "migration": "engineering",
    }
    active_os = start_os or default_start[project_type]
    os_states: Dict[str, Dict[str, Any]] = {}
    for os_name in OS_SEQUENCE:
        first = routing["os_stages"][os_name][0]
        os_states[os_name] = {
            "stage": first,
            "status": "active" if os_name == active_os else "pending",
            "history": [{"stage": first, "at": stamp, "reason": "initialized"}] if os_name == active_os else [],
        }
    return {
        "version": VERSION,
        "revision": 0,
        "project": {
            "name": name,
            "type": project_type,
            "criticality": criticality,
            "profile": profile,
            "root": str(root),
            "created_at": stamp,
            "updated_at": stamp,
        },
        "current_os": active_os,
        "current_stage": "INTAKE",
        "status": "active",
        "os_states": os_states,
        "history": [{"event": "project-initialized", "at": stamp, "os": active_os, "stage": "INTAKE"}],
        "artifacts": {},
        "evidence": [],
        "assumptions": [],
        "decisions": [],
        "risks": [],
        "traceability": [],
        "gates": {},
        "learning": [],
        "routing_log": [],
        "runs": [],
        "work_items": {},
        "active_work_id": "",
    }


def create_kernel(root: Path, state: Dict[str, Any]) -> None:
    base = root / ".sdlc"
    for dirname in ["ledgers", "os", "gates", "artifacts", "evidence", "reviews"]:
        (base / dirname).mkdir(parents=True, exist_ok=True)
    write_text(base / "context.md", f"""# Project Context

## Product

- Name: {state['project']['name']}
- Type: {state['project']['type']}
- Criticality: {state['project']['criticality']}

## Users and problem

Record verified users, jobs, pain points and context. Separate facts, inferences and assumptions.

## Business objective

Define the measurable outcome and time horizon.

## Constraints

Record legal, privacy, security, accessibility, budget, platform and delivery constraints.

## Current scope

Define in-scope and non-goals.
""")
    write_text(base / "config.json", json.dumps({
        "schema_version": VERSION,
        "gate_policy": "strict",
        "allow_waiver": True,
        "max_waiver_days": 14,
        "allow_force_transition": True,
        "force_requires_human_approval": True,
        "waiver_requires_approver": True,
        "artifact_status_required_for_gates": "accepted",
        "gate_artifact_min_bytes": 64,
        "gate_require_integrity": True,
        "stage_policy": "adjacent",
        "evidence_deduplicate": True,
        "process_profile": state["project"].get("profile", "standard"),
        "audit_chain": True,
        "artifact_contract_enforcement": True,
        "independent_verification": "risk-based",
        "cost_budget_usd": None,
        "token_budget": None,
        "budget_hard_enforcement": state["project"].get("profile", "standard") == "high-assurance",
        "domain_packs": [],
        "domain_required_controls": [],
        "domain_required_artifacts": [],
        "domain_required_evidence": [],
        "domain_gate_overlays": {},
        "domain_risk_adjustment": 0.0,
        "domain_budget_multiplier": 1.0,
    }, ensure_ascii=False, indent=2))
    for os_name in OS_SEQUENCE:
        write_text(base / "os" / f"{os_name}.md", f"# {os_name.upper()} OS\n\n## Current work\n\n## Evidence gaps\n\n## Decisions\n\n## Handoff notes\n")
    for gate_name in load_json(find_manifest("gates.json")):
        write_text(base / "gates" / f"{gate_name}.md", f"# Gate: {gate_name}\n\nRun `sdlc.py gate . --name {gate_name}` to generate the current assessment.\n")
    save_state(root, state)


def cmd_init(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    root.mkdir(parents=True, exist_ok=True)
    path = state_path(root)
    if path.exists() and not args.force:
        raise RuntimeError(f"Project already initialized: {path}. Use --force to replace state.")
    if path.exists() and args.force:
        backup = root / f".sdlc.backup-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        shutil.move(str(root / ".sdlc"), str(backup))
    name = args.name or root.name
    profile = args.profile or {"low": "lite", "medium": "standard", "high": "high-assurance"}[args.criticality]
    if args.criticality == "high" and profile == "lite":
        raise RuntimeError("High-criticality projects cannot use the lite process profile")
    state = initial_state(name, args.type, args.criticality, root, args.start_os, profile)
    create_kernel(root, state)
    print(f"Initialized Agentic SDLC OS at {root / '.sdlc'}")
    print(f"Current: {state['current_os']} / {state['current_stage']}")
    return 0


def print_json_or_text(payload: Dict[str, Any], as_json: bool, text: str) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(text)



def _installed_domain_impacts(state: Dict[str, Any], root: Path, text: str, explicit: Sequence[str]) -> List[str]:
    config = load_config(root)
    installed = [str(x) for x in config.get("domain_packs", [])]
    impacts = [str(x) for x in explicit if str(x)]
    lowered = text.lower()
    for pack_id in installed:
        path = _domain_pack_path(pack_id)
        if not path:
            continue
        pack = load_json(path)
        keywords = [str(x).lower() for x in pack.get("keywords", [])]
        if any(keyword and keyword in lowered for keyword in keywords):
            impacts.append(pack_id)
    unknown = sorted(set(impacts) - set(installed))
    if unknown:
        raise RuntimeError("Domain impact is not installed on this project: " + ", ".join(unknown))
    return list(dict.fromkeys(impacts))


def cmd_work_start(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    if active_work_item(state) is not None:
        raise RuntimeError(f"Active work already exists: {active_work_id(state)}")
    paths: List[str] = []
    for value in args.affected_path or []:
        paths.extend(split_csv(value))
    paths = list(dict.fromkeys(paths))
    if args.bounded and not paths:
        raise RuntimeError("--bounded requires at least one --affected-path")
    factors = {
        name: DEFAULT_WORK_FACTORS[name] if getattr(args, name) is None else int(getattr(args, name))
        for name in WORK_FACTOR_NAMES
    }
    text = " ".join([args.title, *paths])
    domain_impacts = _installed_domain_impacts(state, root, text, args.domain_impact or [])
    domain_risk = 0.0
    for pack_id in domain_impacts:
        pack_path = _domain_pack_path(pack_id)
        if pack_path:
            domain_risk += float(load_json(pack_path).get("risk_adjustment", 0.0))
    tailoring = _work_tailoring(factors, domain_risk)
    profile = str(tailoring["profile"])
    escalations = list(tailoring["hard_escalations"])
    lowered_paths = [value.replace("\\", "/").lower() for value in paths]
    if any(pattern in path for path in lowered_paths for pattern in WORK_HIGH_ASSURANCE_PATTERNS):
        profile = "high-assurance"
        escalations.append("high-assurance-path")
    elif any(pattern in path for path in lowered_paths for pattern in WORK_PROTECTED_PATTERNS):
        if PROFILE_ORDER[profile] < PROFILE_ORDER["standard"]:
            profile = "standard"
        escalations.append("protected-path>=standard")
    project_profile = process_profile(state, root)
    if not args.bounded and PROFILE_ORDER[profile] < PROFILE_ORDER[project_profile]:
        profile = project_profile
        escalations.append("unbounded-work>=project-profile")
    item_id = args.id or uid("work")
    ensure_new_id(state, item_id)
    stamp = now()
    item = {
        "id": item_id,
        "title": args.title,
        "status": "active",
        "bounded": bool(args.bounded),
        "affected_paths": paths,
        "profile": profile,
        "criticality": PROFILE_CRITICALITY[profile],
        "risk_score": tailoring["risk_score"],
        "factors": factors,
        "hard_escalations": list(dict.fromkeys(escalations)),
        "domain_impacts": domain_impacts,
        "project_profile": project_profile,
        "rationale": [
            f"work-risk-score={tailoring['risk_score']}",
            f"bounded={bool(args.bounded)}",
            f"affected-paths={len(paths)}",
            f"domain-impacts={','.join(domain_impacts) if domain_impacts else 'none'}",
        ],
        "created_at": stamp,
        "updated_at": stamp,
        "ended_at": "",
        "outcome": "",
    }
    state.setdefault("work_items", {})[item_id] = item
    state["active_work_id"] = item_id
    state.setdefault("history", []).append({
        "event": "work-started", "at": stamp, "work_item_id": item_id,
        "profile": profile, "risk_score": item["risk_score"], "bounded": item["bounded"],
    })
    save_state(root, state, "work-started")
    print(json.dumps(item, ensure_ascii=False, indent=2) if args.json else f"Work {item_id} started: {profile} / {item['criticality']} (risk={item['risk_score']})")
    return 0


def cmd_work_status(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    item = active_work_item(state)
    if args.id:
        item = state.get("work_items", {}).get(args.id)
    if not isinstance(item, dict):
        payload = {"active_work_id": state.get("active_work_id", ""), "work": None}
        print_json_or_text(payload, args.json, "No matching work item")
        return 1
    governance = effective_governance(state, root) if item.get("id") == active_work_id(state) else {
        "profile": item.get("profile"), "criticality": item.get("criticality"), "work_item_id": item.get("id")
    }
    payload = {"work": item, "effective_governance": governance}
    text = f"Work: {item['id']} — {item['title']}\nStatus: {item['status']}\nProfile: {item['profile']} / {item['criticality']}\nBounded: {item['bounded']}\nPaths: {', '.join(item.get('affected_paths', [])) or 'none'}\nDomain impacts: {', '.join(item.get('domain_impacts', [])) or 'none'}"
    print_json_or_text(payload, args.json, text)
    return 0


def cmd_work_end(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    item = active_work_item(state)
    if item is None:
        raise RuntimeError("No active work item")
    if args.id and args.id != item.get("id"):
        raise RuntimeError(f"Active work is {item.get('id')}, not {args.id}")
    item["status"] = args.status
    item["outcome"] = args.outcome or ""
    item["updated_at"] = now()
    item["ended_at"] = item["updated_at"]
    state["active_work_id"] = ""
    state.setdefault("history", []).append({
        "event": "work-ended", "at": item["ended_at"], "work_item_id": item["id"],
        "status": item["status"], "outcome": item["outcome"],
    })
    save_state(root, state, "work-ended")
    print(f"Work {item['id']} ended [{item['status']}]")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    governance = effective_governance(state, root)
    work = active_work_item(state)
    payload = {
        "project": state["project"],
        "version": state.get("version"),
        "revision": state.get("revision", 0),
        "profile": process_profile(state, root),
        "effective_profile": governance["profile"],
        "effective_criticality": governance["criticality"],
        "active_work": work,
        "status": state.get("status"),
        "current_os": state.get("current_os"),
        "current_stage": state.get("current_stage"),
        "accepted_artifacts": sorted(accepted_artifact_types(state)),
        "open_critical_risks": open_critical_risks(state),
        "next": next_recommendation(state, root),
    }
    text = (
        f"Project: {state['project']['name']}\n"
        f"Version/revision: {state.get('version')} / {state.get('revision', 0)}\n"
        f"Project profile: {payload['profile']}\n"
        f"Effective profile: {payload['effective_profile']} / {payload['effective_criticality']}\n"
        f"Active work: {work.get('id') + ' - ' + work.get('title') if work else 'none'}\n"
        f"Status: {state.get('status')}\n"
        f"Current: {state.get('current_os')} / {state.get('current_stage')}\n"
        f"Accepted artifacts: {len(payload['accepted_artifacts'])}\n"
        f"Open critical risks: {len(payload['open_critical_risks'])}\n"
        f"Next: {payload['next']['text']}"
    )
    print_json_or_text(payload, args.json, text)
    return 0

def phrase_matches(text: str, phrase: str) -> bool:
    phrase = phrase.strip().lower()
    if not phrase:
        return False
    if re.fullmatch(r"[a-z0-9_+./-]+", phrase):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text))
    return phrase in text



def route_task(state: Dict[str, Any], task: str) -> Dict[str, Any]:
    routing = load_json(find_manifest("os-routing.json"))
    lowered = task.lower()
    scores: Dict[str, int] = {name: 0 for name in OS_SEQUENCE}
    hits: Dict[str, List[str]] = {name: [] for name in OS_SEQUENCE}
    for os_name, words in routing.get("intent_keywords", {}).items():
        for word in words:
            if phrase_matches(lowered, str(word)):
                weight = 2 if len(str(word)) >= 4 else 1
                scores[os_name] += weight
                hits[os_name].append(str(word))
    for os_name, patterns in routing.get("weighted_patterns", {}).items():
        for pattern, weight in patterns.items():
            if phrase_matches(lowered, str(pattern)):
                scores[os_name] += int(weight)
                hits[os_name].append(str(pattern))

    if any(word in lowered for word in ["production incident", "线上事故", "严重故障", "sev-1", "sev1", "p0事故"]):
        scores["evolution"] += 12
        hits["evolution"].append("incident-override")
    post_release = any(x in lowered for x in ["上线后", "发布后", "生产中", "线上运行", "真实使用结果", "实际用户使用"])
    outcome_signal = any(x in lowered for x in ["下降", "上升", "转化", "留存", "活跃", "根因", "原因", "效果", "指标", "告警", "退化"])
    production_verification = any(x in lowered for x in ["冒烟检查", "上线验证", "发布验证", "部署验证", "立即检查", "关键链路"])
    if post_release and production_verification:
        scores["release"] += 10
        hits["release"].append("production-verification")
    elif post_release and outcome_signal:
        scores["evolution"] += 8
        hits["evolution"].append("post-release-outcome")
    if any(x in lowered for x in ["复现缺陷", "验证修复", "没有引入新问题", "是否可交付", "测试结论", "是否放行"]):
        scores["qa"] += 6
        hits["qa"].append("verification-intent")
    if any(x in lowered for x in ["修复", "重写", "实现", "重构", "内存泄漏", "重复扣款", "编码工作"]):
        scores["engineering"] += 4
        hits["engineering"].append("implementation-intent")
    if any(x in lowered for x in ["灰度", "金丝雀", "逐步扩大", "撤回方案", "版本窗口", "生产配置", "小流量"]):
        scores["release"] += 6
        hits["release"].append("rollout-intent")

    # Cross-cutting security work still needs an execution owner. Route remediation to
    # Engineering, verification-only work to QA, and deployment/rotation work to Release.
    security_signal = any(x in lowered for x in [
        "安全", "鉴权", "认证", "授权", "权限", "密钥", "secret", "jwt",
        "token forgery", "token 伪造", "漏洞", "vulnerability", "credential",
    ])
    security_verify = any(x in lowered for x in [
        "安全测试", "渗透测试", "验证漏洞", "验证修复", "安全验证", "回归验证",
        "security test", "penetration test", "security verification", "verify the security fix",
        "verify the fix", "regression safety", "security regression", "before handoff",
    ])
    security_release = any(x in lowered for x in [
        "轮换密钥", "rotate secret", "rotate key", "secret rotation", "rotate the supplier jwt secret",
        "生产密钥", "secret deployment", "production secret injection", "deploy it safely",
        "rollback controls", "production deployment",
    ])
    security_remediate = any(x in lowered for x in [
        "修复", "移除", "改为", "替换", "注入", "加固", "fix", "remove",
        "replace", "inject", "harden", "require",
    ])
    if security_signal and security_verify:
        scores["qa"] += 14
        hits["qa"].append("security-verification")
    elif security_signal and security_release:
        scores["release"] += 16
        hits["release"].append("security-release")
    elif security_signal and security_remediate:
        scores["engineering"] += 9
        hits["engineering"].append("security-remediation")

    # Readiness/prerequisite audits are upstream decision work when they ask whether
    # implementation may safely begin, even if design artifacts are among the inputs.
    readiness_signal = any(x in lowered for x in [
        "实施就绪", "开发前置", "前置条件", "监管前置", "协议前置",
        "implementation readiness", "implementation prerequisite", "regulatory prerequisite",
    ])
    upstream_signal = any(x in lowered for x in [
        "调研", "research", "功能清单", "feature inventory", "监管", "regulatory",
        "协议", "protocol", "合规", "compliance", "甲方", "外部依赖", "external dependency",
    ])
    if readiness_signal and upstream_signal:
        scores["pm"] += 10
        hits["pm"].append("implementation-readiness")

    ordered = sorted(scores.items(), key=lambda x: (-x[1], OS_SEQUENCE.index(x[0])))
    max_score = ordered[0][1]
    second_score = ordered[1][1] if len(ordered) > 1 else 0
    candidates = [name for name, value in scores.items() if value == max_score]
    selected = state.get("current_os") if state.get("current_os") in candidates else candidates[0]
    if max_score == 0:
        selected = state.get("current_os", "pm")
        reason = "未发现强路由信号，保持当前 OS 作为人工确认回退"
    else:
        reason = f"命中信号：{', '.join(dict.fromkeys(hits[selected]))}" if hits[selected] else "命中高优先级场景"
    stage = state.get("os_states", {}).get(selected, {}).get("stage") or routing["os_stages"][selected][0]
    total_positive = sum(value for value in scores.values() if value > 0)
    margin = max_score - second_score
    confidence = 0.0 if max_score == 0 else min(
        1.0,
        (max_score / max(1, total_positive)) * 0.65 + min(0.35, margin / 10),
    )
    # Deterministic routing is a conservative control layer: low score, tie, or narrow margin must abstain.
    needs_context = max_score == 0 or max_score < 4 or margin < 2
    decision = "abstain" if needs_context else "route"
    if decision == "abstain":
        reason = f"低置信或意图冲突，拒绝自动路由；候选回退为 {selected}。{reason}"
    return {
        "decision": decision,
        "recommended_os": selected if decision == "route" else None,
        "recommended_stage": stage if decision == "route" else None,
        "fallback_os": selected,
        "fallback_stage": stage,
        "scores": scores,
        "hits": hits,
        "reason": reason,
        "confidence": round(confidence, 3),
        "margin": margin,
    }

def cmd_route(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    result = route_task(state, args.task)
    route_id = uid("route")
    ensure_new_id(state, route_id)
    entry = {
        "id": route_id,
        "task": args.task,
        "decision": result["decision"],
        "recommended_os": result["recommended_os"],
        "recommended_stage": result["recommended_stage"],
        "fallback_os": result["fallback_os"],
        "fallback_stage": result["fallback_stage"],
        "confidence": result["confidence"],
        "reason": result["reason"],
        "created_at": now(),
    }
    state.setdefault("routing_log", []).append(entry)
    save_state(root, state)
    if result["decision"] == "route":
        text = f"Route: {result['recommended_os']} / {result['recommended_stage']}\nReason: {result['reason']}"
    else:
        text = f"Route: ABSTAIN\nFallback: {result['fallback_os']} / {result['fallback_stage']}\nReason: {result['reason']}"
    print_json_or_text(result, args.json, text)
    return 0


def effective_stages(state: Dict[str, Any], root: Path, os_name: str, routing: Dict[str, Any]) -> List[str]:
    full = list(routing["os_stages"][os_name])
    work = active_work_item(state)
    governance = effective_governance(state, root)
    if not work or not bool(work.get("bounded")) or governance["profile"] != "lite":
        return full
    compressed = {
        "engineering": ["INTAKE", "BUILD", "HANDOFF"],
        "qa": ["INTAKE", "EXECUTION", "RECOMMENDATION"],
        "release": ["INTAKE", "READINESS", "REVIEW"],
    }.get(os_name)
    return compressed if compressed else full


def next_recommendation(state: Dict[str, Any], root: Optional[Path] = None) -> Dict[str, Any]:
    routing = load_json(find_manifest("os-routing.json"))
    effective_root = state_project_root(state, root)
    current_os = state.get("current_os")
    current_stage = state.get("current_stage")
    stages = effective_stages(state, effective_root, current_os, routing)
    if current_stage not in stages:
        stages = routing["os_stages"][current_os]
    try:
        index = stages.index(current_stage)
    except ValueError:
        return {"kind": "repair", "text": f"Invalid current stage {current_os}/{current_stage}; run validate."}
    if index + 1 < len(stages):
        target = stages[index + 1]
        if current_os == "engineering" and target == "BUILD":
            allowed, result = gate_allows_transition(state, "build-ready", root)
            if not allowed:
                return {"kind": "gate", "gate": "build-ready", "target_os": current_os, "target_stage": target, "result": result, "text": "Complete or explicitly waive `build-ready` before BUILD."}
        return {"kind": "stage", "target_os": current_os, "target_stage": target, "text": f"Advance to {current_os}/{target}."}
    sequence_index = OS_SEQUENCE.index(current_os)
    if current_os == "evolution":
        return {"kind": "learning", "gate": "learning-decision", "text": "Record a learning decision and re-enter the OS that owns the diagnosed gap."}
    target_os = OS_SEQUENCE[sequence_index + 1]
    gate_name = routing["cross_os"].get(f"{current_os}->{target_os}")
    allowed, result = gate_allows_transition(state, gate_name, root)
    if allowed:
        return {"kind": "handoff", "gate": gate_name, "target_os": target_os, "target_stage": routing["os_stages"][target_os][0], "result": result, "text": f"Gate `{gate_name}` allows handoff to {target_os}."}
    return {"kind": "gate", "gate": gate_name, "target_os": target_os, "target_stage": routing["os_stages"][target_os][0], "result": result, "text": f"Complete or explicitly waive `{gate_name}` before handoff to {target_os}."}


def cmd_next(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    result = next_recommendation(state, root)
    print_json_or_text(result, args.json, result["text"])
    return 0


def validate_stage(os_name: str, stage: str, routing: Dict[str, Any]) -> str:
    stage = stage.upper()
    if os_name not in routing["os_stages"]:
        raise RuntimeError(f"Unknown OS: {os_name}")
    if stage not in routing["os_stages"][os_name]:
        valid = ", ".join(routing["os_stages"][os_name])
        raise RuntimeError(f"Invalid stage for {os_name}: {stage}. Valid: {valid}")
    return stage


def cmd_transition(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    config = load_config(root)
    routing = load_json(find_manifest("os-routing.json"))
    source_os = state["current_os"]
    source_stage = state["current_stage"]
    target_os = args.to_os or args.os or source_os
    target_stage_raw = args.to_stage or args.stage or routing["os_stages"][target_os][0]
    target_stage = validate_stage(target_os, target_stage_raw, routing)

    if args.force:
        if not bool(config.get("allow_force_transition", True)):
            raise RuntimeError("Forced transitions are disabled by .sdlc/config.json")
        if bool(config.get("force_requires_human_approval", True)):
            require_human_approval(args.approver or "", args.approval_id or "", "Forced transition")

    gate_name: Optional[str] = None
    gate_result: Optional[Dict[str, Any]] = None
    rework = False
    if target_os == source_os:
        stages = effective_stages(state, root, source_os, routing)
        if source_stage not in stages or target_stage not in stages:
            stages = routing["os_stages"][source_os]
        source_index = stages.index(source_stage)
        target_index = stages.index(target_stage)
        if target_index > source_index + 1 and not args.force:
            raise RuntimeError(
                f"Cannot skip stages {source_os}/{source_stage} -> {target_stage}. "
                "Advance one stage at a time or use an approved --force transition."
            )
        if target_index < source_index:
            rework = True
        if target_os == "engineering" and target_stage == "BUILD" and source_stage != "BUILD":
            gate_name = "build-ready"
    else:
        gate_name = routing.get("cross_os", {}).get(f"{source_os}->{target_os}")
        if not gate_name:
            source_index = OS_SEQUENCE.index(source_os)
            target_index = OS_SEQUENCE.index(target_os)
            if target_index < source_index and source_os != "evolution":
                rework = True
            elif not args.force:
                raise RuntimeError(f"No permitted direct transition {source_os}->{target_os}. Use the normal sequence or --force with an explicit reason.")
        first_target_stage = routing["os_stages"][target_os][0]
        if source_os == "evolution" and target_os != "evolution" and not args.force:
            latest_learning = state.get("learning", [])[-1] if state.get("learning") else None
            if not latest_learning:
                raise RuntimeError("Evolution re-entry requires a recorded learning decision")
            if latest_learning.get("route_os") != target_os or latest_learning.get("route_stage") != target_stage:
                raise RuntimeError(
                    "Evolution re-entry target must match the latest learning decision "
                    f"({latest_learning.get('route_os')}/{latest_learning.get('route_stage')})"
                )
            rework = True
        elif target_stage != first_target_stage and not args.force and not rework:
            raise RuntimeError(
                f"Cross-OS handoff must enter {target_os}/{first_target_stage}; "
                "a later stage requires an approved --force transition."
            )
    if gate_name:
        allowed, gate_result = gate_allows_transition(state, gate_name, root)
        if not allowed and not args.force:
            raise RuntimeError(
                f"Gate `{gate_name}` failed: missing={gate_result['missing_artifacts']}, "
                f"invalid={len(gate_result.get('invalid_artifacts', []))}, "
                f"evidence_shortfall={gate_result.get('evidence_shortfall')}, "
                f"critical_risks={gate_result['blocking_critical_risks']}"
            )

    stamp = now()
    if target_os != source_os:
        state["os_states"][source_os]["status"] = "pending" if rework else "completed"
        state["os_states"][target_os]["status"] = "active"
    state["os_states"][target_os]["stage"] = target_stage
    state["os_states"][target_os].setdefault("history", []).append({"stage": target_stage, "at": stamp, "reason": args.reason, "from": f"{source_os}/{source_stage}"})
    state["current_os"] = target_os
    state["current_stage"] = target_stage
    state["history"].append({
        "event": "transition",
        "at": stamp,
        "from_os": source_os,
        "from_stage": source_stage,
        "to_os": target_os,
        "to_stage": target_stage,
        "reason": args.reason,
        "gate": gate_name,
        "gate_status": gate_result.get("status") if gate_result else None,
        "forced": bool(args.force),
        "approver": args.approver if args.force else None,
        "approval_id": args.approval_id if args.force else None,
        "rework": rework,
    })
    save_state(root, state)
    print(f"Transitioned: {source_os}/{source_stage} -> {target_os}/{target_stage}")
    if gate_name:
        print(f"Gate: {gate_name} ({gate_result.get('status') if gate_result else 'forced'})")
    return 0


def normalize_path(root: Path, value: str) -> str:
    if is_uri(value):
        return value
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (root / path).resolve()
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def cmd_add_artifact(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    governance = effective_governance(state, root)
    profile = str(governance["profile"])
    criticality = str(governance["criticality"])
    if args.status not in ARTIFACT_STATUSES:
        raise RuntimeError(f"Invalid artifact status: {args.status}")
    artifact_id = args.id or uid("art")
    if artifact_id not in state.get("artifacts", {}) and artifact_id in all_record_ids(state):
        raise RuntimeError(f"Record id already exists outside artifacts: {artifact_id}")
    previous = state["artifacts"].get(artifact_id, {})
    current_work = active_work_id(state)
    if previous and current_work and str(previous.get("work_item_id", "")) != current_work:
        raise RuntimeError(f"Artifact {artifact_id} belongs to a different scope/work item; create a new artifact id")
    stamp = now()
    verified_by = args.verified_by or previous.get("verified_by", "")
    normalized_path = normalize_path(root, args.path)
    integrity: Dict[str, Any] = {}
    if args.status == "accepted":
        integrity = record_artifact_integrity(
            root,
            args.path,
            args.checksum or "",
            args.type,
            profile,
            criticality,
            args.owner,
            verified_by,
        )
    item = {
        "id": artifact_id,
        "type": args.type,
        "path": normalized_path,
        "status": args.status,
        "owner": args.owner,
        "description": args.description or previous.get("description", ""),
        "created_at": previous.get("created_at", stamp),
        "updated_at": stamp,
        "accepted_at": stamp if args.status == "accepted" else previous.get("accepted_at", ""),
        "verified_by": verified_by,
        **work_scope_fields(state),
        **integrity,
    }
    if args.status == "accepted":
        item.update({"stale": False, "stale_from": [], "stale_at": "", "stale_reason": ""})
    state["artifacts"][artifact_id] = item
    changed_after_acceptance = bool(previous) and previous.get("status") == "accepted" and (
        args.status != "accepted"
        or previous.get("content_hash") != item.get("content_hash")
        or previous.get("type") != item.get("type")
        or previous.get("path") != item.get("path")
    )
    affected = mark_downstream_stale(
        state,
        [artifact_id],
        f"Upstream artifact {artifact_id} changed after acceptance",
    ) if changed_after_acceptance else []
    state["history"].append({
        "event": "artifact-upserted",
        "at": stamp,
        "artifact": artifact_id,
        "type": args.type,
        "status": args.status,
        "downstream_marked_stale": affected,
    })
    save_state(root, state)
    print(f"Artifact {artifact_id}: {args.type} [{args.status}]")
    return 0


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value or "artifact"


def safe_artifact_destination(root: Path, filename: str) -> Path:
    base = (root / ".sdlc" / "artifacts").resolve()
    value = Path(filename)
    if value.is_absolute():
        raise RuntimeError("Artifact filename must be relative")
    target = (base / value).resolve()
    if target != base and base not in target.parents:
        raise RuntimeError("Artifact filename escapes .sdlc/artifacts")
    if target == base:
        raise RuntimeError("Artifact filename must name a file")
    return target


def cmd_new_artifact(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    governance = effective_governance(state, root)
    profile = str(governance["profile"])
    criticality = str(governance["criticality"])
    filename = args.filename or f"{slugify(args.type)}.md"
    path = safe_artifact_destination(root, filename)
    if path.exists() and not args.force:
        raise RuntimeError(f"Artifact file exists: {path}. Use --force to replace.")
    title = args.title or args.type.replace("-", " ").title()
    content = f"""# {title}

- Artifact type: `{args.type}`
- Status: `{args.status}`
- Owner: {args.owner}
- Created: {now()}

## Decision or objective

State what this artifact is intended to decide or enable.

## Facts and evidence

Record verifiable facts with sources.

## Inferences

Record interpretations derived from the evidence.

## Assumptions and unknowns

Record unverified claims and how they will be tested.

## Specification or result

Provide the domain-specific content.

## Risks and edge cases

Record failure modes, constraints and unresolved risks.

## Acceptance criteria

Define observable conditions for acceptance.

## Traceability

Link upstream intent and downstream implementation, tests, release or metrics.
"""
    write_text(path, content)
    artifact_id = args.id or uid("art")
    ensure_new_id(state, artifact_id)
    integrity: Dict[str, Any] = {}
    if args.status == "accepted":
        integrity = record_artifact_integrity(
            root,
            str(path),
            args.checksum or "",
            args.type,
            profile,
            criticality,
            args.owner,
            args.verified_by or "",
        )
    state["artifacts"][artifact_id] = {
        "id": artifact_id,
        "type": args.type,
        "path": str(path.relative_to(root)),
        "status": args.status,
        "owner": args.owner,
        "description": args.description or "",
        "created_at": now(),
        "updated_at": now(),
        "accepted_at": now() if args.status == "accepted" else "",
        "verified_by": args.verified_by or "",
        **work_scope_fields(state),
        "stale": False,
        "stale_from": [],
        "stale_at": "",
        "stale_reason": "",
        **integrity,
    }
    save_state(root, state)
    print(f"Created {path}")
    print(f"Registered artifact {artifact_id}")
    return 0


def split_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def all_record_ids(state: Dict[str, Any]) -> set[str]:
    ids = {str(x) for x in state.get("artifacts", {}).keys()}
    ids.update(str(x) for x in state.get("work_items", {}).keys())
    for key in ["evidence", "assumptions", "decisions", "risks", "traceability", "learning", "routing_log", "runs"]:
        for item in state.get(key, []):
            if isinstance(item, dict) and item.get("id"):
                ids.add(str(item["id"]))
    return ids


def ensure_new_id(state: Dict[str, Any], item_id: str) -> None:
    if item_id in all_record_ids(state):
        raise RuntimeError(f"Record id already exists: {item_id}")


def cmd_add_evidence(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    if args.quality not in QUALITY_ORDER:
        raise RuntimeError(f"Invalid quality: {args.quality}")
    if args.source_type not in EVIDENCE_SOURCE_TYPES:
        raise RuntimeError(f"Invalid source type: {args.source_type}")
    if args.observed_at and parse_time(args.observed_at) is None:
        raise RuntimeError("--observed-at must be an ISO-8601 timestamp")
    if args.expires_at and parse_time(args.expires_at) is None:
        raise RuntimeError("--expires-at must be an ISO-8601 timestamp")
    item_id = args.id or uid("ev")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "claim": args.claim,
        "source": args.source,
        "source_type": args.source_type,
        "quality": args.quality,
        "supports": split_csv(args.supports),
        "method": args.method or "",
        "limitations": args.limitations or "",
        "observed_at": args.observed_at or now(),
        "expires_at": args.expires_at or "",
        **work_scope_fields(state),
        "created_at": now(),
    }
    state["evidence"].append(item)
    save_state(root, state)
    print(f"Evidence {item['id']} added [{item['quality']}]")
    return 0


def cmd_add_assumption(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    item_id = args.id or uid("asm")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "text": args.text,
        "risk": args.risk,
        "status": args.status,
        "owner": args.owner,
        "test": args.test or "",
        **work_scope_fields(state),
        "created_at": now(),
        "updated_at": now(),
    }
    state["assumptions"].append(item)
    save_state(root, state)
    print(f"Assumption {item['id']} added")
    return 0


def cmd_add_decision(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    item_id = args.id or uid("dec")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "title": args.title,
        "choice": args.choice,
        "rationale": args.rationale,
        "owner": args.owner,
        "alternatives": split_csv(args.alternatives),
        "evidence": split_csv(args.evidence),
        **work_scope_fields(state),
        "created_at": now(),
    }
    state["decisions"].append(item)
    save_state(root, state)
    print(f"Decision {item['id']} recorded")
    return 0


def cmd_add_risk(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    if args.severity not in RISK_SEVERITIES:
        raise RuntimeError(f"Invalid severity: {args.severity}")
    item_id = args.id or uid("risk")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "title": args.title,
        "severity": args.severity,
        "likelihood": args.likelihood,
        "status": args.status,
        "mitigation": args.mitigation,
        "owner": args.owner,
        "trigger": args.trigger or "",
        **work_scope_fields(state),
        "created_at": now(),
        "updated_at": now(),
    }
    state["risks"].append(item)
    save_state(root, state)
    print(f"Risk {item['id']} added [{item['severity']}/{item['status']}]")
    return 0


def cmd_update_risk(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    risk = next((item for item in state.get("risks", []) if item.get("id") == args.id), None)
    if risk is None:
        raise RuntimeError(f"Risk not found: {args.id}")
    changes = {
        "title": args.title,
        "severity": args.severity,
        "likelihood": args.likelihood,
        "status": args.status,
        "mitigation": args.mitigation,
        "owner": args.owner,
        "trigger": args.trigger,
    }
    updates = {key: value for key, value in changes.items() if value is not None}
    if not updates:
        raise RuntimeError("update-risk requires at least one field to change")
    before = {key: risk.get(key) for key in updates}
    risk.update(updates)
    risk["updated_at"] = now()
    state.setdefault("history", []).append({
        "event": "risk-updated",
        "at": risk["updated_at"],
        "id": args.id,
        "before": before,
        "after": updates,
    })
    save_state(root, state)
    print(f"Risk {args.id} updated [{risk.get('severity')}/{risk.get('status')}]")
    return 0



def cmd_trace(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    item_id = args.id or uid("trace")
    ensure_new_id(state, item_id)
    source = str(args.from_id or "").strip()
    target = str(args.to_id or "").strip()
    relation = str(args.relation or "").strip()
    if source == target:
        raise RuntimeError("Trace endpoints must be different")
    if relation not in TRACE_RELATIONS:
        raise RuntimeError(f"Invalid trace relation: {relation}. Valid: {', '.join(sorted(TRACE_RELATIONS))}")
    if not trace_endpoint_valid(state, source):
        raise RuntimeError(f"Invalid trace source endpoint: {source}")
    if not trace_endpoint_valid(state, target):
        raise RuntimeError(f"Invalid trace target endpoint: {target}")
    evidence_ids = split_csv(args.evidence)
    known_evidence = {str(item.get("id")) for item in state.get("evidence", []) if isinstance(item, dict)}
    unknown_evidence = [item for item in evidence_ids if item not in known_evidence]
    if unknown_evidence:
        raise RuntimeError("Trace references unknown evidence: " + ", ".join(unknown_evidence))
    for edge in state.get("traceability", []):
        if (
            isinstance(edge, dict)
            and str(edge.get("from")) == source
            and str(edge.get("relation")) == relation
            and str(edge.get("to")) == target
        ):
            raise RuntimeError(f"Duplicate trace edge: {source} -[{relation}]-> {target}")
    item = {
        "id": item_id,
        "from": source,
        "to": target,
        "relation": relation,
        "evidence": evidence_ids,
        **work_scope_fields(state),
        "created_at": now(),
    }
    state["traceability"].append(item)
    if source in state.get("artifacts", {}) and target in state.get("artifacts", {}):
        source_item = state["artifacts"][source]
        target_item = state["artifacts"][target]
        if target_item.get("status") == "accepted":
            source_governance = governance_for_record(state, root, source_item)
            source_check = inspect_artifact(
                root,
                source_item,
                int(load_config(root).get("gate_artifact_min_bytes", 64)),
                str(source_governance["profile"]),
                str(source_governance["criticality"]),
            )
            if not source_check.get("valid"):
                target_item["stale"] = True
                target_item["stale_from"] = sorted(set(target_item.get("stale_from", [])) | {source})
                target_item["stale_at"] = now()
                target_item["stale_reason"] = f"Trace added from invalid upstream artifact {source}"
    state.setdefault("history", []).append({"event": "trace-added", "at": item["created_at"], "id": item_id})
    save_state(root, state, "trace-added")
    print(f"Trace {item['id']}: {item['from']} -[{item['relation']}]-> {item['to']}")
    return 0


def project_metrics(state: Dict[str, Any], root: Path) -> Dict[str, Any]:
    runs = [x for x in state.get("runs", []) if isinstance(x, dict)]
    transitions = [
        x for x in state.get("history", [])
        if isinstance(x, dict) and x.get("event") == "transition"
    ]
    gate_outcomes = [
        outcome
        for outcomes in state.get("gates", {}).values()
        if isinstance(outcomes, list)
        for outcome in outcomes
        if isinstance(outcome, dict)
    ]
    total_tokens = sum(int(x.get("tokens_input", 0)) + int(x.get("tokens_output", 0)) for x in runs)
    total_cost = round(sum(float(x.get("cost_usd", 0.0)) for x in runs), 6)
    total_duration = sum(int(x.get("duration_ms", 0)) for x in runs)
    stale_artifacts = sorted(
        str(item.get("id")) for item in state.get("artifacts", {}).values()
        if isinstance(item, dict) and item.get("status") == "accepted" and item.get("stale")
    )
    evidence = [x for x in state.get("evidence", []) if isinstance(x, dict)]
    high_quality = [x for x in evidence if x.get("quality") == "high"]
    config = load_config(root)
    cost_budget = config.get("cost_budget_usd")
    token_budget = config.get("token_budget")
    warnings: List[str] = []
    if cost_budget not in {None, ""} and total_cost > float(cost_budget):
        warnings.append(f"Cost budget exceeded: {total_cost} > {float(cost_budget)}")
    if token_budget not in {None, ""} and total_tokens > int(token_budget):
        warnings.append(f"Token budget exceeded: {total_tokens} > {int(token_budget)}")
    return {
        "runs": len(runs),
        "successful_runs": sum(1 for x in runs if x.get("outcome") == "success"),
        "run_success_rate": round(
            sum(1 for x in runs if x.get("outcome") == "success") / len(runs), 4
        ) if runs else None,
        "tokens": total_tokens,
        "tool_calls": sum(int(x.get("tool_calls", 0)) for x in runs),
        "cost_usd": total_cost,
        "human_hours": round(sum(float(x.get("human_hours", 0.0)) for x in runs), 4),
        "average_duration_ms": round(total_duration / len(runs), 2) if runs else None,
        "transitions": len(transitions),
        "rework_transitions": sum(1 for x in transitions if x.get("rework")),
        "forced_transitions": sum(1 for x in transitions if x.get("forced")),
        "gate_passes": sum(1 for x in gate_outcomes if x.get("status") == "pass"),
        "gate_failures": sum(1 for x in gate_outcomes if x.get("status") == "fail"),
        "gate_waivers": sum(1 for x in gate_outcomes if x.get("status") == "waived"),
        "accepted_artifacts": sum(
            1 for x in state.get("artifacts", {}).values()
            if isinstance(x, dict) and x.get("status") == "accepted"
        ),
        "stale_artifacts": stale_artifacts,
        "high_quality_evidence_ratio": round(len(high_quality) / len(evidence), 4) if evidence else None,
        "warnings": warnings,
    }


def cmd_record_run(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    numeric = {
        "duration_ms": args.duration_ms,
        "tokens_input": args.tokens_input,
        "tokens_output": args.tokens_output,
        "tool_calls": args.tool_calls,
        "cost_usd": args.cost_usd,
        "human_hours": args.human_hours,
    }
    if any(float(value) < 0 for value in numeric.values()):
        raise RuntimeError("Run metrics cannot be negative")
    config = load_config(root)
    current_metrics = project_metrics(state, root)
    projected_cost = float(current_metrics.get("cost_usd", 0.0)) + float(args.cost_usd)
    projected_tokens = int(current_metrics.get("tokens", 0)) + int(args.tokens_input) + int(args.tokens_output)
    if bool(config.get("budget_hard_enforcement", False)):
        if config.get("cost_budget_usd") not in {None, ""} and projected_cost > float(config["cost_budget_usd"]):
            raise RuntimeError(f"Cost budget would be exceeded: {projected_cost} > {config['cost_budget_usd']}")
        if config.get("token_budget") not in {None, ""} and projected_tokens > int(config["token_budget"]):
            raise RuntimeError(f"Token budget would be exceeded: {projected_tokens} > {config['token_budget']}")
    item_id = args.id or uid("run")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "actor": args.actor,
        "os": args.os,
        "skill": args.skill,
        "model": args.model,
        "outcome": args.outcome,
        "duration_ms": int(args.duration_ms),
        "tokens_input": int(args.tokens_input),
        "tokens_output": int(args.tokens_output),
        "tool_calls": int(args.tool_calls),
        "cost_usd": round(float(args.cost_usd), 6),
        "human_hours": round(float(args.human_hours), 4),
        "artifacts": split_csv(args.artifacts),
        "notes": args.notes or "",
        **work_scope_fields(state),
        "created_at": now(),
    }
    state.setdefault("runs", []).append(item)
    state.setdefault("history", []).append({
        "event": "agent-run-recorded", "at": item["created_at"], "id": item_id,
        "outcome": item["outcome"], "os": item["os"], "skill": item["skill"],
    })
    save_state(root, state, "agent-run-recorded")
    print(f"Run {item_id} recorded [{item['outcome']}] cost=${item['cost_usd']:.6f}")
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    payload = project_metrics(state, root)
    text = (
        f"Runs: {payload['runs']}\n"
        f"Tokens: {payload['tokens']}\n"
        f"Tool calls: {payload['tool_calls']}\n"
        f"Cost USD: {payload['cost_usd']}\n"
        f"Rework/forced: {payload['rework_transitions']}/{payload['forced_transitions']}\n"
        f"Stale artifacts: {len(payload['stale_artifacts'])}"
    )
    if payload["warnings"]:
        text += "\nWarnings: " + "; ".join(payload["warnings"])
    print_json_or_text(payload, args.json, text)
    return 0


def cmd_quality(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    minimum = int(load_config(root).get("gate_artifact_min_bytes", 64))
    governance = effective_governance(state, root)
    items: List[Dict[str, Any]] = []
    for artifact_id, item in state.get("artifacts", {}).items():
        if not isinstance(item, dict) or (not args.all and item.get("status") != "accepted"):
            continue
        item_governance = governance_for_record(state, root, item)
        inspection = inspect_artifact(
            root, item, minimum, str(item_governance["profile"]), str(item_governance["criticality"])
        )
        inspection["status"] = item.get("status")
        inspection["scope"] = item.get("scope", "legacy")
        inspection["work_item_id"] = item.get("work_item_id", "")
        inspection["governance_profile"] = item_governance["profile"]
        inspection["governance_criticality"] = item_governance["criticality"]
        items.append(inspection)
    payload = {
        "profile": governance["profile"],
        "criticality": governance["criticality"],
        "project_profile": process_profile(state, root),
        "artifacts": items,
        "valid": sum(1 for x in items if x.get("valid")),
        "invalid": sum(1 for x in items if not x.get("valid")),
        "average_quality_score": round(
            sum(float(x.get("quality_score") or 0.0) for x in items) / len(items), 4
        ) if items else None,
    }
    text = (
        f"Artifacts: {len(items)}\nValid: {payload['valid']}\nInvalid: {payload['invalid']}\n"
        f"Average quality: {payload['average_quality_score']}"
    )
    print_json_or_text(payload, args.json, text)
    return 0 if payload["invalid"] == 0 else 2


def cmd_impact(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    source_ids = split_csv(args.artifact_id)
    missing = [x for x in source_ids if x not in state.get("artifacts", {})]
    if missing:
        raise RuntimeError("Unknown artifact IDs: " + ", ".join(missing))
    descendants = sorted(downstream_artifact_ids(state, source_ids))
    payload = {
        "sources": source_ids,
        "descendants": descendants,
        "affected_gates": affected_gates_for_artifacts(state, [*source_ids, *descendants]),
    }
    text = (
        f"Sources: {', '.join(source_ids)}\n"
        f"Downstream artifacts: {', '.join(descendants) if descendants else 'None'}\n"
        f"Affected gates: {', '.join(payload['affected_gates']) if payload['affected_gates'] else 'None'}"
    )
    print_json_or_text(payload, args.json, text)
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    minimum = int(load_config(root).get("gate_artifact_min_bytes", 64))
    inspections = accepted_artifact_inspections(state, root, minimum)
    direct_invalid = {
        artifact_id: inspection
        for artifact_id, inspection in inspections.items()
        if not inspection.get("valid")
    }
    descendants = sorted(downstream_artifact_ids(state, direct_invalid.keys()))
    if args.apply and direct_invalid:
        stamp = now()
        for artifact_id, inspection in direct_invalid.items():
            item = state.get("artifacts", {}).get(artifact_id)
            if not isinstance(item, dict):
                continue
            item["stale"] = True
            item["stale_from"] = sorted(set(item.get("stale_from", [])) | {artifact_id})
            item["stale_at"] = stamp
            item["stale_reason"] = "Reconcile detected: " + ", ".join(inspection.get("issues", []))
        affected = mark_downstream_stale(
            state, direct_invalid.keys(), "Upstream integrity or quality drift detected during reconcile"
        )
        state.setdefault("history", []).append({
            "event": "artifacts-reconciled", "at": stamp,
            "direct_invalid": sorted(direct_invalid), "downstream_stale": affected,
        })
        save_state(root, state, "artifacts-reconciled")
    payload = {
        "direct_invalid": direct_invalid,
        "downstream": descendants,
        "applied": bool(args.apply),
    }
    text = (
        f"Direct invalid: {len(direct_invalid)}\n"
        f"Downstream affected: {len(descendants)}\n"
        f"Applied: {'yes' if args.apply else 'no'}"
    )
    print_json_or_text(payload, args.json, text)
    return 0 if not direct_invalid else 2


def gate_report_markdown(result: Dict[str, Any]) -> str:
    lines = [
        f"# Gate: {result['gate']}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- Checked: {result.get('checked_at')}",
        f"- Profile: {result.get('profile')}",
        f"- Criticality: {result.get('criticality')}",
        f"- Purpose: {result.get('purpose')}",
        "",
        "## Missing artifacts",
        "",
    ]
    lines.extend([f"- `{x}`" for x in result.get("missing_artifacts", [])] or ["- None"])
    lines.extend(["", "## Invalid artifacts", ""])
    invalid = result.get("invalid_artifacts", [])
    lines.extend(
        [
            f"- `{x.get('id')}`: {', '.join(x.get('issues', []))} "
            f"(quality={x.get('quality_score')}, threshold={x.get('quality_threshold')})"
            for x in invalid
        ]
        or ["- None"]
    )
    if result.get("upstream_invalidations"):
        lines.extend(["", "## Upstream invalidations", ""])
        lines.extend([
            f"- `{artifact_id}` depends on invalid upstream: {', '.join(sources)}"
            for artifact_id, sources in result["upstream_invalidations"].items()
        ])
    lines.extend([
        "",
        "## Evidence",
        "",
        f"- Total: {result.get('evidence_count')}",
        f"- Shortfall: {result.get('evidence_shortfall')}",
        f"- High quality: {result.get('high_quality_evidence_count')}",
        f"- High-quality shortfall: {result.get('high_quality_evidence_shortfall')}",
        f"- Distinct sources: {result.get('distinct_source_count')}",
        f"- Distinct-source shortfall: {result.get('distinct_source_shortfall')}",
        f"- Covered evidence targets: {result.get('evidence_target_count')}",
        f"- Evidence-target shortfall: {result.get('evidence_target_shortfall')}",
        f"- Duplicate evidence excluded: {len(result.get('duplicate_evidence', []))}",
        "",
        "## Traceability",
        "",
        f"- Artifact coverage: {result.get('trace_coverage')}",
        f"- Required artifact coverage: {result.get('minimum_trace_coverage')}",
        f"- Directed path coverage: {result.get('trace_path_coverage')}",
        f"- Required path coverage: {result.get('minimum_trace_path_coverage')}",
        "",
        "### Required directed paths",
        "",
    ])
    for item in result.get("trace_path_results", []):
        status = "PASS" if item.get("passed") else "FAIL"
        lines.append(f"- **{status}**: `{' → '.join(item.get('path', []))}`")
    if not result.get("trace_path_results"):
        lines.append("- None")
    lines.extend(["", "## Blocking critical risks", ""])
    lines.extend([f"- `{x}`" for x in result.get("blocking_critical_risks", [])] or ["- None"])
    if result.get("waiver"):
        waiver = result["waiver"]
        lines.extend([
            "", "## Waiver", "",
            f"- Approver: {waiver.get('approver')}",
            f"- Approval ID: {waiver.get('approval_id')}",
            f"- Reason: {waiver.get('reason')}",
            f"- Compensating control: {waiver.get('compensating_control')}",
            f"- Expires: {waiver.get('expires')}",
        ])
    return "\n".join(lines)

def cmd_gate(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    config = load_config(root)
    result = assess_gate(state, args.name, root=root)
    if args.waive:
        if not bool(config.get("allow_waiver", True)):
            raise RuntimeError("Gate waivers are disabled by .sdlc/config.json")
        if result["status"] == "pass":
            raise RuntimeError("Gate already passes; a waiver is unnecessary")
        if result.get("blocking_critical_risks"):
            raise RuntimeError("Open critical risks are non-waivable; mitigate or formally close them first")
        if not args.reason or not args.approver or not args.approval_id or not args.compensating_control or not args.expires:
            raise RuntimeError(
                "Waiver requires --reason, --approver, --approval-id, --compensating-control and --expires"
            )
        require_human_approval(args.approver, args.approval_id, "Gate waiver")
        expiry = parse_time(args.expires)
        current = datetime.now(timezone.utc)
        if expiry is None or expiry <= current:
            raise RuntimeError("Waiver expiry must be a valid future ISO-8601 timestamp")
        max_days = int(config.get("max_waiver_days", 14))
        if (expiry - current).total_seconds() > max_days * 86400:
            raise RuntimeError(f"Waiver expiry exceeds configured maximum of {max_days} days")
        waiver = {
            **result,
            "status": "waived",
            "reason": args.reason,
            "approver": args.approver,
            "approval_id": args.approval_id,
            "compensating_control": args.compensating_control,
            "expires": args.expires,
            "created_at": now(),
        }
        state.setdefault("gates", {}).setdefault(args.name, []).append(waiver)
        result = waiver
    else:
        state.setdefault("gates", {}).setdefault(args.name, []).append(result)
    save_state(root, state)
    write_text(root / ".sdlc" / "gates" / f"{args.name}.md", gate_report_markdown(result))
    text = f"Gate {args.name}: {result['status'].upper()}"
    if result.get("missing_artifacts"):
        text += "\nMissing: " + ", ".join(result["missing_artifacts"])
    if result.get("blocking_critical_risks"):
        text += "\nCritical risks: " + ", ".join(result["blocking_critical_risks"])
    print_json_or_text(result, args.json, text)
    return 0 if result["status"] in {"pass", "waived"} else 2


def cmd_learn(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    routing = load_json(find_manifest("os-routing.json"))
    route_stage = validate_stage(args.route_os, args.route_stage or routing["os_stages"][args.route_os][0], routing)
    item_id = args.id or uid("learn")
    ensure_new_id(state, item_id)
    item = {
        "id": item_id,
        "expected": args.expected,
        "actual": args.actual,
        "gap": args.gap,
        "gap_type": args.gap_type,
        "decision": args.decision,
        "route_os": args.route_os,
        "route_stage": route_stage,
        "evidence": split_csv(args.evidence),
        **work_scope_fields(state),
        "created_at": now(),
    }
    state["learning"].append(item)
    state["history"].append({"event": "learning-decision", "at": item["created_at"], "id": item["id"], "route_os": item["route_os"], "route_stage": item["route_stage"]})
    save_state(root, state)
    print(f"Learning {item['id']} recorded; route to {item['route_os']}/{item['route_stage']}")
    return 0



def cmd_migrate(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    old_version = str(state.get("version", "unknown"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    migration_dir = root / ".sdlc" / "migrations"
    migration_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(state_path(root), migration_dir / f"state-before-{old_version}-{stamp}.json")

    existing_audit = audit_log_path(root)
    if existing_audit.exists():
        try:
            audit_errors = validate_audit_chain(root, state)
        except RuntimeError as exc:
            audit_errors = [str(exc)]
        if audit_errors:
            shutil.move(str(existing_audit), str(migration_dir / f"audit-before-{stamp}.jsonl"))

    criticality = str(state.get("project", {}).get("criticality", "medium"))
    profile = args.profile or str(state.get("project", {}).get("profile", "")).strip()
    if not profile:
        profile = {"low": "lite", "medium": "standard", "high": "high-assurance"}.get(criticality, "standard")
    if profile not in PROCESS_PROFILES:
        raise RuntimeError(f"Invalid process profile: {profile}")
    if criticality == "high" and profile == "lite":
        raise RuntimeError("High-criticality projects cannot use the lite process profile")

    state["version"] = VERSION
    state["revision"] = int(state.get("revision", 0))
    state.setdefault("project", {})["profile"] = profile
    state["project"]["root"] = str(root)
    defaults = {
        "history": [], "artifacts": {}, "evidence": [], "assumptions": [], "decisions": [],
        "risks": [], "traceability": [], "gates": {}, "learning": [], "routing_log": [], "runs": [],
        "work_items": {}, "active_work_id": "",
    }
    for key, value in defaults.items():
        state.setdefault(key, value)
    if old_version != VERSION:
        for item in state.get("artifacts", {}).values():
            if isinstance(item, dict) and "scope" not in item:
                item.update({"scope": "legacy", "work_item_id": ""})
        for collection_name in ["evidence", "assumptions", "decisions", "risks", "traceability", "learning", "runs"]:
            for item in state.get(collection_name, []):
                if isinstance(item, dict) and "scope" not in item:
                    item.update({"scope": "legacy", "work_item_id": ""})
    state.setdefault("history", []).append({
        "event": "state-migrated",
        "at": now(),
        "from_version": old_version,
        "to_version": VERSION,
        "profile": profile,
    })

    config_path = root / ".sdlc" / "config.json"
    try:
        config = load_config(root)
    except RuntimeError:
        config = {}
    config.update({
        "schema_version": VERSION,
        "process_profile": profile,
        "audit_chain": True,
        "artifact_contract_enforcement": True,
        "independent_verification": "risk-based",
        "cost_budget_usd": config.get("cost_budget_usd"),
        "token_budget": config.get("token_budget"),
        "stage_policy": config.get("stage_policy", "adjacent"),
        "gate_policy": config.get("gate_policy", "strict"),
    })
    atomic_write_json(config_path, config)
    save_state(root, state, "state-migrated")
    print(f"Migrated {old_version} -> {VERSION}; profile={profile}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    errors = validate_audit_chain(root, state)
    events = read_audit_events(root) if not errors else []
    payload = {"valid": not errors, "events": len(events), "errors": errors}
    text = f"Audit chain valid: {'yes' if not errors else 'no'}\nEvents: {len(events)}"
    if errors:
        text += "\n" + "\n".join(f"ERROR: {item}" for item in errors)
    print_json_or_text(payload, args.json, text)
    return 0 if not errors else 2


def _clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 1)


def assess_health(root: Path, state: Dict[str, Any]) -> Dict[str, Any]:
    errors, warnings = validation_errors(root, state)
    config = load_config(root)
    minimum_bytes = int(config.get("gate_artifact_min_bytes", 64))
    accepted = [
        item for item in state.get("artifacts", {}).values()
        if isinstance(item, dict) and item.get("status") == "accepted"
    ]
    profile = process_profile(state, root)
    criticality = str(state.get("project", {}).get("criticality", "medium"))
    inspections = []
    for item in accepted:
        item_governance = governance_for_record(state, root, item)
        inspections.append(inspect_artifact(
            root, item, minimum_bytes, str(item_governance["profile"]), str(item_governance["criticality"])
        ))
    valid_accepted = [x for x in inspections if x.get("valid")]

    state_integrity = _clamp_score(100 - 20 * len(errors) - 3 * len(warnings))
    artifact_integrity = _clamp_score(100 * len(valid_accepted) / len(inspections)) if inspections else 40.0
    content_quality = _clamp_score(
        100 * sum(float(x.get("quality_score") or 0.0) for x in inspections) / len(inspections)
    ) if inspections else 40.0
    execution_metrics = project_metrics(state, root)
    execution_economics = 100.0
    if not state.get("runs"):
        execution_economics = 60.0
    if execution_metrics.get("warnings"):
        execution_economics = max(0.0, 50.0 - 20.0 * len(execution_metrics["warnings"]))

    valid_evidence: List[Dict[str, Any]] = []
    seen_keys: set[Tuple[str, str, Tuple[str, ...]]] = set()
    current_time = datetime.now(timezone.utc)
    for item in state.get("evidence", []):
        if not isinstance(item, dict):
            continue
        expiry = parse_time(str(item.get("expires_at", "")))
        key = normalized_evidence_key(item)
        if (
            str(item.get("claim", "")).strip()
            and str(item.get("source", "")).strip()
            and item.get("quality") in QUALITY_ORDER
            and item.get("source_type", "other") in EVIDENCE_SOURCE_TYPES
            and not (expiry and expiry <= current_time)
            and key not in seen_keys
        ):
            seen_keys.add(key)
            valid_evidence.append(item)
    high_quality = [
        x for x in valid_evidence
        if x.get("quality") == "high" and x.get("source_type") in HIGH_QUALITY_SOURCE_TYPES
    ]
    distinct_sources = {str(x.get("source", "")).strip().lower() for x in valid_evidence}
    evidence_quality = _clamp_score(
        min(50.0, len(valid_evidence) * 8.0)
        + min(30.0, len(high_quality) * 12.0)
        + min(20.0, len(distinct_sources) * 5.0)
    )

    valid_ids = {str(x.get("id")) for x in accepted if any(y.get("id") == x.get("id") and y.get("valid") for y in inspections)}
    traced_ids: set[str] = set()
    for edge in state.get("traceability", []):
        if not isinstance(edge, dict) or edge.get("relation") not in TRACE_FORWARD_RELATIONS:
            continue
        source, target = str(edge.get("from", "")), str(edge.get("to", ""))
        if source in valid_ids:
            traced_ids.add(source)
        if target in valid_ids:
            traced_ids.add(target)
    basic_trace = 100 * len(traced_ids) / len(valid_ids) if valid_ids else 0.0

    next_step = next_recommendation(state, root)
    gate_result = next_step.get("result") if isinstance(next_step, dict) else None
    if isinstance(gate_result, dict):
        path_trace = 100 * float(gate_result.get("trace_path_coverage", 0.0))
        required_count = max(1, len(gate_result.get("required", [])))
        artifact_ready = 100 * (required_count - len(gate_result.get("missing_artifacts", []))) / required_count
        evidence_requirements = [
            int(gate_result.get("evidence_shortfall", 0)),
            int(gate_result.get("high_quality_evidence_shortfall", 0)),
            int(gate_result.get("distinct_source_shortfall", 0)),
            int(gate_result.get("evidence_target_shortfall", 0)),
        ]
        evidence_ready = max(0.0, 100.0 - 20.0 * sum(evidence_requirements))
        gate_readiness = _clamp_score(0.45 * artifact_ready + 0.30 * evidence_ready + 0.25 * path_trace)
    else:
        path_trace = basic_trace
        gate_readiness = 65.0
    traceability = _clamp_score(0.4 * basic_trace + 0.6 * path_trace)

    penalties = {"critical": 100, "high": 25, "medium": 10, "low": 5}
    open_risks = [
        x for x in state.get("risks", [])
        if isinstance(x, dict) and x.get("status") in OPEN_RISK_STATUSES
    ]
    risk_control = _clamp_score(100 - sum(penalties.get(str(x.get("severity")), 10) for x in open_risks))

    routing = load_json(find_manifest("os-routing.json"))
    os_name = str(state.get("current_os", "pm"))
    stage = str(state.get("current_stage", "INTAKE"))
    os_index = OS_SEQUENCE.index(os_name) if os_name in OS_SEQUENCE else 0
    stages = effective_stages(state, root, os_name, routing) if os_name in routing.get("os_stages", {}) else [stage]
    if stage not in stages:
        stages = routing.get("os_stages", {}).get(os_name, [stage])
    stage_index = stages.index(stage) if stage in stages else 0
    lifecycle_progress = _clamp_score(
        100 * (os_index + stage_index / max(1, len(stages))) / max(1, len(OS_SEQUENCE))
    )

    dimensions = {
        "state_integrity": state_integrity,
        "artifact_integrity": artifact_integrity,
        "content_quality": content_quality,
        "evidence_quality": evidence_quality,
        "traceability": traceability,
        "risk_control": risk_control,
        "gate_readiness": gate_readiness,
        "lifecycle_progress": lifecycle_progress,
        "execution_economics": execution_economics,
    }
    weighted = (
        dimensions["state_integrity"] * 0.17
        + dimensions["artifact_integrity"] * 0.15
        + dimensions["content_quality"] * 0.12
        + dimensions["evidence_quality"] * 0.13
        + dimensions["traceability"] * 0.13
        + dimensions["risk_control"] * 0.13
        + dimensions["gate_readiness"] * 0.09
        + dimensions["lifecycle_progress"] * 0.04
        + dimensions["execution_economics"] * 0.04
    )
    hard_fails: List[str] = []
    if errors:
        hard_fails.append("state-or-audit-integrity")
    if any(not x.get("valid") for x in inspections):
        hard_fails.append("accepted-artifact-integrity")
    if open_critical_risks(state):
        hard_fails.append("open-critical-risk")
    score = _clamp_score(min(weighted, 49.0) if hard_fails else weighted)

    source_types = {str(x.get("source_type")) for x in valid_evidence}
    confidence = _clamp_score(
        min(30.0, len(valid_evidence) * 4.0)
        + min(24.0, len(source_types) * 8.0)
        + min(20.0, len(valid_accepted) * 2.0)
        + min(16.0, len(state.get("traceability", [])) * 2.0)
        + min(10.0, sum(len(x) for x in state.get("gates", {}).values()) * 2.0)
    )
    recommendations: List[str] = []
    if errors:
        recommendations.append("先运行 validate/audit 并修复状态或审计链错误。")
    if artifact_integrity < 100:
        recommendations.append("重新审核并登记被修改、缺失或内容不足的 accepted 制品。")
    if content_quality < 80:
        recommendations.append("补充具体证据、明确决策、可量化验收和制品间追踪，避免只满足模板结构。")
    if evidence_quality < 70:
        recommendations.append("补充直接、独立且可过期管理的用户/遥测/测试证据。")
    if traceability < 80:
        recommendations.append("补齐 Gate 要求的有向追踪路径，而不是只添加孤立连线。")
    if open_critical_risks(state):
        recommendations.append("关闭或缓解所有开放 critical 风险；该项不可被平均分抵消。")
    if execution_metrics.get("warnings"):
        recommendations.append("处理 Agent 成本或 Token 预算超限，再决定是否扩大自动化范围。")
    if not recommendations:
        recommendations.append("进入下一阶段并持续记录实际结果；当前分数不等于真实项目效果已被证明。")
    return {
        "score": score,
        "confidence": confidence,
        "profile": effective_governance(state, root)["profile"],
        "project_profile": process_profile(state, root),
        "dimensions": dimensions,
        "hard_fails": hard_fails,
        "errors": errors,
        "warnings": warnings,
        "execution_metrics": execution_metrics,
        "next": next_step,
        "recommendations": recommendations,
        "interpretation": "启发式控制面健康度；不是产品质量或业务结果的替代指标。",
        "generated_at": now(),
    }


def cmd_health(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    result = assess_health(root, state)
    text = (
        f"Health: {result['score']}/100\n"
        f"Confidence: {result['confidence']}/100\n"
        f"Profile: {result['profile']}\n"
        f"Hard fails: {', '.join(result['hard_fails']) if result['hard_fails'] else 'none'}"
    )
    print_json_or_text(result, args.json, text)
    return 0 if not result["hard_fails"] else 2



def validation_errors(root: Path, state: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    routing = load_json(find_manifest("os-routing.json"))
    try:
        config = load_config(root)
    except RuntimeError as exc:
        errors.append(str(exc))
        config = {}

    required_keys = [
        "version", "revision", "project", "current_os", "current_stage", "status", "os_states",
        "history", "artifacts", "evidence", "assumptions", "decisions", "risks",
        "traceability", "gates", "learning", "routing_log", "runs", "work_items", "active_work_id",
    ]
    for key in required_keys:
        if key not in state:
            errors.append(f"Missing state key: {key}")

    project = state.get("project", {}) if isinstance(state.get("project"), dict) else {}
    if project.get("type") not in PROJECT_TYPES:
        errors.append(f"Invalid project type: {project.get('type')}")
    if project.get("criticality") not in CRITICALITIES:
        errors.append(f"Invalid criticality: {project.get('criticality')}")
    try:
        profile = process_profile(state, root)
    except RuntimeError as exc:
        errors.append(str(exc))
        profile = ""
    state_profile = str(project.get("profile", "")).strip()
    config_profile = str(config.get("process_profile", "")).strip()
    if state_profile not in PROCESS_PROFILES:
        errors.append(f"Invalid project profile: {state_profile}")
    if state_profile and config_profile and state_profile != config_profile:
        errors.append(f"Process profile mismatch: state={state_profile}, config={config_profile}")
    if profile == "lite" and project.get("criticality") == "high":
        errors.append("High-criticality project cannot use lite profile")
    if not isinstance(state.get("revision"), int) or int(state.get("revision", -1)) < 0:
        errors.append(f"Invalid revision: {state.get('revision')}")
    if state.get("status") not in {"active", "blocked", "paused", "closed"}:
        errors.append(f"Invalid project status: {state.get('status')}")
    configured_root = str(project.get("root", "")).strip()
    if configured_root and Path(configured_root).expanduser().resolve() != root.resolve():
        warnings.append(f"Project root moved: state={configured_root}, actual={root}")
    if state.get("version") != VERSION:
        warnings.append(f"State version {state.get('version')} differs from CLI {VERSION}; run migrate")

    work_items = state.get("work_items", {})
    if not isinstance(work_items, dict):
        errors.append("work_items must be an object")
        work_items = {}
    active_id = str(state.get("active_work_id", "") or "")
    if active_id:
        active = work_items.get(active_id)
        if not isinstance(active, dict):
            errors.append(f"active_work_id not found: {active_id}")
        elif active.get("status") != "active":
            errors.append(f"active_work_id is not active: {active_id}")
    active_count = sum(1 for item in work_items.values() if isinstance(item, dict) and item.get("status") == "active")
    if active_count > 1:
        errors.append("More than one active work item")
    for work_id, item in work_items.items():
        if not isinstance(item, dict):
            errors.append(f"Work item {work_id} is not an object")
            continue
        if str(item.get("id", "")) != str(work_id):
            errors.append(f"Work item key/id mismatch: {work_id} != {item.get('id')}")
        if item.get("profile") not in PROCESS_PROFILES:
            errors.append(f"Invalid work profile: {work_id}/{item.get('profile')}")
        if item.get("criticality") not in CRITICALITIES:
            errors.append(f"Invalid work criticality: {work_id}/{item.get('criticality')}")
        if item.get("status") not in {"active", "completed", "cancelled"}:
            errors.append(f"Invalid work status: {work_id}/{item.get('status')}")

    current_os = state.get("current_os")
    current_stage = state.get("current_stage")
    if current_os not in OS_SEQUENCE:
        errors.append(f"Unknown current_os: {current_os}")
    elif current_stage not in routing["os_stages"][current_os]:
        errors.append(f"Invalid current_stage: {current_stage} for {current_os}")

    artifacts = state.get("artifacts", {})
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
        artifacts = {}
    collections = {
        "evidence": state.get("evidence", []),
        "assumptions": state.get("assumptions", []),
        "decisions": state.get("decisions", []),
        "risks": state.get("risks", []),
        "traceability": state.get("traceability", []),
        "learning": state.get("learning", []),
        "runs": state.get("runs", []),
    }
    for name, collection in list(collections.items()):
        if not isinstance(collection, list):
            errors.append(f"{name} must be an array")
            collections[name] = []

    seen: set[str] = set()
    for key, item in artifacts.items():
        if not isinstance(item, dict):
            errors.append(f"Artifact {key} is not an object")
            continue
        item_id = str(item.get("id", ""))
        if not item_id:
            errors.append(f"Artifact {key} has no id")
        elif item_id != str(key):
            errors.append(f"Artifact key/id mismatch: {key} != {item_id}")
        if item_id in seen:
            errors.append(f"Duplicate id: {item_id}")
        seen.add(item_id)
        if item.get("status") not in ARTIFACT_STATUSES:
            errors.append(f"Invalid artifact status: {item_id}/{item.get('status')}")
        artifact_governance = governance_for_record(state, root, item)
        inspection = inspect_artifact(
            root,
            item,
            int(config.get("gate_artifact_min_bytes", 64)),
            str(artifact_governance["profile"]),
            str(artifact_governance["criticality"]),
        )
        if item.get("status") == "accepted" and not inspection["valid"]:
            errors.append(f"Accepted artifact invalid: {item_id} ({', '.join(inspection['issues'])})")
        elif item.get("status") != "accepted" and "path_not_found" in inspection["issues"]:
            warnings.append(f"Artifact path does not exist: {item_id} -> {item.get('path')}")

    for collection in collections.values():
        for item in collection:
            if not isinstance(item, dict):
                errors.append("Ledger entry is not an object")
                continue
            item_id = str(item.get("id", ""))
            if not item_id:
                errors.append("Entry without id")
            elif item_id in seen:
                errors.append(f"Duplicate id: {item_id}")
            else:
                seen.add(item_id)

    for run in collections["runs"]:
        if not isinstance(run, dict):
            continue
        run_id = str(run.get("id", "<missing-id>"))
        if run.get("os") not in OS_SEQUENCE:
            errors.append(f"Invalid run OS: {run_id}/{run.get('os')}")
        if run.get("outcome") not in {"success", "partial", "failed", "aborted"}:
            errors.append(f"Invalid run outcome: {run_id}/{run.get('outcome')}")
        for field in ["duration_ms", "tokens_input", "tokens_output", "tool_calls", "cost_usd"]:
            try:
                value = float(run.get(field, 0))
            except (TypeError, ValueError):
                errors.append(f"Invalid run metric: {run_id}/{field}")
                continue
            if value < 0:
                errors.append(f"Negative run metric: {run_id}/{field}")

    evidence_keys: set[Tuple[str, str, Tuple[str, ...]]] = set()
    evidence_ids: set[str] = set()
    for item in collections["evidence"]:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("id", "<missing-id>"))
        evidence_ids.add(item_id)
        if item.get("quality") not in QUALITY_ORDER:
            errors.append(f"Invalid evidence quality: {item_id}/{item.get('quality')}")
        if item.get("source_type", "other") not in EVIDENCE_SOURCE_TYPES:
            errors.append(f"Invalid evidence source_type: {item_id}/{item.get('source_type')}")
        if not str(item.get("claim", "")).strip() or not str(item.get("source", "")).strip():
            errors.append(f"Evidence lacks claim/source: {item_id}")
        if item.get("expires_at") and parse_time(str(item.get("expires_at"))) is None:
            errors.append(f"Invalid evidence expiry: {item_id}")
        key = normalized_evidence_key(item)
        if key in evidence_keys:
            warnings.append(f"Duplicate evidence excluded by gates: {item_id}")
        evidence_keys.add(key)
        for supported in item.get("supports", []):
            supported = str(supported)
            if supported not in seen and supported not in load_json(find_manifest("gates.json")) and supported not in accepted_artifact_types(state):
                warnings.append(f"Evidence target not found: {item_id} -> {supported}")

    trace_signatures: set[Tuple[str, str, str]] = set()
    for trace in collections["traceability"]:
        if not isinstance(trace, dict):
            continue
        source = str(trace.get("from", ""))
        target = str(trace.get("to", ""))
        relation = str(trace.get("relation", ""))
        if source == target:
            errors.append(f"Self-referential trace: {trace.get('id')} -> {source}")
        if relation not in TRACE_RELATIONS:
            errors.append(f"Invalid trace relation: {trace.get('id')}/{relation}")
        if not trace_endpoint_valid(state, source):
            errors.append(f"Invalid trace source endpoint: {trace.get('id')} -> {source}")
        if not trace_endpoint_valid(state, target):
            errors.append(f"Invalid trace target endpoint: {trace.get('id')} -> {target}")
        signature = (source, relation, target)
        if signature in trace_signatures:
            errors.append(f"Duplicate trace edge: {source} -[{relation}]-> {target}")
        trace_signatures.add(signature)
        for evidence_id in trace.get("evidence", []):
            if str(evidence_id) not in evidence_ids:
                errors.append(f"Trace references unknown evidence: {trace.get('id')} -> {evidence_id}")

    os_states = state.get("os_states", {})
    if not isinstance(os_states, dict):
        errors.append("os_states must be an object")
        os_states = {}
    for expected_os in OS_SEQUENCE:
        if expected_os not in os_states:
            errors.append(f"Missing OS state: {expected_os}")
    for os_name, entry in os_states.items():
        if os_name not in OS_SEQUENCE:
            errors.append(f"Unknown OS in os_states: {os_name}")
        elif not isinstance(entry, dict) or entry.get("stage") not in routing["os_stages"][os_name]:
            errors.append(f"Invalid stage in os_states: {os_name}/{entry.get('stage') if isinstance(entry, dict) else None}")
    if current_os in os_states and isinstance(os_states.get(current_os), dict):
        if os_states[current_os].get("stage") != current_stage:
            errors.append("current_stage does not match os_states[current_os].stage")
        if os_states[current_os].get("status") != "active":
            warnings.append("Current OS is not marked active")

    gates_manifest = load_json(find_manifest("gates.json"))
    for gate_name, outcomes in state.get("gates", {}).items() if isinstance(state.get("gates"), dict) else []:
        if gate_name not in gates_manifest:
            errors.append(f"Unknown gate history: {gate_name}")
            continue
        if not isinstance(outcomes, list):
            errors.append(f"Gate history must be an array: {gate_name}")
            continue
        for outcome in outcomes:
            if not isinstance(outcome, dict) or outcome.get("status") not in {"pass", "fail", "waived"}:
                errors.append(f"Invalid gate outcome: {gate_name}")
            elif outcome.get("status") == "waived" and not waiver_is_active(outcome, str(outcome.get("state_snapshot", ""))):
                warnings.append(f"Inactive or malformed waiver: {gate_name}/{outcome.get('created_at')}")

    for event in state.get("history", []) if isinstance(state.get("history"), list) else []:
        if isinstance(event, dict) and event.get("forced"):
            if not approval_is_human(str(event.get("approver", ""))) or not str(event.get("approval_id", "")).strip():
                errors.append(f"Forced transition lacks human approval: {event.get('at')}")

    if bool(config.get("audit_chain", True)):
        try:
            errors.extend(validate_audit_chain(root, state))
        except RuntimeError as exc:
            errors.append(str(exc))

    for expected in ["context.md", "config.json", "SUMMARY.md"]:
        if not (root / ".sdlc" / expected).exists():
            warnings.append(f"Missing kernel file: .sdlc/{expected}")
    return list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))

def cmd_validate(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    errors, warnings = validation_errors(root, state)
    payload = {"valid": not errors, "errors": errors, "warnings": warnings}
    text = f"Valid: {'yes' if not errors else 'no'}\nErrors: {len(errors)}\nWarnings: {len(warnings)}"
    if errors:
        text += "\n" + "\n".join(f"ERROR: {x}" for x in errors)
    if warnings:
        text += "\n" + "\n".join(f"WARN: {x}" for x in warnings)
    print_json_or_text(payload, args.json, text)
    return 0 if not errors else 2


def cmd_summary(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    state = require_state(root)
    path = write_summary(root, state)
    print(path)
    return 0


def add_project_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project", nargs="?", default=".", help="Project root (default: current directory)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic SDLC OS shared-kernel CLI")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Initialize .sdlc shared kernel")
    add_project_argument(p)
    p.add_argument("--name")
    p.add_argument("--type", choices=sorted(PROJECT_TYPES), default="greenfield")
    p.add_argument("--criticality", choices=sorted(CRITICALITIES), default="medium")
    p.add_argument("--profile", choices=sorted(PROCESS_PROFILES), help="Process depth; defaults from criticality")
    p.add_argument("--start-os", choices=OS_SEQUENCE, help="Override the project-type default start OS")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", help="Show project status")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("work-start", help="Start a risk-tailored work item inside the project")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--title", required=True)
    p.add_argument("--bounded", action="store_true", help="Declare an explicitly bounded change eligible for project-profile downgrade")
    p.add_argument("--affected-path", action="append", default=[], help="Affected path or comma-separated paths; repeatable")
    p.add_argument("--domain-impact", action="append", default=[], help="Installed domain pack materially affected by this work")
    for factor_name in WORK_FACTOR_NAMES:
        p.add_argument("--" + factor_name.replace("_", "-"), dest=factor_name, type=int)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_work_start)

    p = sub.add_parser("work-status", help="Show the active or selected work item")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_work_status)

    p = sub.add_parser("work-end", help="Close the active work item")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--status", choices=["completed", "cancelled"], default="completed")
    p.add_argument("--outcome")
    p.set_defaults(func=cmd_work_end)

    p = sub.add_parser("migrate", help="Migrate an existing shared kernel to this CLI version")
    add_project_argument(p)
    p.add_argument("--profile", choices=sorted(PROCESS_PROFILES))
    p.set_defaults(func=cmd_migrate)

    p = sub.add_parser("audit", help="Verify the append-only state audit hash chain")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("health", help="Score control-plane health and confidence")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_health)

    p = sub.add_parser("metrics", help="Summarize workflow, agent-run and cost metrics")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_metrics)

    p = sub.add_parser("quality", help="Evaluate artifact integrity and content contracts")
    add_project_argument(p)
    p.add_argument("--all", action="store_true", help="Include draft and rejected artifacts")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_quality)

    p = sub.add_parser("impact", help="Show downstream artifacts and gates affected by a change")
    add_project_argument(p)
    p.add_argument("--artifact-id", required=True, help="Comma-separated source artifact IDs")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_impact)

    p = sub.add_parser("reconcile", help="Detect integrity drift and optionally persist staleness")
    add_project_argument(p)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_reconcile)

    p = sub.add_parser("route", help="Route a task to an OS")
    add_project_argument(p)
    p.add_argument("task")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_route)

    p = sub.add_parser("next", help="Show next stage or blocking gate")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("transition", help="Move within or across OS state machines")
    add_project_argument(p)
    p.add_argument("--to-os", choices=OS_SEQUENCE)
    p.add_argument("--to-stage")
    p.add_argument("--os", choices=OS_SEQUENCE, help=argparse.SUPPRESS)
    p.add_argument("--stage", help=argparse.SUPPRESS)
    p.add_argument("--reason", required=True)
    p.add_argument("--force", action="store_true", help="Emergency override; still recorded")
    p.add_argument("--approver", help="Human approver required for --force")
    p.add_argument("--approval-id", help="Ticket, change request or approval record required for --force")
    p.set_defaults(func=cmd_transition)

    p = sub.add_parser("add-artifact", help="Register or update an artifact")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--type", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--status", choices=sorted(ARTIFACT_STATUSES), default="draft")
    p.add_argument("--owner", default="unassigned")
    p.add_argument("--description")
    p.add_argument("--checksum", help="SHA-256 for external artifacts; local artifacts are hashed automatically")
    p.add_argument("--verified-by", help="Human or system that verified the artifact")
    p.set_defaults(func=cmd_add_artifact)

    p = sub.add_parser("new-artifact", help="Create and register a Markdown artifact")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--type", required=True)
    p.add_argument("--title")
    p.add_argument("--filename")
    p.add_argument("--status", choices=sorted(ARTIFACT_STATUSES), default="draft")
    p.add_argument("--owner", default="unassigned")
    p.add_argument("--description")
    p.add_argument("--checksum")
    p.add_argument("--verified-by")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_artifact)

    p = sub.add_parser("add-evidence", help="Record evidence for a claim")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--claim", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--source-type", choices=sorted(EVIDENCE_SOURCE_TYPES), default="other")
    p.add_argument("--quality", choices=sorted(QUALITY_ORDER), default="medium")
    p.add_argument("--supports", help="Comma-separated artifact, assumption or decision IDs")
    p.add_argument("--method", help="How the evidence was produced or verified")
    p.add_argument("--limitations")
    p.add_argument("--observed-at", help="ISO-8601 observation time")
    p.add_argument("--expires-at", help="ISO-8601 time after which this evidence is stale")
    p.set_defaults(func=cmd_add_evidence)

    p = sub.add_parser("add-assumption", help="Record a testable assumption")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--text", required=True)
    p.add_argument("--risk", choices=sorted(RISK_SEVERITIES), default="medium")
    p.add_argument("--status", choices=["open", "testing", "validated", "invalidated", "retired"], default="open")
    p.add_argument("--owner", default="unassigned")
    p.add_argument("--test")
    p.set_defaults(func=cmd_add_assumption)

    p = sub.add_parser("add-decision", help="Record a decision and rationale")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--title", required=True)
    p.add_argument("--choice", required=True)
    p.add_argument("--rationale", required=True)
    p.add_argument("--owner", default="unassigned")
    p.add_argument("--alternatives")
    p.add_argument("--evidence")
    p.set_defaults(func=cmd_add_decision)

    p = sub.add_parser("add-risk", help="Record a delivery or product risk")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--title", required=True)
    p.add_argument("--severity", choices=sorted(RISK_SEVERITIES), required=True)
    p.add_argument("--likelihood", choices=["rare", "unlikely", "possible", "likely", "almost-certain"], default="possible")
    p.add_argument("--status", choices=["open", "investigating", "mitigated", "accepted", "closed"], default="open")
    p.add_argument("--mitigation", required=True)
    p.add_argument("--owner", default="unassigned")
    p.add_argument("--trigger")
    p.set_defaults(func=cmd_add_risk)

    p = sub.add_parser("update-risk", help="Update or close an existing risk")
    add_project_argument(p)
    p.add_argument("--id", required=True)
    p.add_argument("--title")
    p.add_argument("--severity", choices=sorted(RISK_SEVERITIES))
    p.add_argument("--likelihood", choices=["rare", "unlikely", "possible", "likely", "almost-certain"])
    p.add_argument("--status", choices=["open", "investigating", "mitigated", "accepted", "closed"])
    p.add_argument("--mitigation")
    p.add_argument("--owner")
    p.add_argument("--trigger")
    p.set_defaults(func=cmd_update_risk)

    p = sub.add_parser("trace", help="Add a traceability edge")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--from", dest="from_id", required=True)
    p.add_argument("--to", dest="to_id", required=True)
    p.add_argument("--relation", required=True)
    p.add_argument("--evidence")
    p.set_defaults(func=cmd_trace)

    p = sub.add_parser("record-run", help="Record an Agent or Skill execution for cost and outcome tracking")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--actor", required=True)
    p.add_argument("--os", choices=OS_SEQUENCE, required=True)
    p.add_argument("--skill", required=True)
    p.add_argument("--model", default="unspecified")
    p.add_argument("--outcome", choices=["success", "partial", "failed", "aborted"], required=True)
    p.add_argument("--duration-ms", type=int, default=0)
    p.add_argument("--tokens-input", type=int, default=0)
    p.add_argument("--tokens-output", type=int, default=0)
    p.add_argument("--tool-calls", type=int, default=0)
    p.add_argument("--cost-usd", type=float, default=0.0)
    p.add_argument("--human-hours", type=float, default=0.0)
    p.add_argument("--artifacts", help="Comma-separated artifact IDs")
    p.add_argument("--notes")
    p.set_defaults(func=cmd_record_run)

    p = sub.add_parser("gate", help="Check or waive a stage gate")
    add_project_argument(p)
    p.add_argument("--name", required=True)
    p.add_argument("--check", action="store_true", help="Compatibility flag; checking is the default")
    p.add_argument("--waive", action="store_true")
    p.add_argument("--reason")
    p.add_argument("--approver")
    p.add_argument("--approval-id")
    p.add_argument("--compensating-control")
    p.add_argument("--expires")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("learn", help="Record expected-vs-actual learning and re-entry route")
    add_project_argument(p)
    p.add_argument("--id")
    p.add_argument("--expected", required=True)
    p.add_argument("--actual", required=True)
    p.add_argument("--gap", required=True)
    p.add_argument("--gap-type", choices=["assumption", "evidence", "execution", "strategy", "design", "quality", "operations"], required=True)
    p.add_argument("--decision", required=True)
    p.add_argument("--route-os", choices=OS_SEQUENCE, required=True)
    p.add_argument("--route-stage")
    p.add_argument("--evidence")
    p.set_defaults(func=cmd_learn)

    p = sub.add_parser("validate", help="Validate project-state consistency")
    add_project_argument(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("summary", help="Regenerate .sdlc/SUMMARY.md")
    add_project_argument(p)
    p.set_defaults(func=cmd_summary)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command in MUTATING_COMMANDS:
            with project_lock(project_root(args.project)):
                return int(args.func(args))
        return int(args.func(args))
    except RuntimeError as exc:
        eprint(f"ERROR: {exc}")
        return 2
    except KeyboardInterrupt:
        eprint("Interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
