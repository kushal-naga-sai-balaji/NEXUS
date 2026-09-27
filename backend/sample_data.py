"""
Sample enterprise deals and multi-stage interactions for Nexus Deal Intelligence.
Designed to showcase Hindsight's 4-tier memory hierarchy:
- World (Company profile, stakeholders, tech stack, constraints)
- Experience (Historical interactions, quotes, objections, outcomes)
- Observation (Emergent cross-deal patterns and correlation)
- Opinion / Mental Model (Synthesized tactical beliefs & win-rate playbooks)
"""

SAMPLE_DEALS = [
    {
        "id": "deal-acme-titan",
        "name": "Acme Cloud Services - Project Titan",
        "company": "Acme Cloud Services Inc.",
        "industry": "Enterprise Cloud & Infrastructure",
        "employees": 4200,
        "arr_target": 650000,
        "stage": "Proposal & Negotiation",
        "health_score": 88,
        "bank_id": "nexus-deal-acme-titan",
        "summary": "Full migration of customer telemetry pipeline to autonomous memory-driven agent cluster. Competitor Datadog actively offering aggressive renewal discount.",
        "stakeholders": [
            {
                "name": "Marcus Vance",
                "role": "CTO & Co-Founder",
                "disposition": "Visionary Champion",
                "focus": "Architectural scalability, memory persistence, zero latency degradation",
                "notes": "Loves the biomimetic memory concept. Agreed our architecture eliminates 80% of custom RAG pipeline maintenance."
            },
            {
                "name": "Elena Rostova",
                "role": "Chief Information Security Officer (CISO)",
                "disposition": "Skeptical Gatekeeper",
                "focus": "SOC2 Type II compliance, tenant data isolation, zero cross-tenant memory leakage",
                "notes": "Paranoid about AI models training on memory banks. Demands confirmation of isolated vector storage."
            },
            {
                "name": "David Sterling",
                "role": "Chief Financial Officer (CFO)",
                "disposition": "Cost-Cutting Negotiator",
                "focus": "ROI payback <6 months, benchmarking against Datadog renewal price",
                "notes": "Pushed back on $650k ARR; claimed Datadog offered 30% discount to keep telemetry workload."
            },
            {
                "name": "Chloe Zhao",
                "role": "Head of Enterprise Procurement",
                "disposition": "Contractual Gatekeeper",
                "focus": "Net-60 payment terms, 99.99% uptime SLA, SLA penalty credits",
                "notes": "Will try to extract 15% off list price in final MSA redlines."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Datadog",
                "threat_level": "High",
                "counter_position": "Datadog is purely reactive metric monitoring without persistent cognitive memory or automated root-cause healing. Retaining Hindsight memory reduces MTTR by 74%."
            },
            {
                "name": "In-house Custom RAG",
                "threat_level": "Medium",
                "counter_position": "Custom vector RAG lacks episodic/temporal reasoning (TEMPR) and requires 3 dedicated SREs to maintain."
            }
        ],
        "interactions": [
            {
                "id": "int-101",
                "date": "2026-08-10",
                "type": "Discovery Call",
                "stakeholder": "Marcus Vance (CTO)",
                "summary": "Marcus explained their agent fleet forgets critical session context every 24h. Showed deep interest in Hindsight's 4-tier memory hierarchy.",
                "objections": [
                    {
                        "category": "Technical Feasibility",
                        "text": "How does Hindsight manage memory retention without blowing past LLM context token windows?",
                        "status": "Resolved",
                        "winning_tactic": "Demonstrated TEMPR retrieval filtering (temporal window + entity scoring) keeping context under 4,000 tokens."
                    }
                ],
                "outcome": "Advanced to Security Review & Technical POC"
            },
            {
                "id": "int-102",
                "date": "2026-08-25",
                "type": "Security & Architecture Review",
                "stakeholder": "Elena Rostova (CISO)",
                "summary": "Intense security interrogation. Elena asked whether retained facts can leak between Acme customer tenants.",
                "objections": [
                    {
                        "category": "Security & Compliance",
                        "text": "If two tenants execute agents concurrently, how is vector bank isolation mathematically guaranteed?",
                        "status": "Resolved",
                        "winning_tactic": "Shared SOC2 Type II report + showed cryptographic per-bank namespace partitioning and isolated pgvector schemas."
                    }
                ],
                "outcome": "Security clearance granted pending final BAA & Data Processing Addendum."
            },
            {
                "id": "int-103",
                "date": "2026-09-12",
                "type": "Executive Pricing & ROI Review",
                "stakeholder": "David Sterling (CFO)",
                "summary": "David dropped a pricing bomb: Datadog offered them a 32% discount to renew their legacy contract. Demanded we drop from $650k to $450k.",
                "objections": [
                    {
                        "category": "Price & Budget",
                        "text": "Datadog is $200k cheaper. Unless you match their $450k price, we cannot justify switching to your platform.",
                        "status": "In Progress",
                        "winning_tactic": "Stood firm on platform value; countered with a 2-year term at $620k with complimentary White-Glove Migration Engineering (saving them $80k in contractor costs)."
                    }
                ],
                "outcome": "David agreed to review the 2-year total cost of ownership (TCO) comparison."
            }
        ]
    },
    {
        "id": "deal-fintech-global",
        "name": "FinTech Global - Real-Time Fraud Engine",
        "company": "FinTech Global Inc.",
        "industry": "Financial Services & Payments",
        "employees": 7800,
        "arr_target": 380000,
        "stage": "Technical Evaluation",
        "health_score": 92,
        "bank_id": "nexus-deal-fintech-global",
        "summary": "Deploying memory-augmented agents to retain multi-day fraud investigation patterns across cross-border wire transfers.",
        "stakeholders": [
            {
                "name": "Priya Patel",
                "role": "VP of Fraud Engineering",
                "disposition": "Data-Driven Buyer",
                "focus": "Inference latency under 120ms, high recall accuracy, audit logs",
                "notes": "Extremely metrics-oriented. Benchmark testing our TEMPR recall vs pgvector pure cosine similarity."
            },
            {
                "name": "Arthur Pendelton",
                "role": "Chief Compliance Officer",
                "disposition": "Regulatory Enforcer",
                "focus": "PCI-DSS Level 1, immutable audit trail for every retained fact",
                "notes": "Needs complete provenance on why an agent flagged a transaction as suspicious."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Snowflake Cortex",
                "threat_level": "Medium",
                "counter_position": "Snowflake is great for batch warehouse analytics, but cannot maintain dynamic real-time agent memory or temporal reflect reasoning."
            }
        ],
        "interactions": [
            {
                "id": "int-201",
                "date": "2026-09-02",
                "type": "Technical Benchmark Presentation",
                "stakeholder": "Priya Patel (VP Fraud)",
                "summary": "Presented live benchmark showing Hindsight TEMPR retrieval outperforming basic vector search by 3.8x on cross-border entity association.",
                "objections": [
                    {
                        "category": "Latency SLA",
                        "text": "Can Hindsight recall retrieve fraud patterns within our 100ms API response envelope?",
                        "status": "Resolved",
                        "winning_tactic": "Showed sub-45ms p99 recall with tag-scoped bank queries and cached entity graphs."
                    }
                ],
                "outcome": "Priya agreed to sign off on technical gate."
            }
        ]
    },
    {
        "id": "deal-healthpulse-ai",
        "name": "HealthPulse Systems - Clinical Scribe",
        "company": "HealthPulse Systems",
        "industry": "Healthcare & Digital Health",
        "employees": 2900,
        "arr_target": 490000,
        "stage": "Legal & Procurement",
        "health_score": 75,
        "bank_id": "nexus-deal-healthpulse-ai",
        "summary": "Clinical documentation agent remembering longitudinal patient medical history and physician dictation style across visits.",
        "stakeholders": [
            {
                "name": "Dr. Raymond Scott",
                "role": "Chief Medical Officer",
                "disposition": "Clinical Perfectionist",
                "focus": "Zero clinical hallucination, remembering physician specialty vocabulary",
                "notes": "Impressed by how Hindsight recalls doctor-specific abbreviations without retraining."
            },
            {
                "name": "Kimberly Adams",
                "role": "Director of Legal & Compliance",
                "disposition": "Zero-Risk Officer",
                "focus": "HIPAA Business Associate Agreement (BAA), data zero-retention on public LLM training",
                "notes": "Requires strict BAA and private VPC deployment commitment."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Nuance DAX / Microsoft",
                "threat_level": "High",
                "counter_position": "Nuance is closed-garden, rigid, and costs 2.5x more with no custom memory reflection or API control."
            }
        ],
        "interactions": [
            {
                "id": "int-301",
                "date": "2026-09-18",
                "type": "Executive Pitch",
                "stakeholder": "Dr. Raymond Scott (CMO)",
                "summary": "Demonstrated physician persona memory. Agent recalled Dr. Scott's preference for SOAP note formatting over narrative summaries.",
                "objections": [
                    {
                        "category": "Compliance",
                        "text": "Will patient PHI ever be retained in memory banks accessible across clinics?",
                        "status": "Resolved",
                        "winning_tactic": "Explained cryptographic bank_id tenancy and automatic de-identification entity scrubbers."
                    }
                ],
                "outcome": "Passed to Legal for BAA review."
            }
        ]
    }
]

