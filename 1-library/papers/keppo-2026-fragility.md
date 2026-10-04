---
id: keppo-2026-fragility
type: paper
title: "On the Fragility of AI Agent Collusion"
authors: ["Jussi Keppo", "Yuze Li", "Gerry Tsoukalas", "Nuo Yuan"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2603.20281
doi: null
arxiv: "2603.20281"
cite: "Keppo, J., Li, Y., Tsoukalas, G., & Yuan, N. (2026). On the Fragility of AI Agent Collusion. arXiv preprint arXiv:2603.20281."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A stylised repeated-pricing model predicts that heterogeneity in patience or data access shrinks the set of collusive equilibria; experiments with DeepSeek-R1-Distill-Qwen-32B pricing agents (over 2,000 compute hours, 1,000-period games, 10 runs per condition) test it. Measured: two patient agents converge to prices about 22% above static Nash; patience heterogeneity cuts the lift to 10% and asymmetric data access to 7%. Going from two to five sellers delays and weakens collusion: three can still collude (sometimes at higher prices), four is unstable, five never reaches sustained collusion within the horizon. An LLM against a Q-learning agent breaks collusion; a 32B versus 14B model pair does not, producing leader-follower dynamics that stabilise it.

## Contribution

Evidence that symmetric-agent LLM collusion results are fragile to realistic heterogeneity, with a theory that predicts which heterogeneities matter.

## Key results

- Measured: +22% price lift (homogeneous patient), +10% (patience heterogeneity), +7% (data asymmetry).
- Measured: collusion fails to emerge with five sellers.
- Measured: cross-algorithm heterogeneity breaks collusion; model-size heterogeneity does not.

## Methods and models

Locally run DeepSeek-R1-Distill-Qwen-32B (and a 14B variant); discount factor set in the prompt as the optimisation horizon. Read: abstract, introduction, setup and sections 4 to 5 summaries.

## Limitations and open questions

One model family; the authors explicitly do not claim to identify the cognitive mechanism. Bertrand-style pricing only, no quantities or production.

## Relevance to us

Sets expectations for firm counts in the swarm factory: collusion should weaken from 3 to 5 independent firms. A Sybil principal running several firms removes exactly the heterogeneity this paper finds protective, so Sybil firms should sustain collusion at firm counts where independents fail. That is a testable prediction. Contrast [[agrawal-2025-evaluating]] (model mixing did not help).
