#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

env = dict(os.environ)
env["PYTHONPATH"] = str(ROOT / "src")
raise SystemExit(subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, env=env).returncode)
