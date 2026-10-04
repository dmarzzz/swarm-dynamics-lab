---
id: guo-2019-learning
type: paper
title: Learning Mean-Field Games
authors: [Xin Guo, Anran Hu, Renyuan Xu, Junzi Zhang]
year: 2019
venue: Advances in Neural Information Processing Systems 32 (NeurIPS 2019)
url: https://arxiv.org/abs/1901.09585
doi: null
arxiv: '1901.09585'
cite: Guo, X., Hu, A., Xu, R., & Zhang, J. (2019). Learning mean-field games. In Advances in Neural Information Processing Systems 32 (NeurIPS 2019). arXiv:1901.09585.
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null  # OpenAlex budget exhausted and Semantic Scholar returned 429 on 2026-10-03
code: []
---

## Summary

The paper sets up a "general mean-field game" (GMFG) in which each player's reward and transitions depend on the
population's joint state-action distribution, proves existence and uniqueness of its Nash equilibrium under
contraction assumptions, shows that naively alternating Q-learning with the classical MFG fixed-point iteration
is unstable, and proposes GMF-Q: Q-learning with a Boltzmann (softmax) policy and an epsilon-net projection of
the population distribution, with convergence and complexity analysis. On a repeated ad-auction game it
approximates the N-player equilibrium better than independent learners and mean-field Q-learning.

## Contribution

With [[yang-2018-mean]] it is one of the two standard entry points to "learning in mean-field games" from the
ML side; unlike Yang et al., it learns the population-level equilibrium of the MFG of [[lasry-2007-mean]] rather
than averaging neighbours' actions inside an N-agent critic. The survey [[lauriere-2022-learning]] covers the line
of work that follows.

## Key results

- Theorem 1: under Lipschitz assumptions with d1 d2 + d3 < 1, the GMFG has a unique Nash equilibrium (proved).
- The naive fixed-point plus Q-learning scheme fluctuates and does not converge (measured over 30 sample paths).
- Ad auction, |S| = |A| = 10, N = 20: final distance-to-NE metric C(pi) is 0.220 for independent learners, 0.101
  for MF-Q and 0.065 for GMF-Q (measured); as N grows, GMF-Q's error falls while IL and MF-Q errors rise.

## Methods and models

Discrete-time, finite state and action MFG; population flow L_t over S x A; Step A computes the best response by
Q-learning given L, Step B propagates the population under that policy, repeat to a fixed point. Smoothing comes
from the Boltzmann policy and from projecting L onto an epsilon-net. Experiments use a stylised repeated ad
auction with budget states. Metric C(pi) is a normalised exploitability.

## Limitations and open questions

Contraction assumptions are strong and hard to check; experiments are a single economics-flavoured game, not
spatial or swarm dynamics. No spatial interaction, so it says nothing directly about flocking.

## Relevance to us

The reference for "learn the equilibrium of a population" if a hackathon project wants a mean-field rather than
agent-based learned swarm. Connects [[yang-2018-mean]], [[lasry-2007-mean]] and [[lauriere-2022-learning]].
