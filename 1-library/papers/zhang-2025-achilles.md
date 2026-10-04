---
id: zhang-2025-achilles
type: paper
title: Achilles Heel of Distributed Multi-Agent Systems
authors:
- Yiting Zhang
- Yijiang Li
- Tianwei Zhao
- Kaijie Zhu
- Haohan Wang
- Nuno Vasconcelos
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.07461
doi: null
arxiv: '2504.07461'
cite: Zhang, Y., Li, Y., Zhao, T., Zhu, K., Wang, H., & Vasconcelos, N. (2025). Achilles Heel of Distributed Multi-Agent Systems. arXiv preprint. arXiv:2504.07461.
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

Proposes the distributed multi-agent system (DMAS) setting, in which a central controller orchestrates heterogeneous third-party agents reached over APIs and cannot see inside them, and measures four trust problems in seven frameworks (AutoGen, Camel, AgentVerse, Multi-Agent Debate, Reflexion, ChatDev, CrewAI) on HumanEval, MMLU and MATH subsets and Trivia Creative Writing: free riding (a provider silently swaps in a weaker model), malicious agents (noise injection, jailbreak via "dark traits" system prompts, code that leaks files or kills processes), communication delay, and disconnection. Read: abstract, introduction, threat definitions, experimental settings and all results subsections.

## Contribution

A red-teaming checklist for the case where the orchestrator delegates to agents it does not control, with measurements showing that most current frameworks assume trusted, always-available sub-agents.

## Key results

- Free riding: swapping one role's GPT-4o for LLaMA-2-7B cut performance by over 60% in the less resilient frameworks; LLaMA-3.1-70B cost under 10%; AgentVerse and CrewAI were most resilient (max drops 40% and 34% on math) (measured, three repeats).
- Noise injection into one agent's responses cut coding Pass@1 by 90.5% in AgentVerse and 79.4% in MAD (where the targeted agent was higher in the hierarchy); others 30-45% (measured, Figure 11).
- Injected malicious code (privacy leak, process kill) executed in 100% of trials in Reflexion and AutoGen and about 41% in CrewAI (measured, Table 1).
- Jailbroken agent: 10.8% (AgentVerse, which assigns "ethical roles") to 43.1% (AutoGen, Camel) attack success (measured).
- Disconnection drove task completion to 0% in Camel in most settings; frameworks with retries recovered (measured).

## Methods and models

GPT-4o default backbone, temperature 0; LLaMA-3.1-70B, LLaMA-3-8B, LLaMA-2-7B as substitutes; down-sampled MMLU (175) and MATH (196).

## Limitations and open questions

Attacks are simple (prompted noise, injected code); single malicious agent; results reported mostly as figures; no defences beyond observations about retries and code verification.

## Relevance to us

Q2: the "free ride" result is the quiet version of a corrupted child: a returning part that is simply weaker or substituted, which degrades the merge without any injection. The noise-injection result that targeting a higher-level agent hurt most (MAD, 79%) matches [[he-2025-red]]'s position finding: corruption close to the aggregator matters more than corruption at a leaf. Q3: returned code was executed unverified in two frameworks in every trial, which is the most direct path from a corrupted child to the parent's environment. Related: [[triedman-2025-multi]], [[hagag-2026-architecture]].
