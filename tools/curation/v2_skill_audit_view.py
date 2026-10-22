#!/usr/bin/env python3
"""Print a compact review view of V2 Skills: skill-specific lines only, plus top source ranges."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_excerpt(workspace: Path, ref: str, limit: int) -> str:
    match = re.match(r"(.+):(\d+)-(\d+)$", ref)
    if not match:
        return f"[unparsed ref {ref}]"
    path = workspace / "skills" / match.group(1)
    if not path.is_file():
        return f"[missing {path.as_posix()}]"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start, end = int(match.group(2)), int(match.group(3))
    text = " ".join(line.strip() for line in lines[start - 1:end] if line.strip())
    return text[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--batch", required=True)
    parser.add_argument("--sources", type=int, default=2)
    parser.add_argument("--chars", type=int, default=700)
    args = parser.parse_args()
    workspace = args.workspace_root.resolve()
    catalog = load(workspace / "slots/v2/catalog.json")
    counts: Counter[str] = Counter()
    texts = {}
    for item in catalog["skills"]:
        text = (workspace / item["path"] / "SKILL.md").read_text(encoding="utf-8")
        texts[item["id"]] = text
        counts.update({line.strip() for line in text.splitlines() if line.strip()})
    batch = load(workspace / "curation/v2/skill-audit/batches" / f"{args.batch}.json")
    for item in batch["skills"]:
        skill_id = item["id"]; root = workspace / item["path"]
        contract = load(root / "contract.json"); provenance = load(root / "provenance.json")["candidate_provenance"]
        static = item["static"]
        print(f"\n===== {skill_id} | {contract['permission_identity']} / {contract['execution']['mutation_scope']}")
        print(f"phase9 holdouts={static['phase9_holdouts']} mutation={static['phase9_mutation']} nn={[(n['id'], n['jaccard']) for n in static['nearest_neighbours'][:2]]}")
        for number, line in enumerate(texts[skill_id].splitlines(), 1):
            stripped = line.strip()
            if not stripped or counts[stripped] >= 5 or stripped.startswith("---") or stripped.startswith("name:"):
                continue
            if stripped.startswith("description:"):
                continue
            print(f"{number:>3}: {stripped}")
        refs = sorted(provenance.get("source_evidence", []), key=lambda ref: -(int(ref.rsplit("-", 1)[-1]) - int(ref.rsplit(":", 1)[-1].split("-")[0])) if re.search(r":\d+-\d+$", ref) else 0)
        print(f"sources: {len(refs)} refs; units={len(provenance.get('canonical_unit_ids', []))} atoms={len(provenance.get('root_derived_atom_ids', []))}")
        for ref in refs[: args.sources]:
            print(f"  SRC {ref}: {source_excerpt(workspace, ref, args.chars)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
