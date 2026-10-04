---
id: scan-papers-fm-ai-control
type: task
title: 'Catalogue the papers: AI control, sub-agent delegation and self-replication'
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-ai-control
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: AI safety framings and defensive design patterns for delegating to and reintegrating untrusted sub-agents.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Filled by dmarz/fm-ai-control, 2026-10-03.

**Result.** 29 new entries tagged fork-merge-security (23 papers; 3 blogs: willison, metr, anthropic; 3 code: camel, fides, control-arena), plus `## Notes from dmarz/fm-ai-control` appended to 4 existing entries (hammond-2025-multi, chan-2024-visibility, debenedetti-2025-defeating, hubinger-2024-sleeper). Read in full: greenblatt-2023-ai, costa-2025-securing, makins-2026-multi, jarviniemi-2025-subversion, plus debenedetti-2025-defeating (CaMeL, read in full; notes appended because fm-memory-injection created the entry first) and triedman-2025-multi (read in full; entry owned by fm-contagion). Review articles found and catalogued or annotated: hammond-2025-multi (annotated); de-witt-2025-open already in library (not reopened). `lab.py check` 0 errors; `lab.py verify` 23 papers, 0 problems.

**Rounds (results / new to library).**
1. Seed list, arXiv abs+HTML for 16 seed ids (export API returned 429; used arxiv.org/abs and /html directly) and Semantic Scholar batch metadata: 16 / 13.
2. WebSearch "AI control protocol untrusted subagents delegation orchestrator collusion": 9 / 6 (makins, kutasov, gardner-challis, jarviniemi, tomasev, frank).
3. WebSearch "untrusted monitoring collusion instances same model control evaluation": 9 / 2 new beyond round 2.
4. Forward citations of greenblatt-2023-ai via Semantic Scholar /citations (first 200 of 239): 200 results, 25 matched keyword filter, 6 added (hills, qinqin, radev, lip, plus kutasov and jarviniemi already found); 2 already in library (de-witt-2025-open, rippin-2026-tool).
5. Backward references read inside full texts of CaMeL, Fides and Makins (Willison dual LLM, f-secure, AgentDojo, instruction hierarchy, Abdelnabi firewalls): about 15 / 5.
6. WebSearch "sub-agent results merged back into orchestrator memory poisoning contamination": 10 / 1 added (wang-2026-state); 1 already in library (louck-2026-securing); rest left to the memory-injection lane.
7. WebSearch "scalable oversight hierarchical agents compromised subagent trust propagation": 9 / 2 added (safin-2026-trust, dantuluri-2026-delegation).
8. GitHub API for code repos of catalogued papers (camel-prompt-injection, microsoft/fides, control-arena, rgreenblatt/control-evaluations): 4 / 3 added.
Saturation: rounds 6 and 7 surfaced mostly memory-poisoning work owned by another lane; new AI-control items in the last two rounds were 3 of 19.

**APIs.** arxiv.org abs/html (export API rate-limited), Semantic Scholar graph batch and /citations (search endpoint rate-limited after first calls), GitHub API via gh, WebSearch, WebFetch for blogs. OpenAlex daily budget exhausted on this IP.

**Found but not added.** Tomasev et al. 2026 "Intelligent AI Delegation" (2602.11865, abstract read; delegation framework, no security results); Frank 2026 "Counter-Swarm Doctrine" (2609.06140, abstract read; cross-execution coordination episodes and state quarantine, position paper, good fit for swarm-detection lane); Phuong et al. 2026 "GDM AI Control Roadmap" (2607.13087, metadata only); Shlegeris, Alignment Forum "How to prevent collusion when using untrusted models to monitor each other" (search hit, not opened); forward citations not opened: "Codetta: High-Capacity, Keyless, and Undetectable Multi-Agent Collusion" (2609.28900), "Covert Assistance: Helpful LLM Agents Evade Oversight in Multi-Agent Systems" (2609.39050), "Detecting Multi-Agent Collusion Through Multi-Agent Interpretability" (2604.01151), "TraceGuard" (2604.03968), "Certified Speculative Execution for Untrusted AI Agents" (2606.31023), "From Admission to Invariants: Measuring Deviation in Delegated Agent Systems" (2604.17517); memory-poisoning hits (MemPoison 2607.14651, MemAudit 2605.23723) left to fm-memory-injection; Hines et al. spotlighting (2403.14720) and IsolateGPT (2403.04960) metadata fetched but not catalogued.

**Thin.** (1) Q1 hiding: no AI-control or agent-security paper studies hiding which sub-agent will be reintegrated; the nearest measured levers are honeypots indistinguishable from real returns (greenblatt, gardner-challis) and randomised resampling (bhatt, kutasov, which shows the protection collapses once the attacker knows the schedule). (2) Q2 thresholds: no paper defines a k-of-n merge rule for LLM agents. Measured evidence points the other way: per-part checks fail against coordinated parts (makins), forks of one model share failure modes (self-recognition, focal points), and IFC labels are 1-of-n by construction (costa). Robust aggregation for merges has to come from the federated-learning and BFT lanes. (3) Q3 attack: strongest measured shapes are laundering through sub-agent metadata (triedman), splitting a payload across parts (makins, hills), and summaries that pass filters but carry influence (wang). No paper measures an attack that rewrites a sub-agent's identity and then corrupts its parent at merge time end to end.
