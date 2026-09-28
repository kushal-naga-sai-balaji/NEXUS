"""
NEXUS // DEAL INTELLIGENCE AGENT - DATA REPOSITORY
Production-grade enterprise sales copilot with persistent biomimetic memory.
Stores:
- Customers (ABC Technologies, Nova Systems, Vertex Finance, CloudCore Solutions)
- Deals across stages with dual currency (INR ₹ and USD $)
- 4-Tier Memory (World, Experience, Observation, Opinion)
- Stakeholders, Competitors, Objections, Pricing, Next Actions, Risks
- Meetings, Tasks, Connected Emails, Analytics, Historical Deals
- Live Call Demo Stream Sequence
"""

SAMPLE_CUSTOMERS = [
    {
        "id": "cust-abc",
        "name": "ABC Technologies",
        "industry": "Enterprise Software & Cloud Security",
        "employees": 3500,
        "headquarters": "Bengaluru, India & San Francisco, USA",
        "annual_revenue": "₹450 Cr",
        "website": "https://abctechnologies.io",
        "primary_contact": "Rohan Sharma (CTO)",
        "account_owner": "Sarah Jenkins (Senior AE)",
        "tier": "Tier-1 Enterprise",
        "active_deals": ["deal-abc-security"],
        "summary": "Fast-growing B2B cloud infra provider migrating from legacy perimeter defenses. High emphasis on enterprise compliance, SOC2, and Q4 deployment deadline."
    },
    {
        "id": "cust-nova",
        "name": "Nova Systems",
        "industry": "Cloud Infrastructure & Observability",
        "employees": 5200,
        "headquarters": "Mumbai, India & Austin, USA",
        "annual_revenue": "₹820 Cr",
        "website": "https://novasystems.com",
        "primary_contact": "Marcus Vance (CTO)",
        "account_owner": "Alex Rivera (Enterprise AE)",
        "tier": "Strategic Enterprise",
        "active_deals": ["deal-nova-infra"],
        "summary": "Full migration of customer telemetry pipeline to autonomous agent cluster. Competitor Datadog aggressively offering 32% renewal discount."
    },
    {
        "id": "cust-vertex",
        "name": "Vertex Finance",
        "industry": "Financial Services & Cross-Border Payments",
        "employees": 7800,
        "headquarters": "Singapore & London, UK",
        "annual_revenue": "₹1,400 Cr",
        "website": "https://vertexfinance.global",
        "primary_contact": "Priya Patel (VP Engineering)",
        "account_owner": "Sarah Jenkins (Senior AE)",
        "tier": "Tier-1 Banking",
        "active_deals": ["deal-vertex-fraud"],
        "summary": "Deploying real-time fraud detection agent cluster requiring strict 120ms p99 inference latency and PCI-DSS Level 1 compliance."
    },
    {
        "id": "cust-cloudcore",
        "name": "CloudCore Solutions",
        "industry": "Healthcare & Clinical Systems",
        "employees": 2900,
        "headquarters": "Hyderabad, India & Boston, USA",
        "annual_revenue": "₹320 Cr",
        "website": "https://cloudcoresolutions.ai",
        "primary_contact": "Dr. Raymond Scott (CMO)",
        "account_owner": "Alex Rivera (Enterprise AE)",
        "tier": "Healthcare Enterprise",
        "active_deals": ["deal-cloudcore-protection"],
        "summary": "Clinical documentation agent remembering patient longitudinal history across hospital visits. Currently in legal review for HIPAA BAA."
    }
]

