import unittest

from irrigation_agent.irrigation_guide import get_irrigation_plan
from village_hub.domain_runtime import DOMAIN_DEFINITIONS


class IrrigationAgentTests(unittest.TestCase):
    def test_irrigation_registration_asks_for_method(self):
        fields = dict(DOMAIN_DEFINITIONS["irrigation"]["fields"])
        self.assertIn("irrigation_method", fields)
        self.assertIn("drip", fields["irrigation_method"].lower())

    def test_get_irrigation_plan_returns_practical_guidance(self):
        plan = get_irrigation_plan("borewell", "tomato", "drip", "flowering")
        self.assertIn("water", plan.lower())
        self.assertIn("drip", plan.lower())


if __name__ == "__main__":
    unittest.main()
