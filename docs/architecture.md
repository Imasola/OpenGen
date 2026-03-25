# Architecture

> System overview for developers and contributors. This document describes how OpenGen works, what technologies are involved, and how the public components (this repository) interact with the closed-source Master Agent.

> For the verification system, see [verification-system.md](verification-system.md). For the project vision, see [vision.md](vision.md). For design rationale, see [decisions.md](decisions.md).

---

## Open Core model

OpenGen follows the Open Core licensing model. The open-source components (this repository) and the closed-source components communicate through well-defined APIs.

```
┌───────────────────────────────────────────────────────────────┐
│                CLOSED SOURCE (founders' server)               │
│                                                               │
│  Master Agent            Pipeline (5 agents)    Knowledge     │
│  ├── Research scheduler  ├── Retriever          Graph DB      │
│  ├── Task distributor    ├── Planner            ├── Neo4j     │
│  ├── Worker coordinator  ├── Stylist            ├── Search    │
│  └── Security layer      ├── Visualizer         └── Gap       │
│                          └── Multi-Critic           detection │
│                                                               │
└──────────────────┬─────────────────┬──────────────────────────┘
                   │ mTLS            │ HTTPS
                   ▼                 ▼
┌──────────────────────┐  ┌──────────────────────────────────┐
│  OPEN SOURCE         │  │  OPEN SOURCE                     │
│  Worker client       │  │  Public API + Knowledge Guide    │
│  (this repo)         │  │  (this repo)                     │
│                      │  │                                  │
│  Receives tasks      │  │  Search verified knowledge       │
│  Executes via LLM    │  │  Explore connections             │
│  Returns results     │  │  Ask questions (RAG, no halluc.) │
└──────────────────────┘  └──────────────────────────────────┘
```

| Component | License | Description |
|-----------|---------|-------------|
| Worker client | MIT (open source) | Receives tasks, executes via worker's own LLM API key, returns results |
| Shared data models | MIT (open source) | Data format contract between worker and Master Agent |
| Public API client | MIT (open source) | Client library for querying the verified knowledge graph |
| Master Agent | Closed source | Research planning, 5-agent pipeline, knowledge graph management |

---

## System components

OpenGen consists of six components:

| Component | Access | Technology | Function |
|-----------|--------|-----------|----------|
| Master Agent | Closed source | Python | 24/7 research orchestration, knowledge graph, task planning |
| Security Layer | Closed source | Python | I/O scanning, prompt injection detection, hash verification |
| Account & Leaderboard Server | Public API | FastAPI | User accounts, contribution tracking, badges, rankings |
| Public Live Dashboard | Public web | Next.js + Sigma.js | Live research ticker, graph visualization, stats |
| Worker Dashboard | Authenticated | Next.js | Personal stats, review interface, full leaderboard |
| Worker Client | Open source | Python (this repo) | Distributed compute nodes, Docker sandboxed |

All server-side components run in a German data center (IONOS). The Master Agent and Knowledge Graph DB run on physically separate servers with internal low-latency links (sub-millisecond). Public-facing services sit behind Cloudflare.

---

## Enhanced PaperBanana Pipeline v2.0 (Iterative multi-agent pipeline)

The research pipeline is the Master Agent's core process. It processes a question through five specialized agents with an iterative refinement loop.

> **Note:** The pipeline code is closed source. This section describes how it works so the community understands the system, not how to replicate it.

### Agent chain

```
Input: research question
  │
  ▼
Retriever ──→ Planner ──→ Stylist ──→ Style check
                                         │
                                         ▼
                                ┌──────────────────┐
                                │ Refinement loop  │
                                │ (max 20 rounds)  │
                                │                  │
                                │ Visualizer       │
                                │   ▼              │
                                │ Multi-Critic     │
                                │   score ≥ 0.98?  │
                                │   yes → exit     │
                                │   no  → refine   │
                                └────────┬─────────┘
                                         │
                                         ▼
                                  Verified result
                                  → community review
```

### Agent roles

| Agent | Purpose |
|-------|---------|
| Retriever | Searches the knowledge graph for existing relevant knowledge |
| Planner | Creates a structured research plan with quality criteria |
| Stylist | Optimizes the prompt for maximum LLM output quality |
| Visualizer | Generates the actual research result |
| Multi-Critic (×3) | Evaluates factual accuracy (40%), quality (30%), consistency (30%) |

Acceptance threshold: **≥ 0.98** combined score. Maximum **20** refinement rounds. If the threshold is not reached after 20 rounds, the best result is kept for human review or discarded.

---

## Shared data models

The data models in `src/opengen/models/shared.py` define the contract between the Worker and the Master Agent. Both sides must use the same format.

### Key models

**WorkerTask** - what the worker receives:
```python
{
    "id": "uuid",
    "question": "How does chlorophyll absorb light?",
    "domain": "chemistry",
    "instructions": "Focus on the molecular mechanism.",
    "max_tokens": 4096,
    "timeout_seconds": 300
}
```

