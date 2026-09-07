from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestInstallers(unittest.TestCase):
    def test_external_dry_run_json(self):
        script = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "install_external_skills.py"
        result = subprocess.run(
            [sys.executable, str(script), "--os", "pm", "--profile", "core", "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["selection"]), 5)
        self.assertTrue(all(x["tier"] == "core" for x in payload["selection"]))

    def test_external_custom_is_skipped_without_flag(self):
        script = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "install_external_skills.py"
        result = subprocess.run(
            [sys.executable, str(script), "--os", "release", "--profile", "core", "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        gstack = next(x for x in payload["selection"] if x["repo"] == "garrytan/gstack")
        self.assertIn("--allow-custom", gstack["skipped_reason"])

    def test_local_install_dry_run(self):
        script = ROOT / "scripts" / "install_local_skills.py"
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(script), "--project", tmp, "--agent", "generic", "--dry-run"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("agentic-sdlc-os", result.stdout)
            self.assertFalse((Path(tmp) / ".agents" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
