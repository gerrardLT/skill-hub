from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from test_sdlc import SDLCBase, sdlc


class TestV22RealProjectRouting(SDLCBase):
    def test_supplier_jwt_security_remediation_routes_engineering(self):
        state = self.state()
        result = sdlc.route_task(
            state,
            "Fix supplier portal authentication because SupplierJwtUtils uses a public hard-coded fallback secret and tokens can be forged.",
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "engineering")

    def test_security_verification_routes_qa(self):
        state = self.state()
        result = sdlc.route_task(state, "对供应商 JWT 修复做安全测试和回归，验证漏洞已经被阻断")
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "qa")

    def test_secret_rotation_routes_release(self):
        state = self.state()
        result = sdlc.route_task(state, "在生产环境轮换密钥并验证 secret deployment 和回滚")
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "release")

    def test_english_security_verification_routes_qa(self):
        state = self.state()
        result = sdlc.route_task(
            state,
            "Verify the supplier JWT security fix, dependency risk, token forgery resistance, and regression safety before handoff.",
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "qa")

    def test_english_secret_rotation_deployment_routes_release(self):
        state = self.state()
        result = sdlc.route_task(
            state,
            "Rotate the supplier JWT secret and deploy it safely through production secret injection with rollback controls.",
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "release")

    def test_implementation_readiness_with_design_inputs_routes_pm(self):
        state = self.state()
        result = sdlc.route_task(
            state,
            "Validate implementation readiness of existing research, feature inventory, miniapp design, payment protocol and regulatory prerequisites before development.",
        )
        self.assertEqual(result["decision"], "route")
        self.assertEqual(result["recommended_os"], "pm")


if __name__ == "__main__":
    unittest.main()
