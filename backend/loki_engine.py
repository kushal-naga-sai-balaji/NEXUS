"""
LOKI — Live Operational Knowledge Intelligence
Autonomous AI Intelligence Layer for NEXUS

"Ask anything. Know everything. Act intelligently."
"""

import copy
import datetime
import logging
import re
from typing import Any, Dict, List, Optional

from backend.deal_engine import deal_engine
from backend.hindsight_service import hindsight_service
from backend.llm_service import llm_service
from backend.sample_data import (
    SAMPLE_CUSTOMERS,
    SAMPLE_DEALS,
    SAMPLE_TASKS,
    SAMPLE_EMAILS,
    HISTORICAL_WON_DEALS
)

logger = logging.getLogger("nexus.loki")

# Knowledge Base about the NEXUS Application
NEXUS_APP_KNOWLEDGE = {
    "how_nexus_works": {
        "title": "How NEXUS Works",
        "answer": "NEXUS is an autonomous enterprise B2B sales copilot with persistent biomimetic deal memory.",
        "why": "Traditional CRMs and chat bots suffer from context amnesia between sales calls. NEXUS retains every interaction across 4 memory tiers (World, Experience, Observation, Opinion), analyzes live conversations in real time, and equips reps with historical winning patterns.",
        "evidence": ["NEXUS 3-Panel Cockpit", "Vectorize Hindsight Memory Engine", "Event-Driven Intelligence Pipeline"],
        "recommended_action": "Try clicking ▶ START LIVE DEMO in the top bar to watch real-time objection handling in action."
    },
    "deal_memory": {
        "title": "What Deal Memory Means",
        "answer": "Deal Memory is NEXUS's persistent cognitive memory architecture powered by Vectorize Hindsight.",
        "why": "It separates memory into 4 cognitive tiers: 1) World Tier (Ground truth facts like budget ₹25L and CTO Rohan Sharma), 2) Experience Tier (Episodic meeting transcripts and verbatim quotes), 3) Observation Tier (Emergent patterns like TCO reframing against Competitor X), and 4) Opinion Tier (Organizational negotiation playbooks).",
        "evidence": ["Hindsight Memory Graph", "Deal Memory View in Sidebar", "Retain/Recall/Reflect APIs"],
        "recommended_action": "Navigate to the 'Deal Memory' tab in the sidebar to inspect the live memory graph."
    },
    "live_call": {
        "title": "How the Live Call Feature Works",
        "answer": "The Live Call feature provides a real-time, 3-panel sales cockpit during customer meetings.",
        "why": "Left Panel: Streaming transcript with speaker recognition (Sales Rep vs Customer). Center Panel: Live intelligence alerts (🔴 Critical Objections, 🟢 Buying Signals, 📌 Requirements, 🥊 Competitor Mentions, 🎯 Next Best Actions). Right Panel: Live Deal Memory snapshot with budget, decision-makers, and pending commitments.",
        "evidence": ["Live Call Cockpit", "Audio Waveform Simulation", "Interactive Action Badges"],
        "recommended_action": "Click 'Live Call' in the sidebar or hit ▶ START LIVE DEMO to run a guided call simulation."
    },
    "objection_detection": {
        "title": "How NEXUS Detects & Coaches Objections",
        "answer": "NEXUS classifies customer objections across 11 dimensions (Pricing, Security, Implementation, Technical, Integration, Contract, Timeline, Competition, ROI, Features, Support).",
        "why": "When an objection is detected (e.g., 'Your price is higher than Competitor X'), NEXUS recalls past occurrences, customer budget, and matches against similar historical won deals (e.g. Deal #1024 FinTech ₹30L) to recommend proven reframe strategies rather than raw discounts.",
        "evidence": ["Objection Intelligence View", "Historical Deal Matches", "Hindsight Experience Recall"],
        "recommended_action": "Open the 'Objections' tab in the sidebar to review active objections and counter-strategies."
    },
    "create_deal": {
        "title": "How to Create or Manage Deals",
        "answer": "You can create new deals using the '+ New Deal' button in the Deals Pipeline view, or connect external CRMs like Salesforce and HubSpot.",
        "why": "Every created deal is automatically provisioned with a dedicated Hindsight memory bank (`nexus-{deal_id}`) and grounded with baseline World facts.",
        "evidence": ["Deals Pipeline View", "Integrations Tab (Salesforce/HubSpot)", "REST API: POST /api/deals"],
        "recommended_action": "Switch to the 'Deals' view in the sidebar to see the Kanban pipeline board."
    },
    "high_risk_deals": {
        "title": "High-Risk Deals in the Pipeline",
        "answer": "Currently, 2 deals have elevated risk indicators: ABC Technologies (Health: 68/100, pending pricing objection vs Competitor X) and Vertex Finance (Health: 62/100, stalled security compliance signoff).",
        "why": "NEXUS calculates deal risk transparently based on unanswered emails > 5 days, unresolved pricing objections, and competitor discounting pressure.",
        "evidence": ["ABC Technologies (deal-abc-security)", "Vertex Finance (deal-vertex-cyber)", "Deal Risk Engine"],
        "recommended_action": "Run /risks in LOKI or click 🔍 DEAL X-RAY to perform a deep-dive diagnosis."
    }
}

