# Community verification system

> Design document for OpenGen's human verification layer. This is OpenGen's core differentiator: no AI-generated result enters the permanent knowledge graph without human approval.

**Design philosophy:** Simple for the reviewer, rigorous behind the scenes. A reviewer sees a clean result, gives their assessment in under two minutes, and moves on. Trust scoring, manipulation detection, domain matching, and quality tracking run invisibly in the background.

**Status:** Design complete. Implementation planned for Phase 3.

---

## Contents

1. [Verification process](#1-verification-process)
2. [Reviewer interface](#2-reviewer-interface)
3. [Becoming a reviewer](#3-becoming-a-reviewer)
4. [Trust score](#4-trust-score)
5. [Domain expertise](#5-domain-expertise)
6. [Sensitivity classification](#6-sensitivity-classification)
7. [Cross-domain review](#7-cross-domain-review)
8. [Review quality scoring](#8-review-quality-scoring)
9. [Dissent protection](#9-dissent-protection)
10. [Appeal process](#10-appeal-process)
11. [Re-verification and stability](#11-re-verification-and-stability)
12. [Knowledge version history](#12-knowledge-version-history)
13. [Honeypot system](#13-honeypot-system)
14. [Anti-manipulation safeguards](#14-anti-manipulation-safeguards)
15. [Coordinated influence protection](#15-coordinated-influence-protection)
16. [The pending principle](#16-the-pending-principle)

---

## 1. Verification process

Every result passes through three gates before it becomes permanent knowledge:

**Gate 1 - AI quality gate**
The Enhanced PaperBanana Pipeline must produce a result with a Multi-Critic score ≥ 0.98 within a maximum of 20 refinement rounds. Results that cannot reach this threshold are discarded. See [architecture.md](architecture.md) for pipeline details.

**Gate 2 - Security gate**
The security layer scans the result for prompt injection, malware, data leaks, and verifies the integrity hash (SHA-256). Any failure means immediate rejection - the result never reaches human reviewers.

**Gate 3 - Human verification gate**
The result enters the public review queue on opengen.live. Verified community members evaluate it. This is the final and most important gate.

Outcomes based on weighted approval percentage:

| Weighted approval | Result |
|-------------------|--------|
| 80%+ (Tier 1), 85%+ (Tier 2), 90%+ (Tier 3) | Enters permanent knowledge graph |
| 60-80% | "Disputed" status → second independent review round with fresh reviewers |
| Below 60% | Rejected → returns to pipeline with community feedback attached |

Second-round reviewers have not seen the first round's vote distribution.

---

## 2. Reviewer interface

The interface is intentionally minimal:

1. **The result** - title, content, domain tag, AI confidence score
2. **Three questions**, each answered with one tap:
   - "Are the facts correct?" → Yes / No / Not sure
   - "Is it complete?" → Yes / No / Not sure
   - "Is it clearly written?" → Yes / No / Not sure
3. **Optional feedback field** - free text, not required, but rewarded (see section 8)

No forms, no lengthy assessments. Three taps and an optional comment. Designed to take under two minutes for most results.

Everything described in the following sections runs invisibly behind this interface.

---

## 3. Becoming a reviewer

New accounts do not receive immediate voting rights.

**Observer phase:**
- New accounts start in "Observer" status - full read access, no voting
- Requirements to advance:
  - Email verified
  - Account age ≥ 7 days
  - Complete 10 silent test reviews

**Silent onboarding test:**
- A new user's first 10 reviews are all honeypots - results whose correctness is already known
- The user does not know they are being tested; the interface is identical to regular reviews
- 8 out of 10 correct → automatic promotion to Reviewer
- Fewer than 8 → remains Observer, receives 10 fresh tests after a 7-day cooldown

This tests actual review behavior rather than test-taking ability.

---

## 4. Trust score

Every reviewer has a trust score (invisible to the reviewer) that determines vote weight.

**Scoring rules:**

| Event | Trust change |
|-------|-------------|
| Correct vote (aligned with verified consensus) | +0.01 |
| Incorrect vote (against verified consensus) | -0.05 |
| Honeypot failure | -0.15 |
| Inactivity (per month without reviews) | -0.02 (decays toward 0.5) |

- Starting score: 0.5
- Maximum: 1.0
- Score is never shown as a number to the reviewer - only the badge tier is visible

**Trust thresholds:**

| Trust range | Effect |
|-------------|--------|
| 0.7–1.0 | Full vote weight. Eligible for appeals and dissent protection. |
| 0.3–0.7 | Proportional vote weight |
| 0.2–0.3 | Votes silently ignored. Account flagged for admin review. |
| Below 0.1 | Automatic suspension with notification |

The asymmetry is intentional: trust is slow to build (+0.01) and fast to lose (-0.05 / -0.15). This makes it expensive for bad actors to build trust and costly to abuse it.

---

## 5. Domain expertise

The system learns expertise from behavior, not self-declaration.

**How it works:**
- The system tracks which domains a reviewer votes in most frequently and most accurately
- After 20+ accurate reviews in a single domain → automatically tagged as domain expert
- Domain-expert votes carry **2× weight** on results in their field
- Non-expert votes count at 1× weight (common sense catches errors that specialists miss)
- Expertise fades: 6+ months without reviews in a domain resets the multiplier

**Why behavioral detection:**
- Anyone can claim credentials; not everyone can consistently identify correct results
- Immune to credential fraud
- Rewards demonstrated competence, not titles

---

## 6. Sensitivity classification

Not all knowledge carries equal risk if wrong. Results are classified into three tiers:

| Tier | Description | Min. reviewers | Approval threshold | Domain expert ratio |
|------|-------------|---------------|-------------------|-------------------|
| **Tier 1** - General | Theory, history, general science | 25 | 80% | No minimum |
| **Tier 2** - Applied | Engineering specs, chemical properties, environmental data | 50 | 85% | ≥40% |
| **Tier 3** - Safety-critical | Medical, toxicology, radiation, structural safety | 100 | 90% | ≥60% + admin sign-off |

**Reviewer threshold scaling:**
- Minimum reviewers = 10% of active verified community members
- Floor: values in table above (25 / 50 / 100)
- Cap: 250 reviewers per result

Tier assignment is automatic (Multi-Critic content analysis) but can be escalated by any reviewer or admin. Escalation is one-way - upward only, never downward.

---

## 7. Cross-domain review

Results spanning multiple domains require balanced representation:

- System detects multi-domain results based on tags and knowledge graph connections
- Minimum 5 domain-matched reviewers per involved domain
- Approval threshold must be met **independently within each domain group**
- If one domain approves and another rejects → "disputed" status with domain-specific feedback

This prevents a majority from one domain approving claims in a domain they are not qualified to evaluate.

---

## 8. Review quality scoring

The system tracks engagement quality invisibly:

**Time awareness:**
- Reviews submitted in under 30 seconds on results longer than 500 words are flagged
- Consistently fast reviews (bottom 5% of all reviewers) → trust penalty of -0.03
- Invisible to the reviewer

**Feedback rewards:**
- Written feedback that leads to measurable pipeline improvement → +0.02 trust bonus
- Incentivizes thoughtful critique without requiring it

**Rubber-stamp detection:**
- Reviewers answering "Yes / Yes / Yes" on more than 85% of reviews are flagged
- Honeypot frequency is increased for flagged reviewers
- Genuine evaluation produces natural variance

**Quality badges (visible):**
- "Thorough reviewer" - average review time in top 25%
- "Valuable feedback" - 3+ feedbacks that improved pipeline results
- "Critical eye" - healthy variance in voting patterns

Badges are positive reinforcement. Penalties are invisible.

---

## 9. Dissent protection

Scientific consensus is not always correct. The system protects well-reasoned dissent:

1. A reviewer with trust ≥ 0.85 **and** domain expertise votes against an otherwise approved result
2. Result enters 72-hour hold - not yet finalized
3. Dissenting reviewer must provide written justification (required to maintain hold)
4. Justification is sent to 3 independent domain-expert reviewers (trust ≥ 0.8, not part of original review)
5. If 2 of 3 agree with dissent → result returns to pipeline with critique
6. If overruled → result is approved; minority opinion is permanently preserved in the node's history

Minority opinions are never deleted. They serve as early warnings for future re-evaluation.

---

## 10. Appeal process

**Challenging a rejected result:**
- Any reviewer with trust ≥ 0.7 can file an appeal
- Triggers independent review round with fresh reviewers
- If approved in second round → enters knowledge graph; original rejection logged for analysis

**Challenging an approved result:**
- Any reviewer with trust ≥ 0.7 can flag an approved result
- If 3+ high-trust reviewers independently flag the same result → temporarily removed, full re-review
- Original approval votes analyzed for coordinated manipulation

**Admin escalation:**
- Results failing appeal twice or generating significant dispute → admin review with full audit trail
- Option to consult external subject-matter experts

---

## 11. Re-verification and stability

Not all knowledge requires re-checking at the same frequency. Each node has a stability classification:

| Stability | Re-verification interval | Criteria | Examples |
|-----------|------------------------|----------|----------|
| **Permanent** | Never (can still be appealed) | Mathematical axioms, physical constants, logical tautologies. Must pass with 90%+ approval, ≥3 domain experts, admin confirmation. No qualifying language ("currently," "recent studies suggest"). | 1+1=2, speed of light, gold has 79 protons |
| **Stable** | Every 24 months | Well-established science, extremely unlikely to change | DNA structure, photosynthesis mechanism, Newton's laws |
| **Standard** | Every 12 months | Solid current knowledge that could be refined | Disease mechanisms, climate models, engineering best practices |
| **Fast-moving** | Every 6 months | Active research, changes rapidly | AI benchmarks, pandemic research, new exoplanets |

**Automatic promotion:** A "standard" node that passes re-verification 3 consecutive times without changes is promoted to "stable."

**Automatic demotion:** If a new node contradicts an existing one, both are demoted by one tier and enter re-verification simultaneously.

**High-traffic nodes** (frequently referenced by newer results) are re-verified one tier faster than their classification suggests.

Re-verification follows the same process and thresholds as initial verification.

Nodes that fail re-verification are marked as "outdated" and visually flagged but never deleted.

---

## 12. Knowledge version history

Every change creates a new version, not an overwrite:

- Complete version history is publicly visible on each node
- Each version records: content, review votes, scores, timestamp, reason for change
- Superseded versions are marked "historical" with a "superseded by" link
- Similar to Wikipedia's edit history or Git's commit log

This creates an auditable, tamper-proof record of how knowledge evolves over time.

---

## 13. Honeypot system

Approximately 15% of review queue items are calibration checks - results with known correctness (confirmed correct or deliberately flawed).

- Reviewers cannot distinguish honeypots from real reviews
- Performance directly impacts trust score
- Honeypots are refreshed regularly from a growing pool to prevent pattern recognition

**Purposes:**
1. Catch malicious actors voting incorrectly on purpose
2. Catch careless reviewers voting without reading
3. Provide continuous calibration data for the trust score algorithm

---

## 14. Anti-manipulation safeguards

All protective mechanisms in one place:

- One verified account = one vote per result
- Reviewer-to-result assignment is randomized
- Current vote distribution is hidden until own vote is submitted
- Voting windows are time-limited
- All votes are immutably logged (timestamp, reviewer ID, trust score, domain match status)
- Bulk account creation from same IP or device fingerprint is flagged
- Geographic diversity: max 60% of reviewers from the same country per result
- Trust scoring, honeypots, time tracking, and rubber-stamp detection run continuously
- Admin override for extraordinary circumstances with full audit trail

---

## 15. Coordinated influence protection

Individual bad actors are caught by the trust score, honeypots, and rubber-stamp detection. But these mechanisms are not designed to detect organized influence campaigns - for example, a corporation paying 200 people to register, build trust over months, and then vote strategically on a specific topic. This section addresses that threat.

**Why this matters:**
It is well-documented that industries with financial interests in scientific outcomes - pharmaceuticals, energy, chemicals, tobacco, food - have historically funded biased research and influenced scientific consensus. OpenGen's community verification is only trustworthy if it cannot be captured by the same forces.

**Structural defense: the AI generates the research, not humans.**
In traditional science, a corporation can pay the researchers who write the study. In OpenGen, the Master Agent writes the research - and it runs on a private server that no external party can access or influence. The only attack surface is the review process. Every protection below targets that surface.

**Layer 1 - Coordination detection (automated):**
- Temporal clustering: if 20+ accounts that have never reviewed a domain all vote on the same result in that domain within a short window, the result is flagged and held for admin review
- Behavioral fingerprinting: anonymized profiles of review time, domain preferences, voting patterns, active hours - accounts with unusually similar profiles are flagged as potentially coordinated
- Vote correlation analysis: statistical likelihood that a voting pattern occurred independently - identical votes from moderate-trust accounts while high-trust domain experts are split triggers an anomaly flag
- Registration pattern detection: waves of new accounts progressing through onboarding at similar speeds trigger cohort analysis

**Layer 2 - Economically sensitive topic escalation (automatic):**
- Results tagged with domains where financial manipulation incentives are known (pharmaceutical safety, chemical toxicology, energy comparisons, food safety, pesticide research) are automatically escalated by one sensitivity tier
- The watchlist is maintained by admins and can be expanded
- Escalation is automatic and cannot be overridden by reviewers - only admins can de-escalate with documented justification

**Layer 3 - Source independence in the pipeline:**
- The Retriever Agent must find sources from at least 3 independent research groups for any claim
- Results supported only by industry-funded studies are flagged during Multi-Critic evaluation
- The pipeline explicitly states when evidence is contested or when significant dissenting research exists

**Layer 4 - Transparency as deterrent:**
- Every vote is permanently logged and publicly auditable
- If a coordinated campaign is discovered after the fact, every participating account can be identified and their historical votes re-evaluated
- High-profile verification events are flagged for post-verification audit
- The knowledge graph publicly displays when a result was verified under elevated scrutiny

**Layer 5 - External expert review (last resort):**
- For results where coordinated influence is suspected but not proven, admins can invoke an external expert panel - 3 to 5 independent subject-matter experts outside the OpenGen community
- External experts provide a binding assessment that overrides the community vote if necessary
- This firewall cannot be penetrated by fake reviewers because the experts are selected by admins, not drawn from the reviewer pool

**What this system cannot prevent:**
Honest disagreement is not manipulation. If qualified reviewers genuinely disagree, that is a scientific controversy handled through the "disputed" status and dissent protection (section 9). The coordination detection targets inauthentic behavior - accounts acting in concert - not legitimate differences of scientific opinion.

---

## 16. The pending principle

If the community is too small for the minimum reviewer threshold - or if not enough domain-matched reviewers are available - results remain in "pending" status indefinitely.

OpenGen does not lower its standards to fill the knowledge graph faster. An empty verified graph is more honest than a poorly verified one.

In the early phase, the graph may grow slowly. That is by design. The first verified result will have earned that status through a process more rigorous than any existing AI platform offers.

---

## Summary of all thresholds

| Parameter | Value |
|-----------|-------|
| Pipeline acceptance score | ≥ 0.98 |
| Max refinement rounds | 20 |
| Min reviewers (Tier 1) | 25 |
| Min reviewers (Tier 2) | 50 |
| Min reviewers (Tier 3) | 100 |
| Max reviewers per result | 250 |
| Reviewer scaling | 10% of active community |
| Approval (Tier 1) | 80% weighted |
| Approval (Tier 2) | 85% weighted |
| Approval (Tier 3) | 90% weighted |
| Disputed range | 60–80% |
| Trust start | 0.5 |
| Trust max | 1.0 |
| Trust correct vote | +0.01 |
| Trust incorrect vote | -0.05 |
| Trust honeypot fail | -0.15 |
| Trust inactivity decay | -0.02/month |
| Trust full-weight threshold | 0.7 |
| Trust silence threshold | 0.2 |
| Trust suspension threshold | 0.1 |
| Domain expert qualification | 20+ accurate reviews |
| Domain expert vote weight | 2× |
| Domain expertise fade | 6 months unused |
| Honeypot ratio | ~15% of queue |
| Onboarding test | 8/10 correct |
| Rubber-stamp flag | >85% all-yes |
| Fast-review flag | <30s on 500+ word results |
| Geographic cap | 60% from one country |
| Dissent protection trust | ≥ 0.85 + domain expert |
| Dissent hold duration | 72 hours |
| Appeal trust requirement | ≥ 0.7 |
| Flagging threshold (approved) | 3+ independent flaggers |
| Permanent re-verification | Never (appealable) |
| Stable re-verification | 24 months |
| Standard re-verification | 12 months |
| Fast-moving re-verification | 6 months |
| Auto-promotion to stable | 3 consecutive passes |
| Coordination temporal flag | 20+ accounts in new domain simultaneously |
| Sensitive topic escalation | +1 sensitivity tier (automatic) |
| Source independence minimum | 3 independent research groups |
| External expert panel size | 3–5 experts (admin-selected) |
