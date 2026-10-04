---
id: ellis-2022-smacv2
type: paper
title: "SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning"
authors: [Benjamin Ellis, Jonathan Cook, Skander Moalla, Mikayel Samvelyan, Mingfei Sun, Anuj Mahajan, Jakob N. Foerster, Shimon Whiteson]
year: 2022
venue: Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track
url: https://arxiv.org/abs/2212.07489
doi: null
arxiv: '2212.07489'
cite: "Ellis, B., Cook, J., Moalla, S., Samvelyan, M., Sun, M., Mahajan, A., Foerster, J. N., & Whiteson, S. (2023). SMACv2: An improved benchmark for cooperative multi-agent reinforcement learning. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track. arXiv:2212.07489."
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null
code: [gh-oxwhirl-smacv2]
---

## Summary

The authors show that the popular SMAC benchmark [[samvelyan-2019-starcraft]] is close to deterministic: policies that see only the timestep and agent ID (open-loop) reach non-trivial and sometimes closed-loop-equal win rates on many maps, and a QMIX joint Q-function can be regressed from timestep alone with root-mean-squared error below 12% of the mean Q-value on all but one tested map. They then build SMACv2, which randomises team composition, start positions and true unit ranges each episode, and an Extended Partial Observability (EPO) variant, and show that open-loop policies fail on every SMACv2 map while QMIX, MAPPO, IPPO and QPLEX leave large headroom.

## Contribution

A diagnostic for benchmark saturation (train an observation-blind open-loop policy; if it wins, the benchmark does not test decentralised closed-loop control) and a procedurally generated replacement. It sits in a line of critiques of SMAC alongside [[gorsane-2022-towards]].

## Key results

- On SMAC, MAPPO open-loop matches closed-loop on bane_vs_bane, 3s5z, 1c3s5z and 2s3z; only four maps (3s5z_vs_3s6z, corridor, 6h_vs_8z, 5m_vs_6m) defeat open-loop learning entirely.
- Masking all features, QMIX Q-values are regressable from timestep with error about 5-10% of mean Q for most of an episode (peak about 15%).
- SMACv2: the open-loop baseline learns nothing on any map; asymmetric maps (10v11, 20v23) give low win rates for all algorithms; Zerg is hardest; difficulty does not grow with agent count.
- MAPPO and IPPO perform nearly identically, suggesting the centralised state adds little.
- EPO with p=0 (only first spotter sees an enemy) is much harder than p=1; p=0.5 behaves like p=0. Removing the available-actions mask was necessary for the p gap to appear.
- Experiments: 10M steps, 3 seeds per run; the feature-inferrability study used about 1500 GPU hours.

## Methods and models

Dec-POMDP framing. Open-loop policies condition on (timestep, agent ID) and still use central state in CTDE training. Q-regression: three trained QMIX "expert" policies per map generate 8192 train and 4096 validation episodes; a QMIX-shaped regression network predicts expert Q-values from masked inputs (masks over ally/enemy health, shield, position, last action). SMACv2 generation uses per-race unit-type probabilities and "reflect" or "surround" start-position distributions, configurable via a capability config.

## Limitations and open questions

Three seeds per configuration. Enemies remain the scripted built-in AI, so there is no adversarial learning opponent. Fixed hyperparameter budgets may favour QMIX's sample efficiency. The paper argues evaluating on multiple benchmarks should become the norm because single-benchmark evaluation is vulnerable to hidden environment flaws and community overfitting.

## Relevance to us

The open-loop test is a cheap sanity check we should run on any sim env we build or adopt: if a timestep-only policy does well, the env is not testing the coordination or detection we care about. Also argues for procedural generation of team composition and positions per episode. Code: [[gh-oxwhirl-smacv2]].
