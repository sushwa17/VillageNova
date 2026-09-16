import unittest

from cattle_agent.nutrition_guide import get_nutrition_plan
from village_hub.domain_runtime import DOMAIN_DEFINITIONS


class CattleAgentNutritionTests(unittest.TestCase):
    def test_cattle_registration_asks_for_cattle_type(self):
        fields = dict(DOMAIN_DEFINITIONS["cattle"]["fields"])
        self.assertIn("cattle_type", fields)
        self.assertIn("cow", fields["cattle_type"].lower())

    def test_get_nutrition_plan_returns_food_guidance(self):
        plan = get_nutrition_plan("cow", "milk")
        self.assertIn("green fodder", plan.lower())
        self.assertIn("roughage", plan.lower())


if __name__ == "__main__":
    unittest.main()
