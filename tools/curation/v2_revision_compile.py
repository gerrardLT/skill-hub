#!/usr/bin/env python3
"""Compile the V2 1.1.0 candidate (Skills, Recipes, router) from the frozen 1.0.0 release plus revision records.

Read-only on slots/v2 and recipes/v2. Writes only evals/candidates/capability-compiler-v2/revision-1.1.0/.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

VERSION = "1.1.0-candidate"
OLD = "1.0.0"
REV = Path("curation/v2/revision-1.1.0")
OUT = Path("evals/candidates/capability-compiler-v2/revision-1.1.0")
PROTECTED = {"remote-write-authorized-only", "local-system-write-authorized-only", "local-system-write-external-session-authorized-only"}
ACRONYMS = {"ai", "ui", "apm", "llm", "jtbd", "cli", "ci", "api", "tdd", "qa", "sdk", "pr", "dx", "ux", "mcp", "oidc", "sso", "rca"}
STALE_FORBIDDEN = re.compile(r"claim Phase 9 evaluation[^,]*?(?:, Phase 10 approval,)?[^,]*?(?:or )?(?:released status|release evidence that has not run)")
STALE_FORBIDDEN_NEW = "claim evaluation, approval, release, or completion evidence that has not been produced"
ACTION_BOUNDARY = re.compile(r"This candidate defines an action contract,? but Phase \d candidate construction(?: and evaluation planning)? do(?:es)? not execute the action\.")
ACTION_BOUNDARY_NEW = "This Skill defines an action contract and does not execute the action by itself."
PARTIAL_GATE = "Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable."
DELIVER_LINE = "Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced."
NEEDS_INPUT_TAIL = " Deliver every supported part first and name the owner for the missing part."


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def title_of(name: str) -> str:
    return " ".join(part.upper() if part in ACRONYMS else part.capitalize() for part in name.split("-"))


def parse_skill(text: str) -> tuple[list[tuple[str, str]], str]:
    body = text.split("\n---\n", 1)[1]
    body = body.split("\n", 2)[2] if body.startswith("\n# ") else body.split("\n", 1)[1]
    sections = []
    for match in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", body, re.S | re.M):
        sections.append((match.group(1).strip(), match.group(2).strip("\n")))
    return sections, text


def bullets(block: str) -> list[str]:
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def remap(route: str, merges: dict[str, str], fixes: dict[str, str | None], ids: set[str]) -> str | None:
    route = merges.get(route, route)
    if route in fixes:
        route = fixes[route]
    return route if route in ids else None


def load_records(workspace: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((workspace / REV / "records").glob("*.json")):
        for skill_id, record in load(path)["skills"].items():
            if skill_id in records:
                raise ValueError(f"duplicate revision record: {skill_id}")
            records[skill_id] = record
    return records


def build_skill(workspace: Path, skill_id: str, record: dict[str, Any], structure: dict[str, Any], ids: set[str], catalog_path: str) -> dict[str, bytes]:
    merges, fixes = structure["merges"], structure["reference_fixes"]
    root = workspace / catalog_path
    old_text = (root / "SKILL.md").read_text(encoding="utf-8")
    contract = load(root / "contract.json")
    provenance = load(root / "provenance.json")
    sections = dict(parse_skill(old_text)[0])
    order = [name for name, _ in parse_skill(old_text)[0]]

    signals = record["trigger_signals"]
    responsibility = record.get("responsibility") or contract["responsibility"]
    if not 2 <= len(signals) <= 5 or any(not s.strip() or responsibility.strip().lower() in s.lower() for s in signals):
        raise ValueError(f"{skill_id}: trigger_signals must be 2-5 distinct signals that do not restate the responsibility")

    # anti-triggers
    old_anti = []
    for line in bullets(sections["Trigger"]):
        match = re.match(r"(.*?)\s*Route to `([^`]+)`\.?$", line)
        if match:
            old_anti.append({"text": match.group(1).strip().rstrip("."), "route": match.group(2)})
    anti, seen = [], set()
    for item in [*old_anti, *record.get("anti_add", [])]:
        route = remap(item["route"], merges, fixes, ids)
        if route and route != skill_id and route not in seen and route not in record.get("anti_drop", []):
            seen.add(route)
            anti.append({"text": item["text"].rstrip("."), "route": route})
    trigger = "Use when the request matches any of:\n" + "\n".join(f"- {s}" for s in signals) + "\n\nDo not use when:\n" + "\n".join(f"- {a['text']}. Route to `{a['route']}`." for a in anti)

    # contract
    new = copy.deepcopy(contract)
    new["version"], new["status"] = VERSION, "evaluating"
    new["responsibility"] = responsibility
    new["forbidden_actions"] = [STALE_FORBIDDEN_NEW if re.match(r"claim Phase \d", a) else a for a in contract["forbidden_actions"]]
    new["forbidden_actions"] += [a for a in record.get("forbidden_add", []) if a not in new["forbidden_actions"]]
    new["hard_gates"] = contract["hard_gates"] + [g for g in record.get("gates_add", []) if g not in contract["hard_gates"]]
    new["inputs"] = record.get("inputs", contract["inputs"])
    new["outputs"] = contract["outputs"] + [o for o in record.get("outputs_add", []) if o not in contract["outputs"]]
    new["artifact_types"] = list(new["outputs"])
    if "contract" in record:
        for key, value in record["contract"].items():
            new[key] = value
    contract_bytes = dump(new)

    # procedure
    steps = [re.sub(r"^\d+\.\s*", "", l.strip()) for l in sections["Procedure"].splitlines() if re.match(r"\s*\d+\.", l)]
    if "procedure" in record:
        steps = list(record["procedure"])
    for ins in sorted(record.get("procedure_insert", []), key=lambda i: -i["after"]):
        steps.insert(ins["after"], ins["text"])
    procedure = "\n".join(f"{n}. {s}" for n, s in enumerate(steps, 1))

    # output contract
    evidence = next((p for p in sections["Output Contract"].split("\n\n") if p.startswith("Every")), "")
    output = "Produce:\n" + "\n".join(f"- {o}" for o in new["outputs"]) + ("\n\n" + evidence if evidence else "") + "\n\n" + DELIVER_LINE

    # hard gates and forbidden actions
    gates = list(new["hard_gates"])
    for g in bullets(sections["Hard Gates"]):
        if g not in gates and g not in record.get("superseded_gates", []):
            gates.append(g)
    gates.append(PARTIAL_GATE)
    forbidden = "\n".join(f"- {a}" for a in new["forbidden_actions"])

    # non-responsibilities
    nr = sections["Non-Responsibilities"]
    adjacent = []
    for route in bullets(nr.split("Adjacent capabilities:", 1)[1].split("\n\n", 1)[0]) if "Adjacent capabilities:" in nr else []:
        route = remap(route.strip("`"), merges, fixes, ids)
        if route and route != skill_id and route not in adjacent:
            adjacent.append(route)
    for a in anti:
        if a["route"] not in adjacent:
            adjacent.append(a["route"])
    tail = nr.split("Adjacent capabilities:", 1)[1].split("\n\n", 1)[1].strip() if "Adjacent capabilities:" in nr and "\n\n" in nr.split("Adjacent capabilities:", 1)[1] else ""
    non_resp = "Adjacent capabilities:\n" + "\n".join(f"- `{r}`" for r in adjacent) + ("\n\n" + tail if tail else "")

    status = sections["Status Mapping"]
    status = re.sub(r"^(- `needs-input`:.*?)$", lambda m: m.group(1) + NEEDS_INPUT_TAIL, status, flags=re.M)

    # frontmatter description
    def description(count: int) -> str:
        parts = responsibility.rstrip(".") + ". Use when " + "; ".join(s.rstrip(".") for s in signals[:3]) + "."
        if count:
            parts += " Do not use for: " + "; ".join(f"{a['text']} (-> {a['route']})" for a in anti[:count]) + "."
        return parts
    desc = description(len(anti))
    for count in range(len(anti), -1, -1):
        desc = description(count)
        if len(desc) <= 1024:
            break

    out = [f"---\nname: {skill_id}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n---\n", f"# {title_of(skill_id)}\n"]
    def add(name: str, body: str) -> None:
        out.append(f"## {name}\n\n{body.strip()}\n")
    add("Responsibility", responsibility)
    add("Trigger", trigger)
    required = "\n".join(f"- {i}" for i in new["inputs"])
    add("Required Inputs", required)
    add("Procedure", procedure)
    if record.get("guidance"):
        add("Domain Guidance", "\n".join(f"- {g}" for g in record["guidance"]))
    add("Output Contract", output)
    for name in order:
        if name in {"Responsibility", "Trigger", "Required Inputs", "Procedure", "Output Contract", "Status Mapping", "Non-Responsibilities"}:
            continue
        if name == "Hard Gates":
            add("Hard Gates", "\n".join(f"- {g}" for g in gates))
            add("Forbidden Actions", forbidden)
            continue
        add(name, ACTION_BOUNDARY.sub(ACTION_BOUNDARY_NEW, sections[name]))
    add("Status Mapping", status)
    add("Non-Responsibilities", non_resp)
    skill_bytes = ("\n".join(out)).replace("\n\n\n", "\n\n").encode("utf-8")

    # provenance
    base = copy.deepcopy(provenance["candidate_provenance"])
    absorbed = {}
    for gone, target in merges.items():
        if target == skill_id:
            old_prov = load(workspace / "slots/v2/1.0.0/skills" / gone / "provenance.json")
            absorbed[gone] = old_prov["candidate_provenance"]
            for key in ["canonical_unit_ids", "root_derived_atom_ids", "source_evidence", "source_fragment_ids", "fusion_decision_ids", "retained_auxiliary_unit_ids", "source_cluster_ids", "decision_references"]:
                base[key] = sorted(set(base.get(key, [])) | set(old_prov["candidate_provenance"].get(key, [])))
    base["source_evidence"] = sorted(set(base.get("source_evidence", [])) | set(record.get("source_evidence_add", [])))
    prov = {
        "schema_version": "2.0", "id": skill_id, "version": VERSION, "status": "evaluating", "capability_id": contract["capability_id"],
        "based_on": {"release": OLD, "contract_sha256": sha((root / "contract.json").read_bytes()), "skill_sha256": sha((root / "SKILL.md").read_bytes()), "provenance_sha256": sha((root / "provenance.json").read_bytes())},
        "revision": {"record_sha256": sha(dump(record)), "resolves": record.get("resolves", {}), "authored_content": record.get("authored_content", []), "absorbs": sorted(absorbed)},
        "candidate_provenance": base, "absorbed_candidate_provenance": absorbed,
    }
    return {"SKILL.md": skill_bytes, "contract.json": contract_bytes, "provenance.json": dump(prov)}


def rewrite_strings(value: Any, new_root: str) -> Any:
    if isinstance(value, str):
        value = value.replace(f"recipes/v2/{OLD}/", f"{new_root}/recipes/").replace("slots/v2/catalog.json", f"{new_root}/skill-index.json")
        return re.sub(r"(@)1\.0\.0\b", r"\g<1>" + VERSION, value)
    if isinstance(value, list):
        return [rewrite_strings(v, new_root) for v in value]
    if isinstance(value, dict):
        return {k: rewrite_strings(v, new_root) for k, v in value.items()}
    return value


def compile_recipes(workspace: Path, structure: dict[str, Any], contracts: dict[str, dict[str, Any]], contract_hash: dict[str, str], ids: set[str]) -> dict[str, bytes]:
    merges, root = structure["merges"], OUT.as_posix()
    files: dict[str, bytes] = {}
    stage_docs = {p.stem: load(p) for p in sorted((workspace / f"recipes/v2/{OLD}/stages").glob("*.json"))}
    records, step_stage = [], {}
    for name, doc in stage_docs.items():
        doc["steps"] = [s for s in doc["steps"] if s["id"] not in merges]
        for s in doc["steps"]:
            step_stage[s["id"]] = name
        records += doc["dependency_records"]
    seen, final = set(), []
    for r in records:
        r = copy.deepcopy(r)
        src, tgt = (merges.get(x.split(":", 1)[1], x.split(":", 1)[1]) for x in (r["source_capability_id"], r["target_capability_id"]))
        if src == tgt:
            continue
        key = (src, tgt, r["kind"])
        if key in seen:
            continue
        seen.add(key)
        r["source_capability_id"], r["target_capability_id"] = f"capability:{src}", f"capability:{tgt}"
        final.append(r)
    for r in final:
        if r["id"] in structure.get("downgrade_remapped_hard", []):
            r["kind"] = "optional"
    for r in structure.get("additional_dependency_records", []):
        if r["source_capability_id"].split(":", 1)[1] not in ids or r["target_capability_id"].split(":", 1)[1] not in ids:
            raise ValueError("additional dependency references unknown capability")
        if any(existing["id"] == r["id"] for existing in final):
            raise ValueError("duplicate additional dependency id")
        final.append(copy.deepcopy(r))
    for name, doc in stage_docs.items():
        doc["dependency_records"] = sorted((r for r in final if step_stage[r["target_capability_id"].split(":", 1)[1]] == name), key=lambda r: r["id"])
        for s in doc["steps"]:
            c = contracts[s["id"]]
            protected = c["permission_identity"] in PROTECTED or c["execution"]["remote_write"] or c["execution"]["mutation_scope"] == "authorized-local-git"
            s.update({"skill_ref": f"{s['id']}@{VERSION}", "candidate_path": f"{root}/skills/{s['id']}", "contract_sha256": contract_hash[s["id"]], "inputs": c["inputs"], "outputs": c["outputs"], "hard_gates": c["hard_gates"], "permission_identity": c["permission_identity"], "mutation_scope": c["execution"]["mutation_scope"], "remote_write": c["execution"]["remote_write"], "condition": "Select only when the atomic requested outcome matches: " + c["responsibility"], "activation": "disabled-pending-current-authorization" if protected else "conditional"})
            s["dependency_refs"] = sorted(r["id"] for r in final if r["target_capability_id"] == f"capability:{s['id']}")
        doc.update({"version": VERSION, "status": "evaluating", "execution_state": "candidate-definition-not-executed"})
        files[f"recipes/stages/{name}.json"] = dump(rewrite_strings(doc, root))
    for p in sorted((workspace / f"recipes/v2/{OLD}/composites").glob("*.json")):
        doc = rewrite_strings(load(p), root)
        doc.update({"version": VERSION, "status": "evaluating", "execution_state": "candidate-definition-not-executed"})
        files[f"recipes/composites/{p.name}"] = dump(doc)
    ui = load(workspace / f"recipes/v2/{OLD}/specialized/complete-ui-design-and-review.json")
    gone_steps = {"preflight"}
    ui["steps"] = [s for s in ui["steps"] if s["id"] not in gone_steps]
    edges, seen_edges = [], set()
    for e in ui["edges"]:
        e = {**e, "from": "review-evidence" if e["from"] in gone_steps else e["from"], "to": "review-evidence" if e["to"] in gone_steps else e["to"]}
        if e["from"] == e["to"] or (e["from"], e["to"]) in seen_edges:
            continue
        seen_edges.add((e["from"], e["to"]))
        e["condition"] = e["condition"].replace("cross-domain preflight", "review evidence capture")
        edges.append(e)
    ui["edges"] = edges
    for s in ui["steps"]:
        s["depends_on"] = sorted({e["from"] for e in edges if e["to"] == s["id"]})
        skill_id = s["skill_ref"].split("@")[0]
        c = contracts[skill_id]
        s.update({"skill_ref": f"{skill_id}@{VERSION}", "outputs": c["outputs"], "permission_identity": c["permission_identity"], "mutation_scope": c["execution"]["mutation_scope"]})
    ui.update({"version": VERSION, "status": "evaluating"})
    files["recipes/specialized/complete-ui-design-and-review.json"] = dump(rewrite_strings(ui, root))
    router = rewrite_strings(load(workspace / f"recipes/v2/{OLD}/router.json"), root)
    router.update({"version": VERSION, "status": "evaluating", "execution_state": "candidate-definition-not-executed"})
    files["recipes/router.json"] = dump(router)
    return files


def compile_all(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    structure = load(workspace / REV / "structure.json")
    catalog = load(workspace / "slots/v2/catalog.json")
    all_ids = [s["id"] for s in catalog["skills"]]
    kept = [i for i in all_ids if i not in structure["merges"]]
    ids = set(kept)
    records = load_records(workspace)
    missing = sorted(set(kept) - set(records))
    if missing:
        raise ValueError(f"missing revision records: {missing}")
    paths = {s["id"]: s["path"] for s in catalog["skills"]}
    files: dict[str, bytes] = {}
    contracts, contract_hash, index = {}, {}, []
    for skill_id in kept:
        built = build_skill(workspace, skill_id, records[skill_id], structure, ids, paths[skill_id])
        for name, data in built.items():
            files[f"skills/{skill_id}/{name}"] = data
        contracts[skill_id] = json.loads(built["contract.json"])
        contract_hash[skill_id] = sha(built["contract.json"])
        cap = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
        index.append({"id": skill_id, "path": f"{OUT.as_posix()}/skills/{skill_id}", "responsibility": contracts[skill_id]["responsibility"], "stage_id": cap["lifecycle_stage_id"], "permission_identity": contracts[skill_id]["permission_identity"], "contract_sha256": contract_hash[skill_id], "skill_sha256": sha(built["SKILL.md"]), "provenance_sha256": sha(built["provenance.json"])})
    files["skill-index.json"] = dump({"schema_version": "2.0", "version": VERSION, "status": "evaluating", "skill_count": len(index), "skills": index})
    files.update(compile_recipes(workspace, structure, contracts, contract_hash, ids))
    out_root = workspace / OUT
    for rel, data in files.items():
        write_bytes(out_root / rel, data)
    manifest = {"schema_version": "2.0", "version": VERSION, "base_release": OLD, "skill_count": len(kept), "removed_by_merge": structure["merges"], "files": {rel: sha(data) for rel, data in sorted(files.items())}}
    write_bytes(out_root / "compile-manifest.json", dump(manifest))
    return {"skills": len(kept), "files": len(files), "merged_away": sorted(structure["merges"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(compile_all(args.workspace_root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
