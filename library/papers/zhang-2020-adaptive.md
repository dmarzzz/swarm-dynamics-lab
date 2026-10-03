---
id: zhang-2020-adaptive
type: paper
title: Adaptive Reward-Poisoning Attacks against Reinforcement Learning
authors:
- Xuezhou Zhang
- Yuzhe Ma
- Adish Singla
- Xiaojin Zhu
year: 2020
venue: Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR 119
url: https://arxiv.org/abs/2003.12613
doi: null
arxiv: '2003.12613'
cite: Zhang, X., Ma, Y., Singla, A., & Zhu, X. (2020). Adaptive Reward-Poisoning Attacks against Reinforcement Learning. Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR 119. arXiv:2003.12613.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies online reward poisoning against a Q-learning agent: at every step an attacker may change the reward r_t to r_t + delta_t with |delta_t| bounded by Delta, aiming to make the agent follow a target policy on a chosen set of states. Derives thresholds in Delta below which any attack fails and above which an attack succeeds, separates non-adaptive attacks (delta depends only on the transition) from adaptive ones (delta depends on the agent's current Q-table), and uses deep RL (TD3) to learn attack policies. Read: abstract, introduction, problem setup, the infeasibility and feasibility theorems, the threshold illustration and the empirical section headings; proofs not read.

## Contribution

A certified-safety threshold for reward perturbation in RL, and a proof that adaptivity changes the attacker's cost from exponential to polynomial in the number of states.

## Key results

- Proved: Q-values under any bounded attack stay within Delta/(1-gamma) of the true Q* (Theorem 1), so if Delta is below a threshold set by the gap between optimal and target actions, the agent eventually learns the correct policy and is certified safe.
- Proved: above a threshold Delta_3 (proportional to the largest Q* gap the attacker must overturn on the target states), a non-adaptive attack forces the target policy for all but finitely many rounds (Theorem 4), but can need exponentially many steps.
- Proved: a Fast Adaptive Attack achieves the target in steps polynomial in |S| under mild conditions, O(e^k |S|^2 |A|) in grid worlds (Theorem 5, Corollary 6).
- Five-state chain example: Delta_1 = Delta_2 = 0.0069, Delta_3 = 0.132; over 1000 trials the non-adaptive attack needed about 9,430 non-target rounds in 10^5 steps against 30.4 for the adaptive attack (measured).
- Stated design implication: rewards whose optimal and suboptimal actions are separated by large gaps make poisoning harder.

## Methods and models

Tabular epsilon-greedy Q-learning victims on chain and grid MDPs; attack formulated as an MDP over (state, action, next state, reward, Q-table) and solved with TD3. Published in Proceedings of the 37th ICML, PMLR 119 (per the PDF header).

## Limitations and open questions

Tabular Q-learning victim; attacker observes the learner's Q-table in the adaptive case; per-step L-infinity budget rather than a fraction of corrupted sources.

## Relevance to us

Q2: this is a threshold, but on the size of reward distortion, not on the number of corrupted parts. For a learner that merges experience from copies, a corrupted copy whose reward edits stay below the action-gap threshold cannot change the final policy; above it, it can. Averaging returned rewards over n copies of the same state-action pairs divides a single corrupted copy's effective delta by roughly n (inference, not in the paper), which converts this magnitude threshold into a count threshold only where copies overlap. Q3: the adaptive result means a corrupted copy that can observe the parent's current values (for example because it was forked from them) is far more efficient than one that cannot. Related: [[ma-2019-policy]], [[rakhsha-2020-policy]], [[fan-2021-fault-tolerant]].