SAMPLE_DEALS = [
    {
        "id": "deal-abc-security",
        "customer_id": "cust-abc",
        "name": "Enterprise Security Platform",
        "company": "ABC Technologies",
        "industry": "Enterprise Software & Cloud Security",
        "employees": 3500,
        "arr_target": 300000,
        "arr_target_inr": "₹25,00,000",
        "deal_value_display": "₹25,00,000 ($300k)",
        "list_price": 350000,
        "stage": "Negotiation",
        "health_score": 82,
        "bank_id": "nexus-deal-abc-security",
        "summary": "Enterprise-wide rollout of autonomous memory-driven security copilot. Customer is benchmarking against Competitor X and has a strict December deployment deadline.",
        "requirements": [
            {"id": "req-1", "title": "Enterprise Security & SOC2 Compliance", "status": "Validated", "priority": "High"},
            {"id": "req-2", "title": "Deployment Before December 2026", "status": "Active Deadline", "priority": "Critical"},
            {"id": "req-3", "title": "24/7 Dedicated Support SLA", "status": "Approved", "priority": "High"},
            {"id": "req-4", "title": "Zero Cross-Tenant Memory Leakage", "status": "Validated", "priority": "Critical"}
        ],
        "stakeholders": [
            {
                "name": "Rohan Sharma",
                "role": "Chief Technology Officer (CTO)",
                "department": "Engineering & Technology",
                "influence": "High (Decision Maker)",
                "interest_score": 92,
                "disposition": "Visionary Technical Champion",
                "priority": "Security & Architecture",
                "concern": "Deployment complexity & temporal reasoning across sessions",
                "focus": "Architectural scalability, memory persistence, zero latency degradation",
                "notes": "Loves biomimetic memory. Strongly wants autonomous healing rather than basic logs.",
                "communication_history": "3 Zoom calls, 4 email exchanges. Highly responsive."
            },
            {
                "name": "Anita Roy",
                "role": "Chief Financial Officer (CFO)",
                "department": "Finance",
                "influence": "High (Economic Buyer)",
                "interest_score": 68,
                "disposition": "Cost-Cutting Negotiator",
                "priority": "Cost & ROI",
                "concern": "Budget constraint (₹25L cap) vs Competitor X quote",
                "focus": "Payback under 6 months, benchmarked against Competitor X",
                "notes": "Dropped pricing objection citing Competitor X's 15% discount.",
                "communication_history": "1 executive pricing call, 2 financial model emails."
            },
            {
                "name": "Priya Menon",
                "role": "Head of Enterprise Procurement",
                "department": "Procurement & Legal",
                "influence": "Medium (Gatekeeper)",
                "interest_score": 62,
                "disposition": "Contractual Gatekeeper",
                "priority": "Contract & SLA Terms",
                "concern": "Net-60 payment terms, 99.99% uptime SLA penalties",
                "focus": "Commercial MSA redlines, penalty credits",
                "notes": "Will seek 10-15% discount in final contract review.",
                "communication_history": "MSA redline exchange via procurement portal."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Competitor X",
                "threat_level": "High",
                "mentions_count": 4,
                "advantages_mentioned": "Offered lower initial sticker price (15% discount to win the logo).",
                "weaknesses_mentioned": "Lacks cognitive memory, higher manual SRE maintenance toil, rigid architecture.",
                "counter_position": "Competitor X offers a lower initial license price, but requires 3 full-time engineers (₹36L/yr) to maintain custom scripts. Nexus provides autonomous self-healing memory with 74% MTTR reduction.",
                "kill_points": [
                    "Can Competitor X recall incident post-mortems across 6 months without manual retraining?",
                    "What is the total implementation cost including engineering maintenance hours?"
                ]
            }
        ],
        "pricing_details": {
            "arr_target": 300000,
            "arr_target_inr": "₹25,00,000",
            "list_price": 350000,
            "competitor_offer": 210000,
            "competitor_offer_inr": "₹17,50,000",
            "margin_saved": 90000,
            "margin_saved_inr": "₹7,50,000",
            "budget_cap": "₹25,00,000",
            "previous_discount_request": "15%",
            "billing_term": "Annual Commit",
            "budget_cycle": "Q4 Budget Ending Dec 2026",
            "concessions_log": [
                {
                    "item": "Complimentary Migration Engineering Credits",
                    "value": "₹3,50,000 ($42k)",
                    "status": "Granted",
                    "trade_received": "Secured executive commitment to protect ₹25L base ARR."
                },
                {
                    "item": "Base ARR Discount to match Competitor X ₹17.5L",
                    "value": "₹7,50,000 ($90k)",
                    "status": "Firmly Rejected",
                    "trade_received": "Preserved company recurring gross margins."
                }
            ]
        },
        "milestones": [
            {
                "id": "m1",
                "name": "Initial Discovery & Requirements",
                "status": "Completed",
                "date": "2026-08-15",
                "owner": "Rohan Sharma (CTO)",
                "summary": "Validated requirement for enterprise security and persistent agent memory."
            },
            {
                "id": "m2",
                "name": "Technical Architecture Demonstration",
                "status": "Completed",
                "date": "2026-08-28",
                "owner": "Rohan Sharma (CTO)",
                "summary": "Demonstrated sub-45ms TEMPR recall with context token windows under 4k tokens."
            },
            {
                "id": "m3",
                "name": "Security & Compliance Verification",
                "status": "Completed",
                "date": "2026-09-10",
                "owner": "Rohan Sharma (CTO)",
                "summary": "Shared SOC2 Type II bridge letter and vector namespace isolation documentation."
            },
            {
                "id": "m4",
                "name": "Executive Pricing & Negotiation",
                "status": "In Progress",
                "date": "2026-09-28",
                "owner": "Anita Roy (CFO)",
                "summary": "Overcoming Competitor X price objection through 24-month TCO model."
            },
            {
                "id": "m5",
                "name": "Procurement & Legal MSA Signoff",
                "status": "Upcoming",
                "date": "2026-10-15",
                "owner": "Priya Menon (Procurement)",
                "summary": "Finalizing Net-60 terms and SLA guarantees."
            },
            {
                "id": "m6",
                "name": "Production Deployment",
                "status": "Upcoming",
                "date": "2026-11-20",
                "owner": "Executive Committee",
                "summary": "Target go-live ahead of December hard deadline."
            }
        ],
        "risks": [
            {
                "id": "r1",
                "category": "Pricing Objection Unresolved",
                "severity": "High",
                "warning": "Customer stated Competitor X price is lower. Unresolved objection creates risk of margin erosion.",
                "mitigation": "Focus on total cost of ownership and measurable ROI. Trade migration engineering credits rather than base price discounts."
            },
            {
                "id": "r2",
                "category": "Hard December Deployment Deadline",
                "severity": "Medium",
                "warning": "If procurement redlines drag past October, deployment before December may slip.",
                "mitigation": "Align procurement on standard pre-approved MSA templates with Net-60 terms."
            }
        ],
        "next_actions": [
            {
                "id": "na-1",
                "priority": "Urgent",
                "action": "Address Pricing Concern with TCO Model",
                "reason": "Customer benchmarked against Competitor X discount.",
                "target_stakeholder": "Anita Roy (CFO)",
                "channel": "Executive Briefing & TCO Deck",
                "timing": "Within 24 hours",
                "expected_impact": "Neutralizes Competitor X price challenge and preserves ₹25L ARR.",
                "script_template": "Ask whether the concern is initial sticker price or overall implementation cost. Show that Competitor X requires ₹36L in annual engineering maintenance toil."
            },
            {
                "id": "na-2",
                "priority": "High",
                "action": "Confirm December Deployment Timeline Schedule",
                "reason": "CTO Rohan Sharma indicated December is a non-negotiable go-live date.",
                "target_stakeholder": "Rohan Sharma (CTO)",
                "channel": "Technical Roadmap Sync",
                "timing": "Before Friday",
                "expected_impact": "Proves readiness and locks in technical gate.",
                "script_template": "Rohan, our deployment engineering team has reserved a 14-day onboarding sprint beginning November 1, guaranteeing full go-live 10 days before your December deadline."
            }
        ],
        "follow_ups": [
            {
                "id": "fu-1",
                "stakeholder": "Anita Roy (CFO)",
                "topic": "TCO spreadsheet & ROI comparison against Competitor X",
                "due_date": "2026-09-30",
                "status": "Scheduled",
                "optimal_timing": "Tuesday 10:00 AM IST",
                "recommended_channel": "Email with TCO spreadsheet",
                "draft_message": "Hi Anita, Following up on our pricing discussion: attached is our 24-month TCO analysis detailing how autonomous memory eliminates ₹36L in engineering maintenance compared to Competitor X."
            },
            {
                "id": "fu-2",
                "stakeholder": "Rohan Sharma (CTO)",
                "topic": "December onboarding sprint confirmation",
                "due_date": "2026-10-02",
                "status": "Scheduled",
                "optimal_timing": "Thursday 2:30 PM IST",
                "recommended_channel": "Slack Connect",
                "draft_message": "Hi Rohan, our engineering team confirmed the staging cluster is provisioned and ready to meet your December deployment milestone."
            }
        ],
        "winning_patterns": [
            {
                "id": "wp-1",
                "name": "ROI & Total Cost of Ownership Justification",
                "source_deal": "Deal #1024 (FinTech ₹30L Won)",
                "success_rate": "Worked in 4 similar deals",
                "playbook": "When competitor drops a lower sticker price, shift the axis from software license cost to implementation engineering toil. Trade migration engineering credits rather than base price discounts.",
                "applicability": "100% Match with ABC Technologies Competitor X objection"
            },
            {
                "id": "wp-2",
                "name": "Phased Implementation Milestone Lock",
                "source_deal": "Deal #1088 (SaaS ₹22L Won)",
                "success_rate": "100% On-time Close",
                "playbook": "Provide day-by-day deployment sprint timeline guaranteeing go-live 10 days prior to customer fiscal/quarterly deadline.",
                "applicability": "Directly resolves December deployment deadline requirement"
            }
        ],
        "strategy_playbook": {
            "primary_narrative": "Autonomous Memory vs SRE Engineering Toil",
            "executive_alignment": "Partner with CTO Rohan Sharma on architecture; leverage engineering toil savings to overcome CFO Anita's cost objections.",
            "closing_blueprint": "Deliver TCO model -> Confirm December sprint -> Finalize Procurement Net-60 terms -> Signed MSA by Oct 20."
        },
        "interactions": [
            {
                "id": "int-abc-1",
                "date": "2026-08-15",
                "type": "Discovery Call",
                "stakeholder": "Rohan Sharma (CTO)",
                "summary": "Rohan explained their need for an enterprise security platform with memory persistence across agent sessions.",
                "decisions": ["Proceed to technical POC."],
                "customer_action_items": ["Share staging architecture specs."],
                "rep_action_items": ["Deliver sub-45ms latency benchmark."],
                "objections": [],
                "outcome": "Advanced to Technical Evaluation"
            },
            {
                "id": "int-abc-2",
                "date": "2026-09-12",
                "type": "Executive Pricing Call",
                "stakeholder": "Anita Roy (CFO)",
                "summary": "Anita stated Competitor X offered lower pricing (15% discount). Rep countered with ROI model and migration engineering credits.",
                "decisions": ["Anita agreed to review 24-month TCO comparison."],
                "customer_action_items": ["CFO team to review engineering toil numbers."],
                "rep_action_items": ["Build custom TCO model."],
                "objections": [
                    {
                        "category": "Pricing",
                        "text": "Your price is higher than Competitor X.",
                        "status": "In Progress",
                        "winning_tactic": "Focus on total cost of ownership and measurable ROI. Ask whether concern is initial price or implementation toil."
                    }
                ],
                "outcome": "TCO review pending"
            }
        ]
    },
    {
        "id": "deal-nova-infra",
        "customer_id": "cust-nova",
        "name": "Cloud Infrastructure Upgrade",
        "company": "Nova Systems",
        "industry": "Cloud Infrastructure & Observability",
        "employees": 5200,
        "arr_target": 550000,
        "arr_target_inr": "₹45,00,000",
        "deal_value_display": "₹45,00,000 ($550k)",
        "list_price": 600000,
        "stage": "Proposal",
        "health_score": 88,
        "bank_id": "nexus-deal-nova-infra",
        "summary": "Full migration of customer telemetry pipeline to autonomous memory-driven agent cluster. Datadog actively offering aggressive 32% discount.",
        "requirements": [
            {"id": "req-1", "title": "Context retention across agent fleets", "status": "Validated", "priority": "High"},
            {"id": "req-2", "title": "Sub-45ms p99 recall SLA", "status": "Validated", "priority": "Critical"}
        ],
        "stakeholders": [
            {
                "name": "Marcus Vance",
                "role": "CTO & Co-Founder",
                "department": "Engineering",
                "influence": "High (Technical Champion)",
                "interest_score": 94,
                "disposition": "Visionary Champion",
                "priority": "Scalability & Zero Toil",
                "concern": "Token blowouts with LangChain",
                "focus": "Memory persistence across session boundaries",
                "notes": "Loves biomimetic memory.",
                "communication_history": "Regular weekly syncs."
            },
            {
                "name": "David Sterling",
                "role": "Chief Financial Officer (CFO)",
                "department": "Finance",
                "influence": "High (Economic Buyer)",
                "interest_score": 70,
                "disposition": "Cost-Cutting Negotiator",
                "priority": "ARR & Discounting",
                "concern": "Comparing with Datadog renewal price",
                "focus": "Payback period",
                "notes": "Demanded 32% discount to match Datadog.",
                "communication_history": "1 pricing review call."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Datadog",
                "threat_level": "High",
                "mentions_count": 5,
                "advantages_mentioned": "Incumbent vendor, 32% discount offer.",
                "weaknesses_mentioned": "Purely passive monitoring; zero cognitive memory.",
                "counter_position": "Datadog is purely reactive metric monitoring without persistent memory. Hindsight cuts triage toil by 74%.",
                "kill_points": ["Can Datadog remember past incident post-mortems across 6 months?"]
            }
        ],
        "pricing_details": {
            "arr_target": 550000,
            "arr_target_inr": "₹45,00,000",
            "list_price": 600000,
            "competitor_offer": 374000,
            "competitor_offer_inr": "₹31,00,000",
            "margin_saved": 176000,
            "margin_saved_inr": "₹14,00,000",
            "budget_cap": "₹45,00,000",
            "previous_discount_request": "32%",
            "billing_term": "24 Months Commit",
            "budget_cycle": "Fiscal Year Ends Oct 31",
            "concessions_log": [
                {
                    "item": "White-Glove Migration Engineering",
                    "value": "$50,000 credit",
                    "status": "Granted",
                    "trade_received": "Secured 2-year commit at full ARR."
                }
            ]
        },
        "milestones": [
            {
                "id": "m1",
                "name": "Discovery Call",
                "status": "Completed",
                "date": "2026-08-10",
                "owner": "Marcus Vance",
                "summary": "Validated CTO pain points."
            },
            {
                "id": "m2",
                "name": "Proposal Presentation",
                "status": "In Progress",
                "date": "2026-09-20",
                "owner": "David Sterling",
                "summary": "Reviewing 2-year commit terms."
            }
        ],
        "risks": [
            {
                "id": "r1",
                "category": "Competitor Price Pressure",
                "severity": "High",
                "warning": "Datadog aggressive renewal discount threatens margins.",
                "mitigation": "Hold ARR firm; trade migration credits."
            }
        ],
        "next_actions": [
            {
                "id": "na-1",
                "priority": "High",
                "action": "Deliver 24-Month TCO Model",
                "reason": "CFO requested comparison with Datadog.",
                "target_stakeholder": "David Sterling (CFO)",
                "channel": "Executive Briefing",
                "timing": "This week",
                "expected_impact": "Protects ₹45L contract value.",
                "script_template": "David, our side-by-side model shows $680k in annual engineering toil savings."
            }
        ],
        "follow_ups": [
            {
                "id": "fu-1",
                "stakeholder": "David Sterling (CFO)",
                "topic": "TCO review",
                "due_date": "2026-10-02",
                "status": "Scheduled",
                "optimal_timing": "Thursday 2:30 PM",
                "recommended_channel": "Email",
                "draft_message": "Hi David, I have prepared the 24-month financial model for your review."
            }
        ],
        "winning_patterns": [
            {
                "id": "wp-1",
                "name": "Migration Concession Trade",
                "source_deal": "Nordic Cloud Systems (Won Deal #84)",
                "success_rate": "87% Win Rate",
                "playbook": "Refuse ARR discount; concede $50k in white-glove engineering onboarding.",
                "applicability": "100% Match with Datadog objection"
            }
        ],
        "strategy_playbook": {
            "primary_narrative": "Autonomous Self-Healing vs Passive Dead Logs",
            "executive_alignment": "Partner with Marcus to neutralize David's cost objections.",
            "closing_blueprint": "Deliver TCO -> Finalize 2-year commit -> Close by Oct 31."
        },
        "interactions": []
    },
    {
        "id": "deal-vertex-fraud",
        "customer_id": "cust-vertex",
        "name": "Cybersecurity Transformation",
        "company": "Vertex Finance",
        "industry": "Financial Services & Cross-Border Payments",
        "employees": 7800,
        "arr_target": 420000,
        "arr_target_inr": "₹35,00,000",
        "deal_value_display": "₹35,00,000 ($420k)",
        "list_price": 460000,
        "stage": "Technical Evaluation",
        "health_score": 90,
        "bank_id": "nexus-deal-vertex-fraud",
        "summary": "Deploying memory-augmented agents to retain multi-day fraud investigation patterns across cross-border wire transfers.",
        "requirements": [
            {"id": "req-1", "title": "Sub-120ms API response envelope", "status": "Validated", "priority": "Critical"},
            {"id": "req-2", "title": "PCI-DSS Level 1 compliance", "status": "Under Review", "priority": "Critical"}
        ],
        "stakeholders": [
            {
                "name": "Priya Patel",
                "role": "VP of Fraud Engineering",
                "department": "Fraud & Security",
                "influence": "High (Technical Buyer)",
                "interest_score": 96,
                "disposition": "Data-Driven Buyer",
                "priority": "Latency & Recall SLA",
                "concern": "Peak transaction throughput",
                "focus": "120ms latency SLA",
                "notes": "Extremely metrics-oriented.",
                "communication_history": "Weekly technical POC calls."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "Snowflake Cortex",
                "threat_level": "Medium",
                "mentions_count": 2,
                "advantages_mentioned": "Existing warehouse contract.",
                "weaknesses_mentioned": "Batch warehouse analytics only, zero real-time agent memory.",
                "counter_position": "Snowflake is great for batch warehouse analytics, but cannot maintain dynamic real-time agent memory.",
                "kill_points": ["Can Snowflake update agent memory mid-transaction within 50ms?"]
            }
        ],
        "pricing_details": {
            "arr_target": 420000,
            "arr_target_inr": "₹35,00,000",
            "list_price": 460000,
            "competitor_offer": 320000,
            "competitor_offer_inr": "₹26,50,000",
            "margin_saved": 40000,
            "margin_saved_inr": "₹3,50,000",
            "budget_cap": "₹35,00,000",
            "previous_discount_request": "10%",
            "billing_term": "Annual Prepaid",
            "budget_cycle": "Q4 Budget",
            "concessions_log": []
        },
        "milestones": [
            {
                "id": "m1",
                "name": "Technical Benchmark",
                "status": "Completed",
                "date": "2026-09-02",
                "owner": "Priya Patel",
                "summary": "TEMPR outperformed pure vector search by 3.8x."
            }
        ],
        "risks": [],
        "next_actions": [
            {
                "id": "na-1",
                "priority": "High",
                "action": "Deliver PCI-DSS Compliance Packet",
                "reason": "Compliance review requirement.",
                "target_stakeholder": "Priya Patel",
                "channel": "Email",
                "timing": "Tomorrow",
                "expected_impact": "Clears regulatory gate.",
                "script_template": "Priya, here is the official PCI audit trail mapping."
            }
        ],
        "follow_ups": [],
        "winning_patterns": [],
        "strategy_playbook": {
            "primary_narrative": "Sub-50ms Real-Time Fraud Cognition",
            "executive_alignment": "Priya Patel is an enthusiastic champion.",
            "closing_blueprint": "Deliver PCI compliance packet -> Finalize proposal."
        },
        "interactions": []
    },
    {
        "id": "deal-cloudcore-protection",
        "customer_id": "cust-cloudcore",
        "name": "Data Protection Platform",
        "company": "CloudCore Solutions",
        "industry": "Healthcare & Clinical Systems",
        "employees": 2900,
        "arr_target": 340000,
        "arr_target_inr": "₹28,00,000",
        "deal_value_display": "₹28,00,000 ($340k)",
        "list_price": 380000,
        "stage": "Legal & Security Review",
        "health_score": 75,
        "bank_id": "nexus-deal-cloudcore-protection",
        "summary": "Clinical documentation agent remembering longitudinal patient medical history. Requires strict HIPAA BAA and isolated VPC deployment.",
        "requirements": [
            {"id": "req-1", "title": "Zero PHI retention on public models", "status": "Validated", "priority": "Critical"},
            {"id": "req-2", "title": "HIPAA BAA agreement", "status": "In Legal Redline", "priority": "Critical"}
        ],
        "stakeholders": [
            {
                "name": "Dr. Raymond Scott",
                "role": "Chief Medical Officer",
                "department": "Clinical Informatics",
                "influence": "High (Clinical Sponsor)",
                "interest_score": 88,
                "disposition": "Clinical Perfectionist",
                "priority": "Zero Hallucination",
                "concern": "Clinical shorthand accuracy",
                "focus": "Longitudinal patient memory",
                "notes": "Loves physician abbreviation recall.",
                "communication_history": "Clinical demo call."
            }
        ],
        "competitors_mentioned": [
            {
                "name": "In-house Custom RAG",
                "threat_level": "Medium",
                "mentions_count": 2,
                "advantages_mentioned": "Built internally on PostgreSQL.",
                "weaknesses_mentioned": "Suffers temporal amnesia, violates HIPAA on shared indexes.",
                "counter_position": "Custom vector RAG lacks episodic/temporal reasoning and creates severe compliance liability.",
                "kill_points": ["Can custom RAG mathematically guarantee zero cross-clinic memory leakage?"]
            }
        ],
        "pricing_details": {
            "arr_target": 340000,
            "arr_target_inr": "₹28,00,000",
            "list_price": 380000,
            "competitor_offer": 280000,
            "competitor_offer_inr": "₹23,00,000",
            "margin_saved": 40000,
            "margin_saved_inr": "₹3,30,000",
            "budget_cap": "₹28,00,000",
            "previous_discount_request": "12%",
            "billing_term": "Annual Commit",
            "budget_cycle": "Annual Clinical IT",
            "concessions_log": []
        },
        "milestones": [
            {
                "id": "m1",
                "name": "Clinical Validation Pitch",
                "status": "Completed",
                "date": "2026-09-18",
                "owner": "Dr. Raymond Scott",
                "summary": "Demonstrated physician persona memory."
            }
        ],
        "risks": [],
        "next_actions": [],
        "follow_ups": [],
        "winning_patterns": [],
        "strategy_playbook": {
            "primary_narrative": "Longitudinal Patient Memory for Zero Clinical Burnout",
            "executive_alignment": "Partner with Dr. Scott to overcome legal hesitation.",
            "closing_blueprint": "Execute BAA -> Initiate 30-day Epic integration."
        },
        "interactions": []
    }
]

