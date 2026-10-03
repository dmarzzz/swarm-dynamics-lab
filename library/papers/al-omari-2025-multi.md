---
id: al-omari-2025-multi
type: paper
title: "Multi-Agent Craftax: Benchmarking Open-Ended Multi-Agent Reinforcement Learning at the Hyperscale"
authors: [Bassel Al Omari, Michael Matthews, Alexander Rutherford, Jakob Nicolaus Foerster]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.04904
doi: null
arxiv: '2511.04904'
cite: "Al Omari, B., Matthews, M., Rutherford, A., & Foerster, J. N. (2025). Multi-Agent Craftax: Benchmarking open-ended multi-agent reinforcement learning at the hyperscale. arXiv:2511.04904."
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: [gh-baselomari-ma-craftax]
---

## Summary

Extends the JAX open-ended survival and crafting environment Craftax to multiple agents (Craftax-MA, same mechanics, supports an unbounded number of agents) and introduces Craftax-Coop with three specialised roles (Miner, Forager, Warrior), resource trading at any distance via broadcast requests, friendly fire and revival of dead teammates, all under shared reward. On one L40S GPU, IPPO training with 4 agents in Craftax-MA covers 250 million environment steps in 57 minutes, and 3-agent Craftax-Coop in 52 minutes. Baselines (MAPPO, IPPO, PQN) struggle with long-horizon credit assignment, exploration and cooperation.

## Contribution

Argues existing MARL benchmarks (SMAC, Hanabi) are short-horizon and narrow, and supplies a long-horizon open-ended multi-agent benchmark at accelerator speed that plugs into the JaxMARL interface [[gh-bold-lab-ai-jaxmarl]].

## Key results

- Throughput scales nearly log-log linearly with parallel environments; adding agents monotonically lowers throughput (figure 2, 2/4/8 agents).
- 250M steps in under an hour on a single L40S for both variants.
- Comparisons of shared versus individual rewards as agent count grows (figure 3) show degraded MAPPO performance with more agents (direction read from figure caption; magnitudes not transcribed).

## Methods and models

Dec-POMDP with shared reward; dead agents' actions replaced with no-ops; symbolic observations extended for heterogeneous agents; requests broadcast to all agents for 10 timesteps.

## Limitations and open questions

Fully cooperative shared-reward only, so no defection incentive. Skimmed. A different environment with the same name, "Multi-Agent Craftax (MAC)" by Ye, Tao and Jaques (arXiv 2508.15679), studies self-interested social learning; do not conflate.

## Relevance to us

Fast JAX open-ended world with trading; to use it for Sybil or defector work we would need to switch to individual rewards and add an exploitable trade channel.

## Notes from dmarz/factory-scan

For the planned swarm-factory environment (Factorio-like production feeding Cournot markets): Shows how to bolt trading and specialisation onto a crafting world cheaply. For our factory we want the opposite incentive (individual profit in shared markets) and emergent rather than assigned specialisation, which is the market-division signature measured in [[lin-2024-strategic]]. Could serve as an RL baseline substrate next to [[hopkins-2025-factorio]].
