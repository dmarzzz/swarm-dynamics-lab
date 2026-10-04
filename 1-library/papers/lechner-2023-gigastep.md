---
id: lechner-2023-gigastep
type: paper
title: "Gigastep - One Billion Steps per Second Multi-agent Reinforcement Learning"
authors: [Mathias Lechner, Lianhao Yin, Tim Seyde, Tsun-Hsuan Wang, Wei Xiao, Ramin Hasani, Joshua Rountree, Daniela Rus]
year: 2023
venue: Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track
url: https://papers.nips.cc/paper_files/paper/2023/file/00ba06ba5c324efdfb068865ca44cf0b-Paper-Datasets_and_Benchmarks.pdf
doi: null
arxiv: null
cite: "Lechner, M., Yin, L., Seyde, T., Wang, T.-H., Xiao, W., Hasani, R., Rountree, J., & Rus, D. (2023). Gigastep - One billion steps per second multi-agent reinforcement learning. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track."
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: [gh-mlech26l-gigastep]
---

## Summary

Presents Gigastep, a fully vectorisable JAX multi-agent environment of two teams of agents with 3D dynamics, stochastic observations and stochastic intra-team communication, supporting cooperative and adversarial tasks, continuous or discrete actions, and RGB or feature observations. The abstract claims up to one billion environment steps per second on consumer-grade hardware; the throughput figure I looked at plots on the order of 0.4-1.4 million steps per second for closed-loop rollouts with a neural network policy on RTX 2080Ti, 3090, A6000 and A100, and I did not find in my skim how the billion figure is computed.

## Contribution

Positions itself against the trade-off between complex but compute-hungry MARL environments and fast but simplistic ones, arguing a JAX env with 3D dynamics and partial observability on one consumer GPU widens participation. Related-work section critiques Google Football (fixed rosters), Melting Pot (few agents, no GPU acceleration) and multi-agent MuJoCo (no task-level cooperation).

## Key results

- 288 built-in scenarios varying team sizes (e.g. 5, 10, 20 per team), agent heterogeneity, observability and action types (from the repo README).
- Rollout throughput measured with `jax.jit` + `jax.vmap` over batch size on four GPUs (figure 3); exact headline-to-figure mapping not checked.
- Baseline MARL experiments are reported (not read in detail).

## Methods and models

JAX, XLA-compiled step and reset functions vectorised over environments; per-agent dones; team-level stochastic communication of neighbourhood observations.

## Limitations and open questions

Repository has had no updates since December 2023 despite an "updates coming soon" note. The billion-steps claim should be read as a best-case aggregate until reproduced.

## Relevance to us

A ready JAX template for team-vs-team swarms with lossy communication; good starting point if we want GPU-speed adversarial swarm experiments without writing physics. Code: [[gh-mlech26l-gigastep]]. Compare [[gh-proroklab-vectorizedmultiagentsimulator]].