# Historical Won & Lost Deals Database for Evidence-Based Pattern Matching
HISTORICAL_WON_DEALS = [
    {
        "id": "deal-hist-1024",
        "deal_number": "Deal #1024",
        "name": "FinTech Payment Gateway (Deal #1024)",
        "company": "FinTech Horizon Corp",
        "industry": "FinTech",
        "deal_size_inr": "₹30,00,000",
        "final_arr": 360000,
        "main_objection": "Pricing objection: Customer claimed competitor price was lower by 20%.",
        "resolution": "ROI comparison and 24-month TCO analysis proving engineering toil offset.",
        "outcome": "Won",
        "key_similarity": "Identical pricing objection and budget dynamics as ABC Technologies."
    },
    {
        "id": "deal-hist-1088",
        "deal_number": "Deal #1088",
        "name": "Enterprise SaaS Platform (Deal #1088)",
        "company": "CloudSprint Systems",
        "industry": "SaaS",
        "deal_size_inr": "₹22,00,000",
        "final_arr": 270000,
        "main_objection": "Implementation timeline concern: Customer required rapid go-live before quarter end.",
        "resolution": "Phased rollout roadmap guaranteeing core feature activation in 10 business days.",
        "outcome": "Won",
        "key_similarity": "Matches ABC Technologies requirement for December deployment deadline."
    },
    {
        "id": "deal-hist-nordic-84",
        "deal_number": "Deal #84",
        "name": "Nordic Cloud Systems (Deal #84)",
        "company": "Nordic Cloud Systems AB",
        "industry": "Enterprise Cloud & Infrastructure",
        "deal_size_inr": "₹58,00,000",
        "final_arr": 580000,
        "main_objection": "CFO price war: Datadog offered 30% discount to keep telemetry workload.",
        "resolution": "Refused base ARR discount. Offered 2-year commit at $580k with complimentary migration engineering credits.",
        "outcome": "Won",
        "key_similarity": "Proven margin defense playbook: traded migration services for multi-year contract."
    },
    {
        "id": "deal-hist-cybershield-62",
        "deal_number": "Deal #62",
        "name": "CyberShield Enterprise (Deal #62)",
        "company": "CyberShield Networks",
        "industry": "Cybersecurity",
        "deal_size_inr": "₹42,00,000",
        "final_arr": 420000,
        "main_objection": "CISO challenged cross-tenant memory leakage during concurrent agent executions.",
        "resolution": "Proactively provided SOC2 Annex A.14 bridge letter and isolated vector namespace diagrams.",
        "outcome": "Won",
        "key_similarity": "Accelerated security approval from 21 days down to 4 days."
    }
]

