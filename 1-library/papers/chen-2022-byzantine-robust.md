---
id: chen-2022-byzantine-robust
type: paper
title: Byzantine-Robust Online and Offline Distributed Reinforcement Learning
authors:
- Yiding Chen
- Xuezhou Zhang
- Kaiqing Zhang
- Mengdi Wang
- Xiaojin Zhu
year: 2022
venue: arXiv preprint (v1, under review at time of posting)
url: https://arxiv.org/abs/2206.00165
doi: null
arxiv: '2206.00165'
cite: Chen, Y., Zhang, X., Zhang, K., Wang, M., & Zhu, X. (2022). Byzantine-Robust Online and Offline Distributed Reinforcement Learning. arXiv preprint (v1, under review at time of posting). arXiv:2206.00165.
topics:
- fork-merge-security
- marl-emergence
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

A central server outsources exploration to m agents that each explore the same tabular episodic MDP (online setting) or that each hold logged data (offline setting) and send back experience, here sufficient statistics such as visit counts and empirical transition and reward means per (state, action, step). An alpha fraction of agents are Byzantine: they may collude and report arbitrary data in arbitrary amounts. The core tool is WEIGHTED-CLIQUE, a robust mean estimator for batches of unequal size that clips the largest 2 alpha m batch sizes, builds a confidence interval from each batch, and keeps the largest mutually consistent set. It is plugged into optimistic value iteration (BYZAN-UCBVI, online) and pessimistic value iteration (BYZAN-PEVI, offline). Read: abstract, introduction, related work, the estimator and its theorem with remarks, the online regret theorem and remarks, the offline theorem remarks and the conclusion; proofs not read.

## Contribution

Gives the first Byzantine-robust offline RL guarantee and a near-optimal online regret bound for the exact structure of Sutton's scenario: separate explorers reporting experience to a central learner, with a minority that lies, including about how much data it has.

## Key results

- Proved: the estimator's breakdown point is 1/2 (it works while fewer than half of the providers are corrupted and at least 2 alpha m + 1 report non-empty batches), which is optimal; with equal batch sizes its error matches the optimal rate of Yin et al. 2018 up to log factors (Theorem 3.2, Remarks 3.3-3.4).
- Proved: online regret O~((1 + alpha sqrt(m)) H^2 sqrt(S A m K)) for alpha up to about 1/3, sublinear in the number of episodes K despite Byzantine agents; when alpha is at most 1/sqrt(m) the leading term matches the clean minimax rate (Theorem 5.2, Remark 5.3).
- Proved: offline suboptimality vanishes as good agents collect more data under coverage conditions, for alpha < 1/3 (Theorem 6.5, Remark 6.6).
- Communication cost is logarithmic in K, and agents share only aggregated statistics (stated properties).

## Methods and models

Tabular episodic MDPs with S states, A actions, horizon H; sub-Gaussian reward noise; corrupted agents fully adversarial and colluding; no experiments in the parts read.

## Limitations and open questions

Tabular only; the authors list extension to function approximation and a lower bound for uneven batches as open (stated). Assumes the good agents all run the server's policy and report honestly about the same MDP, so heterogeneous explorers in different domains are not covered.

## Relevance to us

Q2: this is the clearest positive answer to the k-of-n question for Sutton's architecture. If parts explore the same environment and return experience statistics, a learner can tolerate up to a third of them being corrupted (half for the estimation step) and still learn near-optimally, with the corrupted fraction costing an extra alpha sqrt(m) factor in regret. The precondition is the important caveat for dmarz's scenario: the honest parts must sample the same distribution so that corrupted reports are statistically detectable. A part sent alone to a unique domain (the China example) has no peers sampling that domain, so its reports cannot be cross-checked and the threshold drops to 1 of 1. Q3: the result also bounds what the strongest trajectory attacker can do when overlap exists, in contrast to the unbounded influence in [[espeholt-2018-impala]] and [[horgan-2018-distributed]]. Related: [[fan-2021-fault-tolerant]], [[zhang-2021-corruption-robust]], [[ma-2019-policy]], [[zhang-2020-adaptive]].
