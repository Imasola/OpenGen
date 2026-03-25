# Architecture decision records

> This document records the major design decisions made during OpenGen's development, the alternatives considered, and the reasoning behind each choice. It serves as a permanent record of *why* the system is built the way it is.

**Format:** Each decision follows the pattern: context → options considered → decision → reasoning.

---

## Contents

1. [Knowledge graph: property graph, not neural network](#adr-001)
2. [Pipeline threshold: 0.98, not 0.95](#adr-002)
3. [Max refinement rounds: 20, not 3 or unlimited](#adr-003)
4. [Community verification: minimum 25 reviewers, not 5](#adr-004)
5. [Trust score: behavioral, not self-declared credentials](#adr-005)
6. [Master Agent: single location in Germany](#adr-006)
7. [Whitepaper: split into three focused documents](#adr-007)
8. [Re-verification: stability tiers, not uniform intervals](#adr-008)
9. [Reviewer interface: three taps, not detailed rubrics](#adr-009)
10. [LLM strategy: orchestrate existing models, not train from scratch](#adr-010)
11. [Knowledge guide: retrieval-only, not generative](#adr-011)
12. [Graph visualization: Sigma.js 2D, not Three.js 3D](#adr-012)
13. [Approval threshold: 80%, not 51% or 100%](#adr-013)
14. [Sensitivity classification: three tiers, not one-size-fits-all](#adr-014)
15. [Open Core: closed-source Master Agent, open-source worker](#adr-015)
16. [Community chat: postponed, use Discord for now](#adr-016)

---

<a id="adr-001"></a>
### ADR-001: Knowledge graph is a property graph, not a neural network

**Context:** The original vision described the knowledge graph as a "neural network" inspired by tools like Obsidian and biological brain structures.

**Options considered:**
1. Call it a neural network and implement neural network concepts (weights, layers, activation functions)
2. Build a standard property graph but call it a neural network for marketing
3. Build a standard property graph and call it what it is

**Decision:** Option 3. The knowledge graph is a property graph implemented with NetworkX (Phase 1–2) and Neo4j (Phase 3+).

**Reasoning:** A neural network has trained weights, backpropagation, activation functions, and layers. None of these apply to a collection of text nodes with typed edges. Calling it a neural network would be technically incorrect and would undermine credibility with developers and researchers who know the difference. The Obsidian-style visualization *looks* like a neural network, but the underlying data structure is a standard property graph - the same technology used by Google Knowledge Graph and Wikidata. This is well-understood, battle-tested, and the right tool for the job.

---

<a id="adr-002"></a>
### ADR-002: Pipeline acceptance threshold is 0.98, not 0.95

**Context:** The Multi-Critic ensemble produces a combined quality score between 0.0 and 1.0. A threshold determines when a result is "good enough" to pass the AI quality gate.

**Options considered:**
1. 0.90 - passes most results quickly, lower quality
2. 0.95 - good balance of quality and efficiency
3. 0.98 - very high bar, more refinement rounds needed
4. 1.0 - theoretically perfect, practically unreachable

**Decision:** 0.98.

**Reasoning:** Results that pass the AI gate still face human review. But human reviewers should not be burdened with low-quality results - that wastes their time and erodes trust in the system. A threshold of 0.98 means only results the AI itself considers near-excellent reach human eyes. The downside is more refinement rounds (and more API cost per result), but quality is more important than throughput, especially in the early phase when credibility is being established. The score can be adjusted later based on empirical data - if 95% of results that score 0.96 also pass human review, the threshold could be lowered.

---

<a id="adr-003"></a>
### ADR-003: Maximum refinement rounds is 20, not 3 or unlimited

**Context:** The PaperBanana pipeline iteratively refines results. The original framework used T=3 fixed rounds.

**Options considered:**
1. Fixed T=3 (original PaperBanana)
2. Fixed T=10
3. Dynamic with max 10
4. Dynamic with max 20
5. Unlimited (run until threshold is reached)

**Decision:** Dynamic scoring with a hard cap at 20 rounds.

**Reasoning:** T=3 is too few for complex topics - some results need 7+ rounds to converge. Unlimited is dangerous - a result that cannot converge would burn API tokens forever. Empirically, most well-scoped research questions converge within 5-10 rounds. Setting the cap at 20 gives complex cross-domain topics room to develop while preventing runaway costs. Each round costs approximately €0.05-0.50 in API calls, so 20 rounds × 1,000 questions/day = manageable cost. The dynamic scoring means simple results exit after 3-4 rounds; only complex ones use the full budget.

---

<a id="adr-004"></a>
### ADR-004: Minimum 25 reviewers, not 5

**Context:** How many human reviewers should evaluate each result before it can be verified?

**Options considered:**
1. 5 reviewers (quick, but statistically weak)
2. 10 reviewers (better, but still small sample)
3. 25 reviewers (strong baseline, scales with community)
4. 50+ for all results (high bar, but slow)

**Decision:** 25 as the floor for Tier 1 (general knowledge), scaling to 10% of active community with a cap at 250. Higher floors for applied science (50) and safety-critical results (100).

**Reasoning:** 5 reviewers is too few to be statistically meaningful - one bad actor or one careless reviewer has 20% influence. With 25 reviewers and an 80% approval threshold, at least 20 people must agree. Combined with trust-weighted voting, this makes manipulation extremely difficult. The "pending principle" ensures that if fewer than 25 qualified reviewers are available, results wait rather than being verified with insufficient oversight. This is slower but honest.

---

<a id="adr-005"></a>
### ADR-005: Domain expertise from behavior, not self-declared credentials

**Context:** Should reviewers declare their qualifications (e.g., "I have a PhD in biology") or should the system detect expertise from voting patterns?

**Options considered:**
1. Self-declared credentials with document upload
2. Self-declared credentials without verification
3. Behavioral detection from voting accuracy
4. No domain distinction - all votes equal

**Decision:** Option 3. Behavioral detection.

**Reasoning:** Self-declared credentials are trivially faked and impossible to verify at scale. A real biologist who consistently identifies correct biology results demonstrates more useful expertise than someone who uploads a diploma scan. Behavioral detection is immune to credential fraud, works across all countries (no need to verify foreign degrees), and measures what actually matters: can this person reliably evaluate results in this domain? The 20-review qualification threshold is high enough to prevent gaming but low enough that genuine experts qualify within weeks of active use.

---

<a id="adr-006"></a>
### ADR-006: Master Agent hosted in Germany, single location

**Context:** Where should the Master Agent and knowledge graph be hosted?

**Options considered:**
1. Single server in Germany
2. Multi-region deployment (Germany + US + Asia)
3. Fully distributed / peer-to-peer
4. Cloud provider (AWS/GCP) with auto-scaling

**Decision:** Single data center in Germany - with physically separate servers for Master Agent and database. Failover to a second EU location planned for Phase 4+.

**Reasoning:** Germany provides GDPR compliance and EU data sovereignty - a trust advantage for an open-science project. Multi-region adds complexity that is unjustified at this stage. Worker communication is task-polling (every few seconds), not real-time, so 200ms latency to distant workers is acceptable. The real risk is single-point-of-failure, addressed by: (a) separate servers for Master and database within the same data center, and (b) automated daily backups to a geographically separate location. Full multi-region deployment is on the roadmap but not needed before the system handles significant traffic.

---

<a id="adr-007"></a>
### ADR-007: Three focused documents instead of a monolithic whitepaper

**Context:** The original plan was a single whitepaper covering vision, architecture, verification, funding, and ethics.

**Options considered:**
1. Single whitepaper (traditional format)
2. README only (minimal documentation)
3. Three focused documents: architecture, verification system, vision

**Decision:** Option 3, with the whitepaper retained as a separate investor document not published on GitHub.

**Reasoning:** A monolithic whitepaper tries to serve developers, investors, scientists, and community members simultaneously - and serves none of them well. Developers want technical specs, not founders' statements. Investors want costs and vision, not API endpoints. Splitting into three documents lets each audience find exactly what they need. On GitHub specifically, a "whitepaper" signals either academic research (which this is not yet) or crypto/blockchain marketing (which damages credibility). Architecture decision records (this document) add a fourth layer that shows the reasoning behind choices - something the open-source community values highly.

---

<a id="adr-008"></a>
### ADR-008: Re-verification uses stability tiers, not uniform intervals

**Context:** Verified knowledge should be periodically re-checked. But how often?

**Options considered:**
1. No re-verification (verify once, trust forever)
2. Uniform interval (e.g., every 12 months for everything)
3. Stability tiers (permanent, stable, standard, fast-moving)

**Decision:** Option 3. Four stability tiers with different intervals.

**Reasoning:** "1+1=2" and "the latest AI benchmark results" have fundamentally different shelf lives. Re-verifying mathematical axioms every 12 months wastes reviewer time and creates unnecessary review queue load. Conversely, a 12-month interval is too long for fast-moving research areas. The four-tier system (permanent: never, stable: 24 months, standard: 12 months, fast-moving: 6 months) matches re-verification frequency to the actual rate of change in each knowledge area. The "permanent" tier requires admin confirmation to prevent premature classification.

---

<a id="adr-009"></a>
### ADR-009: Reviewer interface uses three simple taps, not detailed rubrics

**Context:** How should reviewers provide their assessment of a result?

**Options considered:**
1. Single vote: Correct / Incorrect
2. Three questions with Yes / No / Not sure (current design)
3. Five-point scale on three dimensions (1–5 for facts, completeness, clarity)
4. Detailed rubric with written justification required

**Decision:** Option 2. Three binary-ish questions.

**Reasoning:** The more complex the review interface, the fewer people will use it. A 5-point scale on three dimensions is 15 mental decisions per review. Required written justification means only highly motivated experts will participate. Three taps with Yes/No/Not sure is completable in under two minutes and accessible to anyone - including non-experts whose common sense catches different errors than domain specialists. The system compensates for the simplicity of individual reviews through volume (25+ reviewers), trust weighting, and quality scoring that runs invisibly behind the simple interface. Optional written feedback is rewarded but never required.

---

<a id="adr-010"></a>
### ADR-010: Orchestrate existing LLMs, not train custom models

**Context:** Should OpenGen use existing LLMs (Claude, GPT-4, Llama) or train its own models?

**Options considered:**
1. Train custom models from the start
2. Use existing LLMs now, train custom models later (Phase 6)
3. Use existing LLMs indefinitely

**Decision:** Option 2. Use existing LLMs immediately, plan custom models for Phase 6+.

**Reasoning:** Training a competitive LLM costs millions in GPU compute. OpenGen's budget for year one is €5,000–10,000. This is not a resource constraint to be overcome - it is a fundamental mismatch in scale. Existing LLMs (Claude, GPT-4) are already excellent at the text tasks OpenGen needs. The innovation is not in the model but in the pipeline, verification, and knowledge graph around it. Custom model fine-tuning becomes viable in Phase 6 when the verified knowledge graph provides a high-quality training dataset - and when community-contributed GPUs provide the compute. Until then, orchestrating existing models is 1,000× more cost-effective.

---

<a id="adr-011"></a>
### ADR-011: Knowledge guide answers only from verified nodes, never generates freely

**Context:** The knowledge guide is a chat interface where users ask questions. Should it generate answers freely or only from verified knowledge?

**Options considered:**
1. General-purpose chatbot that can answer anything (like ChatGPT)
2. Retrieval-augmented generation constrained to verified nodes only
3. No chat interface - search and browse only

**Decision:** Option 2. Retrieval-augmented generation (RAG) with strict constraint to verified nodes.

**Reasoning:** A general-purpose chatbot defeats the entire purpose of OpenGen. If the guide can hallucinate freely, users cannot trust that any given statement is verified. By constraining responses to verified knowledge graph content, every claim the guide makes is traceable to a human-verified source node. When no verified knowledge exists for a question, the guide says so honestly - this transparency is OpenGen's core value proposition. The guide summarizes and connects verified nodes in natural language, but it creates no new claims. This is the critical difference from existing AI chatbots.

---

<a id="adr-012"></a>
### ADR-012: Graph visualization uses Sigma.js 2D, not Three.js 3D

**Context:** The knowledge graph needs a public visualization on opengen.live. What rendering technology should be used?

**Options considered:**
1. Sigma.js (2D force-directed graph, specialized for large networks)
2. D3.js (general-purpose 2D visualization)
3. Three.js (3D WebGL rendering)
4. Cytoscape.js (scientific graph visualization)

**Decision:** Sigma.js for 2D rendering. 3D is not on the current roadmap.

**Reasoning:** Sigma.js is purpose-built for large network visualization in the browser. It handles tens of thousands of nodes smoothly, has built-in zoom/pan/filter, and produces the Obsidian-style visualization that inspired the project. Three.js 3D looks spectacular in demos but is harder to navigate, requires more compute, and doesn't add meaningful utility for a knowledge graph - users need to read text on nodes, which is easier in 2D. D3.js is more general but less performant for pure graph rendering. Cytoscape.js is optimized for scientific analysis, not public-facing visualization. If the graph exceeds ~100,000 nodes, server-side pre-rendering or WebGL-based solutions will be evaluated - but that is a scaling problem for the future, not a technology choice for today.

---

<a id="adr-013"></a>
### ADR-013: Approval threshold is 80%, not 51% or 100%

**Context:** What percentage of reviewers must approve a result for it to enter the knowledge graph?

**Options considered:**
1. Simple majority (51%) - democratic but weak
2. Two-thirds (67%) - moderate consensus
3. 80% (Tier 1), 85% (Tier 2), 90% (Tier 3) - strong consensus with sensitivity scaling
4. Unanimous (100%) - strongest but impractical

**Decision:** Option 3. 80% baseline with elevated thresholds for higher-risk content.

**Reasoning:** 51% means nearly half of reviewers can disagree and the result still passes - that is not meaningful verification. 100% is impractical because even correct results will occasionally receive a wrong vote from inattentive reviewers. 80% with trust-weighted voting means that the *effective* agreement must be very strong - low-trust reviewers' disagreements carry less weight, so 80% weighted approval is a higher real bar than 80% raw count. The tiered system (85% for applied science, 90% for safety-critical) reflects that the cost of error varies: a wrong fact about ancient history is far less dangerous than a wrong fact about chemical toxicity.

---

<a id="adr-014"></a>
### ADR-014: Three sensitivity tiers, not one standard for all content

**Context:** Should all knowledge be verified with the same rigor, or should the verification requirements scale with the risk of the content being wrong?

**Options considered:**
1. One standard for all results (simpler, uniform)
2. Two tiers: general and safety-critical
3. Three tiers: general, applied, safety-critical

**Decision:** Option 3. Three tiers.

**Reasoning:** A single standard forces a compromise: either set it too low (inadequate for medical information) or too high (overkill for historical facts, creating unnecessary bottlenecks). Three tiers allow appropriate rigor for each category. The middle tier ("applied science") captures a large category of knowledge that isn't immediately life-threatening but could inform real decisions - engineering specs, chemical properties, environmental data. These deserve more scrutiny than trivia but don't need the full apparatus required for medical or toxicology content. Tier assignment is automatic but escalation-only (upward), preventing the system from ever underclassifying a result.

---

<a id="adr-015"></a>
### ADR-015: Open Core - closed-source Master Agent, open-source worker

**Context:** Should all code be open source, or should some components remain closed?

**Options considered:**
1. Fully open source - all code on GitHub (including Master Agent, pipeline, knowledge graph)
2. Fully closed source - nothing on GitHub, just binaries
3. Open Core - Master Agent closed, worker client and shared libraries open

**Decision:** Option 3. Open Core.

**Reasoning:** The Master Agent is OpenGen's core intelligence - it plans research, orchestrates agents, manages the knowledge graph, and enforces quality standards. Making it fully open source would allow bad actors to reverse-engineer the research process, study the security layer's detection patterns, and find ways to manipulate the system. At the same time, a fully closed project cannot build community trust or attract volunteer contributors. Open Core solves both: the worker client is open so anyone can verify what runs on their machine, the data models are open so developers can build on the API, and the documentation is open so the community understands how verification works. The Master Agent stays closed to protect system integrity. This is the same model used by GitLab (Community Edition vs. Enterprise), Elastic (Elasticsearch open core), and Grafana (open source dashboard, enterprise features closed).

---

<a id="adr-016"></a>
### ADR-016: Community chat postponed - use Discord for now

**Context:** Should opengen.live include a built-in community chat (similar to Skool or Slack)?

**Options considered:**
1. Build a custom chat into opengen.live from day one
2. Use an existing platform (Discord, GitHub Discussions) now, build custom later
3. No community space at all

**Decision:** Option 2. Discord for now, custom chat in Phase 5+.

**Reasoning:** A real-time chat system with message persistence, moderation, user profiles, and channels is weeks of development work. OpenGen currently has no functioning website, no verification system, and no knowledge graph. Building a chat before the core product works is scope creep - it consumes development time that should go toward the pipeline and verification system. Discord is free, immediately available, supports text channels, voice, and moderation. GitHub Discussions is built into the repository and requires zero setup. Both serve the community-building purpose at zero cost. When opengen.live reaches 1,000+ active users (Phase 5 timeframe), a custom integrated chat becomes worth the investment. Until then, existing tools are the right choice.
