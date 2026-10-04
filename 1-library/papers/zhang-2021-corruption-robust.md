---
id: zhang-2021-corruption-robust
type: paper
title: Corruption-Robust Offline Reinforcement Learning
authors:
- Xuezhou Zhang
- Yiding Chen
- Jerry Zhu
- Wen Sun
year: 2021
venue: arXiv preprint (v1, June 2021)
url: https://arxiv.org/abs/2106.06630
doi: null
arxiv: '2106.06630'
cite: Zhang, X., Chen, Y., Zhu, J., & Sun, W. (2021). Corruption-Robust Offline Reinforcement Learning. arXiv preprint (v1, June 2021). arXiv:2106.06630.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies offline RL when an adversary may arbitrarily modify an epsilon fraction of the (state, action, reward, next state) tuples in the data set. Proves a minimax lower bound showing that a worst-case optimality gap growing with the feature dimension d is unavoidable in linear MDPs, even when only rewards are corrupted, and gives robust least-squares value iteration algorithms (using robust regression oracles plus a pessimism bonus) that nearly match it with and without full data coverage. Also proves that without coverage the learner must know epsilon: adapting to an unknown corruption level is impossible. Read: abstract, introduction and contributions, the lower bound with its proof sketch and remarks, the coverage theorem remarks; the no-coverage analysis was skimmed and proofs were not read.

## Contribution

Shows that robustness to a corrupted fraction of experience is fundamentally harder in offline RL than in supervised learning or online RL, and explains why in terms of how the adversary can concentrate its budget.

## Key results

- Proved: no algorithm can guarantee better than an Omega(epsilon d H) optimality gap under epsilon-contamination in linear MDPs of dimension d and horizon H (Theorem 3.1). The construction: the adversary spends its whole budget on the least-sampled state-action pair, which receives at most a 1/d share of the data, raising its effective corruption to about epsilon d (proof sketch).
- Consequence stated by the authors: robustness is impossible in high-dimensional problems where d is at least 1/epsilon, unlike dimension-free robust mean estimation and robust supervised learning (Remark 3.1). The best-known online lower bound is only Omega(epsilon H) (Remark 3.2).
- With uniform coverage xi, robust LSVI gets a gap of order (sigma + H) H^2 epsilon / xi, which does not vanish with more data, and requires epsilon <= xi to be non-vacuous (Theorem 3.2, Remarks 3.4-3.5).
- Without coverage, knowing epsilon is necessary (impossibility result).

## Methods and models

Linear MDP model; Huber-style contamination of tuples; robust linear regression oracles inside least-squares value iteration; pessimism for partial coverage. Venue not stated on the arXiv page (v1, June 2021).

## Limitations and open questions

Worst-case theory; no experiments in the parts read; linear function approximation.

## Relevance to us

Q2, as a negative threshold result: in Sutton's scenario, the reason to fork is to cover state-action regions the parent rarely visits. The lower bound's proof uses exactly that: an adversary who controls even a small fraction of total experience can concentrate it on the least-covered region and dominate the learner's estimate there. So a k-of-n rule on the total amount of returned experience gives no protection for rarely visited domains; protection requires that each region be covered by several independent parts, with the tolerable corruption bounded by that region's coverage (epsilon <= xi). Q3: the strongest trajectory attack is a reward edit concentrated on rarely visited states, which is what a part exploring a unique domain is in a position to make. Related: [[chen-2022-byzantine-robust]], [[ma-2019-policy]], [[fan-2021-fault-tolerant]].
