---
id: scan-papers-fm-identity-hijack
type: task
title: 'Catalogue the papers: identity and goal hijack of agents'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-identity-hijack
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

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: question (3), at the level of published threat models and measured attacks.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/fm-identity-hijack, 2026-10-03.

Added 26 entries (25 papers, 1 blog), all tagged fork-merge-security. Read in full (4): [[perez-2022-ignore]], [[li-2024-measuring]], [[zerhoudi-2026-compaction]], [[nist-2025-technical]]; also read [[debenedetti-2024-agentdojo]] main text in full and appended notes there. Skim (13): [[zhan-2024-injecagent]], [[zhang-2024-agent]], [[wang-2024-badagent]], [[yang-2024-watch]], [[wang-2025-mcptox]], [[zhang-2024-psysafe]], [[nakash-2024-breaking]], [[chen-2025-persona]], [[liu-2026-safe]], [[xie-2026-what]], [[tan-2024-wolf]], [[ko-2026-attractor]], [[hu-2026-when]]. Abstract (9): [[radosevich-2025-mcp]], [[wang-2025-persona]], [[deng-2024-ai]] (review article), [[liu-2023-prompt]], [[tian-2023-evil]], [[sandhan-2026-persona]], [[abdelnabi-2024-get]], [[luz-de-araujo-2025-persistent]], [[li-2025-system]]. Notes appended to [[debenedetti-2024-agentdojo]], [[invariantlabs-2025-mcp]], [[wallace-2024-instruction]], [[yu-2025-survey]] (also added fork-merge-security to its topics).

Queries and APIs:
- Round 1, arXiv API title search on the lane seeds (Ignore Previous Prompt, Measuring and Controlling Instruction (In)Stability, InjecAgent, AgentDojo, Agent Security Bench, BadAgent, Watch Out for Your Agents, MCP Safety Audit, PsySafe, Evil Geniuses, Crescendo, AiTM, NetSafe, Wolf Within, Persona Vectors, Instruction Hierarchy, Breaking ReAct, HouYi, Emergent Misalignment): about 25 hits, 19 new to the library.
- Round 2, web search: NIST CAISI agent hijacking blog, Invariant Labs MCP tool poisoning, and "prompt injection persists through context compaction summarization" (neighbouring vocabulary: compaction, stored injection, compression boundary): 9 results, 4 new (NIST blog, Compaction Cliff, Relinking, XSPI), 2 already catalogued ([[gadgil-2026-bad]], [[dash-2026-untrusted]]).
- Round 3, Semantic Scholar /citations on Li et al. 2024 (67 citing papers), Perez and Ribeiro 2022 (1000 returned, filtered by title for persona, identity, hijack, drift, multi-agent, propagation, persistence, merge, delegation) and AgentDojo (150): about 110 titles screened, 6 added (attractor states, distributed backdoors, PHISH persona jailbreaking, task drift via activation deltas, persistent personas over 100 rounds, system prompt poisoning).
- Survey search: Deng et al. (ACM CSUR) added; Yu et al. 2025 survey already present.

Found but not added (deliberately left to other lanes or not opened in full): Red-Teaming LLM Multi-Agent Systems via Communication Attacks (2502.14847, AiTM; fm-contagion holds he-2025-red as a stub), NetSafe (2410.15686; fm-contagion holds yu-2024-netsafe), Multi-Agent Systems Execute Arbitrary Malicious Code (2503.12188; fm-contagion holds triedman-2025-multi), Crescendo multi-turn jailbreak (2404.01833, peripheral to identity), Measuring What Persists (2606.21843, single-author identity geometry, drift experiment retracted in abstract), ContextEcho persona drift in coding sessions (2605.24279), Drift No More? Context Equilibria (2510.07777), Sleeper Channels and Provenance Gates (2605.13471), From Prompt Injection to Persistent Control (2605.31042), GroupGuard collusive attacks (2603.13940), AgentDrift (2609.06972), Covert Assistance in MAS oversight (2609.39050), Stealthy Memory Injection in Persistent Personal Agents (2607.05189), MCPTox's sibling MCPXKIT (2508.12538), In-Context Representation Hijacking (2512.03771), Chain-of-Thought Hijacking (2510.26418).

Thin areas:
- No paper measures identity hijack across an actual fork and merge of one agent; the closest are cross-session persistence ([[xie-2026-what]]) and LLM-to-LLM propagation (other lanes).
- "Cutting others out" (a hijacked part excluding honest parts or monopolising the merge channel) has no direct measurement found; closest are asymmetric attractor influence ([[ko-2026-attractor]]) and AiTM (not added here).
- Survival of a hijacked persona through distillation or weight merging is covered by other lanes ([[de-muri-2025-pay]], [[cloud-2025-subliminal]], [[yuan-2025-merge]]); survival through summarisation is measured only indirectly (rules lost in [[zerhoudi-2026-compaction]], attacker instructions assembled in [[liu-2026-safe]]). Nobody has measured whether an injected identity is preferentially retained by compaction.
- No talks or X threads searched.