# Actionable Tasks for Sales Rep
SAMPLE_TASKS = [
    {
        "id": "task-1",
        "deal_id": "deal-abc-security",
        "customer": "ABC Technologies",
        "title": "Send 24-Month TCO Model & ROI Justification to CFO Anita Roy",
        "priority": "Critical",
        "badge_color": "rose",
        "due_date": "Tomorrow, 5:00 PM",
        "status": "Pending Approval",
        "assigned_to": "Sarah Jenkins",
        "source": "AI Recommendation from Live Call"
    },
    {
        "id": "task-2",
        "deal_id": "deal-abc-security",
        "customer": "ABC Technologies",
        "title": "Confirm December Deployment Sprint with CTO Rohan Sharma",
        "priority": "Important",
        "badge_color": "amber",
        "due_date": "Oct 2, 2026",
        "status": "In Progress",
        "assigned_to": "Sarah Jenkins",
        "source": "Requirement Detection (Live Call)"
    },
    {
        "id": "task-3",
        "deal_id": "deal-abc-security",
        "customer": "ABC Technologies",
        "title": "Deliver 24/7 Support SLA Documentation to Procurement",
        "priority": "Important",
        "badge_color": "amber",
        "due_date": "Oct 5, 2026",
        "status": "Approved",
        "assigned_to": "Sarah Jenkins",
        "source": "Meeting Commitment"
    },
    {
        "id": "task-4",
        "deal_id": "deal-nova-infra",
        "customer": "Nova Systems",
        "title": "Schedule Executive Pricing Sync with CFO David Sterling",
        "priority": "Critical",
        "badge_color": "rose",
        "due_date": "Oct 3, 2026",
        "status": "In Progress",
        "assigned_to": "Alex Rivera",
        "source": "Deal Risk Detection"
    }
]

