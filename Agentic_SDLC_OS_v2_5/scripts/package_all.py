#!/usr/bin/env python3
"""Package every Skill and create an aggregate archive plus checksums."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGER = Path("/home/oai/skills/skill-creator/scripts/package_skill.py")
DIST = ROOT / "dist"


def clean_caches() -> None:
    for path in ROOT.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
    for path in ROOT.rglob("*.pyc"):
        path.unlink(missing_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    clean_caches()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    failures = []
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        out = DIST / skill.name
        result = subprocess.run(
            [sys.executable, str(PACKAGER), str(skill), str(out)],
            check=False,
        )
        if result.returncode != 0:
            failures.append(skill.name)
    if failures:
        print("Packaging failed: " + ", ".join(failures), file=sys.stderr)
        return 1

    bundle = DIST / "agentic-sdlc-os-all-skills.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for archive in sorted(DIST.glob("*/skill.zip")):
            zf.write(archive, archive.relative_to(DIST))

    archives = [*sorted(DIST.glob("*/skill.zip")), bundle]
    checksums = DIST / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.relative_to(DIST).as_posix()}\n" for path in archives),
        encoding="utf-8",
    )
    print(bundle)
    print(checksums)
    return 0


if __name__ == "__main__":
    sys.exit(main())
