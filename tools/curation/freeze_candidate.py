"""Create a deterministic SHA-256 manifest for a candidate directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def freeze(root: Path, workspace: Path) -> dict[str, object]:
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        files.append({
            "path": path.resolve().relative_to(workspace.resolve()).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    if not files:
        raise ValueError("candidate directory has no files")
    return {"schema_version": "1.0", "candidate_root": root.resolve().relative_to(workspace.resolve()).as_posix(), "files": files}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = freeze(args.root, args.workspace)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