# Connected Customer Emails
SAMPLE_EMAILS = [
    {
        "id": "email-1",
        "deal_id": "deal-abc-security",
        "customer": "ABC Technologies",
        "sender": "Rohan Sharma <rohan.s@abctechnologies.io>",
        "recipient": "Sarah Jenkins <sarah.j@nexusintel.ai>",
        "date": "September 25, 2026, 4:15 PM IST",
        "subject": "RE: Technical Architecture Review & Deployment Schedule",
        "snippet": "Sarah, we need confirmation that your team can guarantee deployment before December. Also, our CFO Anita is reviewing Competitor X's quote...",
        "extracted_intelligence": {
            "requirements": ["Deployment before December", "SOC2 Type II validation"],
            "competitors": ["Competitor X"],
            "buying_signals": ["Stated intention to deploy across entire engineering fleet if December deadline is met."],
            "risks": ["CFO Anita reviewing Competitor X discount proposal."]
        }
    },
    {
        "id": "email-2",
        "deal_id": "deal-nova-infra",
        "customer": "Nova Systems",
        "sender": "David Sterling <d.sterling@novasystems.com>",
        "recipient": "Alex Rivera <alex.r@nexusintel.ai>",
        "date": "September 24, 2026, 2:30 PM EDT",
        "subject": "Commercial Proposal & Datadog Renewal Notice",
        "snippet": "Alex, Datadog offered 32% off to retain our telemetry contract. Please review the 2-year commit structure...",
        "extracted_intelligence": {
            "objections": ["Pricing pressure (32% Datadog discount demand)"],
            "competitors": ["Datadog"],
            "concessions": ["Requesting multi-year pricing terms."]
        }
    }
]

