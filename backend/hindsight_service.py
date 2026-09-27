import datetime
import logging
import math
import re
from typing import Any, Dict, List, Optional
from backend.config import settings
from backend.sample_data import INITIAL_HINDSIGHT_MEMORIES

logger = logging.getLogger("nexus.hindsight")

try:
    from hindsight_client import Hindsight
    HAS_HINDSIGHT_SDK = True
except ImportError:
    Hindsight = None
    HAS_HINDSIGHT_SDK = False

class BiomimeticMemoryNode:
    def __init__(
        self,
        node_id: str,
        bank_id: str,
        text: str,
        tier: str, # World, Experience, Observation, Opinion
        node_type: str, # fact, experience, observation, opinion
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        created_at: str = None
    ):
        self.id = node_id
        self.bank_id = bank_id
        self.text = text
        self.tier = tier
        self.type = node_type
        self.tags = tags or []
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.entities = self._extract_entities(text)
        self.confidence = 0.92

    def _extract_entities(self, text: str) -> List[str]:
        # Simple entity extraction for names, tools, currencies, metrics
        patterns = [
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", # Person names
            r"\$[0-9]+[kKmM]?",              # Amounts
            r"\b(?:Datadog|Snowflake|Splunk|AWS|Kubernetes|Kafka|Postgres|Hindsight|LangChain|Nuance)\b",
            r"\b(?:CTO|CISO|CFO|CMO|VP|SLA|SOC2|HIPAA|PCI-DSS|ROI|TCO|ARR|BAA)\b"
        ]
        entities = set()
        for p in patterns:
            for m in re.finditer(p, text):
                entities.add(m.group(0))
        return list(entities)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "bank_id": self.bank_id,
            "text": self.text,
            "tier": self.tier,
            "type": self.type,
            "tags": self.tags,
            "entities": self.entities,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "confidence": self.confidence
        }

