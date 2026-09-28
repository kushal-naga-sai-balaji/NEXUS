import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.config import settings
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service
from backend.deal_engine import deal_engine
from backend.loki_engine import loki_engine
from backend.sample_data import LEARNING_CURVE_STAGES, ENTERPRISE_ARTIFACTS

app = FastAPI(
    title="Nexus Deal Intelligence API",
    description="Autonomous B2B Deal Intelligence Copilot powered by Vectorize Hindsight Biomimetic Memory",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class InteractionRequest(BaseModel):
    transcript: str
    interaction_type: str = "Meeting Transcript"
    stakeholder_name: Optional[str] = None

class BriefingRequest(BaseModel):
    stakeholder_name: str
    call_type: str = "Strategic Review"

class ObjectionRequest(BaseModel):
    objection_text: str

class RetainRequest(BaseModel):
    bank_id: str
    content: str
    tier: str = "Experience"
    node_type: str = "experience"
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class RecallRequest(BaseModel):
    bank_id: str
    query: str
    types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    max_results: int = 5

class ReflectRequest(BaseModel):
    bank_id: str
    query: str
    context: Optional[str] = None

class SettingsUpdateRequest(BaseModel):
    hindsight_api_key: Optional[str] = None
    hindsight_base_url: Optional[str] = None
    groq_api_key: Optional[str] = None

class MeetingRequest(BaseModel):
    transcript: str
    interaction_type: str = "Meeting Transcript"
    stakeholder_name: Optional[str] = None

class FollowupDraftRequest(BaseModel):
    stakeholder_name: str
    topic: str

class CRMSearchRequest(BaseModel):
    query: str

class LearningFeedbackRequest(BaseModel):
    tier: str = "Observation"
    category: str = "Tactical Learning"
    insight: str
    promote_global: bool = False

class CompareRequest(BaseModel):
    benchmark_deal_id: Optional[str] = None

class TaskStatusRequest(BaseModel):
    status: str

class TaskCreateRequest(BaseModel):
    deal_id: str
    customer: str
    title: str
    priority: str = "Important"
    badge_color: str = "amber"
    due_date: str = "Tomorrow"
    assigned_to: str = "Sarah Jenkins"
    source: str = "Manual Entry"

class MeetingSummaryApproveRequest(BaseModel):
    meeting_type: str = "Executive Solution Review"
    stakeholder: str = "Rohan Sharma (CTO)"
    key_discussion: str
    customer_requirements: List[str] = []
    objections: List[str] = []
    decisions: List[str] = []
    action_items: List[str] = []
    commitments: List[str] = []

class LokiQueryRequest(BaseModel):
    query: str
    deal_id: Optional[str] = "deal-abc-security"
    mode: Optional[str] = "deal"
    context: Optional[List[Dict[str, str]]] = None

class LokiWhyRequest(BaseModel):
    deal_id: Optional[str] = "deal-abc-security"
    insight_topic: Optional[str] = ""
    text: Optional[str] = ""

class LokiResearchRequest(BaseModel):
    query: str
    deal_id: Optional[str] = "deal-abc-security"

# API ENDPOINTS
@app.get("/api/health")
def get_health():
    return {
        "status": "healthy",
        "hindsight": {
            "connection_status": hindsight_service.connection_status,
            "is_cloud_active": hindsight_service.is_cloud_active,
            "base_url": settings.HINDSIGHT_BASE_URL,
            "has_api_key": bool(settings.HINDSIGHT_API_KEY)
        },
        "llm": {
            "has_groq": llm_service.groq_client is not None,
            "model": settings.GROQ_MODEL
        }
    }

@app.get("/api/deals")
def list_deals():
    return deal_engine.list_deals()

@app.get("/api/deals/{deal_id}")
def get_deal(deal_id: str):
    deal = deal_engine.get_deal(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@app.post("/api/deals")
def create_deal(deal_data: Dict[str, Any]):
    return deal_engine.create_deal(deal_data)

@app.post("/api/deals/{deal_id}/interact")
def process_deal_interaction(deal_id: str, req: InteractionRequest):
    try:
        return deal_engine.process_interaction(
            deal_id=deal_id,
            transcript=req.transcript,
            interaction_type=req.interaction_type,
            stakeholder_name=req.stakeholder_name
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/brief")
def generate_deal_briefing(deal_id: str, req: BriefingRequest):
    try:
        return deal_engine.generate_briefing(
            deal_id=deal_id,
            stakeholder_name=req.stakeholder_name,
            call_type=req.call_type
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/coach")
def coach_deal_objection(deal_id: str, req: ObjectionRequest):
    try:
        return deal_engine.coach_objection(
            deal_id=deal_id,
            objection_text=req.objection_text
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/reflect")
def reflect_deal_strategy(deal_id: str, req: ReflectRequest):
    deal = deal_engine.get_deal(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return hindsight_service.reflect(
        bank_id=deal["bank_id"],
        query=req.query,
        context=req.context
    )

# ==================== 16 CORE DEAL INTELLIGENCE ENDPOINTS ====================

# 1. 🧠 Deal Memory
@app.get("/api/deals/{deal_id}/memory")
def get_deal_memory(deal_id: str):
    try:
        return deal_engine.get_deal_memory(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 2. 📋 Instant Deal Summary
@app.get("/api/deals/{deal_id}/summary")
def get_instant_summary(deal_id: str):
    try:
        return deal_engine.get_instant_summary(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 3. 🎯 Next-Best Action
@app.get("/api/deals/{deal_id}/next-actions")
def get_next_actions(deal_id: str):
    try:
        return deal_engine.get_next_actions(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 4. 💬 Objection Intelligence
@app.get("/api/deals/{deal_id}/objections")
def get_deal_objections(deal_id: str):
    try:
        return deal_engine.get_objections(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/objections/coach")
def coach_objection_alias(deal_id: str, req: ObjectionRequest):
    try:
        return deal_engine.coach_objection(deal_id, req.objection_text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 5. 🏆 Winning Pattern Detection
@app.get("/api/deals/{deal_id}/winning-patterns")
def get_winning_patterns(deal_id: str):
    try:
        return deal_engine.get_winning_patterns(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 6. 👥 Stakeholder Intelligence
@app.get("/api/deals/{deal_id}/stakeholders")
def get_deal_stakeholders(deal_id: str):
    try:
        return deal_engine.get_stakeholders(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 7. 🥊 Competitor Tracking
@app.get("/api/deals/{deal_id}/competitors")
def get_deal_competitors(deal_id: str):
    try:
        return deal_engine.get_competitors(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 8. 💰 Pricing Intelligence
@app.get("/api/deals/{deal_id}/pricing")
def get_deal_pricing(deal_id: str):
    try:
        return deal_engine.get_pricing_intelligence(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 9. 📞 Meeting Intelligence
@app.post("/api/deals/{deal_id}/meetings/analyze")
def analyze_deal_meeting(deal_id: str, req: MeetingRequest):
    try:
        return deal_engine.analyze_meeting_intelligence(
            deal_id=deal_id,
            transcript=req.transcript,
            interaction_type=req.interaction_type,
            stakeholder_name=req.stakeholder_name
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 10. 🔮 Deal Risk Detection
@app.get("/api/deals/{deal_id}/risks")
def get_deal_risks(deal_id: str):
    try:
        return deal_engine.get_deal_risks(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 11. 📈 Deal Progress Tracking
@app.get("/api/deals/{deal_id}/progress")
def get_deal_progress(deal_id: str):
    try:
        return deal_engine.get_deal_progress(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 12. 🔔 Follow-up Intelligence
@app.get("/api/deals/{deal_id}/follow-ups")
def get_deal_follow_ups(deal_id: str):
    try:
        return deal_engine.get_follow_ups(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/follow-ups/draft")
def draft_deal_follow_up(deal_id: str, req: FollowupDraftRequest):
    try:
        return deal_engine.draft_follow_up(deal_id, req.stakeholder_name, req.topic)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 13. 🔍 CRM Knowledge Search
@app.post("/api/deals/{deal_id}/search")
def search_crm_knowledge(deal_id: str, req: CRMSearchRequest):
    try:
        return deal_engine.search_crm_knowledge(deal_id, req.query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 14. 🤝 Personalized Sales Strategy
@app.get("/api/deals/{deal_id}/strategy")
def get_deal_strategy(deal_id: str):
    try:
        return deal_engine.get_personalized_strategy(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 15. 📊 Deal Comparison
@app.get("/api/deals/{deal_id}/compare")
def compare_deal_default(deal_id: str):
    try:
        return deal_engine.compare_deals(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/deals/{deal_id}/compare")
def compare_deal_custom(deal_id: str, req: CompareRequest):
    try:
        return deal_engine.compare_deals(deal_id, req.benchmark_deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 16. 🧬 Persistent Learning
@app.get("/api/deals/{deal_id}/learning")
def get_deal_learning(deal_id: str):
    return deal_engine.get_persistent_learning(deal_id)

@app.post("/api/deals/{deal_id}/learning/feedback")
def submit_learning_feedback(deal_id: str, req: LearningFeedbackRequest):
    return deal_engine.record_learning_feedback(deal_id, req.dict())

@app.get("/api/learning/historical")
def get_historical_deals():
    return deal_engine.historical_deals


@app.get("/api/hindsight/graph")
def get_memory_graph(bank_id: Optional[str] = None):
    return hindsight_service.get_memory_graph(bank_id=bank_id)

@app.post("/api/hindsight/retain")
def retain_memory(req: RetainRequest):
    return hindsight_service.retain(
        bank_id=req.bank_id,
        content=req.content,
        tier=req.tier,
        node_type=req.node_type,
        tags=req.tags,
        metadata=req.metadata
    )

@app.post("/api/hindsight/recall")
def recall_memory(req: RecallRequest):
    return hindsight_service.recall(
        bank_id=req.bank_id,
        query=req.query,
        types=req.types,
        tags=req.tags,
        max_results=req.max_results
    )

@app.post("/api/hindsight/reflect")
def reflect_custom(req: ReflectRequest):
    return hindsight_service.reflect(
        bank_id=req.bank_id,
        query=req.query,
        context=req.context
    )

@app.get("/api/contrast/{scenario_type}")
def get_contrast(scenario_type: str, deal_id: Optional[str] = "deal-acme-titan"):
    deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
    return llm_service.generate_contrast(scenario_type, deal)

@app.api_route("/api/demo/step/{step_number}", methods=["GET", "POST"])
def run_demo_step(step_number: int):
    try:
        return deal_engine.execute_guided_step(step_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/settings/update")
def update_settings(req: SettingsUpdateRequest):
    res_hindsight = {}
    if req.hindsight_api_key is not None or req.hindsight_base_url is not None:
        res_hindsight = hindsight_service.update_credentials(
            api_key=req.hindsight_api_key or settings.HINDSIGHT_API_KEY,
            base_url=req.hindsight_base_url or settings.HINDSIGHT_BASE_URL
        )

    res_groq = {}
    if req.groq_api_key is not None:
        res_groq = llm_service.update_key(groq_key=req.groq_api_key)

    return {
        "status": "updated",
        "hindsight": res_hindsight,
        "llm": res_groq
    }

@app.get("/api/learning-curve")
def get_learning_curve():
    return LEARNING_CURVE_STAGES

@app.get("/api/artifacts")
def get_enterprise_artifacts():
    return ENTERPRISE_ARTIFACTS

# Customer Intelligence
@app.get("/api/customers")
def list_customers():
    return deal_engine.list_customers()

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    cust = deal_engine.get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust

# Task Management & Follow-ups
@app.get("/api/tasks")
def list_tasks(deal_id: Optional[str] = None):
    return deal_engine.list_tasks(deal_id=deal_id)

@app.post("/api/tasks")
def create_task(req: TaskCreateRequest):
    return deal_engine.create_task(req.dict())

@app.post("/api/tasks/{task_id}/status")
def update_task_status(task_id: str, req: TaskStatusRequest):
    try:
        return deal_engine.update_task_status(task_id, req.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Email Intelligence
@app.get("/api/emails")
def list_emails(deal_id: Optional[str] = None):
    return deal_engine.list_emails(deal_id=deal_id)

# Live Demo Script (Section 23 & 28)
@app.get("/api/demo/live-script")
def get_live_demo_script():
    return deal_engine.get_live_demo_script()

# Pre-Meeting 30-Second Deal Briefing (Section 4)
@app.get("/api/deals/{deal_id}/briefing/structured")
def get_deal_briefing_structured(deal_id: str):
    try:
        return deal_engine.get_deal_briefing_structured(deal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Post-Meeting Summary Approval & Memory Commit (Section 11, 23 & 28)
@app.post("/api/deals/{deal_id}/meeting-summary/approve")
def approve_meeting_summary(deal_id: str, req: MeetingSummaryApproveRequest):
    try:
        return deal_engine.approve_meeting_summary(deal_id, req.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== LOKI AI ASSISTANT ENDPOINTS ====================

@app.post("/api/loki/query")
def loki_query(req: LokiQueryRequest):
    return loki_engine.query(
        query_text=req.query,
        deal_id=req.deal_id or "deal-abc-security",
        mode=req.mode or "deal",
        conversation_context=req.context
    )

@app.get("/api/loki/xray/{deal_id}")
def loki_deal_xray(deal_id: str):
    return loki_engine.get_deal_xray(deal_id)

@app.get("/api/loki/connect/{deal_id}")
def loki_connect_dots(deal_id: str):
    return loki_engine.get_loki_connect(deal_id)

@app.get("/api/loki/brief/{deal_id}")
def loki_executive_brief(deal_id: str):
    return loki_engine.get_executive_brief(deal_id)

@app.post("/api/loki/why")
def loki_explain_why(req: LokiWhyRequest):
    return loki_engine.explain_why(
        deal_id=req.deal_id or "deal-abc-security",
        insight_topic=req.insight_topic or "",
        text=req.text or ""
    )

@app.post("/api/loki/research")
def loki_external_research(req: LokiResearchRequest):
    return loki_engine.research_external(
        query=req.query,
        deal_id=req.deal_id or "deal-abc-security"
    )

@app.get("/api/loki/commands")
def loki_commands():
    return loki_engine.get_supported_commands()

# Mount static frontend
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    @app.get("/")
    def serve_index():
        return FileResponse(frontend_dir / "index.html")

    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