# Pre-seeded Hindsight Memories across the 4 biomimetic tiers
INITIAL_HINDSIGHT_MEMORIES = [
    # TIER 1: WORLD (Facts, Profiles, Firmographics, Constraints)
    {
        "tier": "World",
        "bank_id": "nexus-deal-acme-titan",
        "text": "Acme Cloud Services has 4,200 employees, is currently migrating off Datadog, and operates on an annual fiscal budget ending October 31. Decision committee: Marcus Vance (CTO), Elena Rostova (CISO), David Sterling (CFO), Chloe Zhao (Procurement).",
        "type": "fact",
        "tags": ["account_profile", "budget_cycle", "stakeholders", "world"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "World"}
    },
    {
        "tier": "World",
        "bank_id": "nexus-deal-acme-titan",
        "text": "Acme CISO Elena Rostova requires SOC2 Type II certification, isolated vector storage namespaces, and verified zero cross-tenant leakage before any contract execution.",
        "type": "fact",
        "tags": ["ciso", "security_constraint", "compliance", "world"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "World"}
    },
    {
        "tier": "World",
        "bank_id": "nexus-deal-fintech-global",
        "text": "FinTech Global processes 14M daily transactions with a strict 120ms p99 latency SLA. Architecture is built on AWS us-east-1 with Kafka event streams.",
        "type": "fact",
        "tags": ["sla", "architecture", "fintech", "world"],
        "metadata": {"deal_id": "deal-fintech-global", "tier": "World"}
    },

    # TIER 2: EXPERIENCE (Episodic interactions, past quotes, objections, specific outcomes)
    {
        "tier": "Experience",
        "bank_id": "nexus-deal-acme-titan",
        "text": "In Discovery Call #1 (Aug 10), CTO Marcus Vance expressed strong frustration with agent context amnesia and confirmed their internal engineers failed to build reliable custom RAG.",
        "type": "experience",
        "tags": ["discovery", "cto", "pain_point", "experience"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "Experience"}
    },
    {
        "tier": "Experience",
        "bank_id": "nexus-deal-acme-titan",
        "text": "In Pricing Call #3 (Sep 12), CFO David Sterling demanded a 32% price cut to $450k, citing an aggressive retention counter-offer from Datadog. Rep offered a 2-year commit at $620k with complimentary migration engineering instead of discounting.",
        "type": "experience",
        "tags": ["pricing", "cfo", "datadog", "negotiation", "experience"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "Experience"}
    },
    {
        "tier": "Experience",
        "bank_id": "global-nexus-sales-intel",
        "text": "In Won Deal #84 (Nordic Cloud Systems), CFO raised the exact same Datadog 30% discount objection. We held firm on $580k ARR and added quarterly executive business reviews + free onboarding. Deal closed in 14 days without margin loss.",
        "type": "experience",
        "tags": ["won_deal", "cfo_objection", "datadog_displacement", "tactic_success", "experience"],
        "metadata": {"deal_id": "global-nexus-sales-intel", "tier": "Experience"}
    },

    # TIER 3: OBSERVATION (Patterns synthesized across deals and sessions)
    {
        "tier": "Observation",
        "bank_id": "global-nexus-sales-intel",
        "text": "Enterprise CFOs frequently use competitor discount quotes (especially Datadog and Splunk) as an anchoring tactic in late-stage negotiations. In 87% of closed deals, providing value-add migration credits rather than discounting base ARR preserves full contract margins.",
        "type": "observation",
        "tags": ["cfo_pattern", "discount_anchoring", "margin_preservation", "observation"],
        "metadata": {"deal_id": "global-nexus-sales-intel", "tier": "Observation"}
    },
    {
        "tier": "Observation",
        "bank_id": "nexus-deal-acme-titan",
        "text": "Whenever Elena Rostova (CISO) is provided proactively with third-party penetration test summaries and architecture topology diagrams before calls, her review cycle accelerates from 3 weeks to 4 business days.",
        "type": "observation",
        "tags": ["ciso_pattern", "velocity", "security_dossier", "observation"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "Observation"}
    },

    # TIER 4: OPINION / MENTAL MODEL (High-level tactical beliefs, persona psychology, win playbooks)
    {
        "tier": "Opinion",
        "bank_id": "global-nexus-sales-intel",
        "text": "Mental Model: Datadog Competitor Displacement Playbook. Datadog sells infrastructure visibility, whereas Hindsight provides cognitive agent action and learning. When buyers compare the two, reframe Datadog as 'the rear-view mirror' and Hindsight as 'the autonomous driver'. Never engage in a feature-by-feature tickbox; anchor on cost of human engineering toil.",
        "type": "opinion",
        "tags": ["mental_model", "datadog_playbook", "reframing_tactic", "opinion"],
        "metadata": {"deal_id": "global-nexus-sales-intel", "tier": "Opinion"}
    },
    {
        "tier": "Opinion",
        "bank_id": "nexus-deal-acme-titan",
        "text": "Mental Model: David Sterling (CFO) Buyer Psychology. David responds positively to total cost of ownership (TCO) graphs showing engineering hours saved over 24 months. He respects firm negotiation backed by data, but becomes suspicious if a vendor discounts immediately.",
        "type": "opinion",
        "tags": ["buyer_psychology", "cfo_strategy", "negotiation_belief", "opinion"],
        "metadata": {"deal_id": "deal-acme-titan", "tier": "Opinion"}
    }
]

