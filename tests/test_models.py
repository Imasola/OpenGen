"""
OpenGen — Tests
===============

Tests for the shared data models. No API key required.
Run with: pytest tests/ -v
"""

from datetime import datetime

import pytest

from opengen.models.shared import (
    Domain,
    GraphStats,
    KnowledgeEdge,
    KnowledgeNode,
    NodeStatus,
    RelationType,
    SearchResult,
    Stability,
    TaskStatus,
    WorkerHeartbeat,
    WorkerRegistration,
    WorkerResult,
    WorkerTask,
)


class TestKnowledgeNode:
    """Tests for the KnowledgeNode model."""

    def test_create_minimal(self):
        node = KnowledgeNode(title="Test", content="Content")
        assert node.title == "Test"
        assert node.id is not None
        assert node.status == NodeStatus.IN_PROGRESS
        assert node.stability == Stability.STANDARD

    def test_create_full(self):
        node = KnowledgeNode(
            title="Photosynthesis",
            domain=Domain.BIOLOGY,
            content="Plants convert light to energy.",
            quality_score=0.97,
            tags=["photosynthesis", "energy"],
            status=NodeStatus.VERIFIED,
            stability=Stability.STABLE,
        )
        assert node.domain == Domain.BIOLOGY
        assert node.quality_score == 0.97
        assert node.status == NodeStatus.VERIFIED

    def test_unique_ids(self):
        a = KnowledgeNode(title="A", content="A")
        b = KnowledgeNode(title="B", content="B")
        assert a.id != b.id

    def test_has_timestamps(self):
        node = KnowledgeNode(title="T", content="C")
        assert isinstance(node.created_at, datetime)
        assert isinstance(node.updated_at, datetime)


class TestKnowledgeEdge:
    """Tests for the KnowledgeEdge model."""

    def test_create(self):
        edge = KnowledgeEdge(
            source_id="a", target_id="b", relation=RelationType.USES,
        )
        assert edge.weight == 1.0
        assert edge.relation == RelationType.USES

    def test_all_relation_types(self):
        expected = ["uses", "produces", "based_on", "contradicts",
                    "part_of", "related_to", "supersedes", "enables"]
        actual = [r.value for r in RelationType]
        for e in expected:
            assert e in actual, f"Missing: {e}"


class TestWorkerTask:
    """Tests for the WorkerTask model."""

    def test_create(self):
        task = WorkerTask(question="How does gravity work?")
        assert task.question == "How does gravity work?"
        assert task.status == TaskStatus.QUEUED
        assert task.timeout_seconds == 300
        assert task.id is not None

    def test_with_domain(self):
        task = WorkerTask(
            question="Test", domain=Domain.PHYSICS,
        )
        assert task.domain == Domain.PHYSICS


class TestWorkerResult:
    """Tests for the WorkerResult model."""

    def test_create(self):
        result = WorkerResult(
            task_id="task-1",
            worker_id="worker-1",
            content="Research findings...",
            model_used="claude-sonnet-4-20250514",
            tokens_used=1500,
        )
        assert result.task_id == "task-1"
        assert result.tokens_used == 1500


class TestWorkerRegistration:
    """Tests for the WorkerRegistration model."""

    def test_create(self):
        reg = WorkerRegistration(
            cpu_cores=8,
            ram_gb=32.0,
            gpu_name="RTX 4090",
            has_api_key=True,
            supported_providers=["anthropic"],
        )
        assert reg.cpu_cores == 8
        assert reg.has_api_key is True

    def test_defaults(self):
        reg = WorkerRegistration()
        assert reg.cpu_cores == 0
        assert reg.has_api_key is False


class TestWorkerHeartbeat:
    """Tests for the WorkerHeartbeat model."""

    def test_create(self):
        hb = WorkerHeartbeat(worker_id="w-1", tasks_completed=5)
        assert hb.worker_id == "w-1"
        assert hb.status == "active"


class TestDomains:
    """Tests for the Domain enum."""

    def test_core_domains_exist(self):
        required = [
            Domain.BIOLOGY, Domain.CHEMISTRY, Domain.PHYSICS,
            Domain.SPACE, Domain.MEDICINE, Domain.ENGINEERING,
            Domain.MATHEMATICS, Domain.GENERAL,
        ]
        for d in required:
            assert d is not None

    def test_all_values_lowercase(self):
        for d in Domain:
            assert d.value == d.value.lower()

    def test_domain_count(self):
        assert len(Domain) >= 10


class TestStability:
    """Tests for the Stability enum."""

    def test_all_tiers(self):
        assert Stability.PERMANENT.value == "permanent"
        assert Stability.STABLE.value == "stable"
        assert Stability.STANDARD.value == "standard"
        assert Stability.FAST_MOVING.value == "fast_moving"


class TestNodeStatus:
    """Tests for the NodeStatus enum."""

    def test_all_statuses(self):
        expected = ["verified", "pending", "disputed",
                    "needs_review", "outdated", "in_progress"]
        actual = [s.value for s in NodeStatus]
        for e in expected:
            assert e in actual


class TestGraphStats:
    """Tests for the GraphStats model."""

    def test_create(self):
        stats = GraphStats(
            total_nodes=100,
            verified_nodes=80,
            active_workers=5,
            domains={"biology": 30, "physics": 20},
        )
        assert stats.total_nodes == 100
        assert stats.domains["biology"] == 30

    def test_defaults(self):
        stats = GraphStats()
        assert stats.total_nodes == 0
        assert stats.active_workers == 0


class TestSearchResult:
    """Tests for the SearchResult model."""

    def test_create(self):
        node = KnowledgeNode(title="Test", content="Content")
        result = SearchResult(node=node, relevance_score=0.95)
        assert result.relevance_score == 0.95
        assert result.node.title == "Test"