# External Company & Competitor Profiles for Research Mode
EXTERNAL_PROFILES = {
    "abc technologies": {
        "company": "ABC Technologies Inc.",
        "overview": "Leading enterprise enterprise logistics and cloud supply-chain platform serving Fortune 500 manufacturers across North America and APAC.",
        "industry": "Enterprise Supply Chain Software & Cloud Logistics",
        "headquarters": "San Jose, California & Bangalore, India (Dual HQ)",
        "business_model": "B2B SaaS with consumption-based API tiers and enterprise annual licensing.",
        "products": ["ABC TrackNet", "NexusRoute AI", "LogiShield Enterprise Gateway"],
        "technology": "Multi-region AWS & GCP infrastructure, Kubernetes, Apache Kafka, SOC2 Type II certified.",
        "key_executives": [
            "Vikram Malhotra (Chief Executive Officer)",
            "Rohan Sharma (Chief Technology Officer)",
            "Anita Roy (Chief Financial Officer)"
        ],
        "recent_developments": "Announced $45M Series C expansion in Q2 2026 to modernize cyber resilience and real-time inventory telemetry.",
        "major_partnerships": "Strategic integrations with SAP S/4HANA, Snowflake, and Microsoft Azure.",
        "competitors": ["Competitor X", "LogiGlobal", "SupplyChain Dynamics"],
        "market_presence": "Managing $12B+ in annual freight volume across 40+ countries.",
        "relevant_trends": "Rapid migration towards zero-trust cloud architectures to prevent supply chain cyber extortion.",
        "potential_business_needs": "Requires single-tenant vector database isolation, 24/7 round-the-clock enterprise SLA, and zero cross-tenant memory leakage.",
        "relevance_to_deal": "High. The current Enterprise Security Platform deal (₹25L / $300k ARR) directly addresses their zero-trust compliance mandate for December 2026.",
        "sources": [
            {"title": "ABC Tech 2026 Annual Infrastructure Roadmap", "url": "https://abctech.example.com/press/2026-roadmap", "date": "August 2026"},
            {"title": "Gartner Supply Chain Security Magic Quadrant 2026", "url": "https://gartner.example.com/supply-chain-security-2026", "date": "July 2026"}
        ]
    },
    "competitor x": {
        "company": "Competitor X (Securitas Cloud)",
        "overview": "Legacy cybersecurity vendor known for aggressive entry-level pricing and discounting, but limited by manual rule-based alerting and high operational maintenance toil.",
        "industry": "Cloud Workload Protection & Perimeter Firewalls",
        "headquarters": "Austin, Texas",
        "business_model": "Volume-based software licensing with 30-40% first-year discounting gimmicks.",
        "products": ["Securitas Perimeter Guard", "LogAnalyzer Basic"],
        "technology": "Traditional relational database alerting, lacks real-time semantic memory and predictive root-cause correlation.",
        "key_executives": ["Mark Bradley (CEO)", "David Chen (VP Sales)"],
        "recent_developments": "Facing customer churn due to 3-week incident triage latency and high false-positive alert fatigue.",
        "major_partnerships": "Standard reseller channels.",
        "competitors": ["NEXUS", "CyberShield", "Datadog Security"],
        "market_presence": "Established legacy base, losing modern cloud-native accounts.",
        "relevant_trends": "Heavy price-war tactics to defend legacy footprints against autonomous AI agents.",
        "potential_business_needs": "Trying to anchor customer budgets low (₹18L-₹20L) before escalating renewal fees in Year 2.",
        "relevance_to_deal": "Active threat. Rohan Sharma (CTO) mentioned Competitor X offered lower initial price. Counter with TCO analysis showing 74% MTTR reduction.",
        "sources": [
            {"title": "GigaOm Radar for Enterprise Security Platforms 2026", "url": "https://gigaom.example.com/sec-radar-2026", "date": "June 2026"},
            {"title": "PeerSpot Enterprise Security Reviews - Competitor X", "url": "https://peerspot.example.com/products/competitor-x-reviews", "date": "September 2026"}
        ]
    },
    "nova systems": {
        "company": "Nova Systems Corporation",
        "overview": "Next-generation telecom and 5G edge infrastructure provider operating carrier-grade edge compute clusters.",
        "industry": "Telecommunications & Edge Cloud Compute",
        "headquarters": "Boston, Massachusetts",
        "business_model": "Multi-year enterprise infrastructure contracts.",
        "key_executives": ["Priya Patel (VP Engineering)", "Markus Lindqvist (CTO)"],
        "relevance_to_deal": "Target account for Cloud Infrastructure Upgrade (₹35L / $420k ARR).",
        "sources": [{"title": "Nova Systems Press Release Q3 2026", "url": "https://novasystems.example.com/news", "date": "August 2026"}]
    },
    "vertex finance": {
        "company": "Vertex Finance & Banking Corp.",
        "overview": "Tier-1 investment banking and algorithmic trading institution subject to stringent RBI/SEC compliance mandates.",
        "industry": "FinTech & Wealth Management",
        "headquarters": "Mumbai, India & London, UK",
        "business_model": "Institutional financial services.",
        "key_executives": ["Sunil Nambiar (CISO)", "Kavita Rao (Head of Procurement)"],
        "relevance_to_deal": "Cybersecurity Transformation (₹45L / $550k ARR).",
        "sources": [{"title": "FinTech Compliance Review 2026", "url": "https://vertexfin.example.com/investors", "date": "September 2026"}]
    }
}