# Guided Demo Script Steps for Hackathon Presentation
GUIDED_DEMO_STEPS = [
    {
        "step": 1,
        "title": "Day 1: Cold Discovery & Grounding",
        "deal_id": "deal-acme-titan",
        "scenario": "Rep meets CTO Marcus Vance. Agent retains foundational company profile and architectural pain points into Hindsight's World & Experience memory tiers.",
        "action": "ingest_meeting",
        "preset_meeting": {
            "type": "Discovery Call",
            "stakeholder": "Marcus Vance (CTO)",
            "transcript": "Marcus: Our biggest headache is that every time an agent session completes, all context evaporates. We spent 4 months building a custom LangChain vector RAG on Postgres, but it hallucinates past agreements and has zero temporal awareness. We need agents that actually learn from past outages and customer tickets."
        }
    },
    {
        "step": 2,
        "title": "Day 30: Security Interrogation & Memory Recall",
        "deal_id": "deal-acme-titan",
        "scenario": "CISO Elena Rostova challenges tenant isolation. Without memory, reps stumble; with Hindsight memory recall, the agent instantly retrieves architecture guarantees.",
        "action": "tactical_objection",
        "objection_input": "How can you guarantee our customer data in your memory banks won't leak into other clients' agent sessions or be used to train models?"
    },
    {
        "step": 3,
        "title": "Day 60: CFO Price War & Competitor Trap",
        "deal_id": "deal-acme-titan",
        "scenario": "CFO David Sterling threatens to renew with Datadog for a 32% discount. Agent recalls past won deals with identical objections and prepares a counter-tactic.",
        "action": "pre_call_brief",
        "call_type": "CFO Pricing Showdown",
        "stakeholder": "David Sterling (CFO)"
    },
    {
        "step": 4,
        "title": "Day 90: Deep Strategic Reflection",
        "deal_id": "deal-acme-titan",
        "scenario": "Hindsight runs 'reflect' across all interactions and global sales intel, synthesizing an updated Competitor Displacement Playbook and buyer psychological models.",
        "action": "trigger_reflection"
    }
]

