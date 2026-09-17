import unittest

from livelihoods_agent.livelihoods_guide import get_livelihood_update
from village_hub.domain_runtime import DOMAIN_DEFINITIONS


class LivelihoodsAgentTests(unittest.TestCase):
    def test_livelihoods_registration_asks_for_work_type(self):
        fields = dict(DOMAIN_DEFINITIONS["livelihoods"]["fields"])
        self.assertIn("work_type", fields)
        self.assertIn("tailor", fields["work_type"].lower())

    def test_get_livelihood_update_mentions_local_opportunity(self):
        update = get_livelihood_update("tailor", "market", "women")
        self.assertIn("market", update.lower())
        self.assertIn("local", update.lower())


if __name__ == "__main__":
    unittest.main()