# Curated Live Demo Streaming Conversation Sequence (Section 23 & 28)
LIVE_DEMO_SCRIPT = [
    {
        "step": 1,
        "speaker": "Sales Rep",
        "text": "Thanks for joining today, Rohan. Could you tell us about your current infrastructure and what your team is looking to achieve?",
        "detected_event": None,
        "memory_action": None
    },
    {
        "step": 2,
        "speaker": "Customer (Rohan Sharma, CTO)",
        "text": "We're looking for an enterprise security platform with persistent cognitive memory that doesn't suffer from context amnesia across agent sessions.",
        "detected_event": {
            "type": "requirement",
            "badge": "🟢 Buying Requirement Detected",
            "title": "Enterprise Security Platform",
            "detail": "Customer confirmed requirement for cognitive memory across agent fleet.",
            "priority": "High"
        },
        "memory_action": "Retained World fact: Enterprise security platform with persistent memory required."
    },
    {
        "step": 3,
        "speaker": "Customer (Rohan Sharma, CTO)",
        "text": "One non-negotiable requirement: we need the platform fully deployed before December for our Q4 security audit.",
        "detected_event": {
            "type": "deadline",
            "badge": "📌 Deadline Detected",
            "title": "Deployment Deadline: December",
            "detail": "Customer established hard deployment deadline before December for annual compliance audit.",
            "priority": "Critical"
        },
        "memory_action": "Retained Experience node: Hard deadline December 2026."
    },
    {
        "step": 4,
        "speaker": "Customer (Rohan Sharma, CTO)",
        "text": "Also, I have to be candid: Competitor X offered us a significantly lower price with a 15% renewal discount. Your price is higher than Competitor X.",
        "detected_event": {
            "type": "objection",
            "badge": "🔴 Pricing Objection Detected",
            "title": "Pricing Resistance & Competitor X Anchor",
            "detail": "Customer stated: 'Your price is higher than Competitor X.'",
            "priority": "Critical",
            "deal_memory": {
                "budget": "₹25,00,000 ($300k)",
                "competitor": "Competitor X",
                "previous_discount_request": "15%",
                "decision_maker": "CTO Rohan Sharma / CFO Anita Roy"
            },
            "historical_pattern": "ROI comparison worked in 4 similar deals (e.g. Deal #1024 FinTech ₹30L Won).",
            "suggested_approach": "Focus on total cost of ownership and measurable ROI. Ask whether concern is initial sticker price or overall implementation toil.",
            "next_best_action": "Ask whether the concern is initial price or overall implementation cost."
        },
        "memory_action": "Retained Observation: Customer comparing against Competitor X 15% discount."
    },
    {
        "step": 5,
        "speaker": "Sales Rep",
        "text": "I completely understand the budget comparison, Rohan. If this were just another static rule-engine, Competitor X's discount would make sense. But Competitor X requires 3 full-time engineers to maintain scripts, whereas Nexus provides autonomous self-healing memory that cuts MTTR by 74%. Would you say the main concern is initial license price, or total implementation cost over 24 months?",
        "detected_event": {
            "type": "tactic",
            "badge": "🎯 Tactical Reframe Delivered",
            "title": "TCO & Engineering Toil Defense",
            "detail": "Rep executed suggested ROI framework disarming Competitor X discount.",
            "priority": "Positive signal"
        },
        "memory_action": "Retained Experience: Rep executed TCO reframe against Competitor X."
    },
    {
        "step": 6,
        "speaker": "Customer (Rohan Sharma, CTO)",
        "text": "That's a very fair point—engineering maintenance toil is our biggest hidden cost right now. If you can provide 24/7 dedicated support and guarantee deployment before December, we can justify the ₹25L investment.",
        "detected_event": {
            "type": "requirement",
            "badge": "📌 Requirement Detected",
            "title": "24/7 Dedicated Support & December Go-Live",
            "detail": "Customer accepted TCO logic; tied ₹25L agreement to 24/7 support & December milestone.",
            "priority": "Positive signal"
        },
        "memory_action": "Retained World fact: 24/7 Support required to lock in ₹25L ARR."
    },
    {
        "step": 7,
        "speaker": "Sales Rep",
        "text": "Done. We will formalize the 24/7 support tier in Section 4 of the proposal and reserve your deployment engineering sprint starting November 1. I'll send the updated proposal to you and CFO Anita today.",
        "detected_event": {
            "type": "commitment",
            "badge": "🤝 Commitment Locked",
            "title": "Proposal Delivery & November Sprint",
            "detail": "Meeting concluded with agreed next steps and mutual commitments.",
            "priority": "Complete"
        },
        "memory_action": "Retained Experience: Deal advanced toward final agreement."
    }
]

