---
id: ma-2019-policy
type: paper
title: Policy Poisoning in Batch Reinforcement Learning and Control
authors:
- Yuzhe Ma
- Xuezhou Zhang
- Wen Sun
- Xiaojin Zhu
year: 2019
venue: Advances in Neural Information Processing Systems 32 (NeurIPS 2019), per arXiv comment
url: https://arxiv.org/abs/1910.05821
doi: null
arxiv: '1910.05821'
cite: Ma, Y., Zhang, X., Sun, W., & Zhu, X. (2019). Policy Poisoning in Batch Reinforcement Learning and Control. Advances in Neural Information Processing Systems 32 (NeurIPS 2019), per arXiv comment. arXiv:1910.05821.
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

Formulates training-time "policy poisoning" against batch reinforcement learners: the attacker edits the rewards in a fixed data set of (state, action, reward, next state) tuples, as little as possible under a chosen norm, so that the learner, which estimates the MDP from the data and then plans optimally, ends up with a target policy chosen by the attacker. Instantiated as convex (or convex-surrogate) bilevel problems for a tabular certainty-equivalence learner and for a batch linear quadratic regulator. Read: abstract, introduction, related work, problem setup, the feasibility and cost results for the tabular case, all four experiments and the conclusion; the LQR derivation and proofs skimmed.

## Contribution

First characterisation of data poisoning against RL learners rather than test-time perturbation, with a feasibility guarantee and tight attack-cost bounds.

## Key results

- Proved: for the tabular learner, any target policy is reachable by changing rewards only (Proposition 1).
- Proved: the minimum attack cost is bounded above and below linearly in Delta(epsilon), the clean-data Q-value gap between the target and the optimal policy plus a margin; with the L-infinity norm the cost is O(Delta) independent of data size (Theorem 2, Corollary 3).
- Grid world: target policy installed with reward changes of L2 norm about 2.64 against a clean reward vector norm of 21.61; second grid world 0.38 against 11.09 (measured).
- LQR vehicle in a 4D state space: total change over 400 items of L2 norm 0.73 against 112.94 redirected the learned controller (measured).
- Reward shaping with a potential function cannot change the learned policy, which is what separates poisoning from shaping (demonstrated on the two-state MDP).

## Methods and models

Bilevel optimisation solved with CVXPY; tabular MDPs with maximum-likelihood transitions and least-squares rewards; LQR with estimated dynamics. Code at github.com/myzwisc/PPRL_NeurIPS19.

## Limitations and open questions

White-box attacker with full knowledge of the learner and the whole batch; model-based learners only; no defence studied; small illustrative environments.

## Relevance to us

Q3: in Sutton's scenario the returned object from a part is experience, and this paper shows that changing only the rewards in returned experience is sufficient to install any policy in a model-based learner, at a cost proportional to how far the target is from the optimum. A part that explored a domain nobody else visits controls the only data about that domain, so its reward edits are unconstrained by other parts' data there. Q2: the attack cost is a norm over the whole batch, so a k-of-n structure only helps if the merged data from honest parts overlaps the corrupted part's state-action pairs; disjoint exploration (the reason for forking) removes that overlap. Related: [[zhang-2020-adaptive]] (online version), [[rakhsha-2020-policy]] (environment poisoning), [[espeholt-2018-impala]] (architecture where actors return rewards).
