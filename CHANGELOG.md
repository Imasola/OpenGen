# Changelog

All notable changes to OpenGen will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.1.0] — 2026-03-16

### Added
- Project structure and Python package setup
- Core configuration module (`core/config.py`) with .env support
- Pydantic data models for knowledge nodes, edges, tasks, and pipeline results (`core/models.py`)
- Unified LLM client supporting Anthropic and OpenAI (`llm/client.py`)
- Base agent class with LLM integration (`agents/base.py`)
- Critic agent with JSON-based quality scoring (`agents/critic.py`)
- Retriever, Planner, Stylist, and Visualizer agents (`agents/retriever.py`)
- Full pipeline orchestrator connecting all 5 agents (`agents/orchestrator.py`)
- Knowledge graph with JSON persistence, search, and connection tracking (`knowledge/graph.py`)
- Simplified pipeline runner with iterative refinement loop (`pipeline/runner.py`)
- Documentation: architecture, verification system, vision, architecture decisions
- README with quickstart, project structure, and roadmap
- MIT License, Contributing guide, Code of Conduct, Security policy
