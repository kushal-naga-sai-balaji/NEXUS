"""
Automated Test Suite for Nexus Deal Intelligence
Verifies Hindsight 4-Tier Memory operations, the 16 Core Deal Intelligence Capabilities,
Customer management, Task tracking, Email intelligence, and the Live Call Demo Stream:
1. Deal Memory
2. Instant Deal Summary
3. Next-Best Action
4. Objection Intelligence
5. Winning Pattern Detection
6. Stakeholder Intelligence
7. Competitor Tracking
8. Pricing Intelligence
9. Meeting Intelligence
10. Deal Risk Detection
11. Deal Progress Tracking
12. Follow-up Intelligence
13. CRM Knowledge Search
14. Personalized Sales Strategy
15. Deal Comparison
16. Persistent Learning
17. Customer Intelligence
18. Task Management
19. Pre-Meeting 30s Briefing & Meeting Summary Approval
"""

import unittest
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service
from backend.deal_engine import deal_engine

class TestNexusDealIntelligence(unittest.TestCase):

    def setUp(self):
        self.bank_id = "nexus-deal-abc-security"
        self.deal_id = "deal-abc-security"

    def test_01_list_deals(self):
        deals = deal_engine.list_deals()
        self.assertGreaterEqual(len(deals), 4)
        deal_names = [d["name"] for d in deals]
        self.assertTrue(any("Enterprise Security" in n for n in deal_names))

    def test_02_hindsight_4_tier_memory_graph(self):
        graph = hindsight_service.get_memory_graph(self.bank_id)
        stats = graph.get("stats", {})
        self.assertGreater(stats.get("total_memories", 0), 0)
        self.assertGreater(stats.get("world_facts", 0), 0)
        self.assertGreater(stats.get("experiences", 0), 0)
        self.assertGreater(stats.get("observations", 0), 0)
        self.assertGreater(stats.get("opinions", 0), 0)

    def test_03_feature_01_deal_memory(self):
        mem = deal_engine.get_deal_memory(self.deal_id)
        self.assertEqual(mem["deal_id"], self.deal_id)
        self.assertIn("memories_by_tier", mem)
        self.assertIn("world", mem["memories_by_tier"])
        self.assertGreater(len(mem["all_nodes"]), 0)

    def test_04_feature_02_instant_deal_summary(self):
        summary = deal_engine.get_instant_summary(self.deal_id)
        self.assertIn("executive_elevator_pitch", summary)
        self.assertIn("call_readiness_score", summary)
        self.assertGreaterEqual(summary["call_readiness_score"], 70)
        self.assertIn("critical_talking_points", summary)

    def test_05_feature_03_next_best_action(self):
        actions = deal_engine.get_next_actions(self.deal_id)
        self.assertGreaterEqual(len(actions), 2)
        top = actions[0]
        self.assertIn("action", top)
        self.assertIn("priority", top)
        self.assertIn("script_template", top)

    def test_06_feature_04_objection_intelligence(self):
        objs = deal_engine.get_objections(self.deal_id)
        self.assertGreater(objs["total_objections"], 0)
        coaching = deal_engine.coach_objection(
            deal_id=self.deal_id,
            objection_text="Your price is higher than Competitor X."
        )
        self.assertIn("reframe_strategy", coaching)
        self.assertIn("recommended_response", coaching)
        self.assertIn("give_get_tradeoff", coaching)
        self.assertIn("past_deal_citation", coaching)

    def test_07_feature_05_winning_pattern_detection(self):
        patterns = deal_engine.get_winning_patterns(self.deal_id)
        self.assertGreater(patterns["matched_patterns_count"], 0)

    def test_08_feature_06_stakeholder_intelligence(self):
        stakeholders = deal_engine.get_stakeholders(self.deal_id)
        self.assertGreaterEqual(len(stakeholders["stakeholders"]), 3)
        names = [s["name"] for s in stakeholders["stakeholders"]]
        self.assertIn("Rohan Sharma", names)
        self.assertIn("Anita Roy", names)

    def test_09_feature_07_competitor_tracking(self):
        comps = deal_engine.get_competitors(self.deal_id)
        self.assertGreaterEqual(len(comps["competitors"]), 1)
        comp_x = next((c for c in comps["competitors"] if "Competitor X" in c["name"]), None)
        self.assertIsNotNone(comp_x)
        self.assertEqual(comp_x["threat_level"], "High")

    def test_10_feature_08_pricing_intelligence(self):
        pricing = deal_engine.get_pricing_intelligence(self.deal_id)
        p_data = pricing["pricing"]
        self.assertEqual(p_data["arr_target"], 300000)
        self.assertGreater(len(p_data["concessions_log"]), 0)

    def test_11_feature_09_meeting_intelligence(self):
        sample_transcript = "Rohan: We need deployment before December and 24/7 dedicated support SLA to justify ₹25L."
        result = deal_engine.analyze_meeting_intelligence(
            deal_id=self.deal_id,
            transcript=sample_transcript,
            interaction_type="Live Demo Call"
        )
        self.assertIn("decisions", result)
        self.assertIn("customer_action_items", result)
        self.assertIn("rep_action_items", result)

    def test_12_feature_10_deal_risk_detection(self):
        risks = deal_engine.get_deal_risks(self.deal_id)
        self.assertIn("overall_risk_level", risks)
        self.assertIn("risk_factors", risks)
        self.assertGreater(len(risks["risk_factors"]), 0)

    def test_13_feature_11_deal_progress_tracking(self):
        prog = deal_engine.get_deal_progress(self.deal_id)
        self.assertIn("milestones", prog)
        self.assertGreaterEqual(prog["completion_percentage"], 30)
        self.assertEqual(prog["velocity_status"], "On Track")

    def test_14_feature_12_follow_up_intelligence(self):
        fu = deal_engine.get_follow_ups(self.deal_id)
        self.assertGreater(len(fu["follow_ups"]), 0)
        draft = deal_engine.draft_follow_up(self.deal_id, "Rohan Sharma", "December Deployment Schedule & TCO Model")
        self.assertIn("Hi Rohan", draft["body"])
        self.assertIn("attachments_suggested", draft)

    def test_15_feature_13_crm_knowledge_search(self):
        res = deal_engine.search_crm_knowledge(self.deal_id, "What were the customer's main concerns?")
        self.assertIn("answer", res)
        self.assertIn("sources", res)
        self.assertGreater(len(res["sources"]), 0)

    def test_16_feature_14_personalized_sales_strategy(self):
        strat = deal_engine.get_personalized_strategy(self.deal_id)
        self.assertIn("primary_strategic_narrative", strat)
        self.assertIn("closing_blueprint", strat)
        self.assertIn("negotiation_boundary", strat)

    def test_17_feature_15_deal_comparison(self):
        comp = deal_engine.compare_deals(self.deal_id)
        self.assertIn("comparison", comp)
        self.assertIn("comparative_insights", comp["comparison"])
        self.assertGreater(len(comp["available_historical_deals"]), 0)

    def test_18_feature_16_persistent_learning(self):
        learning = deal_engine.get_persistent_learning(self.deal_id)
        self.assertGreater(learning["active_rules_count"], 0)
        
        new_feedback = deal_engine.record_learning_feedback(
            deal_id=self.deal_id,
            feedback_data={
                "tier": "Opinion",
                "category": "CTO Architectural Priority",
                "insight": "CTO Rohan values persistent session state and dedicated 24/7 SLA over raw discount.",
                "promote_global": True
            }
        )
        self.assertEqual(new_feedback["status"], "recorded")

    def test_19_guided_demo_steps(self):
        for step in range(1, 5):
            res = deal_engine.execute_guided_step(step)
            self.assertEqual(res["step"], step)
            self.assertIn("title", res)

    def test_20_customer_tasks_briefing_and_approval(self):
        # 1. Customers
        customers = deal_engine.list_customers()
        self.assertEqual(len(customers), 4)
        abc = deal_engine.get_customer("cust-abc")
        self.assertEqual(abc["name"], "ABC Technologies")

        # 2. Tasks
        tasks = deal_engine.list_tasks()
        self.assertGreaterEqual(len(tasks), 4)

        # 3. Structured 30s briefing
        briefing = deal_engine.get_deal_briefing_structured(self.deal_id)
        self.assertEqual(briefing["customer"], "ABC Technologies")
        self.assertIn("₹25,00,000", briefing["deal_value"])
        self.assertIn("Competitor X", briefing["competitors"])

        # 4. Post-Meeting summary approval
        summary_approval = deal_engine.approve_meeting_summary(
            self.deal_id,
            {
                "meeting_type": "Executive Solution Review",
                "stakeholder": "Rohan Sharma (CTO)",
                "key_discussion": "Discussed 24-month TCO and confirmed December rollout.",
                "customer_requirements": ["24/7 Enterprise Support Tier"],
                "objections": ["Pricing vs Competitor X"],
                "decisions": ["Approve ₹25L ARR upon proposal delivery"],
                "action_items": ["Send updated proposal to Rohan and Anita Roy"]
            }
        )
        self.assertEqual(summary_approval["status"], "success")
        self.assertGreaterEqual(len(summary_approval["new_tasks_created"]), 1)

    def test_loki_intelligence_engine(self):
        """Test LOKI AI Assistant endpoints, commands, X-Ray, Connect, and Why reasoning."""
        from backend.loki_engine import loki_engine

        # 1. Commands
        cmds = loki_engine.get_supported_commands()
        self.assertGreaterEqual(len(cmds), 15)

        # 2. Pin-to-Pin Deal Intelligence Report
        report = loki_engine.get_deal_intelligence_report(self.deal_id)
        self.assertIn("ABC Technologies", report["formatted_content"])
        self.assertIn("Rohan Sharma", report["formatted_content"])
        self.assertIn("Competitor X", report["formatted_content"])

        # 3. Deal X-Ray (18 Dimensions)
        xray = loki_engine.get_deal_xray(self.deal_id)
        self.assertEqual(len(xray["xray_sections"]), 18)

        # 4. LOKI Connect (Interactive flow nodes)
        connect = loki_engine.get_loki_connect(self.deal_id)
        self.assertGreaterEqual(len(connect["nodes"]), 8)

        # 5. Explain Why Root Cause Engine
        why_res = loki_engine.explain_why(self.deal_id, insight_topic="pricing risk")
        self.assertIn("Pricing", why_res["answer"])
        self.assertGreaterEqual(len(why_res["records_considered"]), 2)

        # 6. External Business Research
        research = loki_engine.research_external("Who is Competitor X?", self.deal_id)
        self.assertTrue(research.get("external_intelligence"))
        self.assertGreaterEqual(len(research.get("sources", [])), 1)

        # 7. Slash Commands
        slash_res = loki_engine.query("/risks", deal_id=self.deal_id)
        self.assertIn("pricing", slash_res["answer"].lower())

        # 8. App Knowledge
        app_res = loki_engine.query("How does NEXUS work?", deal_id=self.deal_id)
        self.assertIn("autonomous", app_res["answer"].lower())

if __name__ == "__main__":
    unittest.main()
