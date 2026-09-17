import unittest

from education_agent.ai_guide import get_ai_update
from village_hub.domain_runtime import DOMAIN_DEFINITIONS


class EducationAgentTests(unittest.TestCase):
    def test_education_registration_asks_for_ai_focus(self):
        fields = dict(DOMAIN_DEFINITIONS["education"]["fields"])
        self.assertIn("ai_focus", fields)
        self.assertIn("ai", fields["ai_focus"].lower())

    def test_get_ai_update_mentions_school_innovation(self):
        update = get_ai_update("Govt School", "student", "chatbot")
        self.assertIn("AI", update)
        self.assertIn("school", update.lower())


if __name__ == "__main__":
    unittest.main()
