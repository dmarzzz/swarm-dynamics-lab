---
id: espeholt-2018-impala
type: paper
title: 'IMPALA: Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures'
authors:
- Lasse Espeholt
- Hubert Soyer
- Remi Munos
- Karen Simonyan
- Volodymir Mnih
- Tom Ward
- Yotam Doron
- Vlad Firoiu
- Tim Harley
- Iain Dunning
- Shane Legg
- Koray Kavukcuoglu
year: 2018
venue: Proceedings of the 35th International Conference on Machine Learning (ICML 2018), PMLR 80
url: https://arxiv.org/abs/1802.01561
doi: null
arxiv: '1802.01561'
cite: 'Espeholt, L., Soyer, H., Munos, R., Simonyan, K., Mnih, V., Ward, T., Doron, Y., Firoiu, V., Harley, T., Dunning, I., et al. (2018). IMPALA: Scalable Distributed Deep-RL with Importance Weighted Actor-Learner Architectures. Proceedings of the 35th International Conference on Machine Learning (ICML 2018), PMLR 80. arXiv:1802.01561.'
topics:
- fork-merge-security
- marl-emergence
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

IMPALA is a distributed reinforcement learning architecture in which many actors run copies of the current policy in their own environments, then send whole trajectories (states, actions, rewards, and the behaviour policy's action probabilities) to a central learner, rather than gradients as in A3C. Because an actor's policy lags the learner's by several updates, learning is off-policy; the paper introduces V-trace, an actor-critic target that uses truncated importance weights (clipped at rho-bar and c-bar) to correct for the lag. Evaluated on DMLab-30 (30 3D tasks, one agent for all) and Atari-57. Read: abstract, introduction, architecture, the V-trace definition and its analysis in section 4, the off-policy correction comparison and the multi-task results; appendices not read.

## Contribution

Shows a single learner can absorb experience from thousands of decoupled actors stably, at about 250,000 frames per second (more than 30 times single-machine A3C), with positive transfer across tasks.

## Key results

- DMLab-30 mean capped human-normalised score: A3C deep 23.8%, IMPALA deep 46.5%, with population-based training 49.4% (measured, Table 3).
- Off-policy corrections compared on 5 DMLab tasks: with negligible lag, V-trace and 1-step importance sampling performed similarly; with 50% of each batch drawn from a replay buffer to widen the policy gap, V-trace was best on 4 of 5 tasks and the only method that consistently benefited from replay (measured, Table 2).
- Analytic property (stated in section 4): truncation level rho-bar sets the fixed point, which is the value of a policy between the behaviour policy and the target policy; c-bar only affects variance and convergence speed.

## Methods and models

Actors send unrolls of fixed length; learner trains on mini-batches on GPU; single or multiple synchronous learners. Code at github.com/deepmind/scalable_agent.

## Limitations and open questions

No adversarial or faulty actors are considered. The importance weights use the behaviour probabilities that the actor itself reports, so the correction trusts the actor's account of what policy it ran.

## Relevance to us

This is the architecture closest to Sutton's "copies send experience to a central learner" scenario ([[sutton-2025-father]]), and it is the mechanism the gap brief asks about. Q2: IMPALA has no Byzantine threshold at all; every actor's trajectories enter the batch. V-trace's truncation bounds how much any single off-policy step can be up-weighted (by rho-bar), which caps the per-sample leverage of a lagged or lying actor but does not filter it. An actor that reports false behaviour probabilities controls its own importance weights up to that cap (inference from the V-trace definition; not tested in the paper). Q3: in this architecture the returned object is a trajectory with rewards, so the relevant attack literature is reward and trajectory poisoning ([[ma-2019-policy]], [[zhang-2020-adaptive]], [[rakhsha-2020-policy]]), and the relevant defence is robust aggregation as in [[fan-2021-fault-tolerant]], which IMPALA does not use. Related: [[horgan-2018-distributed]], [[nair-2015-massively]], [[espeholt-2019-seed]].
