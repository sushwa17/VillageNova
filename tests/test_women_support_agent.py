import unittest

from women_support.support_guide import get_support_update
from village_hub.domain_runtime import DOMAIN_DEFINITIONS


class WomenSupportAgentTests(unittest.TestCase):
    def test_women_support_registration_asks_for_support_type(self):
        fields = dict(DOMAIN_DEFINITIONS["women"]["fields"])
        self.assertIn("support_type", fields)
        self.assertIn("safety", fields["support_type"].lower())

    def test_get_support_update_mentions_actionable_support(self):
        update = get_support_update("health", "SHG", "safety")
        self.assertIn("support", update.lower())
        self.assertIn("local", update.lower())


if __name__ == "__main__":
    unittest.main()
