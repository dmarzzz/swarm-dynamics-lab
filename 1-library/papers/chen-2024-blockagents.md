---
id: chen-2024-blockagents
type: paper
title: 'BlockAgents: Towards Byzantine-Robust LLM-Based Multi-Agent Coordination via Blockchain'
authors:
- Bei Chen
- Gaolei Li
- Xi Lin
- Zheng Wang
- Jianhua Li
year: 2024
venue: Proceedings of the ACM Turing Award Celebration Conference - China 2024 (ACM-TURC '24)
url: https://www.semanticscholar.org/paper/e35391872b0170d8f845b9aff3440efbefd0bb02
doi: 10.1145/3674399.3674445
arxiv: null
cite: 'Chen, B., Li, G., Lin, X., Wang, Z., & Li, J. (2024). BlockAgents: Towards Byzantine-Robust LLM-Based Multi-Agent Coordination via Blockchain. In Proceedings of the ACM Turing Award Celebration Conference - China 2024 (ACM-TURC 24), 187-192. https://doi.org/10.1145/3674399.3674445'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 49 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Integrates a blockchain into LLM-based cooperative multi-agent systems to resist Byzantine agents, motivated by deceptive agents inheriting LLM biases and by collusion among multiple malicious agents. The workflow covers role assignment, proposal, evaluation and decision. A proof-of-thought (PoT) consensus combines stake-based miner designation with multi-round debate-style voting so the agent contributing most to group reasoning gains accounting rights; evaluators score proposals with a multi-metric prompt. On three datasets the paper reports that poisoning attacks reduce accuracy by less than 3% and backdoor attack success stays below 5%.

## Contribution

One of the first designs to treat LLM agent collaboration as a Byzantine consensus problem with stake-weighted roles.

## Key results

- Reported in abstract: poisoning interference on accuracy below 3%; backdoor success below 5% (datasets not checked).

## Methods and models

Blockchain ledger, stake-based miner selection, proof-of-thought consensus, debate-style majority voting, prompt-based multi-metric evaluation. Metadata and abstract read via the Crossref and Semantic Scholar APIs; the ACM page was not reachable (HTTP 403).

## Limitations and open questions

Abstract only. [[jo-2025-byzantine]] criticises the fixed-leader debate design: consecutive Byzantine leaders inflate latency, and majority voting can finalise an inferior leader proposal. Stake is the only Sybil bound mentioned.

## Relevance to us

Represents the crypto-economic route to Sybil resistance in agent collectives (stake gates who proposes and validates). Compare [[luo-2025-weighted]] (reputation-weighted BFT), [[jo-2025-byzantine]] (leaderless geometric median), [[hu-2025-inter-agent]] (stake as a trust primitive) and the robot-swarm analogue [[strobel-2023-robot]].
