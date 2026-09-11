import unittest

from ai_hardware_copilot.config import load_yaml
from ai_hardware_copilot.model_router import ModelRoutingPolicy

from .common import ROOT, product_task


class ModelRouterTests(unittest.TestCase):
    def setUp(self):
        self.policy = ModelRoutingPolicy(load_yaml(ROOT / "config" / "model_profiles.yaml"))

    def test_high_risk_synthesis_uses_maximum_profile(self):
        route = self.policy.select(product_task(risk_tier="T3"), "synthesis", active_agent_count=20)
        self.assertEqual(route.profile, "maximum")
        self.assertTrue(route.independent_review)

    def test_exact_lookup_uses_deterministic_profile(self):
        route = self.policy.select(product_task(risk_tier="T4"), "exact_lookup")
        self.assertEqual(route.profile, "deterministic")


if __name__ == "__main__":
    unittest.main()
