---
id: scan-papers-fm-memory-injection
type: task
title: 'Catalogue the papers: memory poisoning and persistent prompt injection in agents'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-memory-injection
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
claimed_at: 2026-10-03T18:11Z
updated: 2026-10-03T18:11Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: agent memory/RAG poisoning and persistent injection.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Filled by dmarz/fm-memory-injection, 2026-10-03.

Added 35 entries tagged fork-merge-security: 28 papers, 3 blogs, 4 code repos. Appended "Notes from dmarz/fm-memory-injection" to 5 existing entries (gu-2024-agent, cohen-2024-here, ju-2024-flooding, lee-2024-prompt, park-2023-generative) and added the fork-merge-security slug to the four that lacked it. Read in full: dong-2025-memory (MINJA), xiang-2024-certifiably (RobustRAG), sharma-2026-smsr, gu-2024-agent (notes only, since the entry belongs to another agent). Skimmed: greshake-2023-not, louck-2026-securing, wei-2025-amemguard, xiong-2026-maple, gadgil-2026-bad, embracethered-2024-spyware, both OWASP lists. The rest at abstract level.

Review articles found and catalogued: lin-2026-survey (long-term memory security, EMNLP 2026), he-2024-emerged (ACM CSUR), shahriar-2025-survey (agentic security, 260+ papers), torra-2026-memory (position and review). Seen in citation lists but not opened, so not catalogued: arXiv 2606.04990 (survey of evidence tracing and execution provenance), 2606.10749 (secure LLM agents survey), 2602.19555 (SoK on agentic supply chain runtime).

Search rounds (results / new-to-library added):
1. arXiv API id_list for the 18 seed papers: 18 / 14 (arXiv export API then rate-limited and failed for later batches; switched to arxiv.org/abs pages).
2. Semantic Scholar search "memory poisoning defense LLM agents": 12 / 6.
3. S2 "persistent prompt injection agent memory": 12 / 5.
4. S2 "memory poisoning multi-agent shared memory LLM": 12 / 2.
5. S2 "survey security LLM agent memory": 12 / 1.
6. Forward citations of MINJA (S2 /citations, 139 citing papers, filtered on memory/defence/multi-agent title words to 45): 45 / 6.
7. Forward citations of AgentPoison: failed (S2 returned malformed JSON).
8. Web: Embrace The Red SpAIware post, OWASP LLM Top 10 2025 page, OWASP Agentic Top 10 landing page plus promptfoo summary for the item list: 3 / 3.
9. GitHub API metadata and READMEs for 6 repos: 6 / 4 (Jacobhhy/Agent-Memory-Poisoning redirected, not catalogued; sail-sg/Agent-Smith not catalogued, as its paper entry belongs to another agent).
10. S2 "experience sharing poisoning self-evolving agents" (vocabulary of the self-evolving-agent community): 15 / 3.
Several further S2 queries ("A-MemGuard memory defense", "self-replicating prompt multi-agent propagation", "Byzantine robust LLM multi-agent", "memory merge sub-agent poisoning parent agent", "memory consolidation poisoning", "shared memory contamination provenance") hit S2 rate limits, and two OpenAlex searches returned errors. These are untried rather than empty.

Found but not added (opened abstract or seen in lists, judged lower priority or out of lane): MemLineage 2605.14421, MemMorph 2605.26154, Memory control-flow attacks 2603.15125, No Attacker Needed cross-user contamination 2604.01350 (abstract read), Topology Matters memory leakage 2512.04668 (abstract read), TRUSTMEM 2606.25161 (abstract read), Collaborative Memory 2505.18279 (abstract read), SuperLocalMemory 2603.02240 (abstract read), Price of Safety 2609.22818 (abstract read), belief-based memory 2606.22030 (abstract read), MEXTRA 2502.13172, BadRAG 2406.00083, A-MEM 2502.12110, Agent Security Bench 2410.02644, AgentDojo 2406.13352, design patterns 2506.08837, Sleeper Agents 2401.05566, InjecMEM 2608.23471, Sleeper Channels 2605.13471, MAPLE-adjacent MemSecBench 2607.27080, Revoked but Still Authoritative 2609.08258.

What is thin: (a) No paper measures the specific attack dmarz describes, an injection that overwrites a sub-agent's identity or core memory so it adopts another principal and excludes others. The closest are goal hijack plus persistence (greshake, gadgil, SpAIware) and infectious spread (gu, cohen, lee). (b) Q1 (hiding which sub-agent is reintegrated) has almost no memory-side literature. Only randomised ablation (SMSR) and private retrieval (torra) touch it, and both by inference. (c) Q2 has three concrete threshold constructions (RobustRAG isolate-then-aggregate, SMSR hypergeometric certificate, TMA-NM k-independent-principal corroboration), none evaluated in a fork-merge topology. (d) Weight-level merging (model soups, task arithmetic, federated aggregation) is out of this lane and should be covered by another.
