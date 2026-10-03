---
id: zhang-2021-robust
type: paper
title: Robust Policy Gradient against Strong Data Corruption
authors:
- Xuezhou Zhang
- Yiding Chen
- Xiaojin Zhu
- Wen Sun
year: 2021
venue: arXiv preprint (v3, June 2021)
url: https://arxiv.org/abs/2102.05800
doi: null
arxiv: '2102.05800'
cite: Zhang, X., Chen, Y., Zhu, X., & Sun, W. (2021). Robust Policy Gradient against Strong Data Corruption. arXiv preprint (v3, June 2021). arXiv:2102.05800.
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

Studies policy-gradient RL when an adaptive adversary may arbitrarily corrupt both rewards and transitions at every step of up to an epsilon fraction of the learning episodes. Proves that no algorithm can do better than O(epsilon)-optimal under this model, that natural policy gradient is already robust when reward corruption is bounded (O(sqrt(epsilon))), and proposes Filtered Policy Gradient (FPG), which replaces the regression step inside natural policy gradient with a robust regression (SEVER) that filters outlier samples, and tolerates unbounded reward corruption (O(epsilon^(1/4))-optimal). A neural version built on TRPO is tested on six MuJoCo tasks. Read: abstract, introduction, the attack model and main theorem statements, the experiment section and figure captions; proofs not read.

## Contribution

First algorithm with a meaningful learning guarantee when a constant fraction of episodes is adversarially corrupted, including unbounded rewards, and an empirical demonstration on continuous control.

## Key results

- Proved: lower bound, no better than O(epsilon)-optimal under the epsilon-fraction episode corruption model.
- Proved: NPG is O(sqrt(epsilon))-optimal under bounded reward corruption; FPG is O(epsilon^(1/4))-optimal under unbounded corruption.
- MuJoCo (6 tasks, 3 seeds), epsilon = 0.01 of episodes corrupted by flipping and scaling rewards by delta, with delta tuned per algorithm from 1 to 64: vanilla TRPO failed completely under the attack (delta = 64 chosen in all tasks), while FPG matched TRPO's clean performance with or without attack (measured, Figure 1).
- HalfCheetah under delta = 100: TRPO learned to run backward, FPG still ran forward (observed, Figure 2).

## Methods and models

Linear Q-function, finite actions and exploratory start distribution for the theory; SEVER robust regression for filtering; TRPO-based FPG for experiments. Code at github.com/zhangxz1123/FilteredPolicyGradient. Venue not stated on the arXiv page (v3, June 2021).

## Limitations and open questions

Theory requires assumptions that do not hold in MuJoCo; the attack is a simple reward-flip strategy rather than an optimised one (stated); the corruption fraction is per episode, not per source.

## Relevance to us

Q3 and Q2 together: one corrupted episode in a hundred was enough to make an unprotected policy-gradient learner learn the opposite behaviour, which is a measured answer to whether a returned trajectory can steer the parent: yes, strongly, at a 1% fraction, if rewards are unbounded and unfiltered. With robust filtering of each update, the same fraction became harmless in these tasks, and the guarantee degrades smoothly with epsilon rather than having a sharp k-of-n cutoff. For Sutton-style continual learners fed by copies, this argues for filtering at the update step (as in [[fan-2021-fault-tolerant]]) rather than trusting per-copy reports. Related: [[zhang-2021-corruption-robust]], [[chen-2022-byzantine-robust]], [[zhang-2020-adaptive]].
