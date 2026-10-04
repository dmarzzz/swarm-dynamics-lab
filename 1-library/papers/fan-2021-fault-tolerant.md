---
id: fan-2021-fault-tolerant
type: paper
title: Fault-Tolerant Federated Reinforcement Learning with Theoretical Guarantee
authors:
- Flint Xiaofeng Fan
- Yining Ma
- Zhongxiang Dai
- Wei Jing
- Cheston Tan
- Bryan Kian Hsiang Low
year: 2021
venue: Advances in Neural Information Processing Systems 34 (NeurIPS 2021)
url: https://arxiv.org/abs/2110.14074
doi: null
arxiv: '2110.14074'
cite: Fan, F. X., Ma, Y., Dai, Z., Jing, W., Tan, C., & Low, B. K. H. (2021). Fault-Tolerant Federated Reinforcement Learning with Theoretical Guarantee. Advances in Neural Information Processing Systems 34 (NeurIPS 2021). arXiv:2110.14074.
topics:
- fork-merge-security
- marl-emergence
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Federated reinforcement learning in which K agents each sample trajectories in their own copy of the MDP with the server's current policy and return only policy gradients; a trusted server aggregates them and updates the policy with a variance-reduced (SCSG-style) inner loop using importance weights to correct for off-policy samples. An alpha fraction (alpha < 0.5) of agents may be Byzantine in any round and send arbitrary vectors. The aggregator, FedPG-BR, keeps only gradients within a concentration radius of a "mean of medians" vector, using the bounded-variance assumption on the gradient estimator. Read: abstract, introduction, problem setup, technical challenges, algorithm and filter, main theorem and corollary, experiments and conclusion; proofs in the appendix not read.

## Contribution

First federated RL method with both a convergence guarantee and Byzantine tolerance, with an explicit cost for the corrupted fraction.

## Key results

- Proved: good agents are never filtered; any Byzantine gradient that passes is within 3 sigma of the true gradient; expected trajectories per agent to reach an epsilon-stationary point is O(1/(epsilon^(5/3) K^(2/3)) + alpha^(4/3)/epsilon^(5/3)), so corrupted agents add only an additive term and the benefit of federation survives for alpha < 0.5 (Theorem 6, Corollary 7).
- HalfCheetah, CartPole, LunarLander with K = 10 and 3 Byzantine agents: random-action agents made federated GPOMDP and SVRPG unable to learn at all, and all three failure types made them worse than a single agent; FedPG-BR with 3 Byzantine agents performed comparably to 10 good agents (measured, Figure 3, 10 runs).
- A colluding attacker who knows the filter and sends mean + 3 sigma (the largest deviation the filter admits) only marginally slowed FedPG-BR, which still beat a single agent (measured, Figure 4).

## Methods and models

REINFORCE or GPOMDP gradient estimators; importance weights p(tau|theta_0)/p(tau|theta_n); filtering rules R1 (high-probability concentration radius) and R2 (2 sigma around the mean of medians). Failures simulated: random noise vectors, random actions (corrupted trajectories), sign flipping (x -2.5). Code at github.com/flint-xf-fan/Byzantine-Federeated-RL.

## Limitations and open questions

Requires a trusted server, homogeneous agents, a known or estimable variance bound sigma, and variance-reduced policy gradient (stated). Workers return gradients, not trajectories, so the filter operates on gradient vectors.

## Relevance to us

Q2: the cleanest positive threshold result on the RL side of Sutton's scenario. When copies of a learner explore separately and return policy gradients to a trusted central learner, fewer than half corrupted copies cannot stop learning, and their damage is bounded by an additive alpha^(4/3) term; a returning copy that passes the filter can shift the update by at most 3 sigma. Q3: the "random action" failure is the closest to a corrupted explorer returning trajectories from a policy other than the one it claims; unfiltered, it alone made learning impossible. The bound depends on returned updates being gradients with bounded variance; it says nothing about returned text memories or model edits. Related: [[lee-2026-fully]], [[alistarh-2018-byzantine]], [[espeholt-2018-impala]], [[zhang-2020-adaptive]].
