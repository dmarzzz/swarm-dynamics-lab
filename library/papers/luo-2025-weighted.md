---
id: luo-2025-weighted
type: paper
title: A Weighted Byzantine Fault Tolerance Consensus Driven Trusted Multiple Large Language Models Network
authors:
- Haoxiang Luo
- Gang Sun
- Yinqiu Liu
- Dongcheng Zhao
- Dusit Niyato
- Hongfang Yu
- Schahram Dustdar
year: 2025
venue: IEEE Transactions on Cognitive Communications and Networking (per Semantic Scholar venue field)
url: https://arxiv.org/abs/2505.05103
doi: null
arxiv: '2505.05103'
cite: 'Luo, H., Sun, G., Liu, Y., Zhao, D., Niyato, D., Yu, H., & Dustdar, S. (2025). A Weighted Byzantine Fault Tolerance Consensus Driven Trusted Multiple Large Language Models Network. arXiv preprint arXiv:2505.05103.'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 35 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes Trusted MultiLLMN, a multi-LLM network in which models answer user queries jointly under a Weighted Byzantine Fault Tolerance (WBFT) blockchain consensus. Voting weights are assigned adaptively from each LLM's response quality and trustworthiness, so reliable models gain influence and malicious ones lose it. Simulations, including under wireless network conditions, show better consensus security and efficiency than classical and modern consensus mechanisms and higher-quality responses than single LLMs or unweighted multi-LLM networks.

## Contribution

Replaces one-agent-one-vote with reputation-weighted voting in an LLM consensus protocol (HotStuff-like two-phase commit, per the description in [[jo-2025-byzantine]]).

## Key results

- Reported in abstract: WBFT improves consensus security and efficiency over baselines; numbers not checked.

## Methods and models

Weighted BFT with adaptive weights, simulated wireless setting.

## Limitations and open questions

Abstract only. Reputation-weighted votes move the Sybil problem into the weight-update rule: an attacker who builds weight on easy queries can spend it on a target query, the laundering pattern measured in [[xia-2026-when]].

## Relevance to us

A reputation-weighted alternative to identity-counting quorums for agent swarms; useful as a target for laundering and whitewashing attacks. See also [[chen-2024-blockagents]].
