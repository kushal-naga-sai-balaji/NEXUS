import copy
import datetime
import logging
from typing import Any, Dict, List, Optional
from backend.sample_data import SAMPLE_DEALS, GUIDED_DEMO_STEPS
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service

logger = logging.getLogger("nexus.deal_engine")

class DealEngine:
    def __init__(self):
        # In-memory storage for deals (initialized from SAMPLE_DEALS)
        self.deals: Dict[str, Dict[str, Any]] = {d["id"]: copy.deepcopy(d) for d in SAMPLE_DEALS}

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

        elif action == "tactical_objection":
            obj_input = matched_step["objection_input"]
            res = self.coach_objection(deal_id=deal_id, objection_text=obj_input)
            return {
                "step": step_number,
                "title": matched_step["title"],
                "scenario": matched_step["scenario"],
                "action_type": action,
                "objection_input": obj_input,
                "data": res
            }

        elif action == "pre_call_brief":
            res = self.generate_briefing(
                deal_id=deal_id,
                stakeholder_name=matched_step["stakeholder"],
                call_type=matched_step["call_type"]
            )
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

deal_engine = DealEngine()