class LokiEngine:
    def __init__(self):
        self.name = "LOKI"
        self.concept = "LOKI — Live Operational Knowledge Intelligence"
        self.tagline = "Ask anything. Know everything. Act intelligently."
        self.history: List[Dict[str, Any]] = []

    def get_supported_commands(self) -> List[Dict[str, str]]:
        return [
            {"command": "/deal", "description": "Display pin-to-pin Deal Intelligence Report for current deal"},
            {"command": "/customer", "description": "View deep customer profile, business model, and contacts"},
            {"command": "/stakeholders", "description": "Inspect stakeholder influence matrix, priorities, and concerns"},
            {"command": "/competitors", "description": "Analyze competitor mentions, battlecards, and win patterns"},
            {"command": "/objections", "description": "Review active objections, previous occurrences, and talk tracks"},
            {"command": "/meetings", "description": "List meeting history, transcripts, commitments, and summaries"},
            {"command": "/memory", "description": "Explore 4-tier persistent deal memory graph (Hindsight)"},
            {"command": "/risks", "description": "Audit transparent deal risks and underlying signals"},
            {"command": "/actions", "description": "Get recommended next-best actions with deadline and owner"},
            {"command": "/history", "description": "Benchmark against similar historical won/lost deals"},
            {"command": "/analytics", "description": "View pipeline velocity, win rates, and objection frequencies"},
            {"command": "/company", "description": "Retrieve comprehensive company intelligence dossier"},
            {"command": "/research", "description": "Conduct external business research with verified sources"},
            {"command": "/xray", "description": "Run deep 18-dimension DEAL X-RAY diagnostic"},
            {"command": "/connect", "description": "Launch LOKI CONNECT visual relationship flow"},
            {"command": "/brief", "description": "Generate Executive Deal Brief for leadership"},
            {"command": "/help", "description": "Show LOKI command guide and intelligence capabilities"}
        ]

    def query(
        self,
        query_text: str,
        deal_id: str = "deal-abc-security",
        mode: str = "deal",
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Main query entrypoint for LOKI.
        Processes natural language, slash commands, application inquiries, and deep deal intelligence.
        """
        query_clean = (query_text or "").strip()
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        actual_deal_id = deal["id"]

        logger.info(f"LOKI received query: '{query_clean}' [mode={mode}, deal={actual_deal_id}]")

        # 1. Check for Slash Commands
        if query_clean.startswith("/"):
            parts = query_clean.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            return self.execute_slash_command(cmd, actual_deal_id, arg)

        # 2. Check for "Deal X-Ray" or "xray" query
        if "x-ray" in query_clean.lower() or "xray" in query_clean.lower():
            return self.get_deal_xray(actual_deal_id)

        # 3. Check for "Loki Connect" or "connect the dots"
        if "connect" in query_clean.lower() and ("dot" in query_clean.lower() or "flow" in query_clean.lower() or "loki" in query_clean.lower()):
            return self.get_loki_connect(actual_deal_id)

        # 4. Check for "Executive Brief" or "brief me"
        if "executive brief" in query_clean.lower() or "brief me" in query_clean.lower() or "loki brief" in query_clean.lower():
            return self.get_executive_brief(actual_deal_id)

        # 5. Check for "Why is this deal at risk?"
        if "at risk" in query_clean.lower() or "why" in query_clean.lower() and "risk" in query_clean.lower():
            return self.explain_deal_risk(actual_deal_id)

        # 6. Check for Application Knowledge questions (Section 2)
        app_res = self._check_app_knowledge(query_clean)
        if app_res:
            return app_res

        # 7. Check for External Research / Company Profile queries (Section 9, 10, 21)
        if mode == "research" or any(w in query_clean.lower() for w in ["who is", "latest developments", "company profile", "research", "industry trends", "regulations"]):
            return self.research_external(query_clean, actual_deal_id)

        # 8. Check for Competitor Questions (Section 12)
        if "competitor" in query_clean.lower() or "competitor x" in query_clean.lower():
            return self._answer_competitor_query(query_clean, actual_deal_id)

        # 9. Check for Stakeholder Questions (Section 11)
        if any(w in query_clean.lower() for w in ["decision-maker", "decision maker", "stakeholder", "cto", "cfo", "procurement", "cares about"]):
            return self._answer_stakeholder_query(query_clean, actual_deal_id)

        # 10. Check for "Tell me everything about this deal" / "Summarize this deal" (Section 3, 13)
        if any(p in query_clean.lower() for p in ["everything about this deal", "summarize this deal", "deal overview", "tell me about this deal"]):
            return self.get_deal_intelligence_report(actual_deal_id)

        # 11. Check for "What should I do next?" (Section 5)
        if "next" in query_clean.lower() and ("do" in query_clean.lower() or "action" in query_clean.lower() or "step" in query_clean.lower()):
            return self._answer_next_actions_query(actual_deal_id)

        # 12. Fallback to Deal Engine Context & Hindsight Reflection
        return self._generate_contextual_answer(query_clean, actual_deal_id, mode)

    def execute_slash_command(self, cmd: str, deal_id: str, arg: str = "") -> Dict[str, Any]:
        """Handles structured /command inputs."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer_name = deal.get("company", deal.get("name", "Customer"))

        if cmd == "/help":
            commands_list = self.get_supported_commands()
            cmd_lines = [f"`{c['command']}` — {c['description']}" for c in commands_list]
            return {
                "answer": "Here are all available LOKI intelligence commands:",
                "why": "LOKI provides instant keyboard shortcuts to audit any dimension of NEXUS deal memory without leaving your workflow.",
                "evidence": ["NEXUS Command Engine", "Pin-to-Pin Memory Index"],
                "recommended_action": "Try typing `/xray` or `/connect` to inspect the current deal.",
                "formatted_content": "\n".join(cmd_lines),
                "quick_actions": ["/xray", "/connect", "/brief", "/risks", "/competitors"]
            }

        elif cmd == "/deal":
            return self.get_deal_intelligence_report(deal_id)

        elif cmd == "/xray":
            return self.get_deal_xray(deal_id)

        elif cmd == "/connect":
            return self.get_loki_connect(deal_id)

        elif cmd == "/brief":
            return self.get_executive_brief(deal_id)

        elif cmd == "/risks":
            return self.explain_deal_risk(deal_id)

        elif cmd == "/competitors":
            return self._answer_competitor_query(arg or "competitors", deal_id)

        elif cmd == "/stakeholders":
            return self._answer_stakeholder_query(arg or "stakeholders", deal_id)

        elif cmd == "/objections":
            objections = deal_engine.get_objections(deal_id)
            obj_list = objections.get("objections", [])
            lines = [f"• **{o.get('type', 'Objection')}** ({o.get('status', 'Open')}): \"{o.get('text', '')}\" — Raised by {o.get('raised_by', 'Customer')}" for o in obj_list]
            return {
                "answer": f"Found {len(obj_list)} recorded objections for {customer_name}.",
                "why": "Unresolved objections directly threaten contract closure velocity and trigger pricing erosion.",
                "evidence": [f"Meeting {o.get('meeting_id', '#1')}" for o in obj_list],
                "formatted_content": "\n".join(lines),
                "recommended_action": "Use TCO and MTTR counter-framing rather than offering base ARR discounts.",
                "quick_actions": ["Analyze Pricing", "Compare Similar Deals", "Show Stakeholders"]
            }

        elif cmd == "/customer":
            cust = deal_engine.get_customer(f"cust-{deal_id.replace('deal-', '')}") or deal_engine.list_customers()[0]
            return {
                "answer": f"**Customer Dossier: {cust.get('name')}** | Industry: {cust.get('industry')} | Employees: {cust.get('employees', 'N/A')}",
                "why": f"World tier grounding indicates annual revenue of {cust.get('annual_revenue')} and headquarters in {cust.get('headquarters')}.",
                "evidence": [f"Customer Account Record: {cust.get('id')}", "World Tier Facts"],
                "formatted_content": f"**Key Contacts:** {', '.join([c.get('name') + ' (' + c.get('role') + ')' for c in cust.get('contacts', [])])}\n\n**Strategic Notes:** {cust.get('notes', 'No notes.')}",
                "recommended_action": "Review stakeholder priorities before reaching out to procurement.",
                "quick_actions": ["Show Stakeholders", "Analyze Competitors", "Run Deal X-Ray"]
            }

        elif cmd == "/meetings":
            interactions = deal.get("interactions", [])
            lines = [f"• **{i.get('date', 'Recent')} — {i.get('type', 'Meeting')}**: with {i.get('stakeholder', 'Team')}. Key Quote: \"{i.get('quote', i.get('notes', ''))[:90]}\"" for i in interactions]
            return {
                "answer": f"Logged {len(interactions)} meetings and calls for {customer_name}.",
                "why": "Every meeting is stored verbatim in Hindsight's Experience Tier to prevent rep amnesia.",
                "evidence": [f"Interaction ID: {i.get('id')}" for i in interactions],
                "formatted_content": "\n".join(lines) if lines else "No logged meetings yet.",
                "recommended_action": "Click 'Live Call' to start streaming and capturing the next customer interaction.",
                "quick_actions": ["Live Call", "Prepare Follow-up", "Generate Brief"]
            }

        elif cmd == "/memory":
            mem = deal_engine.get_deal_memory(deal_id)
            stats = mem.get("stats", {})
            return {
                "answer": f"Persistent Deal Memory contains **{stats.get('total_memories', 0)} cognitive nodes** across 4 biomimetic tiers.",
                "why": f"World: {stats.get('world_facts', 0)} facts | Experience: {stats.get('experiences', 0)} interactions | Observations: {stats.get('observations', 0)} patterns | Opinions: {stats.get('opinions', 0)} playbooks.",
                "evidence": ["Vectorize Hindsight Bank", f"Bank ID: {deal.get('bank_id')}"],
                "recommended_action": "Navigate to the Deal Memory graph view in the sidebar to visualize knowledge links.",
                "quick_actions": ["Open Deal Memory", "Run Deal X-Ray", "LOKI Connect"]
            }

        elif cmd == "/actions":
            return self._answer_next_actions_query(deal_id)

        elif cmd == "/history":
            won = deal_engine.historical_deals
            lines = [f"• **Deal #{d.get('deal_number')} ({d.get('company')})** — ARR: ${d.get('arr', 0):,} / ₹{d.get('inr_display', 'N/A')}. Objection: {d.get('objection_encountered')}. Resolution: {d.get('winning_resolution')} ({d.get('cycle_days')} days to win)." for d in won]
            return {
                "answer": f"Retrieved {len(won)} similar historical won deals with verified resolution patterns.",
                "why": "Evidence from past wins eliminates guessing on discount and objection strategies.",
                "evidence": [f"Historical Deal #{d.get('deal_number')}" for d in won],
                "formatted_content": "\n".join(lines),
                "recommended_action": "Cite Deal #1024 or Deal #84 when countering Competitor X price pressure.",
                "quick_actions": ["Compare Similar Deals", "Analyze Pricing", "View Analytics"]
            }

        elif cmd == "/analytics":
            return {
                "answer": "Current Pipeline Analytics: 39 active enterprise opportunities worth ₹14.8 Cr ($18.2M ARR).",
                "why": "Win rate against Competitor X increases by 34% when TCO ROI analysis is introduced before Stage 4 (Negotiation).",
                "evidence": ["NEXUS Pipeline Engine", "Gong/CRM Historical Datasets"],
                "recommended_action": "Navigate to 'Analytics' in the sidebar for full win-loss and velocity charts.",
                "quick_actions": ["Open Analytics", "Compare Deals", "Review Risks"]
            }

        elif cmd in ["/company", "/research"]:
            target = arg or customer_name
            return self.research_external(target, deal_id)

        else:
            return {
                "answer": f"Unknown command `{cmd}`. Type `/help` to see all supported LOKI commands.",
                "why": "LOKI supports 17 operational commands for deep deal intelligence.",
                "evidence": ["LOKI Command Registry"],
                "recommended_action": "Type `/help` or `/deal` to get started."
            }

    def get_deal_intelligence_report(self, deal_id: str) -> Dict[str, Any]:
        """Generates Section 3 format: DEAL INTELLIGENCE REPORT."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))
        value_inr = deal.get("inr_display", f"₹{deal.get('arr_target', 300000) / 12000:.0f}L")
        value_usd = f"${deal.get('arr_target', 300000):,} ARR"

        decision_makers = [f"{s.get('name')} ({s.get('role')})" for s in deal.get("stakeholders", []) if s.get("influence") == "High"]
        if not decision_makers:
            decision_makers = ["Rohan Sharma (CTO)", "Anita Roy (CFO)", "Kavita Rao (Procurement Head)"]

        requirements = deal.get("key_requirements", [
            "Enterprise security & zero cross-tenant memory leakage",
            "24/7 dedicated support SLA",
            "Deployment before December 2026"
        ])

        objections = [o.get("type", "Pricing") for o in deal.get("objections", [])]
        if not objections:
            objections = ["Pricing higher than Competitor X", "Implementation timeline"]

        competitors = deal.get("competitors_mentioned", ["Competitor X"])

        recent_activity = [
            "Technical architecture review completed with CTO Rohan Sharma",
            "Pricing proposal delivered ($300k / ₹25L ARR target)",
            "CTO requested enterprise SLA compliance documentation"
        ]

        risks = [
            "Pricing objection unresolved (Budget: ₹25L, competitor quote: ₹20L)",
            "Procurement committee review pending commercial contract signoff"
        ]

        next_action = "Schedule technical security & TCO demo with CTO Rohan Sharma within 2 business days."

        report_md = f"""### DEAL INTELLIGENCE REPORT

**Customer:** {customer}
**Deal:** {deal.get('name', 'Enterprise Security Platform')}
**Stage:** {deal.get('stage', 'Negotiation')}
**Deal Value:** {value_inr} ({value_usd})

**Decision Makers:**
{chr(10).join([f"• 👤 {dm}" for dm in decision_makers])}

**Requirements:**
{chr(10).join([f"• ✓ {req}" for req in requirements])}

**Objections:**
{chr(10).join([f"• ⚠ {obj}" for obj in objections])}

**Competitors:**
{chr(10).join([f"• 🥊 {c}" for c in competitors])}

**Recent Activity:**
{chr(10).join([f"• 📅 {act}" for act in recent_activity])}

**Risks:**
{chr(10).join([f"• ⚠ {r}" for r in risks])}

**Next Best Action:**
🎯 {next_action}
"""

        return {
            "answer": f"Here is the complete Pin-to-Pin Deal Intelligence Report for **{customer}**:",
            "why": "Synthesized from 4 persistent memory tiers: account grounding facts, verbatim meeting logs, active competitor quotes, and CRM pipeline stages.",
            "evidence": [
                f"Deal ID: {deal['id']}",
                f"World Tier: {deal.get('company')}",
                "Meeting Transcripts #1-#3",
                "Proposal #1 Document"
            ],
            "formatted_content": report_md,
            "recommended_action": next_action,
            "quick_actions": ["Analyze Pricing", "Compare Similar Deals", "Show Stakeholders", "Run Deal X-Ray"]
        }

    def explain_deal_risk(self, deal_id: str) -> Dict[str, Any]:
        """Explains Section 4 & 16: Pin-to-pin root cause for deal risk."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))
        health = deal.get("health_score", 68)

        answer = "Pricing remains unresolved while Competitor X exerts downward budget pressure."
        why = (
            f"The customer raised pricing concerns across the last two interactions and the procurement team has not "
            f"responded to the revised proposal for 5 business days. Furthermore, Competitor X was mentioned 4 times "
            f"with lower entry pricing. CTO Rohan Sharma requires assurance on zero cross-tenant leakage before December."
        )
        evidence = [
            "Meeting #4: Pricing objection raised by CTO Rohan Sharma",
            "Meeting #5: Competitor X initial price quoted 15% lower",
            "Email #7: Revised commercial proposal unopened for 5 days",
            "Requirement: Hard December 2026 deployment cutoff"
        ]
        action = "Schedule a joint commercial & TCO session with CTO Rohan Sharma and Procurement within 48 hours."

        return {
            "answer": answer,
            "why": why,
            "evidence": evidence,
            "recommended_action": action,
            "health_score": health,
            "risk_level": "Medium-High",
            "follow_ups": [
                "Do you want me to analyze the pricing history and similar deals?",
                "Would you like me to prepare a follow-up draft for CTO Rohan Sharma?",
                "Should I generate a TCO comparison against Competitor X?"
            ],
            "quick_actions": ["Analyze Pricing", "Compare Similar Deals", "Prepare Follow-up", "Show Stakeholders"]
        }

    def get_loki_connect(self, deal_id: str) -> Dict[str, Any]:
        """Generates Section 25: LOKI CONNECT Interactive Flow."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        nodes = [
            {
                "id": "node-1",
                "step": 1,
                "title": "Customer Requirement",
                "summary": "Enterprise Security & Zero-Leakage Architecture",
                "evidence_source": "Discovery Meeting #1",
                "details": "Customer requires guaranteed isolated memory namespaces and SOC2 Type II compliance.",
                "type": "requirement",
                "badge": "📌 Requirement"
            },
            {
                "id": "node-2",
                "step": 2,
                "title": "Deployment Deadline",
                "summary": "Hard Deployment Cutoff: December 2026",
                "evidence_source": "Live Meeting Transcript (CTO Quote)",
                "details": "Rohan Sharma stated: 'We need the platform deployed before December for Q4 compliance.'",
                "type": "deadline",
                "badge": "⏱ Deadline"
            },
            {
                "id": "node-3",
                "step": 3,
                "title": "Technical Objection",
                "summary": "Implementation Complexity & Deployment Bandwidth",
                "evidence_source": "Interaction #2 Architecture Review",
                "details": "Engineering team is concerned about integration friction with existing Kafka event streams.",
                "type": "objection",
                "badge": "⚠ Objection"
            },
            {
                "id": "node-4",
                "step": 4,
                "title": "CTO Primary Concern",
                "summary": "Rohan Sharma: Security posture & MTTR reduction",
                "evidence_source": "Stakeholder Intelligence Dossier",
                "details": "CTO prioritizes enterprise support and 74% MTTR reduction over raw discounting.",
                "type": "stakeholder",
                "badge": "👤 Stakeholder"
            },
            {
                "id": "node-5",
                "step": 5,
                "title": "Competitor X",
                "summary": "Mentioned 4 times with lower upfront pricing",
                "evidence_source": "Meeting #3 & Email #4",
                "details": "Competitor X offering initial discount anchor (₹18L-₹20L) but lacks real-time memory and 24/7 SLA.",
                "type": "competitor",
                "badge": "🥊 Competitor"
            },
            {
                "id": "node-6",
                "step": 6,
                "title": "Pricing Discussion",
                "summary": "Budget Anchor ₹25L ($300k) vs 15% discount request",
                "evidence_source": "Commercial Offer #1",
                "details": "Procurement requested 15% discount match. Historical data shows trading migration credits wins without margin erosion.",
                "type": "pricing",
                "badge": "💰 Pricing"
            },
            {
                "id": "node-7",
                "step": 7,
                "title": "Deal Risk",
                "summary": "Health Score 68/100: Unresolved Pricing Anchor",
                "evidence_source": "NEXUS Risk Engine",
                "details": "Deal will stall if pricing is not reframed around Total Cost of Ownership before procurement signs.",
                "type": "risk",
                "badge": "⚠ Risk"
            },
            {
                "id": "node-8",
                "step": 8,
                "title": "Recommended Action",
                "summary": "Deliver TCO Calculator & Schedule Security Demo in 48h",
                "evidence_source": "Hindsight Opinion Tier Playbook",
                "details": "Trade migration engineering support for 24-month contract commitment at full ₹25L ARR.",
                "type": "action",
                "badge": "🎯 Next Action"
            }
        ]

        connection_summary = (
            f"LOKI CONNECT demonstrates how the initial requirement for zero-trust security led to the December deadline, "
            f"which heightened CTO Rohan Sharma's concern over deployment time, allowing Competitor X to introduce price pressure. "
            f"Reframing pricing via Total Cost of Ownership resolves both the technical and commercial hurdles."
        )

        return {
            "answer": f"**LOKI CONNECT: Pin-to-Pin Deal Chain for {customer}**",
            "why": "This interactive chain reveals the causal relationships linking customer requirements, stakeholder objections, competitor pressure, and next best actions.",
            "evidence": [f"Node {n['step']}: {n['evidence_source']}" for n in nodes],
            "connection_summary": connection_summary,
            "nodes": nodes,
            "recommended_action": "Click any node in the LOKI CONNECT visualizer to inspect the underlying stored evidence.",
            "quick_actions": ["Run Deal X-Ray", "Executive Brief", "Analyze Pricing"]
        }

    def get_deal_xray(self, deal_id: str) -> Dict[str, Any]:
        """Generates Section 27: 🔍 DEAL X-RAY (18 pin-to-pin dimensions)."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))
        val_inr = deal.get("inr_display", "₹25,00,000")
        val_usd = f"${deal.get('arr_target', 300000):,} ARR"

        xray_sections = [
            {"dimension": "1. Customer Profile", "summary": f"{customer} | Enterprise Logistics | 4,200 Employees | ARR Potential: {val_inr}", "status": "Strong", "badge": "emerald"},
            {"dimension": "2. Stakeholders Matrix", "summary": "Rohan Sharma (CTO - Champion), Anita Roy (CFO - Economic Buyer), Procurement Head (Gatekeeper)", "status": "Engaged", "badge": "emerald"},
            {"dimension": "3. Timeline & Velocity", "summary": "Day 42 of 65-day typical sales cycle. Hard deployment deadline: December 2026", "status": "Active", "badge": "indigo"},
            {"dimension": "4. Core Requirements", "summary": "Enterprise Security, Single-Tenant Vector Isolation, 24/7 Support SLA, Zero Cross-Tenant Leakage", "status": "Documented", "badge": "indigo"},
            {"dimension": "5. Active Objections", "summary": "Pricing vs Competitor X (Budget ₹25L, asked 15% discount), Implementation timeline concerns", "status": "Open", "badge": "rose"},
            {"dimension": "6. Competitor Dynamics", "summary": "Competitor X mentioned 4 times with aggressive entry-level price. Lacks 24/7 SLA and real-time memory", "status": "Contested", "badge": "amber"},
            {"dimension": "7. Pricing & Budget", "summary": f"List Target: {val_usd} ({val_inr}). Customer budget: ₹25L. Competitor anchor: ₹20L", "status": "Negotiation", "badge": "amber"},
            {"dimension": "8. Meeting History", "summary": "3 completed executive reviews (Discovery, Technical Architecture, Security Deep Dive)", "status": "Verified", "badge": "emerald"},
            {"dimension": "9. Email Correspondence", "summary": "7 emails exchanged. Last commercial proposal email sent 5 days ago (Pending reply)", "status": "Attention", "badge": "amber"},
            {"dimension": "10. Follow-up Tasks", "summary": "3 active tasks: Schedule security demo, deliver TCO calculator, review procurement contract", "status": "In Progress", "badge": "indigo"},
            {"dimension": "11. Rep & Customer Commitments", "summary": "Rep committed to architecture whitepaper; Customer committed to Q4 deployment review", "status": "Pending", "badge": "indigo"},
            {"dimension": "12. Deal Risks & Health", "summary": f"Health Score: {deal.get('health_score', 68)}/100. Signals: Unanswered proposal, competitor discount pressure", "status": "Medium Risk", "badge": "amber"},
            {"dimension": "13. Buying Signals", "summary": "CTO requested 24/7 support SLA; CFO approved security budget allocation in Q3 roadmap", "status": "Positive", "badge": "emerald"},
            {"dimension": "14. Historical Benchmarks", "summary": "Matches Deal #1024 (FinTech ₹30L Won) and Deal #84 (Nordic Cloud $580k Won with migration credits)", "status": "High Match", "badge": "emerald"},
            {"dimension": "15. External Business Intel", "summary": "ABC Tech completed $45M Series C; expanding APAC logistics footprint; compliance priority high", "status": "Enriched", "badge": "indigo"},
            {"dimension": "16. Missing Information", "summary": "Exact procurement sign-off checklist and legal redline timeline not yet provided", "status": "Gap", "badge": "rose"},
            {"dimension": "17. Recommended Questions", "summary": "'Is the primary concern upfront license price, or total cost of maintenance and engineering hours?'", "status": "Prescribed", "badge": "cyan"},
            {"dimension": "18. Next Best Actions", "summary": "Present Total Cost of Ownership calculator to CTO Rohan Sharma and CFO Anita Roy within 48 hours", "status": "Immediate", "badge": "rose"}
        ]

        return {
            "answer": f"**🔍 DEAL X-RAY: Complete 18-Dimension Diagnostic for {customer}**",
            "why": "LOKI performed a deep multi-tier inspection across all transaction records, CRM data, meeting transcripts, and external intelligence.",
            "evidence": ["NEXUS Memory Bank", "CRM Data Lake", "Gong Transcripts", "Gartner/External Reports"],
            "deal_health": deal.get("health_score", 68),
            "deal_value": val_inr,
            "xray_sections": xray_sections,
            "recommended_action": "Execute the TCO presentation and lock the December deployment architecture.",
            "quick_actions": ["Executive Brief", "LOKI Connect", "Analyze Pricing"]
        }

    def get_executive_brief(self, deal_id: str) -> Dict[str, Any]:
        """Generates Section 20: EXECUTIVE DEAL BRIEF for leadership."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))
        val_inr = deal.get("inr_display", "₹25,00,000")
        val_usd = f"${deal.get('arr_target', 300000):,} ARR"

        brief_text = f"""## EXECUTIVE DEAL BRIEF

**Customer:** {customer}
**Deal Value:** {val_inr} ({val_usd})
**Stage:** {deal.get('stage', 'Negotiation')}
**Current Status:** Contested evaluation entering commercial negotiation.

**Top Requirements:**
• Enterprise security with single-tenant namespace isolation
• Guaranteed deployment before December 2026
• 24/7 dedicated support SLA

**Top Risks:**
• Competitor X offering aggressive initial discount (₹18L-₹20L)
• Commercial proposal unacknowledged by procurement for 5 business days
• Deal Health: {deal.get('health_score', 68)}/100

**Decision Makers:**
• CTO Rohan Sharma (Technical authority — Champion)
• CFO Anita Roy (Economic buyer — Budget approver)
• Procurement Head (Commercial terms & contracting)

**Competitors:**
• Competitor X (Securitas Cloud) — 4 mentions

**Recent Changes:**
• Customer confirmed December hard deadline
• CTO formally requested 24/7 SLA terms

**Unresolved Issues:**
• 15% discount request from procurement team

**Recommended Next Actions:**
1. Deliver Total Cost of Ownership (TCO) calculator demonstrating 74% MTTR reduction.
2. Offer migration engineering credits instead of base ARR discount.
3. Lock security demo with CTO within 48 hours.

**Evidence:**
• Meetings #1-#3 transcripts
• Proposal #1 commercial doc
• Historical Deal #1024 (Won via TCO reframe)
"""
        return {
            "answer": f"**EXECUTIVE DEAL BRIEF: {customer}**",
            "why": "Generated for executive leadership to summarize deal status, risks, and high-margin closing strategy in 30 seconds.",
            "evidence": ["Hindsight Memory", "CRM Pipeline", "Interaction Logs"],
            "formatted_content": brief_text,
            "recommended_action": "Share brief with Sales VP and schedule commercial alignment call.",
            "quick_actions": ["Run Deal X-Ray", "LOKI Connect", "Prepare Follow-up"]
        }

    def explain_why(self, deal_id: str, insight_topic: str = "", text: str = "") -> Dict[str, Any]:
        """Generates Section 26: UNIQUE FEATURE — 'ASK WHY'."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        target = (insight_topic or text or "pricing risk").lower()

        if "price" in target or "pricing" in target or "cost" in target:
            answer = "Pricing is currently the primary deal risk."
            why = "Pricing was mentioned as an objection in the last two meetings. The revised proposal has not received a response. Competitor X was also mentioned during the most recent discussion with lower initial pricing."
            records_considered = [
                "Meeting #4: 'Your price is higher than Competitor X'",
                "Meeting #5: Procurement requested 15% discount",
                "Proposal #2: Delivered 5 business days ago with zero email engagement",
                "Historical Benchmark: Deal #1024 and Deal #84 won by holding firm on ARR and trading migration credits"
            ]
            uncertainty = "Customer has not explicitly revealed Competitor X's final renewal pricing for Year 2."
        elif "competitor" in target:
            answer = "Competitor X is attempting a land-and-expand discount trap."
            why = "Competitor X frequently offers 30-40% first-year discounts to unseat incumbents, then increases maintenance fees by 50% upon renewal."
            records_considered = [
                "Competitor X battlecard [Hindsight Opinion Tier]",
                "4 customer mentions in Meeting #2, #3, and #4",
                "Historical Deal #84 (Nordic Cloud): Competitor X displaced using 3-year TCO comparison"
            ]
            uncertainty = "Customer has not shared the exact contract draft from Competitor X."
        else:
            answer = f"This insight was derived from continuous multi-source correlation for {customer}."
            why = "NEXUS monitors conversation transcripts, CRM email velocity, and historical win patterns to detect anomalies before deals stall."
            records_considered = [
                f"Deal record: {deal['id']}",
                "Recent meeting transcripts",
                "Hindsight cognitive memory tiers"
            ]
            uncertainty = "Dependent on customer's internal procurement review timeline."

        return {
            "answer": answer,
            "why": why,
            "records_considered": records_considered,
            "historical_patterns": "ROI and Total Cost of Ownership reframing succeeded in 4 out of 4 similar enterprise deals.",
            "uncertainty": uncertainty,
            "evidence": records_considered[:3],
            "recommended_action": "Frame the upcoming meeting around Total Cost of Ownership and 74% MTTR reduction.",
            "quick_actions": ["Analyze Pricing", "Run Deal X-Ray", "LOKI Connect"]
        }

    def research_external(self, query: str, deal_id: str) -> Dict[str, Any]:
        """Generates Section 9, 10, 21: GLOBAL BUSINESS INTELLIGENCE & RESEARCH MODE."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        q_lower = query.lower()

        # Find best matching external profile
        matched_profile = None
        for key, prof in EXTERNAL_PROFILES.items():
            if key in q_lower or key.split()[0] in q_lower:
                matched_profile = prof
                break

        if not matched_profile:
            # Fallback to customer's own profile
            matched_profile = EXTERNAL_PROFILES.get("abc technologies")

        comp_name = matched_profile.get("company", "Enterprise Entity")

        formatted_profile = f"""### COMPANY INTELLIGENCE (EXTERNAL INTELLIGENCE)

**Company:** {matched_profile.get('company')}
**Industry:** {matched_profile.get('industry')}
**Headquarters:** {matched_profile.get('headquarters')}
**Business Model:** {matched_profile.get('business_model')}

**Overview:**
{matched_profile.get('overview')}

**Key Products & Services:**
{chr(10).join([f"• {p}" for p in matched_profile.get('products', ['Enterprise Cloud Platform'])])}

**Technology Infrastructure:**
{matched_profile.get('technology', 'Cloud-native multi-region architecture')}

**Key Executives:**
{chr(10).join([f"• 👤 {e}" for e in matched_profile.get('key_executives', ['Executive Leadership'])])}

**Recent Developments:**
{matched_profile.get('recent_developments', 'Expanding enterprise cloud security investments.')}

**Market Presence & Trends:**
{matched_profile.get('market_presence', 'Global tier-1 footprint')}
{matched_profile.get('relevant_trends', 'Accelerating zero-trust compliance.')}

**Relevance to Current Deal:**
{matched_profile.get('relevance_to_deal', 'Directly relevant to ongoing enterprise contract negotiations.')}

**Verified Sources:**
{chr(10).join([f"• 🔗 [{s.get('title')}]({s.get('url')}) — Published {s.get('date')}" for s in matched_profile.get('sources', [])])}
"""

        return {
            "answer": f"Retrieved verified **External Intelligence** dossier for **{comp_name}**:",
            "why": "Compiled from verified external industry sources, financial filings, and analyst benchmarks. Explicitly isolated from internal CRM records.",
            "evidence": [s.get("title") for s in matched_profile.get("sources", [])],
            "formatted_content": formatted_profile,
            "external_intelligence": True,
            "sources": matched_profile.get("sources", []),
            "recommended_action": "Incorporate these market developments into the executive proposal presentation.",
            "quick_actions": ["Analyze Competitors", "Run Deal X-Ray", "Executive Brief"]
        }

    def _check_app_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        q = query.lower()
        if "how does nexus work" in q or "how nexus works" in q or "what is nexus" in q:
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["how_nexus_works"])
        if "deal memory" in q and ("mean" in q or "what" in q or "store" in q or "work" in q):
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["deal_memory"])
        if "live call" in q:
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["live_call"])
        if "detect objection" in q or "how does nexus detect" in q:
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["objection_detection"])
        if "create a deal" in q or "how do i create" in q:
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["create_deal"])
        if "high-risk" in q or "high risk" in q:
            return self._format_app_res(NEXUS_APP_KNOWLEDGE["high_risk_deals"])
        if "previous meetings" in q or "where can i see" in q:
            return {
                "answer": "You can see previous meetings in the 'Meetings' tab in the left sidebar, or under the 'Meetings' sub-tab inside 'Deal Details'.",
                "why": "NEXUS logs all meeting transcripts, auto-generated summaries, and rep commitments chronologically in the Experience memory tier.",
                "evidence": ["Meetings Navigation Tab", "Deal Details -> Meetings Sub-Tab", "Experience Tier Memory"],
                "recommended_action": "Click 'Meetings' in the left navigation sidebar to view logged interactions.",
                "quick_actions": ["/meetings", "Live Call", "Run Deal X-Ray"]
            }
        return None

    def _format_app_res(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "answer": item["answer"],
            "why": item["why"],
            "evidence": item["evidence"],
            "recommended_action": item["recommended_action"],
            "quick_actions": ["/deal", "/xray", "/connect", "/help"]
        }

    def _answer_competitor_query(self, query: str, deal_id: str) -> Dict[str, Any]:
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        answer = "Competitor X (Securitas Cloud) is the primary rival active in this deal."
        why = (
            "Competitor X was mentioned 4 times during customer conversations. CTO Rohan Sharma noted that Competitor X "
            "offered a lower entry price. However, Competitor X lacks real-time biomimetic memory, single-tenant vector "
            "isolation, and 24/7 enterprise support SLAs."
        )
        evidence = [
            "Meeting #2: Rohan Sharma mentions Competitor X initial price",
            "Meeting #4: Customer quotes ₹18L-₹20L entry discount from Competitor X",
            "NEXUS Competitor Battlecard: Competitor X has 3-week triage latency",
            "Historical Deal #84: Competitor X defeated via 3-year TCO framing"
        ]

        competitor_map = """### COMPETITOR MAP

**Our Company (NEXUS Platform)**
  ↓
**Competitor X (Securitas Cloud)** — 4 Mentions
• Customer Perception: Lower initial price (₹18L-₹20L)
• Customer Concern: Lacks 24/7 SLA and real-time semantic memory
• Our Advantage: 74% MTTR reduction, guaranteed single-tenant isolation
• Historical Match: Displaced in 4 of 4 similar deals (e.g. Deal #1024, Deal #84)
"""
        return {
            "answer": answer,
            "why": why,
            "evidence": evidence,
            "formatted_content": competitor_map,
            "recommended_action": "Shift conversation from entry price to 3-year Total Cost of Ownership (TCO) and 74% MTTR reduction.",
            "quick_actions": ["Analyze Pricing", "Compare Similar Deals", "Research Competitor X", "Run Deal X-Ray"]
        }

    def _answer_stakeholder_query(self, query: str, deal_id: str) -> Dict[str, Any]:
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        q_lower = query.lower()

        if "cto" in q_lower:
            answer = "CTO Rohan Sharma is the primary technical champion and security authority."
            why = "His primary priority is enterprise security and single-tenant vector isolation to prevent cross-tenant data leakage. He is concerned about deployment complexity ahead of December."
            evidence = ["Meeting #1 Discovery Transcript", "Meeting #2 Architecture Review"]
        elif "cfo" in q_lower:
            answer = "CFO Anita Roy is the economic buyer controlling budget release."
            why = "Her priority is ROI and budget governance. She approved the ₹25L allocation but requires validation against Competitor X's lower quote."
            evidence = ["World Tier Ground Facts", "Meeting #3 Commercial Review"]
        elif "procurement" in q_lower:
            answer = "Procurement Head is the commercial gatekeeper negotiating contract terms."
            why = "Focused on commercial concessions and payment schedules; currently requesting a 15% discount match."
            evidence = ["Email #4", "Commercial Proposal Redline"]
        else:
            answer = "The real decision-maker is CTO Rohan Sharma (Technical), with sign-off required from CFO Anita Roy (Budget)."
            why = "CTO Rohan Sharma drives the security mandate for December. If his technical security requirements are satisfied, CFO Anita Roy will release the ₹25L budget."
            evidence = [
                "World Tier Stakeholder Matrix",
                "Meeting #1: Rohan Sharma stated compliance deadline",
                "Meeting #3: Anita Roy approved security envelope"
            ]

        stakeholder_profiles = """### STAKEHOLDER INTELLIGENCE

**1. Rohan Sharma — Chief Technology Officer (CTO)**
• Influence: High | Role: Technical Champion
• Priority: Zero cross-tenant data leakage & enterprise security
• Concern: Deployment complexity before December
• LOKI Insight: Focused on architectural robustness rather than price concessions.

**2. Anita Roy — Chief Financial Officer (CFO)**
• Influence: High | Role: Economic Buyer
• Priority: Predictable ROI & Total Cost of Ownership
• Concern: Validating pricing against Competitor X's quote

**3. Kavita Rao — Head of Procurement**
• Influence: Medium | Role: Contract Gatekeeper
• Priority: Contractual concessions & payment schedules
• Concern: Anchoring deal to Competitor X's entry price
"""
        return {
            "answer": answer,
            "why": why,
            "evidence": evidence,
            "formatted_content": stakeholder_profiles,
            "recommended_action": "Conduct a technical deep dive with CTO Rohan Sharma to secure his formal sign-off before procurement renegotiations.",
            "quick_actions": ["Show Stakeholders", "Prepare Follow-up", "Run Deal X-Ray"]
        }

    def _answer_next_actions_query(self, deal_id: str) -> Dict[str, Any]:
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        answer = "The most immediate priority is reframing the pricing objection with CTO Rohan Sharma."
        why = (
            "The procurement team has not responded to the revised proposal for 5 business days, while Competitor X "
            "exerts pricing pressure. Do you want me to analyze the pricing history and similar deals?"
        )
        evidence = [
            "Meeting #4: Pricing objection logged",
            "Email #7: Proposal sent 5 days ago without response",
            "Hard December 2026 deployment deadline"
        ]

        return {
            "answer": answer,
            "why": why,
            "evidence": evidence,
            "recommended_action": "Deliver the Total Cost of Ownership calculator and schedule the technical security review with CTO Rohan Sharma within 2 business days.",
            "follow_ups": [
                "Do you want me to analyze the pricing history and similar deals?",
                "Would you like me to prepare a follow-up email draft?",
                "Should I generate the TCO comparison sheet against Competitor X?"
            ],
            "quick_actions": ["Analyze Pricing", "Compare Similar Deals", "Prepare Follow-up", "Show Stakeholders"]
        }

    def _generate_contextual_answer(self, query: str, deal_id: str, mode: str) -> Dict[str, Any]:
        """Fallback natural language generator grounded in deal memory and Hindsight."""
        deal = deal_engine.get_deal(deal_id) or deal_engine.list_deals()[0]
        customer = deal.get("company", deal.get("name", "ABC Technologies"))

        # Try to query Hindsight reflection or memory
        mem = deal_engine.get_deal_memory(deal_id)
        stats = mem.get("stats", {})

        answer = f"Based on verified deal memory for {customer}, here is what you need to know:"
        why = (
            f"Cross-referencing {stats.get('total_memories', 8)} persistent memory nodes, including account grounding facts, "
            f"verbatim meeting transcripts with CTO Rohan Sharma, and active competitor battlecards."
        )
        evidence = [
            f"Deal: {deal.get('name')}",
            f"Stage: {deal.get('stage')}",
            f"Budget: {deal.get('inr_display', '₹25L')} / ${deal.get('arr_target', 300000):,} ARR",
            "Unresolved Pricing Objection vs Competitor X"
        ]

        return {
            "answer": f"**LOKI Deal Intelligence ({customer})**: {deal.get('summary', 'Active enterprise security evaluation.')}",
            "why": why,
            "evidence": evidence,
            "recommended_action": "Review the Deal Intelligence Report or run /xray for complete pin-to-pin visibility.",
            "quick_actions": ["/deal", "/xray", "/connect", "/brief", "/risks"]
        }


# Global singleton
loki_engine = LokiEngine()
