---
id: karimireddy-2020-learning
type: paper
title: Learning from History for Byzantine Robust Optimization
authors:
- Sai Praneeth Karimireddy
- Lie He
- Martin Jaggi
year: 2020
venue: ICML 2021 (arXiv preprint)
url: https://arxiv.org/abs/2012.10333
doi: null
arxiv: '2012.10333'
cite: 'Karimireddy, S. P., He, L., & Jaggi, M. (2020). Learning from History for Byzantine Robust Optimization. arXiv preprint arXiv:2012.10333.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Identifies two flaws in Byzantine-robust aggregation even with identically distributed data: some state-of-the-art rules fail to converge with no attackers present, and attackers who stay within per-round limits can couple their attacks across rounds and eventually cause divergence. The fix has two parts: a robust iterative clipping procedure (commonly called centered clipping) and worker momentum, which averages out time-coupled attacks. The authors present it as the first provably robust method for the standard stochastic optimisation setting. Code is linked at github.com/epfml/byzantine-robust-optimizer (not opened).

## Contribution

Shows that robustness must be judged over the whole history of rounds, not per round, and introduces iterative clipping with worker momentum.

## Key results

- Shown (per abstract): realistic failures of existing aggregators with no Byzantine workers.
- Proved (per abstract): attackers can couple attacks over time to cause divergence despite per-round influence bounds.
- Proved (per abstract): centered clipping plus worker momentum is provably robust in standard stochastic optimisation.

## Methods and models

Iterative clipping aggregator and worker-side momentum. Only the abstract was read; the choice of clipping centre and radius was not checked.

## Limitations and open questions

Abstract-level reading; constants and tolerated fraction not checked.

## Relevance to us

Q2 and Q3. A Sutton-style agent forks and merges repeatedly, so the relevant attacker is one that nudges the parent a little at every merge. This paper is the formal statement that per-merge bounds do not stop time-coupled drift, and that smoothing over history (worker momentum) and clipping does (inferred from the abstract's claim that momentum overcomes time-coupled attacks). A parent analogue: accept a returning sub-agent's update only as a bounded step from the parent's current memory. Related: [[karimireddy-2020-byzantine]], [[baruch-2019-little]].
