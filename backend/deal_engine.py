import copy
import datetime
import logging
from typing import Any, Dict, List, Optional
from backend.sample_data import (
    SAMPLE_DEALS,
    SAMPLE_CUSTOMERS,
    SAMPLE_TASKS,
    SAMPLE_EMAILS,
    LIVE_DEMO_SCRIPT,
    GUIDED_DEMO_STEPS,
    HISTORICAL_WON_DEALS,
    PERSISTENT_LEARNING_LOG
)
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service

logger = logging.getLogger("nexus.deal_engine")

class DealEngine:
    def __init__(self):
        # In-memory storage for deals, customers, tasks, emails
        self.deals: Dict[str, Dict[str, Any]] = {d["id"]: copy.deepcopy(d) for d in SAMPLE_DEALS}
        self.customers: Dict[str, Dict[str, Any]] = {c["id"]: copy.deepcopy(c) for c in SAMPLE_CUSTOMERS}
        self.tasks: List[Dict[str, Any]] = copy.deepcopy(SAMPLE_TASKS)
        self.emails: List[Dict[str, Any]] = copy.deepcopy(SAMPLE_EMAILS)
        self.live_demo_script: List[Dict[str, Any]] = copy.deepcopy(LIVE_DEMO_SCRIPT)
        self.historical_deals: List[Dict[str, Any]] = copy.deepcopy(HISTORICAL_WON_DEALS)
        self.persistent_learning: List[Dict[str, Any]] = copy.deepcopy(PERSISTENT_LEARNING_LOG)

    def list_deals(self) -> List[Dict[str, Any]]:
        return list(self.deals.values())

    def get_deal(self, deal_id: str) -> Optional[Dict[str, Any]]:
        return self.deals.get(deal_id)

    def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        deal_id = deal_data.get("id") or f"deal-{int(datetime.datetime.now().timestamp())}"
        deal_data["id"] = deal_id
        deal_data["bank_id"] = deal_data.get("bank_id") or f"nexus-{deal_id}"
        deal_data["interactions"] = deal_data.get("interactions", [])
        deal_data["stakeholders"] = deal_data.get("stakeholders", [])
        deal_data["competitors_mentioned"] = deal_data.get("competitors_mentioned", [])
        deal_data["health_score"] = deal_data.get("health_score", 70)

        self.deals[deal_id] = deal_data

        # Automatically retain initial World fact into Hindsight
        summary_text = (
            f"Account: {deal_data.get('name')}. Company: {deal_data.get('company')}. "
            f"ARR Target: ${deal_data.get('arr_target', 0):,}. Stage: {deal_data.get('stage')}. "
            f"Summary: {deal_data.get('summary', '')}"
        )
        hindsight_service.retain(
            bank_id=deal_data["bank_id"],
            content=summary_text,
            tier="World",
            node_type="fact",
            tags=["account_init", "deal_profile", "world"],
            metadata={"deal_id": deal_id}
        )

        return deal_data

    def process_interaction(
        self,
        deal_id: str,
        transcript: str,
        interaction_type: str = "Meeting Transcript",
        stakeholder_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest a sales interaction, analyze it with LLM, retain structured memories to Hindsight,
        and update the deal timeline.
        """
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # 1. Analyze interaction with LLM
        analysis = llm_service.analyze_interaction(transcript, deal)
        stakeholder = stakeholder_name or analysis.get("detected_stakeholder", "Key Executive")

        # 2. Retain extracted memories into Hindsight
        retained_nodes = []
        for mem in analysis.get("hindsight_memories_to_retain", []):
            res = hindsight_service.retain(
                bank_id=deal["bank_id"],
                content=mem.get("text", ""),
                tier=mem.get("tier", "Experience"),
                node_type=mem.get("type", "experience"),
                tags=mem.get("tags", []) + [deal_id, "interaction_ingestion"],
                metadata={"deal_id": deal_id, "interaction_type": interaction_type}
            )
            retained_nodes.append(res)

        # 3. Add to deal interactions timeline
        new_int_id = f"int-{len(deal['interactions']) + 101}"
        interaction_record = {
            "id": new_int_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "type": interaction_type,
            "stakeholder": stakeholder,
            "summary": analysis.get("summary", ""),
            "objections": analysis.get("objections", []),
            "outcome": "Intelligence ingested and retained into Hindsight Memory Bank"
        }
        deal["interactions"].insert(0, interaction_record)

        # 4. Update deal health score slightly based on sentiment
        if analysis.get("buying_signals"):
            deal["health_score"] = min(100, deal.get("health_score", 70) + 4)

        return {
            "interaction_id": new_int_id,
            "deal_id": deal_id,
            "analysis": analysis,
            "retained_memories": retained_nodes,
            "updated_health_score": deal["health_score"]
        }

    def generate_briefing(
        self,
        deal_id: str,
        stakeholder_name: str,
        call_type: str = "Strategic Review"
    ) -> Dict[str, Any]:
        """
        Recall relevant memories from Hindsight and synthesize a pre-call briefing.
        """
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # Query Hindsight memory using TEMPR search
        query = f"{stakeholder_name} {call_type} objection pricing security competitor"
        recalled = hindsight_service.recall(
            bank_id=deal["bank_id"],
            query=query,
            max_results=6,
            include_global=True
        )

        briefing = llm_service.generate_pre_call_brief(
            deal=deal,
            stakeholder_name=stakeholder_name,
            call_type=call_type,
            recalled_memories=recalled
        )

        briefing["recalled_memories"] = recalled
        briefing["deal_summary"] = {
            "name": deal["name"],
            "company": deal["company"],
            "arr_target": deal["arr_target"],
            "stage": deal["stage"]
        }
        return briefing

    def coach_objection(self, deal_id: str, objection_text: str) -> Dict[str, Any]:
        """
        Autonomous tactical objection coaching backed by Hindsight memory recall.
        """
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # Recall memories targeting this objection
        recalled = hindsight_service.recall(
            bank_id=deal["bank_id"],
            query=objection_text,
            max_results=5,
            include_global=True
        )

        coaching = llm_service.coach_objection(
            objection_text=objection_text,
            deal=deal,
            recalled_memories=recalled
        )

        coaching["recalled_memories"] = recalled
        return coaching

    def execute_guided_step(self, step_number: int) -> Dict[str, Any]:
        """
        Execute one of the curated guided demo steps for live hackathon presentations.
        """
        matched_step = next((s for s in GUIDED_DEMO_STEPS if s["step"] == step_number), None)
        if not matched_step:
            raise ValueError(f"Invalid step number: {step_number}")

        deal_id = matched_step["deal_id"]
        deal = self.get_deal(deal_id)
        action = matched_step["action"]

        if action == "ingest_meeting":
            preset = matched_step["preset_meeting"]
            res = self.process_interaction(
                deal_id=deal_id,
                transcript=preset["transcript"],
                interaction_type=preset["type"],
                stakeholder_name=preset["stakeholder"]
            )
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "data": res
            }

        elif action == "pre_call_brief":
            res = self.get_deal_briefing_structured(deal_id)
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "data": res
            }

        elif action == "live_call_stream":
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "data": self.live_demo_script
            }

        elif action == "tactical_objection":
            obj_input = matched_step.get("objection_input", "Your price is higher than Competitor X.")
            res = self.coach_objection(deal_id=deal_id, objection_text=obj_input)
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "objection_input": obj_input,
                "data": res
            }

        elif action == "meeting_summary":
            res = self.get_instant_summary(deal_id)
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "data": res
            }

        elif action == "trigger_reflection":
            res = hindsight_service.reflect(
                bank_id=deal["bank_id"],
                query="Synthesize enterprise win-loss patterns, competitor counter-playbooks, and pricing concession elasticity."
            )
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "data": res
            }

        return {"error": "Unknown action"}

    # ==================== 16 CORE DEAL INTELLIGENCE CAPABILITIES ====================

    # 1. 🧠 Deal Memory
    def get_deal_memory(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        graph = hindsight_service.get_memory_graph(bank_id=deal["bank_id"])
        nodes = graph.get("nodes", [])
        return {
            "deal_id": deal_id,
            "bank_id": deal["bank_id"],
            "deal_name": deal["name"],
            "stats": graph.get("stats", {}),
            "memories_by_tier": {
                "world": [n for n in nodes if n.get("tier") == "World"],
                "experience": [n for n in nodes if n.get("tier") == "Experience"],
                "observation": [n for n in nodes if n.get("tier") == "Observation"],
                "opinion": [n for n in nodes if n.get("tier") == "Opinion"]
            },
            "all_nodes": nodes,
            "edges": graph.get("edges", [])
        }

    # 2. 📋 Instant Deal Summary
    def get_instant_summary(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        recalled = hindsight_service.recall(
            bank_id=deal["bank_id"],
            query=f"{deal['name']} {deal['stage']} pricing objections competitor",
            max_results=6,
            include_global=True
        )
        summary_data = llm_service.generate_instant_deal_summary(deal, recalled)
        summary_data["recalled_memories"] = recalled
        return summary_data

    # 3. 🎯 Next-Best Action
    def get_next_actions(self, deal_id: str) -> List[Dict[str, Any]]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return llm_service.synthesize_next_best_actions(deal)

    # 4. 💬 Objection Intelligence
    def get_objections(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        
        extracted_objections = []
        for inter in deal.get("interactions", []):
            for obj in inter.get("objections", []):
                extracted_objections.append({
                    **obj,
                    "interaction_date": inter.get("date"),
                    "stakeholder": inter.get("stakeholder"),
                    "interaction_type": inter.get("type")
                })
        
        return {
            "deal_id": deal_id,
            "total_objections": len(extracted_objections),
            "objections": extracted_objections,
            "suggested_presets": [
                "Datadog offered us a 32% discount to renew. Unless you match their $450k price, we cannot justify switching.",
                "How can you guarantee our customer data in your memory banks won't leak into other clients' agent sessions or train public models?",
                "We already have an in-house engineering team building custom LangChain RAG on Postgres. Why shouldn't we keep that?"
            ]
        }

    # 5. 🏆 Winning Pattern Detection
    def get_winning_patterns(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        patterns = deal.get("winning_patterns", [])
        return {
            "deal_id": deal_id,
            "deal_name": deal["name"],
            "matched_patterns_count": len(patterns),
            "patterns": patterns,
            "historical_sources": self.historical_deals
        }

    # 6. 👥 Stakeholder Intelligence
    def get_stakeholders(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return {
            "deal_id": deal_id,
            "deal_name": deal["name"],
            "stakeholders": deal.get("stakeholders", [])
        }

    # 7. 🥊 Competitor Tracking
    def get_competitors(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return {
            "deal_id": deal_id,
            "deal_name": deal["name"],
            "competitors": deal.get("competitors_mentioned", [])
        }

    # 8. 💰 Pricing Intelligence
    def get_pricing_intelligence(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        pricing = deal.get("pricing_details", {
            "arr_target": deal.get("arr_target", 0),
            "list_price": deal.get("arr_target", 0) * 1.1,
            "competitor_offer": deal.get("arr_target", 0) * 0.7,
            "margin_saved": 0,
            "concessions_log": []
        })
        return {
            "deal_id": deal_id,
            "deal_name": deal["name"],
            "pricing": pricing
        }

    # 9. 📞 Meeting Intelligence
    def analyze_meeting_intelligence(
        self,
        deal_id: str,
        transcript: str,
        interaction_type: str = "Meeting Transcript",
        stakeholder_name: Optional[str] = None
    ) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        
        meeting_intel = llm_service.extract_meeting_intelligence(transcript, deal)
        
        # Also ingest interaction through deal engine pipeline to retain Hindsight memory
        ingest_res = self.process_interaction(
            deal_id=deal_id,
            transcript=transcript,
            interaction_type=interaction_type,
            stakeholder_name=stakeholder_name or meeting_intel.get("detected_stakeholder")
        )
        
        meeting_intel["ingest_result"] = ingest_res
        return meeting_intel

    # 10. 🔮 Deal Risk Detection
    def get_deal_risks(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return llm_service.detect_deal_risks(deal)

    # 11. 📈 Deal Progress Tracking
    def get_deal_progress(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        milestones = deal.get("milestones", [])
        completed = len([m for m in milestones if m.get("status") == "Completed"])
        total = len(milestones) if milestones else 6
        pct = int((completed / total) * 100) if total else 0
        return {
            "deal_id": deal_id,
            "deal_name": deal["name"],
            "current_stage": deal.get("stage", "Proposal"),
            "health_score": deal.get("health_score", 80),
            "milestones": milestones,
            "completion_percentage": pct,
            "velocity_status": "On Track" if pct >= 30 else "Requires Acceleration",
            "cycle_days": 48
        }

    # 12. 🔔 Follow-up Intelligence
    def get_follow_ups(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return {
            "deal_id": deal_id,
            "follow_ups": deal.get("follow_ups", [])
        }

    def draft_follow_up(self, deal_id: str, stakeholder_name: str, topic: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return llm_service.generate_followup_draft(deal, stakeholder_name, topic)

    # 13. 🔍 CRM Knowledge Search
    def search_crm_knowledge(self, deal_id: str, query: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        recalled = hindsight_service.recall(
            bank_id=deal["bank_id"],
            query=query,
            max_results=5,
            include_global=True
        )
        return llm_service.answer_crm_query(query, deal, recalled)

    # 14. 🤝 Personalized Sales Strategy
    def get_personalized_strategy(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        return llm_service.generate_personalized_strategy(
            deal=deal,
            stakeholders=deal.get("stakeholders", []),
            competitors=deal.get("competitors_mentioned", []),
            winning_patterns=deal.get("winning_patterns", [])
        )

    # 15. 📊 Deal Comparison
    def compare_deals(self, deal_id: str, benchmark_deal_id: Optional[str] = None) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")
        
        benchmark = None
        if benchmark_deal_id:
            benchmark = next((d for d in self.historical_deals if d["id"] == benchmark_deal_id), None)
        if not benchmark and self.historical_deals:
            benchmark = self.historical_deals[0]
            
        return {
            "comparison": llm_service.compare_deals_llm(deal, benchmark),
            "available_historical_deals": self.historical_deals
        }

    # 16. 🧬 Persistent Learning
    def get_persistent_learning(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        return {
            "deal_id": deal_id if deal else None,
            "learning_log": self.persistent_learning,
            "global_bank_id": "global-nexus-sales-intel",
            "active_rules_count": len(self.persistent_learning),
            "status": "Continuous Biomimetic Reflection Active"
        }

    def record_learning_feedback(self, deal_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        new_insight = {
            "id": f"learn-{len(self.persistent_learning) + 1:02d}",
            "tier": feedback_data.get("tier", "Observation"),
            "category": feedback_data.get("category", "Tactical Learning"),
            "insight": feedback_data.get("insight", "User documented outcome from resolved negotiation."),
            "deals_synthesized": 1,
            "status": "Promoted to Global Playbook" if feedback_data.get("promote_global") else "Active Learning",
            "confidence": 0.95
        }
        self.persistent_learning.insert(0, new_insight)
        
        # Also retain into Hindsight global bank
        if deal:
            hindsight_service.retain(
                bank_id="global-nexus-sales-intel",
                content=new_insight["insight"],
                tier=feedback_data.get("tier", "Observation"),
                node_type="opinion" if feedback_data.get("tier") == "Opinion" else "observation",
                tags=["user_feedback", "learned_tactic", feedback_data.get("category", "sales_intel").lower().replace(" ", "_")]
            )
            
        return {
            "status": "recorded",
            "new_insight": new_insight,
            "total_insights": len(self.persistent_learning)
        }

    # Customer Intelligence
    def list_customers(self) -> List[Dict[str, Any]]:
        return list(self.customers.values())

    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        return self.customers.get(customer_id)

    # Task Management & Follow-ups
    def list_tasks(self, deal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if deal_id:
            return [t for t in self.tasks if t.get("deal_id") == deal_id]
        return self.tasks

    def update_task_status(self, task_id: str, status: str) -> Dict[str, Any]:
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task["status"] = status
        return task

    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task_data.get("id") or f"task-{len(self.tasks) + 1}"
        task_data["id"] = task_id
        task_data["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tasks.insert(0, task_data)
        return task_data

    # Email Intelligence
    def list_emails(self, deal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if deal_id:
            return [e for e in self.emails if e.get("deal_id") == deal_id]
        return self.emails

    # Live Demo Conversation Script
    def get_live_demo_script(self) -> List[Dict[str, Any]]:
        return self.live_demo_script

    # Structured 30-Second Pre-Meeting Deal Briefing (Section 4)
    def get_deal_briefing_structured(self, deal_id: str) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # Compile concise briefing from persistent deal state
        return {
            "deal_id": deal_id,
            "customer": deal.get("company", deal.get("name")),
            "deal_stage": deal.get("stage", "Negotiation"),
            "deal_value": deal.get("deal_value_display", f"₹{deal.get('arr_target', 0):,}"),
            "arr_target": deal.get("arr_target", 0),
            "key_requirements": [
                r.get("title") for r in deal.get("requirements", [])
            ] or ["Enterprise security & SOC2", "Deployment before December", "24/7 support SLA"],
            "previous_objections": [
                o.get("objection", o.get("name", "Pricing objection")) for o in deal.get("objections", [])
            ] or ["Pricing pressure vs Competitor X", "Implementation timeline"],
            "competitors": [
                c.get("name") for c in deal.get("competitors_mentioned", [])
            ] or ["Competitor X"],
            "decision_makers": [
                f"{s.get('name')} ({s.get('role')})" for s in deal.get("stakeholders", [])
                if "Decision" in s.get("influence", "") or "High" in s.get("influence", "")
            ] or ["Rohan Sharma (CTO)", "Anita Roy (CFO)"],
            "previous_commitments": [
                "Send 24-month TCO comparison model",
                "Reserve November engineering deployment slot",
                "Formalize 24/7 support tier SLA"
            ],
            "recommended_focus": "Address pricing through ROI and total cost of ownership. Do not compete on raw discount; frame the 74% MTTR reduction vs engineering maintenance toil.",
            "deal_health": deal.get("health_score", 82),
            "risk": "Medium — pricing objection unresolved; Competitor X actively positioning 15% discount.",
            "source": "Persistent Deal Memory (Hindsight Biomimetic Graph)"
        }

    # Post-Meeting Summary Approval & Memory Commit (Section 11, 23 & 28)
    def approve_meeting_summary(self, deal_id: str, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        deal = self.get_deal(deal_id)
        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # 1. Append meeting to deal interactions
        new_int_id = f"int-{len(deal.get('interactions', [])) + 101}"
        new_interaction = {
            "id": new_int_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "type": summary_data.get("meeting_type", "Executive Solution Review"),
            "stakeholder": summary_data.get("stakeholder", "Rohan Sharma (CTO)"),
            "summary": summary_data.get("key_discussion", "Negotiation call confirming ₹25L ARR tied to 24/7 support and December deadline."),
            "objections": summary_data.get("objections", ["Pricing vs Competitor X"]),
            "outcome": "Customer confirmed commitment to proceed upon proposal delivery."
        }
        deal["interactions"].insert(0, new_interaction)

        # 2. Add any newly extracted requirements to deal requirements
        for req_title in summary_data.get("customer_requirements", []):
            if not any(r.get("title") == req_title for r in deal.get("requirements", [])):
                deal["requirements"].append({
                    "id": f"req-{len(deal['requirements']) + 1}",
                    "title": req_title,
                    "status": "Validated",
                    "priority": "High"
                })

        # 3. Create follow-up tasks from action items
        created_tasks = []
        for item in summary_data.get("action_items", []):
            new_task = {
                "id": f"task-{len(self.tasks) + 1}",
                "deal_id": deal_id,
                "customer": deal.get("company", deal.get("name")),
                "title": item if isinstance(item, str) else item.get("title", "Follow up"),
                "priority": "Critical" if "proposal" in str(item).lower() or "cfo" in str(item).lower() else "Important",
                "badge_color": "rose" if "proposal" in str(item).lower() else "amber",
                "due_date": "Within 48 hours",
                "status": "In Progress",
                "assigned_to": "Sarah Jenkins",
                "source": "Approved Meeting Intelligence"
            }
            self.tasks.insert(0, new_task)
            created_tasks.append(new_task)

        # 4. Retain into Hindsight memory
        hindsight_service.retain(
            bank_id=deal["bank_id"],
            content=f"Post-Meeting Summary: {summary_data.get('key_discussion', '')}. Customer committed to ₹25L ARR with 24/7 support SLA.",
            tier="Experience",
            node_type="experience",
            tags=["approved_meeting_summary", "deal_advancement", "tco_defense", "december_deadline"]
        )

        return {
            "status": "success",
            "message": "Meeting summary approved and committed to Persistent Deal Memory.",
            "deal_id": deal_id,
            "interaction_id": new_int_id,
            "new_tasks_created": created_tasks,
            "total_deal_requirements": len(deal.get("requirements", []))
        }

deal_engine = DealEngine()
