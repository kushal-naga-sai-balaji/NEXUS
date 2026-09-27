"""
Automated Test Suite for Nexus Deal Intelligence
Verifies Hindsight 4-Tier Memory operations, TEMPR recall, objection coaching,
briefing generation, and guided demo steps.
"""

import unittest
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service
from backend.deal_engine import deal_engine

class TestNexusDealIntelligence(unittest.TestCase):

    def setUp(self):
        self.bank_id = "nexus-deal-acme-titan"
        self.deal_id = "deal-acme-titan"

    def test_01_list_deals(self):
        deals = deal_engine.list_deals()
        self.assertGreaterEqual(len(deals), 3)
        deal_names = [d["name"] for d in deals]
        self.assertTrue(any("Acme" in n for n in deal_names))

    def test_02_hindsight_4_tier_memory_graph(self):
        graph = hindsight_service.get_memory_graph(self.bank_id)
        stats = graph.get("stats", {})
        self.assertGreater(stats.get("total_memories", 0), 0)
        self.assertGreater(stats.get("world_facts", 0), 0)
        self.assertGreater(stats.get("experiences", 0), 0)
        self.assertGreater(stats.get("observations", 0), 0)
        self.assertGreater(stats.get("opinions", 0), 0)

    def test_03_hindsight_tempr_recall(self):
        # Test TEMPR recall with Datadog pricing objection
        results = hindsight_service.recall(
            bank_id=self.bank_id,
            query="Datadog 32% discount CFO price objection",
            max_results=5
        )
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn("score", top)
        self.assertGreaterEqual(top["score"], 0.5)

    def test_04_pre_call_briefing_generation(self):
        briefing = deal_engine.generate_briefing(
            deal_id=self.deal_id,
            stakeholder_name="David Sterling",
            call_type="Executive Pricing Showdown"
        )
        self.assertIn("briefing_markdown", briefing)
        self.assertIn("David Sterling", briefing["briefing_markdown"])
        self.assertIn("Landmines", briefing["briefing_markdown"])
        self.assertIn("Winning Argument", briefing["briefing_markdown"])

    def test_05_live_objection_coaching(self):
        coaching = deal_engine.coach_objection(
            deal_id=self.deal_id,
            objection_text="Datadog offered 32% discount. Match $450k or we walk."
        )
        self.assertIn("reframe_strategy", coaching)
        self.assertIn("recommended_response", coaching)
        self.assertIn("give_get_tradeoff", coaching)
        self.assertIn("past_deal_citation", coaching)
        self.assertGreaterEqual(coaching["confidence_score"], 0.8)

    def test_06_guided_demo_steps(self):
        for step in range(1, 5):
            res = deal_engine.execute_guided_step(step)
            self.assertEqual(res["step"], step)
            self.assertIn("title", res)

    def test_07_hindsight_reflection(self):
        reflection = hindsight_service.reflect(
            bank_id=self.bank_id,
            query="Synthesize enterprise win-loss patterns and competitor counter-playbooks."
        )
        self.assertIn("key_conclusions", reflection)
        self.assertGreater(len(reflection["key_conclusions"]), 0)
        self.assertIn("recommended_playbooks", reflection)

    def test_08_learning_curve(self):
        from backend.sample_data import LEARNING_CURVE_STAGES
        self.assertEqual(len(LEARNING_CURVE_STAGES), 4)
        self.assertEqual(LEARNING_CURVE_STAGES[0]["competence"], 32)
        self.assertEqual(LEARNING_CURVE_STAGES[3]["competence"], 98)

    def test_09_enterprise_artifacts(self):
        from backend.sample_data import ENTERPRISE_ARTIFACTS
        self.assertIn("ciso_email_thread", ENTERPRISE_ARTIFACTS)
        self.assertIn("enterprise_quote_sheet", ENTERPRISE_ARTIFACTS)
        self.assertIn("competitor_teardown", ENTERPRISE_ARTIFACTS)
        self.assertIn("$650,000", ENTERPRISE_ARTIFACTS["enterprise_quote_sheet"]["effective_arr"])

if __name__ == "__main__":
    unittest.main()
