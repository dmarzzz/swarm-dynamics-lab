---
id: yu-2024-netsafe
type: paper
title: 'NetSafe: Exploring the Topological Safety of Multi-agent Networks'
authors:
- Miao Yu
- Shilong Wang
- Guibin Zhang
- Junyuan Mao
- Chenlong Yin
- Qijiong Liu
- Qingsong Wen
- Kun Wang
- Yang Wang
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2410.15686
doi: null
arxiv: '2410.15686'
cite: 'Yu, M., Wang, S., Zhang, G., Mao, J., Yin, C., Liu, Q., Wen, Q., Wang, K., & Wang, Y. (2024). NetSafe: Exploring the Topological Safety of Multi-agent Networks. arXiv preprint. arXiv:2410.15686.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies which communication topologies make LLM multi-agent networks resist malicious content injected by attacker nodes. A unified iterative message-passing scheme (RelCom) runs six-node networks (chain, cycle, binary tree, star, complete graph) for ten rounds, with one or more attacker nodes whose system prompt instructs them to spread misinformation, stereotypes, or harmful content. Measures per-agent and joint accuracy each round and compares them with static graph metrics. Read: abstract, introduction, setup, all observations of sections 4.2 to 4.4 and the conclusion; appendices not read. Several numbers in the HTML rendering were in stripped math markup and are not reproduced here.

## Contribution

An early systematic test of topology as a safety variable for LLM agent networks, with two named effects: "Agent Hallucination" (one node's false claim spreads and degrades the group) and "Aggregation Safety" (alignment of the benign models prevents bias and harmful content from spreading even when most nodes are attackers).

## Key results

- With one misinformation attacker among six GPT-4o-mini agents, joint accuracy declined over rounds and converged; chain topology was safest on fact and commonsense tasks and star the least safe (measured, Table 1).
- On math (GSMath), the complete graph went from 89.38 accuracy with no attackers to 44.25 with five attackers (measured, RQ3).
- Adding more normal nodes helped little and sometimes hurt; reducing attacker density mattered more (measured, RQ3).
- Bias attacks almost never succeeded (100% detection in 78% of cases, otherwise 99.8%); with five jailbroken nodes and one normal node, the normal node's moderation score stayed at 0.097 against 0.920 for attackers (measured).
- Their proposed static metric (attack path vulnerability) correlated with measured safety; network efficiency and eigenvector centrality did not (measured).

## Methods and models

GPT-4o-mini for agents (GPT-3.5-Turbo for the harmful-content experiment), three runs per setting, custom datasets: Fact (153 statements), CSQA subset (127), GSMath subset (113), bias statements, AdvBench prompts. Code at github.com/Ymm-cll/NetSafe.

## Limitations and open questions

Six-node graphs, a single model family, attackers defined only through system prompts, and a symmetric discussion protocol. "Safety" for misinformation is measured as task accuracy.

## Relevance to us

Q2: this is one of the few measurements of how outcome scales with the number of corrupted nodes. The result is not a sharp Byzantine threshold: degradation is gradual with attacker count, highly topology dependent, and alignment-violating content was blocked even at a 5 of 6 attacker majority while plausible misinformation was not. For fork-merge, the threat that survives majority rejection is subtle factual corruption, not overtly harmful content. Q1: greater average distance from attackers was safer, which supports routing a returning child's content through intermediaries rather than straight into the parent. Related: [[wang-2025-g-safeguard]] (same group, defence), [[he-2025-red]], [[liang-2025-dont]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2410.15686 . Read depth in this session: abstract.

Seed title, nine authors and 2024 initial date verified. The abstract distinguishes misinformation propagation from alignment-related aggregation safety. Consequently, overt harmful-output resistance and accurate factual aggregation must not be collapsed into one contagion metric. Later quarantine approaches [[wang-2025-g-safeguard]] and [[miao-2025-blindguard]] are separate detector interventions; [[niu-2026-reliability-contagion]] explains why density conclusions depend on communication-budget assumptions.
