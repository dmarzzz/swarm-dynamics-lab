---
id: ma-2026-catching
type: paper
title: 'Catching the Infection Before It Spreads: Foresight-Guided Defense in Multi-Agent Systems'
authors:
- Yue Ma
- Ziyuan Yang
- Yi Zhang
year: 2026
venue: arXiv preprint (v3)
url: https://arxiv.org/abs/2605.01758
doi: null
arxiv: '2605.01758'
cite: 'Ma, Y., Yang, Z., & Zhang, Y. (2026). Catching the Infection Before It Spreads: Foresight-Guided Defense in Multi-Agent Systems. arXiv preprint (v3). arXiv:2605.01758.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Defends multimodal multi-agent systems against infectious jailbreak, the attack in which an adversarial image (a "virus adversarial example", VirAE) placed in one agent's retrieval album is preferentially retrieved and passed on in pairwise chats until nearly all agents are compromised. Instead of the earlier defence of spreading a more contagious "cure" image (Cowpox), each agent first simulates its own future chats under several personas and uses the diversity of the simulated retrievals and answers to diagnose whether it is infected. Recent infections are undone by rolling back the latest memory entry; older ones are located by Recursive Binary Diagnosis, which repeatedly halves the image album and re-runs the diagnosis to find and remove the contaminated entries. Read: abstract, introduction, threat model, theoretical analysis, method overview and main results.

## Contribution

A training-free, per-agent purification that restores agents to their prior state rather than replacing one dominant retrieved item (the virus) with another (the cure), and an argument that the cure-factor approach necessarily collapses interaction diversity.

## Key results

- Against the AgentSmith attack, maximum cumulative infection fell from over 95% (baselines) to at most 5.47%, and peak current infection to at most 3.12%, never reaching the 85% or 95% thresholds (measured, Table 1).
- Cowpox as a baseline still reached near-100% cumulative infection in several budgets while current infection hovered around 17-62% (measured, Table 1).
- Retrieval and semantic diversity metrics stayed close to benign baselines with FLP (measured).

## Methods and models

LLaVA-1.5-7B agents with CLIP-based retrieval (also InternVL2-8B, Qwen2VL-8B, InstructBLIP-7B), chat history length 3, album size 10, 4 initially infected agents, 64 chat rounds, following the AgentSmith setup. Discrete-time SIS-style infection model used for analysis.

## Limitations and open questions

Tailored to retrieval-driven image viruses with FIFO memories; the multi-persona simulation adds compute per round; code not yet released at the time of reading.

## Relevance to us

Q2 and merge hygiene: this is the most concrete measured "un-merge" technique in the contagion set. Rollback of the latest memory entries and binary search over memory to find the poisoned item map directly onto a parent checking what a returning child added before accepting it, and onto bisecting a merged memory after an infection is noticed. Q3: the theory section restates the spreading condition (infection rate beating recovery rate) used in [[gu-2024-agent]] and [[wu-2025-cowpox]]; a corrupted child is dangerous at merge if its content is retrieved preferentially, which is what adversarial optimisation buys. Related: [[zhou-2026-infa-guard]], [[papadopoulos-2026-mind]].
