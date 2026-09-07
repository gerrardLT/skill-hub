from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "external-skills.json"
INSTALLER = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "install_external_skills.py"


class TestV24SkillComposition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def skills(self, os_name: str, tier: str | None = None):
        items = [x for x in self.manifest["skills"] if x["os"] == os_name]
        if tier:
            items = [x for x in items if x["tier"] == tier]
        return items

    def dry_run(self, *args: str):
        result = subprocess.run(
            [sys.executable, str(INSTALLER), *args, "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_design_core_is_layered_and_nonduplicative(self):
        core = {x["skill"] for x in self.skills("design", "core")}
        self.assertEqual(core, {"impeccable", "ui-ux-pro-max", "web-design-guidelines", "review-animations"})
        self.assertNotIn("frontend-design", core)
        self.assertNotIn("design-taste-frontend", core)

    def test_qa_core_preserves_independent_verification(self):
        core = {x["skill"] for x in self.skills("qa", "core")}
        self.assertEqual(core, {"testing-strategy", "verification-before-completion", "qa-only", "code-review", "playwright"})
        self.assertTrue({"test-driven-development", "systematic-debugging", "qa"}.isdisjoint(core))
        text = (ROOT / "skills" / "qa-operating-system" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不得修改产品源码", text)
        self.assertIn("独立 QA", text)

    def test_evolution_core_is_vendor_neutral(self):
        core = self.skills("evolution", "core")
        names = {x["skill"] for x in core}
        self.assertEqual(names, {
            "systematic-debugging", "incident-response", "metrics-review",
            "analyzing-user-feedback", "validate-data", "craft-experiment-design",
        })
        vendor_terms = ("sentry", "datadog", "posthog")
        for item in core:
            value = (item["repo"] + " " + item["skill"]).lower()
            self.assertFalse(any(term in value for term in vendor_terms), value)
        text = (ROOT / "skills" / "evolution-operating-system" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Provider Adapter", text)

    def test_provider_adapters_are_explicit_evolution_only(self):
        adapters = self.manifest.get("provider_adapters", [])
        self.assertEqual({x["provider"] for x in adapters}, {"sentry", "datadog", "posthog"})
        self.assertTrue(all(x["os"] == "evolution" for x in adapters))
        self.assertEqual(len(adapters), 11)

    def test_installer_without_provider_never_selects_adapter(self):
        payload = self.dry_run("--os", "evolution", "--profile", "core")
        self.assertEqual(payload["providers"], [])
        self.assertTrue(all(not x.get("provider") for x in payload["selection"]))
        self.assertEqual(len(payload["selection"]), 6)

    def test_datadog_core_adapter_is_bounded(self):
        payload = self.dry_run("--os", "evolution", "--profile", "core", "--provider", "datadog")
        provider = [x for x in payload["selection"] if x.get("provider")]
        self.assertEqual({x["skill"] for x in provider}, {"dd-logs", "dd-apm"})
        self.assertTrue(all(x["provider"] == "datadog" for x in provider))
        self.assertFalse(any(x.get("provider") in {"sentry", "posthog"} for x in payload["selection"]))

    def test_sentry_plugin_is_agent_specific_and_fail_closed(self):
        generic = self.dry_run("--os", "evolution", "--profile", "core", "--provider", "sentry")
        sentry_generic = next(x for x in generic["selection"] if x.get("provider") == "sentry")
        self.assertIn("no automated plugin installer", sentry_generic["skipped_reason"])

        codex = self.dry_run("--os", "evolution", "--profile", "core", "--provider", "sentry", "--agent", "codex", "--allow-custom")
        sentry_codex = next(x for x in codex["selection"] if x.get("provider") == "sentry")
        self.assertIn("codex plugin marketplace add getsentry/plugin-codex", sentry_codex["resolved_install"])
        self.assertEqual(sentry_codex["skipped_reason"], "")

    def test_provider_rejected_for_non_evolution_os(self):
        result = subprocess.run(
            [sys.executable, str(INSTALLER), "--os", "qa", "--profile", "core", "--provider", "posthog", "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("provider", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