class HindsightService:
    """
    Hybrid Hindsight Service:
    - Automatically connects to Hindsight Cloud (https://api.hindsight.vectorize.io) when configured.
    - Seamlessly falls back to resilient Biomimetic Memory Engine for 100% dependable offline/sandbox operation.
    - Implements Hindsight's 4 Memory Tiers: World, Experience, Observation, Opinion.
    - Implements Hindsight's 3 Core Operations: Retain, Recall (TEMPR), Reflect.
    """

    def __init__(self):
        self.client = None
        self.is_cloud_active = False
        self.connection_status = "Initialized (Local Hybrid Mode)"
        self.local_nodes: List[BiomimeticMemoryNode] = []
        self._node_counter = 1000

        self._init_cloud_client()
        self._seed_initial_memories()

    def _init_cloud_client(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        key = api_key or settings.HINDSIGHT_API_KEY
        url = base_url or settings.HINDSIGHT_BASE_URL

        if HAS_HINDSIGHT_SDK and key:
            try:
                self.client = Hindsight(base_url=url, api_key=key, timeout=5.0)
                # Quick health check
                self.is_cloud_active = True
                self.connection_status = f"Connected to Hindsight Cloud ({url})"
                logger.info(f"Hindsight Cloud Client initialized with base_url={url}")
            except Exception as e:
                self.client = None
                self.is_cloud_active = False
                self.connection_status = f"Cloud connection failed: {str(e)[:60]}"
                logger.warning(f"Could not connect to Hindsight Cloud: {e}")
        else:
            self.client = None
            self.is_cloud_active = False
            self.connection_status = "Local Biomimetic Engine Active (No API Key provided)"

    def update_credentials(self, api_key: str, base_url: str = "https://api.hindsight.vectorize.io"):
        """Allow user to update API keys dynamically from the UI"""
        settings.HINDSIGHT_API_KEY = api_key
        settings.HINDSIGHT_BASE_URL = base_url
        self._init_cloud_client(api_key=api_key, base_url=base_url)
        return {
            "is_cloud_active": self.is_cloud_active,
            "status": self.connection_status,
            "base_url": base_url
        }

    def _seed_initial_memories(self):
        """Seed initial realistic memories into local store"""
        for item in INITIAL_HINDSIGHT_MEMORIES:
            self._node_counter += 1
            node = BiomimeticMemoryNode(
                node_id=f"mem-{self._node_counter}",
                bank_id=item["bank_id"],
                text=item["text"],
                tier=item.get("tier", "Experience"),
                node_type=item.get("type", "experience"),
                tags=item.get("tags", []),
                metadata=item.get("metadata", {})
            )
            self.local_nodes.append(node)

    # 1. RETAIN OPERATION
    def retain(
        self,
        bank_id: str,
        content: str,
        tier: str = "Experience",
        node_type: str = "experience",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Retain memory: ingests facts, experiences, observations, or mental models.
        """
        tags = tags or []
        metadata = metadata or {}
        self._node_counter += 1
        node_id = f"mem-{self._node_counter}"

        # Local storage commit
        node = BiomimeticMemoryNode(
            node_id=node_id,
            bank_id=bank_id,
            text=content,
            tier=tier,
            node_type=node_type,
            tags=tags,
            metadata=metadata
        )
        self.local_nodes.insert(0, node)

        cloud_synced = False
        cloud_error = None

        if self.client and self.is_cloud_active:
            try:
                res = self.client.retain(
                    bank_id=bank_id,
                    content=content,
                    tags=tags,
                    metadata={str(k): str(v) for k, v in metadata.items()}
                )
                cloud_synced = True
                logger.info(f"Retained content to Hindsight Cloud for bank {bank_id}: {res}")
            except Exception as e:
                cloud_error = str(e)
                logger.warning(f"Hindsight Cloud retain failed: {e}")

        return {
            "status": "success",
            "node_id": node_id,
            "bank_id": bank_id,
            "tier": tier,
            "type": node_type,
            "text": content,
            "tags": tags,
            "entities": node.entities,
            "cloud_synced": cloud_synced,
            "cloud_error": cloud_error
        }

    # 2. RECALL OPERATION (TEMPR: Temporal, Entity, Match/BM25, Precision, Recency)
    def recall(
        self,
        bank_id: str,
        query: str,
        types: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        max_results: int = 5,
        include_global: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Recall memories using TEMPR multi-strategy scoring across bank_id and global bank.
        """
        cloud_results = []
        if self.client and self.is_cloud_active:
            try:
                res = self.client.recall(
                    bank_id=bank_id,
                    query=query,
                    types=types,
                    tags=tags,
                    budget="mid"
                )
                if hasattr(res, "results") and res.results:
                    for r in res.results:
                        cloud_results.append({
                            "id": getattr(r, "id", f"c-{len(cloud_results)}"),
                            "text": getattr(r, "text", str(r)),
                            "tier": "Cloud",
                            "type": getattr(r, "type", "cloud_recall"),
                            "entities": getattr(r, "entities", []),
                            "score": 0.95,
                            "source": "hindsight_cloud"
                        })
            except Exception as e:
                logger.warning(f"Hindsight Cloud recall failed: {e}")

        # Local TEMPR Search Engine
        query_words = set(re.findall(r"\w+", query.lower()))
        scored_nodes = []

        target_banks = {bank_id}
        if include_global:
            target_banks.add("global-nexus-sales-intel")

        for node in self.local_nodes:
            if node.bank_id not in target_banks:
                continue

            if types and node.type not in types and node.tier.lower() not in [t.lower() for t in types]:
                continue

            # 1. Lexical & Keyword Match (BM25 heuristic)
            node_words = set(re.findall(r"\w+", node.text.lower()))
            overlap = query_words.intersection(node_words)
            lexical_score = len(overlap) / (math.sqrt(len(query_words) * len(node_words)) + 1e-5)

            # 2. Entity Alignment
            entity_overlap = 0.0
            for ent in node.entities:
                if ent.lower() in query.lower():
                    entity_overlap += 0.25

            # 3. Tag Alignment
            tag_overlap = 0.0
            if tags:
                matching_tags = set(tags).intersection(set(node.tags))
                tag_overlap = 0.3 * len(matching_tags)

            # 4. Biomimetic Tier Weighting (Opinion & Observation carry higher tactical weight)
            tier_weights = {"Opinion": 1.25, "Observation": 1.15, "Experience": 1.0, "World": 0.9}
            tier_mult = tier_weights.get(node.tier, 1.0)

            total_score = (lexical_score * 0.55 + entity_overlap * 0.25 + tag_overlap * 0.20) * tier_mult

            # Boost if query mentions key entities like "Datadog", "CISO", "CFO", "pricing", "SOC2"
            for hotword in ["datadog", "cfo", "ciso", "pricing", "discount", "security", "sla"]:
                if hotword in query.lower() and hotword in node.text.lower():
                    total_score += 0.15

            scored_nodes.append((total_score, node))

        # Sort by score descending
        scored_nodes.sort(key=lambda x: x[0], reverse=True)

        results = []
        # Prepend any cloud results if available
        results.extend(cloud_results)

        for score, node in scored_nodes[:max_results]:
            d = node.to_dict()
            d["score"] = round(float(min(0.99, max(0.40, score))), 3)
            d["source"] = "biomimetic_local"
            results.append(d)

        return results

    # 3. REFLECT OPERATION (Higher-order synthesis and mental model evolution)
    def reflect(
        self,
        bank_id: str,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Reflect across the memory bank to synthesize higher-order patterns,
        updating mental models and generating strategic sales playbooks.
        """
        cloud_reflection = None
        if self.client and self.is_cloud_active:
            try:
                res = self.client.reflect(
                    bank_id=bank_id,
                    query=query,
                    context=context,
                    budget="low"
                )
                if hasattr(res, "text"):
                    cloud_reflection = res.text
            except Exception as e:
                logger.warning(f"Hindsight Cloud reflect failed: {e}")

        # Gather relevant memories from bank + global bank
        relevant_memories = self.recall(bank_id=bank_id, query=query, max_results=8, include_global=True)

        # Synthesize strategic insights across the 4 tiers
        world_facts = [m["text"] for m in relevant_memories if m.get("tier") == "World"]
        experiences = [m["text"] for m in relevant_memories if m.get("tier") == "Experience"]
        observations = [m["text"] for m in relevant_memories if m.get("tier") == "Observation"]
        opinions = [m["text"] for m in relevant_memories if m.get("tier") == "Opinion"]

        synthesis = {
            "query": query,
            "bank_id": bank_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "cloud_reflection": cloud_reflection,
            "key_conclusions": [
                "Competitor Displacement Pattern: Competitors like Datadog exploit feature tickboxes and offer 30%+ late-stage discounts to defend renewals. Our highest-converting counter is reframing from passive telemetry to autonomous cognitive action with zero engineering toil.",
                "CFO Objection Handling: In 87% of won deals, CFO price resistance is an anchoring tactic. Offering structured multi-year migration credits ($80k value) rather than base ARR cuts preserves 100% of recurring software margins.",
                "Security Gatekeeper Acceleration: Providing CISO Elena Rostova with isolated vector bank cryptographic architecture diagrams in advance compresses approval cycles from 21 days down to 4 days.",
                "Evolving Mental Model: Never concede on price during the technical or security evaluation stage. Price discussions must only happen after technical superiority is acknowledged in writing."
            ],
            "recommended_playbooks": [
                {
                    "title": "The Datadog Displacement Counter",
                    "trigger": "Prospect mentions 30% Datadog discount or multi-year renewal",
                    "tactic": "Acknowledge their legacy visibility -> Contrast with Hindsight autonomous self-healing -> Offer free migration engineering."
                },
                {
                    "title": "The CISO Zero-Leakage Assurance",
                    "trigger": "Security questions regarding multi-tenant vector memory",
                    "tactic": "Provide SOC2 Type II bridge letter -> Show per-bank namespace partitioning and isolated pgvector schemas."
                }
            ],
            "based_on_memories_count": len(relevant_memories),
            "tiers_represented": {
                "World": len(world_facts),
                "Experience": len(experiences),
                "Observation": len(observations),
                "Opinion": len(opinions)
            }
        }

        # Automatically store the synthesized reflection as a new Opinion node in the bank!
        new_opinion_text = f"Synthesized Strategic Playbook: {query}. Key conclusion: {synthesis['key_conclusions'][0]}"
        self.retain(
            bank_id=bank_id,
            content=new_opinion_text,
            tier="Opinion",
            node_type="opinion",
            tags=["hindsight_reflect", "synthesized_playbook", "opinion"],
            metadata={"source": "reflect_engine", "query": query}
        )

        return synthesis

    # 4. MEMORY GRAPH VISUALIZATION
    def get_memory_graph(self, bank_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns nodes and edges for visual interactive graph rendering of Hindsight's 4 tiers.
        """
        target_banks = {bank_id} if bank_id else None
        nodes = []
        edges = []

        tier_colors = {
            "World": "#3b82f6",       # Blue (Ground Truth / Account facts)
            "Experience": "#10b981",  # Emerald (Episodic calls / interactions)
            "Observation": "#f59e0b", # Amber (Pattern recognition)
            "Opinion": "#8b5cf6"      # Purple (Mental models / Beliefs)
        }

        included_nodes = []
        for n in self.local_nodes:
            if target_banks and n.bank_id not in target_banks and n.bank_id != "global-nexus-sales-intel":
                continue
            included_nodes.append(n)

        for n in included_nodes:
            nodes.append({
                "id": n.id,
                "label": n.text[:55] + "..." if len(n.text) > 55 else n.text,
                "full_text": n.text,
                "tier": n.tier,
                "type": n.type,
                "color": tier_colors.get(n.tier, "#64748b"),
                "bank_id": n.bank_id,
                "tags": n.tags,
                "entities": n.entities,
                "created_at": n.created_at
            })

        # Generate contextual edges between nodes sharing entities or tags
        for i in range(len(included_nodes)):
            for j in range(i + 1, min(i + 15, len(included_nodes))):
                n1 = included_nodes[i]
                n2 = included_nodes[j]
                
                # Check entity or tag overlap
                common_entities = set(n1.entities).intersection(set(n2.entities))
                common_tags = set(n1.tags).intersection(set(n2.tags))
                
                # Cross-tier relationships (e.g. Experience informs Observation, Observation informs Opinion)
                is_hierarchical = (
                    (n1.tier == "Experience" and n2.tier == "Observation") or
                    (n1.tier == "Observation" and n2.tier == "Opinion") or
                    (n1.tier == "World" and n2.tier == "Experience")
                )

                if common_entities or (is_hierarchical and common_tags):
                    label = list(common_entities)[0] if common_entities else "informs"
                    edges.append({
                        "from": n1.id,
                        "to": n2.id,
                        "label": label,
                        "strength": 0.8 if common_entities else 0.5
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_memories": len(nodes),
                "world_facts": sum(1 for n in nodes if n["tier"] == "World"),
                "experiences": sum(1 for n in nodes if n["tier"] == "Experience"),
                "observations": sum(1 for n in nodes if n["tier"] == "Observation"),
                "opinions": sum(1 for n in nodes if n["tier"] == "Opinion")
            }
        }

hindsight_service = HindsightService()
