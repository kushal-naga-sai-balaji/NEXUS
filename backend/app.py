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

# Mount static frontend
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(frontend_dir / "index.html")
