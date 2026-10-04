---
id: rakhsha-2020-policy
type: paper
title: 'Policy Teaching via Environment Poisoning: Training-time Adversarial Attacks against Reinforcement Learning'
authors:
- Amin Rakhsha
- Goran Radanovic
- Rati Devidze
- Xiaojin Zhu
- Adish Singla
year: 2020
venue: Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR 119
url: https://arxiv.org/abs/2003.12909
doi: null
arxiv: '2003.12909'
cite: 'Rakhsha, A., Radanovic, G., Devidze, R., Zhu, X., & Singla, A. (2020). Policy Teaching via Environment Poisoning: Training-time Adversarial Attacks against Reinforcement Learning. Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR 119. arXiv:2003.12909.'
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

Studies "environment poisoning": an attacker who can alter the rewards or the transition dynamics an RL agent experiences during training, with the goal of making a chosen target policy optimal for the agent while keeping the alteration small (stealthy). Victims maximise average reward in undiscounted infinite-horizon MDPs, either by planning in the poisoned MDP (offline) or by a regret-minimising learner such as UCRL receiving poisoned feedback (online). Gives optimisation formulations for reward and dynamics attacks, feasibility conditions and cost bounds. Read: abstract, introduction, problem setup, the statements of Theorems 1-4 and their discussion, the experimental findings and the conclusion; proofs not read.

## Contribution

Extends RL poisoning from rewards to transition dynamics and from planning to online learning, with guarantees that the attacker's average cost and mismatch shrink as the learner's regret is sublinear.

## Key results

- Proved: reward poisoning is always feasible for any target policy, with cost bounded in terms of the target's initial disadvantage (Theorem 1).
- Proved: dynamics poisoning is feasible under a sufficient condition on the target's disadvantage relative to neighbouring policies (Theorem 2) and can be infeasible otherwise.
- Proved: against an online learner with sublinear expected regret, the fraction of rounds where the agent deviates from the target and the attacker's average cost both decay at rates set by that regret (Theorems 3-4); a better learner is easier to steer in this sense.
- Experiments on a 4-state navigation MDP (10 runs): as the required margin grows, reward attacks stay feasible at rising cost while dynamics attacks became infeasible beyond a margin of 0.85; attacks free to change target and non-target states cost far less than attacks restricted to non-target states (measured).

## Methods and models

Convex programs for reward attacks; non-convex for dynamics with convex relaxations; UCRL learner in the online setting. Proceedings of the 37th ICML, PMLR 119 (per the PDF header).

## Limitations and open questions

Small tabular MDPs; white-box attacker who knows the true MDP; defensive strategies left for future work (stated).

## Relevance to us

Q3: a sub-agent sent to a domain the parent cannot observe directly is, from the parent's point of view, the environment for that domain. If it is corrupted it can report both altered rewards and altered dynamics, and this paper proves that reward alteration alone can teach any target policy, with dynamics alteration an additional, sometimes infeasible, lever. The online result says a parent that learns efficiently from returned experience converges to the attacker's target faster, not slower. Q2: the bounds are on the size of the distortion, not on how many sources are corrupted; nothing here gives a k-of-n guarantee, which has to come from aggregation as in [[fan-2021-fault-tolerant]]. Related: [[ma-2019-policy]], [[zhang-2020-adaptive]], [[espeholt-2018-impala]].
