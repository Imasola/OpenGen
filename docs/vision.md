# Vision

> Why OpenGen exists, what it aims to achieve, and the principles it follows. For technical details, see [architecture.md](architecture.md). For the verification system, see [verification-system.md](verification-system.md).

---

## What OpenGen is

OpenGen is an open, community-verified scientific knowledge network. A Master Agent researches autonomously across scientific disciplines. Community members contribute compute power and verify AI-generated results through a structured peer-review system. Only results that pass both AI quality checks and human approval become permanent knowledge.

The knowledge graph is publicly searchable and accessible through a free API. The research process is observable in real time on [opengen.live](https://opengen.live).

---

## The problem

Current AI systems suffer from three weaknesses:

**Hallucination without accountability.** Large language models generate false statements with confidence. No major AI platform has a systematic mechanism to prevent false knowledge from propagating. Users cannot distinguish AI-generated truth from AI-generated fiction.

**Opacity.** Users cannot see what an AI system knows, how it was trained, or what research it has conducted. The knowledge is locked inside proprietary systems controlled by a single company.

**Centralized control.** One company decides what gets researched, what gets prioritized, and what gets filtered. There is no community input into what knowledge gets built.

OpenGen addresses all three through human verification, public transparency, and community governance.

---

## What makes OpenGen different

OpenGen is not a chatbot and does not compete with ChatGPT, Claude, or Gemini. It does something none of them do:

**Verified knowledge.** Every result passes through an AI quality gate (score ≥ 0.98), a security scan, and a community peer review (minimum 25 verified reviewers, 80%+ approval) before it becomes permanent knowledge. No other AI system has this level of verification.

**Transparent process.** Anyone can visit opengen.live and see what the Master Agent is researching right now, how the knowledge graph is growing, and how each result was reviewed. The full review history of every knowledge node is public.

**Open access.** The verified knowledge graph is free to search, free to read, and free to query through a public API. Verified knowledge is treated as a public good.

**Community-driven research.** Contributors influence the research direction by providing compute, reviewing results, and suggesting topics. The system prioritizes research that fills gaps in the knowledge graph.

**Self-correcting.** Knowledge is re-verified periodically. Outdated results are flagged. Version history tracks how understanding evolves. Minority opinions are preserved, not deleted.

**Open Core.** The worker client, shared data models, API client, and all documentation are open source (MIT). The Master Agent and research pipeline are closed source to protect system integrity. See [architecture.md](architecture.md) for details.

---

## Research scope

OpenGen researches across all scientific and engineering disciplines relevant to human advancement - from fundamental sciences like biology, chemistry, physics, and mathematics to applied fields like space science, medicine, energy, robotics, agriculture, and environmental science.

The scope is not limited to predefined domains. It expands as the knowledge graph grows and as the community identifies new areas of interest.

The long-term research direction is driven by a question: what does humanity need to know to thrive - on Earth and beyond?

---

## Who OpenGen is for

**Researchers and academics** gain a searchable, verified knowledge base that grows daily and surfaces cross-domain connections that traditional literature reviews miss. The public API allows integration into existing research workflows.

**Students and educators** get AI-generated explanations that have been verified by the community - with full version history showing how understanding of a topic evolved over time.

**The general public** can browse verified scientific knowledge for free on opengen.live - no account, no subscription, no paywall for reading.

**Open-source developers** can build applications on top of the knowledge graph through the public API - educational tools, research assistants, visualization dashboards, domain-specific apps.

**Contributors** can donate compute power and review expertise, with visible impact tracked through a public leaderboard with badges and rankings.

**Governments and NGOs** can query verified, auditable scientific knowledge as a foundation for evidence-based policy - once the graph reaches sufficient depth in relevant domains.

**Industry** can use verified knowledge nodes as building blocks for domain-specific applications. Unlike raw LLM output, every node comes with a quality score, review history, and source trail.

---

## Ethical principles

1. **Safety first** - Every result is scanned for security threats and verified by humans before it becomes knowledge
2. **Transparency** - The research process is public and observable in real time
3. **Voluntary participation** - Contributing compute, reviews, or donations is always optional
4. **Human benefit** - Designed and intended exclusively for scientific and civilian benefit. The founders will not knowingly cooperate with surveillance, manipulation, or military applications
5. **Privacy by design** - GDPR compliant, minimal data collection, hosted in Germany under EU data protection law
6. **Community governance** - The research agenda is influenced by contributors, not dictated by a single entity
7. **Accountability** - The founders personally stand behind these principles
8. **Open access** - Verified knowledge is a public good, not a proprietary asset

---

## Founders

**Imasola** - a small startup from Germany.

> *"We believe that community-driven infrastructure can contribute to scientific progress in ways that centralized companies cannot - through transparency, community verification, and open access."*

---

## Funding and sustainability

OpenGen is self-funded in its early stage. Estimated monthly costs for Phase 1-2 are €1170-2750 (server hosting, LLM API calls, domain/CDN, Hardware). The 12-month runway requirement is approximately €5,000-10,000.

Costs decrease over time as worker-contributed compute reduces API dependency, caching prevents duplicate queries, and model routing directs simple tasks to cheaper models.

We are open to sponsors, investors who share our values, grants from scientific foundations or EU research programs, and community donations. There are no salaries in the early stage - the founders work on this out of conviction.

Every euro goes directly into infrastructure and research capacity.

---

## Roadmap

| Phase | Focus | Timeline |
|-------|-------|----------|
| Phase 1 | Foundation: LLM client, agents, basic pipeline, knowledge graph | Current |
| Phase 2 | Full 5-agent pipeline, dynamic loop, research scheduler, REST API | Q2 2026 |
| Phase 3 | opengen.live: public dashboard, accounts, leaderboard, community review | Q3 2026 |
| Phase 4 | Worker network: open-source client, security layer, distributed execution | Q4 2026 |
| Phase 5 | Public knowledge API, multilingual support, mobile access | 2027 |
| Phase 6 | Custom model fine-tuning, graph pattern recognition, reduced API dependency | 2027+ |

Timelines are estimates and depend on funding, community growth, and development capacity. Each phase builds on the previous one and produces a functional system - not a prototype that only works when everything is complete.

---

## One principle above all

OpenGen would rather have an empty knowledge graph than a poorly verified one. The first verified result will have earned that status through a process more rigorous than any existing AI platform offers.

That credibility is the foundation everything else is built on.
