#!/usr/bin/env python3
"""Read-only deterministic static scan of the released V2 1.0.0 atomic Skills."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

WORD = re.compile(r"[a-z][a-z0-9-]{2,}")
STOP = set("the and for with from that this into when only each every not are any all one its use than then must does have has was were per via under over across without".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def section(text: str, name: str) -> str:
    match = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1).strip() if match else ""


def bullets(block: str) -> list[str]:
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def terms(text: str) -> set[str]:
    return {word for word in WORD.findall(text.lower()) if word not in STOP}


def scan(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    catalog = load(workspace / "slots/v2/catalog.json")
    ids = {item["id"] for item in catalog["skills"]}
    recipe_ids = {item["id"] for item in load(workspace / "recipes/v2/catalog.json")["recipes"]}
    grading = load(workspace / "evals/runs/capability-compiler-v2/phase-9/grading-report.json")
    run_skill = {run["run_id"]: run.get("skill_id") for run in grading["runs"]}
    holdouts: dict[str, list[str]] = {}
    for item in grading["paired_skill_holdouts"]:
        holdouts.setdefault(item["skill_id"], []).append(item["outcome"])
    mutation: dict[str, str] = {}
    for item in grading["mutation_results"]:
        skill_id = run_skill.get(item.get("control_run")) or run_skill.get(item.get("mutated_run"))
        if skill_id:
            mutation[skill_id] = item["status"]

    docs: dict[str, dict[str, Any]] = {}
    line_counts: Counter[str] = Counter()
    for item in catalog["skills"]:
        root = workspace / item["path"]
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        contract = load(root / "contract.json")
        provenance = load(root / "provenance.json")["candidate_provenance"]
        lines = {line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")}
        line_counts.update(lines)
        docs[item["id"]] = {"text": text, "contract": contract, "provenance": provenance, "lines": lines}

    corpus_terms = {skill_id: terms(doc["contract"]["responsibility"] + " " + " ".join(doc["contract"]["inputs"]) + " " + " ".join(doc["contract"]["outputs"])) for skill_id, doc in docs.items()}
    results = []
    for skill_id, doc in sorted(docs.items()):
        text, contract, provenance = doc["text"], doc["contract"], doc["provenance"]
        responsibility = contract["responsibility"].strip()
        trigger = section(text, "Trigger")
        anti = re.findall(r"Route to `([^`]+)`", trigger)
        procedure = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in section(text, "Procedure").splitlines() if re.match(r"\s*\d+\.", line)]
        skill_outputs = bullets(section(text, "Output Contract"))
        shared = sum(1 for line in doc["lines"] if line_counts[line] >= 20)
        mine = corpus_terms[skill_id]
        neighbours = sorted(((len(mine & other) / max(1, len(mine | other)), other_id) for other_id, other in corpus_terms.items() if other_id != skill_id), reverse=True)[:3]
        outcomes = holdouts.get(skill_id, [])
        findings = []
        if responsibility in trigger:
            findings.append("trigger-restates-responsibility")
        if any(target not in ids for target in anti):
            findings.append("anti-trigger-target-missing")
        if not set(contract["outputs"]).issubset(set(skill_outputs)):
            findings.append("skill-output-contract-drift")
        if any(gate not in text for gate in contract["hard_gates"]):
            findings.append("skill-md-omits-contract-hard-gate")
        if any(action not in text for action in contract.get("forbidden_actions", [])):
            findings.append("skill-md-omits-forbidden-actions")
        if any("released status" in action for action in contract.get("forbidden_actions", [])):
            findings.append("stale-prerelease-forbidden-action")
        if len(provenance.get("source_evidence", [])) <= 2:
            findings.append("thin-source-evidence")
        if outcomes and all(outcome == "tie" for outcome in outcomes):
            findings.append("no-measured-holdout-lift")
        if mutation.get(skill_id) in {"survived", "behavioral-challenge-needed", "invalid-control"}:
            findings.append(f"mutation-{mutation[skill_id]}")
        if neighbours and neighbours[0][0] >= 0.35:
            findings.append("high-semantic-overlap")
        non_refs = re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", section(text, "Non-Responsibilities"))
        dangling = sorted({ref for ref in non_refs if ref not in ids and ref not in recipe_ids})
        if dangling:
            findings.append("dangling-non-responsibility-ref")
        results.append({
            "id": skill_id,
            "permission_identity": contract["permission_identity"],
            "mutation_scope": contract["execution"]["mutation_scope"],
            "words": len(text.split()),
            "procedure_steps": len(procedure),
            "anti_triggers": anti,
            "outputs": len(contract["outputs"]),
            "hard_gates": len(contract["hard_gates"]),
            "boilerplate_line_ratio": round(shared / max(1, len(doc["lines"])), 3),
            "source_evidence_refs": len(provenance.get("source_evidence", [])),
            "canonical_units": len(provenance.get("canonical_unit_ids", [])),
            "root_atoms": len(provenance.get("root_derived_atom_ids", [])),
            "phase9_holdouts": outcomes,
            "phase9_mutation": mutation.get(skill_id, "absent"),
            "nearest_neighbours": [{"id": other_id, "jaccard": round(score, 3)} for score, other_id in neighbours],
            "dangling_refs": dangling,
            "static_findings": findings,
        })
    finding_counts = Counter(finding for item in results for finding in item["static_findings"])
    return {
        "schema_version": "2.0", "scan": "v2-1.0.0-atomic-skill-static", "skill_count": len(results),
        "release_asset_tree_sha256": load(workspace / "curation/v2/release-1.0.0/manifest.json")["release_asset_tree_sha256"],
        "finding_counts": dict(sorted(finding_counts.items())),
        "boilerplate_line_ratio_median": sorted(item["boilerplate_line_ratio"] for item in results)[len(results) // 2],
        "skills": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = scan(args.workspace_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skill_count": result["skill_count"], "finding_counts": result["finding_counts"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
