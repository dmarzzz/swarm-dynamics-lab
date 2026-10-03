---
id: yao-2026-competition
type: paper
title: "Competition and Cooperation of LLM Agents in Games"
authors: ["Jiayi Yao", "Cong Chen", "Baosen Zhang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2604.00487
doi: null
arxiv: "2604.00487"
cite: "Yao, J., Chen, C., & Zhang, B. (2026). Competition and Cooperation of LLM Agents in Games. arXiv preprint arXiv:2604.00487."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Gemini Pro agents play a network resource allocation game and a linear Cournot game. With a myopic single-round prompt they converge to Nash; with a multi-round cumulative-utility prompt they move toward the Pareto front and cooperate, signalling intent by bidding below Nash. When the horizon is not stated, agents behave as if interpolating between myopic and long-term play. Chain-of-thought shows fairness reasoning drives cooperation; asymmetric agents reach a different Pareto point rather than the welfare optimum. The authors fit a deterministic state-space model of the agents' parameter updates, reverse-engineered from CoT.

## Contribution

An analytical model of how LLM agents move from Nash to cooperative outcomes across rounds, with prompt horizon as the switch.

## Key results

- Measured: multi-round prompts produce cooperation beyond Nash in both games (Figure 1, qualitative).
- Measured: explicit signalling in CoT (deliberately low bids to invite cooperation).

## Methods and models

Gemini Pro (model card cited is Gemini 3.1 Pro); the authors say other long-context models give similar results. Read: abstract, introduction, prompts and early results.

## Limitations and open questions

Single model family; small number of agents; results are prompt-dependent, as the authors state.

## Relevance to us

Whether firms are told the horizon is a first-order switch for collusion; the swarm factory should fix and report it (Lin et al. withheld the 50-round horizon in [[lin-2024-strategic]]). Related: [[deshpande-2026-strategic]].
