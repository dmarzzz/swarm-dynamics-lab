---
id: yemini-2022-resilient
type: paper
title: "Resilient Distributed Optimization for Multi-Agent Cyberphysical Systems"
authors: ["Michal Yemini", "Angelia Nedić", "Andrea J. Goldsmith", "Stephanie Gil"]
year: 2022
venue: "arXiv preprint (later IEEE Transactions on Automatic Control)"
url: https://arxiv.org/abs/2212.02459
doi: null
arxiv: "2212.02459"
cite: "Yemini, M., Nedić, A., Goldsmith, A. J., & Gil, S. (2022). Resilient Distributed Optimization for Multi-Agent Cyberphysical Systems. arXiv:2212.02459."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "27 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Distributed optimisation where each legitimate agent's iterates are pulled both by possibly malicious neighbours and by its own objective. With stochastic inter-agent trust values available, the authors recover convergence to the true global optimum in mean and almost surely, give expected-rate bounds on squared distance to the optimum, and show numerically that this holds even when malicious agents are the majority, where existing methods fail.

## Contribution

Extends trust-based resilience from consensus [[yemini-2021-characterizing]] to distributed optimisation.

## Key results

- Convergence to the true optimum in mean and almost surely despite malicious agents (abstract).
- Numerical results with a malicious majority.

## Methods and models

Trust-weighted distributed gradient methods. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Same dependence on an unforgeable trust signal.

## Relevance to us

Relevant if a swarm of agents jointly optimises (for example a shared policy or price); with a trust side channel the malicious-majority regime is not hopeless.
