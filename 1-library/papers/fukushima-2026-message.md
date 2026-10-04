---
id: fukushima-2026-message
type: paper
title: Message capacity and claim wording set the transition points of collective truth-finding in language-model networks
authors:
- Makoto Fukushima
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.19183
doi: null
arxiv: '2609.19183'
cite: Fukushima, M. (2026). Message capacity and claim wording set the transition points of collective truth-finding in language-model networks. arXiv preprint arXiv:2609.19183.
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03); 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Models bounded reading in LLM discussion networks with one number, the message capacity (how many of the others' messages an agent reads), and generates the communication network from it. Over 31,824 randomised queries, an 8B model's judgment of a claim reduces to a logistic function of a weighted sum of its inbox: a stochastic binary neuron with divisively normalised weights. From those weights and degree statistics, theory predicts that a wrong consensus becomes unreachable once agents read fewer than 6.4 of 31 sources on average. In 1,414 episodes this failed: the correct side won fewer than 50% of episodes from every start, and only 28-45% when 75% of agents started correct. The failure traces to a "field" (threshold) set by the claim's wording before any message is read; including each claim's own field, the same weights reproduce outcomes, and reversing wording shows the threshold follows what a claim asserts, not whether it is true. A second 8B model shows predicted claim-dependent bistability (15 of 16 conditions matched); at 70B the assertion bias is not detected.

## Contribution

Reduces an LLM agent to a fitted Ising/Hopfield-like unit (weights plus field) and predicts collective transition points from single-agent measurements: the most explicit "measure the microscopic rule, predict the macroscopic phase" result in this literature. Complements [[de-marzo-2024-ai]] (tanh majority force) and [[ricco-2026-consensus]] (O(n) spin framing).

## Key results

- Claimed: 8B agent response = logistic(weighted inbox sum + field), fitted from 31,824 queries.
- Claimed: predicted transition at mean message capacity < 6.4 of 31 failed until claim-specific fields were added.
- Claimed: correct side wins only 28-45% of episodes even with 75% correct starts.
- Claimed: bistability predictions matched 15 of 16 conditions on a second 8B model; field bias absent at 70B.

## Methods and models

Random communication networks generated from message capacity (31 sources), binary claim judgments by 8B models (one family plus a second family), 70B check; fitted stochastic-neuron update rules; mean-field style transition prediction.

## Limitations and open questions

Abstract-level read; single-author preprint; models are small (8B) and claims binary.

## Relevance to us

Shows how to calibrate an LLM agent's update rule and predict swarm-level bistability; a template for the hackathon's "micro-to-macro" experiments. Related: [[tanaka-2026-when]], [[de-nobili-2026-microscopic]].