# Persistent Biomimetic Hindsight Memory Nodes
INITIAL_HINDSIGHT_MEMORIES = [
    {
        "tier": "World",
        "bank_id": "nexus-deal-abc-security",
        "text": "ABC Technologies has 3,500 employees, is evaluating an enterprise security platform with a ₹25,00,000 budget cap, and has a hard deployment deadline before December 2026. Decision makers: Rohan Sharma (CTO) and Anita Roy (CFO).",
        "type": "fact",
        "tags": ["account_profile", "budget_cap", "december_deadline", "world"],
        "metadata": {"deal_id": "deal-abc-security", "tier": "World"}
    },
    {
        "tier": "Experience",
        "bank_id": "nexus-deal-abc-security",
        "text": "In Live Call Review (Sep 28), CTO Rohan Sharma stated: 'Competitor X offered us a lower price. Your price is higher than Competitor X.' Rep successfully reframed using 24-month TCO and engineering maintenance toil offset.",
        "type": "experience",
        "tags": ["pricing_objection", "competitor_x", "tco_defense", "experience"],
        "metadata": {"deal_id": "deal-abc-security", "tier": "Experience"}
    },
    {
        "tier": "Observation",
        "bank_id": "global-nexus-sales-intel",
        "text": "Across 14 enterprise deals, prospects frequently cite competitor discount offers (e.g. Competitor X 15%, Datadog 30%) as an anchoring bluff. Highlighting the cost of human engineering toil ($680k/yr or ₹36L/yr) preserves 100% of ARR in 87% of won deals.",
        "type": "observation",
        "tags": ["pricing_anchoring", "engineering_toil", "margin_preservation", "observation"],
        "metadata": {"deal_id": "global-nexus-sales-intel", "tier": "Observation"}
    },
    {
        "tier": "Opinion",
        "bank_id": "global-nexus-sales-intel",
        "text": "Mental Model: Never concede on base recurring software subscription price when a customer brings up a competitor discount. Concede on onboarding migration engineering credits or Net-60 terms instead to protect long-term gross margins.",
        "type": "opinion",
        "tags": ["margin_shield_playbook", "concession_rules", "opinion"],
        "metadata": {"deal_id": "global-nexus-sales-intel", "tier": "Opinion"}
    }
]

# Persistent Learning Insights Repository
PERSISTENT_LEARNING_LOG = [
    {
        "id": "learn-01",
        "tier": "Opinion / Mental Model",
        "category": "Pricing & Margin Defense",
        "insight": "Enterprise CFOs use competitor discount quotes (e.g. Competitor X 15%, Datadog 32%) as an anchoring bluff. In 87% of won deals, offering migration engineering credits rather than base ARR discounts preserves 100% of recurring margins.",
        "deals_synthesized": 14,
        "status": "Promoted to Global Playbook",
        "confidence": 0.96
    },
    {
        "id": "learn-02",
        "tier": "Observation",
        "category": "Deployment Deadline Velocity",
        "insight": "When an enterprise customer sets a hard deadline (e.g. December Q4 audit), providing a locked onboarding sprint schedule starting 3 weeks prior accelerates technical gate signoff by 14 days.",
        "deals_synthesized": 11,
        "status": "Promoted to Global Playbook",
        "confidence": 0.94
    },
    {
        "id": "learn-03",
        "tier": "Opinion / Mental Model",
        "category": "Competitor Displacement",
        "insight": "When prospects compare Nexus to Competitor X or Datadog, immediately reframe the competitor as 'the rear-view mirror for dead logs' and Nexus as 'the autonomous driver that learns and acts'. Avoid feature tickbox traps.",
        "deals_synthesized": 18,
        "status": "Promoted to Global Playbook",
        "confidence": 0.98
    }
]

