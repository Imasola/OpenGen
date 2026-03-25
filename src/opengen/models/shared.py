"""
OpenGen  - Shared Data Models
=============================

These models define the data format shared between the Master Agent
and the Worker network. They are the contract that ensures both sides
understand each other.

If you are building a tool that interacts with OpenGen (a worker,
an API client, or a third-party application), these are the models
you need.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# === Enums ===


class Domain(str, Enum):
    """Scientific domains covered by OpenGen."""
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    PHYSICS = "physics"
    SPACE = "space"
    COMPUTER_SCIENCE = "computer_science"
    ENGINEERING = "engineering"
    MEDICINE = "medicine"
    ENERGY = "energy"
    MATHEMATICS = "mathematics"
    ENVIRONMENTAL = "environmental"
    ROBOTICS = "robotics"
    AGRICULTURE = "agriculture"
    PSYCHOLOGY = "psychology"
    GENERAL = "general"


class NodeStatus(str, Enum):
    """Verification status of a knowledge node."""
    VERIFIED = "verified"
    PENDING = "pending"
    DISPUTED = "disputed"
    NEEDS_REVIEW = "needs_review"
    OUTDATED = "outdated"
    IN_PROGRESS = "in_progress"


class Stability(str, Enum):
    """How often a knowledge node needs re-verification."""
    PERMANENT = "permanent"       # Never (e.g., 1+1=2)
    STABLE = "stable"             # Every 24 months
    STANDARD = "standard"         # Every 12 months
    FAST_MOVING = "fast_moving"   # Every 6 months


class RelationType(str, Enum):
    """How two knowledge nodes are connected."""
    USES = "uses"
    PRODUCES = "produces"
    BASED_ON = "based_on"
    CONTRADICTS = "contradicts"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    SUPERSEDES = "supersedes"
    ENABLES = "enables"


class TaskStatus(str, Enum):
    """Status of a worker task."""
    QUEUED = "queued"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


# === Core Models ===


class KnowledgeNode(BaseModel):
    """
    A node in the knowledge graph.

    Every verified research result becomes a node with connections
    to related knowledge. This model is returned by the public API.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    domain: Domain = Domain.GENERAL
    content: str = ""
    summary: str = ""
    quality_score: float = 0.0
    sources: list[str] = []
    tags: list[str] = []
    status: NodeStatus = NodeStatus.IN_PROGRESS
    stability: Stability = Stability.STANDARD
    version: int = 1
    language: str = "en"
    review_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class KnowledgeEdge(BaseModel):
    """
    A connection between two knowledge nodes.

    Edges are typed, weighted, and directional  - they describe
    how pieces of knowledge relate to each other.
    """
    source_id: str
    target_id: str
    relation: RelationType
    weight: float = 1.0
    confidence: float = 1.0
    created_by: str = "system"
    created_at: datetime = Field(default_factory=datetime.now)


class WorkerTask(BaseModel):
    """
    A task assigned to a worker by the Master Agent.

    The worker receives this, executes the task using its own
    LLM API key, and returns a WorkerResult.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    question: str
    domain: Domain = Domain.GENERAL
    context: str = ""
    instructions: str = ""
    max_tokens: int = 4096
    model_preference: str = ""
    status: TaskStatus = TaskStatus.QUEUED
    created_at: datetime = Field(default_factory=datetime.now)
    timeout_seconds: int = 300


class WorkerResult(BaseModel):
    """
    A result submitted by a worker back to the Master Agent.

    The Master Agent validates this, runs it through the
    Multi-Critic ensemble, and routes it to community verification.
    """
    task_id: str
    worker_id: str
    content: str
    model_used: str = ""
    tokens_used: int = 0
    duration_seconds: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)


class WorkerRegistration(BaseModel):
    """
    Information a worker sends when registering with the Master Agent.
    """
    worker_name: str = ""
    cpu_cores: int = 0
    ram_gb: float = 0.0
    gpu_name: str = ""
    gpu_vram_gb: float = 0.0
    has_api_key: bool = False
    supported_providers: list[str] = []
    os: str = ""
    python_version: str = ""


class WorkerHeartbeat(BaseModel):
    """
    Periodic health signal from worker to Master Agent.
    """
    worker_id: str
    status: str = "active"
    tasks_completed: int = 0
    uptime_seconds: float = 0.0
    current_task_id: Optional[str] = None


# === API Response Models ===


class SearchResult(BaseModel):
    """A search result from the public knowledge API."""
    node: KnowledgeNode
    relevance_score: float = 0.0
    connections_count: int = 0


class GraphStats(BaseModel):
    """Public statistics about the knowledge graph."""
    total_nodes: int = 0
    total_edges: int = 0
    verified_nodes: int = 0
    pending_nodes: int = 0
    domains: dict[str, int] = {}
    average_quality_score: float = 0.0
    active_workers: int = 0
    reviews_today: int = 0


if __name__ == "__main__":
    # Demonstrate the data models
    print("=" * 60)
    print("  OpenGen  - Shared Data Models")
    print("=" * 60)

    node = KnowledgeNode(
        title="Photosynthesis  - light reactions",
        domain=Domain.BIOLOGY,
        content="The light reactions of photosynthesis occur in thylakoids.",
        quality_score=0.97,
        tags=["photosynthesis", "energy"],
        status=NodeStatus.VERIFIED,
        stability=Stability.STABLE,
    )
    print(f"\n  Example node: {node.title}")
    print(f"    Domain:    {node.domain.value}")
    print(f"    Score:     {node.quality_score}")
    print(f"    Status:    {node.status.value}")
    print(f"    Stability: {node.stability.value}")

    task = WorkerTask(
        question="How does chlorophyll absorb light?",
        domain=Domain.CHEMISTRY,
        instructions="Focus on the molecular mechanism.",
    )
    print(f"\n  Example task: {task.question}")
    print(f"    Domain:  {task.domain.value}")
    print(f"    Timeout: {task.timeout_seconds}s")

    reg = WorkerRegistration(
        cpu_cores=8,
        ram_gb=32.0,
        gpu_name="NVIDIA RTX 4090",
        gpu_vram_gb=24.0,
        has_api_key=True,
        supported_providers=["anthropic", "openai"],
    )
    print(f"\n  Example worker registration:")
    print(f"    CPU: {reg.cpu_cores} cores, {reg.ram_gb}GB RAM")
    print(f"    GPU: {reg.gpu_name} ({reg.gpu_vram_gb}GB)")
    print(f"    Providers: {', '.join(reg.supported_providers)}")

    print(f"\n  All {len(Domain)} domains:")
    for d in Domain:
        print(f"    - {d.value}")

    print(f"\n  All {len(RelationType)} relation types:")
    for r in RelationType:
        print(f"    - {r.value}")

    print(f"\n  Models loaded successfully.")
    print("=" * 60)
