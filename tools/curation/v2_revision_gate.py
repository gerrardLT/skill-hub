#!/usr/bin/env python3
"""Fail-closed gate for the V2 1.1.0 candidate. Read-only; never touches slots/v2 or recipes/v2."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

OUT = Path("evals/candidates/capability-compiler-v2/revision-1.1.0")
REV = Path("curation/v2/revision-1.1.0")
VERSION = "1.1.0-candidate"
PROTECTED = {"remote-write-authorized-only", "local-system-write-authorized-only", "local-system-write-external-session-authorized-only"}
DANGLING = ["provider-review-comment-response", "artifact-publication", "pull-request-update", "schema-migration-safety"]
RESOLVE = re.compile(r"^(fixed|declined|deferred-to-eval): \S")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def section(text: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def bullets(block: str) -> list[str]:
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def skills_of(ws: Path) -> dict[str, dict[str, Any]]:
    root = ws / OUT / "skills"
    return {p.name: {"contract": load(p / "contract.json"), "prov": load(p / "provenance.json"), "md": (p / "SKILL.md").read_text(encoding="utf-8")} for p in sorted(root.iterdir()) if p.is_dir()}


def check_files(ws: Path, skills: dict) -> list[str]:
    errors, root = [], ws / OUT
    manifest = load(root / "compile-manifest.json")
    on_disk = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} - {"compile-manifest.json"}
    if on_disk != set(manifest["files"]):
        errors.append(f"candidate files differ from manifest: extra={sorted(on_disk - set(manifest['files']))[:3]} missing={sorted(set(manifest['files']) - on_disk)[:3]}")
    for rel, digest in manifest["files"].items():
        p = root / rel
        if p.is_file() and sha(p.read_bytes()) != digest:
            errors.append(f"hash mismatch: {rel}")
    old_ids = {s["id"] for s in load(ws / "slots/v2/catalog.json")["skills"]}
    merges = load(ws / REV / "structure.json")["merges"]
    if set(skills) != old_ids - set(merges) or len(skills) != 154 or manifest["skill_count"] != 154:
        errors.append("candidate skill set is not 1.0.0 minus the three merged Skills (154)")
    index = {s["id"]: s for s in load(root / "skill-index.json")["skills"]}
    if set(index) != set(skills):
        errors.append("skill-index ids differ from skills")
    for sid, s in skills.items():
        d = root / "skills" / sid
        got = index.get(sid, {})
        if got.get("contract_sha256") != sha((d / "contract.json").read_bytes()) or got.get("skill_sha256") != sha((d / "SKILL.md").read_bytes()):
            errors.append(f"skill-index hash mismatch: {sid}")
    return errors


def check_findings(ws: Path, skills: dict) -> list[str]:
    errors, ledger = [], load(ws / "curation/v2/skill-audit/ledger.json")
    resolved: dict[str, str] = {}
    for s in skills.values():
        resolved.update(s["prov"]["revision"]["resolves"])
    total = 0
    for entry in ledger["skills"]:
        for n, finding in enumerate(entry["semantic"]["findings"], 1):
            fid, total = f"{entry['id']}#F{n}", total + 1
            value = resolved.get(fid)
            if value is None:
                errors.append(f"unresolved finding: {fid}")
            elif not RESOLVE.match(value):
                errors.append(f"malformed resolution: {fid}")
            elif value.startswith("deferred-to-eval") and finding["dimension"] != "measured_efficacy" and "Phase R5" not in value:
                errors.append(f"deferred without an R5 test plan: {fid}")
    if total != 231:
        errors.append(f"expected 231 findings, ledger has {total}")
    cross = load(ws / REV / "structure.json").get("cross_resolutions", {})
    for i in range(1, len(ledger["cross_skill_findings"]) + 1):
        if not RESOLVE.match(cross.get(f"X{i}", "")):
            errors.append(f"unresolved cross-skill finding: X{i}")
    return errors


def check_skill_text(ws: Path, skills: dict) -> list[str]:
    errors = []
    merged = list(load(ws / REV / "structure.json")["merges"])
    for sid, s in skills.items():
        c, md = s["contract"], s["md"]
        head = md.split("\n---\n", 1)[0]
        desc = re.search(r'^description: "(.*)"$', head, re.M)
        if not re.search(rf"^name: {re.escape(sid)}$", head, re.M) or not desc or len(desc.group(1)) > 1024:
            errors.append(f"frontmatter invalid: {sid}")
        md_gates = bullets(section(md, "Hard Gates"))
        if [g for g in c["hard_gates"] if g not in md_gates] or not any(g.startswith("Deliver every part") for g in md_gates):
            errors.append(f"SKILL.md lacks a contract hard gate or the partial-delivery gate: {sid}")
        if bullets(section(md, "Forbidden Actions")) != c["forbidden_actions"]:
            errors.append(f"SKILL.md forbidden actions differ from contract: {sid}")
        if len(c["hard_gates"]) < 2 or len(c["forbidden_actions"]) < 1:
            errors.append(f"too few gates or forbidden actions: {sid}")
        triggers = bullets(section(md, "Trigger").split("Do not use when:")[0])
        if len(triggers) < 2 or any(t.strip(".") == c["responsibility"].strip(".") for t in triggers):
            errors.append(f"trigger restates responsibility or has <2 signals: {sid}")
        if re.search(r"Phase \d|released status", md) or re.search(r"Phase \d", json.dumps(c)):
            errors.append(f"stale phase wording: {sid}")
        for ghost in merged + DANGLING:
            if ghost in md or ghost in json.dumps(c):
                errors.append(f"dangling reference {ghost}: {sid}")
        for ref in set(re.findall(r"Route to `([a-z0-9-]+)`", md)):
            if ref not in skills:
                errors.append(f"route to unknown Skill {ref}: {sid}")
        if "## Status Mapping" in md and "Deliver every supported part first" not in md:
            errors.append(f"status mapping lacks partial-delivery rule: {sid}")
    for a, b in load(ws / REV / "structure.json")["overlap_pairs"]:
        for x, y in ((a, b), (b, a)):
            if f"Route to `{y}`" not in skills[x]["md"]:
                errors.append(f"missing anti-trigger {x} -> {y}")
    return errors


def check_permissions(ws: Path, skills: dict) -> list[str]:
    errors, idents = [], {i["id"]: i for i in load(ws / "curation/v2/lifecycle/permission-identities.json")["identities"]}
    for sid, s in skills.items():
        new, old = s["contract"], load(ws / "slots/v2/1.0.0/skills" / sid / "contract.json")
        ne, oe = new["execution"], old["execution"]
        ident = idents.get(new["permission_identity"])
        if ident is None:
            errors.append(f"unknown permission identity: {sid}")
            continue
        if not set(ne.get("model_tools", [])) <= set(ident["model_tools"]) or not set(ne.get("host_actions", [])) <= set(ident["host_actions"]):
            errors.append(f"execution exceeds identity: {sid}")
        if (new["permission_identity"], ne) == (old["permission_identity"], oe):
            continue
        if old["permission_identity"] in PROTECTED or new["permission_identity"] in PROTECTED:
            errors.append(f"protected permission changed: {sid}")
        if not set(ne.get("model_tools", [])) <= set(oe.get("model_tools", [])) or not set(ne.get("host_actions", [])) <= set(oe.get("host_actions", [])):
            errors.append(f"permission widened (tools or host actions): {sid}")
        if ne.get("remote_write") and not oe.get("remote_write"):
            errors.append(f"permission widened (remote write): {sid}")
        if ne.get("external", "none") != oe.get("external", "none") and ne.get("external", "none") != "none":
            errors.append(f"permission widened (external): {sid}")
        if not s["prov"]["revision"]["resolves"]:
            errors.append(f"permission narrowed without a recorded reason: {sid}")
    return errors


def iter_recipes(ws: Path):
    for p in sorted((ws / OUT / "recipes").rglob("*.json")):
        yield p, load(p)


def check_recipes(ws: Path, skills: dict) -> list[str]:
    errors, seen, protected = [], [], 0
    stage_ids = {p.stem for p in (ws / OUT / "recipes/stages").glob("*.json")}
    caps = {f"capability:{s['contract']['capability_id'].removeprefix('capability:')}" for s in skills.values()}
    hard: dict[str, set[str]] = {}
    for p, r in iter_recipes(ws):
        name = p.relative_to(ws / OUT).as_posix()
        if "/stages/" in f"/{name}":
            for step in r["steps"]:
                sid = step["id"]
                seen.append(sid)
                s = skills.get(sid)
                if s is None:
                    errors.append(f"{name}: step for unknown Skill {sid}")
                    continue
                c = s["contract"]
                if step["skill_ref"] != f"{sid}@{VERSION}" or step["contract_sha256"] != sha((ws / OUT / "skills" / sid / "contract.json").read_bytes()):
                    errors.append(f"{name}: stale contract binding {sid}")
                for key, want in (("inputs", c["inputs"]), ("outputs", c["outputs"]), ("hard_gates", c["hard_gates"]), ("permission_identity", c["permission_identity"]), ("mutation_scope", c["execution"]["mutation_scope"]), ("remote_write", c["execution"]["remote_write"])):
                    if step.get(key) != want:
                        errors.append(f"{name}: step {sid} {key} differs from contract")
            for d in r["dependency_records"]:
                for end in ("source_capability_id", "target_capability_id"):
                    if d[end] not in caps:
                        errors.append(f"{name}: dependency endpoint not in candidate: {d[end]}")
                if d["kind"] == "hard":
                    hard.setdefault(d["source_capability_id"], set()).add(d["target_capability_id"])
        for step in r.get("steps", []):
            ident = step.get("permission_identity") or skills.get(str(step.get("skill_ref", "")).split("@")[0], {}).get("contract", {}).get("permission_identity")
            if ident in PROTECTED:
                if step.get("activation") != "disabled-pending-current-authorization":
                    errors.append(f"{name}: protected step not disabled: {step.get('id')}")
            if step.get("activation") == "disabled-pending-current-authorization":
                protected += 1
        if "/specialized/" in f"/{name}":
            ids = {s["id"] for s in r["steps"]}
            if "preflight" in ids:
                errors.append(f"{name}: merged preflight step still present")
            for s in r["steps"]:
                if not s["skill_ref"].endswith(f"@{VERSION}") or s["skill_ref"].split("@")[0] not in skills:
                    errors.append(f"{name}: bad skill_ref {s['skill_ref']}")
    if sorted(seen) != sorted(skills) or len(seen) != 154:
        errors.append("stage recipes do not place the 154 Skills exactly once")
    if protected != 27:
        errors.append(f"expected 27 protected steps, found {protected}")
    state: dict[str, int] = {}

    def cyclic(n: str) -> bool:
        if state.get(n) == 1:
            return True
        if state.get(n) == 2:
            return False
        state[n] = 1
        bad = any(cyclic(m) for m in hard.get(n, ()))
        state[n] = 2
        return bad

    if any(cyclic(n) for n in list(hard)):
        errors.append("hard dependency cycle")
    router = load(ws / OUT / "recipes/router.json")
    if not (ws / router["atomic_index_ref"]).is_file():
        errors.append("router atomic_index_ref missing")
    for key in ("stage_targets", "composite_targets", "specialized_targets"):
        for t in router[key]:
            if not (ws / t["path"]).is_file():
                errors.append(f"router target missing: {t['path']}")
    for t in router["atomic_precedence"]:
        if t["target"] not in skills and t["target"] not in stage_ids:
            errors.append(f"router atomic target unknown: {t['target']}")
    return errors


def verify(workspace: Path, *, check_release: bool = True) -> dict[str, Any]:
    ws, checks = workspace.resolve(), []
    skills = skills_of(ws)
    for name, fn in (("candidate-files-and-skill-set", check_files), ("findings-closed", check_findings), ("skill-text-and-contract", check_skill_text), ("permissions-only-narrowed", check_permissions), ("recipes-and-router", check_recipes)):
        errors = fn(ws, skills)
        checks.append({"name": name, "ok": not errors, "errors": errors[:25], "error_count": len(errors)})
    if check_release:
        sys.path.insert(0, str(Path(__file__).parent))
        import v2_phase12_gate
        rel = v2_phase12_gate.verify(ws)
        errors = [e for c in rel["checks"] if not c["ok"] for e in c["errors"]]
        checks.append({"name": "release-1.0.0-unchanged", "ok": rel["status"] == "passed" if "status" in rel else not errors, "errors": errors[:10], "error_count": len(errors)})
    return {"version": VERSION, "status": "passed" if all(c["ok"] for c in checks) else "failed", "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    report = verify(args.workspace_root)
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