**WorkerResult** - what the worker sends back:
```python
{
    "task_id": "uuid",
    "worker_id": "uuid",
    "content": "Research result text...",
    "model_used": "claude-sonnet-4-20250514",
    "tokens_used": 1500,
    "duration_seconds": 12.3
}
```

**KnowledgeNode** - what the public API returns:
```python
{
    "id": "uuid",
    "title": "Chlorophyll absorption spectrum",
    "domain": "chemistry",
    "content": "Full verified text...",
    "quality_score": 0.97,
    "status": "verified",
    "stability": "stable",
    "review_count": 42,
    "tags": ["chlorophyll", "light", "absorption"]
}
```

Full model definitions: [`src/opengen/models/shared.py`](../src/opengen/models/shared.py)

---

## Worker architecture

The worker client (this repository) handles the compute-contribution side:

```
┌───────────────────────────────────────────────┐
│                 Worker Client                 │
│                                               │
│  1. Register   → send hardware info to Master │
│  2. Poll       → check for available tasks    │
│  3. Execute    → call LLM with own API key    │
│  4. Submit     → send result to Master        │
│  5. Heartbeat  → periodic health signal       │
│  6. Repeat                                    │
│                                               │
│  Runs in Docker sandbox with resource limits  │
└───────────────────────────────────────────────┘
```

**Key principle:** The worker uses its own LLM API key. Keys never leave the worker's machine and are never transmitted to the Master Agent.

### Worker tech stack

| Component | Technology | Status |
|-----------|-----------|--------|
| Language | Python 3.11+ | Implemented |
| Data models | Pydantic v2 | Implemented |
| HTTP client | httpx | Planned |
| Configuration | pydantic-settings | Implemented |
| Containerization | Docker | Planned |
| Worker auth | mTLS certificates | Planned |

---

## Knowledge access

The verified knowledge graph is accessible through three layers:

### Layer 1: Search
A search field on opengen.live. Type a question, receive matching verified nodes with quality scores and sources. No login required.

### Layer 2: Exploration
Every node displays its connections. Click through related knowledge spatially - like Wikipedia, but with semantically detected connections.

### Layer 3: Knowledge Guide (AI-assisted)
A chat interface that answers exclusively from verified knowledge. No hallucination - every claim is linked to its source node. If no verified knowledge exists, the guide says so honestly.

### Layer 4: Developer API
The public REST API for programmatic access.

---

## REST API (planned)

### Public endpoints (no authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/knowledge/search` | Full-text search across verified nodes |
| GET | `/api/v1/knowledge/nodes/{id}` | Node detail with content, history, connections |
| GET | `/api/v1/knowledge/nodes/{id}/connections` | Connected nodes with edge types |
| GET | `/api/v1/knowledge/suggestions/{id}` | Related topics ("you might also want to know...") |
| POST | `/api/v1/guide/ask` | Knowledge Guide: answer from verified nodes only |
| GET | `/api/v1/stats` | Public statistics |
| GET | `/api/v1/live` | Current research topic and recent results |

### Worker endpoints (mTLS)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/worker/register` | Register a new worker |
| GET | `/api/v1/worker/tasks/next` | Poll for next task |
| POST | `/api/v1/worker/tasks/{id}/result` | Submit task result |
| POST | `/api/v1/worker/heartbeat` | Worker health check |

### Rate limits (public API)

| Tier | Limit | Authentication |
|------|-------|---------------|
| Public | 100 requests/hour | None |
| Developer | 1,000 requests/hour | API key (free, non-commercial) |
| Institutional | 10,000 requests/hour | API key (contact for access) |

---

## Security

| Layer | Mechanism | Status |
|-------|-----------|--------|
| Transport | TLS/HTTPS on all connections | Planned |
| Worker auth | mTLS certificates + signed requests | Planned |
| Execution | Docker sandboxes with CPU/memory/network limits | Planned |
| Input scanning | Prompt injection detection on worker outputs | Planned |
| Output scanning | Malware/trojan scan on incoming data | Planned |
| Integrity | SHA-256 hash verification on every result | Planned |
| Kill switch | Instant worker disconnection | Planned |
| Privacy | GDPR compliant; hosted in Germany; no raw data on master | By design |
| API keys | Worker keys remain local; never transmitted | Implemented |
| Audit trail | All actions logged with timestamps and actor IDs | Planned |

The security architecture is extensible. New modules can be added without disrupting existing operations.

---

## Scaling strategy

| Phase | Nodes | Workers | Infrastructure |
|-------|-------|---------|---------------|
| 1–2 | <1,000 | 0 (local only) | Single server, JSON storage |
| 3 | 1,000–50,000 | 10–100 | Two servers (Master + DB), PostgreSQL, Neo4j |
| 4 | 50,000–500,000 | 100–1,000 | Clustered DB with read replicas, Redis queue |
| 5+ | 500,000+ | 1,000+ | Neo4j cluster, dedicated API servers, CDN caching |

Timelines documented in [vision.md](vision.md#roadmap).
