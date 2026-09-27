# Reddit Distribution Templates

As specified in Step 5 of the content guide, submit your article link to these developer communities. **Do NOT mention hackathons in Reddit posts.**

---

## 1. r/llmdevs
**Title:** Why cosine similarity failed our multi-month sales agent (and how we fixed it with Hindsight)  
**Post Type:** Link Post (or Text Post with Link)  
**Body Copy:**
```text
We spent months building an agent to assist with 6-month enterprise sales cycles, but naive RAG was a disaster. It kept recommending huge discounts because it forgot commitments made in earlier discovery calls.

We replaced flat vector embeddings with Hindsight's 4-tier biomimetic memory system (World, Experience, Observation, Opinion). 

Wrote up the full technical breakdown, including how TEMPR multi-strategy search works and code snippets from our FastAPI backend:
[INSERT_YOUR_ARTICLE_URL_HERE]

Curious how others are handling temporal decay and stakeholder contradictions in long-running agent workflows.
```

---

## 2. r/aiagents
**Title:** How we solved agent context amnesia across long deal cycles using Hindsight  
**Post Type:** Link Post  
**URL:** `[INSERT_YOUR_ARTICLE_URL_HERE]`  
**First Comment:**
```text
Key takeaway: Context window stuffing isn't memory. An agent needs structured reflection to synthesize episodic interactions into actionable heuristics. 

Code & Hindsight docs:
https://github.com/vectorize-io/hindsight
```

---

## 3. r/aimemory
**Title:** Moving beyond flat embeddings: Implementing a 4-tier cognitive memory architecture with Hindsight  
**Post Type:** Text / Link Post  
**Body Copy:**
```text
Most AI memory systems treat every text snippet equally. But in complex enterprise workflows, a firmographic fact (World) is fundamentally different from a meeting note (Experience), an account pattern (Observation), or a team playbook (Opinion).

Here is our writeup on implementing Hindsight's biomimetic memory model with TEMPR search for an autonomous deal copilot:
[INSERT_YOUR_ARTICLE_URL_HERE]
```

---

## 4. r/sideproject
**Title:** I built an autonomous B2B deal copilot that remembers stakeholder objections over 6-month sales cycles  
**Post Type:** Link / Media Post  
**Body Copy:**
```text
Sales reps spend hours re-reading CRM notes before executive calls. I built Nexus to autonomously retain, recall, and reflect on deal history using Hindsight agent memory.

Demo & architecture article: [INSERT_YOUR_ARTICLE_URL_HERE]
Open source Hindsight repo: https://github.com/vectorize-io/hindsight
```
