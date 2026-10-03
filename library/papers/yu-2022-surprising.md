---
id: yu-2022-surprising
type: paper
title: The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games
authors:
- Chao Yu
- Akash Velu
- Eugene Vinitsky
- Jiaxuan Gao
- Yu Wang
- Alexandre Bayen
- Yi Wu
year: 2022
venue: Advances in Neural Information Processing Systems 35 (NeurIPS 2022), Datasets and Benchmarks Track
url: https://arxiv.org/abs/2103.01955
doi: null
arxiv: '2103.01955'
cite: Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Bayen, A., & Wu, Y. (2022). The surprising effectiveness of PPO in cooperative, multi-agent games. In Advances in Neural Information Processing Systems 35 (NeurIPS 2022), Datasets and Benchmarks Track. arXiv:2103.01955.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 2865 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

PPO is often assumed to be too sample-inefficient for multi-agent settings. The authors show that PPO-based multi-agent methods (MAPPO, IPPO) achieve strong results on the particle-world environments, SMAC, Google Research Football and Hanabi with minimal tuning and no domain-specific changes, often matching or beating off-policy methods in final return and sample efficiency, and they identify the implementation factors that matter.

## Contribution

Established simple parameter-shared PPO as the strong default baseline for cooperative MARL, which is what most recent swarm-RL work uses.

## Key results

- Competitive or superior returns and sample efficiency versus off-policy MARL on four testbeds (claimed in abstract).

## Methods and models

MAPPO with centralised value function, IPPO; ablations on value normalisation, input representation, clipping, batch size. Abstract-level read. Code: https://github.com/marlbenchmark/on-policy

## Limitations and open questions

Cooperative tasks only; agent counts small.

## Relevance to us

Pick this as the training algorithm for a hackathon learned-swarm baseline before trying anything exotic. Related: [[huttenrauch-2019-deep]] (TRPO), [[baker-2020-emergent]] (PPO at scale).