# The Cognitive Learning Curve (Shows the agent getting visibly smarter over time)
LEARNING_CURVE_STAGES = [
    {
        "stage": 1,
        "label": "Call 1: Cold Discovery",
        "timeline": "Day 1",
        "competence": 32,
        "status": "Level 1: Generic AI",
        "badge_color": "rose",
        "summary": "Agent has zero prior history. Gives bland, generic responses. Ingests foundational company profile and CTO pain points.",
        "memory_impact": "+2 World Facts Retained",
        "sample_dialogue_before": "“We offer an AI platform that helps enterprise teams manage agents and context.”",
        "sample_dialogue_after": "“Marcus, we understand your custom LangChain RAG is failing on temporal reasoning across session boundaries.”"
    },
    {
        "stage": 2,
        "label": "Call 2: Security Grilling",
        "timeline": "Day 15",
        "competence": 65,
        "status": "Level 2: Context-Aware",
        "badge_color": "amber",
        "summary": "Agent recalls Call 1 architecture. Anticipates CISO Elena Rostova's security requirements. Retains SOC2 compliance proof.",
        "memory_impact": "+3 Experience & Observation Nodes",
        "sample_dialogue_before": "“We take security very seriously and follow industry-standard encryption practices.”",
        "sample_dialogue_after": "“Elena, Hindsight enforces cryptographic per-bank namespace partitioning with isolated pgvector schemas.”"
    },
    {
        "stage": 3,
        "label": "Call 3: CFO Price War",
        "timeline": "Day 45",
        "competence": 88,
        "status": "Level 3: Tactical Defender",
        "badge_color": "cyan",
        "summary": "CFO David Sterling drops a 32% discount ultimatum. Agent recalls Call 1 ROI math and Won Deal #84, saving $170,000 in ARR margin.",
        "memory_impact": "+2 Tactical Cross-Deal Playbooks",
        "sample_dialogue_before": "“We really value your business and can match Datadog's $450k price immediately.”",
        "sample_dialogue_after": "“David, rather than cutting ARR, we will structure a 2-year commit at $620k with complimentary migration engineering.”"
    },
    {
        "stage": 4,
        "label": "Call 4: Executive Closing",
        "timeline": "Day 60",
        "competence": 98,
        "status": "Level 4: Master Strategist",
        "badge_color": "emerald",
        "summary": "Agent synthesizes company-wide market mental models using Hindsight reflect. Closes $620k ARR contract with 0% margin leakage.",
        "memory_impact": "Living Competitor Playbooks Generated",
        "sample_dialogue_before": "“Here is our standard master services agreement.”",
        "sample_dialogue_after": "“We have pre-aligned Marcus on architecture, Elena on isolated vector tenancy, and structured David's quarterly billing.”"
    }
]

