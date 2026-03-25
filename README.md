<p align="center">
  <img src="https://img.shields.io/badge/Status-Early%20Stage-blue?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Python-3.11+-yellow?style=flat-square" alt="Python"/>
  <img src="https://img.shields.io/badge/Made%20in-Germany-red?style=flat-square" alt="Germany"/>
</p>

<h1 align="center">OpenGen</h1>

<p align="center">
  <strong>Distributed AI research system - worker client and public API</strong><br>
  Community-powered. Human-verified. Built for science.<br><br>
  <a href="https://opengen.live">opengen.live</a> <sup>(coming soon)</sup> · 
  <a href="#quickstart">Quickstart</a> · 
  <a href="docs/architecture.md">Architecture</a> · 
  <a href="docs/verification-system.md">Verification system</a> · 
  <a href="#contributing">Contributing</a>
</p>

---

## What is OpenGen?

OpenGen is a distributed AI system that researches scientific topics around the clock, improves its own results through an iterative multi-agent pipeline, and stores verified knowledge in a connected graph - like a living encyclopedia that grows every day.

What makes it different:

- **Every result is verified by real humans** before it becomes permanent knowledge
- **The entire research process is transparent** - anyone can watch it live on opengen.live
- **Anyone can contribute compute power** by running the open-source worker program
- **The knowledge graph is open** - searchable and queryable through a free public API
- **Coordinated manipulation is actively detected** - protecting against industry lobbying and organized influence campaigns

OpenGen is not a chatbot. It is an open, community-verified AI knowledge network.

---

## How it works

```
┌─────────────────────────────────────────────────────────────┐
│                    Master Agent (closed source)             │
│  Runs 24/7 on a secure server in Germany                    │
│  Plans research · Orchestrates 5 AI agents                  │
│  Maintains the knowledge graph · Coordinates workers        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Enhanced PaperBanana Pipeline v2.0                 │    │
│  │  Retriever → Planner → Stylist → Visualizer → Critic│    │
│  │  Up to 20 refinement rounds · Score ≥ 0.98 required │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│ Worker A     │ │ Worker B     │ │ Worker N                 │
│ (this repo)  │ │ (this repo)  │ │ (this repo)              │
│ Contributes  │ │ Contributes  │ │ Anyone can run a worker  │
│ CPU/GPU/API  │ │ CPU/GPU/API  │ │ Open source (MIT)        │
└──────┬───────┘ └──────┬───────┘ └────────────┬─────────────┘
       │                │                      │
       └────────────────┼──────────────────────┘
                        │ Results
                        ▼
              ┌──────────────────────┐
              │ Community review     │
              │ Min. 25 reviewers    │
              │ Trust-weighted votes │
              │ Lobby detection      │
              └──────────┬───────────┘
                         │
              ┌──────────▼───────────┐
              │ Knowledge graph      │
              │ Public · Searchable  │
              │ Free API access      │
              └──────────────────────┘
```

---

## Open Core model

OpenGen follows the **Open Core** licensing model, used by companies like GitLab, Elastic, and Grafana:

| Component | License | Location |
|-----------|---------|----------|
| Worker client | MIT (open source) | **This repository** |
| Shared data models | MIT (open source) | **This repository** |
| Public API client | MIT (open source) | **This repository** |
| Documentation | MIT (open source) | **This repository** |
| Master Agent | Closed source | Founders' server |
| Pipeline agents | Closed source | Founders' server |
| Knowledge graph engine | Closed source | Founders' server |
| Research scheduler | Closed source | Founders' server |

**Why?** The Master Agent is OpenGen's core intelligence - the part that plans research, orchestrates agents, and maintains knowledge quality. Keeping it closed source protects the integrity of the system and prevents bad actors from reverse-engineering the research process. Everything you need to **contribute to** and **benefit from** OpenGen is open source.

---

## Documentation

| Document | Description |
|----------|------------|
| **[Architecture](docs/architecture.md)** | System overview, tech stack, API endpoints, data models |
| **[Verification system](docs/verification-system.md)** | Trust scores, sensitivity tiers, honeypots, lobby protection, all thresholds |
| **[Vision](docs/vision.md)** | Why OpenGen exists, ethical principles, use cases, funding, roadmap |
| **[Decisions](docs/decisions.md)** | Architecture decision records: why we chose what we chose |

---

<a id="quickstart"></a>
## Quickstart

> **Note:** The worker client is in active development (Phase 4 on the roadmap). The following instructions install the shared libraries and data models. Full worker functionality will be available when the Master Agent is ready to accept connections.

### Prerequisites

- Python 3.11+
- Git

### Installation

```bash
git clone https://github.com/Imasola/OpenGen.git
cd opengen

python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

pip install -e .

# Test that everything loads correctly
python -m opengen.models.shared
```

### For future worker setup (Phase 4)

```bash
cp .env.example .env
# Edit .env with your connection details and API key
# python -m opengen.worker.client   (not yet available)
```

---

## Project structure

```
opengen/
├── docs/
│   ├── architecture.md            # System overview
│   ├── verification-system.md     # Community review design
│   ├── vision.md                  # Project vision and roadmap
│   └── decisions.md               # Architecture decision records
├── src/opengen/
│   ├── models/
│   │   └── shared.py              # Data models (shared with Master Agent)
│   ├── worker/
│   │   ├── config.py              # Worker connection settings
│   │   ├── client.py              # Worker ↔ Master communication
│   │   ├── executor.py            # Task execution in sandbox
│   │   └── hardware.py            # CPU/GPU/RAM detection
│   └── api/
│       └── client.py              # Public knowledge graph API client
├── tests/
│   └── test_models.py             # Automated tests
├── docker/
│   └── Dockerfile                 # Run the worker in a container
└── [config files]                 # LICENSE, CONTRIBUTING, etc.
```

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Core infrastructure: pipeline, agents, knowledge graph (closed source) | **Current** |
| Phase 2 | Full 5-agent pipeline, dynamic refinement loop, research scheduler | Q2 2026 |
| Phase 3 | opengen.live: public dashboard, accounts, leaderboard, community review | Q3 2026 |
| Phase 4 | **Worker network: this repository becomes functional** | Q4 2026 |
| Phase 5–6 | Public API, multilingual support, custom models | 2027+ |

Timelines are estimates. Full details in [docs/vision.md](docs/vision.md#roadmap).

---

<a id="contributing"></a>
## Contributing

| Way | How |
|-----|-----|
| **Code** | Fork → branch → PR. See [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Compute** | Run the worker program (available Phase 4) |
| **Review** | Vote on AI-generated results at opengen.live (available Phase 3) |
| **Ideas** | Open an issue or start a discussion |
| **Documentation** | Improve docs, fix typos, translate |
| **Spread the word** | Star this repo |

---

## Security

Found a vulnerability? See [SECURITY.md](SECURITY.md). Do not open a public issue.

---

## Founders

**Imasola** — a small startup from Germany.

> *"We believe that community-driven infrastructure can contribute to scientific progress in ways that centralized companies cannot — through transparency, community verification, and open access."*

---

## License

[MIT License](LICENSE) — the worker client, shared models, API client, and all code in this repository are open source.

The Master Agent, pipeline agents, knowledge graph engine, and research scheduler are closed source and run on the founders' infrastructure.

---

<p align="center">
  <strong>OpenGen is a project for the people, by the people.</strong><br>
  Built to advance science. Verified by humans. Powered by community.
</p>