# Guided Demo Script Steps for Quick Walkthrough
GUIDED_DEMO_STEPS = [
    {
        "step": 1,
        "title": "Select Deal: ABC Technologies",
        "deal_id": "deal-abc-security",
        "scenario": "Select ABC Technologies. Nexus generates a 30-second pre-meeting briefing.",
        "action": "pre_call_brief"
    },
    {
        "step": 2,
        "title": "Start Live Call & Real-Time Intelligence",
        "deal_id": "deal-abc-security",
        "scenario": "Stream customer conversation. Nexus detects requirements, deadlines, and Competitor X pricing objection in real time.",
        "action": "live_call_stream"
    },
    {
        "step": 3,
        "title": "Recall Deal Memory & Historical Patterns",
        "deal_id": "deal-abc-security",
        "scenario": "Nexus recalls past won deals (Deal #1024) and equips rep with the TCO counter-argument.",
        "action": "tactical_objection"
    },
    {
        "step": 4,
        "title": "Meeting Summary & Persistent Learning Update",
        "deal_id": "deal-abc-security",
        "scenario": "Automatically generates meeting summary, creates follow-up tasks, and commits insights to persistent memory.",
        "action": "meeting_summary"
    }
]

LEARNING_CURVE_STAGES = [
    {
        "stage": 1,
        "label": "Call 1: Cold Discovery",
        "timeline": "Day 1",
        "competence": 32,
        "status": "Level 1: Generic AI",
        "badge_color": "rose",
        "summary": "Agent has zero prior history. Ingests foundational company profile and CTO requirements.",
        "memory_impact": "+2 World Facts Retained",
        "sample_dialogue_before": "“We offer an AI sales platform that helps enterprise teams manage deals.”",
        "sample_dialogue_after": "“Rohan, we understand your custom RAG is failing on temporal reasoning across session boundaries.”"
    },
    {
        "stage": 2,
        "label": "Call 2: Security & Deadline Review",
        "timeline": "Day 20",
        "competence": 68,
        "status": "Level 2: Context-Aware",
        "badge_color": "amber",
        "summary": "Agent recalls Call 1 architecture. Anticipates SOC2 compliance and December deadline commitments.",
        "memory_impact": "+3 Experience & Observation Nodes",
        "sample_dialogue_before": "“We take security very seriously and follow industry-standard practices.”",
        "sample_dialogue_after": "“Rohan, Hindsight enforces cryptographic per-bank namespace partitioning with isolated schemas.”"
    },
    {
        "stage": 3,
        "label": "Call 3: Competitor Price Showdown",
        "timeline": "Day 45",
        "competence": 89,
        "status": "Level 3: Tactical Defender",
        "badge_color": "cyan",
        "summary": "Customer drops Competitor X 15% discount objection. Agent recalls Deal #1024 TCO playbook, saving ₹7,50,000 in ARR margin.",
        "memory_impact": "+2 Tactical Cross-Deal Playbooks",
        "sample_dialogue_before": "“We can match Competitor X's lower price immediately to earn your business.”",
        "sample_dialogue_after": "“Rohan, Competitor X's sticker price hides ₹36L in annual engineering toil. Rather than cutting ARR, we include migration engineering credits.”"
    },
    {
        "stage": 4,
        "label": "Call 4: Executive Closing",
        "timeline": "Day 60",
        "competence": 98,
        "status": "Level 4: Master Strategist",
        "badge_color": "emerald",
        "summary": "Agent synthesizes company-wide market mental models using Hindsight reflect. Closes ₹25,00,000 ARR contract with 0% margin leakage.",
        "memory_impact": "Living Competitor Playbooks Generated",
        "sample_dialogue_before": "“Here is our standard master services agreement.”",
        "sample_dialogue_after": "“We have pre-aligned Rohan on architecture, confirmed December go-live, and structured Anita's quarterly billing.”"
    }
]

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
2. We require confirmation that customer memory is never piped to upstream foundational LLMs for model fine-tuning or distillation.
3. Please provide your latest SOC2 Type II bridge letter covering Annex A.14.

Elena Rostova
Chief Information Security Officer | Acme Cloud Services Inc."""
    },
    "enterprise_quote_sheet": {
        "title": "Enterprise Order Form: ABC Technologies (₹25,00,000 ARR)",
        "client": "ABC Technologies",
        "term": "Annual Commit (Quarterly Invoicing)",
        "items": [
            {"sku": "NX-AGENT-CORE-ENT", "desc": "Nexus Autonomous Deal Intelligence Copilot (Unlimited Seats)", "qty": 1, "unit": "₹15,00,000", "total": "₹15,00,000"},
            {"sku": "HS-BANK-DEDICATED", "desc": "Vectorize Hindsight Dedicated Persistent Memory Cluster (SOC2 Isolated)", "qty": 1, "unit": "₹6,50,000", "total": "₹6,50,000"},
            {"sku": "NX-SUPPORT-247", "desc": "24/7 Dedicated Enterprise Support & 15-Minute Critical SLA", "qty": 1, "unit": "₹3,50,000", "total": "₹3,50,000"},
            {"sku": "NX-ENG-MIGRATE", "desc": "White-Glove Onboarding & November Sprint Deployment", "qty": 1, "unit": "₹3,50,000", "total": "₹0 (Concession Credit)"}
        ],
        "list_total": "₹28,50,000",
        "effective_arr": "₹25,00,000 ($300k)",
        "margin_preserved": "₹7,50,000 vs Competitor X Discount"
    },
    "competitor_teardown": {
        "title": "Competitive Teardown: Competitor X vs Nexus + Vectorize Hindsight",
        "comparison": [
            {
                "metric": "Core Philosophy",
                "datadog": "Competitor X: Static rule engines & generic chatbots without memory",
                "nexus": "Nexus: Active persistent cognitive memory (Recalls incidents, self-heals, learns)"
            },
            {
                "metric": "Memory Persistence",
                "datadog": "Competitor X: None. Amnesiac chat window resets every session.",
                "nexus": "Nexus: Biomimetic 4-tier hierarchy (World, Experience, Observation, Opinion)."
            },
            {
                "metric": "TCO & Engineering Toil",
                "datadog": "Competitor X: Requires 3 full-time engineers (₹36L/yr) to maintain custom scripts.",
                "nexus": "Nexus: Autonomous reflection cuts triage toil by 74%."
            },
            {
                "metric": "Discount Behavior",
                "datadog": "Competitor X: Offers 15-20% desperation discounts to win logos.",
                "nexus": "Nexus: Never discounts base ARR; trades value-add migration credits."
            }
        ]
    }
}