# Realistic High-Stakes Enterprise Artifacts
ENTERPRISE_ARTIFACTS = {
    "ciso_email_thread": {
        "title": "Email Redline: CISO Security Review (Elena Rostova)",
        "from": "Elena Rostova <e.rostova@acmecloud.io>",
        "to": "Sarah Jenkins <sarah.j@nexusintel.ai>",
        "date": "August 25, 2026, 3:14 PM EDT",
        "subject": "RE: Security Questionnaire Redline - Vector Bank Isolation & Data Retention",
        "body": """Sarah,

We reviewed Section 4.2 of your Data Processing Addendum. Our infosec team flagged that your agent uses an embedded memory bank architecture.

Before I can sign off on the technical gate for CTO Marcus Vance:
1. We need mathematical assurance that our telemetry embeddings cannot leak into other tenants' memory spaces during concurrent execution.
2. We require confirmation that customer memory is never piped to upstream foundational LLMs (e.g. OpenAI or Anthropic) for model fine-tuning or distillation.
3. Please provide your latest SOC2 Type II bridge letter covering Annex A.14.

If this cannot be verified in writing by end of week, we will pause evaluation until our Q4 audit cycle.

Elena Rostova
Chief Information Security Officer | Acme Cloud Services Inc."""
    },
    "enterprise_quote_sheet": {
        "title": "Enterprise Order Form: Project Titan ($650,000 ARR)",
        "client": "Acme Cloud Services Inc.",
        "term": "24 Months (Annual Invoicing)",
        "items": [
            {"sku": "NX-AGENT-CORE-ENT", "desc": "Nexus Cognitive Agent Platform (Unlimited Workflows)", "qty": 1, "unit": "$380,000", "total": "$380,000"},
            {"sku": "HS-BANK-DEDICATED", "desc": "Vectorize Hindsight Dedicated Enterprise Memory Cluster (SOC2 Isolated)", "qty": 4, "unit": "$45,000", "total": "$180,000"},
            {"sku": "NX-TEMPR-INGEST", "desc": "High-Throughput TEMPR Telemetry Ingestion (15M events/mo)", "qty": 1, "unit": "$90,000", "total": "$90,000"},
            {"sku": "NX-ENG-MIGRATE", "desc": "White-Glove Datadog Telemetry Migration Engineering", "qty": 1, "unit": "$50,000", "total": "$0 (Concession Credit)"}
        ],
        "list_total": "$700,000",
        "effective_arr": "$650,000",
        "margin_preserved": "$170,000 vs Competitor Discount"
    },
    "competitor_teardown": {
        "title": "Competitive Teardown: Datadog APM vs Nexus + Hindsight",
        "comparison": [
            {
                "metric": "Core Philosophy",
                "datadog": "Passive observability (Metrics, Traces, Dashboards)",
                "nexus": "Active cognitive memory (Recalls incidents, self-heals, learns)"
            },
            {
                "metric": "Memory Persistence",
                "datadog": "None. Raw time-series logs retained for 15 days.",
                "nexus": "Biomimetic 4-tier hierarchy (World, Experience, Observation, Opinion)."
            },
            {
                "metric": "TCO & Engineering Toil",
                "datadog": "Requires full SRE team to interpret dashboards ($680k/yr).",
                "nexus": "Autonomous reflection cuts triage toil by 74%."
            },
            {
                "metric": "Discount Behavior",
                "datadog": "Offers 30-35% desperation discounts to protect renewals.",
                "nexus": "Never discounts base ARR; trades value-add migration credits."
            }
        ]
    }
}
