# Nexus System Architecture & Memory Flow

### Autonomous B2B Deal Intelligence Copilot with Persistent Biomimetic Memory
**Powered by Vectorize Hindsight**

---

## 🖼️ High-Resolution Architecture Diagram

![Nexus System Architecture](architecture_diagram.jpg)

---

## 📐 Interactive Mermaid Architecture Flow

```mermaid
flowchart LR
    subgraph INGESTION["1. Data Ingestion Layer"]
        CRM["📊 CRM Records<br/>(Salesforce, HubSpot)"]
        TRANSCRIPTS["🎙️ Meeting Transcripts<br/>(Zoom, Gong, Teams)"]
        EMAILS["✉️ Communication Logs<br/>(Pricing & Threads)"]
    end

    subgraph HINDSIGHT["2. Vectorize Hindsight Engine"]
        direction TB
        T4["🧠 Tier 4: OPINION<br/>• Negotiation Playbooks<br/>• Margin Guardrails<br/>• Compliance Veto Rules"]
        T3["🔭 Tier 3: OBSERVATION<br/>• Competitor Dynamics<br/>• Objection Patterns<br/>• Bluffs & Traps"]
        T2["📜 Tier 2: EXPERIENCE<br/>• Episodic Transcripts<br/>• Win/Loss Analyses<br/>• Chronological Logs"]
        T1["🌍 Tier 1: WORLD<br/>• Account Firmographics<br/>• Target ARR ($480k)<br/>• Single-Tenant VPC Specs"]

        T1 -->|Chronological Ingestion| T2
        T2 -->|Cross-Deal Consolidation| T3
        T3 -->|hindsight.reflect\(\)| T4
    end

    subgraph AGENT["3. Nexus Deal Cockpit / Agent Nucleus"]
        API["⚡ FastAPI Gateway<br/>(Async REST & Sockets)"]
        LLM["⚡ Groq LLM Engine<br/>(Llama 3.3 70B Versatile)"]
        DEFENSE["🛡️ Objection Defense<br/>(Anti-Amnesia Generator)"]
        MARGIN["💰 Margin Protection<br/>(Contract & Pricing Guard)"]
        API --> LLM
        LLM --> DEFENSE
        DEFENSE --> MARGIN
    end

    subgraph CLIENT["4. Executive Cockpit UI"]
        HUD["🖥️ Real-Time Deal Cockpit"]
        GUIDED["🎯 4-Stage Guided Demo Flow"]
        EXPLORER["🔍 Biomimetic Memory Explorer"]
        CURVE["📈 Cognitive Learning Curve"]
    end

    INGESTION -->|hindsight.retain\(\)<br/>Entity Extraction & Tiering| HINDSIGHT
    HINDSIGHT -->|hindsight.recall\(\)<br/>TEMPR Multi-Strategy Search| AGENT
    AGENT -->|Live Actionable Battlecards| CLIENT
    CLIENT -.->|User Feedback & Meeting Notes| INGESTION
```

---

## 🔬 Component Breakdown

### 1. Data Ingestion Layer
- **Input Sources:** Ingests raw stakeholder interactions from CRM updates, meeting audio transcripts (Gong, Zoom), and email threads.
- **Entity Extraction:** Automatically identifies and tags key business entities:
  - **Stakeholder Roles:** CISO (Elena Vance), CTO (Marcus Reynolds), CFO (David Sterling).
  - **Competitors:** Datadog, Snowflake, Splunk.
  - **Constraints:** HIPAA, SOC-2 Type II, Single-Tenant VPC, sub-second latency SLA.
- **Tier Routing:** Determines whether the input is ground truth (`World`), episodic interaction (`Experience`), emergent pattern (`Observation`), or team strategy (`Opinion`).

---

### 2. Vectorize Hindsight Persistent Memory Engine

Unlike flat vector databases that compute cosine distance across undifferentiated text blobs, Hindsight organizes enterprise memory into a biomimetic cognitive hierarchy:

| Memory Tier | Cognitive Function | Example in Nexus Deal Engine |
|:---|:---|:---|
| **Tier 1: World** | Permanent Ground Truths | Acme Corp, $480k ARR target, healthcare enterprise with strict SOC-2 compliance. |
| **Tier 2: Experience** | Chronological Episodic Logs | *"Call 2 on April 8: CISO Elena Vance stated that Datadog's multi-tenant cluster fails internal security standards."* |
| **Tier 3: Observation** | Cross-Interaction Patterns | *"Acme Corp CFO brings up competitor discounts late in Q3 as a negotiation bluff."* |
| **Tier 4: Opinion** | Strategic Mental Models | *"Never discount against Datadog on this account. Counter-anchor on single-tenant VPC compliance guarantees."* |

#### Memory Operations:
1. **`hindsight.retain()`**: Commits facts and interactions with entity tags and timestamps.
2. **`hindsight.recall()` (TEMPR Search)**: Multi-strategy retrieval combining:
   - **T** - *Temporal Distance:* Filters for active deal phases.
   - **E** - *Entity Overlap:* Pinpoints exact stakeholders (CISO vs CFO) and competitor mentions.
   - **M** - *Multi-hop Traversal:* Connects high-level objections back to technical discovery logs.
   - **P** - *Preference:* Customizes response format to executive persona.
   - **R** - *Recency:* Prioritizes fresh updates over stale concessions.
3. **`hindsight.reflect()`**: Asynchronous background process that synthesizes accumulated `Experience` nodes into high-order `Opinion` playbooks.

---

### 3. Nexus AI Agent Nucleus

- **FastAPI Backend Gateway:** Async architecture handling high-concurrency requests with sub-5ms routing overhead.
- **Groq Llama 3.3 70B Versatile:** Sub-300ms token generation for real-time live call copilot guidance.
- **Dynamic Objection Defense:** Compares incoming sales objections against recalled Hindsight memories, flagging contradiction traps before the sales rep speaks.
- **Margin Protection Engine:** Enforces pricing floors and contract guardrails based on synthesized `Opinion` playbooks.

---

### 4. Executive Cockpit UI

- **Modern Glassmorphic Dark-Mode HUD:** Built with modern CSS design tokens, Outfit typography, and dynamic animations.
- **Interactive Guided Demo:** 4-stage walkthrough demonstrating the live behavioral difference between memory-powered agents and amnesiac models.
- **Biomimetic Memory Explorer:** Visual inspection tool allowing users and evaluators to browse, filter, and inspect memory nodes across all 4 tiers in real time.
- **Cognitive Learning Curve:** Live visual telemetry tracking win rate improvement (12% $\rightarrow$ 91%) and margin preservation as memory density increases.
